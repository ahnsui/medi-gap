import mysql.connector
from dotenv import load_dotenv
import os
import pandas as pd
import streamlit as st

st.subheader('전국 야간 어린이 병원')

# DB 연결
load_dotenv()
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DATABASE = os.getenv('DB_DATABASE')

connection = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_DATABASE
)

# 병원 수 집계
sql = """
SELECT
    REGION_NAME AS REGION,
    COUNT(*) AS HOSPITAL_COUNT
FROM tbl_night_hospital
GROUP BY REGION
ORDER BY HOSPITAL_COUNT DESC;
"""

df = pd.read_sql(sql, connection)
connection.close()

# 막대그래프
st.bar_chart(df.set_index('REGION')['HOSPITAL_COUNT'])
st.badge('지방의 다수 지역에서 응급 상황에 대비할 수 있는 의료 공백이 존재합니다', icon=":material/check:", color="green")