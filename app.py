"""
Super Store Sales Dashboard - Modular Version
Business Intelligence Project
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from sklearn.linear_model import LinearRegression

# Import modular components
from components.styles import CSS_STYLES, apply_styles
from components.icons import SVG_ICONS
from components.kpi_cards import render_kpi_row1, render_kpi_row2, render_insights_section
from components.charts import (
    create_pie_chart, create_pie_chart_large,
    create_bar_chart_horizontal, create_bar_chart_vertical,
    create_line_chart
)
from components.sidebar import create_all_filters
from utils.data_loader import load_data, filter_data, calculate_kpis, get_top_insights
from utils.export_utils import dataframes_to_xlsx_bytes
from config.settings import CHART_COLORS, CHART_LAYOUT

# Page config
st.set_page_config(
    page_title="Super Store Sales Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set Plotly default template
pio.templates.default = "plotly_white"

# Apply CSS styles
st.markdown(CSS_STYLES, unsafe_allow_html=True)

# Load data
df = load_data()

# Create sidebar filters
filters = create_all_filters(df)

# Apply filters
filtered_df = filter_data(df, filters)

# === DASHBOARD HEADER ===
st.markdown('''
<div class="dashboard-header">
    <h1>🛒 Super Store Sales Dashboard</h1>
    <p>Interactive analytics dashboard for comprehensive sales performance monitoring</p>
</div>
''', unsafe_allow_html=True)

# === KPI SECTION ===
st.markdown(f'''
<p class="section-header">
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="#3b82f6" style="vertical-align: middle; margin-right: 8px;">
        <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 3v11.25A2.25 2.25 0 0 0 6 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0 1 18 16.5h-2.25m-7.5 0h7.5m-7.5 0-1 3m8.5-3 1 3m0 0 .5 1.5m-.5-1.5h-9.5m0 0-.5 1.5m.75-9 3-3 2.148 2.148A12.061 12.061 0 0 1 16.5 7.605" />
    </svg>
    Key Performance Indicators
</p>
''', unsafe_allow_html=True)

# Live stats row
st.markdown(f'''
<div class="live-stats-row">
    <div class="live-pill live-pill--badge">
        <span class="live-dot"></span>
        <span>Live Data</span>
    </div>
    <div class="live-pill">
        <span><i class="fas fa-filter"></i> Showing <strong>{len(filtered_df):,}</strong> of <strong style="color: #3b82f6;">{len(df):,}</strong> records</span>
    </div>
    <div class="live-pill">
        <span><i class="fas fa-calendar-check"></i> Last Updated: <strong>Real-time</strong></span>
    </div>
</div>
''', unsafe_allow_html=True)

# Calculate KPIs
kpis = calculate_kpis(filtered_df)

# Render KPI rows
st.markdown(render_kpi_row1(kpis), unsafe_allow_html=True)
st.markdown(render_kpi_row2(kpis), unsafe_allow_html=True)

st.markdown("---")

# === QUICK INSIGHTS ===
st.markdown(f'''
<p class="section-header">
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="#3b82f6" style="vertical-align: middle; margin-right: 8px;">
        <path stroke-linecap="round" stroke-linejoin="round" d="M12 18v-5.25m0 0a6.01 6.01 0 0 0 1.5-.189m-1.5.189a6.01 6.01 0 0 1-1.5-.189m3.75 7.478a12.06 12.06 0 0 1-4.5 0m3.75 2.383a14.406 14.406 0 0 1-3 0M14.25 18v-.192c0-.983.658-1.823 1.508-2.316a7.5 7.5 0 1 0-7.517 0c.85.493 1.509 1.333 1.509 2.316V18" />
    </svg>
    Quick Insights
</p>
''', unsafe_allow_html=True)

insights = get_top_insights(filtered_df)
st.markdown(render_insights_section(insights), unsafe_allow_html=True)

st.markdown("---")

# === DATA DISTRIBUTION OVERVIEW ===
st.markdown(f'''
<p class="section-header">
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="#3b82f6" style="vertical-align: middle; margin-right: 8px;">
        <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 6a7.5 7.5 0 1 0 7.5 7.5h-7.5V6Z" />
        <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 10.5H21A7.5 7.5 0 0 0 13.5 3v7.5Z" />
    </svg>
    Data Distribution Overview
</p>
''', unsafe_allow_html=True)

summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)

with summary_col1:
    category_counts = filtered_df.groupby('category').size().reset_index(name='count')
    fig_cat = create_pie_chart(category_counts, 'count', 'category', 'Category Distribution')
    st.plotly_chart(fig_cat, use_container_width=True)

with summary_col2:
    segment_counts = filtered_df.groupby('segment').size().reset_index(name='count')
    fig_seg = create_pie_chart(segment_counts, 'count', 'segment', 'Segment Distribution', 
                               ['#7c3aed', '#f59e0b', '#06b6d4'])
    st.plotly_chart(fig_seg, use_container_width=True)

with summary_col3:
    region_counts = filtered_df.groupby('region').size().reset_index(name='count')
    fig_reg = create_pie_chart(region_counts, 'count', 'region', 'Region Distribution',
                               ['#dc2626', '#2563eb', '#16a34a', '#f59e0b'])
    st.plotly_chart(fig_reg, use_container_width=True)

with summary_col4:
    subcat_counts = filtered_df.groupby('sub_category').size().reset_index(name='count')
    subcat_counts = subcat_counts.sort_values('count', ascending=False).head(5)
    fig_subcat = create_bar_chart_horizontal(subcat_counts, 'count', 'sub_category', 'Top 5 Sub-Categories')
    st.plotly_chart(fig_subcat, use_container_width=True)

st.markdown("---")

# === TABS ===
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Overview", "Sales Trend", "Regional Analysis", 
    "Product Analysis", "Customer Analysis", "Forecasting"
])

# Tab 1: Overview
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<p class="sub-header"><i class="fas fa-box"></i> Sales by Category</p>', unsafe_allow_html=True)
        category_sales = filtered_df.groupby('category')['sales'].sum().reset_index()
        fig_category = create_pie_chart_large(category_sales, 'sales', 'category', '')
        st.plotly_chart(fig_category, use_container_width=True)
    
    with col2:
        st.markdown('<p class="sub-header"><i class="fas fa-users"></i> Sales by Segment</p>', unsafe_allow_html=True)
        segment_sales = filtered_df.groupby('segment')['sales'].sum().reset_index()
        fig_segment = create_pie_chart_large(segment_sales, 'sales', 'segment', '', 
                                             ['#7c3aed', '#f59e0b', '#06b6d4'])
        st.plotly_chart(fig_segment, use_container_width=True)
    
    # Region Bar Chart
    st.markdown('<p class="sub-header"><i class="fas fa-globe-americas"></i> Sales by Region</p>', unsafe_allow_html=True)
    region_sales = filtered_df.groupby('region')['sales'].sum().reset_index().sort_values('sales', ascending=True)
    fig_region = create_bar_chart_horizontal(region_sales, 'sales', 'region', '', height=320, show_text=True)
    st.plotly_chart(fig_region, use_container_width=True)

# Tab 2: Sales Trend
with tab2:
    st.markdown('<p class="sub-header"><i class="fas fa-chart-area"></i> Monthly Sales Trend</p>', unsafe_allow_html=True)
    
    monthly_sales = filtered_df.groupby(['order_year', 'order_month_num', 'order_month_name'])['sales'].sum().reset_index()
    monthly_sales['year_month'] = monthly_sales['order_year'].astype(str) + '-' + monthly_sales['order_month_num'].astype(str).str.zfill(2)
    monthly_sales = monthly_sales.sort_values('year_month')
    
    fig_trend = create_line_chart(monthly_sales, 'year_month', 'sales', '')
    st.plotly_chart(fig_trend, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<p class="sub-header"><i class="fas fa-calendar-alt"></i> Quarterly Sales</p>', unsafe_allow_html=True)
        quarterly_sales = filtered_df.groupby(['order_year', 'order_quarter'])['sales'].sum().reset_index()
        quarterly_sales['quarter_label'] = 'Q' + quarterly_sales['order_quarter'].astype(str)
        
        fig_quarterly = px.bar(
            quarterly_sales, x='quarter_label', y='sales', color='order_year',
            barmode='group', color_discrete_sequence=CHART_COLORS
        )
        fig_quarterly.update_layout(**CHART_LAYOUT, height=380, legend_title="Year")
        st.plotly_chart(fig_quarterly, use_container_width=True)
    
    with col2:
        st.markdown('<p class="sub-header"><i class="fas fa-chart-bar"></i> Yearly Sales</p>', unsafe_allow_html=True)
        yearly_sales = filtered_df.groupby('order_year')['sales'].sum().reset_index()
        fig_yearly = create_bar_chart_vertical(yearly_sales, 'order_year', 'sales', '', height=380)
        st.plotly_chart(fig_yearly, use_container_width=True)
    
    # Day of Week
    st.markdown('<p class="sub-header"><i class="fas fa-calendar-week"></i> Sales by Day of Week</p>', unsafe_allow_html=True)
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_sales = filtered_df.groupby('order_day_of_week')['sales'].sum().reset_index()
    day_sales['order_day_of_week'] = pd.Categorical(day_sales['order_day_of_week'], categories=day_order, ordered=True)
    day_sales = day_sales.sort_values('order_day_of_week')
    
    fig_day = create_bar_chart_vertical(day_sales, 'order_day_of_week', 'sales', '', height=350)
    st.plotly_chart(fig_day, use_container_width=True)

# Tab 3: Regional Analysis
with tab3:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<p class="sub-header"><i class="fas fa-building"></i> Top 15 States by Sales</p>', unsafe_allow_html=True)
        state_sales = filtered_df.groupby('state')['sales'].sum().reset_index()
        state_sales = state_sales.sort_values('sales', ascending=False).head(15)
        fig_states = create_bar_chart_horizontal(state_sales, 'sales', 'state', '', height=520, show_text=True)
        st.plotly_chart(fig_states, use_container_width=True)
    
    with col2:
        st.markdown('<p class="sub-header"><i class="fas fa-info-circle"></i> Region Summary</p>', unsafe_allow_html=True)
        region_summary = filtered_df.groupby('region').agg({
            'sales': 'sum',
            'order_id': 'nunique',
            'sk_customer': 'nunique'
        }).reset_index()
        region_summary.columns = ['Region', 'Total Sales', 'Orders', 'Customers']
        region_summary = region_summary.sort_values('Total Sales', ascending=False)
        
        for _, row in region_summary.iterrows():
            st.markdown(f'''
            <div class="region-card">
                <h4>{row['Region']}</h4>
                <p><i class="fas fa-dollar-sign"></i> ${row['Total Sales']:,.2f}</p>
                <p><i class="fas fa-shopping-cart"></i> {row['Orders']:,} orders</p>
                <p><i class="fas fa-user"></i> {row['Customers']:,} customers</p>
            </div>
            ''', unsafe_allow_html=True)
    
    # Top Cities
    st.markdown('<p class="sub-header"><i class="fas fa-city"></i> Top 10 Cities by Sales</p>', unsafe_allow_html=True)
    city_sales = filtered_df.groupby(['city', 'state'])['sales'].sum().reset_index()
    city_sales['city_state'] = city_sales['city'] + ', ' + city_sales['state']
    city_sales = city_sales.sort_values('sales', ascending=False).head(10)
    
    fig_cities = create_bar_chart_horizontal(city_sales, 'sales', 'city_state', '', height=400, show_text=True)
    st.plotly_chart(fig_cities, use_container_width=True)

# Tab 4: Product Analysis
with tab4:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<p class="sub-header"><i class="fas fa-tags"></i> Top 10 Sub-Categories</p>', unsafe_allow_html=True)
        subcat_sales = filtered_df.groupby('sub_category')['sales'].sum().reset_index()
        subcat_sales = subcat_sales.sort_values('sales', ascending=False).head(10)
        fig_subcat = create_bar_chart_horizontal(subcat_sales, 'sales', 'sub_category', '', height=400, show_text=True)
        st.plotly_chart(fig_subcat, use_container_width=True)
    
    with col2:
        st.markdown('<p class="sub-header"><i class="fas fa-sitemap"></i> Category Breakdown</p>', unsafe_allow_html=True)
        category_subcat = filtered_df.groupby(['category', 'sub_category'])['sales'].sum().reset_index()
        
        fig_sunburst = px.sunburst(
            category_subcat, path=['category', 'sub_category'],
            values='sales', color='sales', color_continuous_scale='Blues'
        )
        fig_sunburst.update_layout(
            paper_bgcolor='#ffffff', height=420,
            margin=dict(t=20, b=20, l=20, r=20),
            coloraxis_showscale=False
        )
        fig_sunburst.update_traces(textfont=dict(color='#ffffff', size=10))
        st.plotly_chart(fig_sunburst, use_container_width=True)
    
    # Top Products Table
    st.markdown('<p class="sub-header"><i class="fas fa-trophy"></i> Top 20 Products</p>', unsafe_allow_html=True)
    top_products = filtered_df.groupby(['product_name', 'category', 'sub_category'])['sales'].sum().reset_index()
    top_products = top_products.sort_values('sales', ascending=False).head(20)
    top_products['sales'] = top_products['sales'].apply(lambda x: f"${x:,.2f}")
    top_products.columns = ['Product Name', 'Category', 'Sub-Category', 'Total Sales']
    st.dataframe(top_products, use_container_width=True, hide_index=True)

# Tab 5: Customer Analysis
with tab5:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<p class="sub-header"><i class="fas fa-medal"></i> Top 10 Customers</p>', unsafe_allow_html=True)
        top_customers = filtered_df.groupby(['customer_name', 'segment'])['sales'].sum().reset_index()
        top_customers = top_customers.sort_values('sales', ascending=False).head(10)
        
        fig_customers = px.bar(
            top_customers, x='sales', y='customer_name', orientation='h',
            color='segment', color_discrete_sequence=CHART_COLORS,
            text=top_customers['sales'].apply(lambda x: f'${x:,.0f}')
        )
        fig_customers.update_layout(**CHART_LAYOUT, height=420, legend_title="Segment")
        fig_customers.update_yaxes(categoryorder='total ascending')
        fig_customers.update_traces(textposition='inside', textfont=dict(color='white', size=8))
        st.plotly_chart(fig_customers, use_container_width=True)
    
    with col2:
        st.markdown('<p class="sub-header"><i class="fas fa-user-friends"></i> Segment Distribution</p>', unsafe_allow_html=True)
        segment_dist = filtered_df.groupby('segment').agg({
            'sk_customer': 'nunique',
            'order_id': 'nunique'
        }).reset_index()
        segment_dist.columns = ['Segment', 'Customers', 'Orders']
        
        fig_seg_dist = px.bar(
            segment_dist, x='Segment', y=['Customers', 'Orders'],
            barmode='group', color_discrete_sequence=['#1e3a5f', '#3b82f6']
        )
        fig_seg_dist.update_layout(**CHART_LAYOUT, height=420, legend_title="Metric")
        st.plotly_chart(fig_seg_dist, use_container_width=True)
    
    # Segment Analysis Table
    st.markdown('<p class="sub-header"><i class="fas fa-chart-pie"></i> Segment Performance</p>', unsafe_allow_html=True)
    segment_analysis = filtered_df.groupby('segment').agg({
        'sales': ['sum', 'mean', 'count'],
        'sk_customer': 'nunique',
        'order_id': 'nunique'
    }).round(2)
    segment_analysis.columns = ['Total Sales', 'Avg Sale', 'Transactions', 'Customers', 'Orders']
    segment_analysis['Sales per Customer'] = (segment_analysis['Total Sales'] / segment_analysis['Customers']).round(2)
    segment_analysis = segment_analysis.reset_index()
    segment_analysis['Total Sales'] = segment_analysis['Total Sales'].apply(lambda x: f"${x:,.2f}")
    segment_analysis['Avg Sale'] = segment_analysis['Avg Sale'].apply(lambda x: f"${x:,.2f}")
    segment_analysis['Sales per Customer'] = segment_analysis['Sales per Customer'].apply(lambda x: f"${x:,.2f}")
    st.dataframe(segment_analysis, use_container_width=True, hide_index=True)

# Tab 6: Forecasting
with tab6:
    st.markdown('''
    <div style="background: linear-gradient(135deg, #dbeafe 0%, #eff6ff 100%); padding: 20px; border-radius: 14px; margin-bottom: 20px; border-left: 4px solid #3b82f6;">
        <p style="color: #1e3a5f; margin: 0; font-weight: 600;"><i class="fas fa-info-circle" style="color: #3b82f6;"></i> Method: Linear Regression</p>
        <p style="color: #4a6fa5; margin: 5px 0 0 0; font-size: 0.9rem;">Forecast based on historical monthly sales trends.</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Prepare forecast data
    monthly_forecast = filtered_df.groupby(['order_year', 'order_month_num'])['sales'].sum().reset_index()
    monthly_forecast['period'] = monthly_forecast['order_year'].astype(str) + '-' + monthly_forecast['order_month_num'].astype(str).str.zfill(2)
    monthly_forecast = monthly_forecast.sort_values('period').reset_index(drop=True)
    monthly_forecast['period_num'] = range(1, len(monthly_forecast) + 1)
    
    if len(monthly_forecast) >= 3:
        X = monthly_forecast[['period_num']].values
        y = monthly_forecast['sales'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        historical_pred = model.predict(X)
        future_periods = np.array([[i] for i in range(len(X) + 1, len(X) + 7)])
        future_pred = model.predict(future_periods)
        
        # Future labels
        last_year = monthly_forecast['order_year'].iloc[-1]
        last_month = monthly_forecast['order_month_num'].iloc[-1]
        future_labels = []
        for i in range(1, 7):
            next_month = last_month + i
            next_year = last_year
            while next_month > 12:
                next_month -= 12
                next_year += 1
            future_labels.append(f"{next_year}-{str(next_month).zfill(2)}")
        
        # Create forecast chart
        fig_forecast = go.Figure()
        
        fig_forecast.add_trace(go.Scatter(
            x=monthly_forecast['period'], y=monthly_forecast['sales'],
            mode='lines+markers', name='Actual Sales',
            line=dict(color='#3b82f6', width=3),
            marker=dict(size=8, color='#1e3a5f')
        ))
        
        fig_forecast.add_trace(go.Scatter(
            x=monthly_forecast['period'], y=historical_pred,
            mode='lines', name='Trend Line',
            line=dict(color='#94a3b8', width=2, dash='dash')
        ))
        
        fig_forecast.add_trace(go.Scatter(
            x=[monthly_forecast['period'].iloc[-1]] + future_labels,
            y=[historical_pred[-1]] + list(future_pred),
            mode='lines+markers', name='Forecast',
            line=dict(color='#10b981', width=3, dash='dot'),
            marker=dict(size=10, color='#10b981', symbol='diamond')
        ))
        
        fig_forecast.update_layout(
            title='Sales Forecast - Next 6 Months',
            **CHART_LAYOUT, height=500, hovermode='x unified',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5)
        )
        
        st.plotly_chart(fig_forecast, use_container_width=True)
        
        # Metrics
        st.markdown('<p class="sub-header"><i class="fas fa-chart-pie"></i> Forecast Summary</p>', unsafe_allow_html=True)
        fc1, fc2, fc3, fc4 = st.columns(4)
        
        with fc1:
            st.metric("Avg Forecast", f"${np.mean(future_pred):,.0f}", "per month")
        with fc2:
            st.metric("Total Projected", f"${np.sum(future_pred):,.0f}", "next 6 months")
        with fc3:
            growth = ((future_pred[-1] - y[-1]) / y[-1]) * 100 if y[-1] != 0 else 0
            st.metric("Projected Growth", f"{growth:+.1f}%", "vs last period")
        with fc4:
            st.metric("Model Accuracy (R²)", f"{model.score(X, y):.2%}", "confidence")
        
        # Forecast table
        forecast_table = pd.DataFrame({
            'Period': future_labels,
            'Predicted Sales': [f"${x:,.2f}" for x in future_pred]
        })
        st.dataframe(forecast_table, use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ Insufficient data for forecasting. Need at least 3 periods.")

# === EXPORT SECTION ===
st.markdown("---")
st.markdown(f'''
<p class="section-header">
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="#3b82f6" style="vertical-align: middle; margin-right: 8px;">
        <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
    </svg>
    Export Data
</p>
''', unsafe_allow_html=True)

export_col1, export_col2, export_col3 = st.columns(3)

with export_col1:
    summary_stats = filtered_df.describe(include='all').reset_index().rename(columns={'index': 'metric'})
    category_summary = filtered_df.groupby('category').agg(
        sales_sum=('sales', 'sum'),
        sales_avg=('sales', 'mean'),
        transactions=('sales', 'count'),
        customers=('sk_customer', 'nunique')
    ).reset_index()
    category_summary = category_summary.rename(columns={
        'category': 'Category',
        'sales_sum': 'Total Sales',
        'sales_avg': 'Avg Sale',
        'transactions': 'Transactions',
        'customers': 'Customers'
    })

    xlsx_bytes = dataframes_to_xlsx_bytes({
        'Filtered Data': filtered_df,
        'Summary Stats': summary_stats,
        'Category Summary': category_summary,
    })

    st.download_button(
        label="📥 Download Report (Excel)",
        data=xlsx_bytes,
        file_name="sales_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

with export_col2:
    summary_data = filtered_df.describe().to_csv().encode('utf-8')
    st.download_button(
        label="📊 Download Summary Statistics",
        data=summary_data,
        file_name="sales_summary_stats.csv",
        mime="text/csv",
        use_container_width=True
    )

with export_col3:
    cat_summary = filtered_df.groupby('category').agg({
        'sales': ['sum', 'mean', 'count'],
        'sk_customer': 'nunique'
    }).round(2)
    cat_summary.columns = ['Total Sales', 'Avg Sale', 'Transactions', 'Customers']
    cat_data = cat_summary.to_csv().encode('utf-8')
    st.download_button(
        label="📁 Download Category Summary",
        data=cat_data,
        file_name="category_summary.csv",
        mime="text/csv",
        use_container_width=True
    )

# === FOOTER ===
st.markdown("---")
st.markdown(f'''
<div class="footer" style="background: linear-gradient(135deg, #1e3a5f 0%, #2c5282 100%); padding: 30px; border-radius: 16px; text-align: center;">
    <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-bottom: 15px;">
        <div style="background: rgba(255,255,255,0.1); padding: 10px 20px; border-radius: 30px;">
            <span style="color: #93c5fd;"><i class="fas fa-database"></i></span>
            <span style="color: white; font-weight: 600;"> {len(df):,} Records</span>
        </div>
        <div style="background: rgba(255,255,255,0.1); padding: 10px 20px; border-radius: 30px;">
            <span style="color: #93c5fd;"><i class="fas fa-calendar"></i></span>
            <span style="color: white; font-weight: 600;"> 2015-2018</span>
        </div>
        <div style="background: rgba(255,255,255,0.1); padding: 10px 20px; border-radius: 30px;">
            <span style="color: #93c5fd;"><i class="fas fa-code"></i></span>
            <span style="color: white; font-weight: 600;"> Streamlit + Plotly</span>
        </div>
    </div>
    <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem; margin: 0;">
        Sales Analytics Dashboard | Business Intelligence Project
    </p>
    <p style="color: rgba(255,255,255,0.5); font-size: 0.75rem; margin-top: 10px;">
        Built with ❤️ for UAS Business Intelligence
    </p>
</div>
''', unsafe_allow_html=True)
