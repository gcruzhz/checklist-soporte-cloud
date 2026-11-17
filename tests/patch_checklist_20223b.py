#!/usr/bin/env python3
"""Parche 2.2.3b: el modelo gemini-2.5-flash ya no existe para claves nuevas;
se cambia a gemini-3.8-flash, con respaldo en gemini-flash-latest si vuelve a pasar."""
P = '/home/hatch/workspace/android/checklist-cloud/www/index.html'
s = open(P).read()
orig = s

def rep(old, new, n=1):
    global s
    assert old in s, 'NO ENCONTRADO: ' + old[:90]
    s = s.replace(old, new, n)

# ---------- 1. Versión visible ----------
rep('Versión 2.2.2', 'Versión 2.2.3')
rep('Versión: 2.2.2', 'Versión: 2.2.3')
rep('Checklist de Soporte 2.2.2', 'Checklist de Soporte 2.2.3')
rep('Versión de la app: 2.2.2', 'Versión de la app: 2.2.3')

# ---------- 2. Modelo actual + respaldo ----------
rep("var AI_MODEL = 'gemini-2.5-flash';",
"""var AI_MODEL = 'gemini-3.8-flash';
var AI_MODEL_FALLBACK = 'gemini-flash-latest';""")

# ---------- 3. askAI: si el modelo ya no existe, intenta con el alias actual ----------
rep("""  var res;
  try {
    res = await fetch('https://generativelanguage.googleapis.com/v1beta/models/' + AI_MODEL + ':generateContent', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-goog-api-key': aiKey },
      body: JSON.stringify({ contents: [{ parts: parts }], generationConfig: { temperature: 0.4, maxOutputTokens: 600 } })
    });
  } catch (e) {""",
"""  var body = JSON.stringify({ contents: [{ parts: parts }], generationConfig: { temperature: 0.4, maxOutputTokens: 600 } });
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
  } catch (e) {""")

assert s != orig
open(P, 'w').write(s)
print('OK parche 2.2.3b (index.html) aplicado')
print('Quedan "2.2.2":', len(__import__('re').findall(r'2\.2\.2', s)))
print('Quedan "gemini-2.5-flash":', len(__import__('re').findall(r'gemini-2\.5-flash', s)))
