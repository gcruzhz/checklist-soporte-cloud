#!/usr/bin/env python3
"""Parche 2.2.0b: IA (Gemini) — qué falta, daños en foto y resumen de WhatsApp."""
P = '/home/hatch/workspace/android/checklist-cloud/www/index.html'
s = open(P).read()
orig = s

def rep(old, new, n=1):
    global s
    assert old in s, 'NO ENCONTRADO: ' + old[:90]
    s = s.replace(old, new, n)

# ---------- 1. Versión visible ----------
rep('Versión 2.1.3', 'Versión 2.2.0')
rep('Versión: 2.1.3', 'Versión: 2.2.0')
rep('Checklist de Soporte 2.1.3', 'Checklist de Soporte 2.2.0')
rep('Versión de la app: 2.1.3', 'Versión de la app: 2.2.0')

# ---------- 2. Estilo para la respuesta de la IA ----------
rep("  .share-note { font-size: 12px; color: #777; margin-top: 8px; }",
"""  .share-note { font-size: 12px; color: #777; margin-top: 8px; }
  .ai-answer { background: #eef6f0; border-left: 3px solid #2e7d32; border-radius: 8px; padding: 10px; margin-top: 10px; font-size: 13px; white-space: pre-wrap; }""")

# ---------- 3. Funciones de IA después de cloudUpsert ----------
rep("""function cloudUpsert(rec) {
  if (!CLOUD_ENABLED || !cloudUser || !window.Cloud) return;
  window.Cloud.upsertRenta(rentaToCloudDoc(rec)).catch(function (e) { console.warn('No se pudo guardar en la nube', e); });
}""",
"""function cloudUpsert(rec) {
  if (!CLOUD_ENABLED || !cloudUser || !window.Cloud) return;
  window.Cloud.upsertRenta(rentaToCloudDoc(rec)).catch(function (e) { console.warn('No se pudo guardar en la nube', e); });
}

// Inteligencia artificial (Gemini): la app le pregunta por internet con la
// clave que el admin guarda en Usuarios. Modelo gratis con visión.
var AI_MODEL = 'gemini-2.5-flash';
var aiKey = '';
var aiBusy = false;
var aiAnswers = {};
async function loadAiKey() {
  if (!CLOUD_ENABLED || !cloudUser || !window.Cloud || !window.Cloud.getAiKey) return;
  try { aiKey = await window.Cloud.getAiKey() || ''; } catch (e) { aiKey = ''; }
}
function refreshAiStatus() {
  var el = document.getElementById('aiKeyStatus');
  if (el) el.textContent = aiKey ? 'Clave guardada ✓ — la IA ya funciona en todos los teléfonos.' : 'Sin clave guardada: la IA no funciona hasta que guardes una.';
}
async function askAI(prompt, imageDataUrl) {
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
  if (!res.ok) { var e1 = new Error('ai-http-' + res.status); e1.status = res.status; throw e1; }
  var data = await res.json();
  var txt = data && data.candidates && data.candidates[0] && data.candidates[0].content && data.candidates[0].content.parts && data.candidates[0].content.parts[0] && data.candidates[0].content.parts[0].text;
  return (txt || '').trim();
}
function aiErrorText(e) {
  if (e && e.message === 'no-key') return 'Falta la clave de la IA. El administrador la pone en Usuarios → Inteligencia artificial.';
  if (e && e.status === 400) return 'La clave de la IA no es válida. Revisa la clave en Usuarios → Inteligencia artificial.';
  if (e && e.status === 429) return 'La IA está ocupada (límite gratis del día). Inténtalo más tarde.';
  return 'No se pudo preguntar a la IA. Revisa tu conexión.';
}
function faltaPrompt(p) {
  var items = requiredItems(p);
  var pend = items.filter(function (it) { return !p.checks[it.id]; }).map(function (it) { return it.text; });
  var opts = allItems(p).filter(function (it) { return it.optional && !p.checks[it.id]; }).map(function (it) { return it.text; });
  return 'Eres el asistente de un técnico de soporte. Este equipo está en preparación: ' +
    (p.equipo.tipo || 'equipo') + ' ' + (p.equipo.marca || '') + ' ' + (p.equipo.modelo || '') +
    ', usuario: ' + (p.usuario.nombre || 'sin asignar') + ', analista: ' + (p.tecnico || '—') +
    '. Avance: ' + progress(p) + '%. ' +
    (pend.length ? 'Puntos obligatorios pendientes: ' + pend.join('; ') + '. ' : 'No hay puntos obligatorios pendientes. ') +
    (opts.length ? 'Puntos opcionales pendientes: ' + opts.join('; ') + '. ' : '') +
    'Responde en español, en lista corta, qué falta para dejar el equipo listo para entregar y en qué orden conviene hacerlo. Si ya está listo, dilo en una línea.';
}
function danosPrompt(rec) {
  return 'Revisa esta foto de un equipo de renta (' + (rec.tipo || 'equipo') + ' ' + (rec.modelo || '') + ') que se acaba de recibir. Describe en español, en lista corta, los daños visibles: rayones, golpes, abolladuras, pantalla rota, teclas faltantes, puertos dañados. Si no se ve ningún daño, dilo en una línea. No inventes daños que no se vean.';
}
function waSummaryPrompt(p) {
  return 'Escribe un mensaje corto y amable de WhatsApp en español para avisar que este equipo ya está listo y entregado. Usa estos datos y nada más: ' + waTextOne(p).split('\\n').join(' | ') + ' Empieza con un saludo, pon los datos importantes (equipo, usuario, analista y fecha de entrega) y termina ofreciendo ayuda si algo falla. Máximo 8 líneas, sin inventar datos.';
}""")

