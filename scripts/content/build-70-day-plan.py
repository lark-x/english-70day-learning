#!/usr/bin/env python3
"""
Build 70-day learning plan from normalized data.
Implements vocabulary deduplication, coreScore calculation, and plan generation.
"""

import json
import os
from typing import Dict, List, Any, Set
from dataclasses import dataclass, asdict


@dataclass
class DayPlan:
    day: int
    sourceUnitIds: List[str]
    title: str
    newWordIds: List[str]
    phraseIds: List[str]
    sentenceIds: List[str]
    compositionId: str = ""


@dataclass
class WordWithScore:
    word_id: str
    word: str
    translation: str
    core_score: float
    priority: str  # "core", "important", "extension"
    source_unit_id: str


def load_normalized_data(base_dir: str) -> Dict[str, Any]:
    """Load all normalized data files."""
    data = {}

    # Load words
    words_file = os.path.join(base_dir, 'normalized-data', 'words.json')
    with open(words_file, 'r', encoding='utf-8') as f:
        data['words'] = json.load(f)

    # Load phrases
    phrases_file = os.path.join(base_dir, 'normalized-data', 'phrases.json')
    with open(phrases_file, 'r', encoding='utf-8') as f:
        data['phrases'] = json.load(f)

    # Load units
    units_file = os.path.join(base_dir, 'normalized-data', 'units.json')
    with open(units_file, 'r', encoding='utf-8') as f:
        data['units'] = json.load(f)

    # Load sentences
    sentences_file = os.path.join(base_dir, 'normalized-data', 'sentences.json')
    with open(sentences_file, 'r', encoding='utf-8') as f:
        data['sentences'] = json.load(f)

    return data


def calculate_core_score(word: Dict[str, Any], sentences: List[Dict[str, Any]], phrases: List[Dict[str, Any]]) -> float:
    """
    Calculate coreScore for a word based on various factors.

    Scoring weights:
    - In sentences: +40
    - In phrases: +20
    - Has example: +10
    - Has phonetic: +5
    - Word length (shorter = higher score): +1-10
    """
    score = 0.0
    word_text = word['word'].lower()

    # Check if word appears in sentences
    for sentence in sentences:
        if word_text in sentence['en'].lower():
            score += 40
            break

    # Check if word appears in phrases
    for phrase in phrases:
        if word_text in phrase['phrase'].lower():
            score += 20
            break

    # Has example sentence
    if word.get('exampleEn'):
        score += 10

    # Has phonetic
    if word.get('phonetic'):
        score += 5

    # Word length (shorter words are often more basic/important)
    length = len(word_text)
    if length <= 4:
        score += 10
    elif length <= 6:
        score += 7
    elif length <= 8:
        score += 5
    elif length <= 10:
        score += 3
    else:
        score += 1

    return score


def assign_priority(score: float) -> str:
    """Assign priority based on coreScore."""
    if score >= 50:
        return "core"
    elif score >= 30:
        return "important"
    else:
        return "extension"


