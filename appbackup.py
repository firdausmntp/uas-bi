import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import plotly.io as pio

# Set default Plotly template to ensure charts are visible
pio.templates.default = "plotly_white"

# Konfigurasi halaman
st.set_page_config(
    page_title="Super Store Sales Dashboard",
    page_icon="�",
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
    /* === SVG ICONS FOR METRICS === */
    .metric-icon {
        width: 18px;
        height: 18px;
        display: inline-block;
        vertical-align: middle;
        margin-right: 6px;
        fill: currentColor;
    }
    
    .metric-icon-blue { color: #3b82f6; }
    .metric-icon-green { color: #10b981; }
    .metric-icon-purple { color: #8b5cf6; }
    .metric-icon-orange { color: #f59e0b; }
    .metric-icon-red { color: #ef4444; }
    .metric-icon-cyan { color: #06b6d4; }
    .metric-icon-pink { color: #ec4899; }
    .metric-icon-indigo { color: #6366f1; }
    .metric-icon-teal { color: #14b8a6; }
    
    /* === KPI CARDS WITH SVG ICONS === */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 15px;
        margin-bottom: 20px;
    }
    
    .kpi-grid--4cols {
        grid-template-columns: repeat(4, 1fr);
    }
    
    .kpi-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 16px;
        padding: 20px;
        display: flex;
        align-items: flex-start;
        gap: 15px;
        box-shadow: 0 4px 15px rgba(30, 58, 95, 0.08);
        border: 1px solid rgba(59, 130, 246, 0.1);
        transition: all 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(30, 58, 95, 0.12);
    }
    
    .kpi-icon {
        width: 48px;
        height: 48px;
        min-width: 48px;
        min-height: 48px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        color: white;
    }
    
    .kpi-icon svg {
        width: 24px !important;
        height: 24px !important;
        display: block !important;
        stroke: white !important;
        fill: none !important;
        color: white !important;
    }
    
    .kpi-card--sales .kpi-icon { background: linear-gradient(135deg, #10b981 0%, #059669 100%); }
    .kpi-card--avg .kpi-icon { background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); }
    .kpi-card--customers .kpi-icon { background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); }
    .kpi-card--products .kpi-icon { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); }
    .kpi-card--orders .kpi-icon { background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); }
    .kpi-card--categories .kpi-icon { background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%); }
    .kpi-card--subcategories .kpi-icon { background: linear-gradient(135deg, #ec4899 0%, #db2777 100%); }
    .kpi-card--states .kpi-icon { background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%); }
    .kpi-card--regions .kpi-icon { background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%); }
    
    .kpi-content {
        display: flex;
        flex-direction: column;
        min-width: 0;
    }
    
    .kpi-label {
        font-size: 0.8rem;
        font-weight: 500;
        color: #64748b;
        margin-bottom: 4px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .kpi-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e3a5f;
        line-height: 1.2;
        margin-bottom: 4px;
    }
    
    .kpi-delta {
        font-size: 0.75rem;
        color: #10b981;
        font-weight: 500;
    }
    
    /* KPI Grid Responsive */
    @media screen and (max-width: 1200px) {
        .kpi-grid {
            grid-template-columns: repeat(3, 1fr);
        }
        .kpi-grid--4cols {
            grid-template-columns: repeat(2, 1fr);
        }
        .kpi-value {
            font-size: 1.3rem;
        }
    }
    
    @media screen and (max-width: 768px) {
        .kpi-grid,
        .kpi-grid--4cols {
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
        }
        .kpi-card {
            padding: 15px;
            gap: 10px;
        }
        .kpi-icon {
            width: 40px;
            height: 40px;
        }
        .kpi-icon svg {
            width: 20px;
            height: 20px;
        }
        .kpi-value {
            font-size: 1.1rem;
        }
        .kpi-label {
            font-size: 0.7rem;
        }
        .kpi-delta {
            font-size: 0.65rem;
        }
    }
    
    @media screen and (max-width: 480px) {
        .kpi-grid,
        .kpi-grid--4cols {
            grid-template-columns: 1fr;
        }
        .kpi-card {
            padding: 12px;
        }
        .kpi-value {
            font-size: 1rem;
        }
    }
    
    /* === GLOBAL STYLES === */
    * {
        font-family: 'Poppins', sans-serif !important;
    }
    
    /* === RESPONSIVE DESIGN === */
    @media screen and (max-width: 1400px) {
        .dashboard-header h1 {
            font-size: 2rem !important;
        }
        [data-testid="stMetricValue"] {
            font-size: 1.4rem !important;
        }
        .section-header {
            font-size: 1.3rem !important;
        }
        .sub-header {
            font-size: 1.1rem !important;
        }
    }
    
    @media screen and (max-width: 1200px) {
        .dashboard-header h1 {
            font-size: 1.8rem !important;
        }
        [data-testid="stMetricValue"] {
            font-size: 1.3rem !important;
        }
        .section-header {
            font-size: 1.2rem !important;
        }
        .sub-header {
            font-size: 1rem !important;
        }
        /* Plotly chart responsive */
        .js-plotly-plot .plotly .gtitle {
            font-size: 14px !important;
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
            font-size: 1.2rem !important;
        }
        [data-testid="stMetricLabel"] {
            font-size: 0.75rem !important;
        }
        .region-card {
            padding: 15px;
        }
        div[data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
            align-items: stretch !important;
            gap: 12px !important;
        }
        div[data-testid="column"] {
            width: 100% !important;
            min-width: 100% !important;
        }
        /* Chart container responsive */
        .js-plotly-plot {
            min-height: 280px !important;
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
            font-size: 1rem !important;
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
        .live-stats-row {
            flex-direction: column;
            align-items: stretch;
        }
        .live-stats-row .live-pill {
            width: 100%;
            justify-content: center;
        }
        .insight-grid {
            grid-template-columns: 1fr 1fr;
        }
        .insight-card {
            width: 100%;
        }
        div[data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
            align-items: stretch !important;
            gap: 8px !important;
        }
        div[data-testid="column"] {
            width: 100% !important;
            min-width: 100% !important;
        }
        /* Chart container responsive for tablet */
        .js-plotly-plot {
            min-height: 300px !important;
        }
        .js-plotly-plot .xtick text,
        .js-plotly-plot .ytick text {
            font-size: 10px !important;
        }
        .js-plotly-plot .legendtext {
            font-size: 10px !important;
        }
    }
    
    @media screen and (max-width: 576px) {
        .block-container {
            padding: 0.75rem 0.4rem;
            margin-top: 10px;
        }
        .dashboard-header {
            padding: 12px 16px;
            text-align: center;
        }
        .dashboard-header::before {
            display: none;
        }
        .dashboard-header h1 {
            font-size: 1rem !important;
            justify-content: center;
        }
        .dashboard-header p {
            font-size: 0.85rem !important;
        }
        [data-testid="stMetricValue"] {
            font-size: 0.95rem !important;
        }
        [data-testid="stMetricLabel"] {
            font-size: 0.65rem !important;
        }
        [data-testid="stMetric"] {
            width: 100% !important;
            margin-bottom: 10px;
        }
        .section-header {
            font-size: 0.95rem !important;
        }
        .sub-header {
            font-size: 0.85rem !important;
        }
        .live-stats-row {
            gap: 10px;
        }
        .stTabs [data-baseweb="tab-list"] {
            flex-wrap: nowrap;
            gap: 6px;
            overflow-x: auto;
            scrollbar-width: none;
            -webkit-overflow-scrolling: touch;
        }
        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {
            display: none;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 6px 12px;
            font-size: 0.75rem;
            flex: 0 0 auto;
            white-space: nowrap;
        }
        .insight-grid {
            grid-template-columns: 1fr;
        }
        .insight-card {
            text-align: center;
            min-height: auto;
        }
        .insight-label {
            justify-content: center;
        }
        .insight-value {
            font-size: 1.1rem;
        }
        .custom-table thead th,
        .custom-table tbody td {
            font-size: 0.7rem;
            padding: 8px 10px;
        }
        /* Chart container responsive for mobile */
        .js-plotly-plot {
            min-height: 260px !important;
        }
        .js-plotly-plot .xtick text,
        .js-plotly-plot .ytick text {
            font-size: 9px !important;
        }
        .js-plotly-plot .gtitle {
            font-size: 12px !important;
        }
        .js-plotly-plot .legendtext {
            font-size: 9px !important;
        }
        /* Pie chart label fix for mobile */
        .js-plotly-plot .pielayer text {
            font-size: 8px !important;
        }
    }
    
    @media screen and (max-width: 400px) {
        .dashboard-header h1 {
            font-size: 0.9rem !important;
        }
        .dashboard-header p {
            font-size: 0.75rem !important;
        }
        [data-testid="stMetricValue"] {
            font-size: 0.85rem !important;
        }
        [data-testid="stMetricLabel"] {
            font-size: 0.6rem !important;
        }
        .section-header {
            font-size: 0.85rem !important;
        }
        .sub-header {
            font-size: 0.75rem !important;
            padding: 8px 10px;
        }
        .insight-value {
            font-size: 1rem;
        }
        .insight-label {
            font-size: 0.7rem;
        }
        .custom-table thead th,
        .custom-table tbody td {
            font-size: 0.65rem;
            padding: 6px 8px;
        }
        /* Very small screen chart adjustments */
        .js-plotly-plot {
            min-height: 220px !important;
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
        overflow-x: hidden !important;
    }

    body {
        overflow-x: hidden !important;
    }
    
    /* === CHART VISIBILITY FIX === */
    /* Force all chart containers to have visible background */
    .js-plotly-plot,
    .plotly,
    .plot-container,
    .svg-container {
        width: 100% !important;
        min-height: 200px !important;
        display: block !important;
        background-color: #ffffff !important;
        border-radius: 12px !important;
    }
    
    /* Ensure chart container has proper background */
    [data-testid="stPlotlyChart"] {
        background-color: #ffffff !important;
        border-radius: 16px !important;
        padding: 15px !important;
        box-shadow: 0 4px 20px rgba(30, 58, 95, 0.12) !important;
        margin-bottom: 20px !important;
        border: 1px solid rgba(59, 130, 246, 0.15) !important;
    }
    
    /* Fix SVG visibility in charts - IMPORTANT */
    .js-plotly-plot .main-svg,
    .js-plotly-plot svg {
        background-color: #ffffff !important;
    }
    
    .js-plotly-plot .bg,
    .js-plotly-plot rect.bg {
        fill: #ffffff !important;
    }
    
    /* Fix draglayer and bindlayer backgrounds */
    .js-plotly-plot .draglayer,
    .js-plotly-plot .bindlayer {
        pointer-events: all;
    }
    
    /* Ensure all chart backgrounds are visible */
    .js-plotly-plot .bglayer rect,
    .js-plotly-plot .layer-above,
    .js-plotly-plot .imagelayer {
        fill: #ffffff !important;
    }
    
    /* Ensure text is visible in charts */
    .js-plotly-plot .xtick text,
    .js-plotly-plot .ytick text {
        fill: #1e3a5f !important;
    }
    
    .js-plotly-plot .gtitle {
        fill: #1e3a5f !important;
    }
    
    .js-plotly-plot .legendtext {
        fill: #1e3a5f !important;
    }
    
    /* Force pie chart and bar chart visibility */
    .js-plotly-plot .pielayer,
    .js-plotly-plot .barlayer {
        opacity: 1 !important;
    }
    
    /* Ensure chart traces are visible */
    .js-plotly-plot .trace {
        opacity: 1 !important;
    }
    
    /* Chart title styling */
    .js-plotly-plot .g-gtitle text {
        fill: #1e3a5f !important;
        font-weight: 600 !important;
    }
    
    /* CRITICAL: Fix Streamlit dark mode/theme issues with charts */
    .stApp [data-testid="stPlotlyChart"] > div,
    .stApp [data-testid="stPlotlyChart"] iframe,
    .stApp .element-container [data-testid="stPlotlyChart"] {
        background-color: #ffffff !important;
    }
    
    /* Force visibility on all SVG elements */
    .stApp svg,
    .stApp .js-plotly-plot svg,
    .stApp [data-testid="stPlotlyChart"] svg {
        background-color: #ffffff !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    
    /* Ensure pie slices and bar colors are visible */
    .js-plotly-plot .slice path,
    .js-plotly-plot .bars path {
        opacity: 1 !important;
        stroke-opacity: 1 !important;
        fill-opacity: 1 !important;
    }
    
    /* CRITICAL: Force pie slices to have dark border for visibility */
    .js-plotly-plot .pielayer .trace .slice path {
        stroke: #000000 !important;
        stroke-width: 2px !important;
    }
    
    /* Force bar chart bars to have visible stroke */
    .js-plotly-plot .barlayer .trace .points path {
        stroke: #1e3a5f !important;
        stroke-width: 1px !important;
    }
    
    /* Fix line chart visibility */
    .js-plotly-plot .scatterlayer path,
    .js-plotly-plot .scatterlayer .point {
        opacity: 1 !important;
        stroke-opacity: 1 !important;
    }
    
    /* Ensure legends are visible */
    .js-plotly-plot .legend {
        opacity: 1 !important;
    }
    
    .js-plotly-plot .legend .traces {
        opacity: 1 !important;
    }
    
    /* === DOWNLOAD BUTTON STYLING === */
    .stDownloadButton button,
    [data-testid="stDownloadButton"] button {
        background: linear-gradient(135deg, #1e3a5f 0%, #2c5282 100%) !important;
        color: #ffffff !important;
        border: 2px solid #3b82f6 !important;
        border-radius: 12px !important;
        padding: 12px 20px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(30, 58, 95, 0.2) !important;
    }
    
    .stDownloadButton button:hover,
    [data-testid="stDownloadButton"] button:hover {
        background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%) !important;
        color: #ffffff !important;
        border-color: #93c5fd !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.35) !important;
    }
    
    .stDownloadButton button p,
    [data-testid="stDownloadButton"] button p,
    .stDownloadButton button span,
    [data-testid="stDownloadButton"] button span {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    .stDownloadButton button:hover p,
    [data-testid="stDownloadButton"] button:hover p,
    .stDownloadButton button:hover span,
    [data-testid="stDownloadButton"] button:hover span {
        color: #ffffff !important;
    }
    
    /* Fix all button text visibility on hover */
    button:hover p,
    button:hover span,
    .stButton button:hover p,
    .stButton button:hover span {
        color: inherit !important;
    }
    
    /* CRITICAL: Ensure download button inner elements get white text */
    .stDownloadButton button *,
    [data-testid="stDownloadButton"] button * {
        color: #ffffff !important;
    }
    
    .stDownloadButton button:hover *,
    [data-testid="stDownloadButton"] button:hover * {
        color: #ffffff !important;
    }
    
    .block-container {
        padding-top: 4rem;
        margin-top: 20px;
    }

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

    .live-pill strong {
        color: #1e3a5f;
    }

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
        background: linear-gradient(180deg, #0f172a 0%, #1e3a5f 40%, #2c5282 100%) !important;
        width: 320px !important;
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.15) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    /* Sidebar collapsed state */
    section[data-testid="stSidebar"][aria-expanded="false"] {
        transform: translateX(-100%) !important;
        width: 0 !important;
        min-width: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
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
    
    /* === APP HEADER STYLING === */
    header[data-testid="stHeader"] {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%) !important;
        backdrop-filter: blur(10px) !important;
        border-bottom: 1px solid rgba(59, 130, 246, 0.3) !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Toolbar buttons - HIGHLY VISIBLE */
    [data-testid="stToolbar"] button,
    [data-testid="stToolbarActions"] button,
    header[data-testid="stHeader"] button {
        background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%) !important;
        border: 2px solid #60a5fa !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        transition: all 0.3s ease !important;
        padding: 8px 12px !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4) !important;
    }
    
    [data-testid="stToolbar"] button:hover,
    [data-testid="stToolbarActions"] button:hover,
    header[data-testid="stHeader"] button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%) !important;
        border-color: #93c5fd !important;
        transform: scale(1.1) translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.5) !important;
    }
    
    /* Main menu button */
    [data-testid="stMainMenu"] button {
        background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%) !important;
        border: 2px solid #60a5fa !important;
        border-radius: 10px !important;
        padding: 8px !important;
    }
    
    [data-testid="stMainMenu"] svg {
        fill: #ffffff !important;
    }
    
    /* Share button and other toolbar text */
    [data-testid="stToolbarActionButtonLabel"] {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* All header icons/svgs */
    header[data-testid="stHeader"] svg {
        fill: #ffffff !important;
        color: #ffffff !important;
    }
    
    /* Expand sidebar button styling */
    [data-testid="stExpandSidebarButton"],
    button[data-testid="stExpandSidebarButton"] {
        background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%) !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stExpandSidebarButton"]:hover {
        transform: scale(1.1) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.5) !important;
    }
    
    [data-testid="stExpandSidebarButton"] span,
    [data-testid="stExpandSidebarButton"] [data-testid="stIconMaterial"] {
        color: #ffffff !important;
        font-size: 20px !important;
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
        background: white !important;
    }
    
    /* Force white background on all Plotly elements */
    .js-plotly-plot .plotly,
    .js-plotly-plot .plot-container,
    .js-plotly-plot .svg-container,
    .js-plotly-plot .main-svg,
    .js-plotly-plot .bglayer,
    .js-plotly-plot .bglayer rect,
    .js-plotly-plot .bg {
        background: #ffffff !important;
        fill: #ffffff !important;
    }
    
    /* Force dark text on Plotly axis labels */
    .js-plotly-plot .xtick text,
    .js-plotly-plot .ytick text,
    .js-plotly-plot .gtitle,
    .js-plotly-plot .g-xtitle text,
    .js-plotly-plot .g-ytitle text,
    .js-plotly-plot text {
        fill: #1e3a5f !important;
    }
    
    /* Plotly gridlines */
    .js-plotly-plot .gridlayer path,
    .js-plotly-plot .zerolinelayer path {
        stroke: rgba(59, 130, 246, 0.1) !important;
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
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
            transform: scale(1);
        }
        50% {
            opacity: 0.5;
            transform: scale(1.2);
        }
    }

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
    
    /* Sidebar section divider */
    .sidebar-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        margin: 20px 0;
    }
    
    /* Sidebar filter section */
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
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    .filter-section-title i {
        font-size: 0.7rem;
    }
    
    /* Sidebar info box styling */
    .sidebar-info {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(96, 165, 250, 0.1) 100%) !important;
        color: rgba(255, 255, 255, 0.9) !important;
        font-size: 0.8rem !important;
        padding: 15px !important;
        margin-top: 20px !important;
        border-radius: 12px !important;
        border: 1px solid rgba(96, 165, 250, 0.3) !important;
        text-align: left !important;
    }
    
    .sidebar-info p {
        margin: 8px 0 !important;
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
    }
    
    .sidebar-info strong {
        color: #60a5fa !important;
    }
    
    /* Sidebar reset button */
    section[data-testid="stSidebar"] .stButton button {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 20px !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3) !important;
        margin-top: 10px !important;
    }
    
    section[data-testid="stSidebar"] .stButton button:hover {
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(239, 68, 68, 0.4) !important;
    }
    
    section[data-testid="stSidebar"] .stButton button:active {
        transform: translateY(0) !important;
    }
    
    /* Download button styling - Main content (Blue theme) */
    .main .stDownloadButton button {
        background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%) !important;
        color: #ffffff !important;
        border: 2px solid #60a5fa !important;
        border-radius: 12px !important;
        padding: 14px 22px !important;
        font-weight: 700 !important;
        letter-spacing: 0.2px !important;
        font-size: 0.92rem !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease, border-color 0.2s ease !important;
        box-shadow: 0 6px 18px rgba(59, 130, 246, 0.35) !important;
    }
    
    .main .stDownloadButton button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%) !important;
        border-color: #93c5fd !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 28px rgba(59, 130, 246, 0.45) !important;
    }
    
    .main .stDownloadButton button:active {
        transform: translateY(0) scale(0.98) !important;
        box-shadow: 0 6px 18px rgba(59, 130, 246, 0.35) !important;
    }
    
    .main .stDownloadButton button:focus {
        outline: none !important;
        box-shadow: 0 0 0 4px rgba(147, 197, 253, 0.4) !important;
    }
    
    /* Disabled state */
    .main .stDownloadButton button:disabled,
    .main .stDownloadButton button[disabled] {
        background: linear-gradient(135deg, #cbd5e1 0%, #e2e8f0 100%) !important;
        color: #1f2937 !important;
        border: 2px solid #cbd5e1 !important;
        box-shadow: none !important;
        cursor: not-allowed !important;
        opacity: 0.9 !important;
    }
    
    /* Insight cards */
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
        display: flex;
        flex-direction: column;
        gap: 8px;
        min-height: 130px;
        width: 100%;
        box-sizing: border-box;
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
        margin: 0;
        display: flex;
        align-items: center;
        gap: 6px;
        font-weight: 600;
    }

    .insight-value {
        color: #0f172a !important;
        font-size: 1.4rem;
        font-weight: 800;
        margin: 0;
        line-height: 1.2;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
    }

    .insight-sub {
        font-size: 0.95rem;
        font-weight: 600;
        margin: 0;
    }

    .insight-card--category {
        border-left-color: #3b82f6;
        background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%);
    }

    .insight-card--category .insight-label i {
        color: #f59e0b;
    }

    .insight-card--category .insight-sub {
        color: #3b82f6;
    }

    .insight-card--region {
        border-left-color: #10b981;
        background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
    }

    .insight-card--region .insight-label i {
        color: #10b981;
    }

    .insight-card--region .insight-sub {
        color: #10b981;
    }

    .insight-card--segment {
        border-left-color: #ef4444;
        background: linear-gradient(135deg, #ffffff 0%, #fef3f2 100%);
    }

    .insight-card--segment .insight-label i {
        color: #ef4444;
    }

    .insight-card--segment .insight-sub {
        color: #ef4444;
    }

    .insight-card--month {
        border-left-color: #f59e0b;
        background: linear-gradient(135deg, #ffffff 0%, #fefce8 100%);
    }

    .insight-card--month .insight-label i {
        color: #f59e0b;
    }

    .insight-card--month .insight-sub {
        color: #f59e0b;
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
st.sidebar.markdown('''
<div class="sidebar-header">
    <i class="fas fa-sliders-h"></i> Control Panel
</div>
''', unsafe_allow_html=True)

# === TIME FILTERS SECTION ===
st.sidebar.markdown('''
<div class="filter-section">
    <p class="filter-section-title"><i class="fas fa-clock"></i> Time Filters</p>
</div>
''', unsafe_allow_html=True)

# Filter tahun
st.sidebar.markdown('<p class="filter-label"><i class="fas fa-calendar-alt"></i> Tahun</p>', unsafe_allow_html=True)
years = sorted(df['order_year'].dropna().unique())
selected_years = st.sidebar.multiselect(
    "Tahun",
    options=years,
    default=years,
    label_visibility="collapsed"
)

# Divider
st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

# === GEOGRAPHIC FILTERS SECTION ===
st.sidebar.markdown('''
<div class="filter-section">
    <p class="filter-section-title"><i class="fas fa-map-marked-alt"></i> Geographic Filters</p>
</div>
''', unsafe_allow_html=True)

# Filter region
st.sidebar.markdown('<p class="filter-label"><i class="fas fa-globe-americas"></i> Region</p>', unsafe_allow_html=True)
regions = sorted(df['region'].dropna().unique())
selected_regions = st.sidebar.multiselect(
    "Region",
    options=regions,
    default=regions,
    label_visibility="collapsed"
)

# Filter state
st.sidebar.markdown('<p class="filter-label"><i class="fas fa-map"></i> State</p>', unsafe_allow_html=True)
states = sorted(df['state'].dropna().unique())
selected_states = st.sidebar.multiselect(
    "State",
    options=states,
    default=states,
    label_visibility="collapsed"
)

# Divider
st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

# === CUSTOMER FILTERS SECTION ===
st.sidebar.markdown('''
<div class="filter-section">
    <p class="filter-section-title"><i class="fas fa-user-friends"></i> Customer Filters</p>
</div>
''', unsafe_allow_html=True)

# Filter segment
st.sidebar.markdown('<p class="filter-label"><i class="fas fa-users"></i> Segment</p>', unsafe_allow_html=True)
segments = sorted(df['segment'].dropna().unique())
selected_segments = st.sidebar.multiselect(
    "Segment",
    options=segments,
    default=segments,
    label_visibility="collapsed"
)

# Divider
st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

# === PRODUCT FILTERS SECTION ===
st.sidebar.markdown('''
<div class="filter-section">
    <p class="filter-section-title"><i class="fas fa-box-open"></i> Product Filters</p>
</div>
''', unsafe_allow_html=True)

# Filter category
st.sidebar.markdown('<p class="filter-label"><i class="fas fa-layer-group"></i> Category</p>', unsafe_allow_html=True)
categories = sorted(df['category'].dropna().unique())
selected_categories = st.sidebar.multiselect(
    "Category",
    options=categories,
    default=categories,
    label_visibility="collapsed"
)

# Filter sub-category
st.sidebar.markdown('<p class="filter-label"><i class="fas fa-tags"></i> Sub-Category</p>', unsafe_allow_html=True)
subcategories = sorted(df['sub_category'].dropna().unique())
selected_subcategories = st.sidebar.multiselect(
    "Sub-Category",
    options=subcategories,
    default=subcategories,
    label_visibility="collapsed"
)

# Search product
st.sidebar.markdown('<p class="filter-label"><i class="fas fa-search"></i> Cari Produk</p>', unsafe_allow_html=True)
product_search = st.sidebar.text_input(
    "Search",
    placeholder="Ketik nama produk...",
    label_visibility="collapsed"
)

# Divider
st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

# Sidebar stats info
st.sidebar.markdown(f'''
<div class="sidebar-info">
    <p><i class="fas fa-database"></i> Total Records: <strong>{len(df):,}</strong></p>
    <p><i class="fas fa-chart-pie"></i> Categories: <strong>{len(categories)}</strong></p>
    <p><i class="fas fa-globe"></i> Regions: <strong>{len(regions)}</strong></p>
</div>
''', unsafe_allow_html=True)

# Quick reset button
if st.sidebar.button("Reset All Filters", use_container_width=True):
    st.rerun()

# Apply filters
filtered_df = df[
    (df['order_year'].isin(selected_years)) &
    (df['region'].isin(selected_regions)) &
    (df['state'].isin(selected_states)) &
    (df['segment'].isin(selected_segments)) &
    (df['category'].isin(selected_categories)) &
    (df['sub_category'].isin(selected_subcategories))
]

# Apply product search filter
if product_search:
    filtered_df = filtered_df[filtered_df['product_name'].str.contains(product_search, case=False, na=False)]

# KPI Metrics Row
st.markdown('<p class="section-header"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" style="vertical-align: middle; margin-right: 8px;"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 3v11.25A2.25 2.25 0 0 0 6 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0 1 18 16.5h-2.25m-7.5 0h7.5m-7.5 0-1 3m8.5-3 1 3m0 0 .5 1.5m-.5-1.5h-9.5m0 0-.5 1.5m.75-9 3-3 2.148 2.148A12.061 12.061 0 0 1 16.5 7.605" /></svg> Key Performance Indicators</p>', unsafe_allow_html=True)

# Quick Stats Row dengan Live Indicator
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

# Calculate all KPI values
total_sales = filtered_df['sales'].sum()
avg_order = filtered_df['sales'].mean() if len(filtered_df) > 0 else 0
total_customers = filtered_df['sk_customer'].nunique()
total_products = filtered_df['sk_product'].nunique()
total_orders = filtered_df['order_id'].nunique()
total_categories = filtered_df['category'].nunique()
total_subcategories = filtered_df['sub_category'].nunique()
total_states = filtered_df['state'].nunique()
total_regions = filtered_df['region'].nunique()

# Row 1: Main KPIs dengan SVG Icons
kpi_row1_html = f'''
<div class="kpi-grid">
    <div class="kpi-card kpi-card--sales">
        <div class="kpi-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="#ffffff">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v12m-3-2.818.879.659c1.171.879 3.07.879 4.242 0 1.172-.879 1.172-2.303 0-3.182C13.536 12.219 12.768 12 12 12c-.725 0-1.45-.22-2.003-.659-1.106-.879-1.106-2.303 0-3.182s2.9-.879 4.006 0l.415.33M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
            </svg>
        </div>
        <div class="kpi-content">
            <span class="kpi-label">Total Sales</span>
            <span class="kpi-value">${total_sales:,.2f}</span>
            <span class="kpi-delta">{len(filtered_df):,} transaksi</span>
        </div>
    </div>
    <div class="kpi-card kpi-card--avg">
        <div class="kpi-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="#ffffff">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 0 1 3 19.875v-6.75ZM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V8.625ZM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V4.125Z" />
            </svg>
        </div>
        <div class="kpi-content">
            <span class="kpi-label">Rata-rata Order</span>
            <span class="kpi-value">${avg_order:,.2f}</span>
            <span class="kpi-delta">per transaksi</span>
        </div>
    </div>
    <div class="kpi-card kpi-card--customers">
        <div class="kpi-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="#ffffff">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15 19.128a9.38 9.38 0 0 0 2.625.372 9.337 9.337 0 0 0 4.121-.952 4.125 4.125 0 0 0-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 0 1 8.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0 1 11.964-3.07M12 6.375a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0Zm8.25 2.25a2.625 2.625 0 1 1-5.25 0 2.625 2.625 0 0 1 5.25 0Z" />
            </svg>
        </div>
        <div class="kpi-content">
            <span class="kpi-label">Total Customers</span>
            <span class="kpi-value">{total_customers:,}</span>
            <span class="kpi-delta">unique customers</span>
        </div>
    </div>
    <div class="kpi-card kpi-card--products">
        <div class="kpi-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="#ffffff">
                <path stroke-linecap="round" stroke-linejoin="round" d="m21 7.5-9-5.25L3 7.5m18 0-9 5.25m9-5.25v9l-9 5.25M3 7.5l9 5.25M3 7.5v9l9 5.25m0-9v9" />
            </svg>
        </div>
        <div class="kpi-content">
            <span class="kpi-label">Total Products</span>
            <span class="kpi-value">{total_products:,}</span>
            <span class="kpi-delta">unique products</span>
        </div>
    </div>
    <div class="kpi-card kpi-card--orders">
        <div class="kpi-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="#ffffff">
                <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 0 0-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 0 0-16.536-1.84M7.5 14.25 5.106 5.272M6 20.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm12.75 0a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z" />
            </svg>
        </div>
        <div class="kpi-content">
            <span class="kpi-label">Total Orders</span>
            <span class="kpi-value">{total_orders:,}</span>
            <span class="kpi-delta">unique orders</span>
        </div>
    </div>
</div>
'''
st.markdown(kpi_row1_html, unsafe_allow_html=True)

# Row 2: Additional KPIs dengan SVG Icons
kpi_row2_html = f'''
<div class="kpi-grid kpi-grid--4cols">
    <div class="kpi-card kpi-card--categories">
        <div class="kpi-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="#ffffff">
                <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12.75V12A2.25 2.25 0 0 1 4.5 9.75h15A2.25 2.25 0 0 1 21.75 12v.75m-8.69-6.44-2.12-2.12a1.5 1.5 0 0 0-1.061-.44H4.5A2.25 2.25 0 0 0 2.25 6v12a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18V9a2.25 2.25 0 0 0-2.25-2.25h-5.379a1.5 1.5 0 0 1-1.06-.44Z" />
            </svg>
        </div>
        <div class="kpi-content">
            <span class="kpi-label">Total Categories</span>
            <span class="kpi-value">{total_categories:,}</span>
            <span class="kpi-delta">kategori produk</span>
        </div>
    </div>
    <div class="kpi-card kpi-card--subcategories">
        <div class="kpi-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="#ffffff">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9.568 3H5.25A2.25 2.25 0 0 0 3 5.25v4.318c0 .597.237 1.17.659 1.591l9.581 9.581c.699.699 1.78.872 2.607.33a18.095 18.095 0 0 0 5.223-5.223c.542-.827.369-1.908-.33-2.607L11.16 3.66A2.25 2.25 0 0 0 9.568 3Z" />
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 6h.008v.008H6V6Z" />
            </svg>
        </div>
        <div class="kpi-content">
            <span class="kpi-label">Total Sub-Categories</span>
            <span class="kpi-value">{total_subcategories:,}</span>
            <span class="kpi-delta">sub-kategori</span>
        </div>
    </div>
    <div class="kpi-card kpi-card--states">
        <div class="kpi-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="#ffffff">
                <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 21h19.5m-18-18v18m10.5-18v18m6-13.5V21M6.75 6.75h.75m-.75 3h.75m-.75 3h.75m3-6h.75m-.75 3h.75m-.75 3h.75M6.75 21v-3.375c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21M3 3h12m-.75 4.5H21m-3.75 3.75h.008v.008h-.008v-.008Zm0 3h.008v.008h-.008v-.008Zm0 3h.008v.008h-.008v-.008Z" />
            </svg>
        </div>
        <div class="kpi-content">
            <span class="kpi-label">Total States</span>
            <span class="kpi-value">{total_states:,}</span>
            <span class="kpi-delta">negara bagian</span>
        </div>
    </div>
    <div class="kpi-card kpi-card--regions">
        <div class="kpi-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="#ffffff">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 21a9.004 9.004 0 0 0 8.716-6.747M12 21a9.004 9.004 0 0 1-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 0 1 7.843 4.582M12 3a8.997 8.997 0 0 0-7.843 4.582m15.686 0A11.953 11.953 0 0 1 12 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0 1 21 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0 1 12 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 0 1 3 12c0-1.605.42-3.113 1.157-4.418" />
            </svg>
        </div>
        <div class="kpi-content">
            <span class="kpi-label">Total Regions</span>
            <span class="kpi-value">{total_regions:,}</span>
            <span class="kpi-delta">wilayah</span>
        </div>
    </div>
</div>
'''
st.markdown(kpi_row2_html, unsafe_allow_html=True)

st.markdown("---")

# === QUICK INSIGHTS SECTION ===
st.markdown('<p class="section-header"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" style="vertical-align: middle; margin-right: 8px;"><path stroke-linecap="round" stroke-linejoin="round" d="M12 18v-5.25m0 0a6.01 6.01 0 0 0 1.5-.189m-1.5.189a6.01 6.01 0 0 1-1.5-.189m3.75 7.478a12.06 12.06 0 0 1-4.5 0m3.75 2.383a14.406 14.406 0 0 1-3 0M14.25 18v-.192c0-.983.658-1.823 1.508-2.316a7.5 7.5 0 1 0-7.517 0c.85.493 1.509 1.333 1.509 2.316V18" /></svg> Quick Insights</p>', unsafe_allow_html=True)

# Calculate insights
top_category = filtered_df.groupby('category')['sales'].sum().idxmax() if len(filtered_df) > 0 else "N/A"
top_category_sales = filtered_df.groupby('category')['sales'].sum().max() if len(filtered_df) > 0 else 0
top_region = filtered_df.groupby('region')['sales'].sum().idxmax() if len(filtered_df) > 0 else "N/A"
top_region_sales = filtered_df.groupby('region')['sales'].sum().max() if len(filtered_df) > 0 else 0
top_segment = filtered_df.groupby('segment')['sales'].sum().idxmax() if len(filtered_df) > 0 else "N/A"
best_month = filtered_df.groupby('order_month_name')['sales'].sum().idxmax() if len(filtered_df) > 0 else "N/A"

insights_html = f'''
<div class="insight-grid">
    <div class="insight-card insight-card--category">
        <p class="insight-label">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M16.5 18.75h-9m9 0a3 3 0 0 1 3 3h-15a3 3 0 0 1 3-3m9 0v-3.375c0-.621-.503-1.125-1.125-1.125h-.871M7.5 18.75v-3.375c0-.621.504-1.125 1.125-1.125h.872m5.007 0H9.497m5.007 0a7.454 7.454 0 0 1-.982-3.172M9.497 14.25a7.454 7.454 0 0 0 .981-3.172M5.25 4.236c-.982.143-1.954.317-2.916.52A6.003 6.003 0 0 0 7.73 9.728M5.25 4.236V4.5c0 2.108.966 3.99 2.48 5.228M5.25 4.236V2.721C7.456 2.41 9.71 2.25 12 2.25c2.291 0 4.545.16 6.75.47v1.516M7.73 9.728a6.726 6.726 0 0 0 2.748 1.35m8.272-6.842V4.5c0 2.108-.966 3.99-2.48 5.228m2.48-5.492a46.32 46.32 0 0 1 2.916.52 6.003 6.003 0 0 1-5.395 4.972m0 0a6.726 6.726 0 0 1-2.749 1.35m0 0a6.772 6.772 0 0 1-3.044 0" /></svg>
            Top Category
        </p>
        <h3 class="insight-value">{top_category}</h3>
        <p class="insight-sub">${top_category_sales:,.0f}</p>
    </div>
    <div class="insight-card insight-card--region">
        <p class="insight-label">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" /><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1 1 15 0Z" /></svg>
            Top Region
        </p>
        <h3 class="insight-value">{top_region}</h3>
        <p class="insight-sub">${top_region_sales:,.0f}</p>
    </div>
    <div class="insight-card insight-card--segment">
        <p class="insight-label">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M18 18.72a9.094 9.094 0 0 0 3.741-.479 3 3 0 0 0-4.682-2.72m.94 3.198.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0 1 12 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 0 1 6 18.719m12 0a5.971 5.971 0 0 0-.941-3.197m0 0A5.995 5.995 0 0 0 12 12.75a5.995 5.995 0 0 0-5.058 2.772m0 0a3 3 0 0 0-4.681 2.72 8.986 8.986 0 0 0 3.74.477m.94-3.197a5.971 5.971 0 0 0-.94 3.197M15 6.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Zm6 3a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Zm-13.5 0a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Z" /></svg>
            Top Segment
        </p>
        <h3 class="insight-value">{top_segment}</h3>
        <p class="insight-sub">Best Performer</p>
    </div>
    <div class="insight-card insight-card--month">
        <p class="insight-label">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5m-9-6h.008v.008H12v-.008ZM12 15h.008v.008H12V15Zm0 2.25h.008v.008H12v-.008ZM9.75 15h.008v.008H9.75V15Zm0 2.25h.008v.008H9.75v-.008ZM7.5 15h.008v.008H7.5V15Zm0 2.25h.008v.008H7.5v-.008Zm6.75-4.5h.008v.008h-.008v-.008Zm0 2.25h.008v.008h-.008V15Zm0 2.25h.008v.008h-.008v-.008Zm2.25-4.5h.008v.008H16.5v-.008Zm0 2.25h.008v.008H16.5V15Z" /></svg>
            Peak Month
        </p>
        <h3 class="insight-value">{best_month}</h3>
        <p class="insight-sub">Highest Sales</p>
    </div>
</div>
'''
st.markdown(insights_html, unsafe_allow_html=True)

st.markdown("---")

# === DATA SUMMARY VISUALIZATION ===
st.markdown('<p class="section-header"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" style="vertical-align: middle; margin-right: 8px;"><path stroke-linecap="round" stroke-linejoin="round" d="M10.5 6a7.5 7.5 0 1 0 7.5 7.5h-7.5V6Z" /><path stroke-linecap="round" stroke-linejoin="round" d="M13.5 10.5H21A7.5 7.5 0 0 0 13.5 3v7.5Z" /></svg> Data Distribution Overview</p>', unsafe_allow_html=True)

summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)

with summary_col1:
    # Category distribution
    category_counts = filtered_df.groupby('category').size().reset_index(name='count')
    fig_cat_dist = px.pie(
        category_counts,
        values='count',
        names='category',
        title='Category Distribution',
        color_discrete_sequence=['#dc2626', '#2563eb', '#16a34a'],
        hole=0.4
    )
    fig_cat_dist.update_layout(
        paper_bgcolor='#ffffff',
        plot_bgcolor='#ffffff',
        font=dict(color='#1e3a5f', family='Poppins', size=10),
        title=dict(font=dict(size=12, color='#1e3a5f'), x=0.5, xanchor='center'),
        showlegend=True,
        legend=dict(orientation='h', yanchor='bottom', y=-0.3, xanchor='center', x=0.5, font=dict(size=8, color='#1e3a5f')),
        margin=dict(l=5, r=5, t=35, b=45),
        height=220
    )
    fig_cat_dist.update_traces(textposition='inside', textinfo='percent', textfont=dict(size=9, color='white'), marker=dict(line=dict(color='#000000', width=2)))
    st.plotly_chart(fig_cat_dist, use_container_width=True)

with summary_col2:
    # Segment distribution
    segment_counts = filtered_df.groupby('segment').size().reset_index(name='count')
    fig_seg_dist = px.pie(
        segment_counts,
        values='count',
        names='segment',
        title='Segment Distribution',
        color_discrete_sequence=['#7c3aed', '#f59e0b', '#06b6d4'],
        hole=0.4
    )
    fig_seg_dist.update_layout(
        paper_bgcolor='#ffffff',
        plot_bgcolor='#ffffff',
        font=dict(color='#1e3a5f', family='Poppins', size=10),
        title=dict(font=dict(size=12, color='#1e3a5f'), x=0.5, xanchor='center'),
        showlegend=True,
        legend=dict(orientation='h', yanchor='bottom', y=-0.3, xanchor='center', x=0.5, font=dict(size=8, color='#1e3a5f')),
        margin=dict(l=5, r=5, t=35, b=45),
        height=220
    )
    fig_seg_dist.update_traces(textposition='inside', textinfo='percent', textfont=dict(size=9, color='white'), marker=dict(line=dict(color='#000000', width=2)))
    st.plotly_chart(fig_seg_dist, use_container_width=True)

with summary_col3:
    # Region distribution
    region_counts = filtered_df.groupby('region').size().reset_index(name='count')
    fig_reg_dist = px.pie(
        region_counts,
        values='count',
        names='region',
        title='Region Distribution',
        color_discrete_sequence=['#dc2626', '#2563eb', '#16a34a', '#f59e0b'],
        hole=0.4
    )
    fig_reg_dist.update_layout(
        paper_bgcolor='#ffffff',
        plot_bgcolor='#ffffff',
        font=dict(color='#1e3a5f', family='Poppins', size=10),
        title=dict(font=dict(size=12, color='#1e3a5f'), x=0.5, xanchor='center'),
        showlegend=True,
        legend=dict(orientation='h', yanchor='bottom', y=-0.3, xanchor='center', x=0.5, font=dict(size=8, color='#1e3a5f')),
        margin=dict(l=5, r=5, t=35, b=45),
        height=220
    )
    fig_reg_dist.update_traces(textposition='inside', textinfo='percent', textfont=dict(size=9, color='white'), marker=dict(line=dict(color='#000000', width=2)))
    st.plotly_chart(fig_reg_dist, use_container_width=True)

with summary_col4:
    # Top 5 Sub-Categories by count
    subcat_counts = filtered_df.groupby('sub_category').size().reset_index(name='count').sort_values('count', ascending=False).head(5)
    fig_subcat = px.bar(
        subcat_counts,
        x='count',
        y='sub_category',
        orientation='h',
        title='Top 5 Sub-Categories',
        color='count',
        color_continuous_scale='Blues'
    )
    fig_subcat.update_layout(
        paper_bgcolor='#ffffff',
        plot_bgcolor='#ffffff',
        font=dict(color='#1e3a5f', family='Poppins', size=10),
        title=dict(font=dict(size=12, color='#1e3a5f')),
        showlegend=False,
        coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=40, b=10),
        height=200,
        xaxis=dict(title='', tickfont=dict(size=9, color='#1e3a5f'), gridcolor='rgba(59, 130, 246, 0.1)'),
        yaxis=dict(title='', tickfont=dict(size=9, color='#1e3a5f'), categoryorder='total ascending', gridcolor='rgba(59, 130, 246, 0.1)')
    )
    fig_subcat.update_traces(marker=dict(line=dict(color='#1e3a5f', width=1)))
    st.plotly_chart(fig_subcat, use_container_width=True)

st.markdown("---")

# Tabs untuk berbagai visualisasi
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Overview", 
    "Sales Trend", 
    "Regional Analysis", 
    "Product Analysis",
    "Customer Analysis",
    "Forecasting"
])

