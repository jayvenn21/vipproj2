from transformers import T5ForConditionalGeneration, T5Tokenizer

model_name = "t5-base"
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)

def summarize_text(input_text):
    input_ids = tokenizer.encode(f"summarize: {input_text}", return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(input_ids, max_length=150, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

with open("prompt.txt", "r") as p:
    prompt_text = p.read()

p.close()
result = summarize_text(prompt_text)
with open("result.txt", "w") as r:
    r.write(result)
r.close()