def deduplicate_words(words: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove duplicate words, keeping the first occurrence."""
    seen: Set[str] = set()
    unique_words = []

    for word in words:
        word_text = word['word'].lower().strip()
        if word_text not in seen:
            seen.add(word_text)
            unique_words.append(word)

    return unique_words


def build_70_day_plan(data: Dict[str, Any], max_new_words_per_day: int = 35) -> List[DayPlan]:
    """
    Build 70-day learning plan.

    Strategy:
    1. Deduplicate words
    2. Calculate coreScore for each word
    3. Sort by coreScore (descending)
    4. Distribute words across 70 days
    5. Assign phrases and sentences to each day
    """
    words = data['words']
    phrases = data['phrases']
    sentences = data['sentences']
    units = data['units']

    # Step 1: Deduplicate words
    unique_words = deduplicate_words(words)
    print(f"Original words: {len(words)}")
    print(f"Unique words: {len(unique_words)}")

    # Step 2: Calculate coreScore for each word
    words_with_scores: List[WordWithScore] = []
    for word in unique_words:
        score = calculate_core_score(word, sentences, phrases)
        priority = assign_priority(score)
        words_with_scores.append(WordWithScore(
            word_id=word['id'],
            word=word['word'],
            translation=word['translation'],
            core_score=score,
            priority=priority,
            source_unit_id=word.get('sourceUnitId', 'vocabulary-handbook')
        ))

    # Step 3: Sort by coreScore (descending)
    words_with_scores.sort(key=lambda x: (-x.core_score, x.word))

    # Print score distribution
    core_count = sum(1 for w in words_with_scores if w.priority == "core")
    important_count = sum(1 for w in words_with_scores if w.priority == "important")
    extension_count = sum(1 for w in words_with_scores if w.priority == "extension")
    print(f"\nWord priority distribution:")
    print(f"  Core: {core_count}")
    print(f"  Important: {important_count}")
    print(f"  Extension: {extension_count}")

    # Step 4: Distribute words across 70 days
    total_words = len(words_with_scores)
    words_per_day = min(max_new_words_per_day, total_words // 70 + 1)

    print(f"\nWords per day target: {words_per_day}")

    # Create 70 day plans
    day_plans: List[DayPlan] = []
    word_index = 0

    # Assign units to days (each unit gets approximately 5-6 days)
    unit_day_ranges = {}
    days_per_unit = 70 // len(units)
    for i, unit in enumerate(units):
        start_day = i * days_per_unit + 1
        end_day = min((i + 1) * days_per_unit, 70)
        unit_day_ranges[unit['id']] = (start_day, end_day)

    # Create day plans
    for day_num in range(1, 71):
        # Determine which unit this day belongs to
        source_unit_id = None
        for unit_id, (start, end) in unit_day_ranges.items():
            if start <= day_num <= end:
                source_unit_id = unit_id
                break

        if not source_unit_id:
            source_unit_id = units[-1]['id']  # Default to last unit

        # Get words for this day
        day_words = []
        words_added = 0

        while word_index < total_words and words_added < words_per_day:
            word = words_with_scores[word_index]
            day_words.append(word.word_id)
            word_index += 1
            words_added += 1

        # Get phrases for this day (distribute evenly)
        day_phrases = []
        phrase_start = ((day_num - 1) * len(phrases)) // 70
        phrase_end = (day_num * len(phrases)) // 70
        day_phrases = [p['id'] for p in phrases[phrase_start:phrase_end]]

        # Get sentences for this day (distribute evenly)
        day_sentences = []
        sentence_start = ((day_num - 1) * len(sentences)) // 70
        sentence_end = (day_num * len(sentences)) // 70
        day_sentences = [s['id'] for s in sentences[sentence_start:sentence_end]]

        # Create day plan
        day_plan = DayPlan(
            day=day_num,
            sourceUnitIds=[source_unit_id],
            title=f"Day {day_num}",
            newWordIds=day_words,
            phraseIds=day_phrases,
            sentenceIds=day_sentences
        )

        day_plans.append(day_plan)

    return day_plans


def save_plan(day_plans: List[DayPlan], base_dir: str):
    """Save the 70-day plan to files."""
    output_dir = os.path.join(base_dir, 'normalized-data', 'plan')
    os.makedirs(output_dir, exist_ok=True)

    # Save manifest
    manifest = {
        "schemaVersion": 1,
        "planDays": 70,
        "maxNewWordsPerDay": 35,
        "days": [{"day": dp.day, "file": f"day-{dp.day:02d}.json"} for dp in day_plans]
    }

    manifest_file = os.path.join(output_dir, 'manifest.json')
    with open(manifest_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"\nSaved manifest to {manifest_file}")

    # Save individual day plans
    for day_plan in day_plans:
        day_file = os.path.join(output_dir, f'day-{day_plan.day:02d}.json')
        with open(day_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(day_plan), f, ensure_ascii=False, indent=2)

    print(f"Saved {len(day_plans)} day plans to {output_dir}")

    # Print summary
    total_words = sum(len(dp.newWordIds) for dp in day_plans)
    total_phrases = sum(len(dp.phraseIds) for dp in day_plans)
    total_sentences = sum(len(dp.sentenceIds) for dp in day_plans)

    print(f"\n--- Plan Summary ---")
    print(f"Total days: {len(day_plans)}")
    print(f"Total words: {total_words}")
    print(f"Total phrases: {total_phrases}")
    print(f"Total sentences: {total_sentences}")
    print(f"Average words per day: {total_words / len(day_plans):.1f}")

    # Print word count distribution
    word_counts = [len(dp.newWordIds) for dp in day_plans]
    print(f"\nWord count distribution:")
    print(f"  Min: {min(word_counts)}")
    print(f"  Max: {max(word_counts)}")
    print(f"  Days with 35 words: {sum(1 for c in word_counts if c == 35)}")
    print(f"  Days with < 35 words: {sum(1 for c in word_counts if c < 35)}")


def main():
    """Main function to build 70-day plan."""
    base_dir = '/Volumes/Lark/Study/模块提取'

    print("Loading normalized data...")
    data = load_normalized_data(base_dir)

    print(f"Loaded {len(data['words'])} words")
    print(f"Loaded {len(data['phrases'])} phrases")
    print(f"Loaded {len(data['sentences'])} sentences")
    print(f"Loaded {len(data['units'])} units")

    print("\nBuilding 70-day plan...")
    day_plans = build_70_day_plan(data)

    print("\nSaving plan...")
    save_plan(day_plans, base_dir)

    # Print sample day plans
    print("\n--- Sample Day Plans ---")
    for day_plan in day_plans[:3]:
        print(f"\nDay {day_plan.day}:")
        print(f"  Unit: {day_plan.sourceUnitIds}")
        print(f"  Words: {len(day_plan.newWordIds)}")
        print(f"  Phrases: {len(day_plan.phraseIds)}")
        print(f"  Sentences: {len(day_plan.sentenceIds)}")


if __name__ == '__main__':
    main()
