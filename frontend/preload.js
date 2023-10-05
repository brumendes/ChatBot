const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('electronAPI', {
  getResponse: (input) => ipcRenderer.send('get-response', input)
})