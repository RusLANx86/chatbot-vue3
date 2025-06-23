import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const API_BASE_URL = 'http://localhost:8000'
const WS_URL = 'ws://localhost:8000/ws'

export const useChatStore = defineStore('chat', () => {
  // Состояние
  const messages = ref([])
  const currentUser = ref('User A')
  const isLoading = ref(false)
  const error = ref(null)
  const isConnected = ref(false)
  const llmStatus = ref('unknown') // 'unknown', 'loading', 'ready', 'error'
  
  let ws = null

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

  const botMessages = computed(() => {
    return messages.value.filter(msg => msg.sender === 'Bot')
  })

  const userMessages = computed(() => messages.value.filter(m => m.sender !== 'Bot'))

  // WebSocket соединение
  const connectWebSocket = () => {
    if (ws) {
      ws.close()
    }

    ws = new WebSocket(WS_URL)
    
    ws.onopen = () => {
      console.log('WebSocket соединение установлено')
      isConnected.value = true
      error.value = null
      checkLLMStatus()
    }

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        
        if (data.type === 'new_message') {
          // Проверяем, нет ли уже такого сообщения
          if (!messages.value.some(m => m.id === data.message.id)) {
            messages.value.push(data.message)
          }
        } else if (data.type === 'clear_messages') {
          messages.value = []
        } else if (data.type === 'llm_status') {
          llmStatus.value = data.status
        }
      } catch (err) {
        console.error('Ошибка обработки WebSocket сообщения:', err)
      }
    }

    ws.onclose = () => {
      console.log('WebSocket соединение закрыто')
      isConnected.value = false
      
      // Попытка переподключения через 3 секунды
      setTimeout(() => {
        if (!isConnected.value) {
          connectWebSocket()
        }
      }, 3000)
    }

    ws.onerror = (error) => {
      console.error('WebSocket ошибка:', error)
      isConnected.value = false
    }
  }

  // API функции
  const fetchMessages = async () => {
    try {
      isLoading.value = true
      error.value = null
      const response = await fetch(`${API_BASE_URL}/messages`)
      if (!response.ok) {
        throw new Error('Failed to fetch messages')
      }
      const data = await response.json()
      messages.value = data
    } catch (err) {
      error.value = err.message
      console.error('Error fetching messages:', err)
    } finally {
      isLoading.value = false
    }
  }

  const sendMessage = async (text) => {
    if (!text.trim()) return

    try {
      isLoading.value = true
      error.value = null
      
      if (isConnected.value && ws) {
        // Отправляем через WebSocket для реального времени
        ws.send(JSON.stringify({
          type: 'new_message',
          sender: currentUser.value,
          text: text.trim()
        }))
      } else {
        // Fallback на REST API
        const response = await fetch(`${API_BASE_URL}/messages`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            sender: currentUser.value,
            text: text.trim()
          })
        })

        if (!response.ok) {
          throw new Error('Failed to send message')
        }

        const newMessage = await response.json()
        messages.value.push(newMessage)
      }

    } catch (err) {
      error.value = err.message
      console.error('Error sending message:', err)
    } finally {
      isLoading.value = false
    }
  }

  const clearMessages = async () => {
    try {
      isLoading.value = true
      error.value = null
      
      const response = await fetch(`${API_BASE_URL}/messages`, {
        method: 'DELETE'
      })

      if (!response.ok) {
        throw new Error('Failed to clear messages')
      }

      messages.value = []
    } catch (err) {
      error.value = err.message
      console.error('Error clearing messages:', err)
    } finally {
      isLoading.value = false
    }
  }

  const setCurrentUser = (user) => {
    currentUser.value = user
    localStorage.setItem('chat-current-user', user)
  }

  const loadFromLocalStorage = () => {
    const savedUser = localStorage.getItem('chat-current-user')
    if (savedUser) {
      currentUser.value = savedUser
    }
    // Загружаем сообщения из API и подключаемся к WebSocket
    fetchMessages()
    connectWebSocket()
  }

  const disconnect = () => {
    if (ws) {
      ws.close()
    }
  }

  // Проверка статуса LLM
  const checkLLMStatus = async () => {
    try {
      llmStatus.value = 'loading'
      const response = await fetch(`${API_BASE_URL}/bot/status`)
      const data = await response.json()
      llmStatus.value = data.status
    } catch (error) {
      console.error('Ошибка проверки статуса LLM:', error)
      llmStatus.value = 'error'
    }
  }

  return {
    messages,
    currentUser,
    sortedMessages,
    userAMessages,
    userBMessages,
    botMessages,
    userMessages,
    isLoading,
    error,
    isConnected,
    llmStatus,
    sendMessage,
    setCurrentUser,
    fetchMessages,
    clearMessages,
    loadFromLocalStorage,
    disconnect,
    checkLLMStatus
  }
}) 