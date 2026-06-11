"""
FUTURE INTERNS - Task 1: Sales & Demand Forecasting for Businesses
Author: Future Intern
Date: June 11, 2026

This module implements revenue forecasting using Random Forest and XGBoost models.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb
import joblib
import warnings
warnings.filterwarnings('ignore')


class RevenueForecastingModel:
    """
    Revenue Forecasting Model using Random Forest and XGBoost
    
    This class handles:
    - Feature engineering
    - Model training and comparison
    - Forecasting future revenue
    - Model evaluation
    """
    
    def __init__(self, data_path=None, df=None):
        """
        Initialize the forecasting model
        
        Args:
            data_path (str): Path to revenue dataset CSV
            df (pd.DataFrame): DataFrame with revenue data (alternative to data_path)
        """
        if df is not None:
            self.df = df.copy()
        elif data_path:
            self.df = pd.read_csv(data_path)
        else:
            raise ValueError("Either data_path or df must be provided")
        
        self.model_rf = None
        self.model_xgb = None
        self.best_model = None
        self.best_model_name = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.feature_names = None
        self.evaluation_results = {}
        
        print("✓ RevenueForecastingModel initialized")
        print(f"  Dataset shape: {self.df.shape}")
    
    def prepare_data(self, date_column='Date', target_column='Revenue'):
        """
        Prepare data with time-based feature engineering
        
        Args:
            date_column (str): Name of the date column
            target_column (str): Name of the target column (Revenue)
        
        Returns:
            pd.DataFrame: Prepared dataframe with engineered features
        """
        print("\n" + "="*70)
        print("STEP 1: DATA PREPARATION & FEATURE ENGINEERING")
        print("="*70)
        
        # Convert date column to datetime
        self.df[date_column] = pd.to_datetime(self.df[date_column])
        self.df = self.df.sort_values(date_column).reset_index(drop=True)
        
        print(f"\n✓ Date range: {self.df[date_column].min()} to {self.df[date_column].max()}")
        print(f"✓ Total records: {len(self.df)}")
        
        # Feature Engineering
        print("\n--- Time-Based Feature Engineering ---")
        self.df['Year'] = self.df[date_column].dt.year
        self.df['Month'] = self.df[date_column].dt.month
        self.df['Day'] = self.df[date_column].dt.day
        self.df['DayOfWeek'] = self.df[date_column].dt.dayofweek  # Monday=0, Sunday=6
        self.df['Quarter'] = self.df[date_column].dt.quarter
        
        # Additional useful features
        self.df['DayOfYear'] = self.df[date_column].dt.dayofyear
        self.df['WeekOfYear'] = self.df[date_column].dt.isocalendar().week
        self.df['IsWeekend'] = (self.df['DayOfWeek'] >= 5).astype(int)
        self.df['IsMonthStart'] = self.df[date_column].dt.is_month_start.astype(int)
        self.df['IsMonthEnd'] = self.df[date_column].dt.is_month_end.astype(int)
        
        # Cyclical encoding for better pattern recognition
        self.df['Month_Sin'] = np.sin(2 * np.pi * self.df['Month'] / 12)
        self.df['Month_Cos'] = np.cos(2 * np.pi * self.df['Month'] / 12)
        self.df['DayOfWeek_Sin'] = np.sin(2 * np.pi * self.df['DayOfWeek'] / 7)
        self.df['DayOfWeek_Cos'] = np.cos(2 * np.pi * self.df['DayOfWeek'] / 7)
        
        print("✓ Features created:")
        print("  - Year, Month, Day, DayOfWeek, Quarter")
        print("  - DayOfYear, WeekOfYear")
        print("  - IsWeekend, IsMonthStart, IsMonthEnd")
        print("  - Cyclical encodings (Month_Sin/Cos, DayOfWeek_Sin/Cos)")
        
        self.date_column = date_column
        self.target_column = target_column
        
        return self.df
    
    def split_data(self, test_days=30):
        """
        Split data chronologically into train and test sets
        Last 'test_days' days are used as test data
        
        Args:
            test_days (int): Number of days to use as test data
        
        Returns:
            tuple: (X_train, X_test, y_train, y_test)
        """
        print("\n" + "="*70)
        print("STEP 2: DATA SPLITTING (CHRONOLOGICAL)")
        print("="*70)
        
        # Sort by date to ensure chronological split
        self.df = self.df.sort_values(self.date_column).reset_index(drop=True)
        
        # Calculate split point
        total_records = len(self.df)
        split_index = total_records - test_days
        
        print(f"\n✓ Total records: {total_records}")
        print(f"✓ Training records: {split_index} ({split_index/total_records*100:.1f}%)")
        print(f"✓ Test records: {test_days} ({test_days/total_records*100:.1f}%)")
        
        # Split data
        train_data = self.df.iloc[:split_index]
        test_data = self.df.iloc[split_index:]
        
        print(f"\n✓ Training period: {train_data[self.date_column].min()} to {train_data[self.date_column].max()}")
        print(f"✓ Test period: {test_data[self.date_column].min()} to {test_data[self.date_column].max()}")
        
        # Select features (exclude date and target)
        feature_columns = [col for col in self.df.columns 
                          if col not in [self.date_column, self.target_column]]
        
        self.feature_names = feature_columns
        
        self.X_train = train_data[feature_columns]
        self.X_test = test_data[feature_columns]
        self.y_train = train_data[self.target_column]
        self.y_test = test_data[self.target_column]
        
        print(f"\n✓ Feature count: {len(feature_columns)}")
        print(f"✓ Features: {feature_columns[:5]}... (showing first 5)")
        
        return self.X_train, self.X_test, self.y_train, self.y_test
    
    def train_models(self):
        """
        Train both Random Forest and XGBoost models
        
        Returns:
            dict: Training results for both models
        """
        print("\n" + "="*70)
        print("STEP 3: MODEL TRAINING")
        print("="*70)
        
        # Train Random Forest
        print("\n--- Training Random Forest Regressor ---")
        self.model_rf = RandomForestRegressor(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1,
            verbose=0
        )
        self.model_rf.fit(self.X_train, self.y_train)
        print("✓ Random Forest trained successfully")
        
        # Train XGBoost
        print("\n--- Training XGBoost Regressor ---")
        self.model_xgb = xgb.XGBRegressor(
            n_estimators=200,
            max_depth=8,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            n_jobs=-1,
            verbosity=0
        )
        self.model_xgb.fit(self.X_train, self.y_train)
        print("✓ XGBoost trained successfully")
        
        return {'rf': self.model_rf, 'xgb': self.model_xgb}
    
    def evaluate_models(self):
        """
        Evaluate both models and select the best one
        
        Returns:
            dict: Evaluation metrics for both models
        """
        print("\n" + "="*70)
        print("STEP 4: MODEL EVALUATION")
        print("="*70)
        
        results = {}
        
        # Evaluate Random Forest
        print("\n--- Random Forest Performance ---")
        y_pred_rf = self.model_rf.predict(self.X_test)
        results['Random Forest'] = self._calculate_metrics(self.y_test, y_pred_rf)
        self._print_metrics('Random Forest', results['Random Forest'])
        
        # Evaluate XGBoost
        print("\n--- XGBoost Performance ---")
        y_pred_xgb = self.model_xgb.predict(self.X_test)
        results['XGBoost'] = self._calculate_metrics(self.y_test, y_pred_xgb)
        self._print_metrics('XGBoost', results['XGBoost'])
        
        # Select best model based on R² score
        print("\n" + "="*70)
        if results['Random Forest']['R2'] > results['XGBoost']['R2']:
            self.best_model = self.model_rf
            self.best_model_name = 'Random Forest'
        else:
            self.best_model = self.model_xgb
            self.best_model_name = 'XGBoost'
        
        print(f"🏆 BEST MODEL: {self.best_model_name}")
        print(f"   R² Score: {results[self.best_model_name]['R2']:.4f}")
        print("="*70)
        
        self.evaluation_results = results
        return results
    
    def _calculate_metrics(self, y_true, y_pred):
        """
        Calculate evaluation metrics
        
        Args:
            y_true: Actual values
            y_pred: Predicted values
        
        Returns:
            dict: Dictionary of metrics
        """
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        r2 = r2_score(y_true, y_pred)
        
        # Calculate MAPE (Mean Absolute Percentage Error)
        mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        
        return {
            'MAE': mae,
            'RMSE': rmse,
            'R2': r2,
            'MAPE': mape,
            'predictions': y_pred
        }
    
    def _print_metrics(self, model_name, metrics):
        """Print evaluation metrics in a formatted way"""
        print(f"  MAE:  ${metrics['MAE']:,.2f}")
        print(f"  RMSE: ${metrics['RMSE']:,.2f}")
        print(f"  R²:   {metrics['R2']:.4f}")
        print(f"  MAPE: {metrics['MAPE']:.2f}%")
    
    def forecast_future(self, periods=30):
        """
        Forecast revenue for future periods
        
        Args:
            periods (int): Number of days to forecast
        
        Returns:
            pd.DataFrame: Dataframe with forecasted values
        """
        print("\n" + "="*70)
        print(f"STEP 5: FORECASTING NEXT {periods} DAYS")
        print("="*70)
        
        # Get the last date in the dataset
        last_date = self.df[self.date_column].max()
        
        # Create future dates
        future_dates = pd.date_range(
            start=last_date + pd.Timedelta(days=1),
            periods=periods,
            freq='D'
        )
        
        # Create future dataframe with same features
        future_df = pd.DataFrame({self.date_column: future_dates})
        
        # Engineer features for future dates
        future_df['Year'] = future_df[self.date_column].dt.year
        future_df['Month'] = future_df[self.date_column].dt.month
        future_df['Day'] = future_df[self.date_column].dt.day
        future_df['DayOfWeek'] = future_df[self.date_column].dt.dayofweek
        future_df['Quarter'] = future_df[self.date_column].dt.quarter
        future_df['DayOfYear'] = future_df[self.date_column].dt.dayofyear
        future_df['WeekOfYear'] = future_df[self.date_column].dt.isocalendar().week
        future_df['IsWeekend'] = (future_df['DayOfWeek'] >= 5).astype(int)
        future_df['IsMonthStart'] = future_df[self.date_column].dt.is_month_start.astype(int)
        future_df['IsMonthEnd'] = future_df[self.date_column].dt.is_month_end.astype(int)
        future_df['Month_Sin'] = np.sin(2 * np.pi * future_df['Month'] / 12)
        future_df['Month_Cos'] = np.cos(2 * np.pi * future_df['Month'] / 12)
        future_df['DayOfWeek_Sin'] = np.sin(2 * np.pi * future_df['DayOfWeek'] / 7)
        future_df['DayOfWeek_Cos'] = np.cos(2 * np.pi * future_df['DayOfWeek'] / 7)
        
        # Make predictions using the best model
        X_future = future_df[self.feature_names]
        future_predictions = self.best_model.predict(X_future)
        
        # Create results dataframe
        forecast_results = pd.DataFrame({
            'Date': future_dates,
            'Forecasted_Revenue': future_predictions
        })
        
        print(f"\n✓ Forecast generated for {periods} days")
        print(f"✓ Forecast period: {future_dates[0].date()} to {future_dates[-1].date()}")
        print(f"\n📊 Forecast Summary:")
        print(f"   Mean daily revenue: ${future_predictions.mean():,.2f}")
        print(f"   Total forecasted: ${future_predictions.sum():,.2f}")
        print(f"   Min: ${future_predictions.min():,.2f}")
        print(f"   Max: ${future_predictions.max():,.2f}")
        
        self.forecast_results = forecast_results
        return forecast_results
    
    def get_feature_importance(self):
        """
        Get feature importance from the best model
        
        Returns:
            pd.DataFrame: Feature importance dataframe
        """
        if hasattr(self.best_model, 'feature_importances_'):
            importance_df = pd.DataFrame({
                'Feature': self.feature_names,
                'Importance': self.best_model.feature_importances_
            }).sort_values('Importance', ascending=False)
            
            return importance_df
        else:
            print("Model does not have feature_importances_ attribute")
            return None
    
    def save_model(self, filepath='models/trained_model.pkl'):
        """
        Save the best trained model
        
        Args:
            filepath (str): Path to save the model
        """
        joblib.dump(self.best_model, filepath)
        print(f"✓ Model saved to: {filepath}")
        print(f"   Model type: {self.best_model_name}")
    
    def save_evaluation_metrics(self, filepath='outputs/evaluation_metrics.txt'):
        """
        Save evaluation metrics to a text file
        
        Args:
            filepath (str): Path to save the metrics
        """
        with open(filepath, 'w') as f:
            f.write("="*70 + "\n")
            f.write("MODEL EVALUATION METRICS\n")
            f.write("Future Interns - Task 1: Sales & Demand Forecasting\n")
            f.write("="*70 + "\n\n")
            
            for model_name, metrics in self.evaluation_results.items():
                f.write(f"\n{model_name}:\n")
                f.write("-"*40 + "\n")
                f.write(f"  MAE:  ${metrics['MAE']:,.2f}\n")
                f.write(f"  RMSE: ${metrics['RMSE']:,.2f}\n")
                f.write(f"  R²:   {metrics['R2']:.4f}\n")
                f.write(f"  MAPE: {metrics['MAPE']:.2f}%\n")
            
            f.write("\n" + "="*70 + "\n")
            f.write(f"BEST MODEL: {self.best_model_name}\n")
            f.write(f"R² Score: {self.evaluation_results[self.best_model_name]['R2']:.4f}\n")
            f.write("="*70 + "\n")
        
        print(f"✓ Evaluation metrics saved to: {filepath}")


# Example usage
if __name__ == "__main__":
    print("Revenue Forecasting Model Module")
    print("This module is designed to be imported and used by the main script")
