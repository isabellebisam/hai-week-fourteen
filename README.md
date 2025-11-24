# Nietzsche Corpus Analysis

A comprehensive text analysis system for Friedrich Nietzsche's philosophical works from Project Gutenberg. This repository includes sentiment analysis, style metrics, and interactive visualizations.

## Contents

The repository includes 8 complete works by Nietzsche:
- Beyond Good and Evil
- Ecce Homo
- Human, All Too Human
- The Antichrist
- The Birth of Tragedy
- The Genealogy of Morals
- The Twilight of the Idols
- Thus Spake Zarathustra

## Features

### Text Analysis
- **Preprocessing**: Strips Project Gutenberg headers/footers while preserving translator notes
- **Sentiment Analysis**: VADER-based analysis at both full-text and chapter levels
- **Style Metrics**:
  - Lexical diversity (type-token ratio)
  - Average sentence and word length
  - Readability scores (Flesch Reading Ease, Flesch-Kincaid Grade, Gunning Fog)
  - Vocabulary complexity
  - Distinctive word identification

### Interactive Visualizations
- Sentiment analysis charts and trajectories
- Style metrics comparison
- Dynamic word clouds (D3.js)
- Vocabulary overlap heatmaps
- Word frequency comparisons

## Setup

### Prerequisites
- Python 3.8 or higher
- Modern web browser (for visualizations)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd hai-week-fourteen
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Download required NLTK data (automatic on first run):
```bash
python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt'); nltk.download('stopwords')"
```

## Usage

### Run Complete Analysis

Execute the main analysis script:
```bash
python3 analysis/scripts/analyze_corpus.py
```

This will:
1. Preprocess all texts (strip Gutenberg metadata)
2. Perform sentiment analysis
3. Calculate style metrics
4. Generate word frequency data
5. Calculate vocabulary overlap
6. Save results to `analysis/output/analysis_results.json`

### View Visualizations

After running the analysis, open the web interface:

1. Start a local web server:
```bash
python3 -m http.server 8000
```

2. Open your browser to: `http://localhost:8000`

### Run Individual Analysis Scripts

**Preprocessing only:**
```bash
python3 analysis/scripts/preprocess.py
```

**Sentiment analysis only:**
```bash
python3 analysis/scripts/sentiment_analysis.py
```

**Style metrics only:**
```bash
python3 analysis/scripts/style_metrics.py
```

## Project Structure

```
hai-week-fourteen/
├── analysis/
│   ├── scripts/          # Python analysis scripts
│   │   ├── preprocess.py
│   │   ├── sentiment_analysis.py
│   │   ├── style_metrics.py
│   │   └── analyze_corpus.py
│   ├── data/             # Cleaned text files
│   └── output/           # JSON analysis results
├── js/
│   └── app.js            # Web visualization code
├── index.html            # Main web interface
├── requirements.txt      # Python dependencies
├── CLAUDE.md            # Development guide
└── Nietzsche_*.txt      # Original texts
```

## Output Files

### `analysis/output/analysis_results.json`
Complete analysis results including:
- Text metadata (word counts, chapter counts)
- Sentiment scores (full-text and chapter-level)
- Style metrics (readability, lexical diversity, etc.)
- Word frequency data
- Vocabulary overlap statistics

### `analysis/output/analysis_summary.json`
High-level summary with key metrics for quick reference.

### `analysis/data/*_clean.txt`
Preprocessed text files with Gutenberg metadata removed.

## Technical Details

### Sentiment Analysis
- Uses VADER (Valence Aware Dictionary and sEntiment Reasoner)
- Provides compound, positive, neutral, and negative scores
- Classifies overall sentiment as positive/neutral/negative
- Tracks sentiment trajectory across chapters

### Style Metrics

**Lexical Diversity:**
- Type-token ratio (unique words / total words)
- Hapax legomena count (words appearing once)

**Readability Scores:**
- Flesch Reading Ease (0-100, higher = easier)
- Flesch-Kincaid Grade Level
- Gunning Fog Index

**Vocabulary Complexity:**
- Average word/sentence length
- Complex word percentage (3+ syllables)
- Long word analysis (7+, 10+, 15+ characters)

### Distinctive Words
Uses TF-IDF (Term Frequency-Inverse Document Frequency) to identify words most characteristic of each text.

## License

The Nietzsche texts are from Project Gutenberg and are in the public domain in the United States.

The analysis code and visualizations are provided as-is for educational and research purposes.
