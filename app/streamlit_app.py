"""
Streamlit Web Application for Sales & Demand Forecasting
"""

import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from src.data_preprocessing import DataPreprocessor
from src.eda import EDA
from src.model_training import ModelTrainer
from src.forecasting import Forecaster


# Page configuration
st.set_page_config(
    page_title="Sales & Demand Forecasting",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #A23B72;
        margin-top: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stButton>button {
        background-color: #2E86AB;
        color: white;
        font-size: 1rem;
        padding: 0.5rem 2rem;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """
    Main application function
    """
    
    # Title and description
    st.markdown('<h1 class="main-header">📊 Sales & Demand Forecasting System</h1>', unsafe_allow_html=True)
    st.markdown("### Predict future sales demand and generate actionable business insights")
    
    # Sidebar
    st.sidebar.title("⚙️ Configuration")
    st.sidebar.markdown("---")
    
    # File upload
    st.sidebar.subheader("📁 Upload Dataset")
    uploaded_file = st.sidebar.file_uploader(
        "Upload your CSV file",
        type=['csv'],
        help="Upload a CSV file with Date, Product, Units_Sold, Revenue columns"
    )
    
    if uploaded_file is None:
        # Show welcome page
        show_welcome_page()
        return
    
    # Load data
    try:
        df_raw = pd.read_csv(uploaded_file)
        st.sidebar.success(f"✓ Data loaded: {len(df_raw)} rows")
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return
    
    # Show raw data preview
    with st.expander("🔍 View Raw Data"):
        st.dataframe(df_raw.head(10), use_container_width=True)
        st.write(f"**Shape:** {df_raw.shape[0]} rows × {df_raw.shape[1]} columns")
    
    # Sidebar configuration
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎯 Select Columns")
    
    # Column selection
    date_column = st.sidebar.selectbox(
        "Date Column",
        df_raw.columns.tolist(),
        index=0 if 'Date' in df_raw.columns else 0
    )
    
    numeric_columns = df_raw.select_dtypes(include=[np.number]).columns.tolist()
    target_column = st.sidebar.selectbox(
        "Target Column (to predict)",
        numeric_columns,
        index=0 if numeric_columns else 0
    )
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Data Analysis", "🤖 Model Training", "🔮 Forecasting", "📥 Export Results"])
    
    # ===== TAB 1: Data Analysis =====
    with tab1:
        st.markdown('<h2 class="sub-header">📊 Exploratory Data Analysis</h2>', unsafe_allow_html=True)
        
        if st.button("🚀 Run Data Analysis", key="run_eda"):
            with st.spinner("Processing data..."):
                # Preprocess data
                # Save to temp file
                temp_path = "temp_data.csv"
                df_raw.to_csv(temp_path, index=False)
                
                preprocessor = DataPreprocessor(temp_path)
                df_clean = preprocessor.preprocess(date_column=date_column)
                
                # Store in session state
                st.session_state['df_clean'] = df_clean
                st.session_state['preprocessor'] = preprocessor
                
                # Clean up temp file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                
                st.success("✓ Data preprocessing completed!")
            
            # Display data summary
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Records", len(df_clean))
            with col2:
                st.metric("Features", df_clean.shape[1])
            with col3:
                st.metric("Missing Values", df_clean.isnull().sum().sum())
            with col4:
                date_range = (df_clean[date_column].max() - df_clean[date_column].min()).days
                st.metric("Date Range (days)", date_range)
            
            # EDA
            st.markdown("### 📈 Visualizations")
            
            with st.spinner("Generating visualizations..."):
                eda = EDA(df_clean, date_column=date_column)
                
                # Monthly trend
                st.subheader("Monthly Sales Trend")
                monthly_data = df_clean.groupby(df_clean[date_column].dt.to_period('M'))[target_column].sum().reset_index()
                monthly_data[date_column] = monthly_data[date_column].dt.to_timestamp()
                
                fig = px.line(monthly_data, x=date_column, y=target_column, 
                             title=f'Monthly {target_column} Trend',
                             markers=True)
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                
                # Distribution
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader(f"{target_column} Distribution")
                    fig = px.histogram(df_clean, x=target_column, nbins=50,
                                     title=f'Distribution of {target_column}')
                    fig.update_layout(height=350)
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.subheader(f"{target_column} Statistics")
                    stats = df_clean[target_column].describe()
                    st.dataframe(stats, use_container_width=True)
                
                # Seasonal patterns
                if 'Weekday' in df_clean.columns:
                    st.subheader("Day of Week Pattern")
                    dow_sales = df_clean.groupby('Weekday')[target_column].mean().reset_index()
                    dow_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                    dow_sales['Day'] = dow_sales['Weekday'].apply(lambda x: dow_names[x])
                    
                    fig = px.bar(dow_sales, x='Day', y=target_column,
                               title=f'Average {target_column} by Day of Week',
                               color=target_column)
                    fig.update_layout(height=350)
                    st.plotly_chart(fig, use_container_width=True)
    
    # ===== TAB 2: Model Training =====
    with tab2:
        st.markdown('<h2 class="sub-header">🤖 Machine Learning Model Training</h2>', unsafe_allow_html=True)
        
        if 'df_clean' not in st.session_state:
            st.warning("⚠️ Please run Data Analysis first!")
        else:
            df_clean = st.session_state['df_clean']
            
            st.sidebar.markdown("---")
            st.sidebar.subheader("🔧 Model Selection")
            
            # Model selection
            models_to_train = st.sidebar.multiselect(
                "Select models to train",
                ["Linear Regression", "Random Forest", "XGBoost"],
                default=["Random Forest", "XGBoost"]
            )
            
            test_size = st.sidebar.slider("Test Set Size (%)", 10, 40, 20) / 100
            
            if st.button("🚀 Train Models", key="train_models"):
                if not models_to_train:
                    st.error("Please select at least one model!")
                else:
                    with st.spinner("Training models... This may take a few minutes..."):
                        trainer = ModelTrainer(df_clean, target_column=target_column, date_column=date_column)
                        trainer.split_data(test_size=test_size)
                        
                        results = {}
                        
                        # Train selected models
                        if "Linear Regression" in models_to_train:
                            with st.status("Training Linear Regression..."):
                                trainer.train_linear_regression()
                        
                        if "Random Forest" in models_to_train:
                            with st.status("Training Random Forest..."):
                                trainer.train_random_forest()
                        
                        if "XGBoost" in models_to_train:
                            with st.status("Training XGBoost..."):
                                try:
                                    trainer.train_xgboost()
                                except Exception as e:
                                    st.error(f"XGBoost failed: {str(e)}")
                        
                        # Store in session state
                        st.session_state['trainer'] = trainer
                        st.session_state['models_trained'] = True
                        
                        st.success("✓ All models trained successfully!")
                    
                    # Display results
                    st.markdown("### 📊 Model Performance Comparison")
                    
                    # Create comparison dataframe
                    comparison_data = []
                    for model_name, metrics in trainer.results.items():
                        comparison_data.append({
                            'Model': model_name,
                            'Test MAE': f"{metrics['test_mae']:.2f}",
                            'Test RMSE': f"{metrics['test_rmse']:.2f}",
                            'Test R²': f"{metrics['test_r2']:.4f}"
                        })
                    
                    df_comparison = pd.DataFrame(comparison_data)
                    st.dataframe(df_comparison, use_container_width=True)
                    
                    # Plot comparison
                    col1, col2, col3 = st.columns(3)
                    
                    metrics_df = pd.DataFrame([
                        {'Model': name, 'MAE': metrics['test_mae'], 
                         'RMSE': metrics['test_rmse'], 'R²': metrics['test_r2']}
                        for name, metrics in trainer.results.items()
                    ])
                    
                    with col1:
                        fig = px.bar(metrics_df, x='Model', y='MAE', 
                                   title='Mean Absolute Error',
                                   color='MAE')
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        fig = px.bar(metrics_df, x='Model', y='RMSE',
                                   title='Root Mean Squared Error',
                                   color='RMSE')
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col3:
                        fig = px.bar(metrics_df, x='Model', y='R²',
                                   title='R² Score',
                                   color='R²')
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Best model
                    best_model = metrics_df.loc[metrics_df['R²'].idxmax(), 'Model']
                    st.success(f"🏆 Best Model: **{best_model}** (Highest R² Score)")
                    
                    # Feature importance for tree-based models
                    if best_model in ['Random Forest', 'XGBoost']:
                        st.markdown(f"### 🎯 Feature Importance - {best_model}")
                        importance_df = trainer.get_feature_importance(best_model, top_n=10)
                        
                        if importance_df is not None:
                            fig = px.bar(importance_df, x='Importance', y='Feature',
                                       orientation='h',
                                       title=f'Top 10 Important Features - {best_model}')
                            st.plotly_chart(fig, use_container_width=True)
    
    # ===== TAB 3: Forecasting =====
    with tab3:
        st.markdown('<h2 class="sub-header">🔮 Time-Series Forecasting</h2>', unsafe_allow_html=True)
        
        if 'df_clean' not in st.session_state:
            st.warning("⚠️ Please run Data Analysis first!")
        else:
            df_clean = st.session_state['df_clean']
            
            st.sidebar.markdown("---")
            st.sidebar.subheader("🔮 Forecast Settings")
            
            forecast_model = st.sidebar.selectbox(
                "Select Forecasting Model",
                ["Prophet", "ARIMA"]
            )
            
            forecast_days = st.sidebar.slider("Forecast Period (days)", 7, 90, 30)
            
            if st.button("🚀 Generate Forecast", key="generate_forecast"):
                with st.spinner(f"Generating {forecast_days}-day forecast using {forecast_model}..."):
                    forecaster = Forecaster(df_clean, target_column=target_column, date_column=date_column)
                    
                    forecast_df = forecaster.forecast_next_n_days(
                        n_days=forecast_days,
                        model=forecast_model.lower()
                    )
                    
                    st.session_state['forecast_df'] = forecast_df
                    st.session_state['forecaster'] = forecaster
                    
                    st.success(f"✓ {forecast_days}-day forecast generated!")
                
                if forecast_df is not None:
                    # Display forecast
                    st.markdown("### 📈 Forecast Results")
                    
                    # Metrics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Average Forecast", f"{forecast_df['Forecast'].mean():.2f}")
                    with col2:
                        st.metric("Minimum", f"{forecast_df['Forecast'].min():.2f}")
                    with col3:
                        st.metric("Maximum", f"{forecast_df['Forecast'].max():.2f}")
                    with col4:
                        trend = "📈 Upward" if forecast_df['Forecast'].iloc[-1] > forecast_df['Forecast'].iloc[0] else "📉 Downward"
                        st.metric("Trend", trend)
                    
                    # Plot forecast
                    st.subheader("Forecast Visualization")
                    
                    # Combine historical and forecast
                    fig = go.Figure()
                    
                    # Historical data (last 90 days)
                    historical = df_clean.tail(90)
                    fig.add_trace(go.Scatter(
                        x=historical[date_column],
                        y=historical[target_column],
                        mode='lines',
                        name='Historical Data',
                        line=dict(color='#2E86AB', width=2)
                    ))
                    
                    # Forecast
                    fig.add_trace(go.Scatter(
                        x=forecast_df['Date'],
                        y=forecast_df['Forecast'],
                        mode='lines+markers',
                        name='Forecast',
                        line=dict(color='#D62828', width=2, dash='dash')
                    ))
                    
                    # Confidence interval
                    fig.add_trace(go.Scatter(
                        x=forecast_df['Date'].tolist() + forecast_df['Date'].tolist()[::-1],
                        y=forecast_df['Upper_CI'].tolist() + forecast_df['Lower_CI'].tolist()[::-1],
                        fill='toself',
                        fillcolor='rgba(214, 40, 40, 0.2)',
                        line=dict(color='rgba(255,255,255,0)'),
                        name='95% Confidence Interval',
                        showlegend=True
                    ))
                    
                    fig.update_layout(
                        title=f'{forecast_model} Forecast: {target_column}',
                        xaxis_title='Date',
                        yaxis_title=target_column,
                        height=500,
                        hovermode='x unified'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Forecast table
                    st.subheader("Forecast Data Table")
                    st.dataframe(forecast_df, use_container_width=True)
    
    # ===== TAB 4: Export Results =====
    with tab4:
        st.markdown('<h2 class="sub-header">📥 Export Results</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Download Processed Data")
            if 'df_clean' in st.session_state:
                csv = st.session_state['df_clean'].to_csv(index=False)
                st.download_button(
                    label="Download Processed Data (CSV)",
                    data=csv,
                    file_name="processed_sales_data.csv",
                    mime="text/csv"
                )
            else:
                st.info("Process data first to enable download")
        
        with col2:
            st.subheader("🔮 Download Forecast")
            if 'forecast_df' in st.session_state:
                csv = st.session_state['forecast_df'].to_csv(index=False)
                st.download_button(
                    label="Download Forecast (CSV)",
                    data=csv,
                    file_name="sales_forecast.csv",
                    mime="text/csv"
                )
            else:
                st.info("Generate forecast first to enable download")
        
        st.markdown("---")
        
        st.subheader("💾 Save Trained Models")
        if 'models_trained' in st.session_state and st.session_state['models_trained']:
            st.success("✓ Models are trained and ready to save")
            st.info("Models can be saved using the Model Training module's save_model() method")
        else:
            st.info("Train models first to enable saving")


def show_welcome_page():
    """
    Display welcome page when no file is uploaded
    """
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        ## 👋 Welcome!
        
        This application helps you forecast sales demand using advanced machine learning techniques.
        
        ### 📋 How to Get Started:
        
        1. **Upload your CSV dataset** using the sidebar
        2. **Run Data Analysis** to explore your data
        3. **Train ML Models** to build predictive models
        4. **Generate Forecasts** for future demand
        5. **Export Results** for further analysis
        
        ### 📊 Required Data Format:
        
        Your CSV should include:
        - **Date column** (YYYY-MM-DD format)
        - **Numerical target** (e.g., Units_Sold, Revenue)
        - Optional: Product, Category, Region columns
        
        ### 🎯 Features:
        
        - ✅ Automated data preprocessing
        - ✅ Interactive visualizations
        - ✅ Multiple ML models (Linear Regression, Random Forest, XGBoost)
        - ✅ Time-series forecasting (ARIMA, Prophet)
        - ✅ Model comparison and evaluation
        - ✅ Export results and forecasts
        
        ---
        
        ### 📝 Sample Data Format:
        
        ```
        Date,Product_Name,Units_Sold,Revenue,Region
        2023-01-01,Product A,150,15000,North
        2023-01-02,Product B,200,8000,South
        2023-01-03,Product A,175,17500,North
        ```
        
        ---
        
        **Ready?** Upload your dataset from the sidebar to begin! 🚀
        """)


if __name__ == "__main__":
    main()
