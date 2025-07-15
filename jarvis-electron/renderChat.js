document.addEventListener('DOMContentLoaded', () => {
  // Проверка подключения IPC
  if (!window.ipcRenderer) {
    console.error('IPC Renderer не подключен!');
    return;
  }

  // Элементы интерфейса
  const closeBtn = document.getElementById('close-btn');
  const chatContainer = document.getElementById('chat-container');
  const userInput = document.getElementById('user-input');
  const sendBtn = document.getElementById('send-btn');
  const voiceBtn = document.getElementById('voice-btn');
  const statusBar = document.getElementById('animated-border'); // Добавлено

  // Обработчик закрытия окна
  closeBtn.addEventListener('click', () => {
    window.ipcRenderer.send('close-window', 'chat');
  });

  // Добавление сообщений с эффектом
  function addMessage(sender, text, className) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${className}`;
    
    // Эффект постепенного появления
    messageDiv.style.opacity = '0';
    messageDiv.innerHTML = `<strong>${sender}:</strong> ${text}`;
    chatContainer.appendChild(messageDiv);
    
    // Анимация появления
    let opacity = 0;
    const fadeIn = setInterval(() => {
      opacity += 0.05;
      messageDiv.style.opacity = opacity;
      if (opacity >= 1) clearInterval(fadeIn);
    }, 30);
    
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }

  // Отправка сообщений
  function sendMessage() {
    const message = userInput.value.trim();
    if (message) {
      addMessage('Вы', message, 'user-message');
      socket.emit('user_message', { text: message });
      userInput.value = '';
    }
  }

  // Обработчики событий
  sendBtn.addEventListener('click', sendMessage);
  userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
  });

  // Получение ответов от JARVIS
  socket.on('jarvis_message', (data) => {
    addMessage('JARVIS', data.text, 'jarvis-message');
    
    // Мигание полосы при новом сообщении
    statusBar.style.animation = 'none';
    setTimeout(() => {
      statusBar.style.animation = 
        'border-pulse 4s infinite ease-in-out, gradient-flow 12s infinite linear';
    }, 10);
  });

  // Инициализация Socket.IO
  const socket = io('http://localhost:5000');
});