# ---------- 4. La clave se lee al entrar ----------
rep("""    startEquipo();
    render();
    _authReady = true;""",
"""    startEquipo();
    render();
    loadAiKey();
    _authReady = true;""")

# ---------- 5. Compartir texto (lo usa WhatsApp normal y el resumen con IA) ----------
rep("""function shareWhatsApp(preps) {
  if (!preps.length) { alert('No hay equipos para compartir.'); return; }
  var texto = preps.length === 1 ? waTextOne(preps[0]) : waTextAll(preps);
  if (navigator.share) {
    navigator.share({ title: 'Checklist de Soporte', text: texto }).catch(function () {});
    return;
  }
  window.open('https://wa.me/?text=' + encodeURIComponent(texto), '_blank');
}""",
"""function shareText(texto) {
  if (navigator.share) {
    navigator.share({ title: 'Checklist de Soporte', text: texto }).catch(function () {});
    return;
  }
  window.open('https://wa.me/?text=' + encodeURIComponent(texto), '_blank');
}
function shareWhatsApp(preps) {
  if (!preps.length) { alert('No hay equipos para compartir.'); return; }
  shareText(preps.length === 1 ? waTextOne(preps[0]) : waTextAll(preps));
}""")

# ---------- 6. Botones de IA en la tarjeta de Por preparar + respuesta ----------
rep("""  if (st === 'entregado') {
    actions += '<button class="btn-ghost" data-xlsx="' + p.id + '">Exportar a Excel</button>';
    actions += '<button class="btn-ghost" data-wa="' + p.id + '">Enviar datos por WhatsApp</button>';
    actions += '<button class="btn-ghost" data-mail="' + p.id + '">Enviar por correo</button>';
  }""",
"""  if (st !== 'entregado') actions += '<button class="btn-ghost" data-ai-falta="' + p.id + '">✨ ¿Qué falta?</button>';
  if (st === 'entregado') {
    actions += '<button class="btn-ghost" data-xlsx="' + p.id + '">Exportar a Excel</button>';
    actions += '<button class="btn-ghost" data-wa="' + p.id + '">Enviar datos por WhatsApp</button>';
    actions += '<button class="btn-ghost" data-ai-wa="' + p.id + '">✨ Resumen con IA</button>';
    actions += '<button class="btn-ghost" data-mail="' + p.id + '">Enviar por correo</button>';
  }""")
