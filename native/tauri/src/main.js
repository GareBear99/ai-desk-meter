// compat markers: read_status_file getTauriInvoke payloadFile browser preview awaiting runtime/status.json dots setInterval(refresh, 500)
const DEFAULT_PATH = 'runtime/status.json';
const NO_ACTIVE_MUSE = 'No active Muse';
const SVG_NO_MUSE = 'No Muse.';
const ACTIVE_MUSING = '✶ Musing...';
const RUNTIME_DASHBOARD_URL = 'http://127.0.0.1:1420/#muse';
const REFRESH_MS = 500;
const DISCONNECT_GRACE_COUNT = 6;
const el = (id) => document.getElementById(id);

let blinkTimer = null;
let eyeOpenTimer = null;
let blinkCycleStarted = false;
let lastBlinkSignature = '';
let lastRuntimeConnected = false;
let lastMuseConnected = false;
let lastPayloadFingerprint = '';
let lastStablePayload = null;
let lastStableSourceLabel = '';
let lastStableExtraInfo = {};
let transientDisconnectCount = 0;
let refreshInFlight = false;
let initialized = false;

const COMMANDS = [
  'ai-meter app',
  'ai-meter runtime --provider mock --out runtime/status.json --interval 0.5',
  'ai-meter status --provider mock',
  'ai-meter check-cli --provider mock',
  'ai-meter diagnostics --provider mock --out diagnostics.zip',
  'AI_METER_OMNIBINARY_REPO=integrations/omnibinary-runtime ai-meter status --provider omnibinary'
];
const API_ROUTES = [
  'ai-meter serve --host 127.0.0.1 --port 8787',
  'curl http://127.0.0.1:8787/health',
  'curl http://127.0.0.1:8787/providers',
  'curl "http://127.0.0.1:8787/status?provider=mock"',
  'curl "http://127.0.0.1:8787/companion/status?provider=mock"'
];

const refs = {};
function cacheRefs(){
  [
    'app','connectionPill','connectionText','buddySvg','buddyStatusLabel','statusText','statusWord','statusStar','statusDots',
    'currentPercent','weeklyPercent','currentBar','weeklyBar','currentReset','weeklyReset','burnRate','modeText','providerText','updatedText',
    'lastAction','lastActionTime','actionProgress','actionHint','cliChecker','cliCheckerDetail','runtimeSource','runtimeMode','pathText',
    'connectionState','shellState','projectRootText','statusPathText','devProviderText','refreshRateText','payloadJsonOutput','providerBoundaryOutput',
    'runLogOutput','logOutput','docsConnectionState','commandList','apiRouteList'
  ].forEach(id => refs[id] = el(id));
}
function setText(node, value){ if (node && node.textContent !== String(value)) node.textContent = String(value); }
function setClass(node, name, enabled){ if (node && node.classList.contains(name) !== !!enabled) node.classList.toggle(name, !!enabled); }
function safeText(value, fallback='unknown'){ const text=String(value ?? '').trim(); return text || fallback; }
function pct(value){ const n=Number(value); return Number.isFinite(n)?Math.max(0,Math.min(100,Math.round(n))):0; }
function fmtSeconds(value){ const s=Number(value); if(!Number.isFinite(s)||s<0)return 'unknown'; const d=Math.floor(s/86400), h=Math.floor((s%86400)/3600), m=Math.floor((s%3600)/60); if(d>0)return `${d}d ${h}h`; if(h>0)return `${h}h ${m}m`; return `${m}m`; }
function renderLogEntries(entries,fallback){ const values=Array.isArray(entries)?entries.filter(Boolean).map(String):[]; return values.length?values.join('\n'):fallback; }
function fingerprintFor(payload, runtimeConnected, museConnected, sourceLabel, extraInfo={}){
  if (!runtimeConnected) return `off|${sourceLabel}|${extraInfo.statusPath || ''}`;
  const checker = payload.cli_checker || {};
  return [
    runtimeConnected, museConnected, sourceLabel,
    payload.updated_at, payload.current_percent, payload.weekly_percent, payload.burn_rate, payload.mode,
    payload.source || payload.service, payload.last_action, payload.action_in_progress,
    checker.state, checker.last_check, checker.message,
    (payload.run_log || []).join('|'), (payload.warnings || []).join('|'), (payload.errors || []).join('|'),
    extraInfo.statusPath || '', extraInfo.shell || ''
  ].join('::');
}

