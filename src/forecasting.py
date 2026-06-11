"""
Forecasting Module
Implements time-series forecasting using ARIMA and Prophet
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from prophet import Prophet
import warnings
warnings.filterwarnings('ignore')


class Forecaster:
    """
    Class to perform time-series forecasting
    """
    
    def __init__(self, df, target_column='Units_Sold', date_column='Date'):
        """
        Initialize forecaster
        
        Args:
            df (pd.DataFrame): Time-series dataframe
            target_column (str): Column to forecast
            date_column (str): Date column name
        """
        self.df = df.copy()
        self.target_column = target_column
        self.date_column = date_column
        self.arima_model = None
        self.prophet_model = None
        self.forecast_df = None
        
        # Ensure date column is datetime
        if not pd.api.types.is_datetime64_any_dtype(self.df[date_column]):
            self.df[date_column] = pd.to_datetime(self.df[date_column])
        
        self.df = self.df.sort_values(date_column).reset_index(drop=True)
    
    def check_stationarity(self):
        """
        Check if time series is stationary using Augmented Dickey-Fuller test
        
        Returns:
            bool: True if stationary, False otherwise
        """
        print("\n--- Checking Stationarity (ADF Test) ---")
        
        result = adfuller(self.df[self.target_column].dropna())
        
        print(f"ADF Statistic: {result[0]:.4f}")
        print(f"p-value: {result[1]:.4f}")
        print(f"Critical Values:")
        for key, value in result[4].items():
            print(f"  {key}: {value:.4f}")
        
        is_stationary = result[1] < 0.05
        
        if is_stationary:
            print("✓ Series is STATIONARY (p-value < 0.05)")
        else:
            print("⚠ Series is NON-STATIONARY (p-value >= 0.05)")
            print("  Consider differencing for ARIMA modeling")
        
        return is_stationary
    
    def plot_time_series(self, save_path=None):
        """
        Plot the time series data
        
        Args:
            save_path (str): Path to save the plot
        """
        plt.figure(figsize=(14, 6))
        plt.plot(self.df[self.date_column], self.df[self.target_column], linewidth=1.5)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel(self.target_column, fontsize=12)
        plt.title(f'Time Series: {self.target_column}', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Time series plot saved to: {save_path}")
        
        plt.close()
    
    def train_arima(self, order=(1, 1, 1), seasonal_order=(0, 0, 0, 0)):
        """
        Train ARIMA model
        
        Args:
            order (tuple): ARIMA order (p, d, q)
            seasonal_order (tuple): Seasonal ARIMA order (P, D, Q, s)
            
        Returns:
            Fitted ARIMA model
        """
        print(f"\n--- Training ARIMA Model {order} ---")
        
        try:
            # Prepare data
            ts_data = self.df[[self.date_column, self.target_column]].copy()
            ts_data = ts_data.set_index(self.date_column)
            
            # Fit ARIMA
            self.arima_model = ARIMA(
                ts_data[self.target_column],
                order=order,
                seasonal_order=seasonal_order
            )
            self.arima_fitted = self.arima_model.fit()
            
            print("✓ ARIMA model trained successfully")
            print(f"\nModel Summary:")
            print(f"  AIC: {self.arima_fitted.aic:.2f}")
            print(f"  BIC: {self.arima_fitted.bic:.2f}")
            
            return self.arima_fitted
            
        except Exception as e:
            print(f"✗ ARIMA training failed: {str(e)}")
            return None
    
    def forecast_arima(self, n_periods=30):
        """
        Generate forecasts using ARIMA
        
        Args:
            n_periods (int): Number of periods to forecast
            
        Returns:
            pd.DataFrame: Forecast dataframe
        """
        print(f"\n--- Generating ARIMA Forecast ({n_periods} periods) ---")
        
        if self.arima_fitted is None:
            print("✗ ARIMA model not trained. Training with default parameters...")
            self.train_arima()
        
        if self.arima_fitted is None:
            print("✗ Cannot generate forecast without trained model")
            return None
        
        try:
            # Generate forecast
            forecast_result = self.arima_fitted.forecast(steps=n_periods)
            
            # Get confidence intervals
            forecast_df = self.arima_fitted.get_forecast(steps=n_periods).summary_frame()
            
            # Create date range for forecast
            last_date = self.df[self.date_column].max()
            forecast_dates = pd.date_range(
                start=last_date + pd.Timedelta(days=1),
                periods=n_periods,
                freq='D'
            )
            
            forecast_df.index = forecast_dates
            forecast_df = forecast_df.reset_index()
            forecast_df.columns = ['Date', 'Forecast', 'Std_Error', 'Lower_CI', 'Upper_CI']
            
            print(f"✓ ARIMA forecast generated for {n_periods} periods")
            print(f"\nForecast Summary:")
            print(f"  Mean: {forecast_df['Forecast'].mean():.2f}")
            print(f"  Min: {forecast_df['Forecast'].min():.2f}")
            print(f"  Max: {forecast_df['Forecast'].max():.2f}")
            
            return forecast_df
            
        except Exception as e:
            print(f"✗ Forecast generation failed: {str(e)}")
            return None
    
    def train_prophet(self, yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False):
        """
        Train Prophet model
        
        Args:
            yearly_seasonality (bool): Include yearly seasonality
            weekly_seasonality (bool): Include weekly seasonality
            daily_seasonality (bool): Include daily seasonality
            
        Returns:
            Fitted Prophet model
        """
        print("\n--- Training Prophet Model ---")
        
        try:
            # Prepare data for Prophet (requires 'ds' and 'y' columns)
            prophet_df = self.df[[self.date_column, self.target_column]].copy()
            prophet_df.columns = ['ds', 'y']
            
            # Initialize and fit Prophet
            self.prophet_model = Prophet(
                yearly_seasonality=yearly_seasonality,
                weekly_seasonality=weekly_seasonality,
                daily_seasonality=daily_seasonality,
                changepoint_prior_scale=0.05
            )
            
            self.prophet_model.fit(prophet_df)
            
            print("✓ Prophet model trained successfully")
            
            return self.prophet_model
            
        except Exception as e:
            print(f"✗ Prophet training failed: {str(e)}")
            return None
    
    def forecast_prophet(self, n_periods=30, freq='D'):
        """
        Generate forecasts using Prophet
        
        Args:
            n_periods (int): Number of periods to forecast
            freq (str): Frequency ('D' for daily, 'W' for weekly, 'M' for monthly)
            
        Returns:
            pd.DataFrame: Forecast dataframe
        """
        print(f"\n--- Generating Prophet Forecast ({n_periods} periods) ---")
        
        if self.prophet_model is None:
            print("✗ Prophet model not trained. Training with default parameters...")
            self.train_prophet()
        
        if self.prophet_model is None:
            print("✗ Cannot generate forecast without trained model")
            return None
        
        try:
            # Create future dataframe
            future = self.prophet_model.make_future_dataframe(periods=n_periods, freq=freq)
            
            # Generate forecast
            forecast = self.prophet_model.predict(future)
            
            # Extract only future predictions
            forecast_only = forecast.tail(n_periods)[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
            forecast_only.columns = ['Date', 'Forecast', 'Lower_CI', 'Upper_CI']
            forecast_only = forecast_only.reset_index(drop=True)
            
            print(f"✓ Prophet forecast generated for {n_periods} periods")
            print(f"\nForecast Summary:")
            print(f"  Mean: {forecast_only['Forecast'].mean():.2f}")
            print(f"  Min: {forecast_only['Forecast'].min():.2f}")
            print(f"  Max: {forecast_only['Forecast'].max():.2f}")
            
            self.forecast_df = forecast_only
            
            return forecast_only
            
        except Exception as e:
            print(f"✗ Forecast generation failed: {str(e)}")
            return None
    
    def plot_forecast(self, forecast_df, model_name='Forecast', save_path=None):
        """
        Plot forecast with confidence intervals
        
        Args:
            forecast_df (pd.DataFrame): Forecast dataframe
            model_name (str): Name of the model
            save_path (str): Path to save the plot
        """
        if forecast_df is None:
            print("✗ No forecast data to plot")
            return
        
        fig, ax = plt.subplots(figsize=(16, 6))
        
        # Plot historical data
        ax.plot(self.df[self.date_column], self.df[self.target_column], 
               label='Historical Data', color='#2E86AB', linewidth=2)
        
        # Plot forecast
        ax.plot(forecast_df['Date'], forecast_df['Forecast'], 
               label='Forecast', color='#D62828', linewidth=2, linestyle='--')
        
        # Plot confidence intervals
        ax.fill_between(
            forecast_df['Date'],
            forecast_df['Lower_CI'],
            forecast_df['Upper_CI'],
            alpha=0.3,
            color='#D62828',
            label='95% Confidence Interval'
        )
        
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel(self.target_column, fontsize=12)
        ax.set_title(f'{model_name} Forecast: {self.target_column}', fontsize=14, fontweight='bold')
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Forecast plot saved to: {save_path}")
        
        plt.close()
    
    def compare_forecasts(self, arima_forecast, prophet_forecast, save_path=None):
        """
        Compare ARIMA and Prophet forecasts
        
        Args:
            arima_forecast (pd.DataFrame): ARIMA forecast
            prophet_forecast (pd.DataFrame): Prophet forecast
            save_path (str): Path to save the plot
        """
        fig, ax = plt.subplots(figsize=(16, 6))
        
        # Plot historical data
        ax.plot(self.df[self.date_column].tail(90), 
               self.df[self.target_column].tail(90),
               label='Historical Data (Last 90 days)', color='#2E86AB', linewidth=2)
        
        # Plot ARIMA forecast
        if arima_forecast is not None:
            ax.plot(arima_forecast['Date'], arima_forecast['Forecast'],
                   label='ARIMA Forecast', color='#D62828', linewidth=2, linestyle='--', marker='o')
        
        # Plot Prophet forecast
        if prophet_forecast is not None:
            ax.plot(prophet_forecast['Date'], prophet_forecast['Forecast'],
                   label='Prophet Forecast', color='#06A77D', linewidth=2, linestyle='--', marker='s')
        
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel(self.target_column, fontsize=12)
        ax.set_title('Forecast Comparison: ARIMA vs Prophet', fontsize=14, fontweight='bold')
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Comparison plot saved to: {save_path}")
        
        plt.close()
    
    def forecast_next_n_days(self, n_days=30, model='prophet', save_path=None):
        """
        Complete forecasting pipeline
        
        Args:
            n_days (int): Number of days to forecast
            model (str): 'prophet' or 'arima'
            save_path (str): Path to save results
            
        Returns:
            pd.DataFrame: Forecast dataframe
        """
        print("\n" + "=" * 60)
        print(f"FORECASTING NEXT {n_days} DAYS USING {model.upper()}")
        print("=" * 60)
        
        # Check stationarity
        self.check_stationarity()
        
        # Generate forecast based on model choice
        if model.lower() == 'arima':
            self.train_arima()
            forecast_df = self.forecast_arima(n_periods=n_days)
            model_name = 'ARIMA'
        elif model.lower() == 'prophet':
            self.train_prophet()
            forecast_df = self.forecast_prophet(n_periods=n_days)
            model_name = 'Prophet'
        else:
            print(f"✗ Unknown model: {model}. Using Prophet as default.")
            self.train_prophet()
            forecast_df = self.forecast_prophet(n_periods=n_days)
            model_name = 'Prophet'
        
        # Plot forecast
        if forecast_df is not None and save_path:
            self.plot_forecast(forecast_df, model_name, save_path)
        
        print("\n" + "=" * 60)
        print("FORECASTING COMPLETED")
        print("=" * 60)
        
        return forecast_df
    
    def save_forecast(self, forecast_df, filepath):
        """
        Save forecast to CSV
        
        Args:
            forecast_df (pd.DataFrame): Forecast dataframe
            filepath (str): Path to save the file
        """
        if forecast_df is None:
            print("✗ No forecast data to save")
            return
        
        try:
            forecast_df.to_csv(filepath, index=False)
            print(f"✓ Forecast saved to: {filepath}")
        except Exception as e:
            print(f"✗ Error saving forecast: {str(e)}")


# Example usage
if __name__ == "__main__":
    print("Forecasting Module")
    print("Implements ARIMA and Prophet for time-series forecasting")
    print("\nUsage:")
    print("  forecaster = Forecaster(df_clean, target_column='Units_Sold')")
    print("  forecast_df = forecaster.forecast_next_n_days(30, model='prophet')")
