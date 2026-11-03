<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

// Состояние
const selectedFolder = ref('photos') // Категория по умолчанию
const customFolder = ref('')       // Если захочешь ввести имя папки руками
const fileToUpload = ref<File | null>(null)
const statusMessage = ref('')
const isLoading = ref(false)

// Ловим выбранный файл из инпута
const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    fileToUpload.value = target.files[0] ?? null
  }
}

const uploadFile = async () => {
  if (!fileToUpload.value) {
    statusMessage.value = 'Сначала выбери файл!'
    return
  }

  const folderName = customFolder.value.trim() || selectedFolder.value

  const formData = new FormData()
  formData.append('folder', folderName)
  formData.append('file', fileToUpload.value)

  try {
    isLoading.value = true
    statusMessage.value = 'Загрузка...'

    // Шлем POST-запрос на FastAPI
    const response = await axios.post('http://localhost:8000/api/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    statusMessage.value = response.data.message
    fileToUpload.value = null
  } catch (error) {
    statusMessage.value = 'Ошибка: ' + error
  }
}
</script>

<template>
  <div class="upload-container">
    <h3>Загрузка файлов на сервер</h3>

    <div class="input-group">
      <label>Папка назначения:</label>
      <select v-model="selectedFolder">
        <option value="photos">photos (Фото)</option>
        <option value="ableton">ableton (Проекты)</option>
      </select>
      
      <input 
        type="text" 
        v-model="customFolder" 
        placeholder="Или введи имя новой папки" 
      />
    </div>

    <div class="input-group">
      <input type="file" @change="handleFileChange" />
    </div>

    <button @click="uploadFile" :disabled="isLoading">
      {{ isLoading ? 'Заливаем...' : 'Загрузить файл' }}
    </button>

    <p v-if="statusMessage" class="status">{{ statusMessage }}</p>
  </div>
</template>

<style scoped>
.upload-container {
  padding: 20px;
  border-radius: 8px;
  max-width: 400px;
}
.input-group {
  margin-bottom: 15px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.status {
  color: red;
}

</style>