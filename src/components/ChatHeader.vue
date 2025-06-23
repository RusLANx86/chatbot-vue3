<template>
  <div class="chat-header bg-white rounded-lg shadow-md p-4 mb-4">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="text-2xl">💬</div>
        <div>
          <h1 class="text-xl font-bold text-gray-800">Vue 3 Chat</h1>
          <p class="text-sm text-gray-600">
            Текущий пользователь: 
            <span 
              :class="[
                'font-medium',
                currentUser === 'User A' ? 'text-blue-600' : 'text-green-600'
              ]"
            >
              {{ currentUser }}
            </span>
          </p>
        </div>
      </div>
      
      <div class="flex items-center gap-4">
        <!-- Статус WebSocket подключения -->
        <div class="flex items-center gap-2">
          <div 
            :class="[
              'w-3 h-3 rounded-full',
              isConnected ? 'bg-green-500' : 'bg-red-500'
            ]"
          ></div>
          <span class="text-sm text-gray-500">
            {{ isConnected ? 'Онлайн' : 'Оффлайн' }}
          </span>
        </div>
        
        <!-- Статистика -->
        <div class="text-sm text-gray-500">
          <div>Сообщений: {{ messageCount }}</div>
          <div>Бот ответов: {{ botMessageCount }}</div>
        </div>
        
        <!-- Индикатор загрузки -->
        <div v-if="isLoading" class="flex items-center gap-2">
          <div class="w-3 h-3 bg-blue-500 rounded-full animate-pulse"></div>
          <span class="text-sm text-gray-500">Загрузка...</span>
        </div>
        
        <div class="flex items-center gap-2">
          <button
            @click="clearChat"
            :disabled="isLoading"
            class="px-3 py-1 text-sm bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors duration-200 disabled:opacity-50"
            title="Очистить чат"
          >
            🗑️ Очистить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useChatStore } from '../stores/chat'

const chatStore = useChatStore()
const currentUser = computed(() => chatStore.currentUser)
const messageCount = computed(() => chatStore.messages.length)
const botMessageCount = computed(() => chatStore.botMessages.length)
const isLoading = computed(() => chatStore.isLoading)
const isConnected = computed(() => chatStore.isConnected)

const clearChat = async () => {
  if (confirm('Вы уверены, что хотите очистить весь чат?')) {
    await chatStore.clearMessages()
  }
}
</script> 