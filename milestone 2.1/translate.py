from transformers import MarianMTModel, MarianTokenizer
from benchmark_utils import benchmark

# Function to get the model name based on the source and target language
def get_model_name(source_language, target_language):
    return f"Helsinki-NLP/opus-mt-{source_language}-{target_language}"

# Function to perform translation
@benchmark
def translate_text(input_text, source_language='en', target_language='es'):
    model_name = get_model_name(source_language, target_language)
    
    # Load the MarianMT model and tokenizer for the specific language pair
    model = MarianMTModel.from_pretrained(model_name)
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    
    # Prepare the input text with the correct prefix for translation
    input_ids = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True, padding="max_length")
    
    # Generate the translation
    translated_ids = model.generate(input_ids, max_length=150, num_beams=4, early_stopping=True)
    
    # Decode the translated output
    translation = tokenizer.decode(translated_ids[0], skip_special_tokens=True)
    
    return translation
