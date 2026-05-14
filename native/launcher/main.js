const { app, BrowserWindow, ipcMain, shell } = require('electron');
const path = require('path');
const fs = require('fs');
const childProcess = require('child_process');
const http = require('http');
const url = require('url');

const PROJECT_ROOT = process.env.AI_METER_PROJECT_ROOT || path.resolve(__dirname, '..', '..');
// Default payload: runtime/status.json
const STATUS_PATH = process.env.AI_METER_STATUS_PATH || path.join(PROJECT_ROOT, 'runtime', 'status.json');
const PROVIDER = process.env.AI_METER_PROVIDER || 'mock';
const INTERVAL = process.env.AI_METER_INTERVAL || '0.5';
const OWNS_RUNTIME = process.env.AI_METER_ELECTRON_OWNS_RUNTIME === '1';
let runtimeProcess = null;
let dashboardServer = null;
const DASHBOARD_HOST = '127.0.0.1';
const DASHBOARD_PORT = Number(process.env.AI_METER_DASHBOARD_PORT || '1420');

function candidateAiMeter() {
  const venvBin = process.platform === 'win32'
    ? path.join(PROJECT_ROOT, 'host', '.venv', 'Scripts', 'ai-meter.exe')
    : path.join(PROJECT_ROOT, 'host', '.venv', 'bin', 'ai-meter');
  if (fs.existsSync(venvBin)) return venvBin;
  return 'ai-meter';
}


function ensureRuntime() {
  if (!OWNS_RUNTIME) return;
  fs.mkdirSync(path.dirname(STATUS_PATH), { recursive: true });
  runtimeProcess = childProcess.spawn(candidateAiMeter(), [
    'runtime', '--provider', PROVIDER, '--out', STATUS_PATH, '--interval', INTERVAL
  ], { cwd: PROJECT_ROOT, stdio: ['ignore', 'pipe', 'pipe'] });
  runtimeProcess.stdout.on('data', (data) => console.log(String(data).trim()));
  runtimeProcess.stderr.on('data', (data) => console.error(String(data).trim()));
}

function sendText(res, status, type, body) {
  res.statusCode = status;
  res.setHeader('Content-Type', type);
  res.setHeader('Cache-Control', 'no-store');
  res.end(body);
}

function safeRead(filePath) {
  return fs.readFileSync(filePath, 'utf8');
}

function serveRuntimeDashboardRequest(req, res) {
  const parsed = url.parse(req.url || '/');
  const pathname = parsed.pathname || '/';
  try {
    if (pathname === '/' || pathname === '/index.html') {
      return sendText(res, 200, 'text/html; charset=utf-8', safeRead(path.join(__dirname, 'app', 'index.html')));
    }
    if (pathname === '/runtime/status.json') {
      if (!fs.existsSync(STATUS_PATH)) {
        return sendText(res, 404, 'application/json; charset=utf-8', JSON.stringify({
          schema: 'ai-desk-meter.v1',
          runtime_connected: false,
          muse_connected: false,
          muse_state: 'none',
          status: 'No active Muse',
          mode: 'not connected',
          source: 'runtime-dashboard',
          errors: ['runtime/status.json not found']
        }));
      }
      return sendText(res, 200, 'application/json; charset=utf-8', safeRead(STATUS_PATH));
    }
    if (pathname === '/health') {
      return sendText(res, 200, 'application/json; charset=utf-8', JSON.stringify({
        ok: true,
        dashboard: 'runtime-ip-site',
        statusPath: STATUS_PATH,
        runtimeStatusExists: fs.existsSync(STATUS_PATH)
      }));
    }
    if (pathname === '/app/renderer.js' || pathname === '/renderer.js') {
      return sendText(res, 200, 'application/javascript; charset=utf-8', safeRead(path.join(__dirname, 'app', 'renderer.js')));
    }
    if (pathname === '/app/styles.css' || pathname === '/styles.css') {
      return sendText(res, 200, 'text/css; charset=utf-8', safeRead(path.join(__dirname, 'app', 'styles.css')));
    }
    if (pathname === '/assets/pixel-buddy-musing.svg') {
      return sendText(res, 200, 'image/svg+xml; charset=utf-8', safeRead(path.join(__dirname, 'assets', 'pixel-buddy-musing.svg')));
    }
    if (pathname === '/docs/index.html') {
      return sendText(res, 200, 'text/html; charset=utf-8', safeRead(path.join(PROJECT_ROOT, 'docs', 'index.html')));
    }
    if (pathname === '/DIY_Claude_Code_Desk_Usage_Meter_Spec_Guide.html') {
      return sendText(res, 200, 'text/html; charset=utf-8', safeRead(path.join(PROJECT_ROOT, 'DIY_Claude_Code_Desk_Usage_Meter_Spec_Guide.html')));
    }
    if (pathname === '/docs/parts-and-sourcing.md') {
      return sendText(res, 200, 'text/markdown; charset=utf-8', safeRead(path.join(PROJECT_ROOT, 'docs', 'parts-and-sourcing.md')));
    }
    return sendText(res, 404, 'text/plain; charset=utf-8', 'not found');
  } catch (error) {
    return sendText(res, 500, 'text/plain; charset=utf-8', String(error && error.message ? error.message : error));
  }
}

