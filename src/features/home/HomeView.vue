<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import contentData from '../../data/content.json'

const currentDay = ref(1)
const totalDays = 70

const progress = computed(() => (currentDay.value / totalDays) * 100)

onMounted(() => {
  const savedDay = localStorage.getItem('currentDay')
  if (savedDay) {
    currentDay.value = Math.min(parseInt(savedDay), totalDays)
  }
})
</script>

<template>
  <div class="home-view">
    <div class="welcome-section">
      <h2>欢迎回来！</h2>
      <p>继续你的英语学习之旅</p>
    </div>

    <div class="progress-section">
      <div class="progress-card">
        <h3>学习进度</h3>
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: progress + '%' }"></div>
        </div>
        <p class="progress-text">Day {{ currentDay }} / {{ totalDays }}</p>
      </div>
    </div>

    <div class="action-section">
      <router-link to="/today" class="action-button primary">
        开始今日学习
      </router-link>
      <router-link to="/materials" class="action-button secondary">
        浏览资料库
      </router-link>
    </div>

    <div class="stats-section">
      <div class="stat-card">
        <div class="stat-number">{{ contentData.words.length }}</div>
        <div class="stat-label">总单词</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">{{ contentData.phrases.length }}</div>
        <div class="stat-label">总短语</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">{{ contentData.units.length }}</div>
        <div class="stat-label">学习单元</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-view {
  max-width: 800px;
  margin: 0 auto;
}

.welcome-section {
  text-align: center;
  margin-bottom: 40px;
}

.welcome-section h2 {
  font-size: 2rem;
  color: #333;
  margin-bottom: 10px;
}

.welcome-section p {
  color: #666;
  font-size: 1.1rem;
}

.progress-section {
  margin-bottom: 40px;
}

.progress-card {
  background: #f8f9fa;
  padding: 30px;
  border-radius: 12px;
  text-align: center;
}

.progress-card h3 {
  margin: 0 0 20px 0;
  color: #333;
}

.progress-bar {
  height: 20px;
  background: #e0e0e0;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 15px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #4CAF50, #8BC34A);
  transition: width 0.3s ease;
}

.progress-text {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
}

.action-section {
  display: flex;
  gap: 20px;
  justify-content: center;
  margin-bottom: 40px;
}

.action-button {
  display: inline-block;
  padding: 15px 30px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  font-size: 1.1rem;
  transition: transform 0.2s, box-shadow 0.2s;
}

.action-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.action-button.primary {
  background: #4CAF50;
  color: white;
}

.action-button.secondary {
  background: #2196F3;
  color: white;
}

.stats-section {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.stat-card {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: #4CAF50;
  margin-bottom: 5px;
}

.stat-label {
  color: #666;
  font-size: 0.9rem;
}
</style>
