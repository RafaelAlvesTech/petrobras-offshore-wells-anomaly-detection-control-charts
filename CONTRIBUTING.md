# 🌟 Contributing Guidelines - Petrobras Offshore Wells Anomaly Detection

> **🇧🇷 [Ver diretrizes em Português Brasileiro](CONTRIBUTING.pt-BR.md)**

## 🎯 Welcome Contributors!

Thank you for your interest in contributing to the **Petrobras Offshore Wells Anomaly Detection** project! This is a PIBIC (Undergraduate Research) project focused on detecting anomalies in multivariate time series from offshore wells using state-of-the-art machine learning techniques.

## 🚀 How to Contribute

### 📋 Before You Start

1. **Read the project documentation** - Understand the project goals and architecture
2. **Check existing issues** - See if your idea is already being worked on
3. **Join discussions** - Participate in GitHub Discussions and Issues
4. **Set up your environment** - Follow the [Setup Guide](docs/setup-guide.md)

### 🔄 Contribution Workflow

#### 1. **Fork & Clone**

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/petrobras-offshore-wells-anomaly-detection.git
cd petrobras-offshore-wells-anomaly-detection

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL_REPO/petrobras-offshore-wells-anomaly-detection.git
```

#### 2. **Create Feature Branch**

```bash
# Create and switch to a new branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/your-bug-description
```

#### 3. **Make Changes**

- Follow the [coding standards](#-coding-standards)
- Write tests for new functionality
- Update documentation as needed
- Ensure all tests pass

#### 4. **Commit Your Changes**

```bash
# Use conventional commits
git commit -m "feat: add new anomaly detection model"

# Or for bug fixes
git commit -m "fix: resolve data preprocessing issue"
```

#### 5. **Push & Create Pull Request**

```bash
git push origin feature/your-feature-name
# Create PR on GitHub with detailed description
```

## 📝 Coding Standards

### 🐍 Python Code Style

#### **Type Hints & Documentation**

```python
from typing import List, Optional, Union
import numpy as np
import polars as pl

def detect_anomalies(
    data: pl.DataFrame,
    threshold: float = 0.95,
    window_size: Optional[int] = None
) -> tuple[List[int], np.ndarray]:
    """
    Detect anomalies in multivariate time series data.

    Args:
        data: Input DataFrame with time series data
        threshold: Anomaly detection threshold (0.0 to 1.0)
        window_size: Size of sliding window for analysis

    Returns:
        Tuple of (anomaly_indices, anomaly_scores)

    Raises:
        ValueError: If threshold is outside valid range
    """
    if not 0.0 <= threshold <= 1.0:
        raise ValueError("Threshold must be between 0.0 and 1.0")

    # Implementation here...
    return anomaly_indices, anomaly_scores
```

#### **Code Formatting**

- Use **Ruff** for formatting and linting
- Maximum line length: **88 characters**
- Use **f-strings** for string formatting
- Prefer **list comprehensions** over explicit loops when appropriate

#### **Import Organization**

```python
# Standard library imports
import os
import sys
from typing import List, Optional

# Third-party imports
import numpy as np
import polars as pl
import torch

# Local imports
from src.models.base import BaseModel
from src.utils.helpers import validate_data
```

### 🧪 Testing Standards

#### **Test Structure**

```python
# tests/test_models.py
import pytest
import polars as pl
from src.models.anomaly_detector import AnomalyDetector

class TestAnomalyDetector:
    """Test suite for AnomalyDetector class."""

    @pytest.fixture
    def sample_data(self) -> pl.DataFrame:
        """Create sample data for testing."""
        return pl.DataFrame({
            "timestamp": range(100),
            "pressure": [100 + i * 0.1 for i in range(100)],
            "temperature": [25 + i * 0.05 for i in range(100)]
        })

    def test_detector_initialization(self):
        """Test detector initializes correctly."""
        detector = AnomalyDetector(threshold=0.95)
        assert detector.threshold == 0.95
        assert detector.is_fitted is False

    def test_detector_fitting(self, sample_data):
        """Test detector fitting process."""
        detector = AnomalyDetector(threshold=0.95)
        detector.fit(sample_data)
        assert detector.is_fitted is True
        assert detector.n_features == 2
