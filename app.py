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
    file_path = os.path.join(save_dir, uploaded_file.name)
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
        results = parsing_image(res_latex)
        for exp in results:
            st.latex(exp)
    
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
            st.latex(quiz)
            answers[problem_key] = st.text_input("정답을 입력하세요", key=problem_key)
        
        submit_button = st.form_submit_button("정답 확인")

    if submit_button:
        st.subheader("정답 결과")
        for i, ans in enumerate(st.session_state.ans):
            user_answer = answers.get(f"question_{i+1}", "").strip()
            correct_answer = ans.strip()  
            print(correct_answer)
            st.write(correct_answer)
            result = "정답입니다!" if compare_answer(user_answer, correct_answer) else f"틀렸습니다. 정답은 '{correct_answer}'입니다."
            st.write(f"문제 {i+1}: {result}")
            save_result(st.session_state.quiz[i], user_answer, correct_answer)
            st.latex(st.session_state.sol[i])

# 메인 페이지 - 수학 문제 분석 섹션
st.header("수학 문제 분석 및 유사 문제 출제")

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
