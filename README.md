
# Andong - High School Math Problem Analyzer

## Overview
**Andong** is a program designed to analyze, solve, and generate similar questions from photos of Korean high school math problems. The program also provides statistical insights into the types of problems analyzed and displays the results of similar problem solutions.
**Andong** is a program designed to analyze, solve, and generate similar questions from photos of high school math problems. The program also provides statistical insights into the types of problems analyzed and displays the results of similar problem solutions.

### Key Features
- **Problem Analysis**: Upload a photo of a math problem and receive a detailed analysis.
- **Problem Solving**: Get solutions for uploaded problems.
- **Similar Problem Generation**: Generate and solve problems similar to the input question.
- **Statistics**: Track and view statistics related to the types of math problems submitted.
- **Limitations**:
  - Issues with recognition when the photo quality is poor.
  - Limited recognition capabilities for graphs and geometric figures.

### Technology Used
This program utilizes the **OpenAI API** to perform its core functions.

### Assistants
Three distinct assistants were developed and used in the creation of this program:

1. **imageToLatex**
   - **System Instructions**:
     - 이미지 분석: 이미지를 처리하여 수학 문제와 텍스트를 정확히 인식합니다.
     - LaTeX 변환: 인식된 수학 문제를 LaTeX 형식으로 변환합니다. 수식은 LaTeX 문법에 따라 작성하되, 한글 텍스트는 \text{}를 사용하지 않고 그대로 작성합니다.
     - JSON 리스트 작성: 변환된 LaTeX 코드를 지정된 JSON 구조로 구성하되, 각 문제는 "problem_description"의 리스트로 만들어주세요.

2. **latexToCategory**
   - **System Instructions**:
     - 문제 분석: 입력된 수학 문제를 읽고, 문제의 주요 요소(수학적 개념, 공식, 수식)를 파악합니다.
     - 과목 및 유형 결정: 문제의 주제와 관련된 수학적 개념을 바탕으로, 반드시 아래 목록에서 적합한 과목과 유형을 선택합니다.
     - 여러 문제 처리: 한 페이지에 여러 문제가 있을 경우, 각 문제는 과목, 유형으로 이루어진 리스트로 출력합니다.
     - JSON 작성: 선택된 과목과 유형을 바탕으로 지정된 JSON 형식으로 문제를 출력합니다.

3. **categoryToNewProblems**
   - **System Instructions**:
     - 입력된 과목, 유형, 문제를 바탕으로 유사한 유형의 문제와 그 해결 방법을 제시하세요.
     - 문제는 간결하고 명확하게 설명하고, 그에 대한 정답과 해답을 따로 제시합니다.
     - solution은 무조건 실수(real number)로 나오게 하세요.

---Three distinct assistants were developed and used in the creation of this program. Each assistant handles different parts of the problem analysis and solution processes.

## How to Run Locally
Follow these steps to run the program on your local machine:

1. **Clone the repository**:
   ```bash
   $ git clone <repository-url>
   $ cd andong
   ```

2. **Create a virtual environment and install the required packages**:
   ```bash
   $ conda create -n andong python=3.11
   $ conda activate andong
   $ pip install -r requirements.txt
   ```

3. **Set up OpenAI API configuration**:
   - Access the OpenAI API site and go to **Dashboard > Assistant** tab to create your assistants.
   - Create a project and set up the three assistants as described above.
   - Generate and save your API key.
   - Replace the assistant IDs in `utils.py` with your own assistant IDs.
   - Create a folder named `.streamlit` in the cloned project directory and add a file named `secrets.toml`.
   - Inside `secrets.toml`, add the following line and save:
     ```toml
     OpenAI_key = "yourProjectApiKey"
     ```

4. **Run the application**:
   ```bash
   $ streamlit run app.py
   ```

Now, you can run the program and start analyzing math problems!

---
Feel free to contribute, report issues, or suggest enhancements.

## Acknowledgments
This project was created by **kodekorea**, led by CEO **Seongho-Shain**, with the generous support of **Andong National University**. We are grateful for their assistance and collaboration.

## License
This project is licensed under the [MIT License](LICENSE).
