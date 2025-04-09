from transformers import T5ForConditionalGeneration, T5Tokenizer

model_name = "t5-base"
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)

def answer_question(context, question):
    input_text = f"question: {question} context: {context}"
    input_ids = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
    answer_ids = model.generate(input_ids, max_length=150, num_beams=4, early_stopping=True)
    answer = tokenizer.decode(answer_ids[0], skip_special_tokens=True)
    return answer
