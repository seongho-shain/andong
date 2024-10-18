import streamlit as st
import pandas as pd

st.title("유형별 문제 빈도수")

# 문제 유형 빈도수를 시각화
if "problem_types" in st.session_state:
    if st.session_state.problem_types:
        data = pd.DataFrame(
            list(st.session_state.problem_types.items()), 
            columns=["Problem Type", "Frequency"]
        )
        st.bar_chart(data.set_index("Problem Type"))
        st.write(data)
    else:
        st.write("아직 문제 유형 데이터가 없습니다. 홈 화면에서 문제를 업로드하고 분석해보세요.")
    
    # 초기화 버튼
    if st.button("유형 데이터 초기화"):
        st.session_state.problem_types = {}
        st.success("유형 데이터가 초기화되었습니다.")
        st.experimental_rerun() 
else:
    st.write("유형 데이터가 없습니다. 문제를 업로드하고 분석하세요.")
