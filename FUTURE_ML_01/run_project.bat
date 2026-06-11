@echo off
echo ================================================================================
echo FUTURE INTERNS - Task 1: Sales & Demand Forecasting
echo ================================================================================
echo.

echo Installing dependencies...
pip install -q pandas numpy scikit-learn xgboost matplotlib seaborn joblib

echo.
echo Running forecasting pipeline...
python main.py

echo.
echo ================================================================================
echo Project execution completed!
echo Check the outputs/, models/, and images/ folders for results.
echo ================================================================================
pause
