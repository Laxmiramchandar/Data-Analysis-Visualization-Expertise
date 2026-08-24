import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Ensure data directory exists
os.makedirs('data', exist_ok=True)
np.random.seed(42)

print("Generating 5 domain datasets...")

# ---------------------------------------------------------
# 1. Retail Domain: Supermarket Sales Dataset (2,000 rows)
# ---------------------------------------------------------
start_date = datetime(2024, 1, 1)
dates = [start_date + timedelta(days=int(i // 22), hours=int(np.random.choice([10, 11, 12, 14, 15, 16, 17, 18, 19, 20]))) for i in range(2000)]
categories = ['Electronics', 'Groceries', 'Clothing', 'Home & Lifestyle', 'Health & Beauty', 'Sports & Travel']
cat_weights = [0.30, 0.25, 0.20, 0.12, 0.08, 0.05]
customer_types = ['Member', 'Normal']
genders = ['Male', 'Female']
payment_methods = ['Credit Card', 'E-Wallet', 'Cash']

rows_p1 = []
for i in range(2000):
    dt = dates[i]
    cat = np.random.choice(categories, p=cat_weights)
    if cat == 'Electronics':
        unit_price = round(np.random.uniform(150, 1200), 2)
        qty = np.random.randint(1, 4)
        margin = round(np.random.uniform(0.35, 0.50), 2)
    elif cat == 'Groceries':
        unit_price = round(np.random.uniform(10, 150), 2)
        qty = np.random.randint(2, 10)
        margin = round(np.random.uniform(0.15, 0.25), 2)
    elif cat == 'Clothing':
        unit_price = round(np.random.uniform(40, 300), 2)
        qty = np.random.randint(1, 5)
        margin = round(np.random.uniform(0.25, 0.40), 2)
    else:
        unit_price = round(np.random.uniform(20, 250), 2)
        qty = np.random.randint(1, 6)
        margin = round(np.random.uniform(0.20, 0.35), 2)
    
    # Peak hour multiplier (5-7 PM) and weekend multiplier
    hour = dt.hour
    is_weekend = dt.weekday() >= 5
    multiplier = 1.3 if is_weekend else 1.0
    if 17 <= hour <= 19:
        multiplier *= 1.25

    total_sales = round(unit_price * qty * multiplier, 2)
    cust_type = np.random.choice(customer_types, p=[0.55, 0.45])
    gender = np.random.choice(genders)
    payment = np.random.choice(payment_methods, p=[0.45, 0.35, 0.20])
    rating = round(np.random.uniform(4.0, 10.0), 1)

    rows_p1.append({
        'InvoiceID': f'INV-{10000 + i}',
        'Date': dt.strftime('%Y-%m-%d'),
        'Time': dt.strftime('%H:%M'),
        'Hour': hour,
        'DayOfWeek': dt.strftime('%A'),
        'CustomerType': cust_type,
        'Gender': gender,
        'ProductCategory': cat,
        'UnitPrice': unit_price,
        'Quantity': qty,
        'TotalSales': total_sales,
        'PaymentMethod': payment,
        'Rating': rating,
        'ProfitMargin': margin,
        'Profit': round(total_sales * margin, 2)
    })

df_p1 = pd.DataFrame(rows_p1)
# Inject a few intentional missing values to demonstrate data cleaning pipeline
df_p1.loc[np.random.choice(2000, 15, replace=False), 'Rating'] = np.nan
df_p1.to_csv('data/supermarket_sales.csv', index=False)
print(f"Project 1 Dataset saved: data/supermarket_sales.csv ({df_p1.shape})")

# ---------------------------------------------------------
# 2. Education Domain: Student Performance Dataset (1,000 rows)
# ---------------------------------------------------------
parent_edu_opts = ['High School', 'Associate', 'Bachelor', 'Master', 'Doctorate']
parent_edu_weights = [0.35, 0.25, 0.25, 0.10, 0.05]

rows_p2 = []
for i in range(1, 1001):
    gender = np.random.choice(['Male', 'Female'])
    parent_edu = np.random.choice(parent_edu_opts, p=parent_edu_weights)
    attendance = round(float(np.clip(np.random.normal(82, 12), 40, 100)), 1)
    study_hours = round(float(np.clip(np.random.normal(18, 6), 2, 40)), 1)
    
    # Scores highly correlated with attendance and study hours
    base_score = attendance * 0.45 + study_hours * 1.2 + np.random.normal(10, 8)
    math_score = int(np.clip(base_score + np.random.normal(0, 6), 25, 100))
    science_score = int(np.clip(base_score + np.random.normal(2, 6), 25, 100))
    english_score = int(np.clip(base_score + np.random.normal(4, 5), 30, 100))
    history_score = int(np.clip(base_score + np.random.normal(-1, 5), 25, 100))
    
    overall_avg = round((math_score + science_score + english_score + history_score) / 4.0, 2)
    pass_status = 'Pass' if overall_avg >= 50.0 and attendance >= 60.0 else 'Fail'

    rows_p2.append({
        'StudentID': f'STU-{2000 + i}',
        'Gender': gender,
        'ParentEducation': parent_edu,
        'AttendancePercentage': attendance,
        'StudyHoursPerWeek': study_hours,
        'MathScore': math_score,
        'ScienceScore': science_score,
        'EnglishScore': english_score,
        'HistoryScore': history_score,
        'OverallAverage': overall_avg,
        'PassStatus': pass_status
    })

df_p2 = pd.DataFrame(rows_p2)
# Inject a few nulls for data cleaning demo
df_p2.loc[np.random.choice(1000, 10, replace=False), 'StudyHoursPerWeek'] = np.nan
df_p2.to_csv('data/student_performance.csv', index=False)
print(f"Project 2 Dataset saved: data/student_performance.csv ({df_p2.shape})")

# ---------------------------------------------------------
# 3. Weather Domain: Meteorological Dataset (1,000 rows)
# ---------------------------------------------------------
cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata']
start_weather = datetime(2023, 1, 1)

rows_p3 = []
for i in range(1000):
    city = np.random.choice(cities)
    day_offset = i // 5
    dt = start_weather + timedelta(days=day_offset)
    month = dt.month

    # Seasonal temperature model
    if month in [5, 6, 7]:  # Summer
        temp = round(float(np.random.normal(36, 4)), 1)
        humidity = round(float(np.random.normal(65, 15)), 1)
        rainfall = round(float(max(0, np.random.exponential(18) - 5)), 1)
    elif month in [7, 8, 9]:  # Monsoon
        temp = round(float(np.random.normal(29, 3)), 1)
        humidity = round(float(np.random.normal(85, 8)), 1)
        rainfall = round(float(max(0, np.random.exponential(45))), 1)
    elif month in [11, 12, 1]:  # Winter
        temp = round(float(np.random.normal(19, 4)), 1)
        humidity = round(float(np.random.normal(50, 10)), 1)
        rainfall = round(float(max(0, np.random.exponential(4) - 3)), 1)
    else:  # Spring / Autumn
        temp = round(float(np.random.normal(28, 4)), 1)
        humidity = round(float(np.random.normal(55, 12)), 1)
        rainfall = round(float(max(0, np.random.exponential(8) - 4)), 1)

    wind_speed = round(float(np.random.gamma(3, 4)), 1)
    air_pressure = round(float(np.random.normal(1012, 6)), 1)

    if rainfall > 50:
        cond = 'Heavy Rain'
        extreme = 'Torrential Downpour'
    elif temp > 40:
        cond = 'Sunny'
        extreme = 'Heatwave'
    elif rainfall > 10:
        cond = 'Rainy'
        extreme = 'None'
    elif humidity > 75:
        cond = 'Cloudy'
        extreme = 'None'
    else:
        cond = 'Clear'
        extreme = 'None'

    rows_p3.append({
        'Date': dt.strftime('%Y-%m-%d'),
        'City': city,
        'Temperature_C': temp,
        'Humidity_Pct': humidity,
        'Rainfall_mm': rainfall,
        'WindSpeed_kmh': wind_speed,
        'AirPressure_hPa': air_pressure,
        'WeatherCondition': cond,
        'ExtremeEvent': extreme
    })

df_p3 = pd.DataFrame(rows_p3)
df_p3.loc[np.random.choice(1000, 8, replace=False), 'AirPressure_hPa'] = np.nan
df_p3.to_csv('data/weather_data.csv', index=False)
print(f"Project 3 Dataset saved: data/weather_data.csv ({df_p3.shape})")

# ---------------------------------------------------------
# 4. Healthcare Domain: COVID Trends Dataset (1,000 rows)
# ---------------------------------------------------------
states = ['Maharashtra', 'Delhi', 'Karnataka', 'Tamil Nadu', 'Kerala']
start_covid = datetime(2021, 1, 1)

rows_p4 = []
for i in range(1000):
    state = np.random.choice(states)
    day_offset = i // 5
    dt = start_covid + timedelta(days=day_offset)

    # Wave trajectory modeling (sinusoidal wave dynamics)
    t = day_offset / 40.0
    wave_intensity = max(0.1, np.sin(t) + 0.5 * np.cos(t * 0.5) + np.random.normal(0.8, 0.2))

    new_cases = int(max(50, wave_intensity * 1200 + np.random.normal(100, 50)))
    recoveries = int(max(40, new_cases * np.random.uniform(0.85, 1.05)))
    deaths = int(max(0, new_cases * np.random.uniform(0.01, 0.035)))
    hosp_beds = int(max(20, new_cases * 0.45 + np.random.normal(50, 20)))
    icu_beds = int(max(5, hosp_beds * 0.22 + np.random.normal(10, 5)))
    vax_doses = int(max(500, (day_offset * 150) + np.random.normal(2000, 500)))

    age_impact = np.random.choice(['65+', '46-65', '18-45', '0-17'], p=[0.45, 0.30, 0.18, 0.07])
    positivity_rate = round(float(np.clip((new_cases / 15000.0) * 100, 1.0, 28.0)), 2)

    rows_p4.append({
        'Date': dt.strftime('%Y-%m-%d'),
        'State': state,
        'NewCases': new_cases,
        'Recoveries': recoveries,
        'Deaths': deaths,
        'HospitalBedsOccupied': hosp_beds,
        'ICUBedsOccupied': icu_beds,
        'AgeGroup_HighestImpact': age_impact,
        'VaccinationDosesAdministered': vax_doses,
        'PositivityRate_Pct': positivity_rate
    })

df_p4 = pd.DataFrame(rows_p4)
df_p4.loc[np.random.choice(1000, 12, replace=False), 'PositivityRate_Pct'] = np.nan
df_p4.to_csv('data/healthcare_covid.csv', index=False)
print(f"Project 4 Dataset saved: data/healthcare_covid.csv ({df_p4.shape})")

# ---------------------------------------------------------
# 5. Finance Domain: Stock Market Dataset (1,000 rows)
# ---------------------------------------------------------
tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
base_prices = {'AAPL': 175.0, 'GOOGL': 140.0, 'MSFT': 380.0, 'AMZN': 160.0, 'TSLA': 210.0}

rows_p5 = []
for ticker in tickers:
    current_price = base_prices[ticker]
    start_stock = datetime(2023, 1, 1)
    price_history = []

    for day in range(200):
        dt = start_stock + timedelta(days=day)
        # Geometric Brownian Motion simulation
        daily_return = np.random.normal(0.0008, 0.018)
        open_p = current_price
        close_p = round(open_p * (1 + daily_return), 2)
        high_p = round(max(open_p, close_p) * (1 + abs(np.random.normal(0, 0.008))), 2)
        low_p = round(min(open_p, close_p) * (1 - abs(np.random.normal(0, 0.008))), 2)
        volume = int(np.random.normal(25000000, 5000000))
        current_price = close_p
        price_history.append(close_p)

        ma20 = round(float(np.mean(price_history[-20:])), 2) if len(price_history) >= 20 else close_p
        ma50 = round(float(np.mean(price_history[-50:])), 2) if len(price_history) >= 50 else close_p
        vol30 = round(float(np.std(price_history[-30:])), 2) if len(price_history) >= 30 else 2.5

        rows_p5.append({
            'Date': dt.strftime('%Y-%m-%d'),
            'Ticker': ticker,
            'Open': round(open_p, 2),
            'High': high_p,
            'Low': low_p,
            'Close': close_p,
            'Volume': volume,
            'DailyReturn_Pct': round(daily_return * 100, 2),
            'MA20': ma20,
            'MA50': ma50,
            'Volatility30D': vol30
        })

df_p5 = pd.DataFrame(rows_p5)
df_p5.to_csv('data/stock_market.csv', index=False)
print(f"Project 5 Dataset saved: data/stock_market.csv ({df_p5.shape})")

print("All 5 domain datasets generated successfully!")
