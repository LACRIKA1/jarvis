// Создаем звуковые волны
const soundWave = document.getElementById('sound-wave')
for (let i = 0; i < 12; i++) {
  const bar = document.createElement('div')
  bar.className = 'wave-bar'
  bar.style.animationDelay = `${i * 0.1}s`
  soundWave.appendChild(bar)
}

// Кнопка закрытия
document.getElementById('close-btn').addEventListener('click', () => {
  window.close()
})

// Подключение к Python через WebSocket
const socket = new WebSocket('ws://localhost:5000')

socket.onmessage = (event) => {
  document.getElementById('response').textContent = event.data
}

// Для теста (можно удалить):
setInterval(() => {
  const phrases = [
    "Анализирую данные...",
    "Сканирую сеть...",
    "Готов к работе",
    "Жду указаний"
  ]
  document.getElementById('response').textContent = 
    phrases[Math.floor(Math.random() * phrases.length)]
}, 3000)