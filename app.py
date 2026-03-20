import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from datetime import datetime

# ---------------- CONFIG ----------------
CHANNEL_ID = 3304820
READ_API = "1JBJZ0VWIC0JILIL"

# Page config
st.set_page_config(
    page_title="Smart Boiler Expansion Monitor",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS - COMPLETE UPDATED VERSION ----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    body {
        color: #f1f5f9;
        font-family: 'Inter', sans-serif;
    }

    .main {
        background: linear-gradient(145deg, #0a0e1a 0%, #1a2332 50%, #0f172a 100%);
        padding: 2rem 0;
        color: #f1f5f9;
    }
    
    .header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 2.5rem;
        border-radius: 24px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 20px 40px rgba(30, 58, 138, 0.3);
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        color: #f1f5f9;
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.4);
    }
    
    /* Metric Cards - Perfect Layout */
    .metric-card, .metric-card-green, .metric-card-blue, .metric-card-status {
        border-radius: 16px;
        padding: 1.8rem;
        text-align: center;
        height: 130px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        transition: all 0.3s ease;
    }
    
    .metric-card {
        background: rgba(239, 68, 68, 0.12);
        border: 1px solid rgba(239, 68, 68, 0.25);
    }
    
    .metric-card-green {
        background: rgba(34, 197, 94, 0.12);
        border: 1px solid rgba(34, 197, 94, 0.25);
    }
    
    .metric-card-blue {
        background: rgba(59, 130, 246, 0.12);
        border: 1px solid rgba(59, 130, 246, 0.25);
    }
    
    .metric-card-status {
        background: rgba(100, 116, 139, 0.12);
        border: 1px solid rgba(100, 116, 139, 0.25);
    }
    
    .metric-card:hover, .metric-card-green:hover, .metric-card-blue:hover, .metric-card-status:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #ffffff;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        margin-bottom: 0.3rem;
        line-height: 1.1;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .status-badge {
        padding: 0.6rem 1.2rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
        display: inline-block;
    }
    
    .status-safe {
        background: rgba(34, 197, 94, 0.2);
        color: #22c55e;
        border: 1px solid rgba(34, 197, 94, 0.4);
    }
    
    .status-critical {
        background: rgba(239, 68, 68, 0.2);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.4);
    }
    
    .alert-critical {
        background: linear-gradient(145deg, #ef4444 0%, #dc2626 100%);
        border: 1px solid rgba(252, 165, 165, 0.5);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 15px 40px rgba(239, 68, 68, 0.4);
        margin-bottom: 2rem;
    }
    
    .alert-critical h3 {
        margin: 0 0 1rem 0;
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    .title-main {
        font-size: 3rem;
        font-weight: 800;
        color: #ffffff;
        text-shadow: 0 2px 20px rgba(0,0,0,0.3);
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        font-size: 1.25rem;
        color: #cbd5f5;
        font-weight: 400;
    }
    
    .section-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 1.5rem;
        padding-bottom: 0.8rem;
        border-bottom: 2px solid rgba(255,255,255,0.1);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .sidebar-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 1.5rem;
        padding-bottom: 0.8rem;
        border-bottom: 2px solid rgba(255,255,255,0.1);
    }
    
    /* Sidebar & Streamlit Components */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.06) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        height: 100% !important;
    }
    
    .stSlider > div > div > div {
        background: rgba(255, 255, 255, 0.1);
    }
    
    .stNumberInput > div > div > div {
        background: rgba(255, 255, 255, 0.1);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6, #1e40af) !important;
        border: none !important;
        border-radius: 12px !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 0.8rem 2rem !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.4) !important;
    }
    
    .stExpander {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        margin-bottom: 1rem;
    }
    
    /* Dataframe styling */
    .dataframe {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown('<div class="sidebar-title">⚙️ Configuration</div>', unsafe_allow_html=True)
    
    st.markdown("**Initial Calibration (mm)**")
    col1, col2, col3 = st.columns(3)
    with col1: init_x = st.number_input("🔴 X", value=10.0, step=0.1, format="%.1f")
    with col2: init_y = st.number_input("🟢 Y", value=10.0, step=0.1, format="%.1f")
    with col3: init_z = st.number_input("🔵 Z", value=10.0, step=0.1, format="%.1f")
    
    st.markdown("**Alert Thresholds (mm)**")
    x_threshold = st.slider("X Max", 5.0, 20.0, 10.0, 0.5)
    y_threshold = st.slider("Y Max", 10.0, 30.0, 15.0, 0.5)
    z_threshold = st.slider("Z Max", 5.0, 15.0, 8.0, 0.5)
    
    st.markdown("---")
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

# ---------------- HEADER ----------------
st.markdown("""
<div class="header">
    <div class="title-main">🔥 Smart Boiler Expansion Monitor</div>
    <div class="subtitle">Real-time structural expansion monitoring & predictive alerts</div>
</div>
""", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def fetch_data():
    """Fetch data from ThingSpeak"""
    try:
        url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={READ_API}&results=100"
        res = requests.get(url, timeout=10).json()
        
        data = []
        for f in res['feeds']:
            try:
                x = float(f['field1'] or 0)
                y = float(f['field2'] or 0)
                z = float(f['field3'] or 0)
                timestamp = f['created_at']
                data.append([timestamp, x, y, z])
            except:
                continue
        
        df = pd.DataFrame(data, columns=['timestamp', 'X', 'Y', 'Z'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df.sort_values('timestamp')
    except Exception as e:
        st.error(f"❌ Failed to fetch data: {e}")
        return pd.DataFrame()

# ---------------- MAIN CONTENT ----------------
df = fetch_data()

if df.empty:
    st.warning("⚠️ No data available. Please check your API credentials.")
    st.stop()

# Calculate expansions
df['X_exp'] = (df['X'] - init_x).clip(lower=0)
df['Y_exp'] = (df['Y'] - init_y).clip(lower=0)
df['Z_exp'] = (df['Z'] - init_z).clip(lower=0)

latest = df.iloc[-1]

# Status check
x_alert = latest['X_exp'] > x_threshold
y_alert = latest['Y_exp'] > y_threshold
z_alert = latest['Z_exp'] > z_threshold
critical_alert = x_alert or y_alert or z_alert

# ---------------- KPI METRICS ----------------
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📊 Current Expansion Metrics</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{latest['X_exp']:.2f}</div>
        <div class="metric-label">X Axis</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card metric-card-green">
        <div class="metric-value">{latest['Y_exp']:.2f}</div>
        <div class="metric-label">Y Axis</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card metric-card-blue">
        <div class="metric-value">{latest['Z_exp']:.2f}</div>
        <div class="metric-label">Z Axis</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    status_class = "status-safe" if not critical_alert else "status-critical"
    status_text = "SAFE" if not critical_alert else "CRITICAL"
    st.markdown(f"""
    <div class="metric-card metric-card-status">
        <div class="status-badge {status_class}">{status_text}</div>
        <div class="metric-label">Status</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- CRITICAL ALERT ----------------
if critical_alert:
    st.markdown(f"""
    <div class="alert-critical">
        <h3>🚨 CRITICAL ALERT</h3>
        <div style='font-size: 1.1rem; line-height: 1.6;'>
            <strong>🔴 X:</strong> {latest['X_exp']:.2f}mm {'✅' if not x_alert else '❌'}<br>
            <strong>🟢 Y:</strong> {latest['Y_exp']:.2f}mm {'✅' if not y_alert else '❌'}<br>
            <strong>🔵 Z:</strong> {latest['Z_exp']:.2f}mm {'✅' if not z_alert else '❌'}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- CHARTS ----------------
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📈 Real-time Trends</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=df['X_exp'], name='X', line=dict(color='#ef4444', width=3)))
    fig.add_trace(go.Scatter(y=df['Y_exp'], name='Y', line=dict(color='#22c55e', width=3)))
    fig.add_trace(go.Scatter(y=df['Z_exp'], name='Z', line=dict(color='#3b82f6', width=3)))
    
    fig.add_hline(y=x_threshold, line_dash="dash", line_color="#ef4444", annotation_text=f"X: {x_threshold}")
    fig.add_hline(y=y_threshold, line_dash="dash", line_color="#22c55e", annotation_text=f"Y: {y_threshold}")
    fig.add_hline(y=z_threshold, line_dash="dash", line_color="#3b82f6", annotation_text=f"Z: {z_threshold}")
    
    fig.update_layout(
        template="plotly_dark",
        height=400,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center"),
        hovermode='x unified',
        margin=dict(t=40, b=60)
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig3d = go.Figure(data=[go.Scatter3d(
        x=df['X_exp'], y=df['Y_exp'], z=df['Z_exp'],
        mode='lines+markers',
        line=dict(width=4, color='white'),
        marker=dict(size=5, color='gold', symbol='diamond')
    )])
    
    fig3d.update_layout(
        template="plotly_dark",
        height=400,
        scene=dict(
            xaxis_title='X (mm)', yaxis_title='Y (mm)', zaxis_title='Z (mm)',
            bgcolor='rgba(0,0,0,0)'
        ),
        margin=dict(l=0, r=0, t=0, b=0)
    )
    st.plotly_chart(fig3d, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- DATA TABLE ----------------
with st.expander("📋 Detailed Data & Statistics", expanded=False):
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("📈 Max X", f"{df['X_exp'].max():.2f}mm")
        st.metric("📈 Max Y", f"{df['Y_exp'].max():.2f}mm")
        st.metric("📈 Max Z", f"{df['Z_exp'].max():.2f}mm")
    
    with col2:
        st.dataframe(
            df[['timestamp', 'X_exp', 'Y_exp', 'Z_exp']].tail(15),
            use_container_width=True,
            hide_index=True,
            column_config={
                "timestamp": "Time",
                "X_exp": st.column_config.NumberColumn("X (mm)", format="%.2f"),
                "Y_exp": st.column_config.NumberColumn("Y (mm)", format="%.2f"),
                "Z_exp": st.column_config.NumberColumn("Z (mm)", format="%.2f"),
            }
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown(f"""
<div style='
    text-align: center; 
    padding: 2rem; 
    color: #647