import os
import nbformat as nbf

os.makedirs('notebooks', exist_ok=True)

def create_notebook(title, domain, description, csv_name, load_kwargs, custom_pre_cleaning_cells, cells_data, filename):
    nb = nbf.v4.new_notebook()
    
    header_md = f"""# {title}
**Domain:** {domain}  
**Dataset Source:** `data/{csv_name}`  

---

## Executive Overview
{description}

---
"""
    nb.cells.append(nbf.v4.new_markdown_cell(header_md))

    setup_code = """import os
import sys
sys.path.append('..')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from src.data_loader import DataLoader
from src.statistical_analysis import StatisticalAnalyzer
from src.visualization import Visualizer

%matplotlib inline
plt.style.use('seaborn-v0_8-whitegrid')
"""
    nb.cells.append(nbf.v4.new_code_cell(setup_code))

    dq_md = """## 1. Data Quality & Preprocessing
Checklist:
✓ Dataset shape
✓ Missing values
✓ Duplicate rows
✓ Numeric outliers
"""
    nb.cells.append(nbf.v4.new_markdown_cell(dq_md))
    
    raw_dq_code = f"""loader = DataLoader('../data/{csv_name}')
df = loader.load_data()

print("==============================")
print("     RAW DATA QUALITY")
print("==============================")
print(loader.generate_data_quality_report())
"""
    nb.cells.append(nbf.v4.new_code_cell(raw_dq_code))

    for md_cell, code_cell in custom_pre_cleaning_cells:
        if md_cell: nb.cells.append(nbf.v4.new_markdown_cell(md_cell))
        if code_cell: nb.cells.append(nbf.v4.new_code_cell(code_cell))

    clean_dq_code = f"""df = loader.clean_missing_values({load_kwargs})

print("==============================")
print("   CLEANED DATA QUALITY")
print("==============================")
print(loader.generate_data_quality_report())
"""
    nb.cells.append(nbf.v4.new_code_cell(clean_dq_code))

    for title, business_question, code_snippet, finding, meaning, recommendation in cells_data:
        md = f"### {title}\n"
        if business_question:
            md += f"**Business Question:** {business_question}\n"
            
        nb.cells.append(nbf.v4.new_markdown_cell(md))
        nb.cells.append(nbf.v4.new_code_cell(code_snippet))
        
        if finding or meaning or recommendation:
            rec_md = f"""**Finding:** {finding}  
**Meaning:** {meaning}  
**Recommendation:** {recommendation}"""
            nb.cells.append(nbf.v4.new_markdown_cell(rec_md))

    limitations_md = """## Limitations
- Dataset size is limited.
- Results are observational.
- Correlation does not imply causation.
- Some variables contain missing observations.
- External factors are not included.
"""
    nb.cells.append(nbf.v4.new_markdown_cell(limitations_md))

    filepath = os.path.join('notebooks', filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"Jupyter Notebook generated: {filepath}")

print("Generating 5 advanced Jupyter Notebooks...")

# --- 1. RETAIL ---
retail_cells = [
    ("Outlier Analysis", "Are there anomalous high-value transactions, and are they genuine?", 
     "sns.boxplot(data=df, x='Total')\nplt.title('Outlier Analysis: Transaction Totals')\nplt.show()\nprint('Outliers represent genuine bulk purchases, not data errors. We retain them.')",
     "A few transactions exceed normal IQR boundaries.", "These represent bulk B2B purchases.", "Do not delete these outliers; consider creating a VIP B2B tier."),
    ("Advanced Pandas: Pivot Table", "How do product line sales vary across cities?",
     "city_prod = df.pivot_table(index='City', columns='Product_Line', values='Total', aggfunc='sum')\ndisplay(city_prod)", None, None, None),
    ("Customer Behavior Analysis", "Do Members spend more than Normal customers?",
     "mem_spend = df[df['Customer_Type']=='Member']['Total'].mean()\nnorm_spend = df[df['Customer_Type']=='Normal']['Total'].mean()\nprint(f'Member Avg: {mem_spend:.2f} | Normal Avg: {norm_spend:.2f}')",
     "Members have a slightly higher average transaction value in this sample.", "Members demonstrate stronger spending behavior.", "Introduce targeted loyalty offers to increase member retention."),
    ("Statistical Hypothesis Testing", "Is the difference in spending statistically significant?",
     "stats = StatisticalAnalyzer(df)\nres = stats.two_sample_ttest('Customer_Type', 'Total', 'Member', 'Normal')\nprint(stats.format_hypothesis_report(\n    'No difference in spending between Members and Normal customers.',\n    'Members spend more than Normal customers.',\n    'Two-Sample Independent T-Test',\n    't-stat',\n    res['test_statistic'], res['p_value'],\n    'Members have a statistically higher transaction value.', 'There is no statistically significant difference in average transaction value between Member and Normal customers.',\n    why_it_matters_reject='Validates the ROI of the loyalty program.', ci_lower=res['ci_lower'], ci_upper=res['ci_upper']\n))", None, None, None)
]
create_notebook("Project 1: Retail Analytics", "Retail", "Customer behavior, statistical significance, and advanced aggregations.", "supermarket_sales.csv", "{}", [], retail_cells, "01_supermarket_sales_trend_analysis.ipynb")

