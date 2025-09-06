import mysql.connector
import urllib.request
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
REGION_API_KEY = os.getenv('REGION_API_KEY')


# OPEN API로 데이터 불러오기
base_url = "https://api.odcloud.kr/api/15099157/v1/uddi:99b0fc58-dcac-4041-bb0e-bb3c5d17531d"
all_data = []

for page in range(1, 5):
    url = f"{base_url}?page={page}&perPage=1000&serviceKey={REGION_API_KEY}"
    
    request = urllib.request.Request(url) 
    request.add_header('Authorization', REGION_API_KEY)
    
    response = urllib.request.urlopen(request)
    response_body = response.read()
    
    data = json.loads(response_body)
    all_data.extend(data.get("data", []))

# DB 연결
connection = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_DATABASE
)

cursor = connection.cursor()

# 시군구 단위로 평균 연령 계산
grouped = defaultdict(list)

for item in all_data:
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
