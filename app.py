import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Konfigurasi halaman
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load Font Awesome CDN dan Custom CSS
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" integrity="sha512-DTOQO9RWCH3ppGqcWaEA1BIZOC6xxalwEsw9c2QQeAIftl+Vegovlnee1c9QX4TctnWMn13TZye+giMm8e2LwA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.11.2/font/bootstrap-icons.min.css" integrity="sha512-D3/Ob7k6hPVcsMzQuGdMc5eE0fLU1TqQUz7pBIyFjuEHpzN9CSWi8X75k9pEvHD2LOWg3eWFVfhgeQQ+PKyv0A==" crossorigin="anonymous" referrerpolicy="no-referrer" />
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
    /* === GLOBAL STYLES === */
    * {
        font-family: 'Poppins', sans-serif !important;
    }
    
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .stApp {
        background: linear-gradient(160deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* === METRIC CARDS === */
    [data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: #e2e8f0 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.85rem !important;
        color: #4ade80 !important;
        font-weight: 500;
    }
    
    /* Metric container background */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 20px 25px;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
        border-color: rgba(102, 126, 234, 0.5);
    }
    
    /* === SIDEBAR STYLING === */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%) !important;
        border-right: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: transparent !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #e2e8f0 !important;
        font-weight: 500;
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label {
        color: #c7d2fe !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
        color: #c7d2fe !important;
    }
    
    /* Sidebar multiselect styling */
    [data-testid="stSidebar"] .stMultiSelect > div > div {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(102, 126, 234, 0.4) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
    }
    
    [data-testid="stSidebar"] .stMultiSelect span[data-baseweb="tag"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 500;
    }
    
    /* Sidebar selectbox */
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(102, 126, 234, 0.4) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
    }
    
    /* === HEADER STYLING === */
    .dashboard-header {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%);
        backdrop-filter: blur(20px);
        padding: 35px 45px;
        border-radius: 24px;
        margin-bottom: 35px;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .dashboard-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        pointer-events: none;
    }
    
    .dashboard-header h1 {
        color: #ffffff !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        margin: 0 !important;
        display: flex;
        align-items: center;
        gap: 18px;
        text-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    
    .dashboard-header p {
        color: rgba(255,255,255,0.95) !important;
        font-size: 1.15rem !important;
        margin: 12px 0 0 0 !important;
        font-weight: 400;
    }
    
    .dashboard-header i {
        font-size: 2.5rem;
        filter: drop-shadow(0 4px 10px rgba(0,0,0,0.3));
    }
    
    /* === SECTION HEADERS === */
    .section-header {
        color: #e2e8f0 !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        margin: 30px 0 25px 0 !important;
        padding-bottom: 15px;
        border-bottom: 2px solid rgba(102, 126, 234, 0.5);
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .section-header i {
        color: #a78bfa;
        font-size: 1.4rem;
    }
    
    /* === SUB HEADERS === */
    .sub-header {
        color: #c7d2fe !important;
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        margin: 25px 0 18px 0 !important;
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 18px;
        background: rgba(102, 126, 234, 0.15);
        border-radius: 14px;
        border-left: 4px solid #667eea;
    }
    
    .sub-header i {
        color: #a78bfa;
        font-size: 1.1rem;
    }
    
    /* === REGION CARDS === */
    .region-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        padding: 22px;
        border-radius: 16px;
        margin-bottom: 15px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .region-card:hover {
        transform: translateX(8px);
        border-color: rgba(102, 126, 234, 0.6);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.3);
    }
    
    .region-card h4 {
        color: #ffffff !important;
        margin: 0 0 15px 0 !important;
        font-weight: 700 !important;
        font-size: 1.1rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .region-card h4::before {
        content: '';
        width: 8px;
        height: 8px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 50%;
    }
    
    .region-card p {
        color: #cbd5e1 !important;
        margin: 8px 0 !important;
        font-size: 0.95rem !important;
        display: flex;
        align-items: center;
        gap: 10px;
        font-weight: 400;
    }
    
    .region-card i {
        color: #a78bfa;
        width: 20px;
        font-size: 0.9rem;
    }
    
    /* === DIVIDER STYLING === */
    hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.5), transparent) !important;
        margin: 40px 0 !important;
    }
    
    /* === TAB STYLING === */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        padding: 12px;
        border-radius: 18px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 14px 28px;
        border: 1px solid transparent;
        color: #a5b4fc !important;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(102, 126, 234, 0.2);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
        border-color: transparent;
    }
    
    /* Tab panel background */
    .stTabs [data-baseweb="tab-panel"] {
        background: transparent;
        padding-top: 25px;
    }
    
    /* === SIDEBAR COMPONENTS === */
    .sidebar-header {
        color: #ffffff !important;
        font-size: 1.4rem !important;
        font-weight: 700 !important;
        margin-bottom: 25px !important;
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 18px;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.3) 0%, rgba(118, 75, 162, 0.3) 100%);
        border-radius: 16px;
        border: 1px solid rgba(102, 126, 234, 0.4);
    }
    
    .sidebar-header i {
        color: #a78bfa;
        font-size: 1.3rem;
    }
    
    .filter-label {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 18px 0 10px 0 !important;
        font-size: 0.95rem;
        padding-left: 5px;
    }
    
    .filter-label i {
        color: #a78bfa;
        font-size: 1rem;
    }
    
    /* === FOOTER STYLING === */
    .footer {
        text-align: center;
        color: #cbd5e1;
        padding: 30px;
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        margin-top: 40px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .footer p {
        color: #cbd5e1 !important;
        margin: 8px 0;
    }
    
    .footer i {
        color: #a78bfa;
        margin-right: 10px;
    }
    
    /* === DATAFRAME STYLING === */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    [data-testid="stDataFrame"] > div {
        background: transparent !important;
    }
    
    /* === PLOTLY CHART CONTAINERS === */
    .js-plotly-plot {
        border-radius: 16px;
        overflow: hidden;
    }
    
    /* === EXPANDER STYLING === */
    .streamlit-expanderHeader {
        background: rgba(102, 126, 234, 0.15) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
        font-weight: 600 !important;
    }
    
    /* === COLUMNS GAP === */
    [data-testid="column"] {
        padding: 8px;
    }
    
    /* === SCROLLBAR STYLING === */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2, #667eea);
    }
    
    /* === ANIMATION KEYFRAMES === */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .dashboard-header, .region-card, [data-testid="stMetric"] {
        animation: fadeInUp 0.5s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# Fungsi untuk memuat data
@st.cache_data
def load_data():
    """Memuat dan menggabungkan semua data CSV"""
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Load dimension tables
    dim_customer = pd.read_csv(os.path.join(base_path, 'dim_customer.csv'))
    dim_date = pd.read_csv(os.path.join(base_path, 'dim_date.csv'))
    dim_product = pd.read_csv(os.path.join(base_path, 'dim_product.csv'))
    dim_region = pd.read_csv(os.path.join(base_path, 'dim_region.csv'))
    fact_sales = pd.read_csv(os.path.join(base_path, 'fact_sales.csv'))
    
    # Merge fact table with dimensions
    df = fact_sales.merge(dim_customer, on='sk_customer', how='left')
    df = df.merge(dim_product, on='sk_product', how='left')
    df = df.merge(dim_region, on='sk_region', how='left')
    
    # Merge with date dimension for order date
    dim_date_order = dim_date.copy()
    dim_date_order = dim_date_order.rename(columns={
        'date': 'order_date',
        'year': 'order_year',
        'month_num': 'order_month_num',
        'month_name': 'order_month_name',
        'quarter': 'order_quarter',
        'day_of_week': 'order_day_of_week'
    })
    df = df.merge(dim_date_order, left_on='sk_order_date', right_on='sk_date', how='left')
    
    # Convert order_date to datetime
    df['order_date'] = pd.to_datetime(df['order_date'])
    
    return df, dim_customer, dim_product, dim_region, dim_date

# Load data
df, dim_customer, dim_product, dim_region, dim_date = load_data()

# Header
st.markdown("""
<div class="dashboard-header">
    <h1><i class="fas fa-chart-line"></i> Sales Analytics Dashboard</h1>
    <p>Business Intelligence Dashboard untuk Analisis Penjualan</p>
</div>
""", unsafe_allow_html=True)

# Sidebar untuk filter
st.sidebar.markdown('<div class="sidebar-header"><i class="fas fa-filter"></i> Filter Data</div>', unsafe_allow_html=True)

# Filter tahun
st.sidebar.markdown('<p class="filter-label"><i class="fas fa-calendar"></i> Pilih Tahun</p>', unsafe_allow_html=True)
years = sorted(df['order_year'].dropna().unique())
selected_years = st.sidebar.multiselect(
    "Tahun",
    options=years,
    default=years,
    label_visibility="collapsed"
)

# Filter region
st.sidebar.markdown('<p class="filter-label"><i class="fas fa-globe"></i> Pilih Region</p>', unsafe_allow_html=True)
regions = sorted(df['region'].dropna().unique())
selected_regions = st.sidebar.multiselect(
    "Region",
    options=regions,
    default=regions,
    label_visibility="collapsed"
)

# Filter segment
st.sidebar.markdown('<p class="filter-label"><i class="fas fa-users"></i> Pilih Segment</p>', unsafe_allow_html=True)
segments = sorted(df['segment'].dropna().unique())
selected_segments = st.sidebar.multiselect(
    "Segment",
    options=segments,
    default=segments,
    label_visibility="collapsed"
)

# Filter category
st.sidebar.markdown('<p class="filter-label"><i class="fas fa-boxes"></i> Pilih Category</p>', unsafe_allow_html=True)
categories = sorted(df['category'].dropna().unique())
selected_categories = st.sidebar.multiselect(
    "Category",
    options=categories,
    default=categories,
    label_visibility="collapsed"
)

# Apply filters
filtered_df = df[
    (df['order_year'].isin(selected_years)) &
    (df['region'].isin(selected_regions)) &
    (df['segment'].isin(selected_segments)) &
    (df['category'].isin(selected_categories))
]

# KPI Metrics Row
st.markdown('<p class="section-header"><i class="fas fa-tachometer-alt"></i> Key Performance Indicators</p>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_sales = filtered_df['sales'].sum()
    st.metric(
        label="Total Sales",
        value=f"${total_sales:,.2f}",
        delta=f"{len(filtered_df):,} transaksi"
    )

with col2:
    avg_order = filtered_df['sales'].mean()
    st.metric(
        label="Rata-rata Order",
        value=f"${avg_order:,.2f}",
        delta="per transaksi"
    )

with col3:
    total_customers = filtered_df['sk_customer'].nunique()
    st.metric(
        label="Total Customers",
        value=f"{total_customers:,}",
        delta="unique customers"
    )

with col4:
    total_products = filtered_df['sk_product'].nunique()
    st.metric(
        label="Total Products",
        value=f"{total_products:,}",
        delta="unique products"
    )

with col5:
    total_orders = filtered_df['order_id'].nunique()
    st.metric(
        label="Total Orders",
        value=f"{total_orders:,}",
        delta="unique orders"
    )

st.markdown("---")

# Tabs untuk berbagai visualisasi
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview", 
    "Sales Trend", 
    "Regional Analysis", 
    "Product Analysis",
    "Customer Analysis"
])

