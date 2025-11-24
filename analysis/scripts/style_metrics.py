"""
Style metrics analysis for Nietzsche corpus.
Calculates lexical diversity, readability scores, vocabulary complexity, and distinctive words.
"""

import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
import numpy as np
from preprocess import preprocess_texts


def ensure_nltk_data():
    """Download required NLTK data."""
    datasets = ['punkt', 'stopwords']
    for dataset in datasets:
        try:
            nltk.data.find(f'tokenizers/{dataset}')
        except LookupError:
            try:
                nltk.data.find(f'corpora/{dataset}')
            except LookupError:
                print(f"Downloading {dataset}...")
                nltk.download(dataset, quiet=True)


def tokenize_words(text):
    """Tokenize text into words, excluding punctuation."""
    # Use word_tokenize and filter for alphabetic tokens
    tokens = word_tokenize(text.lower())
    words = [token for token in tokens if token.isalpha()]
    return words


def calculate_lexical_diversity(text):
    """
    Calculate type-token ratio (TTR) and related metrics.
    """
    words = tokenize_words(text)

    if not words:
        return {
            'type_token_ratio': 0.0,
            'unique_words': 0,
            'total_words': 0
        }

    unique_words = set(words)

    return {
        'type_token_ratio': len(unique_words) / len(words),
        'unique_words': len(unique_words),
        'total_words': len(words),
        'hapax_legomena': sum(1 for word, count in Counter(words).items() if count == 1),
        'avg_word_frequency': len(words) / len(unique_words)
    }


def calculate_sentence_metrics(text):
    """Calculate sentence-level statistics."""
    sentences = sent_tokenize(text)

    if not sentences:
        return {
            'sentence_count': 0,
            'avg_sentence_length': 0.0,
            'sentence_length_std': 0.0
        }

    sentence_lengths = [len(word_tokenize(sent)) for sent in sentences]

    return {
        'sentence_count': len(sentences),
        'avg_sentence_length': np.mean(sentence_lengths),
        'sentence_length_std': np.std(sentence_lengths),
        'min_sentence_length': min(sentence_lengths),
        'max_sentence_length': max(sentence_lengths)
    }


def calculate_word_metrics(text):
    """Calculate word-level statistics."""
    words = tokenize_words(text)

    if not words:
        return {
            'avg_word_length': 0.0,
            'word_length_std': 0.0
        }

    word_lengths = [len(word) for word in words]

    return {
        'avg_word_length': np.mean(word_lengths),
        'word_length_std': np.std(word_lengths),
        'min_word_length': min(word_lengths) if word_lengths else 0,
        'max_word_length': max(word_lengths) if word_lengths else 0
    }


def calculate_readability_scores(text):
    """
    Calculate various readability scores.
    """
    sentences = sent_tokenize(text)
    words = tokenize_words(text)

    if not sentences or not words:
        return {
            'flesch_reading_ease': 0.0,
            'flesch_kincaid_grade': 0.0,
            'gunning_fog': 0.0
        }

    # Count syllables (approximation)
    def count_syllables(word):
        word = word.lower()
        count = 0
        vowels = 'aeiouy'
        previous_was_vowel = False

        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                count += 1
            previous_was_vowel = is_vowel

        # Adjust for silent e
        if word.endswith('e'):
            count -= 1

        # Ensure at least one syllable
        if count == 0:
            count = 1

        return count

    total_syllables = sum(count_syllables(word) for word in words)
    total_words = len(words)
    total_sentences = len(sentences)

    # Flesch Reading Ease
    flesch_reading_ease = 206.835 - 1.015 * (total_words / total_sentences) - 84.6 * (total_syllables / total_words)

    # Flesch-Kincaid Grade Level
    flesch_kincaid_grade = 0.39 * (total_words / total_sentences) + 11.8 * (total_syllables / total_words) - 15.59

    # Gunning Fog Index (count complex words as 3+ syllables)
    complex_words = sum(1 for word in words if count_syllables(word) >= 3)
    gunning_fog = 0.4 * ((total_words / total_sentences) + 100 * (complex_words / total_words))

    return {
        'flesch_reading_ease': flesch_reading_ease,
        'flesch_kincaid_grade': flesch_kincaid_grade,
        'gunning_fog': gunning_fog,
        'avg_syllables_per_word': total_syllables / total_words,
        'complex_word_percentage': (complex_words / total_words) * 100
    }


