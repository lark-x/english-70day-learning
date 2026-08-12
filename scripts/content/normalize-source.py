#!/usr/bin/env python3
"""
Normalize source data from vocabulary handbook and unit files.
Extracts words, phrases, sentences, dialogues, and exercises.
"""

import re
import json
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class WordItem:
    id: str
    word: str
    phonetic: Optional[str] = None
    partOfSpeech: Optional[str] = None
    translation: str = ""
    exampleEn: Optional[str] = None
    exampleZh: Optional[str] = None
    sourceUnitId: str = "vocabulary-handbook"


@dataclass
class PhraseItem:
    id: str
    phrase: str
    translation: str = ""
    exampleEn: Optional[str] = None
    exampleZh: Optional[str] = None
    sourceUnitId: str = "vocabulary-handbook"


@dataclass
class SentenceItem:
    id: str
    en: str
    zh: str
    sourceUnitId: str = ""


@dataclass
class UnitInfo:
    id: str
    order: int
    title: str
    subtitle: Optional[str] = None


def parse_vocabulary_handbook(filepath: str) -> Dict[str, Any]:
    """Parse the vocabulary handbook and extract words and phrases."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    words: List[WordItem] = []
    phrases: List[PhraseItem] = []

    # Split into sections
    sections = re.split(r'^# ', content, flags=re.MULTILINE)

    current_section = None
    for section in sections:
        if section.startswith('第一部分：单词'):
            current_section = 'words'
            _parse_word_section(section, words)
        elif section.startswith('第二部分：短语/词组'):
            current_section = 'phrases'
            _parse_phrase_section(section, phrases)

    return {
        'words': words,
        'phrases': phrases
    }


def _parse_word_section(section: str, words: List[WordItem]):
    """Parse word entries from the vocabulary handbook."""
    # Split by ### headers
    entries = re.split(r'^### ', section, flags=re.MULTILINE)

    for entry in entries[1:]:  # Skip first empty split
        lines = entry.strip().split('\n')
        if not lines:
            continue

        word = lines[0].strip()
        if not word:
            continue

        # Extract phonetic
        phonetic = None
        for line in lines[1:]:
            match = re.search(r'\*\*音标\*\*:\s*(.+)', line)
            if match:
                phonetic = match.group(1).strip()
                break

        # Extract part of speech
        part_of_speech = None
        for line in lines[1:]:
            match = re.search(r'\*\*词性\*\*:\s*(.+)', line)
            if match:
                part_of_speech = match.group(1).strip()
                break

        # Extract translation
        translation = ""
        for line in lines[1:]:
            match = re.search(r'\*\*释义\*\*:\s*(.+)', line)
            if match:
                translation = match.group(1).strip()
                break

        # Extract example
        example_en = None
        example_zh = None
        for i, line in enumerate(lines[1:], 1):
            match = re.search(r'\*\*例句\*\*:\s*(.+)', line)
            if match:
                example_en = match.group(1).strip()
                # Look for translation on next line
                if i + 1 < len(lines):
                    zh_match = re.search(r'\*\*翻译\*\*:\s*(.+)', lines[i + 1])
                    if zh_match:
                        example_zh = zh_match.group(1).strip()
                break

        # Generate ID
        word_id = f"word-{len(words) + 1:04d}"

        words.append(WordItem(
            id=word_id,
            word=word,
            phonetic=phonetic,
            partOfSpeech=part_of_speech,
            translation=translation,
            exampleEn=example_en,
            exampleZh=example_zh
        ))


def _parse_phrase_section(section: str, phrases: List[PhraseItem]):
    """Parse phrase entries from the vocabulary handbook."""
    # Split by ### headers
    entries = re.split(r'^### ', section, flags=re.MULTILINE)

    for entry in entries[1:]:  # Skip first empty split
        lines = entry.strip().split('\n')
        if not lines:
            continue

        phrase = lines[0].strip()
        if not phrase:
            continue

        # Extract translation
        translation = ""
        for line in lines[1:]:
            match = re.search(r'\*\*释义\*\*:\s*(.+)', line)
            if match:
                translation = match.group(1).strip()
                break

        # Extract example
        example_en = None
        example_zh = None
        for i, line in enumerate(lines[1:], 1):
            match = re.search(r'\*\*例句\*\*:\s*(.+)', line)
            if match:
                example_en = match.group(1).strip()
                # Look for translation on next line
                if i + 1 < len(lines):
                    zh_match = re.search(r'\*\*翻译\*\*:\s*(.+)', lines[i + 1])
                    if zh_match:
                        example_zh = zh_match.group(1).strip()
                break

        # Generate ID
        phrase_id = f"phrase-{len(phrases) + 1:04d}"

        phrases.append(PhraseItem(
            id=phrase_id,
            phrase=phrase,
            translation=translation,
            exampleEn=example_en,
            exampleZh=example_zh
        ))


def parse_unit_files(base_dir: str) -> Dict[str, Any]:
    """Parse all unit files and extract content."""
    units: List[UnitInfo] = []
    sentences: List[SentenceItem] = []
    unit_phrases: List[PhraseItem] = []

    # Unit titles
    unit_titles = {
        '01': 'The Power of Language',
        '02': 'Mistakes to Success',
        '03': 'Friendship and Loyalty',
        '04': 'The Joy of Work',
        '05': 'Keeping Your Dreams Alive',
        '06': 'The Value of Money',
        '07': 'Inner Voice',
        '08': 'The Great Minds',
        '09': 'Facing Life\'s Challenges',
        '10': 'Ode to Public Transport',
        '11': 'Cyber World',
        '12': 'A Break from Life'
    }

    for unit_num, title in unit_titles.items():
        unit_id = f"unit-{unit_num}"
        units.append(UnitInfo(
            id=unit_id,
            order=int(unit_num),
            title=title
        ))

        # Parse key sentences
        key_sentences_file = os.path.join(base_dir, f'Unit_{unit_num}', f'Unit_{unit_num}_key_sentences.md')
        if os.path.exists(key_sentences_file):
            _parse_key_sentences(key_sentences_file, unit_id, sentences)

        # Parse phrases from unit files
        phrases_file = os.path.join(base_dir, f'Unit_{unit_num}', f'Unit_{unit_num}_phrases_expressions.md')
        if os.path.exists(phrases_file):
            _parse_unit_phrases(phrases_file, unit_id, unit_phrases)

    return {
        'units': units,
        'sentences': sentences,
        'unit_phrases': unit_phrases
    }


def _parse_key_sentences(filepath: str, unit_id: str, sentences: List[SentenceItem]) -> List[SentenceItem]:
    """Parse key sentences from unit file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by numbered items
    items = re.split(r'^\d+\.\s+', content, flags=re.MULTILINE)

    for idx, item in enumerate(items[1:], 1):  # Skip first empty split
        lines = item.strip().split('\n')
        if not lines:
            continue

        # Collect English and Chinese lines
        en_lines = []
        zh_lines = []
        is_chinese = False

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check if line contains Chinese characters
            if re.search(r'[\u4e00-\u9fff]', line):
                is_chinese = True
                zh_lines.append(line)
            elif is_chinese:
                # Already in Chinese section
                zh_lines.append(line)
            else:
                en_lines.append(line)

        en = ' '.join(en_lines)
        zh = ' '.join(zh_lines)

        if en and zh:
            sentence_id = f"sentence-{len(sentences) + 1:04d}"
            sentences.append(SentenceItem(
                id=sentence_id,
                en=en,
                zh=zh,
                sourceUnitId=unit_id
            ))

    return sentences