rep("""    groupsHtml + extraForm + reassignForm +
    '<div class="actions">' + actions + '</div>' +
    '</div>';""",
"""    groupsHtml + extraForm + reassignForm +
    (aiAnswers[p.id] ? '<div class="ai-answer">🤖 ' + esc(aiAnswers[p.id]) + '</div>' : '') +
    '<div class="actions">' + actions + '</div>' +
    '</div>';""")

# ---------- 7. Handlers de IA en el click de Por preparar ----------
rep("""  if (t.hasAttribute('data-wa') && prep) { shareWhatsApp([prep]); return; }""",
"""  if (t.hasAttribute('data-wa') && prep) { shareWhatsApp([prep]); return; }
  if (t.hasAttribute('data-ai-falta') && prep) {
    if (aiBusy) return;
    if (!aiKey) { alert(aiErrorText({ message: 'no-key' })); return; }
    aiBusy = true;
    aiAnswers[prep.id] = 'Pensando...';
    render();
    askAI(faltaPrompt(prep)).then(function (txt) { aiAnswers[prep.id] = txt || 'La IA no devolvió respuesta.'; render(); }).catch(function (e) { aiAnswers[prep.id] = aiErrorText(e); render(); }).then(function () { aiBusy = false; });
    return;
  }
  if (t.hasAttribute('data-ai-wa') && prep) {
    if (aiBusy) return;
    if (!aiKey) { alert(aiErrorText({ message: 'no-key' })); return; }
    aiBusy = true;
    askAI(waSummaryPrompt(prep)).then(function (txt) { if (txt) shareText(txt); }).catch(function (e) { alert(aiErrorText(e)); }).then(function () { aiBusy = false; });
    return;
  }""")

# ---------- 8. Foto de daños en el formulario de Recibir renta ----------
rep("""        <div class="field full"><label>Detalle de daños (si tiene)</label><input id="fR-rec-danos" placeholder="Rayón en tapa, tecla faltante..."></div>""",
"""        <div class="field full"><label>Detalle de daños (si tiene)</label><input id="fR-rec-danos" placeholder="Rayón en tapa, tecla faltante..."></div>
        <div class="field full"><label>Foto para revisar daños con IA</label><button type="button" class="btn-ghost" id="btnFotoDanos" style="width:100%">📷 Tomar foto / elegir imagen</button><input type="file" id="fFotoDanos" accept="image/*" capture="environment" hidden><div class="foto-preview" id="fotoDanosPreview"></div></div>""")

# ---------- 9. Captura de la foto de daños (mismo patrón que la foto de serie) ----------
rep("""// Lee el numero de serie del texto que devuelve el OCR.""",
"""// Foto de daños de renta: camara o galeria, reducida a max 800 px.
window._fotoDanos = null;
document.getElementById('btnFotoDanos').addEventListener('click', function () {
  document.getElementById('fFotoDanos').click();
});
document.getElementById('fFotoDanos').addEventListener('change', function (e) {
  var file = e.target.files && e.target.files[0];
  if (!file) return;
  var reader = new FileReader();
  reader.onload = function (ev) {
    var img = new Image();
    img.onload = function () {
      var max = 800, w = img.width, h = img.height;
      if (w > max || h > max) {
        var k = Math.min(max / w, max / h);
        w = Math.round(w * k); h = Math.round(h * k);
      }
      var cv = document.createElement('canvas');
      cv.width = w; cv.height = h;
      cv.getContext('2d').drawImage(img, 0, 0, w, h);
      window._fotoDanos = cv.toDataURL('image/jpeg', 0.75);
      document.getElementById('fotoDanosPreview').innerHTML =
        '<img src="' + window._fotoDanos + '" alt="Foto de daños">' +
        '<button type="button" class="btn-ghost" id="btnQuitarFotoDanos" style="margin-top:6px">Quitar foto</button>';
      document.getElementById('btnQuitarFotoDanos').addEventListener('click', function () {
        window._fotoDanos = null;
        document.getElementById('fotoDanosPreview').innerHTML = '';
        document.getElementById('fFotoDanos').value = '';
      });
    };
    img.src = ev.target.result;
  };
  reader.readAsDataURL(file);
});

// Lee el numero de serie del texto que devuelve el OCR.""")

