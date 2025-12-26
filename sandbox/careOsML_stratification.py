import pymc as pm
import numpy as np
import numpy.ma as ma
import arviz as az
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification

# ==========================================
# STEP 1: Generate Data using sklearn
# ==========================================
print("Generating synthetic data...")

# Generate a dataset with 2 features
# n_samples=150: We will split this into 120 Labeled and 30 Unlabeled
X, y = make_classification(
    n_samples=150,
    n_features=2,
    n_informative=2,
    n_redundant=0,
    n_clusters_per_class=1,
    flip_y=0.1,        # Add some noise/error to the labels
    class_sep=0.8,     # Separation between classes
    random_state=42
)

# Split into Labeled and Unlabeled sets
n_unlabeled = 30

# Labeled Data (The first 120 patients)
X_labeled = X[:-n_unlabeled]
y_labeled = y[:-n_unlabeled]

# Unlabeled Data (The last 30 patients - we hide their 'y')
X_unlabeled = X[-n_unlabeled:]
y_true_unlabeled = y[-n_unlabeled:]  # Keep true labels for evaluation

# Combine Features for the model
X_combined = np.vstack([X_labeled, X_unlabeled])

# Create Masked Target Array for Semi-Supervised Learning
# Mask is False for observed data, True for missing data
y_mask = np.concatenate([
    np.zeros(len(y_labeled), dtype=bool),  # Observed
    np.ones(n_unlabeled, dtype=bool)       # Missing/Unlabeled
])

# Create the masked array.
# We pad the y values with zeros for the masked part (values ignored by PyMC anyway)
y_combined_data = np.concatenate([y_labeled, np.zeros(n_unlabeled)])
y_combined = ma.masked_array(y_combined_data, mask=y_mask)

print(f"Labeled samples: {len(X_labeled)}")
print(f"Unlabeled samples: {len(X_unlabeled)}")

# ==========================================
# STEP 2: PyMC Model Construction
# ==========================================
print("\nBuilding PyMC model...")

with pm.Model() as model:
    # --- Data Containers ---
    # Passing X as Data allows for potential future shape changes or prediction workflows
    X_data = pm.Data("X_data", X_combined)

    # --- Component A: Platt Scaling (Calibrating Scores) ---
    # We learn separate scaling parameters for each of the 2 features.
    # Constraint: Slopes (a) must be positive (HalfNormal) to enforce monotonicity.
    a = pm.HalfNormal("scale_slope", sigma=1, shape=2)
    b = pm.Normal("scale_bias", mu=0, sigma=1, shape=2)

    # Apply sigmoid to get calibrated probabilities 'q' for each score column
    # q shape: (n_samples, 2)
    q = pm.math.sigmoid(a * X_data + b)

    # --- Component B: Dirichlet Aggregation (Ensemble Weighting) ---
    # We learn weights 'w' that sum to 1 to combine the two calibrated scores.
    # alpha=1 implies a uniform prior (no initial preference for feature 1 vs 2)
    w = pm.Dirichlet("weights", a=np.ones(2))

    # --- Component C: Final Probability P ---
    # Weighted sum: P = w[0]*q[:,0] + w[1]*q[:,1]
    p = pm.Deterministic("p", pm.math.dot(q, w))

    # --- Likelihood (Semi-Supervised) ---
    # PyMC handles the masked values in y_combined automatically,
    # treating them as parameters to be imputed.
    obs = pm.Bernoulli("y", p=p, observed=y_combined)

    # --- Inference ---
    print("Sampling from posterior...")
    trace = pm.sample(1000, tune=1000, target_accept=0.95, random_seed=42, return_inferencedata=True)

# ==========================================
# STEP 3: Model Diagnostics
# ==========================================
print("\n" + "="*60)
print("POSTERIOR SUMMARY")
print("="*60)

# Summary of key parameters
summary = az.summary(trace, var_names=["scale_slope", "scale_bias", "weights"])
print(summary)

# ==========================================
# STEP 4: Predictions for Unlabeled Data
# ==========================================
print("\n" + "="*60)
print("PREDICTIONS FOR UNLABELED DATA")
print("="*60)

# Extract posterior probabilities for the Unlabeled patients
# The variable 'p' contains predictions for ALL patients.
posterior_p = trace.posterior["p"].values  # Shape: (chains, draws, n_total)
unlabeled_posterior = posterior_p[:, :, -n_unlabeled:]