def _parse_unit_phrases(filepath: str, unit_id: str, phrases: List[PhraseItem]) -> List[PhraseItem]:
    """Parse phrases from unit file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if file contains table format
    if '| --- |' in content:
        _parse_unit_phrases_table(content, unit_id, phrases)
    else:
        _parse_unit_phrases_text(content, unit_id, phrases)

    return phrases


def _parse_unit_phrases_table(content: str, unit_id: str, phrases: List[PhraseItem]):
    """Parse phrases from table format."""
    lines = content.split('\n')

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#') or line.startswith('**') or line.startswith('---'):
            continue

        # Skip table header and separator
        if '短语 (Phrase)' in line or '| --- |' in line:
            continue

        # Parse table row: | phrase | definition | translation |
        match = re.match(r'\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|', line)
        if match:
            phrase = match.group(1).strip()
            definition = match.group(2).strip()
            translation = match.group(3).strip()

            if phrase and translation:
                phrase_id = f"unit-phrase-{len(phrases) + 1:04d}"
                phrases.append(PhraseItem(
                    id=phrase_id,
                    phrase=phrase,
                    translation=translation,
                    sourceUnitId=unit_id
                ))


def _parse_unit_phrases_text(content: str, unit_id: str, phrases: List[PhraseItem]):
    """Parse phrases from text format."""
    lines = content.split('\n')

    # Skip header lines
    start_idx = 0
    for i, line in enumerate(lines):
        if line.strip() == '---':
            start_idx = i + 1
            break

    # Process remaining lines
    i = start_idx
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        # Skip lines that are just definitions (start with "to " or contain only English)
        if line.startswith('to ') or line.startswith('(') or line.startswith('if '):
            i += 1
            continue

        # Check if line contains a phrase (not starting with common definition patterns)
        # Phrases are typically short and don't start with "to" or "("
        if not line.startswith('Directions') and not line.startswith('Read'):
            # Look for phrase followed by definition on same line
            # Pattern: "phrase definition chinese"
            parts = re.split(r'\s{2,}', line)  # Split by 2+ spaces
            if len(parts) >= 2:
                phrase = parts[0].strip()
                rest = ' '.join(parts[1:])

                # Extract Chinese translation (after English definition)
                # Look for Chinese characters
                zh_match = re.search(r'([\u4e00-\u9fff].+)', rest)
                if zh_match:
                    translation = zh_match.group(1).strip()
                    if phrase and translation:
                        phrase_id = f"unit-phrase-{len(phrases) + 1:04d}"
                        phrases.append(PhraseItem(
                            id=phrase_id,
                            phrase=phrase,
                            translation=translation,
                            sourceUnitId=unit_id
                        ))

        i += 1


def main():
    """Main function to normalize all source data."""
    base_dir = '/Volumes/Lark/Study/模块提取'
    vocab_file = os.path.join(base_dir, '英语二_学习单词手册.md')

    print("Parsing vocabulary handbook...")
    vocab_data = parse_vocabulary_handbook(vocab_file)

    print(f"Found {len(vocab_data['words'])} words")
    print(f"Found {len(vocab_data['phrases'])} phrases")

    print("\nParsing unit files...")
    unit_data = parse_unit_files(base_dir)

    print(f"Found {len(unit_data['units'])} units")
    print(f"Found {len(unit_data['sentences'])} sentences")
    print(f"Found {len(unit_data['unit_phrases'])} unit phrases")

    # Combine all phrases
    all_phrases = vocab_data['phrases'] + unit_data['unit_phrases']

    # Save normalized data
    output_dir = os.path.join(base_dir, 'normalized-data')
    os.makedirs(output_dir, exist_ok=True)

    # Save words
    words_file = os.path.join(output_dir, 'words.json')
    with open(words_file, 'w', encoding='utf-8') as f:
        json.dump([asdict(w) for w in vocab_data['words']], f, ensure_ascii=False, indent=2)
    print(f"\nSaved words to {words_file}")

    # Save phrases
    phrases_file = os.path.join(output_dir, 'phrases.json')
    with open(phrases_file, 'w', encoding='utf-8') as f:
        json.dump([asdict(p) for p in all_phrases], f, ensure_ascii=False, indent=2)
    print(f"Saved phrases to {phrases_file}")

    # Save units
    units_file = os.path.join(output_dir, 'units.json')
    with open(units_file, 'w', encoding='utf-8') as f:
        json.dump([asdict(u) for u in unit_data['units']], f, ensure_ascii=False, indent=2)
    print(f"Saved units to {units_file}")

    # Save sentences
    sentences_file = os.path.join(output_dir, 'sentences.json')
    with open(sentences_file, 'w', encoding='utf-8') as f:
        json.dump([asdict(s) for s in unit_data['sentences']], f, ensure_ascii=False, indent=2)
    print(f"Saved sentences to {sentences_file}")

    # Print sample data
    print("\n--- Sample Words ---")
    for word in vocab_data['words'][:3]:
        print(f"  {word.word}: {word.translation}")

    print("\n--- Sample Phrases ---")
    for phrase in all_phrases[:5]:
        print(f"  {phrase.phrase}: {phrase.translation}")

    print("\n--- Sample Sentences ---")
    for sentence in unit_data['sentences'][:3]:
        print(f"  EN: {sentence.en}")
        print(f"  ZH: {sentence.zh}")
        print()


if __name__ == '__main__':
    main()
