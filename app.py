import streamlit as st
import pandas as pd

st.title("QM 자동화 시스템 테스트")
st.write("서버가 정상 작동 중입니다.")

# 파일 업로더가 제대로 뜨는지 확인만 하는 테스트
file = st.file_uploader("파일을 올려보세요", type=['xlsx'])
if file:
    st.write("파일 업로드 성공!")
