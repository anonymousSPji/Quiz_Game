import tkinter as tk
from tkinter import messagebox, ttk
from ttkbootstrap import Style
from datetime import datetime  
import sqlite3
from quiz_data import quiz_data

def show_question():
    question = quiz_data[current_question]
    qs_label.config(text=question["question"])

    choices = question["choices"]
    for i in range(4):
        choice_btns[i].config(text=choices[i], state="normal") 

    feedback_label.config(text="")
    next_btn.config(state="disabled")

def check_answer(choice):
    question = quiz_data[current_question]
    selected_choice = choice_btns[choice].cget("text")
    if selected_choice == question["answer"]:
        global score
        score += 1
        update_score(score)  # Update score
        feedback_label.config(text="Correct!", foreground="green")
    else:
        feedback_label.config(text="Incorrect!", foreground="red")
    
    for button in choice_btns:
        button.config(state="disabled")
    next_btn.config(state="normal")
    store_answer(question["question"], selected_choice)  

def store_answer(question, answer):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
    cursor.execute("INSERT INTO user_answers (timestamp, username, question, answer) VALUES (?, ?, ?, ?)", 
                   (current_time, username, question, answer))
    conn.commit()

def update_score(score):
    score_label.config(text=f"Score: {score}/{len(quiz_data)}")  

def next_question():
    global current_question
    current_question += 1

    if current_question < len(quiz_data):
        show_question()
    else:
        messagebox.showinfo("Quiz Completed",
                            f"Quiz Completed! Final score: {score}/{len(quiz_data)}")
        root.destroy()

def submit_name():
    global username
    username = name_entry.get()
    name_label.config(text=f"Welcome, {username}!")  
    name_entry.config(state="disabled")
    submit_btn.config(state="disabled")
    show_question()

conn = sqlite3.connect('quiz_database.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS user_answers
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT,
                  username TEXT,
                  question TEXT,
                  answer TEXT)''')
conn.commit()

root = tk.Tk()
root.title("Quiz App")
root.geometry("600x500")
style = Style(theme="minty")  

style.configure("TLabel", font=("Helvetica", 20), background="white") 
style.configure("TButton", font=("Helvetica", 16), background="#007bff", foreground="white", relief="raised")  # Setting button style

name_label = ttk.Label(root, text="Enter your name:")
name_label.pack(pady=10)
name_entry = ttk.Entry(root)
name_entry.pack(pady=5)
submit_btn = ttk.Button(root, text="Submit", command=submit_name)
submit_btn.pack(pady=5)

qs_label = ttk.Label(
    root,
    anchor="center",
    wraplength=500,
    padding=10
)
qs_label.pack(pady=20, padx=10, fill="both") 

choice_btns = []
for i in range(4):
    button = ttk.Button(
        root,
        command=lambda i=i: check_answer(i)
    )
    button.pack(pady=5, padx=20, fill="both") 
    choice_btns.append(button)

feedback_label = ttk.Label(
    root,
    anchor="center",
    padding=10
)
feedback_label.pack(pady=10)
score = 0
score_label = ttk.Label(
    root,
    text="Score: 0/{}".format(len(quiz_data)),
    anchor="center",
    padding=10
)
score_label.pack(pady=10)

next_btn = ttk.Button(
    root,
    text="Next",
    command=next_question,
    state="disabled"
)
next_btn.pack(pady=10)

current_question = 0
username = ""

root.mainloop()
conn.close()
