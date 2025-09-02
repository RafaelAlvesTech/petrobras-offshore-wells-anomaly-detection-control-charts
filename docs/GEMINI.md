# Project Overview

This project is focused on anomaly detection in multivariate time series data from Petrobras offshore wells. It is a PIBIC (Graduate Research) project for the years 2025-2026, developed at the Risk Studies Center (CER-UFBA) of the Federal University of Bahia (UFBA). The project utilizes machine learning and deep learning techniques to identify operational anomalies in real-time drilling and production data.

## Key Technologies

- **Programming Language:** Python 3.11+
- **Data Manipulation:** Polars, Pandas
- **Machine Learning:** PyTorch, Scikit-learn, PyOD, tslearn
- **Deep Learning Models:** TranAD, LSTM-VAE, USAD
- **Hyperparameter Optimization:** Optuna
- **Model Interpretability:** SHAP
- **Interactive Notebooks:** Marimo
- **Package Management:** uv
- **Cloud Platforms:** AWS, Google Cloud Platform (GCP)
- **MLOps:** MLflow
- **Containerization:** Docker

## Project Structure

The project is organized into the following directories:

- `src/`: Core source code, including data processing, models, and utilities.
- `notebooks/`: Marimo interactive notebooks for analysis and experimentation.
- `data/`: Datasets and processed data.
- `tests/`: Automated test suite.
- `docs/`: Project documentation.
- `config/`: Configuration files.
- `docker/`: Docker-related files for containerization.
- `scripts/`: Automation scripts for setup, deployment, and other tasks.

# Building and Running

## Prerequisites

- Python 3.11+
- uv package manager
- Git

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/petrobras-offshore-wells-anomaly-detection.git
    cd petrobras-offshore-wells-anomaly-detection
    ```

2.  **Install uv (if not already installed):**

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

3.  **Create a virtual environment and install dependencies:**

    ```bash
    uv sync
    ```

4.  **Activate the environment:**

    ```bash
    source .venv/bin/activate  # Linux/macOS
    # or
    .venv\Scripts\activate     # Windows
    ```

## Running the Project

- **Start the Marimo notebook server:**

  ```bash
  marimo edit notebooks/
  ```

- **Run anomaly detection models:**

  ```bash
  python src/main.py
  ```

- **Execute tests:**

  ```bash
  pytest tests/
  ```

# Development Conventions

- **Commit Messages:** The project follows the [Conventional Commits](docs/CONVENTIONAL_COMMITS.md) specification.
- **Contributing:** Contributions are welcome. Please see the [Contributing Guidelines](CONTRIBUTING.md) for more details.
- **Code Quality:** The project uses `ruff` for linting, `black` for formatting, and `mypy` for type checking. These tools are enforced using pre-commit hooks.

## Development Setup

1.  **Install development dependencies:**

    ```bash
    uv sync --group dev
    ```

2.  **Install pre-commit hooks:**

    ```bash
    pre-commit install
    ```
