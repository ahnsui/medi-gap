-- 유저에게 권한 설정
CREATE USER sui@'%' IDENTIFIED BY 'sui';

-- DB 생성
CREATE DATABASE hospitaldb;
GRANT ALL PRIVILEGES ON hospitaldb.* TO sui@'%';