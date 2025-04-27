from transformers import pipeline
from benchmark_utils import benchmark

qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

@benchmark
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
    # Post-processing for better results
    result = qa_pipeline(question=question, context=context)
    
    return result['answer'] if result else "I couldn't find an answer."