```

#### **Test Coverage Requirements**

- **Minimum coverage**: 80%
- **Critical functions**: 95% coverage
- **New features**: Must include tests
- **Bug fixes**: Must include regression tests

### 📚 Documentation Standards

#### **Docstring Format (Google Style)**

```python
def train_model(
    data: pl.DataFrame,
    model_type: str = "tranad",
    hyperparameters: Optional[dict] = None
) -> BaseModel:
    """Train an anomaly detection model.

    This function trains various types of anomaly detection models
    including TranAD, LSTM-VAE, and USAD.

    Args:
        data: Training data as Polars DataFrame
        model_type: Type of model to train ('tranad', 'lstm-vae', 'usad')
        hyperparameters: Optional hyperparameter dictionary

    Returns:
        Trained model instance

    Raises:
        ValueError: If model_type is not supported
        DataError: If data format is invalid

    Example:
        >>> data = load_well_data("well_001.csv")
        >>> model = train_model(data, "tranad")
        >>> predictions = model.predict(data)
    """
```

#### **README Updates**

- Update README.md for new features
- Include usage examples
- Update installation instructions if needed
- Add new dependencies to requirements

## 🔧 Development Setup

### **Environment Setup**

```bash
# Clone and setup
git clone <your-fork>
cd petrobras-offshore-wells-anomaly-detection

# Create virtual environment
uv venv
source .venv/bin/activate  # Linux/macOS
# or .venv\Scripts\activate  # Windows

# Install dependencies
uv sync --group dev

# Install pre-commit hooks
uv run pre-commit install
```

### **Pre-commit Hooks**

The project uses pre-commit hooks to ensure code quality:

- **Ruff**: Code formatting and linting
- **Black**: Code formatting
- **MyPy**: Type checking
- **Pytest**: Test execution

### **Running Quality Checks**

```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check .

# Type checking
uv run mypy src/

# Run tests
uv run pytest

# Run all checks
uv run pre-commit run --all-files
```

## 📊 Pull Request Guidelines

### **PR Template**

```markdown
## 🎯 Description

Brief description of changes and motivation

## 🔧 Changes Made

- [ ] Feature A added
- [ ] Bug B fixed
- [ ] Documentation C updated

## 🧪 Testing

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## 📚 Documentation

- [ ] Code documented
- [ ] README updated
- [ ] API docs updated

## 🔍 Checklist

- [ ] Code follows style guidelines
- [ ] Tests added for new functionality
- [ ] All existing tests pass
- [ ] Documentation updated
- [ ] No breaking changes introduced
```

### **Review Process**

1. **Automated checks** must pass
2. **Code review** by maintainers
3. **Test coverage** requirements met
4. **Documentation** updated
5. **Squash commits** before merge

## 🐛 Bug Reports

### **Bug Report Template**

```markdown
## 🐛 Bug Description

Clear description of the bug

## 🔍 Steps to Reproduce

1. Step 1
2. Step 2
3. Step 3

## 📱 Expected vs Actual Behavior

- **Expected**: What should happen
- **Actual**: What actually happens

## 💻 Environment

- OS: [e.g., Ubuntu 20.04]
- Python: [e.g., 3.11.5]
- Package versions: [e.g., polars==1.32.3]

## 📋 Additional Context

Any other relevant information
```

## 💡 Feature Requests

### **Feature Request Template**

```markdown
## 🚀 Feature Description

Clear description of the requested feature

## 🎯 Use Case

Why this feature is needed and how it will be used

## 🔧 Implementation Ideas

Any thoughts on how to implement this feature

## 📚 Related Issues

Links to related issues or discussions
```

## 🤝 Community Guidelines

### **Code of Conduct**

- **Be respectful** and inclusive
- **Help newcomers** get started
- **Provide constructive feedback**
- **Focus on the code**, not the person
- **Celebrate contributions** and improvements

### **Communication Channels**

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Pull Requests**: Code contributions
- **Email**: [your.email@university.edu]

## 🏆 Recognition

### **Contributor Levels**

- **🌱 New Contributor**: First contribution
- **🌿 Regular Contributor**: Multiple contributions
- **🌳 Core Contributor**: Significant contributions
- **🏆 Maintainer**: Project leadership

### **Hall of Fame**

Contributors will be recognized in:

- Project README
- Release notes
- Contributor documentation
- Annual acknowledgments

## 📞 Getting Help

### **Resources**

- [Project Documentation](docs/)
- [Setup Guide](docs/setup-guide.md)
- [3W Integration](docs/3W_INTEGRATION.md)
- [GitHub Issues](https://github.com/your-repo/issues)

### **Contact**

- **Project Lead**: [Your Name]
- **Email**: [your.email@university.edu]
- **Institution**: [Your University]

---

> **🇧🇷 [Ver diretrizes em Português Brasileiro](CONTRIBUTING.pt-BR.md)**

<div align="center">
  <sub>Built with ❤️ by the open source community</sub>
</div>
