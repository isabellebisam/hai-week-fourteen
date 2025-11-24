"""
Preprocessing script for Nietzsche text corpus.
Strips Project Gutenberg headers and footers while preserving translator notes and prefaces.
"""

import re
import os
from pathlib import Path


def strip_gutenberg_metadata(text, filename):
    """
    Remove Project Gutenberg headers and footers from text.
    Preserves translator notes and prefaces.
    """
    # Find START marker
    start_pattern = r'\*\*\* START OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*'
    start_match = re.search(start_pattern, text, re.IGNORECASE)

    # Find END marker
    end_pattern = r'\*\*\* END OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*'
    end_match = re.search(end_pattern, text, re.IGNORECASE)

    if start_match and end_match:
        # Extract content between markers
        content = text[start_match.end():end_match.start()].strip()
    elif start_match:
        # Only start marker found, take everything after it
        content = text[start_match.end():].strip()
    else:
        # No markers found, use entire text
        print(f"Warning: No Gutenberg markers found in {filename}")
        content = text

    return content


def extract_title_from_filename(filename):
    """Extract clean title from filename."""
    # Remove 'Nietzsche_' prefix and '.txt' extension
    title = filename.replace('Nietzsche_', '').replace('.txt', '')
    # Handle special case for Zarathustra
    title = title.replace('_A Book for All and None', '')
    return title


def detect_chapters(text, title):
    """
    Detect chapter divisions in text.
    Returns list of (chapter_name, chapter_text) tuples.
    """
    chapters = []

    # Common chapter patterns
    patterns = [
        r'\n\s*CHAPTER\s+([IVXLCDM]+|[0-9]+)\.?\s*([^\n]*)\n',
        r'\n\s*PART\s+([IVXLCDM]+|[0-9]+)\.?\s*([^\n]*)\n',
        r'\n\s*([IVXLCDM]+)\.\s*([^\n]+)\n',
        r'\n\s*([0-9]+)\.\s*([^\n]+)\n',
    ]

    # Try each pattern
    for pattern in patterns:
        matches = list(re.finditer(pattern, text))
        if len(matches) >= 3:  # Need at least 3 chapters to be confident
            for i, match in enumerate(matches):
                start = match.start()
                end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

                chapter_num = match.group(1)
                chapter_title = match.group(2).strip() if len(match.groups()) > 1 else ''
                chapter_text = text[match.end():end].strip()

                if chapter_title:
                    chapter_name = f"Chapter {chapter_num}: {chapter_title}"
                else:
                    chapter_name = f"Chapter {chapter_num}"

                chapters.append((chapter_name, chapter_text))

            return chapters

    # If no chapters detected, treat entire text as one unit
    return [("Full Text", text)]


def preprocess_texts(input_dir='.', output_dir='analysis/data'):
    """
    Preprocess all Nietzsche texts.
    Returns dict with cleaned texts and metadata.
    """
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Find all Nietzsche text files
    text_files = sorted([f for f in os.listdir(input_dir) if f.startswith('Nietzsche_') and f.endswith('.txt')])

    processed_texts = {}

    for filename in text_files:
        filepath = os.path.join(input_dir, filename)
        title = extract_title_from_filename(filename)

        print(f"Processing: {title}")

        # Read file
        with open(filepath, 'r', encoding='utf-8') as f:
            raw_text = f.read()

        # Strip Gutenberg metadata
        cleaned_text = strip_gutenberg_metadata(raw_text, filename)

        # Detect chapters
        chapters = detect_chapters(cleaned_text, title)

        # Save cleaned full text
        clean_filepath = os.path.join(output_dir, f"{title.replace(' ', '_')}_clean.txt")
        with open(clean_filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)

        processed_texts[title] = {
            'filename': filename,
            'clean_filepath': clean_filepath,
            'full_text': cleaned_text,
            'chapters': chapters,
            'num_chapters': len(chapters),
            'word_count': len(cleaned_text.split()),
            'char_count': len(cleaned_text)
        }

        print(f"  - {len(chapters)} chapter(s) detected")
        print(f"  - {processed_texts[title]['word_count']:,} words")

    return processed_texts


if __name__ == '__main__':
    print("Preprocessing Nietzsche corpus...")
    print("=" * 50)

    texts = preprocess_texts()

    print("\n" + "=" * 50)
    print(f"Successfully processed {len(texts)} texts")
    print(f"Output saved to: analysis/data/")
