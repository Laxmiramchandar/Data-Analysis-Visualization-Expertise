# Technical Architecture & Pipeline Design

## Overview
The **Multi-Domain Data Analysis Pipeline** follows a modular, scalable architecture separating data ingestion, processing, statistical computation, visualization, and document compilation.

---

## Architectural Diagram

```
+------------------+     +--------------------+     +------------------------+
|   Raw Datasets   | --> |  src/data_loader   | --> | src/statistical_analysis|
|  (data/*.csv)    |     |  (Clean & Impute)  |     | (Stats & Hypothesis)   |
+------------------+     +--------------------+     +------------------------+
                                                                |
                                                                v
+------------------+     +--------------------+     +------------------------+
|  reports/*.pdf   | <-- | src/pdf_generator  | <-- |   src/visualization    |
| (ReportLab PDFs) |     |  (Platypus Engine) |     | (15+ PNG Charts)       |
+------------------+     +--------------------+     +------------------------+
```

---

## Component Specifications

### 1. `src/data_loader.py`
- **Responsibility:** Ingests CSV files, performs missing value median/mean/mode imputation, parses date columns, detects outliers via IQR (`q3 + 1.5 * iqr`).

### 2. `src/statistical_analysis.py`
- **Responsibility:** Calculates descriptive statistics (mean, median, std, min, 25%, 50%, 75%, max, skewness, kurtosis), computes Pearson/Spearman correlation matrices, executes 2-sample independent t-tests and One-Way ANOVA tests via `scipy.stats`.

### 3. `src/visualization.py`
- **Responsibility:** Encapsulates Seaborn & Matplotlib figure rendering routines with publication-ready styling (dpi=300), exporting PNG chart figures to `visualizations/`.

### 4. `src/pdf_generator.py`
- **Responsibility:** Builds multi-page executive PDF reports using ReportLab Platypus framework, formatting cover banners, KPI data tables, bulleted insights, embedded chart images, and strategic recommendations.

### 5. `src/data_validation.py`
- **Responsibility:** Asserts column schema compliance, duplicate record counts, null thresholds, and negative value metrics across input datasets.
