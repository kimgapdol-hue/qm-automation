Python
import streamlit as st
import pandas as pd

st.set_page_config(page_title="QM 자동화", layout="centered")
st.title("🚢 조선소 QM 코멘트 자동화")
st.write("사진을 올리고, 아래 칸에 내용을 직접 입력하면 엑셀 양식으로 저장됩니다.")

# 1. 파일 업로드 (이미지 확인용)
uploaded_file = st.file_uploader("검사 결과 사진 업로드", type=['jpg', 'png'])

# 2. 정보 입력 칸
hull_no = st.text_input("호선번호", placeholder="예: H1234")
title = st.text_input("제목(검사명)", placeholder="검사명을 입력하세요")
content = st.text_area("코멘트 내용", placeholder="코멘트 내용을 입력하세요")

# 3. 엑셀 다운로드 버튼
if st.button("엑셀 양식 생성"):
    data = {
        '호선번호': [hull_no],
        '제목': [title],
        '코멘트 내용': [content]
    }
    df = pd.DataFrame(data)
    
    csv = df.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="📥 엑셀(CSV) 다운로드",
        data=csv,
        file_name='QM_Comment.csv',
        mime='text/csv'
    )
    st.success("준비되었습니다! 다운로드 버튼을 누르세요.")
