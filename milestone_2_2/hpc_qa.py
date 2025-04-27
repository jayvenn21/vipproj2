from transformers import pipeline
from benchmark_utils import benchmark
import secret

qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")


REMOTE_INPUT_FILE = secret.REMOTE_INPUT_FILE
REMOTE_OUTPUT_FILE = secret.REMOTE_OUTPUT_FILE

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
    result = qa_pipeline(question=question, context=context)
    
    return result['answer'] if result else "I couldn't find an answer."

with open(REMOTE_INPUT_FILE, "r") as p:
    prompt = p.readlines()


prompt = [line.strip() for line in prompt]
prompt_text = "\n".join(prompt[1:])
p.close()
result = answer_question(prompt[0], prompt_text)
with open(REMOTE_OUTPUT_FILE, "w") as r:
    r.write(result)
r.close()