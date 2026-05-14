const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('aiDeskMeter', {
  readStatus: () => ipcRenderer.invoke('read-status'),
  appInfo: () => ipcRenderer.invoke('app-info'),
  openDevView: () => ipcRenderer.invoke('open-dev-view'),
  openRuntimeDashboard: () => ipcRenderer.invoke('open-runtime-dashboard'),
  openDocsPage: () => ipcRenderer.invoke('open-docs-page'),
  openDiySpecPage: () => ipcRenderer.invoke('open-diy-spec-page'),
  openPartsSourcingPage: () => ipcRenderer.invoke('open-parts-sourcing-page')
});
