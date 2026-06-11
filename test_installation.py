"""
Installation and Setup Verification Script
Run this script to verify that all dependencies are correctly installed
"""

import sys
import importlib
from datetime import datetime


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(text.center(80))
    print("=" * 80)


def print_section(text):
    """Print formatted section"""
    print("\n" + "-" * 80)
    print(text)
    print("-" * 80)


def check_python_version():
    """Check Python version"""
    print_section("1. Python Version Check")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print(f"Python version: {version_str}")
    
    if version.major >= 3 and version.minor >= 8:
        print("✅ Python version is compatible (3.8+)")
        return True
    else:
        print("❌ Python 3.8 or higher is required")
        return False


def check_package(package_name, import_name=None):
    """
    Check if a package is installed
    
    Args:
        package_name (str): Name of the package
        import_name (str): Import name if different from package name
        
    Returns:
        bool: True if installed, False otherwise
    """
    if import_name is None:
        import_name = package_name
    
    try:
        module = importlib.import_module(import_name)
        version = getattr(module, '__version__', 'unknown')
        print(f"  ✅ {package_name:20s} version {version}")
        return True
    except ImportError:
        print(f"  ❌ {package_name:20s} NOT INSTALLED")
        return False


def check_core_packages():
    """Check all core packages"""
    print_section("2. Core Package Check")
    
    packages = [
        ('pandas', None),
        ('numpy', None),
        ('matplotlib', None),
        ('seaborn', None),
        ('sklearn', 'scikit-learn'),
        ('xgboost', None),
        ('statsmodels', None),
        ('prophet', None),
        ('streamlit', None),
        ('plotly', None),
        ('joblib', None),
        ('openpyxl', None)
    ]
    
    results = []
    for package_info in packages:
        if len(package_info) == 2:
            import_name, display_name = package_info
            display_name = display_name or import_name
        else:
            import_name = display_name = package_info[0]
        
        results.append(check_package(display_name, import_name))
    
    return all(results)


def check_project_structure():
    """Check if project directories exist"""
    print_section("3. Project Structure Check")
    
    import os
    
    required_dirs = [
        'dataset',
        'notebooks',
        'src',
        'app',
        'models',
        'output'
    ]
    
    required_files = [
        'README.md',
        'requirements.txt',
        'main.py',
        'config.py',
        'src/data_preprocessing.py',
        'src/eda.py',
        'src/model_training.py',
        'src/forecasting.py',
        'app/streamlit_app.py'
    ]
    
    all_good = True
    
    print("\nDirectories:")
    for directory in required_dirs:
        if os.path.exists(directory) and os.path.isdir(directory):
            print(f"  ✅ {directory}/")
        else:
            print(f"  ❌ {directory}/ NOT FOUND")
            all_good = False
    
    print("\nCore Files:")
    for file in required_files:
        if os.path.exists(file) and os.path.isfile(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} NOT FOUND")
            all_good = False
    
    return all_good


def check_module_imports():
    """Check if project modules can be imported"""
    print_section("4. Project Module Import Check")
    
    sys.path.append('.')
    
    modules = [
        'src.data_preprocessing',
        'src.eda',
        'src.model_training',
        'src.forecasting',
        'config'
    ]
    
    all_good = True
    
    for module_name in modules:
        try:
            importlib.import_module(module_name)
            print(f"  ✅ {module_name}")
        except Exception as e:
            print(f"  ❌ {module_name} - Error: {str(e)}")
            all_good = False
    
    return all_good


def run_quick_test():
    """Run a quick functionality test"""
    print_section("5. Quick Functionality Test")
    
    try:
        print("\n  Testing data preprocessing...")
        from src.data_preprocessing import DataPreprocessor
        print("  ✅ DataPreprocessor class loaded")
        
        print("\n  Testing EDA...")
        from src.eda import EDA
        print("  ✅ EDA class loaded")
        
        print("\n  Testing model training...")
        from src.model_training import ModelTrainer
        print("  ✅ ModelTrainer class loaded")
        
        print("\n  Testing forecasting...")
        from src.forecasting import Forecaster
        print("  ✅ Forecaster class loaded")
        
        print("\n  Creating test dataset...")
        import pandas as pd
        import numpy as np
        
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
        data = {
            'Date': dates,
            'Units_Sold': np.random.randint(100, 500, len(dates)),
            'Revenue': np.random.uniform(1000, 5000, len(dates))
        }
        df_test = pd.DataFrame(data)
        print(f"  ✅ Test dataset created: {len(df_test)} rows")
        
        print("\n  Testing basic preprocessing...")
        df_test['Year'] = df_test['Date'].dt.year
        df_test['Month'] = df_test['Date'].dt.month
        print("  ✅ Feature engineering works")
        
        print("\n  Testing visualization libraries...")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        plt.close(fig)
        print("  ✅ Matplotlib works")
        
        import seaborn as sns
        print("  ✅ Seaborn works")
        
        import plotly.graph_objects as go
        print("  ✅ Plotly works")
        
        return True
        
    except Exception as e:
        print(f"\n  ❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def check_system_info():
    """Display system information"""
    print_section("6. System Information")
    
    import platform
    
    print(f"  Operating System: {platform.system()} {platform.release()}")
    print(f"  Machine: {platform.machine()}")
    print(f"  Processor: {platform.processor()}")
    print(f"  Python Implementation: {platform.python_implementation()}")
    print(f"  Python Build: {platform.python_build()[0]}")


def generate_report(results):
    """Generate final report"""
    print_header("VERIFICATION REPORT")
    
    all_passed = all(results.values())
    
    print("\nTest Results:")
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"  {test_name:30s} {status}")
    
    print("\n" + "=" * 80)
    
    if all_passed:
        print("🎉 SUCCESS! All checks passed. Your environment is ready!")
        print("\nNext Steps:")
        print("  1. Run 'python main.py' to execute the complete pipeline")
        print("  2. Or run 'streamlit run app/streamlit_app.py' to launch the web app")
        print("  3. Check the QUICKSTART.md for more information")
    else:
        print("⚠️  WARNING! Some checks failed. Please fix the issues above.")
        print("\nRecommended Actions:")
        print("  1. Install missing packages: pip install -r requirements.txt")
        print("  2. Verify Python version is 3.8 or higher")
        print("  3. Check project structure and missing files")
        print("  4. Rerun this script to verify fixes")
    
    print("=" * 80)
    
    return all_passed


def main():
    """Main verification function"""
    print_header("🔍 Installation & Setup Verification")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    
    # Run all checks
    results['Python Version'] = check_python_version()
    results['Core Packages'] = check_core_packages()
    results['Project Structure'] = check_project_structure()
    results['Module Imports'] = check_module_imports()
    results['Functionality Test'] = run_quick_test()
    
    # System info
    check_system_info()
    
    # Generate report
    all_passed = generate_report(results)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
