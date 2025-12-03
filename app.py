import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# 如果字型沒有就自動忽略，不會壞掉
try:
    plt.rcParams['font.family'] = 'Microsoft JhengHei'
except Exception:
    pass

st.set_page_config(
    page_title="一週氣溫預報",
    layout="wide"
)

st.title("🌤️ 一週氣溫預報查詢系統")
st.markdown("資料來源：中央氣象署農業氣象預報（F-A0010-001）")

# 連線到 SQLite（假設 data.db 跟 app.py 放在同一層）
conn = sqlite3.connect("data.db")

# 取得所有地區名稱
regions_df = pd.read_sql_query(
    "SELECT DISTINCT regionName FROM TemperatureForecasts",
    conn
)
region_list = regions_df["regionName"].tolist()

# 側邊欄選單
st.sidebar.header("🔎 查詢設定")
selected_region = st.sidebar.selectbox("請選擇地區", region_list)

# 查詢該地區資料
query = """
SELECT dataDate, mint, maxt
FROM TemperatureForecasts
WHERE regionName = ?
ORDER BY dataDate
"""
df = pd.read_sql_query(query, conn, params=(selected_region,))

conn.close()

# 主畫面顯示
st.subheader(f"📋 {selected_region} 一週氣溫資料表")
st.dataframe(df, use_container_width=True)

st.subheader("📈 溫度趨勢圖（最高 / 最低氣溫）")
fig, ax = plt.subplots()
ax.plot(df["dataDate"], df["maxt"], marker='o', label="最高氣溫")
ax.plot(df["dataDate"], df["mint"], marker='o', label="最低氣溫")
ax.set_ylabel("氣溫 (°C)")
ax.set_xlabel("日期")
ax.set_title(f"{selected_region} 一週氣溫趨勢")
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()

st.pyplot(fig)

