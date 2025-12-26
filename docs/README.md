# CareOs

Saffron’s mission is to improve women’s healthcare everywhere.

Our vision is to partner with healthcare providers, payers, and patients to orchestrate care, using menopause as the front door. We call this vision Saffron’s CareOs.

We plan to achieve this vision by:

1. Establishing a low‑overhead, scalable data infrastructure that allows us to integrate seamlessly with providers’ claims and EHR data (CareOs-Infra).

2. Identifying women who may be missing a diagnosis or appropriate treatment for perimenopause or menopause using clinically-driven machine learning (CareOs-ML).

3. Recommending a clinically-validated care‑management plan that providers can implement (CareOs-CDS).

4. Implementing a flexible business model that allows us to serve women managed through both value‑based care and fee‑for‑service clinic (CareOs-Contract).

We believe this strategy will: 
1. Improve the quality of life for women experiencing severe menopause and perimenopause.
2. Reduce short‑term healthcare costs by preventing unnecessary utilization.
3. Reduce long‑term healthcare costs by supporting preventive measures for chronic conditions.
4. Decrease administrative burden for providers while enabling more comprehensive care for women in their clinics.

# CareOs-ML


## Project Structure

```
CareOSML/
├── src/careosml/       # Main package source code
├── tests/              # Unit and integration tests
├── notebooks/          # Jupyter notebooks for exploration
├── data/
│   ├── raw/           # Raw, immutable data
│   ├── processed/     # Cleaned and processed data
│   └── external/      # External data sources
├── models/            # Trained model artifacts
├── configs/           # Configuration files
└── scripts/           # Utility scripts
```

## Installation

```bash
# Install dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate
```

## Development

```bash
# Run tests
pytest

# Launch Jupyter
jupyter notebook
```

## Dependencies

- pandas: Data manipulation and analysis
- numpy: Numerical computing
- scikit-learn: Machine learning algorithms
- matplotlib: Data visualization
- jupyter: Interactive notebooks
- pytest: Testing framework
