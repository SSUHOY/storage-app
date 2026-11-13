<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import SideBar from "./components/sidebar/SideBar.vue";
import axios from "axios";
import AddFileModal from "./components/modal/AddFileModal.vue";

interface FolderItem {
  id: string;
  name: string;
}

const router = useRouter();
const folders = ref<FolderItem[]>([]);

const isCreateFileModalOpen = ref(false);

const fetchFolders = async () => {
  try {
    const res = await axios.get("http://localhost:8000/api/folders");
    folders.value = res.data.folders;
  } catch (e) {
    console.error("Не удалось загрузить папки", e);
  }
};

onMounted(() => {
  fetchFolders();
});

// Обработчики кликов из сайдбара
const handleSelectAll = () => {
  router.push("/"); // Переходим на главную
};

const handleSelectRecent = () => {
  // router.push('/recent') — пока заглушка на будущее
  console.log("Клик на Недавние");
};

const handleSelectFolder = (folder: FolderItem) => {
  // В будущем будем роутить на страницу папки, например router.push(`/folder/${folder.name}`)
  console.log("выбрана папка:", folder.name);
};

const handleCreateFolder = async () => {
  try {
    const res = await axios.post("http://localhost:8000/api/folders", {
      name: "Новая папка",
    });

    folders.value.push(res.data.folder);

    console.log("test create log", res.data.folder.name);
  } catch (e) {
    console.error("Не удалось создать папку", e);
    console.error("Ошибка при создании папки:", e);
    alert("Не удалось создать папку");
  }
};

const handleDeleteFolder = async (folderId: string) => {
  
  if (!confirm("Вы уверены, что хотите удалить эту папку со всеми файлами?"))
    return;
  
    try {
    await axios.delete(`http://localhost:8000/api/folders/${folderId}`);
    await fetchFolders();
  } catch (error) {
    console.error("Ошибка при удалении папки:", error);
    alert("Не удалось удалить папку");
  }
};

const handleUploadClick = () => {
  console.log("Клик по кнопке + открывает модалку");
  isCreateFileModalOpen.value = true;
};
</script>

<template>
  <div class="app-layout">
    <SideBar
      :folders="folders"
      @select-all="handleSelectAll"
      @select-recent="handleSelectRecent"
      @select-folder="handleSelectFolder"
      @create-folder="handleCreateFolder"
      @upload-click="handleUploadClick"
      @delete-folder="handleDeleteFolder"
    />

    <!-- Основная рабочая область справа -->
    <main class="main-content">
      <!-- Верхняя шапка поиска (можно тоже вынести в компонент Header.vue позже) -->
      <header class="top-header">
        <div class="search-box">
          <span class="search-icon">🔍</span>
          <input type="text" placeholder="Поиск файлов и папок" disabled />
        </div>
      </header>

      <AddFileModal v-model:isCreateFileModalOpen="isCreateFileModalOpen" />

      <div class="page-container">
        <router-view />
      </div>
    </main>
  </div>
</template>

<style scoped src="./assets/main.css"></style>
