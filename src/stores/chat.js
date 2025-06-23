import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useChatStore = defineStore('chat', () => {
  // Состояние
  const messages = ref([])
  const currentUser = ref('User A')
  const botResponses = [
    'Интересно! Расскажи подробнее.',
    'Понятно, что ты имеешь в виду.',
    'Это очень интересная мысль!',
    'Согласен с тобой.',
    'Хм, нужно подумать об этом.',
    'Отличная идея!',
    'Спасибо за информацию.',
    'Это заставляет задуматься.',
    'Очень хорошо сказано!',
    'Продолжай, мне интересно.'
  ]

  // Геттеры
  const sortedMessages = computed(() => {
    return [...messages.value].sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp))
  })

  const userAMessages = computed(() => {
    return messages.value.filter(msg => msg.sender === 'User A')
  })

  const userBMessages = computed(() => {
    return messages.value.filter(msg => msg.sender === 'User B')
  })

  // Действия
  const addMessage = (text) => {
    if (!text.trim()) return

    const message = {
      id: Date.now(),
      sender: currentUser.value,
      text: text.trim(),
      timestamp: new Date().toISOString()
    }

    messages.value.push(message)
    saveToLocalStorage()

    // Имитация ответа бота через 1-2 секунды
    setTimeout(() => {
      const botResponse = {
        id: Date.now() + 1,
        sender: currentUser.value === 'User A' ? 'User B' : 'User A',
        text: botResponses[Math.floor(Math.random() * botResponses.length)],
        timestamp: new Date().toISOString()
      }
      messages.value.push(botResponse)
      saveToLocalStorage()
    }, 1000 + Math.random() * 1000)
  }

  const setCurrentUser = (user) => {
    currentUser.value = user
    saveToLocalStorage()
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
    localStorage.removeItem('chat-messages')
  }

  return {
    messages,
    currentUser,
    sortedMessages,
    userAMessages,
    userBMessages,
    addMessage,
    setCurrentUser,
    loadFromLocalStorage,
    clearChat
  }
}) 