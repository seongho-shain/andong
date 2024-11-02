#####CHANGE ASSISTANT ID HERE ########## 
imageToLatexID = "asst_1Yb0JzkBzD3z2AntEyU0J1bi"
latexToCategoryID = "asst_W6nsih5HPkl4iwQzk7i5MQZK"
categoryToNewProblems = "asst_cxV4mDJPvwhAwoZcaKTqqkNL"
########################################



from openai import OpenAI
from fractions import Fraction
import streamlit as st
import json
client = OpenAI(api_key=st.secrets["OpenAI_key"])


def get_category(questionList):
    return ask_assistant(latexToCategoryID, questionList)

def image_to_latex(image_id):
    return ask_assistant_with_image(imageToLatexID, image_id)

def make_similar_type(categoryList):
    return ask_assistant(categoryToNewProblems, categoryList)

def parsing_image(string):
    dic = json.loads(string)['problems']
    lst = [item['problem_description'] for item in dic]
    return lst

def parsing_category(string2):
    dic2 = json.loads(string2)['problems']
    return dic2

def parsing_new_quiz(string):
    dic = json.loads(string)['problems']
    return dic

def compare_answer(user_input, correct_answer):
    try:
        # 분수 형태의 입력을 float로 변환
        user_value = float(Fraction(user_input))
        # 정답을 float로 변환
        correct_value = float(correct_answer)
        # 입력값과 정답값을 비교 (적절한 오차 범위 내에서)
        return abs(user_value - correct_value) < 1e-6  # 오차 범위 설정
    except ValueError:
        # 입력이 유효하지 않으면 False 반환
        return False
    
def get_file_id(file_path):
    try:
        with open(file_path, "rb") as file:
            response = client.files.create(
                file=file,
                purpose="vision"
            )
        return response.id
    except Exception as e:
        print(f"An error occurred while uploading the file: {str(e)}")
        return None
    
    

def ask_assistant(assis_id ,prompt):
    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assis_id,
    )
    if run.status == 'completed': 
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        return messages.data[0].content[0].text.value
        
    else:
        return run.status
    
def ask_assistant_with_image(assis_id ,file_id):
    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=  [{"type": "text", "text":"convert to latex"},
                            {"type": "image_file", 
                            "image_file": {"file_id": file_id, "detail": "low"}}])
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assis_id,
    )
    if run.status == 'completed': 
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        return messages.data[0].content[0].text.value
        
    else:
        return run.status
