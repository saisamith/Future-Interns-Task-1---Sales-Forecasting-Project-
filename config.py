"""
Configuration File
Central place for all project settings and parameters
"""

import os

# ===== PROJECT PATHS =====
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(PROJECT_ROOT, 'dataset')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'output')
MODELS_DIR = os.path.join(PROJECT_ROOT, 'models')
NOTEBOOKS_DIR = os.path.join(PROJECT_ROOT, 'notebooks')

# ===== DATA SETTINGS =====
DATA_CONFIG = {
    'date_column': 'Date',
    'target_column': 'Units_Sold',
    'revenue_column': 'Revenue',
    'product_column': 'Product_Name',
    'category_column': 'Category',
    'region_column': 'Region',
    'store_column': 'Store'
}

# ===== PREPROCESSING SETTINGS =====
PREPROCESSING_CONFIG = {
    'create_lag_features': False,
    'lag_periods': [1, 7, 14, 30],
    'rolling_windows': [7, 30],
    'handle_missing': 'median',  # 'median', 'mean', 'drop'
    'remove_duplicates': True,
    'date_format': '%Y-%m-%d'
}

# ===== MODEL TRAINING SETTINGS =====
MODEL_CONFIG = {
    'test_size': 0.2,
    'random_state': 42,
    'models_to_train': ['Linear Regression', 'Random Forest', 'XGBoost'],
    
    # Linear Regression
    'linear_regression': {
        'fit_intercept': True
    },
    
    # Random Forest
    'random_forest': {
        'n_estimators': 100,
        'max_depth': None,
        'min_samples_split': 2,
        'min_samples_leaf': 1,
        'random_state': 42,
        'n_jobs': -1
    },
    
    # XGBoost
    'xgboost': {
        'n_estimators': 100,
        'learning_rate': 0.1,
        'max_depth': 6,
        'min_child_weight': 1,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'random_state': 42,
        'n_jobs': -1
    }
}

# ===== FORECASTING SETTINGS =====
FORECAST_CONFIG = {
    'default_model': 'prophet',  # 'prophet' or 'arima'
    'forecast_periods': 30,
    'frequency': 'D',  # 'D' for daily, 'W' for weekly, 'M' for monthly
    
    # ARIMA
    'arima': {
        'order': (1, 1, 1),  # (p, d, q)
        'seasonal_order': (0, 0, 0, 0),  # (P, D, Q, s)
        'auto_arima': False  # If True, find optimal parameters automatically
    },
    
    # Prophet
    'prophet': {
        'yearly_seasonality': True,
        'weekly_seasonality': True,
        'daily_seasonality': False,
        'changepoint_prior_scale': 0.05,
        'seasonality_prior_scale': 10.0,
        'holidays_prior_scale': 10.0,
        'seasonality_mode': 'additive',  # 'additive' or 'multiplicative'
        'interval_width': 0.95
    }
}

# ===== VISUALIZATION SETTINGS =====
VISUALIZATION_CONFIG = {
    'figure_size': (14, 6),
    'dpi': 300,
    'style': 'whitegrid',
    'color_palette': 'Set2',
    'save_format': 'png',  # 'png', 'jpg', 'svg', 'pdf'
    
    'colors': {
        'primary': '#2E86AB',
        'secondary': '#A23B72',
        'success': '#06A77D',
        'warning': '#F18F01',
        'danger': '#D62828',
        'info': '#4ECDC4'
    }
}

# ===== EDA SETTINGS =====
EDA_CONFIG = {
    'top_products_count': 10,
    'correlation_threshold': 0.7,
    'histogram_bins': 50,
    'generate_all_plots': True,
    'save_plots': True
}

# ===== STREAMLIT APP SETTINGS =====
STREAMLIT_CONFIG = {
    'page_title': 'Sales & Demand Forecasting',
    'page_icon': '📊',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded',
    'max_upload_size': 200,  # MB
    'cache_ttl': 3600  # seconds
}

# ===== EXPORT SETTINGS =====
EXPORT_CONFIG = {
    'csv_encoding': 'utf-8',
    'csv_index': False,
    'excel_engine': 'openpyxl',
    'json_indent': 2,
    'include_timestamp': True
}

# ===== LOGGING SETTINGS =====
LOGGING_CONFIG = {
    'level': 'INFO',  # 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'date_format': '%Y-%m-%d %H:%M:%S',
    'log_to_file': False,
    'log_file': 'logs/app.log'
}

# ===== PERFORMANCE SETTINGS =====
PERFORMANCE_CONFIG = {
    'n_jobs': -1,  # Number of parallel jobs (-1 = all cores)
    'chunk_size': 10000,  # For processing large datasets
    'memory_limit': '4GB',
    'cache_predictions': True
}

# ===== VALIDATION SETTINGS =====
VALIDATION_CONFIG = {
    'min_data_points': 100,
    'min_date_range_days': 30,
    'max_missing_percentage': 20,
    'required_columns': ['Date'],
    'check_data_quality': True
}


def get_config(section=None):
    """
    Get configuration for a specific section or all config
    
    Args:
        section (str): Section name (e.g., 'MODEL_CONFIG')
        
    Returns:
        dict: Configuration dictionary
    """
    if section is None:
        return {
            'DATA': DATA_CONFIG,
            'PREPROCESSING': PREPROCESSING_CONFIG,
            'MODEL': MODEL_CONFIG,
            'FORECAST': FORECAST_CONFIG,
            'VISUALIZATION': VISUALIZATION_CONFIG,
            'EDA': EDA_CONFIG,
            'STREAMLIT': STREAMLIT_CONFIG,
            'EXPORT': EXPORT_CONFIG,
            'LOGGING': LOGGING_CONFIG,
            'PERFORMANCE': PERFORMANCE_CONFIG,
            'VALIDATION': VALIDATION_CONFIG
        }
    
    config_map = {
        'data': DATA_CONFIG,
        'preprocessing': PREPROCESSING_CONFIG,
        'model': MODEL_CONFIG,
        'forecast': FORECAST_CONFIG,
        'visualization': VISUALIZATION_CONFIG,
        'eda': EDA_CONFIG,
        'streamlit': STREAMLIT_CONFIG,
        'export': EXPORT_CONFIG,
        'logging': LOGGING_CONFIG,
        'performance': PERFORMANCE_CONFIG,
        'validation': VALIDATION_CONFIG
    }
    
    return config_map.get(section.lower(), {})


def print_config():
    """
    Print all configuration settings
    """
    print("=" * 80)
    print("PROJECT CONFIGURATION")
    print("=" * 80)
    
    all_config = get_config()
    
    for section_name, section_config in all_config.items():
        print(f"\n{section_name}:")
        print("-" * 40)
        for key, value in section_config.items():
            print(f"  {key}: {value}")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    print_config()
