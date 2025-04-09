from transformers import T5ForConditionalGeneration, T5Tokenizer

model_name = "t5-base"
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)

def classify_text(input_text):
    input_ids = tokenizer.encode(f"classify: {input_text}", return_tensors="pt", max_length=512, truncation=True)
    classification_ids = model.generate(input_ids, max_length=150, num_beams=4, early_stopping=True)
    classification = tokenizer.decode(classification_ids[0], skip_special_tokens=True)
    return classification
