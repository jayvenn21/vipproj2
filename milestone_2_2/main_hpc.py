import tkinter as tk
from tkinter import messagebox
import subprocess

import milestone_2_2.secret as secret
import time
import psutil

# === CONFIGURATION ===
LOCAL_INPUT_FILE = "prompt.txt"
LOCAL_OUTPUT_FILE = "result.txt"
HPC_USER = secret.HPC_USER
HPC_HOST = secret.HPC_HOST
REMOTE_INPUT_FILE = secret.REMOTE_INPUT_FILE
REMOTE_OUTPUT_FILE = secret.REMOTE_OUTPUT_FILE
HPC_JOB_SCRIPT = secret.HPC_JOB_SCRIPT

def run_task():
    task = task_var.get()
    input_text = input_text_box.get("1.0", tk.END)

    try:
         # Step 1: Transfer prompt to HPC
        with open(LOCAL_INPUT_FILE, "w") as f1:
            if task == "Translate":
                f1.write(source_lang_var.get() + "\n")
                f1.write(target_lang_var.get() + "\n")
            f1.write(input_text)

        #memt = subprocess.Popen(["python", "memorytracker.py", str(process.pid)])
        print("Timer started:")
        subprocess.run(["scp", LOCAL_INPUT_FILE, f"{HPC_USER}@{HPC_HOST}:{REMOTE_INPUT_FILE}"])
        print("File copied")
        job_cmd = f"sbatch {HPC_JOB_SCRIPT} {task} {REMOTE_INPUT_FILE} {REMOTE_OUTPUT_FILE}"
        
        # Run the command over SSH
        ssh = subprocess.Popen(
            ["ssh", f"{HPC_USER}@{HPC_HOST}", job_cmd],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = ssh.communicate()
        print("SLURM thing sent i think")

        if ssh.returncode != 0:
            return f"[ERROR] Job submission failed:\n{stderr.decode()}"

        job_output = stdout.decode()
        print("Submitted job:", job_output)
        job_id = job_output.strip().split()[-1]  # Optional: parse job ID
        print("we going places")
        # Waits for the SLURM job to be done before parsing result - to prevent previous result from showing up
        while True:
            time.sleep(0.001)
            result = subprocess.run(
                ["ssh", f"{HPC_USER}@{HPC_HOST}", f"squeue -j {job_id} | wc -l"],
                stdout=subprocess.PIPE
            )
            lines = int(result.stdout.decode().strip())
            if lines <= 1:
                break
        print("first loop broken")

        #Polling result
        while True:
            time.sleep(0.001)
            result = subprocess.run(
                ["ssh", f"{HPC_USER}@{HPC_HOST}", f"test -f {REMOTE_OUTPUT_FILE} && echo DONE || echo WAIT"],
                stdout=subprocess.PIPE
            )
            if result.stdout.decode().strip() == "DONE":
                subprocess.run(["scp", f"{HPC_USER}@{HPC_HOST}:{REMOTE_OUTPUT_FILE}", LOCAL_OUTPUT_FILE], check=True)
                break

        # Download the result file
        print("second loop broken")

        # Return the result
        resulttext = "test text"
        with open(LOCAL_OUTPUT_FILE) as f2:
            resulttext = f2.read()

        f1.close()
        f2.close()

        #memt.terminate()
        result_text_box.delete("1.0", tk.END)
        result_text_box.insert(tk.END, resulttext)
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
