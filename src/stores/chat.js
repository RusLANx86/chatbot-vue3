import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useChatStore = defineStore('chat', () => {
  const messages = ref([])
  const currentUser = ref('User A')
  const typingUsers = ref(new Set())
  const channel = new BroadcastChannel('vue3-chat')

  const sortedMessages = computed(() => {
    return [...messages.value].sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp))
  })

  const userAMessages = computed(() => {
    return messages.value.filter(msg => msg.sender === 'User A')
  })

  const userBMessages = computed(() => {
    return messages.value.filter(msg => msg.sender === 'User B')
  })

  channel.onmessage = (event) => {
    const data = event.data
    if (data.type === 'new_message') {
      // Не дублируем сообщение, если оно уже есть
      if (!messages.value.some(m => m.id === data.message.id)) {
        messages.value.push(data.message)
        saveToLocalStorage()
      }
    } else if (data.type === 'user_typing') {
      if (data.user !== currentUser.value) {
        if (data.isTyping) {
          typingUsers.value.add(data.user)
        } else {
          typingUsers.value.delete(data.user)
        }
      }
    } else if (data.type === 'clear_chat') {
      messages.value = []
      saveToLocalStorage()
    }
  }

  const addMessage = (text) => {
    if (!text.trim()) return
    const message = {
      id: Date.now() + Math.random(),
      sender: currentUser.value,
      text: text.trim(),
      timestamp: new Date().toISOString()
    }
    messages.value.push(message)
    saveToLocalStorage()
    channel.postMessage({ type: 'new_message', message })
  }

  const setCurrentUser = (user) => {
    currentUser.value = user
    saveToLocalStorage()
  }

  const sendTypingStatus = (isTyping) => {
    channel.postMessage({
      type: 'user_typing',
      user: currentUser.value,
      isTyping
    })
  }

  const saveToLocalStorage = () => {
    localStorage.setItem('chat-messages', JSON.stringify(messages.value))
    localStorage.setItem('chat-current-user', currentUser.value)
  }

  const loadFromLocalStorage = () => {
    const savedMessages = localStorage.getItem('chat-messages')
    const savedUser = localStorage.getItem('chat-current-user')
    if (savedMessages) {
      messages.value = JSON.parse(savedMessages)
    }
    if (savedUser) {
      currentUser.value = savedUser
    }
  }

  const clearChat = () => {
    messages.value = []
    saveToLocalStorage()
    channel.postMessage({ type: 'clear_chat' })
  }

  return {
    messages,
    currentUser,
    sortedMessages,
    userAMessages,
    userBMessages,
    typingUsers,
    addMessage,
    setCurrentUser,
    sendTypingStatus,
    loadFromLocalStorage,
    clearChat
  }
}) 