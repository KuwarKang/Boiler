import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
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

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        background: linear-gradient(145deg, #0a0e1a 0%, #1a2332 50%, #0f172a 100%);
        padding: 2rem 0;
    }
    
    .header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 2.5rem;
        border-radius: 24px;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(30, 58, 138, 0.3);
        text-align: center;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
        margin-bottom: 2rem;
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.4);
    }
    
    .metric-card {
        background: linear-gradient(145deg, rgba(239, 68, 68, 0.15) 0%, rgba(239, 68, 68, 0.05) 100%);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 16px;
        padding: 1.8rem;
        text-align: center;
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .metric-card-green {
        background: linear-gradient(145deg, rgba(34, 197, 94, 0.15) 0%, rgba(34, 197, 94, 0.05) 100%);
        border: 1px solid rgba(34, 197, 94, 0.3);
    }
    
    .metric-card-blue {
        background: linear-gradient(145deg, rgba(59, 130, 246, 0.15) 0%, rgba(59, 130, 246, 0.05) 100%);
        border: 1px solid rgba(59, 130, 246, 0.3);
    }
    
    .metric-card-status {
        background: linear-gradient(145deg, rgba(100, 116, 139, 0.15) 0%, rgba(100, 116, 139, 0.05) 100%);
        border: 1px solid rgba(100, 116, 139, 0.3);
        height: 120px;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
        background: linear-gradient(45deg, #ffffff 0%, #f8fafc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #cbd5e1;
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
    }
    
    .status-safe { background: rgba(34, 197, 94, 0.2); color: #22c55e; border: 1px solid rgba(34, 197, 94, 0.4); }
    .status-critical { background: rgba(239, 68, 68, 0.2); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.4); }
    
    .alert-critical {
        background: linear-gradient(145deg, #ef4444 0%, #dc2626 100%);
        border: 1px solid #fca5a5;
        border-radius: 16px;
        padding: 1.8rem;
        text-align: center;
        box-shadow: 0 15px 40px rgba(239, 68, 68, 0.4);
        margin-bottom: 2rem;
        color: white;
    }
    
    .title-main {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #e2e8f0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        font-size: 1.25rem;
        color: #e2e8f0;
        font-weight: 400;
    }
    
    .section-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(255,255,255,0.1);
    }
    
    .sidebar-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 1.5rem;
        padding-bottom: 0.8rem;
        border-bottom: 2px solid rgba(255,255,255,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR - FIXED ----------------
with st.sidebar:
    st.markdown("""
    <div style='
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        height: 100%;
    '>
    """, unsafe_allow_html=True)
    
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
    if st.button("🔄 Refresh Data", type="primary", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="header">
    <div class="title-main">🔥 Smart Boiler Expansion Monitor</div>
    <div class="subtitle">Real-time structural expansion monitoring & predictive alerts</div>
</div>
""", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def fetch_data():
    """Fetch and process data from ThingSpeak"""
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
        return df
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")
        return pd.DataFrame()

# ---------------- DATA PROCESSING ----------------
df = fetch_data()
if df.empty:
    st.warning("No data available. Please check your API credentials.")
    st.stop()

# Calculate expansions
df['X_exp'] = (df['X'] - init_x).clip(lower=0)
df['Y_exp'] = (df['Y'] - init_y).clip(lower=0)
df['Z_exp'] = (df['Z'] - init_z).clip(lower=0)

# Latest values
latest = df.iloc[-1]

# Status check
x_alert = latest['X_exp'] > x_threshold
y_alert = latest['Y_exp'] > y_threshold
z_alert = latest['Z_exp'] > z_threshold
critical_alert = x_alert or y_alert or z_alert

# ---------------- METRICS ROW - FIXED ----------------
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

# ---------------- ALERT BANNER ----------------
if critical_alert:
    st.markdown(f"""
    <div class="alert-critical">
        <h3 style='margin: 0 0 1rem 0;'>🚨 CRITICAL ALERT</h3>
        <div style='font-size: 1.1rem;'>
            <strong>X:</strong> {latest['X_exp']:.2f}mm {'✅' if not x_alert else '❌'} | 
            <strong>Y:</strong> {latest['Y_exp']:.2f}mm {'✅' if not y_alert else '❌'} | 
            <strong>Z:</strong> {latest['Z_exp']:.2f}mm {'✅' if not z_alert else '❌'}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- CHARTS ROW ----------------
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📈 Real-time Expansion Trends</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=df['X_exp'], name='X', line=dict(color='#ef4444', width=3)))
    fig.add_trace(go.Scatter(y=df['Y_exp'], name='Y', line=dict(color='#22c55e', width=3)))
    fig.add_trace(go.Scatter(y=df['Z_exp'], name='Z', line=dict(color='#3b82f6', width=3)))
    
    fig.add_hline(y=x_threshold, line_dash="dash", line_color="#ef4444")
    fig.add_hline(y=y_threshold, line_dash="dash", line_color="#22c55e")
    fig.add_hline(y=z_threshold, line_dash="dash", line_color="#3b82f6")
    
    fig.update_layout(
        template="plotly_dark", height=400, showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15),
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig3d = go.Figure(data=[go.Scatter3d(
        x=df['X_exp'], y=df['Y_exp'], z=df['Z_exp'],
        mode='lines+markers',
        line=dict(width=4, color='white'),
        marker=dict(size=4, color='gold')
    )])
    
    fig3d.update_layout(
        template="plotly_dark", height=400,
        scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z')
    )
    st.plotly_chart(fig3d, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- DATA TABLE ----------------
with st.expander("📋 Detailed Data", expanded=False):
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.dataframe(
        df[['timestamp', 'X_exp', 'Y_exp', 'Z_exp']].tail(20),
        use_container_width=True,
        hide_index=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown(f"""
<div style='text-align: center; padding: 2rem; color: #64748b; font-size: 0.9rem; border-top: 1px solid rgba(255,255,255,0.1);'>
    <div>🔥 Smart Boiler Expansion Monitor v2.0</div>
    <div>Data last updated: <span style='color: #94a3b8;'>{datetime.now().strftime("%H:%M:%S")}</span></div>
</div>
""", unsafe_allow_html=True)