import mysql.connector
from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# DB 연결
def get_db_connection():
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
    cursor = connection.cursor()
    return connection, cursor

# Selenium 드라이버 생성
def get_driver(chrome_path='chromedriver.exe'):
    service = Service(chrome_path)
    driver = webdriver.Chrome(service=service)
    return driver

# DB 종료
def close_db(connection, cursor):
    connection.commit()
    cursor.close()
    connection.close()
