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
    layout="wide"
)

# ---------------- CLEAN UI CSS ----------------
st.markdown("""
<style>
body {
    color: #f1f5f9;
    font-family: 'Segoe UI', sans-serif;
}

.main {
    background: linear-gradient(145deg, #0a0e1a, #0f172a);
}

.header {
    background: linear-gradient(135deg, #1e3a8a, #3b82f6);
    padding: 2rem;
    border-radius: 16px;
    text-align: center;
    color: white;
    margin-bottom: 20px;
}

.card {
    background: rgba(255,255,255,0.05);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
}

.metric {
    font-size: 2rem;
    font-weight: bold;
    color: white;
}

.label {
    color: #94a3b8;
    font-size: 0.8rem;
}

.alert {
    background: #ef4444;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    color: white;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙️ Settings")

    col1, col2, col3 = st.columns(3)
    with col1:
        init_x = st.number_input("X", value=10.0)
    with col2:
        init_y = st.number_input("Y", value=10.0)
    with col3:
        init_z = st.number_input("Z", value=10.0)

    x_th = st.slider("X Limit", 5.0, 20.0, 10.0)
    y_th = st.slider("Y Limit", 10.0, 30.0, 15.0)
    z_th = st.slider("Z Limit", 5.0, 15.0, 8.0)

# ---------------- HEADER ----------------
st.markdown("""
<div class="header">
<h2>🔥 Smart Boiler Expansion Monitor</h2>
<p>Real-time Monitoring Dashboard</p>
</div>
""", unsafe_allow_html=True)

# ---------------- FETCH DATA ----------------
@st.cache_data(ttl=60)
def fetch():
    url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={READ_API}&results=50"
    res = requests.get(url).json()

    data = []
    for f in res['feeds']:
        try:
            x = float(f['field1'] or 0)
            y = float(f['field2'] or 0)
            z = float(f['field3'] or 0)
            t = f['created_at']
            data.append([t,x,y,z])
        except:
            continue

    df = pd.DataFrame(data, columns=['time','X','Y','Z'])
    return df

df = fetch()

if df.empty:
    st.warning("No data")
    st.stop()

# ---------------- CALCULATIONS ----------------
df['X_exp'] = (df['X'] - init_x).clip(lower=0)
df['Y_exp'] = (df['Y'] - init_y).clip(lower=0)
df['Z_exp'] = (df['Z'] - init_z).clip(lower=0)

latest = df.iloc[-1]

# ---------------- METRICS ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f'<div class="card"><div class="metric">{latest["X_exp"]:.2f}</div><div class="label">X Axis</div></div>', unsafe_allow_html=True)

with col2:
    st.markdown(f'<div class="card"><div class="metric">{latest["Y_exp"]:.2f}</div><div class="label">Y Axis</div></div>', unsafe_allow_html=True)

with col3:
    st.markdown(f'<div class="card"><div class="metric">{latest["Z_exp"]:.2f}</div><div class="label">Z Axis</div></div>', unsafe_allow_html=True)

# ---------------- ALERT ----------------
if (latest['X_exp']>x_th) or (latest['Y_exp']>y_th) or (latest['Z_exp']>z_th):
    st.markdown('<div class="alert">🚨 LIMIT EXCEEDED</div>', unsafe_allow_html=True)

# ---------------- GRAPH ----------------
fig = go.Figure()

fig.add_trace(go.Scatter(y=df['X_exp'], name='X'))
fig.add_trace(go.Scatter(y=df['Y_exp'], name='Y'))
fig.add_trace(go.Scatter(y=df['Z_exp'], name='Z'))

fig.update_layout(template="plotly_dark", height=400)

st.plotly_chart(fig, use_container_width=True)

# ---------------- 3D GRAPH ----------------
fig3d = go.Figure(data=[go.Scatter3d(
    x=df['X_exp'],
    y=df['Y_exp'],
    z=df['Z_exp'],
    mode='lines+markers'
)])

fig3d.update_layout(template="plotly_dark", height=400)

st.plotly_chart(fig3d, use_container_width=True)

# ---------------- TABLE ----------------
with st.expander("Data"):
    st.dataframe(df)

# ---------------- FOOTER ----------------
st.markdown(f"""
<div style='text-align:center; padding:20px; color:#64748b'>
Updated: {datetime.now().strftime("%H:%M:%S")}
</div>
""", unsafe_allow_html=True)