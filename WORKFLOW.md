# 📊 Sales Forecasting Workflow

## Complete System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     INPUT: Raw Sales Data (CSV)                  │
│        Date | Product | Units_Sold | Revenue | Region           │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              MODULE 1: Data Preprocessing                        │
│              (src/data_preprocessing.py)                         │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ • Load CSV data                                            │ │
│  │ • Handle missing values (median/mode)                      │ │
│  │ • Remove duplicates                                        │ │
│  │ • Convert date columns to datetime                         │ │
│  │ • Sort by date                                             │ │
│  │ • Feature Engineering:                                     │ │
│  │   - Year, Month, Day, Weekday                             │ │
│  │   - Quarter, DayOfYear, WeekOfYear                        │ │
│  │   - Cyclical encoding (sin/cos)                           │ │
│  │   - Lag features (optional)                               │ │
│  │   - Rolling statistics (optional)                         │ │
│  │ • Normalize data (StandardScaler/MinMaxScaler)            │ │
│  └────────────────────────────────────────────────────────────┘ │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
            ┌────────────┴────────────┐
            │                         │
            ▼                         ▼
┌─────────────────────────┐  ┌─────────────────────────┐
│   MODULE 2: EDA         │  │  MODULE 3: Modeling     │
│   (src/eda.py)          │  │  (src/model_training.py)│
├─────────────────────────┤  ├─────────────────────────┤
│ • Monthly sales trends  │  │ • Split train/test      │
│ • Revenue analysis      │  │ • Train models:         │
│ • Product demand        │  │   - Linear Regression   │
│ • Correlation heatmap   │  │   - Random Forest       │
│ • Seasonal patterns:    │  │   - XGBoost             │
│   - Day of week         │  │ • Evaluate metrics:     │
│   - Monthly             │  │   - MAE, RMSE, R²       │
│   - Quarterly           │  │ • Compare models        │
│   - Yearly              │  │ • Feature importance    │
│ • Generate insights     │  │ • Save best model       │
│ • Export visualizations │  │ • Plot predictions      │
└────────┬────────────────┘  └────────┬────────────────┘
         │                            │
         │                            │
         └────────────┬───────────────┘
                      │
                      ▼
         ┌────────────────────────────┐
         │  MODULE 4: Forecasting     │
         │  (src/forecasting.py)      │
         ├────────────────────────────┤
         │ • Check stationarity (ADF) │
         │ • Train forecasting models:│
         │   ┌──────────────────────┐ │
         │   │ ARIMA                │ │
         │   │ - Auto-regressive    │ │
         │   │ - Integrated         │ │
         │   │ - Moving average     │ │
         │   │ - AIC/BIC criteria   │ │
         │   └──────────────────────┘ │
         │   ┌──────────────────────┐ │
         │   │ Prophet              │ │
         │   │ - Trend component    │ │
         │   │ - Seasonality        │ │
         │   │ - Holiday effects    │ │
         │   │ - Changepoints       │ │
         │   └──────────────────────┘ │
         │ • Generate forecasts       │
         │ • Confidence intervals     │
         │ • Compare models           │
         │ • Export predictions       │
         └────────────┬───────────────┘
                      │
                      ▼
         ┌────────────────────────────┐
         │   OUTPUT: Results          │
         ├────────────────────────────┤
         │ • Cleaned data (CSV)       │
         │ • Visualizations (PNG/HTML)│
         │ • Trained models (PKL)     │
         │ • Forecasts (CSV)          │
         │ • Summary report (JSON)    │
         │ • Business insights (TXT)  │
         └────────────────────────────┘
```

---

## 🔄 Three Ways to Use the System

### 1. Command Line (main.py)

```
python main.py
     │
     ├─> Creates sample data (if needed)
     ├─> Runs data preprocessing
     ├─> Performs EDA
     ├─> Trains all models
     ├─> Generates forecasts
     └─> Exports everything to output/
```

**Use when:** You want full automation and batch processing

---

### 2. Web Interface (Streamlit)

```
streamlit run app/streamlit_app.py
     │
     ├─> Browser opens at localhost:8501
     │
     └─> User Interface:
         ├─> Tab 1: Data Analysis
         │   ├─> Upload CSV
         │   ├─> View data preview
         │   ├─> Generate visualizations
         │   └─> See statistics
         │
         ├─> Tab 2: Model Training
         │   ├─> Select models
         │   ├─> Configure parameters
         │   ├─> Train & compare
         │   └─> View performance
         │
         ├─> Tab 3: Forecasting
         │   ├─> Choose model (Prophet/ARIMA)
         │   ├─> Set forecast period
         │   ├─> Generate predictions
         │   └─> Interactive plots
         │
         └─> Tab 4: Export Results
             ├─> Download processed data
             ├─> Download forecasts
             └─> Save models
