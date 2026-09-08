import dash
from dash import html, dcc, Input, Output, callback
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os

# ============================================================
# READ DATA
# ============================================================
possible_files = ['Dash.csv', 'Dash.txt', 'Dash', 'dash.csv', 'dash.txt']
df = None
for file_name in possible_files:
    if os.path.exists(file_name):
        try:
            df = pd.read_csv(file_name)
            print(f"Loaded: {file_name}")
            break
        except Exception as e:
            print(f"Error: {e}")

if df is None:
    df = pd.DataFrame({
        'Month': ['January']*6 + ['February'] + ['March']*3 + ['April']*3,
        'Area': ['Cairo','Giza','Bani_Seif','Alex','Aswan','Cairo',
                 'Giza','Giza','Bani_Seif','Bani_Seif','Bani_Seif','Bani_Seif','Bani_Seif'],
        'Sales': [15000,8000,16000,12000,11500,14000,12500,17500,10320,7000,4000,18000,20000],
        'Unit': [200,210,450,320,150,400,200,320,450,600,170,190,200],
        'Profit': [3250,4000,2000,1000,900,190,400,1200,3400,1900,2700,1100,5100]
    })
    print("Using fallback data")

df.columns = df.columns.str.strip()
for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].astype(str).str.strip()

# ============================================================
# AGGREGATIONS
# ============================================================
total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
total_units = df['Unit'].sum()
avg_profit_margin = (total_profit / total_sales * 100) if total_sales else 0

month_order = ['January','February','March','April','May','June',
               'July','August','September','October','November','December']

sales_by_month = df.groupby('Month', sort=False).agg(
    Total_Sales=('Sales','sum'), Total_Profit=('Profit','sum'), Total_Units=('Unit','sum')
).reset_index()
existing_months = [m for m in month_order if m in sales_by_month['Month'].values]
sales_by_month['Month'] = pd.Categorical(sales_by_month['Month'], categories=existing_months, ordered=True)
sales_by_month = sales_by_month.sort_values('Month').reset_index(drop=True)

sales_by_area = df.groupby('Area').agg(
    Total_Sales=('Sales','sum'), Total_Profit=('Profit','sum'), Total_Units=('Unit','sum')
).reset_index()

sales_by_area_month = df.groupby(['Month','Area']).agg(
    Total_Sales=('Sales','sum'), Total_Profit=('Profit','sum')
).reset_index()
sales_by_area_month['Month'] = pd.Categorical(
    sales_by_area_month['Month'], categories=existing_months, ordered=True
)
sales_by_area_month = sales_by_area_month.sort_values('Month')

# ============================================================
# COLORS
# ============================================================
BG = '#0a1628'
CARD = '#111d35'
BORDER = '#1a2d50'
TEXT = '#e0e6ed'
MUTED = '#8899aa'
CYAN = '#00e5ff'
TEAL = '#00bfa5'
BLUE = '#4fc3f7'
PURPLE = '#7c4dff'
GREEN = '#69f0ae'
ORANGE = '#ffab40'
PINK = '#ff4081'
COLORS = [CYAN, BLUE, TEAL, PURPLE, ORANGE, GREEN, PINK]

# ============================================================
# ANIMATION CONFIG
# ============================================================
ANIM_CONFIG = {
    'transition': {'duration': 800, 'easing': 'cubic-in-out'},
    'frame': {'duration': 600, 'redraw': True},
}

# ============================================================
# HELPERS
# ============================================================
def card(children, style=None, class_name=''):
    s = {
        'backgroundColor': CARD, 'borderRadius': '16px',
        'border': f'1px solid {BORDER}', 'padding': '20px',
        'boxShadow': '0 4px 24px rgba(0,0,0,0.35)', 'height': '100%',
        'boxSizing': 'border-box',
    }
    if style:
        s.update(style)
    return html.Div(children, style=s, className=f'card-anim {class_name}')


def goal_row(label, current, target, delay=0):
    pct = min(int(current / target * 100), 100) if target else 0
    return html.Div([
        html.Div([
            html.Span(label, style={
                'color': MUTED, 'fontSize': '13px', 'flex': '1',
                'fontFamily': 'Orbitron, monospace', 'letterSpacing': '1px'}),
            html.Span(f'${current:,}/${target:,}',
                      style={'color': MUTED, 'fontSize': '11px', 'marginRight': '8px',
                             'fontFamily': 'Orbitron, monospace'}),
            html.Span(f'{pct}%', style={
                'color': CYAN, 'fontSize': '12px', 'fontWeight': '700',
                'fontFamily': 'Orbitron, monospace'}),
        ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '5px'}),
        html.Div(
            html.Div(className='bar-fill', style={
                'width': f'{pct}%', 'height': '6px', 'borderRadius': '3px',
                'background': f'linear-gradient(90deg,{TEAL},{CYAN})',
                'boxShadow': f'0 0 10px {CYAN}',
                'animation': f'growBar 1.2s ease-out {delay}s both',
            }),
            style={'width': '100%', 'height': '6px', 'borderRadius': '3px',
                   'backgroundColor': BORDER, 'marginBottom': '14px',
                   'overflow': 'hidden'}
        ),
    ], className='fade-in-up', style={'animationDelay': f'{delay}s'})


def legend_row(name, pct, val, color):
    return html.Div([
        html.Span('■', style={
            'color': color, 'marginRight': '10px', 'fontSize': '11px',
            'textShadow': f'0 0 8px {color}'}),
        html.Span(name.replace('_', ' '), style={
            'color': MUTED, 'fontSize': '12px', 'flex': '1', 'minWidth': '70px',
            'fontFamily': 'Orbitron, monospace', 'letterSpacing': '0.5px'}),
        html.Span(f'{pct}%', style={
            'color': MUTED, 'fontSize': '12px', 'marginRight': '10px',
            'fontFamily': 'Orbitron, monospace'}),
        html.Span(f'${val:,}', style={
            'color': TEXT, 'fontSize': '12px', 'fontWeight': '600',
            'fontFamily': 'Orbitron, monospace'}),
    ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '8px'},
       className='legend-hover')


