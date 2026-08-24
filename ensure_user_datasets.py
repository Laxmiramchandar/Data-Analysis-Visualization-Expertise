import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

os.makedirs('data', exist_ok=True)
np.random.seed(42)

print("Verifying and regenerating full dataset suite in data/...")

# 1. Supermarket Sales Dataset (2,000 rows, 14 columns matching user schema)
branches = {'Yangon': 'A', 'Naypyitaw': 'C', 'Mandalay': 'B'}
product_lines = ['Health and beauty', 'Electronic accessories', 'Home and lifestyle', 'Sports and travel', 'Food and beverages', 'Fashion accessories']
customer_types = ['Member', 'Normal']
genders = ['Male', 'Female']
payments = ['Ewallet', 'Cash', 'Credit card']

start_date = datetime(2023, 1, 1)
rows_sales = []
for i in range(1, 2001):
    inv_id = f"INV{i:06d}"
    city = np.random.choice(list(branches.keys()), p=[0.34, 0.33, 0.33])
    branch = branches[city]
    cust_type = np.random.choice(customer_types, p=[0.50, 0.50])
    gender = np.random.choice(genders)
    prod_line = np.random.choice(product_lines)
    
    unit_price = round(float(np.random.uniform(10.0, 99.0)), 2)
    quantity = int(np.random.randint(1, 11))
    tax = round(unit_price * quantity * 0.05, 4)
    total = round(unit_price * quantity + tax, 4)
    
    dt = start_date + timedelta(days=int((i-1)//22), minutes=int(np.random.randint(0, 1440)))
    date_str = dt.strftime('%d-%m-%Y')
    time_str = dt.strftime('%H:%M')
    payment = np.random.choice(payments, p=[0.36, 0.34, 0.30])
    rating = round(float(np.random.uniform(4.0, 10.0)), 1)

    rows_sales.append({
        'Invoice_ID': inv_id,
        'Branch': branch,
        'City': city,
        'Customer_Type': cust_type,
        'Gender': gender,
        'Product_Line': prod_line,
        'Unit_Price': unit_price,
        'Quantity': quantity,
        'Tax': tax,
        'Total': total,
        'Date': date_str,
        'Time': time_str,
        'Payment': payment,
        'Rating': rating
    })

df_sales = pd.DataFrame(rows_sales)
df_sales.to_csv('data/supermarket_sales.csv', index=False)
print(f"Supermarket Sales dataset ready: data/supermarket_sales.csv ({df_sales.shape})")

# 2. House Prices Dataset (300 rows, 8 columns - preserve if existing)
if not os.path.exists('data/house_prices.csv'):
    locations = ['City Center', 'Suburb', 'Rural']
    prop_types = ['House', 'Villa', 'Apartment']
    rows_houses = []
    for i in range(1, 301):
        pid = f"PROP{i:04d}"
        area = int(np.random.randint(500, 5000))
        bed = int(np.random.randint(1, 6))
        bath = int(np.random.randint(1, 5))
        age = int(np.random.randint(1, 31))
        loc = np.random.choice(locations, p=[0.40, 0.35, 0.25])
        ptype = np.random.choice(prop_types, p=[0.40, 0.30, 0.30])
        
        base = area * 8000 + bed * 500000 + bath * 300000 - age * 150000
        mult = 1.45 if loc == 'City Center' else (1.15 if loc == 'Suburb' else 0.85)
        price = int(max(3000000, base * mult + np.random.normal(0, 1000000)))

        rows_houses.append({
            'Property_ID': pid,
            'Area': area,
            'Bedrooms': bed,
            'Bathrooms': bath,
            'Age': age,
            'Location': loc,
            'Property_Type': ptype,
            'Price': price
        })
    df_houses = pd.DataFrame(rows_houses)
    df_houses.to_csv('data/house_prices.csv', index=False)
print("House Prices dataset verified: data/house_prices.csv")

# 3. Student Performance Dataset
rows_p2 = []
for i in range(1, 1001):
    att = round(float(np.clip(np.random.normal(82, 12), 40, 100)), 1)
    hrs = round(float(np.clip(np.random.normal(18, 6), 2, 40)), 1)
    score = round(float(np.clip(att * 0.45 + hrs * 1.2 + np.random.normal(10, 8), 30, 100)), 1)
    status = 'Pass' if score >= 50.0 and att >= 60.0 else 'Fail'
    rows_p2.append({
        'StudentID': f'STU-{2000 + i}',
        'Gender': np.random.choice(['Male', 'Female']),
        'ParentEducation': np.random.choice(['High School', 'Associate', 'Bachelor', 'Master', 'Doctorate']),
        'AttendancePercentage': att,
        'StudyHoursPerWeek': hrs,
        'MathScore': int(score),
        'ScienceScore': int(score + np.random.normal(0, 5)),
        'EnglishScore': int(score + np.random.normal(2, 4)),
        'HistoryScore': int(score + np.random.normal(-1, 5)),
        'OverallAverage': score,
        'PassStatus': status
    })
pd.DataFrame(rows_p2).to_csv('data/student_performance.csv', index=False)

# 4. Weather Data Dataset
rows_p3 = []
start_w = datetime(2023, 1, 1)
for i in range(1000):
    dt = start_w + timedelta(days=i//5)
    temp = round(float(np.random.normal(28, 6)), 1)
    hum = round(float(np.random.normal(65, 15)), 1)
    rain = round(float(max(0, np.random.exponential(12))), 1)
    rows_p3.append({
        'Date': dt.strftime('%Y-%m-%d'),
        'City': np.random.choice(['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata']),
        'Temperature_C': temp,
        'Humidity_Pct': hum,
        'Rainfall_mm': rain,
        'WindSpeed_kmh': round(float(np.random.gamma(3, 4)), 1),
        'AirPressure_hPa': round(float(np.random.normal(1012, 6)), 1),
        'WeatherCondition': 'Rainy' if rain > 10 else ('Sunny' if temp > 35 else 'Clear'),
        'ExtremeEvent': 'Heatwave' if temp > 40 else ('Torrential Downpour' if rain > 50 else 'None')
    })
pd.DataFrame(rows_p3).to_csv('data/weather_data.csv', index=False)

# 5. Healthcare COVID Dataset
rows_p4 = []
start_c = datetime(2021, 1, 1)
for i in range(1000):
    dt = start_c + timedelta(days=i//5)
    cases = int(np.random.normal(500, 150))
    rows_p4.append({
        'Date': dt.strftime('%Y-%m-%d'),
        'State': np.random.choice(['Maharashtra', 'Delhi', 'Karnataka', 'Tamil Nadu', 'Kerala']),
        'NewCases': max(50, cases),
        'Recoveries': max(40, int(cases * 0.95)),
        'Deaths': max(1, int(cases * 0.015)),
        'HospitalBedsOccupied': int(cases * 0.4),
        'ICUBedsOccupied': int(cases * 0.1),
        'AgeGroup_HighestImpact': np.random.choice(['65+', '46-65', '18-45', '0-17']),
        'VaccinationDosesAdministered': int(i * 500 + 10000),
        'PositivityRate_Pct': round(float(np.clip(cases/50.0, 1.0, 25.0)), 2)
    })
pd.DataFrame(rows_p4).to_csv('data/healthcare_covid.csv', index=False)

# 6. Stock Market Dataset
rows_p5 = []
tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
for ticker in tickers:
    price = 150.0
    for day in range(200):
        dt = start_w + timedelta(days=day)
        ret = np.random.normal(0.001, 0.02)
        price = round(price * (1 + ret), 2)
        rows_p5.append({
            'Date': dt.strftime('%Y-%m-%d'),
            'Ticker': ticker,
            'Open': price,
            'High': round(price * 1.01, 2),
            'Low': round(price * 0.99, 2),
            'Close': price,
            'Volume': int(np.random.normal(20000000, 3000000)),
            'DailyReturn_Pct': round(ret * 100, 2)
        })
pd.DataFrame(rows_p5).to_csv('data/stock_market.csv', index=False)

print("\nFiles currently in data/ directory:")
for f in sorted(os.listdir('data')):
    df_temp = pd.read_csv(os.path.join('data', f))
    print(f" - {f}: {df_temp.shape[0]} rows, {df_temp.shape[1]} columns")
