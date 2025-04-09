import tkinter as tk
from tkinter import messagebox
from summarize import summarize_text
from translate import translate_text
from generate import generate_text
from qa import answer_question
from classify import classify_text

def run_task():
    task = task_var.get()
    input_text = input_text_box.get("1.0", tk.END)

    try:
        if task == "Summarize":
            result = summarize_text(input_text)
        elif task == "Translate":
            result = translate_text(input_text, 'en', 'es')  # Change source and target language as needed
        elif task == "Generate":
            result = generate_text(input_text)
        elif task == "Answer Question":
            context = input_text.split("\n")[0]  # First line as context
            question = input_text.split("\n")[1]  # Second line as question
            result = answer_question(context, question)
        elif task == "Classify":
            result = classify_text(input_text)
        else:
            result = "Please select a task"
        
        result_text_box.delete("1.0", tk.END)
        result_text_box.insert(tk.END, result)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Set up the Tkinter window
root = tk.Tk()
root.title("T5 Model NLP Tool")

task_var = tk.StringVar(value="Summarize")

# Dropdown for task selection
task_label = tk.Label(root, text="Select Task:")
task_label.pack()
task_menu = tk.OptionMenu(root, task_var, "Summarize", "Translate", "Generate", "Answer Question", "Classify")
task_menu.pack()

# Input text box
input_label = tk.Label(root, text="Enter Input Text:")
input_label.pack()
input_text_box = tk.Text(root, height=10, width=50)
input_text_box.pack()

# Button to run the selected task
run_button = tk.Button(root, text="Run Task", command=run_task)
run_button.pack()

# Output text box
result_label = tk.Label(root, text="Result:")
result_label.pack()
result_text_box = tk.Text(root, height=10, width=50)
result_text_box.pack()

# Run the Tkinter event loop
root.mainloop()
