#!/usr/bin/env python3
"""Parche 2.2.5b: DeepSeek como respaldo de la IA.
Gerardo tiene una API de DeepSeek por si Gemini no funciona. Se agrega:
- firebase.js: getDeepseekKey/setDeepseekKey en config/ai (campo deepseekKey).
  OJO: setAiKey ahora usa { merge: true } para no borrar deepseekKey al guardar
  la clave de Gemini, y setDeepseekKey igual para no borrar la de Gemini.
- index.html: panel DeepSeek en Usuarios, askDeepSeek (modelo deepseek-flash,
  con visión, endpoint OpenAI-compatible), askAI usa DeepSeek cuando Gemini
  falla en sus tres modelos (o cuando no hay clave de Gemini), y mensajes de
  error propios de DeepSeek (401 clave, 402 sin saldo, 429 límite, 503 saturado).
Verificado antes: CORS de api.deepseek.com permite Origin https://localhost
(preflight con authorization,content-type) y deepseek-chat/deepseek-reasoner
están retirados desde 2026-07-24; el modelo actual es deepseek-flash."""
import re

def patch(path, pairs):
    s = open(path).read()
    orig = s
    for old, new in pairs:
        assert old in s, 'NO ENCONTRADO en ' + path + ': ' + old[:90]
        s = s.replace(old, new, 1)
    assert s != orig, 'Sin cambios en ' + path
    open(path, 'w').write(s)
    return s

# ---------- firebase.js ----------
fb = patch('/home/hatch/workspace/android/checklist-cloud/www/cloud/firebase.js', [
("""async function setAiKey(key) {
  await setDoc(doc(db, 'config', 'ai'), { key: key || '' });
}""",
"""async function setAiKey(key) {
  await setDoc(doc(db, 'config', 'ai'), { key: key || '' }, { merge: true });
}
// Clave de DeepSeek (respaldo): mismo documento config/ai, otro campo, para
// que guardar una clave no borre la otra. DeepSeek cobra por uso (muy barato).
async function getDeepseekKey() {
  const snap = await getDoc(doc(db, 'config', 'ai'));
  return snap.exists() ? (snap.data().deepseekKey || '') : '';
}
async function setDeepseekKey(key) {
  await setDoc(doc(db, 'config', 'ai'), { deepseekKey: key || '' }, { merge: true });
}"""),
("""  getAiKey,
  setAiKey,""",
"""  getAiKey,
  setAiKey,
  getDeepseekKey,
  setDeepseekKey,"""),
])