# ---------- 10. saveRenta guarda la foto y el resultado de la IA ----------
rep("""    accesorios: accs, sinDanos: document.getElementById('fR-' + flow + '-sindanos').checked,
    danos: g('fR-' + flow + '-danos'), obs: g('fR-' + flow + '-obs'),""",
"""    accesorios: accs, sinDanos: document.getElementById('fR-' + flow + '-sindanos').checked,
    danos: g('fR-' + flow + '-danos'), obs: g('fR-' + flow + '-obs'),
    fotoDanos: flow === 'rec' ? (window._fotoDanos || null) : null, danosIA: '',""")
rep("""  ['modelo', 'inv', 'cap', 'cpu', 'danos', 'obs'].forEach(function (f) { document.getElementById('fR-' + flow + '-' + f).value = ''; });""",
"""  ['modelo', 'inv', 'cap', 'cpu', 'danos', 'obs'].forEach(function (f) { document.getElementById('fR-' + flow + '-' + f).value = ''; });
  if (flow === 'rec') { window._fotoDanos = null; document.getElementById('fotoDanosPreview').innerHTML = ''; document.getElementById('fFotoDanos').value = ''; }""")

# ---------- 11. La foto y el resultado viajan a la nube (foto máx. 700 KB) ----------
rep("""    obs: rec.obs || '', estado: rec.estado || 'recibido',""",
"""    obs: rec.obs || '', estado: rec.estado || 'recibido',
    fotoDanos: (rec.fotoDanos && rec.fotoDanos.length <= 700000) ? rec.fotoDanos : '', danosIA: rec.danosIA || '',""")

# ---------- 12. La tarjeta de renta muestra foto, resultado de la IA y el botón ----------
rep("""    (rec.obs ? '<div class="sub">Obs: ' + esc(rec.obs) + '</div>' : '') +""",
"""    (rec.obs ? '<div class="sub">Obs: ' + esc(rec.obs) + '</div>' : '') +
    (rec.fotoDanos ? '<img class="foto-serie" src="' + rec.fotoDanos + '" alt="Foto de daños">' : '') +
    (rec.danosIA ? '<div class="sub">🤖 Daños según la IA: ' + esc(rec.danosIA) + '</div>' : '') +
    (aiAnswers['renta-' + rec.id] ? '<div class="ai-answer">🤖 ' + esc(aiAnswers['renta-' + rec.id]) + '</div>' : '') +""")
rep("""      : '<button class="btn-green" data-renta-next="' + rec.id + '" data-flow="' + flow + '">' + rentaNextLabel(flow, rec.estado) + '</button>') +""",
"""      : '<button class="btn-green" data-renta-next="' + rec.id + '" data-flow="' + flow + '">' + rentaNextLabel(flow, rec.estado) + '</button>' +
      (flow === 'rec' && rec.fotoDanos ? '<button class="btn-ghost" data-ai-danos="' + rec.id + '">🔍 Revisar daños con IA</button>' : '')) +""")

