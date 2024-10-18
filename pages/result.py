import streamlit as st

st.title("문제 풀이 결과 및 오답 풀이")

# 문제 풀이 결과 표시
if "results" in st.session_state:
    if st.session_state.results:
        for i, result in enumerate(st.session_state.results):
            st.subheader(f"문제 {i + 1}")
            st.latex(result["problem"])
            st.write(f"사용자 답안: {result['user_answer']}")
            st.write(f"정답: {result['correct_answer']}")
            if result["is_correct"]:
                st.success("정답입니다!")
            else:
                st.error("틀렸습니다.")
                st.write("오답 설명: 이 부분에 오답 풀이를 작성할 수 있습니다.")
    else:
        st.write("아직 풀이한 문제가 없습니다. 홈 화면에서 문제를 풀어보세요.")
    
    # 초기화 버튼
    if st.button("풀이 결과 초기화"):
        st.session_state.results = []
        st.success("풀이 결과가 초기화되었습니다.")
        st.experimental_rerun() 
else:
    st.write("풀이 결과가 없습니다. 문제를 풀어보세요.")
