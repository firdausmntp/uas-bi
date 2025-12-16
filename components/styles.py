"""
CSS Styles untuk Dashboard Sales Super Store
"""

CSS_STYLES = '''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
    /* === GLOBAL STYLES === */
    html, body, .stApp {
        font-family: 'Poppins', sans-serif !important;
    }
    
    .stApp {
        background: linear-gradient(145deg, #f0f4f8 0%, #e8f0f8 100%);
    }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(145deg, #f0f4f8 0%, #e8f0f8 100%);
    }
    
    .main .block-container {
        padding: 1.5rem 2rem 2rem 2rem !important;
        max-width: 100% !important;
    }
    
    /* === KPI CARDS === */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 16px;
        margin-bottom: 20px;
    }
    
    .kpi-grid--4cols {
        grid-template-columns: repeat(4, 1fr);
    }
    
    .kpi-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8fbff 100%);
        border-radius: 16px;
        padding: 20px;
        display: flex;
        align-items: center;
        gap: 15px;
        box-shadow: 0 4px 15px rgba(30, 58, 95, 0.08);
        border: 1px solid #d0e3f7;
        transition: all 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(30, 58, 95, 0.15);
        border-color: #3b82f6;
    }
    
    .kpi-icon {
        width: 50px;
        height: 50px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    
    .kpi-card--sales .kpi-icon { background: linear-gradient(135deg, #10b981 0%, #34d399 100%); }
    .kpi-card--avg .kpi-icon { background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%); }
    .kpi-card--customers .kpi-icon { background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%); }
    .kpi-card--products .kpi-icon { background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%); }
    .kpi-card--orders .kpi-icon { background: linear-gradient(135deg, #ef4444 0%, #f87171 100%); }
    .kpi-card--categories .kpi-icon { background: linear-gradient(135deg, #06b6d4 0%, #22d3ee 100%); }
    .kpi-card--subcategories .kpi-icon { background: linear-gradient(135deg, #ec4899 0%, #f472b6 100%); }
    .kpi-card--states .kpi-icon { background: linear-gradient(135deg, #14b8a6 0%, #2dd4bf 100%); }
    .kpi-card--regions .kpi-icon { background: linear-gradient(135deg, #6366f1 0%, #818cf8 100%); }
    
    .kpi-icon svg {
        width: 24px;
        height: 24px;
    }
    
    .kpi-content {
        display: flex;
        flex-direction: column;
        min-width: 0;
    }
    
    .kpi-label {
        font-size: 0.75rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
    }
    
    .kpi-value {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1e3a5f;
        line-height: 1.2;
    }
    
    .kpi-delta {
        font-size: 0.75rem;
        color: #10b981;
        font-weight: 500;
    }
    
    /* Responsive KPI Grid */
    @media (max-width: 1400px) {
        .kpi-grid { grid-template-columns: repeat(3, 1fr); }
        .kpi-grid--4cols { grid-template-columns: repeat(2, 1fr); }
    }
    
    @media (max-width: 900px) {
        .kpi-grid { grid-template-columns: repeat(2, 1fr); }
        .kpi-grid--4cols { grid-template-columns: repeat(2, 1fr); }
    }
    
    @media (max-width: 600px) {
        .kpi-grid { grid-template-columns: 1fr; }
        .kpi-grid--4cols { grid-template-columns: 1fr; }
    }
    
    /* === LIVE STATS ROW === */
    .live-stats-row {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 20px;
        flex-wrap: wrap;
    }
    
    .live-pill {
        display: flex;
        align-items: center;
        gap: 8px;
        border-radius: 20px;
        padding: 8px 16px;
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid #e0e8f0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        color: #4a6fa5;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    .live-pill strong { color: #1e3a5f; }
    
    .live-pill--badge {
        background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
        border: none;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
        color: #ffffff;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .live-dot {
        width: 10px;
        height: 10px;
        background: #ffffff;
        border-radius: 50%;
        animation: pulse 1.5s infinite;
    }
    
    /* === METRIC CARDS === */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        color: #1e3a5f !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        color: #4a6fa5 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.75rem !important;
        color: #2e7d32 !important;
        font-weight: 500;
    }
    
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #ffffff 0%, #f8fbff 100%);
        border: 1px solid #d0e3f7;
        padding: 20px 25px;
        border-radius: 16px;
        box-shadow: 0 4px 15px rgba(30, 58, 95, 0.08);
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(30, 58, 95, 0.15);
        border-color: #3b82f6;
    }
    
    /* === SIDEBAR STYLING === */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e3a5f 40%, #2c5282 100%) !important;
        width: 320px !important;
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.15) !important;
    }
    
    section[data-testid="stSidebar"][aria-expanded="false"] {
        transform: translateX(-100%) !important;
        width: 0 !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }
    
    section[data-testid="stSidebar"] > div {
        background: transparent !important;
        padding: 1rem !important;
    }
    
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
        font-weight: 500;
    }

    /* === SIDEBAR COLLAPSE BUTTON (ALWAYS VISIBLE) === */
    section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button {
        opacity: 1 !important;
        background: rgba(255, 255, 255, 0.18) !important;
        border: 1px solid rgba(255, 255, 255, 0.55) !important;
        border-radius: 10px !important;
        width: 40px !important;
        height: 40px !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.25) !important;
    }

    section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button:hover {
        background: rgba(255, 255, 255, 0.28) !important;
        border-color: rgba(255, 255, 255, 0.80) !important;
        transform: translateY(-1px);
    }

    section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] span,
    section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] span[data-testid="stIconMaterial"] {
        color: #ffffff !important;
    }
    
    /* === HEADER STYLING === */
    header[data-testid="stHeader"] {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%) !important;
        backdrop-filter: blur(10px) !important;
        border-bottom: 1px solid rgba(59, 130, 246, 0.3) !important;
    }
    
    [data-testid="stToolbar"] button,
    header[data-testid="stHeader"] button {
        background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%) !important;
        border: 2px solid #60a5fa !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        padding: 8px 12px !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4) !important;
    }
    
    header[data-testid="stHeader"] svg { fill: #ffffff !important; }
    
    /* Sidebar Labels */
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMultiSelect label {
        color: #e0f0ff !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
    
    /* Sidebar multiselect */
    section[data-testid="stSidebar"] .stMultiSelect > div > div {
        background: #ffffff !important;
        border: 1px solid #d0e3f7 !important;
        border-radius: 10px !important;
        color: #1e3a5f !important;
    }
    
    section[data-testid="stSidebar"] .stMultiSelect span[data-baseweb="tag"] {
        background: #ffffff !important;
        color: #1e3a5f !important;
        border: 1px solid #3b82f6 !important;
        border-radius: 8px !important;
        font-weight: 600;
    }
    
    section[data-testid="stSidebar"] .stSelectbox > div > div {
        background: #ffffff !important;
        border: 1px solid #d0e3f7 !important;
        border-radius: 10px !important;
        color: #1e3a5f !important;
    }
    
    /* === DASHBOARD HEADER === */
    .dashboard-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #2c5282 50%, #3b82f6 100%);
        padding: 30px 40px;
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow: 0 10px 40px rgba(30, 58, 95, 0.25);
        position: relative;
        overflow: hidden;
    }
    
    .dashboard-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -30%;
        width: 80%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%);
        pointer-events: none;
    }
    
    .dashboard-header h1 {
        color: #ffffff !important;
        font-size: 2.3rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .dashboard-header p {
        color: rgba(255,255,255,0.9) !important;
        font-size: 1.1rem !important;
        margin: 10px 0 0 0 !important;
    }
    
    /* === SECTION HEADERS === */
    .section-header {
        color: #1e3a5f !important;
        font-size: 1.4rem !important;
        font-weight: 700 !important;
        margin: 25px 0 20px 0 !important;
        padding-bottom: 12px;
        border-bottom: 3px solid #3b82f6;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .sub-header {
        color: #1e3a5f !important;
        font-size: 1.15rem !important;
        font-weight: 600 !important;
        margin: 20px 0 15px 0 !important;
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 12px 16px;
        background: linear-gradient(135deg, #e8f4fc 0%, #f0f7ff 100%);
        border-radius: 12px;
        border-left: 4px solid #3b82f6;
    }
    
    .sub-header i { color: #3b82f6; font-size: 1rem; }
    
    /* === REGION CARDS === */
    .region-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8fbff 100%);
        padding: 20px;
        border-radius: 14px;
        margin-bottom: 12px;
        border: 1px solid #d0e3f7;
        box-shadow: 0 4px 12px rgba(30, 58, 95, 0.08);
        transition: all 0.35s ease;
    }
    
    .region-card:hover {
        transform: translateY(-5px) scale(1.02);
        border-color: #3b82f6;
        box-shadow: 0 12px 28px rgba(59, 130, 246, 0.22);
    }
    
    .region-card h4 {
        color: #1e3a5f !important;
        margin: 0 0 12px 0 !important;
        font-weight: 700 !important;
    }
    
    .region-card p {
        color: #4a6fa5 !important;
        margin: 6px 0 !important;
        font-size: 0.9rem !important;
    }
    
    /* === TAB STYLING === */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #ffffff;
        padding: 10px;
        border-radius: 14px;
        box-shadow: 0 4px 15px rgba(30, 58, 95, 0.08);
        border: 1px solid #e0e8f0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #f0f4f8;
        border-radius: 10px;
        padding: 12px 24px;
        color: #4a6fa5 !important;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #e8f4fc;
        border-color: #3b82f6;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1e3a5f 0%, #3b82f6 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    
    /* === SIDEBAR COMPONENTS === */
    .sidebar-header {
        color: #ffffff !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        margin-bottom: 20px !important;
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 15px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .sidebar-header i { color: #60a5fa; }
    
    .filter-label {
        color: #ffffff !important;
        font-weight: 600 !important;
        display: flex !important;
        align-items: center !important;
        gap: 8px;
        margin: 15px 0 8px 0 !important;
        font-size: 0.9rem;
    }
    
    .filter-label i { color: #60a5fa; }
    
    .sidebar-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        margin: 20px 0;
    }
    
    .filter-section {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .filter-section-title {
        color: #60a5fa !important;
        font-size: 0.75rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px !important;
    }
    
    /* === SIDEBAR INFO BOX === */
    .sidebar-info {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(96, 165, 250, 0.1) 100%) !important;
        color: rgba(255, 255, 255, 0.9) !important;
        font-size: 0.8rem !important;
        padding: 15px !important;
        margin-top: 20px !important;
        border-radius: 12px !important;
        border: 1px solid rgba(96, 165, 250, 0.3) !important;
    }
    
    .sidebar-info strong { color: #60a5fa !important; }
    
    /* === SIDEBAR BUTTONS === */
    section[data-testid="stSidebar"] .stButton button {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 20px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3) !important;
    }
    
    section[data-testid="stSidebar"] .stButton button:hover {
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%) !important;
        transform: translateY(-2px) !important;
    }
    
    /* === DOWNLOAD BUTTON === */
    .main .stDownloadButton button {
        background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%) !important;
        color: #ffffff !important;
        border: 2px solid #60a5fa !important;
        border-radius: 12px !important;
        padding: 14px 22px !important;
        font-weight: 700 !important;
        box-shadow: 0 6px 18px rgba(59, 130, 246, 0.35) !important;
    }
    
    .main .stDownloadButton button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%) !important;
        transform: translateY(-2px) !important;
    }
    
    .main .stDownloadButton button *,
    .main .stDownloadButton button span,
    .main .stDownloadButton button p,
    .main .stDownloadButton button div {
        color: #ffffff !important;
    }
    
    /* === FOOTER === */
    .footer {
        text-align: center;
        color: #4a6fa5;
        padding: 25px;
        background: linear-gradient(145deg, #ffffff 0%, #f8fbff 100%);
        border-radius: 16px;
        margin-top: 35px;
        box-shadow: 0 4px 15px rgba(30, 58, 95, 0.08);
        border: 1px solid #d0e3f7;
    }
    
    .footer p { color: #4a6fa5 !important; }
    .footer i { color: #3b82f6; margin-right: 8px; }
    
    /* === DATAFRAME === */
    [data-testid="stDataFrame"] {
        background: #ffffff !important;
        border-radius: 14px !important;
        border: 1px solid #d0e3f7 !important;
    }
    
    [data-testid="stDataFrame"] * {
        color: #1e3a5f !important;
    }
    
    thead th {
        background: linear-gradient(135deg, #1e3a5f 0%, #2c5282 100%) !important;
        color: #ffffff !important;
    }
    
    tbody td {
        color: #1e3a5f !important;
        background: #ffffff !important;
    }
    
    tbody tr:nth-child(even) td { background: #f8fbff !important; }
    tbody tr:hover td { background: #eaf3ff !important; }
    
    /* === PLOTLY CHARTS === */
    .js-plotly-plot {
        border-radius: 14px;
        overflow: visible;
        background: #ffffff !important;
        border: 1px solid #e0e8f0;
        padding-top: 8px;
        box-sizing: border-box;
    }
    
    .js-plotly-plot:hover {
        box-shadow: 0 8px 25px rgba(30, 58, 95, 0.12);
        transform: translateY(-2px);
    }
    
    .js-plotly-plot .plotly,
    .js-plotly-plot .plot-container,
    .js-plotly-plot .svg-container,
    .js-plotly-plot .bglayer,
    .js-plotly-plot .bglayer rect {
        background: #ffffff !important;
    }

    /* Keep axes/title readable without overriding trace label colors (e.g., pie labels) */
    .js-plotly-plot .xtick text,
    .js-plotly-plot .ytick text,
    .js-plotly-plot .gtitle {
        fill: #1e3a5f;
    }
    
    .js-plotly-plot .gridlayer path {
        stroke: rgba(59, 130, 246, 0.1) !important;
    }
    
    /* === INSIGHT CARDS === */
    .insight-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 16px;
        width: 100%;
    }
    
    .insight-card {
        border-radius: 16px;
        padding: 20px;
        border-left: 4px solid transparent;
        background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        min-height: 130px;
    }
    
    .insight-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .insight-label {
        color: #475569;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    .insight-value {
        color: #0f172a !important;
        font-size: 1.4rem;
        font-weight: 800;
        line-height: 1.2;
    }
    
    .insight-sub {
        font-size: 0.95rem;
        font-weight: 600;
    }
    
    .insight-card--category { border-left-color: #3b82f6; background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%); }
    .insight-card--category .insight-sub { color: #3b82f6; }
    
    .insight-card--region { border-left-color: #10b981; background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%); }
    .insight-card--region .insight-sub { color: #10b981; }
    
    .insight-card--segment { border-left-color: #ef4444; background: linear-gradient(135deg, #ffffff 0%, #fef3f2 100%); }
    .insight-card--segment .insight-sub { color: #ef4444; }
    
    .insight-card--month { border-left-color: #f59e0b; background: linear-gradient(135deg, #ffffff 0%, #fefce8 100%); }
    .insight-card--month .insight-sub { color: #f59e0b; }
    
    /* === SCROLLBAR === */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #f0f4f8; border-radius: 10px; }
    ::-webkit-scrollbar-thumb { background: linear-gradient(135deg, #3b82f6, #60a5fa); border-radius: 10px; }
    
    /* === ANIMATIONS === */
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.2); }
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .dashboard-header, .region-card, [data-testid="stMetric"], .kpi-card {
        animation: fadeInUp 0.4s ease-out;
    }
    
    /* === DIVIDER === */
    hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent, #3b82f6, transparent) !important;
        margin: 35px 0 !important;
    }
</style>
'''


def apply_styles():
    """Apply CSS styles to the Streamlit app"""
    import streamlit as st
    st.markdown(CSS_STYLES, unsafe_allow_html=True)
