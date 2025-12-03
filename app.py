import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# --- 字型設定 (Noto Sans TC) ---
font_path = "NotoSansTC-VariableFont_wght.ttf"
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams["font.family"] = font_prop.get_name()
plt.rcParams["axes.unicode_minus"] = False

# --- Streamlit 基本設定 ---
st.set_page_config(page_title="一週氣溫預報", layout="wide")
st.markdown("""
<style>
/* ====== 氣象局風格卡片 ====== */
.weather-card {
    border-radius: 16px;
    padding: 18px 20px;
    color: white;
    font-size: 20px;
    font-weight: 600;
    text-align: left;
    margin-bottom: 12px;
    height: 80px;
    display: flex;
    align-items: center;
}

/* 卡片配色 */
.bg-blue   { background-color: #4a90e2; }
.bg-cyan   { background-color: #6ccff6; }
.bg-purple { background-color: #b090f8; }

/* 圖表置中 + 縮小 */
.center-plot {
    display: flex;
    justify-content: center;
}
.plot-box {
    width: 75%;
}
</style>
""", unsafe_allow_html=True)

# --- 標題 ---
st.title("🌤️ 一週氣溫預報查詢系統")
st.markdown("資料來源：中央氣象署農業氣象預報（F-A0010-001）")

# --- 讀取資料庫 ---
conn = sqlite3.connect("dataset.db")
df_all = pd.read_sql_query(
    "SELECT regionName, dataDate, mint, maxt FROM TemperatureForecasts",
    conn
)

regions = df_all["regionName"].unique()

# 卡片顏色配置
colors = ["bg-blue", "bg-cyan", "bg-purple"]

st.subheader("📍 各地區當週氣溫概況")

cols = st.columns(3)

selected_region = None

# --- 生成卡片 (官方氣象局風格) ---
for i, region in enumerate(regions):
    df_r = df_all[df_all["regionName"] == region]

    max_t = df_r["maxt"].max()
    min_t = df_r["mint"].min()
    card_color = colors[i % 3]

    with cols[i % 3]:
        if st.button(region, key=region):
            selected_region = region

        st.markdown(
            f"""
            <div class="weather-card {card_color}">
                <div>{region}<br>最高 {max_t}°C　最低 {min_t}°C</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# --- 若有點擊地區，顯示折線圖（中央氣象局風格） ---
if selected_region:
    st.markdown(f"## 📊 {selected_region} 一週溫度趨勢圖")

    df_show = df_all[df_all["regionName"] == selected_region].sort_values("dataDate")

    fig, ax = plt.subplots(figsize=(10, 4))  # ⭐ 圖片縮小

    ax.plot(df_show["dataDate"], df_show["maxt"], marker="o", label="最高氣溫")
    ax.plot(df_show["dataDate"], df_show["mint"], marker="o", label="最低氣溫")

    ax.set_title(f"{selected_region} — 一週氣溫變化", fontproperties=font_prop, fontsize=18)
    ax.set_xlabel("日期", fontproperties=font_prop)
    ax.set_ylabel("氣溫 (°C)", fontproperties=font_prop)

    plt.xticks(rotation=45, fontproperties=font_prop)
    plt.legend(prop=font_prop)
    plt.tight_layout()

    st.markdown("<div class='center-plot'><div class='plot-box'>", unsafe_allow_html=True)
    st.pyplot(fig)
    st.markdown("</div></div>", unsafe_allow_html=True)

conn.close()
