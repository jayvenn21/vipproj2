from transformers import pipeline
import secret

REMOTE_INPUT_FILE = secret.REMOTE_INPUT_FILE
REMOTE_OUTPUT_FILE = secret.REMOTE_OUTPUT_FILE

# Load the sentiment-analysis pipeline from Hugging Face
classifier = pipeline("sentiment-analysis")

def classify_sentiment(input_text):
    # Use the classifier to classify the sentiment of the input text
    result = classifier(input_text)
    return result[0]['label']  # Returning only the sentiment label (POSITIVE or NEGATIVE)

with open(REMOTE_INPUT_FILE, "r") as p:
    prompt_text = p.read()

p.close()
result = classify_sentiment(prompt_text)
with open(REMOTE_OUTPUT_FILE, "w") as r:
    r.write(result)
r.close()