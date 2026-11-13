<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{
  isCreateFileModalOpen: boolean;
}>();

const emit = defineEmits<{
  (e: "update:isCreateFileModalOpen", value: boolean): void;
}>();

const isOpen = computed({
  get: () => props.isCreateFileModalOpen,
  set: (value) => emit("update:isCreateFileModalOpen", value),
});
</script>

<template>
  <UModal v-model:open="isOpen">
    <template #header>
      <div
        style="
          display: flex;
          justify-content: space-between;
          align-items: center;
          width: 100%;
        "
      >
        <h3 style="margin: 0; font-size: 18px; font-weight: 600">
          Загрузка файла
        </h3>
      </div>
    </template>

    <template #body>
      <div style="padding: 10px 0">
        <p style="color: #4b5563; margin-bottom: 16px">
          Выберите файл для загрузки в текущее хранилище:
        </p>
        <input
          type="file"
          style="
            width: 100%;
            padding: 8px;
            border: 1px dashed #d1d5db;
            border-radius: 8px;
          "
        />
      </div>

      <div
        style="
          display: flex;
          justify-content: flex-end;
          gap: 10px;
          width: 100%;
          margin-top: 16px;
        "
      >
        <!-- Меняем isOpen, что автоматически вызовет emit наверх в App.vue -->
        <UButton color="primary" @click="isOpen = false"> Загрузить </UButton>
        <UButton
          label="Отмена"
          color="neutral"
          variant="subtle"
          @click="isOpen = false"
        />
      </div>
    </template>
  </UModal>
</template>
