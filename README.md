# 🛢️ Petrobras Offshore Wells Anomaly Detection

[![Python 3.11](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Linting: ruff](https://img.shields.io/badge/linting-ruff-red.svg)](https://github.com/astral-sh/ruff)

> **🇧🇷 [Ver documentação em Português Brasileiro](README.pt-BR.md)**

## 🎯 Project Overview

This is a PIBIC (Undergraduate Research) project focused on **anomaly detection in multivariate time series** from Petrobras offshore wells. The project leverages state-of-the-art machine learning and deep learning techniques to identify operational anomalies in real-time drilling and production data.

## 🚀 Key Features

- **Multivariate Time Series Analysis**: Handles complex interdependencies between multiple well parameters
- **State-of-the-Art Models**: Implements TranAD, LSTM-VAE, USAD, and ECOD algorithms
- **Real-time Processing**: Optimized for high-frequency offshore well data
- **Interpretable Results**: SHAP-based model explanations for operational decisions
- **Cloud-Ready**: AWS and GCP deployment configurations included

## 🏗️ Architecture

```
petrobras-offshore-wells-anomaly-detection/
├── src/                    # Core source code
│   ├── models/            # ML/DL model implementations
│   ├── data/              # Data processing pipelines
│   ├── features/          # Feature engineering
│   └── utils/             # Utility functions
├── notebooks/             # Marimo interactive notebooks
├── data/                  # Datasets and processed data
├── tests/                 # Automated test suite
├── docs/                  # Documentation
├── config/                # Configuration files
├── docker/                # Containerization
└── scripts/               # Automation scripts
```

## 🛠️ Technology Stack

### Core Technologies
- **Python 3.11+** - Modern Python with type hints
- **Polars** - High-performance data manipulation (faster than Pandas)
- **Marimo** - Interactive notebooks for collaborative development
- **uv** - Fast Python package manager and environment management

### Machine Learning & Deep Learning
- **PyTorch** - Deep learning framework
- **Scikit-learn** - Traditional ML algorithms
- **Optuna** - Hyperparameter optimization
- **SHAP** - Model interpretability

### Data Science & Visualization
- **Plotly** - Interactive visualizations
- **ydata-profiling** - Automated EDA
- **tslearn** - Time series learning utilities

### Cloud & Deployment
- **AWS** - Cloud infrastructure and ML services
- **GCP** - Google Cloud Platform integration
- **MLflow** - Model lifecycle management
- **Docker** - Containerization

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- uv package manager
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/petrobras-offshore-wells-anomaly-detection.git
   cd petrobras-offshore-wells-anomaly-detection
   ```

2. **Install uv (if not already installed)**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Create virtual environment and install dependencies**
   ```bash
   uv sync
   ```

4. **Activate the environment**
   ```bash
   source .venv/bin/activate  # Linux/macOS
   # or
   .venv\Scripts\activate     # Windows
   ```

### Running the Project

1. **Start Marimo notebook server**
   ```bash
   marimo edit notebooks/
   ```

2. **Run anomaly detection models**
   ```bash
   python src/main.py
   ```

3. **Execute tests**
   ```bash
   pytest tests/
   ```

## 📊 Usage Examples

### Basic Anomaly Detection

```python
from src.models import TranADModel
from src.data import WellDataProcessor

# Load and preprocess well data
processor = WellDataProcessor()
data = processor.load_data("well_001.csv")

# Initialize and train model
model = TranADModel()
model.train(data)

# Detect anomalies
anomalies = model.detect_anomalies(data)
```

### Interactive Analysis with Marimo

```python
# In Marimo notebook
import marimo as mo
import polars as pl

# Load data
df = pl.read_csv("data/well_data.csv")

# Interactive visualization
mo.md(f"## Well Data Analysis\n\nDataset shape: {df.shape}")
```

## 📚 Documentation

### Core Documentation
- **[Setup Guide](docs/setup-guide.md)** - Complete project setup instructions
- **[3W Integration](docs/3W_INTEGRATION.md)** - Integration with 3W system
- **[AWS Setup](docs/AWS_SETUP.md)** - AWS deployment and configuration
- **[GCP Setup](docs/GCP_SETUP.md)** - Google Cloud Platform setup

### Development Guidelines
- **[Conventional Commits](docs/CONVENTIONAL_COMMITS.md)** - Git commit standards
- **[Contributing Guidelines](CONTRIBUTING.md)** - How to contribute to the project

## 🔬 Research Focus

### Anomaly Detection Challenges
- **Multivariate Dependencies**: Complex relationships between well parameters
- **Real-time Processing**: High-frequency data streams from offshore sensors
- **Operational Context**: Domain-specific anomaly definitions
- **Interpretability**: Explainable AI for operational decisions

### Model Performance Metrics
- **AUC-PR**: Precision-Recall curves for imbalanced data
- **F1-Score**: Balanced precision and recall
- **Detection Latency**: Time to anomaly identification
- **False Positive Rate**: Operational efficiency considerations

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test categories
pytest tests/test_models.py
pytest tests/test_data_processing.py
```

## 🚀 Performance Optimization

- **Polars**: 10-100x faster than Pandas for large datasets
- **Vectorized Operations**: Optimized numerical computations
- **Memory Management**: Efficient data structures for time series
- **Parallel Processing**: Multi-core support for model training

## 🌟 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Install development dependencies
uv sync --group dev

# Install pre-commit hooks
pre-commit install

# Run code quality checks
ruff check src/
black src/
mypy src/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.

## 🤝 Acknowledgments

- **Petrobras** - For providing domain expertise and data access
- **PIBIC Program** - Undergraduate research funding
- **Open Source Community** - For the amazing tools and libraries

## 📞 Contact

- **Project Lead**: [Your Name]
- **Institution**: [Your University]
- **Email**: [your.email@university.edu]

---

> **🇧🇷 [Ver documentação em Português Brasileiro](README.pt-BR.md)**

<div align="center">
  <sub>Built with ❤️ for offshore well safety and efficiency</sub>
</div>