# ---------- index.html ----------
idx = patch('/home/hatch/workspace/android/checklist-cloud/www/index.html', [
# 1. Versión visible
('Versión 2.2.4', 'Versión 2.2.5'),
('Versión: 2.2.4', 'Versión: 2.2.5'),
('Checklist de Soporte 2.2.4', 'Checklist de Soporte 2.2.5'),
('Versión de la app: 2.2.4', 'Versión de la app: 2.2.5'),
# 2. Panel DeepSeek en Usuarios (después del bloque de Gemini)
("""      <div class="actions"><button class="btn-green" id="btnAiGuardar">Guardar clave</button><button class="btn-ghost" id="btnAiQuitar">Quitar clave</button></div>""",
"""      <div class="actions"><button class="btn-green" id="btnAiGuardar">Guardar clave</button><button class="btn-ghost" id="btnAiQuitar">Quitar clave</button></div>
      <b>🔷 Inteligencia artificial (DeepSeek, respaldo)</b>
      <div class="share-note">Si Gemini falla, la app usa DeepSeek automáticamente, sin que hagas nada. DeepSeek cobra por uso (muy barato) y necesita saldo en su cuenta.</div>
      <div class="field"><label>Clave de la API de DeepSeek</label><input id="fAiKeyDs" type="password" placeholder="Pega aquí tu clave de DeepSeek"></div>
      <div class="share-note" id="aiKeyDsStatus">Sin clave de DeepSeek guardada.</div>
      <div class="actions"><button class="btn-green" id="btnAiGuardarDs">Guardar clave</button><button class="btn-ghost" id="btnAiQuitarDs">Quitar clave</button></div>"""),
# 3. Variables y carga de claves
("""// Inteligencia artificial (Gemini): la app le pregunta por internet con la
// clave que el admin guarda en Usuarios. Modelo gratis con visión.
var AI_MODEL = 'gemini-3.8-flash';
var AI_MODEL_FALLBACK = 'gemini-flash-latest';
var aiKey = '';""",
"""// Inteligencia artificial: la app le pregunta por internet con la clave que
// el admin guarda en Usuarios. Gemini es gratis; DeepSeek es el respaldo y
// cobra por uso (muy barato). Ambos modelos tienen visión.
var AI_MODEL = 'gemini-3.8-flash';
var AI_MODEL_FALLBACK = 'gemini-flash-latest';
var aiKey = '';
var aiKeyDs = '';"""),
("""async function loadAiKey() {
  if (!CLOUD_ENABLED || !cloudUser || !window.Cloud || !window.Cloud.getAiKey) return;
  try { aiKey = await window.Cloud.getAiKey() || ''; } catch (e) { aiKey = ''; }
}
function refreshAiStatus() {
  var el = document.getElementById('aiKeyStatus');
  if (el) el.textContent = aiKey ? 'Clave guardada ✓ — la IA ya funciona en todos los teléfonos.' : 'Sin clave guardada: la IA no funciona hasta que guardes una.';
}""",
"""async function loadAiKey() {
  if (!CLOUD_ENABLED || !cloudUser || !window.Cloud || !window.Cloud.getAiKey) return;
  try { aiKey = await window.Cloud.getAiKey() || ''; } catch (e) { aiKey = ''; }
  try { if (window.Cloud.getDeepseekKey) aiKeyDs = await window.Cloud.getDeepseekKey() || ''; } catch (e) { aiKeyDs = ''; }
}
function refreshAiStatus() {
  var el = document.getElementById('aiKeyStatus');
  if (el) el.textContent = aiKey ? 'Clave guardada ✓ — la IA ya funciona en todos los teléfonos.' : 'Sin clave guardada: la IA no funciona hasta que guardes una.';
  var elDs = document.getElementById('aiKeyDsStatus');
  if (elDs) elDs.textContent = aiKeyDs ? 'Clave de DeepSeek guardada ✓ — entra si Gemini falla.' : 'Sin clave de DeepSeek guardada.';
}"""),
# 4. askAI con respaldo DeepSeek + askDeepSeek
("""async function askAI(prompt, imageDataUrl, retry) {
  if (!aiKey) { var e0 = new Error('no-key'); throw e0; }
  var parts = [{ text: prompt }];
  if (imageDataUrl) {
    var m = /^data:(image\\/[a-z]+);base64,(.*)$/.exec(imageDataUrl || '');
    if (m) parts.push({ inline_data: { mime_type: m[1], data: m[2] } });
  }
  var body = JSON.stringify({ contents: [{ parts: parts }], generationConfig: { temperature: 0.4, maxOutputTokens: 600 } });""",
"""async function askAI(prompt, imageDataUrl, retry) {
  if (!aiKey && !aiKeyDs) { var e0 = new Error('no-key'); throw e0; }
  if (!aiKey) return askDeepSeek(prompt, imageDataUrl, retry);
  var parts = [{ text: prompt }];
  if (imageDataUrl) {
    var m = /^data:(image\\/[a-z]+);base64,(.*)$/.exec(imageDataUrl || '');
    if (m) parts.push({ inline_data: { mime_type: m[1], data: m[2] } });
  }
  var body = JSON.stringify({ contents: [{ parts: parts }], generationConfig: { temperature: 0.4, maxOutputTokens: 600 } });"""),
("""    // Solo vale la pena probar otro modelo si el error es de modelo no disponible,
    // saturado o límite de uso; con clave no válida o permisos no se reintenta.
    if (res.status !== 404 && res.status !== 503 && res.status !== 429) break;
  }
  throw lastErr;
}""",
"""    // Solo vale la pena probar otro modelo si el error es de modelo no disponible,
    // saturado o límite de uso; con clave no válida o permisos no se reintenta.
    if (res.status !== 404 && res.status !== 503 && res.status !== 429) break;
  }
  // Gemini falló en todos sus modelos: si hay clave de DeepSeek, se usa el respaldo.
  if (aiKeyDs) return askDeepSeek(prompt, imageDataUrl, retry);
  throw lastErr;
}
// Respaldo con DeepSeek (modelo deepseek-flash, con visión): se usa solo cuando
// Gemini no responde. La clave la guarda el admin en Usuarios.
async function askDeepSeek(prompt, imageDataUrl, retry) {
  var content = prompt;
  if (imageDataUrl) content = [{ type: 'text', text: prompt }, { type: 'image_url', image_url: { url: imageDataUrl } }];
  var res;
  try {
    res = await fetch('https://api.deepseek.com/chat/completions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + aiKeyDs },
      body: JSON.stringify({ model: 'deepseek-flash', messages: [{ role: 'user', content: content }], temperature: 0.4, max_tokens: 600 })
    });
  } catch (e) {
    if (!retry) { await new Promise(function (r) { setTimeout(r, 1500); }); return askDeepSeek(prompt, imageDataUrl, true); }
    throw e;
  }
  if (!res.ok) {
    var msg = '';
    try { var d = await res.json(); if (d && d.error && d.error.message) msg = d.error.message; } catch (e2) {}
    var e1 = new Error('deepseek-http-' + res.status + (msg ? ': ' + msg : ''));
    e1.status = res.status; e1.apiMessage = msg; e1.provider = 'deepseek';
    throw e1;
  }
  var data = await res.json();
  var txt = data && data.choices && data.choices[0] && data.choices[0].message && data.choices[0].message.content;
  return (txt || '').trim();
}"""),
# 5. Mensajes de error de DeepSeek (antes de los de Gemini)
("""function aiErrorText(e) {
  if (e && e.message === 'no-key') return 'Falta la clave de la IA. El administrador la pone en Usuarios → Inteligencia artificial.';""",
"""function aiErrorText(e) {
  if (e && e.message === 'no-key') return 'Falta la clave de la IA. El administrador la pone en Usuarios → Inteligencia artificial.';
  if (e && e.provider === 'deepseek') {
    if (e.status === 401) return 'La clave de DeepSeek no es válida. Revisa la clave en Usuarios → Inteligencia artificial.';
    if (e.status === 402) return 'La cuenta de DeepSeek no tiene saldo. Recarga en platform.deepseek.com.';
    if (e.status === 429) return 'DeepSeek está ocupado (límite de uso). Inténtalo más tarde.';
    if (e.status === 503) return 'DeepSeek está saturado en este momento. Inténtalo de nuevo en un rato.';
    if (e.status) return 'DeepSeek respondió con error (código ' + e.status + ').' + (e.apiMessage ? ' ' + e.apiMessage : '');
    return 'No se pudo preguntar a DeepSeek. Revisa tu conexión.';
  }"""),
# 6. Botones de DeepSeek (después del handler de Quitar clave de Gemini)
("""document.getElementById('btnAiQuitar').addEventListener('click', function () {
  if (!confirm('¿Quitar la clave de la IA? La IA dejará de funcionar en todos los teléfonos.')) return;
  window.Cloud.setAiKey('').then(function () { aiKey = ''; refreshAiStatus(); }).catch(function () { alert('No se pudo quitar la clave. Revisa tu conexión.'); });
});""",
"""document.getElementById('btnAiQuitar').addEventListener('click', function () {
  if (!confirm('¿Quitar la clave de la IA? La IA dejará de funcionar en todos los teléfonos.')) return;
  window.Cloud.setAiKey('').then(function () { aiKey = ''; refreshAiStatus(); }).catch(function () { alert('No se pudo quitar la clave. Revisa tu conexión.'); });
});
document.getElementById('btnAiGuardarDs').addEventListener('click', function () {
  var k = document.getElementById('fAiKeyDs').value.trim();
  if (!k) { alert('Pega primero tu clave de DeepSeek.'); return; }
  window.Cloud.setDeepseekKey(k).then(function () { aiKeyDs = k; document.getElementById('fAiKeyDs').value = ''; refreshAiStatus(); }).catch(function () { alert('No se pudo guardar la clave. Revisa tu conexión.'); });
});
document.getElementById('btnAiQuitarDs').addEventListener('click', function () {
  if (!confirm('¿Quitar la clave de DeepSeek? Si Gemini falla, la IA dejará de tener respaldo.')) return;
  window.Cloud.setDeepseekKey('').then(function () { aiKeyDs = ''; refreshAiStatus(); }).catch(function () { alert('No se pudo quitar la clave. Revisa tu conexión.'); });
});"""),
])

print('OK parche 2.2.5b aplicado')
print('Quedan "2.2.4":', len(re.findall(r'2\.2\.4', idx)))
print('deepseek-flash en index:', idx.count('deepseek-flash'), '| askDeepSeek:', idx.count('askDeepSeek'), '| getDeepseekKey en fb:', fb.count('getDeepseekKey'), '| merge en fb:', fb.count('merge: true'))
