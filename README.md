# Data Analysis & Visualization Portfolio

> **Month 2: Data Analysis & Visualization Expertise**  
> A complete, professional GitHub portfolio containing 5 rigorous data analysis projects across **5 distinct domains** (Retail, Education, Weather, Healthcare, and Finance).

---

## 📚 Core Features & Rigor
- **Formal Statistical Hypothesis Testing:** Every project executes strict statistical tests (T-Test, ANOVA, Pearson) with explicit H₀/H₁ definitions, p-values, and strategic business interpretations.
- **Advanced Pandas Operations:** Demonstrates high-performance processing using `pivot_table()`, `melt()`, `resample()`, `rolling()`, and vectorized `groupby` aggregations.
- **Data Quality & Outliers:** Standardized schema validation, missing-value handling, and IQR outlier detection implemented across all 5 domains.
- **Large-Data Optimization:** Implements generator `chunksize` ingestion and memory reduction techniques (downcasting to `category` dtypes) to demonstrate techniques for improving memory efficiency and processing larger datasets.
- **Automated Dynamic Reporting:** `ReportLab` PDF engine automatically extracts actual computed statistics (e.g. Sharpe Ratio, correlation coefficients) directly from the codebase into the final executive PDFs.
- **Interactive Dashboard:** Includes a Streamlit + Plotly multi-domain web application.

---

## 📁 Repository Directory Structure

```
.
├── README.md                                          # Master portfolio documentation & guide
├── portfolio_overview.md                             # Cross-domain executive portfolio summary
├── requirements.txt                                   # Python dependencies (pandas, streamlit, plotly, etc.)
├── data/                                              # Datasets directory (5 domains)
├── src/                                               # Reusable Python analytical package
│   ├── data_loader.py                                 # Memory-optimized data loading & quality checks
│   ├── statistical_analysis.py                        # Strict hypothesis testing (T-tests, ANOVA, Risk)
│   ├── visualization.py                               # Matplotlib/Seaborn charting engine
│   ├── pdf_generator.py                               # Dynamic ReportLab PDF compilation
│   └── data_validation.py                             # Automated schema validation
├── notebooks/                                         # 5 Executable Jupyter Notebooks
├── visualizations/                                    # Saved high-res chart images (.png)
├── reports/                                           # 6 Executive PDF Reports (ReportLab)
├── dashboard/                                         # Interactive Web Dashboard
│   └── app.py                                         # Streamlit application
└── tests/                                             # Automated test suite
    ├── test_data_pipeline.py
    └── run_tests.py
```

---

## 🔄 Reproducibility & Setup Guide

Designed to be reproducible across supported Python environments using the provided requirements.txt. Follow these steps to re-generate the entire portfolio:

```bash
# 1. Clone repository
git clone <your-repo-url>
cd <your-repo-directory>

# 2. Create virtual environment
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# 3. Install requirements
pip install -r requirements.txt

# 4. Run automated test suite (Validates data, math, and ETL)
python tests/run_tests.py

# 5. Generate Jupyter Notebooks
python scripts/generate_notebooks.py

# 6. Execute core pipeline (Generates PDFs, Visualizations, and Stats)
python scripts/run_full_analysis.py

# 7. Launch Interactive Dashboard
streamlit run dashboard/app.py
```

---

## ⚠️ General Limitations

Across all 5 analytical domains, the following standard limitations apply:
- **Observational Nature:** Results are strictly observational; correlation does not imply causation (especially within Healthcare and Education domains).
- **Dataset Size:** Datasets serve as statistical samples, meaning margin of error exists scaling up to enterprise populations.
- **External Factors:** Models do not account for external macroeconomic variables (e.g., inflation in Retail, global recessions in Finance).
