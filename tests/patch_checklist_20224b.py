#!/usr/bin/env python3
"""Parche 2.2.4b (corregido): el modelo 3.8-flash responde 503 (saturado) con la clave
de Gerardo; askAI ahora prueba en cadena 3.8-flash -> 3.5-flash-lite -> flash-latest
cuando el error es 404, 503 o 429, y el mensaje de 503 dice que la IA está saturada.
OJO: el bloque viejo se tomó del archivo real (la forma del error es e1/ai-http-...,
no err/AI request failed)."""
P = '/home/hatch/workspace/android/checklist-cloud/www/index.html'
s = open(P).read()
orig = s

def rep(old, new, n=1):
    global s
    assert old in s, 'NO ENCONTRADO: ' + old[:90]
    s = s.replace(old, new, n)

# ---------- 1. Versión visible ----------
rep('Versión 2.2.3', 'Versión 2.2.4')
rep('Versión: 2.2.3', 'Versión: 2.2.4')
rep('Checklist de Soporte 2.2.3', 'Checklist de Soporte 2.2.4')
rep('Versión de la app: 2.2.3', 'Versión de la app: 2.2.4')

# ---------- 2. askAI: cadena de modelos ante 404, 503 o 429 ----------
old_askai = """  var body = JSON.stringify({ contents: [{ parts: parts }], generationConfig: { temperature: 0.4, maxOutputTokens: 600 } });
  var res;
  try {
    res = await fetch('https://generativelanguage.googleapis.com/v1beta/models/' + AI_MODEL + ':generateContent', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-goog-api-key': aiKey },
      body: body
    });
    // Si Google retiró el modelo, se intenta con el alias del modelo actual.
    if (res.status === 404) {
      res = await fetch('https://generativelanguage.googleapis.com/v1beta/models/' + AI_MODEL_FALLBACK + ':generateContent', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'x-goog-api-key': aiKey },
        body: body
      });
    }
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
  }
  var data = await res.json();
  var txt = data && data.candidates && data.candidates[0] && data.candidates[0].content && data.candidates[0].content.parts && data.candidates[0].content.parts[0] && data.candidates[0].content.parts[0].text;
  return (txt || '').trim();"""
new_askai = """  var body = JSON.stringify({ contents: [{ parts: parts }], generationConfig: { temperature: 0.4, maxOutputTokens: 600 } });
  // Se prueba en cadena: si un modelo no existe, está saturado o llegó a su límite,
  // se intenta con el siguiente (cada modelo tiene su propio cupo gratis).
  var models = [AI_MODEL, 'gemini-3.5-flash-lite', AI_MODEL_FALLBACK];
  var lastErr = null;
  for (var mi = 0; mi < models.length; mi++) {
    var res;
    try {
      res = await fetch('https://generativelanguage.googleapis.com/v1beta/models/' + models[mi] + ':generateContent', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'x-goog-api-key': aiKey },
        body: body
      });
    } catch (e) {
      // La red falló (señal, Wi-Fi): se reintenta una vez antes de avisar.
      if (!retry) { await new Promise(function (r) { setTimeout(r, 1500); }); return askAI(prompt, imageDataUrl, true); }
      throw e;
    }
    if (res.ok) {
      var data = await res.json();
      var txt = data && data.candidates && data.candidates[0] && data.candidates[0].content && data.candidates[0].content.parts && data.candidates[0].content.parts[0] && data.candidates[0].content.parts[0].text;
      return (txt || '').trim();
    }
    var msg = '';
    try { var d = await res.json(); if (d && d.error && d.error.message) msg = d.error.message; } catch (e2) {}
    var e1 = new Error('ai-http-' + res.status + (msg ? ': ' + msg : ''));
    e1.status = res.status; e1.apiMessage = msg;
    lastErr = e1;
    // Solo vale la pena probar otro modelo si el error es de modelo no disponible,
    // saturado o límite de uso; con clave no válida o permisos no se reintenta.
    if (res.status !== 404 && res.status !== 503 && res.status !== 429) break;
  }
  throw lastErr;"""
rep(old_askai, new_askai)

# ---------- 3. Mensaje claro para 503 ----------
rep("""  if (e && e.status === 404) return 'El modelo de IA no está disponible en este momento.';""",
"""  if (e && e.status === 404) return 'El modelo de IA no está disponible en este momento.';
  if (e && e.status === 503) return 'La IA está saturada en este momento. Inténtalo de nuevo en un rato.';""")

assert s != orig
open(P, 'w').write(s)
print('OK parche 2.2.4b (index.html) aplicado')
print('Quedan "2.2.3":', len(__import__('re').findall(r'2\.2\.3', s)))
print('Tiene cadena de modelos:', 'gemini-3.5-flash-lite' in s, '| mensaje 503:', 'saturada en este momento' in s)
