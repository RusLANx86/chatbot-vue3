<template>
  <div class="app min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
    <div class="max-w-4xl mx-auto">
      <ChatHeader />
      <UserSelector />
      
      <div class="chat-container bg-white rounded-lg shadow-lg overflow-hidden">
        <MessageList />
        <MessageForm />
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useChatStore } from './stores/chat'
import ChatHeader from './components/ChatHeader.vue'
import UserSelector from './components/UserSelector.vue'
import MessageList from './components/MessageList.vue'
import MessageForm from './components/MessageForm.vue'

const chatStore = useChatStore()

onMounted(() => {
  chatStore.loadFromLocalStorage()
})
</script>

<style>
.app {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.chat-container {
  height: 60vh;
  display: flex;
  flex-direction: column;
}
</style> 