```

**Use when:** You want interactive exploration or non-technical users

---

### 3. Jupyter Notebook

```
notebooks/sales_forecasting_demo.ipynb
     │
     ├─> Cell 1: Setup & imports
     ├─> Cell 2: Create sample data
     ├─> Cell 3: Data preprocessing
     ├─> Cell 4: Exploratory analysis
     ├─> Cell 5: Model training
     ├─> Cell 6: Visualize performance
     ├─> Cell 7: Prophet forecasting
     ├─> Cell 8: ARIMA forecasting
     ├─> Cell 9: Compare forecasts
     ├─> Cell 10: Export results
     ├─> Cell 11: Business insights
     └─> Cell 12: Next steps
```

**Use when:** You want step-by-step learning and experimentation

---

## 📦 Module Dependencies

```
data_preprocessing.py
    │
    ├── pandas
    ├── numpy
    ├── sklearn.preprocessing
    └── warnings

eda.py
    │
    ├── pandas
    ├── numpy
    ├── matplotlib.pyplot
    ├── seaborn
    ├── plotly.express
    ├── plotly.graph_objects
    └── warnings

model_training.py
    │
    ├── pandas
    ├── numpy
    ├── sklearn.model_selection
    ├── sklearn.linear_model
    ├── sklearn.ensemble
    ├── sklearn.metrics
    ├── xgboost
    ├── joblib
    ├── matplotlib.pyplot
    ├── seaborn
    └── warnings

forecasting.py
    │
    ├── pandas
    ├── numpy
    ├── matplotlib.pyplot
    ├── seaborn
    ├── statsmodels.tsa.arima.model
    ├── statsmodels.tsa.stattools
    ├── prophet
    └── warnings

streamlit_app.py
    │
    ├── streamlit
    ├── pandas
    ├── numpy
    ├── plotly.express
    ├── plotly.graph_objects
    ├── sys, os, pathlib
    └── [all src modules]
```

---

## 🔄 Data Flow Diagram

```
RAW DATA
   │
   ├─> Date: 2023-01-01
   ├─> Product: Product A
   ├─> Units_Sold: 150
   ├─> Revenue: 15000
   └─> Region: North
   
         │ (Preprocessing)
         ▼
         
PROCESSED DATA
   │
   ├─> Date: 2023-01-01
   ├─> Product: Product A
   ├─> Units_Sold: 150
   ├─> Revenue: 15000
   ├─> Region: North
   ├─> Year: 2023
   ├─> Month: 1
   ├─> Day: 1
   ├─> Weekday: 6 (Sunday)
   ├─> Quarter: 1
   ├─> Month_Sin: 0.5
   ├─> Month_Cos: 0.866
   └─> ... (more features)
   
         │ (Feature Selection)
         ▼
         
TRAINING DATA
   │
   ├─> Features (X):
   │   [Year, Month, Day, Weekday, Quarter, ...]
   │
   └─> Target (y):
       [Units_Sold or Revenue]
   
         │ (Model Training)
         ▼
         
TRAINED MODELS
   │
   ├─> Linear Regression Model
   ├─> Random Forest Model
   └─> XGBoost Model
   
         │ (Prediction)
         ▼
         
PREDICTIONS
   │
   └─> Forecasted Units_Sold for next 30 days
       with confidence intervals
```

---

## ⚙️ Configuration Flow

```
config.py
   │
   ├─> DATA_CONFIG
   │   └─> Column names, formats
   │
   ├─> PREPROCESSING_CONFIG
   │   └─> Feature engineering options
   │
   ├─> MODEL_CONFIG
   │   ├─> Linear Regression params
   │   ├─> Random Forest params
   │   └─> XGBoost params
   │
   ├─> FORECAST_CONFIG
   │   ├─> ARIMA params
   │   └─> Prophet params
   │
   ├─> VISUALIZATION_CONFIG
   │   └─> Plot settings, colors
   │
   └─> EXPORT_CONFIG
       └─> File formats, paths

         │
         ▼
         
    Used by all modules