def h_progress(label, pct, color, delay=0):
    return html.Div([
        html.Div([
            html.Span(label, style={
                'color': MUTED, 'fontSize': '12px', 'flex': '1',
                'fontFamily': 'Orbitron, monospace', 'letterSpacing': '1px'}),
            html.Span(f'{pct}%', style={
                'color': color, 'fontSize': '12px', 'fontWeight': '700',
                'fontFamily': 'Orbitron, monospace'}),
        ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '4px'}),
        html.Div(
            html.Div(style={
                'width': f'{pct}%', 'height': '5px', 'borderRadius': '3px',
                'background': color, 'boxShadow': f'0 0 8px {color}',
                'animation': f'growBar 1s ease-out {delay}s both'}),
            style={'width': '100%', 'height': '5px', 'borderRadius': '3px',
                   'backgroundColor': BORDER, 'marginBottom': '12px',
                   'overflow': 'hidden'}
        ),
    ])


def kpi_card(title, value, color, delay=0):
    return html.Div([
        html.Div(title, style={
            'color': MUTED, 'fontSize': '12px', 'marginBottom': '10px',
            'fontFamily': 'Orbitron, monospace', 'letterSpacing': '2px',
            'textTransform': 'uppercase'}),
        html.Div(value, style={
            'fontSize': '28px', 'fontWeight': '900', 'color': color,
            'fontFamily': 'Orbitron, monospace', 'letterSpacing': '1px',
            'textShadow': f'0 0 20px {color}80'}),
        html.Div(style={
            'width': '40px', 'height': '3px', 'background': color,
            'marginTop': '10px', 'borderRadius': '2px',
            'boxShadow': f'0 0 10px {color}'}),
    ], className='kpi-anim fade-in-up',
       style={
            'backgroundColor': CARD, 'borderRadius': '16px',
            'border': f'1px solid {BORDER}', 'padding': '22px',
            'height': '100%', 'boxSizing': 'border-box',
            'animationDelay': f'{delay}s',
            'position': 'relative', 'overflow': 'hidden',
    })


# ============================================================
# CHARTS (with animations)
# ============================================================
def fig_monthly_bar():
    ms = [m[:3].upper() for m in sales_by_month['Month']]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=ms, y=sales_by_month['Total_Sales'], name='Sales',
        marker=dict(color=CYAN, cornerradius=5,
                     line=dict(color=CYAN, width=0)),
        text=[f'${v/1000:.1f}k' for v in sales_by_month['Total_Sales']],
        textposition='outside',
        textfont=dict(color=TEXT, size=12, family='Orbitron'),
        hovertemplate='<b>%{x}</b><br>$%{y:,.0f}<extra></extra>',
    ))
    fig.add_trace(go.Bar(
        x=ms, y=sales_by_month['Total_Profit'], name='Profit',
        marker=dict(color=TEAL, cornerradius=5),
        text=[f'${v/1000:.1f}k' for v in sales_by_month['Total_Profit']],
        textposition='outside',
        textfont=dict(color=TEAL, size=11, family='Orbitron'),
        hovertemplate='<b>%{x}</b><br>$%{y:,.0f}<extra></extra>',
    ))
    fig.update_layout(
        barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=TEXT, family='Orbitron'),
        margin=dict(l=30, r=10, t=20, b=30),
        xaxis=dict(showgrid=False, tickfont=dict(color=MUTED, size=11, family='Orbitron')),
        yaxis=dict(showgrid=True, gridcolor=BORDER,
                   tickfont=dict(color=MUTED, size=10, family='Orbitron')),
        showlegend=False, height=280,
        transition=ANIM_CONFIG['transition'],
    )
    return fig


def fig_radar():
    areas = sales_by_area['Area'].tolist()
    vals = sales_by_area['Total_Sales'].tolist()
    fig = go.Figure(go.Scatterpolar(
        r=vals + [vals[0]], theta=areas + [areas[0]],
        fill='toself', fillcolor='rgba(0,229,255,0.15)',
        line=dict(color=CYAN, width=2),
        marker=dict(color=CYAN, size=8,
                     line=dict(color='white', width=2)),
        hovertemplate='<b>%{theta}</b><br>$%{r:,.0f}<extra></extra>',
    ))
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(visible=True, showticklabels=False,
                            gridcolor=BORDER, linecolor=BORDER),
            angularaxis=dict(tickfont=dict(color=MUTED, size=11, family='Orbitron'),
                             gridcolor=BORDER, linecolor=BORDER),
        ),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=50, r=50, t=30, b=30), height=280, showlegend=False,
        transition=ANIM_CONFIG['transition'],
    )
    return fig


def fig_donut(values, labels, center_text, center_sub, colors=None):
    c = colors or COLORS
    fig = go.Figure(go.Pie(
        labels=labels, values=values, hole=0.68,
        marker=dict(colors=c[:len(values)], line=dict(color=BG, width=3)),
        textinfo='percent',
        textfont=dict(color='white', size=11, family='Orbitron'),
        hovertemplate='<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>',
        sort=False,
        rotation=90,
    ))
    fig.add_annotation(text=f'<b>{center_text}</b>', x=0.5, y=0.55,
                       font=dict(size=20, color='white', family='Orbitron'),
                       showarrow=False)
    fig.add_annotation(text=center_sub.upper(), x=0.5, y=0.40,
                       font=dict(size=10, color=MUTED, family='Orbitron'),
                       showarrow=False)
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=5, r=5, t=5, b=5), height=240, showlegend=False,
        transition=ANIM_CONFIG['transition'],
    )
    return fig


def fig_compare_line():
    fig = go.Figure()
    for i, area in enumerate(sales_by_area_month['Area'].unique()):
        ad = sales_by_area_month[sales_by_area_month['Area'] == area]
        color = COLORS[i % len(COLORS)]
        fig.add_trace(go.Scatter(
            x=[m[:3].upper() for m in ad['Month'].astype(str)],
            y=ad['Total_Sales'], mode='lines+markers',
            name=area.replace('_', ' '),
            line=dict(width=2.5, shape='spline', color=color),
            marker=dict(size=7, line=dict(color='white', width=1)),
            hovertemplate='<b>%{x}</b><br>$%{y:,.0f}<extra></extra>',
        ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=TEXT, family='Orbitron'),
        margin=dict(l=30, r=10, t=30, b=30),
        xaxis=dict(showgrid=False, tickfont=dict(color=MUTED, family='Orbitron')),
        yaxis=dict(showgrid=True, gridcolor=BORDER,
                   tickfont=dict(color=MUTED, family='Orbitron')),
        legend=dict(orientation='h', y=1.15, x=0.5, xanchor='center',
                    font=dict(color=MUTED, size=10, family='Orbitron'),
                    bgcolor='rgba(0,0,0,0)'),
        height=260,
        transition=ANIM_CONFIG['transition'],
    )
    return fig


