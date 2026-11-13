<script setup lang="ts">
import { defineProps, defineEmits } from "vue";

interface FolderItem {
  id: string;
  name: string;
  count?: number;
}

defineProps<{
  folders: FolderItem[];
  selectedFolderId?: string | null;
}>();

const emit = defineEmits<{
  (e: "select-all"): void;
  (e: "select-recent"): void;
  (e: "select-folder", folder: FolderItem): void;
  (e: "create-folder"): void;
  (e: "upload-click"): void;
  (e: "delete-click", folderId: string): void;
}>();
</script>

<template>
  <aside class="sidebar">
    <!-- Лого -->
    <div class="logo-area">
      <div class="logo-icon">☁️</div>
      <span class="logo-text">StorageMe</span>
    </div>

    <!-- Кнопка Добавить -->
    <div class="action-dropdown">
      <button class="add-btn" @click="emit('upload-click')">
        <span>+ Добавить</span>
        <span class="arrow">▼</span>
      </button>
    </div>

    <!-- Навигация по хранилищу -->
    <div class="nav-section">
      <span class="section-title">ХРАНИЛИЩЕ</span>
      <ul>
        <li class="nav-item" @click="emit('select-all')">📁 Все файлы</li>
        <li class="nav-item" @click="emit('select-recent')">🕒 Недавние</li>
      </ul>
    </div>

    <!-- Список папок с кнопкой добавления новой -->
    <div class="nav-section">
      <div class="folders-header">
        <span class="section-title">ПАПКИ</span>
        <button
          class="add-folder-btn"
          @click="emit('create-folder')"
          title="Создать папку"
        >
          +
        </button>
      </div>

      <ul class="folders-list">
        <li
          v-for="folder in folders"
          :key="folder.id"
          class="folder-item"
          @click="emit('select-folder', folder)"
        >
          <span class="folder-name">📁 {{ folder.name }}</span>
          <span v-if="folder.count !== undefined" class="folder-count">{{
            folder.count
          }}</span>

          <!-- TODO: разобраться, почему не рабоает удаление -->

          <button
            class="delete-folder-btn"
            title="Удалить папку"
            @click.stop="emit('delete-click', folder.id)"
          >
            🗑
          </button>
        </li>
      </ul>
    </div>
  </aside>
</template>

<style src="./sideBar.css" scoped></style>
