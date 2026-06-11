"""
Model Training Module
Implements multiple ML models for sales forecasting
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


class ModelTrainer:
    """
    Class to train and evaluate multiple regression models
    """
    
    def __init__(self, df, target_column='Units_Sold', date_column='Date'):
        """
        Initialize the model trainer
        
        Args:
            df (pd.DataFrame): Preprocessed dataframe
            target_column (str): Target variable to predict
            date_column (str): Date column name
        """
        self.df = df.copy()
        self.target_column = target_column
        self.date_column = date_column
        self.models = {}
        self.results = {}
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.feature_columns = None
        
    def prepare_features(self, exclude_columns=None):
        """
        Prepare features for modeling
        
        Args:
            exclude_columns (list): Columns to exclude from features
        """
        print("\n--- Preparing Features ---")
        
        if exclude_columns is None:
            exclude_columns = []
        
        # Default exclusions
        default_exclude = [self.target_column, self.date_column]
        
        # Add columns with lag features that might have NaN
        lag_cols = [col for col in self.df.columns if 'Lag' in col or 'Rolling' in col]
        
        # Exclude non-numeric and specified columns
        all_exclude = default_exclude + exclude_columns + lag_cols
        
        # Select numeric columns only
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Filter out excluded columns
        self.feature_columns = [col for col in numeric_cols if col not in all_exclude]
        
        print(f"✓ Features selected: {len(self.feature_columns)} columns")
        print(f"  Features: {self.feature_columns[:10]}{'...' if len(self.feature_columns) > 10 else ''}")
        
    def split_data(self, test_size=0.2, random_state=42):
        """
        Split data into train and test sets
        
        Args:
            test_size (float): Proportion of test data
            random_state (int): Random seed for reproducibility
        """
        print("\n--- Splitting Data ---")
        
        if self.feature_columns is None:
            self.prepare_features()
        
        X = self.df[self.feature_columns]
        y = self.df[self.target_column]
        
        # Handle any remaining NaN values
        X = X.fillna(X.median())
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, shuffle=True
        )
        
        print(f"✓ Training set: {len(self.X_train)} samples")
        print(f"✓ Test set: {len(self.X_test)} samples")
        print(f"✓ Features: {self.X_train.shape[1]} columns")
        
    def train_linear_regression(self):
        """
        Train Linear Regression model
        """
        print("\n--- Training Linear Regression ---")
        
        model = LinearRegression()
        model.fit(self.X_train, self.y_train)
        
        # Predictions
        y_pred_train = model.predict(self.X_train)
        y_pred_test = model.predict(self.X_test)
        
        # Metrics
        metrics = self._calculate_metrics(self.y_train, y_pred_train, self.y_test, y_pred_test)
        
        self.models['Linear Regression'] = model
        self.results['Linear Regression'] = metrics
        
        self._print_metrics('Linear Regression', metrics)
        
        return model, metrics
    
    def train_random_forest(self, n_estimators=100, max_depth=None, random_state=42):
        """
        Train Random Forest model
        
        Args:
            n_estimators (int): Number of trees
            max_depth (int): Maximum depth of trees
            random_state (int): Random seed
        """
        print("\n--- Training Random Forest ---")
        
        model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state,
            n_jobs=-1
        )
        model.fit(self.X_train, self.y_train)
        
        # Predictions
        y_pred_train = model.predict(self.X_train)
        y_pred_test = model.predict(self.X_test)
        
        # Metrics
        metrics = self._calculate_metrics(self.y_train, y_pred_train, self.y_test, y_pred_test)
        
        self.models['Random Forest'] = model
        self.results['Random Forest'] = metrics
        
        self._print_metrics('Random Forest', metrics)
        
        return model, metrics
    
    def train_xgboost(self, n_estimators=100, learning_rate=0.1, max_depth=6, random_state=42):
        """
        Train XGBoost model
        
        Args:
            n_estimators (int): Number of boosting rounds
            learning_rate (float): Learning rate
            max_depth (int): Maximum tree depth
            random_state (int): Random seed
        """
        print("\n--- Training XGBoost ---")
        
        model = xgb.XGBRegressor(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            max_depth=max_depth,
            random_state=random_state,
            n_jobs=-1
        )
        model.fit(self.X_train, self.y_train)
        
        # Predictions
        y_pred_train = model.predict(self.X_train)
        y_pred_test = model.predict(self.X_test)
        
        # Metrics
        metrics = self._calculate_metrics(self.y_train, y_pred_train, self.y_test, y_pred_test)
        
        self.models['XGBoost'] = model
        self.results['XGBoost'] = metrics
        
        self._print_metrics('XGBoost', metrics)
        
        return model, metrics
    
    def _calculate_metrics(self, y_train, y_pred_train, y_test, y_pred_test):
        """
        Calculate evaluation metrics
        
        Args:
            y_train: Training targets
            y_pred_train: Training predictions
            y_test: Test targets
            y_pred_test: Test predictions
            
        Returns:
            dict: Metrics dictionary
        """
        metrics = {
            'train_mae': mean_absolute_error(y_train, y_pred_train),
            'test_mae': mean_absolute_error(y_test, y_pred_test),
            'train_rmse': np.sqrt(mean_squared_error(y_train, y_pred_train)),
            'test_rmse': np.sqrt(mean_squared_error(y_test, y_pred_test)),
            'train_r2': r2_score(y_train, y_pred_train),
            'test_r2': r2_score(y_test, y_pred_test),
            'y_pred_test': y_pred_test
        }
        
        return metrics
    
    def _print_metrics(self, model_name, metrics):
        """
        Print model metrics
        
        Args:
            model_name (str): Name of the model
            metrics (dict): Metrics dictionary
        """
        print(f"\n{model_name} Results:")
        print(f"  Train MAE:  {metrics['train_mae']:.2f}")
        print(f"  Test MAE:   {metrics['test_mae']:.2f}")
        print(f"  Train RMSE: {metrics['train_rmse']:.2f}")
        print(f"  Test RMSE:  {metrics['test_rmse']:.2f}")
        print(f"  Train R²:   {metrics['train_r2']:.4f}")
        print(f"  Test R²:    {metrics['test_r2']:.4f}")
    
    def train_all_models(self):
        """
        Train all available models
        
        Returns:
            dict: Results for all models
        """
        print("\n" + "=" * 60)
        print("TRAINING ALL MODELS")
        print("=" * 60)
        
        if self.X_train is None:
            self.split_data()
        
        # Train each model
        self.train_linear_regression()
        self.train_random_forest()
        
        try:
            self.train_xgboost()
        except Exception as e:
            print(f"⚠ XGBoost training failed: {str(e)}")
        
        print("\n" + "=" * 60)
        print("ALL MODELS TRAINED")
        print("=" * 60)
        
        return self.results
    
    def compare_models(self, save_path=None):
        """
        Compare performance of all models
        
        Args:
            save_path (str): Path to save comparison plot
        """
        print("\n--- Comparing Models ---")
        
        if not self.results:
            print("✗ No models trained yet")
            return
        
        # Prepare comparison data
        comparison_data = []
        for model_name, metrics in self.results.items():
            comparison_data.append({
                'Model': model_name,
                'MAE': metrics['test_mae'],
                'RMSE': metrics['test_rmse'],
                'R² Score': metrics['test_r2']
            })
        
        df_comparison = pd.DataFrame(comparison_data)
        
        # Create comparison plots
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        
        # MAE comparison
        axes[0].bar(df_comparison['Model'], df_comparison['MAE'], color='#FF6B6B')
        axes[0].set_title('Mean Absolute Error (Lower is Better)', fontsize=12, fontweight='bold')
        axes[0].set_ylabel('MAE')
        axes[0].tick_params(axis='x', rotation=45)
        
        # RMSE comparison
        axes[1].bar(df_comparison['Model'], df_comparison['RMSE'], color='#4ECDC4')
        axes[1].set_title('Root Mean Squared Error (Lower is Better)', fontsize=12, fontweight='bold')
        axes[1].set_ylabel('RMSE')
        axes[1].tick_params(axis='x', rotation=45)
        
        # R² comparison
        axes[2].bar(df_comparison['Model'], df_comparison['R² Score'], color='#95E1D3')
        axes[2].set_title('R² Score (Higher is Better)', fontsize=12, fontweight='bold')
        axes[2].set_ylabel('R² Score')
        axes[2].tick_params(axis='x', rotation=45)
        axes[2].axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Comparison plot saved to: {save_path}")
        
        plt.close()
        
        # Print comparison table
        print("\n" + "=" * 60)
        print("MODEL COMPARISON TABLE")
        print("=" * 60)
        print(df_comparison.to_string(index=False))
        
        # Find best model
        best_model_name = df_comparison.loc[df_comparison['R² Score'].idxmax(), 'Model']
        print(f"\n🏆 Best Model: {best_model_name}")
        
        return df_comparison
    
    def plot_predictions(self, model_name='Random Forest', save_path=None):
        """
        Plot actual vs predicted values
        
        Args:
            model_name (str): Name of the model to visualize
            save_path (str): Path to save the plot
        """
        if model_name not in self.results:
            print(f"✗ Model '{model_name}' not found")
            return
        
        y_pred = self.results[model_name]['y_pred_test']
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # Scatter plot
        axes[0].scatter(self.y_test, y_pred, alpha=0.5, color='#2E86AB')
        axes[0].plot([self.y_test.min(), self.y_test.max()], 
                    [self.y_test.min(), self.y_test.max()], 
                    'r--', linewidth=2, label='Perfect Prediction')
        axes[0].set_xlabel('Actual Values', fontsize=12)
        axes[0].set_ylabel('Predicted Values', fontsize=12)
        axes[0].set_title(f'{model_name}: Actual vs Predicted', fontsize=14, fontweight='bold')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Residual plot
        residuals = self.y_test - y_pred
        axes[1].scatter(y_pred, residuals, alpha=0.5, color='#A23B72')
        axes[1].axhline(y=0, color='r', linestyle='--', linewidth=2)
        axes[1].set_xlabel('Predicted Values', fontsize=12)
        axes[1].set_ylabel('Residuals', fontsize=12)
        axes[1].set_title(f'{model_name}: Residual Plot', fontsize=14, fontweight='bold')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Predictions plot saved to: {save_path}")
        
        plt.close()
    
    def save_model(self, model_name, filepath):
        """
        Save trained model to disk
        
        Args:
            model_name (str): Name of the model to save
            filepath (str): Path to save the model
        """
        if model_name not in self.models:
            print(f"✗ Model '{model_name}' not found")
            return
        
        try:
            joblib.dump(self.models[model_name], filepath)
            print(f"✓ Model saved to: {filepath}")
        except Exception as e:
            print(f"✗ Error saving model: {str(e)}")
    
    def load_model(self, filepath):
        """
        Load a trained model from disk
        
        Args:
            filepath (str): Path to the model file
            
        Returns:
            model: Loaded model
        """
        try:
            model = joblib.load(filepath)
            print(f"✓ Model loaded from: {filepath}")
            return model
        except Exception as e:
            print(f"✗ Error loading model: {str(e)}")
            return None
    
    def get_feature_importance(self, model_name='Random Forest', top_n=10, save_path=None):
        """
        Get feature importance for tree-based models
        
        Args:
            model_name (str): Name of the model
            top_n (int): Number of top features to show
            save_path (str): Path to save the plot
        """
        if model_name not in self.models:
            print(f"✗ Model '{model_name}' not found")
            return
        
        model = self.models[model_name]
        
        if not hasattr(model, 'feature_importances_'):
            print(f"✗ Model '{model_name}' does not have feature_importances_")
            return
        
        # Get feature importance
        importance_df = pd.DataFrame({
            'Feature': self.feature_columns,
            'Importance': model.feature_importances_
        }).sort_values('Importance', ascending=False).head(top_n)
        
        # Plot
        plt.figure(figsize=(10, 6))
        plt.barh(importance_df['Feature'], importance_df['Importance'], color='#F18F01')
        plt.xlabel('Importance', fontsize=12)
        plt.title(f'Top {top_n} Feature Importance - {model_name}', fontsize=14, fontweight='bold')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Feature importance plot saved to: {save_path}")
        
        plt.close()
        
        print(f"\nTop {top_n} Features:")
        print(importance_df.to_string(index=False))
        
        return importance_df


# Example usage
if __name__ == "__main__":
    print("Model Training Module")
    print("Trains multiple ML models and compares performance")
    print("\nUsage:")
    print("  trainer = ModelTrainer(df_clean, target_column='Units_Sold')")
    print("  results = trainer.train_all_models()")
    print("  trainer.compare_models()")
