import tkinter as tk
from tkinter import messagebox
from summarize import summarize_text
from translate import translate_text
from qa import answer_question
from classify import classify_sentiment

def validate_input(task, input_text):
    """Check if input is valid for the selected task."""
    if not input_text.strip():
        raise ValueError("Input text cannot be empty!")
    
    if task == "Answer Question":
        lines = input_text.strip().split("\n")
        if len(lines) < 2:
            raise ValueError(
                "For 'Answer Question', input must have:\n"
                "Line 1: Context (text with the answer)\n"
                "Line 2: Question"
            )
    return True

def run_task():
    task = task_var.get()
    input_text = input_text_box.get("1.0", tk.END).strip()

    try:
        # Validate input before processing
        validate_input(task, input_text)

        if task == "Summarize":
            result = summarize_text(input_text)
        elif task == "Translate":
            source_lang = source_lang_var.get()
            target_lang = target_lang_var.get()
            result = translate_text(input_text, source_lang, target_lang)
        elif task == "Answer Question":
            lines = input_text.split("\n")
            context, question = lines[0], lines[1]
            result = answer_question(context, question)
        elif task == "Classify":
            result = classify_sentiment(input_text)
        else:
            result = "Please select a task"
        
        result_text_box.delete("1.0", tk.END)
        result_text_box.insert(tk.END, result)

    except Exception as e:
        # User-friendly error messages
        error_messages = {
            "ValueError": str(e),
            "RuntimeError": "Model failed to process. Try shorter text.",
            "IndexError": "For 'Answer Question', provide both context and question.",
        }
        messagebox.showerror(
            "Error",
            error_messages.get(type(e).__name__, f"An error occurred: {str(e)}")
        )

def toggle_language_selection(*args):
    """Show/hide language dropdowns for translation."""
    if task_var.get() == "Translate":
        language_frame.pack()
        input_label.config(text="Enter Text to Translate:")
    else:
        language_frame.pack_forget()
        input_label.config(text="Enter Input Text:")

# --- GUI Setup ---
root = tk.Tk()
root.title("AI NLP Tool")

# Task selection dropdown
task_var = tk.StringVar(value="Summarize")
task_label = tk.Label(root, text="Select Task:")
task_label.pack()
task_menu = tk.OptionMenu(root, task_var, "Summarize", "Translate", "Answer Question", "Classify")
task_menu.pack()

# Input text box with dynamic label
input_label = tk.Label(root, text="Enter Input Text:")
input_label.pack()
input_text_box = tk.Text(root, height=10, width=50)
input_text_box.pack()

# Help text (task-specific guidance)
help_text = tk.StringVar(value="Tip: For 'Answer Question', enter context and question on separate lines.")
help_label = tk.Label(root, textvariable=help_text, fg="gray", wraplength=300)
help_label.pack()

# Language selection (hidden by default)
language_frame = tk.Frame(root)
source_lang_var = tk.StringVar(value="en")
target_lang_var = tk.StringVar(value="es")

source_lang_label = tk.Label(language_frame, text="From:")
source_lang_label.pack()
source_lang_menu = tk.OptionMenu(language_frame, source_lang_var, "en", "es", "fr", "de", "it", "pt", "ja", "zh")
source_lang_menu.pack()

target_lang_label = tk.Label(language_frame, text="To:")
target_lang_label.pack()
target_lang_menu = tk.OptionMenu(language_frame, target_lang_var, "en", "es", "fr", "de", "it", "pt", "ja", "zh")
target_lang_menu.pack()

# Run button
run_button = tk.Button(root, text="Run Task", command=run_task)
run_button.pack()

# Result box
result_label = tk.Label(root, text="Result:")
result_label.pack()
result_text_box = tk.Text(root, height=10, width=50, state="normal")
result_text_box.pack()

# Update UI based on task selection
task_var.trace_add("write", lambda *_: (
    toggle_language_selection(),
    help_text.set(
        "Tip: For 'Answer Question', enter context (line 1) and question (line 2)."
        if task_var.get() == "Answer Question" else
        "Tip: Enter text and click 'Run Task'."
    )
))

root.mainloop()