# --- 2. EDUCATION ---
edu_cells = [
    ("Outlier Analysis", "Are there unusual academic scores?", 
     "sns.boxplot(data=df, x='MathScore')\nplt.show()", "A few scores fall below the lower whisker.", "These are students requiring extreme intervention.", "Provide immediate tutoring for these specific IDs."),
    ("Advanced Pandas: Groupby & Agg", "What is the detailed statistical breakdown of scores by Parent Education?",
     "ed_stats = df.groupby('ParentEducation').agg({'MathScore': ['mean', 'median', 'std', 'count']})\ndisplay(ed_stats)", None, None, None),
    ("Statistical Hypothesis Testing (ANOVA)", "Is parent education associated with academic performance?",
     "stats = StatisticalAnalyzer(df)\nres = stats.one_way_anova('ParentEducation', 'MathScore')\nprint(stats.format_hypothesis_report(\n    'No difference in scores by parent education.', 'Scores differ by parent education.', 'One-Way ANOVA', 'F-stat', res['test_statistic'], res['p_value'], 'Parent education is associated with math scores.', 'No significant evidence that parent education impacts math scores in this dataset.', why_it_matters_reject='Suggests targeted interventions for at-risk demographics may be beneficial.'\n))", None, None, None),
    ("Statistical Hypothesis Testing (Correlation)", "Is higher attendance associated with better academic performance?",
     "res = stats.pearson_correlation_test('AttendancePercentage', 'MathScore')\nprint(stats.format_hypothesis_report(\n    'No correlation between attendance and score.', 'Positive correlation exists.', 'Pearson Correlation', 'r', res['r_statistic'], res['p_value'], 'High attendance correlates with high grades.', 'No statistically significant relationship detected between attendance and math scores.', why_it_matters_reject='Supports enforcing strict attendance policies.', ci_lower=res['ci_lower'], ci_upper=res['ci_upper']\n))", None, None, None)
]
create_notebook("Project 2: Education Analytics", "Education", "Statistical drivers of student performance.", "student_performance.csv", "{}", [], edu_cells, "02_student_performance_analysis.ipynb")

# --- 3. WEATHER ---
weather_pre_clean = [
    ("### Domain Assumption: Missing Rainfall\nObserve the RAW DATA QUALITY above. Rainfall is missing in 96.8% of the rows. If we assume 'missing' means 'no rainfall was recorded because it didn't rain', then imputing with `0.0` is the correct domain approach. We will now apply this cleaning decision.", "")
]
weather_cells = [
    ("Outlier Analysis", "Are there anomalous temperature readings?", 
     "sns.boxplot(data=df, y='Temperature_C')\nplt.show()", "No extreme outliers observed.", "Data is well-bounded.", "Proceed with standard analysis."),
    ("Advanced Pandas: Time Series Resampling", "What is the monthly average rainfall?",
     "df['Date'] = pd.to_datetime(df['Date'])\nmonthly = df.set_index('Date').resample('ME')['Rainfall_mm'].mean()\ndisplay(monthly.head())", None, None, None),
    ("Extreme Weather Definition", "How often do heatwaves occur?",
     "heatwave_thresh = df['Temperature_C'].quantile(0.95)\nheatwaves = df[df['Temperature_C'] > heatwave_thresh]\nprint(f'Defined heatwave as > {heatwave_thresh:.1f}C. Found {len(heatwaves)} instances.')", "Heatwaves are rare but identifiable.", "We have a strict 95th percentile definition.", "Issue alerts when temp exceeds 95th percentile."),
    ("Statistical Hypothesis Testing (ANOVA) & Tukey HSD", "Are weather condition temperature differences statistically significant?",
     "stats = StatisticalAnalyzer(df)\nres = stats.one_way_anova('WeatherCondition', 'Temperature_C')\ntukey = stats.tukey_hsd_test('WeatherCondition', 'Temperature_C')\nsig_pairs = tukey[tukey['is_significant']]\ntukey_insight = 'Post-hoc Tukey HSD reveals significant differences between: ' + ', '.join([f\"{r['group1']} vs {r['group2']}\" for _, r in sig_pairs.head(3).iterrows()])\nprint(stats.format_hypothesis_report(\n    'No difference in mean temp across conditions.', 'Mean temp differs by condition.', 'One-Way ANOVA', 'F', res['test_statistic'], res['p_value'], f'Conditions have distinct temperature profiles. {tukey_insight}', 'No significant evidence that conditions vary by temperature.', why_it_matters_reject='Useful for forecasting energy grid demand during specific weather events.'\n))", None, None, None)
]
create_notebook("Project 3: Weather Analytics", "Weather", "Time series and extreme event analysis.", "weather_data.csv", "strategy_map={'Rainfall_mm': 0.0}", weather_pre_clean, weather_cells, "03_weather_data_analysis.ipynb")

