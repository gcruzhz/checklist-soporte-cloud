
var LS_KEY = 'checklist-soporte-v1';
var GROUPS = { hardware: 'Equipo y hardware', software: 'Software', datos: 'Datos del usuario' };
var GROUP_ORDER = ['hardware', 'software', 'datos'];

function uid() { return 'id' + Date.now().toString(36) + Math.random().toString(36).slice(2, 7); }

function defaultTemplate() {
  return [
    { id: 't1', group: 'hardware', text: 'Equipo enciende y sin daños físicos' },
    { id: 't2', group: 'hardware', text: 'Teclado, pantalla y puertos funcionando' },
    { id: 't3', group: 'hardware', text: 'Batería y cargador en buen estado' },
    { id: 't4', group: 'hardware', text: 'Etiqueta de inventario y número de serie registrados' },
    { id: 't26', group: 'hardware', text: 'Limpieza física del equipo', reassignOnly: true },
    { id: 't6', group: 'software', text: 'Sistema operativo actualizado' },
    { id: 't7', group: 'software', text: 'Antivirus instalado y actualizado' },
    { id: 't8', group: 'software', text: 'Office instalado y activado', options: ['Office 365', 'LibreOffice'] },
    { id: 't9', group: 'software', text: 'Impresoras configuradas' },
    { id: 't10', group: 'software', text: 'VPN configurada (opcional)', optional: true },
    { id: 't11', group: 'software', text: 'Inicio rápido de Windows desactivado' },
    { id: 't12', group: 'software', text: 'Equipo registrado en Invgate' },
    { id: 't18', group: 'software', text: 'Google Chrome instalado' },
    { id: 't19', group: 'software', text: 'Adobe Reader instalado' },
    { id: 't20', group: 'software', text: 'WinRAR instalado' },
    { id: 't21', group: 'software', text: 'Sistema Lapi Fox configurado (opcional)', optional: true },
    { id: 't22', group: 'software', text: 'Alfaweb configurado' },
    { id: 't23', group: 'software', text: 'Alfaprinter instalado (opcional)', optional: true },
    { id: 't24', group: 'software', text: 'Accesos directos: historia clínica y estudios de gabinete' },
    { id: 't25', group: 'software', text: 'AnyDesk Gris instalado' },
    { id: 't13', group: 'datos', text: 'Cuenta de correo creada' },
    { id: 't15', group: 'datos', text: 'Contraseña inicial entregada al usuario' },
    { id: 't16', group: 'datos', text: 'Archivos y perfil del usuario migrados' },
    { id: 't17', group: 'datos', text: 'Firma de resguardo recabada' }
  ];
}

var state = load();
if (!Array.isArray(state.renta)) state.renta = [];
migrateTemplate();
function migrateTemplate() {
  if (state.templateVersion === 3) return;
  var oldIds = ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12', 't13', 't14', 't15', 't16', 't17', 't18', 't19', 't20', 't21', 't22', 't23', 't24', 't25'];
  var newIds = {};
  defaultTemplate().forEach(function (t) { newIds[t.id] = true; });
  var custom = (state.template || []).filter(function (t) { return oldIds.indexOf(t.id) === -1 && !newIds[t.id]; });
  state.template = defaultTemplate().concat(custom);
  state.templateVersion = 3;
  save();
}
function load() {
  try {
    var raw = localStorage.getItem(LS_KEY);
    if (raw) { var s = JSON.parse(raw); if (s.template && s.preparations) return s; }
  } catch (e) {}
  return { template: defaultTemplate(), preparations: [] };
}
function save() { localStorage.setItem(LS_KEY, JSON.stringify(state)); }

// ---------- Nube (Firebase) ----------
// Con config real: login obligatorio y renta sincronizada. Sin config real
// (PLACEHOLDER): modo local, igual que la 1.8.
var CLOUD_ENABLED = !!(window.FIREBASE_CONFIG && window.FIREBASE_CONFIG.apiKey && window.FIREBASE_CONFIG.apiKey !== 'TU_API_KEY');
var cloudUser = null;
var cloudRole = null;
var sessionPassword = null;
var cloudUnsub = null;
var lastUsers = [];
var MIG_KEY = 'checklist-soporte-migrado-v2';

function rentaToCloudDoc(rec) {
  return {
    id: rec.id, tipo: rec.tipo, modelo: rec.modelo || '', inventario: rec.inventario || '',
    capacidad: rec.capacidad || '', cpu: rec.cpu || '',
    accesorios: rec.accesorios || {}, sinDanos: !!rec.sinDanos, danos: rec.danos || '',
    obs: rec.obs || '', estado: rec.estado || 'recibido',
    fotoDanos: (rec.fotoDanos && rec.fotoDanos.length <= 700000) ? rec.fotoDanos : '', danosIA: rec.danosIA || '',
    entregados: rec.entregados || {}, flujo: rec.flujo || 'rec',
    recibidoPor: rec.recibidoPor || '', entregadoPor: rec.entregadoPor || '',
    createdAt: rec.createdAt || Date.now(),
    creadoPor: rec.creadoPor || (cloudUser ? { uid: cloudUser.uid, email: cloudUser.email } : null),
    updatedAt: Date.now()
  };
}
function rentaFromCloud(doc) {
  return {
    id: doc.id, tipo: doc.tipo, modelo: doc.modelo || '', inventario: doc.inventario || '',
    capacidad: doc.capacidad || '', cpu: doc.cpu || '',
    accesorios: doc.accesorios || {}, sinDanos: doc.sinDanos !== false, danos: doc.danos || '',
    obs: doc.obs || '', estado: doc.estado || 'recibido',
    entregados: doc.entregados || {}, flujo: doc.flujo || 'rec',
    createdAt: doc.createdAt || 0,
    creadoPor: doc.creadoPor || null,
    recibidoPor: doc.recibidoPor || '', entregadoPor: doc.entregadoPor || ''
  };
}
function cloudUpsert(rec) {
  if (!CLOUD_ENABLED || !cloudUser || !window.Cloud) return;
  window.Cloud.upsertRenta(rentaToCloudDoc(rec)).catch(function (e) { console.warn('No se pudo guardar en la nube', e); });
}

// Inteligencia artificial: la app le pregunta por internet con la clave que
// el admin guarda en Usuarios. Gemini es gratis; DeepSeek es el respaldo y
// cobra por uso (muy barato). Ambos modelos tienen visión.
var AI_MODEL = 'gemini-3.8-flash';
var AI_MODEL_FALLBACK = 'gemini-flash-latest';
var aiKey = '';
var aiKeyDs = '';
var aiBusy = false;
var aiAnswers = {};
async function loadAiKey() {
  if (!CLOUD_ENABLED || !cloudUser || !window.Cloud || !window.Cloud.getAiKey) return;
  try { aiKey = await window.Cloud.getAiKey() || ''; } catch (e) { aiKey = ''; }
  try { if (window.Cloud.getDeepseekKey) aiKeyDs = await window.Cloud.getDeepseekKey() || ''; } catch (e) { aiKeyDs = ''; }
}
function refreshAiStatus() {
  var el = document.getElementById('aiKeyStatus');
  if (el) el.textContent = aiKey ? 'Clave guardada ✓ — la IA ya funciona en todos los teléfonos.' : 'Sin clave guardada: la IA no funciona hasta que guardes una.';
  var elDs = document.getElementById('aiKeyDsStatus');
  if (elDs) elDs.textContent = aiKeyDs ? 'Clave de DeepSeek guardada ✓ — entra si Gemini falla.' : 'Sin clave de DeepSeek guardada.';
}
async function askAI(prompt, imageDataUrl, retry) {
  if (!aiKey && !aiKeyDs) { var e0 = new Error('no-key'); throw e0; }
  if (!aiKey) return askDeepSeek(prompt, imageDataUrl, retry);
  var parts = [{ text: prompt }];
  if (imageDataUrl) {
    var m = /^data:(image\/[a-z]+);base64,(.*)$/.exec(imageDataUrl || '');
    if (m) parts.push({ inline_data: { mime_type: m[1], data: m[2] } });
  }
  var body = JSON.stringify({ contents: [{ parts: parts }], generationConfig: { temperature: 0.4, maxOutputTokens: 600 } });
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
}
function aiErrorText(e) {
  if (e && e.message === 'no-key') return 'Falta la clave de la IA. El administrador la pone en Usuarios → Inteligencia artificial.';
  if (e && e.provider === 'deepseek') {
    if (e.status === 401) return 'La clave de DeepSeek no es válida. Revisa la clave en Usuarios → Inteligencia artificial.';
    if (e.status === 402) return 'La cuenta de DeepSeek no tiene saldo. Recarga en platform.deepseek.com.';
    if (e.status === 429) return 'DeepSeek está ocupado (límite de uso). Inténtalo más tarde.';
    if (e.status === 503) return 'DeepSeek está saturado en este momento. Inténtalo de nuevo en un rato.';
    if (e.status) return 'DeepSeek respondió con error (código ' + e.status + ').' + (e.apiMessage ? ' ' + e.apiMessage : '');
    return 'No se pudo preguntar a DeepSeek. Revisa tu conexión.';
  }
  if (e && e.status === 400) return 'La clave de la IA no es válida. Revisa la clave en Usuarios → Inteligencia artificial.';
  if (e && e.status === 403) return 'Google no dejó usar la IA con esta clave: revisa en Google Cloud que la clave permita la API de Gemini (Generative Language API) y que esa API esté habilitada.';
  if (e && e.status === 404) return 'El modelo de IA no está disponible en este momento.';
  if (e && e.status === 503) return 'La IA está saturada en este momento. Inténtalo de nuevo en un rato.';
  if (e && e.status === 429) return 'La IA está ocupada (límite gratis del día). Inténtalo más tarde.';
  if (e && e.status) return 'La IA respondió con error (código ' + e.status + ').' + (e.apiMessage ? ' ' + e.apiMessage : '');
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
  return 'Escribe un mensaje corto y amable de WhatsApp en español para avisar que este equipo ya está listo y entregado. Usa estos datos y nada más: ' + waTextOne(p).split('\n').join(' | ') + ' Empieza con un saludo, pon los datos importantes (equipo, usuario, analista y fecha de entrega) y termina ofreciendo ayuda si algo falla. Máximo 8 líneas, sin inventar datos.';
}
function cloudDelete(id) {
  if (!CLOUD_ENABLED || !cloudUser || !window.Cloud) return;
  window.Cloud.deleteRenta(id).catch(function (e) { console.warn('No se pudo borrar en la nube', e); });
}