# Warna untuk chart (Blue theme)
blue_colors = ['#dc2626', '#2563eb', '#16a34a', '#f59e0b', '#7c3aed', '#06b6d4']
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
            paper_bgcolor='#ffffff',
            plot_bgcolor='#ffffff',
            font=dict(color='#1e3a5f', family='Poppins', size=11),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5,
                font=dict(color='#1e3a5f', size=10)
            ),
            margin=dict(l=20, r=20, t=20, b=60),
            height=350
        )
        fig_category.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont=dict(size=10, color='white'),
            hovertemplate='<b>%{label}</b><br>Sales: $%{value:,.2f}<br>Percentage: %{percent}<extra></extra>',
            marker=dict(line=dict(color='#000000', width=2))
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
            color_discrete_sequence=['#7c3aed', '#f59e0b', '#06b6d4'],
            hole=0.45
        )
        fig_segment.update_layout(
            paper_bgcolor='#ffffff',
            plot_bgcolor='#ffffff',
            font=dict(color='#1e3a5f', family='Poppins', size=11),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5,
                font=dict(color='#1e3a5f', size=10)
            ),
            margin=dict(l=20, r=20, t=20, b=60),
            height=350
        )
        fig_segment.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont=dict(size=10, color='white'),
            hovertemplate='<b>%{label}</b><br>Sales: $%{value:,.2f}<br>Percentage: %{percent}<extra></extra>',
            marker=dict(line=dict(color='#000000', width=2))
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
        color_continuous_scale='Blues',
        text=region_sales['sales'].apply(lambda x: f'${x:,.0f}')
    )
    fig_region.update_layout(
        paper_bgcolor='#ffffff',
        plot_bgcolor='#ffffff',
        font=dict(color='#1e3a5f', family='Poppins', size=11),
        xaxis=dict(
            gridcolor='rgba(59, 130, 246, 0.15)',
            title='Total Sales',
            title_font=dict(color='#1e3a5f', size=12),
            tickfont=dict(color='#4a6fa5', size=10),
            automargin=True
        ),
        yaxis=dict(
            gridcolor='rgba(59, 130, 246, 0.15)',
            title='',
            title_font=dict(color='#1e3a5f', size=12),
            tickfont=dict(color='#1e3a5f', size=11),
            automargin=True
        ),
        showlegend=False,
        coloraxis_showscale=False,
        height=320,
        margin=dict(l=10, r=30, t=20, b=40)
    )
    fig_region.update_traces(
        textposition='inside',
        textfont=dict(color='white', size=11),
        hovertemplate='<b>%{y}</b><br>Sales: $%{x:,.2f}<extra></extra>'
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
        paper_bgcolor='#ffffff',
        plot_bgcolor='#ffffff',
        font=dict(color='#1e3a5f', family='Poppins', size=11),
        xaxis=dict(
            gridcolor='rgba(59, 130, 246, 0.15)',
            title='Bulan',
            title_font=dict(color='#1e3a5f', size=12),
            tickfont=dict(color='#4a6fa5', size=9),
            tickangle=-45,
            automargin=True
        ),
        yaxis=dict(
            gridcolor='rgba(59, 130, 246, 0.15)',
            title='Total Sales',
            title_font=dict(color='#1e3a5f', size=12),
            tickfont=dict(color='#4a6fa5', size=10),
            automargin=True
        ),
        height=400,
        margin=dict(l=10, r=20, t=20, b=80)
    )
    fig_trend.update_traces(
        line=dict(width=3, color='#3b82f6'),
        marker=dict(size=8, color='#1e3a5f', line=dict(width=2, color='#ffffff')),
        hovertemplate='<b>%{x}</b><br>Sales: $%{y:,.2f}<extra></extra>'
    )
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
            paper_bgcolor='#ffffff',
            plot_bgcolor='#ffffff',
            font=dict(color='#1e3a5f', family='Poppins', size=11),
            xaxis=dict(
                gridcolor='rgba(59, 130, 246, 0.15)',
                title='Quarter',
                title_font=dict(color='#1e3a5f', size=12),
                tickfont=dict(color='#4a6fa5', size=11),
                automargin=True
            ),
            yaxis=dict(
                gridcolor='rgba(59, 130, 246, 0.15)',
                title='Total Sales',
                title_font=dict(color='#1e3a5f', size=12),
                tickfont=dict(color='#4a6fa5', size=10),
                automargin=True
            ),
            legend_title="Tahun",
            legend=dict(font=dict(color='#1e3a5f', size=10), orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
            height=380,
            margin=dict(l=10, r=10, t=40, b=40)
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
            paper_bgcolor='#ffffff',
            plot_bgcolor='#ffffff',
            font=dict(color='#1e3a5f', family='Poppins', size=11),
            xaxis=dict(
                gridcolor='rgba(59, 130, 246, 0.15)',
                title='Tahun',
                title_font=dict(color='#1e3a5f', size=12),
                tickfont=dict(color='#4a6fa5', size=11),
                automargin=True
            ),
            yaxis=dict(
                gridcolor='rgba(59, 130, 246, 0.15)',
                title='Total Sales',
                title_font=dict(color='#1e3a5f', size=12),
                tickfont=dict(color='#4a6fa5', size=10),
                automargin=True
            ),
            showlegend=False,
            coloraxis_showscale=False,
            height=380,
            margin=dict(l=10, r=10, t=40, b=40)
        )
        fig_yearly.update_traces(
            texttemplate='$%{text:,.0f}',
            textposition='outside',
            textfont=dict(color='#1e3a5f', size=10)
        )
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
        color_continuous_scale='Blues',
        text=day_sales['sales'].apply(lambda x: f'${x:,.0f}')
    )
    fig_day.update_layout(
        paper_bgcolor='#ffffff',
        plot_bgcolor='#ffffff',
        font=dict(color='#1e3a5f', family='Poppins', size=11),
        xaxis=dict(
            gridcolor='rgba(59, 130, 246, 0.15)',
            title='Hari',
            title_font=dict(color='#1e3a5f', size=12),
            tickfont=dict(color='#4a6fa5', size=10),
            tickangle=-30,
            automargin=True
        ),
        yaxis=dict(
            gridcolor='rgba(59, 130, 246, 0.15)',
            title='Total Sales',
            title_font=dict(color='#1e3a5f', size=12),
            tickfont=dict(color='#4a6fa5', size=10),
            automargin=True
        ),
        coloraxis_showscale=False,
        height=350,
        margin=dict(l=10, r=20, t=20, b=60)
    )
    fig_day.update_traces(
        textposition='outside',
        textfont=dict(color='#1e3a5f', size=9),
        hovertemplate='<b>%{x}</b><br>Sales: $%{y:,.2f}<extra></extra>'
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
            color_continuous_scale='Blues',
            text=state_sales['sales'].apply(lambda x: f'${x:,.0f}')
        )
        fig_states.update_layout(
            paper_bgcolor='#ffffff',
            plot_bgcolor='#ffffff',
            font=dict(color='#1e3a5f', family='Poppins', size=11),
            xaxis=dict(
                gridcolor='rgba(59, 130, 246, 0.15)',
                title='Total Sales',
                title_font=dict(color='#1e3a5f', size=12),
                tickfont=dict(color='#4a6fa5', size=10),
                automargin=True
            ),
            yaxis=dict(
                gridcolor='rgba(59, 130, 246, 0.15)',
                title='',
                categoryorder='total ascending',
                title_font=dict(color='#1e3a5f', size=12),
                tickfont=dict(color='#1e3a5f', size=10),
                automargin=True
            ),
            coloraxis_showscale=False,
            height=520,
            margin=dict(l=10, r=30, t=20, b=40)
        )
        fig_states.update_traces(
            textposition='inside',
            textfont=dict(color='white', size=9),
            hovertemplate='<b>%{y}</b><br>Sales: $%{x:,.2f}<extra></extra>'
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
            color_continuous_scale='Blues',
            text=subcat_sales['sales'].apply(lambda x: f'${x:,.0f}')
        )
        fig_subcat.update_layout(
            paper_bgcolor='#ffffff',
            plot_bgcolor='#ffffff',
            font=dict(color='#1e3a5f', family='Poppins', size=11),
            xaxis=dict(
                gridcolor='rgba(59, 130, 246, 0.15)',
                title='Total Sales',
                title_font=dict(color='#1e3a5f', size=12),
                tickfont=dict(color='#4a6fa5', size=10),
                automargin=True
            ),
            yaxis=dict(
                gridcolor='rgba(59, 130, 246, 0.15)',
                title='',
                categoryorder='total ascending',
                title_font=dict(color='#1e3a5f', size=12),
                tickfont=dict(color='#1e3a5f', size=10),
                automargin=True
            ),
            coloraxis_showscale=False,
            height=400,
            margin=dict(l=10, r=30, t=20, b=40)
        )
        fig_subcat.update_traces(
            textposition='inside',
            textfont=dict(color='white', size=9),
            hovertemplate='<b>%{y}</b><br>Sales: $%{x:,.2f}<extra></extra>'
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
            font=dict(color='#1e3a5f', family='Poppins', size=11),
            height=420,
            margin=dict(t=20, b=20, l=20, r=20),
            coloraxis_showscale=False,
            hoverlabel=dict(
                bgcolor='#1e3a5f',
                font_size=12,
                font_family='Poppins',
                font_color='white'
            )
        )
        fig_sunburst.update_traces(
            textfont=dict(color='#ffffff', size=10, family='Poppins'),
            hovertemplate='<b>%{label}</b><br>Sales: $%{value:,.2f}<extra></extra>',
            insidetextorientation='horizontal'
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
            color_discrete_sequence=blue_colors,
            text=top_customers['sales'].apply(lambda x: f'${x:,.0f}')
        )
        fig_customers.update_layout(
            paper_bgcolor='#ffffff',
            plot_bgcolor='#ffffff',
            font=dict(color='#1e3a5f', family='Poppins', size=11),
            xaxis=dict(
                gridcolor='rgba(59, 130, 246, 0.15)',
                title='Total Sales',
                title_font=dict(color='#1e3a5f', size=12),
                tickfont=dict(color='#4a6fa5', size=10),
                automargin=True
            ),
            yaxis=dict(
                gridcolor='rgba(59, 130, 246, 0.15)',
                title='',
                categoryorder='total ascending',
                title_font=dict(color='#1e3a5f', size=12),
                tickfont=dict(color='#1e3a5f', size=9),
                automargin=True
            ),
            legend_title="Segment",
            legend=dict(font=dict(color='#1e3a5f', size=9), orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
            height=420,
            margin=dict(l=10, r=30, t=40, b=40)
        )
        fig_customers.update_traces(
            textposition='inside',
            textfont=dict(color='white', size=8),
            hovertemplate='<b>%{y}</b><br>Sales: $%{x:,.2f}<extra></extra>'
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
            paper_bgcolor='#ffffff',
            plot_bgcolor='#ffffff',
            font=dict(color='#1e3a5f', family='Poppins', size=11),
            xaxis=dict(
                gridcolor='rgba(59, 130, 246, 0.15)',
                title='',
                title_font=dict(color='#1e3a5f', size=12),
                tickfont=dict(color='#4a6fa5', size=11),
                automargin=True
            ),
            yaxis=dict(
                gridcolor='rgba(59, 130, 246, 0.15)',
                title='Count',
                title_font=dict(color='#1e3a5f', size=12),
                tickfont=dict(color='#4a6fa5', size=10),
                automargin=True
            ),
            legend_title="Metric",
            legend=dict(font=dict(color='#1e3a5f', size=9), orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
            height=420,
            margin=dict(l=10, r=10, t=40, b=40)
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

# Tab 6: Forecasting
with tab6:
    st.markdown('<p class="section-header"><i class="fas fa-crystal-ball"></i> Sales Forecasting</p>', unsafe_allow_html=True)
    st.markdown('''
    <div style="background: linear-gradient(135deg, #dbeafe 0%, #eff6ff 100%); padding: 20px; border-radius: 14px; margin-bottom: 20px; border-left: 4px solid #3b82f6;">
        <p style="color: #1e3a5f; margin: 0; font-weight: 600;"><i class="fas fa-info-circle" style="color: #3b82f6;"></i> Metode: Linear Regression</p>
        <p style="color: #4a6fa5; margin: 5px 0 0 0; font-size: 0.9rem;">Prediksi didasarkan pada tren historis penjualan bulanan. Model menggunakan data historis untuk memproyeksikan penjualan di periode mendatang.</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Prepare data for forecasting
    monthly_forecast_data = filtered_df.groupby(['order_year', 'order_month_num'])['sales'].sum().reset_index()
    monthly_forecast_data['period'] = monthly_forecast_data['order_year'].astype(str) + '-' + monthly_forecast_data['order_month_num'].astype(str).str.zfill(2)
    monthly_forecast_data = monthly_forecast_data.sort_values('period').reset_index(drop=True)
    monthly_forecast_data['period_num'] = range(1, len(monthly_forecast_data) + 1)
    
    if len(monthly_forecast_data) >= 3:
        # Train simple linear regression
        X = monthly_forecast_data[['period_num']].values
        y = monthly_forecast_data['sales'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        # Predict historical + future
        historical_pred = model.predict(X)
        
        # Predict next 6 months
        future_periods = np.array([[i] for i in range(len(X) + 1, len(X) + 7)])
        future_pred = model.predict(future_periods)
        
        # Create future labels
        last_year = monthly_forecast_data['order_year'].iloc[-1]
        last_month = monthly_forecast_data['order_month_num'].iloc[-1]
        future_labels = []
        for i in range(1, 7):
            next_month = last_month + i
            next_year = last_year
            while next_month > 12:
                next_month -= 12
                next_year += 1
            future_labels.append(f"{next_year}-{str(next_month).zfill(2)}")
        
        # Create combined dataframe for visualization
        historical_df = pd.DataFrame({
            'period': monthly_forecast_data['period'],
            'actual': monthly_forecast_data['sales'],
            'predicted': historical_pred,
            'type': 'Historical'
        })
        
        future_df = pd.DataFrame({
            'period': future_labels,
            'actual': [None] * 6,
            'predicted': future_pred,
            'type': 'Forecast'
        })
        
        combined_df = pd.concat([historical_df, future_df], ignore_index=True)
        
        # Plot
        fig_forecast = go.Figure()
        
        # Actual sales line
        fig_forecast.add_trace(go.Scatter(
            x=historical_df['period'],
            y=historical_df['actual'],
            mode='lines+markers',
            name='Actual Sales',
            line=dict(color='#3b82f6', width=3),
            marker=dict(size=8, color='#1e3a5f', line=dict(width=2, color='white'))
        ))
        
        # Trend line (historical)
        fig_forecast.add_trace(go.Scatter(
            x=historical_df['period'],
            y=historical_df['predicted'],
            mode='lines',
            name='Trend Line',
            line=dict(color='#94a3b8', width=2, dash='dash')
        ))
        
        # Forecast line
        all_periods = list(historical_df['period']) + list(future_df['period'])
        all_forecast = list(historical_df['predicted']) + list(future_df['predicted'])
        
        fig_forecast.add_trace(go.Scatter(
            x=[historical_df['period'].iloc[-1]] + future_labels,
            y=[historical_df['predicted'].iloc[-1]] + list(future_pred),
            mode='lines+markers',
            name='Forecast',
            line=dict(color='#10b981', width=3, dash='dot'),
            marker=dict(size=10, color='#10b981', symbol='diamond', line=dict(width=2, color='white'))
        ))
        
        fig_forecast.update_layout(
            title='Sales Forecast - Next 6 Months',
            paper_bgcolor='#ffffff',
            plot_bgcolor='#ffffff',
            font=dict(color='#1e3a5f', family='Poppins'),
            xaxis=dict(
                title='Period',
                gridcolor='rgba(59, 130, 246, 0.1)',
                tickangle=45,
                tickfont=dict(color='#1e3a5f'),
                title_font=dict(color='#1e3a5f')
            ),
            yaxis=dict(
                title='Sales ($)',
                gridcolor='rgba(59, 130, 246, 0.1)',
                tickfont=dict(color='#1e3a5f'),
                title_font=dict(color='#1e3a5f')
            ),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='center',
                x=0.5,
                font=dict(color='#1e3a5f')
            ),
            height=500,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_forecast, use_container_width=True)
        
        # Forecast Summary Cards
        st.markdown('<p class="sub-header"><i class="fas fa-chart-pie"></i> Forecast Summary</p>', unsafe_allow_html=True)
        
        forecast_col1, forecast_col2, forecast_col3, forecast_col4 = st.columns(4)
        
        with forecast_col1:
            avg_forecast = np.mean(future_pred)
            st.metric(
                label="Avg Forecast (6 months)",
                value=f"${avg_forecast:,.0f}",
                delta="per month"
            )
        
        with forecast_col2:
            total_forecast = np.sum(future_pred)
            st.metric(
                label="Total Projected",
                value=f"${total_forecast:,.0f}",
                delta="next 6 months"
            )
        
        with forecast_col3:
            growth_rate = ((future_pred[-1] - y[-1]) / y[-1]) * 100 if y[-1] != 0 else 0
            st.metric(
                label="Projected Growth",
                value=f"{growth_rate:+.1f}%",
                delta="vs last period"
            )
        
        with forecast_col4:
            model_r2 = model.score(X, y)
            st.metric(
                label="Model Accuracy (R²)",
                value=f"{model_r2:.2%}",
                delta="confidence"
            )
        
        # Forecast table
        st.markdown('<p class="sub-header"><i class="fas fa-table"></i> Detailed Forecast</p>', unsafe_allow_html=True)
        
        forecast_table = pd.DataFrame({
            'Period': future_labels,
            'Predicted Sales': [f"${x:,.2f}" for x in future_pred],
            'Growth vs Prev': [f"{((future_pred[i] - (future_pred[i-1] if i > 0 else y[-1])) / (future_pred[i-1] if i > 0 else y[-1]) * 100):+.1f}%" if (future_pred[i-1] if i > 0 else y[-1]) != 0 else "N/A" for i in range(len(future_pred))]
        })
        
        table_html_forecast = '<div class="custom-table-container"><div class="table-scroll-wrapper"><table class="custom-table"><thead><tr>'
        for col in forecast_table.columns:
            table_html_forecast += f'<th>{col}</th>'
        table_html_forecast += '</tr></thead><tbody>'
        for _, row in forecast_table.iterrows():
            table_html_forecast += '<tr>'
            for val in row:
                table_html_forecast += f'<td>{val}</td>'
            table_html_forecast += '</tr>'
        table_html_forecast += '</tbody></table></div></div>'
        st.markdown(table_html_forecast, unsafe_allow_html=True)
        
    else:
        st.warning("⚠️ Data tidak cukup untuk melakukan forecasting. Minimal 3 periode data diperlukan.")


# === EXPORT & DOWNLOAD SECTION ===
st.markdown("---")
st.markdown('<p class="section-header"><i class="fas fa-download"></i> Export Data</p>', unsafe_allow_html=True)

export_col1, export_col2, export_col3 = st.columns(3)

with export_col1:
    # Download filtered data as CSV
    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data (CSV)",
        data=csv_data,
        file_name="filtered_sales_data.csv",
        mime="text/csv",
        use_container_width=True
    )

with export_col2:
    # Summary statistics
    summary_data = filtered_df.describe().to_csv().encode('utf-8')
    st.download_button(
        label="📊 Download Summary Statistics",
        data=summary_data,
        file_name="sales_summary_stats.csv",
        mime="text/csv",
        use_container_width=True
    )

with export_col3:
    # Category summary
    cat_summary = filtered_df.groupby('category').agg({
        'sales': ['sum', 'mean', 'count'],
        'sk_customer': 'nunique'
    }).round(2)
    cat_summary.columns = ['Total Sales', 'Avg Sale', 'Transactions', 'Unique Customers']
    cat_data = cat_summary.to_csv().encode('utf-8')
    st.download_button(
        label="📁 Download Category Summary",
        data=cat_data,
        file_name="category_summary.csv",
        mime="text/csv",
        use_container_width=True
    )

# Footer
st.markdown("---")
st.markdown(f"""
<div class="footer" style="background: linear-gradient(135deg, #1e3a5f 0%, #2c5282 100%); padding: 30px; border-radius: 16px; margin-top: 30px; text-align: center; box-shadow: 0 -4px 20px rgba(30, 58, 95, 0.2);">
    <div style="display: flex; justify-content: center; align-items: center; gap: 20px; flex-wrap: wrap; margin-bottom: 15px;">
        <div style="background: rgba(255,255,255,0.1); padding: 10px 20px; border-radius: 30px;">
            <span style="color: #93c5fd;"><i class="fas fa-database"></i></span>
            <span style="color: white; font-weight: 600;"> {len(df):,} Total Records</span>
        </div>
        <div style="background: rgba(255,255,255,0.1); padding: 10px 20px; border-radius: 30px;">
            <span style="color: #93c5fd;"><i class="fas fa-calendar"></i></span>
            <span style="color: white; font-weight: 600;"> 2015-2018 Data</span>
        </div>
        <div style="background: rgba(255,255,255,0.1); padding: 10px 20px; border-radius: 30px;">
            <span style="color: #93c5fd;"><i class="fas fa-code"></i></span>
            <span style="color: white; font-weight: 600;"> Streamlit + Plotly</span>
        </div>
    </div>
    <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem; margin: 0;">
        <i class="fas fa-chart-line" style="color: #60a5fa;"></i> Sales Analytics Dashboard | 
        <i class="fas fa-graduation-cap" style="color: #60a5fa;"></i> Business Intelligence Project
    </p>
    <p style="color: rgba(255,255,255,0.5); font-size: 0.75rem; margin-top: 10px;">
        Built with ❤️ for UAS Business Intelligence
    </p>
</div>
""", unsafe_allow_html=True)
