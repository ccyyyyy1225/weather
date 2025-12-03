import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import plotly.express as px
import json

# --- 設定 matplotlib 中文字型 ---
font_path = "NotoSansTC-VariableFont_wght.ttf"  # 字型檔路徑
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams["font.family"] = font_prop.get_name()
plt.rcParams["axes.unicode_minus"] = False

# --- Streamlit 頁面設定 ---
st.set_page_config(
    page_title="一週氣溫預報",
    layout="wide"
)

st.title("🌤️ 一週氣溫預報查詢系統")
st.markdown("資料來源：中央氣象署農業氣象預報（F-A0010-001）")

# --- 連線資料庫 ---
conn = sqlite3.connect("dataset.db")

# (A) 讀取全資料（地圖用）
df_all = pd.read_sql_query(
    "SELECT regionName, dataDate, mint, maxt FROM TemperatureForecasts",
    conn
)

# (B) 讀取所有地區名稱（下拉選單用）
regions_df = pd.read_sql_query(
    "SELECT DISTINCT regionName FROM TemperatureForecasts",
    conn
)
region_list = regions_df["regionName"].tolist()

# 側邊欄：地區選擇
st.sidebar.header("🔎 查詢設定")
selected_region = st.sidebar.selectbox("請選擇地區", region_list)

# (C) 讀取該地區詳細資料（折線圖用）
df = pd.read_sql_query(
    "SELECT dataDate, mint, maxt FROM TemperatureForecasts WHERE regionName = ? ORDER BY dataDate",
    conn,
    params=(selected_region,)
)

conn.close()

# ---------------- 台灣地圖（Plotly） ----------------
st.subheader("🗺️ 台灣地區氣溫熱度圖")

# 讀取 geojson
with open("taiwan_regions.geojson", "r", encoding="utf-8") as f:
    tw_geo = json.load(f)

# 計算平均溫度（每個地區）
df_map = df_all.groupby("regionName").agg(
    avg_temp=("maxt", "mean")
).reset_index()

# 畫地圖
fig_map = px.choropleth_mapbox(
    df_map,
    geojson=tw_geo,
    locations="regionName",
    featureidkey="properties.name",
    color="avg_temp",
    color_continuous_scale="YlOrRd",
    mapbox_style="carto-positron",
    zoom=6.3,
    center={"lat": 23.7, "lon": 121},
    opacity=0.7,
)

st.plotly_chart(fig_map, use_container_width=True)

# ---------------- 折線圖（當前地區） ----------------
st.subheader(f"📈 {selected_region} 溫度趨勢圖（最高 / 最低氣溫）")

fig, ax = plt.subplots()

ax.plot(df["dataDate"], df["maxt"], marker='o', label="最高氣溫")
ax.plot(df["dataDate"], df["mint"], marker='o', label="最低氣溫")

ax.set_title(f"{selected_region} 一週氣溫趨勢", fontproperties=font_prop)
ax.set_xlabel("日期", fontproperties=font_prop)
ax.set_ylabel("氣溫 (°C)", fontproperties=font_prop)

plt.xticks(rotation=45, fontproperties=font_prop)
plt.legend(prop=font_prop)

st.pyplot(fig)