// ---------- Por preparar sincronizado ----------
// Los equipos en preparación (nuevos o reasignados) viven en Firestore
// (colección preparations) y se ven en todos los teléfonos, igual que la
// renta. La plantilla del checklist sigue siendo local de cada teléfono.
var cloudPrepUnsub = null;
var cloudDetectadosUnsub = null;
var detectados = [];
var PREP_MIG_KEY = 'checklist-soporte-migrado-preps-v1';
var MAX_FOTO_CLOUD = 700000; // la foto de serie no viaja si pasa de ~700 KB (límite de 1 MB por documento)
// La foto del número de serie es una imagen en base64 que puede pesar
// cientos de KB; si viajara entera, el documento pasaría el límite de
// 1 MB de Firestore y la escritura fallaría sin avisar.
function prepToCloudDoc(p) {
  var eq = p.equipo || {};
  var foto = eq.fotoSerie || null;
  if (foto && foto.length > MAX_FOTO_CLOUD) foto = null;
  return {
    id: p.id, createdAt: p.createdAt || Date.now(), deliveredAt: p.deliveredAt || null, readyAt: p.readyAt || null,
    checks: p.checks || {}, extraItems: p.extraItems || [], reasignaciones: p.reasignaciones || [],
    autoDetectado: p.autoDetectado || [],
    equipo: { tipo: eq.tipo || '', marca: eq.marca || '', modelo: eq.modelo || '', serie: eq.serie || '', inventario: eq.inventario || '', hostname: eq.hostname || '', fotoSerie: foto },
    usuario: { nombre: (p.usuario && p.usuario.nombre) || '', area: (p.usuario && p.usuario.area) || '', correo: (p.usuario && p.usuario.correo) || '' },
    tecnico: p.tecnico || '',
    updatedAt: Date.now()
  };
}
function prepFromCloud(doc) {
  var eq = doc.equipo || {};
  return {
    id: doc.id, createdAt: doc.createdAt || 0, deliveredAt: doc.deliveredAt || null, readyAt: doc.readyAt || null,
    checks: doc.checks || {}, extraItems: doc.extraItems || [], reasignaciones: doc.reasignaciones || [],
    autoDetectado: doc.autoDetectado || [],
    equipo: { tipo: eq.tipo || '', marca: eq.marca || '', modelo: eq.modelo || '', serie: eq.serie || '', inventario: eq.inventario || '', hostname: eq.hostname || '', fotoSerie: eq.fotoSerie || null },
    usuario: { nombre: (doc.usuario && doc.usuario.nombre) || '', area: (doc.usuario && doc.usuario.area) || '', correo: (doc.usuario && doc.usuario.correo) || '' },
    tecnico: doc.tecnico || ''
  };
}
function cloudUpsertPrep(prep) {
  if (!CLOUD_ENABLED || !cloudUser || !window.Cloud) return;
  window.Cloud.upsertPrep(prepToCloudDoc(prep)).catch(function (e) { console.warn('No se pudo guardar el equipo en la nube', e); });
}
function cloudDeletePrep(id) {
  if (!CLOUD_ENABLED || !cloudUser || !window.Cloud) return;
  window.Cloud.deletePrep(id).catch(function (e) { console.warn('No se pudo borrar el equipo en la nube', e); });
}
function cloudMarkDetectadoUsado(id) {
  if (!CLOUD_ENABLED || !cloudUser || !window.Cloud || !window.Cloud.markDetectadoUsado) return;
  window.Cloud.markDetectadoUsado(id).catch(function (e) { console.warn('No se pudo marcar el equipo detectado como usado', e); });
}
function cloudDeleteDetectado(id) {
  if (!CLOUD_ENABLED || !cloudUser || !window.Cloud || !window.Cloud.deleteDetectado) return;
  window.Cloud.deleteDetectado(id).catch(function (e) { console.warn('No se pudo descartar el equipo detectado', e); });
}
// Checks del detector (2.3.1): el detector de escritorio reporta qué
// software y hardware encontró (d.checks) y detalles (d.detalles, p. ej.
// officeDetectado). Solo los ids detectables de la plantilla actual
// pueden nacer marcados (t3/t4 de hardware y el software); datos,
// Invgate y la limpieza nunca.
var DETECTABLE_IDS = ['t3', 't4', 't6', 't7', 't8', 't9', 't10', 't11', 't18', 't19', 't20', 't21', 't22', 't23', 't24', 't25'];
var DET_SHORT = {
  t3: 'Batería y cargador', t4: 'Etiqueta y serie',
  t6: 'SO actualizado', t7: 'Antivirus', t8: 'Office', t9: 'Impresoras',
  t10: 'VPN', t11: 'Inicio rápido desactivado', t18: 'Chrome',
  t19: 'Adobe Reader', t20: 'WinRAR', t21: 'Lapi Fox', t22: 'Alfaweb',
  t23: 'Alfaprinter', t24: 'Accesos directos', t25: 'AnyDesk Gris'
};
function detShortName(id, val) {
  if (id === 't8') return (typeof val === 'string' && val) ? val : 'Office';
  if (DET_SHORT[id]) return DET_SHORT[id];
  var t = defaultTemplate().find(function (x) { return x.id === id; });
  return t ? t.text : id;
}
// Filtra los checks crudos del detector contra la plantilla actual:
// t8 solo si su valor es una de sus opciones; ids desconocidos se ignoran.
function filterDetectedChecks(raw) {
  var tpl = {};
  defaultTemplate().forEach(function (t) { tpl[t.id] = t; });
  var checks = {};
  var ids = [];
  DETECTABLE_IDS.forEach(function (id) {
    var t = tpl[id];
    if (!t) return;
    var v = raw ? raw[id] : undefined;
    if (id === 't8') {
      if (typeof v === 'string' && (t.options || []).indexOf(v) !== -1) { checks[id] = v; ids.push(id); }
      return;
    }
    if (v === true) { checks[id] = true; ids.push(id); }
  });
  return { checks: checks, ids: ids };
}
function detectedNames(checks, ids) {
  var list = ids || Object.keys(checks || {});
  return list.filter(function (id) { return checks && checks[id] !== undefined && checks[id] !== false; }).map(function (id) { return detShortName(id, checks[id]); });
}
function detLineFor(d) {
  var f = filterDetectedChecks(d.checks || {});
  var parts = detectedNames(f.checks, f.ids);
  if (d.detalles && d.detalles.officeDetectado && !f.checks.t8) parts.push('Office instalado, activación sin verificar');
  if (!parts.length) return '';
  return 'Detectado: ' + parts.map(function (n) { return esc(n); }).join(', ');
}
// Equipos detectados (2.3.1): solo se listan los NO usados, con sus datos
// y dos acciones: usarlo (llena Nuevo equipo) o descartarlo.
function renderDetectados() {
  var box = document.getElementById('detList');
  if (!box) return;
  var list = detectados.filter(function (d) { return !d.usado; });
  if (!list.length) { box.innerHTML = '<div class="empty">No hay equipos detectados pendientes.</div>'; return; }
  box.innerHTML = list.map(function (d) {
    var detLine = detLineFor(d);
    return '<div class="card"><h2>' + esc(d.hostname || 'Equipo') + '</h2>' +
      '<div class="sub">' + esc((d.marca || '') + ' ' + (d.modelo || '')) + ' · Serie: ' + esc(d.serie || '—') + '</div>' +
      '<div class="sub">CPU: ' + esc(d.cpu || '—') + ' · RAM: ' + (d.ramGB != null ? esc(d.ramGB) + ' GB' : '—') + ' · Disco: ' + (d.discoGB != null ? esc(d.discoGB) + ' GB' : '—') + ' · SO: ' + esc(d.so || '—') + '</div>' +
      '<div class="sub">Detectado ' + timeAgo(d.detectadoEn) + (d.detectadoPor ? ' por ' + esc(d.detectadoPor) : '') + '</div>' +
      (detLine ? '<div class="sub">' + detLine + '</div>' : '') +
      '<div class="actions"><button class="btn-green" data-det-use="' + esc(d.id) + '">Usar este equipo</button>' +
      '<button class="btn-ghost" data-det-del="' + esc(d.id) + '">Descartar</button></div></div>';
  }).join('');
}
async function migrateLocalPreparations() {
  try {
    var flag = PREP_MIG_KEY + ':' + cloudUser.uid;
    if (localStorage.getItem(flag)) return;
    var inCloud = await window.Cloud.getAllPreparations();
    var ids = {};
    inCloud.forEach(function (d) { ids[d.id] = true; });
    var pendientes = state.preparations.filter(function (p) { return !ids[p.id]; });
    for (var i = 0; i < pendientes.length; i++) {
      await window.Cloud.upsertPrep(prepToCloudDoc(pendientes[i]));
    }
    localStorage.setItem(flag, '1');
  } catch (e) { console.warn('Migración de preparaciones pendiente', e); }
}
// Al recibir la lista de la nube, conservar la foto de serie que cada
// teléfono ya tenía si la nube no la trae (la foto no siempre viaja).
function mergePrepsWithLocal(docs) {
  var localById = {};
  state.preparations.forEach(function (p) { localById[p.id] = p; });
  return docs.map(function (d) {
    var p = prepFromCloud(d);
    var local = localById[p.id];
    if (local && local.equipo && local.equipo.fotoSerie && !p.equipo.fotoSerie) p.equipo.fotoSerie = local.equipo.fotoSerie;
    return p;
  });
}
function technicianName() {
  return (cloudUser && (cloudUser.nombre || cloudUser.email)) || '';
}
var prefillUserName = '';
function prefillTecnico() {
  var f = document.getElementById('fTec');
  var name = technicianName();
  if (f && name && (!f.value || f.value === prefillUserName)) { f.value = name; prefillUserName = name; }
  var t = document.getElementById('tecnicoLine');
  if (t) t.textContent = name ? 'Analista: ' + name : '';
}
function applyRoleUI() {
  var isAdmin = cloudRole === 'admin';
  document.getElementById('tabUsuarios').hidden = !isAdmin;
  if (!isAdmin && !document.getElementById('viewUsuarios').hidden) showVista('preparar');
  var bar = document.getElementById('sessionBar');
  bar.hidden = !cloudUser;
  if (cloudUser) document.getElementById('sessionUser').textContent = (cloudUser.nombre || cloudUser.email) + (cloudRole ? ' · ' + (cloudRole === 'admin' ? 'Administrador' : 'Usuario') : '');
}
async function renderUsuarios() {
  var box = document.getElementById('userList');
  if (!CLOUD_ENABLED || cloudRole !== 'admin') { box.innerHTML = ''; return; }
  try {
    var users = await window.Cloud.listUsers();
    lastUsers = users;
    var locks = {};
    if (window.Cloud.listLoginLocks) {
      try {
        (await window.Cloud.listLoginLocks()).forEach(function (l) { locks[l.uid] = l; });
      } catch (e2) { /* sin bloqueos */ }
    }
    loadAiKey().then(refreshAiStatus);
    refreshAiStatus();
    box.innerHTML = users.map(function (u) {
      var locked = !!(locks[u.uid] && locks[u.uid].locked);
      return '<div class="card"><h2>' + esc(u.nombre || u.email) + '</h2>' +
        '<div class="sub">' + esc(u.email) + '</div>' +
        (u.usuario ? '<div class="sub">Usuario: ' + esc(u.usuario) + '</div>' : '') +
        '<span class="badge ' + (u.rol === 'admin' ? 'b-listo' : 'b-entr') + '">' + (u.rol === 'admin' ? 'Administrador' : 'Usuario') + '</span> ' +
        '<span class="badge ' + (u.activo === false ? 'b-prep' : 'b-listo') + '">' + (u.activo === false ? 'Desactivado' : 'Activo') + '</span>' +
        (locked ? ' <span class="badge b-prep">🔒 Bloqueada</span>' : '') +
        '<div class="actions">' +
        '<button class="btn-ghost" data-user-toggle="' + u.uid + '">' + (u.activo === false ? 'Activar' : 'Desactivar') + '</button>' +
        '<button class="btn-ghost" data-user-role="' + u.uid + '">' + (u.rol === 'admin' ? 'Hacer usuario' : 'Hacer admin') + '</button>' +
        '<button class="btn-ghost" data-user-pass="' + u.uid + '">Contraseña</button>' +
        '<button class="btn-ghost" data-user-edit="' + u.uid + '">Editar</button>' +
        (locked ? '<button class="btn-ghost" data-user-unlock="' + u.uid + '">🔓 Desbloquear</button>' : '') +
        '<button class="btn-danger" data-user-del="' + u.uid + '">Eliminar</button></div></div>';
    }).join('') || '<div class="empty">No hay usuarios.</div>';
  } catch (e) { box.innerHTML = '<div class="empty">No se pudieron cargar los usuarios.</div>'; }
}
async function migrateLocalRenta() {
  try {
    var flag = MIG_KEY + ':' + cloudUser.uid;
    if (localStorage.getItem(flag)) return;
    var inCloud = await window.Cloud.getAllRenta();
    var ids = {};
    inCloud.forEach(function (d) { ids[d.id] = true; });
    var pendientes = state.renta.filter(function (r) { return !ids[r.id]; });
    for (var i = 0; i < pendientes.length; i++) {
      await window.Cloud.upsertRenta(rentaToCloudDoc(pendientes[i]));
    }
    localStorage.setItem(flag, '1');
  } catch (e) { console.warn('Migración pendiente', e); }
}
async function checkBootstrap() {
  try {
    var done = await window.Cloud.isInitialized();
    document.getElementById('bootstrapBox').hidden = !!done;
    // El login siempre queda visible: si el admin ya se creó en Auth pero
    // su documento no se guardó, debe poder entrar para completar el alta.
    document.getElementById('loginBox').hidden = false;
  } catch (e) { /* sin conexión: mostrar el login normal */ }
}
async function onAuthChanged(user) {
  if (!user) {
    cloudUser = null; cloudRole = null;
    if (cloudUnsub) { cloudUnsub(); cloudUnsub = null; }
    if (cloudPrepUnsub) { cloudPrepUnsub(); cloudPrepUnsub = null; }
    if (cloudDetectadosUnsub) { cloudDetectadosUnsub(); cloudDetectadosUnsub = null; }
    document.getElementById('mainApp').hidden = true;
    document.getElementById('appHeader').hidden = true;
    document.getElementById('loginView').hidden = false;
    checkBootstrap();
    _authReady = true;
    return;
  }
  var doc = null;
  var lastReadErr = null;
  // Tres intentos: la lectura puede fallar al inicio (el documento se está
  // guardando o el token de sesión aún no llega a Firestore).
  var delays = [0, 1500, 3000];
  for (var i = 0; i < delays.length && !doc; i++) {
    if (delays[i]) await new Promise(function (r) { setTimeout(r, delays[i]); });
    try {
      doc = await window.Cloud.getUserDoc(user.uid);
    } catch (e) { lastReadErr = e; doc = null; }
  }
  if (!doc) {
    // El usuario existe en Auth pero su documento no se guardó
    // (alta de admin a medio crear). Si todavía no hay admin,
    // completar el alta como administrador en vez de quedarse trabado.
    try {
      var done = await window.Cloud.isInitialized();
      if (!done) {
        await window.Cloud.repairAdmin(user.uid, user.email);
        await new Promise(function (r) { setTimeout(r, 800); });
        doc = await window.Cloud.getUserDoc(user.uid);
      }
    } catch (e) { /* cae al mensaje de abajo */ }
  }
  if (!doc || doc.activo === false || !doc.rol) {
    if (doc && doc.activo === false) {
      document.getElementById('loginError').textContent = 'Tu usuario está desactivado. Contacta al administrador.';
      await window.Cloud.signOut();
      _authReady = true;
      return;
    }
    var codeTxt = lastReadErr && lastReadErr.code ? ' (' + lastReadErr.code + ')' : '';
    document.getElementById('loginError').textContent = 'Tu usuario no tiene rol asignado. Pide al administrador que te registre.' + codeTxt;
    // No cerrar sesión: el usuario puede reintentar sin volver a escribir
    // su contraseña (la lectura pudo fallar por red o por el token).
    document.getElementById('btnReintentarLogin').hidden = false;
    _authReady = true;
    return;
  }
  try {
    cloudUser = { uid: user.uid, email: user.email, nombre: doc.nombre || '' };
    cloudRole = doc.rol;
    document.getElementById('loginView').hidden = true;
    document.getElementById('mainApp').hidden = false;
    document.getElementById('appHeader').hidden = false;
    document.getElementById('loginError').textContent = '';
    document.getElementById('btnReintentarLogin').hidden = true;
    applyRoleUI();
    prefillTecnico();
    await migrateLocalRenta();
    await migrateLocalPreparations();
    if (cloudUnsub) cloudUnsub();
    cloudUnsub = window.Cloud.subscribeRenta(function (docs) {
      state.renta = docs.map(rentaFromCloud);
      save(); render();
    });
    if (cloudPrepUnsub) cloudPrepUnsub();
    cloudPrepUnsub = window.Cloud.subscribePreparations(function (docs) {
      state.preparations = mergePrepsWithLocal(docs);
      save(); render();
    });
    if (window.Cloud.subscribeDetectados) {
      if (cloudDetectadosUnsub) cloudDetectadosUnsub();
      cloudDetectadosUnsub = window.Cloud.subscribeDetectados(function (docs) {
        detectados = docs || [];
        renderDetectados();
      });
    }
    startEquipo();
    render();
    loadAiKey();
    _authReady = true;
  } catch (e) {
    document.getElementById('loginError').textContent = 'No se pudo verificar tu usuario. Revisa tu conexión.' + (e && e.code ? ' (' + e.code + ')' : '');
    _authReady = true;
  }
}
var _authReady = false;
async function boot() {
  if (!CLOUD_ENABLED) { document.getElementById('mainApp').hidden = false; document.getElementById('appHeader').hidden = false; _authReady = true; render(); return; }
  var ok = false;
  try { ok = window.Cloud && await window.Cloud.init(window.FIREBASE_CONFIG); } catch (e) { ok = false; }
  if (!ok) { CLOUD_ENABLED = false; document.getElementById('mainApp').hidden = false; document.getElementById('appHeader').hidden = false; _authReady = true; render(); return; }
  document.getElementById('mainApp').hidden = true;
  document.getElementById('appHeader').hidden = true;
  document.getElementById('loginView').hidden = false;
  window.Cloud.onAuth(function (user) { onAuthChanged(user); });
  checkBootstrap();
  var savedId = localStorage.getItem('checklist-login-id');
  if (savedId) document.getElementById('loginEmail').value = savedId;
  if (localStorage.getItem('checklist-remember') === '0') document.getElementById('loginRemember').checked = false;
  refreshBioButton();
}

var filterStatus = 'todos';
var todosPage = 0;
var searchText = '';

function allItems(prep) {
  var isRe = !!(prep.reasignaciones && prep.reasignaciones.length);
  var items = state.template.filter(function (t) { return !t.reassignOnly || isRe; }).map(function (t) { return { id: t.id, group: t.group, text: t.text, extra: false, options: t.options, optional: !!t.optional, reassignOnly: !!t.reassignOnly }; });
  (prep.extraItems || []).forEach(function (x) { items.push({ id: x.id, group: x.group, text: x.text, extra: true }); });
  return items;
}
function itemDisplayText(prep, it) {
  var txt = it.text;
  if (it.options && typeof prep.checks[it.id] === 'string' && prep.checks[it.id]) txt += ' — ' + prep.checks[it.id];
  return txt;
}
function requiredItems(prep) {
  return allItems(prep).filter(function (it) { return !it.optional; });
}
function progress(prep) {
  var all = allItems(prep);
  var items = requiredItems(prep);
  if (!all.length) return 0;
  if (!items.length) return 100;
  var done = items.filter(function (it) { return prep.checks[it.id]; }).length;
  return Math.round(done / items.length * 100);
}
function statusOf(prep) {
  if (prep.deliveredAt) return 'entregado';
  if (prep.readyAt) return 'listo';
  return progress(prep) === 100 ? 'listo' : 'preparacion';
}
function statusLabel(s) {
  return s === 'entregado' ? 'Entregado' : s === 'listo' ? 'Listo para entregar' : 'En preparación';
}
function statusClass(s) {
  return s === 'entregado' ? 'b-entr' : s === 'listo' ? 'b-listo' : 'b-prep';
}
var DELIVERED_VISIBLE_DAYS = 15;
function deliveredVisible(p) {
  if (!p.deliveredAt) return true;
  if (cloudRole === 'admin') return true;
  return (Date.now() - p.deliveredAt) <= DELIVERED_VISIBLE_DAYS * 86400000;
}
function visiblePreps() { return state.preparations.filter(deliveredVisible); }
function reassignText(p) {
  return (p.reasignaciones || []).map(function (r) {
    return (r.de || '—') + ' → ' + (r.a || '—') + ' (' + fmtDate(r.fecha) + ')';
  }).join('; ');
}
function esc(s) {
  return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
  });
}
function fmtDate(ts) {
  var d = new Date(ts);
  return d.toLocaleDateString('es-MX', { day: '2-digit', month: 'short', year: 'numeric' }) +
    ' ' + d.toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' });
}
function fmtTime(ts) {
  return new Date(ts).toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' });
}
function timeAgo(ms) {
  if (!ms) return 'sin registro';
  var d = Date.now() - ms;
  if (d < 60 * 1000) return 'hace un momento';
  if (d < 60 * 60 * 1000) return 'hace ' + Math.floor(d / 60000) + ' min';
  if (d < 24 * 60 * 60 * 1000) return 'hace ' + Math.floor(d / 3600000) + ' h';
  return fmtDate(ms);
}

