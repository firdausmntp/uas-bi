"""
Chart components for the dashboard
"""
import plotly.express as px
import plotly.graph_objects as go
from config.settings import CHART_COLORS, CHART_LAYOUT, PIE_CHART_SETTINGS, BAR_CHART_SETTINGS


def create_pie_chart(data, values, names, title, colors=None, height=220):
    """Create a styled pie chart"""
    if colors is None:
        colors = CHART_COLORS
    
    fig = px.pie(
        data,
        values=values,
        names=names,
        title=f'<b>{title}</b>' if title else '',
        color_discrete_sequence=colors,
        hole=PIE_CHART_SETTINGS['hole']
    )
    
    fig.update_layout(
        paper_bgcolor=CHART_LAYOUT['paper_bgcolor'],
        plot_bgcolor=CHART_LAYOUT['plot_bgcolor'],
        font=dict(color='#1e3a5f', family='Poppins', size=10),
        title=dict(font=dict(size=12, color='#1e3a5f'), x=0.5, xanchor='center'),
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.3,
            xanchor='center',
            x=0.5,
            font=dict(size=8, color='#1e3a5f')
        ),
        margin=dict(l=5, r=5, t=35, b=45),
        height=height
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent',
        textfont=dict(size=10, color='#ffffff', family='Poppins'),
        insidetextorientation='radial',
        marker=dict(line=dict(
            color='#ffffff',
            width=2
        )),
        pull=[0.02] * len(data)
    )
    
    return fig


def create_pie_chart_large(data, values, names, title='', colors=None, height=350):
    """Create a larger pie chart for tab views"""
    if colors is None:
        colors = CHART_COLORS
    
    fig = px.pie(
        data,
        values=values,
        names=names,
        color_discrete_sequence=colors,
        hole=0.45
    )
    
    fig.update_layout(
        paper_bgcolor=CHART_LAYOUT['paper_bgcolor'],
        plot_bgcolor=CHART_LAYOUT['plot_bgcolor'],
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
        height=height
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        textfont=dict(size=11, color='#ffffff', family='Poppins'),
        insidetextorientation='radial',
        hovertemplate='<b>%{label}</b><br>Sales: $%{value:,.2f}<br>Percentage: %{percent}<extra></extra>',
        marker=dict(line=dict(color='#ffffff', width=2)),
        pull=[0.02] * len(data)
    )
    
    return fig


def create_bar_chart_horizontal(data, x, y, title, color_column=None, height=200, show_text=False):
    """Create a horizontal bar chart"""
    # Use empty string (not None) to avoid Plotly rendering 'undefined'
    formatted_title = f'<b>{title}</b>' if title else ''
    
    if color_column:
        fig = px.bar(
            data,
            x=x,
            y=y,
            orientation='h',
            title=formatted_title,
            color=color_column,
            color_continuous_scale='Blues',
            text=data[x].apply(lambda val: f'${val:,.0f}') if show_text else None
        )
    else:
        fig = px.bar(
            data,
            x=x,
            y=y,
            orientation='h',
            title=formatted_title,
            color=x,
            color_continuous_scale='Blues',
            text=data[x].apply(lambda val: f'${val:,.0f}') if show_text else None
        )
    
    fig.update_layout(
        paper_bgcolor=CHART_LAYOUT['paper_bgcolor'],
        plot_bgcolor=CHART_LAYOUT['plot_bgcolor'],
        font=dict(color='#1e3a5f', family='Poppins', size=10),
        title=dict(text=formatted_title, font=dict(size=12, color='#1e3a5f')),
        showlegend=False,
        coloraxis_showscale=False,
        # Extra top space prevents the modebar from overlapping the plot area
        margin=dict(l=10, r=10, t=40, b=10),
        height=height,
        xaxis=dict(
            title='',
            tickfont=dict(size=9, color='#1e3a5f'),
            gridcolor='rgba(59, 130, 246, 0.1)'
        ),
        yaxis=dict(
            title='',
            tickfont=dict(size=9, color='#1e3a5f'),
            categoryorder='total ascending',
            gridcolor='rgba(59, 130, 246, 0.1)'
        )
    )
    
    if show_text:
        fig.update_traces(textposition='inside', textfont=dict(color='white', size=9))
    
    fig.update_traces(marker=dict(line=dict(
        color=BAR_CHART_SETTINGS['marker_line_color'],
        width=BAR_CHART_SETTINGS['marker_line_width']
    )))
    
    return fig


