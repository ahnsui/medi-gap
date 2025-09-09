import mysql.connector
from dotenv import load_dotenv
import os
import pandas as pd
import streamlit as st

st.subheader('전국 병원 지도')

# DB 연결
load_dotenv()
connection = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_DATABASE')
)

# 병원 데이터 가져오기
sql = """
SELECT 
    H.HOSPITAL_NAME,
    H.LAT,
    H.LON,
    R.ADDRESS
FROM tbl_hospital H
JOIN tbl_region R USING(REGION_CODE)
WHERE H.LAT IS NOT NULL AND H.LON IS NOT NULL
"""
df = pd.read_sql(sql, connection)
connection.close()

# 지역별 병원 수 집계, 평균 좌표 계산
df_grouped = df.groupby("ADDRESS").agg(
    hospital_count=("HOSPITAL_NAME", "count"),
    lat=("LAT", "mean"),
    lon=("LON", "mean")
).reset_index()

df_grouped = df_grouped.rename(columns={"lat": "lat", "lon": "lon"})
df_grouped["size"] = df_grouped["hospital_count"] * 20  # 스케일 조정

# 지역별 색상 지정 (RGB 리스트)
regions = df_grouped["ADDRESS"].unique()
color_map = {region: [i*30 % 255, i*70 % 255, i*110 % 255] for i, region in enumerate(regions)}
df_grouped["color"] = df_grouped["ADDRESS"].apply(lambda x: color_map[x])

st.map(df_grouped, latitude="lat", longitude="lon", size="size", color="color")
