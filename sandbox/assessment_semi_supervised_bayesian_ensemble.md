# Assessment: Semi-Supervised Bayesian Ensemble with Learned Calibration

## Executive Summary

This document evaluates a novel machine learning architecture that integrates three methodological streams—semi-supervised learning, Bayesian calibration via Platt scaling, and adaptive ensemble weighting—within a unified probabilistic framework. While each component exists independently in the literature, their synthesis into a single generative model represents a meaningful contribution to healthcare predictive analytics, particularly for settings where labeled outcomes are scarce and calibrated uncertainty estimates are clinically essential.

---

## 1. Assessment of Innovation

### 1.1 Methodological Synthesis

The proposed approach combines the following elements into a cohesive probabilistic model:

| Component | Traditional Implementation | This Approach |
|-----------|---------------------------|---------------|
| Semi-supervised learning | EM algorithms, pseudo-labeling, self-training | Latent variable imputation via MCMC with full posterior inference |
| Platt scaling | Post-hoc logistic regression on held-out calibration set | Jointly learned calibration parameters with monotonicity constraints |
| Ensemble weighting | Fixed weights, stacking with cross-validation | Bayesian Beta priors yielding data-driven weight posteriors |
| Uncertainty quantification | Separate calibration step or conformal prediction | Intrinsic to the generative model across all components |

The key innovation lies not in any single component but in the joint inference architecture. Traditional pipelines treat calibration and ensembling as sequential post-processing steps. Here, calibration parameters, ensemble weights, and latent labels are inferred simultaneously, allowing information to flow bidirectionally between components during training.

#### Modular Pipelines: Unidirectional Information Flow

In a traditional approach, stages execute sequentially:

```
Step 1: Train classifier → raw scores
Step 2: Platt scaling on held-out set → calibrated probabilities  
Step 3: Learn ensemble weights via stacking → final predictions
```

Information flows in one direction only. The calibration parameters learned in Step 2 have no way to influence what happened in Step 1. The ensemble weights in Step 3 cannot reach back and adjust the calibration. Each stage is frozen before the next begins.

#### Joint Bayesian Model: Bidirectional Information Flow

In the proposed PyMC model, all parameters are inferred simultaneously within the same MCMC sampling process. At each iteration, the sampler proposes new values for:

- Calibration slopes (a) and biases (b)
- Ensemble weights (w)
- Latent labels for unlabeled patients (y_obs_unobserved)

The acceptance probability for a proposed calibration slope depends on how well it explains *both* the labeled data *and* the current imputed labels for unlabeled data. Simultaneously, the imputed labels depend on the current calibration and weighting. Everything conditions on everything else.

#### Concrete Example from Demonstrated Results

The model learned that Feature 1 deserves higher ensemble weight (0.65 vs. 0.25). In a modular pipeline, this inference would require labeled data exclusively. In the semi-supervised formulation, the 30 unlabeled patients contributed to this inference—their imputed labels, combined with how well each calibrated feature predicted those imputations, jointly informed the weight posterior.

If calibration had been performed separately on just the 120 labeled patients, with parameters frozen before learning weights, this feedback loop would be lost. The unlabeled data would never influence calibration quality assessment.

This is the bidirectional flow: latent labels ↔ calibration ↔ weights, all updating together within a single inferential framework.

### 1.2 Novel Contributions

**Unified Generative Model.** By expressing the entire pipeline as a directed graphical model, the approach enables coherent uncertainty propagation. Posterior uncertainty in calibration slopes influences ensemble weight inference, which in turn affects latent label imputation. This interdependence is lost in modular pipelines.

**Constrained Calibration.** The use of HalfNormal priors on Platt scaling slopes enforces monotonicity—a critical property ensuring that higher raw scores always map to higher predicted probabilities. This constraint is often violated in small-sample regimes when calibration is performed post-hoc.

**Adaptive Feature Trust.** The Beta-distributed ensemble weights provide an interpretable measure of feature informativeness. In the demonstrated results, the model correctly identified Feature 1 as more discriminative (weight ≈ 0.65 vs. 0.25), a finding that emerged naturally from the data rather than requiring manual feature selection.

**Label-Efficient Learning.** The semi-supervised formulation leverages unlabeled observations to regularize parameter estimates. This is particularly valuable in healthcare contexts where chart review or adjudication for gold-standard labels is expensive.

### 1.3 Positioning Relative to Existing Literature

Semi-supervised deep learning methods (e.g., MixMatch, FixMatch) dominate recent literature but sacrifice interpretability and calibration quality. Gaussian process classifiers offer principled uncertainty but scale poorly. The proposed approach occupies a useful middle ground: interpretable parametric structure, rigorous uncertainty quantification, and compatibility with domain constraints common in clinical applications.

To our knowledge, the specific combination of masked-array semi-supervised inference, Bayesian Platt scaling with monotonicity constraints, and learned ensemble weights within a single PyMC model has not been previously described in the healthcare ML literature.