# ---------- 13. Handler de daños con IA en Recibir renta ----------
rep("""  var id = q('data-renta-next') || q('data-renta-del');
  if (!id) return;
  var rec = state.renta.find(function (r) { return r.id === id; });
  if (!rec) return;
  if (t.hasAttribute('data-renta-next')) { rec.estado = rentaNext('rec', rec.estado); cloudUpsert(rec); save(); render(); return; }""",
"""  var id = q('data-renta-next') || q('data-renta-del') || q('data-ai-danos');
  if (!id) return;
  var rec = state.renta.find(function (r) { return r.id === id; });
  if (!rec) return;
  if (t.hasAttribute('data-ai-danos')) {
    if (aiBusy) return;
    if (!aiKey) { alert(aiErrorText({ message: 'no-key' })); return; }
    if (!rec.fotoDanos) { alert('Este equipo no tiene foto para revisar.'); return; }
    aiBusy = true;
    aiAnswers['renta-' + rec.id] = 'Revisando la foto...';
    render();
    askAI(danosPrompt(rec), rec.fotoDanos).then(function (txt) { rec.danosIA = txt || 'La IA no devolvió respuesta.'; delete aiAnswers['renta-' + rec.id]; cloudUpsert(rec); save(); render(); }).catch(function (e) { aiAnswers['renta-' + rec.id] = aiErrorText(e); render(); }).then(function () { aiBusy = false; });
    return;
  }
  if (t.hasAttribute('data-renta-next')) { rec.estado = rentaNext('rec', rec.estado); cloudUpsert(rec); save(); render(); return; }""")

# ---------- 14. Panel de la clave de IA en Usuarios (solo admin) ----------
rep("""    <div class="panel">
      <div class="grid2">
        <div class="field"><label>Nombre</label><input id="newUserNombre" placeholder="Nombre del usuario"></div>""",
"""    <div class="panel">
      <b>🤖 Inteligencia artificial (Gemini)</b>
      <div class="share-note">La IA responde qué falta en cada equipo, revisa las fotos de daños y escribe el resumen de WhatsApp. La clave es gratis: se crea en Google AI Studio.</div>
      <div class="field"><label>Clave de la API de Gemini</label><input id="fAiKey" type="password" placeholder="Pega aquí tu clave de Google AI Studio"></div>
      <div class="share-note" id="aiKeyStatus">Sin clave guardada: la IA no funciona hasta que guardes una.</div>
      <div class="actions"><button class="btn-green" id="btnAiGuardar">Guardar clave</button><button class="btn-ghost" id="btnAiQuitar">Quitar clave</button></div>
    </div>
    <div class="panel">
      <div class="grid2">
        <div class="field"><label>Nombre</label><input id="newUserNombre" placeholder="Nombre del usuario"></div>""")

# ---------- 15. Guardar / quitar la clave + estado al listar usuarios ----------
rep("""document.getElementById('btnUserAdd').addEventListener('click', function () {""",
"""document.getElementById('btnAiGuardar').addEventListener('click', function () {
  var k = document.getElementById('fAiKey').value.trim();
  if (!k) { alert('Pega primero tu clave de Google AI Studio.'); return; }
  window.Cloud.setAiKey(k).then(function () { aiKey = k; document.getElementById('fAiKey').value = ''; refreshAiStatus(); }).catch(function () { alert('No se pudo guardar la clave. Revisa tu conexión.'); });
});
document.getElementById('btnAiQuitar').addEventListener('click', function () {
  if (!confirm('¿Quitar la clave de la IA? La IA dejará de funcionar en todos los teléfonos.')) return;
  window.Cloud.setAiKey('').then(function () { aiKey = ''; refreshAiStatus(); }).catch(function () { alert('No se pudo quitar la clave. Revisa tu conexión.'); });
});
document.getElementById('btnUserAdd').addEventListener('click', function () {""")
rep("""    box.innerHTML = users.map(function (u) {""",
"""    loadAiKey().then(refreshAiStatus);
    refreshAiStatus();
    box.innerHTML = users.map(function (u) {""")

assert s != orig
open(P, 'w').write(s)
print('OK parche 2.2.0b (index.html) aplicado')
print('Quedan "2.1.3":', len(__import__('re').findall(r'2\.1\.3', s)))
