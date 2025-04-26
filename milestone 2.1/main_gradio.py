import gradio as gr
from summarize import summarize_text
from translate import translate_text
from qa import answer_question
from classify import classify_sentiment

# Language mapping dictionary
LANGUAGE_MAP = {
    "en": "English",
    "es": "Español (Spanish)",
    "fr": "Français (French)",
    "de": "Deutsch (German)",
    "it": "Italiano (Italian)",
    "pt": "Português (Portuguese)",
    "ja": "日本語 (Japanese)",
    "zh": "中文 (Chinese)"
}

language_options = [f"{code} - {name}" for code, name in LANGUAGE_MAP.items()]

def validate_input(task, input_text):
    if not input_text.strip():
        raise gr.Error("Input text cannot be empty!")

    if task == "Answer Question":
        lines = input_text.strip().split("\n")
        if len(lines) < 2:
            raise gr.Error(
                "For 'Answer Question', input must have:\n"
                "Line 1: Context (text with the answer)\n"
                "Line 2: Question"
            )
    return True

def run_task(task, input_text, source_lang, target_lang):
    validate_input(task, input_text)

    if task == "Summarize":
        return summarize_text(input_text)
    elif task == "Translate":
        source_code = source_lang.split(" ")[0]
        target_code = target_lang.split(" ")[0]
        return translate_text(input_text, source_code, target_code)
    elif task == "Answer Question":
        lines = input_text.strip().split("\n")
        context, question = lines[0], lines[1]
        return answer_question(context, question)
    elif task == "Classify":
        return classify_sentiment(input_text)
    else:
        return "Please select a valid task."

def show_translation_fields(task):
    return gr.update(visible=(task == "Translate"))

def update_help_text(task):
    if task == "Answer Question":
        return "Tip: Enter context (line 1) and question (line 2)."
    elif task == "Translate":
        return "Tip: Enter text and select source and target languages."
    else:
        return "Tip: Enter text and click 'Run Task'."

with gr.Blocks() as demo:
    gr.Markdown("## 🧠 AI NLP Tool")

    task = gr.Dropdown(["Summarize", "Translate", "Answer Question", "Classify"], label="Select Task", value="Summarize")
    help_message = gr.Markdown("Tip: Enter text and click 'Run Task'.")

    input_text = gr.Textbox(label="Enter Input Text", lines=8, placeholder="Enter your text here...")
    
    with gr.Row(visible=False) as language_row:
        source_lang = gr.Dropdown(language_options, label="From", value=language_options[0])
        target_lang = gr.Dropdown(language_options, label="To", value=language_options[1])

    run_btn = gr.Button("Run Task")
    output_text = gr.Textbox(label="Result", lines=8)

    # Interactions
    task.change(fn=show_translation_fields, inputs=task, outputs=language_row)
    task.change(fn=update_help_text, inputs=task, outputs=help_message)
    run_btn.click(fn=run_task, inputs=[task, input_text, source_lang, target_lang], outputs=output_text)

demo.launch()