# Warna untuk chart (Blue theme)
blue_colors = ['#1e40af', '#2563eb', '#3b82f6', '#60a5fa', '#93c5fd', '#bfdbfe']
blue_scale = [[0, '#bfdbfe'], [0.5, '#3b82f6'], [1, '#1e40af']]

# Tab 1: Overview
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        # Sales by Category
        st.markdown('<p class="sub-header"><i class="fas fa-box"></i> Sales by Category</p>', unsafe_allow_html=True)
        category_sales = filtered_df.groupby('category')['sales'].sum().reset_index()
        fig_category = px.pie(
            category_sales, 
            values='sales', 
            names='category',
            color_discrete_sequence=blue_colors,
            hole=0.4
        )
        fig_category.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#1e293b'),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
        )
        st.plotly_chart(fig_category, use_container_width=True)
    
    with col2:
        # Sales by Segment
        st.markdown('<p class="sub-header"><i class="fas fa-users"></i> Sales by Segment</p>', unsafe_allow_html=True)
        segment_sales = filtered_df.groupby('segment')['sales'].sum().reset_index()
        fig_segment = px.pie(
            segment_sales, 
            values='sales', 
            names='segment',
            color_discrete_sequence=['#0ea5e9', '#38bdf8', '#7dd3fc'],
            hole=0.4
        )
        fig_segment.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#1e293b'),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
        )
        st.plotly_chart(fig_segment, use_container_width=True)
    
    # Sales by Region Bar Chart
    st.markdown('<p class="sub-header"><i class="fas fa-globe-americas"></i> Sales by Region</p>', unsafe_allow_html=True)
    region_sales = filtered_df.groupby('region')['sales'].sum().reset_index().sort_values('sales', ascending=True)
    fig_region = px.bar(
        region_sales,
        x='sales',
        y='region',
        orientation='h',
        color='sales',
        color_continuous_scale='Blues'
    )
    fig_region.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#1e293b'),
        xaxis=dict(gridcolor='rgba(30, 64, 175, 0.1)'),
        yaxis=dict(gridcolor='rgba(30, 64, 175, 0.1)'),
        showlegend=False,
        coloraxis_showscale=False,
        height=300
    )
    st.plotly_chart(fig_region, use_container_width=True)

