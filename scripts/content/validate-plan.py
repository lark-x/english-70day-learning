#!/usr/bin/env python3
"""
Validate 70-day learning plan.
Checks for completeness, consistency, and correctness.
"""

import json
import os
from typing import Dict, List, Any, Set


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


def validate_plan(data: Dict[str, Any]) -> List[str]:
    """
    Validate the 70-day plan.

    Returns list of validation errors (empty if valid).
    """
    errors: List[str] = []

    days = data['days']
    words = data['words']
    phrases = data['phrases']
    sentences = data['sentences']
    units = data['units']

    # Create ID sets for quick lookup
    word_ids = {w['id'] for w in words}
    phrase_ids = {p['id'] for p in phrases}
    sentence_ids = {s['id'] for s in sentences}
    unit_ids = {u['id'] for u in units}

    # Check 1: Must have exactly 70 days
    if len(days) != 70:
        errors.append(f"Expected 70 days, found {len(days)}")

    # Check 2: Days must be numbered 1-70
    day_numbers = {d['day'] for d in days}
    expected_days = set(range(1, 71))
    if day_numbers != expected_days:
        missing = expected_days - day_numbers
        extra = day_numbers - expected_days
        if missing:
            errors.append(f"Missing days: {sorted(missing)}")
        if extra:
            errors.append(f"Extra days: {sorted(extra)}")

    # Check 3: Each day's newWordIds.length <= 35
    for day in days:
        if len(day['newWordIds']) > 35:
            errors.append(f"Day {day['day']}: {len(day['newWordIds'])} words exceeds limit of 35")

    # Check 4: Word uniqueness - same word cannot be new in two different days
    seen_word_ids: Set[str] = set()
    for day in days:
        for word_id in day['newWordIds']:
            if word_id in seen_word_ids:
                errors.append(f"Word {word_id} appears as new word in multiple days")
            seen_word_ids.add(word_id)

    # Check 5: All word IDs must exist in course data
    for day in days:
        for word_id in day['newWordIds']:
            if word_id not in word_ids:
                errors.append(f"Day {day['day']}: Word ID {word_id} not found in course data")

    # Check 6: All phrase IDs must exist in course data
    for day in days:
        for phrase_id in day['phraseIds']:
            if phrase_id not in phrase_ids:
                errors.append(f"Day {day['day']}: Phrase ID {phrase_id} not found in course data")

    # Check 7: All sentence IDs must exist in course data
    for day in days:
        for sentence_id in day['sentenceIds']:
            if sentence_id not in sentence_ids:
                errors.append(f"Day {day['day']}: Sentence ID {sentence_id} not found in course data")

    # Check 8: All unit IDs must exist in course data
    for day in days:
        for unit_id in day['sourceUnitIds']:
            if unit_id not in unit_ids:
                errors.append(f"Day {day['day']}: Unit ID {unit_id} not found in course data")

    # Check 9: All sentences must have both English and Chinese
    for sentence in sentences:
        if not sentence.get('en') or not sentence.get('zh'):
            errors.append(f"Sentence {sentence['id']}: Missing English or Chinese text")

    # Check 10: Manifest must match day plans
    manifest_days = {d['day'] for d in data['manifest']['days']}
    if manifest_days != day_numbers:
        errors.append("Manifest days do not match day plan days")

    return errors


def print_validation_report(errors: List[str]):
    """Print validation report."""
    if not errors:
        print("\n✅ Validation PASSED - No errors found!")
    else:
        print(f"\n❌ Validation FAILED - {len(errors)} error(s) found:")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")


def print_plan_statistics(data: Dict[str, Any]):
    """Print plan statistics."""
    days = data['days']

    # Word statistics
    total_words = sum(len(d['newWordIds']) for d in days)
    word_counts = [len(d['newWordIds']) for d in days]

    # Phrase statistics
    total_phrases = sum(len(d['phraseIds']) for d in days)
    phrase_counts = [len(d['phraseIds']) for d in days]

    # Sentence statistics
    total_sentences = sum(len(d['sentenceIds']) for d in days)
    sentence_counts = [len(d['sentenceIds']) for d in days]

    print("\n--- Plan Statistics ---")
    print(f"Total days: {len(days)}")
    print(f"Total words: {total_words}")
    print(f"Total phrases: {total_phrases}")
    print(f"Total sentences: {total_sentences}")

    print(f"\nWord count per day:")
    print(f"  Min: {min(word_counts)}")
    print(f"  Max: {max(word_counts)}")
    print(f"  Average: {total_words / len(days):.1f}")
    print(f"  Days with 35 words: {sum(1 for c in word_counts if c == 35)}")
    print(f"  Days with < 35 words: {sum(1 for c in word_counts if c < 35)}")

    print(f"\nPhrase count per day:")
    print(f"  Min: {min(phrase_counts)}")
    print(f"  Max: {max(phrase_counts)}")
    print(f"  Average: {total_phrases / len(days):.1f}")

    print(f"\nSentence count per day:")
    print(f"  Min: {min(sentence_counts)}")
    print(f"  Max: {max(sentence_counts)}")
    print(f"  Average: {total_sentences / len(days):.1f}")

    # Unit distribution
    unit_days: Dict[str, int] = {}
    for day in days:
        for unit_id in day['sourceUnitIds']:
            unit_days[unit_id] = unit_days.get(unit_id, 0) + 1

    print(f"\nUnit distribution:")
    for unit_id, count in sorted(unit_days.items()):
        print(f"  {unit_id}: {count} days")


def main():
    """Main function to validate 70-day plan."""
    base_dir = '/Volumes/Lark/Study/模块提取'

    print("Loading plan data...")
    data = load_plan_data(base_dir)

    print("Validating plan...")
    errors = validate_plan(data)

    print_plan_statistics(data)
    print_validation_report(errors)

    # Return exit code
    return 0 if not errors else 1


if __name__ == '__main__':
    exit(main())
