const { app, BrowserWindow } = require('electron') //импорт модуля
const path = require('path')

let mainWindow

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    transparent: true,          // Прозрачное окно
    frame: false,               // Без рамки
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  })
// load html file
  mainWindow.loadFile('index.html')

  // Открываем DevTools для отладки (можно убрать)
  // mainWindow.webContents.openDevTools()
}

app.whenReady().then(createWindow)

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit()
})