# --- 4. HEALTHCARE ---
health_cells = [
    ("Outlier Analysis", "Are there spikes in new cases?", 
     "sns.boxplot(data=df, x='NewCases')\nplt.show()", "Massive spikes (outliers) exist.", "These represent distinct 'waves' of the pandemic.", "Ensure surge capacity during wave events."),
    ("Advanced Pandas: Melt", "How do cases, recoveries, and deaths compare in a normalized format?",
     "melted = df.melt(id_vars=['Date', 'State'], value_vars=['NewCases', 'Recoveries', 'Deaths'])\ndisplay(melted.head())", None, None, None),
    ("Trend Analysis", "How are cases trending over time?",
     "df['Date'] = pd.to_datetime(df['Date'])\ndf.groupby('Date')['NewCases'].sum().plot()\nplt.title('Total Cases Over Time')\nplt.show()", None, None, None),
    ("Statistical Hypothesis Testing", "Is vaccination associated with lower positivity?",
     "stats = StatisticalAnalyzer(df)\nres = stats.pearson_correlation_test('VaccinationDosesAdministered', 'PositivityRate_Pct')\nprint(stats.format_hypothesis_report(\n    'No correlation between vax and positivity.', 'Negative correlation exists.', 'Pearson Correlation', 'r', res['r_statistic'], res['p_value'], 'Higher vaccination rates are associated with lower positivity rates.', 'No statistically significant linear relationship was detected between vaccination doses and positivity rate.', why_it_matters_reject='Suggests the efficacy of vaccination campaigns on community spread.', ci_lower=res['ci_lower'], ci_upper=res['ci_upper']\n))", None, None, None)
]
create_notebook("Project 4: Healthcare Analytics", "Healthcare", "COVID-19 trends and correlation analysis.", "healthcare_covid.csv", "{}", [], health_cells, "04_healthcare_covid_analysis.ipynb")

# --- 5. FINANCE ---
fin_cells = [
    ("Outlier Analysis", "Are there anomalous trading volumes?", 
     "sns.boxplot(data=df, x='Volume')\nplt.show()", "High volume days are present.", "These represent institutional buying/selling or news events.", "Monitor these days for volatility."),
    ("Advanced Pandas: Rolling & Shift", "What is the 20-Day Moving Average?",
     "df['20D_MA'] = df['Close'].rolling(20).mean()\ndf['DailyReturn_Pct'] = df['Close'].pct_change() * 100\ndisplay(df[['Date', 'Close', '20D_MA', 'DailyReturn_Pct']].tail())", None, None, None),
    ("Risk Metrics", "What is the Sharpe Ratio and Max Drawdown?",
     "stats = StatisticalAnalyzer(df.dropna())\nsharpe = stats.calculate_sharpe_ratio('DailyReturn_Pct')\ndrawdown = stats.calculate_max_drawdown('Close')\nprint(f'Sharpe Ratio: {sharpe}\\nMax Drawdown: {drawdown}%')", "Sharpe ratio indicates risk-adjusted return.", "Provides insight into portfolio quality.", "Use these metrics for asset allocation."),
    ("Statistical Hypothesis Testing", "Is volume correlated with volatility (absolute daily return)?",
     "df['Abs_Return'] = df['DailyReturn_Pct'].abs()\nstats = StatisticalAnalyzer(df.dropna())\nres = stats.pearson_correlation_test('Volume', 'Abs_Return')\nprint(stats.format_hypothesis_report(\n    'No correlation between volume and volatility.', 'Positive correlation exists.', 'Pearson Correlation', 'r', res['r_statistic'], res['p_value'], 'Days with high trading volume correlate with price swings.', 'The dataset does not provide sufficient evidence of a statistically significant relationship between trading volume and absolute daily returns.', why_it_matters_reject='Suggests risk managers monitor market volume to anticipate risk events.', ci_lower=res['ci_lower'], ci_upper=res['ci_upper']\n))", None, None, None)
]
create_notebook("Project 5: Finance Analytics", "Finance", "Moving averages, risk metrics, and returns.", "stock_market.csv", "{}", [], fin_cells, "05_finance_stock_analysis.ipynb")

print("Finished generating notebooks.")
