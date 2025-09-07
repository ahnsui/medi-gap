import mysql.connector
from dotenv import load_dotenv
import os
import csv

load_dotenv()
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DATABASE = os.getenv('DB_DATABASE')

connection = mysql.connector.connect(
    host = DB_HOST,
    user = DB_USER,
    password = DB_PASSWORD,
    database = DB_DATABASE
)

cursor = connection.cursor()

with open('data/전국병원정보.csv', 'r', encoding='utf-8') as f:
    data = csv.DictReader(f)
    
    for item in data:
        hospital_name = item.get('\ufeff요양기관명')
        doctor_num = item.get('총의사수')

        # 주소
        address = item.get('주소')
        address_list = address.split()

        if address_list[0]=='세종특별자치시':
            region = address_list[:1]
        else:
            region = address_list[:2]
        
        # 끝 글자가 '구'인 경우 추가
        if address_list[2].endswith('구'):
            region.append(address_list[2])
        
        region_name = " ".join(region)
        
        sql = """
            INSERT INTO tbl_hospital (REGION_CODE, HOSPITAL_NAME, DOCTOR_NUM)
            VALUES ((SELECT REGION_CODE FROM tbl_region R WHERE R.ADDRESS = %s), %s, %s)
        """
        cursor.execute(sql, (region_name, hospital_name, doctor_num))

# 커밋 및 종료
connection.commit()
cursor.close()
connection.close()