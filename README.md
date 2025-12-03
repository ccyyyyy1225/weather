# 一週氣溫預報系統

## 專案說明
這是「機器學習與應用 / AIoT 作業 HW4」的實作專案。

主要功能：
- 使用中央氣象署農業氣象預報 API（F-A0010-001）取得六大地區未來一週氣溫資料。
- 將資料整理後儲存進 SQLite 資料庫 `data.db` 的 `TemperatureForecasts` 資料表。
- 使用 Streamlit 建立網頁介面，提供地區下拉選單，顯示：
  - 一週氣溫資料表
  - 最高 / 最低氣溫折線圖

## 檔案說明
- `app.py`：Streamlit 主程式，讀取 `data.db` 並顯示表格與折線圖。
- `data.db`：SQLite 資料庫，內含 TemperatureForecasts 資料表。
- `hw4_all_steps.py`：HW4-1 ~ HW4-3 在 Colab 實作的整合程式碼（包含呼叫 API、解析 JSON、寫入 SQLite 等過程）。
- `requirements.txt`：專案所需套件列表。
- `README.md`：專案說明文件。

## 本機執行方式
1. 安裝套件：
   ```bash
   pip install -r requirements.txt
