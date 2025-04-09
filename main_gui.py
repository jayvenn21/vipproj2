import tkinter as tk
from tkinter import messagebox
from summarize import summarize_text
from translate import translate_text
from qa import answer_question
from classify import classify_sentiment  # Updated import to match the function name

def run_task():
    task = task_var.get()
    input_text = input_text_box.get("1.0", tk.END)

    try:
        if task == "Summarize":
            result = summarize_text(input_text)
        elif task == "Translate":
            source_lang = source_lang_var.get()
            target_lang = target_lang_var.get()
            result = translate_text(input_text, source_lang, target_lang)  # Use selected languages
        elif task == "Answer Question":
            context = input_text.split("\n")[0]  # First line as context
            question = input_text.split("\n")[1]  # Second line as question
            result = answer_question(context, question)
        elif task == "Classify":
            result = classify_sentiment(input_text)  # Call the correct function here
        else:
            result = "Please select a task"
        
        result_text_box.delete("1.0", tk.END)
        result_text_box.insert(tk.END, result)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def toggle_language_selection(*args):
    if task_var.get() == "Translate":
        language_frame.pack()  # Show the language selection frame
    else:
        language_frame.pack_forget()  # Hide the language selection frame

# Set up the Tkinter window
root = tk.Tk()
root.title("T5 Model NLP Tool")

task_var = tk.StringVar(value="Summarize")

# Dropdown for task selection
task_label = tk.Label(root, text="Select Task:")
task_label.pack()
task_menu = tk.OptionMenu(root, task_var, "Summarize", "Translate", "Answer Question", "Classify")  # Removed "Generate"
task_menu.pack()

# Input text box
input_label = tk.Label(root, text="Enter Input Text:")
input_label.pack()
input_text_box = tk.Text(root, height=10, width=50)
input_text_box.pack()

# Dropdowns for language selection (only visible when "Translate" is selected)
language_frame = tk.Frame(root)

# Source language dropdown
source_lang_var = tk.StringVar(value="en")
source_lang_label = tk.Label(language_frame, text="Source Language:")
source_lang_label.pack()
source_lang_menu = tk.OptionMenu(language_frame, source_lang_var, "en", "es", "fr", "de", "it", "pt", "ja", "zh")
source_lang_menu.pack()

# Target language dropdown
target_lang_var = tk.StringVar(value="es")
target_lang_label = tk.Label(language_frame, text="Target Language:")
target_lang_label.pack()
target_lang_menu = tk.OptionMenu(language_frame, target_lang_var, "en", "es", "fr", "de", "it", "pt", "ja", "zh")
target_lang_menu.pack()

# Button to run the selected task
run_button = tk.Button(root, text="Run Task", command=run_task)
run_button.pack()

# Output text box
result_label = tk.Label(root, text="Result:")
result_label.pack()
result_text_box = tk.Text(root, height=10, width=50)
result_text_box.pack()

# Update the visibility of language selection based on task selection
task_var.trace_add("write", toggle_language_selection)

# Run the Tkinter event loop
root.mainloop()
