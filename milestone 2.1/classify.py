from transformers import pipeline
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from benchmark_utils import benchmark

# Initialize both models
hf_classifier = pipeline(
    "text-classification",
    model="finiteautomata/bertweet-base-sentiment-analysis",
    return_all_scores=True
)
vader = SentimentIntensityAnalyzer()

@benchmark
def classify_sentiment(input_text):
    """
    Hybrid sentiment analysis combining transformer models with VADER intensity analysis
    Returns formatted string with nuanced sentiment assessment
    """
    try:
        hf_results = hf_classifier(input_text, truncation=True)[0]
        pos_score = next(r['score'] for r in hf_results if r['label'] == 'POS')
        neg_score = next(r['score'] for r in hf_results if r['label'] == 'NEG')
        
        vader_scores = vader.polarity_scores(input_text)
        
        combined_pos = (pos_score * 0.7) + (vader_scores['pos'] * 0.3)
        combined_neg = (neg_score * 0.7) + (vader_scores['neg'] * 0.3)
        
        if combined_pos > combined_neg:
            sentiment = "POSITIVE"
            base_confidence = combined_pos
            intensity = vader_scores['pos']
        else:
            sentiment = "NEGATIVE"
            base_confidence = combined_neg
            intensity = vader_scores['neg']
        
        adjusted_confidence = min(base_confidence * (1 + intensity), 0.99)
        
        strength_ranges = [
            (0.9, "Extremely"),
            (0.8, "Very"),
            (0.7, "Strongly"),
            (0.6, "Fairly"),
            (0.5, "Moderately"),
            (0.4, "Somewhat"),
            (0, "Slightly")
        ]
        
        strength = next(
            desc for threshold, desc in strength_ranges 
            if adjusted_confidence >= threshold
        )
        
        modifiers = {
            "Extremely": "!",
            "Very": "!",
            "Strongly": "",
            "Fairly": "",
            "Moderately": " (somewhat)",
            "Somewhat": " (mildly)",
            "Slightly": " (barely)"
        }
        
        return (
            f"{strength} {sentiment}{modifiers[strength]} "
            f"(Confidence: {adjusted_confidence:.0%})"
        )
        
    except Exception as e:
        return f"Analysis error: {str(e)}"