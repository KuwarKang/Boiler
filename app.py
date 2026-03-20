import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from datetime import datetime

# ---------------- CONFIG ----------------
CHANNEL_ID = 3304820
READ_API = "1JBJZ0VWIC0JILIL"

st.set_page_config(
    page_title="Smart Boiler Expansion Monitor",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- COMPLETE PROFESSIONAL CSS ----------------
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
        transition: all 0.3s ease;
        color: #f1f5f9;
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.4);
    }
    
    /* Metric Cards */
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
    }
    
    .status-safe { background: rgba(34, 197, 94, 0.2); color: #22c55e; border: 1px solid rgba(34, 197, 94, 0.4); }
    .status-critical { background: rgba(239, 68, 68, 0.2); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.4); }
    
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
    
    .title-main { font-size: 3rem; font-weight: 800; color: #ffffff; text-shadow: 0 2px 20px rgba(0,0,0,0.3); margin-bottom: 0.5rem; }
    .subtitle { font-size: 1.25rem; color: #cbd5f5; font-weight: 400; }
    
    .section-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 1.5rem;
        padding-bottom: 0.8rem;
        border-bottom: 2px solid rgba(255,255,255,0.1);
    }
    
    .sidebar-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 1.5rem;
        padding-bottom: 0.8rem;
        border-bottom: 2px solid rgba(255,255,255,0.1);
    }
    
    /* Streamlit Components */
    .css-1d391kg { background: rgba(255,255,255,0.06) !important; backdrop-filter: blur(20px) !important; border: 1px solid rgba(255,255,255,0.08) !important; border-radius: 20px !important; padding: 2rem !important; }
    .stButton > button { background: linear-gradient(135deg, #3b82f6, #1e40af) !important; border-radius: 12px !important; color: white !important; font-weight: 600 !important; width: 100% !important; }
    .stExpander { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; }
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown('<div class="sidebar-title">⚙️ Settings</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1: init_x = st.number_input("🔴 X", value=10.0, step=0.1)
    with col2: init_y = st.number_input("🟢 Y", value=10.0, step=0.1)
    with col3: init_z = st.number_input("🔵 Z", value=10.0, step=0.1)

    st.markdown("**Alert Limits (mm)**")
    x_th = st.slider("X Limit", 5.0, 20.0, 10.0, 0.5)
    y_th = st.slider("Y Limit", 10.0, 30.0, 15.0, 0.5)
    z_th = st.slider("Z Limit", 5.0, 15.0, 8.0, 0.5)

    if st.button("🔄 Refresh", type="primary"):
        st.cache_data.clear()
        st.rerun()

# ---------------- HEADER ----------------
st.markdown("""
<div class="header">
    <div class="title-main">🔥 Smart Boiler Expansion Monitor</div>
    <div class="subtitle">Real-time Monitoring Dashboard</div>
</div>
""", unsafe_allow_html=True)

# ---------------- FETCH DATA ----------------
@st.cache_data(ttl=60)
def fetch():
    try:
        url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={READ_API}&results=50"
        res = requests.get(url, timeout=10).json()

        data = []
        for f in res['feeds']:
            try:
                x = float(f['field1'] or 0)
                y = float(f['field2'] or 0)
                z = float(f['field3'] or 0)
                t = f['created_at']
                data.append([t, x, y, z])
            except:
                continue

        df = pd.DataFrame(data, columns=['time', 'X', 'Y', 'Z'])
        df['time'] = pd.to_datetime(df['time'])
        return df.sort_values('time')
    except:
        return pd.DataFrame()

df = fetch()

if df.empty:
    st.warning("⚠️ No data available")
    st.stop()

# ---------------- CALCULATIONS ----------------
df['X_exp'] = (df['X'] - init_x).clip(lower=0)
df['Y_exp'] = (df['Y'] - init_y).clip(lower=0)
df['Z_exp'] = (df['Z'] - init_z).clip(lower=0)

latest = df.iloc[-1]

# ---------------- METRICS - 4 COLUMNS ----------------
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📊 Current Readings</div>', unsafe_allow_html=True)

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
    status_class = "status-safe" if not ((latest['X_exp']>x_th) or (latest['Y_exp']>y_th) or (latest['Z_exp']>z_th)) else "status-critical"
    status_text = "SAFE" if status_class == "status-safe" else "ALERT"
    st.markdown(f"""
    <div class="metric-card metric-card-status">
        <div class="status-badge {status_class}">{status_text}</div>
        <div class="metric-label">Status</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- ALERT ----------------
if (latest['X_exp']>x_th) or (latest['Y_exp']>y_th) or (latest['Z_exp']>z_th):
    st.markdown(f"""
    <div class="alert-critical">
        <h3>🚨 LIMIT EXCEEDED</h3>
        <div>X: {latest['X_exp']:.2f} | Y: {latest['Y_exp']:.2f} | Z: {latest['Z_exp']:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- GRAPHS ----------------
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📈 Expansion Trends</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=df['X_exp'], name='X', line=dict(color='#ef4444', width=3)))
    fig.add_trace(go.Scatter(y=df['Y_exp'], name='Y', line=dict(color='#22c55e', width=3)))
    fig.add_trace(go.Scatter(y=df['Z_exp'], name='Z', line=dict(color='#3b82f6', width=3)))
    
    fig.add_hline(y=x_th, line_dash="dash", line_color="#ef4444")
    fig.add_hline(y=y_th, line_dash="dash", line_color="#22c55e")
    fig.add_hline(y=z_th, line_dash="dash", line_color="#3b82f6")
    
    fig.update_layout(
        template="plotly_dark",
        height=400,
        showlegend=True,
        legend=dict(orientation="h", y=-0.15),
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
        template="plotly_dark",
        height=400,
        scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z')
    )
    st.plotly_chart(fig3d, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- TABLE ----------------
with st.expander("📋 Raw Data", expanded=False):
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.dataframe(
        df[['time', 'X_exp', 'Y_exp', 'Z_exp']].tail(20),
        use_container_width=True,
        hide_index=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown(f"""
<div style='
    text-align: center; 
    padding: 2rem; 
    color: #64748b; 
    font-size: 0.9rem;
    border-top: 1px solid rgba(255,255,255,0.1);
'>
    🔥 Smart Boiler Monitor | Updated: <strong>{datetime.now().strftime("%H:%M:%S")}</strong>
</div>
""", unsafe_allow_html=True)