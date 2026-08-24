# Setup & Environment Installation Guide

## System Requirements
- **OS:** Windows 10/11, macOS, or Linux
- **Python:** Version 3.10+
- **Pip:** Updated package manager (`pip install --upgrade pip`)

---

## Installation Steps

### 1. Clone or Download Repository
```bash
git clone <repository_url>
cd "2nd task"
```

### 2. Set Up Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Execution Guide

### Generate Datasets
```bash
python scripts/generate_datasets.py
```

### Run Full Analysis Pipeline & Generate PDF Reports
```bash
python scripts/run_full_analysis.py
```

### Generate Jupyter Notebooks
```bash
python scripts/generate_notebooks.py
```

### Execute Test Suite
```bash
python tests/run_tests.py
```