```

---

## 🎯 Execution Flow

### Automated Pipeline (main.py)

```
START
  │
  ├─> [1] Check for sample data
  │   ├─> If missing: create_sample_data()
  │   └─> If exists: use existing
  │
  ├─> [2] Data Preprocessing
  │   ├─> Load CSV
  │   ├─> Clean data
  │   ├─> Engineer features
  │   └─> Save processed data
  │
  ├─> [3] Exploratory Analysis
  │   ├─> Monthly trends
  │   ├─> Revenue analysis
  │   ├─> Product demand
  │   ├─> Correlations
  │   ├─> Seasonal patterns
  │   └─> Save visualizations
  │
  ├─> [4] Model Training
  │   ├─> Split train/test
  │   ├─> Train Linear Regression
  │   ├─> Train Random Forest
  │   ├─> Train XGBoost
  │   ├─> Compare models
  │   ├─> Select best model
  │   ├─> Plot predictions
  │   ├─> Feature importance
  │   └─> Save best model
  │
  ├─> [5] Forecasting
  │   ├─> Aggregate by date
  │   ├─> Check stationarity
  │   ├─> Train Prophet
  │   ├─> Generate Prophet forecast
  │   ├─> Train ARIMA
  │   ├─> Generate ARIMA forecast
  │   ├─> Compare forecasts
  │   └─> Save forecasts
  │
  ├─> [6] Summary Report
  │   ├─> Dataset statistics
  │   ├─> Model performance
  │   ├─> Forecast summary
  │   ├─> Business insights
  │   └─> Save JSON report
  │
  └─> END
```

---

## 📊 Output Structure

```
output/
  │
  ├─> Data Visualizations:
  │   ├─> monthly_sales_trend.png
  │   ├─> revenue_analysis.html
  │   ├─> product_demand.png
  │   ├─> correlation_heatmap.png
  │   └─> seasonal_patterns.png
  │
  ├─> Model Performance:
  │   ├─> model_comparison.png
  │   ├─> Random_Forest_predictions.png
  │   └─> XGBoost_feature_importance.png
  │
  ├─> Forecasts:
  │   ├─> prophet_forecast.png
  │   ├─> prophet_forecast.csv
  │   ├─> arima_forecast.png
  │   ├─> arima_forecast.csv
  │   └─> forecast_comparison.png
  │
  ├─> Data:
  │   └─> processed_data.csv
  │
  └─> Reports:
      └─> summary_report.json

models/
  │
  └─> Trained Models:
      ├─> Random_Forest_model.pkl
      └─> XGBoost_model.pkl
```

---

## 🚀 Quick Reference

### Common Commands

```bash
# Setup
pip install -r requirements.txt

# Verify installation
python test_installation.py

# Run full pipeline
python main.py

# Launch web app
streamlit run app/streamlit_app.py

# Start Jupyter
jupyter notebook
```

### Common Imports

```python
# Data preprocessing
from src.data_preprocessing import DataPreprocessor

# EDA
from src.eda import EDA

# Model training
from src.model_training import ModelTrainer

# Forecasting
from src.forecasting import Forecaster

# Configuration
import config
```

### Quick Usage

```python
# Complete workflow in 5 lines
preprocessor = DataPreprocessor('data.csv')
df = preprocessor.preprocess()
trainer = ModelTrainer(df, target_column='Units_Sold')
trainer.train_all_models()
forecaster = Forecaster(df, target_column='Units_Sold')
forecast = forecaster.forecast_next_n_days(30)
```

---

## 📈 Success Metrics

After running the pipeline, you should see:

```
✅ Data Preprocessing: 100%
   - Missing values: 0
   - Duplicates removed: X
   - Features created: 10+

✅ EDA Complete:
   - Visualizations: 5+
   - Insights generated: 5+
   
✅ Models Trained: 3
   - Best R² Score: > 0.70
   - Test MAE: < 50
   
✅ Forecasts Generated: 2
   - Prophet forecast: 30 days
   - ARIMA forecast: 30 days
   - Confidence intervals: 95%

✅ Files Exported:
   - Plots: 10+
   - Models: 1+
   - Forecasts: 2
   - Reports: 1
```

---

**Your complete sales forecasting workflow is ready!** 🎉

Use this guide as a reference for understanding how all components work together.