def fig_annual():
    ms = [m[:3].upper() for m in sales_by_month['Month']]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=ms, y=sales_by_month['Total_Sales'], name='Sales',
        marker=dict(color=BLUE, cornerradius=4), width=0.3,
    ))
    fig.add_trace(go.Bar(
        x=ms, y=sales_by_month['Total_Profit'], name='Profit',
        marker=dict(color=CYAN, cornerradius=4), width=0.3,
    ))
    fig.update_layout(
        barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=TEXT, family='Orbitron'),
        margin=dict(l=30, r=10, t=30, b=30),
        xaxis=dict(showgrid=False, tickfont=dict(color=MUTED, family='Orbitron')),
        yaxis=dict(showgrid=True, gridcolor=BORDER,
                   tickfont=dict(color=MUTED, family='Orbitron')),
        legend=dict(orientation='h', y=1.15, x=0.5, xanchor='center',
                    font=dict(color=MUTED, size=10, family='Orbitron'),
                    bgcolor='rgba(0,0,0,0)'),
        height=260,
        transition=ANIM_CONFIG['transition'],
    )
    return fig


def fig_sparkline():
    cum = np.cumsum(sales_by_month['Total_Profit'].values)
    fig = go.Figure(go.Scatter(
        y=cum, mode='lines',
        line=dict(color=CYAN, width=2.5, shape='spline'),
        fill='tozeroy', fillcolor='rgba(0,229,255,0.12)',
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0), height=55,
        xaxis=dict(visible=False), yaxis=dict(visible=False),
    )
    return fig


# ============================================================
# GOALS
# ============================================================
goals = []
for _, r in sales_by_area.iterrows():
    goals.append({
        'label': r['Area'].replace('_', ' ').upper(),
        'current': int(r['Total_Sales']),
        'target': int(r['Total_Sales'] * 1.15),
    })
g_cur = sum(g['current'] for g in goals)
g_tgt = sum(g['target'] for g in goals)
g_pct = int(g_cur / g_tgt * 100) if g_tgt else 0

AREA_COLOR = {a: COLORS[i % len(COLORS)] for i, a in enumerate(sales_by_area['Area'])}


