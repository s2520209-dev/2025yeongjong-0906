import streamlit as st

import pandas as pd

from datetime import date

import os



# 1. 페이지 제목 및 소개

st.title('자원봉사자 현황 대시보드')

st.markdown("### 2024년 보건복지부의 자원봉사자 통계를 시각화합니다.")

st.write("이 데이터는 시설별, 시도별 자원봉사자 현황을 보여줍니다.")



# 2. 로컬에 있는 CSV 파일 불러오기

# 최신 data.csv 파일을 불러옵니다.



file_path = 'https://github.com/s2520209-dev/2025yeongjong-0906/blob/main/data.csv'+'?raw=true'

    

df = pd.read_csv(file_path, encoding='cp949', header=2)

st.dataframe(df)
