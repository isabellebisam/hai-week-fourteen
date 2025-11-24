"""
Main analysis script for Nietzsche corpus.
Runs all analyses and generates JSON output for web visualization.
"""

import json
import os
from pathlib import Path
from datetime import datetime

from preprocess import preprocess_texts
from sentiment_analysis import analyze_corpus_sentiment
from style_metrics import analyze_style_metrics


def serialize_results(obj):
    """Convert numpy types to native Python types for JSON serialization."""
    import numpy as np

    if isinstance(obj, dict):
        return {k: serialize_results(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize_results(item) for item in obj]
    elif isinstance(obj, tuple):
        return [serialize_results(item) for item in obj]
    elif isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj


def generate_word_frequency_data(processed_texts, top_n=100):
    """
    Generate word frequency data for each text.
    """
    from collections import Counter
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize

    try:
        stop_words = set(stopwords.words('english'))
    except LookupError:
        import nltk
        nltk.download('stopwords', quiet=True)
        stop_words = set(stopwords.words('english'))

    word_freq_data = {}

    for title, data in processed_texts.items():
        # Tokenize and filter
        words = word_tokenize(data['full_text'].lower())
        words = [w for w in words if w.isalpha() and w not in stop_words and len(w) > 3]

        # Count frequencies
        freq = Counter(words)
        top_words = freq.most_common(top_n)

        word_freq_data[title] = {
            'words': [word for word, count in top_words],
            'frequencies': [count for word, count in top_words]
        }

    return word_freq_data


def generate_vocabulary_overlap(processed_texts):
    """
    Calculate vocabulary overlap between texts.
    """
    from nltk.tokenize import word_tokenize

    # Get vocabulary for each text
    vocabularies = {}
    for title, data in processed_texts.items():
        words = word_tokenize(data['full_text'].lower())
        vocab = set(w for w in words if w.isalpha() and len(w) > 3)
        vocabularies[title] = vocab

    # Calculate pairwise overlaps
    overlap_matrix = {}
    titles = list(vocabularies.keys())

    for i, title1 in enumerate(titles):
        overlap_matrix[title1] = {}
        for title2 in titles:
            if title1 == title2:
                overlap_matrix[title1][title2] = 100.0
            else:
                vocab1 = vocabularies[title1]
                vocab2 = vocabularies[title2]
                intersection = vocab1 & vocab2
                union = vocab1 | vocab2
                jaccard = len(intersection) / len(union) * 100 if union else 0
                overlap_matrix[title1][title2] = jaccard

    # Also calculate unique words per text
    unique_words = {}
    all_vocabs = set.union(*vocabularies.values())

    for title, vocab in vocabularies.items():
        # Words unique to this text
        unique = vocab - set.union(*[v for t, v in vocabularies.items() if t != title])
        unique_words[title] = {
            'count': len(unique),
            'percentage': len(unique) / len(vocab) * 100 if vocab else 0,
            'examples': sorted(list(unique))[:20]  # Top 20 examples
        }

    return {
        'overlap_matrix': overlap_matrix,
        'unique_words': unique_words,
        'total_unique_words': len(all_vocabs)
    }


def run_full_analysis(output_dir='analysis/output'):
    """
    Run complete analysis pipeline and save results.
    """
    print("=" * 70)
    print("NIETZSCHE CORPUS ANALYSIS")
    print("=" * 70)

    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Step 1: Preprocess texts
    print("\n[1/5] Preprocessing texts...")
    processed_texts = preprocess_texts()

    # Step 2: Sentiment analysis
    print("\n[2/5] Analyzing sentiment...")
    sentiment_results = analyze_corpus_sentiment(processed_texts)

    # Step 3: Style metrics
    print("\n[3/5] Calculating style metrics...")
    style_results = analyze_style_metrics(processed_texts)

    # Step 4: Word frequency analysis
    print("\n[4/5] Generating word frequency data...")
    word_freq_data = generate_word_frequency_data(processed_texts)

    # Step 5: Vocabulary overlap
    print("\n[5/5] Calculating vocabulary overlap...")
    vocab_overlap = generate_vocabulary_overlap(processed_texts)

    # Combine all results
    print("\nCombining results...")
    combined_results = {
        'metadata': {
            'analysis_date': datetime.now().isoformat(),
            'num_texts': len(processed_texts),
            'texts': list(processed_texts.keys())
        },
        'texts': {}
    }

    for title in processed_texts.keys():
        combined_results['texts'][title] = {
            'basic_info': {
                'word_count': processed_texts[title]['word_count'],
                'char_count': processed_texts[title]['char_count'],
                'num_chapters': processed_texts[title]['num_chapters']
            },
            'sentiment': sentiment_results[title],
            'style': style_results[title],
            'word_frequencies': word_freq_data[title]
        }

    combined_results['corpus_wide'] = {
        'vocabulary_overlap': vocab_overlap
    }

    # Serialize and save as JSON
    print("\nSaving results to JSON...")
    serialized_results = serialize_results(combined_results)

    output_file = os.path.join(output_dir, 'analysis_results.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(serialized_results, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Results saved to: {output_file}")

    # Also save a summary
    summary = {
        'texts': list(processed_texts.keys()),
        'total_words': sum(d['word_count'] for d in processed_texts.values()),
        'analysis_date': datetime.now().isoformat(),
        'overall_sentiment': {
            title: {
                'compound': sentiment_results[title]['full_text']['compound'],
                'classification': sentiment_results[title]['full_text']['classification']
            }
            for title in processed_texts.keys()
        },
        'readability_comparison': {
            title: {
                'flesch_reading_ease': style_results[title]['readability']['flesch_reading_ease'],
                'flesch_kincaid_grade': style_results[title]['readability']['flesch_kincaid_grade']
            }
            for title in processed_texts.keys()
        }
    }

    summary_file = os.path.join(output_dir, 'analysis_summary.json')
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(serialize_results(summary), f, indent=2, ensure_ascii=False)

    print(f"✓ Summary saved to: {summary_file}")

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE!")
    print("=" * 70)
    print(f"\nTotal words analyzed: {sum(d['word_count'] for d in processed_texts.values()):,}")
    print(f"Output directory: {output_dir}")

    return combined_results


if __name__ == '__main__':
    results = run_full_analysis()
