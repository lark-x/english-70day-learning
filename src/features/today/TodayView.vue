<script setup lang="ts">
import { ref, onMounted } from 'vue'

const currentDay = ref(1)
const isLoading = ref(true)

// Sample data - in real app, this would come from the plan
const todayWords = ref([
  { id: 'word-0001', word: 'able-bodied', translation: '健康的；健壮的' },
  { id: 'word-0002', word: 'abnormal', translation: '不正常的；反常的' },
  { id: 'word-0003', word: 'absolute', translation: '肯定的；无疑的' },
])

const todayPhrases = ref([
  { id: 'phrase-0001', phrase: 'a multitude of', translation: '众多的；大量的' },
  { id: 'phrase-0002', phrase: 'a series of', translation: '一系列；连续' },
])

const todaySentences = ref([
  {
    id: 'sentence-0001',
    en: 'In either case, you must recognize and take into account any differences.',
    zh: '不论哪种情况，你必须注意并考虑任何差异。'
  }
])

onMounted(() => {
  // Load current day from storage
  const savedDay = localStorage.getItem('currentDay')
  if (savedDay) {
    currentDay.value = parseInt(savedDay)
  }
  isLoading.value = false
})

const completeDay = () => {
  // Save progress
  localStorage.setItem('currentDay', String(currentDay.value + 1))
  currentDay.value++
  alert(`Day ${currentDay.value - 1} 完成！明天继续 Day ${currentDay.value}`)
}
</script>

<template>
  <div class="today-view">
    <div class="day-header">
      <h2>Day {{ currentDay }} / 70</h2>
      <p class="subtitle">今日学习内容</p>
    </div>

    <div v-if="isLoading" class="loading">加载中...</div>

    <div v-else class="content-sections">
      <!-- Words Section -->
      <section class="content-section">
        <h3>📚 新单词 ({{ todayWords.length }})</h3>
        <div class="word-list">
          <div v-for="word in todayWords" :key="word.id" class="word-card">
            <div class="word-english">{{ word.word }}</div>
            <div class="word-translation">{{ word.translation }}</div>
          </div>
        </div>
      </section>

      <!-- Phrases Section -->
      <section class="content-section">
        <h3>📝 新短语 ({{ todayPhrases.length }})</h3>
        <div class="phrase-list">
          <div v-for="phrase in todayPhrases" :key="phrase.id" class="phrase-card">
            <div class="phrase-english">{{ phrase.phrase }}</div>
            <div class="phrase-translation">{{ phrase.translation }}</div>
          </div>
        </div>
      </section>

      <!-- Sentences Section -->
      <section class="content-section">
        <h3>📖 核心句型 ({{ todaySentences.length }})</h3>
        <div class="sentence-list">
          <div v-for="sentence in todaySentences" :key="sentence.id" class="sentence-card">
            <div class="sentence-en">{{ sentence.en }}</div>
            <div class="sentence-zh">{{ sentence.zh }}</div>
          </div>
        </div>
      </section>

      <!-- Complete Button -->
      <div class="complete-section">
        <button @click="completeDay" class="complete-button">
          完成今日学习
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.today-view {
  max-width: 800px;
  margin: 0 auto;
}

.day-header {
  text-align: center;
  margin-bottom: 30px;
}

.day-header h2 {
  font-size: 2rem;
  color: #333;
  margin-bottom: 5px;
}

.subtitle {
  color: #666;
  font-size: 1.1rem;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #666;
}

.content-sections {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.content-section {
  background: #f8f9fa;
  padding: 25px;
  border-radius: 12px;
}

.content-section h3 {
  margin: 0 0 20px 0;
  color: #333;
  font-size: 1.3rem;
}

.word-list, .phrase-list, .sentence-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.word-card, .phrase-card, .sentence-card {
  background: white;
  padding: 15px;
  border-radius: 8px;
  border-left: 4px solid #4CAF50;
}

.word-english, .phrase-english {
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 5px;
}

.word-translation, .phrase-translation {
  color: #666;
  font-size: 0.95rem;
}

.sentence-en {
  font-size: 1.1rem;
  color: #333;
  margin-bottom: 8px;
  line-height: 1.5;
}

.sentence-zh {
  color: #666;
  font-size: 0.95rem;
  line-height: 1.5;
}

.complete-section {
  text-align: center;
  margin-top: 20px;
}

.complete-button {
  background: #4CAF50;
  color: white;
  border: none;
  padding: 15px 40px;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s, transform 0.2s;
}

.complete-button:hover {
  background: #45a049;
  transform: translateY(-2px);
}
</style>
