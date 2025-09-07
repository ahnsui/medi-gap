from common_module import get_db_connection, get_driver, close_db
from dotenv import load_dotenv
import os
import urllib.request
import json
from collections import defaultdict

connection, cursor = get_db_connection()
load_dotenv()
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
    
    # json -> dictionary 후 리스트 붙이기
    data = json.loads(response_body)
    all_data.extend(data.get("data"))

# 시군구 단위로 평균 연령 계산
grouped = defaultdict(list)

for item in all_data:
    region_name = item.get('시도명')
    region_subname = item.get('시군구명')
    address = f"{region_name} {region_subname or ''}".strip()
    age = float(item.get('전체 평균연령'))
    grouped[address].append(age)

# DB에 INSERT
for address, ages in grouped.items():
    avg_age = round(sum(ages) / len(ages), 2)
    sql = "INSERT INTO tbl_region (ADDRESS, AVERAGE_AGE) VALUES (%s, %s)"
    cursor.execute(sql, (address, avg_age))

close_db(connection, cursor)

