import mysql.connector
from dotenv import load_dotenv
import os
import pandas as pd
import streamlit as st

st.subheader('전국 암 진료 협력 병원')

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
    REGION_NAME,
    COUNT(*) AS HOSPITAL_COUNT
FROM tbl_cancer_hospital
GROUP BY REGION_NAME
ORDER BY HOSPITAL_COUNT DESC
"""

# 상세 암 진료 정보
sql_cancer = """
SELECT
    H.REGION_NAME AS 지역,
    H.HOSPITAL_NAME AS 병원,
    T.CANCER_TYPE AS 암,
    C.ALLOW_TREATMENT AS 항암치료,
    C.ALLOW_RADIATION AS 방사선치료,
    C.ALLOW_SURGERY AS 암수술
FROM tbl_cancer_hospital H 
JOIN tbl_cancer_care C USING(HOSPITAL_ID)
JOIN tbl_cancer_type T USING(CANCER_ID)
"""

df = pd.read_sql(sql, connection)
df_cancer = pd.read_sql(sql_cancer, connection)
connection.close()

# 막대그래프
st.bar_chart(df.set_index('REGION_NAME')['HOSPITAL_COUNT'])

regions = df_cancer['지역'].unique()
cancers = df_cancer['암'].unique()

selected_regions = st.multiselect("지역 선택", regions)
selected_cancers = st.multiselect("암 종류 선택", cancers)
treatment_only = st.checkbox("항암 치료 가능")
radiation_only = st.checkbox("방사선 치료 가능")
surgery_only = st.checkbox("암 수술 가능")

filtered_df = df_cancer.copy()

if selected_regions:
    filtered_df = filtered_df[filtered_df["지역"].isin(selected_regions)]
if selected_cancers:
    filtered_df = filtered_df[filtered_df["암"].isin(selected_cancers)]
if treatment_only:
    filtered_df = filtered_df[filtered_df["항암치료"] == 1]
if radiation_only:
    filtered_df = filtered_df[filtered_df["방사선치료"] == 1]
if surgery_only:
    filtered_df = filtered_df[filtered_df["암수술"] == 1]

st.write(f"총 {len(filtered_df)} 개 병원")
st.dataframe(filtered_df)
