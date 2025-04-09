from transformers import T5ForConditionalGeneration, T5Tokenizer

model_name = "t5-base"
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)

def translate_text(input_text, source_language='en', target_language='es'):
    input_ids = tokenizer.encode(f"translate {source_language} to {target_language}: {input_text}", return_tensors="pt", max_length=512, truncation=True)
    translated_ids = model.generate(input_ids, max_length=150, num_beams=4, early_stopping=True)
    translation = tokenizer.decode(translated_ids[0], skip_special_tokens=True)
    return translation
