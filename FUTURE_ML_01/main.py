"""
FUTURE INTERNS - Task 1: Sales & Demand Forecasting for Businesses
Main Execution Script

Author: Future Intern
Date: June 11, 2026

This script executes the complete forecasting pipeline:
1. Data Preparation & Feature Engineering
2. Train-Test Split (Last 30 days as test)
3. Model Training (Random Forest & XGBoost)
4. Model Evaluation & Selection
5. Future Revenue Forecasting (30 days)
6. Visualization Generation
7. Business Insights Generation
8. Results Export
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.forecasting_model import RevenueForecastingModel
from src.visualizations import ForecastVisualizer
from src.business_insights import BusinessInsightsGenerator


def create_sample_revenue_data():
    """
    Create sample revenue dataset for demonstration
    This can be replaced with actual revenue data
    
    Returns:
        pd.DataFrame: Sample revenue dataset
    """
    print("\n" + "="*80)
    print("CREATING SAMPLE REVENUE DATASET")
    print("="*80)
    
    # Generate 1 year of daily revenue data
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    n_days = len(dates)
    
    # Create revenue with trends and seasonality
    trend = np.linspace(50000, 70000, n_days)  # Growing trend
    seasonality = 10000 * np.sin(2 * np.pi * np.arange(n_days) / 365)  # Yearly seasonality
    weekly_pattern = 5000 * np.sin(2 * np.pi * np.arange(n_days) / 7)  # Weekly pattern
    noise = np.random.normal(0, 3000, n_days)  # Random variation
    
    revenue = trend + seasonality + weekly_pattern + noise
    revenue = np.maximum(revenue, 30000)  # Minimum revenue floor
    
    df = pd.DataFrame({
        'Date': dates,
        'Revenue': revenue
    })
    
    print(f"✓ Sample dataset created: {len(df)} records")
    print(f"✓ Date range: {df['Date'].min()} to {df['Date'].max()}")
    print(f"✓ Revenue range: ${df['Revenue'].min():,.2f} to ${df['Revenue'].max():,.2f}")
    
    return df


def main():
    """
    Main execution function
    """
    print("\n" + "="*80)
    print("FUTURE INTERNS - TASK 1")
    print("Sales & Demand Forecasting for Businesses")
    print("="*80)
    print(f"Execution started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    # Create directories if they don't exist
    os.makedirs('dataset', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    os.makedirs('outputs', exist_ok=True)
    os.makedirs('images', exist_ok=True)
    
    try:
        # ===== STEP 0: Load or Create Dataset =====
        dataset_path = 'dataset/revenue_data.csv'
        
        if os.path.exists(dataset_path):
            print(f"\n✓ Loading existing dataset from: {dataset_path}")
            df = pd.read_csv(dataset_path)
        else:
            print(f"\n⚠ Dataset not found. Creating sample data...")
            df = create_sample_revenue_data()
            df.to_csv(dataset_path, index=False)
            print(f"✓ Sample dataset saved to: {dataset_path}")
        
        # ===== STEP 1: Initialize Model =====
        model = RevenueForecastingModel(df=df)
        
        # ===== STEP 2: Prepare Data with Feature Engineering =====
        model.prepare_data(date_column='Date', target_column='Revenue')
        
        # ===== STEP 3: Split Data (Last 30 days as test) =====
        model.split_data(test_days=30)
        
        # ===== STEP 4: Train Models =====
        model.train_models()
        
        # ===== STEP 5: Evaluate Models =====
        evaluation_results = model.evaluate_models()
        
        # ===== STEP 6: Forecast Future 30 Days =====
        forecast_results = model.forecast_future(periods=30)
        
        # ===== STEP 7: Generate Visualizations =====
        visualizer = ForecastVisualizer(model)
        visualizer.generate_all_visualizations()
        
        # ===== STEP 8: Generate Business Insights =====
        insights_generator = BusinessInsightsGenerator(model)
        insights_report = insights_generator.generate_all_insights()
        
        # ===== STEP 9: Save Results =====
        print("\n" + "="*70)
        print("STEP 8: SAVING RESULTS")
        print("="*70)
        
        # Save forecast results
        forecast_results.to_csv('outputs/forecast_results.csv', index=False)
        print("✓ Forecast results saved to: outputs/forecast_results.csv")
        
        # Save trained model
        model.save_model('models/trained_model.pkl')
        
        # Save evaluation metrics
        model.save_evaluation_metrics('outputs/evaluation_metrics.txt')
        
        # Save feature importance
        importance_df = model.get_feature_importance()
        if importance_df is not None:
            importance_df.to_csv('outputs/feature_importance.csv', index=False)
            print("✓ Feature importance saved to: outputs/feature_importance.csv")
        
        # ===== FINAL SUMMARY =====
        print("\n" + "="*80)
        print("EXECUTION COMPLETED SUCCESSFULLY!")
        print("="*80)
        
        print("\n📊 SUMMARY:")
        print(f"  Best Model: {model.best_model_name}")
        print(f"  R² Score: {evaluation_results[model.best_model_name]['R2']:.4f}")
        print(f"  MAPE: {evaluation_results[model.best_model_name]['MAPE']:.2f}%")
        print(f"  30-Day Forecast Total: ${forecast_results['Forecasted_Revenue'].sum():,.2f}")
        
        print("\n📁 OUTPUT FILES:")
        print("  ✓ outputs/forecast_results.csv")
        print("  ✓ outputs/evaluation_metrics.txt")
        print("  ✓ outputs/business_insights.txt")
        print("  ✓ outputs/feature_importance.csv")
        print("  ✓ models/trained_model.pkl")
        print("  ✓ images/actual_vs_predicted.png")
        print("  ✓ images/future_forecast.png")
        print("  ✓ images/feature_importance.png")
        print("  ✓ images/forecast_confidence.png")
        print("  ✓ images/model_comparison.png")
        
        print("\n✅ Task 1 completed! Ready for submission.")
        print("="*80)
        print(f"Execution finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        
    except Exception as e:
        print("\n" + "="*80)
        print("❌ ERROR OCCURRED")
        print("="*80)
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
