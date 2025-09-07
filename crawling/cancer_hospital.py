from selenium.webdriver.common.by import By
import time
from common_module import get_db_connection, get_driver, close_db

connection, cursor = get_db_connection()

driver = get_driver()
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

        allow_treatment = td_list[3].text
        allow_radiation = td_list[4].text
        allow_surgery = td_list[5].text

        sql_type = 'INSERT INTO tbl_cancer_care(HOSPITAL_ID, CANCER_ID, ALLOW_TREATMENT, ALLOW_RADIATION, ALLOW_SURGERY) VALUES(%s, %s, %s, %s, %s)'
        cursor.execute(sql_type, (hospital_id, cancer_id, allow_treatment, allow_radiation, allow_surgery))
    else:
        cancer_id += 1
        if 0 < len(td_list[0].text) < 4:
            allow_treatment = td_list[1].text
            allow_radiation = td_list[2].text
            allow_surgery = td_list[3].text

            sql_type = 'INSERT INTO tbl_cancer_care(HOSPITAL_ID, CANCER_ID, ALLOW_TREATMENT, ALLOW_RADIATION, ALLOW_SURGERY) VALUES(%s, %s, %s, %s, %s)'
            cursor.execute(sql_type, (hospital_id, cancer_id, allow_treatment, allow_radiation, allow_surgery))

driver.quit()
close_db(connection, cursor)