// Generador de PDF sin dependencias: un PDF 1.4 valido con Helvetica.
function pdfEsc(s) {
  return String(s == null ? '' : s).replace(/\\/g, '\\\\').replace(/\(/g, '\\(').replace(/\)/g, '\\)');
}
function pdfBytes(str) {
  var b = new Uint8Array(str.length);
  for (var i = 0; i < str.length; i++) b[i] = str.charCodeAt(i) & 0xFF;
  return b;
}
function wrapText(text, maxChars) {
  var words = String(text).split(/\s+/).filter(Boolean);
  var lines = [], cur = '';
  words.forEach(function (w) {
    if ((cur + ' ' + w).trim().length > maxChars && cur) { lines.push(cur); cur = w; }
    else cur = (cur + ' ' + w).trim();
  });
  if (cur) lines.push(cur);
  return lines.length ? lines : [''];
}
function buildPdf(prep) {
  var st = statusOf(prep), pct = progress(prep);
  var rows = [];
  function row(t, f, s) { rows.push({ t: t, f: f || 'F1', s: s || 11 }); }
  row('Checklist de Soporte', 'F2', 18);
  wrapText((prep.equipo.marca || 'Equipo') + ' ' + (prep.equipo.modelo || ''), 55).forEach(function (ln) { row(ln, 'F2', 14); });
  row('', 'F1', 11);
  row('Tipo: ' + (prep.equipo.tipo || '—'), 'F1', 11);
  row('Marca: ' + (prep.equipo.marca || '—'), 'F1', 11);
  row('Modelo: ' + (prep.equipo.modelo || '—'), 'F1', 11);
  row('No. de serie: ' + (prep.equipo.serie || '—'), 'F1', 11);
  if (prep.equipo.fotoSerie) row('Foto de serie: Sí — guardada en la app', 'F1', 11);
  row('No. de inventario: ' + (prep.equipo.inventario || '—'), 'F1', 11);
  row('Hostname: ' + (prep.equipo.hostname || '—'), 'F1', 11);
  row('Usuario: ' + (prep.usuario.nombre || '—'), 'F1', 11);
  row('Área: ' + (prep.usuario.area || '—'), 'F1', 11);
  row('Correo: ' + (prep.usuario.correo || '—'), 'F1', 11);
  row('Analista: ' + (prep.tecnico || '—'), 'F1', 11);
  row('Estado: ' + statusLabel(st) + ' — ' + pct + '% completado', 'F2', 11);
  row('Creado: ' + fmtDate(prep.createdAt), 'F1', 11);
  if (prep.deliveredAt) row('Entregado: ' + fmtDate(prep.deliveredAt), 'F1', 11);
  (prep.reasignaciones || []).forEach(function (r) {
    row('Reasignado: ' + (r.de || '—') + ' → ' + (r.a || '—') + ' (' + fmtDate(r.fecha) + ')', 'F1', 11);
  });
  row('', 'F1', 11);
  var items = allItems(prep);
  GROUP_ORDER.forEach(function (g) {
    var gi = items.filter(function (it) { return it.group === g; });
    if (!gi.length) return;
    row(GROUPS[g], 'F2', 13);
    gi.forEach(function (it) {
      var mark = prep.checks[it.id] ? '[x] ' : '[ ] ';
      wrapText(mark + itemDisplayText(prep, it), 82).forEach(function (ln) { row(ln, 'F1', 11); });
    });
    row('', 'F1', 11);
  });
  row('Generado el ' + fmtDate(Date.now()) + ' — Checklist de Soporte', 'F1', 10);
  var W = 595, H = 842, M = 48, usable = H - M * 2;
  var pages = [], cur = [], y = 0;
  rows.forEach(function (r) {
    var lh = r.s * 1.45;
    if (y + lh > usable && cur.length) { pages.push(cur); cur = []; y = 0; }
    cur.push(r); y += lh;
  });
  if (cur.length) pages.push(cur);
  var objs = [];
  objs[1] = '<< /Type /Catalog /Pages 2 0 R >>';
  var kidRefs = [];
  var nextId = 5;
  pages.forEach(function (pg) {
    var contentId = nextId++, pageId = nextId++;
    var cs = '';
    var yy = H - M;
    pg.forEach(function (r) {
      var lh = r.s * 1.45;
      yy -= lh;
      cs += 'BT /' + r.f + ' ' + r.s + ' Tf ' + M + ' ' + yy.toFixed(1) + ' Td (' + pdfEsc(r.t) + ') Tj ET\n';
    });
    objs[contentId] = '<< /Length ' + pdfBytes(cs).length + ' >>\nstream\n' + cs + '\nendstream';
    objs[pageId] = '<< /Type /Page /Parent 2 0 R /MediaBox [0 0 ' + W + ' ' + H + '] /Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents ' + contentId + ' 0 R >>';
    kidRefs.push(pageId + ' 0 R');
  });
  objs[2] = '<< /Type /Pages /Kids [' + kidRefs.join(' ') + '] /Count ' + pages.length + ' >>';
  objs[3] = '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>';
  objs[4] = '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>';
  var pdf = '%PDF-1.4\n';
  var offsets = [0];
  for (var i = 1; i < nextId; i++) {
    offsets[i] = pdfBytes(pdf).length;
    pdf += i + ' 0 obj\n' + objs[i] + '\nendobj\n';
  }
  var xrefPos = pdfBytes(pdf).length;
  var n = nextId;
  pdf += 'xref\n0 ' + n + '\n';
  pdf += '0000000000 65535 f \n';
  for (var j = 1; j < n; j++) {
    pdf += ('0000000000' + offsets[j]).slice(-10) + ' 00000 n \n';
  }
  pdf += 'trailer\n<< /Size ' + n + ' /Root 1 0 R >>\nstartxref\n' + xrefPos + '\n%%EOF';
  return new Blob([pdfBytes(pdf)], { type: 'application/pdf' });
}
function sharePdf(prep) {
  var blob = buildPdf(prep);
  var name = ('checklist-' + (prep.equipo.marca || 'equipo') + '-' + (prep.equipo.modelo || '') + '-' + (prep.equipo.serie || '')).toLowerCase()
    .replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '') + '.pdf';
  var file = new File([blob], name, { type: 'application/pdf' });
  var texto = 'Checklist de Soporte: ' + (prep.equipo.marca || 'Equipo') + ' ' + (prep.equipo.modelo || '') +
    ' — ' + progress(prep) + '% completado (' + statusLabel(statusOf(prep)) + ').';
  if (navigator.canShare && navigator.canShare({ files: [file] })) {
    navigator.share({ files: [file], title: 'Checklist de Soporte', text: texto }).catch(function () {});
    return;
  }
  var a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = name;
  a.click();
  setTimeout(function () { URL.revokeObjectURL(a.href); }, 5000);
  if (navigator.share) {
    navigator.share({ title: 'Checklist de Soporte', text: texto + ' El PDF se descargó, adjúntalo en WhatsApp.' }).catch(function () {});
  } else {
    alert('PDF descargado: ' + name + '. Compártelo por WhatsApp desde tus archivos.');
  }
}

