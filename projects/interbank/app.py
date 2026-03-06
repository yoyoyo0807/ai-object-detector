import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
import os

if "gcp_service_account" in st.secrets:
    info = dict(st.secrets["gcp_service_account"])
    # 秘密鍵の改行をプログラム側で強制修正
    info["private_key"] = info["private_key"].replace("\\n", "\n").strip()
    
    credentials = service_account.Credentials.from_service_account_info(info)
    client = bigquery.Client(credentials=credentials, project=info["project_id"])
    st.success("BigQueryに接続しました！")
    
    # テストクエリ
    df = client.query(f"SELECT * FROM `{client.project}.student_data.habits_performance` LIMIT 5").to_dataframe()
    st.dataframe(df)
else:
    st.error("Secretsが設定されていません。")
