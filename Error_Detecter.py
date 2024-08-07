import subprocess
import os
import pylint
import tkinter as tk
from tkinter import filedialog, scrolledtext
import re

##티킨터로 검사할 파일 이름을 작성하고 작성된 파일을 pylint, flake8이 분석하여 오류를 찾아내는 프로그램

window = tk.Tk()
window.title('Error_Detecter')
window.geometry("600x400+100+100")


#pylint 실행해서 pylint의 평가를 튜플로 설정
def run_pylint(file_path):
    result = subprocess.run(['pylint', file_path], capture_output=True, text=True, encoding='utf-8', errors='replace')
    return result.stdout, result.stderr


#flake8 실행해서 flake8의 평가를 튜플로 설정
def run_flake8(file_path):
    result = subprocess.run(['flake8', file_path], capture_output=True, text=True, encoding='utf-8', errors='replace')
    return result.stdout, result.stderr


#설정한 값을 문자열로 변환
def check_file():
    file_path = file_path_entry.get()
    #pylint, flake8으로 설정한 튜플 값을 result_pylint으로 정함
    result_pylint = run_pylint(file_path)


    #정한 튜플 값을 문자열로 변환
    result_pylint_stdout = result_pylint[0]


    #pylint의 종합 평가 점수를 score에 저장
    string = 'Your code has been rated at'
    if string in result_pylint_stdout:
        score_line = line_split(string, result_pylint_stdout)
        if score_line:
            score = check_score(score_line[0])
            scoreboard.config(text=f'종합 점수: {score}/10.00')
        else:
            scoreboard.config(text='종합 점수: Error')
    else:
        scoreboard.config(text='종합 점수: Error')


#설정한 값을 스크롤에 설정
def detail_check():
    file_path = file_path_entry.get()
    if not os.path.exists(file_path):
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f'{file_path} 의 파일 경로를 찾을 수 없습니다.')
        output_text.place(x=0, y=130)
        return
    
    pylint_stdout, pylint_stderr = run_pylint(file_path)
    flake8_stdout, flake8_stderr = run_flake8(file_path)

    pylint_stdout = str(pylint_stdout)
    pylint_stderr = str(pylint_stderr)
    flake8_stdout = str(flake8_stdout)
    flake8_stderr = str(flake8_stderr)

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, 'Pylint 결과:\n')
    output_text.insert(tk.END, pylint_stdout)
    output_text.insert(tk.END, pylint_stderr)
    output_text.insert(tk.END, "\nFlake8 결과:\n")
    output_text.insert(tk.END, flake8_stdout)
    output_text.insert(tk.END, flake8_stderr)
    output_text.place(x=0, y=130)


#평가의 앞의 긴 문장 삭제
def line_split(word, text):
    pattern = rf'^{re.escape(word)}.*'
    matches = re.findall(pattern, text, re.MULTILINE)
    return matches


#평가 중에서 원하는 word 값만 선택해 추출
def check_score(text):
    match = re.search(r'at\s+(\S+)/\d+', text)
    if match:
        return match.group(1)
    return None


#브라우저 버튼을 누르면 파일 선택 기능
def browse_file():
    file_path = filedialog.askopenfilename()
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, file_path)


#화면에 표시되는 것들 설정
file_path_entry = tk.Entry(window, width=50)
browse = tk.Button(window, text='Browse', command=browse_file)
confirm = tk.Button(window, text='Confirm', command=check_file)
scoreboard = tk.Label(window, text='종합 점수: 0/10.00', font=("Arial, 20"))
detail_up = tk.Button(window, text='Detail', command=detail_check)
output_text = scrolledtext.ScrolledText(window, width=83, height=20)


#화면에 표시
file_path_entry.place(x=110, y=20)
browse.place(x=470, y=16)
confirm.place(x=150, y=50)
scoreboard.place(x=280, y=50)
detail_up.place(x=270, y=100)


window.mainloop()