import csv
from common_module import get_db_connection, close_db

connection, cursor = get_db_connection()

with open('data/전국병원정보.csv', 'r', encoding='utf-8') as f:
    data = csv.DictReader(f)
    
    for item in data:
        hospital_name = item.get('\ufeff요양기관명')
        doctor_num = item.get('총의사수')
        lat = item.get('좌표(Y)')  # 위도
        lon = item.get('좌표(X)')  # 경도

        # float 변환
        lat = float(lat) if lat and lat.strip() else None
        lon = float(lon) if lon and lon.strip() else None

        # 주소
        address = item.get('주소')
        address_list = address.split()

        if address_list[0]=='세종특별자치시':
            region = address_list[:1]
        else:
            region = address_list[:2]
        
        if len(address_list) > 2 and address_list[2].endswith('구'):
            region.append(address_list[2])
        
        region_name = " ".join(region)
        
        sql = """
            INSERT INTO tbl_hospital (REGION_CODE, HOSPITAL_NAME, DOCTOR_NUM, LAT, LON)
            VALUES (
                (SELECT REGION_CODE FROM tbl_region R WHERE R.ADDRESS = %s),
                %s, %s, %s, %s
            )
        """
        cursor.execute(sql, (region_name, hospital_name, doctor_num, lat, lon))

connection.commit()
close_db(connection, cursor)
