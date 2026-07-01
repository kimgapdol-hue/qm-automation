mport streamlit as st
import pandas as pd
import google.generativeai as genai
from PIL import Image
import io

st.title("🚢 조선소 QM 코멘트 자동화")

# 1. API 키와 엑셀 템플릿 파일 입력
api_key = st.text_input("Gemini API Key 입력", type="password")
uploaded_img = st.file_uploader("검사 사진 업로드", type=['png', 'jpg'])
template_file = st.file_uploader("원본 엑셀 양식(xlsx) 업로드", type=['xlsx'])

if api_key and uploaded_img and template_file:
    if st.button("자동 분석 및 엑셀 생성"):
        try:
            # 2. AI 분석 (간결하게 추출)
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            img = Image.open(uploaded_img)
            
            prompt = "이 사진에서 '호선번호', '제목(Inspection Item)', '코멘트 내용'을 추출해서 JSON으로 줘."
            response = model.generate_content([prompt, img])
            st.write("분석 결과 확인 중...")

            # 3. 엑셀 로드 및 데이터 매핑
            df = pd.read_excel(template_file, header=5) # 7행부터 데이터 시작하도록 설정
            
            # 여기서 AI 응답을 파싱하여 df에 적용 (테스트용 하드코딩)
            # 호선번호(A열=0), 제목(K열=10), 코멘트 내용(L열=11)
            df.iloc[0, 0] = "AI_분석_호선번호"
            df.iloc[0, 10] = "AI_분석_제목"
            df.iloc[0, 11] = "AI_분석_내용"
            
            # 4. 결과 다운로드
            output = io.BytesIO()
            df.to_excel(output, index=False)
            st.download_button("📥 정형화된 엑셀 다운로드", output.getvalue(), "QM_Result.xlsx")
            st.success("완료!")
        except Exception as e:
            st.error(f"오류 발생: {e}")
