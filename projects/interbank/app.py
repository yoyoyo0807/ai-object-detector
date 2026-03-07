import streamlit as st
import pandas as pd
import joblib
import os
import json
import base64
from google.cloud import bigquery
from google.oauth2 import service_account

# ページ設定
st.set_page_config(page_title="Student Success AI", layout="wide")

def get_bq_client():
    if "gcp_service_account" in st.secrets:
        encoded_key = st.secrets["GCP_SERVICE_ACCOUNT_BASE64"]
        decoded_key = base64.b64decode(encoded_key).decode("utf-8")
        info = json.loads(decoded_key)
        info["private_key"] = info["private_key"].replace("\\n", "\n")
        credentials = service_account.Credentials.from_service_account_info(info)
        return bigquery.Client(credentials=credentials, project=info["project_id"])
    return None

st.title("🎓 大学生の習慣分析・成績向上アドバイザー")

# --- 1. 学習済みモデルの読み込み ---
try:
    # 以前作成した学習済みモデルファイルを読み込む
    model = joblib.load('student_model.pkl')
    st.sidebar.success("✅ 学習済みモデルをロードしました")
except Exception as e:
    st.sidebar.error(f"❌ モデルのロードに失敗: {e}")
    st.stop()

# --- 2. 予測のためのユーザー入力フォーム ---
st.header("🔍 成績予測シミュレーション")
col1, col2 = st.columns(2)

with col1:
    study_hours = st.slider("1日の勉強時間 (時間)", 0.0, 15.0, 5.0)
    sleep_hours = st.slider("1日の睡眠時間 (時間)", 0.0, 12.0, 7.0)

with col2:
    attendance = st.slider("講義の出席率 (%)", 0, 100, 90)
    prev_score = st.number_input("前回の試験スコア", 0, 100, 70)

# 予測実行ボタン
if st.button("AIで試験成績を予測する"):
    # モデルに渡す形式に整形
    input_data = pd.DataFrame([[study_hours, sleep_hours, attendance, prev_score]], 
                              columns=['study_hours', 'sleep_hours', 'attendance', 'prev_score'])
    
    prediction = model.predict(input_data)[0]
    st.metric(label="予測スコア", value=f"{prediction:.1f} 点")
    
    # 分析に基づいた一言アドバイス
    if prediction < 60:
        st.warning("⚠️ 生活習慣を見直すことで、スコアがさらに伸びる可能性があります！")
    else:
        st.info("✨ 素晴らしい習慣です！この調子で継続しましょう。")

# --- 3. BigQueryからのデータ表示（実績確認） ---
st.divider()
st.subheader("📊 実際の学習データ (BigQuery)")
client = get_bq_client()
if client:
    df = client.query(f"SELECT * FROM `{client.project}.student_data.habits_performance` LIMIT 5").to_dataframe()
    st.dataframe(df)

