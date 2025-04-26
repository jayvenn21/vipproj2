from transformers import T5ForConditionalGeneration, T5Tokenizer

model_name = "t5-base"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

def answer_question(context, question):
    """
    Enhanced question answering with T5
    Args:
        context: Background information text (1-3 sentences work best)
        question: Clear question about the context
    Returns:
        Concise answer extracted from context
    """
    # Improved input formatting
    input_text = f"answer question based on context: {question} context: {context}"
    
    # Better tokenization with attention to question-context balance
    input_ids = tokenizer.encode(
        input_text,
        return_tensors="pt",
        max_length=512,
        truncation=True,
        padding="max_length"  # Helps with consistency
    )
    
    # Optimized generation parameters
    answer_ids = model.generate(
        input_ids,
        max_length=100,        # More concise answers
        min_length=5,          # Avoid empty answers
        num_beams=5,           # Better quality than 4 beams
        early_stopping=True,
        repetition_penalty=2.5, # Reduce repeated phrases
        length_penalty=1.5,     # Prefer shorter answers
        no_repeat_ngram_size=3, # Prevent word repetition
        temperature=0.7         # Adds slight creativity
    )
    
    # Improved decoding
    answer = tokenizer.decode(
        answer_ids[0],
        skip_special_tokens=True,
        clean_up_tokenization_spaces=True
    )
    
    # Post-processing for better results
    answer = answer.split(".")[0]  # Take the first complete thought
    answer = answer.strip()
    
    return answer if answer else "I couldn't find an answer in the context."