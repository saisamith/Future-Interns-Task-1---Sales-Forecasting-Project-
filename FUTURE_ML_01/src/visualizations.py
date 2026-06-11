"""
FUTURE INTERNS - Task 1: Visualization Module
Author: Future Intern
Date: June 11, 2026

This module creates all required visualizations for the forecasting project.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 6)
plt.rcParams['font.size'] = 10


class ForecastVisualizer:
    """
    Creates visualizations for revenue forecasting analysis
    """
    
    def __init__(self, model):
        """
        Initialize visualizer with trained model
        
        Args:
            model: Trained RevenueForecastingModel instance
        """
        self.model = model
        print("✓ ForecastVisualizer initialized")
    
    def plot_actual_vs_predicted(self, save_path='images/actual_vs_predicted.png'):
        """
        Plot actual vs predicted revenue for test set
        
        Args:
            save_path (str): Path to save the plot
        """
        print("\n--- Generating Actual vs Predicted Plot ---")
        
        # Get predictions for test set
        y_pred = self.model.best_model.predict(self.model.X_test)
        y_true = self.model.y_test
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # Plot 1: Scatter plot
        axes[0].scatter(y_true, y_pred, alpha=0.6, color='#2E86AB', s=50, edgecolors='white', linewidth=0.5)
        
        # Perfect prediction line
        min_val = min(y_true.min(), y_pred.min())
        max_val = max(y_true.max(), y_pred.max())
        axes[0].plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Perfect Prediction')
        
        axes[0].set_xlabel('Actual Revenue ($)', fontsize=12, fontweight='bold')
        axes[0].set_ylabel('Predicted Revenue ($)', fontsize=12, fontweight='bold')
        axes[0].set_title(f'Actual vs Predicted Revenue\n{self.model.best_model_name} Model', 
                         fontsize=14, fontweight='bold', pad=15)
        axes[0].legend(loc='upper left', fontsize=10)
        axes[0].grid(True, alpha=0.3)
        
        # Add R² score as text
        r2 = self.model.evaluation_results[self.model.best_model_name]['R2']
        axes[0].text(0.05, 0.95, f'R² = {r2:.4f}', transform=axes[0].transAxes,
                    fontsize=12, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        # Plot 2: Time series comparison
        test_indices = range(len(y_true))
        axes[1].plot(test_indices, y_true.values, label='Actual', color='#2E86AB', linewidth=2, marker='o', markersize=4)
        axes[1].plot(test_indices, y_pred, label='Predicted', color='#D62828', linewidth=2, marker='s', markersize=4, linestyle='--')
        
        axes[1].set_xlabel('Test Sample Index', fontsize=12, fontweight='bold')
        axes[1].set_ylabel('Revenue ($)', fontsize=12, fontweight='bold')
        axes[1].set_title('Actual vs Predicted Revenue (Time Series)', fontsize=14, fontweight='bold', pad=15)
        axes[1].legend(loc='best', fontsize=10)
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Saved to: {save_path}")
    
    def plot_future_forecast(self, save_path='images/future_forecast.png'):
        """
        Plot 30-day future revenue forecast
        
        Args:
            save_path (str): Path to save the plot
        """
        print("\n--- Generating Future Forecast Plot ---")
        
        # Get historical data (last 60 days)
        historical_df = self.model.df[[self.model.date_column, self.model.target_column]].tail(60)
        forecast_df = self.model.forecast_results
        
        fig, ax = plt.subplots(figsize=(16, 7))
        
        # Plot historical data
        ax.plot(historical_df[self.model.date_column], 
               historical_df[self.model.target_column],
               label='Historical Revenue', color='#2E86AB', linewidth=2.5, marker='o', markersize=5)
        
        # Plot forecast
        ax.plot(forecast_df['Date'], 
               forecast_df['Forecasted_Revenue'],
               label='Forecasted Revenue', color='#D62828', linewidth=2.5, marker='s', markersize=5, linestyle='--')
        
        # Add forecast confidence band (simplified using std)
        forecast_std = forecast_df['Forecasted_Revenue'].std()
        ax.fill_between(forecast_df['Date'],
                        forecast_df['Forecasted_Revenue'] - forecast_std,
                        forecast_df['Forecasted_Revenue'] + forecast_std,
                        alpha=0.2, color='#D62828', label='Confidence Band (±1 Std Dev)')
        
        # Formatting
        ax.set_xlabel('Date', fontsize=13, fontweight='bold')
        ax.set_ylabel('Revenue ($)', fontsize=13, fontweight='bold')
        ax.set_title('30-Day Revenue Forecast\nHistorical Data + Future Predictions', 
                    fontsize=15, fontweight='bold', pad=20)
        ax.legend(loc='best', fontsize=11, framealpha=0.9)
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right')
        
        # Add vertical line separating historical and forecast
        last_historical_date = historical_df[self.model.date_column].iloc[-1]
        ax.axvline(x=last_historical_date, color='black', linestyle=':', linewidth=2, alpha=0.5, label='Forecast Start')
        
        # Add statistics box
        mean_forecast = forecast_df['Forecasted_Revenue'].mean()
        total_forecast = forecast_df['Forecasted_Revenue'].sum()
        stats_text = f'Forecast Statistics:\nMean Daily: ${mean_forecast:,.0f}\nTotal 30-Day: ${total_forecast:,.0f}'
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
               fontsize=10, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Saved to: {save_path}")
    
    def plot_feature_importance(self, top_n=15, save_path='images/feature_importance.png'):
        """
        Plot feature importance from the best model
        
        Args:
            top_n (int): Number of top features to show
            save_path (str): Path to save the plot
        """
        print("\n--- Generating Feature Importance Plot ---")
        
        importance_df = self.model.get_feature_importance()
        
        if importance_df is None:
            print("✗ Cannot generate feature importance plot")
            return
        
        # Get top N features
        top_features = importance_df.head(top_n)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Create horizontal bar plot
        colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(top_features)))
        bars = ax.barh(range(len(top_features)), top_features['Importance'], color=colors, edgecolor='white', linewidth=1.5)
        
        ax.set_yticks(range(len(top_features)))
        ax.set_yticklabels(top_features['Feature'], fontsize=11)
        ax.set_xlabel('Importance Score', fontsize=13, fontweight='bold')
        ax.set_title(f'Top {top_n} Feature Importance\n{self.model.best_model_name} Model', 
                    fontsize=15, fontweight='bold', pad=20)
        ax.grid(True, axis='x', alpha=0.3, linestyle='--')
        
        # Invert y-axis to show highest importance at top
        ax.invert_yaxis()
        
        # Add value labels on bars
        for i, (idx, row) in enumerate(top_features.iterrows()):
            ax.text(row['Importance'] + 0.005, i, f"{row['Importance']:.4f}", 
                   va='center', fontsize=9, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Saved to: {save_path}")
    
    def plot_forecast_confidence(self, save_path='images/forecast_confidence.png'):
        """
        Plot forecast with confidence intervals
        
        Args:
            save_path (str): Path to save the plot
        """
        print("\n--- Generating Forecast Confidence Visualization ---")
        
        forecast_df = self.model.forecast_results.copy()
        
        # Calculate confidence intervals (using bootstrap-like approach)
        # In production, you'd use quantile regression or prediction intervals
        mean_forecast = forecast_df['Forecasted_Revenue'].values
        std_forecast = forecast_df['Forecasted_Revenue'].std()
        
        # Create confidence bounds
        forecast_df['Lower_Bound_95'] = mean_forecast - 1.96 * std_forecast
        forecast_df['Upper_Bound_95'] = mean_forecast + 1.96 * std_forecast
        forecast_df['Lower_Bound_68'] = mean_forecast - 1.0 * std_forecast
        forecast_df['Upper_Bound_68'] = mean_forecast + 1.0 * std_forecast
        
        fig, ax = plt.subplots(figsize=(16, 8))
        
        # Plot forecast
        ax.plot(forecast_df['Date'], forecast_df['Forecasted_Revenue'],
               label='Forecasted Revenue', color='#2E86AB', linewidth=3, marker='o', markersize=6)
        
        # Plot 95% confidence interval
        ax.fill_between(forecast_df['Date'],
                        forecast_df['Lower_Bound_95'],
                        forecast_df['Upper_Bound_95'],
                        alpha=0.2, color='#D62828', label='95% Confidence Interval')
        
        # Plot 68% confidence interval
        ax.fill_between(forecast_df['Date'],
                        forecast_df['Lower_Bound_68'],
                        forecast_df['Upper_Bound_68'],
                        alpha=0.3, color='#F18F01', label='68% Confidence Interval')
        
        # Formatting
        ax.set_xlabel('Date', fontsize=13, fontweight='bold')
        ax.set_ylabel('Revenue ($)', fontsize=13, fontweight='bold')
        ax.set_title('30-Day Revenue Forecast with Confidence Intervals', 
                    fontsize=15, fontweight='bold', pad=20)
        ax.legend(loc='best', fontsize=11, framealpha=0.9)
        ax.grid(True, alpha=0.3, linestyle='--')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Saved to: {save_path}")
    
    def plot_model_comparison(self, save_path='images/model_comparison.png'):
        """
        Compare Random Forest and XGBoost performance
        
        Args:
            save_path (str): Path to save the plot
        """
        print("\n--- Generating Model Comparison Plot ---")
        
        results = self.model.evaluation_results
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        models = list(results.keys())
        metrics = ['MAE', 'RMSE', 'R2', 'MAPE']
        titles = ['Mean Absolute Error (Lower is Better)',
                 'Root Mean Squared Error (Lower is Better)',
                 'R² Score (Higher is Better)',
                 'MAPE % (Lower is Better)']
        colors = ['#4ECDC4', '#FF6B6B']
        
        for idx, (metric, title) in enumerate(zip(metrics, titles)):
            row = idx // 2
            col = idx % 2
            ax = axes[row, col]
            
            values = [results[model][metric] for model in models]
            bars = ax.bar(models, values, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
            
            ax.set_title(title, fontsize=12, fontweight='bold', pad=10)
            ax.set_ylabel(metric, fontsize=11, fontweight='bold')
            ax.grid(True, axis='y', alpha=0.3, linestyle='--')
            
            # Add value labels on bars
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{value:.2f}',
                       ha='center', va='bottom', fontsize=10, fontweight='bold')
            
            # Highlight best model
            if metric in ['MAE', 'RMSE', 'MAPE']:
                best_idx = values.index(min(values))
            else:
                best_idx = values.index(max(values))
            bars[best_idx].set_edgecolor('gold')
            bars[best_idx].set_linewidth(4)
        
        plt.suptitle('Model Performance Comparison\nRandom Forest vs XGBoost', 
                    fontsize=16, fontweight='bold', y=1.00)
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Saved to: {save_path}")
    
    def generate_all_visualizations(self):
        """
        Generate all required visualizations
        """
        print("\n" + "="*70)
        print("STEP 6: GENERATING VISUALIZATIONS")
        print("="*70)
        
        self.plot_actual_vs_predicted()
        self.plot_future_forecast()
        self.plot_feature_importance()
        self.plot_forecast_confidence()
        self.plot_model_comparison()
        
        print("\n✓ All visualizations generated successfully!")


# Example usage
if __name__ == "__main__":
    print("Forecast Visualization Module")
    print("This module is designed to be imported and used by the main script")
