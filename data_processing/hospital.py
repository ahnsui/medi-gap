import csv
from common_module import get_db_connection, get_driver, close_db

connection, cursor = get_db_connection()


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

close_db(connection, cursor)