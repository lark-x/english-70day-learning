<script setup lang="ts">
import { ref, computed } from 'vue'
import contentData from '../../data/content.json'

const activeTab = ref('words')
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = 20

const tabs = [
  { id: 'words', label: `单词 (${contentData.words.length})` },
  { id: 'phrases', label: `短语 (${contentData.phrases.length})` },
  { id: 'units', label: `单元 (${contentData.units.length})` },
]

const words = contentData.words
const phrases = contentData.phrases
const units = contentData.units

const filteredWords = computed(() => {
  const q = searchQuery.value.toLowerCase()
  if (!q) return words
  return words.filter(w => w.word.toLowerCase().includes(q) || (w.translation && w.translation.includes(q)))
})

const filteredPhrases = computed(() => {
  const q = searchQuery.value.toLowerCase()
  if (!q) return phrases
  return phrases.filter(p => p.phrase.toLowerCase().includes(q) || (p.translation && p.translation.includes(q)))
})

const paginatedWords = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredWords.value.slice(start, start + pageSize)
})

const totalWordPages = computed(() => Math.ceil(filteredWords.value.length / pageSize))

const paginatedPhrases = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredPhrases.value.slice(start, start + pageSize)
})

const totalPhrasePages = computed(() => Math.ceil(filteredPhrases.value.length / pageSize))

function resetPage() { currentPage.value = 1 }
</script>

<template>
  <div class="materials-view">
    <h2>资料库</h2>
    <p class="subtitle">浏览全部学习内容</p>

    <!-- Tabs -->
    <div class="tabs">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        :class="['tab-button', { active: activeTab === tab.id }]"
        @click="activeTab = tab.id; resetPage()"
      >
        {{ tab.label }}
      </button>
    </div>

    <!-- Search -->
    <div class="search-bar">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="搜索单词或短语..."
        @input="resetPage"
      />
    </div>

    <!-- Content -->
    <div class="content">
      <!-- Words -->
      <div v-if="activeTab === 'words'" class="tab-content">
        <p class="result-count">共 {{ filteredWords.length }} 个单词</p>
        <div class="word-grid">
          <div v-for="word in paginatedWords" :key="word.word" class="word-card">
            <div class="word-english">{{ word.word }}</div>
            <div class="word-phonetic">{{ word.phonetic }}</div>
            <div class="word-translation">{{ word.translation }}</div>
            <div v-if="word.partOfSpeech" class="word-pos">{{ word.partOfSpeech }}</div>
          </div>
        </div>
        <div v-if="totalWordPages > 1" class="pagination">
          <button :disabled="currentPage <= 1" @click="currentPage--">上一页</button>
          <span>{{ currentPage }} / {{ totalWordPages }}</span>
          <button :disabled="currentPage >= totalWordPages" @click="currentPage++">下一页</button>
        </div>
      </div>

      <!-- Phrases -->
      <div v-if="activeTab === 'phrases'" class="tab-content">
        <p class="result-count">共 {{ filteredPhrases.length }} 个短语</p>
        <div class="phrase-list">
          <div v-for="phrase in paginatedPhrases" :key="phrase.phrase" class="phrase-card">
            <div class="phrase-english">{{ phrase.phrase }}</div>
            <div class="phrase-translation">{{ phrase.translation }}</div>
          </div>
        </div>
        <div v-if="totalPhrasePages > 1" class="pagination">
          <button :disabled="currentPage <= 1" @click="currentPage--">上一页</button>
          <span>{{ currentPage }} / {{ totalPhrasePages }}</span>
          <button :disabled="currentPage >= totalPhrasePages" @click="currentPage++">下一页</button>
        </div>
      </div>

      <!-- Units -->
      <div v-if="activeTab === 'units'" class="tab-content">
        <div class="unit-list">
          <div v-for="unit in units" :key="unit.id" class="unit-card">
            <div class="unit-id">Unit {{ unit.unitNum }}</div>
            <div class="unit-title">{{ unit.title }}</div>
            <div v-if="unit.sentences && unit.sentences.length" class="unit-meta">
              {{ unit.sentences.length }} 个核心句型
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.materials-view {
  max-width: 1000px;
  margin: 0 auto;
}

h2 {
  font-size: 2rem;
  color: #333;
  margin-bottom: 5px;
}

.subtitle {
  color: #666;
  font-size: 1.1rem;
  margin-bottom: 30px;
}

.tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
  border-bottom: 2px solid #eee;
  padding-bottom: 10px;
}

.tab-button {
  padding: 10px 20px;
  border: none;
  background: none;
  font-size: 1rem;
  color: #666;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  margin-bottom: -12px;
  transition: color 0.2s, border-color 0.2s;
}

.tab-button:hover {
  color: #333;
}

.tab-button.active {
  color: #4CAF50;
  border-bottom-color: #4CAF50;
}

.content {
  min-height: 400px;
}

.word-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.word-card, .phrase-card, .sentence-card, .unit-card {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  border-left: 4px solid #4CAF50;
}

.word-english {
  font-size: 1.3rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 5px;
}

.word-phonetic {
  color: #888;
  font-size: 0.9rem;
  margin-bottom: 8px;
}

.word-translation, .phrase-translation {
  color: #666;
}

.phrase-english {
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 5px;
}

.sentence-en {
  font-size: 1.1rem;
  color: #333;
  margin-bottom: 8px;
  line-height: 1.5;
}

.sentence-zh {
  color: #666;
  line-height: 1.5;
}

.unit-id {
  font-size: 0.9rem;
  color: #888;
  margin-bottom: 5px;
}

.unit-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
}

.phrase-list, .sentence-list, .unit-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.search-bar {
  margin-bottom: 20px;
}

.search-bar input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.2s;
}

.search-bar input:focus {
  border-color: #4CAF50;
}

.result-count {
  color: #888;
  font-size: 0.9rem;
  margin-bottom: 15px;
}

.word-pos {
  display: inline-block;
  background: #e8f5e9;
  color: #4CAF50;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  margin-top: 5px;
}

.unit-meta {
  color: #888;
  font-size: 0.85rem;
  margin-top: 5px;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 30px;
  padding: 15px 0;
}

.pagination button {
  padding: 8px 20px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.95rem;
}

.pagination button:hover:not(:disabled) {
  background: #4CAF50;
  color: white;
  border-color: #4CAF50;
}

.pagination button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
</style>