function ensureRuntimeDashboardServer() {
  if (dashboardServer && dashboardServer.listening) return;
  dashboardServer = http.createServer(serveRuntimeDashboardRequest);
  dashboardServer.on('error', (error) => {
    // If another dashboard already owns the port, do not crash; the URL can still be tried.
    console.error('runtime dashboard IP server warning:', error && error.message ? error.message : error);
  });
  dashboardServer.listen(DASHBOARD_PORT, DASHBOARD_HOST, () => {
    console.log(`runtime dashboard IP site listening at http://${DASHBOARD_HOST}:${DASHBOARD_PORT}/#muse`);
  });
}

function createWindow() {
  const win = new BrowserWindow({
    width: 1180,
    height: 820,
    minWidth: 900,
    minHeight: 620,
    title: 'AI Desk Meter',
    backgroundColor: '#05070b',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: false
    }
  });
  win.loadFile(path.join(__dirname, 'app', 'index.html'));
}

ipcMain.handle('read-status', async () => {
  try {
    return { ok: true, path: STATUS_PATH, text: fs.readFileSync(STATUS_PATH, 'utf8') };
  } catch (error) {
    return { ok: false, path: STATUS_PATH, error: String(error && error.message ? error.message : error) };
  }
});

ipcMain.handle('app-info', async () => ({
  projectRoot: PROJECT_ROOT,
  statusPath: STATUS_PATH,
  provider: PROVIDER,
  interval: INTERVAL,
  ownsRuntime: OWNS_RUNTIME
}));


ipcMain.handle('open-runtime-dashboard', async () => {
  try {
    ensureRuntimeDashboardServer();
    const target = `http://${DASHBOARD_HOST}:${DASHBOARD_PORT}/#muse`;
    setTimeout(() => shell.openExternal(target), 300);
    return { ok: true, target };
  } catch (error) {
    return { ok: false, error: String(error && error.message ? error.message : error) };
  }
});

ipcMain.handle('open-docs-page', async () => {
  try {
    const docsPath = path.join(PROJECT_ROOT, 'docs', 'index.html');
    await shell.openExternal('file://' + docsPath);
    return { ok: true, target: docsPath };
  } catch (error) {
    return { ok: false, error: String(error && error.message ? error.message : error) };
  }
});



ipcMain.handle('open-diy-spec-page', async () => {
  try {
    const specPath = path.join(PROJECT_ROOT, 'DIY_Claude_Code_Desk_Usage_Meter_Spec_Guide.html');
    await shell.openExternal('file://' + specPath + '#bom');
    return { ok: true, target: specPath + '#bom' };
  } catch (error) {
    return { ok: false, error: String(error && error.message ? error.message : error) };
  }
});


ipcMain.handle('open-parts-sourcing-page', async () => {
  try {
    const partsPath = path.join(PROJECT_ROOT, 'docs', 'parts-and-sourcing.md');
    await shell.openExternal('file://' + partsPath);
    return { ok: true, target: partsPath };
  } catch (error) {
    return { ok: false, error: String(error && error.message ? error.message : error) };
  }
});

ipcMain.handle('open-dev-view', async () => {
  try {
    const pagePath = path.join(__dirname, 'app', 'index.html');
    await shell.openExternal('file://' + pagePath + '#docs');
    return { ok: true, target: pagePath + '#docs' };
  } catch (error) {
    return { ok: false, error: String(error && error.message ? error.message : error) };
  }
});

app.whenReady().then(() => {
  ensureRuntime();
  ensureRuntimeDashboardServer();
  createWindow();
});

app.on('window-all-closed', () => {
  if (runtimeProcess) runtimeProcess.kill();
  if (dashboardServer) dashboardServer.close();
  if (process.platform !== 'darwin') app.quit();
});

app.on('before-quit', () => {
  if (runtimeProcess) runtimeProcess.kill();
  if (dashboardServer) dashboardServer.close();
});
