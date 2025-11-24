# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This repository contains a collection of Friedrich Nietzsche's philosophical works from Project Gutenberg. It serves as a text corpus for analysis, research, or reference purposes.

## Available Texts

The repository includes 8 complete works by Nietzsche (57,375 total lines):

1. **Beyond Good and Evil** (6,503 lines, 400KB) - Nietzsche's critique of traditional morality
2. **Ecce Homo** (6,652 lines, 297KB) - Autobiographical work
3. **Human, All Too Human** (4,313 lines, 239KB) - Aphoristic work on human nature
4. **The Antichrist** (3,774 lines, 222KB) - Critique of Christianity
5. **The Birth of Tragedy** (5,832 lines, 346KB) - Early work on Greek tragedy and aesthetics
6. **The Genealogy of Morals** (5,859 lines, 351KB) - Investigation into the origins of moral concepts
7. **The Twilight of the Idols** (8,442 lines, 444KB) - Late work critiquing Western philosophy
8. **Thus Spake Zarathustra** (16,000 lines, 667KB) - Philosophical novel featuring the prophet Zarathustra

All texts are English translations in Project Gutenberg format, including headers with licensing information and translator credits.

## Common Operations

### Searching for Concepts or Quotes

Search across all texts for a specific term:
```bash
grep -i "eternal recurrence" *.txt
grep -n "God is dead" *.txt  # With line numbers
grep -A 3 -B 3 "Übermensch" *.txt  # With 3 lines of context
```

Search within a specific work:
```bash
grep -i "superman" "Nietzsche_Thus Spake Zarathustra_A Book for All and None.txt"
```

### Text Analysis

Count word occurrences:
```bash
grep -o -i "will to power" *.txt | wc -l
```

Find all books mentioning a concept:
```bash
grep -l "nihilism" *.txt
```

### Viewing Content

Display specific sections (example for line ranges):
```bash
sed -n '100,200p' "Nietzsche_Beyond Good and Evil.txt"
head -n 100 "Nietzsche_The Antichrist.txt"
tail -n 50 "Nietzsche_Ecce Homo.txt"
```

## File Format

- All files are UTF-8 encoded plain text with `.txt` extension
- Naming convention: `Nietzsche_[Title].txt`
- Each file includes Project Gutenberg header (licensing, translator info, release date)
- Each file includes Project Gutenberg footer (donation info, legal notices)
- The actual work content is between the header and footer sections

## Text Processing Considerations

When processing these texts:
- The beginning of each file contains ~50 lines of Project Gutenberg metadata
- The end of each file contains ~30-40 lines of Project Gutenberg legal/donation information
- Main content starts after "*** START OF THE PROJECT GUTENBERG EBOOK [TITLE] ***"
- Main content ends before "*** END OF THE PROJECT GUTENBERG EBOOK [TITLE] ***"
- Some works contain translator's notes, prefaces, or commentary in addition to Nietzsche's text

## Analysis System

This repository includes a comprehensive text analysis system with sentiment analysis, style metrics, and interactive visualizations.

### Setup and Installation

Install Python dependencies:
```bash
pip install -r requirements.txt
```

Download required NLTK data (automatic on first run):
```bash
python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt'); nltk.download('stopwords')"
```

### Running the Analysis

**Complete analysis pipeline:**
```bash
python3 analysis/scripts/analyze_corpus.py
```

This runs all analyses and generates `analysis/output/analysis_results.json` with complete results.

**Individual analysis scripts:**
```bash
# Preprocessing only (strip Gutenberg headers/footers)
python3 analysis/scripts/preprocess.py

# Sentiment analysis only (VADER-based)
python3 analysis/scripts/sentiment_analysis.py

# Style metrics only (readability, lexical diversity, etc.)
python3 analysis/scripts/style_metrics.py
```

### Viewing Visualizations

Start a local web server:
```bash
python3 -m http.server 8000
```

Then open browser to `http://localhost:8000`

### Project Structure

```
analysis/
├── scripts/              # Analysis Python scripts
│   ├── preprocess.py           # Text preprocessing
│   ├── sentiment_analysis.py   # VADER sentiment analysis
│   ├── style_metrics.py        # Style and readability metrics
│   └── analyze_corpus.py       # Main analysis pipeline
├── data/                 # Cleaned text files (generated)
└── output/               # JSON analysis results (generated)
    ├── analysis_results.json    # Complete results
    └── analysis_summary.json    # High-level summary

js/
└── app.js               # Web visualization code (D3.js)

index.html               # Main web interface
```

### Analysis Features

**Sentiment Analysis (VADER):**
- Full-text and chapter-level analysis
- Compound, positive, neutral, negative scores
- Sentiment classification and trajectory tracking

**Style Metrics:**
- Lexical diversity (type-token ratio, hapax legomena)
- Sentence and word length statistics
- Readability scores (Flesch Reading Ease, Flesch-Kincaid Grade, Gunning Fog)
- Vocabulary complexity (complex words, long words)
- Distinctive word identification (TF-IDF)

**Visualizations:**
- Sentiment comparison charts and trajectories
- Style metrics comparison tables
- Dynamic word clouds (D3.js)
- Vocabulary overlap heatmaps
- Word frequency comparisons

### Output Files

- `analysis/output/analysis_results.json` - Complete analysis data for all texts
- `analysis/output/analysis_summary.json` - Quick reference summary
- `analysis/data/*_clean.txt` - Preprocessed texts with metadata removed

### Technical Stack

**Python:**
- NLTK (tokenization, VADER sentiment analysis)
- scikit-learn (TF-IDF for distinctive words)
- NumPy (numerical computations)

**Frontend:**
- Bootstrap 5 (UI framework)
- D3.js v7 (data visualizations)
- D3-cloud (word cloud generation)
- Vanilla JavaScript (no framework dependencies)

### Development Workflow

1. **Modify analysis scripts** in `analysis/scripts/`
2. **Run analysis** with `python3 analysis/scripts/analyze_corpus.py`
3. **Check output** in `analysis/output/analysis_results.json`
4. **View results** by opening `index.html` in browser
5. **Update visualizations** by editing `js/app.js`

### Common Analysis Tasks

**Add new style metric:**
1. Add calculation function to `analysis/scripts/style_metrics.py`
2. Include in `analyze_style_metrics()` function
3. Update JSON output structure
4. Add visualization in `js/app.js`

**Add new visualization:**
1. Add tab/section to `index.html`
2. Create chart function in `js/app.js`
3. Call from `initializeApp()` or appropriate event handler

**Modify preprocessing:**
1. Edit detection logic in `analysis/scripts/preprocess.py`
2. Adjust `strip_gutenberg_metadata()` or `detect_chapters()`
3. Rerun full analysis pipeline

### Dependencies

See `requirements.txt` for Python dependencies:
- `nltk>=3.8.1` - Natural language processing
- `numpy>=1.24.0` - Numerical computing
- `scikit-learn>=1.3.0` - Machine learning (TF-IDF)