# Calculate the mean risk (probability) for each unlabeled patient
p_mean = unlabeled_posterior.mean(axis=(0, 1))

# Predicted class (threshold=0.5)
y_pred_class = (p_mean > 0.5).astype(int)

print(f"\nPredicted probabilities (first 10): {p_mean[:10]}")
print(f"Predicted classes (first 10): {y_pred_class[:10]}")
print(f"True classes (first 10): {y_true_unlabeled[:10]}")

# Accuracy
accuracy = (y_pred_class == y_true_unlabeled).mean()
print(f"\nAccuracy on unlabeled data (threshold=0.5): {accuracy:.2%}")

# ==========================================
# STEP 5: Cost-Sensitive Analysis
# ==========================================
print("\n" + "="*60)
print("COST-SENSITIVE DECISION ANALYSIS")
print("="*60)

# Define Costs
# Scenario: Missing a sick patient (False Negative) is 10x costlier than a False Alarm.
COST_FN = 10  # Cost of False Negative
COST_FP = 1   # Cost of False Positive

# Calculate Expected Loss for each decision
# Loss if we TREAT = Prob(Healthy) * Cost_FP
loss_treat = (1 - p_mean) * COST_FP

# Loss if we DON'T TREAT = Prob(Sick) * Cost_FN
loss_no_treat = p_mean * COST_FN

# Make Decisions (Minimize Loss)
decisions = loss_treat < loss_no_treat

# Calculate Optimal Threshold (for reference)
optimal_threshold = COST_FP / (COST_FP + COST_FN)

print(f"\nOptimal Probability Threshold: {optimal_threshold:.2f}")
print("-" * 60)
print(f"{'Patient ID':<12} | {'Risk (p)':<10} | {'Decision':<12} | {'Exp. Loss':<10}")
print("-" * 60)

for i in range(5):  # Show first 5 unlabeled patients as example
    action = "TREAT" if decisions[i] else "Dismiss"
    loss = min(loss_treat[i], loss_no_treat[i])
    print(f"Unknown_{i:<4} | {p_mean[i]:.3f}      | {action:<12} | {loss:.3f}")

# Cost-sensitive accuracy
y_pred_cost_sensitive = decisions.astype(int)
cost_sensitive_accuracy = (y_pred_cost_sensitive == y_true_unlabeled).mean()
print(f"\nAccuracy with cost-sensitive threshold ({optimal_threshold:.2f}): {cost_sensitive_accuracy:.2%}")

# Feature Importance
print("\nFeature Importance (Dirichlet Weights):")
weights_mean = trace.posterior["weights"].mean(dim=["chain", "draw"]).values
print(f"Feature 1 Weight: {weights_mean[0]:.3f}")
print(f"Feature 2 Weight: {weights_mean[1]:.3f}")

# ==========================================
# STEP 6: Comprehensive Visualization
# ==========================================
print("\nGenerating comprehensive visualizations...")

# Create main figure with 6 subplots
fig = plt.figure(figsize=(16, 12))
gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)

# Plot 1: Data visualization
ax1 = fig.add_subplot(gs[0, 0])
ax1.scatter(X_labeled[y_labeled==0, 0], X_labeled[y_labeled==0, 1],
            c='blue', alpha=0.6, label='Labeled Class 0', marker='o')
ax1.scatter(X_labeled[y_labeled==1, 0], X_labeled[y_labeled==1, 1],
            c='red', alpha=0.6, label='Labeled Class 1', marker='o')
ax1.scatter(X_unlabeled[:, 0], X_unlabeled[:, 1],
            c='gray', alpha=0.8, label='Unlabeled', marker='x', s=100)
