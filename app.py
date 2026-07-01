Python
import streamlit as st
import pandas as pd
import pytesseract
from PIL import Image
import re

# 엑셀 업로드 양식에 맞춘 전체 컬럼 구성
EXCEL_COLUMNS = [
    '호선번호', '문서종류', '공종코드', '코멘트\nSequence', '선주코멘트\nSequence', '호선번호\nORG', '문서종류\nORG', '공종코드\nORG', '코멘트 Sequence\nORG', '중요도\n코드', '제목', '코멘트 내용', 'QM\n추가의견', '결함코드', '선종', '구역번호', '상세구역', '발행일자', '발행자\n사번', 'QM담당자\n사번', '조치부서\n기능코드1', '조치담당자\n사번1', '조치부서\n기능코드2', '조치담당자\n사번2', '조치부서\n기능코드3', '조치담당자\n사번3', '조치부서\n기능코드4', '조치담당자\n사번4', '결함원인\n부서코드', '검사\nACT No', '선원/장비명', '파일경로', '결함원인\n업체코드', '업로드 성공여부', 'DB 성공\n여부', 'DB 에러 \n메세지', '파일 성공\n여부', '파일 에러 \n메세지', '저장파일수'
]

def parse_comment_text(extracted_text):
    # 빈 데이터 딕셔너리 생성
    data = {col: "" for col in EXCEL_COLUMNS}
    
    # 1. 호선번호 추출 (H로 시작하는 4자리 숫자)
    hull_match = re.search(r'H\d{4}', extracted_text)
    data['호선번호'] = hull_match.group(0) if hull_match else "미확인"
    
    # 2. 제목 추출 (전체 텍스트 중 첫 줄)
    lines = [line.strip() for line in extracted_text.split('\n') if line.strip()]
    data['제목'] = lines[0] if lines else "검사명 미상"
    
    # 3. 코멘트 내용 추출 (전체 내용)
    data['코멘트 내용'] = extracted_text.replace('\n', ' ')
    
    return data

st.set_page_config(page_title="QM 자동화", layout="wide")
st.title("🚢 조선소 QM 코멘트 엑셀 자동화")

if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=EXCEL_COLUMNS)

uploaded_file = st.file_uploader("검사 결과 사진 업로드", type=['png', 'jpg', 'jpeg'])

if uploaded_file and st.button("분석 및 데이터 추가"):
    image = Image.open(uploaded_file)
    text = pytesseract.image_to_string(image, lang='kor+eng')
    
    parsed_data = parse_comment_text(text)
    new_df = pd.DataFrame([parsed_data])
    st.session_state.df = pd.concat([st.session_state.df, new_df], ignore_index=True)
    st.success("데이터가 추가되었습니다!")

if not st.session_state.df.empty:
    st.dataframe(st.session_state.df)
    csv = st.session_state.df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 엑셀(CSV) 다운로드", csv, "result.csv")