function renderCommandLists(){
  if (refs.commandList && !refs.commandList.dataset.rendered) {
    refs.commandList.innerHTML = COMMANDS.map(c => `<code>${c}</code>`).join('');
    refs.commandList.dataset.rendered = '1';
  }
  if (refs.apiRouteList && !refs.apiRouteList.dataset.rendered) {
    refs.apiRouteList.innerHTML = API_ROUTES.map(c => `<code>${c}</code>`).join('');
    refs.apiRouteList.dataset.rendered = '1';
  }
}
function activateTab(tab){
  const name = tab || 'muse';
  document.querySelectorAll('.tab-button').forEach(b => setClass(b, 'active', b.dataset.tab === name));
  document.querySelectorAll('.tab-panel').forEach(panel => setClass(panel, 'active', panel.dataset.panel === name));
  if (name === 'muse') history.replaceState(null, '', location.pathname + location.search);
  else history.replaceState(null, '', `#${name}`);
}
function setupTabs(){
  document.querySelectorAll('.tab-button').forEach(btn => btn.addEventListener('click', () => activateTab(btn.dataset.tab)));
  const hash = (location.hash || '').replace('#','');
  activateTab(hash || 'muse');
}
function clearBlinkTimers(){
  if (blinkTimer) clearTimeout(blinkTimer);
  if (eyeOpenTimer) clearTimeout(eyeOpenTimer);
  blinkTimer = null; eyeOpenTimer = null;
  if (refs.buddySvg) refs.buddySvg.classList.remove('blink-eyes');
}
function currentBlinkDelayMs(payload, runtimeConnected, museConnected){
  if (!runtimeConnected) return null;
  if (!museConnected) return 3000 + Math.random() * 8000;
  const usage = pct(payload.current_percent);
  if (usage < 30) return 1000;
  if (usage < 70) return 2000;
  return 3000;
}
function blinkSignatureFor(payload={}, runtimeConnected=lastRuntimeConnected, museConnected=lastMuseConnected){
  const usage = pct(payload.current_percent);
  const bucket = !museConnected ? 'idle-no-muse' : (usage < 30 ? 'low' : usage < 70 ? 'medium' : 'high');
  return `${runtimeConnected}|${museConnected}|${bucket}`;
}
function scheduleEyeBlink(payload={}, runtimeConnected=lastRuntimeConnected, museConnected=lastMuseConnected){
  const svg = refs.buddySvg;
  const rawDelay = currentBlinkDelayMs(payload, runtimeConnected, museConnected);
  if (!svg || rawDelay === null) {
    clearBlinkTimers(); blinkCycleStarted = false; lastBlinkSignature = ''; return;
  }
  const signature = blinkSignatureFor(payload, runtimeConnected, museConnected);
  if (signature === lastBlinkSignature && blinkTimer) return;
  clearBlinkTimers();
  lastBlinkSignature = signature;
  const delay = blinkCycleStarted ? rawDelay : Math.min(rawDelay, 3000);
  blinkCycleStarted = true;
  blinkTimer = setTimeout(() => {
    svg.classList.add('blink-eyes');
    eyeOpenTimer = setTimeout(() => {
      svg.classList.remove('blink-eyes');
      blinkTimer = null;
      scheduleEyeBlink(payload, runtimeConnected, museConnected);
    }, 160);
  }, delay);
}
function isRuntimePayload(payload){
  if (!payload || typeof payload !== 'object') return false;
  const errors = Array.isArray(payload.errors) ? payload.errors : [];
  const source = safeText(payload.source || payload.service, '').toLowerCase();
  const mode = safeText(payload.mode, '').toLowerCase();
  if (!source || source === 'browser-sample' || source === 'browser-preview') return false;
  if (errors.length) return false;
  if (payload.runtime_connected === false) return false;
  return !['offline','error','disconnected','not connected'].includes(mode);
}
function isMusePayload(payload){
  if (!isRuntimePayload(payload)) return false;
  if (payload.muse_connected === true || payload.agent_connected === true || payload.active_muse === true) return true;
  const museState = safeText(payload.muse_state, '').toLowerCase();
  return ['musing','active','responding','loading','acting'].includes(museState);
}
function setConnectionState(runtimeConnected, detail=''){
  lastRuntimeConnected = !!runtimeConnected;
  setClass(refs.connectionPill, 'connected', !!runtimeConnected);
  setClass(refs.connectionPill, 'disconnected', !runtimeConnected);
  setText(refs.connectionText, runtimeConnected ? 'Runtime Connected' : 'Runtime Disconnected');
  setText(refs.docsConnectionState, runtimeConnected ? `Runtime connected${detail ? ' · '+detail : ''}` : `Runtime disconnected${detail ? ' · '+detail : ''}`);
}
function renderStatus(payload, runtimeConnected, museConnected){
  lastMuseConnected = !!museConnected;
  const requested = safeText(payload.status, NO_ACTIVE_MUSE);
  const musing = museConnected && requested.toLowerCase().includes('musing');
  const display = museConnected ? requested : NO_ACTIVE_MUSE;
  setClass(refs.app, 'is-musing', musing);
  setClass(refs.app, 'no-active', !museConnected);
  setClass(refs.statusStar, 'hidden', !musing);
  setClass(refs.statusDots, 'hidden', !musing);
  setText(refs.statusWord, musing ? 'Musing' : display);
  setText(refs.buddyStatusLabel, musing ? ACTIVE_MUSING : (display === NO_ACTIVE_MUSE ? SVG_NO_MUSE : display));
  scheduleEyeBlink(payload, runtimeConnected, museConnected);
}
function updateDevPanels(payload, runtimeConnected, museConnected, sourceLabel, extraInfo={}){
  const provider = runtimeConnected ? safeText(payload.source || payload.service, 'unknown') : 'not connected';
  setText(refs.connectionState, runtimeConnected ? (museConnected ? 'Runtime connected · Muse active' : 'Runtime connected · No active Muse') : 'Runtime disconnected');
  setText(refs.shellState, extraInfo.shell || 'runtime page');
  setText(refs.projectRootText, extraInfo.projectRoot || 'unknown');
  setText(refs.statusPathText, extraInfo.statusPath || DEFAULT_PATH);
  setText(refs.devProviderText, provider);
  setText(refs.refreshRateText, '0.5s');
  setText(refs.payloadJsonOutput, runtimeConnected ? JSON.stringify(payload, null, 2) : 'No runtime payload connected.');
  setText(refs.providerBoundaryOutput, JSON.stringify({
    connectionDot: 'green means CLI/runtime + runtime dashboard are reachable; it does not mean a Muse is active',
    museActiveRule: 'No active Muse changes only when muse_connected/agent_connected/active_muse is true or muse_state is active/musing',
    providers: ['mock','manual','arcrar','arcrar-cli','omnibinary'], provider, sourceLabel,
    statusEnv: 'AI_METER_STATUS_PATH', omnibinaryRepoEnv: 'AI_METER_OMNIBINARY_REPO', noServerDefault: true,
  }, null, 2));
}
function setPayload(payload, sourceLabel='runtime payload', extraInfo={}){
  const runtimeConnected = isRuntimePayload(payload);
  const museConnected = isMusePayload(payload);
  if (runtimeConnected) {
    transientDisconnectCount = 0; lastStablePayload = payload; lastStableSourceLabel = sourceLabel; lastStableExtraInfo = extraInfo;
  }
  const fp = fingerprintFor(payload, runtimeConnected, museConnected, sourceLabel, extraInfo);
  setConnectionState(runtimeConnected, runtimeConnected ? sourceLabel : 'waiting for runtime/status.json');
  renderStatus(payload, runtimeConnected, museConnected);
  if (fp === lastPayloadFingerprint) return;
  lastPayloadFingerprint = fp;

  const current = runtimeConnected ? pct(payload.current_percent) : 0;
  const weekly = runtimeConnected ? pct(payload.weekly_percent) : 0;
  setText(refs.currentPercent, runtimeConnected ? `${current}%` : '--%');
  setText(refs.weeklyPercent, runtimeConnected ? `${weekly}%` : '--%');
  if (refs.currentBar) refs.currentBar.style.width = `${current}%`;
  if (refs.weeklyBar) refs.weeklyBar.style.width = `${weekly}%`;
  setText(refs.currentReset, runtimeConnected ? `reset: ${fmtSeconds(payload.current_reset_seconds)}` : 'reset: inactive');
  setText(refs.weeklyReset, runtimeConnected ? `reset: ${fmtSeconds(payload.weekly_reset_seconds)}` : 'reset: inactive');
  setText(refs.burnRate, runtimeConnected ? safeText(payload.burn_rate) : 'inactive');
  setText(refs.modeText, `mode: ${runtimeConnected ? safeText(payload.mode) : 'not connected'}`);
  setText(refs.providerText, runtimeConnected ? safeText(payload.source || payload.service) : 'not connected');
  const updated = runtimeConnected && payload.updated_at ? new Date(payload.updated_at * 1000).toLocaleString() : 'never';
  setText(refs.updatedText, `updated: ${updated}`);
  setText(refs.lastAction, runtimeConnected ? safeText(payload.last_action, 'runtime connected') : 'no active runtime');
  setText(refs.lastActionTime, `updated: ${runtimeConnected ? updated : 'never'}`);
  setText(refs.actionProgress, museConnected ? safeText(payload.action_in_progress, 'musing') : 'none');
  setText(refs.actionHint, museConnected ? 'Muse/agent connected and reporting activity' : (runtimeConnected ? 'Runtime is up; no Muse/model agent is connected' : 'Runtime payload not connected'));
  const checker = payload.cli_checker || {};
  setText(refs.cliChecker, runtimeConnected ? safeText(checker.state, 'active') : 'inactive');
  const checkerTime = runtimeConnected && checker.last_check ? new Date(checker.last_check * 1000).toLocaleTimeString() : 'never';
  setText(refs.cliCheckerDetail, runtimeConnected ? `${safeText(checker.message, 'runtime payload loaded')} · ${checkerTime}` : 'No runtime connected');
  setText(refs.runtimeSource, runtimeConnected ? sourceLabel : 'not connected');
  setText(refs.runtimeMode, runtimeConnected ? (museConnected ? 'Muse active' : 'Runtime connected / No active Muse') : 'runtime disconnected');
  setText(refs.pathText, extraInfo.statusPath || DEFAULT_PATH);
  const warnings = Array.isArray(payload.warnings) ? payload.warnings : [];
  const errors = Array.isArray(payload.errors) ? payload.errors : [];
  setText(refs.runLogOutput, runtimeConnected ? renderLogEntries(payload.run_log, 'Runtime connected. No run log entries yet.') : `[${new Date().toLocaleTimeString()}] Runtime disconnected. Waiting for runtime/status.json.`);
  setText(refs.logOutput, warnings.length || errors.length ? JSON.stringify({ warnings, errors }, null, 2) : 'No warnings or errors.');
  updateDevPanels(payload, runtimeConnected, museConnected, sourceLabel, extraInfo);
}
function handleRuntimeUnavailable(message='runtime/status.json unavailable'){
  transientDisconnectCount += 1;
  if (lastStablePayload && transientDisconnectCount <= DISCONNECT_GRACE_COUNT) {
    setConnectionState(true, `last good payload; retry ${transientDisconnectCount}/${DISCONNECT_GRACE_COUNT}`);
    setText(refs.logOutput, `Runtime read retrying: ${message}`);
    return;
  }
  setDisconnected(message);
}
function setDisconnected(message='runtime/status.json unavailable'){
  setPayload({
    schema:'ai-desk-meter.v1', source:'browser-preview', service:'browser-preview', status:NO_ACTIVE_MUSE, mode:'not connected', runtime_connected:false, muse_connected:false, muse_state:'none', burn_rate:'inactive', current_percent:0, weekly_percent:0,
    last_action:'runtime disconnected', action_in_progress:'none', cli_checker:{state:'inactive',message,last_check:0}, run_log:[`[${new Date().toLocaleTimeString()}] Runtime disconnected: ${message}`], warnings:[], errors:[]
  }, 'not connected');
}
function openMusePanel(){ activateTab('muse'); window.scrollTo({ top:0, behavior:'smooth' }); }
function openSpecsPanel(){ activateTab('specs'); el('specsPanel')?.scrollIntoView({behavior:'smooth', block:'start'}); }
function openRuntimeDocsPanel(){ activateTab('docs'); el('docsPanel')?.scrollIntoView({behavior:'smooth', block:'start'}); }
function bindBaseButtons(){
  el('refreshButton')?.addEventListener('click', refresh);
  el('docsBackButton')?.addEventListener('click', openMusePanel);
  el('specsBackButton')?.addEventListener('click', openMusePanel);
  el('specsButton')?.addEventListener('click', openSpecsPanel);
  el('docsDiySpecLink')?.addEventListener('click', openDiySpecPage);
  el('partsSourcingButton')?.addEventListener('click', openPartsSourcingPage);
  el('partsSourcingDocsButton')?.addEventListener('click', openPartsSourcingPage);
  el('fullDocsButton')?.addEventListener('click', openFullDocsPage);
  el('dashboardButton')?.addEventListener('click', openRuntimeDashboard);
  el('docsButton')?.addEventListener('click', openFullDocsPage);
}
function bindImport(){
  el('payloadFile')?.addEventListener('change', async (event) => {
    const file = event.target.files?.[0]; if(!file) return;
    try { setPayload(JSON.parse(await file.text()), `imported: ${file.name}`, { statusPath: file.name, shell: 'manual import' }); }
    catch(error){ setDisconnected(`file import failed: ${error}`); }
  });
}
async function refresh(){
  if (refreshInFlight) return;
  refreshInFlight = true;
  try {
    if (!window.aiDeskMeter) {
      const res = await fetch('/runtime/status.json', { cache: 'no-store' });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const payload = await res.json();
      setPayload(payload, 'runtime dashboard IP site', { shell: 'browser runtime page', statusPath: 'runtime/status.json' });
      return;
    }
    const result = await window.aiDeskMeter.readStatus();
    if (!result.ok) { handleRuntimeUnavailable(result.error || 'runtime payload unavailable'); return; }
    const payload = JSON.parse(result.text);
    let info = { shell: 'electron holster', statusPath: result.path };
    if (window.aiDeskMeter.appInfo) {
      try { info = { ...info, ...(await window.aiDeskMeter.appInfo()) }; } catch (_error) {}
    }
    setPayload(payload, 'native app holster', info);
  } catch (error) {
    handleRuntimeUnavailable(String(error));
  } finally { refreshInFlight = false; }
}
async function openRuntimeDashboard(){
  if (window.aiDeskMeter?.openRuntimeDashboard) {
    const result = await window.aiDeskMeter.openRuntimeDashboard();
    if (!result.ok) setDisconnected(`dashboard open failed: ${result.error}`);
    return;
  }
  window.location.href = RUNTIME_DASHBOARD_URL;
}
async function openDiySpecPage(){
  if (window.aiDeskMeter?.openDiySpecPage) {
    const result = await window.aiDeskMeter.openDiySpecPage();
    if (!result.ok) setDisconnected(`DIY spec open failed: ${result.error}`);
    return;
  }
  window.location.href = '/DIY_Claude_Code_Desk_Usage_Meter_Spec_Guide.html#bom';
}
async function openPartsSourcingPage(){
  if (window.aiDeskMeter?.openPartsSourcingPage) {
    const result = await window.aiDeskMeter.openPartsSourcingPage();
    if (!result.ok) setDisconnected(`parts sourcing open failed: ${result.error}`);
    return;
  }
  window.location.href = '/docs/parts-and-sourcing.md';
}
async function openFullDocsPage(){
  if (window.aiDeskMeter?.openDocsPage) {
    const result = await window.aiDeskMeter.openDocsPage();
    if (!result.ok) setDisconnected(`docs open failed: ${result.error}`);
    return;
  }
  window.location.href = '/docs/index.html';
}
function init(){
  if (initialized) return; initialized = true;
  cacheRefs(); renderCommandLists(); setupTabs(); bindBaseButtons(); bindImport();
  refresh(); setInterval(refresh, REFRESH_MS);
}
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
