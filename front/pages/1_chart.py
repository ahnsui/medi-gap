import mysql.connector
from dotenv import load_dotenv
import os
import pandas as pd
import streamlit as st

st.subheader('지역별 병원 현황')

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

sql = """
SELECT 
    R.ADDRESS,
    R.AVERAGE_AGE,
    COUNT(*) AS HOSPITAL_COUNT,
    SUM(H.DOCTOR_NUM) AS DOCTOR_COUNT
FROM tbl_region R
JOIN tbl_hospital H USING(REGION_CODE)
GROUP BY R.REGION_CODE, R.ADDRESS
ORDER BY HOSPITAL_COUNT DESC
"""

sql_age = """
SELECT 
    ADDRESS,
    AVERAGE_AGE
FROM tbl_region
"""

# SQL 실행 후 DataFrame 생성
df = pd.read_sql(sql, connection)
df_age = pd.read_sql(sql_age, connection)

connection.close()

# 지역 목록 가져오기
regions = df["ADDRESS"].unique()
selected_regions = st.multiselect("2개 이상의 지역을 선택해주세요", regions, default=['서울특별시 강남구', '서울특별시 서초구', '울산광역시 동구', '경상북도 영덕군'] )

filtered_df = df[df["ADDRESS"].isin(selected_regions)]
filtered_age = df_age[df_age["ADDRESS"].isin(selected_regions)]

# 병원 & 의사 수 차트
st.bar_chart(filtered_df.set_index("ADDRESS")[["HOSPITAL_COUNT", "DOCTOR_COUNT"]], stack=False)

st.subheader('지역별 평균 연령')

# 평균 연령 차트
st.line_chart(filtered_age.set_index("ADDRESS")["AVERAGE_AGE"], color='#FF0000')
