import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Konfigurasi halaman
st.set_page_config(
    page_title="Super Store Sales Dashboard",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Font Awesome CDN dan Custom CSS
st.markdown("""
<meta charset="UTF-8">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
<style>
    /* === GLOBAL STYLES === */
    * {
        font-family: 'Poppins', sans-serif !important;
    }
    
    /* === RESPONSIVE DESIGN === */
    @media screen and (max-width: 1200px) {
        .dashboard-header h1 {
            font-size: 1.8rem !important;
        }
        [data-testid="stMetricValue"] {
            font-size: 1.5rem !important;
        }
        .section-header {
            font-size: 1.2rem !important;
        }
        .sub-header {
            font-size: 1rem !important;
        }
    }
    
    @media screen and (max-width: 992px) {
        .dashboard-header {
            padding: 20px 25px;
        }
        .dashboard-header h1 {
            font-size: 1.5rem !important;
        }
        [data-testid="stMetric"] {
            padding: 15px 18px;
        }
        [data-testid="stMetricValue"] {
            font-size: 1.3rem !important;
        }
        [data-testid="stMetricLabel"] {
            font-size: 0.8rem !important;
        }
        .region-card {
            padding: 15px;
        }
    }
    
    @media screen and (max-width: 768px) {
        .block-container {
            padding: 1rem 0.5rem;
        }
        .dashboard-header {
            padding: 15px 20px;
            border-radius: 12px;
        }
        .dashboard-header h1 {
            font-size: 1.2rem !important;
            flex-wrap: wrap;
        }
        .dashboard-header p {
            font-size: 0.9rem !important;
        }
        [data-testid="stMetric"] {
            padding: 12px 15px;
            border-radius: 12px;
        }
        [data-testid="stMetricValue"] {
            font-size: 1.1rem !important;
        }
        .section-header {
            font-size: 1rem !important;
            flex-wrap: wrap;
        }
        .sub-header {
            font-size: 0.9rem !important;
            padding: 10px 12px;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 8px 12px;
            font-size: 0.85rem;
        }
        .region-card {
            padding: 12px;
        }
        .region-card h4 {
            font-size: 0.95rem;
        }
        .region-card p {
            font-size: 0.8rem !important;
        }
    }
    
    @media screen and (max-width: 576px) {
        .dashboard-header h1 {
            font-size: 1rem !important;
        }
        [data-testid="stMetricValue"] {
            font-size: 1rem !important;
        }
        [data-testid="stMetricLabel"] {
            font-size: 0.7rem !important;
        }
        .stTabs [data-baseweb="tab-list"] {
            flex-wrap: wrap;
            gap: 4px;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 6px 10px;
            font-size: 0.75rem;
        }
    }
    
    /* Font Awesome Icons Fix */
    .fa, .fas, .far, .fab, .fal, .fad, [class*="fa-"] {
        font-family: 'Font Awesome 6 Free' !important;
        font-style: normal !important;
        font-variant: normal !important;
        text-rendering: auto !important;
        -webkit-font-smoothing: antialiased !important;
        -moz-osx-font-smoothing: grayscale !important;
        display: inline-block !important;
        width: auto !important;
        height: auto !important;
        line-height: 1 !important;
        vertical-align: -0.125em !important;
    }
    
    .fas, .fa-solid {
        font-weight: 900 !important;
        font-family: 'Font Awesome 6 Free' !important;
    }
    
    .far, .fa-regular {
        font-weight: 400 !important;
        font-family: 'Font Awesome 6 Free' !important;
    }
    
    .fab, .fa-brands {
        font-family: 'Font Awesome 6 Brands' !important;
        font-weight: 400 !important;
    }
    
    /* Sidebar icons visible */
    section[data-testid="stSidebar"] i {
        display: inline-block !important;
        width: auto !important;
        margin-right: 5px !important;
        color: inherit !important;
    }
    
    /* Main container styling - White & Blue Theme */
    .main, .stApp {
        background: linear-gradient(135deg, #f0f4f8 0%, #e8f4fc 50%, #f5f9ff 100%) !important;
    }
    
    .block-container {
        padding-top: 2rem;
    }
    
    /* === METRIC CARDS === */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #1e3a5f !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        color: #4a6fa5 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.85rem !important;
        color: #2e7d32 !important;
        font-weight: 500;
    }
    
    /* Metric container background */
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
        background: linear-gradient(180deg, #1e3a5f 0%, #2c5282 50%, #3b6ca8 100%) !important;
        width: 300px !important;
    }
    
    section[data-testid="stSidebar"] > div {
        background: transparent !important;
    }
    
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
        font-weight: 500;
    }
    
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMultiSelect label {
        color: #e0f0ff !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
    
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
        color: #e0f0ff !important;
    }
    
    /* Sidebar multiselect styling */
    section[data-testid="stSidebar"] .stMultiSelect > div > div {
        background: #ffffff !important;
        border: 1px solid #d0e3f7 !important;
        border-radius: 10px !important;
        color: #1e3a5f !important;
        transition: box-shadow 0.2s ease, border-color 0.2s ease;
    }
    
    section[data-testid="stSidebar"] .stMultiSelect > div > div:hover {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.12);
    }
    
    section[data-testid="stSidebar"] .stMultiSelect input {
        color: #1e3a5f !important;
    }
    
    section[data-testid="stSidebar"] .stMultiSelect span[data-baseweb="tag"] {
        background: #ffffff !important;
        color: #1e3a5f !important;
        border: 1px solid #3b82f6 !important;
        border-radius: 8px !important;
        font-weight: 600;
        box-shadow: 0 2px 6px rgba(30, 58, 95, 0.12);
        transition: background 0.15s ease, color 0.15s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    }
    
    section[data-testid="stSidebar"] .stMultiSelect span[data-baseweb="tag"]:hover {
        background: #e8f4fc !important;
        color: #1e3a5f !important;
        border-color: #1e3a5f !important;
        box-shadow: 0 3px 8px rgba(59, 130, 246, 0.2);
    }
    
    section[data-testid="stSidebar"] .stMultiSelect span[data-baseweb="tag"] svg path {
        fill: #1e3a5f !important;
    }
    
    /* Sidebar selectbox */
    section[data-testid="stSidebar"] .stSelectbox > div > div {
        background: #ffffff !important;
        border: 1px solid #d0e3f7 !important;
        border-radius: 10px !important;
        color: #1e3a5f !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox input {
        color: #1e3a5f !important;
    }
    
    /* === HEADER STYLING === */
    .dashboard-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #2c5282 50%, #3b82f6 100%);
        padding: 30px 40px;
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow: 0 10px 40px rgba(30, 58, 95, 0.25);
        border: none;
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
        display: flex;
        align-items: center;
        gap: 15px;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .dashboard-header p {
        color: rgba(255,255,255,0.9) !important;
        font-size: 1.1rem !important;
        margin: 10px 0 0 0 !important;
        font-weight: 400;
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
    
    .section-header i {
        color: #3b82f6;
        font-size: 1.3rem;
    }
    
    /* === SUB HEADERS === */
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
    
    .sub-header i {
        color: #3b82f6;
        font-size: 1rem;
    }
    
    /* === REGION CARDS === */
    .region-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8fbff 100%);
        padding: 20px;
        border-radius: 14px;
        margin-bottom: 12px;
        border: 1px solid #d0e3f7;
        box-shadow: 0 4px 12px rgba(30, 58, 95, 0.08);
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .region-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.08), transparent);
        transition: left 0.5s ease;
    }
    
    .region-card:hover {
        transform: translateY(-5px) scale(1.02);
        border-color: #3b82f6;
        box-shadow: 0 12px 28px rgba(59, 130, 246, 0.22);
        background: linear-gradient(145deg, #ffffff 0%, #eef6ff 100%);
    }
    
    .region-card:hover::before {
        left: 100%;
    }
    
    .region-card h4 {
        color: #1e3a5f !important;
        margin: 0 0 12px 0 !important;
        font-weight: 700 !important;
        font-size: 1.05rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .region-card h4::before {
        content: '';
        width: 8px;
        height: 8px;
        background: linear-gradient(135deg, #3b82f6, #60a5fa);
        border-radius: 50%;
    }
    
    .region-card p {
        color: #4a6fa5 !important;
        margin: 6px 0 !important;
        font-size: 0.9rem !important;
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 500;
    }
    
    .region-card i {
        color: #3b82f6;
        width: 18px;
        font-size: 0.85rem;
    }
    
    /* === DIVIDER STYLING === */
    hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent, #3b82f6, transparent) !important;
        margin: 35px 0 !important;
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
        border: 1px solid transparent;
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
        border-color: transparent;
    }
    
    /* Tab panel background */
    .stTabs [data-baseweb="tab-panel"] {
        background: transparent;
        padding-top: 20px;
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
    
    .sidebar-header i {
        color: #60a5fa;
        font-size: 1.2rem;
        display: inline-block !important;
        width: auto !important;
    }
    
    .filter-label {
        color: #ffffff !important;
        font-weight: 600 !important;
        display: flex !important;
        align-items: center !important;
        gap: 8px;
        margin: 15px 0 8px 0 !important;
        font-size: 0.9rem;
        padding-left: 5px;
    }
    
    .filter-label i {
        color: #60a5fa;
        font-size: 0.95rem;
        display: inline-block !important;
        width: auto !important;
    }
    
    .filter-label .fa, .filter-label .fas, .filter-label .far, .filter-label .fab {
        display: inline-block !important;
        width: auto !important;
        font-size: 0.95rem !important;
    }
    
    /* === FOOTER STYLING === */
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
    
    .footer p {
        color: #4a6fa5 !important;
        margin: 6px 0;
    }
    
    .footer i {
        color: #3b82f6;
        margin-right: 8px;
    }
    
    /* === DATAFRAME STYLING === */
    [data-testid="stDataFrame"] {
        background: #ffffff !important;
        border-radius: 14px !important;
        overflow: hidden;
        border: 1px solid #d0e3f7 !important;
        box-shadow: 0 4px 15px rgba(30, 58, 95, 0.08);
    }
    
    [data-testid="stDataFrameResizable"] {
        background: #ffffff !important;
    }
    
    .stDataFrame {
        background: #ffffff !important;
    }
    
    /* Fix Glide Data Editor (dataframe renderer) */
    .dvn-scroller,
    .dvn-scroll-inner,
    .dvn-stack,
    .dvn-container {
        background: #ffffff !important;
        color: #1e3a5f !important;
    }
    
    .dvn-scroller,
    .dvn-scroll-inner,
    .dvn-stack {
        overflow: visible !important;
    }
    
    /* DataFrame cell styling */
    .dvn-cell,
    .dvn-text,
    .dvn-cell span,
    .dvn-cell div,
    .dvn-stack div,
    .dvn-stack span {
        background: #ffffff !important;
        color: #1e3a5f !important;
        fill: #1e3a5f !important;
    }
    
    /* Force SVG text (Glide uses SVG for text sometimes) */
    .dvn-container svg text {
        fill: #1e3a5f !important;
        color: #1e3a5f !important;
    }
    
    /* Final safeguard for dataframe text visibility */
    [data-testid="stDataFrame"] * {
        color: #1e3a5f !important;
        fill: #1e3a5f !important;
    }
    
    /* Aggressive fix for Glide DataEditor canvas text */
    canvas {
        filter: none !important;
    }
    
    [data-testid="stDataFrame"] canvas + div,
    [data-testid="stDataFrame"] canvas ~ div {
        color: #1e3a5f !important;
    }
    
    /* Override any Streamlit dark theme remnants */
    .stDataFrame div[data-testid="glideDataEditor"],
    .stDataFrame [class*="glide"],
    div[data-glide-id] {
        background: #ffffff !important;
        color: #1e3a5f !important;
    }
    
    /* Force all text in data grid */
    [data-testid="stDataFrame"] span,
    [data-testid="stDataFrame"] div,
    [data-testid="stDataFrame"] p,
    [data-testid="stDataFrame"] td,
    [data-testid="stDataFrame"] th {
        color: #1e3a5f !important;
        background-color: transparent !important;
    }
    
    /* Glide cell text rendering */
    .gdg-cell,
    .gdg-header,
    .gdg-text {
        color: #1e3a5f !important;
        fill: #1e3a5f !important;
    }
    
    /* DataFrame header cell */
    .dvn-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #2c5282 100%) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* DataFrame Table Styling */
    [role="grid"] {
        background: #ffffff !important;
    }
    
    [role="rowheader"] {
        background: #ffffff !important;
        color: #1e3a5f !important;
    }
    
    /* Fix black background in dataframe */
    div[data-testid="stDataFrame"] > div {
        background: #ffffff !important;
    }
    
    div[data-testid="stDataFrame"] table {
        background: #ffffff !important;
    }
    
    /* DataFrame header */
    thead {
        background: linear-gradient(135deg, #1e3a5f 0%, #2c5282 100%) !important;
    }
    
    thead th {
        background: linear-gradient(135deg, #1e3a5f 0%, #2c5282 100%) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* DataFrame rows */
    tbody td {
        color: #1e3a5f !important;
        background: #ffffff !important;
        border-color: #e0e8f0 !important;
    }
    
    tbody tr:nth-child(even) td {
        background: #f8fbff !important;
    }
    
    /* === PLOTLY CHART CONTAINERS === */
    .js-plotly-plot {
        border-radius: 14px;
        overflow: hidden;
        background: white;
    }
    
    /* === COLUMNS GAP === */
    [data-testid="column"] {
        padding: 6px;
    }
    
    /* === SCROLLBAR STYLING === */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f0f4f8;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #3b82f6, #60a5fa);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #1e3a5f, #3b82f6);
    }
    
    /* === ANIMATION KEYFRAMES === */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(15px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .dashboard-header, .region-card, [data-testid="stMetric"] {
        animation: fadeInUp 0.4s ease-out;
    }
    
    /* Hover polish */
    [data-testid="stMetric"]:hover,
    .region-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(30, 58, 95, 0.18);
    }
    
    [data-testid="stSidebar"] .stSelectbox > div > div:hover {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.12);
    }
    
    tbody tr:hover td {
        background: #eaf3ff !important;
    }
    
    /* === SIDEBAR TOGGLE BUTTON FIX === */
    button[kind="header"],
    button[kind="headerNoPadding"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapseButton"] button,
    [data-testid="collapsedControl"],
    [data-testid="collapsedControl"] button {
        background: #ffffff !important;
        border: 2px solid #3b82f6 !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 12px rgba(30, 58, 95, 0.2) !important;
        padding: 8px !important;
        transition: all 0.3s ease !important;
    }
    
    button[kind="header"]:hover,
    button[kind="headerNoPadding"]:hover,
    [data-testid="stSidebarCollapseButton"]:hover,
    [data-testid="stSidebarCollapseButton"] button:hover,
    [data-testid="collapsedControl"]:hover,
    [data-testid="collapsedControl"] button:hover {
        background: linear-gradient(135deg, #e8f4fc 0%, #dbeafe 100%) !important;
        border-color: #1e3a5f !important;
        transform: scale(1.05) !important;
        box-shadow: 0 6px 16px rgba(59, 130, 246, 0.3) !important;
    }
    
    /* Material Icons Fix for Streamlit */
    [data-testid="stIconMaterial"],
    .st-emotion-cache-ujm5ma,
    span[data-testid="stIconMaterial"] {
        font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
        font-weight: normal !important;
        font-style: normal !important;
        font-size: 24px !important;
        line-height: 1 !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        display: inline-block !important;
        white-space: nowrap !important;
        word-wrap: normal !important;
        direction: ltr !important;
        -webkit-font-feature-settings: 'liga' !important;
        -webkit-font-smoothing: antialiased !important;
        color: #1e3a5f !important;
    }
    
    /* Sidebar toggle icon color */
    [data-testid="stSidebarCollapseButton"] span,
    [data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"],
    [data-testid="collapsedControl"] span,
    [data-testid="collapsedControl"] [data-testid="stIconMaterial"] {
        color: #1e3a5f !important;
        font-size: 22px !important;
    }
    
    /* SVG fallback */
    button[kind="header"] svg,
    button[kind="headerNoPadding"] svg,
    [data-testid="stSidebarCollapseButton"] svg,
    [data-testid="collapsedControl"] svg {
        fill: #1e3a5f !important;
        color: #1e3a5f !important;
        stroke: #1e3a5f !important;
        width: 22px !important;
        height: 22px !important;
    }
    
    /* BaseWeb icon styling */
    [data-baseweb="icon"] {
        color: inherit !important;
    }
    
    section[data-testid="stSidebar"] [data-baseweb="icon"] svg {
        fill: #ffffff !important;
    }
    
    /* === CUSTOM TABLE STYLING === */
    .custom-table-container {
        background: #ffffff;
        border-radius: 14px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(30, 58, 95, 0.1);
        border: 1px solid #d0e3f7;
        margin: 10px 0;
    }
    
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        font-family: 'Poppins', sans-serif;
        background: #ffffff;
    }
    
    .custom-table thead {
        background: linear-gradient(135deg, #1e3a5f 0%, #2c5282 100%);
    }
    
    .custom-table thead th {
        padding: 14px 16px;
        text-align: left;
        font-weight: 600;
        font-size: 0.9rem;
        color: #ffffff !important;
        border: none;
        white-space: nowrap;
    }
    
    .custom-table tbody tr {
        transition: background 0.2s ease;
    }
    
    .custom-table tbody tr:nth-child(even) {
        background: #f8fbff;
    }
    
    .custom-table tbody tr:nth-child(odd) {
        background: #ffffff;
    }
    
    .custom-table tbody tr:hover {
        background: linear-gradient(135deg, #eef6ff 0%, #e0f0ff 100%) !important;
    }
    
    .custom-table tbody td {
        padding: 12px 16px;
        color: #1e3a5f !important;
        font-size: 0.875rem;
        border-bottom: 1px solid #e8f0f8;
        font-weight: 500;
    }
    
    .custom-table tbody tr:last-child td {
        border-bottom: none;
    }
    
    /* Scrollable table wrapper */
    .table-scroll-wrapper {
        max-height: 400px;
        overflow-y: auto;
        overflow-x: auto;
    }
    
    .table-scroll-wrapper::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    
    .table-scroll-wrapper::-webkit-scrollbar-thumb {
        background: #3b82f6;
        border-radius: 10px;
    }
    
    /* === PLOTLY HOVER IMPROVEMENTS === */
    .js-plotly-plot .plotly .hoverlayer {
        pointer-events: none;
    }
    
    .js-plotly-plot {
        border-radius: 14px;
        overflow: hidden;
        background: #ffffff !important;
        box-shadow: 0 4px 15px rgba(30, 58, 95, 0.08);
        border: 1px solid #e0e8f0;
        transition: box-shadow 0.3s ease, transform 0.3s ease;
    }
    
    .js-plotly-plot:hover {
        box-shadow: 0 8px 25px rgba(30, 58, 95, 0.12);
        transform: translateY(-2px);
    }
    
    /* Search input in multiselect */
    section[data-testid="stSidebar"] .stMultiSelect input::placeholder {
        color: #94a3b8 !important;
        font-style: italic;
    }
    
    section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="popover"] {
        background: #ffffff !important;
        border: 1px solid #3b82f6 !important;
        border-radius: 10px !important;
        box-shadow: 0 8px 20px rgba(30, 58, 95, 0.15) !important;
    }
    
    section[data-testid="stSidebar"] .stMultiSelect [role="listbox"] {
        background: #ffffff !important;
    }
    
    section[data-testid="stSidebar"] .stMultiSelect [role="option"] {
        color: #1e3a5f !important;
        background: #ffffff !important;
        padding: 10px 14px !important;
        transition: background 0.15s ease;
    }
    
    section[data-testid="stSidebar"] .stMultiSelect [role="option"]:hover {
        background: linear-gradient(135deg, #e8f4fc 0%, #dbeafe 100%) !important;
    }
    
    section[data-testid="stSidebar"] .stMultiSelect [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%) !important;
        color: #ffffff !important;
    }
    
    /* Search/Text input styling in sidebar */
    section[data-testid="stSidebar"] .stTextInput > div > div {
        background: #ffffff !important;
        border: 1px solid #d0e3f7 !important;
        border-radius: 10px !important;
        color: #1e3a5f !important;
        transition: box-shadow 0.2s ease, border-color 0.2s ease;
    }
    
    section[data-testid="stSidebar"] .stTextInput > div > div:hover,
    section[data-testid="stSidebar"] .stTextInput > div > div:focus-within {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important;
    }
    
    section[data-testid="stSidebar"] .stTextInput input {
        color: #1e3a5f !important;
        font-weight: 500 !important;
    }
    
    section[data-testid="stSidebar"] .stTextInput input::placeholder {
        color: #94a3b8 !important;
        font-style: italic;
    }
    
    /* Sidebar info text */
    .sidebar-info {
        color: rgba(255, 255, 255, 0.7) !important;
        font-size: 0.8rem !important;
        padding: 10px;
        margin-top: 20px;
        border-top: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center;
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

# Search product
st.sidebar.markdown('<p class="filter-label"><i class="fas fa-search"></i> Cari Produk</p>', unsafe_allow_html=True)
product_search = st.sidebar.text_input(
    "Search",
    placeholder="Ketik nama produk...",
    label_visibility="collapsed"
)

# Sidebar info
st.sidebar.markdown('''
<div class="sidebar-info">
    <p><i class="fas fa-info-circle"></i> Gunakan filter untuk menyaring data</p>
    <p>💡 Klik tombol ▶ untuk menutup sidebar</p>
</div>
''', unsafe_allow_html=True)

# Apply filters
filtered_df = df[
    (df['order_year'].isin(selected_years)) &
    (df['region'].isin(selected_regions)) &
    (df['segment'].isin(selected_segments)) &
    (df['category'].isin(selected_categories))
]

# Apply product search filter
if product_search:
    filtered_df = filtered_df[filtered_df['product_name'].str.contains(product_search, case=False, na=False)]

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
blue_colors = ['#1e3a5f', '#2c5282', '#3b82f6', '#60a5fa', '#93c5fd', '#bfdbfe']
gradient_scale = [[0, '#bfdbfe'], [0.5, '#3b82f6'], [1, '#1e3a5f']]

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
            hole=0.45
        )
        fig_category.update_layout(
            paper_bgcolor='rgba(255,255,255,0.9)',
            plot_bgcolor='rgba(255,255,255,0.9)',
            font=dict(color='#1e3a5f', family='Poppins'),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5,
                font=dict(color='#1e3a5f')
            )
        )
        fig_category.update_traces(textfont=dict(color='#ffffff'))
        st.plotly_chart(fig_category, use_container_width=True)
    
    with col2:
        # Sales by Segment
        st.markdown('<p class="sub-header"><i class="fas fa-users"></i> Sales by Segment</p>', unsafe_allow_html=True)
        segment_sales = filtered_df.groupby('segment')['sales'].sum().reset_index()
        fig_segment = px.pie(
            segment_sales, 
            values='sales', 
            names='segment',
            color_discrete_sequence=['#2c5282', '#3b82f6', '#93c5fd'],
            hole=0.45
        )
        fig_segment.update_layout(
            paper_bgcolor='rgba(255,255,255,0.9)',
            plot_bgcolor='rgba(255,255,255,0.9)',
            font=dict(color='#1e3a5f', family='Poppins'),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5,
                font=dict(color='#1e3a5f')
            )
        )
        fig_segment.update_traces(textfont=dict(color='#ffffff'))
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
        paper_bgcolor='rgba(255,255,255,0.9)',
        plot_bgcolor='rgba(255,255,255,0.9)',
        font=dict(color='#1e3a5f', family='Poppins'),
        xaxis=dict(gridcolor='rgba(59, 130, 246, 0.15)', title_font=dict(color='#1e3a5f'), tickfont=dict(color='#4a6fa5')),
        yaxis=dict(gridcolor='rgba(59, 130, 246, 0.15)', title_font=dict(color='#1e3a5f'), tickfont=dict(color='#4a6fa5')),
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
        color_discrete_sequence=['#3b82f6']
    )
    fig_trend.update_layout(
        paper_bgcolor='rgba(255,255,255,0.9)',
        plot_bgcolor='rgba(255,255,255,0.9)',
        font=dict(color='#1e3a5f', family='Poppins'),
        xaxis=dict(gridcolor='rgba(59, 130, 246, 0.15)', title='Bulan', title_font=dict(color='#1e3a5f'), tickfont=dict(color='#4a6fa5')),
        yaxis=dict(gridcolor='rgba(59, 130, 246, 0.15)', title='Total Sales', title_font=dict(color='#1e3a5f'), tickfont=dict(color='#4a6fa5')),
        height=400
    )
    fig_trend.update_traces(line=dict(width=4, color='#3b82f6'), marker=dict(size=10, color='#1e3a5f', line=dict(width=2, color='#ffffff')))
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
            paper_bgcolor='rgba(255,255,255,0.9)',
            plot_bgcolor='rgba(255,255,255,0.9)',
            font=dict(color='#1e3a5f', family='Poppins'),
            xaxis=dict(gridcolor='rgba(59, 130, 246, 0.15)', title='Quarter', title_font=dict(color='#1e3a5f'), tickfont=dict(color='#4a6fa5')),
            yaxis=dict(gridcolor='rgba(59, 130, 246, 0.15)', title='Total Sales', title_font=dict(color='#1e3a5f'), tickfont=dict(color='#4a6fa5')),
            legend_title="Tahun",
            legend=dict(font=dict(color='#1e3a5f'))
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
            paper_bgcolor='rgba(255,255,255,0.9)',
            plot_bgcolor='rgba(255,255,255,0.9)',
            font=dict(color='#1e3a5f', family='Poppins'),
            xaxis=dict(gridcolor='rgba(59, 130, 246, 0.15)', title='Tahun', title_font=dict(color='#1e3a5f'), tickfont=dict(color='#4a6fa5')),
            yaxis=dict(gridcolor='rgba(59, 130, 246, 0.15)', title='Total Sales', title_font=dict(color='#1e3a5f'), tickfont=dict(color='#4a6fa5')),
            showlegend=False,
            coloraxis_showscale=False
        )
        fig_yearly.update_traces(texttemplate='$%{text:,.0f}', textposition='outside', textfont=dict(color='#1e3a5f'))
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
        paper_bgcolor='rgba(255,255,255,0.9)',
        plot_bgcolor='rgba(255,255,255,0.9)',
        font=dict(color='#1e3a5f', family='Poppins'),
        xaxis=dict(gridcolor='rgba(59, 130, 246, 0.15)', title='Hari', title_font=dict(color='#1e3a5f'), tickfont=dict(color='#4a6fa5')),
        yaxis=dict(gridcolor='rgba(59, 130, 246, 0.15)', title='Total Sales', title_font=dict(color='#1e3a5f'), tickfont=dict(color='#4a6fa5')),
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
            paper_bgcolor='rgba(255,255,255,0.9)',
            plot_bgcolor='rgba(255,255,255,0.9)',
            font=dict(color='#1e3a5f', family='Poppins'),
            xaxis=dict(gridcolor='rgba(59, 130, 246, 0.15)', title='Total Sales', title_font=dict(color='#1e3a5f'), tickfont=dict(color='#4a6fa5')),
            yaxis=dict(gridcolor='rgba(59, 130, 246, 0.15)', title='State', categoryorder='total ascending', title_font=dict(color='#1e3a5f'), tickfont=dict(color='#4a6fa5')),
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
    
    fig_cities = px.bar(
        city_sales,
        x='sales',
        y='city_state',
        orientation='h',
        color='sales',
        color_continuous_scale='Blues',
        text=city_sales['sales'].apply(lambda x: f'${x:,.0f}')
    )
    fig_cities.update_layout(
        paper_bgcolor='#ffffff',
        plot_bgcolor='#ffffff',
        font=dict(color='#1e3a5f', family='Poppins'),
        xaxis=dict(
            gridcolor='rgba(59, 130, 246, 0.15)',
            title='Total Sales',
            title_font=dict(color='#1e3a5f'),
            tickfont=dict(color='#4a6fa5')
        ),
        yaxis=dict(
            gridcolor='rgba(59, 130, 246, 0.15)',
            title='',
            categoryorder='total ascending',
            title_font=dict(color='#1e3a5f'),
            tickfont=dict(color='#1e3a5f', size=11)
        ),
        coloraxis_showscale=False,
        height=400,
        margin=dict(l=10, r=10, t=10, b=10),
        hoverlabel=dict(
            bgcolor='#1e3a5f',
            font_size=13,
            font_family='Poppins',
            font_color='white',
            bordercolor='#3b82f6'
        )
    )
    fig_cities.update_traces(
        textposition='inside',
        textfont=dict(color='white', size=11, family='Poppins'),
        hovertemplate='<b>%{y}</b><br>Sales: $%{x:,.2f}<extra></extra>',
        marker=dict(line=dict(color='#1e3a5f', width=1))
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
            paper_bgcolor='rgba(255,255,255,0.9)',
            plot_bgcolor='rgba(255,255,255,0.9)',
            font=dict(color='#1e3a5f', family='Poppins'),
            xaxis=dict(gridcolor='rgba(59, 130, 246, 0.15)', title='Total Sales', title_font=dict(color='#1e3a5f'), tickfont=dict(color='#4a6fa5')),
            yaxis=dict(gridcolor='rgba(59, 130, 246, 0.15)', title='Sub-Category', categoryorder='total ascending', title_font=dict(color='#1e3a5f'), tickfont=dict(color='#4a6fa5')),
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
            paper_bgcolor='#ffffff',
            font=dict(color='#1e3a5f', family='Poppins'),
            height=400,
            margin=dict(t=10, b=10, l=10, r=10),
            coloraxis_showscale=False,
            hoverlabel=dict(
                bgcolor='#1e3a5f',
                font_size=13,
                font_family='Poppins',
                font_color='white'
            )
        )
        fig_sunburst.update_traces(
            textfont=dict(color='#ffffff', size=12, family='Poppins'),
            hovertemplate='<b>%{label}</b><br>Sales: $%{value:,.2f}<extra></extra>',
            insidetextorientation='radial'
        )
        st.plotly_chart(fig_sunburst, use_container_width=True)
    
    # Top Products Table
    st.markdown('<p class="sub-header"><i class="fas fa-trophy"></i> Top 20 Products by Sales</p>', unsafe_allow_html=True)
    top_products = filtered_df.groupby(['product_name', 'category', 'sub_category'])['sales'].sum().reset_index()
    top_products = top_products.sort_values('sales', ascending=False).head(20)
    top_products['sales'] = top_products['sales'].apply(lambda x: f"${x:,.2f}")
    top_products.columns = ['Product Name', 'Category', 'Sub-Category', 'Total Sales']
    
    # Custom HTML table
    table_html = '<div class="custom-table-container"><div class="table-scroll-wrapper"><table class="custom-table"><thead><tr>'
    for col in top_products.columns:
        table_html += f'<th>{col}</th>'
    table_html += '</tr></thead><tbody>'
    for _, row in top_products.iterrows():
        table_html += '<tr>'
        for val in row:
            table_html += f'<td>{val}</td>'
        table_html += '</tr>'
    table_html += '</tbody></table></div></div>'
    st.markdown(table_html, unsafe_allow_html=True)

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
            paper_bgcolor='rgba(255,255,255,0.9)',
            plot_bgcolor='rgba(255,255,255,0.9)',
            font=dict(color='#1e3a5f', family='Poppins'),
            xaxis=dict(gridcolor='rgba(59, 130, 246, 0.15)', title='Total Sales', title_font=dict(color='#1e3a5f'), tickfont=dict(color='#4a6fa5')),
            yaxis=dict(gridcolor='rgba(59, 130, 246, 0.15)', title='Customer', categoryorder='total ascending', title_font=dict(color='#1e3a5f'), tickfont=dict(color='#4a6fa5')),
            legend_title="Segment",
            legend=dict(font=dict(color='#1e3a5f')),
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
            color_discrete_sequence=['#1e3a5f', '#3b82f6']
        )
        fig_seg_dist.update_layout(
            paper_bgcolor='rgba(255,255,255,0.9)',
            plot_bgcolor='rgba(255,255,255,0.9)',
            font=dict(color='#1e3a5f', family='Poppins'),
            xaxis=dict(gridcolor='rgba(59, 130, 246, 0.15)', title_font=dict(color='#1e3a5f'), tickfont=dict(color='#4a6fa5')),
            yaxis=dict(gridcolor='rgba(59, 130, 246, 0.15)', title='Count', title_font=dict(color='#1e3a5f'), tickfont=dict(color='#4a6fa5')),
            legend_title="Metric",
            legend=dict(font=dict(color='#1e3a5f')),
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
    
    # Custom HTML table
    table_html2 = '<div class="custom-table-container"><div class="table-scroll-wrapper"><table class="custom-table"><thead><tr>'
    for col in segment_analysis.columns:
        table_html2 += f'<th>{col}</th>'
    table_html2 += '</tr></thead><tbody>'
    for _, row in segment_analysis.iterrows():
        table_html2 += '<tr>'
        for val in row:
            table_html2 += f'<td>{val}</td>'
        table_html2 += '</tr>'
    table_html2 += '</tbody></table></div></div>'
    st.markdown(table_html2, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <p><i class="fas fa-chart-line"></i> Sales Analytics Dashboard | Built with Streamlit & Plotly</p>
    <p><i class="fas fa-database"></i> Data: 2015-2018 Sales Data</p>
</div>
""", unsafe_allow_html=True)
