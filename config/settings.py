"""
Configuration settings for the dashboard
"""

# Color palettes - using vibrant, high contrast colors
CHART_COLORS = ['#dc2626', '#2563eb', '#16a34a', '#f59e0b', '#7c3aed', '#06b6d4']

# KPI Card gradient colors
KPI_GRADIENTS = {
    'sales': 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
    'avg': 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
    'customers': 'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)',
    'products': 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
    'orders': 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
    'categories': 'linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)',
    'subcategories': 'linear-gradient(135deg, #ec4899 0%, #db2777 100%)',
    'states': 'linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)',
    'regions': 'linear-gradient(135deg, #14b8a6 0%, #0d9488 100%)',
}

# Chart layout defaults
CHART_LAYOUT = {
    'paper_bgcolor': '#ffffff',
    'plot_bgcolor': '#ffffff',
    'font': {'color': '#1e3a5f', 'family': 'Poppins'},
    'margin': {'l': 20, 'r': 20, 't': 40, 'b': 40},
}

# Pie chart specific settings
PIE_CHART_SETTINGS = {
    'hole': 0.4,
    'textposition': 'inside',
    'textinfo': 'percent',
    'marker_line_color': '#000000',
    'marker_line_width': 2,
}

# Bar chart specific settings
BAR_CHART_SETTINGS = {
    'marker_line_color': '#1e3a5f',
    'marker_line_width': 1,
}
