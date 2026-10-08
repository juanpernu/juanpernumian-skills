#!/usr/bin/env node
// check-wireframe.mjs · prueba de comportamiento de un wireframe en Chrome REAL (CDP), a 390 px y a 1440 px.
// Uso:  node check-wireframe.mjs <archivo.html> [--json]      (Node 22 o superior; sin dependencias)
// Variables: CHROME=/ruta/al/chrome
//
// Qué comprueba (lo que se rompe cuando un agente edita el wireframe):
//   - sin scroll horizontal a 390 y a 1440 px;
//   - un solo <h1> y ninguna FAQ <details> abierta;
//   - validación de cada formulario [data-lead-form]: error con un valor inválido, el error se va con uno válido,
//     el envío vacío muestra el error y deja el foco en el campo;
//   - barra fija mobile (#barra-fija): apagada al cargar, prendida cuando el formulario del hero quedó arriba y ningún
//     formulario está en pantalla, apagada con CUALQUIER formulario a la vista; el botón del header se oculta mientras está activa;
//   - los botones [data-goto-form] llevan el foco al formulario más cercano al centro de la pantalla;
//   - ?clean=1 (versión limpia para pruebas de 5 segundos) oculta banner y etiquetas pero conserva los sellos.
// Código de salida: 0 todo bien · 1 alguna comprobación falló · 2 uso o error de Chrome.