# Tab 2: Sales Trend
with tab2:
    # Monthly Sales Trend
    st.markdown('<p class="sub-header"><i class="fas fa-chart-area"></i> Monthly Sales Trend</p>', unsafe_allow_html=True)
    
    monthly_sales = filtered_df.groupby(['order_year', 'order_month_num', 'order_month_name'])['sales'].sum().reset_index()
    monthly_sales['year_month'] = monthly_sales['order_year'].astype(str) + '-' + monthly_sales['order_month_num'].astype(str).str.zfill(2)
    monthly_sales = monthly_sales.sort_values('year_month')
    
    fig_trend = px.line(
        monthly_sales,
        x='year_month',
        y='sales',
        markers=True,
        color_discrete_sequence=['#1e40af']
    )
    fig_trend.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#1e293b'),
        xaxis=dict(gridcolor='rgba(30, 64, 175, 0.1)', title='Bulan'),
        yaxis=dict(gridcolor='rgba(30, 64, 175, 0.1)', title='Total Sales'),
        height=400
    )
    fig_trend.update_traces(line=dict(width=3), marker=dict(size=8))
    st.plotly_chart(fig_trend, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Quarterly Sales
        st.markdown('<p class="sub-header"><i class="fas fa-calendar-alt"></i> Quarterly Sales Comparison</p>', unsafe_allow_html=True)
        quarterly_sales = filtered_df.groupby(['order_year', 'order_quarter'])['sales'].sum().reset_index()
        quarterly_sales['quarter_label'] = 'Q' + quarterly_sales['order_quarter'].astype(str)
        
        fig_quarterly = px.bar(
            quarterly_sales,
            x='quarter_label',
            y='sales',
            color='order_year',
            barmode='group',
            color_discrete_sequence=blue_colors
        )
        fig_quarterly.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#1e293b'),
            xaxis=dict(gridcolor='rgba(30, 64, 175, 0.1)', title='Quarter'),
            yaxis=dict(gridcolor='rgba(30, 64, 175, 0.1)', title='Total Sales'),
            legend_title="Tahun"
        )
        st.plotly_chart(fig_quarterly, use_container_width=True)
    
    with col2:
        # Yearly Sales
        st.markdown('<p class="sub-header"><i class="fas fa-chart-bar"></i> Yearly Sales Growth</p>', unsafe_allow_html=True)
        yearly_sales = filtered_df.groupby('order_year')['sales'].sum().reset_index()
        
        fig_yearly = px.bar(
            yearly_sales,
            x='order_year',
            y='sales',
            color='sales',
            color_continuous_scale='Blues',
            text='sales'
        )
        fig_yearly.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#1e293b'),
            xaxis=dict(gridcolor='rgba(30, 64, 175, 0.1)', title='Tahun'),
            yaxis=dict(gridcolor='rgba(30, 64, 175, 0.1)', title='Total Sales'),
            showlegend=False,
            coloraxis_showscale=False
        )
        fig_yearly.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
        st.plotly_chart(fig_yearly, use_container_width=True)
    
    # Day of Week Analysis
    st.markdown('<p class="sub-header"><i class="fas fa-calendar-week"></i> Sales by Day of Week</p>', unsafe_allow_html=True)
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_sales = filtered_df.groupby('order_day_of_week')['sales'].sum().reset_index()
    day_sales['order_day_of_week'] = pd.Categorical(day_sales['order_day_of_week'], categories=day_order, ordered=True)
    day_sales = day_sales.sort_values('order_day_of_week')
    
    fig_day = px.bar(
        day_sales,
        x='order_day_of_week',
        y='sales',
        color='sales',
        color_continuous_scale='Blues'
    )
    fig_day.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#1e293b'),
        xaxis=dict(gridcolor='rgba(30, 64, 175, 0.1)', title='Hari'),
        yaxis=dict(gridcolor='rgba(30, 64, 175, 0.1)', title='Total Sales'),
        coloraxis_showscale=False,
        height=350
    )
    st.plotly_chart(fig_day, use_container_width=True)

