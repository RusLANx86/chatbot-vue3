<template>
  <div class="message-form bg-white rounded-lg shadow-md p-4">
    <form @submit.prevent="sendMessage" class="flex gap-2">
      <input
        v-model="messageText"
        type="text"
        placeholder="Введите сообщение..."
        class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        :disabled="isTyping"
      />
      <button
        type="submit"
        :disabled="!messageText.trim() || isTyping"
        :class="[
          'px-6 py-2 rounded-lg font-medium transition-all duration-200',
          messageText.trim() && !isTyping
            ? 'bg-blue-500 text-white hover:bg-blue-600 shadow-md'
            : 'bg-gray-300 text-gray-500 cursor-not-allowed'
        ]"
      >
        <span v-if="!isTyping">📤</span>
        <span v-else class="animate-pulse">⏳</span>
      </button>
    </form>
    
    <div v-if="isTyping" class="mt-2 text-sm text-gray-500 flex items-center gap-2">
      <div class="flex space-x-1">
        <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
        <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
        <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
      </div>
      <span>{{ currentUser === 'User A' ? 'User B' : 'User A' }} печатает...</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useChatStore } from '../stores/chat'

const chatStore = useChatStore()
const messageText = ref('')
const isTyping = ref(false)

const currentUser = computed(() => chatStore.currentUser)

// Отслеживаем изменения в сообщениях для показа индикатора печати
watch(() => chatStore.messages.length, (newCount, oldCount) => {
  if (newCount > oldCount) {
    const lastMessage = chatStore.messages[chatStore.messages.length - 1]
    if (lastMessage.sender !== currentUser.value) {
      isTyping.value = true
      setTimeout(() => {
        isTyping.value = false
      }, 2000)
    }
  }
})

const sendMessage = () => {
  if (!messageText.value.trim()) return
  
  chatStore.addMessage(messageText.value)
  messageText.value = ''
}
</script> 