def calculate_vocabulary_complexity(text):
    """
    Analyze vocabulary complexity.
    """
    words = tokenize_words(text)

    if not words:
        return {
            'long_words_percentage': 0.0,
            'avg_word_length': 0.0
        }

    long_words = [word for word in words if len(word) >= 7]

    return {
        'long_words_percentage': (len(long_words) / len(words)) * 100,
        'avg_word_length': np.mean([len(word) for word in words]),
        'words_over_10_chars': sum(1 for word in words if len(word) >= 10),
        'words_over_15_chars': sum(1 for word in words if len(word) >= 15)
    }


def find_distinctive_words(processed_texts, top_n=20):
    """
    Find distinctive words for each text using TF-IDF-like approach.
    """
    from sklearn.feature_extraction.text import TfidfVectorizer

    # Prepare documents
    documents = []
    titles = []

    for title, data in processed_texts.items():
        documents.append(data['full_text'])
        titles.append(title)

    # Calculate TF-IDF
    vectorizer = TfidfVectorizer(
        max_features=1000,
        stop_words='english',
        lowercase=True,
        token_pattern=r'\b[a-zA-Z]{3,}\b'  # Only words with 3+ letters
    )

    tfidf_matrix = vectorizer.fit_transform(documents)
    feature_names = vectorizer.get_feature_names_out()

    # Extract top words for each document
    distinctive = {}

    for idx, title in enumerate(titles):
        # Get TF-IDF scores for this document
        scores = tfidf_matrix[idx].toarray()[0]

        # Get top N words
        top_indices = scores.argsort()[-top_n:][::-1]
        top_words = [(feature_names[i], float(scores[i])) for i in top_indices]

        distinctive[title] = top_words

    return distinctive


def analyze_style_metrics(processed_texts):
    """
    Perform comprehensive style analysis on corpus.
    """
    ensure_nltk_data()

    results = {}

    for title, data in processed_texts.items():
        print(f"\nAnalyzing style: {title}")

        text = data['full_text']

        # Calculate all metrics
        lexical = calculate_lexical_diversity(text)
        sentences = calculate_sentence_metrics(text)
        words = calculate_word_metrics(text)
        readability = calculate_readability_scores(text)
        vocabulary = calculate_vocabulary_complexity(text)

        results[title] = {
            'lexical_diversity': lexical,
            'sentence_metrics': sentences,
            'word_metrics': words,
            'readability': readability,
            'vocabulary_complexity': vocabulary
        }

        print(f"  Type-token ratio: {lexical['type_token_ratio']:.3f}")
        print(f"  Avg sentence length: {sentences['avg_sentence_length']:.1f} words")
        print(f"  Flesch reading ease: {readability['flesch_reading_ease']:.1f}")

    # Find distinctive words
    print("\nFinding distinctive words...")
    distinctive_words = find_distinctive_words(processed_texts)

    for title in results:
        results[title]['distinctive_words'] = distinctive_words[title]

    return results


def print_style_comparison(style_results):
    """Print comparative style analysis."""
    print("\n" + "=" * 70)
    print("STYLE METRICS COMPARISON")
    print("=" * 70)

    metrics_to_compare = [
        ('Type-Token Ratio', lambda r: r['lexical_diversity']['type_token_ratio']),
        ('Avg Sentence Length', lambda r: r['sentence_metrics']['avg_sentence_length']),
        ('Avg Word Length', lambda r: r['word_metrics']['avg_word_length']),
        ('Flesch Reading Ease', lambda r: r['readability']['flesch_reading_ease']),
        ('Flesch-Kincaid Grade', lambda r: r['readability']['flesch_kincaid_grade']),
    ]

    for metric_name, extractor in metrics_to_compare:
        print(f"\n{metric_name}:")
        values = [(title, extractor(data)) for title, data in style_results.items()]
        values.sort(key=lambda x: x[1], reverse=True)

        for title, value in values:
            print(f"  {title:40} {value:6.2f}")


if __name__ == '__main__':
    print("Performing style analysis on Nietzsche corpus...")
    print("=" * 70)

    # Preprocess texts
    processed_texts = preprocess_texts()

    # Analyze style
    style_results = analyze_style_metrics(processed_texts)

    # Print comparison
    print_style_comparison(style_results)

    print("\n" + "=" * 70)
    print("Style analysis complete!")
