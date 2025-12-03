import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# --- 設定中文字型 ---
font_path = "NotoSansTC-VariableFont_wght.ttf"
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams["font.family"] = font_prop.get_name()
plt.rcParams["axes.unicode_minus"] = False

# --- Streamlit 設定 ---
st.set_page_config(page_title="一週氣溫預報", layout="wide")

st.title("🌤️ 一週氣溫預報查詢系統")
st.markdown("資料來源：中央氣象署農業氣象預報（F-A0010-001）")

# --- 連線資料庫 ---
conn = sqlite3.connect("dataset.db")

# (A) 讀取全資料
df_all = pd.read_sql_query(
    "SELECT regionName, dataDate, mint, maxt FROM TemperatureForecasts",
    conn
)

# (B) 取得地區清單
regions = df_all["regionName"].unique()

# --- 卡片 UI 樣式 ---
card_style = """
<style>
.card {
    padding: 15px;
    border-radius: 15px;
    color: white;
    margin-bottom: 10px;
}
</style>
"""
st.markdown(card_style, unsafe_allow_html=True)

# --- 產生地區卡片 ---
st.subheader("📍 各地區溫度概況")

cols = st.columns(3)

region_to_color = {
    "北部地區": "#d1495b",
    "中部地區": "#f79256",
    "南部地區": "#fbd1a2",
    "東北部地區": "#9db4c0",
    "東部地區": "#6699cc",
    "東南部地區": "#bc6ff1"
}

selected_region = None

for i, region in enumerate(regions):
    df_r = df_all[df_all["regionName"] == region]
    max_t = df_r["maxt"].max()
    min_t = df_r["mint"].min()
    avg_t = df_r["maxt"].mean()

    with cols[i % 3]:
        if st.button(
            f"🌎 {region}\n最高:{max_t}°C  最低:{min_t}°C",
            key=region,
            help="點擊查看詳細資料",
        ):
            selected_region = region

        st.markdown(
            f"""
            <div class="card" style="background-color:{region_to_color.get(region, '#888')}">
                <h4>{region}</h4>
                <p>平均氣溫：{avg_t:.1f}°C</p>
                <p>最高氣溫：{max_t}°C</p>
                <p>最低氣溫：{min_t}°C</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# --- 若有點選地區 → 顯示折線圖 ---
if selected_region:
    st.subheader(f"📈 {selected_region} 一週溫度趨勢圖")

    df_show = df_all[df_all["regionName"] == selected_region].sort_values("dataDate")

    fig, ax = plt.subplots()
    ax.plot(df_show["dataDate"], df_show["maxt"], marker='o', label="最高氣溫")
    ax.plot(df_show["dataDate"], df_show["mint"], marker='o', label="最低氣溫")

    ax.set_title(f"{selected_region} 一週氣溫變化", fontproperties=font_prop)
    ax.set_xlabel("日期", fontproperties=font_prop)
    ax.set_ylabel("氣溫 (°C)", fontproperties=font_prop)

    plt.xticks(rotation=45, fontproperties=font_prop)
    plt.legend(prop=font_prop)

    st.pyplot(fig)

conn.close()
