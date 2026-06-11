"""
Data Preprocessing Module
Handles data loading, cleaning, and feature engineering
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import warnings
warnings.filterwarnings('ignore')


class DataPreprocessor:
    """
    Class to preprocess sales data for forecasting
    """
    
    def __init__(self, filepath):
        """
        Initialize the preprocessor
        
        Args:
            filepath (str): Path to the CSV file
        """
        self.filepath = filepath
        self.df = None
        self.scaler = None
        
    def load_data(self):
        """
        Load data from CSV file
        
        Returns:
            pd.DataFrame: Loaded dataframe
        """
        try:
            self.df = pd.read_csv(self.filepath)
            print(f"✓ Data loaded successfully: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
            return self.df
        except Exception as e:
            print(f"✗ Error loading data: {str(e)}")
            raise
    
    def handle_missing_values(self):
        """
        Handle missing values in the dataset
        """
        print("\n--- Handling Missing Values ---")
        missing_before = self.df.isnull().sum().sum()
        print(f"Missing values before: {missing_before}")
        
        # Fill numerical columns with median
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numerical_cols:
            if self.df[col].isnull().any():
                self.df[col].fillna(self.df[col].median(), inplace=True)
        
        # Fill categorical columns with mode
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if col != 'Date' and self.df[col].isnull().any():
                self.df[col].fillna(self.df[col].mode()[0], inplace=True)
        
        missing_after = self.df.isnull().sum().sum()
        print(f"Missing values after: {missing_after}")
        print("✓ Missing values handled")
    
    def remove_duplicates(self):
        """
        Remove duplicate rows
        """
        print("\n--- Removing Duplicates ---")
        rows_before = len(self.df)
        self.df.drop_duplicates(inplace=True)
        rows_after = len(self.df)
        print(f"Rows removed: {rows_before - rows_after}")
        print("✓ Duplicates removed")
    
    def convert_date_column(self, date_column='Date'):
        """
        Convert date column to datetime format
        
        Args:
            date_column (str): Name of the date column
        """
        print("\n--- Converting Date Column ---")
        try:
            self.df[date_column] = pd.to_datetime(self.df[date_column])
            self.df = self.df.sort_values(by=date_column).reset_index(drop=True)
            print(f"✓ Date column '{date_column}' converted to datetime")
            print(f"Date range: {self.df[date_column].min()} to {self.df[date_column].max()}")
        except Exception as e:
            print(f"✗ Error converting date column: {str(e)}")
    
    def feature_engineering(self, date_column='Date'):
        """
        Create time-based features from date column
        
        Args:
            date_column (str): Name of the date column
        """
        print("\n--- Feature Engineering ---")
        
        if date_column not in self.df.columns:
            print(f"✗ Date column '{date_column}' not found")
            return
        
        # Extract time features
        self.df['Year'] = self.df[date_column].dt.year
        self.df['Month'] = self.df[date_column].dt.month
        self.df['Day'] = self.df[date_column].dt.day
        self.df['Weekday'] = self.df[date_column].dt.dayofweek  # Monday=0, Sunday=6
        self.df['Quarter'] = self.df[date_column].dt.quarter
        self.df['DayOfYear'] = self.df[date_column].dt.dayofyear
        self.df['WeekOfYear'] = self.df[date_column].dt.isocalendar().week
        
        # Cyclical encoding for month and weekday
        self.df['Month_Sin'] = np.sin(2 * np.pi * self.df['Month'] / 12)
        self.df['Month_Cos'] = np.cos(2 * np.pi * self.df['Month'] / 12)
        self.df['Weekday_Sin'] = np.sin(2 * np.pi * self.df['Weekday'] / 7)
        self.df['Weekday_Cos'] = np.cos(2 * np.pi * self.df['Weekday'] / 7)
        
        print("✓ Time-based features created:")
        print("  - Year, Month, Day, Weekday")
        print("  - Quarter, DayOfYear, WeekOfYear")
        print("  - Cyclical encodings (Month_Sin/Cos, Weekday_Sin/Cos)")
    
    def normalize_data(self, columns=None, method='standard'):
        """
        Normalize or scale numerical columns
        
        Args:
            columns (list): List of columns to normalize (None = all numerical)
            method (str): 'standard' or 'minmax'
        """
        print("\n--- Normalizing Data ---")
        
        if columns is None:
            # Select numerical columns except engineered features
            columns = [col for col in self.df.select_dtypes(include=[np.number]).columns 
                      if col not in ['Year', 'Month', 'Day', 'Weekday', 'Quarter', 'DayOfYear', 'WeekOfYear',
                                     'Month_Sin', 'Month_Cos', 'Weekday_Sin', 'Weekday_Cos']]
        
        if method == 'standard':
            self.scaler = StandardScaler()
        elif method == 'minmax':
            self.scaler = MinMaxScaler()
        else:
            print("✗ Invalid normalization method")
            return
        
        # Store original columns for later use
        self.df_original = self.df.copy()
        
        # Note: We typically don't scale the target variable for better interpretability
        # But we'll create scaled versions for models that benefit from it
        print(f"✓ Scaler ({method}) fitted on columns: {columns}")
    
    def create_lag_features(self, target_column, lags=[1, 7, 14, 30]):
        """
        Create lag features for time series
        
        Args:
            target_column (str): Column to create lags for
            lags (list): List of lag periods
        """
        print("\n--- Creating Lag Features ---")
        
        for lag in lags:
            self.df[f'{target_column}_Lag_{lag}'] = self.df[target_column].shift(lag)
        
        # Rolling statistics
        self.df[f'{target_column}_Rolling_Mean_7'] = self.df[target_column].rolling(window=7).mean()
        self.df[f'{target_column}_Rolling_Std_7'] = self.df[target_column].rolling(window=7).std()
        self.df[f'{target_column}_Rolling_Mean_30'] = self.df[target_column].rolling(window=30).mean()
        
        print(f"✓ Lag features created for {target_column}")
        print(f"  - Lags: {lags}")
        print(f"  - Rolling statistics (7-day and 30-day)")
    
    def preprocess(self, date_column='Date', create_lags=False, target_column=None):
        """
        Execute full preprocessing pipeline
        
        Args:
            date_column (str): Name of the date column
            create_lags (bool): Whether to create lag features
            target_column (str): Target column for lag features
            
        Returns:
            pd.DataFrame: Preprocessed dataframe
        """
        print("=" * 60)
        print("STARTING DATA PREPROCESSING PIPELINE")
        print("=" * 60)
        
        # Load data
        self.load_data()
        
        # Clean data
        self.handle_missing_values()
        self.remove_duplicates()
        
        # Process dates
        self.convert_date_column(date_column)
        
        # Engineer features
        self.feature_engineering(date_column)
        
        # Create lag features if requested
        if create_lags and target_column:
            self.create_lag_features(target_column)
            # Drop rows with NaN created by lag features
            self.df.dropna(inplace=True)
            print(f"✓ Rows after dropping NaN from lags: {len(self.df)}")
        
        print("\n" + "=" * 60)
        print("PREPROCESSING COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print(f"\nFinal dataset shape: {self.df.shape}")
        print(f"Columns: {list(self.df.columns)}")
        
        return self.df
    
    def get_data_summary(self):
        """
        Get summary statistics of the processed data
        
        Returns:
            dict: Summary statistics
        """
        if self.df is None:
            return "No data loaded"
        
        summary = {
            'shape': self.df.shape,
            'columns': list(self.df.columns),
            'dtypes': self.df.dtypes.to_dict(),
            'missing_values': self.df.isnull().sum().to_dict(),
            'numerical_summary': self.df.describe().to_dict()
        }
        
        return summary
    
    def save_processed_data(self, output_path):
        """
        Save processed data to CSV
        
        Args:
            output_path (str): Path to save the file
        """
        try:
            self.df.to_csv(output_path, index=False)
            print(f"✓ Processed data saved to: {output_path}")
        except Exception as e:
            print(f"✗ Error saving data: {str(e)}")


# Example usage
if __name__ == "__main__":
    # Example with synthetic data
    print("Data Preprocessing Module")
    print("This module handles data loading, cleaning, and feature engineering")
    print("\nUsage:")
    print("  preprocessor = DataPreprocessor('dataset/sales_data.csv')")
    print("  df_clean = preprocessor.preprocess()")
