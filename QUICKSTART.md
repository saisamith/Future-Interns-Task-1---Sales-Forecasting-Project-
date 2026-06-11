# 🚀 Quick Start Guide

This guide will help you get started with the Sales & Demand Forecasting System in minutes!

## 📋 Prerequisites

- Python 3.8 or higher
- pip package manager
- (Optional) Virtual environment tool

## ⚡ Quick Setup (3 Steps)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages including:
- pandas, numpy (data manipulation)
- matplotlib, seaborn, plotly (visualizations)
- scikit-learn, xgboost (ML models)
- prophet, statsmodels (time-series forecasting)
- streamlit (web app)

### 2. Run the Complete Pipeline

```bash
python main.py
```

This will:
- ✅ Create a sample dataset
- ✅ Preprocess the data
- ✅ Generate visualizations
- ✅ Train multiple ML models
- ✅ Create forecasts
- ✅ Export all results

**Output:** Check the `output/` folder for visualizations and `models/` for trained models.

### 3. Launch the Web App

```bash
streamlit run app/streamlit_app.py
```

Then open your browser to `http://localhost:8501` and:
- Upload your own CSV dataset
- Explore interactive visualizations
- Train models with custom settings
- Generate forecasts
- Download results

## 📊 Using Your Own Data

### Required CSV Format:

```csv
Date,Product_Name,Units_Sold,Revenue,Region
2023-01-01,Product A,150,15000,North
2023-01-02,Product B,200,8000,South
```

**Minimum required columns:**
- Date (YYYY-MM-DD format)
- At least one numerical column (e.g., Units_Sold, Revenue)

**Optional columns:**
- Product_Name, Category
- Region, Store
- Any other relevant features

### Using Your Data:

#### Option 1: Via Streamlit App
1. Run `streamlit run app/streamlit_app.py`
2. Upload your CSV using the sidebar
3. Select date and target columns
4. Click "Run Data Analysis"

#### Option 2: Via Python Script
```python
from src.data_preprocessing import DataPreprocessor
from src.model_training import ModelTrainer
from src.forecasting import Forecaster

# Preprocess
preprocessor = DataPreprocessor('path/to/your/data.csv')
df_clean = preprocessor.preprocess(date_column='Date')

# Train models
trainer = ModelTrainer(df_clean, target_column='Units_Sold')
results = trainer.train_all_models()

# Forecast
forecaster = Forecaster(df_clean, target_column='Units_Sold')
forecast = forecaster.forecast_next_n_days(30, model='prophet')
```

#### Option 3: Via Jupyter Notebook
1. Open `notebooks/sales_forecasting_demo.ipynb`
2. Replace the sample data path with your CSV path
3. Run all cells

## 🎯 Common Tasks

### Task 1: Train Only Specific Models

```python
trainer = ModelTrainer(df, target_column='Units_Sold')
trainer.split_data()

# Train only Random Forest
trainer.train_random_forest(n_estimators=200, max_depth=10)
```

### Task 2: Forecast with Custom Settings

```python
# Prophet with custom seasonality
forecaster = Forecaster(df, target_column='Units_Sold')
forecaster.train_prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False
)
forecast = forecaster.forecast_prophet(n_periods=60)
```

### Task 3: Save and Load Models

```python
# Save
trainer.save_model('Random Forest', 'models/my_model.pkl')

# Load
model = trainer.load_model('models/my_model.pkl')
```

### Task 4: Export Forecast to Excel

```python
import pandas as pd

forecast_df = forecaster.forecast_next_n_days(30)
forecast_df.to_excel('forecast_results.xlsx', index=False)
```

## 📁 Project Structure

```
futures_ml_1/
├── dataset/              # Your CSV datasets
├── notebooks/            # Jupyter notebooks
├── src/                  # Core modules
│   ├── data_preprocessing.py
│   ├── eda.py
│   ├── model_training.py
│   └── forecasting.py
├── app/                  # Streamlit web app
│   └── streamlit_app.py
├── models/               # Saved trained models
├── output/               # Generated plots and results
├── main.py              # Complete pipeline script
├── requirements.txt     # Python dependencies
└── README.md           # Full documentation
```

## 🔧 Troubleshooting

### Issue: Prophet installation fails

**Solution:**
```bash
# Try installing prophet separately
pip install prophet --upgrade

# Or use conda
conda install -c conda-forge prophet
```

### Issue: "No module named 'src'"

**Solution:**
```python
# Add to top of your script
import sys
sys.path.append('path/to/futures_ml_1')
```

### Issue: Plots not showing in Jupyter

**Solution:**
```python
# Add to notebook
%matplotlib inline
import matplotlib.pyplot as plt
```

### Issue: Streamlit app won't start

**Solution:**
```bash
# Ensure streamlit is installed
pip install streamlit --upgrade

# Run with full path
python -m streamlit run app/streamlit_app.py
```

## 💡 Tips for Best Results

1. **Data Quality:**
   - Use at least 6 months of historical data
   - Ensure consistent date format
   - Handle missing values appropriately

2. **Model Selection:**
   - Random Forest: Good for non-linear patterns
   - XGBoost: Best overall performance usually
   - Prophet: Excellent for time-series with seasonality
   - ARIMA: Good for stationary time-series

3. **Feature Engineering:**
   - Enable lag features for time-dependent patterns
   - Include holiday/promotion indicators if available
   - Add external factors (weather, events)

4. **Forecasting:**
   - Prophet works better for longer forecasts (30+ days)
   - ARIMA better for shorter forecasts (7-14 days)
   - Use confidence intervals to assess uncertainty

## 🎓 Next Steps

1. **Explore the Jupyter Notebook:**
   ```bash
   jupyter notebook notebooks/sales_forecasting_demo.ipynb
   ```

2. **Customize the Models:**
   - Experiment with hyperparameters
   - Try different feature combinations
   - Add custom features

3. **Deploy the App:**
   - Deploy Streamlit app to cloud
   - Create REST API with Flask/FastAPI
   - Set up automated retraining

4. **Read Full Documentation:**
   - Check `README.md` for detailed info
   - Review code comments in each module

## 📞 Need Help?

- **Documentation:** See README.md
- **Code Examples:** Check notebooks/
- **Module Help:** Use Python's help() function
  ```python
  from src.model_training import ModelTrainer
  help(ModelTrainer)
  ```

## ✨ Features Checklist

- [x] Data preprocessing and cleaning
- [x] Exploratory data analysis
- [x] Multiple ML models (Linear, RF, XGBoost)
- [x] Time-series forecasting (ARIMA, Prophet)
- [x] Interactive web application
- [x] Model comparison and evaluation
- [x] Feature importance analysis
- [x] Export capabilities (CSV, Excel)
- [x] Comprehensive visualizations
- [x] Business insights generation

---

**Ready to forecast?** Run `python main.py` and let's go! 🚀
