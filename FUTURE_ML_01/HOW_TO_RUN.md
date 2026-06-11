# 🚀 How to Run the Application - Step by Step

## ✅ Prerequisites Check

Before running, ensure you have:
- ✅ Python 3.8 or higher installed
- ✅ pip (Python package manager)
- ✅ Internet connection (for installing packages)

---

## 🏃 Method 1: Using the Batch File (Windows - Easiest!)

### **Step 1: Open File Explorer**
1. Press `Windows Key + E` to open File Explorer
2. Navigate to: `C:\Users\saisa\OneDrive\Desktop\Documents\futures_ml_1\FUTURE_ML_01`

### **Step 2: Double-Click the Batch File**
1. Find the file: `run_project.bat`
2. Double-click it
3. A command window will open and automatically:
   - Install required packages
   - Run the forecasting pipeline
   - Generate all outputs

### **Step 3: Wait for Completion**
- Execution time: 30-60 seconds
- You'll see progress messages
- When complete, press any key to close

### **Step 4: Check the Results**
Navigate to these folders to see the outputs:
- `outputs/` - 4 CSV/TXT files with results
- `images/` - 5 PNG visualization files
- `models/` - 1 trained model file

---

## 💻 Method 2: Using Command Prompt (Windows)

### **Step 1: Open Command Prompt**
1. Press `Windows Key + R`
2. Type: `cmd`
3. Press Enter

### **Step 2: Navigate to Project Folder**
```cmd
cd C:\Users\saisa\OneDrive\Desktop\Documents\futures_ml_1\FUTURE_ML_01
```

### **Step 3: Install Dependencies (First Time Only)**
```cmd
pip install -r requirements.txt
```

Wait for installation to complete (30-60 seconds)

### **Step 4: Run the Project**
```cmd
python main.py
```

### **Step 5: Watch the Progress**
You'll see output like:
```
================================================================================
FUTURE INTERNS - TASK 1
Sales & Demand Forecasting for Businesses
================================================================================

STEP 1: DATA PREPARATION & FEATURE ENGINEERING
✓ Features created...

STEP 2: DATA SPLITTING (CHRONOLOGICAL)
✓ Training: 335 days, Test: 30 days...

STEP 3: MODEL TRAINING
✓ Random Forest trained
✓ XGBoost trained

STEP 4: MODEL EVALUATION
🏆 BEST MODEL: XGBoost (R² = 0.8767)

STEP 5: FORECASTING NEXT 30 DAYS
✓ Forecast generated...

STEP 6: GENERATING VISUALIZATIONS
✓ All visualizations created

STEP 7: GENERATING BUSINESS INSIGHTS
✓ Business insights generated

STEP 8: SAVING RESULTS
✓ All files saved

EXECUTION COMPLETED SUCCESSFULLY!
✅ Task 1 completed! Ready for submission.
```

---

## 🐍 Method 3: Using Python IDLE

### **Step 1: Open Python IDLE**
1. Search for "IDLE" in Windows Start Menu
2. Click "IDLE (Python 3.x)"

### **Step 2: Open the Main Script**
1. In IDLE, click `File` → `Open`
2. Navigate to: `C:\Users\saisa\OneDrive\Desktop\Documents\futures_ml_1\FUTURE_ML_01\main.py`
3. Click Open

### **Step 3: Run the Script**
1. Press `F5` or click `Run` → `Run Module`
2. Watch the output in the Shell window

---

## 🔧 Method 4: Using VS Code (If Installed)

### **Step 1: Open VS Code**
1. Open Visual Studio Code
2. Click `File` → `Open Folder`
3. Select: `C:\Users\saisa\OneDrive\Desktop\Documents\futures_ml_1\FUTURE_ML_01`

### **Step 2: Open Terminal in VS Code**
1. Press `Ctrl + ~` (backtick) or
2. Click `Terminal` → `New Terminal`

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 4: Run the Project**
```bash
python main.py
```

---

## 📊 What Gets Created

After running, you'll see these new files:

### **📁 dataset/ (1 file)**
```
revenue_data.csv - Sample revenue dataset (365 days)
```