# ============================================================
# PAGES
# ============================================================
def page_dashboard():
    return html.Div([
        # ROW 1
        html.Div([
            html.Div(card([
                html.Div([
                    html.Span('BALANCE', style={
                        'color': MUTED, 'fontSize': '11px',
                        'fontFamily': 'Orbitron, monospace', 'letterSpacing': '2px'}),
                ], style={'marginBottom': '6px'}),
                html.Div(f'${total_profit:,}', className='glow-text', style={
                    'fontSize': '30px', 'fontWeight': '900', 'color': 'white',
                    'fontFamily': 'Orbitron, monospace', 'letterSpacing': '1px',
                    'marginBottom': '14px'}),

                html.Div([
                    html.Div(className='shimmer', style={
                        'width': '36px', 'height': '7px', 'borderRadius': '4px',
                        'background': f'linear-gradient(90deg,{CYAN},{TEAL})',
                        'marginRight': '6px',
                        'boxShadow': f'0 0 8px {CYAN}'}),
                    html.Span('▪▪▪▪▪▪▪▪▪▪▪▪', style={
                        'color': MUTED, 'fontSize': '8px', 'letterSpacing': '2px'}),
                ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '12px'}),

                html.Div([
                    html.Span('BUDGET LOAD', style={
                        'color': MUTED, 'fontSize': '11px', 'flex': '1',
                        'fontFamily': 'Orbitron, monospace', 'letterSpacing': '1.5px'}),
                    html.Span(f'{int(avg_profit_margin)}%', style={
                        'color': CYAN, 'fontSize': '12px', 'fontWeight': '700',
                        'backgroundColor': BORDER, 'padding': '3px 12px',
                        'borderRadius': '10px', 'fontFamily': 'Orbitron, monospace',
                        'border': f'1px solid {CYAN}40'}),
                ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '12px'}),

                html.Div(f'${total_sales:,}', className='glow-text-sm', style={
                    'fontSize': '22px', 'fontWeight': '900', 'color': 'white',
                    'fontFamily': 'Orbitron, monospace', 'letterSpacing': '1px'}),
                html.Div('TOTAL FLOW', style={
                    'color': MUTED, 'fontSize': '10px', 'marginBottom': '8px',
                    'fontFamily': 'Orbitron, monospace', 'letterSpacing': '2px'}),
                dcc.Graph(figure=fig_sparkline(), config={'displayModeBar': False}),
                html.Div([
                    html.Span('ACTUAL CHANGE', style={
                        'color': MUTED, 'fontSize': '10px',
                        'fontFamily': 'Orbitron, monospace', 'letterSpacing': '1.5px'}),
                    html.Span(f'+${total_profit/1000:.1f}K', style={
                        'color': GREEN, 'fontSize': '12px', 'fontWeight': '700',
                        'marginLeft': '8px', 'fontFamily': 'Orbitron, monospace',
                        'textShadow': f'0 0 8px {GREEN}'}),
                ]),
            ], class_name='delay-1'), style={'flex': '1', 'minWidth': '240px', 'maxWidth': '280px'}),

            html.Div(card([
                html.Div([
                    html.Span('INFLOW', style={
                        'fontSize': '15px', 'fontWeight': '700', 'color': 'white',
                        'marginRight': '14px', 'fontFamily': 'Orbitron, monospace',
                        'letterSpacing': '2px'}),
                    html.Span('SALES', className='pill', style={
                        'fontSize': '10px', 'padding': '4px 12px', 'borderRadius': '4px',
                        'backgroundColor': BORDER, 'color': MUTED, 'marginRight': '4px',
                        'fontFamily': 'Orbitron, monospace', 'letterSpacing': '1.5px'}),
                    html.Span('PROFIT', className='pill', style={
                        'fontSize': '10px', 'padding': '4px 12px', 'borderRadius': '4px',
                        'backgroundColor': BORDER, 'color': MUTED, 'marginRight': '4px',
                        'fontFamily': 'Orbitron, monospace', 'letterSpacing': '1.5px'}),
                    html.Span('INFLOW', className='pill pill-active', style={
                        'fontSize': '10px', 'padding': '4px 12px', 'borderRadius': '4px',
                        'backgroundColor': CYAN, 'color': BG, 'fontWeight': '700',
                        'fontFamily': 'Orbitron, monospace', 'letterSpacing': '1.5px',
                        'boxShadow': f'0 0 12px {CYAN}80'}),
                    html.Span(f'${total_sales:,}', style={
                        'fontSize': '17px', 'fontWeight': '900', 'color': 'white',
                        'marginLeft': 'auto', 'fontFamily': 'Orbitron, monospace'}),
                ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '4px'}),
                dcc.Graph(figure=fig_monthly_bar(), config={'displayModeBar': False},
                          animate=True),
            ], class_name='delay-2'), style={'flex': '2.2', 'minWidth': '380px'}),

            html.Div(card([
                html.Div('STRUCTURE', style={
                    'fontSize': '15px', 'fontWeight': '700', 'color': 'white',
                    'fontFamily': 'Orbitron, monospace', 'letterSpacing': '2px'}),
                html.Div('INFLOW', style={
                    'color': MUTED, 'fontSize': '11px', 'marginBottom': '4px',
                    'fontFamily': 'Orbitron, monospace', 'letterSpacing': '2px'}),
                dcc.Graph(figure=fig_radar(), config={'displayModeBar': False}),
            ], class_name='delay-3'), style={'flex': '1.1', 'minWidth': '260px'}),
        ], className='row-anim',
           style={'display': 'flex', 'gap': '14px', 'marginBottom': '14px', 'flexWrap': 'wrap'}),

        # ROW 2
        html.Div([
            html.Div([
                html.Div([
                    html.Span('GOALS', style={
                        'fontSize': '15px', 'fontWeight': '700', 'color': 'white',
                        'marginRight': '10px', 'fontFamily': 'Orbitron, monospace',
                        'letterSpacing': '2px'}),
                    html.Span(f'${g_cur:,} / ${g_tgt:,}', style={
                        'color': CYAN, 'fontSize': '12px', 'fontWeight': '600',
                        'marginRight': '8px', 'fontFamily': 'Orbitron, monospace'}),
                    html.Span(f'{g_pct}%', style={
                        'color': 'white', 'fontSize': '13px', 'fontWeight': '700',
                        'fontFamily': 'Orbitron, monospace'}),
                ], style={'marginBottom': '10px'}),
                html.Div(
                    html.Div(style={
                        'width': f'{g_pct}%', 'height': '8px', 'borderRadius': '4px',
                        'background': f'linear-gradient(90deg,{TEAL},{CYAN})',
                        'boxShadow': f'0 0 12px {CYAN}',
                        'animation': 'growBar 1.5s ease-out both'}),
                    style={'width': '100%', 'height': '8px', 'borderRadius': '4px',
                           'backgroundColor': BORDER, 'marginBottom': '18px',
                           'overflow': 'hidden'}
                ),
                *[goal_row(g['label'], g['current'], g['target'], delay=i*0.15)
                  for i, g in enumerate(goals)],
            ], className='fade-in-up',
               style={'flex': '1', 'minWidth': '240px', 'maxWidth': '280px', 'paddingTop': '6px'}),

            html.Div(card([
                html.Div('BUDGET', style={
                    'fontSize': '15px', 'fontWeight': '700', 'color': 'white',
                    'marginBottom': '8px', 'fontFamily': 'Orbitron, monospace',
                    'letterSpacing': '2px'}),
                html.Div([
                    html.Div([
                        dcc.Graph(figure=fig_donut(
                            sales_by_area['Total_Sales'].tolist(),
                            sales_by_area['Area'].tolist(),
                            f'${total_sales/1000:.1f}K', 'TOTAL SALES'),
                            config={'displayModeBar': False}),
                    ], style={'flex': '1'}),
                    html.Div([
                        h_progress('INFLOW', 53, CYAN, delay=0.3),
                        h_progress('OUTFLOW', 47, BLUE, delay=0.4),
                        html.Hr(style={'borderColor': BORDER, 'margin': '8px 0'}),
                        *[legend_row(a, int(s/total_sales*100), s, AREA_COLOR.get(a, CYAN))
                          for a, s in zip(sales_by_area['Area'], sales_by_area['Total_Sales'])],
                        html.Div(style={'height': '8px'}),
                        html.Div(f'${total_profit:,}', className='glow-text-sm', style={
                            'fontSize': '20px', 'fontWeight': '900', 'color': 'white',
                            'fontFamily': 'Orbitron, monospace'}),
                        html.Div('BALANCE', style={
                            'color': MUTED, 'fontSize': '10px',
                            'fontFamily': 'Orbitron, monospace', 'letterSpacing': '2px'}),
                    ], style={'flex': '1', 'paddingLeft': '14px'}),
                ], style={'display': 'flex', 'alignItems': 'center'}),
            ], class_name='delay-2'), style={'flex': '2.2', 'minWidth': '380px'}),

            html.Div(card([
                html.Div('COSTS', style={
                    'fontSize': '15px', 'fontWeight': '700', 'color': 'white',
                    'marginBottom': '4px', 'fontFamily': 'Orbitron, monospace',
                    'letterSpacing': '2px'}),
                dcc.Graph(figure=fig_donut(
                    sales_by_area['Total_Profit'].tolist(),
                    sales_by_area['Area'].tolist(),
                    f'${total_profit:,}', 'TOTAL PROFIT',
                    colors=[TEAL, CYAN, BLUE, PURPLE, ORANGE]),
                    config={'displayModeBar': False}),
                html.Div([
                    *[legend_row(a, int(p/total_profit*100) if total_profit else 0, p,
                                 AREA_COLOR.get(a, CYAN))
                      for a, p in zip(sales_by_area['Area'], sales_by_area['Total_Profit'])]
                ], style={'marginTop': '4px'}),
            ], class_name='delay-3'), style={'flex': '1.1', 'minWidth': '260px'}),
        ], className='row-anim',
           style={'display': 'flex', 'gap': '14px', 'marginBottom': '14px', 'flexWrap': 'wrap'}),

        # ROW 3
        html.Div([
            html.Div(card([
                html.Div([
                    html.Span('COMPARE COSTS', style={
                        'fontSize': '15px', 'fontWeight': '700', 'color': 'white',
                        'marginRight': '8px', 'fontFamily': 'Orbitron, monospace',
                        'letterSpacing': '2px'}),
                    html.Span(f'${total_profit:,}', style={
                        'color': CYAN, 'fontSize': '13px', 'fontWeight': '600',
                        'fontFamily': 'Orbitron, monospace'}),
                ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '4px'}),
                dcc.Graph(figure=fig_compare_line(), config={'displayModeBar': False}),
            ], class_name='delay-1'), style={'flex': '1', 'minWidth': '400px'}),

            html.Div(card([
                html.Div('ANNUAL PLANS', style={
                    'fontSize': '15px', 'fontWeight': '700', 'color': 'white',
                    'marginBottom': '4px', 'fontFamily': 'Orbitron, monospace',
                    'letterSpacing': '2px'}),
                html.Div([
                    html.Div([
                        dcc.Graph(figure=fig_annual(), config={'displayModeBar': False}),
                    ], style={'flex': '2'}),
                    html.Div([
                        *[legend_row(a, int(p/total_profit*100) if total_profit else 0, p,
                                     AREA_COLOR.get(a, CYAN))
                          for a, p in zip(sales_by_area['Area'], sales_by_area['Total_Profit'])]
                    ], style={'flex': '1', 'paddingLeft': '12px', 'display': 'flex',
                              'flexDirection': 'column', 'justifyContent': 'center'}),
                ], style={'display': 'flex'}),
            ], class_name='delay-2'), style={'flex': '1', 'minWidth': '400px'}),
        ], className='row-anim',
           style={'display': 'flex', 'gap': '14px', 'marginBottom': '14px', 'flexWrap': 'wrap'}),

        # KPIs
        html.Div([
            html.Div(kpi_card('TOTAL SALES', f'${total_sales:,}', CYAN, delay=0.1),
                     style={'flex': '1', 'minWidth': '180px'}),
            html.Div(kpi_card('TOTAL PROFIT', f'${total_profit:,}', GREEN, delay=0.2),
                     style={'flex': '1', 'minWidth': '180px'}),
            html.Div(kpi_card('TOTAL UNITS', f'{total_units:,}', BLUE, delay=0.3),
                     style={'flex': '1', 'minWidth': '180px'}),
            html.Div(kpi_card('MARGIN', f'{avg_profit_margin:.1f}%', ORANGE, delay=0.4),
                     style={'flex': '1', 'minWidth': '180px'}),
            html.Div(kpi_card('AREAS', f'{df["Area"].nunique()}', PURPLE, delay=0.5),
                     style={'flex': '1', 'minWidth': '180px'}),
        ], style={'display': 'flex', 'gap': '14px', 'flexWrap': 'wrap'}),
    ], className='page-fade')


