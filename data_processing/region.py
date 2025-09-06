import mysql.connector
from dotenv import load_dotenv
import os
import json
from collections import defaultdict

# env 불러오기
load_dotenv()
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DATABASE = os.getenv('DB_DATABASE')

# DB 연결
connection = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_DATABASE
)
cursor = connection.cursor()

# JSON 읽기
with open('data/지역별평균연령.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 시군구 단위로 평균 연령 계산
grouped = defaultdict(list)

for item in data:
    region_name = item.get('시도명')
    region_subname = item.get('시군구명')
    age = float(item.get('전체 평균연령'))
    grouped[(region_name, region_subname)].append(age)

# DB에 INSERT
for (region_name, region_subname), ages in grouped.items():
    avg_age = sum(ages) / len(ages)
    sql = "INSERT INTO tbl_region (REGION_NAME, REGION_SUBNAME, AVERAGE_AGE) VALUES (%s, %s, %s)"
    cursor.execute(sql, (region_name, region_subname, avg_age))

# 커밋 및 종료
connection.commit()
cursor.close()
connection.close()
