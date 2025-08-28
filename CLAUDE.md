# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🛢️ Project Overview

This is a **PIBIC (Undergraduate Research) project** focused on **anomaly detection in multivariate time series** from Petrobras offshore wells. The project leverages state-of-the-art machine learning and deep learning techniques to identify operational anomalies in real-time drilling and production data.

**Research Institution**: Risk Studies Center (CER-UFBA), Department of Statistics, Federal University of Bahia (UFBA)

## 🚀 Essential Development Commands

### Environment Setup
```bash
# Setup virtual environment and dependencies
uv sync

# Activate environment
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Install development dependencies
uv sync --group dev
```

### Code Quality and Testing
```bash
# Format code with Ruff
uv run ruff format .

# Lint code with Ruff
uv run ruff check .

# Type checking with MyPy
uv run mypy src/

# Run tests with pytest
uv run pytest

# Run tests with coverage
uv run pytest --cov=src

# Run all pre-commit hooks
uv run pre-commit run --all-files

# Install pre-commit hooks
uv run pre-commit install
```

### Interactive Development
```bash
# Start Marimo notebook server
marimo edit notebooks/

# Run specific Python scripts
python src/main.py

# AWS/GCP setup scripts
./scripts/setup_aws.sh
./scripts/setup_gcp.sh
./scripts/setup_3w_integration.sh
```

### Git and Commit Management
```bash
# Generate conventional commit helper
./scripts/commit-emoji.sh generate

# Show commit types and scopes
./scripts/commit-emoji.sh types
./scripts/commit-emoji.sh scopes
```

## 🏗️ Project Architecture

### Core Structure
```
src/
├── api/                    # API endpoints and interfaces
├── aws/                    # AWS integration modules
│   ├── aws_config_manager.py
│   └── aws_training.py
├── config/                 # Configuration management
│   ├── config_manager.py   # Main config manager with caching
│   └── threew_config.py    # 3W dataset specific config
├── data/                   # Data processing pipeline
│   ├── data_loader.py      # Generic data loading
│   ├── preprocessing.py    # Data preprocessing utilities
│   └── threew_dataset.py   # 3W dataset specific loader
├── evaluation/             # Model evaluation metrics
├── gcp/                    # Google Cloud Platform integration
│   ├── auth.py            # GCP authentication
│   ├── config.py          # GCP configuration
│   ├── mlflow_integration.py
│   ├── storage.py         # Cloud storage operations
│   ├── training.py        # GCP training jobs
│   └── vertex_ai.py       # Vertex AI integration
└── models/                # ML/DL model implementations
```

### Key Configuration Files
- **`pyproject.toml`**: Main dependency management (uses `uv`)
- **`config/3w_config.yaml`**: 3W dataset configuration with preprocessing, caching, and performance settings
- **`aws-config.yaml`**: Complete AWS SageMaker, EC2, and S3 configuration
- **`gcp-config.yaml`**: Google Cloud Platform and Vertex AI configuration
- **`.cursorrules`**: Development rules and coding standards

### Data Processing Architecture
The project uses a **three-tier data architecture**:

1. **Raw Data Layer**: Original 3W dataset files
2. **Processing Layer**: `src/data/` modules handle normalization, feature engineering, and windowing
3. **Model Layer**: `src/models/` implements TranAD, LSTM-VAE, USAD, and ECOD algorithms

The `ConfigManager` class (`src/config/config_manager.py`) provides:
- YAML-based configuration loading with caching
- Environment-specific settings
- Runtime configuration updates
- Configuration validation

## 🛠️ Technology Stack & Key Dependencies

### Core Technologies
- **Python 3.11.13** (strict version requirement)
- **uv**: Package manager and environment management
- **Polars >= 1.32.3**: High-performance data manipulation (prefer over Pandas)
- **Marimo >= 0.15.0**: Interactive notebooks for collaborative development

### ML/DL Stack
- **PyTorch >= 2.0.1**: Deep learning framework with GPU support
- **Scikit-learn >= 1.7.1**: Traditional ML algorithms
- **Optuna >= 3.4.0**: Hyperparameter optimization
- **MLflow >= 2.8.0**: Model lifecycle management
- **TensorBoard >= 2.15.0**: Training visualization

### Data Processing
- **PyArrow >= 19.0**: Columnar data processing
- **TSlearn >= 0.6**: Time series utilities
- **ydata-profiling >= 4.15**: Automated EDA
- **Numba >= 0.61**: JIT compilation for numerical computations

## 📊 Development Patterns

### Data Processing Patterns
```python
# Always prefer Polars over Pandas for performance
import polars as pl

# Use lazy evaluation for large datasets
df = pl.scan_csv("data/well_data.csv").lazy()
result = df.filter(pl.col("pressure") > threshold).collect()

# Use configuration manager for settings
from src.config.config_manager import get_config_manager
config = get_config_manager().get_config("3w")
```

