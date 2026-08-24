import os
import sys
import unittest
import pandas as pd
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_loader import DataLoader
from src.statistical_analysis import StatisticalAnalyzer
from src.visualization import Visualizer
from src.pdf_generator import ReportGenerator
from src.data_validation import DataValidator

class TestDataPipeline(unittest.TestCase):

    def test_01_all_datasets_present(self):
        """Test that all required datasets exist in data directory."""
        data_dir = 'data'
        expected_files = [
            'supermarket_sales.csv', 'house_prices.csv',
            'student_performance.csv', 'weather_data.csv',
            'healthcare_covid.csv', 'stock_market.csv'
        ]
        for f in expected_files:
            self.assertTrue(os.path.exists(os.path.join(data_dir, f)), f"Missing dataset: {f}")

    def test_02_data_validator_full(self):
        """Test strict validation suite asserting all datasets exist and pass schema checks."""
        validator = DataValidator(data_dir='data')
        all_passed, results = validator.run_full_validation_suite()
        self.assertTrue(all_passed, "Validation should pass for the fully cleaned and fixed datasets.")
        self.assertTrue(results['supermarket_sales.csv']['valid'], "Retail data should pass strict validation.")
        self.assertEqual(len(results), 6)

    def test_03_statistical_analyzer(self):
        """Test statistical calculations on supermarket sales and house prices."""
        df_sales = pd.read_csv('data/supermarket_sales.csv')
        stats_s = StatisticalAnalyzer(df_sales)
        desc = stats_s.descriptive_stats(['Total', 'Unit_Price', 'Quantity', 'Rating'])
        self.assertIn('mean', desc.columns)

        df_houses = pd.read_csv('data/house_prices.csv')
        stats_h = StatisticalAnalyzer(df_houses)
        corr = stats_h.correlation_matrix(['Price', 'Area', 'Bedrooms', 'Age'])
        self.assertIn('Price', corr.columns)

    def test_04_visualizer_generation(self):
        """Test chart generation."""
        df_houses = pd.read_csv('data/house_prices.csv')
        viz = Visualizer(output_dir='visualizations')
        img_path = viz.plot_scatter_with_regression(df_houses, 'Area', 'Price', 'Location', 'Area vs Price', 'Area', 'Price', 'test_data_validation_plot.png')
        self.assertTrue(os.path.exists(img_path))

    def test_05_pdf_report_generator(self):
        """Test PDF report compilation engine."""
        pdf_gen = ReportGenerator(output_dir='reports')
        filepath = pdf_gen.generate_project_report(
            title="Data Folder Validation Report",
            domain_name="Dataset Verification",
            filename="Test_Dataset_Validation_Report.pdf",
            executive_summary="Unit test verifying all datasets present in data directory.",
            kpi_data=[["Datasets Present", "6 Files", "100% verified"]],
            insights=["All dataset files confirmed present in data/."],
            recommendations=["Maintain full dataset availability."],
            image_paths=[]
        )
        
    def test_06_missing_value_handling(self):
        """Test the custom strategy map for missing values."""
        df = pd.DataFrame({
            'numeric_col': [1.0, np.nan, 3.0],
            'categorical_col': ['A', np.nan, 'C'],
            'zero_fill_col': [5.0, np.nan, 7.0]
        })
        # Save temp csv to use DataLoader
        df.to_csv('temp_test.csv', index=False)
        dl = DataLoader('temp_test.csv')
        dl.load_data()
        
        # Test custom map
        dl.clean_missing_values(strategy_map={
            'numeric_col': 'median',
            'categorical_col': 'mode',
            'zero_fill_col': 0.0
        })
        
        self.assertEqual(dl.df['numeric_col'].iloc[1], 2.0)
        self.assertEqual(dl.df['zero_fill_col'].iloc[1], 0.0)
        os.remove('temp_test.csv')

    def test_07_outlier_detection(self):
        """Test IQR outlier detection math."""
        df = pd.DataFrame({'val': [10, 12, 11, 100, 13, 9, 10]}) # 100 is outlier
        df.to_csv('temp_outlier.csv', index=False)
        dl = DataLoader('temp_outlier.csv')
        dl.load_data()
        outliers = dl.detect_outliers_iqr('val')
        self.assertTrue(outliers.iloc[3])
        self.assertFalse(outliers.iloc[0])
        os.remove('temp_outlier.csv')

    def test_08_advanced_statistics(self):
        """Test Sharpe Ratio and Drawdown calculations."""
        df = pd.DataFrame({'returns': [1.0, -0.5, 2.0, -1.0, 1.5], 'price': [100, 110, 90, 120, 115]})
        stats = StatisticalAnalyzer(df)
        
        sharpe = stats.calculate_sharpe_ratio('returns')
        self.assertIsInstance(sharpe, float)
        
        drawdown = stats.calculate_max_drawdown('price')
        self.assertTrue(drawdown < 0) # price went from 110 to 90, so drawdown is ~-18%

    def test_09_hypothesis_testing(self):
        """Test Pearson correlation and T-test output format."""
        df = pd.DataFrame({
            'group': ['A', 'A', 'B', 'B', 'B'],
            'val': [10, 12, 20, 22, 25],
            'val2': [5, 6, 10, 11, 12]
        })
        stats = StatisticalAnalyzer(df)
        
        ttest = stats.two_sample_ttest('group', 'val', 'A', 'B')
        self.assertTrue('p_value' in ttest)
        
        pearson = stats.pearson_correlation_test('val', 'val2')
        self.assertTrue('p_value' in pearson)
        self.assertTrue(pearson['r_statistic'] > 0.9)

    def tearDown(self):
        """Clean up temporary test artifacts."""
        for test_file in ['visualizations/test_data_validation_plot.png', 'reports/Test_Dataset_Validation_Report.pdf']:
            if os.path.exists(test_file):
                os.remove(test_file)

if __name__ == '__main__':
    unittest.main()
