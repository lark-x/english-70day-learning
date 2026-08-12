<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
  <div class="app">
    <header class="app-header">
      <h1>英语 70 天学习系统</h1>
      <nav>
        <router-link to="/">首页</router-link>
        <router-link to="/today">今日学习</router-link>
        <router-link to="/materials">资料库</router-link>
        <router-link to="/mistakes">错题本</router-link>
      </nav>
    </header>
    <main class="app-main">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.app {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.app-header h1 {
  margin: 0;
  font-size: 1.5rem;
  color: #333;
}

.app-header nav {
  display: flex;
  gap: 20px;
}

.app-header nav a {
  text-decoration: none;
  color: #666;
  font-weight: 500;
}

.app-header nav a.router-link-active {
  color: #4CAF50;
}

.app-main {
  min-height: calc(100vh - 200px);
}
</style>
