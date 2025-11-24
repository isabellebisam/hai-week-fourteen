"""
Sentiment analysis for Nietzsche corpus using VADER.
Analyzes sentiment at both full-text and chapter levels.
"""

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize
import numpy as np
from preprocess import preprocess_texts


def ensure_nltk_data():
    """Download required NLTK data."""
    try:
        nltk.data.find('sentiment/vader_lexicon.zip')
    except LookupError:
        print("Downloading VADER lexicon...")
        nltk.download('vader_lexicon', quiet=True)

    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("Downloading punkt tokenizer...")
        nltk.download('punkt', quiet=True)


def analyze_sentiment(text, analyzer):
    """
    Analyze sentiment of text using VADER.
    Returns dict with compound, positive, neutral, negative scores.
    """
    # Split into sentences for more accurate analysis
    sentences = sent_tokenize(text)

    if not sentences:
        return {
            'compound': 0.0,
            'positive': 0.0,
            'neutral': 0.0,
            'negative': 0.0,
            'sentence_count': 0
        }

    # Analyze each sentence
    scores = [analyzer.polarity_scores(sent) for sent in sentences]

    # Aggregate scores
    return {
        'compound': np.mean([s['compound'] for s in scores]),
        'positive': np.mean([s['pos'] for s in scores]),
        'neutral': np.mean([s['neu'] for s in scores]),
        'negative': np.mean([s['neg'] for s in scores]),
        'sentence_count': len(sentences),
        'compound_std': np.std([s['compound'] for s in scores]),
        'sentiment_range': (
            min([s['compound'] for s in scores]),
            max([s['compound'] for s in scores])
        )
    }


def classify_sentiment(compound_score):
    """
    Classify sentiment based on compound score.
    """
    if compound_score >= 0.05:
        return 'positive'
    elif compound_score <= -0.05:
        return 'negative'
    else:
        return 'neutral'


def analyze_corpus_sentiment(processed_texts):
    """
    Perform sentiment analysis on entire corpus.
    """
    ensure_nltk_data()
    analyzer = SentimentIntensityAnalyzer()

    results = {}

    for title, data in processed_texts.items():
        print(f"\nAnalyzing: {title}")

        # Analyze full text
        full_text_sentiment = analyze_sentiment(data['full_text'], analyzer)
        full_text_sentiment['classification'] = classify_sentiment(full_text_sentiment['compound'])

        # Analyze each chapter
        chapter_sentiments = []
        for chapter_name, chapter_text in data['chapters']:
            chapter_sentiment = analyze_sentiment(chapter_text, analyzer)
            chapter_sentiment['chapter'] = chapter_name
            chapter_sentiment['classification'] = classify_sentiment(chapter_sentiment['compound'])
            chapter_sentiments.append(chapter_sentiment)

        results[title] = {
            'full_text': full_text_sentiment,
            'chapters': chapter_sentiments,
            'sentiment_trajectory': [cs['compound'] for cs in chapter_sentiments]
        }

        print(f"  Overall sentiment: {full_text_sentiment['classification']} "
              f"(compound: {full_text_sentiment['compound']:.3f})")
        print(f"  Analyzed {len(chapter_sentiments)} chapter(s)")

    return results


def print_sentiment_summary(sentiment_results):
    """Print summary of sentiment analysis."""
    print("\n" + "=" * 60)
    print("SENTIMENT ANALYSIS SUMMARY")
    print("=" * 60)

    for title, data in sentiment_results.items():
        print(f"\n{title}:")
        print(f"  Classification: {data['full_text']['classification'].upper()}")
        print(f"  Compound: {data['full_text']['compound']:.3f}")
        print(f"  Positive: {data['full_text']['positive']:.3f}")
        print(f"  Neutral: {data['full_text']['neutral']:.3f}")
        print(f"  Negative: {data['full_text']['negative']:.3f}")

        if len(data['chapters']) > 1:
            trajectory = data['sentiment_trajectory']
            print(f"  Sentiment trajectory: {min(trajectory):.3f} → {max(trajectory):.3f}")


if __name__ == '__main__':
    print("Performing sentiment analysis on Nietzsche corpus...")
    print("=" * 60)

    # Preprocess texts
    processed_texts = preprocess_texts()

    # Analyze sentiment
    sentiment_results = analyze_corpus_sentiment(processed_texts)

    # Print summary
    print_sentiment_summary(sentiment_results)

    print("\n" + "=" * 60)
    print("Sentiment analysis complete!")
