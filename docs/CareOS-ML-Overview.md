# CareOS-ML Overview

*Proprietary + Confidential*

---

## Mission and Vision

**Saffron's mission is to improve women's healthcare everywhere.**

Our vision is to partner with healthcare providers, payers, and patients to orchestrate care, using menopause as the front door. We call this vision **Saffron's CareOs**.

### Strategic Pillars

We plan to achieve this vision by:

1. **CareOs-Infra**: Establishing a low-overhead, scalable data infrastructure that allows us to integrate seamlessly with providers' claims and EHR data.

2. **CareOs-ML**: Identifying women who may be missing a diagnosis or appropriate treatment for perimenopause or menopause using clinically-driven machine learning.

3. **CareOs-NAV**: Recommending a clinically-validated care-management plan that providers can implement and help women navigate menopause-related symptoms.

4. **CareOs-Contract**: Implementing a flexible business model that allows us to serve women managed through both value-based care and fee-for-service clinic.

---

## Benefits

We believe this strategy will:

1. **Improve the quality of life** for women experiencing severe menopause and perimenopause.

2. **Reduce short-term healthcare costs** by preventing unnecessary utilization.

3. **Reduce long-term healthcare costs** by supporting preventive measures for chronic conditions.

4. **Decrease administrative burden** for providers while enabling more comprehensive care for women in their clinics.

---

## CareOS-Infra

### Data Architecture

**Golden Data Sources:**
- EHR (Private, Public, Synthetic)
- Claims Data (Private, Public, Synthetic)
- Customer Data (ad hoc)

**Data Normalization:**
- Normalize Golden Data Set
- Normalize Ad Hoc Customer Data

**Data Products:**

1. **Patient Event Stream**
   - Trace in time
   - Dense
   - Fixed for each model

2. **Patient Snapshot**
   - Fixed period
   - Dense / sparse
   - Varies per clinic

Both data products feed into **CareOS-ML** for analysis and predictions.

---

## CareOS ML/AI

### Clinical Guidance System

The system provides **Recommended Actions Based on Posterior Distribution** with different confidence levels:

#### Patient A Profile (HIGH CONFIDENCE)
**Risk Score: 80% ± 5%**

**Indicators:**
- Clear vasomotor symptom documentation
- Consistent sleep/mood complaint pattern
- Age-appropriate lab values available

**Recommended Actions:**
- → Prioritize for provider outreach
- → Review for HRT candidacy assessment
- → Consider formal diagnosis documentation
- → Evaluate for guideline-based management

#### Patient B Profile (LOW CONFIDENCE)
**Risk Score: 80% ± 22.5%**

**Indicators:**
- Sparse clinical documentation
- Symptoms overlap with other conditions
- Missing confirmatory lab results

**Recommended Actions:**
- → Defer outreach pending more data
- → Flag for symptom tracking at next visit
- → Order FSH/estradiol if not recent
- → Re-score after records update

---

## CareOS ML/AI: How Does It Work?

### 1. Foundation Models

We train our models on **Saffron's Golden Data Set** (≥200,000 women with linked claims and EHR data), learning generalizable patterns for perimenopause and menopause detection across diverse populations and care settings.

We then incorporate each **partner's local data** (<20,000 women is sufficient) to adjust for site-specific:
- Documentation practices
- Coding conventions
- Patient demographics
- Care patterns

### 2. Learning from Incomplete Labels

**The Challenge:**
Traditional models require confirmed diagnoses for training. In perimenopause, this creates circularity—the undocumented cases are excluded from model development.

**Our Solution:**
Our approach learns jointly from:
- Patients with **confirmed diagnoses** (labeled data)
- Patients with **suggestive patterns but no formal documentation** (unlabeled data)

The model identifies which combinations of symptoms, medications, labs, and utilization patterns predict the condition **regardless of whether it was coded**.

### 3. Quantifying Uncertainty

**The Problem:**
Most models produce single-number predictions: "78% probability of undiagnosed perimenopause." But clinical utility depends on knowing whether that estimate is reliable.

**Our Approach:**
Two patients scored at 78% may have very different underlying certainty:
- One with **rich documentation and clear symptom patterns**
- Another with **sparse records and ambiguous presentation**

Our model distinguishes these cases, providing **uncertainty ranges that inform clinical prioritization**.

### The Calibrated Uncertainty Advantage

**Same probability score, different clinical decisions**

