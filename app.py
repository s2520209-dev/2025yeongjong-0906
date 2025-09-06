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

except Exception as e:
    st.error("파일을 불러오는 중 오류가 발생했습니다.")
    st.write(f"오류 내용: {e}")
    st.write("GitHub 저장소의 **사용자 이름**, **저장소 이름**, **브랜치 이름**이 정확한지 확인해주세요.")
    st.stop()


# 3. 주요 통계 정보를 metric으로 시각화
st.write("---")
st.header("주요 통계 정보")
st.write("전국의 자원봉사자 수 현황을 전광판 형태로 확인할 수 있습니다.")

# '계' 행에서 전체 데이터 추출
total_row = df.loc[df['시도별'] == '계']

if not total_row.empty:
    # 데이터 타입 변환 (콤마 제거 후 정수로 변환)
    total_registered = int(total_row['등록자원봉사자'].item().replace(',', ''))
    total_active = int(total_row['활동자원봉사자'].item().replace(',', ''))
    
    # 두 개의 열을 구성하여 metric 표시
    col1, col2 = st.columns(2)
    col1.metric("총 등록자원봉사자", f"{total_registered:,} 명")
    col2.metric("총 활동자원봉사자", f"{total_active:,} 명")
else:
    st.warning("전체 합계('계') 데이터가 없어 metric을 표시할 수 없습니다.")


# 4. 차트로 데이터 시각화하기
st.write("---")
st.header("자원봉사 현황 차트")

# 시도별 활동자원봉사자 막대 그래프
# '계' 행을 제외하고 데이터 시각화
city_df = df[df['시도별'] != '계'].copy()
# 활동자원봉사자 열의 데이터를 정수형으로 변환
city_df['활동자원봉사자'] = city_df['활동자원봉사자'].str.replace(',', '').astype(int)

st.markdown("##### 시도별 활동자원봉사자 현황")
st.bar_chart(city_df, x='시도별', y='활동자원봉사자')


# 사회복지 분야별 활동자원봉사자 막대 그래프 (전국 기준)
# 사회복지 세부 항목 추출
social_welfare_cols = ['아동시설', '노인시설', '장애인시설', '여성복지시설', '정신요양시설', '노숙인복지시설', '복지관', '법인/단체']
social_welfare_df = total_row[social_welfare_cols].T
social_welfare_df.columns = ['활동인원']
social_welfare_df.index.name = '시설종류'
# 활동인원 열의 데이터를 정수형으로 변환
social_welfare_df['활동인원'] = social_welfare_df['활동인원'].str.replace(',', '').astype(int)

st.markdown("##### 사회복지 분야별 활동자원봉사자 (전국)")
st.bar_chart(social_welfare_df)

# 지도 차트는 데이터에 위도, 경도 정보가 없어 포함하지 않습니다.

# 5. 다양한 입력 기능과 폼
st.write("---")
st.header("자원봉사 활동 의견 제출")
st.write("자원봉사 활동에 대한 소중한 의견을 남겨주세요.")

# with st.form을 사용하여 입력 내용을 한 번에 제출
with st.form('자원봉사 의견'):
    d = st.date_input("활동 날짜를 선택해주세요.")
    w = st.selectbox("가장 기억에 남는 활동 분야를 선택해주세요.", social_welfare_cols)
    c = st.text_area("활동 후기를 남겨주세요.", placeholder="자유롭게 후기를 작성해주세요.")
    s = st.slider("활동 만족도를 선택해주세요.", 1, 5, 3)
    r = st.radio("앞으로도 자원봉사 활동에 참여할 의사가 있나요?", ["예", "아니오"])
    submitted = st.form_submit_button('제출')

# 제출 내용 확인
if submitted:
    st.balloons()
    st.success("의견이 성공적으로 제출되었습니다!")
    st.write(f"""
        **제출된 내용:**
        - **활동 날짜:** {d}
        - **활동 분야:** {w}
        - **후기:** {c}
        - **만족도:** {s}점
        - **재참여 의사:** {r}
    """)
