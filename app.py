import streamlit as st
import pandas as pd
from PIL import Image
import easyocr  # pytesseract 대신 easyocr 사용

st.set_page_config(page_title="QM 자동화", layout="wide")
st.title("🚢 조선소 QM 코멘트 엑셀 자동화 시스템")

# EasyOCR 리더 초기화 (처음 한 번만 실행)
@st.cache_resource
def load_reader():
    return easyocr.Reader(['ko', 'en'])

reader = load_reader()
uploaded_file = st.file_uploader("검사 결과 사진 업로드", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    image = Image.open(uploaded_file)
    # 이미지에서 글자 추출
    results = reader.readtext(uploaded_file.getvalue(), detail=0)
    text = " ".join(results)
    
    st.write("추출된 텍스트:", text)
    # 이후 데이터 처리 로직 동일
