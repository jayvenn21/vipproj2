from transformers import T5ForConditionalGeneration, T5Tokenizer
from benchmark_utils import benchmark

model_name = "t5-base"
tokenizer = T5Tokenizer.from_pretrained(model_name, legacy=False)
model = T5ForConditionalGeneration.from_pretrained(model_name)

@benchmark
def summarize_text(input_text):
    # Preprocess input
    input_text = input_text.strip()
    if len(input_text.split()) < 15:  # Minimum words needed for good summary
        return "Input too short - please provide at least 15-20 words for meaningful summarization."
    
    # Format for T5 (crucial!)
    input_text = "summarize: " + input_text
    
    # Tokenize with better truncation
    input_ids = tokenizer.encode(
        input_text,
        return_tensors="pt",
        max_length=512,
        truncation=True,
        padding="max_length"  # Helps with short texts
    )
    
    # Generate with adjusted parameters
    summary_ids = model.generate(
        input_ids,
        max_length=100,       # Reduced from 150
        min_length=30,        # Reduced from 50
        length_penalty=3.0,   # Increased to favor shorter summaries
        num_beams=6,          # Increased from 4
        early_stopping=True,
        no_repeat_ngram_size=3  # Prevents word repetition
    )
    
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
    # Post-process output
    if summary.lower() == input_text[11:].lower():  # If output == input
        return "Summary failed (input may be too short or unclear). Try with longer text."
    
    return summary