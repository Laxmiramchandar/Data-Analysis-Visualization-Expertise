import os
import glob

def cleanup_duplicates():
    print("Cleaning up old and duplicate files across notebooks/, reports/, and visualizations/...")

    # Allowed notebook files
    allowed_notebooks = {
        '01_supermarket_sales_trend_analysis.ipynb',
        '02_product_line_customer_behavior.ipynb',
        '03_house_prices_valuation_drivers.ipynb',
        '04_location_economics_property_age.ipynb',
        '05_multi_domain_comparative_stats.ipynb'
    }

    # Allowed report files
    allowed_reports = {
        'Project1_Supermarket_Sales_Trend_Report.pdf',
        'Project2_Product_Line_Customer_Behavior_Report.pdf',
        'Project3_House_Prices_Valuation_Report.pdf',
        'Project4_Location_Economics_Property_Age_Report.pdf',
        'Project5_Multi_Domain_Comparative_Stats_Report.pdf',
        'Portfolio_Summary_Report.pdf'
    }

    # Allowed visualization files
    allowed_visualizations = {
        'p1_daily_sales_trend.png', 'p1_city_branch_revenue.png', 'p1_hourly_sales_dist.png',
        'p2_product_line_revenue.png', 'p2_payment_customer_box.png', 'p2_rating_distribution.png',
        'p3_area_vs_price_scatter.png', 'p3_bedrooms_bathrooms_price.png', 'p3_feature_correlation_heatmap.png',
        'p4_location_price_bar.png', 'p4_property_age_vs_price.png', 'p4_price_per_sqft_location_box.png',
        'p5_retail_vs_realestate_dist.png', 'p5_statistical_ttest_bar.png', 'p5_cross_domain_heatmap.png'
    }

    # Clean notebooks
    for filepath in glob.glob('notebooks/*'):
        filename = os.path.basename(filepath)
        if filename not in allowed_notebooks:
            os.remove(filepath)
            print(f"Removed duplicate/old notebook: notebooks/{filename}")

    # Clean reports
    for filepath in glob.glob('reports/*'):
        filename = os.path.basename(filepath)
        if filename not in allowed_reports:
            os.remove(filepath)
            print(f"Removed duplicate/old report: reports/{filename}")

    # Clean visualizations
    for filepath in glob.glob('visualizations/*'):
        filename = os.path.basename(filepath)
        if filename not in allowed_visualizations:
            os.remove(filepath)
            print(f"Removed duplicate/old chart: visualizations/{filename}")

    print("\nCleaned Directory Status:")
    print("Notebooks:", sorted(os.listdir('notebooks')))
    print("Reports:", sorted(os.listdir('reports')))
    print("Visualizations:", sorted(os.listdir('visualizations')))

if __name__ == '__main__':
    cleanup_duplicates()
