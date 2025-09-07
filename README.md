## 프로젝트 소개 
**지역 간 의료 격차 시각화 플랫폼**

건강보험심사평가원의 공공데이터(전국 병·의원 및 약국 현황)를 기반으로, 수도권과 지방의 의료 인프라 격차를 데이터 분석 및 시각화로 보여주는 웹 플랫폼을 구축한다. 병원·약국의 밀도, 장비 보유 현황, 야간·주말 진료 여부, 인구 대비 의료 접근성 등을 지표화하여 지역별 의료 수준을 평가하고, 사용자(일반인·고령층·정책 담당자)가 쉽게 확인할 수 있도록 제공한다.

**프로젝트 필요성**

대한민국은 의료 접근성 면에서 수도권과 지방 간의 격차가 크다는 지적이 꾸준히 제기되고 있다. 특히 고령인구 비중이 높은 농촌 지역에서는 가까운 병원·약국이 부족하거나 야간·주말 진료 공백이 발생해 실질적인 의료 사각지대가 형성된다. 그러나 이러한 문제는 체감 수준에 머무르는 경우가 많고, 객관적 데이터를 기반으로 한 비교·분석은 부족하다. 따라서 공공데이터와 크롤링 데이터를 활용해 격차를 정량적으로 보여주는 작업이 필요하다.

<img src='images\medi_gap_news.png' alt='news' />
<img src='images\medi_gap_news2.png' alt='news' />

[인구감소지역 의료접근성 문제 심각…의료기관 폐업률도 늘어](https://www.akomnews.com/bbs/board.php?bo_table=news&wr_id=61715)

<img src='images\medi_gap_children.png' alt='news' />

[붕괴 직면 소아청소년 의료, 비가역적 상황 내몰려](https://doctorsnews.co.kr/news/articleView.html?idxno=161032)

**프로젝트 목표**

1. 건강보험심사평가원 및 기타 공공데이터를 활용하여 지역별 의료 인프라 현황을 정량화한다.
2. 의료기관 밀도, 장비 가용성, 야간·주말 진료 가능 여부 등 핵심 지표를 도출한다.
3. 수도권과 지방 간의 의료 격차를 시각화(지도·차트)하여 누구나 직관적으로 확인할 수 있도록 한다.
4. 분석 결과를 토대로 각 지역별 맞춤형 정책·서비스 개선 방안을 제안한다.

## 데이터 셋

1. [전국 병의원 및 약국 현황](https://opendata.hira.or.kr/op/opc/selectOpenData.do?sno=11925)
    
2. [지역별(행정동) 성별 주민등록 평균연령](https://www.data.go.kr/data/15099157/fileData.do#layer_data_infomation)
    
3. [전국 암 진료 협력 병원 목록](https://www.e-gen.or.kr/cancer/hospitalList.do)
    
4. [전국 야간 어린이 병원 목록](https://www.goodoc.co.kr/hospitals/curation?managedTagName=%EB%8B%AC%EB%B9%9B%EC%96%B4%EB%A6%B0%EC%9D%B4%EB%B3%91%EC%9B%90&region=%EC%A0%84%EA%B5%AD)    

## 폴더 구조
```
├── crawling/
├── data/
├── data_processing/
├── front/
|	└── main.py           
|	└── pages/   
│		├── 1_chart.py                  # 지역별 병의원 및 약국 현황 & 평균 연령      
│		├── 2_cancer_hospitals.py       # 전국 암진료 협력 병원 목록   
│		└── 3_night_hospitals.py        # 전국 야간 어린이 병원 목록
├── images/
├── sql/
├── .env                      
├── .gitignore       
└── README.md
```


## 기술 스택

| 카테고리 | 기술 스택 |
| --- | --- |
| **WEB** | Streamlit |
| **라이브러리** | Pandas |
| **데이터베이스** | MySQL |
| **개발 환경** | Git,  VSCode,  Notion |



## ERD
<img src='images\ERD.png' alt='erd' />

