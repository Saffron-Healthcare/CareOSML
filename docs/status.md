# Project Status

**Last Updated:** 2025-12-26
**Branch:** `ideation`
**Phase:** Early Development / Proof of Concept

---

## Current State

### Repository Structure
- ✅ Basic ML project structure established
- ✅ Python package configured (`careosml`)
- ✅ Dependencies defined (pandas, numpy, scikit-learn, matplotlib, jupyter, pytest, **pymc**)
- ⚠️ Main branch not yet created
- ⚠️ Production code minimal (`src/careosml/` has only `__init__.py`)
- ⚠️ No tests written yet

### Documentation
- ✅ `docs/README.md` - Project overview
- ✅ `docs/CareOS-ML-Overview.md` - Converted from PDF, comprehensive ML strategy
- ✅ `CLAUDE.md` - Session guidelines and team preferences
- ✅ `docs/status.md` - This file (current state)
- ✅ `docs/progress.md` - Session notes
- ✅ `docs/tasks.md` - Task backlog

### Code/Implementation
- ✅ Sandbox POC: `sandbox/careOsML_stratification.py`
  - Semi-supervised Bayesian approach with PyMC
  - Platt scaling for probability calibration
  - Dirichlet aggregation for ensemble weighting
  - Cost-sensitive decision analysis
  - Comprehensive visualization
- ❌ No production implementation in `src/careosml/`
- ❌ No test coverage

### Uncommitted Changes
- Modified: `docs/README.md`
- Untracked: `sandbox/` directory
- Untracked: New documentation files (`status.md`, `progress.md`, `tasks.md`, `CareOS-ML-Overview.md`)

---

## Technical Architecture (Planned)

### ML Pipeline Components
Based on `docs/CareOS-ML-Overview.md`:

1. **Data Infrastructure (CareOS-Infra)**
   - Golden Data Set normalization (≥200K patients)
   - Partner/Client data normalization (<20K patients)
   - Patient Event Stream (temporal, dense)
   - Patient Snapshot (fixed period, varies by clinic)

2. **ML Model (CareOS-ML)**
   - Foundation models trained on Golden Dataset
   - Local calibration per partner site
   - Semi-supervised Bayesian ensemble
   - Calibrated uncertainty quantification
   - Output: Precision-optimized worklist with probabilities + confidence intervals

3. **Clinical Decision Support (CareOS-Nav)**
   - Risk stratification (Low/Monitor/Action zones)
   - Recommended actions based on posterior distribution
   - Cost-sensitive decision framework

---

## Execution Timeline (from Overview Doc)

**Current Position:** M1 (Month 1) - Early setup phase

**Immediate Goals (M1-M3):**
- Build Data Rails infrastructure
- Hire Clinical Core and Data/ML Team
- Prepare for pilot

**Near-term (M4-M6):**
- Complete ML Risk Engine v1
- Run pilot with 450 members
- Begin Employer & Broker roadshow

**Mid-term (M7-M12):**
- Scale to 2,000 members
- Develop v1.5 and Light Workflow
- Build pipeline for Series A

---

## Blockers / Questions

1. **Data Access:** Do we have access to Golden Dataset (200K+ patients) yet?
2. **Infrastructure:** Where will data normalization pipeline run?
3. **Model Training:** What compute resources available for PyMC Bayesian models?
4. **Clinical Validation:** Who will validate the risk stratification thresholds?
5. **Partner Data:** Do we have a pilot partner identified for local calibration (<20K patients)?

---

## Next Session Goals

Based on current state, potential next steps:
1. Commit current work to `ideation` branch
2. Review and refine sandbox POC approach
3. Start production code structure in `src/careosml/`
4. Define data schemas for Patient Event Stream and Patient Snapshot
5. Set up testing infrastructure