---

## 2. Scalability Assessment

### 2.1 Current Computational Profile

The reference implementation exhibits the following characteristics at N = 150 observations:

| Metric | Observed Value |
|--------|----------------|
| Sampling time | ~11 seconds (2 chains × 2,000 iterations) |
| Sampler | NUTS for continuous parameters; BinaryGibbsMetropolis for latent labels |
| Memory footprint | Modest (full data in memory) |
| Convergence diagnostics | R-hat = 1.0, ESS > 900 for all parameters |

### 2.2 Scaling Considerations

Extending this approach to one million patients introduces computational considerations that are addressable with appropriate tooling:

**Consideration 1: MCMC Iteration Cost.** Each NUTS iteration requires gradient evaluation across all observations. Computational complexity scales as O(N × P × D) per iteration, where N is sample size, P is the number of parameters, and D is the cost of gradient computation. At N = 10^6, GPU acceleration becomes valuable but not strictly required.

**Consideration 2: Discrete Latent Variables.** The BinaryGibbsMetropolis sampler for unobserved labels scales linearly with the number of unlabeled observations. Mixing efficiency depends on the ratio of unlabeled to labeled data; with reasonable labeling rates (>10%), convergence remains tractable.

**Consideration 3: Memory Requirements.** The implementation must hold the design matrix and posterior samples in memory. At N = 10^6 with modest feature dimensionality, this requires 10-50 GB RAM—readily available on cloud GPU instances (e.g., AWS p3.2xlarge provides 61 GB RAM, GCP n1-highmem instances scale to 624 GB).

### 2.3 Implementation Options

Several techniques can optimize this architecture for production inference at N ≤ 1,000,000:

**Pathway A: Variational Inference (For Development Iteration).**  
Replace MCMC with stochastic variational inference (SVI) using mini-batches during model development phases. PyMC supports ADVI (Automatic Differentiation Variational Inference), which approximates the posterior with a factorized Gaussian. This reduces per-run time to 5-10 minutes, enabling rapid hyperparameter tuning and feature engineering before committing to full MCMC for production runs.

| Aspect | MCMC (Production) | Variational Inference (Development) |
|--------|-------------------|-------------------------------------|
| Runtime at N=10^6 | 30-90 minutes | 5-10 minutes |
| Posterior quality | Exact (asymptotically) | Approximate |
| Discrete latents | Gibbs sampling | Continuous relaxation |
| Use case | Daily/3x-weekly production | Rapid iteration during development |

**Pathway B: JAX/NumPyro Backend with Cloud GPU (Recommended).**  
Migrating the model to NumPyro enables GPU acceleration and JIT compilation. Empirical benchmarks suggest 10-100× speedups for models of this complexity. NumPyro's enumeration strategy can also marginalize discrete latents exactly when cardinality is manageable.

Recommended cloud GPU instances:
- AWS: p3.2xlarge (V100, 16GB VRAM) or g5.xlarge (A10G, 24GB VRAM)
- GCP: n1-standard-8 with T4 or V100
- Azure: NC6s_v3 (V100)

Spot/preemptible pricing reduces costs by 60-70% compared to on-demand.

**Pathway C: Warm-Starting for Faster Convergence.**  
With daily or thrice-weekly runs, consecutive estimations share substantial overlap in both data and posterior structure. Warm-starting MCMC from the previous day's posterior can reduce required tuning iterations:

1. Save posterior samples from each run.
2. Initialize next run's chains from previous posterior means.
3. Reduce tuning steps from 1,000 to 200-500.
4. Expected runtime reduction: 20-40%.

This optimization is particularly effective when underlying data changes incrementally between runs.

**Pathway D: Sparse Gaussian Process Approximations.**  
If the calibration component is extended to nonparametric Platt scaling (e.g., GP-based isotonic regression), inducing point methods (SVGP, FITC) reduce complexity from O(N³) to O(N × M²), where M << N is the number of inducing points.

### 2.4 Recommended Scalability Architecture

For production deployment at the target scale (N ≤ 1,000,000 patients) with cloud infrastructure and daily or thrice-weekly estimation cycles, full Bayesian inference remains tractable. The architecture below optimizes for operational efficiency and cost management.

**Primary Recommendation: NumPyro + Cloud GPU**

For populations up to one million patients with frequent retraining, NumPyro with cloud GPU acceleration provides the optimal balance of posterior quality, computational efficiency, and operational cost.

