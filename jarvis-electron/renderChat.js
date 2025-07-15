document.addEventListener('DOMContentLoaded', () => {
  // Проверка подключения IPC
  if (!window.ipcRenderer) {
    console.error('IPC Renderer не подключен!')
    return
  }

  // Элементы интерфейса
const closeBtn = document.getElementById('close-btn');

// Обработчик закрытия окна
closeBtn.addEventListener('click', () => {
    window.ipcRenderer.send('close-window', 'chat');
});

  // Остальной код чата...
  const socket = io('http://localhost:5000')
  const chatContainer = document.getElementById('chat-container')
  const userInput = document.getElementById('user-input')
  const sendBtn = document.getElementById('send-btn')
  const voiceBtn = document.getElementById('voice-btn')

  function addMessage(sender, text, className) {
    const messageDiv = document.createElement('div')
    messageDiv.className = `message ${className}`
    messageDiv.innerHTML = `<strong>${sender}:</strong> ${text}`
    chatContainer.appendChild(messageDiv)
    chatContainer.scrollTop = chatContainer.scrollHeight
  }

  function sendMessage() {
    const message = userInput.value.trim()
    if (message) {
      addMessage('Вы', message, 'user-message')
      socket.emit('user_message', { text: message })
      userInput.value = ''
    }
  }

  sendBtn.addEventListener('click', sendMessage)
  userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage()
  })

  socket.on('jarvis_message', (data) => {
    addMessage('JARVIS', data.text, 'jarvis-message')
  })
})