| **Patient A (High Confidence)** | **Patient B (Low Confidence)** |
|--------------------------------|-------------------------------|
| **80%** probability score | **80%** probability score |
| 95% CI: 75-85% | 95% CI: 50-95% |
| ✓ Clear symptom pattern | ⚠ Sparse records |
| ✓ Rich documentation | ⚠ Ambiguous presentation |
| ✓ Consistent indicators | ⚠ Mixed signals |
| **→ Prioritize for outreach** | **→ Defer, gather more info** |

#### Why This Matters

**Without Uncertainty:**
- Both patients appear identical
- Resources wasted on low-yield cases
- Provider trust erodes over time
- No basis for prioritization

**With CareOS-ML:**
- Confidence maps to real-world accuracy
- Clinical resources allocated appropriately
- Provider trust preserved
- Actionable decision thresholds

**Key differentiator:** When the model expresses high confidence, chart review confirms predictions at correspondingly high rates.

---

## Understanding Prediction Confidence

**Posterior probability distributions for perimenopause/menopause detection**

### Probability Distribution Visualization

The model outputs full posterior distributions showing:

- **Low Risk Zone** (0%-40%): Low probability of undiagnosed condition
- **Monitor Zone** (40%-60%): Moderate probability, continue observation
- **Action Recommended Zone** (60%-100%): High probability, clinical action warranted

**Patient A (High Confidence):**
- Point Estimate: 80%
- 95% CI: 75-85%
- Narrow distribution (green curve)
- High confidence in prediction

**Patient B (Low Confidence):**
- Point Estimate: 80%
- 95% CI: 50-95%
- Wide distribution (orange curve)
- Low confidence despite same point estimate

---

## CareOS ML/AI: Architecture

### Data Flow

#### Saffron's Data
**Golden Data Set**
- ≥200K women (claims and EHR)
- → Train ML model using **claims data**
- → Train ML model using **EHR data**

#### Client's Data
- ~20K women (EHR and Claims)
- Local calibration data

### Processing Pipeline

**Golden Data + Client Data** → **CareOS-ML** (Semi-Supervised Bayesian Ensemble) → **Selected patients for care management**

### Model Components

**Base Models**
- Trained on Saffron's Golden Dataset with linked claims and EHR
- Learning generalizable patterns across diverse populations

**Local Calibration**
- Client data adjusts for site-specific documentation practices, coding conventions, and patient demographics

**Actionable Output**
- Precision-optimized worklist of patients with:
  - Probability estimates
  - Confidence intervals
  - Contributing evidence

### Key Specifications
- **200K+** base training set
- **<20K** min. client data
- **Claims + EHR** fusion
- **Calibrated** uncertainty

---

## CareOS-ML: Deployment Model

CareOS-ML combines a **base model** trained on large datasets with **client-specific calibration**, producing predictions tuned to the characteristics of each clinic or health system.

Our approach enables partnerships with organizations that would otherwise lack sufficient data for standalone model development.

**Example:** A regional clinic with 5,000 eligible patients benefits from patterns learned across 200,000+ patients while still receiving predictions calibrated to their specific context.

---

## CareOS-Nav

*[Section title only - content to be developed]*

---

## Execution Plan

**Goal:** Prove outcomes in 6 months; ship v1, scale to 2k members by M12 to support Series A

### Timeline by Quarter

| **Workstream** | **M1-M3** | **M4-M6 (Pilot)** | **M7-M12 (Scale)** |
|----------------|-----------|-------------------|-------------------|
| **Hiring & Org** | Clinical Core, Data/ML Team | Pilot Window | Team Ramp-up & Training |
| **Platform Build** | Data Rails | ML Risk Engine v1, LLM Care Plan Composer v1 | v1.5, Light Workflow |
| **Clinical Operations** | Pilot Prep, Implementation | Pilot Run: 450 Members | Scale: 2,000 Members, Outcomes Readout & Member Expansion |
| **Go-to-Market** | - | Employer & Broker Roadshow | Pipeline Building → Series A |

### Key Milestones

1. **M1-M2:** Hire Clinical Core and Data/ML Team
2. **M2-M3:** Build Data Rails infrastructure
3. **M3-M6:** Develop ML Risk Engine v1
4. **M3-M9:** Build LLM Care Plan Composer v1
5. **M4-M6:** Run pilot with 450 members
6. **M6-M8:** Employer & Broker roadshow
7. **M7-M11:** Scale to 2,000 members
8. **M8-M9:** Team ramp-up & training
9. **M9-M12:** Build pipeline for Series A
10. **M10-M12:** Develop v1.5 and Light Workflow
11. **M12:** Series A fundraise

---

*Document Source: CareOS-ML.pdf*
*Converted to Markdown: 2025-12-26*
