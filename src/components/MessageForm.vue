<template>
  <div class="message-form bg-white rounded-lg shadow-md p-4">
    <form @submit.prevent="sendMessage" class="flex gap-2">
      <input
        v-model="messageText"
        type="text"
        placeholder="Введите сообщение..."
        class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        @input="handleTyping"
        @focus="handleTyping"
        @blur="stopTyping"
      />
      <button
        type="submit"
        :disabled="!messageText.trim()"
        :class="[
          'px-6 py-2 rounded-lg font-medium transition-all duration-200',
          messageText.trim()
            ? 'bg-blue-500 text-white hover:bg-blue-600 shadow-md'
            : 'bg-gray-300 text-gray-500 cursor-not-allowed'
        ]"
      >
        📤
      </button>
    </form>
    
    <!-- Индикатор печати других пользователей -->
    <div v-if="otherUsersTyping.length > 0" class="mt-2 text-sm text-gray-500 flex items-center gap-2">
      <div class="flex space-x-1">
        <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
        <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
        <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
      </div>
      <span>{{ otherUsersTyping.join(', ') }} печатает...</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted } from 'vue'
import { useChatStore } from '../stores/chat'

const chatStore = useChatStore()
const messageText = ref('')
const isTyping = ref(false)
let typingTimeout = null

const currentUser = computed(() => chatStore.currentUser)
const typingUsers = computed(() => chatStore.typingUsers)

// Пользователи, которые печатают (кроме текущего)
const otherUsersTyping = computed(() => {
  return Array.from(typingUsers.value).filter(user => user !== currentUser.value)
})

const handleTyping = () => {
  if (!isTyping.value) {
    isTyping.value = true
    chatStore.sendTypingStatus(true)
  }
  if (typingTimeout) {
    clearTimeout(typingTimeout)
  }
  typingTimeout = setTimeout(() => {
    stopTyping()
  }, 2000)
}

const stopTyping = () => {
  if (isTyping.value) {
    isTyping.value = false
    chatStore.sendTypingStatus(false)
  }
  if (typingTimeout) {
    clearTimeout(typingTimeout)
    typingTimeout = null
  }
}

const sendMessage = () => {
  if (!messageText.value.trim()) return
  chatStore.addMessage(messageText.value)
  messageText.value = ''
  stopTyping()
}

onUnmounted(() => {
  stopTyping()
})
</script> 