#Make .streamlit/secrets.toml 
#pip install -r requirements.txt
#PLEASE READ README.md for more informations

import streamlit as st
import json
import os
from utils import *

# 초기 상태 설정
if "quiz" not in st.session_state:
    st.session_state.quiz = []
if "sol" not in st.session_state:
    st.session_state.sol = []
if "ans" not in st.session_state:
    st.session_state.ans = []
if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None
if "image_processed" not in st.session_state:
    st.session_state.image_processed = False
if "response" not in st.session_state:
    st.session_state.response = None
if "problem_types" not in st.session_state:
    st.session_state.problem_types = {}
if "results" not in st.session_state:
    st.session_state.results = []
if "show_solution" not in st.session_state:
    st.session_state.show_solution = False


# 페이지 초기화
st.set_page_config(layout="wide")

def save_uploaded_file(uploaded_file):
    """업로드된 파일을 저장하고 경로를 반환합니다."""
    save_dir = "uploaded_files"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
     # 파일 확장자를 소문자로 변환
    file_name, file_extension = os.path.splitext(uploaded_file.name)
    file_extension = file_extension.lower()  # 확장자를 소문자로 변경
    file_path = os.path.join(save_dir, f"{file_name}{file_extension}")
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.image(file_path)
    return file_path.replace("\\", "/")

def process_image(file_path):
    """이미지 파일 경로로부터 LaTeX 표현식과 문제 유형을 분석하고 유사 문제를 생성합니다."""
    file_id = get_file_id(file_path)
    if not file_id:
        st.error("파일 업로드에 실패했습니다.")
        return None

    with st.spinner("이미지를 분석하고 있습니다..."):
        res_latex = image_to_latex(file_id)
        st.subheader("LaTeX 변환 결과")
        problems = parsing_image(res_latex)
        for p in problems:
            steps, final_answer = getAnswer(p)
            for s in steps:
                st.write(s["explanation"])
                output = s["output"]
                if "$" in output or r"\(" in output or r"\[" in output:
                    st.markdown(output)  # LaTeX 표기법이 포함된 경우, Markdown으로 처리
                else:
                    st.latex(output)     # LaTeX 수식만 포함된 경우, st.latex() 사용    # LaTeX 수식인 경우, st.latex() 사용
        
        st.latex(final_answer)

                  
    with st.spinner("유형을 분석하고 있습니다..."):
        res_category = get_category(res_latex)
        problem_types = json.loads(res_category)['problems']
        for problem_type in problem_types:
            pt = problem_type.get("유형", '기타')
            st.session_state.problem_types[pt] = st.session_state.problem_types.get(pt, 0) + 1
        st.subheader("유형 분석 결과")
        st.write(json.loads(res_category)['problems'])
    
    return res_category

def make_problems(response):
    """유사 문제를 세션 상태에 저장합니다. """
    with st.spinner("유형에 관련된 문제를 만들고 있습니다..."):
        st.subheader("유사 문제")
        res_quiz = make_similar_type(response)
        quizes = parsing_new_quiz(res_quiz)
        for quiz in quizes:
            st.session_state.quiz.append(quiz['problem'])
            st.session_state.sol.append(quiz['solution'])
            st.session_state.ans.append(quiz['answer'])

def save_result(problem, user_answer, correct_answer):
    """결과를 세션 상태에 저장합니다."""
    is_correct = compare_answer(user_answer, correct_answer)
    result = {
        "problem": problem,
        "user_answer": user_answer,
        "correct_answer": correct_answer,
        "is_correct": is_correct
    }
    st.session_state.results.append(result)

def render_quiz_form():
    """사용자 답안을 처리합니다."""
    with st.form("quiz_form"):
        answers = {}
        for i, quiz in enumerate(st.session_state.quiz):
            problem_key = f"question_{i+1}"
            st.subheader(f"문제 {i+1}")
            #st.latex(quiz)
            #quiz_escaped = quiz.replace("\\", "\\\\")
            st.markdown(quiz)
            answers[problem_key] = st.text_input("정답을 입력하세요", key=problem_key)
        
        submit_button = st.form_submit_button("정답 확인")

    if submit_button:
        st.subheader("정답 결과")
        for i, ans in enumerate(st.session_state.ans):
            user_answer = answers.get(f"question_{i+1}", "")
    
            # user_answer가 문자열인지 확인하고, 아니라면 문자열로 변환
            if isinstance(user_answer, str):
                user_answer = user_answer.strip()

            correct_answer = ans  # correct_answer도 마찬가지로 문자열로 가정
            print(correct_answer)
            st.write(correct_answer)
            result = "정답입니다!" if compare_answer(user_answer, correct_answer) else f"틀렸습니다. 정답은 '{correct_answer}'입니다."
            st.write(f"문제 {i+1}: {result}")
            save_result(st.session_state.quiz[i], user_answer, correct_answer)
            #st.latex(st.session_state.sol[i])
            #ans_escaped = st.session_state.sol[i].replace("\\", "\\\\")
            st.markdown(st.session_state.sol[i])

# 메인 페이지 - 수학 문제 분석 섹션
st.header("수학 문제 분석 및 유사 문제 출제")
st.subheader("UPDATED : 2024-11-05")

uploaded_file = st.file_uploader("수학 문제 이미지를 업로드하세요", type=["png", "jpg", "jpeg"])
if uploaded_file and uploaded_file.name != st.session_state.uploaded_file_name:
    st.session_state.quiz = []
    st.session_state.ans = []
    st.session_state.sol = []
    st.session_state.uploaded_file_name = uploaded_file.name
    st.session_state.image_processed = False
    st.session_state.response = None
    st.session_state.show_solution = False

if uploaded_file and not st.session_state.image_processed:
    file_path = save_uploaded_file(uploaded_file)
    response = process_image(file_path)
    if response:
        st.session_state.response = response
        st.session_state.image_processed = True

# 이미 처리된 이미지에 대해 문제 생성
if st.session_state.response and not st.session_state.quiz:
    make_problems(st.session_state.response)

# 문제 폼 출력
if st.session_state.quiz:
    render_quiz_form()