ax1.set_xlabel('Feature 1')
ax1.set_ylabel('Feature 2')
ax1.set_title('Semi-Supervised Classification Data')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot 2: Posterior of ensemble weights
ax2 = fig.add_subplot(gs[0, 1])
w_samples = trace.posterior["weights"].values.reshape(-1, 2)
ax2.hist(w_samples[:, 0], bins=30, alpha=0.7, label='Feature 1 Weight', color='steelblue')
ax2.hist(w_samples[:, 1], bins=30, alpha=0.7, label='Feature 2 Weight', color='coral')
ax2.axvline(weights_mean[0], color='steelblue', linestyle='--', linewidth=2)
ax2.axvline(weights_mean[1], color='coral', linestyle='--', linewidth=2)
ax2.set_xlabel('Weight Value')
ax2.set_ylabel('Frequency')
ax2.set_title('Posterior: Ensemble Weights (Dirichlet)')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Plot 3: Posterior of scale slopes
ax3 = fig.add_subplot(gs[1, 0])
slope_samples = trace.posterior["scale_slope"].values.reshape(-1, 2)
ax3.hist(slope_samples[:, 0], bins=30, alpha=0.7, label='Feature 1 Slope', color='steelblue')
ax3.hist(slope_samples[:, 1], bins=30, alpha=0.7, label='Feature 2 Slope', color='coral')
ax3.set_xlabel('Slope Value')
ax3.set_ylabel('Frequency')
ax3.set_title('Posterior: Platt Scale Slopes')
ax3.legend()
ax3.grid(True, alpha=0.3)

# Plot 4: Parameter estimates
ax4 = fig.add_subplot(gs[1, 1])
param_names = ['slope[0]', 'slope[1]', 'bias[0]', 'bias[1]', 'weight[0]', 'weight[1]']
param_values = [
    trace.posterior["scale_slope"].sel(scale_slope_dim_0=0).mean().values,
    trace.posterior["scale_slope"].sel(scale_slope_dim_0=1).mean().values,
    trace.posterior["scale_bias"].sel(scale_bias_dim_0=0).mean().values,
    trace.posterior["scale_bias"].sel(scale_bias_dim_0=1).mean().values,
    trace.posterior["weights"].sel(weights_dim_0=0).mean().values,
    trace.posterior["weights"].sel(weights_dim_0=1).mean().values
]
colors = ['steelblue', 'coral', 'steelblue', 'coral', 'seagreen', 'seagreen']
ax4.barh(param_names, param_values, color=colors, alpha=0.7)
ax4.set_xlabel('Posterior Mean')
ax4.set_title('Parameter Estimates')
ax4.grid(True, alpha=0.3, axis='x')

# Plot 5: Cost-Sensitive Decision Boundary
ax5 = fig.add_subplot(gs[2, 0])
probs = np.linspace(0, 1, 100)
l_treat = (1 - probs) * COST_FP
l_no_treat = probs * COST_FN
ax5.plot(probs, l_treat, label='Cost if Treated', color='green', linewidth=2)
ax5.plot(probs, l_no_treat, label='Cost if Not Treated', color='red', linewidth=2)
ax5.axvline(optimal_threshold, linestyle='--', color='black', linewidth=2, label='Optimal Threshold')
# Plot a few patient examples
for i in range(min(5, len(p_mean))):
    ax5.scatter([p_mean[i]], [min(loss_treat[i], loss_no_treat[i])],
                color='blue', zorder=5, alpha=0.6, s=50)
ax5.set_xlabel('Probability of Class 1 (p)')
ax5.set_ylabel('Expected Cost')
ax5.set_title(f'Cost-Sensitive Decision Boundary (Threshold = {optimal_threshold:.2f})')
ax5.legend()
ax5.grid(True, alpha=0.3)

# Plot 6: Prediction Performance
ax6 = fig.add_subplot(gs[2, 1])
metrics = ['Standard\n(threshold=0.5)', f'Cost-Sensitive\n(threshold={optimal_threshold:.2f})']
accuracies = [accuracy, cost_sensitive_accuracy]
bars = ax6.bar(metrics, accuracies, color=['steelblue', 'coral'], alpha=0.7, width=0.6)
ax6.set_ylabel('Accuracy')
ax6.set_ylim([0, 1])
ax6.set_title('Prediction Performance on Unlabeled Data')
ax6.grid(True, alpha=0.3, axis='y')
# Add value labels on bars
for bar, acc in zip(bars, accuracies):
    height = bar.get_height()
    ax6.text(bar.get_x() + bar.get_width()/2., height,
             f'{acc:.2%}', ha='center', va='bottom', fontweight='bold')

plt.suptitle('Unified Semi-Supervised Learning with Cost-Sensitive Analysis',
             fontsize=14, fontweight='bold', y=0.995)

# Additional trace plot
print("\nGenerating trace plots...")
fig2 = plt.figure(figsize=(12, 8))
az.plot_trace(trace, var_names=["scale_slope", "scale_bias", "weights"])
plt.tight_layout()

print("\nDisplaying visualizations...")
plt.show()

print("\nDone! All analysis complete.")
