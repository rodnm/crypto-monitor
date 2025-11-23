import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import ast
import sys
import os

# Add the parent directory to sys.path to allow imports from etl
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from etl.main import run_etl

# Configuration
DATA_FILE = "data/crypto_market.csv"

# --- Catppuccin Palettes ---
THEMES = {
    "Mocha": {
        'rosewater': '#f5e0dc', 'flamingo': '#f2cdcd', 'pink': '#f5c2e7', 'mauve': '#cba6f7',
        'red': '#f38ba8', 'maroon': '#eba0ac', 'peach': '#fab387', 'yellow': '#f9e2af',
        'green': '#a6e3a1', 'teal': '#94e2d5', 'sky': '#89dceb', 'sapphire': '#74c7ec',
        'blue': '#89b4fa', 'lavender': '#b4befe', 'text': '#cdd6f4', 'subtext1': '#bac2de',
        'subtext0': '#a6adc8', 'overlay2': '#9399b2', 'overlay1': '#7f849c', 'overlay0': '#6c7086',
        'surface2': '#585b70', 'surface1': '#45475a', 'surface0': '#313244', 'base': '#1e1e2e',
        'mantle': '#181825', 'crust': '#11111b'
    },
    "Macchiato": {
        'rosewater': '#f4dbd6', 'flamingo': '#f0c6c6', 'pink': '#f5bde6', 'mauve': '#c6a0f6',
        'red': '#ed8796', 'maroon': '#ee99a0', 'peach': '#f5a97f', 'yellow': '#eed49f',
        'green': '#a6da95', 'teal': '#8bd5ca', 'sky': '#91d7e3', 'sapphire': '#7dc4e4',
        'blue': '#8aadf4', 'lavender': '#b7bdf8', 'text': '#cad3f5', 'subtext1': '#b8c0e0',
        'subtext0': '#a5adcb', 'overlay2': '#9399b2', 'overlay1': '#8087a2', 'overlay0': '#6e738d',
        'surface2': '#5b6078', 'surface1': '#494d64', 'surface0': '#363a4f', 'base': '#24273a',
        'mantle': '#1e2030', 'crust': '#181926'
    },
    "Frappe": {
        'rosewater': '#f2d5cf', 'flamingo': '#eebebe', 'pink': '#f4b8e4', 'mauve': '#ca9ee6',
        'red': '#e78284', 'maroon': '#ea999c', 'peach': '#ef9f76', 'yellow': '#e5c890',
        'green': '#a6d189', 'teal': '#81c8be', 'sky': '#99d1db', 'sapphire': '#85c1dc',
        'blue': '#8caaee', 'lavender': '#babbf1', 'text': '#c6d0f5', 'subtext1': '#b5bfe2',
        'subtext0': '#a5adce', 'overlay2': '#949cbb', 'overlay1': '#838ba7', 'overlay0': '#737994',
        'surface2': '#626880', 'surface1': '#51576d', 'surface0': '#414559', 'base': '#303446',
        'mantle': '#292c3c', 'crust': '#232634'
    },
    "Latte": {
        'rosewater': '#dc8a78', 'flamingo': '#dd7878', 'pink': '#ea76cb', 'mauve': '#8839ef',
        'red': '#d20f39', 'maroon': '#e64553', 'peach': '#fe640b', 'yellow': '#df8e1d',
        'green': '#40a02b', 'teal': '#179299', 'sky': '#04a5e5', 'sapphire': '#209fb5',
        'blue': '#1e66f5', 'lavender': '#7287fd', 'text': '#4c4f69', 'subtext1': '#5c5f77',
        'subtext0': '#6c6f85', 'overlay2': '#7c7f93', 'overlay1': '#8c8fa1', 'overlay0': '#9ca0b0',
        'surface2': '#acb0be', 'surface1': '#bcc0cc', 'surface0': '#ccd0da', 'base': '#eff1f5',
        'mantle': '#e6e9ef', 'crust': '#dce0e8'
    }
}

st.set_page_config(
    page_title="Crypto Monitor 🚀",
    page_icon="📈",
    layout="wide"
)

# --- Theme Selection & CSS Injection ---
st.sidebar.title("Crypto Monitor")
selected_theme_name = st.sidebar.selectbox("Select Theme", list(THEMES.keys()), index=0)
current_theme = THEMES[selected_theme_name]

# Inject CSS to override Streamlit defaults dynamically
st.markdown(f"""
    <style>
        .stApp {{
            background-color: {current_theme['base']};
            color: {current_theme['text']};
        }}
        .stSidebar {{
            background-color: {current_theme['mantle']};
        }}
        [data-testid="stSidebar"] {{
            background-color: {current_theme['mantle']};
        }}
        .stMarkdown, .stText, h1, h2, h3, h4, h5, h6, label, .stMetricValue, .stMetricLabel {{
            color: {current_theme['text']} !important;
        }}
        /* Table styles */
        .dataframe {{
            color: {current_theme['text']} !important;
            background-color: {current_theme['surface0']} !important;
        }}
    </style>
""", unsafe_allow_html=True)


def run_etl_process():
    """Runs the ETL script to fetch fresh data."""
    try:
        run_etl()
        st.toast("Data updated successfully!", icon="✅")
    except Exception as e:
        st.error(f"Failed to update data: {e}")

