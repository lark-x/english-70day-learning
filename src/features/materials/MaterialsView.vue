<script setup lang="ts">
import { ref } from 'vue'

const activeTab = ref('words')

const tabs = [
  { id: 'words', label: '单词' },
  { id: 'phrases', label: '短语' },
  { id: 'sentences', label: '句子' },
  { id: 'units', label: '单元' },
]

// Sample data
const words = ref([
  { id: 'word-0001', word: 'able-bodied', phonetic: '/ˌeɪbl ˈbɒdɪd/', translation: '健康的；健壮的' },
  { id: 'word-0002', word: 'abnormal', phonetic: '/æbˈnɔːrml/', translation: '不正常的；反常的' },
  { id: 'word-0003', word: 'absolute', phonetic: '/ˈæbsəluːt/', translation: '肯定的；无疑的' },
])

const phrases = ref([
  { id: 'phrase-0001', phrase: 'a multitude of', translation: '众多的；大量的' },
  { id: 'phrase-0002', phrase: 'a series of', translation: '一系列；连续' },
])

const sentences = ref([
  {
    id: 'sentence-0001',
    en: 'In either case, you must recognize and take into account any differences.',
    zh: '不论哪种情况，你必须注意并考虑任何差异。'
  }
])

const units = ref([
  { id: 'unit-01', title: 'The Power of Language' },
  { id: 'unit-02', title: 'Mistakes to Success' },
  { id: 'unit-03', title: 'Friendship and Loyalty' },
])
</script>

<template>
  <div class="materials-view">
    <h2>资料库</h2>
    <p class="subtitle">浏览所有学习内容</p>

    <!-- Tabs -->
    <div class="tabs">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        :class="['tab-button', { active: activeTab === tab.id }]"
        @click="activeTab = tab.id"
      >
        {{ tab.label }}
      </button>
    </div>

    <!-- Content -->
    <div class="content">
      <!-- Words -->
      <div v-if="activeTab === 'words'" class="tab-content">
        <div class="word-grid">
          <div v-for="word in words" :key="word.id" class="word-card">
            <div class="word-english">{{ word.word }}</div>
            <div class="word-phonetic">{{ word.phonetic }}</div>
            <div class="word-translation">{{ word.translation }}</div>
          </div>
        </div>
      </div>

      <!-- Phrases -->
      <div v-if="activeTab === 'phrases'" class="tab-content">
        <div class="phrase-list">
          <div v-for="phrase in phrases" :key="phrase.id" class="phrase-card">
            <div class="phrase-english">{{ phrase.phrase }}</div>
            <div class="phrase-translation">{{ phrase.translation }}</div>
          </div>
        </div>
      </div>

      <!-- Sentences -->
      <div v-if="activeTab === 'sentences'" class="tab-content">
        <div class="sentence-list">
          <div v-for="sentence in sentences" :key="sentence.id" class="sentence-card">
            <div class="sentence-en">{{ sentence.en }}</div>
            <div class="sentence-zh">{{ sentence.zh }}</div>
          </div>
        </div>
      </div>

      <!-- Units -->
      <div v-if="activeTab === 'units'" class="tab-content">
        <div class="unit-list">
          <div v-for="unit in units" :key="unit.id" class="unit-card">
            <div class="unit-id">{{ unit.id }}</div>
            <div class="unit-title">{{ unit.title }}</div>
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
</style>