def page_structure():
    return html.Div([
        html.Div([
            html.Div(card([
                html.Div('SALES BY AREA — RADAR', style={
                    'fontSize': '15px', 'fontWeight': '700', 'color': 'white',
                    'marginBottom': '8px', 'fontFamily': 'Orbitron, monospace',
                    'letterSpacing': '2px'}),
                dcc.Graph(figure=fig_radar(), config={'displayModeBar': False},
                          style={'height': '400px'}),
            ], class_name='delay-1'), style={'flex': '1', 'minWidth': '400px'}),

            html.Div(card([
                html.Div('SALES DISTRIBUTION', style={
                    'fontSize': '15px', 'fontWeight': '700', 'color': 'white',
                    'marginBottom': '8px', 'fontFamily': 'Orbitron, monospace',
                    'letterSpacing': '2px'}),
                dcc.Graph(figure=fig_donut(
                    sales_by_area['Total_Sales'].tolist(),
                    [a.replace('_', ' ') for a in sales_by_area['Area']],
                    f'${total_sales/1000:.1f}K', 'TOTAL'),
                    config={'displayModeBar': False}, style={'height': '400px'}),
            ], class_name='delay-2'), style={'flex': '1', 'minWidth': '400px'}),
        ], className='row-anim',
           style={'display': 'flex', 'gap': '14px', 'flexWrap': 'wrap', 'marginBottom': '14px'}),

        html.Div(card([
            html.Div('AREA BREAKDOWN', style={
                'fontSize': '15px', 'fontWeight': '700', 'color': 'white',
                'marginBottom': '16px', 'fontFamily': 'Orbitron, monospace',
                'letterSpacing': '2px'}),
            html.Div([
                *[html.Div([
                    html.Div([
                        html.Span('■', style={
                            'color': AREA_COLOR.get(a, CYAN), 'fontSize': '18px',
                            'marginRight': '12px',
                            'textShadow': f'0 0 10px {AREA_COLOR.get(a, CYAN)}'}),
                        html.Span(a.replace('_', ' ').upper(), style={
                            'color': TEXT, 'fontSize': '14px', 'fontWeight': '600',
                            'flex': '1', 'fontFamily': 'Orbitron, monospace',
                            'letterSpacing': '1.5px'}),
                        html.Span(f'SALES: ${s:,}', style={
                            'color': CYAN, 'fontSize': '12px', 'marginRight': '20px',
                            'fontFamily': 'Orbitron, monospace'}),
                        html.Span(f'PROFIT: ${p:,}', style={
                            'color': TEAL, 'fontSize': '12px', 'marginRight': '20px',
                            'fontFamily': 'Orbitron, monospace'}),
                        html.Span(f'UNITS: {u:,}', style={
                            'color': MUTED, 'fontSize': '12px',
                            'fontFamily': 'Orbitron, monospace'}),
                    ], className='area-row', style={
                        'display': 'flex', 'alignItems': 'center', 'padding': '14px 18px',
                        'backgroundColor': 'rgba(26,45,80,0.4)', 'borderRadius': '10px',
                        'marginBottom': '10px',
                        'borderLeft': f'3px solid {AREA_COLOR.get(a, CYAN)}',
                        'animation': f'slideInLeft 0.6s ease-out {i*0.1}s both'}),
                ]) for i, (a, s, p, u) in enumerate(zip(
                    sales_by_area['Area'], sales_by_area['Total_Sales'],
                    sales_by_area['Total_Profit'], sales_by_area['Total_Units']))]
            ]),
        ], class_name='delay-3')),
    ], className='page-fade')