### **📁 outputs/ (4 files)**
```
forecast_results.csv        - 30-day revenue predictions
evaluation_metrics.txt      - Model performance metrics
business_insights.txt       - Business analysis report
feature_importance.csv      - Feature rankings
```

### **📁 models/ (1 file)**
```
trained_model.pkl          - Trained XGBoost model (~2MB)
```

### **📁 images/ (5 files)**
```
actual_vs_predicted.png    - Model validation chart
future_forecast.png        - 30-day forecast visualization
feature_importance.png     - Top features bar chart
forecast_confidence.png    - Confidence intervals
model_comparison.png       - Random Forest vs XGBoost comparison
```

---

## 🎯 Quick Verification

To verify everything worked:

1. ✅ Check `outputs/` folder - Should have 4 files
2. ✅ Check `images/` folder - Should have 5 PNG files
3. ✅ Check `models/` folder - Should have 1 PKL file
4. ✅ Open `outputs/business_insights.txt` - Should have analysis
5. ✅ Open any PNG in `images/` - Should see visualizations

---

## ❓ Troubleshooting

### **Problem: "Python is not recognized"**
**Solution:**
```cmd
# Check if Python is installed
python --version

# If not installed, download from: https://www.python.org/downloads/
# During installation, CHECK "Add Python to PATH"
```

### **Problem: "No module named 'pandas'"**
**Solution:**
```cmd
pip install -r requirements.txt
```

### **Problem: "Permission denied"**
**Solution:**
- Right-click Command Prompt
- Select "Run as administrator"
- Try again

### **Problem: Path with spaces causes errors**
**Solution:**
```cmd
# Use quotes around the path
cd "C:\Users\saisa\OneDrive\Desktop\Documents\futures_ml_1\FUTURE_ML_01"
```

### **Problem: "ModuleNotFoundError: No module named 'src'"**
**Solution:**
- Make sure you're in the FUTURE_ML_01 directory
- Check that the `src/` folder exists with 3 Python files

### **Problem: Execution is slow**
**Solution:**
- Normal execution time is 30-60 seconds
- Model training takes the most time
- Be patient, it will complete

---

## 🎓 Understanding the Output

### **Console Output Sections:**

1. **Data Preparation** - Loading and feature engineering
2. **Data Splitting** - Creating train/test sets
3. **Model Training** - Training Random Forest & XGBoost
4. **Model Evaluation** - Comparing models, selecting best
5. **Forecasting** - Generating 30-day predictions
6. **Visualizations** - Creating 5 charts
7. **Business Insights** - Generating analysis
8. **Saving Results** - Writing files to disk

### **Success Indicators:**
```
✓ Data loaded successfully
✓ Features created
✓ Models trained
🏆 BEST MODEL: XGBoost
✓ Forecast generated
✓ All visualizations created
✓ Business insights generated
✅ Task 1 completed! Ready for submission.
```

---

## 💡 Tips for Best Results

1. **Close other programs** - For faster execution
2. **Stable internet** - For package installation
3. **Don't interrupt** - Let it complete fully
4. **Check outputs** - Verify all files were created
5. **Read business_insights.txt** - Understand the results

---

## 🔄 Running Again

If you want to run the project again:

1. **Clean previous outputs** (optional):
   ```cmd
   del outputs\*.* /Q
   del images\*.* /Q
   del models\*.* /Q
   del dataset\*.* /Q
   ```

2. **Run again**:
   ```cmd
   python main.py
   ```

3. **New outputs** will be generated

---

## 📱 Need Help?

If you encounter issues:

1. Check the `QUICK_START.txt` file
2. Read the `README.md` for detailed info
3. Review error messages carefully
4. Ensure all prerequisites are met
5. Try Method 1 (batch file) - it's the easiest

---

## ✅ Success!

When you see this message:
```
✅ Task 1 completed! Ready for submission.
```

You're done! Your project has:
- ✅ Generated 10 output files
- ✅ Trained a machine learning model
- ✅ Created 5 visualizations
- ✅ Generated business insights
- ✅ Everything ready for submission

---

**🎉 Congratulations! Your forecasting system is running!** 🎉

Next step: Upload to GitHub (see `GITHUB_UPLOAD_GUIDE.md`)
