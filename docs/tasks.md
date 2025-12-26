# Task Backlog

Tasks organized by priority and workstream, aligned with the 12-month execution plan.

---

## Immediate / High Priority

### Data Infrastructure (M1-M3: Data Rails)

- [ ] **Define data schemas**
  - [ ] Patient Event Stream schema (temporal)
  - [ ] Patient Snapshot schema (fixed period)
  - [ ] Claims data format specification
  - [ ] EHR data format specification
  - Technical owner: Data/ML Team

- [ ] **Data normalization pipeline**
  - [ ] Design ETL architecture
  - [ ] Implement claims data parser
  - [ ] Implement EHR data parser
  - [ ] Build data validation layer
  - Technical owner: Data/ML Team

- [ ] **Synthetic data generation**
  - [ ] Create realistic synthetic Golden Dataset (200K+ patients)
  - [ ] Create synthetic partner dataset (5-20K patients)
  - [ ] Ensure data includes: symptoms, medications, labs, utilization patterns
  - Technical owner: Data/ML Team

### ML Model Development (M3-M6: ML Risk Engine v1)

- [ ] **Production code structure**
  - [ ] Design package architecture for `src/careosml/`
  - [ ] Create module structure (data, models, features, evaluation, utils)
  - [ ] Set up logging and configuration management
  - Technical owner: Data/ML Team

- [ ] **Foundation model implementation**
  - [ ] Port sandbox POC to production code
  - [ ] Implement Platt scaling component
  - [ ] Implement Dirichlet aggregation component
  - [ ] Optimize PyMC sampling performance
  - Technical owner: Data/ML Team

- [ ] **Semi-supervised learning**
  - [ ] Implement masked array handling for unlabeled data
  - [ ] Validate imputation approach for missing labels
  - [ ] Test on synthetic data with varying labeled/unlabeled ratios
  - Technical owner: Data/ML Team

- [ ] **Uncertainty quantification**
  - [ ] Implement posterior distribution extraction
  - [ ] Calculate credible intervals (95% CI)
  - [ ] Create confidence calibration metrics
  - [ ] Validate that high confidence → high accuracy
  - Technical owner: Data/ML Team

- [ ] **Local calibration**
  - [ ] Design transfer learning approach for partner data
  - [ ] Implement site-specific adjustment layer
  - [ ] Test with simulated site differences (documentation styles, coding practices)
  - Technical owner: Data/ML Team

### Testing & Validation

- [ ] **Test infrastructure**
  - [ ] Set up pytest structure in `tests/`
  - [ ] Create fixtures for synthetic data
  - [ ] Implement integration tests for ML pipeline
  - Technical owner: Data/ML Team

- [ ] **Model evaluation**
  - [ ] Define evaluation metrics (accuracy, calibration, uncertainty quality)
  - [ ] Implement cost-sensitive evaluation
  - [ ] Create visualization tools for model performance
  - Technical owner: Data/ML Team

- [ ] **Clinical validation**
  - [ ] Define risk stratification thresholds (Low/Monitor/Action)
  - [ ] Validate decision rules with clinical team
  - [ ] Test on historical cases with known outcomes
  - Technical owner: Clinical Core + Data/ML Team

---

## Medium Priority

### Clinical Decision Support (M3-M9: LLM Care Plan Composer v1)

- [ ] **Risk stratification**
  - [ ] Implement patient profile classification (High/Low confidence)
  - [ ] Generate recommended actions based on posterior distribution
  - [ ] Create evidence summary for each prediction
  - Technical owner: Clinical Core + Data/ML Team

- [ ] **Worklist generation**
  - [ ] Sort patients by probability × confidence
  - [ ] Filter by actionability threshold
  - [ ] Generate precision-optimized output format
  - Technical owner: Clinical Core + Data/ML Team

- [ ] **LLM integration** (if applicable)
  - [ ] Design care plan generation prompts
  - [ ] Integrate with LLM API
  - [ ] Validate clinical accuracy of generated plans
  - Technical owner: Clinical Core

### Documentation

- [ ] **Technical documentation**
  - [ ] API documentation for `careosml` package
  - [ ] Model architecture documentation
  - [ ] Data pipeline documentation
  - Technical owner: Data/ML Team

- [ ] **Clinical documentation**
  - [ ] Clinical validation report
  - [ ] Risk stratification guidelines
  - [ ] Recommended actions playbook
  - Technical owner: Clinical Core

- [ ] **Standards**
  - [ ] Create `docs/standards/` directory
  - [ ] Define coding standards
  - [ ] Define testing standards
  - [ ] Define documentation standards
  - Technical owner: All

---

## Lower Priority / Future

### Platform (M7-M12: v1.5, Light Workflow)

- [ ] **Model versioning**
  - [ ] Implement model registry
  - [ ] Track model lineage and hyperparameters
  - [ ] A/B testing infrastructure

- [ ] **Monitoring**
  - [ ] Model performance monitoring
  - [ ] Data drift detection
  - [ ] Prediction confidence monitoring

- [ ] **Scalability**
  - [ ] Optimize inference latency
  - [ ] Batch prediction pipeline
  - [ ] Distributed training (if needed)

### Research / Exploration

- [ ] **Feature engineering**
  - [ ] Identify additional predictive features
  - [ ] Test temporal patterns (sequence modeling)
  - [ ] Explore medication interaction features

- [ ] **Model improvements**
  - [ ] Compare PyMC vs other Bayesian frameworks
  - [ ] Explore deep learning approaches
  - [ ] Investigate multi-task learning (peri vs menopause)

- [ ] **Clinical research**
  - [ ] Literature review on menopause detection
  - [ ] Analyze diagnostic criteria from NAMS, IMS
  - [ ] Consult with clinical experts on feature selection

---

## Blocked / Waiting

- [ ] **Golden Dataset access** - Need 200K+ patient records with linked claims + EHR
- [ ] **Partner identification** - Need pilot partner with 5-20K patients for local calibration
- [ ] **Clinical validation partner** - Need clinical team to validate risk thresholds
- [ ] **Infrastructure decisions** - Where will models run? Cloud provider? On-premise?

---

## Completed

- [x] Repository initialization
- [x] Basic project structure
- [x] Dependencies configuration (`pyproject.toml`)
- [x] Session guidelines (`CLAUDE.md`)
- [x] Sandbox POC (semi-supervised Bayesian approach)
- [x] Convert CareOS-ML PDF to markdown
- [x] Create documentation structure (`status.md`, `progress.md`, `tasks.md`)

---

## Notes

- Tasks aligned with 12-month execution plan from `docs/CareOS-ML-Overview.md`
- M1-M3 focus: Data Rails
- M3-M6 focus: ML Risk Engine v1
- M4-M6: Pilot with 450 members
- M7-M12: Scale to 2,000 members
- This backlog should be updated regularly as work progresses
- Use `docs/progress.md` to log completed work each session
