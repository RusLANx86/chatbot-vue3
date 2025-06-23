<template>
  <div class="user-selector bg-white rounded-lg shadow-md p-4 mb-4">
    <h3 class="text-lg font-semibold text-gray-800 mb-3">Выберите пользователя:</h3>
    <div class="flex gap-2">
      <button
        @click="setUser('User A')"
        :class="[
          'px-4 py-2 rounded-lg font-medium transition-all duration-200',
          currentUser === 'User A'
            ? 'bg-blue-500 text-white shadow-lg'
            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
        ]"
      >
        👤 User A
      </button>
      <button
        @click="setUser('User B')"
        :class="[
          'px-4 py-2 rounded-lg font-medium transition-all duration-200',
          currentUser === 'User B'
            ? 'bg-green-500 text-white shadow-lg'
            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
        ]"
      >
        👤 User B
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useChatStore } from '../stores/chat'

const chatStore = useChatStore()
const currentUser = computed(() => chatStore.currentUser)

const setUser = (user) => {
  chatStore.setCurrentUser(user)
}
</script> 