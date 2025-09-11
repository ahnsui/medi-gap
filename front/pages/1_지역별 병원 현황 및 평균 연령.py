import mysql.connector
from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# 폰트 설정
import matplotlib.font_manager as fm
import matplotlib

font_path = 'C:\\Windows\\Fonts\\gulim.ttc'
font = fm.FontProperties(fname=font_path).get_name()
matplotlib.rc('font', family=font)

st.subheader('지역별 병원 현황 및 평균 연령')

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

# 두 데이터프레임 merge해서 같은 순서 유지
merged_df = pd.merge(
    filtered_df,
    filtered_age,
    on="ADDRESS",
    suffixes=("", "_AGE")
)

fig, ax1 = plt.subplots(figsize=(10,6))

# 막대그래프 (병원/의사 수)
ax1.bar(merged_df["ADDRESS"], merged_df["HOSPITAL_COUNT"], color='blue', label="병원 수")
ax1.bar(merged_df["ADDRESS"], merged_df["DOCTOR_COUNT"], 
        bottom=merged_df["HOSPITAL_COUNT"], color='skyblue', label="의사 수")
ax1.set_ylabel("병원 & 의사 수")
ax1.tick_params(axis='x', rotation=45)

# 두 번째 y축 (평균 연령)
ax2 = ax1.twinx()
ax2.plot(merged_df["ADDRESS"], merged_df["AVERAGE_AGE"], 
         color='red', marker='o', label="평균 연령")
ax2.set_ylabel("평균 연령")

# 범례 합치기
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

st.pyplot(fig)

st.badge('고령 인구가 많은 지역일수록 의료 인프라 부족 문제가 더 두드러지는 경향이 있습니다', icon=":material/check:", color="green")
st.badge('농어촌 지역과 수도권 지역의 의료 접근성 격차가 매우 큰 것을 확인할 수 있습니다.', icon=":material/check:", color="green")