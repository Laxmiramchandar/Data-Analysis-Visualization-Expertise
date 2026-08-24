import os
import pandas as pd

class DataValidator:
    """
    Strict Data Quality Assurance & Validation Suite.
    """

    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.schemas = {
            'supermarket_sales.csv': [
                'Invoice_ID', 'Branch', 'City', 'Customer_Type', 'Gender', 'Product_Line',
                'Unit_Price', 'Quantity', 'Tax', 'Total', 'Date', 'Time', 'Payment', 'Rating'
            ],
            'house_prices.csv': [
                'Property_ID', 'Area', 'Bedrooms', 'Bathrooms', 'Age', 'Location', 'Property_Type', 'Price'
            ],
            'student_performance.csv': [
                'StudentID', 'Gender', 'AttendancePercentage', 'StudyHoursPerWeek', 'OverallAverage', 'PassStatus', 'MathScore', 'ParentEducation'
            ],
            'weather_data.csv': [
                'Date', 'City', 'Temperature_C', 'Humidity_Pct', 'Rainfall_mm', 'WeatherCondition', 'WindSpeed_kmh'
            ],
            'healthcare_covid.csv': [
                'Date', 'State', 'NewCases', 'Recoveries', 'Deaths', 'HospitalBedsOccupied', 'VaccinationDosesAdministered', 'PositivityRate_Pct', 'AgeGroup_HighestImpact'
            ],
            'stock_market.csv': [
                'Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Volume', 'DailyReturn_Pct'
            ]
        }

    def validate_dataset_schema(self, filename):
        """Verifies dataset existence and column schema compliance."""
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.exists(filepath):
            return False, None, f"File {filename} does not exist."

        df = pd.read_csv(filepath)
        expected_cols = self.schemas.get(filename, [])
        missing_cols = [c for c in expected_cols if c not in df.columns]

        if missing_cols:
            return False, df, f"Missing columns in {filename}: {missing_cols}"
        return True, df, f"Schema valid for {filename}."

    def check_data_quality_metrics(self, df):
        """Calculates duplicate count, missing percentage, and negative value checks for numeric fields."""
        dup_count = df.duplicated().sum()
        null_counts = df.isnull().sum().to_dict()
        numeric_cols = df.select_dtypes(include=['number']).columns

        negatives = {}
        for col in numeric_cols:
            negatives[col] = int((df[col] < 0).sum())

        return {
            'duplicate_count': int(dup_count),
            'null_counts': null_counts,
            'negative_value_counts': negatives,
            'total_rows': len(df)
        }

    def run_full_validation_suite(self):
        """Runs validation checks across all datasets in data/ and enforces strict rules."""
        results = {}
        all_passed = True
        
        for filename in self.schemas.keys():
            valid_schema, df, msg = self.validate_dataset_schema(filename)
            if not valid_schema:
                results[filename] = {'valid': False, 'message': msg}
                all_passed = False
                continue
                
            metrics = self.check_data_quality_metrics(df)
            total_rows = metrics['total_rows']
            
            # Strict Rule 1: No duplicates
            if metrics['duplicate_count'] > 0:
                results[filename] = {'valid': False, 'message': f"Failed: Found {metrics['duplicate_count']} duplicate rows."}
                all_passed = False
                continue
                
            # Strict Rule 2: No negatives in specific domains where impossible
            has_negative = False
            for col, count in metrics['negative_value_counts'].items():
                if count > 0:
                    # Allow negative returns in finance
                    if filename == 'stock_market.csv' and col == 'DailyReturn_Pct':
                        continue
                    # Allow negative temperatures in weather
                    if filename == 'weather_data.csv' and col == 'Temperature_C':
                        continue
                        
                    has_negative = True
                    results[filename] = {'valid': False, 'message': f"Failed: Found {count} impossible negative values in column {col}."}
                    all_passed = False
                    break
            if has_negative: continue
            
            # Strict Rule 3: Missing values must not exceed 5% (unless explicitly justified like rainfall)
            has_excess_missing = False
            for col, count in metrics['null_counts'].items():
                pct_missing = (count / total_rows) * 100
                if pct_missing > 5.0:
                    if filename == 'weather_data.csv' and col in ['Rainfall_mm', 'ExtremeEvent']:
                        continue # Valid domain exception: missing = no rain / no extreme event
                    
                    has_excess_missing = True
                    results[filename] = {'valid': False, 'message': f"Failed: Column {col} has {pct_missing:.1f}% missing values (threshold is 5%)."}
                    all_passed = False
                    break
            if has_excess_missing: continue
            
            # Strict Rule 4: Logical Data Bounds
            if filename == 'stock_market.csv':
                invalid_bounds = df[
                    (df['High'] < df['Low']) |
                    (df['High'] < df['Open']) |
                    (df['High'] < df['Close']) |
                    (df['Low'] > df['Open']) |
                    (df['Low'] > df['Close']) |
                    (df['Volume'] < 0)
                ]
                if len(invalid_bounds) > 0:
                    results[filename] = {'valid': False, 'message': f"Failed: Found {len(invalid_bounds)} rows with logical price/volume errors."}
                    all_passed = False
                    continue
                    
            if filename == 'supermarket_sales.csv':
                invalid_bounds = df[
                    (df['Quantity'] <= 0) |
                    (df['Unit_Price'] <= 0) |
                    (df['Tax'] < 0) |
                    (df['Total'] < 0) |
                    (df['Rating'] < 1) |
                    (df['Rating'] > 10)
                ]
                if len(invalid_bounds) > 0:
                    results[filename] = {'valid': False, 'message': f"Failed: Found {len(invalid_bounds)} rows with logical retail bound errors."}
                    all_passed = False
                    continue

            results[filename] = {'valid': True, 'message': f"Passed validation ({total_rows} rows)."}
            
        return all_passed, results

if __name__ == '__main__':
    validator = DataValidator()
    passed, res = validator.run_full_validation_suite()
    print("Validation Status:", passed)
    for fname, details in res.items():
        print(f" - {fname}: {details['message']}")
