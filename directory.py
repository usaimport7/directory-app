import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

# Streamlitのsecretsからサービスアカウント情報を取得
service_account_info = json.loads(st.secrets["google_service_account"])
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# サービスアカウントの認証情報を使用
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)

# Googleスプレッドシートのデータを読み込む関数
def load_data_from_spreadsheet():
    client = gspread.authorize(creds)
    spreadsheet = client.open("directory_app")
    worksheet = spreadsheet.sheet1
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

# データの読み込み
df = load_data_from_spreadsheet()

# カテゴリと国の選択肢をセットアップ
categories = ['IT', '製造者', '雑貨', 'エネルギー/パワー', 'ハイテク小売/電子商取引', 'IoT/センサー', '製造業', '情報技術', '家電', 'テクノロジー', 'ソフトウェア', '自動車メーカー', '環境', '小売業', '通信業', '健康']
countries = df['Country'].unique()

# Streamlitのセレクトボックスを使用してユーザーに選択させる
selected_category = st.selectbox('カテゴリを選択', categories)
selected_country = st.selectbox('国を選択', countries)

# データフレームをフィルタリング
filtered_df = df[df['Category'].str.contains(selected_category, na=False) & (df['Country'] == selected_country)]

# 結果を表示
st.write(filtered_df)
