import streamlit as st
import pandas as pd
import numpy as np
import os
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest

st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}
.metric-container {
    background-color: #1f2937;
    padding: 15px;
    border-radius: 10px;
}
h1, h2, h3 {
    color: #38bdf8;
}
</style>
""", unsafe_allow_html=True)


st.set_page_config(page_title="Smart Water Management", layout="wide")

st.title("💧 AI-Driven Smart Water Management System")
st.write("Real-time monitoring, AI analytics, and sustainability impact dashboard")

# ---- DATA CHECK ----
if not os.path.exists("water_data.csv"):
    st.error("❌ water_data.csv not found. Run data_generator.py first.")
    st.stop()

df = pd.read_csv("water_data.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])

st.success("✅ Data loaded successfully")
st.dataframe(df.head())

# ---- METRICS ----
today_usage = int(df.tail(24)["water_usage"].sum())
leak_count = (df["leak"] > 0).sum()

st.subheader("📊 System Overview")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
    st.metric("Today's Usage (Liters)", today_usage)
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
    st.metric("Total Leak Alerts", leak_count)
    st.markdown("</div>", unsafe_allow_html=True)

with c3:
    st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
    st.metric("System Status", "Stable" if leak_count < 3 else "Critical")
    st.markdown("</div>", unsafe_allow_html=True)


# ---- CHART ----
st.subheader("📈 Water Usage Trend")
st.line_chart(df.set_index("timestamp")["water_usage"])

# ---- LEAK ALERTS ----
st.subheader("🚨 Leak Detection")
leaks = df[df["leak"] > 0]
if len(leaks) > 0:
    for _, row in leaks.tail(3).iterrows():
        st.error(f"Leak detected at {row['timestamp']} | Extra usage: {row['leak']} L")
else:
    st.success("No leaks detected")

# ---- AI DEMAND PREDICTION ----
df["hour"] = range(len(df))
X = df[["hour"]]
y = df["water_usage"]

model = LinearRegression()
model.fit(X, y)

future_df = pd.DataFrame({"hour": [len(df) + 1]})
prediction = int(model.predict(future_df)[0])

st.subheader("🔮 AI Demand Forecast")
st.info(f"Predicted water usage for next hour: {prediction} Liters")

# ---- ANOMALY DETECTION ----
iso = IsolationForest(contamination=0.05)
df["anomaly"] = iso.fit_predict(df[["water_usage"]])

anomalies = df[df["anomaly"] == -1]
st.subheader("⚠️ AI Detected Anomalies")
if len(anomalies) > 0:
    st.warning(f"{len(anomalies)} abnormal consumption points found")
    st.dataframe(anomalies.tail(5))
else:
    st.success("No abnormal usage detected")

# ---- AI RECOMMENDATIONS ----
st.subheader("🤖 AI Recommendations")
if leak_count > 0:
    st.write("✔ Dispatch maintenance team")
if prediction > 140:
    st.write("✔ Reduce pressure during peak hours")
st.write("✔ Encourage water conservation awareness")

# ---- SUSTAINABILITY IMPACT ----
st.subheader("🌱 Sustainability Impact")

st.write("Water Wastage Reduction")
st.progress(35)

st.write("Energy Consumption Reduction")
st.progress(18)

st.write("CO₂ Emissions Reduction")
st.progress(25)

