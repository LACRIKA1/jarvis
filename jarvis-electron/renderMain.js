// Создание волн (центрированных, отдельно от текста)
const soundWave = document.getElementById('sound-wave');
soundWave.style.display = 'flex';
soundWave.style.justifyContent = 'center';
soundWave.style.alignItems = 'flex-end';
soundWave.style.height = '100px'; // Фиксированная высота для волн
soundWave.style.gap = '4px';

for (let i = 0; i < 16; i++) {
  const bar = document.createElement('div');
  bar.style.width = '3px';
  bar.style.height = '20px';
  bar.style.background = `hsl(${100 + i * 5}, 100%, 50%)`;
  bar.style.boxShadow = '0 0 8px currentColor';
  bar.style.borderRadius = '2px';
  bar.style.animation = `pulse ${1.5 + Math.random()}s infinite alternate ease-in-out`;
  bar.style.animationDelay = `${i * 0.1}s`;
  soundWave.appendChild(bar);
}

let isGlitching = false;
let glitchInterval;
let restoreInterval;

function glitchText() {
  if (isGlitching) return;
  isGlitching = true;
  
  const el = document.getElementById('response');
  const originalText = el.textContent;
  const chars = "0123456789ABCDEF";
  const glitchDuration = 2000; 
  const restoreDuration = 9000; 
  const frameRate = 24; // кадров в секунду

  // Фаза превращения в цифры
  clearInterval(glitchInterval);
  let glitchSteps = 0;
  const totalGlitchSteps = (glitchDuration / 1000) * frameRate;
  
  glitchInterval = setInterval(() => {
    const progress = glitchSteps / totalGlitchSteps;
    el.textContent = originalText.split('').map(char => {
      // Постепенно увеличиваем вероятность замены символа
      if (Math.random() > progress * 10) return char;//
      return chars[Math.floor(Math.random() * chars.length)];
    }).join('');

    if (++glitchSteps >= totalGlitchSteps) {
      clearInterval(glitchInterval);
      
      // Фаза восстановления в исходный текст
      let restoreSteps = 0;
      const totalRestoreSteps = (restoreDuration / 1000) * frameRate;
      const finalText = originalText;
      const currentText = el.textContent.split('');
      
      restoreInterval = setInterval(() => {
        const restoreProgress = restoreSteps / totalRestoreSteps;
        el.textContent = currentText.map((char, index) => {
          // Плавное восстановление каждого символа
          if (Math.random() < restoreProgress * 25) {//
            return finalText[index];
          }
          return char;
        }).join('');

        if (++restoreSteps >= totalRestoreSteps) {
          clearInterval(restoreInterval);
          el.textContent = finalText;
          isGlitching = false;
        }
      }, 1000 / frameRate);
    }
  }, 1000 / frameRate);
}

// Запускаем глитч каждые 15 секунд
setInterval(glitchText, 15000);

// Первый запуск с задержкой
setTimeout(glitchText, 5000);

function handleVoiceCommand(command) {
  if (command.includes('активируйся')) {
    window.ipcRenderer.send('open-chat-window')
  }
}

// Стили
const style = document.createElement('style');
style.textContent = `
  #text-container {
    position: absolute;
    top: 20%;
    width: 100%;
    text-align: center;
  }
  
  #wave-container {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 80%;
  }
  
  @keyframes pulse {
    0%, 100% { 
      height: 20px;
      opacity: 0.7;
    }
    50% { 
      height: 60px;
      opacity: 1;
    }
  }
`;
document.head.appendChild(style);