// Excel real (.xlsx) sin dependencias: ZIP con entradas STORED + CRC32.
function crc32(buf) {
  var t = crc32.table;
  if (!t) {
    t = crc32.table = [];
    for (var n = 0; n < 256; n++) { var c = n; for (var k = 0; k < 8; k++) c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1); t[n] = c >>> 0; }
  }
  var crc = 0xFFFFFFFF;
  for (var i = 0; i < buf.length; i++) crc = t[(crc ^ buf[i]) & 0xFF] ^ (crc >>> 8);
  return (crc ^ 0xFFFFFFFF) >>> 0;
}
function u16(n) { return new Uint8Array([n & 0xFF, (n >> 8) & 0xFF]); }
function u32(n) { return new Uint8Array([n & 0xFF, (n >> 8) & 0xFF, (n >> 16) & 0xFF, (n >> 24) & 0xFF]); }
function concatBytes(parts) {
  var len = 0; parts.forEach(function (x) { len += x.length; });
  var out = new Uint8Array(len), off = 0;
  parts.forEach(function (x) { out.set(x, off); off += x.length; });
  return out;
}
function zipStored(files) {
  var enc = new TextEncoder();
  var parts = [], central = [], offset = 0;
  var d = new Date();
  var dosTime = ((d.getHours() & 31) << 11) | ((d.getMinutes() & 63) << 5) | ((d.getSeconds() >> 1) & 31);
  var dosDate = (((d.getFullYear() - 1980) & 127) << 9) | (((d.getMonth() + 1) & 15) << 5) | (d.getDate() & 31);
  files.forEach(function (f) {
    var nameB = enc.encode(f.name), crc = crc32(f.data);
    var local = concatBytes([enc.encode('PK\x03\x04'), u16(20), u16(0x0800), u16(0), u16(dosTime), u16(dosDate), u32(crc), u32(f.data.length), u32(f.data.length), u16(nameB.length), u16(0), nameB, f.data]);
    parts.push(local);
    central.push(concatBytes([enc.encode('PK\x01\x02'), u16(20), u16(20), u16(0x0800), u16(0), u16(dosTime), u16(dosDate), u32(crc), u32(f.data.length), u32(f.data.length), u16(nameB.length), u16(0), u16(0), u16(0), u16(0), u32(0), u32(offset), nameB]));
    offset += local.length;
  });
  var centralStart = offset;
  var centralBytes = concatBytes(central);
  parts.push(centralBytes);
  offset += centralBytes.length;
  parts.push(concatBytes([enc.encode('PK\x05\x06'), u16(0), u16(0), u16(files.length), u16(files.length), u32(centralBytes.length), u32(centralStart), u16(0)]));
  return new Blob(parts, { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
}
function xmlEsc(s) {
  return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
function colLetter(i) {
  var s = '';
  while (i >= 0) { s = String.fromCharCode(65 + (i % 26)) + s; i = Math.floor(i / 26) - 1; }
  return s;
}
function xlsxCell(r, c, v) {
  var ref = colLetter(c) + r;
  if (typeof v === 'number') return '<c r="' + ref + '"><v>' + v + '</v></c>';
  return '<c r="' + ref + '" t="inlineStr"><is><t>' + xmlEsc(v) + '</t></is></c>';
}
function buildXlsxFromTable(headers, rows, sheetName) {
  var enc = new TextEncoder();
  var sheetRows = headers ? '<row r="1">' + headers.map(function (h, i) { return xlsxCell(1, i, h); }).join('') + '</row>' : '';
  var startRow = headers ? 2 : 1;
  rows.forEach(function (vals, idx) {
    var r = startRow + idx;
    sheetRows += '<row r="' + r + '">' + vals.map(function (v, i) { return xlsxCell(r, i, v); }).join('') + '</row>';
  });
  var sheet = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' +
    '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>' + sheetRows + '</sheetData></worksheet>';
  var contentTypes = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' +
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">' +
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>' +
    '<Default Extension="xml" ContentType="application/xml"/>' +
    '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>' +
    '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' +
    '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/></Types>';
  var rels = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' +
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' +
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>';
  var workbook = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' +
    '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">' +
    '<sheets><sheet name="' + xmlEsc(sheetName) + '" sheetId="1" r:id="rId1"/></sheets></workbook>';
  var wbRels = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' +
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' +
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>' +
    '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>';
  var styles = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' +
    '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">' +
    '<fonts><font><sz val="11"/><name val="Calibri"/></font></fonts>' +
    '<fills><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill></fills>' +
    '<borders><border><left/><right/><top/><bottom/><diagonal/></border></borders>' +
    '<cellStyleXfs><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>' +
    '<cellXfs><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/></cellXfs>' +
    '<cellStyles><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles></styleSheet>';
  return zipStored([
    { name: '[Content_Types].xml', data: enc.encode(contentTypes) },
    { name: '_rels/.rels', data: enc.encode(rels) },
    { name: 'xl/workbook.xml', data: enc.encode(workbook) },
    { name: 'xl/_rels/workbook.xml.rels', data: enc.encode(wbRels) },
    { name: 'xl/worksheets/sheet1.xml', data: enc.encode(sheet) },
    { name: 'xl/styles.xml', data: enc.encode(styles) }
  ]);
}
function buildXlsx(preps) {
  var headers = ['Tipo', 'Marca', 'Modelo', 'No. de serie', 'No. de inventario', 'Hostname', 'Usuario', 'Área', 'Correo', 'Analista', 'Estado', 'Avance %', 'Creado', 'Entregado', 'Reasignaciones'];
  var rows = preps.map(function (p) {
    return [p.equipo.tipo, p.equipo.marca, p.equipo.modelo, p.equipo.serie, p.equipo.inventario, p.equipo.hostname,
      p.usuario.nombre, p.usuario.area, p.usuario.correo, p.tecnico,
      statusLabel(statusOf(p)), progress(p), fmtDate(p.createdAt), p.deliveredAt ? fmtDate(p.deliveredAt) : '', reassignText(p)];
  });
  return buildXlsxFromTable(headers, rows, 'Equipos');
}
function rentaDescripcion(rec) {
  var accs = (ACCS_POR_TIPO[rec.tipo] || []).filter(function (k) { return rec.accesorios && rec.accesorios[k]; })
    .map(function (k) { return ACCS_LABEL[k].toUpperCase(); });
  var base;
  if (rec.tipo === 'iPad') {
    base = ((rec.modelo || '') + ' ' + (rec.capacidad || '')).trim().toUpperCase();
  } else if (rec.tipo === 'PC') {
    base = [rec.modelo, rec.cpu, rec.capacidad].filter(Boolean).join(' ').toUpperCase();
  } else {
    base = (rec.modelo || '').toUpperCase();
  }
  var desc = base;
  if (accs.length) desc = (desc ? desc + ', ' : '') + accs.join(', ');
  if (!rec.sinDanos) desc += (desc ? ' - ' : '') + 'DAÑOS' + (rec.danos ? ': ' + rec.danos.toUpperCase() : '');
  return desc || '—';
}
function buildXlsxRenta(list, flow) {
  var orden = ['Laptop', 'PC', 'iPad'];
  var headersPorTipo = {
    Laptop: ['Equipo', '# Inventario', 'Laptop', 'Analista'],
    PC: ['Equipo', '# Inventario', 'CPU', 'Analista'],
    iPad: ['Equipo', 'Ipads', '# inventario', 'Analista']
  };
  var rows = [];
  orden.forEach(function (tipo) {
    var items = list.filter(function (r) { return r.tipo === tipo; });
    if (!items.length) return;
    rows.push(headersPorTipo[tipo]);
    items.forEach(function (rec, idx) {
      var inv = rec.inventario ? '*' + rec.inventario + '*' : '';
      var tec = flow === 'rec' ? (rec.recibidoPor || '') : (rec.entregadoPor || '');
      if (tipo === 'iPad') rows.push([idx + 1, rentaDescripcion(rec), inv, tec]);
      else rows.push([idx + 1, inv, rentaDescripcion(rec), tec]);
    });
    rows.push([]);
  });
  return buildXlsxFromTable(null, rows, flow === 'rec' ? 'Recibir renta' : 'Entrega Renta');
}
function blobToBase64(blob) {
  return new Promise(function (resolve, reject) {
    var r = new FileReader();
    r.onload = function () { resolve(String(r.result).split(',')[1]); };
    r.onerror = reject;
    r.readAsDataURL(blob);
  });
}
async function openXlsxFile(blob, name) {
  try {
    var Plugins = window.Capacitor && window.Capacitor.Plugins;
    if (Plugins && Plugins.Filesystem && Plugins.FileOpener) {
      var base64 = await blobToBase64(blob);
      var saved = await Plugins.Filesystem.writeFile({ path: name, data: base64, directory: 'CACHE' });
      await Plugins.FileOpener.open({ filePath: saved.uri, contentType: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
      return true;
    }
  } catch (e) { /* cae al respaldo web */ }
  var url = URL.createObjectURL(blob);
  window.open(url, '_blank');
  setTimeout(function () { URL.revokeObjectURL(url); }, 60000);
  return false;
}
async function openXlsxRenta(flow) {
  var list = rentaList(flow);
  if (!list.length) { alert('No hay equipos de renta en esta sección.'); return; }
  var blob = buildXlsxRenta(list, flow);
  var name = flow === 'rec' ? 'equipos-renta-recibir.xlsx' : 'equipos-renta-entrega.xlsx';
  try {
    await openXlsxFile(blob, name);
  } catch (e) {
    alert('No se pudo abrir el archivo. Usa Compartir para mandarlo por WhatsApp o Drive.');
  }
}
async function shareRentaFile(flow, channel) {
  var list = rentaList(flow);
  if (!list.length) { alert('No hay equipos de renta en esta sección.'); return; }
  var blob = buildXlsxRenta(list, flow);
  var name = flow === 'rec' ? 'equipos-renta-recibir.xlsx' : 'equipos-renta-entrega.xlsx';
  try {
    var Plugins = window.Capacitor && window.Capacitor.Plugins;
    if (!Plugins || !Plugins.Filesystem || !Plugins.Share) throw new Error('share-no-disponible');
    var base64 = await blobToBase64(blob);
    var saved = await Plugins.Filesystem.writeFile({ path: name, data: base64, directory: 'CACHE' });
    await Plugins.Share.share({
      title: 'Checklist de Soporte',
      text: 'Equipos de renta — Checklist de Soporte.',
      url: saved.uri,
      dialogTitle: channel === 'wa' ? 'Compartir por WhatsApp' : 'Enviar por correo'
    });
  } catch (e) {
    alert('No se pudo compartir el archivo. Usa Abrir para verlo en el teléfono.');
  }
}
function cleanName(s) {
  return String(s || '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
}
async function shareXlsx(preps, name, dialogTitle) {
  if (!preps.length) { alert('No hay equipos para compartir.'); return; }
  var blob = buildXlsx(preps);
  try {
    var Plugins = window.Capacitor && window.Capacitor.Plugins;
    if (!Plugins || !Plugins.Filesystem || !Plugins.Share) throw new Error('share-no-disponible');
    var base64 = await blobToBase64(blob);
    var saved = await Plugins.Filesystem.writeFile({ path: name, data: base64, directory: 'CACHE' });
    await Plugins.Share.share({
      title: 'Checklist de Soporte',
      text: 'Datos de equipos — Checklist de Soporte.',
      url: saved.uri,
      dialogTitle: dialogTitle || 'Compartir Excel'
    });
  } catch (e) {
    alert('No se pudo compartir el archivo. Usa Abrir para verlo en el teléfono.');
  }
}
async function shareMail(preps, name) { return shareXlsx(preps, name, 'Enviar por correo'); }
function waTextOne(p) {
  var items = requiredItems(p);
  var done = items.filter(function (it) { return p.checks[it.id]; }).length;
  var pendientes = items.filter(function (it) { return !p.checks[it.id]; }).map(function (it) { return it.text; });
  var lines = ['🖥️ Checklist de Soporte', '',
    (p.equipo.marca || 'Equipo') + ' ' + (p.equipo.modelo || ''),
    'Tipo: ' + (p.equipo.tipo || '—'),
    'Serie: ' + (p.equipo.serie || '—'),
    'Inventario: ' + (p.equipo.inventario || '—'),
    'Hostname: ' + (p.equipo.hostname || '—'),
    'Usuario: ' + (p.usuario.nombre || '—') + (p.usuario.area ? ' (' + p.usuario.area + ')' : ''),
    'Analista: ' + (p.tecnico || '—'),
    'Estado: ' + statusLabel(statusOf(p)) + ' — ' + progress(p) + '% (' + done + '/' + items.length + ' puntos)'];
  if ((p.reasignaciones || []).length) {
    lines.push('Reasignaciones:');
    p.reasignaciones.forEach(function (r) { lines.push('• ' + (r.de || '—') + ' → ' + (r.a || '—') + ' (' + fmtDate(r.fecha) + ')'); });
  }
  if (pendientes.length) {
    lines.push('', 'Pendiente:');
    pendientes.slice(0, 8).forEach(function (t) { lines.push('• ' + t); });
    if (pendientes.length > 8) lines.push('... y ' + (pendientes.length - 8) + ' más.');
  } else {
    lines.push('', 'Checklist completo \u2713');
  }
  return lines.join('\n');
}
function waTextAll(list) {
  var counts = { preparacion: 0, listo: 0, entregado: 0 };
  list.forEach(function (p) { counts[statusOf(p)]++; });
  var lines = ['🖥️ Checklist de Soporte — ' + list.length + ' equipos', '',
    'En preparación: ' + counts.preparacion + ' · Listos: ' + counts.listo + ' · Entregados: ' + counts.entregado, ''];
  list.forEach(function (p) {
    lines.push('• ' + (p.equipo.marca || 'Equipo') + ' ' + (p.equipo.modelo || '') +
      ' — Serie: ' + (p.equipo.serie || '—') +
      (p.equipo.hostname ? ' — Host: ' + p.equipo.hostname : '') +
      ' — ' + (p.usuario.nombre || 'sin usuario') +
      ' — ' + statusLabel(statusOf(p)) + ' ' + progress(p) + '%');
  });
  return lines.join('\n');
}
function shareText(texto) {
  if (navigator.share) {
    navigator.share({ title: 'Checklist de Soporte', text: texto }).catch(function () {});
    return;
  }
  window.open('https://wa.me/?text=' + encodeURIComponent(texto), '_blank');
}
function shareWhatsApp(preps) {
  if (!preps.length) { alert('No hay equipos para compartir.'); return; }
  shareText(preps.length === 1 ? waTextOne(preps[0]) : waTextAll(preps));
}

function currentList() {
  var q = searchText.trim().toLowerCase();
  var list = state.preparations.filter(function (p) {
    if (!deliveredVisible(p)) return false;
    if (filterStatus !== 'todos' && statusOf(p) !== filterStatus) return false;
    if (!q) return true;
    var hay = [p.equipo.tipo, p.equipo.marca, p.equipo.modelo, p.equipo.serie, p.equipo.inventario, p.equipo.hostname,
      p.usuario.nombre, p.usuario.area, p.usuario.correo, p.tecnico,
      (p.reasignaciones || []).map(function (r) { return (r.de || '') + ' ' + (r.a || ''); }).join(' ')].join(' ').toLowerCase();
    return hay.indexOf(q) !== -1;
  });
  // Más recientes primero
  list.sort(function (a, b) { return b.createdAt - a.createdAt; });
  return list;
}

// Equipos de renta: recepcion (rec) y entrega (for).
var ACCS_LABEL = { cargador: 'Cargador', cable: 'Cable', mouse: 'Mouse', maletin: 'Maletín', teclado: 'Teclado', cableCorriente: 'Cable de corriente', cableVideo: 'Cable de video', tarjetaVideo: 'Tarjeta de vídeo' };
var ACCS_POR_TIPO = { Laptop: ['mouse', 'cargador', 'maletin'], iPad: ['cargador', 'cable'], PC: ['cableCorriente', 'mouse', 'teclado', 'cableVideo', 'tarjetaVideo'] };
function rentaList(flow) {
  // Recibir renta: solo los equipos pendientes de entregar.
  // Entrega Renta: todos los equipos de renta, lleguen de donde lleguen.
  if (flow === 'rec') {
    return state.renta.filter(function (r) { return r.flujo === 'rec' && r.estado !== 'entregado'; })
      .sort(function (a, b) { return a.createdAt - b.createdAt; });
  }
  var list = state.renta.slice();
  // Entregados solo los ve el admin; a los usuarios ya no les aparecen.
  if (CLOUD_ENABLED && cloudRole !== 'admin') list = list.filter(function (r) { return r.estado !== 'entregado'; });
  return list.sort(function (a, b) { return a.createdAt - b.createdAt; });
}
function rentaEstadoLabel(e) {
  return e === 'recibido' ? 'Recibido' : e === 'revisado' ? 'Revisado' : e === 'entregado' ? 'Entregado' : 'Por entregar';
}
function rentaEstadoClase(e) {
  return e === 'entregado' ? 'b-entr' : e === 'revisado' ? 'b-listo' : 'b-prep';
}
function rentaNext(flow, e) {
  if (flow === 'rec') return e === 'recibido' ? 'revisado' : 'recibido';
  return e === 'en formateo' ? 'revisado' : e === 'revisado' ? 'entregado' : 'en formateo';
}
function rentaNextLabel(flow, e) {
  var n = rentaNext(flow, e);
  return n === 'revisado' ? 'Marcar revisado' : n === 'entregado' ? 'Marcar entregado' : 'Reabrir';
}
function rentaCardHtml(rec, num, flow, entrega) {
  var accs = ACCS_POR_TIPO[rec.tipo].map(function (k) {
    var ok = rec.accesorios && rec.accesorios[k];
    return '<span class="badge ' + (ok ? 'b-listo' : 'b-prep') + '">' + (ok ? '✓ ' : '✗ ') + ACCS_LABEL[k] + '</span>';
  }).join(' ');
  var accsHtml = entrega
    ? '<div class="sub">Componentes con los que se recibió:</div>' + ACCS_POR_TIPO[rec.tipo].map(function (k) {
        var ok = rec.accesorios && rec.accesorios[k];
        return '<div class="sub">' + (ok ? '✓ ' : '✗ ') + ACCS_LABEL[k] + '</div>';
      }).join('') +
      '<div class="sub">Checklist de entrega (toca cada componente al entregarlo):</div>' + ACCS_POR_TIPO[rec.tipo].map(function (k) {
        var trajo = rec.accesorios && rec.accesorios[k];
        if (!trajo) return '<div class="sub">✗ ' + ACCS_LABEL[k] + ' (no se recibió)</div>';
        var ok = rec.entregados && rec.entregados[k];
        return '<div class="sub"><button class="btn-ghost" data-entrega-acc="' + k + '" data-id="' + rec.id + '">' + (ok ? '☑ ' : '☐ ') + ACCS_LABEL[k] + '</button></div>';
      }).join('')
    : '<div class="sub">Accesorios: ' + accs + '</div>';
  var extras = [];
  if (rec.capacidad) extras.push('Capacidad: ' + esc(rec.capacidad));
  if (rec.cpu) extras.push('CPU: ' + esc(rec.cpu));
  return '<div class="card">' +
    '<h2>Equipo #' + num + ' — ' + esc(rec.tipo) + ' ' + esc(rec.modelo || '') + '</h2>' +
    '<div class="sub">No. de inventario de renta: <b>' + esc(rec.inventario || '—') + '</b></div>' +
    (extras.length ? '<div class="sub">' + extras.join(' · ') + '</div>' : '') +
    accsHtml +
    '<div class="sub">' + (entrega ? 'Cómo se recibió: ' : '') + (rec.sinDanos ? '✅ Sin daños' : '⚠️ Con daños' + (rec.danos ? ': ' + esc(rec.danos) : '')) + '</div>' +
    (rec.obs ? '<div class="sub">Obs: ' + esc(rec.obs) + '</div>' : '') +
    (rec.fotoDanos ? '<img class="foto-serie" src="' + rec.fotoDanos + '" alt="Foto de daños">' : '') +
    (rec.danosIA ? '<div class="sub">🤖 Daños según la IA: ' + esc(rec.danosIA) + '</div>' : '') +
    (aiAnswers['renta-' + rec.id] ? '<div class="ai-answer">🤖 ' + esc(aiAnswers['renta-' + rec.id]) + '</div>' : '') +
    (rec.recibidoPor ? '<div class="sub">Recibido por: ' + esc(rec.recibidoPor) + '</div>' : '') +
    (rec.entregadoPor ? '<div class="sub">Entregado por: ' + esc(rec.entregadoPor) + '</div>' : '') +
    '<span class="badge ' + rentaEstadoClase(rec.estado) + '">' + rentaEstadoLabel(rec.estado) + '</span>' +
    '<div class="delivered-line">Registrado el ' + fmtDate(rec.createdAt) + '</div>' +
    '<div class="actions">' + (entrega
      ? (rec.estado === 'entregado'
        ? '<button class="btn-ghost" data-renta-reopen="' + rec.id + '">Reabrir</button>'
        : '<button class="btn-green" data-renta-deliver="' + rec.id + '">✅ Marcar entregado</button>')
      : '<button class="btn-green" data-renta-next="' + rec.id + '" data-flow="' + flow + '">' + rentaNextLabel(flow, rec.estado) + '</button>' +
      (flow === 'rec' && rec.fotoDanos ? '<button class="btn-ghost" data-ai-danos="' + rec.id + '">🔍 Revisar daños con IA</button>' : '')) +
    '<button class="btn-danger" data-renta-del="' + rec.id + '">Eliminar</button></div></div>';
}
function renderRenta(flow) {
  var list = rentaList(flow);
  var box = document.getElementById(flow === 'rec' ? 'list-rec' : 'list-for');
  if (!list.length) {
    box.innerHTML = '<div class="empty">No hay equipos de renta aquí todavía.</div>';
  } else {
    box.innerHTML = list.map(function (rec, i) { return rentaCardHtml(rec, i + 1, flow); }).join('');
  }
}
function entregaCola() {
  var orden = { iPad: 0, Laptop: 1, PC: 2 };
  var list = state.renta.slice();
  // Entregados solo los ve el admin; a los usuarios ya no les aparecen.
  if (CLOUD_ENABLED && cloudRole !== 'admin') list = list.filter(function (r) { return r.estado !== 'entregado'; });
  return list.sort(function (a, b) { return (orden[a.tipo] - orden[b.tipo]) || (a.createdAt - b.createdAt); });
}
function renderEntrega() {
  var box = document.getElementById('list-for');
  var cola = entregaCola();
  if (!cola.length) {
    var msg = (CLOUD_ENABLED && cloudRole !== 'admin' && state.renta.length)
      ? 'No hay equipos por entregar. Los ya entregados solo los ve el administrador.'
      : 'No hay equipos de renta todavía. Agrégalos en Recibir renta.';
    box.innerHTML = '<div class="empty">' + msg + '</div>';
    return;
  }
  var idx = cola.findIndex(function (r) { return r.id === state.entregaActual; });
  if (idx === -1) {
    idx = cola.findIndex(function (r) { return r.estado !== 'entregado'; });
    if (idx === -1) idx = cola.length - 1;
    state.entregaActual = cola[idx].id;
    save();
  }
  var rec = cola[idx];
  var pendientes = cola.filter(function (r) { return r.estado !== 'entregado'; }).length;
  var html = '<div class="sub">📦 Entrega ' + (idx + 1) + ' de ' + cola.length + ' · ' + pendientes + ' por entregar</div>';
  html += rentaCardHtml(rec, idx + 1, 'for', true);
  html += '<div class="actions">' +
    '<button class="btn-ghost" data-entrega-nav="prev"' + (idx === 0 ? ' disabled' : '') + '>← Anterior</button>' +
    '<button class="btn-ghost" data-entrega-nav="next"' + (idx === cola.length - 1 ? ' disabled' : '') + '>Siguiente →</button></div>';
  box.innerHTML = html;
}
function renderAccs(flow) {
  var tipo = document.getElementById('fR-' + flow + '-tipo').value;
  document.getElementById('accs-' + flow).innerHTML = (ACCS_POR_TIPO[tipo] || []).map(function (k) {
    return '<label><input type="checkbox" id="acc-' + flow + '-' + k + '"> ' + ACCS_LABEL[k] + '</label>';
  }).join('');
}
function updateRentaForm(flow) {
  var tipo = document.getElementById('fR-' + flow + '-tipo').value;
  document.getElementById('wrap-' + flow + '-cap').style.display = (tipo === 'iPad' || tipo === 'PC') ? '' : 'none';
  document.getElementById('wrap-' + flow + '-cpu').style.display = tipo === 'PC' ? '' : 'none';
  renderAccs(flow);
}
function saveRenta(flow) {
  var g = function (id) { return document.getElementById(id).value.trim(); };
  var tipo = g('fR-' + flow + '-tipo');
  var accs = {};
  (ACCS_POR_TIPO[tipo] || []).forEach(function (k) {
    var el = document.getElementById('acc-' + flow + '-' + k);
    accs[k] = !!(el && el.checked);
  });
  var rec = {
    id: uid(), createdAt: Date.now(), flujo: flow, tipo: tipo,
    modelo: g('fR-' + flow + '-modelo'), inventario: g('fR-' + flow + '-inv'),
    capacidad: g('fR-' + flow + '-cap'), cpu: g('fR-' + flow + '-cpu'),
    accesorios: accs, sinDanos: document.getElementById('fR-' + flow + '-sindanos').checked,
    danos: g('fR-' + flow + '-danos'), obs: g('fR-' + flow + '-obs'),
    fotoDanos: flow === 'rec' ? (window._fotoDanos || null) : null, danosIA: '',
    estado: flow === 'rec' ? 'recibido' : 'en formateo',
    recibidoPor: technicianName(), entregadoPor: ''
  };
  if (!rec.modelo && !rec.inventario) { alert('Pon al menos el modelo o el número de inventario de renta.'); return; }
  state.renta.push(rec);
  cloudUpsert(rec);
  save();
  ['modelo', 'inv', 'cap', 'cpu', 'danos', 'obs'].forEach(function (f) { document.getElementById('fR-' + flow + '-' + f).value = ''; });
  if (flow === 'rec') { window._fotoDanos = null; document.getElementById('fotoDanosPreview').innerHTML = ''; document.getElementById('fFotoDanos').value = ''; }
  document.getElementById('fR-' + flow + '-sindanos').checked = false;
  updateRentaForm(flow);
  render();
}

function todosListHtml(list) {
  var activos = list.filter(function (p) { return statusOf(p) !== 'entregado'; });
  var entregados = list.filter(function (p) { return statusOf(p) === 'entregado'; });
  var html = activos.map(cardHtml).join('');
  if (!entregados.length) return html;
  var totalPages = Math.max(1, Math.ceil(entregados.length / 5));
  if (todosPage >= totalPages) todosPage = totalPages - 1;
  if (todosPage < 0) todosPage = 0;
  var page = entregados.slice(todosPage * 5, todosPage * 5 + 5);
  html += '<div class="sub" style="margin-top:14px"><b>Equipos entregados (' + entregados.length + ')</b> — toca uno para verlo completo</div>';
  html += page.map(function (p) {
    if (window._expandedId === p.id) return '<button class="btn-ghost" data-collapse="' + p.id + '">▲ Contraer</button>' + cardHtml(p);
    return '<div class="todo-row" data-expand="' + p.id + '"><b>' + esc((p.equipo.marca || 'Equipo') + ' ' + (p.equipo.modelo || '')) + '</b> · ' + esc(p.usuario.nombre || 'sin usuario') + ' · Entregado el ' + fmtDate(p.deliveredAt) + '</div>';
  }).join('');
  if (totalPages > 1) {
    html += '<div class="row" style="margin-top:10px">' +
      '<button class="btn-ghost" data-todos-prev' + (todosPage === 0 ? ' disabled' : '') + '>← Anterior</button>' +
      '<span class="pct">Página ' + (todosPage + 1) + ' de ' + totalPages + '</span>' +
      '<button class="btn-ghost" data-todos-next' + (todosPage === totalPages - 1 ? ' disabled' : '') + '>Siguiente →</button></div>';
  }
  return html;
}

function render() {
  document.getElementById('tabEquipo').hidden = !CLOUD_ENABLED;
  var counts = { preparacion: 0, listo: 0, entregado: 0 };
  visiblePreps().forEach(function (p) { counts[statusOf(p)]++; });
  document.getElementById('cPrep').textContent = counts.preparacion;
  document.getElementById('cListo').textContent = counts.listo;
  document.getElementById('cEntr').textContent = counts.entregado;
  document.getElementById('shareBar').hidden = filterStatus !== 'entregado';
  var btnDet = document.getElementById('btnDetectar');
  if (btnDet) btnDet.hidden = !window.Desktop;

  var list = currentList();

  var box = document.getElementById('list');
  if (!list.length) {
    box.innerHTML = '<div class="empty">No hay equipos aquí todavía.<br>Agrega uno con “Nuevo equipo por preparar”.</div>';
  } else if (filterStatus === 'todos') {
    box.innerHTML = todosListHtml(list);
  } else {
    box.innerHTML = list.map(cardHtml).join('');
  }
  renderTemplate();
  renderRenta('rec');
  renderEntrega();
}

function cardHtml(p) {
  var st = statusOf(p);
  var pct = progress(p);
  var items = allItems(p);
  var locked = !!p.deliveredAt;
  var groupsHtml = GROUP_ORDER.map(function (g) {
    var gi = items.filter(function (it) { return it.group === g; });
    if (!gi.length) return '';
    var rows = gi.map(function (it) {
      var checked = !!p.checks[it.id];
      var del = it.extra ? '<button class="x" data-del-extra="' + it.id + '" data-prep="' + p.id + '" title="Quitar punto">×</button>' : '';
      if (it.options) {
        var opts = it.options.map(function (o) {
          var sel = p.checks[it.id] === o;
          return '<button class="chip' + (sel ? ' on' : '') + '" data-choice="' + it.id + '" data-prep="' + p.id + '" data-value="' + esc(o) + '"' + (locked ? ' disabled' : '') + '>' + esc(o) + '</button>';
        }).join(' ');
        var hint = checked ? '' : ' <span class="choice-hint">⚠️ Elige una opción</span>';
        return '<div class="item' + (checked ? ' done' : '') + '" style="flex-wrap:wrap">' +
          '<label>' + esc(it.text) + '</label> ' + opts + hint + del + '</div>';
      }
      return '<div class="item' + (checked ? ' done' : '') + '">' +
        '<input type="checkbox" data-check="' + it.id + '" data-prep="' + p.id + '"' +
        (checked ? ' checked' : '') + (locked ? ' disabled' : '') + '>' +
        '<label>' + esc(it.text) + '</label>' + del + '</div>';
    }).join('');
    return '<div class="group"><h3>' + GROUPS[g] + '</h3>' + rows + '</div>';
  }).join('');

  var actions = '';
  if (st === 'preparacion') actions += '<button class="btn-green" data-ready="' + p.id + '">Listo</button>';
  if (st === 'listo') actions += '<button class="btn-green" data-deliver="' + p.id + '">Entregado</button>';
  if (st === 'listo' && p.readyAt && pct < 100) actions += '<button class="btn-ghost" data-unready="' + p.id + '">Quitar listo</button>';
  if (st === 'entregado') actions += '<button class="btn-ghost" data-reopen="' + p.id + '">Reabrir</button>';
  if (!locked) actions += '<button class="btn-ghost" data-add-extra="' + p.id + '">+ Punto extra</button>';
  if (cloudRole === 'admin') actions += '<button class="btn-dark" data-pdf="' + p.id + '">PDF / Compartir</button>';
  if (st !== 'entregado') actions += '<button class="btn-ghost" data-ai-falta="' + p.id + '">✨ ¿Qué falta?</button>';
  if (st === 'entregado') {
    actions += '<button class="btn-ghost" data-xlsx="' + p.id + '">Exportar a Excel</button>';
    actions += '<button class="btn-ghost" data-wa="' + p.id + '">Enviar datos por WhatsApp</button>';
    actions += '<button class="btn-ghost" data-ai-wa="' + p.id + '">✨ Resumen con IA</button>';
    actions += '<button class="btn-ghost" data-mail="' + p.id + '">Enviar por correo</button>';
  }
  if (cloudRole === 'admin') actions += '<button class="btn-ghost" data-reassign="' + p.id + '">Reasignar</button>';
  if (cloudRole === 'admin') actions += '<button class="btn-danger" data-del-prep="' + p.id + '">Eliminar</button>';

  var deliveredLine = p.deliveredAt ? '<div class="delivered-line">Entregado el ' + fmtDate(p.deliveredAt) + '</div>' : '';
  var detNote = (p.autoDetectado && p.autoDetectado.length)
    ? '<div class="sub">Puntos marcados por el detector: ' + esc(detectedNames(p.checks, p.autoDetectado).join(', ')) + '</div>' : '';
  var reassignLine = (p.reasignaciones && p.reasignaciones.length)
    ? '<div class="sub">Reasignaciones: ' + esc(reassignText(p)) + '</div>' : '';
  var reassignForm = (window._reassignFor === p.id)
    ? '<div class="row" style="margin-top:10px"><input id="reDe" placeholder="Era de..." value="' + esc(p.usuario.nombre || '') + '">' +
      '<input id="reA" placeholder="Se reasigna a...">' +
      '<button class="btn-dark" data-save-reassign="' + p.id + '">Guardar reasignación</button></div>' : '';
  var extraForm = (!locked && window._extraFor === p.id)
    ? '<div class="row" style="margin-top:10px"><input id="extraText" placeholder="Punto extra para este equipo...">' +
      '<select id="extraGroup" style="max-width:130px"><option value="hardware">Hardware</option><option value="software">Software</option><option value="datos">Datos usuario</option></select>' +
      '<button class="btn-dark" data-save-extra="' + p.id + '">Agregar</button></div>' : '';

  return '<div class="card">' +
    '<h2>' + esc(p.equipo.marca || 'Equipo') + ' ' + esc(p.equipo.modelo || '') + '</h2>' +
    '<div class="sub">' + esc(p.equipo.tipo) + ' · Serie: ' + esc(p.equipo.serie || '—') + ' · Inv: ' + esc(p.equipo.inventario || '—') + (p.equipo.hostname ? ' · Host: ' + esc(p.equipo.hostname) : '') + '</div>' +
    (p.equipo.fotoSerie ? '<img class="foto-serie" src="' + p.equipo.fotoSerie + '" alt="Foto del número de serie" title="Toca para ampliar">' : '') +
    '<div class="sub">Usuario: <b>' + esc(p.usuario.nombre || '—') + '</b>' +
    (p.usuario.area ? ' · ' + esc(p.usuario.area) : '') +
    (p.usuario.correo ? '<br>' + esc(p.usuario.correo) : '') +
    (p.tecnico ? '<br>Analista: ' + esc(p.tecnico) : '') + '</div>' +
    '<span class="badge ' + statusClass(st) + '">' + statusLabel(st) + '</span>' +
    '<div class="bar"><i style="width:' + pct + '%"></i></div>' +
    '<div class="pct">' + pct + '% completado</div>' + deliveredLine + reassignLine + detNote +
    groupsHtml + extraForm + reassignForm +
    (aiAnswers[p.id] ? '<div class="ai-answer">🤖 ' + esc(aiAnswers[p.id]) + '</div>' : '') +
    '<div class="actions">' + actions + '</div>' +
    '</div>';
}

function renderTemplate() {
  var box = document.getElementById('tplList');
  box.innerHTML = state.template.map(function (t) {
    return '<div class="tpl-item"><span class="tag">' + GROUPS[t.group] + '</span><span>' + esc(t.text) + (t.reassignOnly ? ' <i>(solo reasignación)</i>' : '') + '</span>' +
      '<button class="x" data-del-tpl="' + t.id + '">×</button></div>';
  }).join('');
}

document.getElementById('search').addEventListener('input', function (e) { searchText = e.target.value; render(); });
function setFilter(f) {
  filterStatus = f;
  todosPage = 0;
  window._expandedId = null;
  document.querySelectorAll('#chips .chip').forEach(function (c) { c.classList.toggle('on', c.getAttribute('data-f') === f); });
}

document.getElementById('chips').addEventListener('click', function (e) {
  var b = e.target.closest('[data-f]');
  if (!b) return;
  setFilter(b.getAttribute('data-f'));
  render();
});

// El boton Guardar solo se habilita cuando ya hay datos del equipo.
function formReady() {
  var v = function (id) { return document.getElementById(id).value.trim(); };
  return !!(v('fModelo') || v('fSerie') || v('fUser'));
}
function updateSaveBtn() {
  var ok = formReady();
  document.getElementById('btnAdd').disabled = !ok;
  document.getElementById('saveHint').textContent = ok
    ? 'Datos listos: toca Guardar equipo para crear su checklist.'
    : 'Completa al menos el modelo, el número de serie o el nombre del usuario para guardar.';
}
['fModelo', 'fSerie', 'fUser'].forEach(function (id) {
  document.getElementById(id).addEventListener('input', updateSaveBtn);
});
updateSaveBtn();

// Foto del numero de serie: camara o galeria, reducida a max 1024 px para no llenar el telefono.
window._fotoSerie = null;
// Reduce una foto (data URL) a max px y JPEG con la calidad dada.
function reducePhoto(dataUrl, max, quality, done) {
  var img = new Image();
  img.onload = function () {
    var w = img.width, h = img.height;
    if (w > max || h > max) {
      var k = Math.min(max / w, max / h);
      w = Math.round(w * k); h = Math.round(h * k);
    }
    var cv = document.createElement('canvas');
    cv.width = w; cv.height = h;
    cv.getContext('2d').drawImage(img, 0, 0, w, h);
    done(cv.toDataURL('image/jpeg', quality));
  };
  img.src = dataUrl;
}
function setFotoSerie(dataUrl) {
  window._fotoSerie = dataUrl;
  document.getElementById('fotoSeriePreview').innerHTML =
    '<img src="' + window._fotoSerie + '" alt="Foto del número de serie">' +
    '<button type="button" class="btn-ghost" id="btnQuitarFoto" style="margin-top:6px">Quitar foto</button>';
  document.getElementById('btnQuitarFoto').addEventListener('click', function () {
    window._fotoSerie = null;
    document.getElementById('fotoSeriePreview').innerHTML = '';
    document.getElementById('fFotoSerie').value = '';
  });
}
// Abre el menú nativo (Tomar foto / Elegir de la galería); si el plugin de
// cámara no está, usa el selector de archivos del sistema.
function pickPhoto(max, quality, onDone) {
  var Cam = window.Capacitor && window.Capacitor.Plugins && window.Capacitor.Plugins.Camera;
  if (Cam && Cam.getPhoto) {
    Cam.getPhoto({ quality: 90, allowEditing: false, resultType: 'dataUrl', source: 'PROMPT' }).then(function (photo) {
      if (photo && photo.dataUrl) reducePhoto(photo.dataUrl, max, quality, onDone);
    }).catch(function () { /* el usuario canceló: no se hace nada */ });
    return true;
  }
  return false;
}
document.getElementById('btnFotoSerie').addEventListener('click', function () {
  if (!pickPhoto(1024, 0.82, setFotoSerie)) document.getElementById('fFotoSerie').click();
});
document.getElementById('fFotoSerie').addEventListener('change', function (e) {
  var file = e.target.files && e.target.files[0];
  if (!file) return;
  var reader = new FileReader();
  reader.onload = function (ev) { reducePhoto(ev.target.result, 1024, 0.82, setFotoSerie); };
  reader.readAsDataURL(file);
});

// Foto de daños de renta: camara o galeria, reducida a max 800 px.
window._fotoDanos = null;
function setFotoDanos(dataUrl) {
  window._fotoDanos = dataUrl;
  document.getElementById('fotoDanosPreview').innerHTML =
    '<img src="' + window._fotoDanos + '" alt="Foto de daños">' +
    '<button type="button" class="btn-ghost" id="btnQuitarFotoDanos" style="margin-top:6px">Quitar foto</button>';
  document.getElementById('btnQuitarFotoDanos').addEventListener('click', function () {
    window._fotoDanos = null;
    document.getElementById('fotoDanosPreview').innerHTML = '';
    document.getElementById('fFotoDanos').value = '';
  });
}
document.getElementById('btnFotoDanos').addEventListener('click', function () {
  if (!pickPhoto(800, 0.75, setFotoDanos)) document.getElementById('fFotoDanos').click();
});
document.getElementById('fFotoDanos').addEventListener('change', function (e) {
  var file = e.target.files && e.target.files[0];
  if (!file) return;
  var reader = new FileReader();
  reader.onload = function (ev) { reducePhoto(ev.target.result, 800, 0.75, setFotoDanos); };
  reader.readAsDataURL(file);
});

// Lee el numero de serie del texto que devuelve el OCR.
function extractSerial(text) {
  var STOP = { SERIAL: 1, PRODUCT: 1, MODEL: 1, NUMBER: 1, WARRANTY: 1, CHINA: 1, RATED: 1, MADE: 1, PROBOOK: 1 };
  function clean(tok) { return String(tok || '').toUpperCase().replace(/[^A-Z0-9]/g, ''); }
  function isSerial(tok) {
    return tok.length >= 6 && !STOP[tok] && /[A-Z]/.test(tok) && /[0-9]/.test(tok);
  }
  function best(tokens) {
    var good = tokens.map(clean).filter(isSerial);
    good.sort(function (a, b) { return b.length - a.length; });
    return good.length ? good[0] : null;
  }
  var lines = String(text || '').split(/\n/);
  for (var i = 0; i < lines.length; i++) {
    if (/serial|s\s*\/\s*n/i.test(lines[i])) {
      var hit = best(lines[i].match(/[A-Z0-9][A-Z0-9\-#]{5,}/gi) || []);
      if (hit) return hit;
    }
  }
  return best(String(text || '').match(/[A-Z0-9]{6,20}/gi) || []);
}

document.getElementById('btnEscanear').addEventListener('click', function () {
  var status = document.getElementById('ocrStatus');
  var btn = document.getElementById('btnEscanear');
  if (!window._fotoSerie) { status.textContent = 'Primero toma o elige la foto del número de serie.'; return; }
  if (typeof Tesseract === 'undefined') { status.textContent = 'El lector de texto no cargó, cierra y vuelve a abrir la app.'; return; }
  btn.disabled = true;
  status.textContent = 'Leyendo la foto...';
  Tesseract.recognize(window._fotoSerie, 'eng', {
    workerPath: 'ocr/worker.min.js',
    corePath: 'ocr/tesseract-core.wasm.js',
    langPath: 'ocr/lang',
    // aapt2 descomprime los .gz de assets al empaquetar: en el APK el
    // archivo queda como eng.traineddata (sin .gz), por eso gzip:false.
    gzip: false,
    cacheMethod: 'none',
    logger: function (m) {
      if (m.status === 'recognizing text' && typeof m.progress === 'number') {
        status.textContent = 'Leyendo la foto... ' + Math.round(m.progress * 100) + '%';
      }
    }
  }).then(function (result) {
    var serie = extractSerial(result.data.text || '');
    if (serie) {
      document.getElementById('fSerie').value = serie;
      updateSaveBtn();
      status.textContent = 'Leído: ' + serie + ' — revísalo y corrígelo si hace falta.';
    } else {
      status.textContent = 'No se pudo leer el número de serie, escríbelo a mano.';
    }
    btn.disabled = false;
  }).catch(function () {
    status.textContent = 'No se pudo leer la foto, intenta con otra foto con mejor luz.';
    btn.disabled = false;
  });
});

// Botones bonitos del menu: abren un panel y cierran el otro.
function togglePanel(id) {
  var show = document.getElementById(id);
  var wasHidden = show.hidden;
  ['newBox', 'tplBox', 'reBox', 'detBox'].forEach(function (p) { if (p !== id) document.getElementById(p).hidden = true; });
  show.hidden = !wasHidden;
  if (!show.hidden) show.scrollIntoView({ behavior: 'smooth', block: 'start' });
}
document.getElementById('btnShowNew').addEventListener('click', function () { window._detectedChecks = null; window._detectedDetalles = null; togglePanel('newBox'); });
document.getElementById('btnShowTpl').addEventListener('click', function () { togglePanel('tplBox'); });
function fillReEquipo() {
  var sel = document.getElementById('fReEquipo');
  var opts = visiblePreps().slice().sort(function (a, b) { return b.createdAt - a.createdAt; }).map(function (p) {
    return '<option value="' + p.id + '">' + esc((p.equipo.marca || 'Equipo') + ' ' + (p.equipo.modelo || '')) + ' · Serie: ' + esc(p.equipo.serie || '—') + ' · ' + esc(p.usuario.nombre || 'sin usuario') + '</option>';
  }).join('');
  sel.innerHTML = '<option value="">— Elige el equipo —</option>' + opts + '<option value="__nuevo__">Otro equipo (escribir datos)</option>';
  document.getElementById('reEquipoNuevo').hidden = true;
  document.getElementById('fReDe').value = '';
  document.getElementById('fReA').value = '';
}
document.getElementById('btnShowRe').addEventListener('click', function () { fillReEquipo(); togglePanel('reBox'); });
document.getElementById('btnShowDet').addEventListener('click', function () { renderDetectados(); togglePanel('detBox'); });
document.getElementById('btnDetectar').addEventListener('click', function () {
  var btn = document.getElementById('btnDetectar');
  if (!window.Desktop || !window.Desktop.detect) { alert('La detección solo funciona en la app de escritorio.'); return; }
  if (!cloudUser) { alert('Inicia sesión para reportar el equipo detectado.'); return; }
  var oldHtml = btn.innerHTML;
  btn.disabled = true;
  btn.innerHTML = '<span class="ic">&#128187;</span><span>Detectando software...</span>';
  var p;
  try { p = Promise.resolve(window.Desktop.detect()); } catch (e) { btn.disabled = false; btn.innerHTML = oldHtml; alert('No se pudo detectar el equipo.'); return; }
  p.then(function (info) {
    if (!window.Cloud || !window.Cloud.reportDetected) throw new Error('sin-nube');
    var data = Object.assign({}, info || {});
    data.detectadoPor = technicianName();
    return window.Cloud.reportDetected(data);
  }).then(function () { alert('Equipo detectado, ya aparece en los teléfonos'); }).catch(function (e) { alert('No se pudo detectar el equipo.' + (e && e.message ? ' ' + e.message : '')); }).then(function () { btn.disabled = false; btn.innerHTML = oldHtml; });
});
document.getElementById('detList').addEventListener('click', function (e) {
  var t = e.target;
  var use = t.closest('[data-det-use]');
  var del = t.closest('[data-det-del]');
  if (!use && !del) return;
  var id = (use || del).getAttribute(use ? 'data-det-use' : 'data-det-del');
  if (use) {
    var d = detectados.find(function (x) { return String(x.id) === String(id); });
    if (!d) return;
    document.getElementById('fTipo').value = d.tipo || 'Desktop';
    document.getElementById('fMarca').value = d.marca || '';
    document.getElementById('fModelo').value = d.modelo || '';
    document.getElementById('fSerie').value = d.serie || '';
    document.getElementById('fHostname').value = d.hostname || '';
    window._detectedChecks = d.checks || {};
    window._detectedDetalles = d.detalles || {};
    cloudMarkDetectadoUsado(d.id);
    document.getElementById('detBox').hidden = true;
    document.getElementById('newBox').hidden = false;
    updateSaveBtn();
    return;
  }
  if (del) {
    if (!confirm('¿Descartar este equipo detectado?')) return;
    cloudDeleteDetectado(id);
  }
});
document.getElementById('fReEquipo').addEventListener('change', function () {
  var id = this.value;
  document.getElementById('reEquipoNuevo').hidden = id !== '__nuevo__';
  var p = state.preparations.find(function (x) { return x.id === id; });
  document.getElementById('fReDe').value = p ? (p.usuario.nombre || '') : '';
});
document.getElementById('btnReGuardar').addEventListener('click', function () {
  var id = document.getElementById('fReEquipo').value;
  var a = document.getElementById('fReA').value.trim();
  var de = document.getElementById('fReDe').value.trim();
  if (!id) { alert('Elige el equipo a reasignar.'); return; }
  if (!a) { alert('Pon a quién se reasigna el equipo.'); return; }
  if (id === '__nuevo__') {
    var v = function (x) { return document.getElementById(x).value.trim(); };
    var prep = {
      id: uid(), createdAt: Date.now(), deliveredAt: null, readyAt: null, checks: {}, extraItems: [],
      reasignaciones: [{ de: de, a: a, fecha: Date.now(), analista: technicianName() }],
      equipo: { tipo: v('fReTipo'), marca: v('fReMarca'), modelo: v('fReModelo'), serie: v('fReSerie'), inventario: v('fReInv'), hostname: v('fReHostname'), fotoSerie: null },
      usuario: { nombre: a, area: '', correo: '' },
      tecnico: technicianName()
    };
    if (!prep.equipo.modelo && !prep.equipo.serie && !prep.usuario.nombre) { alert('Pon al menos el modelo, la serie o el nombre del usuario.'); return; }
    state.preparations.push(prep);
  } else {
    var prep = state.preparations.find(function (x) { return x.id === id; });
    if (!prep) { alert('Ese equipo ya no está en la lista.'); return; }
    doReassign(prep, de, a);
  }
  cloudUpsertPrep(prep);
  save();
  ['fReDe', 'fReA', 'fReMarca', 'fReModelo', 'fReSerie', 'fReInv'].forEach(function (x) { document.getElementById(x).value = ''; });
  document.getElementById('reBox').hidden = true;
  setFilter('preparacion');
  render();
});

// Compartir en grupo: los equipos que se ven en la lista.
document.getElementById('btnXlsxAll').addEventListener('click', function () { shareXlsx(currentList(), 'equipos-checklist.xlsx'); });
document.getElementById('btnWaAll').addEventListener('click', function () { shareWhatsApp(currentList()); });
document.getElementById('btnMailAll').addEventListener('click', function () { shareMail(currentList(), 'equipos-checklist.xlsx'); });

document.getElementById('btnAdd').addEventListener('click', function () {
  var v = function (id) { return document.getElementById(id).value.trim(); };
  var det = filterDetectedChecks(window._detectedChecks || {});
  var prep = {
    id: uid(), createdAt: Date.now(), deliveredAt: null, readyAt: null, checks: det.checks, autoDetectado: det.ids, extraItems: [], reasignaciones: [],
    equipo: { tipo: v('fTipo'), marca: v('fMarca'), modelo: v('fModelo'), serie: v('fSerie'), inventario: v('fInv'), hostname: v('fHostname'), fotoSerie: window._fotoSerie || null },
    usuario: { nombre: v('fUser'), area: v('fArea'), correo: v('fCorreo') },
    tecnico: v('fTec') || technicianName()
  };
  if (!prep.equipo.modelo && !prep.equipo.serie && !prep.usuario.nombre) {
    alert('Pon al menos el modelo, la serie o el nombre del usuario.');
    return;
  }
  state.preparations.push(prep);
  window._detectedChecks = null;
  window._detectedDetalles = null;
  cloudUpsertPrep(prep);
  save();
  ['fMarca', 'fModelo', 'fSerie', 'fInv', 'fHostname', 'fTec', 'fUser', 'fArea', 'fCorreo'].forEach(function (id) { document.getElementById(id).value = ''; });
  prefillTecnico();
  window._fotoSerie = null;
  document.getElementById('fotoSeriePreview').innerHTML = '';
  document.getElementById('fFotoSerie').value = '';
  updateSaveBtn();
  document.getElementById('newBox').hidden = true;
  setFilter('preparacion');
  render();
});

function doReassign(prep, de, a) {
  if (!prep.reasignaciones) prep.reasignaciones = [];
  prep.reasignaciones.push({ de: de || prep.usuario.nombre || '', a: a, fecha: Date.now(), analista: technicianName() });
  prep.usuario.nombre = a; prep.usuario.area = ''; prep.usuario.correo = '';
  prep.deliveredAt = null; prep.readyAt = null;
}
document.getElementById('list').addEventListener('click', function (e) {
  var t = e.target;
  if (t.classList && t.classList.contains('foto-serie')) { t.classList.toggle('big'); return; }
  var q = function (attr) { var el = t.closest('[' + attr + ']'); return el ? el.getAttribute(attr) : null; };
  var prepId = q('data-prep') || q('data-deliver') || q('data-ready') || q('data-unready') || q('data-reopen') || q('data-add-extra') || q('data-del-prep') || q('data-save-extra') || q('data-pdf') || q('data-xlsx') || q('data-wa') || q('data-mail') || q('data-reassign') || q('data-save-reassign') || q('data-expand') || q('data-collapse') || q('data-choice') || q('data-ai-falta') || q('data-ai-wa');
  var prep = state.preparations.find(function (p) { return p.id === prepId; });

  if (t.hasAttribute('data-todos-next') || t.hasAttribute('data-todos-prev')) {
    var nEnt = currentList().filter(function (p) { return statusOf(p) === 'entregado'; }).length;
    var totalPg = Math.max(1, Math.ceil(nEnt / 5));
    todosPage += t.hasAttribute('data-todos-next') ? 1 : -1;
    if (todosPage < 0) todosPage = 0;
    if (todosPage > totalPg - 1) todosPage = totalPg - 1;
    render(); return;
  }
  if (t.hasAttribute('data-expand') && prep) { window._expandedId = prep.id; render(); return; }
  if (t.hasAttribute('data-collapse') && prep) { window._expandedId = null; render(); return; }
  if (t.hasAttribute('data-choice') && prep) {
    var cid = t.getAttribute('data-choice');
    var cval = t.getAttribute('data-value');
    prep.checks[cid] = (prep.checks[cid] === cval) ? false : cval;
    cloudUpsertPrep(prep);
    save(); render(); return;
  }
  if (t.hasAttribute('data-pdf') && prep) { sharePdf(prep); return; }
  if (t.hasAttribute('data-xlsx') && prep) { shareXlsx([prep], 'equipo-' + (cleanName(prep.equipo.marca) || 'equipo') + '-' + (cleanName(prep.equipo.modelo) || '') + '.xlsx'); return; }
  if (t.hasAttribute('data-wa') && prep) { shareWhatsApp([prep]); return; }
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
  }
  if (t.hasAttribute('data-mail') && prep) { shareMail([prep], 'equipo-' + (cleanName(prep.equipo.marca) || 'equipo') + '-' + (cleanName(prep.equipo.modelo) || '') + '.xlsx'); return; }
  if (t.hasAttribute('data-reassign') && prep) { window._reassignFor = (window._reassignFor === prep.id ? null : prep.id); render(); return; }
  if (t.hasAttribute('data-save-reassign') && prep) {
    var reDe = document.getElementById('reDe').value.trim();
    var reA = document.getElementById('reA').value.trim();
    if (!reA) { alert('Pon a quién se reasigna el equipo.'); return; }
    doReassign(prep, reDe, reA);
    window._reassignFor = null;
    cloudUpsertPrep(prep);
    save(); setFilter(statusOf(prep)); render(); return;
  }
  if (t.hasAttribute('data-deliver') && prep) { prep.deliveredAt = Date.now(); cloudUpsertPrep(prep); save(); setFilter('entregado'); render(); return; }
  if (t.hasAttribute('data-ready') && prep) { prep.readyAt = Date.now(); cloudUpsertPrep(prep); save(); setFilter('listo'); render(); return; }
  if (t.hasAttribute('data-unready') && prep) { prep.readyAt = null; cloudUpsertPrep(prep); save(); setFilter('preparacion'); render(); return; }
  if (t.hasAttribute('data-reopen') && prep) { prep.deliveredAt = null; cloudUpsertPrep(prep); save(); setFilter(statusOf(prep)); render(); return; }
  if (t.hasAttribute('data-del-prep') && prep) {
    if (confirm('¿Eliminar este equipo y su checklist?')) {
      state.preparations = state.preparations.filter(function (p) { return p.id !== prep.id; });
      cloudDeletePrep(prep.id);
      save(); render();
    }
    return;
  }
  if (t.hasAttribute('data-add-extra') && prep) { window._extraFor = (window._extraFor === prep.id ? null : prep.id); render(); return; }
  if (t.hasAttribute('data-save-extra') && prep) {
    var txt = document.getElementById('extraText').value.trim();
    if (!txt) return;
    prep.extraItems.push({ id: uid(), group: document.getElementById('extraGroup').value, text: txt });
    window._extraFor = null;
    cloudUpsertPrep(prep);
    save(); render(); return;
  }
  if (t.hasAttribute('data-del-extra') && prep) {
    var xid = t.getAttribute('data-del-extra');
    prep.extraItems = prep.extraItems.filter(function (x) { return x.id !== xid; });
    delete prep.checks[xid];
    cloudUpsertPrep(prep);
    save(); render(); return;
  }
});
document.getElementById('list').addEventListener('change', function (e) {
  var t = e.target;
  if (!t.hasAttribute('data-check')) return;
  var prep = state.preparations.find(function (p) { return p.id === t.getAttribute('data-prep'); });
  if (!prep) return;
  prep.checks[t.getAttribute('data-check')] = t.checked;
  cloudUpsertPrep(prep);
  save(); render();
});

document.getElementById('tplAdd').addEventListener('click', function () {
  var txt = document.getElementById('tplText').value.trim();
  if (!txt) return;
  state.template.push({ id: uid(), group: document.getElementById('tplGroup').value, text: txt });
  document.getElementById('tplText').value = '';
  save(); render();
});
document.getElementById('tplList').addEventListener('click', function (e) {
  var b = e.target.closest('[data-del-tpl]');
  if (!b) return;
  var id = b.getAttribute('data-del-tpl');
  state.template = state.template.filter(function (t) { return t.id !== id; });
  save(); render();
});
document.getElementById('tplReset').addEventListener('click', function () {
  if (confirm('¿Restaurar la plantilla predeterminada?')) {
    state.template = defaultTemplate();
    save(); render();
  }
});

// Equipo: quién está en línea + chat interno.
var presenceList = [];
var chatMessages = [];
var dmMessages = [];
var dmPeer = null;
var teamUsers = [];
var presenceUnsub = null, chatUnsub = null, dmUnsub = null, heartbeatTimer = null;
var ONLINE_MS = 3 * 60 * 1000;
var HEARTBEAT_MS = 120 * 1000;

function tsMs(ts) {
  if (!ts) return 0;
  if (typeof ts.toMillis === 'function') return ts.toMillis();
  if (typeof ts === 'number') return ts;
  if (ts.seconds) return ts.seconds * 1000;
  return 0;
}
function renderEquipo() {
  var box = document.getElementById('onlineList');
  var now = Date.now();
  var online = [], offline = [];
  function pushUser(u, pr) {
    var ms = pr ? tsMs(pr.lastSeen) : 0;
    var isOn = !!ms && (now - ms) <= ONLINE_MS;
    (isOn ? online : offline).push({ u: u, ms: ms, isOn: isOn });
  }
  teamUsers.forEach(function (u) {
    var pr = null;
    presenceList.forEach(function (p) { if (p.uid === u.uid || p.id === u.uid) pr = p; });
    pushUser(u, pr);
  });
  presenceList.forEach(function (p) {
    var seen = teamUsers.some(function (u) { return u.uid === p.uid || u.uid === p.id; });
    if (!seen) pushUser({ uid: p.uid || p.id, nombre: p.nombre || p.uid, rol: p.rol || 'usuario' }, p);
  });
  function row(x) {
    return '<div class="user-row"><span class="dot' + (x.isOn ? ' on' : '') + '"></span><span class="who"><b>' + esc(x.u.nombre || x.u.email || 'Usuario') + '</b>' + (x.u.rol === 'admin' ? ' · Administrador' : '') + (cloudUser && x.u.uid === cloudUser.uid ? ' (tú)' : '') + '</span><span class="st">' + (x.isOn ? 'en línea' : timeAgo(x.ms)) + '</span></div>';
  }
  var html = '';
  if (online.length) html += '<div class="sub">En línea (' + online.length + ')</div>' + online.map(row).join('');
  if (offline.length) html += '<div class="sub" style="margin-top:10px">Sin conexión</div>' + offline.map(row).join('');
  if (!online.length && !offline.length) html = '<div class="empty">No hay usuarios todavía.</div>';
  box.innerHTML = html;
  var isAdmin = cloudRole === 'admin';
  var cb = document.getElementById('chatBox');
  if (!chatMessages.length) { cb.innerHTML = '<div class="empty">Aún no hay mensajes.</div>'; }
  else {
    cb.innerHTML = chatMessages.map(function (m) {
      var mine = cloudUser && m.uid === cloudUser.uid;
      var ms = tsMs(m.createdAt);
      return '<div class="msg' + (mine ? ' mine' : '') + '"><div class="meta">' + esc(m.nombre || 'Usuario') + ' · ' + (ms ? fmtTime(ms) : 'enviando…') + (isAdmin ? ' <button class="msg-del" data-del-chat="' + m.id + '" title="Borrar mensaje">🗑️</button>' : '') + '</div><div class="txt">' + esc(m.texto || '') + '</div></div>';
    }).join('');
    cb.scrollTop = cb.scrollHeight;
  }
  // Chat individual: lista de compañeros o conversación con uno.
  var dl = document.getElementById('dmList');
  var db = document.getElementById('dmBox');
  if (dmPeer) {
    dl.hidden = true; db.hidden = false;
    var peer = null;
    teamUsers.forEach(function (u) { if (u.uid === dmPeer) peer = u; });
    peer = peer || { nombre: 'Usuario' };
    document.getElementById('dmTitle').textContent = peer.nombre || peer.email || 'Usuario';
    var conv = dmMessages.filter(function (m) { return m.participants && m.participants.indexOf(dmPeer) !== -1; })
      .sort(function (a, b) { return tsMs(a.createdAt) - tsMs(b.createdAt); });
    var dcb = document.getElementById('dmChatBox');
    if (!conv.length) { dcb.innerHTML = '<div class="empty">Aún no hay mensajes con ' + esc(peer.nombre || peer.email || 'este usuario') + '.</div>'; }
    else {
      dcb.innerHTML = conv.map(function (m) {
        var mine = cloudUser && m.from === cloudUser.uid;
        var ms = tsMs(m.createdAt);
        return '<div class="msg' + (mine ? ' mine' : '') + '"><div class="meta">' + esc(m.nombre || 'Usuario') + ' · ' + (ms ? fmtTime(ms) : 'enviando…') + (isAdmin ? ' <button class="msg-del" data-del-dm="' + m.id + '" title="Borrar mensaje">🗑️</button>' : '') + '</div><div class="txt">' + esc(m.texto || '') + '</div></div>';
      }).join('');
      dcb.scrollTop = dcb.scrollHeight;
    }
  } else {
    dl.hidden = false; db.hidden = true;
    var others = teamUsers.filter(function (u) { return !cloudUser || u.uid !== cloudUser.uid; });
    if (!others.length) { dl.innerHTML = '<div class="empty">No hay otros usuarios todavía.</div>'; }
    else {
      dl.innerHTML = others.map(function (u) {
        var pr = null;
        presenceList.forEach(function (p) { if (p.uid === u.uid || p.id === u.uid) pr = p; });
        var ms = pr ? tsMs(pr.lastSeen) : 0;
        var isOn = !!ms && (Date.now() - ms) <= ONLINE_MS;
        var last = dmMessages.filter(function (m) { return m.participants && m.participants.indexOf(u.uid) !== -1; })
          .sort(function (a, b) { return tsMs(b.createdAt) - tsMs(a.createdAt); })[0];
        return '<div class="user-row" data-dm-user="' + u.uid + '" style="cursor:pointer"><span class="dot' + (isOn ? ' on' : '') + '"></span><span class="who"><b>' + esc(u.nombre || u.email || 'Usuario') + '</b>' + (u.rol === 'admin' ? ' · Administrador' : '') + '</span><span class="st">' + (last ? esc((last.texto || '').slice(0, 30)) : (isOn ? 'en línea' : timeAgo(ms))) + '</span></div>';
      }).join('');
    }
  }
}
function refreshTeamUsers() {
  if (!window.Cloud || !CLOUD_ENABLED) return;
  window.Cloud.listUsers().then(function (us) { teamUsers = us || []; renderEquipo(); }).catch(function () {});
}
function startEquipo() {
  if (!window.Cloud || !CLOUD_ENABLED || !cloudUser) return;
  stopEquipo();
  var beat = function () { window.Cloud.heartbeat(technicianName(), cloudRole || 'usuario'); };
  beat();
  if (window.Cloud.pruneChat) window.Cloud.pruneChat();
  heartbeatTimer = setInterval(beat, HEARTBEAT_MS);
  presenceUnsub = window.Cloud.subscribePresence(function (docs) { presenceList = docs; if (!document.getElementById('viewEquipo').hidden) renderEquipo(); });
  chatUnsub = window.Cloud.subscribeChat(function (docs) { chatMessages = docs; if (!document.getElementById('viewEquipo').hidden) renderEquipo(); });
  dmUnsub = window.Cloud.subscribeDm(function (docs) { dmMessages = docs; if (!document.getElementById('viewEquipo').hidden) renderEquipo(); });
  refreshTeamUsers();
}
function stopEquipo() {
  if (heartbeatTimer) { clearInterval(heartbeatTimer); heartbeatTimer = null; }
  if (presenceUnsub) { presenceUnsub(); presenceUnsub = null; }
  if (chatUnsub) { chatUnsub(); chatUnsub = null; }
  if (dmUnsub) { dmUnsub(); dmUnsub = null; }
  if (window.Cloud) window.Cloud.clearPresence();
}
function sendChatMsg() {
  if (!window.Cloud || !CLOUD_ENABLED) { alert('El chat necesita conexión a la nube.'); return; }
  var inp = document.getElementById('chatInput');
  var t = inp.value.trim();
  if (!t) return;
  inp.value = '';
  window.Cloud.sendChat(t, technicianName()).catch(function () { alert('No se pudo enviar el mensaje. Revisa tu conexión.'); });
}
document.getElementById('btnChatSend').addEventListener('click', sendChatMsg);
document.getElementById('chatInput').addEventListener('keydown', function (e) { if (e.key === 'Enter') sendChatMsg(); });
function sendDmMsg() {
  if (!window.Cloud || !CLOUD_ENABLED || !dmPeer) return;
  var inp = document.getElementById('dmInput');
  var t = inp.value.trim();
  if (!t) return;
  inp.value = '';
  window.Cloud.sendDm(dmPeer, t, technicianName()).catch(function () { alert('No se pudo enviar el mensaje. Revisa tu conexión.'); });
}
document.getElementById('btnDmSend').addEventListener('click', sendDmMsg);
document.getElementById('dmInput').addEventListener('keydown', function (e) { if (e.key === 'Enter') sendDmMsg(); });
document.getElementById('dmList').addEventListener('click', function (e) {
  var row = e.target.closest('[data-dm-user]');
  if (!row) return;
  dmPeer = row.getAttribute('data-dm-user');
  renderEquipo();
});
document.getElementById('btnDmBack').addEventListener('click', function () { dmPeer = null; renderEquipo(); });
// Moderación: solo el admin ve el botón de borrar; borra el mensaje para todos.
document.getElementById('chatBox').addEventListener('click', function (e) {
  var b = e.target.closest('[data-del-chat]');
  if (!b) return;
  if (!confirm('¿Borrar este mensaje para todos?')) return;
  window.Cloud.deleteChatMessage(b.getAttribute('data-del-chat')).catch(function () { alert('No se pudo borrar el mensaje.'); });
});
document.getElementById('dmChatBox').addEventListener('click', function (e) {
  var b = e.target.closest('[data-del-dm]');
  if (!b) return;
  if (!confirm('¿Borrar este mensaje para los dos?')) return;
  window.Cloud.deleteDmMessage(b.getAttribute('data-del-dm')).catch(function () { alert('No se pudo borrar el mensaje.'); });
});

// Menu de 3 secciones.
function showVista(v) {
  if (v === 'usuarios' && cloudRole !== 'admin') v = 'preparar';
  document.getElementById('viewPreparar').hidden = v !== 'preparar';
  document.getElementById('viewRenta-rec').hidden = v !== 'rec';
  document.getElementById('viewRenta-for').hidden = v !== 'for';
  document.getElementById('viewUsuarios').hidden = v !== 'usuarios';
  document.getElementById('viewEquipo').hidden = v !== 'equipo';
  document.getElementById('viewCuenta').hidden = true;
  document.getElementById('viewBio').hidden = true;
  if (v === 'usuarios') renderUsuarios();
  if (v === 'equipo') { renderEquipo(); refreshTeamUsers(); }
  if (v === 'preparar') prefillTecnico();
  document.querySelectorAll('#tabs .tab').forEach(function (b) { b.classList.toggle('on', b.getAttribute('data-v') === v); });
  window.scrollTo(0, 0);
}
document.getElementById('tabs').addEventListener('click', function (e) {
  var b = e.target.closest('[data-v]');
  if (b) showVista(b.getAttribute('data-v'));
});
// Recibir renta: formulario y lista.
document.getElementById('fR-rec-tipo').addEventListener('change', function () { updateRentaForm('rec'); });
document.getElementById('btnR-rec-add').addEventListener('click', function () { saveRenta('rec'); });
document.getElementById('btnWaRec').addEventListener('click', function () { shareRentaFile('rec', 'wa'); });
document.getElementById('btnMailRec').addEventListener('click', function () { shareRentaFile('rec', 'mail'); });
document.getElementById('btnAbrirRec').addEventListener('click', function () { openXlsxRenta('rec'); });
document.getElementById('list-rec').addEventListener('click', function (e) {
  var t = e.target;
  var q = function (attr) { var el = t.closest('[' + attr + ']'); return el ? el.getAttribute(attr) : null; };
  var id = q('data-renta-next') || q('data-renta-del') || q('data-ai-danos');
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
  if (t.hasAttribute('data-renta-next')) { rec.estado = rentaNext('rec', rec.estado); cloudUpsert(rec); save(); render(); return; }
  if (t.hasAttribute('data-renta-del') && confirm('¿Eliminar este equipo de renta?')) {
    state.renta = state.renta.filter(function (r) { return r.id !== id; });
    cloudDelete(id);
    save(); render();
  }
});
updateRentaForm('rec');
// Entrega Renta: los equipos llegan desde Recibir renta; aquí se revisan y se entregan.
document.getElementById('btnWaFor').addEventListener('click', function () { shareRentaFile('for', 'wa'); });
document.getElementById('btnMailFor').addEventListener('click', function () { shareRentaFile('for', 'mail'); });
document.getElementById('btnAbrirFor').addEventListener('click', function () { openXlsxRenta('for'); });
document.getElementById('list-for').addEventListener('click', function (e) {
  var t = e.target;
  var nav = t.closest('[data-entrega-nav]');
  if (nav) {
    var cola = entregaCola();
    var idx = cola.findIndex(function (r) { return r.id === state.entregaActual; });
    if (idx === -1) idx = 0;
    var sig = nav.getAttribute('data-entrega-nav') === 'prev' ? idx - 1 : idx + 1;
    if (sig >= 0 && sig < cola.length) { state.entregaActual = cola[sig].id; save(); render(); }
    return;
  }
  var q = function (attr) { var el = t.closest('[' + attr + ']'); return el ? el.getAttribute(attr) : null; };
  var accEl = t.closest('[data-entrega-acc]');
  var id = q('data-renta-deliver') || q('data-renta-reopen') || q('data-renta-del') || (accEl ? accEl.getAttribute('data-id') : null);
  if (!id) return;
  var rec = state.renta.find(function (r) { return r.id === id; });
  if (!rec) return;
  if (accEl) {
    var k = accEl.getAttribute('data-entrega-acc');
    rec.entregados = rec.entregados || {};
    rec.entregados[k] = !rec.entregados[k];
    cloudUpsert(rec);
    save(); render(); return;
  }
  if (t.hasAttribute('data-renta-deliver')) {
    rec.estado = 'entregado';
    rec.entregadoPor = technicianName();
    var cola2 = entregaCola();
    var i = cola2.findIndex(function (r) { return r.id === rec.id; });
    var siguiente = null;
    var j;
    for (j = i + 1; j < cola2.length; j++) { if (cola2[j].estado !== 'entregado') { siguiente = cola2[j].id; break; } }
    if (!siguiente) { for (j = 0; j < cola2.length; j++) { if (cola2[j].estado !== 'entregado') { siguiente = cola2[j].id; break; } } }
    state.entregaActual = siguiente || rec.id;
    cloudUpsert(rec);
    save(); render(); return;
  }
  if (t.hasAttribute('data-renta-reopen')) { rec.estado = 'revisado'; rec.entregadoPor = ''; cloudUpsert(rec); save(); render(); return; }
  if (t.hasAttribute('data-renta-del') && confirm('¿Eliminar este equipo de renta?')) {
    state.renta = state.renta.filter(function (r) { return r.id !== id; });
    if (state.entregaActual === id) state.entregaActual = null;
    cloudDelete(id);
    save(); render();
  }
});

// Acceso con huella (biométricos del teléfono + credencial guardada segura).
var BIO_SERVER = 'checklist-soporte';
var bioAvailable = false;
async function bioCheck() {
  try {
    var P = window.Capacitor && window.Capacitor.Plugins;
    if (!P || !P.NativeBiometric) return false;
    var r = await P.NativeBiometric.isAvailable();
    return !!(r && r.isAvailable);
  } catch (e) { return false; }
}
async function bioHasStored() {
  try {
    var P = window.Capacitor && window.Capacitor.Plugins;
    if (!P || !P.NativeBiometric) return false;
    await P.NativeBiometric.getCredentials({ server: BIO_SERVER });
    return true;
  } catch (e) { return false; }
}
async function refreshBioButton() {
  var btn = document.getElementById('btnBiometric');
  if (!btn) return;
  bioAvailable = await bioCheck();
  var stored = bioAvailable ? await bioHasStored() : false;
  btn.hidden = !stored;
  var dis = document.getElementById('btnBioDisable');
  var ena = document.getElementById('btnBioEnable');
  if (dis) dis.hidden = !stored;
  if (ena) ena.hidden = !!stored;
}
async function offerBiometrics(authEmail) {
  try {
    if (localStorage.getItem('checklist-bio-declined') === '1') return;
    if (!await bioCheck()) return;
    if (await bioHasStored()) return;
    if (!sessionPassword) return;
    if (!confirm('¿Activar el acceso con huella en este teléfono para entrar sin escribir tu contraseña?')) {
      localStorage.setItem('checklist-bio-declined', '1');
      return;
    }
    var P = window.Capacitor.Plugins;
    await P.NativeBiometric.verifyIdentity({ reason: 'Activa el acceso con huella para Checklist de Soporte.', title: 'Checklist de Soporte', subtitle: 'Acceso con huella', negativeButtonText: 'Cancelar' });
    await P.NativeBiometric.setCredentials({ username: authEmail, password: sessionPassword, server: BIO_SERVER });
    localStorage.removeItem('checklist-bio-declined');
    refreshBioButton();
  } catch (e) { /* cancelado o no disponible: no pasa nada */ }
}

// Login y usuarios (nube).
document.getElementById('loginForm').addEventListener('submit', async function (e) {
  e.preventDefault();
  var id = document.getElementById('loginEmail').value.trim();
  var pass = document.getElementById('loginPass').value;
  var err = document.getElementById('loginError');
  var remember = document.getElementById('loginRemember').checked;
  err.textContent = '';
  if (!id || !pass) { err.textContent = 'Escribe tu usuario y contraseña.'; return; }
  if (id.indexOf('@') === -1 && !/^[a-z0-9._-]+$/i.test(id)) { err.textContent = 'El usuario solo puede tener letras, números, puntos, guiones y guion bajo, sin espacios.'; return; }
  err.textContent = 'Entrando…';
  var lockUid = null, lockRol = null, lockEmail = id;
  try {
    var email = id;
    if (id.indexOf('@') === -1) {
      var m = await window.Cloud.resolveUsername(id.toLowerCase());
      if (m) { email = m.email; lockUid = m.uid; lockRol = m.rol; }
      else email = id.toLowerCase() + '@checklist.local';
    } else {
      var m2 = window.Cloud.resolveEmail ? await window.Cloud.resolveEmail(id.toLowerCase()) : null;
      if (m2) { email = m2.email; lockUid = m2.uid; lockRol = m2.rol; }
    }
    lockEmail = email;
    // Bloqueo por intentos: solo a los usuarios; al admin nunca se le bloquea.
    if (lockUid && lockRol !== 'admin' && window.Cloud.getLoginLock) {
      var lock = await window.Cloud.getLoginLock(lockUid);
      if (lock && lock.locked) { err.textContent = 'Tu cuenta está bloqueada por demasiados intentos fallidos. Pide al administrador que la desbloquee.'; return; }
    }
    await window.Cloud.setPersistenceMode(remember);
    var cred = await window.Cloud.signIn(email, pass);
    if (lockUid && lockRol !== 'admin' && window.Cloud.resetLoginLock) window.Cloud.resetLoginLock(lockUid).catch(function () {});
    if (remember) localStorage.setItem('checklist-login-id', id);
    else localStorage.removeItem('checklist-login-id');
    localStorage.setItem('checklist-remember', remember ? '1' : '0');
    sessionPassword = pass;
    // Verificar explícitamente: si la sesión ya estaba iniciada con el
    // mismo usuario, el listener de auth no vuelve a dispararse.
    onAuthChanged(cred.user);
    offerBiometrics(email);
  } catch (er) {
    if (lockUid && lockRol !== 'admin' && er && (er.code === 'auth/invalid-credential' || er.code === 'auth/user-not-found' || er.code === 'auth/wrong-password') && window.Cloud.recordLoginFailure) {
      try {
        var r = await window.Cloud.recordLoginFailure(lockUid, lockEmail);
        err.textContent = r.locked ? 'Cuenta bloqueada por 10 intentos fallidos. Pide al administrador que la desbloquee.' : 'Usuario o contraseña incorrectos. Te quedan ' + Math.max(0, 10 - r.count) + ' intentos.';
      } catch (e2) {
        err.textContent = 'Usuario o contraseña incorrectos.';
      }
    } else {
      err.textContent = (er && er.code === 'auth/invalid-credential') ? 'Usuario o contraseña incorrectos.' : 'No se pudo entrar. Revisa tu conexión.' + (er && er.code ? ' (' + er.code + ')' : '');
    }
  }
});
document.getElementById('btnBiometric').addEventListener('click', async function () {
  var err = document.getElementById('loginError');
  err.textContent = '';
  err.style.color = '';
  try {
    var P = window.Capacitor.Plugins;
    await P.NativeBiometric.verifyIdentity({ reason: 'Entra a Checklist de Soporte con tu huella.', title: 'Checklist de Soporte', subtitle: 'Acceso con huella', negativeButtonText: 'Usar contraseña' });
    var stored = await P.NativeBiometric.getCredentials({ server: BIO_SERVER });
    err.textContent = 'Entrando…';
    var cred = await window.Cloud.signIn(stored.username, stored.password);
    sessionPassword = stored.password;
    onAuthChanged(cred.user);
  } catch (e) {
    if (e && (e.code === 'auth/invalid-credential' || e.code === 'auth/user-not-found' || e.code === 'auth/wrong-password')) {
      try { await window.Capacitor.Plugins.NativeBiometric.deleteCredentials({ server: BIO_SERVER }); } catch (e2) {}
      refreshBioButton();
      err.textContent = 'Tu contraseña cambió. Entra con tu contraseña.';
    } else if (e && (e.code === 16 || (e.message && /cancel/i.test(String(e.message))))) {
      err.textContent = '';
    } else {
      err.textContent = 'No se pudo entrar con huella. Usa tu contraseña.';
    }
  }
});
document.getElementById('btnForgot').addEventListener('click', async function () {
  var id = document.getElementById('loginEmail').value.trim();
  var err = document.getElementById('loginError');
  err.textContent = '';
  err.style.color = '';
  if (!id) { err.textContent = 'Escribe primero tu usuario o correo.'; return; }
  err.textContent = 'Buscando tu cuenta…';
  try {
    var realEmail = null;
    if (id.indexOf('@') === -1) {
      var m = await window.Cloud.resolveUsername(id.toLowerCase());
      if (!m) { err.textContent = 'No encontramos ese usuario.'; return; }
      realEmail = m.emailReal || m.email;
    } else {
      var m2 = window.Cloud.resolveEmail ? await window.Cloud.resolveEmail(id.toLowerCase()) : null;
      realEmail = m2 ? (m2.emailReal || m2.email) : id;
    }
    if (!realEmail || String(realEmail).toLowerCase().endsWith('@checklist.local')) {
      err.textContent = 'Tu cuenta no tiene un correo registrado. Pídele al administrador que te cambie la contraseña desde la app.';
      return;
    }
    await window.Cloud.sendPasswordReset(realEmail);
    err.style.color = '#2e7d6b';
    err.textContent = 'Te enviamos un correo a ' + realEmail + ' con el enlace para crear una contraseña nueva.';
  } catch (e) {
    err.textContent = (e && e.code === 'auth/user-not-found') ? 'No encontramos una cuenta con ese correo.' : 'No se pudo enviar el correo. Revisa tu conexión.';
  }
});
document.getElementById('bootstrapForm').addEventListener('submit', function (e) {
  e.preventDefault();
  var nombre = document.getElementById('bootNombre').value.trim();
  var email = document.getElementById('bootEmail').value.trim();
  var pass = document.getElementById('bootPass').value;
  var err = document.getElementById('loginError');
  err.textContent = '';
  if (!nombre || !email || pass.length < 6) { err.textContent = 'Escribe nombre, correo y una contraseña de al menos 6 caracteres.'; return; }
  window.Cloud.bootstrapAdmin({ nombre: nombre, email: email, password: pass }).then(function (user) {
    onAuthChanged(user);
  }).catch(function (er) {
    err.textContent = (er && er.code === 'auth/email-already-in-use') ? 'Ese correo ya está registrado. Entra con ese correo y contraseña en el formulario de arriba.' : 'No se pudo crear el administrador.' + (er && er.code ? ' (' + er.code + ')' : '');
  });
});
document.getElementById('btnReintentarLogin').addEventListener('click', function () {
  var u = (window.Cloud && window.Cloud.currentUser && window.Cloud.currentUser()) || cloudUser;
  document.getElementById('btnReintentarLogin').hidden = true;
  document.getElementById('loginError').textContent = 'Reintentando…';
  if (u) onAuthChanged(u);
});
document.getElementById('btnPassOpen').addEventListener('click', function () {
  document.getElementById('viewCuenta').hidden = false;
  document.getElementById('viewBio').hidden = false;
  refreshBioButton();
  document.getElementById('viewCuenta').scrollIntoView();
});
document.getElementById('btnPassCancel').addEventListener('click', function () {
  document.getElementById('viewCuenta').hidden = true;
  document.getElementById('viewBio').hidden = true;
  ['fPassActual', 'fPassNueva', 'fPassNueva2'].forEach(function (id) { document.getElementById(id).value = ''; });
});
document.getElementById('btnBioEnable').addEventListener('click', async function () {
  try {
    var P = window.Capacitor.Plugins;
    if (!P || !P.NativeBiometric) { alert('Este teléfono no tiene acceso biométrico.'); return; }
    if (!sessionPassword || !cloudUser) { alert('Entra con tu contraseña primero y vuelve a intentarlo.'); return; }
    var av = await P.NativeBiometric.isAvailable();
    if (!av.isAvailable) { alert('Este teléfono no tiene huella o rostro configurado.'); return; }
    await P.NativeBiometric.verifyIdentity({ reason: 'Activa el acceso con huella para Checklist de Soporte.', title: 'Checklist de Soporte', subtitle: 'Acceso con huella', negativeButtonText: 'Cancelar' });
    await P.NativeBiometric.setCredentials({ username: cloudUser.email, password: sessionPassword, server: BIO_SERVER });
    localStorage.removeItem('checklist-bio-declined');
    alert('Acceso con huella activado en este teléfono.');
    refreshBioButton();
  } catch (e) { alert('No se pudo activar el acceso con huella.'); }
});
document.getElementById('btnBioDisable').addEventListener('click', async function () {
  try { var P = window.Capacitor.Plugins; if (P && P.NativeBiometric) await P.NativeBiometric.deleteCredentials({ server: BIO_SERVER }); } catch (e) {}
  localStorage.setItem('checklist-bio-declined', '1');
  alert('Acceso con huella desactivado en este teléfono.');
  refreshBioButton();
});
document.getElementById('btnPassSave').addEventListener('click', function () {
  var actual = document.getElementById('fPassActual').value;
  var nueva = document.getElementById('fPassNueva').value;
  var nueva2 = document.getElementById('fPassNueva2').value;
  if (nueva.length < 6) { alert('La nueva contraseña debe tener al menos 6 caracteres.'); return; }
  if (nueva !== nueva2) { alert('La nueva contraseña no coincide.'); return; }
  window.Cloud.changeOwnPassword(actual, nueva).then(async function () {
    sessionPassword = nueva;
    try {
      var P = window.Capacitor.Plugins;
      if (P && P.NativeBiometric && await bioHasStored()) await P.NativeBiometric.setCredentials({ username: cloudUser.email, password: nueva, server: BIO_SERVER });
    } catch (e) {}
    alert('Contraseña cambiada.');
    document.getElementById('btnPassCancel').click();
  }).catch(function (er) {
    alert((er && (er.code === 'auth/invalid-credential' || er.code === 'auth/wrong-password')) ? 'La contraseña actual no es correcta.' : 'No se pudo cambiar la contraseña. Revisa tu conexión.');
  });
});
document.getElementById('btnLogout').addEventListener('click', function () {
  stopEquipo();
  if (cloudUnsub) { cloudUnsub(); cloudUnsub = null; }
  if (cloudDetectadosUnsub) { cloudDetectadosUnsub(); cloudDetectadosUnsub = null; }
  cloudUser = null; cloudRole = null; sessionPassword = null;
  showVista('preparar');
  if (window.Cloud) window.Cloud.signOut();
});
document.getElementById('btnAiGuardar').addEventListener('click', function () {
  var k = document.getElementById('fAiKey').value.trim();
  if (!k) { alert('Pega primero tu clave de Google AI Studio.'); return; }
  window.Cloud.setAiKey(k).then(function () { aiKey = k; document.getElementById('fAiKey').value = ''; refreshAiStatus(); }).catch(function () { alert('No se pudo guardar la clave. Revisa tu conexión.'); });
});
document.getElementById('btnAiQuitar').addEventListener('click', function () {
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
});
document.getElementById('btnUserAdd').addEventListener('click', function () {
  var nombre = document.getElementById('newUserNombre').value.trim();
  var usuario = document.getElementById('newUserUsuario').value.trim().toLowerCase();
  var email = document.getElementById('newUserEmail').value.trim();
  var pass = document.getElementById('newUserPass').value;
  var rol = document.getElementById('newUserRol').value;
  if (!nombre || !usuario || pass.length < 6) { alert('Escribe nombre, usuario y una contraseña de al menos 6 caracteres.'); return; }
  if (!/^[a-z0-9._-]+$/.test(usuario)) { alert('El usuario solo puede tener letras, números, puntos, guiones y guion bajo, sin espacios.'); return; }
  if (email && email.indexOf('@') === -1) { alert('El correo no es válido.'); return; }
  var authEmail = email || (usuario + '@checklist.local');
  window.Cloud.createUserByAdmin({ email: authEmail, password: pass, nombre: nombre, usuario: usuario, rol: rol }).then(function () {
    document.getElementById('newUserNombre').value = '';
    document.getElementById('newUserUsuario').value = '';
    document.getElementById('newUserEmail').value = '';
    document.getElementById('newUserPass').value = '';
    renderUsuarios();
  }).catch(function (er) {
    alert((er && er.code === 'auth/email-already-in-use') ? 'Ese usuario o correo ya está registrado.' : 'No se pudo crear el usuario.');
  });
});
document.getElementById('userList').addEventListener('click', function (e) {
  var t = e.target;
  var tog = t.closest('[data-user-toggle]');
  var rol = t.closest('[data-user-role]');
  var del = t.closest('[data-user-del]');
  var unl = t.closest('[data-user-unlock]');
  var pas = t.closest('[data-user-pass]');
  var edt = t.closest('[data-user-edit]');
  if (!tog && !rol && !del && !unl && !pas && !edt) return;
  var uid = (tog || rol || del || unl || pas || edt).getAttribute(tog ? 'data-user-toggle' : rol ? 'data-user-role' : del ? 'data-user-del' : unl ? 'data-user-unlock' : pas ? 'data-user-pass' : 'data-user-edit');
  var u = lastUsers.find(function (x) { return x.uid === uid; });
  if (!u) return;
  if (edt) {
    window._editUserUid = uid;
    window._editUserOld = u.usuario || '';
    document.getElementById('fEuNombre').value = u.nombre || '';
    document.getElementById('fEuUsuario').value = u.usuario || '';
    document.getElementById('fEuCorreo').value = u.email || '';
    document.getElementById('userEditBox').hidden = false;
    return;
  }
  if (uid === cloudUser.uid) { alert('No puedes cambiar tu propio usuario desde aquí.'); return; }
  if (unl) {
    window.Cloud.unlockUser(uid).then(renderUsuarios).catch(function () { alert('No se pudo desbloquear la cuenta.'); });
    return;
  }
  if (pas) {
    var np = prompt('Nueva contraseña para ' + (u.nombre || u.email) + ' (mínimo 6 caracteres):');
    if (np === null) return;
    if (np.length < 6) { alert('La contraseña debe tener al menos 6 caracteres.'); return; }
    window.Cloud.adminResetPassword({ uid: uid, usuario: u.usuario || '', email: u.email, nombre: u.nombre || '', rol: u.rol || 'usuario', newPassword: np }).then(function () { alert('Contraseña cambiada para ' + (u.nombre || u.email) + '.'); renderUsuarios(); }).catch(function () { alert('No se pudo cambiar la contraseña.'); });
    return;
  }
  if (del) {
    if (!confirm('¿Eliminar a ' + (u.nombre || u.email) + '? Ya no podrá entrar a la app.')) return;
    window.Cloud.deleteUserByAdmin(uid, u.usuario || '').then(renderUsuarios).catch(function () { alert('No se pudo eliminar el usuario.'); });
    return;
  }
  if (tog) {
    window.Cloud.setUserActive(uid, u.activo === false).then(renderUsuarios);
  } else {
    window.Cloud.setUserRole(uid, u.rol === 'admin' ? 'usuario' : 'admin').then(renderUsuarios);
  }
});
document.getElementById('btnEuCancelar').addEventListener('click', function () {
  document.getElementById('userEditBox').hidden = true;
  window._editUserUid = null;
});
document.getElementById('btnEuGuardar').addEventListener('click', function () {
  var uid = window._editUserUid;
  if (!uid) return;
  var nombre = document.getElementById('fEuNombre').value.trim();
  var usuario = document.getElementById('fEuUsuario').value.trim().toLowerCase();
  var email = document.getElementById('fEuCorreo').value.trim();
  if (!nombre || !usuario) { alert('Escribe el nombre y el usuario.'); return; }
  if (!/^[a-z0-9._-]+$/.test(usuario)) { alert('El usuario solo puede tener letras, números, puntos, guiones y guion bajo, sin espacios.'); return; }
  if (email && email.indexOf('@') === -1) { alert('El correo no es válido.'); return; }
  window.Cloud.adminUpdateUser(uid, window._editUserOld || '', { nombre: nombre, usuario: usuario, email: email }).then(function () {
    document.getElementById('userEditBox').hidden = true;
    window._editUserUid = null;
    renderUsuarios();
  }).catch(function (er) {
    alert((er && er.code === 'auth/email-already-in-use') ? 'Ese usuario ya está registrado por otro.' : 'No se pudo guardar los cambios.');
  });
});
document.getElementById('btnReportar').addEventListener('click', function () {
  window.location.href = 'mailto:gerardo.cruzhz@linux.com?subject=' + encodeURIComponent('Reporte de problema - Checklist de Soporte 2.3.1') + '&body=' + encodeURIComponent('Describe el problema:\n\n\nVersión de la app: 2.3.1');
});

boot();
// El splash no se quita hasta que la app ya decidió qué mostrar (login o
// interfaz): si se quitara antes, se vería la interfaz como si la sesión
// ya estuviera iniciada. Último recurso: a los 9 s se quita de todos modos.
function hideSplash() {
  var s = document.getElementById('splash');
  if (!s) return;
  if (!_authReady) { setTimeout(hideSplash, 400); return; }
  s.classList.add('hide');
  setTimeout(function () { var s2 = document.getElementById('splash'); if (s2) s2.remove(); }, 500);
}
setTimeout(function () { document.getElementById('atom').classList.add('form'); }, 1400);
setTimeout(hideSplash, 2400);
setTimeout(function () { _authReady = true; hideSplash(); }, 9000);
