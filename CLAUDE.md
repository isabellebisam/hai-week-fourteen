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
