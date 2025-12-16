"""
Data loading and processing utilities
"""
import streamlit as st
import pandas as pd
import os


@st.cache_data
def load_data():
    """Load and merge all data from CSV files"""
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Load dimension tables
    dim_customer = pd.read_csv(os.path.join(base_path, 'dim_customer.csv'))
    dim_date = pd.read_csv(os.path.join(base_path, 'dim_date.csv'))
    dim_product = pd.read_csv(os.path.join(base_path, 'dim_product.csv'))
    dim_region = pd.read_csv(os.path.join(base_path, 'dim_region.csv'))
    fact_sales = pd.read_csv(os.path.join(base_path, 'fact_sales.csv'))
    
    # Rename dim_date columns for clarity
    dim_date = dim_date.rename(columns={
        'year': 'order_year',
        'month_num': 'order_month_num',
        'month_name': 'order_month_name',
        'quarter': 'order_quarter',
        'day_of_week': 'order_day_of_week'
    })
    
    # Merge data - fact_sales uses sk_order_date to join with dim_date.sk_date
    df = fact_sales.merge(dim_customer, on='sk_customer', how='left')
    df = df.merge(dim_date, left_on='sk_order_date', right_on='sk_date', how='left')
    df = df.merge(dim_product, on='sk_product', how='left')
    df = df.merge(dim_region, on='sk_region', how='left')
    
    return df


def filter_data(df, filters):
    """Apply filters to the dataframe
    
    Args:
        df: DataFrame to filter
        filters: Dictionary with filter values from sidebar
    """
    filtered_df = df.copy()
    
    if filters.get('years'):
        filtered_df = filtered_df[filtered_df['order_year'].isin(filters['years'])]
    if filters.get('regions'):
        filtered_df = filtered_df[filtered_df['region'].isin(filters['regions'])]
    if filters.get('states'):
        filtered_df = filtered_df[filtered_df['state'].isin(filters['states'])]
    if filters.get('segments'):
        filtered_df = filtered_df[filtered_df['segment'].isin(filters['segments'])]
    if filters.get('categories'):
        filtered_df = filtered_df[filtered_df['category'].isin(filters['categories'])]
    if filters.get('subcategories'):
        filtered_df = filtered_df[filtered_df['sub_category'].isin(filters['subcategories'])]
    if filters.get('product_search'):
        filtered_df = filtered_df[filtered_df['product_name'].str.contains(filters['product_search'], case=False, na=False)]
    
    return filtered_df


def calculate_kpis(filtered_df):
    """Calculate KPI values from filtered data"""
    return {
        'total_sales': filtered_df['sales'].sum(),
        'avg_order': filtered_df['sales'].mean() if len(filtered_df) > 0 else 0,
        'total_customers': filtered_df['sk_customer'].nunique(),
        'total_products': filtered_df['sk_product'].nunique(),
        'total_orders': filtered_df['order_id'].nunique(),
        'total_categories': filtered_df['category'].nunique(),
        'total_subcategories': filtered_df['sub_category'].nunique(),
        'total_states': filtered_df['state'].nunique(),
        'total_regions': filtered_df['region'].nunique(),
        'transaction_count': len(filtered_df),
    }


def get_top_insights(filtered_df):
    """Generate quick insights from filtered data"""
    insights = {}
    
    # Top category
    if not filtered_df.empty:
        top_cat = filtered_df.groupby('category')['sales'].sum().idxmax()
        top_cat_sales = filtered_df.groupby('category')['sales'].sum().max()
        insights['top_category'] = {'name': top_cat, 'sales': top_cat_sales}
        
        # Top region
        top_region = filtered_df.groupby('region')['sales'].sum().idxmax()
        top_region_sales = filtered_df.groupby('region')['sales'].sum().max()
        insights['top_region'] = {'name': top_region, 'sales': top_region_sales}
        
        # Top segment
        top_segment = filtered_df.groupby('segment')['sales'].sum().idxmax()
        top_segment_sales = filtered_df.groupby('segment')['sales'].sum().max()
        insights['top_segment'] = {'name': top_segment, 'sales': top_segment_sales}
        
        # Top state
        top_state = filtered_df.groupby('state')['sales'].sum().idxmax()
        top_state_sales = filtered_df.groupby('state')['sales'].sum().max()
        insights['top_state'] = {'name': top_state, 'sales': top_state_sales}
    
    return insights
