const { app, BrowserWindow, ipcMain } = require('electron')
let mainWindow,chatWindow
 

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    transparent: true,
    frame: false,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  })

  mainWindow.loadFile('index.html')

  // Окно чата (изначально скрыто)
  chatWindow = new BrowserWindow({
    width: 800,
    height: 600,
    transparent: true,
    frame: false,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    },
    show: false  // Сразу скрываем
  })
  chatWindow.loadFile('chat.html')
  
ipcMain.on('close-window', (event, windowType) => {
  if (windowType === 'main') {
    mainWindow.close(); // Закрыть приложение
  } else if (windowType === 'chat') {
    chatWindow.close(); // Или close(), если нужно полностью уничтожить
  }
});
}

app.whenReady().then(createWindow)

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit()
})