# Tab 3: Regional Analysis
with tab3:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Top 15 States by Sales
        st.markdown('<p class="sub-header"><i class="fas fa-building"></i> Top 15 States by Sales</p>', unsafe_allow_html=True)
        state_sales = filtered_df.groupby('state')['sales'].sum().reset_index().sort_values('sales', ascending=False).head(15)
        
        fig_states = px.bar(
            state_sales,
            x='sales',
            y='state',
            orientation='h',
            color='sales',
            color_continuous_scale='Blues'
        )
        fig_states.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#1e293b'),
            xaxis=dict(gridcolor='rgba(30, 64, 175, 0.1)', title='Total Sales'),
            yaxis=dict(gridcolor='rgba(30, 64, 175, 0.1)', title='State', categoryorder='total ascending'),
            coloraxis_showscale=False,
            height=500
        )
        st.plotly_chart(fig_states, use_container_width=True)
    
    with col2:
        # Region Summary
        st.markdown('<p class="sub-header"><i class="fas fa-info-circle"></i> Region Summary</p>', unsafe_allow_html=True)
        region_summary = filtered_df.groupby('region').agg({
            'sales': 'sum',
            'order_id': 'nunique',
            'sk_customer': 'nunique'
        }).reset_index()
        region_summary.columns = ['Region', 'Total Sales', 'Orders', 'Customers']
        region_summary['Avg per Order'] = region_summary['Total Sales'] / region_summary['Orders']
        region_summary = region_summary.sort_values('Total Sales', ascending=False)
        
        for _, row in region_summary.iterrows():
            st.markdown(f"""
            <div class="region-card">
                <h4>{row['Region']}</h4>
                <p><i class="fas fa-dollar-sign"></i> ${row['Total Sales']:,.2f}</p>
                <p><i class="fas fa-shopping-cart"></i> {row['Orders']:,} orders</p>
                <p><i class="fas fa-user"></i> {row['Customers']:,} customers</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Top 10 Cities
    st.markdown('<p class="sub-header"><i class="fas fa-city"></i> Top 10 Cities by Sales</p>', unsafe_allow_html=True)
    city_sales = filtered_df.groupby(['city', 'state'])['sales'].sum().reset_index()
    city_sales['city_state'] = city_sales['city'] + ', ' + city_sales['state']
    city_sales = city_sales.sort_values('sales', ascending=False).head(10)
    
    fig_cities = px.treemap(
        city_sales,
        path=['city_state'],
        values='sales',
        color='sales',
        color_continuous_scale='Blues'
    )
    fig_cities.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#1e293b'),
        height=400
    )
    st.plotly_chart(fig_cities, use_container_width=True)

# Tab 4: Product Analysis
with tab4:
    col1, col2 = st.columns(2)
    
    with col1:
        # Sales by Sub-Category
        st.markdown('<p class="sub-header"><i class="fas fa-tags"></i> Top 10 Sub-Categories</p>', unsafe_allow_html=True)
        subcat_sales = filtered_df.groupby('sub_category')['sales'].sum().reset_index()
        subcat_sales = subcat_sales.sort_values('sales', ascending=False).head(10)
        
        fig_subcat = px.bar(
            subcat_sales,
            x='sales',
            y='sub_category',
            orientation='h',
            color='sales',
            color_continuous_scale='Blues'
        )
        fig_subcat.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#1e293b'),
            xaxis=dict(gridcolor='rgba(30, 64, 175, 0.1)', title='Total Sales'),
            yaxis=dict(gridcolor='rgba(30, 64, 175, 0.1)', title='Sub-Category', categoryorder='total ascending'),
            coloraxis_showscale=False,
            height=400
        )
        st.plotly_chart(fig_subcat, use_container_width=True)
    
    with col2:
        # Category Sales Breakdown
        st.markdown('<p class="sub-header"><i class="fas fa-sitemap"></i> Category Sales Breakdown</p>', unsafe_allow_html=True)
        category_subcat = filtered_df.groupby(['category', 'sub_category'])['sales'].sum().reset_index()
        
        fig_sunburst = px.sunburst(
            category_subcat,
            path=['category', 'sub_category'],
            values='sales',
            color='sales',
            color_continuous_scale='Blues'
        )
        fig_sunburst.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#1e293b'),
            height=400
        )
        st.plotly_chart(fig_sunburst, use_container_width=True)
    
    # Top Products Table
    st.markdown('<p class="sub-header"><i class="fas fa-trophy"></i> Top 20 Products by Sales</p>', unsafe_allow_html=True)
    top_products = filtered_df.groupby(['product_name', 'category', 'sub_category'])['sales'].sum().reset_index()
    top_products = top_products.sort_values('sales', ascending=False).head(20)
    top_products['sales'] = top_products['sales'].apply(lambda x: f"${x:,.2f}")
    top_products.columns = ['Product Name', 'Category', 'Sub-Category', 'Total Sales']
    
    st.dataframe(
        top_products,
        use_container_width=True,
        hide_index=True,
        height=400
    )

# Tab 5: Customer Analysis
with tab5:
    col1, col2 = st.columns(2)
    
    with col1:
        # Top 10 Customers
        st.markdown('<p class="sub-header"><i class="fas fa-medal"></i> Top 10 Customers by Sales</p>', unsafe_allow_html=True)
        top_customers = filtered_df.groupby(['customer_name', 'segment'])['sales'].sum().reset_index()
        top_customers = top_customers.sort_values('sales', ascending=False).head(10)
        
        fig_customers = px.bar(
            top_customers,
            x='sales',
            y='customer_name',
            orientation='h',
            color='segment',
            color_discrete_sequence=blue_colors
        )
        fig_customers.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#1e293b'),
            xaxis=dict(gridcolor='rgba(30, 64, 175, 0.1)', title='Total Sales'),
            yaxis=dict(gridcolor='rgba(30, 64, 175, 0.1)', title='Customer', categoryorder='total ascending'),
            legend_title="Segment",
            height=400
        )
        st.plotly_chart(fig_customers, use_container_width=True)
    
    with col2:
        # Segment Distribution
        st.markdown('<p class="sub-header"><i class="fas fa-user-friends"></i> Customer Segment Distribution</p>', unsafe_allow_html=True)
        segment_dist = filtered_df.groupby('segment').agg({
            'sk_customer': 'nunique',
            'sales': 'sum',
            'order_id': 'nunique'
        }).reset_index()
        segment_dist.columns = ['Segment', 'Customers', 'Total Sales', 'Orders']
        
        fig_seg_dist = px.bar(
            segment_dist,
            x='Segment',
            y=['Customers', 'Orders'],
            barmode='group',
            color_discrete_sequence=['#1e40af', '#3b82f6']
        )
        fig_seg_dist.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#1e293b'),
            xaxis=dict(gridcolor='rgba(30, 64, 175, 0.1)'),
            yaxis=dict(gridcolor='rgba(30, 64, 175, 0.1)', title='Count'),
            legend_title="Metric",
            height=400
        )
        st.plotly_chart(fig_seg_dist, use_container_width=True)
    
    # Customer Segment Analysis
    st.markdown('<p class="sub-header"><i class="fas fa-chart-pie"></i> Segment Performance Analysis</p>', unsafe_allow_html=True)
    segment_analysis = filtered_df.groupby('segment').agg({
        'sales': ['sum', 'mean', 'count'],
        'sk_customer': 'nunique',
        'order_id': 'nunique'
    }).round(2)
    segment_analysis.columns = ['Total Sales', 'Avg Sale', 'Transactions', 'Unique Customers', 'Unique Orders']
    segment_analysis['Sales per Customer'] = (segment_analysis['Total Sales'] / segment_analysis['Unique Customers']).round(2)
    segment_analysis['Orders per Customer'] = (segment_analysis['Unique Orders'] / segment_analysis['Unique Customers']).round(2)
    
    # Reset index dan format
    segment_analysis = segment_analysis.reset_index()
    segment_analysis['Total Sales'] = segment_analysis['Total Sales'].apply(lambda x: f"${x:,.2f}")
    segment_analysis['Avg Sale'] = segment_analysis['Avg Sale'].apply(lambda x: f"${x:,.2f}")
    segment_analysis['Sales per Customer'] = segment_analysis['Sales per Customer'].apply(lambda x: f"${x:,.2f}")
    
    st.dataframe(
        segment_analysis,
        use_container_width=True,
        hide_index=True
    )

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <p><i class="fas fa-chart-line"></i> Sales Analytics Dashboard | Built with Streamlit & Plotly</p>
    <p><i class="fas fa-database"></i> Data: 2015-2018 Sales Data</p>
</div>
""", unsafe_allow_html=True)
