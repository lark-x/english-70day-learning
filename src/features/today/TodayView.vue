<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import contentData from '../../data/content.json'

const currentDay = ref(1)
const isLoading = ref(true)

const totalDays = 70
const wordsPerDay = Math.ceil(contentData.words.length / totalDays)
const phrasesPerDay = Math.ceil(contentData.phrases.length / totalDays)

const todayWords = computed(() => {
  const start = (currentDay.value - 1) * wordsPerDay
  return contentData.words.slice(start, start + wordsPerDay)
})

const todayPhrases = computed(() => {
  const start = (currentDay.value - 1) * phrasesPerDay
  return contentData.phrases.slice(start, start + phrasesPerDay)
})

// Rotate units: each day focuses on one unit's sentences
const currentUnit = computed(() => {
  const unitIndex = (currentDay.value - 1) % contentData.units.length
  return contentData.units[unitIndex]
})

onMounted(() => {
  const savedDay = localStorage.getItem('currentDay')
  if (savedDay) {
    currentDay.value = Math.min(parseInt(savedDay), totalDays)
  }
  isLoading.value = false
})

const completeDay = () => {
  localStorage.setItem('currentDay', String(currentDay.value + 1))
  currentDay.value++
  alert(`Day ${currentDay.value - 1} 完成！明天继续 Day ${currentDay.value}`)
}
</script>

<template>
  <div class="today-view">
    <div class="day-header">
      <h2>Day {{ currentDay }} / {{ totalDays }}</h2>
      <p class="subtitle">今日学习内容</p>
    </div>

    <div v-if="isLoading" class="loading">加载中...</div>

    <div v-else class="content-sections">
      <!-- Words Section -->
      <section class="content-section">
        <h3>📚 今日单词 ({{ todayWords.length }})</h3>
        <div class="word-list">
          <div v-for="word in todayWords" :key="word.word" class="word-card">
            <div class="word-english">{{ word.word }}</div>
            <span v-if="word.phonetic" class="word-phonetic">{{ word.phonetic }}</span>
            <div class="word-translation">{{ word.translation }}</div>
          </div>
        </div>
      </section>

      <!-- Phrases Section -->
      <section class="content-section">
        <h3>📝 今日短语 ({{ todayPhrases.length }})</h3>
        <div class="phrase-list">
          <div v-for="phrase in todayPhrases" :key="phrase.phrase" class="phrase-card">
            <div class="phrase-english">{{ phrase.phrase }}</div>
            <div class="phrase-translation">{{ phrase.translation }}</div>
          </div>
        </div>
      </section>

      <!-- Unit Sentences Section -->
      <section class="content-section">
        <h3>📖 Unit {{ currentUnit.unitNum }} - {{ currentUnit.title }}</h3>
        <div class="sentence-list">
          <div v-for="(sentence, idx) in (currentUnit.sentences || []).slice(0, 5)" :key="idx" class="sentence-card">
            <div class="sentence-en">{{ sentence.en }}</div>
            <div class="sentence-zh">{{ sentence.zh }}</div>
          </div>
          <p v-if="!currentUnit.sentences || currentUnit.sentences.length === 0" class="no-data">
            暂无核心句型
          </p>
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

.word-phonetic {
  color: #888;
  font-size: 0.85rem;
  margin-bottom: 4px;
}

.no-data {
  color: #999;
  text-align: center;
  padding: 20px;
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
