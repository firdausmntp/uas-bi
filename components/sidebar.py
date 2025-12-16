"""
Sidebar components for filtering
"""
import streamlit as st


def render_sidebar_header():
    """Render the sidebar header"""
    st.sidebar.markdown('''
    <div class="sidebar-header">
        <h2 class="sidebar-title"><i class="fas fa-filter"></i> Filter Data</h2>
    </div>
    ''', unsafe_allow_html=True)


def render_filter_section(title, icon):
    """Render a filter section header"""
    st.sidebar.markdown(f'''
    <div class="filter-section">
        <p class="filter-section-title"><i class="fas fa-{icon}"></i> {title}</p>
    </div>
    ''', unsafe_allow_html=True)


def render_filter_label(label, icon):
    """Render a filter label"""
    st.sidebar.markdown(f'<p class="filter-label"><i class="fas fa-{icon}"></i> {label}</p>', unsafe_allow_html=True)


def render_divider():
    """Render a sidebar divider"""
    st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)


def create_year_filter(df):
    """Create year filter"""
    render_filter_label('Tahun', 'calendar-alt')
    years = sorted(df['order_year'].dropna().unique())
    return st.sidebar.multiselect(
        "Tahun",
        options=years,
        default=years,
        label_visibility="collapsed"
    )


def create_region_filter(df):
    """Create region filter"""
    render_filter_label('Region', 'globe-americas')
    regions = sorted(df['region'].dropna().unique())
    return st.sidebar.multiselect(
        "Region",
        options=regions,
        default=regions,
        label_visibility="collapsed"
    )


def create_state_filter(df):
    """Create state filter"""
    render_filter_label('State', 'map')
    states = sorted(df['state'].dropna().unique())
    return st.sidebar.multiselect(
        "State",
        options=states,
        default=states,
        label_visibility="collapsed"
    )


def create_segment_filter(df):
    """Create segment filter"""
    render_filter_label('Segment', 'users')
    segments = sorted(df['segment'].dropna().unique())
    return st.sidebar.multiselect(
        "Segment",
        options=segments,
        default=segments,
        label_visibility="collapsed"
    )


def create_category_filter(df):
    """Create category filter"""
    render_filter_label('Category', 'layer-group')
    categories = sorted(df['category'].dropna().unique())
    return st.sidebar.multiselect(
        "Category",
        options=categories,
        default=categories,
        label_visibility="collapsed"
    )


def create_subcategory_filter(df):
    """Create sub-category filter"""
    render_filter_label('Sub-Category', 'tags')
    subcategories = sorted(df['sub_category'].dropna().unique())
    return st.sidebar.multiselect(
        "Sub-Category",
        options=subcategories,
        default=subcategories,
        label_visibility="collapsed"
    )


def create_product_search():
    """Create product search input"""
    render_filter_label('Cari Produk', 'search')
    return st.sidebar.text_input(
        "Search",
        placeholder="Ketik nama produk...",
        label_visibility="collapsed"
    )


def create_all_filters(df):
    """Create all sidebar filters and return selected values"""
    render_sidebar_header()
    
    # Time Filters
    render_filter_section('Time Filters', 'clock')
    selected_years = create_year_filter(df)
    render_divider()
    
    # Geographic Filters
    render_filter_section('Geographic Filters', 'map-marked-alt')
    selected_regions = create_region_filter(df)
    selected_states = create_state_filter(df)
    render_divider()
    
    # Customer Filters
    render_filter_section('Customer Filters', 'user-friends')
    selected_segments = create_segment_filter(df)
    render_divider()
    
    # Product Filters
    render_filter_section('Product Filters', 'box-open')
    selected_categories = create_category_filter(df)
    selected_subcategories = create_subcategory_filter(df)
    product_search = create_product_search()
    render_divider()
    
    # Footer
    render_sidebar_footer(df)
    
    return {
        'years': selected_years,
        'regions': selected_regions,
        'states': selected_states,
        'segments': selected_segments,
        'categories': selected_categories,
        'subcategories': selected_subcategories,
        'product_search': product_search
    }


def render_sidebar_footer(df):
    """Render sidebar footer with data info"""
    st.sidebar.markdown(f'''
    <div class="sidebar-footer">
        <p class="data-info"><i class="fas fa-database"></i> Total Data: <strong>{len(df):,}</strong> records</p>
        <p class="data-info"><i class="fas fa-calendar"></i> Period: <strong>{df['order_year'].min():.0f} - {df['order_year'].max():.0f}</strong></p>
    </div>
    ''', unsafe_allow_html=True)
