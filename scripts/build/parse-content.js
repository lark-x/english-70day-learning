import { readFileSync, writeFileSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '../..');

function parseVocabFile() {
  const content = readFileSync(join(ROOT, '英语二_学习单词手册.md'), 'utf-8');
  const words = [];
  const phrases = [];

  let currentSection = 'words';
  let currentLetter = '';

  const lines = content.split('\n');
  let i = 0;

  while (i < lines.length) {
    const line = lines[i].trim();

    if (line === '# 第二部分：短语/词组') {
      currentSection = 'phrases';
      i++;
      continue;
    }

    if (/^## [A-Z]$/.test(line)) {
      currentLetter = line.replace('## ', '');
      i++;
      continue;
    }

    if (line.startsWith('### ') && currentSection === 'words') {
      const word = {};
      word.word = line.replace('### ', '').trim();
      word.letter = currentLetter;
      i++;

      while (i < lines.length) {
        const l = lines[i].trim();
        if (l.startsWith('### ') || l.startsWith('## ') || l.startsWith('# ') || l === '---') {
          break;
        }
        if (l.startsWith('- **音标**:')) {
          word.phonetic = l.replace('- **音标**:', '').trim();
        } else if (l.startsWith('- **词性**:')) {
          word.partOfSpeech = l.replace('- **词性**:', '').trim();
        } else if (l.startsWith('- **释义**:')) {
          word.translation = l.replace('- **释义**:', '').trim();
        } else if (l.startsWith('- **例句**:')) {
          word.example = l.replace('- **例句**:', '').trim();
        } else if (l.startsWith('- **翻译**:')) {
          word.exampleTranslation = l.replace('- **翻译**:', '').trim();
        }
        i++;
      }

      if (word.word && word.translation) {
        words.push(word);
      }
      continue;
    }

    if (line.startsWith('### ') && currentSection === 'phrases') {
      const phrase = {};
      phrase.phrase = line.replace('### ', '').trim();
      phrase.letter = currentLetter;
      i++;

      while (i < lines.length) {
        const l = lines[i].trim();
        if (l.startsWith('### ') || l.startsWith('## ') || l.startsWith('# ') || l === '---') {
          break;
        }
        if (l.startsWith('- **释义**:')) {
          phrase.translation = l.replace('- **释义**:', '').trim();
        } else if (l.startsWith('- **例句**:')) {
          phrase.example = l.replace('- **例句**:', '').trim();
        } else if (l.startsWith('- **翻译**:')) {
          phrase.exampleTranslation = l.replace('- **翻译**:', '').trim();
        }
        i++;
      }

      if (phrase.phrase && phrase.translation) {
        phrases.push(phrase);
      }
      continue;
    }

    i++;
  }

  return { words, phrases };
}

function parseUnitFiles() {
  const units = [];
  for (let n = 1; n <= 11; n++) {
    const unitNum = String(n).padStart(2, '0');
    const unitDir = join(ROOT, `Unit_${unitNum}`);
    const unit = { id: n, unitNum, sentences: [] };

    try {
      const notesFile = join(unitDir, `Unit_${unitNum}_notes.md`);
      const notes = readFileSync(notesFile, 'utf-8');
      const titleMatch = notes.match(/\*\*单元\*\*: Unit \d+ - (.+)/);
      if (titleMatch) unit.title = titleMatch[1];

      // Notes content
      const headerEnd = notes.indexOf('---');
      if (headerEnd !== -1) {
        unit.notes = notes.substring(headerEnd + 3).trim();
      }
    } catch (e) { /* file may not exist */ unit.title = `Unit ${n}`; }

    try {
      const sentencesContent = readFileSync(join(unitDir, `Unit_${unitNum}_key_sentences.md`), 'utf-8');
      const sentenceLines = sentencesContent.split('\n');
      let currentEn = '';
      let currentZh = '';
      let collectingEn = true;

      for (const line of sentenceLines) {
        const trimmed = line.trim();
        if (/^\d+\./.test(trimmed)) {
          if (currentEn) {
            unit.sentences.push({ en: currentEn.trim(), zh: currentZh.trim() });
          }
          currentEn = trimmed.replace(/^\d+\.\s*/, '');
          currentZh = '';
          collectingEn = true;
        } else if (trimmed && collectingEn && !/[\u4e00-\u9fff]/.test(trimmed.charAt(0))) {
          currentEn += ' ' + trimmed;
        } else if (trimmed && /[\u4e00-\u9fff]/.test(trimmed.charAt(0))) {
          collectingEn = false;
          currentZh += trimmed;
        }
      }
      if (currentEn) {
        unit.sentences.push({ en: currentEn.trim(), zh: currentZh.trim() });
      }
    } catch (e) { /* file may not exist */ }

    try {
      const dialogueContent = readFileSync(join(unitDir, `Unit_${unitNum}_simple_dialogue.md`), 'utf-8');
      const hdr = dialogueContent.indexOf('---');
      if (hdr !== -1) unit.dialogue = dialogueContent.substring(hdr + 3).trim();
    } catch (e) { /* file may not exist */ }

    units.push(unit);
  }
  return units;
}

console.log('Parsing vocabulary...');
const { words, phrases } = parseVocabFile();
console.log(`  Found ${words.length} words, ${phrases.length} phrases`);

console.log('Parsing units...');
const units = parseUnitFiles();
console.log(`  Found ${units.length} units`);

const data = { words, phrases, units };
const outDir = join(ROOT, 'src', 'data');
mkdirSync(outDir, { recursive: true });
const outFile = join(outDir, 'content.json');
writeFileSync(outFile, JSON.stringify(data, null, 2), 'utf-8');
console.log(`Data written to ${outFile}`);
