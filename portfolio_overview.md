# Executive Portfolio Overview: Multi-Domain

## Executive Summary
This portfolio presents 5 end-to-end data analysis projects built across **5 distinct domains**. Each project enforces strict data quality checks, rigorous formal hypothesis testing, and delivers automated dynamic PDF reports.

---

## 🔍 Cross-Domain Analytical Insights

By standardizing our object-oriented `src/` pipeline across all 5 distinct sectors, several core truths regarding data analysis emerged:

1. **Universal Data Quality Requirements:** Whether predicting COVID-19 transmission or stock market volatility, missing values and outliers consistently demand domain-specific context. (e.g., dropping a rainfall NaN is acceptable, dropping a stock price NaN is disastrous).
2. **Standardization of EDA:** The flow of `Data Cleaning → EDA → Hypothesis Testing → Business Interpretation` proved remarkably resilient regardless of the dataset.
3. **Statistical Rigor vs Visual Assumption:** Raw visualization frequently masks statistical insignificance. The integration of Pearson correlations, ANOVAs, and T-tests ensured that recommendations were backed by mathematical confidence (e.g., proving Member spending behavior in Retail was statistically significant, not just a visual anomaly).
4. **Actionable Recommendations:** Converting findings to business recommendations followed the identical strict format (`Finding → Meaning → Recommendation`), proving that data scientists must always serve as business translators.

---

## 5 Projects Overview

### Project 1: Retail - Supermarket Sales Revenue Analysis
- **Domain:** Retail
- **Objective:** Analyze daily sales patterns and test customer behavior spending limits.
- **Hypothesis Test:** Independent Two-Sample T-Test (Member vs Normal).
- **Deliverables:** `notebooks/01_supermarket_sales_trend_analysis.ipynb`, `reports/Project1_Supermarket_Sales_Trend_Report.pdf`

### Project 2: Education - Student Performance Analysis
- **Domain:** Education
- **Objective:** Calculate pass/fail rates and evaluate the correlation between attendance and academic scores.
- **Hypothesis Test:** Pearson Correlation (Attendance vs Score), One-Way ANOVA (Parent Education).
- **Deliverables:** `notebooks/02_student_performance_analysis.ipynb`, `reports/Project2_Student_Performance_Report.pdf`

### Project 3: Weather - Climate Data Analysis
- **Domain:** Weather
- **Objective:** Analyze temperature distributions and properly handle NaN values (safely treating missing rainfall as 0.0).
- **Hypothesis Test:** One-Way ANOVA (Seasonal Temperature Variation).
- **Deliverables:** `notebooks/03_weather_data_analysis.ipynb`, `reports/Project3_Weather_Data_Report.pdf`

### Project 4: Healthcare - COVID-19 Trends
- **Domain:** Healthcare
- **Objective:** Analyze COVID-19 infection trends across states and recovery rates.
- **Hypothesis Test:** Pearson Correlation (Vaccination vs Positivity). Indicates association, deliberately avoiding claims of causation.
- **Deliverables:** `notebooks/04_healthcare_covid_analysis.ipynb`, `reports/Project4_Healthcare_COVID_Report.pdf`

### Project 5: Finance - Stock Market Analysis
- **Domain:** Finance
- **Objective:** Analyze stock market volume distribution and calculate portfolio risk metrics (Sharpe Ratio, Max Drawdown).
- **Hypothesis Test:** Pearson Correlation (Volume vs Return Volatility).
- **Deliverables:** `notebooks/05_finance_stock_analysis.ipynb`, `reports/Project5_Finance_Stock_Report.pdf`

---

## Deliverables Index
- **Interactive Streamlit Dashboard:** `dashboard/app.py`
- **5 Jupyter Notebooks** in `notebooks/`
- **6 Professional PDF Reports** in `reports/` (Includes 1 Master Summary Report)
- **15+ High-Res Visualizations** in `visualizations/`
- **Automated Test Suite** in `tests/run_tests.py`