def page_costs():
    return html.Div([
        html.Div([
            html.Div(card([
                html.Div('PROFIT BY AREA', style={
                    'fontSize': '15px', 'fontWeight': '700', 'color': 'white',
                    'marginBottom': '8px', 'fontFamily': 'Orbitron, monospace',
                    'letterSpacing': '2px'}),
                dcc.Graph(figure=fig_donut(
                    sales_by_area['Total_Profit'].tolist(),
                    [a.replace('_', ' ') for a in sales_by_area['Area']],
                    f'${total_profit:,}', 'PROFIT',
                    colors=[TEAL, CYAN, BLUE, PURPLE, ORANGE]),
                    config={'displayModeBar': False}, style={'height': '350px'}),
            ], class_name='delay-1'), style={'flex': '1', 'minWidth': '350px'}),

            html.Div(card([
                html.Div('COMPARE BY MONTH', style={
                    'fontSize': '15px', 'fontWeight': '700', 'color': 'white',
                    'marginBottom': '8px', 'fontFamily': 'Orbitron, monospace',
                    'letterSpacing': '2px'}),
                dcc.Graph(figure=fig_compare_line(), config={'displayModeBar': False},
                          style={'height': '350px'}),
            ], class_name='delay-2'), style={'flex': '1.5', 'minWidth': '400px'}),
        ], className='row-anim',
           style={'display': 'flex', 'gap': '14px', 'flexWrap': 'wrap', 'marginBottom': '14px'}),

        html.Div(card([
            html.Div('MONTHLY PROFIT BARS', style={
                'fontSize': '15px', 'fontWeight': '700', 'color': 'white',
                'marginBottom': '8px', 'fontFamily': 'Orbitron, monospace',
                'letterSpacing': '2px'}),
            dcc.Graph(figure=fig_monthly_bar(), config={'displayModeBar': False}),
        ], class_name='delay-3')),
    ], className='page-fade')


def page_budget():
    return html.Div([
        html.Div([
            html.Div(kpi_card('TOTAL SALES', f'${total_sales:,}', CYAN, delay=0.1),
                     style={'flex': '1', 'minWidth': '180px'}),
            html.Div(kpi_card('TOTAL PROFIT', f'${total_profit:,}', GREEN, delay=0.2),
                     style={'flex': '1', 'minWidth': '180px'}),
            html.Div(kpi_card('BUDGET LOAD', f'{avg_profit_margin:.0f}%', ORANGE, delay=0.3),
                     style={'flex': '1', 'minWidth': '180px'}),
            html.Div(kpi_card('GOAL PROGRESS', f'{g_pct}%', PURPLE, delay=0.4),
                     style={'flex': '1', 'minWidth': '180px'}),
        ], style={'display': 'flex', 'gap': '14px', 'marginBottom': '14px', 'flexWrap': 'wrap'}),

        html.Div([
            html.Div(card([
                html.Div('BUDGET ALLOCATION', style={
                    'fontSize': '15px', 'fontWeight': '700', 'color': 'white',
                    'marginBottom': '8px', 'fontFamily': 'Orbitron, monospace',
                    'letterSpacing': '2px'}),
                dcc.Graph(figure=fig_donut(
                    sales_by_area['Total_Sales'].tolist(),
                    [a.replace('_', ' ') for a in sales_by_area['Area']],
                    f'${total_sales/1000:.1f}K', 'BUDGET'),
                    config={'displayModeBar': False}, style={'height': '320px'}),
                html.Div([
                    h_progress('INFLOW', 53, CYAN, delay=0.5),
                    h_progress('OUTFLOW', 47, BLUE, delay=0.6),
                ], style={'marginTop': '10px'}),
            ], class_name='delay-1'), style={'flex': '1', 'minWidth': '350px'}),

            html.Div(card([
                html.Div([
                    html.Span('GOALS PROGRESS', style={
                        'fontSize': '15px', 'fontWeight': '700', 'color': 'white',
                        'marginRight': '10px', 'fontFamily': 'Orbitron, monospace',
                        'letterSpacing': '2px'}),
                    html.Span(f'{g_pct}%', style={
                        'color': CYAN, 'fontSize': '14px', 'fontWeight': '700',
                        'fontFamily': 'Orbitron, monospace'}),
                ], style={'marginBottom': '16px'}),
                html.Div(
                    html.Div(style={
                        'width': f'{g_pct}%', 'height': '10px', 'borderRadius': '5px',
                        'background': f'linear-gradient(90deg,{TEAL},{CYAN})',
                        'boxShadow': f'0 0 15px {CYAN}',
                        'animation': 'growBar 1.5s ease-out both'}),
                    style={'width': '100%', 'height': '10px', 'borderRadius': '5px',
                           'backgroundColor': BORDER, 'marginBottom': '22px',
                           'overflow': 'hidden'}
                ),
                *[goal_row(g['label'], g['current'], g['target'], delay=i*0.15)
                  for i, g in enumerate(goals)],
            ], class_name='delay-2'), style={'flex': '1', 'minWidth': '350px'}),
        ], className='row-anim',
           style={'display': 'flex', 'gap': '14px', 'flexWrap': 'wrap', 'marginBottom': '14px'}),

        html.Div(card([
            html.Div('ANNUAL PLANS', style={
                'fontSize': '15px', 'fontWeight': '700', 'color': 'white',
                'marginBottom': '8px', 'fontFamily': 'Orbitron, monospace',
                'letterSpacing': '2px'}),
            dcc.Graph(figure=fig_annual(), config={'displayModeBar': False}),
        ], class_name='delay-3')),
    ], className='page-fade')


# ============================================================
# APP
# ============================================================
app = dash.Dash(__name__)
app.title = 'SALES FINANCE'

