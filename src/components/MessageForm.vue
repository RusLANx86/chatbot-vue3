<template>
  <div class="message-form bg-white rounded-lg shadow-md p-4">
    <form @submit.prevent="sendMessage" class="flex gap-2">
      <input
        v-model="messageText"
        type="text"
        placeholder="Введите сообщение..."
        class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        :disabled="isLoading"
      />
      <button
        type="submit"
        :disabled="!messageText.trim() || isLoading"
        :class="[
          'px-6 py-2 rounded-lg font-medium transition-all duration-200',
          messageText.trim() && !isLoading
            ? 'bg-blue-500 text-white hover:bg-blue-600 shadow-md'
            : 'bg-gray-300 text-gray-500 cursor-not-allowed'
        ]"
      >
        <span v-if="!isLoading">📤</span>
        <span v-else class="animate-spin">⏳</span>
      </button>
    </form>
    
    <!-- Индикатор загрузки -->
    <div v-if="isLoading" class="mt-2 text-sm text-gray-500 flex items-center gap-2">
      <div class="flex space-x-1">
        <div class="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
        <div class="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
        <div class="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
      </div>
      <span>Отправка сообщения...</span>
    </div>

    <!-- Ошибка -->
    <div v-if="error" class="mt-2 text-sm text-red-500">
      Ошибка: {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useChatStore } from '../stores/chat'

const chatStore = useChatStore()
const messageText = ref('')

const isLoading = computed(() => chatStore.isLoading)
const error = computed(() => chatStore.error)

const sendMessage = async () => {
  if (!messageText.value.trim() || isLoading.value) return
  
  await chatStore.sendMessage(messageText.value)
  messageText.value = ''
}
</script> 