"""
KPI Card components
"""
from components.icons import SVG_ICONS


def render_kpi_card(card_type, label, value, delta):
    """Render a single KPI card with SVG icon"""
    icon = SVG_ICONS.get(card_type, SVG_ICONS['sales'])
    return f'''
    <div class="kpi-card kpi-card--{card_type}">
        <div class="kpi-icon">
            {icon}
        </div>
        <div class="kpi-content">
            <span class="kpi-label">{label}</span>
            <span class="kpi-value">{value}</span>
            <span class="kpi-delta">{delta}</span>
        </div>
    </div>
    '''


def render_kpi_row1(kpis):
    """Render the first row of KPI cards (5 cards)"""
    cards = [
        render_kpi_card('sales', 'Total Sales', f"${kpis['total_sales']:,.2f}", f"{kpis['transaction_count']:,} transaksi"),
        render_kpi_card('avg', 'Rata-rata Order', f"${kpis['avg_order']:,.2f}", "per transaksi"),
        render_kpi_card('customers', 'Total Customers', f"{kpis['total_customers']:,}", "unique customers"),
        render_kpi_card('products', 'Total Products', f"{kpis['total_products']:,}", "unique products"),
        render_kpi_card('orders', 'Total Orders', f"{kpis['total_orders']:,}", "unique orders"),
    ]
    
    return f'''
    <div class="kpi-grid">
        {''.join(cards)}
    </div>
    '''


def render_kpi_row2(kpis):
    """Render the second row of KPI cards (4 cards)"""
    cards = [
        render_kpi_card('categories', 'Total Categories', f"{kpis['total_categories']:,}", "kategori produk"),
        render_kpi_card('subcategories', 'Total Sub-Categories', f"{kpis['total_subcategories']:,}", "sub-kategori"),
        render_kpi_card('states', 'Total States', f"{kpis['total_states']:,}", "negara bagian"),
        render_kpi_card('regions', 'Total Regions', f"{kpis['total_regions']:,}", "wilayah"),
    ]
    
    return f'''
    <div class="kpi-grid kpi-grid--4cols">
        {''.join(cards)}
    </div>
    '''


def render_insight_card(card_class, label_icon, label, value, subtitle):
    """Render a quick insight card"""
    return f'''
    <div class="insight-card {card_class}">
        <p class="insight-label">
            {label_icon}
            {label}
        </p>
        <h3 class="insight-value">{value}</h3>
        <p class="insight-sub">{subtitle}</p>
    </div>
    '''


def render_insights_section(insights):
    """Render the quick insights section"""
    cards_html = ''
    
    if 'top_category' in insights:
        cards_html += render_insight_card(
            'insight-card--category',
            '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="#f59e0b"><path stroke-linecap="round" stroke-linejoin="round" d="M16.5 18.75h-9m9 0a3 3 0 0 1 3 3h-15a3 3 0 0 1 3-3m9 0v-3.375c0-.621-.503-1.125-1.125-1.125h-.871M7.5 18.75v-3.375c0-.621.504-1.125 1.125-1.125h.872m5.007 0H9.497m5.007 0a7.454 7.454 0 0 1-.982-3.172M9.497 14.25a7.454 7.454 0 0 0 .981-3.172M5.25 4.236c-.982.143-1.954.317-2.916.52A6.003 6.003 0 0 0 7.73 9.728M5.25 4.236V4.5c0 2.108.966 3.99 2.48 5.228M5.25 4.236V2.721C7.456 2.41 9.71 2.25 12 2.25c2.291 0 4.545.16 6.75.47v1.516M7.73 9.728a6.726 6.726 0 0 0 2.748 1.35m8.272-6.842V4.5c0 2.108-.966 3.99-2.48 5.228m2.48-5.492a46.32 46.32 0 0 1 2.916.52 6.003 6.003 0 0 1-5.395 4.972m0 0a6.726 6.726 0 0 1-2.749 1.35m0 0a6.772 6.772 0 0 1-3.044 0" /></svg>',
            'Top Category',
            insights['top_category']['name'],
            f"${insights['top_category']['sales']:,.0f}"
        )
    
    if 'top_region' in insights:
        cards_html += render_insight_card(
            'insight-card--region',
            '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="#10b981"><path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" /><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1 1 15 0Z" /></svg>',
            'Top Region',
            insights['top_region']['name'],
            f"${insights['top_region']['sales']:,.0f}"
        )
    
    if 'top_segment' in insights:
        cards_html += render_insight_card(
            'insight-card--segment',
            '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="#ef4444"><path stroke-linecap="round" stroke-linejoin="round" d="M18 18.72a9.094 9.094 0 0 0 3.741-.479 3 3 0 0 0-4.682-2.72m.94 3.198.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0 1 12 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 0 1 6 18.719m12 0a5.971 5.971 0 0 0-.941-3.197m0 0A5.995 5.995 0 0 0 12 12.75a5.995 5.995 0 0 0-5.058 2.772m0 0a3 3 0 0 0-4.681 2.72 8.986 8.986 0 0 0 3.74.477m.94-3.197a5.971 5.971 0 0 0-.94 3.197M15 6.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Zm6 3a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Zm-13.5 0a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Z" /></svg>',
            'Top Segment',
            insights['top_segment']['name'],
            'Best Performer'
        )
    
    if 'top_state' in insights:
        cards_html += render_insight_card(
            'insight-card--month',
            '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="#f59e0b"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 21h19.5m-18-18v18m10.5-18v18m6-13.5V21M6.75 6.75h.75m-.75 3h.75m-.75 3h.75m3-6h.75m-.75 3h.75m-.75 3h.75M6.75 21v-3.375c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21M3 3h12m-.75 4.5H21m-3.75 3.75h.008v.008h-.008v-.008Zm0 3h.008v.008h-.008v-.008Zm0 3h.008v.008h-.008v-.008Z" /></svg>',
            'Top State',
            insights['top_state']['name'],
            f"${insights['top_state']['sales']:,.0f}"
        )
    
    return f'''
    <div class="insight-grid">
        {cards_html}
    </div>
    '''