```
┌─────────────────────────────────────────────────────────────────┐
│                    CLOUD INFRASTRUCTURE                         │
├─────────────────────────────────────────────────────────────────┤
│  Compute: GPU instance (e.g., AWS p3.2xlarge, GCP n1-standard   │
│           with T4/V100, Azure NC-series)                        │
│  Storage: Cloud object storage for data and model artifacts     │
│  Orchestration: Airflow, Prefect, or cloud-native scheduler     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    INFERENCE PIPELINE (Daily/3x Weekly)         │
├─────────────────────────────────────────────────────────────────┤
│  1. Scheduled trigger: cron or event-driven                     │
│  2. Spin up GPU instance (spot/preemptible for cost savings)    │
│  3. Data pull: feature matrix + masked label array from warehouse│
│  4. NumPyro model with JAX backend (GPU-accelerated)            │
│  5. NUTS sampling: 4 chains × 2,000 iterations                  │
│  6. Expected runtime: 30-90 minutes at N = 1,000,000            │
│  7. Export: posterior summaries + predictions to storage        │
│  8. Terminate instance                                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   SCORING & DELIVERY                            │
├─────────────────────────────────────────────────────────────────┤
│  Option A: Batch predictions (typical for daily refresh)        │
│    - Write scored patient list to data warehouse                │
│    - Downstream dashboards/EHR integrations pull from warehouse │
│                                                                 │
│  Option B: On-demand scoring API (if real-time needs arise)     │
│    - Lightweight service using posterior means                  │
│    - Decoupled from training pipeline                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   MONITORING & ALERTING                         │
├─────────────────────────────────────────────────────────────────┤
│  1. Convergence checks: R-hat, ESS, divergences per run         │
│  2. Calibration tracking: Brier score, reliability diagrams     │
│  3. Drift detection: parameter shift relative to moving average │
│  4. Alerting: notify on convergence failure or calibration drift│
└─────────────────────────────────────────────────────────────────┘
```

**Cost Optimization Strategies**

| Strategy | Description | Estimated Savings |
|----------|-------------|-------------------|
| Spot/Preemptible instances | Use interruptible GPU instances for training | 60-70% vs on-demand |
| Right-sizing | Match instance to workload (V100 vs A100) | Variable |
| Auto-termination | Shut down immediately after pipeline completion | Avoid idle costs |
| Checkpointing | Save MCMC state to resume if interrupted | Enables spot usage |

At daily frequency with spot pricing, estimated monthly cloud compute cost for the training pipeline is $150-400 depending on provider and instance selection.

**Alternative: Variational Inference for Faster Iteration**

If operational requirements shift to multiple runs per day or near-real-time updates, SVI with mini-batches reduces training time to 5-10 minutes at the cost of approximate posteriors. This provides a natural escalation path without architectural changes.

### 2.5 Scalability Summary

| Scale | Infrastructure | Approach | Runtime per Run |
|-------|---------------|----------|-----------------|
| N < 10,000 | Any | Full MCMC via PyMC | Minutes |
| 10,000 < N < 100,000 | Cloud GPU | NumPyro + NUTS | 5-15 minutes |
| 100,000 < N ≤ 1,000,000 | Cloud GPU | NumPyro + NUTS | 30-90 minutes |

**Operational Feasibility at Target Frequency**

| Frequency | Runs/Month | Est. GPU Hours/Month | Monthly Cost (Spot) |
|-----------|------------|----------------------|---------------------|
| Daily | 30 | 15-45 | $150-400 |
| 3x Weekly | 12-13 | 6-20 | $60-175 |

At the target scale and frequency, full Bayesian inference with exact MCMC remains operationally and economically viable using cloud GPU resources.

---

## 3. Conclusions

### 3.1 Innovation Assessment

The proposed semi-supervised Bayesian ensemble with learned calibration represents a genuine methodological contribution. Its value lies in the principled integration of components that are typically treated in isolation, yielding a model that is simultaneously label-efficient, well-calibrated, uncertainty-aware, and interpretable. These properties align well with the requirements of clinical decision support, where trust and transparency are paramount.

### 3.2 Scalability Assessment

The current PyMC implementation is appropriate for research and pilot studies. For the target production scale of up to one million patients with daily or thrice-weekly estimation cycles, full Bayesian inference remains tractable using cloud GPU resources. Expected runtime of 30-90 minutes per run and estimated monthly costs of $150-400 (daily) or $60-175 (3x weekly) using spot instances place this approach well within operational feasibility. The transition path is straightforward: porting the model to NumPyro and deploying to cloud infrastructure preserves exact posterior inference while meeting the required estimation frequency.

### 3.3 Recommendations

1. **Short-term:** Validate the approach on a labeled clinical cohort (e.g., chart-reviewed HCC conditions) to establish empirical calibration quality relative to standard approaches.

2. **Medium-term:** Port the model to NumPyro and deploy to cloud infrastructure. Benchmark GPU-accelerated MCMC at increasing sample sizes (N = 10K, 100K, 500K, 1M) to establish runtime curves and validate cost estimates.

3. **Long-term:** Operationalize the pipeline with:
   - Automated daily/3x-weekly scheduling via workflow orchestrator
   - Spot instance usage with checkpointing for cost efficiency
   - Convergence and calibration monitoring with alerting
   - Integration with downstream clinical decision support systems

---

*Document prepared for internal technical review.*
