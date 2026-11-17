#!/usr/bin/env python3
"""Parche 2.2.2b: la IA dice la causa real del error y reintenta si falla la red."""
P = '/home/hatch/workspace/android/checklist-cloud/www/index.html'
s = open(P).read()
orig = s

def rep(old, new, n=1):
    global s
    assert old in s, 'NO ENCONTRADO: ' + old[:90]
    s = s.replace(old, new, n)

# ---------- 1. Versión visible ----------
rep('Versión 2.2.1', 'Versión 2.2.2')
rep('Versión: 2.2.1', 'Versión: 2.2.2')
rep('Checklist de Soporte 2.2.1', 'Checklist de Soporte 2.2.2')
rep('Versión de la app: 2.2.1', 'Versión de la app: 2.2.2')

# ---------- 2. askAI: reintento ante fallo de red y lee el mensaje de error de Google ----------
rep("""async function askAI(prompt, imageDataUrl) {
  if (!aiKey) { var e0 = new Error('no-key'); throw e0; }
  var parts = [{ text: prompt }];
  if (imageDataUrl) {
    var m = /^data:(image\\/[a-z]+);base64,(.*)$/.exec(imageDataUrl || '');
    if (m) parts.push({ inline_data: { mime_type: m[1], data: m[2] } });
  }
  var res = await fetch('https://generativelanguage.googleapis.com/v1beta/models/' + AI_MODEL + ':generateContent', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'x-goog-api-key': aiKey },
    body: JSON.stringify({ contents: [{ parts: parts }], generationConfig: { temperature: 0.4, maxOutputTokens: 600 } })
  });
  if (!res.ok) { var e1 = new Error('ai-http-' + res.status); e1.status = res.status; throw e1; }""",
"""async function askAI(prompt, imageDataUrl, retry) {
  if (!aiKey) { var e0 = new Error('no-key'); throw e0; }
  var parts = [{ text: prompt }];
  if (imageDataUrl) {
    var m = /^data:(image\\/[a-z]+);base64,(.*)$/.exec(imageDataUrl || '');
    if (m) parts.push({ inline_data: { mime_type: m[1], data: m[2] } });
  }
  var res;
  try {
    res = await fetch('https://generativelanguage.googleapis.com/v1beta/models/' + AI_MODEL + ':generateContent', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-goog-api-key': aiKey },
      body: JSON.stringify({ contents: [{ parts: parts }], generationConfig: { temperature: 0.4, maxOutputTokens: 600 } })
    });
  } catch (e) {
    // La red falló (señal, Wi-Fi): se reintenta una vez antes de avisar.
    if (!retry) { await new Promise(function (r) { setTimeout(r, 1500); }); return askAI(prompt, imageDataUrl, true); }
    throw e;
  }
  if (!res.ok) {
    var msg = '';
    try { var d = await res.json(); if (d && d.error && d.error.message) msg = d.error.message; } catch (e2) {}
    var e1 = new Error('ai-http-' + res.status + (msg ? ': ' + msg : ''));
    e1.status = res.status; e1.apiMessage = msg;
    throw e1;
  }""")

# ---------- 3. aiErrorText: cada causa con su mensaje ----------
rep("""function aiErrorText(e) {
  if (e && e.message === 'no-key') return 'Falta la clave de la IA. El administrador la pone en Usuarios → Inteligencia artificial.';
  if (e && e.status === 400) return 'La clave de la IA no es válida. Revisa la clave en Usuarios → Inteligencia artificial.';
  if (e && e.status === 429) return 'La IA está ocupada (límite gratis del día). Inténtalo más tarde.';
  return 'No se pudo preguntar a la IA. Revisa tu conexión.';
}""",
"""function aiErrorText(e) {
  if (e && e.message === 'no-key') return 'Falta la clave de la IA. El administrador la pone en Usuarios → Inteligencia artificial.';
  if (e && e.status === 400) return 'La clave de la IA no es válida. Revisa la clave en Usuarios → Inteligencia artificial.';
  if (e && e.status === 403) return 'Google no dejó usar la IA con esta clave: revisa en Google Cloud que la clave permita la API de Gemini (Generative Language API) y que esa API esté habilitada.';
  if (e && e.status === 404) return 'El modelo de IA no está disponible en este momento.';
  if (e && e.status === 429) return 'La IA está ocupada (límite gratis del día). Inténtalo más tarde.';
  if (e && e.status) return 'La IA respondió con error (código ' + e.status + ').' + (e.apiMessage ? ' ' + e.apiMessage : '');
  return 'No se pudo preguntar a la IA. Revisa tu conexión.';
}""")

assert s != orig
open(P, 'w').write(s)
print('OK parche 2.2.2b (index.html) aplicado')
print('Quedan "2.2.1":', len(__import__('re').findall(r'2\.2\.1', s)))
