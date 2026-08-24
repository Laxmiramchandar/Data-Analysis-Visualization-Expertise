import os
import pandas as pd
import numpy as np

class DataLoader:
    """
    Data Loading, Preprocessing & Quality Assurance Module
    """

    def __init__(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Dataset file not found: {filepath}")
        self.filepath = filepath
        self.raw_df = None
        self.df = None

    def load_data(self):
        """Loads dataset from CSV file."""
        self.raw_df = pd.read_csv(self.filepath)
        self.df = self.raw_df.copy()
        return self.df
        
    def load_data_optimized(self, chunksize=None, category_cols=None):
        """Loads dataset optimized for memory (Point 11)."""
        if chunksize:
            # Return an iterator for chunk processing
            return pd.read_csv(self.filepath, chunksize=chunksize)
            
        self.raw_df = pd.read_csv(self.filepath)
        self.df = self.raw_df.copy()
        
        # Optimize memory by downcasting and using categories
        if category_cols:
            for col in category_cols:
                if col in self.df.columns:
                    self.df[col] = self.df[col].astype('category')
                    
        return self.df

    def explore(self):
        """Returns comprehensive summary of missing values, dtypes, and statistics."""
        if self.df is None:
            self.load_data()
        
        info = {
            'shape': self.df.shape,
            'columns': list(self.df.columns),
            'dtypes': self.df.dtypes.to_dict(),
            'missing_values': self.df.isnull().sum().to_dict(),
            'duplicate_rows': int(self.df.duplicated().sum())
        }
        return info

    def generate_data_quality_report(self):
        """Generates a text report for Data Quality (Point 3)."""
        if self.df is None:
            self.load_data()
            
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df)) * 100
        dupes = self.df.duplicated().sum()
        
        report = []
        report.append("DATA QUALITY CHECK")
        report.append("-" * 18)
        report.append(f"Rows: {self.df.shape[0]:,}")
        report.append(f"Columns: {self.df.shape[1]}")
        report.append("\nMissing values:")
        
        for col in self.df.columns:
            if missing[col] > 0:
                report.append(f"{col:<20} {missing[col]:<5} ({missing_pct[col]:.1f}%)")
            else:
                report.append(f"{col:<20} 0")
                
        report.append(f"\nDuplicates: {dupes}")
        
        # Add basic outlier count using IQR for numeric cols
        total_outliers = 0
        for col in self.df.select_dtypes(include=np.number).columns:
            outliers = self.detect_outliers_iqr(col)
            total_outliers += outliers.sum()
            
        report.append(f"Numeric Outliers: {total_outliers}")
        
        return "\n".join(report)

    def clean_missing_values(self, strategy_map=None):
        """
        Cleans missing values based on custom column strategy map.
        (Fixes Point 2: Does not blindly fill all numerics with median).
        """
        if self.df is None:
            self.load_data()

        if strategy_map is None:
            strategy_map = {}

        for col in self.df.columns:
            if self.df[col].isnull().sum() > 0:
                if col in strategy_map:
                    strat = strategy_map[col]
                    if strat == 'mean':
                        self.df[col] = self.df[col].fillna(self.df[col].mean())
                    elif strat == 'median':
                        self.df[col] = self.df[col].fillna(self.df[col].median())
                    elif strat == 'mode':
                        self.df[col] = self.df[col].fillna(self.df[col].mode()[0])
                    elif isinstance(strat, (int, float, str)):
                        self.df[col] = self.df[col].fillna(strat)
                else:
                    # Default safe behavior: do nothing if not specified in strategy map
                    pass

        return self.df

    def detect_outliers_iqr(self, column, factor=1.5):
        """Detects outliers using IQR (Interquartile Range) method."""
        if column not in self.df.columns or not pd.api.types.is_numeric_dtype(self.df[column]):
            return pd.Series([False] * len(self.df))

        q1 = self.df[column].quantile(0.25)
        q3 = self.df[column].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - factor * iqr
        upper_bound = q3 + factor * iqr
        return (self.df[column] < lower_bound) | (self.df[column] > upper_bound)

    def parse_dates(self, date_columns):
        """Parses specified date columns to datetime dtypes."""
        for col in date_columns:
            if col in self.df.columns:
                self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
        return self.df
