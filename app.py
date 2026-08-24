import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

# Add parent directory to path to import src modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.statistical_analysis import StatisticalAnalyzer

st.set_page_config(page_title="Data Analysis Portfolio", layout="wide", page_icon="📊")

# --- DATA LOADING ---
@st.cache_data
def load_data(domain):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    if domain == "Retail":
        df = pd.read_csv(os.path.join(base_dir, 'data', 'supermarket_sales.csv'))
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
        return df
    elif domain == "Education":
        return pd.read_csv(os.path.join(base_dir, 'data', 'student_performance.csv'))
    elif domain == "Weather":
        df = pd.read_csv(os.path.join(base_dir, 'data', 'weather_data.csv'))
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    elif domain == "Healthcare":
        df = pd.read_csv(os.path.join(base_dir, 'data', 'healthcare_covid.csv'))
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    elif domain == "Finance":
        df = pd.read_csv(os.path.join(base_dir, 'data', 'stock_market.csv'))
        df['Date'] = pd.to_datetime(df['Date'])
        return df

# --- SIDEBAR ---
st.sidebar.title("📊 Portfolio Dashboard")
st.sidebar.markdown("Explore 5 distinct data domains.")

project = st.sidebar.selectbox("Select Project Domain", ["Retail", "Education", "Weather", "Healthcare", "Finance"])

df = load_data(project)

# --- MAIN APP ---
st.title(f"{project} Analytics Dashboard")

# Interactive Filters
st.sidebar.subheader("Filters")
if 'Date' in df.columns:
    min_date = df['Date'].min()
    max_date = df['Date'].max()
    date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]

if project == "Retail":
    category = st.sidebar.multiselect("Select Product Line", df['Product_Line'].unique(), default=df['Product_Line'].unique())
    df = df[df['Product_Line'].isin(category)]

    # KPIs
    st.subheader("Key Performance Indicators")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Revenue", f"₹{df['Total'].sum():,.2f}")
    c2.metric("Total Transactions", f"{len(df):,}")
    c3.metric("Avg Order Value", f"₹{df['Total'].mean():,.2f}")

    # Charts
    st.subheader("Interactive Visualizations")
    daily_sales = df.groupby('Date')['Total'].sum().reset_index()
    fig1 = px.line(daily_sales, x='Date', y='Total', title='Daily Revenue Trend')
    st.plotly_chart(fig1, use_container_width=True)

    c4, c5 = st.columns(2)
    fig2 = px.bar(df.groupby('City')['Total'].sum().reset_index(), x='City', y='Total', title='Revenue by City', color='City')
    c4.plotly_chart(fig2, use_container_width=True)
    
    fig3 = px.box(df, x='Customer_Type', y='Total', title='Spend by Customer Type', color='Customer_Type')
    c5.plotly_chart(fig3, use_container_width=True)

    # Insights
    stats = StatisticalAnalyzer(df)
    t_test_retail = stats.two_sample_ttest('Customer_Type', 'Total', 'Member', 'Normal')
    if t_test_retail['p_value'] < 0.05:
        st.info("**Business Insight:** Members show higher average spend than Normal customers. Consider prioritizing loyalty signups.")
    else:
        st.info("**Business Insight:** No statistically significant difference detected in average spend between Member and Normal customers. The loyalty program is not currently associated with higher transaction values.")

elif project == "Education":
    gender = st.sidebar.multiselect("Select Gender", df['Gender'].unique(), default=df['Gender'].unique())
    df = df[df['Gender'].isin(gender)]
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Students", f"{len(df):,}")
    c2.metric("Avg Math Score", f"{df['MathScore'].mean():.1f}")
    c3.metric("Pass Rate", f"{(df['PassStatus']=='Pass').mean()*100:.1f}%")
    
    st.subheader("Interactive Visualizations")
    c4, c5 = st.columns(2)
    pass_counts = df['PassStatus'].value_counts().reset_index()
    pass_counts.columns = ['Status', 'Count']
    fig1 = px.bar(pass_counts, x='Status', y='Count', title='Student Pass vs Fail Count', color='Status')
    c4.plotly_chart(fig1, use_container_width=True)
    
    fig2 = px.box(df, x='ParentEducation', y='OverallAverage', title='Overall Score by Parent Education', color='ParentEducation')
    c5.plotly_chart(fig2, use_container_width=True)
    
    fig3 = px.scatter(df, x='AttendancePercentage', y='MathScore', color='PassStatus', title='Attendance vs Math Score', trendline="ols")
    st.plotly_chart(fig3, use_container_width=True)
    
    stats = StatisticalAnalyzer(df)
    pearson_edu = stats.pearson_correlation_test('AttendancePercentage', 'MathScore')
    if pearson_edu['p_value'] < 0.05:
        st.info("**Business Insight:** Correlation observed between attendance and performance. Consider implementing early warning systems for truancy.")
    else:
        st.info("**Business Insight:** No statistically significant relationship detected between attendance and math scores.")