def create_bar_chart_vertical(data, x, y, title=None, color=None, height=350):
    """Create a vertical bar chart"""
    fig = px.bar(
        data,
        x=x,
        y=y,
        color=color,
        color_discrete_sequence=CHART_COLORS,
        barmode='group' if color else 'relative'
    )
    
    fig.update_layout(
        paper_bgcolor=CHART_LAYOUT['paper_bgcolor'],
        plot_bgcolor=CHART_LAYOUT['plot_bgcolor'],
        font=dict(color='#1e3a5f', family='Poppins', size=11),
        showlegend=True if color else False,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            font=dict(color='#1e3a5f', size=10)
        ),
        margin=dict(l=10, r=20, t=20, b=60),
        height=height,
        xaxis=dict(
            gridcolor='rgba(59, 130, 246, 0.15)',
            tickfont=dict(color='#4a6fa5', size=10)
        ),
        yaxis=dict(
            gridcolor='rgba(59, 130, 246, 0.15)',
            tickfont=dict(color='#4a6fa5', size=10)
        )
    )
    
    fig.update_traces(marker=dict(line=dict(color='#1e3a5f', width=1)))
    
    return fig


def create_line_chart(data, x, y, title=None, height=400):
    """Create a line chart with markers"""
    fig = px.line(
        data,
        x=x,
        y=y,
        markers=True,
        color_discrete_sequence=['#3b82f6']
    )
    
    fig.update_layout(
        paper_bgcolor=CHART_LAYOUT['paper_bgcolor'],
        plot_bgcolor=CHART_LAYOUT['plot_bgcolor'],
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
        height=height,
        margin=dict(l=10, r=20, t=20, b=80)
    )
    
    fig.update_traces(
        line=dict(width=3, color='#3b82f6'),
        marker=dict(size=8, color='#1e3a5f', line=dict(width=2, color='#ffffff')),
        hovertemplate='<b>%{x}</b><br>Sales: $%{y:,.2f}<extra></extra>'
    )
    
    return fig


_US_STATE_TO_ABBR = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}


def create_us_sales_choropleth(state_sales, state_col='state', value_col='sales', title='', height=420):
    """Create a USA choropleth map (sales by state).

    Expects a DataFrame with a state name column (e.g., 'California') and a numeric value column.
    """
    df_map = state_sales.copy()
    df_map['_state_code'] = df_map[state_col].map(_US_STATE_TO_ABBR)
    df_map = df_map.dropna(subset=['_state_code'])

    fig = px.choropleth(
        df_map,
        locations='_state_code',
        locationmode='USA-states',
        color=value_col,
        scope='usa',
        color_continuous_scale='Blues'
    )

    fig.update_layout(
        paper_bgcolor=CHART_LAYOUT['paper_bgcolor'],
        plot_bgcolor=CHART_LAYOUT['plot_bgcolor'],
        font=dict(color='#1e3a5f', family='Poppins', size=11),
        title=dict(text=f'<b>{title}</b>' if title else '', x=0.5, xanchor='center', font=dict(size=14, color='#1e3a5f')),
        height=height,
        margin=dict(l=10, r=10, t=40 if title else 20, b=10),
        coloraxis_colorbar=dict(
            title=dict(text='Sales', font=dict(color='#1e3a5f', size=11)),
            tickfont=dict(color='#1e3a5f', size=10)
        ),
        geo=dict(
            bgcolor='rgba(0,0,0,0)',
            showframe=False,
            showcoastlines=False,
        ),
    )

    fig.update_traces(
        marker_line_color='#ffffff',
        marker_line_width=0.6,
        hovertemplate='<b>%{location}</b><br>Sales: $%{z:,.2f}<extra></extra>'
    )

    return fig
