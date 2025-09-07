from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.service import Service
import mysql.connector
from dotenv import load_dotenv
import os

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

# Selenium 설정
path = 'chromedriver.exe'
service = Service(path)
driver = webdriver.Chrome(service=service)
driver.get('https://www.e-gen.or.kr/cancer/hospitalList.do')
time.sleep(1)

# 검색 버튼 클릭
search_btn = driver.find_element(By.XPATH, '//*[@id="btnSearch2"]')
search_btn.click()
time.sleep(1)

rows = driver.find_elements(By.CSS_SELECTOR, 'table tbody tr')
hospital_id = 0
cancer_id = 0

# DB 저장
for row in rows:
    class_name = row.get_attribute('class')
    td_list = row.find_elements(By.TAG_NAME, 'td')

    if class_name=='first':
        hospital_id += 1
        cancer_id = 1

        region_name = td_list[0].text
        hospital_name = td_list[1].text
        sql_hospital = 'INSERT INTO tbl_cancer_hospital(HOSPITAL_ID, REGION_NAME, HOSPITAL_NAME) VALUES(%s, %s, %s)'
        cursor.execute(sql_hospital, (hospital_id, region_name, hospital_name))

        allow_treatment = True if td_list[3].text == 'O' else False
        allow_radiation = True if td_list[4].text == 'O' else False
        allow_surgery = True if td_list[5].text == 'O' else False

        sql_type = 'INSERT INTO tbl_cancer_care(HOSPITAL_ID, CANCER_ID, ALLOW_TREATMENT, ALLOW_RADIATION, ALLOW_SURGERY) VALUES(%s, %s, %s, %s, %s)'
        cursor.execute(sql_type, (hospital_id, cancer_id, allow_treatment, allow_radiation, allow_surgery))
    else:
        cancer_id += 1
        if 0 < len(td_list[0].text) < 4:
            allow_treatment = True if td_list[1].text == 'O' else False
            allow_radiation = True if td_list[2].text == 'O' else False
            allow_surgery = True if td_list[3].text == 'O' else False

            sql_type = 'INSERT INTO tbl_cancer_care(HOSPITAL_ID, CANCER_ID, ALLOW_TREATMENT, ALLOW_RADIATION, ALLOW_SURGERY) VALUES(%s, %s, %s, %s, %s)'
            cursor.execute(sql_type, (hospital_id, cancer_id, allow_treatment, allow_radiation, allow_surgery))

driver.quit()

# 커밋 및 종료
connection.commit()
cursor.close()
connection.close()
