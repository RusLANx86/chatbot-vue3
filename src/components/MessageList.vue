<template>
  <div class="message-list flex-1 overflow-y-auto p-4 space-y-4">
    <div v-if="sortedMessages.length === 0" class="text-center text-gray-500 py-8">
      <div class="text-4xl mb-2">💬</div>
      <p>Начните разговор, отправив первое сообщение!</p>
    </div>
    
    <div
      v-for="message in sortedMessages"
      :key="message.id"
      :class="[
        'message flex',
        message.sender === currentUser ? 'justify-end' : 'justify-start'
      ]"
    >
      <div
        :class="[
          'max-w-xs lg:max-w-md px-4 py-2 rounded-lg shadow-sm',
          message.sender === currentUser
            ? 'bg-blue-500 text-white'
            : message.sender === 'Bot'
            ? 'bg-purple-500 text-white'
            : 'bg-gray-100 text-gray-800'
        ]"
      >
        <div class="flex items-center justify-between mb-1">
          <span class="font-medium text-sm">
            {{ message.sender }}
            <span v-if="message.sender === 'Bot'" class="text-xs">🤖</span>
          </span>
          <span 
            :class="[
              'text-xs',
              message.sender === currentUser 
                ? 'text-blue-100' 
                : message.sender === 'Bot'
                ? 'text-purple-100'
                : 'text-gray-500'
            ]"
          >
            {{ formatTime(message.timestamp) }}
          </span>
        </div>
        <p class="text-sm leading-relaxed">{{ message.text }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useChatStore } from '../stores/chat'

const chatStore = useChatStore()
const currentUser = computed(() => chatStore.currentUser)
const sortedMessages = computed(() => chatStore.sortedMessages)

const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  return date.toLocaleTimeString('ru-RU', {
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style scoped>
.message-list {
  scrollbar-width: thin;
  scrollbar-color: #cbd5e0 #f7fafc;
}

.message-list::-webkit-scrollbar {
  width: 6px;
}

.message-list::-webkit-scrollbar-track {
  background: #f7fafc;
}

.message-list::-webkit-scrollbar-thumb {
  background: #cbd5e0;
  border-radius: 3px;
}

.message-list::-webkit-scrollbar-thumb:hover {
  background: #a0aec0;
}
</style> 