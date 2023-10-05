const { app, BrowserWindow } = require('electron')

const createWindow = () => {
  const win = new BrowserWindow({
    width: 500,
    height: 700,
    autoHideMenuBar: true,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    },
    resizable: false,
  })

  // win.webContents.openDevTools()
  win.setSize(500, 800)
  win.loadFile('app.html')
  win.setIcon('assets/ipo-small-logo.ico')
}

app.whenReady().then(() => {
  createWindow()
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit()
})

try {
  require('electron-reloader')(module)
} catch (_) {}