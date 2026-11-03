<script setup lang="ts">
import {ref, onMounted, type Ref} from 'vue'
import axios from "axios"

interface FolderItem {
  id: string
  name: string
}

interface FileItem {
  id: string
  name: string
}

const folders = ref<FolderItem[]>([])
const selectedFolder = ref<FolderItem | null>(null)
const files = ref<FileItem[]>([])

const fetchFolders = async () => {
  const res = await axios.get('http://localhost:8000/api/folders')
  folders.value = res.data.folders
}

onMounted(async () => {
  fetchFolders()
})

const selectFolder = async (folder: FolderItem) => {
  selectedFolder.value = folder
  const res = await axios.get(`http://localhost:8000/api/files/${folder.name}`)
  files.value = res.data.files
}

const deleteFile = async (selectedFolderName: string, fileId: string, fileName: string) => {
  if (!confirm(`Точно удалить файл ${fileName}?`)) return

  try {
    await axios.delete(`http://localhost:8000/api/files/${selectedFolderName}/${fileId}`)
    
    // Убираем файл из локального списка по его id
    files.value = files.value.filter(f => f.id !== fileId)
  } catch (error) {
    console.error("Ошибка при удалении:", error)
    alert("Не удалось удалить файл")
  }
}

// Удаление папки (рекурсивно стирает всё внутри)
const deleteFolder = async (folderId: string, folderName: string) => {
  if (!confirm(`ВНИМАНИЕ! Папка "${folderName}" и все файлы внутри неё будут удалены. Продолжить?`)) return

  try {
    await axios.delete(`http://localhost:8000/api/folders/${folderId}`)
    
    // Если удалили ту папку, которая сейчас открыта — сбрасываем просмотр
    if (selectedFolder.value?.id === folderId) {
      selectedFolder.value = null
      files.value = []
    }
    
    // Обновляем список папок
    await fetchFolders()
  } catch (error) {
    console.error("Ошибка при удалении папки:", error)
    alert("Не удалось удалить папку")
  }
}

// TODO: добавть возможность загрузить файлы через форму папок

</script>

<template>
    <div>
    <h2>Выбери папку:</h2>
    <ul v-if="folders.length > 0">
      <li v-for="folder in folders" :key="folder.id" @click="selectFolder(folder)">
        <span @click="selectFolder(folder)" style="cursor: pointer;">
          📁 {{ folder.name }}
        </span>
        <button @click.stop="deleteFolder(folder.id, folder.name)" class="delete-folder-btn" style="margin-left: 10px; color: red;">
          Удалить папку
        </button>
      </li>
    </ul>

    <p v-else class="empty-text">Папок нет</p>

    <div v-if="selectedFolder">
      <h3>Файлы в папке: {{ selectedFolder.name }}</h3>
      <ul v-if="files.length > 0">
          <li v-for="file in files" :key="file.id" class="list-item">
            📄 {{ file.name }} 
            <button @click="deleteFile(selectedFolder.name, file.id, file.name)" class="delete-button">Удалить</button>
          </li>
      </ul>
      
      <p v-else class="empty-text">📭 В этой папке пока пусто или файлы не найдены</p>
    </div>
  </div>
</template>

<style scoped>

.list-item {
  display: flex;
  gap: 12px;
  align-items: center;
}

.delete-button {
  background-color: brown;
  border: 1px;
  border-radius: 2px;
}

</style>