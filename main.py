"""
Main Script - Complete Sales Forecasting Pipeline
Run this script to execute the entire forecasting workflow
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime

# Add src to path
sys.path.append(os.path.dirname(__file__))

from src.data_preprocessing import DataPreprocessor
from src.eda import EDA
from src.model_training import ModelTrainer
from src.forecasting import Forecaster


def create_sample_data(output_path='dataset/sample_sales_data.csv'):
    """
    Create sample sales dataset for demonstration
    
    Args:
        output_path (str): Path to save the sample dataset
    """
    print("\n" + "=" * 80)
    print("CREATING SAMPLE DATASET")
    print("=" * 80)
    
    np.random.seed(42)
    
    # Generate date range (2 years of daily data)
    dates = pd.date_range(start='2022-01-01', end='2023-12-31', freq='D')
    n_days = len(dates)
    
    # Products and categories
    products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
    categories = ['Electronics', 'Clothing', 'Food', 'Books', 'Toys']
    regions = ['North', 'South', 'East', 'West']
    stores = ['Store1', 'Store2', 'Store3', 'Store4', 'Store5']
    
    # Generate data with seasonality and trend
    data = []
    for i, date in enumerate(dates):
        # Add trend
        trend = i * 0.1
        
        # Add seasonality (weekly and yearly)
        weekly_seasonality = 50 * np.sin(2 * np.pi * i / 7)
        yearly_seasonality = 100 * np.sin(2 * np.pi * i / 365)
        
        # Base sales with noise
        base_sales = 200 + trend + weekly_seasonality + yearly_seasonality + np.random.normal(0, 30)
        
        # Generate multiple records per day
        for _ in range(np.random.randint(3, 8)):
            product = np.random.choice(products)
            category = categories[products.index(product)]
            units_sold = max(int(base_sales + np.random.normal(0, 50)), 10)
            price_per_unit = np.random.uniform(20, 100)
            revenue = units_sold * price_per_unit
            
            data.append({
                'Date': date,
                'Product_Name': product,
                'Category': category,
                'Units_Sold': units_sold,
                'Revenue': round(revenue, 2),
                'Region': np.random.choice(regions),
                'Store': np.random.choice(stores)
            })
    
    df = pd.DataFrame(data)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    
    print(f"\n✓ Sample dataset created: {len(df)} records")
    print(f"✓ Date range: {df['Date'].min()} to {df['Date'].max()}")
    print(f"✓ Saved to: {output_path}")
    
    return output_path


def run_complete_pipeline(data_path, target_column='Units_Sold', forecast_days=30):
    """
    Run the complete forecasting pipeline
    
    Args:
        data_path (str): Path to the dataset
        target_column (str): Target variable to predict
        forecast_days (int): Number of days to forecast
    """
    
    # Create output directories
    os.makedirs('output', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    
    print("\n" + "=" * 80)
    print("SALES & DEMAND FORECASTING PIPELINE")
    print("=" * 80)
    print(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Dataset: {data_path}")
    print(f"Target: {target_column}")
    print(f"Forecast Period: {forecast_days} days")
    
    # ===== STEP 1: Data Preprocessing =====
    print("\n" + "=" * 80)
    print("STEP 1: DATA PREPROCESSING")
    print("=" * 80)
    
    preprocessor = DataPreprocessor(data_path)
    df_clean = preprocessor.preprocess(date_column='Date', create_lags=False)
    preprocessor.save_processed_data('output/processed_data.csv')
    
    # ===== STEP 2: Exploratory Data Analysis =====
    print("\n" + "=" * 80)
    print("STEP 2: EXPLORATORY DATA ANALYSIS")
    print("=" * 80)
    
    eda = EDA(df_clean, date_column='Date')
    insights = eda.generate_all_visualizations(
        output_dir='output',
        value_column=target_column,
        revenue_column='Revenue'
    )
    
    # ===== STEP 3: Model Training =====
    print("\n" + "=" * 80)
    print("STEP 3: MODEL TRAINING")
    print("=" * 80)
    
    trainer = ModelTrainer(df_clean, target_column=target_column, date_column='Date')
    results = trainer.train_all_models()
    
    # Compare models
    comparison_df = trainer.compare_models(save_path='output/model_comparison.png')
    
    # Get best model
    best_model_name = comparison_df.loc[comparison_df['R² Score'].idxmax(), 'Model']
    
    # Plot predictions and feature importance
    trainer.plot_predictions(
        model_name=best_model_name,
        save_path=f'output/{best_model_name.replace(" ", "_")}_predictions.png'
    )
    
    if best_model_name in ['Random Forest', 'XGBoost']:
        trainer.get_feature_importance(
            model_name=best_model_name,
            top_n=15,
            save_path=f'output/{best_model_name.replace(" ", "_")}_feature_importance.png'
        )
    
    # Save best model
    trainer.save_model(
        best_model_name,
        f'models/{best_model_name.replace(" ", "_")}_model.pkl'
    )
    
    # ===== STEP 4: Time-Series Forecasting =====
    print("\n" + "=" * 80)
    print("STEP 4: TIME-SERIES FORECASTING")
    print("=" * 80)
    
    # Aggregate data by date for time-series forecasting
    df_ts = df_clean.groupby('Date')[target_column].sum().reset_index()
    
    # Prophet Forecast
    print("\n--- Prophet Forecasting ---")
    forecaster_prophet = Forecaster(df_ts, target_column=target_column, date_column='Date')
    forecast_prophet = forecaster_prophet.forecast_next_n_days(
        n_days=forecast_days,
        model='prophet',
        save_path='output/prophet_forecast.png'
    )
    
    if forecast_prophet is not None:
        forecaster_prophet.save_forecast(forecast_prophet, 'output/prophet_forecast.csv')
    
    # ARIMA Forecast
    print("\n--- ARIMA Forecasting ---")
    forecaster_arima = Forecaster(df_ts, target_column=target_column, date_column='Date')
    forecast_arima = forecaster_arima.forecast_next_n_days(
        n_days=forecast_days,
        model='arima',
        save_path='output/arima_forecast.png'
    )
    
    if forecast_arima is not None:
        forecaster_arima.save_forecast(forecast_arima, 'output/arima_forecast.csv')
    
    # Compare forecasts
    if forecast_prophet is not None and forecast_arima is not None:
        forecaster_prophet.compare_forecasts(
            arima_forecast=forecast_arima,
            prophet_forecast=forecast_prophet,
            save_path='output/forecast_comparison.png'
        )
    
    # ===== STEP 5: Generate Summary Report =====
    print("\n" + "=" * 80)
    print("SUMMARY REPORT")
    print("=" * 80)
    
    summary = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'dataset': {
            'path': data_path,
            'total_records': len(df_clean),
            'date_range': f"{df_clean['Date'].min()} to {df_clean['Date'].max()}",
            'total_revenue': df_clean['Revenue'].sum() if 'Revenue' in df_clean.columns else 0,
            'total_units_sold': df_clean[target_column].sum()
        },
        'best_model': {
            'name': best_model_name,
            'test_r2': results[best_model_name]['test_r2'],
            'test_mae': results[best_model_name]['test_mae'],
            'test_rmse': results[best_model_name]['test_rmse']
        },
        'forecast': {
            'periods': forecast_days,
            'prophet_mean': forecast_prophet['Forecast'].mean() if forecast_prophet is not None else 0,
            'arima_mean': forecast_arima['Forecast'].mean() if forecast_arima is not None else 0
        },
        'insights': insights
    }
    
    print("\n📊 DATASET SUMMARY:")
    print(f"  Total Records: {summary['dataset']['total_records']:,}")
    print(f"  Date Range: {summary['dataset']['date_range']}")
    print(f"  Total Revenue: ${summary['dataset']['total_revenue']:,.2f}")
    print(f"  Total Units Sold: {summary['dataset']['total_units_sold']:,.0f}")
    
    print("\n🤖 BEST MODEL:")
    print(f"  Name: {summary['best_model']['name']}")
    print(f"  Test R² Score: {summary['best_model']['test_r2']:.4f}")
    print(f"  Test MAE: {summary['best_model']['test_mae']:.2f}")
    print(f"  Test RMSE: {summary['best_model']['test_rmse']:.2f}")
    
    print(f"\n🔮 FORECAST ({forecast_days} days):")
    if forecast_prophet is not None:
        print(f"  Prophet Average: {summary['forecast']['prophet_mean']:.2f} units/day")
        print(f"  Prophet Total: {forecast_prophet['Forecast'].sum():.0f} units")
    if forecast_arima is not None:
        print(f"  ARIMA Average: {summary['forecast']['arima_mean']:.2f} units/day")
        print(f"  ARIMA Total: {forecast_arima['Forecast'].sum():.0f} units")
    
    print("\n📈 KEY INSIGHTS:")
    for i, insight in enumerate(insights, 1):
        print(f"  {i}. {insight}")
    
    print("\n📁 OUTPUT FILES:")
    print("  - output/processed_data.csv")
    print("  - output/monthly_sales_trend.png")
    print("  - output/revenue_analysis.html")
    print("  - output/product_demand.png")
    print("  - output/correlation_heatmap.png")
    print("  - output/seasonal_patterns.png")
    print("  - output/model_comparison.png")
    print(f"  - output/{best_model_name.replace(' ', '_')}_predictions.png")
    print("  - output/prophet_forecast.png")
    print("  - output/prophet_forecast.csv")
    print("  - output/arima_forecast.png")
    print("  - output/arima_forecast.csv")
    print("  - output/forecast_comparison.png")
    print(f"  - models/{best_model_name.replace(' ', '_')}_model.pkl")
    
    # Save summary to JSON
    import json
    with open('output/summary_report.json', 'w') as f:
        json.dump(summary, f, indent=2, default=str)
    print("  - output/summary_report.json")
    
    print("\n" + "=" * 80)
    print("PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print("\nNext Steps:")
    print("  1. Review visualizations in the 'output' folder")
    print("  2. Check model performance metrics")
    print("  3. Analyze forecasts for business planning")
    print("  4. Run the Streamlit app: streamlit run app/streamlit_app.py")
    print("  5. Explore the Jupyter notebook: notebooks/sales_forecasting_demo.ipynb")
    
    return summary


def main():
    """
    Main execution function
    """
    print("\n" + "=" * 80)
    print("SALES & DEMAND FORECASTING SYSTEM")
    print("=" * 80)
    
    # Check if sample data exists
    sample_data_path = 'dataset/sample_sales_data.csv'
    
    if not os.path.exists(sample_data_path):
        print("\n⚠ Sample dataset not found. Creating one...")
        create_sample_data(sample_data_path)
    else:
        print(f"\n✓ Using existing dataset: {sample_data_path}")
    
    # Run the complete pipeline
    try:
        summary = run_complete_pipeline(
            data_path=sample_data_path,
            target_column='Units_Sold',
            forecast_days=30
        )
        
        print("\n✅ All tasks completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during execution: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
