# 🌤️ 一週氣溫預報查詢系統

**A Streamlit Web App for Taiwan Weekly Temperature Forecast Visualization**

本專案提供台灣各地區的一週氣溫預報查詢，資料來源為中央氣象署農業氣象預報（F-A0010-001）。
使用 SQLite 儲存氣象資料，並以 Streamlit 展示地區卡片、日溫變化趨勢圖，
介面風格參考中央氣象局之 UI 進行設計，簡潔清楚、易於閱讀。

---

## 📌 Demo（線上展示頁面）

👉 **Streamlit Cloud:**
（https://weather-7zhaynkyrallvucyu3h6oc.streamlit.app/）

---

## 📁 專案結構

```
weather-app/
│── app.py                 # 主程式（Streamlit）
│── dataset.db             # SQLite 資料庫
│── NotoSansTC-VariableFont_wght.ttf  # 中文字型
│── requirements.txt       # 套件環境
│── README.md              # 專案說明
```

---

## 🚀 功能特色 Features

### 🌡️ 即時氣象資料呈現

* 讀取 SQLite 氣象資料庫（dataset.db）
* 顯示各地區最高、最低、平均氣溫

### 🗂️ 多地區氣象卡片（氣象局 UI）

* 將六大地區以卡片方式呈現
* 官方配色風格：藍色、青色、紫色
* 每張卡片顯示：

  * 地區名稱
  * 當週最高氣溫
  * 當週最低氣溫
* 點擊卡片即可查看該地區的詳細趨勢圖

### 📈 一週氣溫趨勢圖

* 顯示：

  * 最高氣溫趨勢
  * 最低氣溫趨勢
* 中文字型正常呈現（NotoSansTC）
* 圖表縮小置中，版面更一致

### 📱 響應式設計

* 自動適應電腦與手機版
* 三欄式卡片佈局

---

## 🔧 使用技術 Tech Stack

* **Python 3.10+**
* **Streamlit** — 建置前端互動式應用程式
* **SQLite** — 儲存氣象資料
* **Pandas** — 數據處理
* **Matplotlib** — 畫折線圖
* **Noto Sans TC** — 中文字體

---

## 📦 安裝 Installation

1. 下載或 Clone 專案：

```bash
git clone https://github.com/你的帳號/weather-app.git
cd weather-app
```

2. 安裝套件：

```bash
pip install -r requirements.txt
```

3. 執行 Streamlit：

```bash
streamlit run app.py
```

---

## 🗄 資料庫格式 (dataset.db)

`TemperatureForecasts` 資料表包含：

| 欄位名稱       | 說明   |
| ---------- | ---- |
| regionName | 地區名稱 |
| dataDate   | 預報日期 |
| mint       | 最低氣溫 |
| maxt       | 最高氣溫 |


---

## 🔒 資料來源 Data Source

資料來源：**中央氣象署農業氣象預報（F-A0010-001）**
[https://opendata.cwa.gov.tw/](https://opendata.cwa.gov.tw/)
