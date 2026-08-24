# Testing Evidence & Data Validation Documentation

## Overview
This document records automated test execution evidence and data quality validation checks across the 5 domain projects.

---

## Test Execution Results (`tests/run_tests.py`)

```
test_01_all_datasets_present (tests.test_data_pipeline.TestDataPipeline) ... ok
test_02_data_validator_full (tests.test_data_pipeline.TestDataPipeline) ... ok
test_03_statistical_analyzer (tests.test_data_pipeline.TestDataPipeline) ... ok
test_04_visualizer_generation (tests.test_data_pipeline.TestDataPipeline) ... ok
test_05_pdf_report_generator (tests.test_data_pipeline.TestDataPipeline) ... ok
test_06_missing_value_handling (tests.test_data_pipeline.TestDataPipeline) ... ok
test_07_outlier_detection (tests.test_data_pipeline.TestDataPipeline) ... ok
test_08_advanced_statistics (tests.test_data_pipeline.TestDataPipeline) ... ok
test_09_hypothesis_testing (tests.test_data_pipeline.TestDataPipeline) ... ok

----------------------------------------------------------------------
Ran 9 tests in 1.301s

OK
```

---

## Dataset Quality Metrics

| Dataset Name | Total Rows | Total Columns | Duplicate Rows | Missing Value Handling | Schema Status |
|--------------|------------|---------------+----------------+------------------------|---------------|
| `supermarket_sales.csv` | 2,000 | 15 | 0 | Rating imputed via median | **PASSED** |
| `student_performance.csv` | 1,000 | 11 | 0 | StudyHours imputed via median | **PASSED** |
| `weather_data.csv` | 1,000 | 9 | 0 | Pressure imputed via mean | **PASSED** |
| `healthcare_covid.csv` | 1,000 | 10 | 0 | Positivity rate imputed via median | **PASSED** |
| `stock_market.csv` | 1,000 | 11 | 0 | Zero missing values | **PASSED** |

---

## Statistical Validation Evidence
- **Dynamic PDF Reporting:** Hypothesis tests now dynamically evaluate `p_value < 0.05` to inject true analytical conclusions. Effect sizes (Cohen's d, Eta Squared) and 95% Confidence Intervals are extracted natively from `scipy.stats`.
- **Tukey HSD Post-Hoc:** Following ANOVA tests (e.g., Weather dataset), Tukey HSD accurately highlights specific categorical pairs exhibiting statistical differences.
- **Finance Risk Metrics:** Annualized Volatility, Sharpe Ratio, Sortino Ratio, and Max Drawdowns strictly verified against financial formulas.
