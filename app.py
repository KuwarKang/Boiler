import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import numpy as np

# ---------------- CONFIG ----------------
CHANNEL_ID = 3304820
READ_API = "1JBJZ0VWIC0JILIL"

st.set_page_config(layout="wide")

st.title("🔥 Smart Boiler Expansion Dashboard")

# ---------------- USER INPUT ----------------
initial = st.number_input("Enter Initial Value (mm)", value=10)

# ---------------- FETCH DATA ----------------
url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={READ_API}&results=100"
res = requests.get(url).json()

feeds = res['feeds']

data = []

for f in feeds:
    try:
        x = float(f['field1'])
        y = float(f['field2'])
        z = float(f['field3'])
        alarm = int(f['field4']) if f['field4'] else 0

        data.append([x,y,z,alarm])
    except:
        continue

df = pd.DataFrame(data, columns=['X','Y','Z','Alarm'])

# ---------------- CALCULATIONS ----------------
df['X_exp'] = df['X'] - initial
df['Y_exp'] = df['Y'] - initial
df['Z_exp'] = df['Z'] - initial

# ---------------- ALARM LOGIC ----------------
df['Alert'] = ((abs(df['X_exp'])>10) | (abs(df['Y_exp'])>15) | (abs(df['Z_exp'])>8))

# ---------------- DISPLAY TABLE ----------------
st.subheader("📊 Data Table")
st.dataframe(df)

# ---------------- LINE GRAPH ----------------
st.subheader("📈 Expansion Trends")

fig = go.Figure()
fig.add_trace(go.Scatter(y=df['X_exp'], name='X', line=dict(color='red')))
fig.add_trace(go.Scatter(y=df['Y_exp'], name='Y', line=dict(color='green')))
fig.add_trace(go.Scatter(y=df['Z_exp'], name='Z', line=dict(color='blue')))

fig.update_layout(
    template="plotly_dark",
    xaxis_title="Time",
    yaxis_title="Expansion (mm)"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- 3D GRAPH ----------------
st.subheader("📊 3D Expansion Visualization")

fig3d = go.Figure(data=[go.Scatter3d(
    x=df['X_exp'],
    y=df['Y_exp'],
    z=df['Z_exp'],
    mode='lines+markers',
    marker=dict(size=3)
)])

fig3d.update_layout(
    template="plotly_dark",
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z'
    )
)

st.plotly_chart(fig3d, use_container_width=True)

# ---------------- ALERT ----------------
if df['Alert'].any():
    st.error("🚨 ALERT: Expansion Limit Exceeded!")
else:
    st.success("✅ System Normal")

# ---------------- AI PREDICTION ----------------
st.subheader("🧠 Prediction")

if len(df) > 2:
    pred_x = df['X_exp'].iloc[-1] + (df['X_exp'].iloc[-1] - df['X_exp'].iloc[-2])
    pred_y = df['Y_exp'].iloc[-1] + (df['Y_exp'].iloc[-1] - df['Y_exp'].iloc[-2])
    pred_z = df['Z_exp'].iloc[-1] + (df['Z_exp'].iloc[-1] - df['Z_exp'].iloc[-2])

    st.write(f"Next Predicted X: {pred_x:.2f}")
    st.write(f"Next Predicted Y: {pred_y:.2f}")
    st.write(f"Next Predicted Z: {pred_z:.2f}")