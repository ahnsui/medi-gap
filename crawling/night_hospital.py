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
driver.get('https://www.goodoc.co.kr/hospitals/curation?managedTagName=달빛어린이병원&region=전국')
time.sleep(1)

articles = driver.find_elements(By.TAG_NAME, 'article')

# DB 저장
for article in articles:
    hospital_name = article.find_element(By.CSS_SELECTOR, 'span._1m3fjzl3').text
    region_name = article.find_element(By.CSS_SELECTOR, 'span._1m3fjzl0').text

    sql = 'INSERT INTO tbl_night_hospital(REGION_NAME, HOSPITAL_NAME) VALUES(%s, %s)'
    cursor.execute(sql, (region_name, hospital_name))

driver.quit()

# 커밋 및 종료
connection.commit()
cursor.close()
connection.close()