app.index_string = '''
<!DOCTYPE html>
<html>
<head>
    {%metas%}
    <title>{%title%}</title>
    {%favicon%}
    {%css%}
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Rajdhani:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html, body {
            background-color: #0a1628 !important;
            overflow-x: hidden;
            font-family: 'Rajdhani', sans-serif;
        }
        #react-entry-point, ._dash-loading {
            background-color: #0a1628 !important;
        }

        /* Scrollbar */
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: #0a1628; }
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #00e5ff, #00bfa5);
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover { background: #00e5ff; }

        /* Buttons */
        button { font-family: 'Orbitron', monospace !important; }
        button:hover { transform: translateY(-1px); }
        button:focus { outline: none; }

        /* ============ ANIMATIONS ============ */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes slideInLeft {
            from { opacity: 0; transform: translateX(-40px); }
            to { opacity: 1; transform: translateX(0); }
        }
        @keyframes slideInRight {
            from { opacity: 0; transform: translateX(40px); }
            to { opacity: 1; transform: translateX(0); }
        }
        @keyframes growBar {
            from { width: 0 !important; }
        }
        @keyframes glow {
            0%, 100% { text-shadow: 0 0 10px rgba(0,229,255,0.5), 0 0 20px rgba(0,229,255,0.3); }
            50% { text-shadow: 0 0 15px rgba(0,229,255,0.8), 0 0 30px rgba(0,229,255,0.5); }
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); box-shadow: 0 0 12px rgba(0,229,255,0.8); }
            50% { transform: scale(1.05); box-shadow: 0 0 20px rgba(0,229,255,1); }
        }
        @keyframes shimmer {
            0% { background-position: -200% 0; }
            100% { background-position: 200% 0; }
        }
        @keyframes scanline {
            0% { transform: translateY(-100%); }
            100% { transform: translateY(100vh); }
        }

        /* Card animations */
        .card-anim {
            animation: fadeInUp 0.7s ease-out both;
            transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        .card-anim:hover {
            transform: translateY(-4px);
            border-color: #00e5ff !important;
            box-shadow: 0 8px 32px rgba(0,229,255,0.2) !important;
        }
        .card-anim::before {
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 100%; height: 2px;
            background: linear-gradient(90deg, transparent, #00e5ff, transparent);
            transition: left 0.6s ease;
        }
        .card-anim:hover::before {
            left: 100%;
        }

        .delay-1 { animation-delay: 0.1s !important; }
        .delay-2 { animation-delay: 0.25s !important; }
        .delay-3 { animation-delay: 0.4s !important; }

        .fade-in-up { animation: fadeInUp 0.7s ease-out both; }
        .page-fade { animation: fadeIn 0.5s ease-out; }
        .row-anim > * { animation: fadeInUp 0.7s ease-out both; }

        /* KPI hover */
        .kpi-anim::after {
            content: '';
            position: absolute;
            top: 0; right: 0;
            width: 60px; height: 60px;
            background: radial-gradient(circle, currentColor 0%, transparent 70%);
            opacity: 0.08;
            border-radius: 50%;
            transform: translate(20px, -20px);
        }
        .kpi-anim {
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .kpi-anim:hover {
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 10px 40px rgba(0,229,255,0.25);
        }

        /* Glow text */
        .glow-text {
            animation: glow 3s ease-in-out infinite;
        }
        .glow-text-sm {
            text-shadow: 0 0 8px rgba(255,255,255,0.4);
        }

        /* Shimmer bar */
        .shimmer {
            background: linear-gradient(90deg, #00bfa5, #00e5ff, #00bfa5);
            background-size: 200% 100%;
            animation: shimmer 2s infinite linear;
        }

        /* Pills */
        .pill {
            transition: all 0.3s ease;
            cursor: pointer;
        }
        .pill:hover {
            background-color: #1e3660 !important;
            color: #00e5ff !important;
        }
        .pill-active {
            animation: pulse 2.5s ease-in-out infinite;
        }

        /* Legend hover */
        .legend-hover {
            transition: transform 0.2s ease, background-color 0.2s ease;
            padding: 4px 8px;
            border-radius: 4px;
            margin-left: -8px;
            cursor: pointer;
        }
        .legend-hover:hover {
            background-color: rgba(0,229,255,0.08);
            transform: translateX(4px);
        }

        /* Area row hover */
        .area-row {
            transition: all 0.3s ease;
            cursor: pointer;
        }
        .area-row:hover {
            background-color: rgba(0,229,255,0.1) !important;
            transform: translateX(6px);
            box-shadow: 0 4px 20px rgba(0,229,255,0.15);
        }

        /* Nav button hover */
        .nav-btn {
            transition: all 0.3s ease !important;
        }
        .nav-btn:hover {
            border-color: #00e5ff !important;
            color: #00e5ff !important;
            background-color: rgba(0,229,255,0.08) !important;
            box-shadow: 0 0 15px rgba(0,229,255,0.3);
        }

        /* Quarter buttons */
        .q-btn {
            transition: all 0.3s ease;
            padding: 4px 8px;
            border-radius: 4px;
        }
        .q-btn:hover {
            color: #00e5ff !important;
            background-color: rgba(0,229,255,0.1);
        }

        /* Header logo animation */
        .logo-box {
            animation: pulse 3s ease-in-out infinite;
        }

        /* Background grid effect */
        body::before {
            content: '';
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background-image:
                linear-gradient(rgba(0,229,255,0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0,229,255,0.03) 1px, transparent 1px);
            background-size: 40px 40px;
            pointer-events: none;
            z-index: 0;
        }

        /* Scanline effect */
        body::after {
            content: '';
            position: fixed;
            top: 0; left: 0; right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, rgba(0,229,255,0.4), transparent);
            animation: scanline 8s linear infinite;
            pointer-events: none;
            z-index: 1;
        }

        #page-content, header { position: relative; z-index: 2; }
    </style>
</head>
<body>
    {%app_entry%}
    <footer>
        {%config%}
        {%scripts%}
        {%renderer%}
    </footer>
</body>
</html>
'''