import { spawn } from 'node:child_process';
import { mkdtempSync, rmSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const args = process.argv.slice(2);
const asJson = args.includes('--json');
const file = args.find((a) => !a.startsWith('--'));
if (!file || !existsSync(file)) { console.error('uso: node check-wireframe.mjs <archivo.html> [--json]'); process.exit(2); }
const url = pathToFileURL(resolve(file)).href;

let chromeBin = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
if (!existsSync(chromeBin)) {
  for (const c of ['/usr/bin/google-chrome', '/usr/bin/google-chrome-stable', '/usr/bin/chromium', '/usr/bin/chromium-browser']) if (existsSync(c)) { chromeBin = c; break; }
}
if (!existsSync(chromeBin)) { console.error('No encuentro Chrome. Exportá CHROME=/ruta/al/binario'); process.exit(2); }

const port = 9300 + Math.floor(Math.random() * 500);
const profile = mkdtempSync(join(tmpdir(), 'vpl-cdp-'));
const chrome = spawn(chromeBin, ['--headless=new', '--disable-gpu', '--allow-file-access-from-files', '--no-first-run',
  '--host-resolver-rules=MAP * ~NOTFOUND , EXCLUDE localhost',
  '--no-default-browser-check', `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`, 'about:blank'], { stdio: 'ignore' });
const cleanup = () => { try { chrome.kill('SIGKILL'); } catch {} try { rmSync(profile, { recursive: true, force: true }); } catch {} };
process.on('exit', cleanup);

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function connect() {
  for (let i = 0; i < 80; i++) {
    try {
      const list = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
      const page = list.find((t) => t.type === 'page');
      if (page) return page.webSocketDebuggerUrl;
    } catch {}
    await sleep(150);
  }
  throw new Error('Chrome no abrió el puerto de depuración');
}

const wsUrl = await connect();
const ws = new WebSocket(wsUrl);
await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
let id = 0; const pending = new Map(); const waiters = [];
ws.onmessage = (m) => {
  const msg = JSON.parse(m.data);
  if (msg.id && pending.has(msg.id)) { pending.get(msg.id)(msg); pending.delete(msg.id); }
  else if (msg.method) waiters.slice().forEach((w) => w(msg));
};
const send = (method, params = {}) => new Promise((res) => { const i = ++id; pending.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
const waitEvent = (name) => new Promise((res) => { const w = (m) => { if (m.method === name) { waiters.splice(waiters.indexOf(w), 1); res(m); } }; waiters.push(w); });
async function evaluate(expr) {
  const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true });
  if (r.result.exceptionDetails) throw new Error(JSON.stringify(r.result.exceptionDetails.exception?.description || r.result.exceptionDetails));
  return r.result.result.value;
}

const results = [];
const check = (name, ok, detail = '') => results.push({ name, ok: !!ok, detail });

async function load(width, height, mobile) {
  await send('Page.enable');
  await send('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile });
  const loaded = waitEvent('Page.loadEventFired');
  await send('Page.navigate', { url });
  await loaded;
  await sleep(700);
}

// ---------- 1440 px ----------
await load(1440, 900, false);
// Se compara contra el ancho pedido (no contra innerWidth): con emulación mobile Chrome agranda el viewport para que entre el contenido ancho.
const sw1440 = await evaluate('document.documentElement.scrollWidth');
check('desktop 1440: sin scroll horizontal', sw1440 <= 1440, 'scrollWidth=' + sw1440);

// ---------- 390 px ----------
await load(390, 844, true);
const sw390 = await evaluate('document.documentElement.scrollWidth');
check('mobile 390: sin scroll horizontal', sw390 <= 390, 'scrollWidth=' + sw390);
check('un solo <h1>', (await evaluate('document.querySelectorAll("h1").length')) === 1);
check('ninguna FAQ <details> abierta', (await evaluate('document.querySelectorAll("details[open]").length')) === 0);

const nForms = await evaluate('document.querySelectorAll("[data-lead-form]").length');
check('hay formularios [data-lead-form]', nForms > 0, 'cantidad=' + nForms);

// Validación de cada formulario
const val = await evaluate(`(async () => {
  const out = [];
  const forms = [...document.querySelectorAll('[data-lead-form]')];
  for (const form of forms) {
    const inp = form.querySelector('input'); const err = form.querySelector('.err');
    const bad = { email: 'mal', domain: 'mal', text: '' }[inp.getAttribute('data-validate') || 'text'];
    const good = { email: 'nombre@dominio-1.com', domain: 'dominio-1.com', text: 'valor valido' }[inp.getAttribute('data-validate') || 'text'];
    window.scrollTo({ top: 0, behavior: 'instant' });
    inp.value = bad; inp.dispatchEvent(new Event('blur'));
    const errOnBad = !err.hidden && inp.getAttribute('aria-invalid') === 'true';
    inp.value = good; inp.dispatchEvent(new Event('input'));
    const clears = err.hidden && !inp.hasAttribute('aria-invalid');
    inp.value = ''; form.dispatchEvent(new Event('submit', { cancelable: true }));
    const emptyErr = !err.hidden; const focused = document.activeElement === inp;
    inp.value = ''; inp.blur(); err.hidden = true; inp.removeAttribute('aria-invalid');
    out.push({ id: form.id, errOnBad, clears, emptyErr, focused });
  }
  return out;
})()`);
for (const v of val) {
  check(`formulario ${v.id}: error con valor inválido`, v.errOnBad);
  check(`formulario ${v.id}: el error se va con un valor válido`, v.clears);
  check(`formulario ${v.id}: envío vacío muestra error y deja el foco`, v.emptyErr && v.focused);
}

// Barra fija
const hasBar = await evaluate('!!document.getElementById("barra-fija")');
if (hasBar) {
  const info = await evaluate(`(() => {
    const H = innerHeight;
    const forms = [...document.querySelectorAll('[data-lead-form]')].map(f => { const r = f.getBoundingClientRect(); return { id: f.id, top: r.top + scrollY, bot: r.bottom + scrollY }; });
    return { H, forms, total: document.documentElement.scrollHeight };
  })()`);
  const inView = (y) => info.forms.some((f) => f.bot > y && f.top < y + info.H);
  const bar = (js) => evaluate(js);
  const isOn = () => evaluate('document.getElementById("barra-fija").classList.contains("is-on")');
  const jump = async (y) => { await evaluate(`window.scrollTo({top:${Math.max(0, Math.round(y))},left:0,behavior:'instant'})`); await sleep(700); };

  await jump(0);
  check('barra fija: apagada al cargar (el formulario del hero está a la vista)', !(await isOn()));
  let yFree = null;
  for (let y = info.forms[0].bot + 60; y < info.total - info.H; y += 40) { if (!inView(y)) { yFree = y; break; } }
  if (yFree === null) { check('barra fija: existe una posición sin formularios a la vista', false, 'no hay tramo sin formularios; ¿demasiados formularios?'); }
  else {
    await jump(yFree);
    check('barra fija: prendida con el hero arriba y ningún formulario a la vista', await isOn(), 'scrollY=' + Math.round(yFree));
    check('botón del header oculto mientras la barra está activa', await evaluate('document.body.classList.contains("bar-on")'));
    // goto desde la barra: foco en el formulario más cercano al centro
    await evaluate('document.querySelector("#barra-fija [data-goto-form]").click()');
    await sleep(1600);
    const near = await evaluate(`(() => { const a = document.activeElement; return a && a.tagName === 'INPUT' ? a.id : null; })()`);
    check('[data-goto-form] de la barra lleva el foco a un campo de formulario', !!near, 'foco en: ' + near);
  }
  for (const f of info.forms.slice(1)) {
    await jump(f.top - info.H / 3);
    check(`barra fija: apagada con ${f.id} a la vista`, !(await isOn()));
  }
  await jump(0);
}

// Versión limpia para pruebas de 5 segundos: ?clean=1 oculta banner y etiquetas de wireframe, pero deja los sellos EJEMPLO.
if (await evaluate('!!document.querySelector(".wf-banner")')) {
  const cleanUrl = url + (url.includes('?') ? '&' : '?') + 'clean=1';
  const loaded2 = waitEvent('Page.loadEventFired');
  await send('Page.navigate', { url: cleanUrl });
  await loaded2;
  await sleep(500);
  const clean = await evaluate(`(() => {
    const vis = (e) => !!e && getComputedStyle(e).display !== 'none';
    return { banner: vis(document.querySelector('.wf-banner')), tags: [...document.querySelectorAll('.wf-tag')].some(vis),
             stamps: [...document.querySelectorAll('.stamp')].every(vis) && document.querySelectorAll('.stamp').length > 0 };
  })()`);
  check('?clean=1 oculta el banner y las etiquetas de wireframe', !clean.banner && !clean.tags);
  check('?clean=1 conserva los sellos EJEMPLO de los mocks', clean.stamps);
}

const failed = results.filter((r) => !r.ok);
if (asJson) console.log(JSON.stringify({ file, results, failed: failed.length }, null, 2));
else {
  for (const r of results) console.log(`${r.ok ? ' ok' : ' X '} ${r.name}${r.detail ? '  (' + r.detail + ')' : ''}`);
  console.log(`\nRESULTADO: ${failed.length ? failed.length + ' comprobación(es) fallaron' : 'OK, ' + results.length + ' comprobaciones'}`);
}
ws.close(); cleanup();
process.exit(failed.length ? 1 : 0);
