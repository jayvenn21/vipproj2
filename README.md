under construction

dependencies: 
pip install transformers torch sentencepiece scikit-learn accelerate

how to run:
python main_gui.py

for each feature:
- Summarize (t5-base): place some text as input
- Translate (Helsinki-NLP/opus-mt-{source}-{target}): place some text as input and choose source language and target language
- Answer Question (t5-base): Line 1: context (text that contains the answer), Line 2: the question
- Classify (sentiment analysis): place some sentence or paragraph as input
