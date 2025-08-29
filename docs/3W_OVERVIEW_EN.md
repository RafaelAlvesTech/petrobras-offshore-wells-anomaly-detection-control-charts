# 🛢️ Petrobras 3W Project Overview

> **🇧🇷 [Ver em Português Brasileiro](3W_OVERVIEW.md)**

## 📋 Introduction

The **3W Project (Three Worlds)** is Petrobras' first public repository on GitHub, launched on May 30, 2022. It represents a strategic initiative to promote experimentation and development of Machine Learning-based approaches for specific problems related to detection and classification of undesirable events that occur in offshore oil wells.

## 🎯 Why "3W"?

The name **3W** was chosen because this dataset is composed of instances from **3** different sources and which contain undesirable events that occur in oil **W**ells.

## 🚀 Motivation and Impact

### Industry Problems

- **Production Losses**: Undesirable events can cause up to **5% production losses** in certain scenarios
- **Maintenance Costs**: The cost of a maritime probe, required to perform various types of operations, can exceed **US$ 500,000 per day**
- **Safety**: Prevention of environmental accidents and human casualties
- **Integrity**: Monitoring of well integrity and subsea systems

### Expected Benefits

- **Improve the process** of identifying undesirable events in drilling, completion and production phases
- **Increase efficiency** of monitoring well integrity and subsea systems
- **Prevent losses** for people, environment and company image

## 🏗️ Strategy and Governance

### Innovation Connections Program

The 3W is the first pilot of Petrobras' **"Conexões para Inovação - Módulo Open Lab"** program, composed of:

1. **3W Dataset**: Evolves and is supplemented with more instances over time
2. **3W Toolkit**: Evolves in many ways to cover an increasing number of undesirable events

### Governance

- **Leadership**: Flow Assurance department and research center (CENPES)
- **Expansion**: Since May 1st, 2024, includes the Well Integrity department
- **Evolution**: Project increasingly consolidated at Petrobras
- **Professionals**: More specialists in instance labeling
- **Tools**: More investment in digital tools for labeling and export

## 📊 Project Resources

### 3W Dataset

- **First realistic and public dataset** with rare undesirable real events in oil wells
- **Format**: Parquet files with Brotli compression
- **License**: Creative Commons Attribution 4.0 International
- **Structure**: Multiple Parquet files saved in subdirectories
- **Theory**: Based on the paper "A realistic and public dataset with rare undesirable real events in oil wells" (Journal of Petroleum Science and Engineering)

### 3W Toolkit

- **Software package** written in Python 3
- **Facilitates**: Dataset overview generation, experimentation and comparative analysis
- **Standardization**: Key points of ML-based algorithm development pipeline
- **Arbitrary choices**: Carefully made to allow adequate comparative analysis

### Incorporated Problems

Currently available:

- **Binary Classifier for Spurious DHSV Closure**
  - Type: Binary classification
  - Objective: Identify unintended valve closures
  - Application: Well safety and integrity
  - Phase: Production

## 🌍 Community and Contributions

### Expected Contribution Types

- **Individuals**: Independent researchers
- **Research Institutions**: Universities and research centers
- **Startups**: Technology companies
- **Companies**: Industry partners
- **Oil Operators**: Other companies in the sector

### How to Contribute

Before contributing, you need to read and agree to:

- [Code of Conduct](https://github.com/petrobras/3W/blob/main/CODE_OF_CONDUCT.md)
- [Contributor License Agreement](https://github.com/petrobras/3W/blob/main/CLA.md)
- [Contributing Guide](https://github.com/petrobras/3W/blob/main/CONTRIBUTING.md)

### Community Engagement

- **Discussions**: [GitHub Discussions](https://github.com/petrobras/3W/discussions)
- **Annual Workshop**: 4th edition in 2025 - [Registration Form](https://forms.gle/cmLa2u4VaXd1T7qp8)
- **Participation**: Read, participate and follow discussions

## 📚 Licenses and Versioning

### Licenses

- **Code**: Licensed under Apache 2.0 License
- **Data**: Dataset data files licensed under Creative Commons Attribution 4.0 International License

### Versioning Strategy

- **3W Toolkit**: Version specified in `__init__.py` file
- **3W Dataset**: Version specified in `dataset.ini` file
- **3W Project**: Version specified with tags in git repository
- **Standard**: Exclusively semantic versioning defined at [semver.org](https://semver.org)
- **Updates**: Always updated manually
- **Independence**: Toolkit and Dataset versioning are completely independent
- **Tags**: Only annotated tags with automatic GitHub releases

## 🔬 Research Impact

### Unique Characteristics

- **First realistic dataset** with rare real events in oil wells
- **Benchmark dataset** for ML technique development
- **Inherent difficulties** of real data
- **Industry standards** for ML pipeline

### Applications

- **Flow Assurance**: Flow monitoring in wells
- **Artificial Lifting Methods**: Pumping systems
- **Well Integrity**: Structural safety
- **Subsea Systems**: Offshore infrastructure

## 🚀 Next Steps

### Development

- **Dataset Evolution**: More instances and event types
- **Toolkit Expansion**: New functionalities and problems
- **Approaches and Algorithms**: Incorporation of dedicated systems
- **Useful Tools**: Utility development

### Community

- **Global Expansion**: More countries and institutions
- **Annual Workshops**: In-person and online events
- **Collaborations**: Partnerships with universities and companies
- **Publications**: Scientific and technical papers

## 📞 Support and Contact

### Help Resources

1. **Official Documentation**: [GitHub 3W](https://github.com/petrobras/3W)
2. **Discussions**: [GitHub Discussions](https://github.com/petrobras/3W/discussions)
3. **Workshop**: [Registration Form](https://forms.gle/cmLa2u4VaXd1T7qp8)
4. **Contributions**: [Contributing Guide](https://github.com/petrobras/3W/blob/main/CONTRIBUTING.md)

### Questions

- Check the discussions section
- Open discussions for specific questions
- Participate actively in the community

---

**🔗 Important Links:**

- [Main 3W Repository](https://github.com/petrobras/3W)
- [Dataset Structure](https://github.com/petrobras/3W/blob/main/3W_DATASET_STRUCTURE.md)
- [Toolkit Structure](https://github.com/petrobras/3W/blob/main/3W_TOOLKIT_STRUCTURE.md)
- [Contributing Guide](https://github.com/petrobras/3W/blob/main/CONTRIBUTING.md)
- [3W Workshop 2025](https://forms.gle/cmLa2u4VaXd1T7qp8)
