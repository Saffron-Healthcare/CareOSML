# CareOSML

Machine learning tools and models for healthcare applications.

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