def load_data():
    """Loads data from CSV."""
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame()
    df = pd.read_csv(DATA_FILE)
    if 'Sparkline (7d)' in df.columns:
        df['Sparkline (7d)'] = df['Sparkline (7d)'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    return df

if st.sidebar.button("🔄 Refresh Data"):
    with st.spinner("Fetching latest prices..."):
        run_etl_process()
        st.rerun()

# Load Data
df = load_data()

# Filters
selected_coins = []
if not df.empty:
    st.sidebar.divider()
    st.sidebar.header("Filters")
    selected_coins = st.sidebar.multiselect(
        "Select Coins to Display",
        options=df['Symbol'].unique(),
        default=df['Symbol'].unique()
    )

# Main Content
st.title("🚀 Real-Time Crypto Tracker")

if df.empty:
    st.warning("No data found. Please click 'Refresh Data'.")
else:
    # Apply Filter
    if selected_coins:
        filtered_df = df[df['Symbol'].isin(selected_coins)]
    else:
        filtered_df = df

    if filtered_df.empty:
        st.info("No coins selected.")
    else:
        # KPI Row
        col1, col2, col3 = st.columns(3)
        
        top_gainer = filtered_df.loc[filtered_df['Change (24h) %'].idxmax()]
        top_loser = filtered_df.loc[filtered_df['Change (24h) %'].idxmin()]
        avg_change = filtered_df['Change (24h) %'].mean()
        
        col1.metric("Top Gainer 🚀", f"{top_gainer['Name']}", f"{top_gainer['Change (24h) %']:.2f}%")
        col2.metric("Top Loser 📉", f"{top_loser['Name']}", f"{top_loser['Change (24h) %']:.2f}%")
        col3.metric("Market Trend (Avg) 📊", f"{avg_change:.2f}%", delta_color="normal")
        
        st.divider()

        # --- Visualizations ---
        
        # 1. Market Overview Treemap
        st.subheader("Market Overview (Treemap)")
        st.caption("Size = Market Cap | Color = 24h Change (Red=Down, Green=Up)")
        
        fig_treemap = px.treemap(
            filtered_df, 
            path=['Symbol'], 
            values='Market Cap',
            color='Change (24h) %',
            color_continuous_scale=[current_theme['red'], current_theme['surface0'], current_theme['green']],
            color_continuous_midpoint=0,
            hover_data=['Name', 'Price (USD)', 'Change (24h) %']
        )
        fig_treemap.update_layout(
            margin=dict(t=0, l=0, r=0, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=current_theme['text'])
        )
        st.plotly_chart(fig_treemap, use_container_width=True)

        # 2. Split View: Donut Chart & Trend Chart
        col_chart1, col_chart2 = st.columns([1, 2]) 
        
        with col_chart1:
            st.subheader("Market Dominance")
            fig_donut = px.pie(
                filtered_df, 
                values='Market Cap', 
                names='Symbol', 
                hole=0.4,
                title="Share of Market Cap",
                color_discrete_sequence=[
                    current_theme['mauve'], current_theme['blue'], current_theme['teal'], 
                    current_theme['green'], current_theme['peach'], current_theme['yellow'], 
                    current_theme['red'], current_theme['maroon']
                ]
            )
            fig_donut.update_traces(textposition='inside', textinfo='percent+label')
            fig_donut.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color=current_theme['text']),
                showlegend=False
            )
            st.plotly_chart(fig_donut, use_container_width=True)
            
        with col_chart2:
            st.subheader("7-Day Price Trend")
            
            trend_data = []
            for index, row in filtered_df.iterrows():
                prices = row['Sparkline (7d)']
                if isinstance(prices, list) and prices:
                    start_price = prices[0]
                    normalized_prices = [(p - start_price) / start_price * 100 for p in prices]
                    
                    temp_df = pd.DataFrame({
                        'Hour': range(len(prices)),
                        'Price Change %': normalized_prices,
                        'Symbol': row['Symbol']
                    })
                    trend_data.append(temp_df)
            
            if trend_data:
                trend_df = pd.concat(trend_data)
                fig_trend = px.line(
                    trend_df, x='Hour', y='Price Change %', color='Symbol',
                    labels={"Hour": "Hours Ago", "Price Change %": "Change (%)"},
                    color_discrete_sequence=[
                        current_theme['sky'], current_theme['pink'], current_theme['lavender'], 
                        current_theme['green'], current_theme['peach'], current_theme['yellow']
                    ]
                )
                fig_trend.update_layout(
                    hovermode="x unified",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color=current_theme['text']),
                    xaxis=dict(showgrid=False, zeroline=False),
                    yaxis=dict(showgrid=True, gridcolor=current_theme['surface0'], zeroline=False)
                )
                st.plotly_chart(fig_trend, use_container_width=True)

        # Data Table
        st.subheader("Detailed Market Data")
        
        display_df = filtered_df.drop(columns=['Sparkline (7d)'])
        
        st.dataframe(
            display_df.style.format({
                "Price (USD)": "${:,.2f}",
                "Market Cap": "${:,.0f}",
                "Volume (24h)": "${:,.0f}",
                "Change (24h) %": "{:+.2f}%"
            }),
            use_container_width=True
        )
        
        st.caption(f"Last updated: {df['Last Updated'].iloc[0]}")