elif project == "Weather":
    c1, c2, c3 = st.columns(3)
    c1.metric("Avg Temp", f"{df['Temperature_C'].mean():.1f}°C")
    c2.metric("Max Temp", f"{df['Temperature_C'].max():.1f}°C")
    c3.metric("Total Rainfall", f"{df['Rainfall_mm'].sum():.1f} mm")
    
    st.subheader("Interactive Visualizations")
    fig1 = px.box(df, x='WeatherCondition', y='Temperature_C', color='WeatherCondition', title='Temperature Distribution by Condition')
    st.plotly_chart(fig1, use_container_width=True)
    
    c4, c5 = st.columns(2)
    avg_temp_city = df.groupby('City')['Temperature_C'].mean().reset_index()
    fig2 = px.bar(avg_temp_city, x='City', y='Temperature_C', title='Average Temperature by City', color='City')
    c4.plotly_chart(fig2, use_container_width=True)
    
    fig3 = px.scatter(df, x='Humidity_Pct', y='Rainfall_mm', color='City', title='Humidity vs Rainfall', trendline="ols")
    c5.plotly_chart(fig3, use_container_width=True)
    
    stats = StatisticalAnalyzer(df)
    anova_weather = stats.one_way_anova('WeatherCondition', 'Temperature_C')
    if anova_weather['p_value'] < 0.05:
        st.info("**Business Insight:** Weather conditions exhibit distinct temperature profiles. Extreme heatwaves (>95th pct) may require municipal alerts.")
    else:
        st.info("**Business Insight:** No significant evidence that weather conditions vary by temperature.")

elif project == "Healthcare":
    state = st.sidebar.multiselect("Select State", df['State'].unique(), default=df['State'].unique()[:5])
    df = df[df['State'].isin(state)]
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total New Cases", f"{df['NewCases'].sum():,}")
    c2.metric("Total Recoveries", f"{df['Recoveries'].sum():,}")
    c3.metric("Recovery Rate", f"{(df['Recoveries'].sum() / df['NewCases'].sum()) * 100:.1f}%")
    
    st.subheader("Interactive Visualizations")
    fig1 = px.bar(df.groupby('State')['NewCases'].sum().reset_index(), x='State', y='NewCases', title='Total Cases by State', color='State')
    st.plotly_chart(fig1, use_container_width=True)
    
    c4, c5 = st.columns(2)
    fig2 = px.scatter(df, x='Recoveries', y='Deaths', color='State', title='Recoveries vs Deaths', trendline="ols")
    c4.plotly_chart(fig2, use_container_width=True)
    
    fig3 = px.box(df, x='AgeGroup_HighestImpact', y='PositivityRate_Pct', title='Positivity Rate by Impacted Age Group', color='AgeGroup_HighestImpact')
    c5.plotly_chart(fig3, use_container_width=True)
    
    stats = StatisticalAnalyzer(df)
    pearson_health = stats.pearson_correlation_test('VaccinationDosesAdministered', 'PositivityRate_Pct')
    if pearson_health['p_value'] < 0.05:
        st.info("**Business Insight:** Caseloads are geographically skewed. High vaccination rates correlate with reduced positivity rates.")
    else:
        st.info("**Business Insight:** No statistically significant linear relationship was detected between vaccination doses administered and positivity rate in this dataset.")

elif project == "Finance":
    ticker = st.sidebar.selectbox("Select Ticker", df['Ticker'].unique())
    df = df[df['Ticker'] == ticker]
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Current Price", f"${df['Close'].iloc[-1]:.2f}")
    c2.metric("Avg Daily Volume", f"{df['Volume'].mean():,.0f}")
    c3.metric("Volatility (Std Dev)", f"{df['DailyReturn_Pct'].std():.2f}%")
    
    st.subheader("Interactive Visualizations")
    c4, c5 = st.columns(2)
    fig1 = px.line(df, x='Date', y='Close', title=f'{ticker} Stock Price History')
    c4.plotly_chart(fig1, use_container_width=True)
    
    fig2 = px.histogram(df, x='DailyReturn_Pct', title='Daily Return Distribution', nbins=30)
    c5.plotly_chart(fig2, use_container_width=True)
    
    # Cumulative Return & Drawdown Plotly Chart
    df_sorted = df.sort_values(by='Date')
    rets = df_sorted['DailyReturn_Pct'].dropna() / 100.0
    cum_ret = (1 + rets).cumprod() - 1
    roll_max = (1 + rets).cumprod().cummax()
    drawdown = ((1 + rets).cumprod() - roll_max) / roll_max
    
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=df_sorted['Date'], y=cum_ret*100, mode='lines', name='Cumulative Return (%)', line=dict(color='green')))
    fig3.add_trace(go.Scatter(x=df_sorted['Date'], y=drawdown*100, mode='lines', name='Drawdown (%)', fill='tozeroy', line=dict(color='red')))
    fig3.update_layout(title='Cumulative Return and Maximum Drawdown', xaxis_title='Date', yaxis_title='Percentage (%)')
    st.plotly_chart(fig3, use_container_width=True)
    
    df['Abs_Return'] = df['DailyReturn_Pct'].abs()
    stats = StatisticalAnalyzer(df.dropna())
    pearson_fin = stats.pearson_correlation_test('Volume', 'Abs_Return')
    if pearson_fin['p_value'] < 0.05:
        st.info("**Business Insight:** Volume spikes correlate with absolute daily returns (volatility). Risk parameters should be monitored during high volume.")
    else:
        st.info("**Business Insight:** The dataset does not provide sufficient evidence of a statistically significant relationship between trading volume and absolute daily returns.")

st.markdown("---")
st.markdown("*Data Analysis & Visualization Portfolio. Generated for full-stack review.*")
