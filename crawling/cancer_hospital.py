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

# 동적 웹 크롤링
path = 'chromedriver.exe'
service = Service(path)
driver = webdriver.Chrome(service=service)

driver.get('https://www.e-gen.or.kr/cancer/hospitalList.do')
time.sleep(1)

search_btn = driver.find_element(By.XPATH, '//*[@id="btnSearch2"]')
search_btn.click()
time.sleep(1)

hospitals_elems = driver.find_elements(By.CSS_SELECTOR, 'tr.first')

# DB 저장
for hospital in hospitals_elems:
    region_name = hospital.find_element(By.CSS_SELECTOR, '.btn-custumed').text
    hospital_name = hospital.find_element(By.CSS_SELECTOR, '.emogtd').text

    sql = 'INSERT INTO tbl_cancer_hospital(REGION_NAME, HOSPITAL_NAME) VALUES(%s, %s)'
    cursor.execute(sql, (region_name, hospital_name))
    
driver.quit()

# 커밋 및 종료
connection.commit()
cursor.close()
connection.close()