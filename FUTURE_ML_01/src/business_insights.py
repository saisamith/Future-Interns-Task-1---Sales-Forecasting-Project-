"""
FUTURE INTERNS - Task 1: Business Insights Module
Author: Future Intern
Date: June 11, 2026

This module generates business insights from the forecasting analysis.
"""

import pandas as pd
import numpy as np


class BusinessInsightsGenerator:
    """
    Generates actionable business insights from forecasting results
    """
    
    def __init__(self, model):
        """
        Initialize insights generator
        
        Args:
            model: Trained RevenueForecastingModel instance
        """
        self.model = model
        self.insights = []
        print("✓ BusinessInsightsGenerator initialized")
    
    def analyze_revenue_trends(self):
        """
        Analyze historical revenue trends
        
        Returns:
            dict: Revenue trend analysis
        """
        df = self.model.df.copy()
        
        # Overall trend
        revenue_series = df[self.model.target_column]
        mean_revenue = revenue_series.mean()
        std_revenue = revenue_series.std()
        
        # Growth analysis
        first_half = revenue_series[:len(revenue_series)//2].mean()
        second_half = revenue_series[len(revenue_series)//2:].mean()
        growth_rate = ((second_half - first_half) / first_half) * 100
        
        # Volatility
        cv = (std_revenue / mean_revenue) * 100  # Coefficient of variation
        
        insight = f"""
📊 **REVENUE TREND ANALYSIS**

Historical Performance:
- Average Daily Revenue: ${mean_revenue:,.2f}
- Standard Deviation: ${std_revenue:,.2f}
- Revenue Volatility: {cv:.2f}% (Coefficient of Variation)

Growth Trend:
- First Half Average: ${first_half:,.2f}
- Second Half Average: ${second_half:,.2f}
- Growth Rate: {growth_rate:+.2f}%
"""
        
        if growth_rate > 5:
            insight += "\n✓ Strong positive growth trend observed"
        elif growth_rate > 0:
            insight += "\n✓ Moderate positive growth trend"
        elif growth_rate < -5:
            insight += "\n⚠ Declining revenue trend - requires attention"
        else:
            insight += "\n→ Stable revenue with minimal growth"
        
        self.insights.append(insight)
        return {
            'mean': mean_revenue,
            'std': std_revenue,
            'growth_rate': growth_rate,
            'volatility': cv
        }
    
    def analyze_seasonal_patterns(self):
        """
        Analyze seasonal patterns in revenue
        
        Returns:
            dict: Seasonal analysis results
        """
        df = self.model.df.copy()
        
        # Day of week analysis
        dow_revenue = df.groupby('DayOfWeek')[self.model.target_column].agg(['mean', 'std']).round(2)
        dow_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dow_revenue.index = dow_names
        best_day = dow_revenue['mean'].idxmax()
        worst_day = dow_revenue['mean'].idxmin()
        
        # Monthly analysis
        month_revenue = df.groupby('Month')[self.model.target_column].agg(['mean', 'std']).round(2)
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        best_month = month_names[month_revenue['mean'].idxmax() - 1]
        worst_month = month_names[month_revenue['mean'].idxmin() - 1]
        
        # Weekend vs Weekday
        weekend_revenue = df[df['IsWeekend'] == 1][self.model.target_column].mean()
        weekday_revenue = df[df['IsWeekend'] == 0][self.model.target_column].mean()
        weekend_diff = ((weekend_revenue - weekday_revenue) / weekday_revenue) * 100
        
        insight = f"""
📅 **SEASONAL PATTERN ANALYSIS**

Day of Week Patterns:
- Best Day: {best_day} (${dow_revenue.loc[best_day, 'mean']:,.2f})
- Lowest Day: {worst_day} (${dow_revenue.loc[worst_day, 'mean']:,.2f})
- Weekend vs Weekday: {weekend_diff:+.2f}% difference

Monthly Patterns:
- Best Month: {best_month} (${month_revenue.loc[month_revenue['mean'].idxmax(), 'mean']:,.2f})
- Lowest Month: {worst_month} (${month_revenue.loc[month_revenue['mean'].idxmin(), 'mean']:,.2f})
"""
        
        if abs(weekend_diff) > 10:
            if weekend_diff > 0:
                insight += "\n✓ Significantly higher weekend revenue - optimize weekend operations"
            else:
                insight += "\n✓ Significantly higher weekday revenue - focus on weekday promotions"
        
        self.insights.append(insight)
        return {
            'best_day': best_day,
            'worst_day': worst_day,
            'best_month': best_month,
            'worst_month': worst_month,
            'weekend_diff': weekend_diff
        }
    
    def analyze_forecast_implications(self):
        """
        Analyze implications of the forecast
        
        Returns:
            dict: Forecast implications
        """
        forecast_df = self.model.forecast_results
        historical_mean = self.model.df[self.model.target_column].mean()
        forecast_mean = forecast_df['Forecasted_Revenue'].mean()
        forecast_total = forecast_df['Forecasted_Revenue'].sum()
        
        # Compare forecast with historical
        forecast_vs_historical = ((forecast_mean - historical_mean) / historical_mean) * 100
        
        # Forecast volatility
        forecast_std = forecast_df['Forecasted_Revenue'].std()
        forecast_cv = (forecast_std / forecast_mean) * 100
        
        # Model confidence
        r2_score = self.model.evaluation_results[self.model.best_model_name]['R2']
        mape = self.model.evaluation_results[self.model.best_model_name]['MAPE']
        
        insight = f"""
🔮 **FORECAST IMPLICATIONS**

30-Day Forecast Summary:
- Forecasted Average Daily Revenue: ${forecast_mean:,.2f}
- Total 30-Day Revenue: ${forecast_total:,.2f}
- Forecast vs Historical Average: {forecast_vs_historical:+.2f}%

Model Confidence:
- R² Score: {r2_score:.4f} ({r2_score*100:.1f}% variance explained)
- MAPE: {mape:.2f}% (prediction error)
- Model Used: {self.model.best_model_name}
"""
        
        if r2_score > 0.8:
            insight += "\n✓ High model confidence - reliable forecast"
        elif r2_score > 0.6:
            insight += "\n→ Good model confidence - forecast is reasonably reliable"
        else:
            insight += "\n⚠ Moderate confidence - use forecast with caution"
        
        if forecast_vs_historical > 10:
            insight += "\n✓ Forecast indicates significant revenue increase"
        elif forecast_vs_historical < -10:
            insight += "\n⚠ Forecast indicates potential revenue decline"
        else:
            insight += "\n→ Forecast indicates stable revenue levels"
        
        self.insights.append(insight)
        return {
            'forecast_mean': forecast_mean,
            'forecast_total': forecast_total,
            'forecast_vs_historical': forecast_vs_historical,
            'r2_score': r2_score,
            'mape': mape
        }
    
    def generate_recommendations(self):
        """
        Generate actionable recommendations for decision makers
        
        Returns:
            str: Recommendations text
        """
        recommendations = """
💡 **RECOMMENDATIONS FOR DECISION MAKERS**

1. Inventory Management:
   - Plan inventory levels based on forecasted daily revenue
   - Increase stock during predicted high-revenue periods
   - Optimize reorder points using forecast confidence intervals

2. Staffing & Operations:
   - Adjust staffing levels based on day-of-week patterns
   - Schedule more staff during peak days identified in analysis
   - Consider flexible staffing for volatile revenue periods

3. Marketing & Promotions:
   - Target promotions during historically low-revenue periods
   - Capitalize on seasonal patterns with strategic campaigns
   - Use forecast to plan promotional budgets

4. Financial Planning:
   - Use 30-day forecast for cash flow projections
   - Plan expenses considering revenue volatility
   - Set realistic targets based on growth trends

5. Risk Management:
   - Monitor actual vs forecasted performance weekly
   - Investigate significant deviations (>10%) immediately
   - Maintain buffer inventory for forecast uncertainty

6. Continuous Improvement:
   - Retrain model monthly with new data
   - Track forecast accuracy and adjust strategies
   - Consider external factors (holidays, events) for manual adjustments
"""
        
        self.insights.append(recommendations)
        return recommendations
    
    def generate_all_insights(self, save_path='outputs/business_insights.txt'):
        """
        Generate all insights and save to file
        
        Args:
            save_path (str): Path to save insights
        """
        print("\n" + "="*70)
        print("STEP 7: GENERATING BUSINESS INSIGHTS")
        print("="*70)
        
        # Generate all analyses
        trend_analysis = self.analyze_revenue_trends()
        seasonal_analysis = self.analyze_seasonal_patterns()
        forecast_analysis = self.analyze_forecast_implications()
        recommendations = self.generate_recommendations()
        
        # Compile full report
        full_report = f"""
{'='*80}
BUSINESS INSIGHTS REPORT
Future Interns - Task 1: Sales & Demand Forecasting for Businesses
Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*80}

{self.insights[0]}

{self.insights[1]}

{self.insights[2]}

{self.insights[3]}

{'='*80}
CONCLUSION

This analysis provides data-driven insights for strategic decision-making.
The forecasting model has been validated and shows reliable performance.
Regular monitoring and model updates are recommended for sustained accuracy.

For questions or clarifications, please refer to the technical documentation.
{'='*80}
"""
        
        # Save to file
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(full_report)
        
        print(f"\n✓ Business insights saved to: {save_path}")
        
        # Print to console
        print("\n" + "="*70)
        print("BUSINESS INSIGHTS SUMMARY")
        print("="*70)
        for insight in self.insights:
            print(insight)
        
        return full_report


# Example usage
if __name__ == "__main__":
    print("Business Insights Generator Module")
    print("This module is designed to be imported and used by the main script")
