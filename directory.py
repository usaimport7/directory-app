import streamlit as st
import pandas as pd
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
import os

# 環境変数からJSONキーファイルのパスを取得
json_keyfile_path = os.getenv("JSON_KEYFILE_PATH")
# Secretsから認証情報を読み込む
service_account_info = json.loads(st.secrets["google_service_account"])
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)

# Googleスプレッドシートの認証とデータの読み込み
def load_data_from_spreadsheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_path, scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open("directory_app")
    worksheet = spreadsheet.sheet1
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

# データの読み込み
df = load_data_from_spreadsheet()

# カテゴリの選択肢をセットアップ
categories = ['IT', '製造者', '雑貨', 'エネルギー/パワー', 'ハイテク小売/電子商取引', 'IoT/センサー', '製造業', '情報技術', '家電', 'テクノロジー', 'ソフトウェア', '自動車メーカー', '環境', '小売業', '通信業', '健康']

# Streamlitのセレクトボックスを使用してユーザーに選択させる
selected_category = st.selectbox('カテゴリを選択', categories)

# 国の選択肢をセットアップ
countries = df['Country'].unique()

# Streamlitのセレクトボックスを使用してユーザーに選択させる
selected_country = st.selectbox('国を選択', countries)

# データフレームをフィルタリング
filtered_df = df[df['Category'].str.contains(selected_category) & (df['Country'] == selected_country)]

# 結果を表示
st.write(filtered_df)
