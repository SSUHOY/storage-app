<template>
  <div class="empty-home">
    <h2>Добро пожаловать в Cloudly!</h2>
    <p>Выберите папку в сайдбаре слева или загрузите первый файл.</p>
  </div>
</template>

<style scoped>
.empty-home {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 60vh;
  color: #6b7280;
  text-align: center;
}

.empty-home h2 {
  color: #374151;
  margin-bottom: 8px;
}
</style>