app.layout = html.Div([
    dcc.Store(id='active-page', data='dashboard'),
    dcc.Store(id='active-quarter', data='Q2'),

    # HEADER
    html.Header([
        # Logo
        html.Div([
            html.Div([
                html.Div(className='logo-box', style={
                    'width': '16px', 'height': '16px', 'borderRadius': '3px',
                    'background': f'linear-gradient(135deg,{CYAN},{PURPLE})',
                    'display': 'inline-block', 'marginRight': '4px'}),
                html.Div(className='logo-box', style={
                    'width': '16px', 'height': '16px', 'borderRadius': '3px',
                    'background': f'linear-gradient(135deg,{TEAL},{GREEN})',
                    'display': 'inline-block', 'animationDelay': '0.5s'}),
            ], style={'marginRight': '12px'}),
            html.Span('SALES FINANCE', className='glow-text', style={
                'fontSize': '20px', 'fontWeight': '900', 'color': 'white',
                'fontFamily': 'Orbitron, monospace', 'letterSpacing': '3px'}),
        ], style={'display': 'flex', 'alignItems': 'center'}),

        # Nav
        html.Div([
            html.Button('DASHBOARD', id='btn-dashboard', n_clicks=0, className='nav-btn'),
            html.Button('STRUCTURE', id='btn-structure', n_clicks=0, className='nav-btn'),
            html.Button('COSTS', id='btn-costs', n_clicks=0, className='nav-btn'),
            html.Button('BUDGET', id='btn-budget', n_clicks=0, className='nav-btn'),
        ], style={'display': 'flex', 'alignItems': 'center', 'gap': '8px'}),

        # Quarters
        html.Div([
            html.Span('Q1', id='btn-q1', n_clicks=0, className='q-btn', style={
                'color': MUTED, 'marginLeft': '14px', 'cursor': 'pointer',
                'fontSize': '14px', 'fontWeight': '500',
                'fontFamily': 'Orbitron, monospace', 'letterSpacing': '2px',
                'userSelect': 'none'}),
            html.Span('Q2', id='btn-q2', n_clicks=0, className='q-btn glow-text', style={
                'color': CYAN, 'marginLeft': '14px', 'cursor': 'pointer',
                'fontSize': '14px', 'fontWeight': '900',
                'fontFamily': 'Orbitron, monospace', 'letterSpacing': '2px',
                'userSelect': 'none'}),
            html.Span('Q3', id='btn-q3', n_clicks=0, className='q-btn', style={
                'color': MUTED, 'marginLeft': '14px', 'cursor': 'pointer',
                'fontSize': '14px', 'fontWeight': '500',
                'fontFamily': 'Orbitron, monospace', 'letterSpacing': '2px',
                'userSelect': 'none'}),
        ], style={'display': 'flex', 'alignItems': 'center'}),

    ], style={
        'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center',
        'padding': '16px 32px', 'backgroundColor': BG,
        'borderBottom': f'1px solid {BORDER}',
        'boxShadow': '0 2px 20px rgba(0,229,255,0.05)',
    }),

    # PAGE CONTENT
    html.Div(id='page-content', style={'padding': '20px 24px'}),

], style={
    'backgroundColor': BG,
    'minHeight': '100vh',
    'fontFamily': "'Rajdhani', 'Segoe UI', sans-serif",
})


# ============================================================
# CALLBACKS
# ============================================================
@callback(
    Output('active-page', 'data'),
    Input('btn-dashboard', 'n_clicks'),
    Input('btn-structure', 'n_clicks'),
    Input('btn-costs', 'n_clicks'),
    Input('btn-budget', 'n_clicks'),
    prevent_initial_call=True,
)
def set_page(n1, n2, n3, n4):
    ctx = dash.callback_context
    if not ctx.triggered:
        return 'dashboard'
    btn = ctx.triggered[0]['prop_id'].split('.')[0]
    return {
        'btn-dashboard': 'dashboard',
        'btn-structure': 'structure',
        'btn-costs': 'costs',
        'btn-budget': 'budget',
    }.get(btn, 'dashboard')


@callback(Output('page-content', 'children'), Input('active-page', 'data'))
def render_page(page):
    return {
        'dashboard': page_dashboard,
        'structure': page_structure,
        'costs': page_costs,
        'budget': page_budget,
    }.get(page, page_dashboard)()


@callback(
    Output('btn-dashboard', 'style'),
    Output('btn-structure', 'style'),
    Output('btn-costs', 'style'),
    Output('btn-budget', 'style'),
    Input('active-page', 'data'),
)
def style_nav(page):
    def s(active):
        return {
            'padding': '9px 24px', 'borderRadius': '20px', 'cursor': 'pointer',
            'border': f'1.5px solid {CYAN if active else BORDER}',
            'backgroundColor': 'rgba(0,229,255,0.15)' if active else 'transparent',
            'color': CYAN if active else MUTED,
            'fontSize': '12px', 'fontWeight': '700',
            'outline': 'none', 'letterSpacing': '2px',
            'fontFamily': 'Orbitron, monospace',
            'boxShadow': f'0 0 15px rgba(0,229,255,0.4)' if active else 'none',
        }
    return s(page=='dashboard'), s(page=='structure'), s(page=='costs'), s(page=='budget')


@callback(
    Output('active-quarter', 'data'),
    Input('btn-q1', 'n_clicks'),
    Input('btn-q2', 'n_clicks'),
    Input('btn-q3', 'n_clicks'),
    prevent_initial_call=True,
)
def set_quarter(n1, n2, n3):
    ctx = dash.callback_context
    if not ctx.triggered:
        return 'Q2'
    btn = ctx.triggered[0]['prop_id'].split('.')[0]
    return {'btn-q1': 'Q1', 'btn-q2': 'Q2', 'btn-q3': 'Q3'}.get(btn, 'Q2')


@callback(
    Output('btn-q1', 'style'),
    Output('btn-q2', 'style'),
    Output('btn-q3', 'style'),
    Input('active-quarter', 'data'),
)
def style_quarter(q):
    def s(active):
        return {
            'color': CYAN if active else MUTED,
            'fontWeight': '900' if active else '500',
            'marginLeft': '14px', 'cursor': 'pointer',
            'fontSize': '14px', 'userSelect': 'none',
            'fontFamily': 'Orbitron, monospace', 'letterSpacing': '2px',
            'textShadow': f'0 0 12px {CYAN}' if active else 'none',
        }
    return s(q=='Q1'), s(q=='Q2'), s(q=='Q3')


if __name__ == '__main__':
    app.run(debug=True, port=8050)