<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface Mistake {
  id: string
  question: string
  userAnswer: string
  correctAnswer: string
  wrongCount: number
  status: 'unresolved' | 'reviewing' | 'resolved'
  date: string
}

const mistakes = ref<Mistake[]>([])

onMounted(() => {
  try {
    const saved = localStorage.getItem('mistakes')
    if (saved) {
      mistakes.value = JSON.parse(saved)
    }
  } catch (e) { /* ignore */ }
})

const getStatusColor = (status: string) => {
  switch (status) {
    case 'unresolved': return '#f44336'
    case 'reviewing': return '#ff9800'
    case 'resolved': return '#4CAF50'
    default: return '#666'
  }
}

const getStatusText = (status: string) => {
  switch (status) {
    case 'unresolved': return '未解决'
    case 'reviewing': return '复习中'
    case 'resolved': return '已解决'
    default: return '未知'
  }
}
</script>

<template>
  <div class="mistakes-view">
    <h2>错题本</h2>
    <p class="subtitle">共 {{ mistakes.length }} 道错题</p>

    <div class="mistakes-list">
      <div v-for="mistake in mistakes" :key="mistake.id" class="mistake-card">
        <div class="mistake-header">
          <span class="mistake-date">{{ mistake.date }}</span>
          <span
            class="mistake-status"
            :style="{ color: getStatusColor(mistake.status) }"
          >
            {{ getStatusText(mistake.status) }}
          </span>
        </div>

        <div class="mistake-question">{{ mistake.question }}</div>

        <div class="mistake-answers">
          <div class="answer-row">
            <span class="answer-label">你的答案：</span>
            <span class="answer-wrong">{{ mistake.userAnswer }}</span>
          </div>
          <div class="answer-row">
            <span class="answer-label">正确答案：</span>
            <span class="answer-correct">{{ mistake.correctAnswer }}</span>
          </div>
        </div>

        <div class="mistake-meta">
          <span>错误次数：{{ mistake.wrongCount }}</span>
        </div>
      </div>
    </div>

    <div v-if="mistakes.length === 0" class="empty-state">
      <p>🎉 太棒了！没有错题！</p>
    </div>
  </div>
</template>

<style scoped>
.mistakes-view {
  max-width: 800px;
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

.mistakes-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.mistake-card {
  background: #f8f9fa;
  padding: 25px;
  border-radius: 12px;
  border-left: 4px solid #f44336;
}

.mistake-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.mistake-date {
  font-size: 0.9rem;
  color: #888;
}

.mistake-status {
  font-weight: 600;
  font-size: 0.9rem;
}

.mistake-question {
  font-size: 1.1rem;
  color: #333;
  margin-bottom: 15px;
  line-height: 1.5;
}

.mistake-answers {
  background: white;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 15px;
}

.answer-row {
  display: flex;
  gap: 10px;
  margin-bottom: 8px;
}

.answer-row:last-child {
  margin-bottom: 0;
}

.answer-label {
  color: #666;
  min-width: 80px;
}

.answer-wrong {
  color: #f44336;
  font-weight: 500;
}

.answer-correct {
  color: #4CAF50;
  font-weight: 500;
}

.mistake-meta {
  color: #888;
  font-size: 0.9rem;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #666;
  font-size: 1.2rem;
}
</style>
