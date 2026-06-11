"""
Exploratory Data Analysis Module
Generates visualizations and insights from sales data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')


class EDA:
    """
    Class to perform exploratory data analysis on sales data
    """
    
    def __init__(self, df, date_column='Date'):
        """
        Initialize EDA class
        
        Args:
            df (pd.DataFrame): Preprocessed dataframe
            date_column (str): Name of the date column
        """
        self.df = df.copy()
        self.date_column = date_column
        self.insights = []
        
        # Set style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 6)
    
    def monthly_sales_trend(self, value_column='Units_Sold', save_path=None):
        """
        Visualize monthly sales trends
        
        Args:
            value_column (str): Column to analyze
            save_path (str): Path to save the plot
        """
        print(f"\n--- Analyzing Monthly {value_column} Trend ---")
        
        # Aggregate by month
        monthly_data = self.df.groupby(self.df[self.date_column].dt.to_period('M'))[value_column].agg(['sum', 'mean', 'count']).reset_index()
        monthly_data[self.date_column] = monthly_data[self.date_column].dt.to_timestamp()
        
        # Create subplots
        fig, axes = plt.subplots(2, 1, figsize=(14, 10))
        
        # Plot 1: Total monthly sales
        axes[0].plot(monthly_data[self.date_column], monthly_data['sum'], marker='o', linewidth=2, color='#2E86AB')
        axes[0].fill_between(monthly_data[self.date_column], monthly_data['sum'], alpha=0.3, color='#2E86AB')
        axes[0].set_title(f'Monthly Total {value_column}', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Month', fontsize=12)
        axes[0].set_ylabel(f'Total {value_column}', fontsize=12)
        axes[0].grid(True, alpha=0.3)
        
        # Plot 2: Average daily sales per month
        axes[1].bar(monthly_data[self.date_column], monthly_data['mean'], color='#A23B72', alpha=0.7)
        axes[1].set_title(f'Average Daily {value_column} per Month', fontsize=14, fontweight='bold')
        axes[1].set_xlabel('Month', fontsize=12)
        axes[1].set_ylabel(f'Average {value_column}', fontsize=12)
        axes[1].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Saved to: {save_path}")
        
        plt.close()
        
        # Generate insights
        max_month = monthly_data.loc[monthly_data['sum'].idxmax()]
        min_month = monthly_data.loc[monthly_data['sum'].idxmin()]
        avg_sales = monthly_data['sum'].mean()
        
        insight = f"📊 Monthly Trend: Peak sales in {max_month[self.date_column].strftime('%B %Y')} ({max_month['sum']:.0f}), Lowest in {min_month[self.date_column].strftime('%B %Y')} ({min_month['sum']:.0f}). Average: {avg_sales:.0f}"
        self.insights.append(insight)
        print(insight)
        
        return monthly_data
    
    def revenue_analysis(self, revenue_column='Revenue', save_path=None):
        """
        Analyze revenue trends
        
        Args:
            revenue_column (str): Revenue column name
            save_path (str): Path to save the plot
        """
        print(f"\n--- Analyzing {revenue_column} ---")
        
        if revenue_column not in self.df.columns:
            print(f"✗ Column '{revenue_column}' not found")
            return
        
        # Daily revenue
        daily_revenue = self.df.groupby(self.date_column)[revenue_column].sum().reset_index()
        
        # Create interactive plot
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Daily Revenue Trend', 'Revenue Distribution', 
                          'Monthly Revenue', 'Revenue Growth Rate'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Daily revenue trend
        fig.add_trace(
            go.Scatter(x=daily_revenue[self.date_column], y=daily_revenue[revenue_column],
                      mode='lines', name='Daily Revenue', line=dict(color='#06A77D')),
            row=1, col=1
        )
        
        # Revenue distribution
        fig.add_trace(
            go.Histogram(x=daily_revenue[revenue_column], name='Distribution',
                        marker=dict(color='#F18F01'), nbinsx=30),
            row=1, col=2
        )
        
        # Monthly revenue
        monthly_revenue = self.df.groupby(self.df[self.date_column].dt.to_period('M'))[revenue_column].sum().reset_index()
        monthly_revenue[self.date_column] = monthly_revenue[self.date_column].dt.to_timestamp()
        
        fig.add_trace(
            go.Bar(x=monthly_revenue[self.date_column], y=monthly_revenue[revenue_column],
                  name='Monthly Revenue', marker=dict(color='#D62828')),
            row=2, col=1
        )
        
        # Growth rate
        monthly_revenue['Growth_Rate'] = monthly_revenue[revenue_column].pct_change() * 100
        fig.add_trace(
            go.Scatter(x=monthly_revenue[self.date_column], y=monthly_revenue['Growth_Rate'],
                      mode='lines+markers', name='Growth %', line=dict(color='#003049')),
            row=2, col=2
        )
        
        fig.update_layout(height=800, showlegend=False, title_text="Revenue Analysis Dashboard")
        
        if save_path:
            fig.write_html(save_path.replace('.png', '.html'))
            print(f"✓ Saved to: {save_path.replace('.png', '.html')}")
        
        # Generate insights
        total_revenue = self.df[revenue_column].sum()
        avg_daily = daily_revenue[revenue_column].mean()
        max_day = daily_revenue.loc[daily_revenue[revenue_column].idxmax()]
        
        insight = f"💰 Revenue: Total ${total_revenue:,.2f}, Daily Average ${avg_daily:,.2f}, Best Day: {max_day[self.date_column].strftime('%Y-%m-%d')} (${max_day[revenue_column]:,.2f})"
        self.insights.append(insight)
        print(insight)
        
        return daily_revenue
    
    def product_demand_analysis(self, product_column='Product_Name', value_column='Units_Sold', top_n=10, save_path=None):
        """
        Analyze product-wise demand
        
        Args:
            product_column (str): Product column name
            value_column (str): Value column to analyze
            top_n (int): Number of top products to show
            save_path (str): Path to save the plot
        """
        print(f"\n--- Analyzing Product Demand ---")
        
        if product_column not in self.df.columns:
            print(f"⚠ Column '{product_column}' not found. Skipping product analysis.")
            return None
        
        # Aggregate by product
        product_sales = self.df.groupby(product_column)[value_column].agg(['sum', 'mean', 'count']).reset_index()
        product_sales = product_sales.sort_values('sum', ascending=False).head(top_n)
        
        # Create visualization
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # Top products by total sales
        axes[0].barh(product_sales[product_column], product_sales['sum'], color='#4ECDC4')
        axes[0].set_xlabel(f'Total {value_column}', fontsize=12)
        axes[0].set_title(f'Top {top_n} Products by Total {value_column}', fontsize=14, fontweight='bold')
        axes[0].invert_yaxis()
        
        # Average sales per transaction
        axes[1].barh(product_sales[product_column], product_sales['mean'], color='#FF6B6B')
        axes[1].set_xlabel(f'Average {value_column}', fontsize=12)
        axes[1].set_title(f'Top {top_n} Products by Average {value_column}', fontsize=14, fontweight='bold')
        axes[1].invert_yaxis()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Saved to: {save_path}")
        
        plt.close()
        
        # Insights
        top_product = product_sales.iloc[0]
        insight = f"🏆 Top Product: '{top_product[product_column]}' with {top_product['sum']:.0f} total {value_column} across {top_product['count']:.0f} transactions"
        self.insights.append(insight)
        print(insight)
        
        return product_sales
    
    def correlation_heatmap(self, save_path=None):
        """
        Generate correlation heatmap for numerical features
        
        Args:
            save_path (str): Path to save the plot
        """
        print("\n--- Generating Correlation Heatmap ---")
        
        # Select numerical columns
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Exclude some engineered features for cleaner visualization
        exclude_cols = ['Year', 'Month_Sin', 'Month_Cos', 'Weekday_Sin', 'Weekday_Cos']
        numerical_cols = [col for col in numerical_cols if col not in exclude_cols]
        
        # Limit to max 15 columns for readability
        if len(numerical_cols) > 15:
            numerical_cols = numerical_cols[:15]
        
        # Calculate correlation
        correlation_matrix = self.df[numerical_cols].corr()
        
        # Create heatmap
        plt.figure(figsize=(12, 10))
        mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
        
        sns.heatmap(correlation_matrix, mask=mask, annot=True, fmt='.2f', 
                   cmap='coolwarm', center=0, square=True, linewidths=1,
                   cbar_kws={"shrink": 0.8})
        
        plt.title('Correlation Heatmap of Features', fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Saved to: {save_path}")
        
        plt.close()
        
        # Find strong correlations
        strong_corr = []
        for i in range(len(correlation_matrix.columns)):
            for j in range(i+1, len(correlation_matrix.columns)):
                if abs(correlation_matrix.iloc[i, j]) > 0.7:
                    strong_corr.append((correlation_matrix.columns[i], 
                                      correlation_matrix.columns[j], 
                                      correlation_matrix.iloc[i, j]))
        
        if strong_corr:
            insight = f"🔗 Strong Correlations: Found {len(strong_corr)} pairs with correlation > 0.7"
            self.insights.append(insight)
            print(insight)
            for col1, col2, corr in strong_corr[:3]:  # Show top 3
                print(f"   {col1} ↔ {col2}: {corr:.2f}")
        
        return correlation_matrix
    
    def seasonal_patterns(self, value_column='Units_Sold', save_path=None):
        """
        Analyze seasonal patterns
        
        Args:
            value_column (str): Column to analyze
            save_path (str): Path to save the plot
        """
        print(f"\n--- Analyzing Seasonal Patterns ---")
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 10))
        
        # Day of week pattern
        dow_sales = self.df.groupby('Weekday')[value_column].mean()
        dow_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        axes[0, 0].bar(range(7), dow_sales.values, color='#6A4C93')
        axes[0, 0].set_xticks(range(7))
        axes[0, 0].set_xticklabels(dow_names)
        axes[0, 0].set_title('Average Sales by Day of Week', fontsize=12, fontweight='bold')
        axes[0, 0].set_ylabel(f'Average {value_column}')
        
        # Monthly pattern
        month_sales = self.df.groupby('Month')[value_column].mean()
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        axes[0, 1].plot(range(1, 13), month_sales.values, marker='o', linewidth=2, markersize=8, color='#1982C4')
        axes[0, 1].set_xticks(range(1, 13))
        axes[0, 1].set_xticklabels(month_names, rotation=45)
        axes[0, 1].set_title('Average Sales by Month', fontsize=12, fontweight='bold')
        axes[0, 1].set_ylabel(f'Average {value_column}')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Quarterly pattern
        if 'Quarter' in self.df.columns:
            quarter_sales = self.df.groupby('Quarter')[value_column].sum()
            axes[1, 0].bar(quarter_sales.index, quarter_sales.values, color='#FF595E')
            axes[1, 0].set_xlabel('Quarter')
            axes[1, 0].set_title('Total Sales by Quarter', fontsize=12, fontweight='bold')
            axes[1, 0].set_ylabel(f'Total {value_column}')
        
        # Year over year (if multiple years)
        if 'Year' in self.df.columns and self.df['Year'].nunique() > 1:
            yearly_sales = self.df.groupby('Year')[value_column].sum()
            axes[1, 1].bar(yearly_sales.index, yearly_sales.values, color='#FFCA3A')
            axes[1, 1].set_xlabel('Year')
            axes[1, 1].set_title('Total Sales by Year', fontsize=12, fontweight='bold')
            axes[1, 1].set_ylabel(f'Total {value_column}')
        else:
            axes[1, 1].text(0.5, 0.5, 'Insufficient data\nfor yearly comparison', 
                          ha='center', va='center', fontsize=12)
            axes[1, 1].axis('off')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Saved to: {save_path}")
        
        plt.close()
        
        # Insights
        best_dow = dow_names[dow_sales.idxmax()]
        best_month = month_names[month_sales.idxmax() - 1]
        
        insight = f"📅 Seasonal Patterns: Best day is {best_dow}, Best month is {best_month}"
        self.insights.append(insight)
        print(insight)
    
    def generate_all_visualizations(self, output_dir='output', value_column='Units_Sold', revenue_column='Revenue'):
        """
        Generate all visualizations at once
        
        Args:
            output_dir (str): Directory to save plots
            value_column (str): Main value column
            revenue_column (str): Revenue column
        """
        print("\n" + "=" * 60)
        print("GENERATING ALL VISUALIZATIONS")
        print("=" * 60)
        
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate all plots
        self.monthly_sales_trend(value_column, f'{output_dir}/monthly_sales_trend.png')
        
        if revenue_column in self.df.columns:
            self.revenue_analysis(revenue_column, f'{output_dir}/revenue_analysis.png')
        
        # Try product analysis with common column names
        product_cols = ['Product_Name', 'Product', 'Category', 'Product_Category']
        for col in product_cols:
            if col in self.df.columns:
                self.product_demand_analysis(col, value_column, save_path=f'{output_dir}/product_demand.png')
                break
        
        self.correlation_heatmap(f'{output_dir}/correlation_heatmap.png')
        self.seasonal_patterns(value_column, f'{output_dir}/seasonal_patterns.png')
        
        print("\n" + "=" * 60)
        print("ALL VISUALIZATIONS COMPLETED")
        print("=" * 60)
        
        # Print all insights
        print("\n📋 BUSINESS INSIGHTS SUMMARY:")
        print("-" * 60)
        for i, insight in enumerate(self.insights, 1):
            print(f"{i}. {insight}")
        
        return self.insights


# Example usage
if __name__ == "__main__":
    print("Exploratory Data Analysis Module")
    print("Generates visualizations and business insights")
    print("\nUsage:")
    print("  eda = EDA(df_clean)")
    print("  eda.generate_all_visualizations()")
