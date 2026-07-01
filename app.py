import streamlit as st
import pandas as pd
from PIL import Image
import google.generativeai as genai
import io

st.title("🚢 QM 자동화 시스템")
api_key = st.text_input("Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    uploaded_file = st.file_uploader("검사 사진 업로드", type=['jpg', 'png'])
    template_file = st.file_uploader("엑셀 템플릿(xlsx) 업로드", type=['xlsx'])

    if uploaded_file and template_file:
        if st.button("자동 작성"):
            st.write("분석 중...")
            img = Image.open(uploaded_file)
            # 엑셀 로드 (7행부터 데이터 시작)
            df = pd.read_excel(template_file, header=5)
            
            # AI 분석 및 데이터 넣기
            df.iloc[0, 0] = "분석된 호선" 
            df.iloc[0, 10] = "분석된 제목"
            df.iloc[0, 11] = "분석된 코멘트"
            
            output = io.BytesIO()
            df.to_excel(output, index=False)
            st.download_button("결과 파일 다운로드", output.getvalue(), "Result.xlsx")
