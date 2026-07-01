import streamlit as st
import pandas as pd
import google.generativeai as genai
from PIL import Image
import io

st.title("🚢 조선소 QM 자동화 시스템")

# 1. API 키와 파일 입력
api_key = st.sidebar.text_input("Gemini API Key 입력", type="password")
uploaded_img = st.file_uploader("검사 사진 업로드", type=['png', 'jpg', 'jpeg'])
template_file = st.file_uploader("원본 엑셀 양식(xlsx)", type=['xlsx'])

if api_key and uploaded_img and template_file:
    if st.button("양식 자동 작성 시작"):
        try:
            # 2. AI 분석 (OCR 없이 Gemini가 직접 인식)
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            img = Image.open(uploaded_img)
            
            prompt = "사진에서 '호선번호', '제목(Inspection Item)', '코멘트 내용'을 추출해서 JSON 형식으로 줘."
            response = model.generate_content([prompt, img])
            
            # 3. 엑셀 로드 및 데이터 매핑 (7행부터 데이터 시작)
            df = pd.read_excel(template_file, header=5)
            
            # 실제 데이터가 들어갈 열: 호선번호(A열=0), 제목(K열=10), 코멘트 내용(L열=11)
            # AI 결과값을 여기에 넣습니다.
            df.iloc[0, 0] = "분석된 호선" 
            df.iloc[0, 10] = "분석된 제목"
            df.iloc[0, 11] = "분석된 코멘트"
            
            output = io.BytesIO()
            df.to_excel(output, index=False)
            st.download_button("📥 정형화된 엑셀 다운로드", output.getvalue(), "Result.xlsx")
            st.success("완료!")
        except Exception as e:
            st.error(f"오류: {e}")
