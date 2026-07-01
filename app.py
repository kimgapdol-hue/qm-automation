import streamlit as st
import pandas as pd
import google.generativeai as genai
from PIL import Image
import io

st.title("🚢 조선소 QM 자동화 시스템")
api_key = st.sidebar.text_input("Gemini API Key 입력", type="password")
uploaded_img = st.file_uploader("검사 사진 업로드", type=['png', 'jpg'])
template_file = st.file_uploader("원본 엑셀 양식(xlsx)", type=['xlsx'])

if api_key and uploaded_img and template_file:
    if st.button("양식 자동 작성 시작"):
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        img = Image.open(uploaded_img)
        
        # AI 분석
        prompt = "사진에서 '호선번호', '제목', '코멘트 내용'을 추출해서 JSON으로 줘."
        response = model.generate_content([prompt, img])
        
        # 엑셀 로드 및 데이터 입력
        df = pd.read_excel(template_file, header=5)
        # 호선번호(A열=0), 제목(K열=10), 코멘트 내용(L열=11)에 데이터 삽입
        df.iloc[0, 0] = "분석데이터" 
        df.iloc[0, 10] = "분석데이터"
        df.iloc[0, 11] = "분석데이터"
        
        output = io.BytesIO()
        df.to_excel(output, index=False)
        st.download_button("📥 정형화된 엑셀 다운로드", output.getvalue(), "Result.xlsx")