### Model Development Pattern
```python
# Follow this structure for new anomaly detection models
from typing import Dict, List, Tuple
import torch
from src.models.base import BaseModel  # If exists

class NewAnomalyModel(BaseModel):
    def __init__(self, config: Dict):
        # Initialize with configuration
        pass

    def fit(self, data: pl.DataFrame) -> None:
        # Training logic
        pass

    def detect_anomalies(self, data: pl.DataFrame) -> Tuple[List[int], np.ndarray]:
        # Return (anomaly_indices, anomaly_scores)
        pass
```

### Configuration Usage Pattern
```python
from src.config.config_manager import get_threew_setting

# Get specific settings with defaults
window_size = get_threew_setting("dataset.rolling_window.window_size", default=100)
batch_size = get_threew_setting("performance.batch_size", default=1000)
```

## 🔬 Anomaly Detection Domain Knowledge

### Core Models Implemented
- **TranAD**: Transformer-based anomaly detection for multivariate time series
- **LSTM-VAE**: Long Short-Term Memory Variational Autoencoder
- **USAD**: UnSupervised Anomaly Detection with adversarial training
- **ECOD**: Empirical Cumulative Distribution Outlier Detection

### Evaluation Metrics Focus
- **AUC-PR**: Precision-Recall curves (critical for imbalanced offshore well data)
- **F1-Score**: Balanced precision and recall for anomaly detection
- **Detection Latency**: Time to identify anomalies in real-time scenarios
- **False Positive Rate**: Critical for operational efficiency

### 3W Dataset Integration
The project integrates with the **3W (Three Worlds) dataset** from Petrobras:
- **Problem Types**: Binary classification for spurious DHSV closures
- **Data Format**: Multivariate time series with rolling windows
- **Preprocessing**: Robust scaling, imputation, and feature selection
- **Validation**: 5-fold cross-validation with hyperparameter optimization

## 🚀 Cloud Integration

### AWS Integration (SageMaker/EC2)
- **Training**: GPU instances (P3, G4dn, G5 families) for deep learning models
- **Storage**: S3 bucket structure with lifecycle policies
- **Monitoring**: CloudWatch integration with custom metrics
- **MLflow**: Artifact storage and experiment tracking

### GCP Integration (Vertex AI)
- **Training Jobs**: Vertex AI custom jobs with GPU support
- **Model Registry**: Vertex AI model registry integration
- **Storage**: Google Cloud Storage for datasets and models
- **Monitoring**: Cloud Logging and Monitoring integration

## 🧪 Testing and Quality Standards

### Test Structure
```bash
tests/
├── test_models.py           # Model unit tests
├── test_data_processing.py  # Data pipeline tests
├── test_config_manager.py   # Configuration tests
└── test_aws_integration.py  # Cloud integration tests
```

### Pre-commit Hooks Configured
- **Ruff**: Fast Python linting and formatting
- **MyPy**: Static type checking
- **YAML validation**: Configuration file validation
- **JSON validation**: Metadata validation
- **Large file detection**: Prevent accidental large file commits

## 🌟 Development Best Practices

### Commit Standards
Use **Conventional Commits** with emojis (see `docs/CONVENTIONAL_COMMITS.md`):
```bash
🚀 feat(anomaly-detection): implement TranAD model
🐛 fix(data-processing): correct normalization for pressure data
📚 docs(readme): update installation instructions
♻️ refactor(models): optimize LSTM-VAE architecture
```

### Code Style Enforced
- **Line length**: 88 characters (Black standard)
- **Type hints**: Required for public APIs
- **Docstrings**: Google/NumPy style for all classes and functions
- **Import organization**: Standard library, third-party, local imports

### Configuration Management
- Use `ConfigManager` class for all configuration access
- Store sensitive data in environment variables
- Validate configurations before use
- Support for multiple environments (dev, prod, cloud)

## 🔧 Special Integration Notes

### 3W Dataset Integration
```python
# Use the specialized 3W configuration and loader
from src.config.threew_config import ThreeWConfig
from src.data.threew_dataset import ThreeWDataset

# Load with proper preprocessing pipeline
dataset = ThreeWDataset(config_name="3w")
data = dataset.load_problem("01_binary_classifier_of_spurious_closure_of_dhsv")
```

### Cloud Training Pattern
```python
# AWS training example
from src.aws.aws_training import train_on_sagemaker
train_on_sagemaker(model_config, data_path, instance_type="ml.p3.2xlarge")

# GCP training example
from src.gcp.training import train_on_vertex_ai
train_on_vertex_ai(model_config, data_path, machine_type="n1-standard-4")
```

### Performance Optimization
- Use **Polars** for data operations (10-100x faster than Pandas)
- Enable **multiprocessing** in config for CPU-intensive tasks
- Use **memory-efficient** mode for large datasets
- Implement **caching** for repeated data access patterns

This project represents cutting-edge research in industrial anomaly detection with real-world offshore well applications. Focus on performance, interpretability, and scalability when contributing.
