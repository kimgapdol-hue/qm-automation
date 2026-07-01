Python
import streamlit as st
import pandas as pd
import google.generativeai as genai
import PIL.Image

# 1. API 키 설정 (보안상 동료들과 쓸 때는 환경변수로 처리하거나, 입력받도록 설정)
api_key = st.text_input("구글 AI API 키를 입력하세요", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    uploaded_file = st.file_uploader("검사 결과(사진/PDF) 업로드", type=['png', 'jpg', 'jpeg'])

    if uploaded_file and st.button("AI 자동 분석 시작"):
        img = PIL.Image.open(uploaded_file)
        # AI에게 분석 요청
        prompt = "이 사진에서 호선번호, 제목, 코멘트 내용을 추출해서 표 형식으로 정리해줘."
        response = model.generate_content([prompt, img])
        
        st.write("분석 결과:", response.text)
        # 이후 이 결과를 엑셀로 다운로드하는 버튼 구현...
