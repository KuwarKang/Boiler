import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go

# ---------------- CONFIG ----------------
CHANNEL_ID = 3304820
READ_API = "1JBJZ0VWIC0JILIL"

st.set_page_config(layout="wide")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f172a, #020617);
}

.block-container {
    padding-top: 1rem;
}

.card {
    background: rgba(30,41,59,0.6);
    backdrop-filter: blur(12px);
    padding: 15px;
    border-radius: 16px;
    box-shadow: 0 0 20px rgba(0,0,0,0.4);
    margin-bottom: 15px;
}

.title {
    font-size: 28px;
    font-weight: bold;
    text-align: center;
}

.metric {
    font-size: 22px;
    font-weight: bold;
}

.alert {
    padding: 10px;
    border-radius: 10px;
    background: linear-gradient(90deg, #ef4444, #dc2626);
    text-align: center;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown('<div class="title">🔥 Smart Boiler Expansion Dashboard</div>', unsafe_allow_html=True)

# ---------------- INITIAL VALUES ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### ⚙️ Initial Calibration Values")

col1, col2, col3 = st.columns(3)

with col1:
    init_x = st.number_input("🔴 X Axis (mm)", value=10)

with col2:
    init_y = st.number_input("🟢 Y Axis (mm)", value=10)

with col3:
    init_z = st.number_input("🔵 Z Axis (mm)", value=10)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FETCH DATA ----------------
url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={READ_API}&results=50"
res = requests.get(url).json()

data = []
for f in res['feeds']:
    try:
        x = float(f['field1'])
        y = float(f['field2'])
        z = float(f['field3'])
        alarm = int(f['field4']) if f['field4'] else 0
        data.append([x,y,z,alarm])
    except:
        continue

df = pd.DataFrame(data, columns=['X','Y','Z','Alarm'])

# ---------------- SAFE CALCULATIONS ----------------
df['X_exp'] = (df['X'] - init_x).clip(lower=0)
df['Y_exp'] = (df['Y'] - init_y).clip(lower=0)
df['Z_exp'] = (df['Z'] - init_z).clip(lower=0)

# ---------------- KPI CARDS ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f'<div class="card"><div class="metric">🔴 X: {df["X_exp"].iloc[-1]:.2f} mm</div></div>', unsafe_allow_html=True)

with col2:
    st.markdown(f'<div class="card"><div class="metric">🟢 Y: {df["Y_exp"].iloc[-1]:.2f} mm</div></div>', unsafe_allow_html=True)

with col3:
    st.markdown(f'<div class="card"><div class="metric">🔵 Z: {df["Z_exp"].iloc[-1]:.2f} mm</div></div>', unsafe_allow_html=True)

# ---------------- ALERT ----------------
if ((df['X_exp']>10) | (df['Y_exp']>15) | (df['Z_exp']>8)).any():
    st.markdown('<div class="alert">🚨 LIMIT EXCEEDED</div>', unsafe_allow_html=True)

# ---------------- GRAPH ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)

fig = go.Figure()
fig.add_trace(go.Scatter(y=df['X_exp'], name='X', line=dict(color='#ef4444')))
fig.add_trace(go.Scatter(y=df['Y_exp'], name='Y', line=dict(color='#22c55e')))
fig.add_trace(go.Scatter(y=df['Z_exp'], name='Z', line=dict(color='#3b82f6')))

fig.update_layout(
    template="plotly_dark",
    height=400,
    margin=dict(l=10,r=10,t=10,b=10),
    xaxis_title="Time",
    yaxis_title="Expansion (mm)"
)

st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- 3D GRAPH ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)

fig3d = go.Figure(data=[go.Scatter3d(
    x=df['X_exp'],
    y=df['Y_exp'],
    z=df['Z_exp'],
    mode='lines+markers',
    marker=dict(size=3)
)])

fig3d.update_layout(
    template="plotly_dark",
    height=400,
    margin=dict(l=0,r=0,t=0,b=0),
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z'
    )
)

st.plotly_chart(fig3d, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- DATA TABLE ----------------
with st.expander("📊 View Raw Data"):
    st.dataframe(df)
