#!/usr/bin/env python3
"""
Generate content plan report.
"""

import json
import os
from typing import Dict, List, Any


def load_plan_data(base_dir: str) -> Dict[str, Any]:
    """Load all plan data files."""
    data = {}

    # Load manifest
    manifest_file = os.path.join(base_dir, 'normalized-data', 'plan', 'manifest.json')
    with open(manifest_file, 'r', encoding='utf-8') as f:
        data['manifest'] = json.load(f)

    # Load day plans
    data['days'] = []
    for day_num in range(1, 71):
        day_file = os.path.join(base_dir, 'normalized-data', 'plan', f'day-{day_num:02d}.json')
        if os.path.exists(day_file):
            with open(day_file, 'r', encoding='utf-8') as f:
                data['days'].append(json.load(f))

    # Load course data
    words_file = os.path.join(base_dir, 'normalized-data', 'words.json')
    with open(words_file, 'r', encoding='utf-8') as f:
        data['words'] = json.load(f)

    phrases_file = os.path.join(base_dir, 'normalized-data', 'phrases.json')
    with open(phrases_file, 'r', encoding='utf-8') as f:
        data['phrases'] = json.load(f)

    sentences_file = os.path.join(base_dir, 'normalized-data', 'sentences.json')
    with open(sentences_file, 'r', encoding='utf-8') as f:
        data['sentences'] = json.load(f)

    units_file = os.path.join(base_dir, 'normalized-data', 'units.json')
    with open(units_file, 'r', encoding='utf-8') as f:
        data['units'] = json.load(f)

    return data


def generate_report(data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate content plan report."""
    days = data['days']
    words = data['words']
    phrases = data['phrases']
    sentences = data['sentences']
    units = data['units']

    # Word statistics
    total_words = len(words)
    scheduled_words = sum(len(d['newWordIds']) for d in days)
    extension_words = total_words - scheduled_words

    word_counts = [len(d['newWordIds']) for d in days]
    days_with_35 = sum(1 for c in word_counts if c == 35)
    days_with_less = sum(1 for c in word_counts if c < 35)

    # Phrase statistics
    total_phrases = len(phrases)
    scheduled_phrases = sum(len(d['phraseIds']) for d in days)

    # Sentence statistics
    total_sentences = len(sentences)
    scheduled_sentences = sum(len(d['sentenceIds']) for d in days)

    # Missing data
    missing_translations = 0
    missing_phonetics = 0

    for word in words:
        if not word.get('translation'):
            missing_translations += 1
        if not word.get('phonetic'):
            missing_phonetics += 1

    for phrase in phrases:
        if not phrase.get('translation'):
            missing_translations += 1

    for sentence in sentences:
        if not sentence.get('zh'):
            missing_translations += 1

    # Warnings
    warnings = []

    if missing_translations > 0:
        warnings.append(f"{missing_translations} items missing translations")

    if missing_phonetics > 0:
        warnings.append(f"{missing_phonetics} words missing phonetics")

    if days_with_less == 70:
        warnings.append("All days have less than 35 words (data insufficient for full plan)")

    if scheduled_sentences < total_sentences:
        warnings.append(f"Some sentences not scheduled ({scheduled_sentences}/{total_sentences})")

    report = {
        "planDays": 70,
        "maxNewWordsPerDay": 35,

        "uniqueWords": total_words,
        "scheduledNewWords": scheduled_words,
        "extensionWords": extension_words,

        "daysWith35Words": days_with_35,
        "minWordsPerDay": min(word_counts),
        "maxWordsPerDay": max(word_counts),

        "units": len(units),

        "missingTranslations": missing_translations,
        "missingPhonetics": missing_phonetics,

        "warnings": warnings
    }

    return report


def main():
    """Main function to generate report."""
    base_dir = '/Volumes/Lark/Study/模块提取'

    print("Loading plan data...")
    data = load_plan_data(base_dir)

    print("Generating report...")
    report = generate_report(data)

    # Save report
    report_file = os.path.join(base_dir, 'normalized-data', 'content-plan-report.json')
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\nSaved report to {report_file}")

    # Print report
    print("\n--- Content Plan Report ---")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
