import streamlit as st
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

# --- Streamlit UI ---
st.set_page_config(page_title="AI NLP Tool", layout="centered")
st.title("🧠 AI NLP Tool")

# Task selection
task = st.selectbox("Select Task:", ["Summarize", "Translate", "Answer Question", "Classify"])

# Dynamic help text
if task == "Answer Question":
    st.info("ℹ️ For 'Answer Question', enter context (line 1) and question (line 2).")
elif task == "Translate":
    st.info("ℹ️ Enter text and select languages from the dropdown menus.")
else:
    st.info("ℹ️ Enter text and click 'Run Task'.")

# Text input
input_text = st.text_area("Enter Input Text:", height=200)

# Translation language selectors
if task == "Translate":
    language_options = [f"{code} - {name}" for code, name in LANGUAGE_MAP.items()]
    source_lang = st.selectbox("From:", language_options, index=0)
    target_lang = st.selectbox("To:", language_options, index=1)

# Run task
if st.button("Run Task"):
    try:
        # Validate input
        validate_input(task, input_text)

        if task == "Summarize":
            result = summarize_text(input_text)
        elif task == "Translate":
            source_code = source_lang.split(" - ")[0]
            target_code = target_lang.split(" - ")[0]
            result = translate_text(input_text, source_code, target_code)
        elif task == "Answer Question":
            lines = input_text.strip().split("\n")
            context, question = lines[0], lines[1]
            result = answer_question(context, question)
        elif task == "Classify":
            result = classify_sentiment(input_text)
        else:
            result = "Unknown task."

        st.success("✅ Task Completed")
        st.text_area("Result:", value=result, height=200)

    except Exception as e:
        error_messages = {
            "ValueError": str(e),
            "RuntimeError": "Model failed to process. Try shorter text.",
            "IndexError": "For 'Answer Question', provide both context and question.",
        }
        error_msg = error_messages.get(type(e).__name__, f"An error occurred: {str(e)}")
        st.error(error_msg)