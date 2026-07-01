import streamlit as st
import pandas as pd
import google.generativeai as genai
from PIL import Image
import io

st.set_page_config(page_title="QM 엑셀 자동화", layout="wide")
st.title("🚢 조선소 QM 코멘트 자동화 시스템")

# 1. API 키 설정 (사용자 입력)
api_key = st.sidebar.text_input("Gemini API Key를 입력하세요", type="password")

# 2. 파일 업로드
uploaded_img = st.file_uploader("검사 결과(사진/PDF) 업로드", type=['png', 'jpg', 'jpeg', 'pdf'])
# 3. 빈 엑셀 양식 업로드 (사용자님이 사용하시는 엑셀 파일을 여기에 업로드하게 합니다)
template_file = st.file_uploader("원본 엑셀 양식(QM_Template) 업로드", type=['xlsx'])

if uploaded_img and template_file and api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    if st.button("양식 자동 작성 시작"):
        # AI 분석
        img = Image.open(uploaded_img)
        prompt = "이 사진에서 호선번호, Inspection Item(제목), 코멘트 내용을 추출해서 표 형식으로 정리해줘."
        response = model.generate_content([prompt, img])
        
        # 엑셀 처리
        df_template = pd.read_excel(template_file, header=5) # 7행부터 데이터 시작 (인덱스상 5)
        
        # AI 결과값 매핑 (간소화)
        # 실제 환경에선 AI 응답을 파싱하여 아래와 같이 넣습니다.
        df_template.loc[0, '호선번호'] = "분석된 호선" 
        df_template.loc[0, '제목'] = "분석된 제목"
        df_template.loc[0, '코멘트 내용'] = "분석된 코멘트"
        
        output = io.BytesIO()
        df_template.to_excel(output, index=False)
        st.download_button("📥 정형화된 엑셀 다운로드", output.getvalue(), "QM_Result_Filled.
