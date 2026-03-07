import streamlit as st
import pandas as pd
import joblib
import os
from google.cloud import bigquery
from google.oauth2 import service_account

def get_bq_client():
    """Streamlit Secretsから認証情報を読み込み、改行コードを補正してクライアントを作成"""
    if "gcp_service_account" in st.secrets:
        # Secretsから辞書を取得
        info = dict(st.secrets["gcp_service_account"])
        
        # 【重要】private_key内の文字列としての \n を実際の改行文字に置換
        if "private_key" in info:
            info["private_key"] = info["private_key"].replace("\\n", "\n")
            
        credentials = service_account.Credentials.from_service_account_info(info)
        return bigquery.Client(credentials=credentials, project=info["project_id"])
    return None

st.set_page_config(page_title="Student Success AI", layout="wide")
st.title("🎓 大学生の習慣分析・成績向上アドバイザー")

# --- 1. 学習済みモデルの読み込み ---
try:
    model = joblib.load('student_model.pkl')
    st.sidebar.success("✅ 学習済みモデルをロードしました")
except Exception as e:
    st.sidebar.error(f"❌ モデルのロードに失敗: {e}")
    st.stop()

# --- 2. 予測シミュレーション ---
st.header("🔍 成績予測シミュレーション")

col1, col2 = st.columns(2)
with col1:
    study_hours_per_day = st.slider("1日の勉強時間", 0.0, 15.0, 7.3)
    sleep_hours = st.slider("睡眠時間 (時間)", 0.0, 12.0, 3.2)
with col2:
    social_media_hours = st.slider("SNS利用時間 (時間)", 0.0, 12.0, 2.0)
    attendance_percentage = st.slider("出席率 (%)", 0.0, 100.0, 14.0)

if st.button("AIで試験成績を予測する"):
    # 成功が確認された順序を維持
    columns_order = ['study_hours_per_day', 'sleep_hours', 'social_media_hours', 'attendance_percentage']
    input_values = [study_hours_per_day, sleep_hours, social_media_hours, attendance_percentage]
    input_df = pd.DataFrame([input_values], columns=columns_order)
    
    try:
        prediction = model.predict(input_df)[0]
        st.metric(label="AI予測スコア (exam_score)", value=f"{prediction:.1f} 点")
        
        if prediction >= 80:
            st.balloons()
            st.success("✨ 素晴らしい習慣です！")
        elif prediction < 60:
            st.warning("⚠️ 生活習慣の調整でさらなる向上が期待できます。")
            
    except Exception as e:
        st.error(f"予測エラーが発生しました: {e}")

# --- 3. BigQueryからの実績表示 ---
st.divider()
st.subheader("📊 BigQuery 実績データ確認")
client = get_bq_client()
if client:
    try:
        query = f"SELECT student_id, study_hours_per_day, sleep_hours, social_media_hours, attendance_percentage, exam_score FROM `{client.project}.student_data.habits_performance` LIMIT 10"
        df = client.query(query).to_dataframe()
        st.dataframe(df)
    except Exception as e:
        st.error(f"データ取得エラー: {e}")
else:
    st.info("💡 Secretsを設定してください。設定後、BigQueryの実績データが表示されます。")
