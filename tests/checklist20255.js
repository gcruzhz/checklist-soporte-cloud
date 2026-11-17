
// Avisos y confirmaciones sin diálogos nativos (251): los diálogos
// nativos del navegador roban el foco en el escritorio y podían dejar
// los campos sin tecleo; a partir de aquí todo aviso es un toast
// in-app y toda confirmación es un modal inline propio. El toast no es
// modal, no bloquea la ejecución y nunca recibe el foco: solo se
// muestra ~3 s y se auto-oculta. El modal solo recibe el foco cuando
// el usuario hace clic en él; al cerrarlo no se fuerza el foco a
// ningún lado.
function showToast(msg) {
  var t = document.getElementById('toast');
  if (!t) return;
  t.textContent = String(msg == null ? '' : msg);
  t.hidden = false;
  if (window._toastTimer) clearTimeout(window._toastTimer);
  window._toastTimer = setTimeout(function () { t.hidden = true; }, 3000);
}
function showConfirm(msg) {
  return new Promise(function (resolve) {
    var m = document.getElementById('confirmModal');
    var msgEl = document.getElementById('confirmMsg');
    var yes = document.getElementById('confirmYes');
    var no = document.getElementById('confirmNo');
    if (!m || !msgEl || !yes || !no) { resolve(false); return; }
    msgEl.textContent = String(msg == null ? '' : msg);
    m.hidden = false;
    function done(v) { m.hidden = true; yes.onclick = null; no.onclick = null; resolve(v); }
    yes.onclick = function () { done(true); };
    no.onclick = function () { done(false); };
  });
}
function showPrompt(msg) {
  return new Promise(function (resolve) {
    var m = document.getElementById('promptModal');
    var msgEl = document.getElementById('promptMsg');
    var inp = document.getElementById('promptInput');
    var ok = document.getElementById('promptOk');
    var cancel = document.getElementById('promptCancel');
    if (!m || !msgEl || !inp || !ok || !cancel) { resolve(null); return; }
    msgEl.textContent = String(msg == null ? '' : msg);
    inp.value = '';
    m.hidden = false;
    function done(v) { m.hidden = true; ok.onclick = null; cancel.onclick = null; resolve(v); }
    ok.onclick = function () { done(inp.value); };
    cancel.onclick = function () { done(null); };
  });
}
// Diagnóstico de foco (251): línea en Acerca de que muestra si el
// documento tiene el foco y qué elemento está activo, actualizada en
// cada render y cuando el foco entra o sale de la ventana.
function updateFocusDiag() {
  var el = document.getElementById('focusDiag');
  if (!el) return;
  var has = (typeof document.hasFocus === 'function') ? document.hasFocus() : true;
  var ae = document.activeElement;
  var id = (ae && ae.id) ? ae.id : 'ninguno';
  el.textContent = 'Foco: ' + (has ? 'sí' : 'no') + ' · Elemento activo: ' + id;
}
if (typeof window.addEventListener === 'function') {
  window.addEventListener('focus', updateFocusDiag);
  window.addEventListener('blur', updateFocusDiag);
}
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
    recibidoPor: rec.recibidoPor || '', entregadoPor: rec.entregadoPor || '', entregadoAt: rec.entregadoAt || null,
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
    recibidoPor: doc.recibidoPor || '', entregadoPor: doc.entregadoPor || '', entregadoAt: doc.entregadoAt || null
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
  var v = p.versiones || {};
  var foto = eq.fotoSerie || null;
  if (foto && foto.length > MAX_FOTO_CLOUD) foto = null;
  return {
    id: p.id, createdAt: p.createdAt || Date.now(), deliveredAt: p.deliveredAt || null, readyAt: p.readyAt || null,
    checks: p.checks || {}, extraItems: p.extraItems || [], reasignaciones: p.reasignaciones || [],
    tecnicoUid: p.tecnicoUid || '', asignaciones: p.asignaciones || [], solicitudAsignacion: p.solicitudAsignacion || null,
    naItems: p.naItems || {}, removedItems: p.removedItems || [], noListo: p.noListo || null,
    autoDetectado: p.autoDetectado || [], borrador: p.borrador || false,
    versiones: { so: v.so || '', antivirus: v.antivirus || '', esetAgent: v.esetAgent || '', chrome: v.chrome || '' },
    equipo: { tipo: eq.tipo || '', marca: eq.marca || '', modelo: eq.modelo || '', serie: eq.serie || '', inventario: eq.inventario || '', hostname: eq.hostname || '', cpu: eq.cpu || '', ramGB: (eq.ramGB == null ? '' : eq.ramGB), discoGB: (eq.discoGB == null ? '' : eq.discoGB), discoTipo: eq.discoTipo || '', ip: eq.ip || '', ipTipo: eq.ipTipo || '', anydeskId: eq.anydeskId || '', anydeskAlias: eq.anydeskAlias || '', redes: Array.isArray(eq.redes) ? eq.redes.map(function (r) { return { nombre: r.nombre || '', ip: r.ip || '', ipTipo: r.ipTipo || '' }; }) : [], fotoSerie: foto },
    usuario: { nombre: (p.usuario && p.usuario.nombre) || '', area: (p.usuario && p.usuario.area) || '', correo: (p.usuario && p.usuario.correo) || '' },
    tecnico: p.tecnico || '',
    updatedAt: Date.now()
  };
}
function prepFromCloud(doc) {
  var eq = doc.equipo || {};
  var v = doc.versiones || {};
  return {
    id: doc.id, createdAt: doc.createdAt || 0, deliveredAt: doc.deliveredAt || null, readyAt: doc.readyAt || null,
    checks: doc.checks || {}, extraItems: doc.extraItems || [], reasignaciones: doc.reasignaciones || [],
    tecnicoUid: doc.tecnicoUid || '', asignaciones: doc.asignaciones || [], solicitudAsignacion: doc.solicitudAsignacion || null,
    naItems: doc.naItems || {}, removedItems: doc.removedItems || [], noListo: doc.noListo || null,
    autoDetectado: doc.autoDetectado || [], borrador: doc.borrador || false,
    versiones: { so: v.so || '', antivirus: v.antivirus || '', esetAgent: v.esetAgent || '', chrome: v.chrome || '' },
    equipo: { tipo: eq.tipo || '', marca: eq.marca || '', modelo: eq.modelo || '', serie: eq.serie || '', inventario: eq.inventario || '', hostname: eq.hostname || '', cpu: eq.cpu || '', ramGB: (eq.ramGB == null ? '' : eq.ramGB), discoGB: (eq.discoGB == null ? '' : eq.discoGB), discoTipo: eq.discoTipo || '', ip: eq.ip || '', ipTipo: eq.ipTipo || '', anydeskId: eq.anydeskId || '', anydeskAlias: eq.anydeskAlias || '', redes: Array.isArray(eq.redes) ? eq.redes.map(function (r) { return { nombre: r.nombre || '', ip: r.ip || '', ipTipo: r.ipTipo || '' }; }) : [], fotoSerie: eq.fotoSerie || null },
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
// Botón Detectar bloqueado por máquina (251): se deshabilita cuando ESTA
// máquina ya tiene una detección pendiente sin usar (un documento en
// 'detectados' con id == machineId de esta PC y usado !== true) y muestra
// 'Equipo detectado ✓'; la detección de otra PC no bloquea esta. El
// machineId lo expone el detector de escritorio (window.Desktop.
// getMachineId()); si no existe o falla, no hay bloqueo y el botón funciona
// como antes. El botón reacciona a la suscripción: al usarse o descartarse
// la entrada, la suscripción lo refleja y se vuelve a habilitar.
var machineId = null;        // id de esta máquina, si el detector lo expone
var machineIdTried = false;  // ya se pidió getMachineId a este Desktop
var machineIdDesktop = null; // Desktop al que se le pidió (si cambia, reintentar)
var detectingNow = false;    // detección en curso (progreso)
var DETECTAR_HTML = '<span class="ic">&#128187;</span><span>Detectar este equipo<small>solo en escritorio</small></span>';
var DETECTAR_MANT_HTML = '<span class="ic">🖥️</span><span>Detectar equipo<small>solo en escritorio</small></span>';
function thisMachinePending() {
  if (!machineId) return false;
  return detectados.some(function (d) { return String(d.id) === String(machineId) && !d.usado; });
}
function refreshDetectarBtn() {
  // (252) Los dos botones de detección comparten el mismo estado:
  // #btnDetectar (Por preparar) y #btnMantDetectar (Mantenimientos).
  // Cada uno conserva su propia etiqueta por defecto.
  [['btnDetectar', DETECTAR_HTML], ['btnMantDetectar', DETECTAR_MANT_HTML]].forEach(function (pair) {
    var btn = document.getElementById(pair[0]);
    if (!btn) return;
    var defHtml = pair[1];
    btn.hidden = !window.Desktop;
    if (detectingNow) {
      btn.disabled = true;
      btn.innerHTML = '<span class="ic">&#128187;</span><span>Detectando software...</span>';
      return;
    }
    if (thisMachinePending()) {
      btn.disabled = true;
      btn.innerHTML = '<span class="ic">&#128187;</span><span>Equipo detectado ✓</span>';
      return;
    }
    btn.disabled = false;
    // Solo se restaura la etiqueta por defecto si la puso este control
    // (progreso o bloqueo); si otro código puso su propio texto, se respeta.
    if (btn.innerHTML.indexOf('Detectando software...') !== -1 || btn.innerHTML.indexOf('Equipo detectado') !== -1) btn.innerHTML = defHtml;
  });
}
function loadMachineId() {
  if (window.Desktop !== machineIdDesktop) { machineIdTried = false; machineId = null; machineIdDesktop = window.Desktop || null; }
  if (machineIdTried || !window.Desktop || typeof window.Desktop.getMachineId !== 'function') { machineIdTried = true; return Promise.resolve(machineId); }
  machineIdTried = true;
  var p;
  try { p = Promise.resolve(window.Desktop.getMachineId()); } catch (e) { refreshDetectarBtn(); return Promise.resolve(null); }
  return p.then(function (id) { machineId = id ? String(id) : null; refreshDetectarBtn(); return machineId; }).catch(function () { machineId = null; refreshDetectarBtn(); return null; });
}
// Checks del detector (251): el detector de escritorio reporta qué
// software y hardware encontró (d.checks), versiones (d.versiones) y
// detalles (d.detalles, p. ej. officeDetectado, invgate, adobe).
// Solo los ids detectables de la plantilla actual pueden nacer
// marcados (t3/t4 de hardware, el software e Invgate t12); datos
// (t13-t17), t1/t2 y la limpieza (t26) nunca.
var DETECTABLE_IDS = ['t3', 't4', 't6', 't7', 't8', 't9', 't10', 't11', 't12', 't18', 't19', 't20', 't21', 't22', 't23', 't24', 't25'];
var DET_SHORT = {
  t3: 'Batería y cargador', t4: 'Etiqueta y serie',
  t6: 'SO actualizado', t7: 'Antivirus', t8: 'Office', t9: 'Impresoras',
  t10: 'VPN', t11: 'Inicio rápido desactivado', t12: 'Invgate', t18: 'Chrome',
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
  if (f.checks.t19 && d.detalles && d.detalles.adobe) {
    var ad = d.detalles.adobe === 'Acrobat' ? 'Adobe Acrobat' : 'Adobe Reader';
    for (var i = 0; i < parts.length; i++) if (parts[i] === 'Adobe Reader') parts[i] = ad;
  }
  if (d.detalles && d.detalles.officeDetectado && !f.checks.t8) parts.push('Office instalado, activación sin verificar');
  if (d.detalles && d.detalles.invgate && !f.checks.t12) parts.push('Agente de Invgate detectado');
  if (!parts.length) return '';
  return 'Detectado: ' + parts.map(function (n) { return esc(n); }).join(', ');
}
// Versiones detectadas (251): solo las conocidas, en el orden SO,
// antivirus, agente ESET, Chrome. Vacío si no se conoce ninguna.
// El agente ESET solo aparece si el detector lo encontró (nunca se
// inventa): 'Agente ESET: 11.1.1234.0'.
function versionesLine(v) {
  v = v || {};
  var parts = [];
  if (v.so) parts.push('SO: ' + v.so);
  if (v.antivirus) parts.push('Antivirus: ' + v.antivirus);
  if (v.esetAgent) parts.push('Agente ESET: ' + v.esetAgent);
  if (v.chrome) parts.push('Chrome: ' + v.chrome);
  if (!parts.length) return '';
  return 'Versiones detectadas: ' + parts.join(' • ');
}
// Línea de hardware (251): solo los datos conocidos; vacía si no hay
// ninguno. Disco con su tipo (HDD/SSD/NVMe) e IP con su tipo cuando se
// conocen ('IP: 192.168.1.45 (Dinámica)').
function hardwareLine(eq) {
  eq = eq || {};
  var parts = [];
  if (eq.cpu) parts.push('Procesador: ' + eq.cpu);
  if (eq.ramGB != null && eq.ramGB !== '') parts.push('RAM: ' + eq.ramGB + ' GB');
  if (eq.discoGB != null && eq.discoGB !== '') parts.push('Disco: ' + eq.discoGB + ' GB' + (eq.discoTipo ? ' ' + eq.discoTipo : ''));
  if (eq.ip) parts.push('IP: ' + eq.ip + (eq.ipTipo ? ' (' + eq.ipTipo + ')' : ''));
  return parts.join(' • ');
}
// AnyDesk (251): el ID de 9 dígitos se muestra agrupado ('123 456 789')
// y con su alias si se conoce. Vacío si no hay ID.
function anydeskDisplay(id) {
  var d = String(id || '').replace(/\D/g, '');
  if (d.length === 9) return d.slice(0, 3) + ' ' + d.slice(3, 6) + ' ' + d.slice(6);
  return String(id || '');
}
function anydeskLine(eq) {
  eq = eq || {};
  if (!eq.anydeskId) return '';
  var s = 'AnyDesk: ' + anydeskDisplay(eq.anydeskId);
  if (eq.anydeskAlias) s += ' (' + eq.anydeskAlias + ')';
  return s;
}
// Escritorio revisado: el detector guarda en detalles las rutas de
// Escritorio realmente escaneadas (escritorioRutas, array de strings) y
// cuántos .lnk/.url encontró (atajosVistos, número). Solo se muestra
// cuando esos campos existen en el equipo detectado: 'Escritorio
// revisado: <ruta1, ruta2>' y, si hay conteo, '· N atajos vistos'. Sin
// rutas ni conteo no hay línea. Una ruta suelta (string) se acepta como
// una sola ruta; el conteo solo vale si es número (0 incluido).
function escritorioLine(d) {
  var det = (d && d.detalles) || {};
  var rutas = det.escritorioRutas;
  if (typeof rutas === 'string' && rutas) rutas = [rutas];
  var n = det.atajosVistos;
  var parts = [];
  if (Array.isArray(rutas) && rutas.length) parts.push('Escritorio revisado: ' + rutas.join(', '));
  if (typeof n === 'number') parts.push(parts.length ? n + ' atajos vistos' : 'Atajos vistos: ' + n);
  if (!parts.length) return '';
  return parts.join(' \u00b7 ');
}
// Redes del equipo: el detector trae redes [{nombre, ip, ipTipo}] (ipTipo
// 'Estática'|'Dinámica' o ''); la ip/ipTipo sueltas del adaptador principal
// se siguen mostrando por hardwareLine. Sin redes (o sin ip en ninguna)
// no hay línea en ningún sitio.
function redesText(eq) {
  var list = (eq && eq.redes) || [];
  if (!Array.isArray(list)) return '';
  return list.filter(function (r) { return r && r.ip; }).map(function (r) {
    return (r.nombre ? r.nombre + ': ' : '') + r.ip + (r.ipTipo ? ' (' + r.ipTipo + ')' : '');
  }).join(' \u00b7 ');
}
function redesLine(eq) {
  var t = redesText(eq);
  return t ? 'Redes: ' + t : '';
}
// Fuente del SO: el detector dice en detalles.osFuente de dónde sacó el
// nombre del sistema operativo ('registro' | 'cim' | 'computerinfo' | 'si').
function osFuenteLine(d) {
  var det = (d && d.detalles) || {};
  var v = det.osFuente;
  if (!v) return '';
  var names = { registro: 'Registro de Windows', cim: 'CIM (WMI)', computerinfo: 'Get-ComputerInfo', si: 'Información del sistema' };
  return 'SO detectado por: ' + (names[v] || v);
}
// Puntos N/A o quitados por equipo: naItems {id:true} no cuenta en el
// avance (ni numerador ni denominador) y no lo pide '¿Qué falta?';
// removedItems [id] oculta el punto de la tarjeta. Defaults {} / [] para
// equipos viejos que no traen estos campos (ver prepFromCloud).
function isNA(p, id) { return !!(p.naItems && p.naItems[id]); }
function isRemoved(p, id) { return (p.removedItems || []).indexOf(id) !== -1; }
function naText(p) {
  return allItems(p).filter(function (it) { return isNA(p, it.id); }).map(function (it) { return it.text; }).join('; ');
}
function pendingRequired(p) {
  return requiredItems(p).filter(function (it) { return !p.checks[it.id]; });
}
// El marcador 'No listo' se limpia solo al llegar al 100% (o al pulsar
// 'Listo' de nuevo, en su handler): al marcar/quitar un punto, al poner o
// quitar un N/A, o al elegir una opción, el avance puede llegar a 100%.
function clearNoListoIfDone(p) {
  if (p.noListo && progress(p) === 100) delete p.noListo;
}
// Borrador (238b): un equipo detectado guardado para después nace como
// prep en En preparación con los datos detectados (checks, hardware,
// versiones, autoDetectado) y los datos del formulario vacíos
// (inventario, usuario, área, correo), marcado borrador: true.
function prepFromDetectado(d) {
  var det = filterDetectedChecks(d.checks || {});
  var ver = d.versiones || {};
  return {
    id: uid(), createdAt: Date.now(), deliveredAt: null, readyAt: null,
    checks: det.checks, autoDetectado: det.ids, extraItems: [], reasignaciones: [], naItems: {}, removedItems: [],
    borrador: true,
    versiones: { so: (typeof ver.so === 'string' ? ver.so : ''), antivirus: (typeof ver.antivirus === 'string' ? ver.antivirus : ''), chrome: (typeof ver.chrome === 'string' ? ver.chrome : '') },
    equipo: { tipo: d.tipo || 'Desktop', marca: d.marca || '', modelo: d.modelo || '', serie: d.serie || '', inventario: '', hostname: d.hostname || '', cpu: d.cpu || '', ramGB: (d.ramGB == null ? '' : d.ramGB), discoGB: (d.discoGB == null ? '' : d.discoGB), discoTipo: d.discoTipo || '', ip: d.ip || '', ipTipo: d.ipTipo || '', anydeskId: d.anydeskId || '', anydeskAlias: d.anydeskAlias || '', redes: Array.isArray(d.redes) ? d.redes : [], fotoSerie: null },
    usuario: { nombre: '', area: '', correo: '' },
    tecnico: technicianName(),
    tecnicoUid: tecnicoUidFor(technicianName())
  };
}
// Equipos detectados (251): solo se listan los NO usados, con sus datos
// y dos acciones: usarlo (llena Nuevo equipo) o descartarlo.
function renderDetectados() {
  var box = document.getElementById('detList');
  if (!box) return;
  var list = detectados.filter(function (d) { return !d.usado; });
  if (!list.length) { box.innerHTML = '<div class="empty">No hay equipos detectados pendientes.</div>'; refreshDetectarBtn(); return; }
  box.innerHTML = list.map(function (d) {
    var detLine = detLineFor(d);
    var hwLine = hardwareLine(d);
    if (d.so) hwLine = hwLine ? hwLine + ' • SO: ' + d.so : 'SO: ' + d.so;
    var verLine = versionesLine(d.versiones);
    var adLine = anydeskLine(d);
    var redesDet = redesLine(d);
    var osfLine = osFuenteLine(d);
    var escLine = escritorioLine(d);
    return '<div class="card"><h2>' + esc(d.hostname || 'Equipo') + '</h2>' +
      '<div class="sub">' + esc((d.marca || '') + ' ' + (d.modelo || '')) + ' · Serie: ' + esc(d.serie || '—') + '</div>' +
      (hwLine ? '<div class="sub">' + esc(hwLine) + '</div>' : '') +
      (adLine ? '<div class="sub">' + esc(adLine) + '</div>' : '') +
      (redesDet ? '<div class="sub">' + esc(redesDet) + '</div>' : '') +
      (verLine ? '<div class="sub">' + esc(verLine) + '</div>' : '') +
      (osfLine ? '<div class="sub">' + esc(osfLine) + '</div>' : '') +
      (escLine ? '<div class="sub">' + esc(escLine) + '</div>' : '') +
      '<div class="sub">Detectado ' + timeAgo(d.detectadoEn) + (d.detectadoPor ? ' por ' + esc(d.detectadoPor) : '') + '</div>' +
      (detLine ? '<div class="sub">' + detLine + '</div>' : '') +
      '<div class="actions"><button class="btn-green" data-det-use="' + esc(d.id) + '">Usar este equipo</button>' +
      '<button class="btn-dark" data-det-save="' + esc(d.id) + '">💾 Guardar para después</button>' +
      '<button class="btn-ghost" data-det-del="' + esc(d.id) + '">Descartar</button></div></div>';
  }).join('');
  refreshDetectarBtn();
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
  var auRow = document.getElementById('adminUserRow');
  if (auRow) auRow.hidden = !isAdmin;
  if (isAdmin) refreshAdminUserFilter();
  if (!isAdmin && !document.getElementById('viewUsuarios').hidden) showVista('inicio');
  var bar = document.getElementById('sessionBar');
  bar.hidden = !cloudUser;
  if (cloudUser) document.getElementById('sessionUser').textContent = (cloudUser.nombre || cloudUser.email) + (cloudRole ? ' · ' + (cloudRole === 'admin' ? 'Administrador' : 'Usuario') : '');
  refreshMantAccess();
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
        (u.mantBloqueado ? ' <span class="badge b-prep">🔧 Mantenimientos bloqueados</span>' : '') +
        '<div class="actions">' +
        '<button class="btn-ghost" data-user-toggle="' + u.uid + '">' + (u.activo === false ? 'Activar' : 'Desactivar') + '</button>' +
        '<button class="btn-ghost" data-user-role="' + u.uid + '">' + (u.rol === 'admin' ? 'Hacer usuario' : 'Hacer admin') + '</button>' +
        '<button class="btn-ghost" data-user-pass="' + u.uid + '">Contraseña</button>' +
        '<button class="btn-ghost" data-user-edit="' + u.uid + '">Editar</button>' +
        ((u.rol !== 'admin' && cloudUser && u.uid !== cloudUser.uid) ? '<button class="btn-ghost" data-user-mantblock="' + u.uid + '">' + (u.mantBloqueado ? 'Desbloquear mantenimientos' : 'Bloquear mantenimientos') + '</button>' : '') +
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
    if (cloudMantUnsub) { cloudMantUnsub(); cloudMantUnsub = null; }
    if (cloudUserUnsub) { cloudUserUnsub(); cloudUserUnsub = null; }
    mantenimientos = [];
    detectados = [];
    refreshDetectarBtn();
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
    cloudUser = { uid: user.uid, email: user.email, nombre: doc.nombre || '', mantBloqueado: !!doc.mantBloqueado };
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
    await migrateLocalMants();
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
        // (252) Si el panel de Mantenimientos está abierto, la lista
        // se actualiza sola cuando llega la detección (la escritura
        // de reportDetected y la suscripción no son instantáneas).
        var mb = document.getElementById('mantDetBox');
        if (mb && !mb.hidden) renderMantDetectados();
      });
    }
    if (window.Cloud.subscribeMantenimientos) {
      if (cloudMantUnsub) cloudMantUnsub();
      cloudMantUnsub = window.Cloud.subscribeMantenimientos(function (docs) {
        mantenimientos = mergeMantWithLocal(docs);
        saveMantLocal();
        renderMant();
        // (254) Si la vista de orden está abierta, re-renderizarla al
        // llegar cambios (p. ej. la firma del usuario por el link de
        // WhatsApp): si no, la orden se queda en "pendiente" hasta recargar.
        if (mantOrderId && !document.getElementById('mantOrderBox').hidden) {
          var mo = mantFind(mantOrderId);
          if (mo) { mantFillFromFirma(mo); renderMantOrder(mo); }
        }
      }, cloudRole === 'admin' ? null : (cloudUser ? cloudUser.uid : null));
    }
    if (window.Cloud.subscribeUserDoc) {
      if (cloudUserUnsub) cloudUserUnsub();
      cloudUserUnsub = window.Cloud.subscribeUserDoc(cloudUser.uid, function (d) {
        if (!d || !cloudUser) return;
        var antes = !!cloudUser.mantBloqueado;
        cloudUser.mantBloqueado = !!d.mantBloqueado;
        refreshMantAccess();
        // (254) El bloqueo llega en vivo: si estaba dentro de
        // Mantenimientos, se le saca a Inicio con el aviso.
        if (!antes && cloudUser.mantBloqueado && !document.getElementById('viewMant').hidden) {
          showToast('El acceso a Mantenimientos está bloqueado por el administrador.');
          showVista('inicio');
        }
      });
    }
    startEquipo();
    render();
    showVista('inicio');
    loadAiKey();
    _authReady = true;
  } catch (e) {
    document.getElementById('loginError').textContent = 'No se pudo verificar tu usuario. Revisa tu conexión.' + (e && e.code ? ' (' + e.code + ')' : '');
    _authReady = true;
  }
}
var _authReady = false;
async function boot() {
  if (!CLOUD_ENABLED) { document.getElementById('mainApp').hidden = false; document.getElementById('appHeader').hidden = false; _authReady = true; render(); showVista('inicio'); return; }
  var ok = false;
  try { ok = window.Cloud && await window.Cloud.init(window.FIREBASE_CONFIG); } catch (e) { ok = false; }
  if (!ok) { CLOUD_ENABLED = false; document.getElementById('mainApp').hidden = false; document.getElementById('appHeader').hidden = false; _authReady = true; render(); showVista('inicio'); return; }
  // Escritorio (251): el .exe siempre pide iniciar sesión al abrirse.
  // Se cierra cualquier sesión guardada ANTES de escuchar el estado de
  // autenticación, para que onAuthChanged nunca vea una sesión vieja ni
  // parpadee la interfaz. Si el cierre falla, se sigue al login igual.
  if (window.Desktop && window.Cloud && window.Cloud.signOut) {
    try { await window.Cloud.signOut(); } catch (e) { /* seguir al login */ }
  }
  document.getElementById('mainApp').hidden = true;
  document.getElementById('appHeader').hidden = true;
  document.getElementById('loginView').hidden = false;
  window.Cloud.onAuth(function (user) { onAuthChanged(user); });
  checkBootstrap();
  var savedId = localStorage.getItem('checklist-login-id');
  if (savedId) document.getElementById('loginEmail').value = savedId;
  if (localStorage.getItem('checklist-remember') === '0') document.getElementById('loginRemember').checked = false;
  // Escritorio (251): la sesión nunca se recuerda ni hay huella en el
  // .exe; en el teléfono todo sigue como siempre.
  if (window.Desktop) {
    var remRow = document.getElementById('loginRememberRow');
    if (remRow) remRow.hidden = true;
    document.getElementById('loginRemember').checked = false;
  } else {
    var remRow2 = document.getElementById('loginRememberRow');
    if (remRow2) remRow2.hidden = false;
  }
  refreshBioButton();
}

var filterStatus = 'todos';
var todosPage = 0;
var searchText = '';
// Ver equipos de otros analistas (238b): por defecto OCULTOS. El estado
// se recuerda por teléfono (localStorage): quien lo enciende lo vuelve a
// encontrar encendido al abrir la app; sin valor guardado, apagado.
var SHOW_OTHERS_KEY = 'checklist-soporte-ver-otros-v1';
var showOthers = false;
try { showOthers = localStorage.getItem(SHOW_OTHERS_KEY) === '1'; } catch (e) { showOthers = false; }

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
  // N/A y quitados quedan fuera: progress(), faltaPrompt(), waTextOne()
  // y avanceText() los heredan gratis al usar requiredItems().
  return allItems(prep).filter(function (it) { return !it.optional && !isNA(prep, it.id) && !isRemoved(prep, it.id); });
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
// Permisos por analista (251): cada equipo tiene un analista responsable
// (prep.tecnicoUid + prep.tecnico). El admin puede con todos; un usuario
// normal solo edita los suyos; los de otros son solo lectura (WhatsApp y
// correo). Sin sesión (modo local) no hay restricciones.
var adminViewUid = 'todos'; // admin: 'todos' = Todos los usuarios, o el uid de un analista
function isOwnPrep(p) {
  if (!cloudUser) return true;
  if (p.tecnicoUid) return p.tecnicoUid === cloudUser.uid;
  // Equipos viejos sin tecnicoUid: respaldo por el nombre del analista.
  if (p.tecnico && (p.tecnico === technicianName() || p.tecnico === cloudUser.nombre)) return true;
  // Participó en una reasignación: fue el analista que la registró.
  var tn = technicianName();
  return (p.reasignaciones || []).some(function (r) { return r.analista === tn || r.analista === cloudUser.nombre; });
}
function isPrepOfAnalyst(p, uid) {
  if (p.tecnicoUid) return p.tecnicoUid === uid;
  var u = null;
  teamUsers.forEach(function (x) { if (x.uid === uid) u = x; });
  if (u && p.tecnico) return p.tecnico === (u.nombre || u.email);
  return false;
}
function canEditPrep(p) { return cloudRole === 'admin' || isOwnPrep(p); }
// Uid del analista responsable por su nombre: el propio usuario, o un
// compañero de teamUsers si se escribió su nombre a mano en el formulario.
function tecnicoUidFor(nombre) {
  if (!nombre) return cloudUser ? cloudUser.uid : '';
  if (cloudUser && (nombre === cloudUser.nombre || nombre === cloudUser.email)) return cloudUser.uid;
  var hit = null;
  teamUsers.forEach(function (u) { if (u.nombre === nombre || u.email === nombre) hit = u; });
  if (hit) return hit.uid;
  return '';
}
function analystOptionsHtml(excludeUid) {
  return teamUsers.filter(function (u) { return u.uid !== excludeUid; }).map(function (u) {
    return '<option value="' + esc(u.uid) + '">' + esc(u.nombre || u.email || 'Usuario') + '</option>';
  }).join('');
}
function refreshAdminUserFilter() {
  var sel = document.getElementById('adminUserFilter');
  if (!sel) return;
  var cur = adminViewUid || 'todos';
  sel.innerHTML = '<option value="todos">Todos los usuarios</option>' + teamUsers.map(function (u) {
    return '<option value="' + esc(u.uid) + '"' + (u.uid === cur ? ' selected' : '') + '>' + esc(u.nombre || u.email || 'Usuario') + '</option>';
  }).join('');
  sel.value = cur;
}
function asignacionesText(p) {
  return (p.asignaciones || []).map(function (a) { return (a.de || '—') + ' → ' + (a.a || '—') + ' (' + fmtDate(a.fecha) + ')'; }).join('; ');
}
// Asignar (251): transfiere la responsabilidad al nuevo analista y lo
// registra en prep.asignaciones (distinto de reasignaciones, que cambia el
// TITULAR del equipo). El traspaso resuelve cualquier solicitud pendiente.
function doAssign(prep, newUid, newNombre) {
  if (!prep.asignaciones) prep.asignaciones = [];
  prep.asignaciones.push({ de: prep.tecnico || '', a: newNombre, fecha: Date.now() });
  prep.tecnicoUid = newUid;
  prep.tecnico = newNombre;
  prep.solicitudAsignacion = null;
}
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
// Ensamblador de PDF (251): buildPdf y buildPdfMant comparten la
// paginación y el xref. Las filas pueden llevar una imagen JPEG
// (r.img = {name, w, h} en puntos): el texto va arriba y la imagen debajo,
// en el mismo bloque, sin partirse entre páginas. images = {nombre:
// {bytes, w, h}} con bytes JPEG.
function binStrFromBytes(bytes) {
  var s = '';
  var CH = 8192;
  for (var i = 0; i < bytes.length; i += CH) {
    var chunk = [];
    for (var j = i; j < Math.min(i + CH, bytes.length); j++) chunk.push(bytes[j]);
    s += String.fromCharCode.apply(null, chunk);
  }
  return s;
}
// Ancho de texto para alinear a la derecha (251, punto 13): anchos
// Helvetica (unidades por 1000 em) para los caracteres ASCII; fuera de
// ese rango se usa 556, salvo los casos listados.
var PDF_CW = [278,278,355,556,556,889,667,191,333,333,389,584,278,333,278,278,556,556,556,556,556,556,556,556,556,556,278,278,584,584,584,556,1015,667,667,722,722,667,611,778,722,278,500,667,556,833,722,778,667,778,722,667,611,722,667,944,667,667,611,278,278,278,469,556,333,556,556,500,556,556,278,556,556,222,222,500,222,833,556,556,556,556,333,500,278,556,500,722,500,500,500,334,260,334,584];
function pdfTextWidth(t, f, s) {
  var w = 0;
  String(t || '').split('').forEach(function (ch) {
    var c = ch.charCodeAt(0);
    if (c >= 32 && c <= 126) w += PDF_CW[c - 32];
    else if (ch === 'í') w += 222;
    else if (ch === '¡') w += 278;
    else if (ch === '·') w += 278;
    else if (ch === '—' || ch === '–') w += 1000;
    else w += 556;
  });
  return w * (s || 11) / 1000;
}
function assemblePdf(rows, images) {
  images = images || {};
  var W = 595, H = 842, M = 48, usable = H - M * 2;
  var pages = [], cur = [], y = 0;
  function rowH(r) { return r.s * 1.45 + (r.img ? r.img.h + 6 : 0); }
  rows.forEach(function (r) {
    var lh = rowH(r);
    if (y + lh > usable && cur.length) { pages.push(cur); cur = []; y = 0; }
    cur.push(r); y += lh;
  });
  if (cur.length) pages.push(cur);
  var objs = [];
  objs[1] = '<< /Type /Catalog /Pages 2 0 R >>';
  var kidRefs = [];
  var nextId = 5;
  var imgIds = {};
  Object.keys(images).forEach(function (name) {
    var im = images[name];
    if (!im || !im.bytes) return;
    imgIds[name] = nextId++;
  });
  pages.forEach(function (pg) {
    var contentId = nextId++, pageId = nextId++;
    var cs = '';
    var yy = H - M;
    pg.forEach(function (r) {
      var lh = r.s * 1.45;
      var imgH = r.img ? r.img.h + 6 : 0;
      yy -= (lh + imgH);
      var tx = M;
      if (r.a === 'R') tx = W - M - pdfTextWidth(r.t, r.f, r.s);
      else if (r.a === 'C') tx = (W - pdfTextWidth(r.t, r.f, r.s)) / 2;
      cs += 'BT /' + r.f + ' ' + r.s + ' Tf ' + tx.toFixed(1) + ' ' + (yy + imgH).toFixed(1) + ' Td (' + pdfEsc(r.t) + ') Tj ET\n';
      if (r.img && imgIds[r.img.name]) {
        var ix = (r.a === 'R') ? (W - M - r.img.w) : ((r.a === 'C') ? ((W - r.img.w) / 2) : M);
        cs += 'q ' + r.img.w + ' 0 0 ' + r.img.h + ' ' + ix.toFixed(1) + ' ' + yy.toFixed(1) + ' cm /Im' + r.img.name + ' Do Q\n';
      }
    });
    objs[contentId] = '<< /Length ' + pdfBytes(cs).length + ' >>\nstream\n' + cs + '\nendstream';
    var res = '<< /Font << /F1 3 0 R /F2 4 0 R >>';
    var xobjs = Object.keys(imgIds).map(function (n) { return '/Im' + n + ' ' + imgIds[n] + ' 0 R'; }).join(' ');
    if (xobjs) res += ' /XObject << ' + xobjs + ' >>';
    res += ' >>';
    objs[pageId] = '<< /Type /Page /Parent 2 0 R /MediaBox [0 0 ' + W + ' ' + H + '] /Resources ' + res + ' /Contents ' + contentId + ' 0 R >>';
    kidRefs.push(pageId + ' 0 R');
  });
  Object.keys(imgIds).forEach(function (name) {
    var im = images[name];
    objs[imgIds[name]] = '<< /Type /XObject /Subtype /Image /Width ' + im.w + ' /Height ' + im.h + ' /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length ' + im.bytes.length + ' >>\nstream\n' + binStrFromBytes(im.bytes) + '\nendstream';
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
// (254) Texto seguro para el PDF: pdfBytes toma charCodeAt & 0xFF, así que
// solo valen caracteres latin-1; los de más de 255 saldrían corruptos.
function pdfSafe(s) {
  var map = { '—': '-', '–': '-', '·': ', ', '✓': '', '✗': '', '“': '"', '”': '"', '‘': "'", '’': "'", '•': '-', '…': '...', '🔧': '', '📄': '', '💬': '', '🔄': '' };
  return String(s == null ? '' : s).replace(/[—–·✓✗“”‘’•…🔧📄💬🔄]/g, function (c) { return map[c] || ''; });
}
// (254) Ensamblador de PDF por operaciones absolutas (para el formato de
// la orden de servicio): igual estructura que assemblePdf (catálogo,
// páginas, fuentes, imágenes, xref), pero cada página es una lista de
// operaciones con coordenadas absolutas. NO lo usa buildPdf (preparación).
// Operaciones: {k:'t', x, y, f, s, str, a, color} texto (y = línea base
// desde abajo; a = 'C' centrado en x, 'R' borde derecho en x, color 'red');
// {k:'r', x, y, w, h, fill} rectángulo (y = borde inferior; fill = gris
// 0..1 o null, siempre con borde); {k:'ln', x1, y1, x2, y2} línea;
// {k:'img', name, x, y, w, h} imagen (y = borde inferior).
// (255) Tamaño de página opcional: carta (612x792) para la orden de
// servicio; por defecto A4 (595x842).
function assemblePdfOps(pages, images, pageSize) {
  images = images || {};
  var W = (pageSize && pageSize.w) || 595, H = (pageSize && pageSize.h) || 842;
  var objs = [];
  objs[1] = '<< /Type /Catalog /Pages 2 0 R >>';
  var kidRefs = [];
  var nextId = 5;
  var imgIds = {};
  Object.keys(images).forEach(function (name) {
    var im = images[name];
    if (!im || !im.bytes) return;
    imgIds[name] = nextId++;
  });
  pages.forEach(function (pg) {
    var contentId = nextId++, pageId = nextId++;
    var cs = '';
    pg.forEach(function (op) {
      if (op.k === 't') {
        var tx = op.x;
        if (op.a === 'R') tx = op.x - pdfTextWidth(op.str, op.f, op.s);
        else if (op.a === 'C') tx = op.x - pdfTextWidth(op.str, op.f, op.s) / 2;
        if (op.color === 'red') cs += '1 0 0 rg ';
        cs += 'BT /' + op.f + ' ' + op.s + ' Tf ' + tx.toFixed(1) + ' ' + op.y.toFixed(1) + ' Td (' + pdfEsc(op.str) + ') Tj ET\n';
        if (op.color === 'red') cs += '0 g\n';
      } else if (op.k === 'r') {
        if (op.fill != null) cs += op.fill + ' g ' + op.x.toFixed(1) + ' ' + op.y.toFixed(1) + ' ' + op.w.toFixed(1) + ' ' + op.h.toFixed(1) + ' re f\n0 g\n';
        cs += '0.6 w ' + op.x.toFixed(1) + ' ' + op.y.toFixed(1) + ' ' + op.w.toFixed(1) + ' ' + op.h.toFixed(1) + ' re S\n';
      } else if (op.k === 'ln') {
        cs += '0.6 w ' + op.x1.toFixed(1) + ' ' + op.y1.toFixed(1) + ' m ' + op.x2.toFixed(1) + ' ' + op.y2.toFixed(1) + ' l S\n';
      } else if (op.k === 'img' && imgIds[op.name]) {
        cs += 'q ' + op.w + ' 0 0 ' + op.h + ' ' + op.x.toFixed(1) + ' ' + op.y.toFixed(1) + ' cm /Im' + op.name + ' Do Q\n';
      }
    });
    objs[contentId] = '<< /Length ' + pdfBytes(cs).length + ' >>\nstream\n' + cs + '\nendstream';
    var res = '<< /Font << /F1 3 0 R /F2 4 0 R >>';
    var xobjs = Object.keys(imgIds).map(function (n) { return '/Im' + n + ' ' + imgIds[n] + ' 0 R'; }).join(' ');
    if (xobjs) res += ' /XObject << ' + xobjs + ' >>';
    res += ' >>';
    objs[pageId] = '<< /Type /Page /Parent 2 0 R /MediaBox [0 0 ' + W + ' ' + H + '] /Resources ' + res + ' /Contents ' + contentId + ' 0 R >>';
    kidRefs.push(pageId + ' 0 R');
  });
  Object.keys(imgIds).forEach(function (name) {
    var im = images[name];
    objs[imgIds[name]] = '<< /Type /XObject /Subtype /Image /Width ' + im.w + ' /Height ' + im.h + ' /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length ' + im.bytes.length + ' >>\nstream\n' + binStrFromBytes(im.bytes) + '\nendstream';
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
  if (prep.equipo.cpu) row('Procesador: ' + prep.equipo.cpu, 'F1', 11);
  if (prep.equipo.ramGB != null && prep.equipo.ramGB !== '') row('RAM: ' + prep.equipo.ramGB + ' GB', 'F1', 11);
  if (prep.equipo.discoGB != null && prep.equipo.discoGB !== '') row('Disco: ' + prep.equipo.discoGB + ' GB' + (prep.equipo.discoTipo ? ' ' + prep.equipo.discoTipo : ''), 'F1', 11);
  if (prep.equipo.ip) row('IP: ' + prep.equipo.ip + (prep.equipo.ipTipo ? ' (' + prep.equipo.ipTipo + ')' : ''), 'F1', 11);
  if (prep.equipo.anydeskId) row(anydeskLine(prep.equipo), 'F1', 11);
  if (redesLine(prep.equipo)) row(redesLine(prep.equipo), 'F1', 11);
  var vv = prep.versiones || {};
  if (vv.so || vv.antivirus || vv.esetAgent || vv.chrome) {
    row('Versiones detectadas:', 'F2', 12);
    if (vv.so) row('SO: ' + vv.so, 'F1', 11);
    if (vv.antivirus) row('Antivirus: ' + vv.antivirus, 'F1', 11);
    if (vv.esetAgent) row('Agente ESET: ' + vv.esetAgent, 'F1', 11);
    if (vv.chrome) row('Chrome: ' + vv.chrome, 'F1', 11);
  }
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
      if (isRemoved(prep, it.id)) return;
      var mark = isNA(prep, it.id) ? '[N/A] ' : (prep.checks[it.id] ? '[x] ' : '[ ] ');
      wrapText(mark + itemDisplayText(prep, it), 82).forEach(function (ln) { row(ln, 'F1', 11); });
    });
    row('', 'F1', 11);
  });
  row('Generado el ' + fmtDate(Date.now()) + ' — Checklist de Soporte', 'F1', 10);
  return assemblePdf(rows);
}
async function sharePdf(prep) {
  var blob = buildPdf(prep);
  var name = ('checklist-' + (prep.equipo.marca || 'equipo') + '-' + (prep.equipo.modelo || '') + '-' + (prep.equipo.serie || '')).toLowerCase()
    .replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '') + '.pdf';
  var texto = 'Checklist de Soporte: ' + (prep.equipo.marca || 'Equipo') + ' ' + (prep.equipo.modelo || '') +
    ' — ' + progress(prep) + '% completado (' + statusLabel(statusOf(prep)) + ').';
  // (254) En teléfono el PDF se guarda de verdad (ver sharePdfMant); en
  // escritorio/navegador sigue el camino web de siempre.
  try {
    var res = await guardarPdfCapacitor(blob, name, texto);
    if (res === 'guardado') return;
  } catch (e) {
    showToast('No se pudo guardar el PDF: ' + (e && e.message ? e.message : 'error al escribir el archivo'));
    return;
  }
  var file = new File([blob], name, { type: 'application/pdf' });
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
    showToast('PDF descargado: ' + name + '. Compártelo por WhatsApp desde tus archivos.');
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
  var headers = ['Tipo', 'Marca', 'Modelo', 'No. de serie', 'No. de inventario', 'Hostname', 'CPU', 'RAM', 'Disco', 'IP', 'AnyDesk', 'Redes', 'Usuario', 'Área', 'Correo', 'Analista', 'Estado', 'Avance %', 'Puntos N/A', 'Creado', 'Entregado', 'Reasignaciones'];
  var rows = preps.map(function (p) {
    return [p.equipo.tipo, p.equipo.marca, p.equipo.modelo, p.equipo.serie, p.equipo.inventario, p.equipo.hostname,
      p.equipo.cpu || '', (p.equipo.ramGB != null && p.equipo.ramGB !== '' ? p.equipo.ramGB + ' GB' : ''),
      (p.equipo.discoGB != null && p.equipo.discoGB !== '' ? p.equipo.discoGB + ' GB' + (p.equipo.discoTipo ? ' ' + p.equipo.discoTipo : '') : ''),
      (p.equipo.ip ? p.equipo.ip + (p.equipo.ipTipo ? ' (' + p.equipo.ipTipo + ')' : '') : ''),
      (p.equipo.anydeskId ? anydeskDisplay(p.equipo.anydeskId) + (p.equipo.anydeskAlias ? ' (' + p.equipo.anydeskAlias + ')' : '') : ''),
      redesText(p.equipo || {}),
      p.usuario.nombre, p.usuario.area, p.usuario.correo, p.tecnico,
      statusLabel(statusOf(p)), progress(p), naText(p), fmtDate(p.createdAt), p.deliveredAt ? fmtDate(p.deliveredAt) : '', reassignText(p)];
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
  if (flow === 'for') {
    var lSel = rentaSelListFor();
    if (!lSel.todos.length) { showToast('No hay equipos de renta en esta sección.'); return; }
    list = lSel.sel.length ? lSel.sel : lSel.todos;
    if (!lSel.sel.length) showToast('Sin selección: se exportan todos los equipos entregados.');
  }
  if (!list.length) { showToast('No hay equipos de renta en esta sección.'); return; }
  var blob = buildXlsxRenta(list, flow);
  var name = flow === 'rec' ? 'equipos-renta-recibir.xlsx' : 'equipos-renta-entrega.xlsx';
  try {
    await openXlsxFile(blob, name);
  } catch (e) {
    showToast('No se pudo abrir el archivo. Usa Compartir para mandarlo por WhatsApp o Drive.');
  }
}
async function shareRentaFile(flow, channel) {
  var list = rentaList(flow);
  if (flow === 'for') {
    var lSel2 = rentaSelListFor();
    if (!lSel2.todos.length) { showToast('No hay equipos de renta en esta sección.'); return; }
    list = lSel2.sel.length ? lSel2.sel : lSel2.todos;
    if (!lSel2.sel.length) showToast('Sin selección: se comparten todos los equipos entregados.');
  }
  if (!list.length) { showToast('No hay equipos de renta en esta sección.'); return; }
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
    showToast('No se pudo compartir el archivo. Usa Abrir para verlo en el teléfono.');
  }
}
function cleanName(s) {
  return String(s || '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
}
async function shareXlsx(preps, name, dialogTitle) {
  if (!preps.length) { showToast('No hay equipos para compartir.'); return; }
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
    showToast('No se pudo compartir el archivo. Usa Abrir para verlo en el teléfono.');
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
  var hwOne = hardwareLine(p.equipo || {});
  if (hwOne) lines.push(hwOne);
  var adOne = anydeskLine(p.equipo || {});
  if (adOne) lines.push(adOne);
  var redesOne = redesLine(p.equipo || {});
  if (redesOne) lines.push(redesOne);
  var verOne = versionesLine(p.versiones);
  if (verOne) lines.push(verOne);
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
  var naOne = naText(p);
  if (naOne) lines.push('No aplica (N/A): ' + naOne);
  return lines.join('\n');
}
function waTextAll(list) {
  var counts = { preparacion: 0, listo: 0, entregado: 0 };
  list.forEach(function (p) { counts[statusOf(p)]++; });
  var lines = ['🖥️ Checklist de Soporte — ' + list.length + ' equipos', '',
    'En preparación: ' + counts.preparacion + ' · Listos: ' + counts.listo + ' · Entregados: ' + counts.entregado, ''];
  list.forEach(function (p) {
    var extra = [];
    var hwAll = hardwareLine(p.equipo || {});
    if (hwAll) extra.push(hwAll);
    var adAll = anydeskLine(p.equipo || {});
    if (adAll) extra.push(adAll);
    var redesAll = redesLine(p.equipo || {});
    if (redesAll) extra.push(redesAll);
    var verAll = versionesLine(p.versiones);
    if (verAll) extra.push(verAll);
    lines.push('• ' + (p.equipo.marca || 'Equipo') + ' ' + (p.equipo.modelo || '') +
      ' — Serie: ' + (p.equipo.serie || '—') +
      (p.equipo.hostname ? ' — Host: ' + p.equipo.hostname : '') +
      ' — ' + (p.usuario.nombre || 'sin usuario') +
      ' — ' + statusLabel(statusOf(p)) + ' ' + progress(p) + '%' + (extra.length ? ' — ' + extra.join(' — ') : ''));
  });
  return lines.join('\n');
}
// Resumen de avance para equipos sin terminar: porcentaje, marcados/total
// y la lista de lo que falta (sin contar los N/A ni los quitados, que ya
// excluye requiredItems()). Lo usan 'Compartir avance' (WhatsApp) y
// 'Avance por correo' (mailto).
function avanceText(p) {
  var items = requiredItems(p);
  var done = items.filter(function (it) { return p.checks[it.id]; }).length;
  var pend = items.filter(function (it) { return !p.checks[it.id]; }).map(function (it) { return it.text; });
  var lines = ['Checklist de Soporte — Avance', '',
    (p.equipo.marca || 'Equipo') + ' ' + (p.equipo.modelo || ''),
    'Usuario: ' + (p.usuario.nombre || '—') + (p.usuario.area ? ' (' + p.usuario.area + ')' : ''),
    'Analista: ' + (p.tecnico || '—'),
    'Estado: ' + statusLabel(statusOf(p)) + ' — ' + progress(p) + '% (' + done + '/' + items.length + ' puntos)'];
  if (pend.length) {
    lines.push('', 'Falta:');
    pend.forEach(function (t) { lines.push('• ' + t); });
  } else {
    lines.push('', 'Checklist completo ✓');
  }
  var na = naText(p);
  if (na) lines.push('', 'No aplica (N/A): ' + na);
  return lines.join('\n');
}
// Avance por correo: abre el correo con el resumen como cuerpo del mensaje.
function shareAvanceMail(p) {
  var asunto = 'Avance — ' + (p.equipo.marca || 'Equipo') + ' ' + (p.equipo.modelo || '');
  window.location.href = 'mailto:?subject=' + encodeURIComponent(asunto) + '&body=' + encodeURIComponent(avanceText(p));
}
function shareText(texto) {
  if (navigator.share) {
    navigator.share({ title: 'Checklist de Soporte', text: texto }).catch(function () {});
    return;
  }
  window.open('https://wa.me/?text=' + encodeURIComponent(texto), '_blank');
}
function shareWhatsApp(preps, texto) {
  // Con texto (avanceText) se comparte ese resumen; sin texto, el
  // resumen normal del equipo o de la lista, como antes.
  if (!preps.length && !texto) { showToast('No hay equipos para compartir.'); return; }
  shareText(texto || (preps.length === 1 ? waTextOne(preps[0]) : waTextAll(preps)));
}

function currentList() {
  var q = searchText.trim().toLowerCase();
  var list = state.preparations.filter(function (p) {
    if (!deliveredVisible(p)) return false;
    // Admin con un analista elegido: solo los equipos de ese analista.
    if (cloudRole === 'admin' && adminViewUid && adminViewUid !== 'todos' && !isPrepOfAnalyst(p, adminViewUid)) return false;
    // Equipos de otros analistas ocultos por defecto (238b): solo se ven
    // con el interruptor 'Ver equipos de otros analistas'. Al admin no le
    // aplica: usa el selector 'Todos los usuarios'. Sin sesión (modo
    // local) no hay ajenos: isOwnPrep devuelve true para todos.
    if (cloudRole !== 'admin' && !showOthers && !isOwnPrep(p)) return false;
    // Pestañas por usuario (251): solo equipos propios. 'Nuevo' = propio
    // en preparación o listo, sin reasignaciones; 'Reasignado' = propio con
    // al menos una reasignación; 'Devuelto' = propio ya entregado. El admin
    // ve en estas pestañas los equipos de todos (permisos totales).
    if (filterStatus === 'nuevo') {
      if (cloudRole !== 'admin' && !isOwnPrep(p)) return false;
      if (statusOf(p) === 'entregado') return false;
      if ((p.reasignaciones || []).length) return false;
    } else if (filterStatus === 'reasignado') {
      if (cloudRole !== 'admin' && !isOwnPrep(p)) return false;
      if (!(p.reasignaciones || []).length) return false;
    } else if (filterStatus === 'devuelto') {
      if (cloudRole !== 'admin' && !isOwnPrep(p)) return false;
      if (statusOf(p) !== 'entregado') return false;
    } else if (filterStatus !== 'todos' && statusOf(p) !== filterStatus) return false;
    if (!q) return true;
    var hay = [p.equipo.tipo, p.equipo.marca, p.equipo.modelo, p.equipo.serie, p.equipo.inventario, p.equipo.hostname,
      p.usuario.nombre, p.usuario.area, p.usuario.correo, p.tecnico,
      (p.reasignaciones || []).map(function (r) { return (r.de || '') + ' ' + (r.a || ''); }).join(' ')].join(' ').toLowerCase();
    return hay.indexOf(q) !== -1;
  });
  // Vista principal (251): primero los propios, en el orden en que se
  // prepararon (createdAt ascendente, el más antiguo primero), y luego los
  // de otros analistas. El admin no usa este orden: ve todos en orden de
  // preparación.
  // (253) Entregados y Devuelto: el recién entregado arriba — deliveredAt
  // descendente y, en empate, createdAt descendente. Los demás filtros
  // conservan createdAt ascendente.
  var ordenEntregados = filterStatus === 'entregado' || filterStatus === 'devuelto';
  function cmpEntregado(a, b) {
    var d = (b.deliveredAt || 0) - (a.deliveredAt || 0);
    return d !== 0 ? d : b.createdAt - a.createdAt;
  }
  if (cloudRole === 'admin') {
    list.sort(ordenEntregados ? cmpEntregado : function (a, b) { return a.createdAt - b.createdAt; });
  } else {
    list.sort(function (a, b) {
      var ao = isOwnPrep(a) ? 0 : 1, bo = isOwnPrep(b) ? 0 : 1;
      if (ao !== bo) return ao - bo;
      return ordenEntregados ? cmpEntregado(a, b) : a.createdAt - b.createdAt;
    });
  }
  return list;
}

// Equipos de renta: recepcion (rec) y entrega (for).
var ACCS_LABEL = { cargador: 'Cargador', cable: 'Cable', mouse: 'Mouse', maletin: 'Maletín', teclado: 'Teclado', cableCorriente: 'Cable de corriente', cableVideo: 'Cable de video', tarjetaVideo: 'Tarjeta de vídeo' };
var ACCS_POR_TIPO = { Laptop: ['mouse', 'cargador', 'maletin'], iPad: ['cargador', 'cable'], PC: ['cableCorriente', 'mouse', 'teclado', 'cableVideo', 'tarjetaVideo'] };
// (255) Seleccion en Entrega Renta: checkbox por equipo entregado.
// Compartir (WhatsApp/correo) y Exportar a Excel actuan sobre los
// marcados; sin seleccion, sobre todos los entregados visibles.
var rentaSelFor = {};
// (255) Entregados de renta: como Por preparar (DELIVERED_VISIBLE_DAYS =
// 15) — el usuario normal los sigue viendo 15 dias despues de la entrega;
// pasado ese tiempo solo los ve el admin. Sin entregadoAt (registros
// viejos), se usa createdAt como respaldo.
function rentaEntregadoVisible(r) {
  if (!r || r.estado !== 'entregado') return true;
  if (!CLOUD_ENABLED || cloudRole === 'admin') return true;
  var t = r.entregadoAt || r.createdAt || 0;
  return (Date.now() - t) <= DELIVERED_VISIBLE_DAYS * 86400000;
}
function rentaEntregadosFor() {
  return rentaList('for').filter(function (r) { return r.estado === 'entregado'; });
}
function rentaSelListFor() {
  var todos = rentaEntregadosFor();
  var sel = todos.filter(function (r) { return rentaSelFor[r.id]; });
  return { todos: todos, sel: sel };
}
function rentaSelTodosFor(sel) {
  rentaEntregadosFor().forEach(function (r) { if (sel) rentaSelFor[r.id] = true; else delete rentaSelFor[r.id]; });
  render();
}
function rentaActualizarSelInfo() {
  var el = document.getElementById('rentaSelInfo');
  if (!el) return;
  var l = rentaSelListFor();
  el.textContent = l.sel.length ? ('Seleccionados: ' + l.sel.length + ' de ' + l.todos.length + ' entregados.') : ('Sin selección: se exportan/comparten todos los entregados (' + l.todos.length + ').');
}
function rentaList(flow) {
  // Recibir renta: solo los equipos pendientes de entregar.
  // Entrega Renta: todos los equipos de renta, lleguen de donde lleguen.
  if (flow === 'rec') {
    return state.renta.filter(function (r) { return r.flujo === 'rec' && r.estado !== 'entregado'; })
      .sort(function (a, b) { return a.createdAt - b.createdAt; });
  }
  var list = state.renta.slice();
  // Entregados: el usuario normal los ve 15 dias (rentaEntregadoVisible);
  // pasado ese tiempo solo los ve el admin.
  list = list.filter(rentaEntregadoVisible);
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
  var btnExp = document.getElementById(flow === 'rec' ? 'btnAbrirRec' : 'btnAbrirFor');
  if (btnExp) btnExp.disabled = flow === 'rec' ? !list.length : !list.some(function (r) { return r.estado === 'entregado'; });
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
  // Entregados: el usuario normal los ve 15 dias (rentaEntregadoVisible);
  // pasado ese tiempo solo los ve el admin.
  list = list.filter(rentaEntregadoVisible);
  return list.sort(function (a, b) { return (orden[a.tipo] - orden[b.tipo]) || (a.createdAt - b.createdAt); });
}
function renderEntrega() {
  var box = document.getElementById('list-for');
  var cola = entregaCola();
  var btnExpFor = document.getElementById('btnAbrirFor');
  if (btnExpFor) btnExpFor.disabled = !cola.some(function (r) { return r.estado === 'entregado'; });
  if (!cola.length) {
    var msg = (CLOUD_ENABLED && cloudRole !== 'admin' && state.renta.length)
      ? 'No hay equipos por entregar. Los entregados hace más de 15 días solo los ve el administrador.'
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
  var entregados = cola.filter(function (r) { return r.estado === 'entregado'; });
  if (entregados.length) {
    html += '<div class="sub" style="margin-top:14px"><b>Equipos entregados (' + entregados.length + ')</b> — marca los que quieres exportar o compartir:</div>';
    html += '<div class="actions"><button class="btn-ghost" data-renta-sel-all>Seleccionar todos</button><button class="btn-ghost" data-renta-sel-none>Ninguno</button></div>';
    html += '<div class="share-note" id="rentaSelInfo"></div>';
    html += entregados.map(function (r) {
      var chk = rentaSelFor[r.id] ? ' checked' : '';
      return '<div class="sub"><label><input type="checkbox" data-renta-sel="' + esc(r.id) + '"' + chk + ' style="width:auto"> ' + esc(r.tipo + ' ' + (r.modelo || '') + ' · Inv. ' + (r.inventario || '—') + ' · Entregado por ' + (r.entregadoPor || '—')) + '</label></div>';
    }).join('');
  }
  box.innerHTML = html;
  rentaActualizarSelInfo();
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
    recibidoPor: technicianName(), entregadoPor: '', entregadoAt: null
  };
  if (!rec.modelo && !rec.inventario) { showToast('Pon al menos el modelo o el número de inventario de renta.'); return; }
  state.renta.push(rec);
  cloudUpsert(rec);
  save();
  ['modelo', 'inv', 'cap', 'cpu', 'danos', 'obs'].forEach(function (f) { document.getElementById('fR-' + flow + '-' + f).value = ''; });
  if (flow === 'rec') { window._fotoDanos = null; document.getElementById('fotoDanosPreview').innerHTML = ''; document.getElementById('fFotoDanos').value = ''; }
  document.getElementById('fR-' + flow + '-sindanos').checked = false;
  updateRentaForm(flow);
  render();
}

// Tarjetas con sección aparte para los equipos de otros analistas
// (solo lectura): primero los propios, luego el encabezado y los ajenos.
function sectionedCards(list) {
  if (cloudRole === 'admin') return list.map(cardHtml).join('');
  var own = list.filter(isOwnPrep);
  var other = list.filter(function (p) { return !isOwnPrep(p); });
  var html = own.map(cardHtml).join('');
  if (other.length) html += '<div class="group-title">Equipos de otros analistas (solo lectura)</div>' + other.map(cardHtml).join('');
  return html;
}
function todosListHtml(list) {
  var activos = list.filter(function (p) { return statusOf(p) !== 'entregado'; });
  var entregados = list.filter(function (p) { return statusOf(p) === 'entregado'; });
  var html = sectionedCards(activos);
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
  var voBtn = document.getElementById('btnVerOtros');
  if (voBtn) {
    voBtn.hidden = (cloudRole === 'admin' || !cloudUser);
    voBtn.textContent = showOthers ? '🙈 Ocultar equipos de otros analistas' : '👀 Ver equipos de otros analistas';
    voBtn.classList.toggle('on', !!showOthers);
  }
  document.getElementById('shareBar').hidden = filterStatus !== 'entregado' && filterStatus !== 'devuelto';
  refreshDetectarBtn();
  if (window.Desktop) loadMachineId();

  var list = currentList();

  var box = document.getElementById('list');
  if (!list.length) {
    box.innerHTML = '<div class="empty">No hay equipos aquí todavía.<br>Agrega uno con “Nuevo equipo por preparar”.</div>';
  } else if (filterStatus === 'todos') {
    box.innerHTML = todosListHtml(list);
  } else {
    box.innerHTML = sectionedCards(list);
  }
  renderTemplate();
  renderRenta('rec');
  renderEntrega();
  updateFocusDiag();
}

function cardHtml(p) {
  var st = statusOf(p);
  var pct = progress(p);
  // Listo con pendientes (251): marcado Listo con avance <100% — la
  // tarjeta NO se presenta como lista para entregar: letrero prominente
  // y etiqueta 'Equipo con pendientes'. Derivado de readyAt + avance,
  // así que se actualiza solo al marcar/quitar puntos (cada render lo
  // recalcula). Al llegar al 100% vuelve a 'Listo para entregar' con su
  // botón 'Entregado' normal.
  var conPendientes = st === 'listo' && p.readyAt && pct < 100;
  var pendientesN = conPendientes ? pendingRequired(p).length : 0;
  // Borrador (238b): la etiqueta es 'Borrador' sea cual sea el avance
  // (un borrador al 100% tampoco se presenta como listo para entregar:
  // le faltan los datos del usuario). La línea de abajo dice qué falta.
  var stateLabel = p.borrador ? 'Borrador' : (conPendientes ? 'Equipo con pendientes' : statusLabel(st));
  var stateClass = p.borrador ? 'b-prep' : statusClass(st);
  var items = allItems(p);
  var locked = !!p.deliveredAt;
  var editable = canEditPrep(p);
  var groupsHtml = GROUP_ORDER.map(function (g) {
    var gi = items.filter(function (it) { return it.group === g; });
    if (!gi.length) return '';
    var rows = gi.map(function (it) {
      if (isRemoved(p, it.id)) return '';
      var checked = !!p.checks[it.id];
      var del = (it.extra && editable) ? '<button class="x" data-del-extra="' + it.id + '" data-prep="' + p.id + '" title="Quitar punto">×</button>' : '';
      // N/A: el punto no cuenta y no se pide; tocar de nuevo lo deshace.
      // Quitar (✕, solo puntos de plantilla: los extra ya tienen su ×):
      // el punto se oculta y se puede restaurar desde la tarjeta.
      var na = isNA(p, it.id);
      if (na) {
        return '<div class="item"><label>' + esc(it.text) + '</label> <span class="badge badge-na">N/A</span>' +
          ((locked || !editable) ? '' : ' <button class="btn-ghost btn-mini" data-na="' + it.id + '" data-prep="' + p.id + '">N/A</button>') + del + '</div>';
      }
      var naBtns = (!locked && editable && !checked)
        ? ' <button class="btn-ghost btn-mini" data-na="' + it.id + '" data-prep="' + p.id + '">N/A</button>' +
          (it.extra ? '' : ' <button class="btn-ghost btn-mini" data-remove-item="' + it.id + '" data-prep="' + p.id + '" title="Quitar punto">✕</button>') : '';
      if (it.options) {
        var opts = it.options.map(function (o) {
          var sel = p.checks[it.id] === o;
          return '<button class="chip' + (sel ? ' on' : '') + '" data-choice="' + it.id + '" data-prep="' + p.id + '" data-value="' + esc(o) + '"' + ((locked || !editable) ? ' disabled' : '') + '>' + esc(o) + '</button>';
        }).join(' ');
        var hint = checked ? '' : ' <span class="choice-hint">⚠️ Elige una opción</span>';
        return '<div class="item' + (checked ? ' done' : '') + '" style="flex-wrap:wrap">' +
          '<label>' + esc(it.text) + '</label> ' + opts + hint + naBtns + del + '</div>';
      }
      return '<div class="item' + (checked ? ' done' : '') + '">' +
        '<input type="checkbox" data-check="' + it.id + '" data-prep="' + p.id + '"' +
        (checked ? ' checked' : '') + ((locked || !editable) ? ' disabled' : '') + '>' +
        '<label>' + esc(it.text) + '</label>' + naBtns + del + '</div>';
    }).join('');
    var verBlock = '';
    if (g === 'software') { var vlCard = versionesLine(p.versiones); if (vlCard) verBlock = '<div class="sub">' + esc(vlCard) + '</div>'; }
    return '<div class="group"><h3>' + GROUPS[g] + '</h3>' + rows + verBlock + '</div>';
  }).join('');

  // Equipo ajeno (251): solo lectura — solo WhatsApp y correo, más
  // 'Solicitar asignación' (ver solicitudHtml más abajo). Nada de editar:
  // ni casillas, ni N/A/quitar, ni Listo/Entregado, ni Reasignar, ni
  // Eliminar, ni PDF, ni Excel, ni IA, ni Compartir avance ni No listo.
  var actions = '';
  if (!editable) {
    actions += '<button class="btn-ghost" data-wa="' + p.id + '">Enviar datos por WhatsApp</button>';
    actions += '<button class="btn-ghost" data-mail="' + p.id + '">Enviar por correo</button>';
  } else {
    // Borrador (238b): solo el dueño o el admin (editable) lo ve; un
    // equipo ajeno nunca muestra este botón (su tarjeta es solo lectura).
    if (p.borrador) actions += '<button class="btn-green" data-completar="' + p.id + '">📝 Completar datos</button>';
    // Borrador sin Listo (238b): hasta completarlo no sigue el flujo
    // (así nunca muestra 'Equipo con pendientes' siendo borrador).
    if (st === 'preparacion' && !p.borrador) actions += '<button class="btn-green" data-ready="' + p.id + '">Listo</button>';
    // Entrega (251): con pendientes el botón dice 'Entregar', no
    // 'Entregado': no debe leerse como si estuviera al 100%. El handler
    // data-deliver ya muestra el panel de confirmación a <100%.
    if (st === 'listo' && !p.borrador) actions += '<button class="btn-green" data-deliver="' + p.id + '">' + (pct < 100 ? 'Entregar' : 'Entregado') + '</button>';
    // Guardar avance (251): guardado explícito del checklist mientras se
    // revisa (en preparación o listo, propio o admin; nunca ajeno — la rama
    // !editable no lo muestra — ni entregado). El guardado automático por
    // cambio sigue igual; este botón solo añade la confirmación visible.
    // Borradores: sí aparece (su checklist también se revisa y se guarda).
    if (st === 'preparacion' || st === 'listo') actions += '<button class="btn-ghost" data-guardar-avance="' + p.id + '">💾 Guardar avance</button>';
    if ((st === 'preparacion' || st === 'listo') && pct < 100) {
      actions += '<button class="btn-ghost" data-share-avance="' + p.id + '">📤 Compartir avance</button>';
      actions += '<button class="btn-ghost" data-mail-avance="' + p.id + '">✉️ Avance por correo</button>';
      actions += '<button class="btn-ghost" data-nolisto="' + p.id + '">No listo</button>';
    }
    if (st === 'listo' && p.readyAt && pct < 100) actions += '<button class="btn-ghost" data-unready="' + p.id + '">Quitar listo</button>';
    if (st === 'entregado') actions += '<button class="btn-ghost" data-reopen="' + p.id + '">Reabrir</button>';
    if (!locked) actions += '<button class="btn-ghost" data-add-extra="' + p.id + '">+ Punto extra</button>';
    if ((st === 'preparacion' || st === 'listo') && !locked) actions += '<button class="btn-dark" data-asignar="' + p.id + '">Asignar a…</button>';
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
  }

  var deliveredLine = p.deliveredAt ? '<div class="delivered-line">Entregado el ' + fmtDate(p.deliveredAt) + '</div>' : '';
  var redesCard = redesLine(p.equipo || {});
  // Listo con pendientes (251): letrero prominente, mismo estilo visible
  // que el marcador 'No listo' de la 2.3.6. Si el equipo ya tiene el
  // marcador 'No listo', no se duplica: manda el letrero de pendientes
  // (el de 'No listo' solo se ve en preparación). En la práctica no
  // coexisten (Listo borra noListo y 'No listo' limpia readyAt).
  // Borrador (238b): qué datos faltan (inventario, usuario, área,
  // correo). Convive con 'Equipo con pendientes' sin confundirse: ese
  // letrero solo existe en Listo (readyAt), y un borrador nunca llega a
  // Listo (el botón Listo está oculto hasta completarlo), así que en una
  // misma tarjeta solo se ve uno de los dos.
  var faltanDatos = [];
  if (p.borrador) {
    if (!p.equipo.inventario) faltanDatos.push('inventario');
    if (!p.usuario.nombre) faltanDatos.push('usuario');
    if (!p.usuario.area) faltanDatos.push('área');
    if (!p.usuario.correo) faltanDatos.push('correo');
  }
  var borradorLine = p.borrador ? '<div class="sub">📝 Borrador — faltan datos' + (faltanDatos.length ? ': ' + faltanDatos.join(', ') : '') + '</div>' : '';
  var pendientesLine = conPendientes ? '<div class="sub">⚠️ Equipo con pendientes — faltan ' + pendientesN + ' puntos</div>' : '';
  var noListoLine = (!conPendientes && p.noListo) ? '<div class="sub">⚠️ No listo — faltan ' + (p.noListo.faltan || 0) + ' puntos</div>' : '';
  var detNote = (p.autoDetectado && p.autoDetectado.length)
    ? '<div class="sub">Puntos marcados por el detector: ' + esc(detectedNames(p.checks, p.autoDetectado).join(', ')) + '</div>' : '';
  var hwLine = hardwareLine(p.equipo || {});
  var adLine = anydeskLine(p.equipo || {});
  var reassignLine = (p.reasignaciones && p.reasignaciones.length)
    ? '<div class="sub">Reasignaciones: ' + esc(reassignText(p)) + '</div>' : '';
  var asignLine = (p.asignaciones && p.asignaciones.length)
    ? '<div class="sub">Asignaciones: ' + esc(asignacionesText(p)) + '</div>' : '';
  // Solicitud de asignación (251): solo hay una pendiente a la vez. El
  // admin ve Aprobar/Rechazar; el solicitante ve Cancelar solicitud; otro
  // usuario solo ve de quién es la solicitud pendiente.
  var sol = p.solicitudAsignacion && p.solicitudAsignacion.estado === 'pendiente' ? p.solicitudAsignacion : null;
  var solicitudHtml = '';
  if (sol) {
    if (cloudRole === 'admin') {
      solicitudHtml = '<div class="sub">📩 ' + esc(sol.deNombre || 'Un analista') + ' pide que se le asigne este equipo para terminarlo.</div>' +
        '<div class="actions"><button class="btn-green" data-aprobar-solicitud="' + p.id + '">Aprobar asignación</button>' +
        '<button class="btn-ghost" data-rechazar-solicitud="' + p.id + '">Rechazar</button></div>';
    } else if (cloudUser && sol.deUid === cloudUser.uid) {
      solicitudHtml = '<div class="sub">📩 Solicitud de asignación enviada (pendiente).</div>' +
        '<div class="actions"><button class="btn-ghost" data-cancel-solicitud="' + p.id + '">Cancelar solicitud</button></div>';
    } else {
      solicitudHtml = '<div class="sub">📩 Solicitud pendiente de ' + esc(sol.deNombre || 'otro analista') + '</div>';
    }
  } else if (!editable && cloudUser) {
    solicitudHtml = '<div class="actions"><button class="btn-dark" data-solicitar-asignacion="' + p.id + '">Solicitar asignación</button></div>';
  }
  var asignarForm = (editable && window._asignarFor === p.id && (st === 'preparacion' || st === 'listo'))
    ? '<div class="row" style="margin-top:10px"><select id="asignarSelect" style="flex:1">' + analystOptionsHtml(p.tecnicoUid || (cloudUser && cloudUser.uid)) + '</select>' +
      '<button class="btn-dark" data-save-asignar="' + p.id + '">Asignar</button></div>' +
      (teamUsers.filter(function (u) { return u.uid !== (p.tecnicoUid || (cloudUser && cloudUser.uid)); }).length ? '' : '<div class="sub">No hay otros analistas todavía.</div>') : '';
  var reassignForm = (cloudRole === 'admin' && window._reassignFor === p.id)
    ? '<div class="row" style="margin-top:10px"><input id="reDe" placeholder="Era de..." value="' + esc(p.usuario.nombre || '') + '">' +
      '<input id="reA" placeholder="Se reasigna a...">' +
      '<button class="btn-dark" data-save-reassign="' + p.id + '">Guardar reasignación</button></div>' : '';
  var extraForm = (!locked && editable && window._extraFor === p.id)
    ? '<div class="row" style="margin-top:10px"><input id="extraText" placeholder="Punto extra para este equipo...">' +
      '<select id="extraGroup" style="max-width:130px"><option value="hardware">Hardware</option><option value="software">Software</option><option value="datos">Datos usuario</option></select>' +
      '<button class="btn-dark" data-save-extra="' + p.id + '">Agregar</button></div>' : '';
  var removedLine = (!locked && editable && p.removedItems && p.removedItems.length)
    ? '<div class="sub">Puntos quitados: ' + p.removedItems.length + ' <button class="btn-ghost btn-mini" data-restore-removed="' + p.id + '">Restaurar</button></div>' : '';
  // Panel de entrega con avance <100%: qué falta (porcentaje y casillas)
  // y dos salidas explícitas; al 100% no se muestra (entrega directa).
  var deliverPanel = (window._deliverConfirmFor === p.id && st === 'listo' && pct < 100)
    ? '<div class="sub" style="margin-top:10px"><b>⚠️ Este equipo no está al 100% (avance ' + pct + '%) — faltan ' + pendingRequired(p).length + ' puntos:</b></div>' +
      pendingRequired(p).map(function (it) { return '<div class="sub">• ' + esc(it.text) + '</div>'; }).join('') +
      '<div class="actions"><button class="btn-green" data-deliver-reopen="' + p.id + '">Reabrir para completar</button>' +
      '<button class="btn-dark" data-deliver-confirm="' + p.id + '">Entregar así</button></div>' : '';

  return '<div class="card">' +
    '<h2>' + esc(p.equipo.marca || 'Equipo') + ' ' + esc(p.equipo.modelo || '') + '</h2>' +
    '<div class="sub">' + esc(p.equipo.tipo) + ' · Serie: ' + esc(p.equipo.serie || '—') + ' · Inv: ' + esc(p.equipo.inventario || '—') + (p.equipo.hostname ? ' · Host: ' + esc(p.equipo.hostname) : '') + '</div>' +
    (hwLine ? '<div class="sub">' + esc(hwLine) + '</div>' : '') +
    (adLine ? '<div class="sub">' + esc(adLine) + '</div>' : '') +
    (redesCard ? '<div class="sub">' + esc(redesCard) + '</div>' : '') +
    (p.equipo.fotoSerie ? '<img class="foto-serie" src="' + p.equipo.fotoSerie + '" alt="Foto del número de serie" title="Toca para ampliar">' : '') +
    '<div class="sub">Usuario: <b>' + esc(p.usuario.nombre || '—') + '</b>' +
    (p.usuario.area ? ' · ' + esc(p.usuario.area) : '') +
    (p.usuario.correo ? '<br>' + esc(p.usuario.correo) : '') +
    (p.tecnico ? '<br>Analista: ' + esc(p.tecnico) : '') + '</div>' +
    '<span class="badge ' + stateClass + '">' + stateLabel + '</span>' +
    '<div class="bar"><i style="width:' + pct + '%"></i></div>' +
    '<div class="pct">' + pct + '% completado</div>' + deliveredLine + noListoLine + pendientesLine + borradorLine + reassignLine + asignLine + detNote +
    groupsHtml + removedLine + deliverPanel + extraForm + reassignForm + solicitudHtml + asignarForm +
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

document.getElementById('adminUserFilter').addEventListener('change', function (e) {
  adminViewUid = e.target.value || 'todos';
  todosPage = 0;
  window._expandedId = null;
  render();
});
// Interruptor 'Ver equipos de otros analistas' (238b): revela u oculta
// la sección de ajenos en todos los filtros de Por preparar. Se recuerda
// por teléfono (localStorage); el admin no lo ve (usa su selector).
document.getElementById('btnVerOtros').addEventListener('click', function () {
  showOthers = !showOthers;
  try { localStorage.setItem(SHOW_OTHERS_KEY, showOthers ? '1' : '0'); } catch (e) { /* sin persistencia */ }
  render();
});
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
document.getElementById('btnShowNew').addEventListener('click', function () { window._detectedChecks = null; window._detectedDetalles = null; window._detectedVersiones = null; window._detectedHardware = null; window._completarBorradorId = null; document.getElementById('btnAdd').textContent = '💾 Guardar equipo'; togglePanel('newBox'); });
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
// Detección de escritorio (252): flujo compartido por #btnDetectar
// (Por preparar) y #btnMantDetectar (Mantenimientos). Recibe el botón
// pulsado y devuelve una promesa que resuelve true si la detección se
// reportó y false si no (sin Desktop, sin sesión, bloqueado o error).
function detectarEquipo(btn) {
  if (!window.Desktop || !window.Desktop.detect) { showToast('La detección solo funciona en la app de escritorio.'); return Promise.resolve(false); }
  if (!cloudUser) { showToast('Inicia sesión para reportar el equipo detectado.'); return Promise.resolve(false); }
  if (btn.disabled) return Promise.resolve(false); // ya detectando, o esta máquina ya tiene una detección pendiente
  var oldHtml = btn.innerHTML;
  detectingNow = true;
  refreshDetectarBtn();
  var p;
  try { p = Promise.resolve(window.Desktop.detect()); } catch (e) { detectingNow = false; btn.disabled = false; btn.innerHTML = oldHtml; refreshDetectarBtn(); showToast('No se pudo detectar el equipo.'); return Promise.resolve(false); }
  return p.then(function (info) {
    if (!window.Cloud || !window.Cloud.reportDetected) throw new Error('sin-nube');
    var data = Object.assign({}, info || {});
    data.detectadoPor = technicianName();
    return window.Cloud.reportDetected(data);
  }).then(function () { showToast('Equipo detectado, ya aparece en los teléfonos'); return true; }).catch(function (e) { showToast('No se pudo detectar el equipo.' + (e && e.message ? ' ' + e.message : '')); return false; }).then(function (ok) { detectingNow = false; btn.disabled = false; btn.innerHTML = oldHtml; refreshDetectarBtn(); return ok; });
}
document.getElementById('btnDetectar').addEventListener('click', function () { detectarEquipo(document.getElementById('btnDetectar')); });
document.getElementById('detList').addEventListener('click', function (e) {
  var t = e.target;
  var use = t.closest('[data-det-use]');
  var del = t.closest('[data-det-del]');
  var sav = t.closest('[data-det-save]');
  if (!use && !del && !sav) return;
  var id = (use || del || sav).getAttribute(use ? 'data-det-use' : del ? 'data-det-del' : 'data-det-save');
  // Guardar para después (238b): crea el borrador en En preparación y
  // marca la detección como usada (sale del panel, igual que 'Usar este
  // equipo'). Si el borrador se elimina después, no vuelve al panel:
  // la detección sigue usada.
  if (sav) {
    var dd = detectados.find(function (x) { return String(x.id) === String(id); });
    if (!dd) return;
    var draft = prepFromDetectado(dd);
    state.preparations.push(draft);
    dd.usado = true;
    cloudMarkDetectadoUsado(dd.id);
    cloudUpsertPrep(draft);
    save();
    document.getElementById('detBox').hidden = true;
    setFilter('preparacion');
    render();
    return;
  }
  if (use) {
    var d = detectados.find(function (x) { return String(x.id) === String(id); });
    if (!d) return;
    // Borrador latente (251): si antes se abrió 'Completar datos' y se
    // cerró sin guardar, _completarBorradorId seguía puesto y Guardar
    // actualizaría ese borrador viejo en vez de crear un equipo nuevo.
    // Se limpia aquí igual que en btnShowNew, antes de rellenar el form.
    window._completarBorradorId = null; document.getElementById('btnAdd').textContent = '💾 Guardar equipo';
    document.getElementById('fTipo').value = d.tipo || 'Desktop';
    document.getElementById('fMarca').value = d.marca || '';
    document.getElementById('fModelo').value = d.modelo || '';
    document.getElementById('fSerie').value = d.serie || '';
    document.getElementById('fHostname').value = d.hostname || '';
    window._detectedChecks = d.checks || {};
    window._detectedDetalles = d.detalles || {};
    window._detectedVersiones = d.versiones || {};
    window._detectedHardware = { cpu: d.cpu || '', ramGB: (d.ramGB == null ? '' : d.ramGB), discoGB: (d.discoGB == null ? '' : d.discoGB), discoTipo: d.discoTipo || '', ip: d.ip || '', ipTipo: d.ipTipo || '', anydeskId: d.anydeskId || '', anydeskAlias: d.anydeskAlias || '', redes: Array.isArray(d.redes) ? d.redes : [] };
    cloudMarkDetectadoUsado(d.id);
    document.getElementById('detBox').hidden = true;
    document.getElementById('newBox').hidden = false;
    updateSaveBtn();
    return;
  }
  if (del) {
    // Confirmación inline (251): el modal es asíncrono; solo con Sí se
    // descarta el equipo detectado.
    showConfirm('¿Descartar este equipo detectado?').then(function (ok) { if (!ok) return; cloudDeleteDetectado(id); });
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
  if (!id) { showToast('Elige el equipo a reasignar.'); return; }
  if (!a) { showToast('Pon a quién se reasigna el equipo.'); return; }
  if (id === '__nuevo__') {
    var v = function (x) { return document.getElementById(x).value.trim(); };
    var prep = {
      id: uid(), createdAt: Date.now(), deliveredAt: null, readyAt: null, checks: {}, extraItems: [], naItems: {}, removedItems: [],
      reasignaciones: [{ de: de, a: a, fecha: Date.now(), analista: technicianName() }],
      equipo: { tipo: v('fReTipo'), marca: v('fReMarca'), modelo: v('fReModelo'), serie: v('fReSerie'), inventario: v('fReInv'), hostname: v('fReHostname'), fotoSerie: null },
      usuario: { nombre: a, area: '', correo: '' },
      tecnico: technicianName(),
      tecnicoUid: tecnicoUidFor(technicianName())
    };
    if (!prep.equipo.modelo && !prep.equipo.serie && !prep.usuario.nombre) { showToast('Pon al menos el modelo, la serie o el nombre del usuario.'); return; }
    state.preparations.push(prep);
  } else {
    var prep = state.preparations.find(function (x) { return x.id === id; });
    if (!prep) { showToast('Ese equipo ya no está en la lista.'); return; }
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
  // Completar borrador (238b): si se abrió el formulario con
  // 'Completar datos', Guardar actualiza ESE equipo (sin crear otro) y
  // quita la marca de borrador. Los checks no se tocan: se conservan los
  // detectados y los marcados a mano en la tarjeta. Si el borrador ya no
  // existe (o ya no es borrador), se sigue como equipo nuevo.
  var completarId = window._completarBorradorId || null;
  if (completarId) {
    var ex = state.preparations.find(function (x) { return x.id === completarId; });
    window._completarBorradorId = null;
    document.getElementById('btnAdd').textContent = '💾 Guardar equipo';
    if (ex && ex.borrador && canEditPrep(ex)) {
      if (!v('fModelo') && !v('fSerie') && !v('fUser')) { showToast('Pon al menos el modelo, la serie o el nombre del usuario.'); return; }
      ex.equipo.tipo = v('fTipo'); ex.equipo.marca = v('fMarca'); ex.equipo.modelo = v('fModelo'); ex.equipo.serie = v('fSerie'); ex.equipo.inventario = v('fInv'); ex.equipo.hostname = v('fHostname');
      if (window._fotoSerie) ex.equipo.fotoSerie = window._fotoSerie;
      ex.usuario.nombre = v('fUser'); ex.usuario.area = v('fArea'); ex.usuario.correo = v('fCorreo');
      ex.tecnico = v('fTec') || technicianName(); ex.tecnicoUid = tecnicoUidFor(v('fTec') || technicianName());
      delete ex.borrador;
      window._detectedChecks = null; window._detectedDetalles = null; window._detectedVersiones = null; window._detectedHardware = null;
      cloudUpsertPrep(ex);
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
      return;
    }
    // Si no se pudo completar, se sigue abajo como equipo nuevo con lo
    // que haya en el formulario (el borrador, si existe, queda intacto).
  }
  var det = filterDetectedChecks(window._detectedChecks || {});
  var detHw = window._detectedHardware || {};
  var detVer = window._detectedVersiones || {};
  var prep = {
    id: uid(), createdAt: Date.now(), deliveredAt: null, readyAt: null, checks: det.checks, autoDetectado: det.ids, extraItems: [], reasignaciones: [], naItems: {}, removedItems: [],
    versiones: { so: (typeof detVer.so === 'string' ? detVer.so : ''), antivirus: (typeof detVer.antivirus === 'string' ? detVer.antivirus : ''), esetAgent: (typeof detVer.esetAgent === 'string' ? detVer.esetAgent : ''), chrome: (typeof detVer.chrome === 'string' ? detVer.chrome : '') },
    equipo: { tipo: v('fTipo'), marca: v('fMarca'), modelo: v('fModelo'), serie: v('fSerie'), inventario: v('fInv'), hostname: v('fHostname'), cpu: detHw.cpu || '', ramGB: (detHw.ramGB == null ? '' : detHw.ramGB), discoGB: (detHw.discoGB == null ? '' : detHw.discoGB), discoTipo: detHw.discoTipo || '', ip: detHw.ip || '', ipTipo: detHw.ipTipo || '', anydeskId: detHw.anydeskId || '', anydeskAlias: detHw.anydeskAlias || '', redes: Array.isArray(detHw.redes) ? detHw.redes : [], fotoSerie: window._fotoSerie || null },
    usuario: { nombre: v('fUser'), area: v('fArea'), correo: v('fCorreo') },
    tecnico: v('fTec') || technicianName(),
    tecnicoUid: tecnicoUidFor(v('fTec') || technicianName())
  };
  if (!prep.equipo.modelo && !prep.equipo.serie && !prep.usuario.nombre) {
    showToast('Pon al menos el modelo, la serie o el nombre del usuario.');
    return;
  }
  state.preparations.push(prep);
  window._detectedChecks = null;
  window._detectedDetalles = null;
  window._detectedVersiones = null;
  window._detectedHardware = null;
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
  var prepId = q('data-prep') || q('data-deliver') || q('data-ready') || q('data-unready') || q('data-reopen') || q('data-add-extra') || q('data-del-prep') || q('data-save-extra') || q('data-pdf') || q('data-xlsx') || q('data-wa') || q('data-mail') || q('data-reassign') || q('data-save-reassign') || q('data-expand') || q('data-collapse') || q('data-choice') || q('data-ai-falta') || q('data-ai-wa') || q('data-na') || q('data-remove-item') || q('data-restore-removed') || q('data-share-avance') || q('data-mail-avance') || q('data-nolisto') || q('data-deliver-reopen') || q('data-deliver-confirm') || q('data-asignar') || q('data-save-asignar') || q('data-solicitar-asignacion') || q('data-cancel-solicitud') || q('data-aprobar-solicitud') || q('data-rechazar-solicitud') || q('data-completar') || q('data-guardar-avance');
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
  // Guarda defensiva (251): un equipo ajeno es solo lectura para un
  // usuario normal. Solo WhatsApp y correo pasan; el resto se ignora con
  // un aviso breve. La tarjeta ya oculta esos botones; esto cubre
  // llamadas directas al handler.
  if (prep && !canEditPrep(prep)) {
    var EDIT_ATTRS = ['data-choice', 'data-pdf', 'data-xlsx', 'data-ai-falta', 'data-ai-wa', 'data-reassign', 'data-save-reassign', 'data-na', 'data-remove-item', 'data-restore-removed', 'data-share-avance', 'data-mail-avance', 'data-nolisto', 'data-deliver-reopen', 'data-deliver-confirm', 'data-deliver', 'data-ready', 'data-unready', 'data-reopen', 'data-del-prep', 'data-add-extra', 'data-save-extra', 'data-del-extra', 'data-asignar', 'data-save-asignar', 'data-completar', 'data-guardar-avance'];
    var blocked = EDIT_ATTRS.some(function (a) { return t.hasAttribute(a); });
    if (blocked) { showToast('Este equipo es de otro analista: solo puedes compartirlo por WhatsApp o correo.'); return; }
  }
  // Completar datos de un borrador (238b): abre Nuevo equipo prellenado
  // con los datos detectados; Guardar (btnAdd) actualiza ese mismo equipo
  // y quita la marca. Solo borradores: un equipo completo no tiene este
  // botón y aquí se ignora (no hay edición general, como hasta ahora).
  if (t.hasAttribute('data-completar') && prep) {
    if (!canEditPrep(prep)) { showToast('Este equipo es de otro analista: solo puedes compartirlo por WhatsApp o correo.'); return; }
    if (!prep.borrador) return;
    document.getElementById('fTipo').value = prep.equipo.tipo || 'Laptop';
    document.getElementById('fMarca').value = prep.equipo.marca || '';
    document.getElementById('fModelo').value = prep.equipo.modelo || '';
    document.getElementById('fSerie').value = prep.equipo.serie || '';
    document.getElementById('fInv').value = prep.equipo.inventario || '';
    document.getElementById('fHostname').value = prep.equipo.hostname || '';
    document.getElementById('fTec').value = prep.tecnico || '';
    document.getElementById('fUser').value = prep.usuario.nombre || '';
    document.getElementById('fArea').value = prep.usuario.area || '';
    document.getElementById('fCorreo').value = prep.usuario.correo || '';
    window._detectedChecks = null; window._detectedDetalles = null; window._detectedVersiones = null; window._detectedHardware = null;
    window._completarBorradorId = prep.id;
    document.getElementById('btnAdd').textContent = '💾 Guardar datos completos';
    document.getElementById('detBox').hidden = true;
    document.getElementById('newBox').hidden = false;
    updateSaveBtn();
    return;
  }
  if (t.hasAttribute('data-choice') && prep) {
    var cid = t.getAttribute('data-choice');
    var cval = t.getAttribute('data-value');
    prep.checks[cid] = (prep.checks[cid] === cval) ? false : cval;
    clearNoListoIfDone(prep);
    cloudUpsertPrep(prep);
    save(); render(); return;
  }
  if (t.hasAttribute('data-pdf') && prep) { sharePdf(prep); return; }
  if (t.hasAttribute('data-xlsx') && prep) { shareXlsx([prep], 'equipo-' + (cleanName(prep.equipo.marca) || 'equipo') + '-' + (cleanName(prep.equipo.modelo) || '') + '.xlsx'); return; }
  if (t.hasAttribute('data-wa') && prep) { shareWhatsApp([prep]); return; }
  if (t.hasAttribute('data-ai-falta') && prep) {
    if (aiBusy) return;
    if (!aiKey) { showToast(aiErrorText({ message: 'no-key' })); return; }
    aiBusy = true;
    aiAnswers[prep.id] = 'Pensando...';
    render();
    askAI(faltaPrompt(prep)).then(function (txt) { aiAnswers[prep.id] = txt || 'La IA no devolvió respuesta.'; render(); }).catch(function (e) { aiAnswers[prep.id] = aiErrorText(e); render(); }).then(function () { aiBusy = false; });
    return;
  }
  if (t.hasAttribute('data-ai-wa') && prep) {
    if (aiBusy) return;
    if (!aiKey) { showToast(aiErrorText({ message: 'no-key' })); return; }
    aiBusy = true;
    askAI(waSummaryPrompt(prep)).then(function (txt) { if (txt) shareText(txt); }).catch(function (e) { showToast(aiErrorText(e)); }).then(function () { aiBusy = false; });
    return;
  }
  if (t.hasAttribute('data-mail') && prep) { shareMail([prep], 'equipo-' + (cleanName(prep.equipo.marca) || 'equipo') + '-' + (cleanName(prep.equipo.modelo) || '') + '.xlsx'); return; }
  if (t.hasAttribute('data-reassign') && prep) { window._reassignFor = (window._reassignFor === prep.id ? null : prep.id); render(); return; }
  if (t.hasAttribute('data-save-reassign') && prep) {
    var reDe = document.getElementById('reDe').value.trim();
    var reA = document.getElementById('reA').value.trim();
    if (!reA) { showToast('Pon a quién se reasigna el equipo.'); return; }
    doReassign(prep, reDe, reA);
    window._reassignFor = null;
    cloudUpsertPrep(prep);
    save(); setFilter(statusOf(prep)); render(); return;
  }
  // Asignar a otro analista (251): abre el selector; al confirmar
  // transfiere la responsabilidad y registra el traspaso en asignaciones.
  if (t.hasAttribute('data-asignar') && prep) {
    if (!canEditPrep(prep)) { showToast('Solo el analista responsable o el administrador puede asignar este equipo.'); return; }
    window._asignarFor = (window._asignarFor === prep.id ? null : prep.id);
    render(); return;
  }
  if (t.hasAttribute('data-save-asignar') && prep) {
    if (!canEditPrep(prep)) { showToast('Solo el analista responsable o el administrador puede asignar este equipo.'); return; }
    var selAs = document.getElementById('asignarSelect');
    var newUid = selAs ? selAs.value : '';
    var newUser = null;
    teamUsers.forEach(function (u) { if (u.uid === newUid) newUser = u; });
    if (!newUser) { showToast('Elige a quién asignar el equipo.'); return; }
    doAssign(prep, newUid, newUser.nombre || newUser.email || '');
    window._asignarFor = null;
    cloudUpsertPrep(prep);
    save(); render(); return;
  }
  // Solicitar asignación (251): una sola solicitud pendiente por equipo,
  // guardada en el documento del equipo (sin colección nueva).
  if (t.hasAttribute('data-solicitar-asignacion') && prep) {
    if (canEditPrep(prep)) return; // propio: no hace falta pedirlo
    var cur = prep.solicitudAsignacion;
    if (cur && cur.estado === 'pendiente') return; // ya hay una: no se duplica
    prep.solicitudAsignacion = { deUid: cloudUser ? cloudUser.uid : '', deNombre: technicianName(), fecha: Date.now(), estado: 'pendiente' };
    cloudUpsertPrep(prep);
    save(); render(); return;
  }
  if (t.hasAttribute('data-cancel-solicitud') && prep) {
    var curC = prep.solicitudAsignacion;
    if (!curC || curC.estado !== 'pendiente') return;
    if (!cloudUser || curC.deUid !== cloudUser.uid) { showToast('Solo quien pidió la asignación puede cancelarla.'); return; }
    prep.solicitudAsignacion = null;
    cloudUpsertPrep(prep);
    save(); render(); return;
  }
  if (t.hasAttribute('data-aprobar-solicitud') && prep) {
    if (cloudRole !== 'admin') { showToast('Solo el administrador aprueba solicitudes.'); return; }
    var curA = prep.solicitudAsignacion;
    if (!curA || curA.estado !== 'pendiente') return;
    doAssign(prep, curA.deUid, curA.deNombre);
    cloudUpsertPrep(prep);
    save(); render(); return;
  }
  if (t.hasAttribute('data-rechazar-solicitud') && prep) {
    if (cloudRole !== 'admin') { showToast('Solo el administrador rechaza solicitudes.'); return; }
    if (!prep.solicitudAsignacion || prep.solicitudAsignacion.estado !== 'pendiente') return;
    prep.solicitudAsignacion = null;
    cloudUpsertPrep(prep);
    save(); render(); return;
  }
  // N/A por punto: alterna; si el avance llega a 100% se limpia 'No listo'.
  if (t.hasAttribute('data-na') && prep) {
    var naId = t.getAttribute('data-na');
    if (!prep.naItems) prep.naItems = {};
    if (prep.naItems[naId]) delete prep.naItems[naId]; else prep.naItems[naId] = true;
    clearNoListoIfDone(prep);
    cloudUpsertPrep(prep);
    save(); render(); return;
  }
  // Quitar punto: se oculta de la tarjeta (no cuenta en el avance).
  if (t.hasAttribute('data-remove-item') && prep) {
    var remId = t.getAttribute('data-remove-item');
    if (!prep.removedItems) prep.removedItems = [];
    if (prep.removedItems.indexOf(remId) === -1) prep.removedItems.push(remId);
    clearNoListoIfDone(prep);
    cloudUpsertPrep(prep);
    save(); render(); return;
  }
  if (t.hasAttribute('data-restore-removed') && prep) {
    prep.removedItems = [];
    cloudUpsertPrep(prep);
    save(); render(); return;
  }
  // Guardar avance (251): guardado explícito del checklist en revisión.
  // Guarda local (save) + nube (cloudUpsertPrep, si hay sesión) SIN cambiar
  // el estado ni duplicar el equipo, y confirma en el propio botón ('✓
  // Avance guardado', deshabilitado ~2 s, sin alert). No re-renderiza de
  // inmediato para que la confirmación se vea; a los 2 s restaura el botón
  // y re-renderiza. Sin sesión/nube guarda local y confirma igual.
  if (t.hasAttribute('data-guardar-avance') && prep) {
    if (!canEditPrep(prep)) { showToast('Este equipo es de otro analista: solo puedes compartirlo por WhatsApp o correo.'); return; }
    cloudUpsertPrep(prep);
    save();
    t.textContent = '✓ Avance guardado';
    t.disabled = true;
    setTimeout(function () { t.textContent = '💾 Guardar avance'; t.disabled = false; render(); }, 2000);
    return;
  }
  if (t.hasAttribute('data-share-avance') && prep) { shareWhatsApp([prep], avanceText(prep)); return; }
  if (t.hasAttribute('data-mail-avance') && prep) { shareAvanceMail(prep); return; }
  // 'No listo': si estaba listo, vuelve a preparación; marca cuántos
  // puntos faltan. Distinto de 'Quitar listo' (deshacer silencioso).
  if (t.hasAttribute('data-nolisto') && prep) {
    if (prep.readyAt) prep.readyAt = null;
    prep.noListo = { fecha: Date.now(), faltan: pendingRequired(prep).length };
    cloudUpsertPrep(prep);
    save(); setFilter('preparacion'); render(); return;
  }
  // Entrega con avance <100%: 'Reabrir para completar' no entrega y
  // vuelve a preparación; 'Entregar así' entrega como está.
  if (t.hasAttribute('data-deliver-reopen') && prep) {
    prep.readyAt = null;
    window._deliverConfirmFor = null;
    cloudUpsertPrep(prep);
    save(); setFilter('preparacion'); render(); return;
  }
  if (t.hasAttribute('data-deliver-confirm') && prep) {
    prep.deliveredAt = Date.now();
    window._deliverConfirmFor = null;
    cloudUpsertPrep(prep);
    save(); setFilter('entregado'); render(); return;
  }
  if (t.hasAttribute('data-deliver') && prep) {
    if (progress(prep) < 100) { window._deliverConfirmFor = prep.id; render(); return; }
    prep.deliveredAt = Date.now(); cloudUpsertPrep(prep); save(); setFilter('entregado'); render(); return;
  }
  if (t.hasAttribute('data-ready') && prep) { prep.readyAt = Date.now(); delete prep.noListo; window._deliverConfirmFor = null; cloudUpsertPrep(prep); save(); setFilter('listo'); render(); return; }
  if (t.hasAttribute('data-unready') && prep) { prep.readyAt = null; window._deliverConfirmFor = null; cloudUpsertPrep(prep); save(); setFilter('preparacion'); render(); return; }
  // 'Reabrir' de un entregado: limpia deliveredAt Y readyAt, vuelve a
  // preparación para completar al 100% (antes quedaba en listo).
  if (t.hasAttribute('data-reopen') && prep) { prep.deliveredAt = null; prep.readyAt = null; cloudUpsertPrep(prep); save(); setFilter('preparacion'); render(); return; }
  if (t.hasAttribute('data-del-prep') && prep) {
    // Confirmación inline (251): el modal es asíncrono; solo con Sí se
    // elimina el equipo y su checklist.
    showConfirm('¿Eliminar este equipo y su checklist?').then(function (ok) {
      if (!ok) return;
      state.preparations = state.preparations.filter(function (p) { return p.id !== prep.id; });
      cloudDeletePrep(prep.id);
      save(); render();
    });
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
  if (!canEditPrep(prep)) { showToast('Este equipo es de otro analista: solo puedes compartirlo por WhatsApp o correo.'); return; }
  prep.checks[t.getAttribute('data-check')] = t.checked;
  clearNoListoIfDone(prep);
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
  // Confirmación inline (251): solo con Sí se restaura la plantilla.
  showConfirm('¿Restaurar la plantilla predeterminada?').then(function (ok) {
    if (!ok) return;
    state.template = defaultTemplate();
    save(); render();
  });
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
  window.Cloud.listUsers().then(function (us) { teamUsers = us || []; refreshAdminUserFilter(); renderEquipo(); }).catch(function () {});
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
  if (!window.Cloud || !CLOUD_ENABLED) { showToast('El chat necesita conexión a la nube.'); return; }
  var inp = document.getElementById('chatInput');
  var t = inp.value.trim();
  if (!t) return;
  inp.value = '';
  window.Cloud.sendChat(t, technicianName()).catch(function () { showToast('No se pudo enviar el mensaje. Revisa tu conexión.'); });
}
document.getElementById('btnChatSend').addEventListener('click', sendChatMsg);
document.getElementById('chatInput').addEventListener('keydown', function (e) { if (e.key === 'Enter') sendChatMsg(); });
function sendDmMsg() {
  if (!window.Cloud || !CLOUD_ENABLED || !dmPeer) return;
  var inp = document.getElementById('dmInput');
  var t = inp.value.trim();
  if (!t) return;
  inp.value = '';
  window.Cloud.sendDm(dmPeer, t, technicianName()).catch(function () { showToast('No se pudo enviar el mensaje. Revisa tu conexión.'); });
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
  // Confirmación inline (251): solo con Sí se borra el mensaje.
  showConfirm('¿Borrar este mensaje para todos?').then(function (ok) {
    if (!ok) return;
    window.Cloud.deleteChatMessage(b.getAttribute('data-del-chat')).catch(function () { showToast('No se pudo borrar el mensaje.'); });
  });
});
document.getElementById('dmChatBox').addEventListener('click', function (e) {
  var b = e.target.closest('[data-del-dm]');
  if (!b) return;
  // Confirmación inline (251): solo con Sí se borra el mensaje.
  showConfirm('¿Borrar este mensaje para los dos?').then(function (ok) {
    if (!ok) return;
    window.Cloud.deleteDmMessage(b.getAttribute('data-del-dm')).catch(function () { showToast('No se pudo borrar el mensaje.'); });
  });
});

// ---------- Mantenimientos Preventivos (251) ----------
// Órdenes de servicio con folio: el técnico crea el mantenimiento (desde
// un equipo detectado o en blanco), lo guarda como borrador sin folio o
// crea la orden (asigna folio con transacción), y el usuario la firma
// desde el link que le llega por WhatsApp. Un usuario normal solo ve sus
// propios mantenimientos; el admin ve todos con su selector de usuario.
var MANT_COMPONENTES = [['impresora', 'Impresora'], ['cpu', 'CPU'], ['monitor', 'Monitor'], ['teclado', 'Teclado'], ['mouse', 'Mouse'], ['noBreak', 'No Break']];
var MANT_LS_KEY = 'checklist-soporte-mant-v1';
var MANT_MIG_KEY = 'checklist-soporte-migrado-mant-v1';
var mantenimientos = [];
var cloudMantUnsub = null;
var cloudUserUnsub = null;  // (254) suscripción en vivo al documento del usuario (bloqueo de Mantenimientos)
var mantAdminViewUid = 'todos';
var mantFormId = null;      // id del mantenimiento que se está editando (null = nuevo)
var mantFormBase = null;    // objeto que se está editando (borrador o nuevo pre-llenado)
var mantFormFromDet = null; // id del detectado que llenó el formulario
var mantFirmaData = '';     // data URL de la firma del técnico dibujada
var mantPolFuente = '';       // de dónde salieron las políticas (gpedit / secedit / net accounts)
var mantOrderId = null;     // id de la orden que muestra la vista de orden
var prefillMantUserName = '';
var FIRMA_URL_BASE = 'https://checklist-soporte.web.app/firma.html';
// Defaults del formulario de mantenimientos (251): solo se prellenan
// cuando el campo está vacío al abrir el formulario; un valor guardado
// por el técnico nunca se sobrescribe.
var MANT_TITULO_DEF = 'Mantenimiento Preventivo sistemas';
var MANT_DESC_CAMBIOS_DEF = 'se realiza mantenimiento preventivo en hardware y software, sopleteo y limpieza general, instalación de actualización, revisión de políticas y antivirus, desinstalación de software no permitido';
function mantAnioActual() { return new Date().getFullYear(); }
function mantTituloBase(t) { return String(t || '').replace(/\s+(19|20)\d\d\s*$/, '').trim(); }
function mantAnioOf(m) {
  if (m && m.anio) return Number(m.anio);
  var mm = /((?:19|20)\d\d)\s*$/.exec(String((m && m.tituloCaso) || ''));
  return mm ? Number(mm[1]) : mantAnioActual();
}
function mantTituloCompuesto(m) {
  var base = mantTituloBase(m ? m.tituloCaso : '');
  if (!base) base = MANT_TITULO_DEF;
  return base + ' ' + mantAnioOf(m);
}
function mantEmpresaOf(m) { return (m && m.empresa) || 'Lapi'; }
function mantFillAnioOptions() {
  var sel = document.getElementById('fM-anio');
  if (!sel) return;
  var y = mantAnioActual(), cur = String(sel.value || y);
  var years = [y - 1, y, y + 1, y + 2];
  var target = cur;
  // El año de una orden vieja se conserva como opción extra aunque quede
  // fuera del rango (actual -1 a +2), para no cambiarle el año al editar.
  if (/^\d{4}$/.test(cur) && years.indexOf(Number(cur)) === -1) years.push(Number(cur));
  else if (years.indexOf(Number(cur)) === -1) target = String(y);
  years.sort(function (a, b) { return a - b; });
  var opts = '';
  years.forEach(function (yy) { opts += '<option value="' + yy + '"' + (String(yy) === target ? ' selected' : '') + '>' + yy + '</option>'; });
  sel.innerHTML = opts;
  sel.value = target;
}
// Prellenado al abrir el formulario (251): '/' en tiempos, tipo de
// falla y fechas de planeación/compromiso/periodo; título y descripción
// de cambios por default; descripción del equipo = hostname; ambos tipos
// marcados si ninguno lo está; empresa Lapi si está vacía.
function mantApplyDefaults() {
  mantFillAnioOptions();
  function slash(id) { var el = document.getElementById(id); if (el && !String(el.value || '').trim()) el.value = '/'; }
  ['fM-tRep', 'fM-tViaje', 'fM-tCaido', 'fM-tipoFalla', 'fM-fechaPlan', 'fM-fechaComp', 'fM-periodoPrueba'].forEach(slash);
  var tit = document.getElementById('fM-titulo');
  if (tit && !tit.value.trim()) tit.value = MANT_TITULO_DEF;
  var dc = document.getElementById('fM-descCambios');
  if (dc && !dc.value.trim()) dc.value = MANT_DESC_CAMBIOS_DEF;
  var de = document.getElementById('fM-descEquipo');
  var hn = document.getElementById('fM-hostname');
  if (de && hn && !de.value.trim() && hn.value.trim()) de.value = hn.value.trim();
  var em = document.getElementById('fM-empresa');
  if (em && !em.value) em.value = 'Lapi';
  if (!mantCheck('fM-tipo-sw') && !mantCheck('fM-tipo-hw')) { mantSetCheck('fM-tipo-sw', true); mantSetCheck('fM-tipo-hw', true); }
}

function mantEmptyChecks() { return { impresora: false, cpu: false, monitor: false, teclado: false, mouse: false, noBreak: false }; }
function newMantBlank() {
  return {
    id: uid(), createdAt: Date.now(), folio: null, estado: 'borrador',
    tecnicoUid: cloudUser ? cloudUser.uid : '', tecnico: technicianName(),
    empresa: 'Lapi', anio: mantAnioActual(),
    tipo: 'SOFTWARE/HARDWARE', area: '', responsable: '',
    tiempoReparacion: '', tiempoViaje: '', tiempoSistemaCaido: '',
    fechaServicio: '', fechaTermino: '', tituloCaso: '', tipoFalla: '',
    identificacion: mantEmptyChecks(), descripcionEquipo: '',
    condiciones: Object.assign(mantEmptyChecks(), { notas: '' }),
    preventivo: mantEmptyChecks(),
    descripcionCambios: '', conclusion: '', comentarios: '',
    fechaPlaneacion: '', fechaCompromiso: '', periodoPrueba: '', fechaLiberacion: '',
    observaciones: '', observacionesDetectadas: '',
    equipo: { tipo: 'Laptop', marca: '', modelo: '', serie: '', hostname: '', cpu: '', ramGB: '', discoGB: '', discoTipo: '', ip: '', redes: [], impresora: '', anydeskId: '', anydeskAlias: '', antivirus: '', politicas: { cambioDias: '', minLongitud: '', bloqueoIntentos: '', bloqueoSegundos: '', bloqueoManual: false, cumpleCambio: null, cumpleLongitud: null, cumpleIntentos: null, cumpleBloqueo: null, cumple: null }, politicasFuente: '', usuarioSistemas: false, so: '', versiones: { so: '', antivirus: '', esetAgent: '', chrome: '' } },
    whatsappUsuario: '', firmaTecnico: '', firma: null
  };
}
// Saneo como prepToCloudDoc/prepFromCloud: la firma (data URL) no viaja
// si pasa de ~700 KB (límite de 1 MB por documento), igual que fotoSerie.
function mantToCloudDoc(m) {
  var eq = m.equipo || {};
  var pol = eq.politicas || {};
  var firmaTec = m.firmaTecnico || '';
  if (firmaTec && firmaTec.length > MAX_FOTO_CLOUD) firmaTec = '';
  var firmaUsr = m.firma || null;
  if (firmaUsr && firmaUsr.firma && firmaUsr.firma.length > MAX_FOTO_CLOUD) firmaUsr = Object.assign({}, firmaUsr, { firma: '' });
  function ck(o) { return { impresora: !!(o && o.impresora), cpu: !!(o && o.cpu), monitor: !!(o && o.monitor), teclado: !!(o && o.teclado), mouse: !!(o && o.mouse), noBreak: !!(o && o.noBreak) }; }
  var cond = ck(m.condiciones);
  cond.notas = (m.condiciones && m.condiciones.notas) || '';
  return {
    id: m.id, createdAt: m.createdAt || Date.now(), folio: (m.folio == null ? null : m.folio), estado: m.estado || 'borrador',
    tecnicoUid: m.tecnicoUid || '', tecnico: m.tecnico || '',
    empresa: m.empresa || 'Lapi', anio: (m.anio == null ? mantAnioActual() : m.anio),
    tipo: m.tipo || '', area: m.area || '', responsable: m.responsable || '',
    tiempoReparacion: m.tiempoReparacion || '', tiempoViaje: m.tiempoViaje || '', tiempoSistemaCaido: m.tiempoSistemaCaido || '',
    fechaServicio: m.fechaServicio || '', fechaTermino: m.fechaTermino || '',
    tituloCaso: m.tituloCaso || '', tipoFalla: m.tipoFalla || '',
    identificacion: ck(m.identificacion), descripcionEquipo: m.descripcionEquipo || '',
    condiciones: cond, preventivo: ck(m.preventivo),
    descripcionCambios: m.descripcionCambios || '', conclusion: m.conclusion || '', comentarios: m.comentarios || '',
    fechaPlaneacion: m.fechaPlaneacion || '', fechaCompromiso: m.fechaCompromiso || '', periodoPrueba: m.periodoPrueba || '', fechaLiberacion: m.fechaLiberacion || '',
    observaciones: m.observaciones || '', observacionesDetectadas: m.observacionesDetectadas || '',
    equipo: { tipo: eq.tipo || '', marca: eq.marca || '', modelo: eq.modelo || '', serie: eq.serie || '', hostname: eq.hostname || '', cpu: eq.cpu || '', ramGB: (eq.ramGB == null ? '' : eq.ramGB), discoGB: (eq.discoGB == null ? '' : eq.discoGB), discoTipo: eq.discoTipo || '', ip: eq.ip || '', redes: Array.isArray(eq.redes) ? eq.redes.map(function (r) { return { nombre: r.nombre || '', ip: r.ip || '', ipTipo: r.ipTipo || '' }; }) : [], impresora: eq.impresora || '', anydeskId: eq.anydeskId || '', anydeskAlias: eq.anydeskAlias || '', antivirus: eq.antivirus || '', politicas: { cambioDias: (pol.cambioDias == null ? '' : pol.cambioDias), minLongitud: (pol.minLongitud == null ? '' : pol.minLongitud), bloqueoIntentos: (pol.bloqueoIntentos == null ? '' : pol.bloqueoIntentos), bloqueoSegundos: (pol.bloqueoSegundos == null ? '' : pol.bloqueoSegundos), bloqueoManual: !!pol.bloqueoManual, cumpleCambio: (pol.cumpleCambio == null ? null : !!pol.cumpleCambio), cumpleLongitud: (pol.cumpleLongitud == null ? null : !!pol.cumpleLongitud), cumpleIntentos: (pol.cumpleIntentos == null ? null : !!pol.cumpleIntentos), cumpleBloqueo: (pol.cumpleBloqueo == null ? null : !!pol.cumpleBloqueo), cumple: (pol.cumple == null ? null : !!pol.cumple) }, politicasFuente: eq.politicasFuente || '', usuarioSistemas: !!eq.usuarioSistemas, so: eq.so || '', versiones: { so: ((eq.versiones && eq.versiones.so) || ''), antivirus: ((eq.versiones && eq.versiones.antivirus) || ''), esetAgent: ((eq.versiones && eq.versiones.esetAgent) || ''), chrome: ((eq.versiones && eq.versiones.chrome) || '') } },
    whatsappUsuario: m.whatsappUsuario || '',
    firmaTecnico: firmaTec,
    firma: firmaUsr,
    updatedAt: Date.now()
  };
}
function mantFromCloud(doc) {
  var m = newMantBlank();
  var d = doc || {};
  var eq = d.equipo || {};
  var pol = eq.politicas || {};
  var ver = eq.versiones || {};
  m.id = d.id || m.id;
  m.createdAt = d.createdAt || 0;
  m.folio = (d.folio == null ? null : d.folio);
  m.estado = d.estado || 'borrador';
  m.tecnicoUid = d.tecnicoUid || '';
  m.tecnico = d.tecnico || '';
  m.empresa = d.empresa || 'Lapi';
  m.anio = d.anio || null;
  if (!m.anio) { var mmAnio = /((?:19|20)\d\d)\s*$/.exec(String(d.tituloCaso || '')); m.anio = mmAnio ? Number(mmAnio[1]) : mantAnioActual(); }
  m.tipo = d.tipo || 'SOFTWARE/HARDWARE';
  m.area = d.area || '';
  m.responsable = d.responsable || '';
  m.tiempoReparacion = d.tiempoReparacion || '';
  m.tiempoViaje = d.tiempoViaje || '';
  m.tiempoSistemaCaido = d.tiempoSistemaCaido || '';
  m.fechaServicio = d.fechaServicio || '';
  m.fechaTermino = d.fechaTermino || '';
  m.tituloCaso = d.tituloCaso || '';
  m.tipoFalla = d.tipoFalla || '';
  ['identificacion', 'preventivo'].forEach(function (k) { var o = d[k] || {}; MANT_COMPONENTES.forEach(function (c) { m[k][c[0]] = !!o[c[0]]; }); });
  var cond = d.condiciones || {};
  MANT_COMPONENTES.forEach(function (c) { m.condiciones[c[0]] = !!cond[c[0]]; });
  m.condiciones.notas = cond.notas || '';
  m.descripcionEquipo = d.descripcionEquipo || '';
  m.descripcionCambios = d.descripcionCambios || '';
  m.conclusion = d.conclusion || '';
  m.comentarios = d.comentarios || '';
  m.fechaPlaneacion = d.fechaPlaneacion || '';
  m.fechaCompromiso = d.fechaCompromiso || '';
  m.periodoPrueba = d.periodoPrueba || '';
  m.fechaLiberacion = d.fechaLiberacion || '';
  m.observaciones = d.observaciones || '';
  m.observacionesDetectadas = d.observacionesDetectadas || '';
  m.equipo.tipo = eq.tipo || 'Laptop';
  m.equipo.marca = eq.marca || '';
  m.equipo.modelo = eq.modelo || '';
  m.equipo.serie = eq.serie || '';
  m.equipo.hostname = eq.hostname || '';
  m.equipo.cpu = eq.cpu || '';
  m.equipo.ramGB = (eq.ramGB == null ? '' : eq.ramGB);
  m.equipo.discoGB = (eq.discoGB == null ? '' : eq.discoGB);
  m.equipo.discoTipo = eq.discoTipo || '';
  m.equipo.ip = eq.ip || '';
  m.equipo.redes = Array.isArray(eq.redes) ? eq.redes.map(function (r) { return { nombre: r.nombre || '', ip: r.ip || '', ipTipo: r.ipTipo || '' }; }) : [];
  m.equipo.impresora = eq.impresora || '';
  m.equipo.anydeskId = eq.anydeskId || '';
  m.equipo.anydeskAlias = eq.anydeskAlias || '';
  m.equipo.antivirus = eq.antivirus || '';
  m.equipo.politicas.cambioDias = (pol.cambioDias == null ? '' : pol.cambioDias);
  m.equipo.politicas.minLongitud = (pol.minLongitud == null ? '' : pol.minLongitud);
  m.equipo.politicas.bloqueoIntentos = (pol.bloqueoIntentos == null ? '' : pol.bloqueoIntentos);
  m.equipo.politicas.bloqueoSegundos = (pol.bloqueoSegundos == null ? '' : pol.bloqueoSegundos);
  m.equipo.politicas.cumpleCambio = (pol.cumpleCambio == null ? null : !!pol.cumpleCambio);
  m.equipo.politicas.cumpleLongitud = (pol.cumpleLongitud == null ? null : !!pol.cumpleLongitud);
  m.equipo.politicas.cumpleIntentos = (pol.cumpleIntentos == null ? null : !!pol.cumpleIntentos);
  m.equipo.politicas.cumpleBloqueo = (pol.cumpleBloqueo == null ? null : !!pol.cumpleBloqueo);
  m.equipo.politicas.cumple = (pol.cumple == null ? null : !!pol.cumple);
  m.equipo.politicas.bloqueoManual = !!pol.bloqueoManual;
  m.equipo.politicasFuente = eq.politicasFuente || '';
  m.equipo.usuarioSistemas = !!eq.usuarioSistemas;
  m.equipo.so = eq.so || ver.so || '';
  m.equipo.versiones = { so: ver.so || '', antivirus: ver.antivirus || '', esetAgent: ver.esetAgent || '', chrome: ver.chrome || '' };
  m.whatsappUsuario = d.whatsappUsuario || '';
  m.firmaTecnico = d.firmaTecnico || '';
  m.firma = d.firma || null;
  return m;
}
// Políticas de contraseña (251): lo esperado es cambio cada 90 días,
// longitud mínima 10, bloqueo a los 5 intentos y bloqueo de 350 s.
// Cumple si el valor detectado está dentro de lo esperado (cambio cada 90
// días o menos, longitud 10 o más, bloqueo con 5 intentos o menos,
// bloqueo de 350 s o más). Sin dato no se puede decir: null.
function mantPoliticasCumple(pol) {
  pol = pol || {};
  function num(v) { if (v == null || v === '') return null; var n = Number(v); return isNaN(n) ? null : n; }
  var cambio = num(pol.cambioDias), lon = num(pol.minLongitud), inten = num(pol.bloqueoIntentos), bloq = num(pol.bloqueoSegundos);
  // (255) Bloqueo manual (LockoutDuration 0 en la directiva): el equipo
  // queda bloqueado hasta que un administrador lo desbloquee, así que
  // cumple el bloqueo sin importar los segundos.
  var manual = !!pol.bloqueoManual;
  var cC = cambio == null ? null : cambio <= 90;
  var cL = lon == null ? null : lon >= 10;
  var cI = inten == null ? null : inten <= 5;
  var cB = manual ? true : (bloq == null ? null : bloq >= 350);
  var vals = [cC, cL, cI, cB].filter(function (v) { return v !== null; });
  return { cambioDias: cambio, minLongitud: lon, bloqueoIntentos: inten, bloqueoSegundos: bloq, bloqueoManual: manual, cumpleCambio: cC, cumpleLongitud: cL, cumpleIntentos: cI, cumpleBloqueo: cB, cumple: vals.length ? vals.every(function (v) { return v === true; }) : null };
}
function politicasText(pol) {
  var c = mantPoliticasCumple(pol);
  var parts = [];
  parts.push('cambio cada ' + (c.cambioDias == null ? '—' : c.cambioDias + ' días') + (c.cumpleCambio == null ? '' : (c.cumpleCambio ? ' ✓' : ' ✗')));
  parts.push('longitud mínima ' + (c.minLongitud == null ? '—' : c.minLongitud) + (c.cumpleLongitud == null ? '' : (c.cumpleLongitud ? ' ✓' : ' ✗')));
  parts.push('bloqueo a los ' + (c.bloqueoIntentos == null ? '—' : c.bloqueoIntentos + ' intentos') + (c.cumpleIntentos == null ? '' : (c.cumpleIntentos ? ' ✓' : ' ✗')));
  parts.push(c.bloqueoManual ? 'bloqueo hasta desbloqueo manual ✓' : ('bloqueo ' + (c.bloqueoSegundos == null ? '—' : c.bloqueoSegundos + ' s') + (c.cumpleBloqueo == null ? '' : (c.cumpleBloqueo ? ' ✓' : ' ✗'))));
  return 'Políticas: ' + parts.join(' · ') + (c.cumple == null ? '' : (c.cumple ? ' — Cumple' : ' — No cumple'));
}
// Observaciones detectadas (251): los datos detectados se compilan en
// un texto (software y versiones, IPs/redes, impresora, AnyDesk,
// antivirus, políticas con su cumplimiento, usuario de sistemas,
// hostname, serie, modelo), no como campos sueltos.
function compileObservacionesDetectadas(d) {
  d = d || {};
  var det = d.detalles || {};
  var ver = d.versiones || {};
  var lines = [];
  var hw = hardwareLine(d);
  if (hw) lines.push(hw);
  var rd = redesLine(d);
  if (rd) lines.push(rd);
  var vl = versionesLine(ver);
  if (vl) lines.push(vl);
  if (d.so && !ver.so) lines.push('SO: ' + d.so);
  var ad = anydeskLine(d);
  if (ad) lines.push(ad);
  var imp = d.impresora || det.impresora || '';
  if (imp) lines.push('Impresora: ' + imp);
  var av = ver.antivirus || d.antivirus || det.antivirus || '';
  if (av) lines.push('Antivirus: ' + av);
  var pol = d.politicas || det.politicas || null;
  if (pol) lines.push(politicasText(pol));
  var us = (typeof d.usuarioSistemas !== 'undefined') ? d.usuarioSistemas : det.usuarioSistemas;
  if (typeof us === 'boolean') lines.push('Usuario de sistemas: ' + (us ? 'Sí' : 'No'));
  if (d.hostname) lines.push('Hostname: ' + d.hostname);
  if (d.serie) lines.push('Serie: ' + d.serie);
  if (d.modelo) lines.push('Modelo: ' + ((d.marca ? d.marca + ' ' : '') + d.modelo));
  return lines.join('\n');
}
function mantFromDetectado(d) {
  var m = newMantBlank();
  var ver = d.versiones || {};
  var det = d.detalles || {};
  var pol = d.politicas || det.politicas || null;
  m.equipo.tipo = d.tipo || 'Desktop';
  m.equipo.marca = d.marca || '';
  m.equipo.modelo = d.modelo || '';
  m.equipo.serie = d.serie || '';
  m.equipo.hostname = d.hostname || '';
  m.equipo.cpu = d.cpu || '';
  m.equipo.ramGB = (d.ramGB == null ? '' : d.ramGB);
  m.equipo.discoGB = (d.discoGB == null ? '' : d.discoGB);
  m.equipo.discoTipo = d.discoTipo || '';
  m.equipo.ip = d.ip || '';
  m.equipo.redes = Array.isArray(d.redes) ? d.redes.map(function (r) { return { nombre: r.nombre || '', ip: r.ip || '', ipTipo: r.ipTipo || '' }; }) : [];
  m.equipo.impresora = d.impresora || det.impresora || '';
  m.equipo.anydeskId = d.anydeskId || '';
  m.equipo.anydeskAlias = d.anydeskAlias || '';
  m.equipo.antivirus = ver.antivirus || d.antivirus || det.antivirus || '';
  m.equipo.so = d.so || ver.so || '';
  m.equipo.versiones = { so: ver.so || '', antivirus: ver.antivirus || '', esetAgent: ver.esetAgent || '', chrome: ver.chrome || '' };
  if (pol) m.equipo.politicas = mantPoliticasCumple(pol);
  m.equipo.politicasFuente = det.politicasFuente || '';
  if (typeof d.usuarioSistemas !== 'undefined') m.equipo.usuarioSistemas = !!d.usuarioSistemas;
  else if (typeof det.usuarioSistemas !== 'undefined') m.equipo.usuarioSistemas = !!det.usuarioSistemas;
  m.observacionesDetectadas = compileObservacionesDetectadas(d);
  return m;
}
// Redes del formulario: "Wi-Fi: 192.168.1.45 (Dinámica), Ethernet:
// 10.0.0.20 (Estática)" o separadas con '·' (como las escribe
// redesText). Un segmento sin IP se guarda con su nombre y sin IP.
function parseRedesText(s) {
  var out = [];
  String(s || '').split(/[,·]/).forEach(function (seg) {
    seg = seg.trim();
    if (!seg) return;
    var m = /^(.*?):\s*([0-9]{1,3}(?:\.[0-9]{1,3}){3})\s*(?:\(([^)]*)\))?$/.exec(seg);
    if (m) { out.push({ nombre: (m[1] || '').trim(), ip: m[2], ipTipo: (m[3] || '').trim() }); return; }
    var ipOnly = /^([0-9]{1,3}(?:\.[0-9]{1,3}){3})$/.exec(seg);
    if (ipOnly) { out.push({ nombre: '', ip: ipOnly[1], ipTipo: '' }); return; }
    out.push({ nombre: seg, ip: '', ipTipo: '' });
  });
  return out;
}
// Visibilidad (251, más estricta que Por preparar): un usuario normal
// ve ÚNICAMENTE sus propios mantenimientos (tecnicoUid propio, con
// respaldo por nombre para registros viejos, igual que en Por preparar);
// los de otros analistas NO se ven en absoluto, sin toggle de 'ver otros'.
// El admin ve todos, con su selector de usuario.
function isOwnMant(m) {
  if (!cloudUser) return true;
  if (m.tecnicoUid) return m.tecnicoUid === cloudUser.uid;
  if (m.tecnico && (m.tecnico === technicianName() || m.tecnico === cloudUser.nombre)) return true;
  return false;
}
function isMantOfAnalyst(m, uid) {
  if (m.tecnicoUid) return m.tecnicoUid === uid;
  var u = null;
  teamUsers.forEach(function (x) { if (x.uid === uid) u = x; });
  if (u && m.tecnico) return m.tecnico === (u.nombre || u.email);
  return false;
}
function mantVisibleList() {
  var list = mantenimientos.slice().sort(function (a, b) { return (b.createdAt || 0) - (a.createdAt || 0); });
  if (cloudRole === 'admin') {
    if (mantAdminViewUid && mantAdminViewUid !== 'todos') list = list.filter(function (m) { return isMantOfAnalyst(m, mantAdminViewUid); });
    return list;
  }
  return list.filter(isOwnMant);
}
function mantEstadoLabel(m) {
  return { borrador: 'Borrador', creada: 'Creada', firmada: 'Firmada', cancelada: 'Cancelada' }[m.estado] || m.estado || '—';
}
function mantCardHtml(m) {
  var eq = m.equipo || {};
  var pol = mantPoliticasCumple(eq.politicas || {});
  var polTxt = pol.cumple == null ? '' : (pol.cumple ? 'Políticas: ✓ Cumple' : 'Políticas: ✗ No cumple');
  var firmaTxt = m.firma ? ('Firmada por ' + (m.firma.nombre || '—') + (m.firma.satisfaccion != null && m.firma.satisfaccion !== '' ? ' · Satisfacción: ' + m.firma.satisfaccion + '/10' : '')) : (m.firmaTecnico ? 'Firma del técnico: sí · Firma del usuario: pendiente' : 'Sin firmas');
  var idLine = 'Serie: ' + (eq.serie || '—') + ' · Hostname: ' + (eq.hostname || '—') + ' · Modelo: ' + (eq.modelo || '—');
  return '<div class="card"><h2>' + esc(m.tituloCaso ? mantTituloCompuesto(m) : 'Mantenimiento sin título') + '</h2>' +
    '<div class="mant-id-line">' + esc(idLine) + '</div>' +
    '<div class="sub">' + esc((m.empresa || 'Lapi') + ' · ' + (m.tipo || '') + ' · ' + (mantAreaOf(m) || '—') + ' · Responsable: ' + (mantRespOf(m) || '—')) + '</div>' +
    '<div class="sub">Técnico: ' + esc(m.tecnico || '—') + ' · Fecha del servicio: ' + esc(m.fechaServicio || '—') + '</div>' +
    (polTxt ? '<div class="sub">' + esc(polTxt) + '</div>' : '') +
    '<div class="sub">' + esc(firmaTxt) + '</div>' +
    '<span class="badge ' + (m.estado === 'firmada' ? 'b-listo' : (m.estado === 'cancelada' ? 'b-prep' : 'b-entr')) + '">' + esc(mantEstadoLabel(m)) + (m.folio ? ' · Folio ' + esc(m.folio) : ' · Sin folio') + '</span>' +
    '<div class="actions">' +
    (m.estado === 'borrador' ? '<button class="btn-green" data-mant-edit="' + esc(m.id) + '">Editar</button>' : '<button class="btn-dark" data-mant-order="' + esc(m.id) + '">Ver orden</button>') +
    ((m.estado === 'creada' || m.estado === 'firmada') ? '<button class="btn-ghost" data-mant-cancel-order="' + esc(m.id) + '">Cancelar orden</button>' : '') +
    (m.estado === 'borrador' ? '<button class="btn-danger" data-mant-del="' + esc(m.id) + '">Eliminar</button>' : '') +
    ((cloudRole === 'admin' && m.estado !== 'borrador') ? '<button class="btn-danger" data-mant-del-order="' + esc(m.id) + '">Eliminar</button>' : '') +
    '</div></div>';
}
function renderMant() {
  var box = document.getElementById('mantList');
  if (!box) return;
  var isAdmin = cloudRole === 'admin';
  var row = document.getElementById('mantAdminRow');
  if (row) row.hidden = !isAdmin;
  if (isAdmin) refreshMantAdminFilter();
  var list = mantVisibleList();
  if (!list.length) { box.innerHTML = '<div class="empty">No hay mantenimientos.</div>'; return; }
  box.innerHTML = list.map(mantCardHtml).join('');
}
function refreshMantAdminFilter() {
  var sel = document.getElementById('mantAdminFilter');
  if (!sel) return;
  var cur = mantAdminViewUid || 'todos';
  sel.innerHTML = '<option value="todos">Todos los usuarios</option>' + teamUsers.map(function (u) {
    return '<option value="' + esc(u.uid) + '"' + (u.uid === cur ? ' selected' : '') + '>' + esc(u.nombre || u.email || 'Usuario') + '</option>';
  }).join('');
  sel.value = cur;
}
function renderMantDetectados() {
  var box = document.getElementById('mantDetList');
  if (!box) return;
  var list = detectados.filter(function (d) { return !d.usado; });
  if (!list.length) { box.innerHTML = '<div class="empty">No hay equipos detectados pendientes.</div>'; return; }
  box.innerHTML = list.map(function (d) {
    var hwLine = hardwareLine(d);
    if (d.so) hwLine = hwLine ? hwLine + ' • SO: ' + d.so : 'SO: ' + d.so;
    return '<div class="card"><h2>' + esc(d.hostname || 'Equipo') + '</h2>' +
      '<div class="sub">' + esc((d.marca || '') + ' ' + (d.modelo || '')) + ' · Serie: ' + esc(d.serie || '—') + '</div>' +
      (hwLine ? '<div class="sub">' + esc(hwLine) + '</div>' : '') +
      '<div class="sub">Detectado ' + timeAgo(d.detectadoEn) + (d.detectadoPor ? ' por ' + esc(d.detectadoPor) : '') + '</div>' +
            '<div class="actions"><button class="btn-green" data-mant-det-use="' + esc(d.id) + '">🔧 Dar mantenimiento a este equipo</button></div></div>';
  }).join('');
}
function renderMantCheckboxes() {
  function groupHtml(prefix) {
    return MANT_COMPONENTES.map(function (c) {
      return '<label><input type="checkbox" id="' + prefix + '-' + c[0] + '"> ' + c[1] + '</label>';
    }).join('');
  }
  var a = document.getElementById('accs-mant-id'); if (a) a.innerHTML = groupHtml('fM-id');
  var b = document.getElementById('accs-mant-cond'); if (b) b.innerHTML = groupHtml('fM-cond');
  var c = document.getElementById('accs-mant-prev'); if (c) c.innerHTML = groupHtml('fM-prev');
}
// Nombre de quien presta el servicio (251): mismo patrón prefillTecnico
// de la 2.0.18 — se llena solo con el login; si el técnico lo escribe a
// mano, se respeta.
function prefillMantTecnico() {
  var f = document.getElementById('fM-tecnico');
  var name = technicianName();
  if (f && name && (!f.value || f.value === prefillMantUserName)) { f.value = name; prefillMantUserName = name; }
}
function mantVal(id) { var el = document.getElementById(id); return el ? String(el.value == null ? '' : el.value) : ''; }
function mantCheck(id) { var el = document.getElementById(id); return !!(el && el.checked); }
function mantSetVal(id, v) { var el = document.getElementById(id); if (el) el.value = (v == null ? '' : v); }
function mantSetCheck(id, v) { var el = document.getElementById(id); if (el) el.checked = !!v; }
function mantNum(id) { var s = mantVal(id).trim(); if (s === '') return ''; var n = Number(s); return isNaN(n) ? s : n; }
function mantScrollTo(id) { var el = document.getElementById(id); if (el && el.scrollIntoView) el.scrollIntoView(); }
function mantReadForm() {
  var m = mantFormBase ? mantFromCloud(mantToCloudDoc(mantFormBase)) : newMantBlank();
  m.tecnico = mantVal('fM-tecnico').trim() || technicianName();
  m.tecnicoUid = tecnicoUidFor(m.tecnico);
  m.empresa = mantVal('fM-empresa') || 'Lapi';
  var anioSel = Number(mantVal('fM-anio')) || mantAnioActual();
  m.anio = anioSel;
  var swTipo = mantCheck('fM-tipo-sw'), hwTipo = mantCheck('fM-tipo-hw');
  m.tipo = (swTipo && hwTipo) ? 'SOFTWARE/HARDWARE' : (swTipo ? 'SOFTWARE' : (hwTipo ? 'HARDWARE' : ''));
  m.area = mantVal('fM-area').trim();
  m.responsable = mantVal('fM-responsable').trim();
  m.tiempoReparacion = mantVal('fM-tRep').trim();
  m.tiempoViaje = mantVal('fM-tViaje').trim();
  m.tiempoSistemaCaido = mantVal('fM-tCaido').trim();
  m.fechaServicio = mantVal('fM-fechaServ');
  m.fechaTermino = mantVal('fM-fechaTerm');
  var titBase = mantTituloBase(mantVal('fM-titulo'));
  m.tituloCaso = titBase ? titBase + ' ' + anioSel : '';
  m.tipoFalla = mantVal('fM-tipoFalla').trim();
  MANT_COMPONENTES.forEach(function (c) {
    m.identificacion[c[0]] = mantCheck('fM-id-' + c[0]);
    m.condiciones[c[0]] = mantCheck('fM-cond-' + c[0]);
    m.preventivo[c[0]] = mantCheck('fM-prev-' + c[0]);
  });
  m.descripcionEquipo = mantVal('fM-descEquipo').trim();
  m.condiciones.notas = mantVal('fM-condNotas').trim();
  m.descripcionCambios = mantVal('fM-descCambios').trim();
  m.conclusion = mantVal('fM-conclusion').trim();
  m.comentarios = mantVal('fM-comentarios').trim();
  m.fechaPlaneacion = mantVal('fM-fechaPlan');
  m.fechaCompromiso = mantVal('fM-fechaComp');
  m.periodoPrueba = mantVal('fM-periodoPrueba').trim();
  m.fechaLiberacion = mantVal('fM-fechaLib');
  m.observaciones = mantVal('fM-observaciones').trim();
  m.observacionesDetectadas = mantVal('fM-obsDet');
  m.whatsappUsuario = mantVal('fM-whatsapp').trim();
  var eq = m.equipo;
  eq.tipo = mantVal('fM-eq-tipo') || 'Laptop';
  eq.marca = mantVal('fM-eq-marca').trim();
  eq.modelo = mantVal('fM-modelo').trim();
  eq.serie = mantVal('fM-serie').trim();
  eq.hostname = mantVal('fM-hostname').trim();
  eq.cpu = mantVal('fM-eq-cpu').trim();
  eq.ramGB = mantNum('fM-eq-ram');
  eq.discoGB = mantNum('fM-eq-disco');
  eq.discoTipo = mantVal('fM-eq-discoTipo').trim();
  eq.ip = mantVal('fM-eq-ip').trim();
  eq.redes = parseRedesText(mantVal('fM-eq-redes'));
  eq.impresora = mantVal('fM-eq-impresora').trim();
  eq.anydeskId = mantVal('fM-eq-anydesk').trim();
  eq.anydeskAlias = mantVal('fM-eq-anydeskAlias').trim();
  eq.antivirus = mantVal('fM-eq-antivirus').trim();
  eq.so = mantVal('fM-eq-so').trim();
  eq.usuarioSistemas = mantCheck('fM-eq-usuarioSistemas');
  eq.politicas = mantPoliticasCumple({ cambioDias: mantNum('fM-pol-cambio'), minLongitud: mantNum('fM-pol-long'), bloqueoIntentos: mantNum('fM-pol-intentos'), bloqueoSegundos: mantNum('fM-pol-bloqueo'), bloqueoManual: !!(m.equipo.politicas && m.equipo.politicas.bloqueoManual) });
  if (mantFirmaData) m.firmaTecnico = mantFirmaData;
  return m;
}
function mantFillForm(m) {
  mantSetVal('fM-tecnico', m.tecnico);
  mantSetVal('fM-empresa', mantEmpresaOf(m));
  mantSetCheck('fM-tipo-sw', !m.tipo || String(m.tipo).indexOf('SOFTWARE') !== -1);
  mantSetCheck('fM-tipo-hw', !m.tipo || String(m.tipo).indexOf('HARDWARE') !== -1);
  mantSetVal('fM-area', m.area);
  mantSetVal('fM-responsable', m.responsable);
  mantSetVal('fM-tRep', m.tiempoReparacion);
  mantSetVal('fM-tViaje', m.tiempoViaje);
  mantSetVal('fM-tCaido', m.tiempoSistemaCaido);
  mantSetVal('fM-fechaServ', m.fechaServicio);
  mantSetVal('fM-fechaTerm', m.fechaTermino);
  mantSetVal('fM-titulo', mantTituloBase(m.tituloCaso) || MANT_TITULO_DEF);
  mantSetVal('fM-anio', String(mantAnioOf(m)));
  mantSetVal('fM-tipoFalla', m.tipoFalla);
  MANT_COMPONENTES.forEach(function (c) {
    mantSetCheck('fM-id-' + c[0], m.identificacion[c[0]]);
    mantSetCheck('fM-cond-' + c[0], m.condiciones[c[0]]);
    mantSetCheck('fM-prev-' + c[0], m.preventivo[c[0]]);
  });
  mantSetVal('fM-descEquipo', m.descripcionEquipo);
  mantSetVal('fM-condNotas', m.condiciones.notas);
  mantSetVal('fM-descCambios', m.descripcionCambios);
  mantSetVal('fM-conclusion', m.conclusion);
  mantSetVal('fM-comentarios', m.comentarios);
  mantSetVal('fM-fechaPlan', m.fechaPlaneacion);
  mantSetVal('fM-fechaComp', m.fechaCompromiso);
  mantSetVal('fM-periodoPrueba', m.periodoPrueba);
  mantSetVal('fM-fechaLib', m.fechaLiberacion);
  mantSetVal('fM-observaciones', m.observaciones);
  mantSetVal('fM-obsDet', m.observacionesDetectadas);
  mantSetVal('fM-whatsapp', m.whatsappUsuario);
  var eq = m.equipo || {};
  mantSetVal('fM-eq-tipo', eq.tipo);
  mantSetVal('fM-eq-marca', eq.marca);
  mantSetVal('fM-modelo', eq.modelo);
  mantSetVal('fM-serie', eq.serie);
  mantSetVal('fM-hostname', eq.hostname);
  mantSetVal('fM-eq-cpu', eq.cpu);
  mantSetVal('fM-eq-ram', eq.ramGB);
  mantSetVal('fM-eq-disco', eq.discoGB);
  mantSetVal('fM-eq-discoTipo', eq.discoTipo);
  mantSetVal('fM-eq-ip', eq.ip);
  mantSetVal('fM-eq-redes', redesText(eq));
  mantSetVal('fM-eq-impresora', eq.impresora);
  mantSetVal('fM-eq-anydesk', eq.anydeskId);
  mantSetVal('fM-eq-anydeskAlias', eq.anydeskAlias);
  mantSetVal('fM-eq-antivirus', eq.antivirus);
  mantSetVal('fM-eq-so', eq.so);
  mantSetCheck('fM-eq-usuarioSistemas', eq.usuarioSistemas);
  var pol = eq.politicas || {};
  mantSetVal('fM-pol-cambio', pol.cambioDias);
  mantSetVal('fM-pol-long', pol.minLongitud);
  mantSetVal('fM-pol-intentos', pol.bloqueoIntentos);
  mantSetVal('fM-pol-bloqueo', pol.bloqueoSegundos);
  mantPolFuente = (m.equipo && m.equipo.politicasFuente) || '';
  refreshMantPolLine();
  mantFirmaData = m.firmaTecnico || '';
  mantDrawFirmaOnCanvas(mantFirmaData);
}
function mantFormHasData() {
  var ids = ['fM-serie', 'fM-hostname', 'fM-modelo', 'fM-area', 'fM-responsable', 'fM-tRep', 'fM-tViaje', 'fM-tCaido', 'fM-fechaServ', 'fM-fechaTerm', 'fM-titulo', 'fM-tipoFalla', 'fM-descEquipo', 'fM-condNotas', 'fM-descCambios', 'fM-conclusion', 'fM-comentarios', 'fM-fechaPlan', 'fM-fechaComp', 'fM-periodoPrueba', 'fM-fechaLib', 'fM-observaciones', 'fM-obsDet', 'fM-whatsapp', 'fM-eq-marca', 'fM-eq-cpu', 'fM-eq-ram', 'fM-eq-disco', 'fM-eq-discoTipo', 'fM-eq-ip', 'fM-eq-redes', 'fM-eq-impresora', 'fM-eq-anydesk', 'fM-eq-anydeskAlias', 'fM-eq-antivirus', 'fM-eq-so'];
  var defVals = { 'fM-tRep': '/', 'fM-tViaje': '/', 'fM-tCaido': '/', 'fM-tipoFalla': '/', 'fM-fechaPlan': '/', 'fM-fechaComp': '/', 'fM-periodoPrueba': '/', 'fM-titulo': MANT_TITULO_DEF, 'fM-descCambios': MANT_DESC_CAMBIOS_DEF };
  for (var i = 0; i < ids.length; i++) { var vv = mantVal(ids[i]).trim(); if (vv && defVals[ids[i]] !== vv) return true; }
  var any = false;
  MANT_COMPONENTES.forEach(function (c) { if (mantCheck('fM-id-' + c[0]) || mantCheck('fM-cond-' + c[0]) || mantCheck('fM-prev-' + c[0])) any = true; });
  if (mantCheck('fM-eq-usuarioSistemas')) any = true;
  if (mantFirmaData) any = true;
  return any;
}
// Validación de 'Crear orden de servicio' (251): serie, hostname y
// modelo son obligatorios y destacados (aclaración de Gerardo 23:53) —
// si falta alguno, no se crea la orden y el toast dice cuál falta. El
// borrador SÍ se puede guardar sin ellos: lo que no se asigna es el folio.
// (255) Obligatorios para crear la orden: serie, hostname, modelo, tipo,
// título, tipo de falla, descripción, fecha del servicio, WhatsApp y
// firma del técnico. Área y Responsable YA NO son obligatorios: se llenan
// con lo que el usuario envía al firmar (mantFillFromFirma). La lista
// completa sirve para marcar en rojo cada campo vacío (punto 2); la
// función vieja sigue devolviendo el primero para el toast.
function mantFaltantesCrear(m) {
  var out = [];
  function falta(id, label, ok) { if (!ok) out.push({ id: id, label: label }); }
  falta('fM-serie', 'el número de serie del equipo', m.equipo.serie);
  falta('fM-hostname', 'el hostname del equipo', m.equipo.hostname);
  falta('fM-modelo', 'el modelo del equipo', m.equipo.modelo);
  if (!m.tipo) { out.push({ id: 'fM-tipo-sw', label: 'el tipo de mantenimiento' }); out.push({ id: 'fM-tipo-hw', label: 'el tipo de mantenimiento' }); }
  falta('fM-titulo', 'el título del caso', m.tituloCaso);
  falta('fM-tipoFalla', 'el tipo de falla', m.tipoFalla);
  falta('fM-descEquipo', 'la descripción del equipo', m.descripcionEquipo);
  falta('fM-fechaServ', 'la fecha del servicio', m.fechaServicio);
  falta('fM-whatsapp', 'el WhatsApp del usuario', m.whatsappUsuario);
  falta('fM-firmaCanvas', 'la firma del técnico', m.firmaTecnico);
  return out;
}
function mantFaltaCrear(m) {
  var f = mantFaltantesCrear(m);
  return f.length ? f[0].label : null;
}
// (255) Marca en rojo los campos obligatorios vacíos; se quita al
// escribir o cambiar el campo (listener en #mantFormBox).
function mantMarcarFaltantes(list) {
  var prev = document.querySelectorAll('.campo-falta');
  for (var i = 0; i < prev.length; i++) prev[i].classList.remove('campo-falta');
  list.forEach(function (f) { var el = document.getElementById(f.id); if (el && el.classList) el.classList.add('campo-falta'); });
}
function mantLimpiarFaltantes() { mantMarcarFaltantes([]); }
function mantOpenForm(m, fromDetId) {
  mantFormBase = m || null;
  mantFormId = m ? m.id : null;
  mantFormFromDet = fromDetId || null;
  mantFirmaData = m ? (m.firmaTecnico || '') : '';
  document.getElementById('mantFormTitle').textContent = m ? 'Editar borrador' : 'Nuevo mantenimiento';
  document.getElementById('mantFormBox').hidden = false;
  document.getElementById('mantOrderBox').hidden = true;
  document.getElementById('mantDetBox').hidden = true;
  if (m) mantFillForm(m); else { mantClearForm(); prefillMantTecnico(); }
  mantLimpiarFaltantes();
  mantApplyDefaults();
  mantScrollTo('mantFormBox');
}
function mantClearForm() {
  mantFormBase = null;
  mantFormId = null;
  mantFormFromDet = null;
  mantFirmaData = '';
  mantFillForm(newMantBlank());
  mantClearFirmaCanvas();
  prefillMantTecnico();
}
function mantCloseForm() {
  document.getElementById('mantFormBox').hidden = true;
  mantFormBase = null;
  mantFormId = null;
  mantFormFromDet = null;
  mantFirmaData = '';
  renderMant();
}
function mantSave(m) {
  var i = -1;
  mantenimientos.forEach(function (x, idx) { if (x.id === m.id) i = idx; });
  if (i === -1) mantenimientos.push(m); else mantenimientos[i] = m;
  saveMantLocal();
  cloudUpsertMant(m);
  renderMant();
}
function cloudUpsertMant(m) {
  if (!CLOUD_ENABLED || !cloudUser || !window.Cloud || !window.Cloud.upsertMant) return;
  window.Cloud.upsertMant(mantToCloudDoc(m)).catch(function (e) { console.warn('No se pudo guardar el mantenimiento en la nube', e); });
}
function cloudDeleteMant(id) {
  if (!CLOUD_ENABLED || !cloudUser || !window.Cloud || !window.Cloud.deleteMant) return;
  window.Cloud.deleteMant(id).catch(function (e) { console.warn('No se pudo borrar el mantenimiento en la nube', e); });
}
function loadMantLocal() {
  try {
    var raw = localStorage.getItem(MANT_LS_KEY);
    if (raw) { var arr = JSON.parse(raw); if (Array.isArray(arr)) mantenimientos = arr.map(mantFromCloud); }
  } catch (e) {}
}
function saveMantLocal() {
  try { localStorage.setItem(MANT_LS_KEY, JSON.stringify(mantenimientos.map(mantToCloudDoc))); } catch (e) {}
}
// Al recibir la lista de la nube, conservar los borradores locales que la
// nube aún no trae (igual que mergePrepsWithLocal).
function mergeMantWithLocal(docs) {
  var localById = {};
  mantenimientos.forEach(function (m) { localById[m.id] = m; });
  var out = docs.map(function (d) { return mantFromCloud(d); });
  var ids = {};
  out.forEach(function (m) { ids[m.id] = true; });
  Object.keys(localById).forEach(function (id) { if (!ids[id]) out.push(localById[id]); });
  return out;
}
async function migrateLocalMants() {
  try {
    if (!window.Cloud.getAllMantenimientos) return;
    var flag = MANT_MIG_KEY + ':' + cloudUser.uid;
    if (localStorage.getItem(flag)) return;
    var inCloud = await window.Cloud.getAllMantenimientos();
    var ids = {};
    inCloud.forEach(function (d) { ids[d.id] = true; });
    var pendientes = mantenimientos.filter(function (m) { return !ids[m.id]; });
    for (var i = 0; i < pendientes.length; i++) {
      await window.Cloud.upsertMant(mantToCloudDoc(pendientes[i]));
    }
    localStorage.setItem(flag, '1');
  } catch (e) { console.warn('Migración de mantenimientos pendiente', e); }
}
async function mantCrearOrden() {
  var m = mantReadForm();
  var faltantes = mantFaltantesCrear(m);
  if (faltantes.length) {
    mantMarcarFaltantes(faltantes);
    var nombres = [];
    faltantes.forEach(function (f) { if (nombres.indexOf(f.label) === -1) nombres.push(f.label); });
    showToast('Falta ' + nombres.join(', ') + ' para crear la orden.');
    return;
  }
  var folio = null;
  if (window.Cloud && window.Cloud.asignarFolio && CLOUD_ENABLED && cloudUser) {
    try { folio = await window.Cloud.asignarFolio(); } catch (e) { folio = null; }
  }
  if (!folio) {
    // Sin conexión: no se puede asignar folio; se guarda como borrador sin folio.
    m.estado = 'borrador';
    m.folio = null;
    mantSave(m);
    mantFormBase = m;
    mantFormId = m.id;
    showToast('Sin conexión: no se pudo asignar folio. Se guardó como borrador sin folio.');
    return;
  }
  m.folio = folio;
  m.estado = 'creada';
  mantSave(m);
  if (mantFormFromDet) cloudMarkDetectadoUsado(mantFormFromDet);
  mantCloseForm();
  mantShowOrder(m.id);
  showToast('Orden de servicio creada con folio ' + folio + '.');
}
function mantGuardarBorrador() {
  var m = mantReadForm();
  if (!m.folio) { m.estado = 'borrador'; m.folio = null; }
  mantSave(m);
  mantFormBase = m;
  mantFormId = m.id;
  showToast(m.folio ? 'Orden guardada.' : 'Borrador guardado.');
}
function mantCancelarForm() {
  if (!mantFormHasData()) { mantCloseForm(); return; }
  showConfirm('¿Descartar los cambios sin guardar?').then(function (ok) {
    if (!ok) return;
    mantCloseForm();
  });
}
function mantUseDetectado(id) {
  var d = null;
  detectados.forEach(function (x) { if (String(x.id) === String(id)) d = x; });
  if (!d) { showToast('Ese equipo detectado ya no está en la lista.'); return; }
  var m = mantFromDetectado(d);
  mantOpenForm(m, d.id);
  showToast('Datos del equipo detectado cargados. Revisa la serie, el hostname y el modelo.');
}
function mantFind(id) { var f = null; mantenimientos.forEach(function (x) { if (x.id === id) f = x; }); return f; }
function mantFirmaUrl(m) { return FIRMA_URL_BASE + '?id=' + encodeURIComponent(m.id); }
// Número para wa.me: solo dígitos; si tiene 10 dígitos es de México y se
// le antepone 52 (interpretación 251).
function mantWaNumber(num) {
  var d = String(num || '').replace(/\D/g, '');
  if (d.length === 10) d = '52' + d;
  return d;
}
function mantFirmaWaUrl(m) {
  var num = mantWaNumber(m.whatsappUsuario);
  var txt = 'Hola, te comparto la orden de servicio' + (m.folio ? ' con folio ' + m.folio : '') + ' de Checklist de Soporte. Para firmarla abre este enlace: ' + mantFirmaUrl(m);
  return 'https://wa.me/' + num + '?text=' + encodeURIComponent(txt);
}
function mantEnviarLink() {
  var m = mantFind(mantOrderId);
  if (!m) return;
  if (!mantWaNumber(m.whatsappUsuario)) { showToast('Falta el WhatsApp del usuario para enviar el formulario.'); return; }
  window.open(mantFirmaWaUrl(m), '_blank');
}
function mantPdfFalta(m) {
  if (!m.firmaTecnico) return 'la firma del técnico';
  if (!m.firma || !m.firma.firma) return 'la firma del usuario';
  return null;
}
// (255) Responsable y Área sin llenar al crear la orden: se toman de lo
// que el usuario envió al firmar (nombre y área del formulario de firma).
function mantRespOf(m) { return (m.responsable || (m.firma && m.firma.nombre) || ''); }
function mantAreaOf(m) { return (m.area || (m.firma && m.firma.area) || ''); }
// (255) Llena responsable/área con la firma llegada y lo guarda (update
// autenticado de la propia orden; nunca en firma.html, cuya regla pública
// solo deja tocar firma+estado). Solo si faltan: la guarda impide
// reescribir en bucle cuando la suscripción vuelva a disparar.
function mantFillFromFirma(m) {
  if (!m || !m.firma || !m.firma.firma) return false;
  if (m.estado === 'cancelada') return false;
  var cambio = false;
  if (!m.responsable && m.firma.nombre) { m.responsable = m.firma.nombre; cambio = true; }
  if (!m.area && m.firma.area) { m.area = m.firma.area; cambio = true; }
  if (!cambio) return false;
  if (CLOUD_ENABLED && cloudUser && (cloudRole === 'admin' || !m.tecnicoUid || m.tecnicoUid === cloudUser.uid)) mantSave(m);
  return true;
}
function renderMantOrder(m) {
  var eq = m.equipo || {};
  var body = document.getElementById('mantOrderBody');
  var both = !mantPdfFalta(m);
  var falta = mantPdfFalta(m);
  var html = '<h2>Orden de servicio' + (m.folio ? ' · Folio ' + esc(m.folio) : '') + '</h2>' +
    '<div class="sub">Estado: ' + esc(mantEstadoLabel(m)) + ' · Empresa: ' + esc(mantEmpresaOf(m)) + ' · Tipo: ' + esc(m.tipo || '—') + ' · Área: ' + esc(mantAreaOf(m) || 'Pendiente de firma') + '</div>' +
    '<div class="mant-id-line">Serie: ' + esc(eq.serie || '—') + ' · Hostname: ' + esc(eq.hostname || '—') + ' · Modelo: ' + esc(eq.modelo || '—') + '</div>' +
    '<div class="sub">Técnico: ' + esc(m.tecnico || '—') + ' · Responsable: ' + esc(mantRespOf(m) || 'Pendiente de firma') + '</div>' +
    '<div class="sub">Título del caso: ' + esc(mantTituloCompuesto(m)) + ' · Tipo de falla: ' + esc(m.tipoFalla || '—') + '</div>' +
    '<div class="sub">Fecha del servicio: ' + esc(m.fechaServicio || '—') + (m.fechaTermino ? ' · Término: ' + esc(m.fechaTermino) : '') + '</div>' +
    '<div class="sub">Firma del técnico: ' + (m.firmaTecnico ? 'sí ✓' : 'pendiente') + ' · Firma del usuario: ' + (m.firma && m.firma.firma ? 'sí ✓ (' + esc(m.firma.nombre || '') + ')' : 'pendiente') + '</div>';
  if (m.firma && m.firma.firma) {
    html += '<div class="sub">El usuario firmó: ' + esc(m.firma.nombre || '—') + ' · Área: ' + esc(m.firma.area || '—') + ' · Satisfacción: ' + esc(String(m.firma.satisfaccion == null ? '—' : m.firma.satisfaccion)) + '/10' + (m.firma.firmadoEn ? ' · ' + fmtDate(m.firma.firmadoEn) : '') + '</div>';
    if (m.firma.comentarios) html += '<div class="sub">Comentarios del usuario: ' + esc(m.firma.comentarios) + '</div>';
  }
  html += '<div class="sub">Link de firma: <a href="' + esc(mantFirmaUrl(m)) + '">' + esc(mantFirmaUrl(m)) + '</a></div>';
  if (body) body.innerHTML = html;
  var shareBtn = document.getElementById('btnMantCompartir');
  if (shareBtn) shareBtn.disabled = !both;
  var note = document.getElementById('mantOrderNote');
  if (note) note.textContent = both ? 'La orden tiene ambas firmas: ya puedes compartir la copia y generar el PDF.' : ('Para compartir la copia y generar el PDF falta ' + falta + '.');
  var cancelBtn = document.getElementById('btnMantCancelarOrden');
  if (cancelBtn) cancelBtn.hidden = !(m.estado === 'creada' || m.estado === 'firmada');
  var delBtn = document.getElementById('btnMantEliminarOrden');
  if (delBtn) delBtn.hidden = !(cloudRole === 'admin' && m.estado !== 'borrador');
}
function mantShowOrder(id) {
  var m = mantFind(id);
  if (!m) { showToast('Esa orden ya no está en la lista.'); return; }
  mantOrderId = id;
  document.getElementById('mantFormBox').hidden = true;
  document.getElementById('mantDetBox').hidden = true;
  renderMantOrder(m);
  document.getElementById('mantOrderBox').hidden = false;
  mantScrollTo('mantOrderBox');
}
// (254) Actualizar la orden desde la nube: cuando el usuario firma por el
// link de WhatsApp, la vista abierta queda desactualizada ("Firma del
// usuario: pendiente") hasta recargar; el botón re-lee la orden y la
// re-renderiza. El toast dice el resultado real, nunca un éxito falso.
async function mantActualizarOrden() {
  if (!mantOrderId) return;
  var btn = document.getElementById('btnMantActualizar');
  if (btn) btn.disabled = true;
  try {
    if (!window.Cloud || !window.Cloud.getMantenimiento) { showToast('No se puede actualizar sin conexión a la nube.'); return; }
    var fresh = await window.Cloud.getMantenimiento(mantOrderId);
    if (!fresh) { showToast('La orden ya no existe en la nube.'); return; }
    var m = mantFromCloud(fresh);
    var i = -1;
    mantenimientos.forEach(function (x, idx) { if (x.id === m.id) i = idx; });
    if (i === -1) mantenimientos.push(m); else mantenimientos[i] = m;
    saveMantLocal();
    renderMant();
    mantFillFromFirma(m);
    renderMantOrder(m);
    if (m.firma && m.firma.firma) showToast('El usuario ya firmó ✓');
    else showToast('Sin cambios: el usuario aún no firma.');
  } catch (e) {
    showToast('No se pudo actualizar: ' + (e && e.message ? e.message : 'error de conexión'));
  } finally {
    if (btn) btn.disabled = false;
  }
}
function mantCancelarOrden() {
  var m = mantFind(mantOrderId);
  if (!m) return;
  showConfirm('¿Cancelar esta orden? Se conserva el registro y el folio ' + (m.folio || '—') + ' no se vuelve a usar.').then(function (ok) {
    if (!ok) return;
    m.estado = 'cancelada';
    mantSave(m);
    renderMantOrder(m);
    showToast('Orden cancelada. El folio no se reutiliza.');
  });
}
function mantEliminarOrden(id) {
  var m = mantFind(id || mantOrderId);
  if (!m) return;
  showConfirm('¿Eliminar esta orden de servicio? Esta acción no se puede deshacer.').then(function (ok) {
    if (!ok) return;
    mantenimientos = mantenimientos.filter(function (x) { return x.id !== m.id; });
    saveMantLocal();
    cloudDeleteMant(m.id);
    document.getElementById('mantOrderBox').hidden = true;
    mantOrderId = null;
    renderMant();
    showToast('Orden de servicio eliminada.');
  });
}
// Escala de satisfacción (251, interpretación): 0–3 INACEPTABLE,
// 4–7 ACEPTABLE, 8–10 EXCELENTE.
function satLabel(v) {
  if (v == null || v === '') return '—';
  var n = Number(v);
  if (isNaN(n)) return String(v);
  if (n <= 3) return n + ' (INACEPTABLE)';
  if (n <= 7) return n + ' (ACEPTABLE)';
  return n + ' (EXCELENTE)';
}
// (254) Orden de servicio con el formato de papel F0.S1.01 Rev0: encabezado
// con las tres empresas, folio en rojo, casillas SOFTWARE/HARDWARE, los
// campos del formato y las firmas en sus bloques. (255) Una hoja tamaño
// carta (612x792): la descripción del equipo lleva solo el hostname y los
// demás datos del equipo van al final, en Conclusión/Comentarios; ningún
// dato se pierde. Si el contenido se desborda, fluye limpio a la página 2
// (need() mueve la sección).
function buildPdfMant(m, sigImgs) {
  sigImgs = sigImgs || {};
  var eq = m.equipo || {};
  var pol = eq.politicas || {};
  var W = 612, H = 792, M = 36, USABLE = H - M * 2;
  var pages = [[]];
  var yt = 0;
  function cur() { return pages[pages.length - 1]; }
  function need(h) { if (yt + h > USABLE) { pages.push([]); yt = 0; } }
  function py(ytop) { return H - M - ytop; }
  function T(str, x, ytop, f, s, color, align) {
    cur().push({ k: 't', x: x, y: py(ytop) - (s || 9) * 0.8, f: f || 'F1', s: s || 9, str: pdfSafe(str), color: color || null, a: align || 'L' });
  }
  function R(x, ytop, w, h, fill) {
    cur().push({ k: 'r', x: x, y: py(ytop) - h, w: w, h: h, fill: (fill == null ? null : fill) });
  }
  function check(x, ytop, checked, label, s) {
    s = s || 9;
    R(x, ytop, 9, 9, null);
    if (checked) T('X', x + 1.5, ytop + 0.5, 'F2', 8);
    if (label) T(label, x + 13, ytop, 'F1', s);
  }
  function wrapLines(str, w, s) {
    return wrapText(pdfSafe(str), Math.max(10, Math.floor(w / ((s || 9) * 0.5))));
  }
  function hasImg(im) { return !!(im && im.bytes && im.w && im.h); }
  function fitImg(im, maxW, maxH) {
    var sc = Math.min(maxW / im.w, maxH / im.h, 1);
    return { w: Math.max(4, Math.round(im.w * sc)), h: Math.max(4, Math.round(im.h * sc)) };
  }
  function val(v) { return (v == null || v === '') ? '-' : String(v); }
  function compList(o) { return MANT_COMPONENTES.filter(function (c) { return o && o[c[0]]; }).map(function (c) { return c[1]; }); }

  var emp = mantEmpresaOf(m);
  var tipoSW = (m.tipo || '').indexOf('SOFTWARE') !== -1;
  var tipoHW = (m.tipo || '').indexOf('HARDWARE') !== -1;
  var tecImg = hasImg(sigImgs.tecnico) ? sigImgs.tecnico : null;
  var usrImg = hasImg(sigImgs.usuario) ? sigImgs.usuario : null;

  // 1. Encabezado: empresas + contacto (solo Lapi) a la izquierda;
  // título, folio en rojo y SOFTWARE/HARDWARE a la derecha.
  need(84);
  var y0 = yt;
  R(36, y0, 168, 84, null);
  [['Lapi', 'Lapi'], ['Ludi', 'Ludi'], ['Lapi Hemodiálisis', 'Lapi Hemodiálisis']].forEach(function (e, i) {
    check(44, y0 + 8 + i * 17, emp === e[0], e[1], 11);
  });
  if (emp === 'Lapi') {
    T('SISTEMAS', 44, y0 + 56, 'F2', 7);
    T('Rosa Blanca 63, Col. Molino de Rosas', 44, y0 + 63, 'F1', 7);
    T('C.P. 01470 Tel. 53371283 y 53370207', 44, y0 + 70, 'F1', 7);
    T('sistemas@lapi.com.mx, info@lapi.com.mx', 44, y0 + 77, 'F1', 6.5);
  }
  T('ORDEN DE SERVICIO', 390, y0 + 4, 'F2', 15, null, 'C');
  R(492, y0 + 24, 84, 24, null);
  T('FOLIO', 485, y0 + 30, 'F2', 8, null, 'R');
  T(val(m.folio), 534, y0 + 28, 'F2', 13, 'red', 'C');
  check(308, y0 + 56, tipoSW, 'SOFTWARE', 9);
  check(408, y0 + 56, tipoHW, 'HARDWARE', 9);
  yt += 84 + 3;

  // 2. Área / Responsable.
  need(28);
  y0 = yt;
  R(36, y0, 264, 28, null); R(312, y0, 264, 28, null);
  T('ÁREA / UNIDAD', 42, y0 + 4, 'F2', 7);
  T(val(mantAreaOf(m)), 42, y0 + 14, 'F1', 9);
  T('RESPONSABLE', 318, y0 + 4, 'F2', 7);
  T(val(mantRespOf(m)), 318, y0 + 14, 'F1', 9);
  yt += 28 + 3;

  // 3. Quién presta el servicio + tiempos y fechas.
  need(32);
  y0 = yt;
  var campos3 = [
    ['NOMBRE DE QUIEN PRESTA EL SERVICIO', val(m.tecnico), 145],
    ['TIEMPO DE REPARACIÓN', val(m.tiempoReparacion), 73],
    ['TIEMPO DE VIAJE', val(m.tiempoViaje), 73],
    ['TIEMPO DE SISTEMA CAÍDO', val(m.tiempoSistemaCaido), 73],
    ['FECHA DEL SERVICIO', val(m.fechaServicio), 73],
    ['FECHA DE TÉRMINO', val(m.fechaTermino), 73]
  ];
  var x3 = 36;
  campos3.forEach(function (c, i) {
    R(x3, y0, c[2], 32, null);
    T(c[0], x3 + 3, y0 + 4, 'F2', i === 0 ? 6 : 5);
    T(c[1], x3 + 5, y0 + 15, 'F1', 8.5);
    x3 += c[2] + (i < campos3.length - 1 ? 6 : 0);
  });
  yt += 32 + 3;

  // 4. Título del caso.
  need(28);
  y0 = yt;
  T('TÍTULO DEL CASO', 36, y0, 'F2', 8);
  R(36, y0 + 9, 540, 19, null);
  T(mantTituloCompuesto(m), 42, y0 + 13, 'F1', 9.5);
  yt += 28 + 3;

  // 5. Tipo de falla (caja gris).
  var fallaLines = wrapLines(val(m.tipoFalla), 528, 9);
  var h5 = 9 + 6 + fallaLines.length * 11 + 6;
  need(h5);
  y0 = yt;
  T('TIPO DE FALLA REPORTADA / SOLICITUD DESARROLLO DE SOFTWARE', 36, y0, 'F2', 8);
  R(36, y0 + 9, 540, h5 - 9, 0.88);
  fallaLines.forEach(function (ln, i) { T(ln, 42, y0 + 13 + i * 11, 'F1', 9); });
  yt += h5 + 3;

  // 6. Identificación del equipo: 6 casillas.
  need(22);
  y0 = yt;
  T('IDENTIFICACIÓN DEL EQUIPO', 36, y0, 'F2', 8);
  MANT_COMPONENTES.forEach(function (c, i) {
    check(36 + i * 90, y0 + 10, !!(m.identificacion && m.identificacion[c[0]]), c[1], 9);
  });
  yt += 20 + 3;

  // 7. Descripción del equipo: SOLO el hostname (255). Los demás datos
  // del equipo (marca, modelo, serie, hardware, versiones, políticas,
  // impresora, AnyDesk y observaciones detectadas) van al final, en
  // Conclusión/Comentarios. Nada se pierde, solo se reubica.
  var ver = eq.versiones || {};
  var h7 = 9 + 6 + 10 + 6;
  need(h7);
  y0 = yt;
  T('DESCRIPCIÓN DEL EQUIPO', 36, y0, 'F2', 8);
  R(36, y0 + 9, 540, h7 - 9, null);
  T('Hostname: ' + val(eq.hostname), 42, y0 + 13, 'F1', 8.5);
  yt += h7 + 3;

  // 8. Condiciones generales + notas.
  var notaLines = wrapLines('Notas: ' + val((m.condiciones && m.condiciones.notas) || ''), 528, 8.5);
  var h8 = 20 + notaLines.length * 9.5 + 4;
  need(h8);
  y0 = yt;
  T('CONDICIONES GENERALES EN QUE SE ENCONTRÓ EL EQUIPO', 36, y0, 'F2', 8);
  MANT_COMPONENTES.forEach(function (c, i) {
    check(36 + i * 90, y0 + 10, !!(m.condiciones && m.condiciones[c[0]]), c[1], 9);
  });
  notaLines.forEach(function (ln, i) { T(ln, 42, y0 + 22 + i * 9.5, 'F1', 8.5); });
  yt += h8 + 3;

  // 9. Mantenimiento preventivo: sopleteo, limpieza y revisión.
  need(22);
  y0 = yt;
  T('MANTENIMIENTO PREVENTIVO', 36, y0, 'F2', 8);
  T('SOPLETEO, LIMPIEZA Y REVISIÓN DE:', 36, y0 + 10, 'F2', 8);
  MANT_COMPONENTES.forEach(function (c, i) {
    check(250 + i * 55, y0 + 10, !!(m.preventivo && m.preventivo[c[0]]), c[1], 8);
  });
  yt += 20 + 3;

  // 10. Descripción de cambios (caja gris).
  var cambLines = wrapLines(val(m.descripcionCambios), 528, 9);
  var h10 = 9 + 6 + cambLines.length * 11 + 6;
  need(h10);
  y0 = yt;
  T('DESCRIPCIÓN DE CAMBIOS Y SERVICIO DE HARDWARE / DESARROLLO DE SOFTWARE', 36, y0, 'F2', 8);
  R(36, y0 + 9, 540, h10 - 9, 0.88);
  cambLines.forEach(function (ln, i) { T(ln, 42, y0 + 13 + i * 11, 'F1', 9); });
  yt += h10 + 3;

  // 11. Conclusión y/o comentarios (con observaciones).
  var conclLines = [];
  wrapLines('Conclusión: ' + val(m.conclusion), 528, 8.5).forEach(function (w) { conclLines.push(w); });
  if (m.comentarios) wrapLines('Comentarios: ' + m.comentarios, 528, 8.5).forEach(function (w) { conclLines.push(w); });
  if (m.observaciones) wrapLines('Observaciones del técnico: ' + m.observaciones, 528, 8.5).forEach(function (w) { conclLines.push(w); });
  if (m.observacionesDetectadas) wrapLines('Datos detectados: ' + m.observacionesDetectadas, 528, 8.5).forEach(function (w) { conclLines.push(w); });
  // (255) Datos del equipo al final: serie, modelo, tipo, marca, hardware,
  // IP/redes, impresora, AnyDesk, antivirus, SO, versiones, políticas y
  // usuario de sistemas — y la descripción escrita por el técnico.
  var eqLines = [];
  if (m.descripcionEquipo) eqLines.push('Descripción: ' + m.descripcionEquipo);
  eqLines.push('Serie: ' + val(eq.serie) + ', Modelo: ' + val(eq.modelo) + ', Tipo: ' + val(eq.tipo) + ', Marca: ' + val(eq.marca));
  eqLines.push('Procesador: ' + val(eq.cpu) + ', RAM: ' + ((eq.ramGB == null || eq.ramGB === '') ? '-' : eq.ramGB + ' GB') + ', Disco: ' + ((eq.discoGB == null || eq.discoGB === '') ? '-' : eq.discoGB + ' GB' + (eq.discoTipo ? ' ' + eq.discoTipo : '')));
  var rd11 = redesText(eq);
  eqLines.push('IP: ' + val(eq.ip) + (rd11 ? ', Redes: ' + rd11 : '') + ', Impresora: ' + val(eq.impresora));
  eqLines.push('AnyDesk: ' + (eq.anydeskId ? anydeskDisplay(eq.anydeskId) + (eq.anydeskAlias ? ' (' + eq.anydeskAlias + ')' : '') : '-') + ', Antivirus: ' + val(eq.antivirus) + ', SO: ' + val(eq.so));
  if (ver.so || ver.antivirus || ver.esetAgent || ver.chrome) {
    eqLines.push('Versiones: ' + [ver.so ? 'SO: ' + ver.so : '', ver.antivirus ? 'Antivirus: ' + ver.antivirus : '', ver.esetAgent ? 'Agente ESET: ' + ver.esetAgent : '', ver.chrome ? 'Chrome: ' + ver.chrome : ''].filter(Boolean).join(', '));
  }
  eqLines.push(pdfSafe(politicasText(pol)));
  eqLines.push('Usuario de sistemas: ' + (eq.usuarioSistemas ? 'Sí' : 'No'));
  eqLines.forEach(function (ln) { wrapLines(ln, 528, 8.5).forEach(function (w) { conclLines.push(w); }); });
  if (!conclLines.length) conclLines = ['-'];
  var h11 = 9 + 6 + conclLines.length * 9.5 + 6;
  need(h11);
  y0 = yt;
  T('CONCLUSIÓN Y/O COMENTARIOS DEL SERVICIO (SISTEMAS)', 36, y0, 'F2', 8);
  R(36, y0 + 9, 540, h11 - 9, null);
  conclLines.forEach(function (ln, i) { T(ln, 42, y0 + 13 + i * 9.5, 'F1', 8.5); });
  yt += h11 + 3;

  // 12. Cuatro bloques de fecha con firmas (Sistemas / Área solicitante).
  // Planeación, Compromiso y Periodo de prueba llevan '/' (sin firmar
  // ahí); solo la Liberación lleva la fecha elegida y ambas firmas.
  need(58);
  y0 = yt;
  var fases = [
    ['FECHA DE PLANEACIÓN', val(m.fechaPlaneacion), null, null],
    ['FECHA DE COMPROMISO DE INSTALACIÓN', val(m.fechaCompromiso), null, null],
    ['PERIODO DE PRUEBA', val(m.periodoPrueba), null, null],
    ['FECHA DE LIBERACIÓN', val(m.fechaLiberacion), tecImg, usrImg]
  ];
  fases.forEach(function (f, j) {
    var x = 36 + j * 135;
    T(f[0], x, y0, 'F2', 5.5);
    T(f[1], x, y0 + 9, 'F1', 8.5);
    R(x, y0 + 19, 61, 32, 0.88);
    R(x + 66, y0 + 19, 61, 32, 0.88);
    T('FIRMA', x + 30, y0 + 22, 'F1', 7, null, 'C');
    T('FIRMA', x + 96, y0 + 22, 'F1', 7, null, 'C');
    T('SISTEMAS', x + 30, y0 + 54, 'F1', 7, null, 'C');
    T('ÁREA SOLICITANTE', x + 96, y0 + 54, 'F1', 7, null, 'C');
    if (f[2]) { var d1 = fitImg(f[2], 57, 18); cur().push({ k: 'img', name: 'tecnico', x: x + 2, y: py(y0 + 29) - d1.h, w: d1.w, h: d1.h }); }
    else if (j === 3) T(m.tecnico || '-', x + 30, y0 + 30, 'F1', 7, null, 'C');
    if (f[3]) { var d2 = fitImg(f[3], 57, 18); cur().push({ k: 'img', name: 'usuario', x: x + 68, y: py(y0 + 29) - d2.h, w: d2.w, h: d2.h }); }
    else if (j === 3 && m.firma) T(m.firma.nombre || '-', x + 96, y0 + 30, 'F1', 7, null, 'C');
  });
  yt += 58 + 3;

  // 13. Comentarios del usuario + escala de satisfacción + conformidad.
  need(116);
  y0 = yt;
  R(36, y0, 258, 116, 0.88);
  T('COMENTARIOS', 42, y0 + 5, 'F2', 8);
  var comLines = (m.firma && m.firma.comentarios) ? wrapLines(m.firma.comentarios, 246, 8.5) : ['-'];
  comLines.forEach(function (ln, i) { T(ln, 42, y0 + 16 + i * 10, 'F1', 8.5); });
  var xr = 302;
  var escLines = wrapText(pdfSafe('ESTIMADO USUARIO LE DAMOS A CONOCER COMO REFERENCIA LA SIGUIENTE ESCALA DE SATISFACCIÓN PARA PODER EVALUAR NUESTRO SERVICIO'), 65);
  escLines.forEach(function (ln, i) { T(ln, xr, y0 + i * 7.5, 'F1', 6.5); });
  var sat = m.firma ? m.firma.satisfaccion : null;
  var yEsc = y0 + escLines.length * 7.5 + 5;
  for (var n = 0; n <= 10; n++) {
    var bx = xr + n * 24;
    R(bx, yEsc, 20, 15, (sat != null && sat !== '' && Number(sat) === n) ? 0.75 : null);
    T(String(n), bx + 10, yEsc + 2, (sat != null && sat !== '' && Number(sat) === n) ? 'F2' : 'F1', 8, null, 'C');
  }
  T('Escala de satisfacción (0-10): ' + satLabel(sat), xr, yEsc + 17, 'F1', 8);
  if (sat != null && sat !== '') {
    var marks = [];
    for (var i2 = 0; i2 <= 10; i2++) marks.push(i2 === Number(sat) ? '[' + i2 + ']' : String(i2));
    T(marks.join('  '), xr, yEsc + 26, 'F1', 8);
  }
  T('INACEPTABLE 0-3, ACEPTABLE 4-7, EXCELENTE 8-10', xr, yEsc + 35, 'F1', 7.5);
  var yConf = yEsc + 46;
  R(xr, yConf, 274, 116 - (yConf - y0), 0.88);
  T('FECHA, HORA, NOMBRE Y FIRMA DE CONFORMIDAD', xr + 5, yConf + 4, 'F2', 6.5);
  if (m.firma) {
    T('Fecha: ' + (m.firma.firmadoEn ? fmtDate(m.firma.firmadoEn) : '-') + '  Hora: ' + (m.firma.firmadoEn ? fmtTime(m.firma.firmadoEn) : '-'), xr + 5, yConf + 14, 'F1', 7.5);
    T('Nombre: ' + (m.firma.nombre || '-') + '  Área: ' + (m.firma.area || '-'), xr + 5, yConf + 23, 'F1', 7.5);
    if (usrImg) { var d3 = fitImg(usrImg, 120, 14); cur().push({ k: 'img', name: 'usuario', x: xr + 5, y: py(yConf + 28) - d3.h, w: d3.w, h: d3.h }); }
    else T('Firma: ' + (m.firma.nombre || '-') + ' (guardada en la app)', xr + 5, yConf + 30, 'F1', 7.5);
  } else {
    T('Pendiente de firma.', xr + 5, yConf + 14, 'F1', 8);
  }
  yt += 116 + 3;

  // 14. Pie del formato.
  need(12);
  y0 = yt;
  T('F0.S1.01', 36, y0, 'F1', 8);
  T('Generado el ' + fmtDate(Date.now()) + ' - Checklist de Soporte', 306, y0, 'F1', 8, null, 'C');
  T('Rev0.', 576, y0, 'F1', 8, null, 'R');
  yt += 12;

  return assemblePdfOps(pages, sigImgs, { w: 612, h: 792 });
}
// Convierte una firma (data URL PNG del canvas o de la página de firma)
// a JPEG sobre fondo blanco, que es lo que el PDF puede incrustar.
function dataUrlToJpeg(dataUrl, maxW) {
  return new Promise(function (resolve) {
    try {
      if (typeof Image === 'undefined') { resolve(null); return; }
      var img = new Image();
      img.onload = function () {
        try {
          var c = document.createElement('canvas');
          var scale = Math.min(1, (maxW || 400) / (img.width || 1));
          c.width = Math.max(1, Math.round((img.width || 1) * scale));
          c.height = Math.max(1, Math.round((img.height || 1) * scale));
          var ctx = c.getContext('2d');
          if (!ctx) { resolve(null); return; }
          ctx.fillStyle = '#ffffff';
          ctx.fillRect(0, 0, c.width, c.height);
          ctx.drawImage(img, 0, 0, c.width, c.height);
          var url = c.toDataURL('image/jpeg', 0.85);
          var b64 = (url || '').split(',')[1] || '';
          var bin = atob(b64);
          var bytes = new Uint8Array(bin.length);
          for (var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
          resolve({ bytes: bytes, w: c.width, h: c.height });
        } catch (e) { resolve(null); }
      };
      img.onerror = function () { resolve(null); };
      img.src = dataUrl;
    } catch (e) { resolve(null); }
  });
}
async function mantPdfBlob(m) {
  var imgs = {};
  try {
    var t = await dataUrlToJpeg(m.firmaTecnico, 400);
    if (t) imgs.tecnico = t;
    if (m.firma && m.firma.firma) {
      var u = await dataUrlToJpeg(m.firma.firma, 400);
      if (u) imgs.usuario = u;
    }
  } catch (e) {}
  var blob = buildPdfMant(m, imgs);
  return { blob: blob, name: 'orden-servicio-' + (m.folio || m.id) + '.pdf' };
}
// (254) Guardar un PDF de verdad en el teléfono: Filesystem.writeFile en
// Documentos (respaldo CACHE), verificado con stat ANTES de avisar; luego
// se abre con FileOpener o se comparte con Share. Devuelve 'guardado' si
// el archivo quedó verificado, 'web' si no hay Capacitor nativo (el
// llamador usa entonces el camino web) y LANZA el error si la escritura
// falló en un teléfono (el llamador lo muestra, no promete nada falso).
async function guardarPdfCapacitor(blob, name, texto) {
  var Plugins = window.Capacitor && window.Capacitor.Plugins;
  if (!Plugins || !Plugins.Filesystem) return 'web';
  var platform = 'web';
  try { if (window.Capacitor.getPlatform) platform = window.Capacitor.getPlatform(); } catch (e) {}
  if (platform !== 'android' && platform !== 'ios') return 'web';
  var base64 = await blobToBase64(blob);
  var saved = null, dirUsado = '';
  try {
    saved = await Plugins.Filesystem.writeFile({ path: name, data: base64, directory: 'DOCUMENTS' });
    dirUsado = 'DOCUMENTS';
  } catch (eDoc) {
    saved = await Plugins.Filesystem.writeFile({ path: name, data: base64, directory: 'CACHE' });
    dirUsado = 'CACHE';
  }
  var st = null;
  try { st = await Plugins.Filesystem.stat({ path: name, directory: dirUsado }); } catch (eSt) {}
  if (!st || !st.size) {
    var err = new Error('no se pudo verificar el archivo guardado');
    err.code = 'no-se-verifico';
    throw err;
  }
  var uri = st.uri || (saved && saved.uri);
  var abierto = false;
  if (Plugins.FileOpener && uri) {
    try { await Plugins.FileOpener.open({ filePath: uri, contentType: 'application/pdf' }); abierto = true; } catch (eFo) {}
  }
  if (!abierto && Plugins.Share && uri) {
    try { await Plugins.Share.share({ title: 'Checklist de Soporte', text: texto, url: uri, dialogTitle: 'Orden de servicio' }); abierto = true; } catch (eSh) {}
  }
  showToast('PDF guardado: ' + name + (dirUsado === 'DOCUMENTS' ? ' (en Documentos).' : ' (en archivos temporales).'));
  return 'guardado';
}
// El PDF solo se genera con ambas firmas (técnico + usuario); si falta
// alguna, el botón avisa con toast cuál falta.
async function sharePdfMant(m) {
  var falta = mantPdfFalta(m);
  if (falta) { showToast('Falta ' + falta + ' para generar el PDF.'); return; }
  var out = await mantPdfBlob(m);
  var texto = 'Orden de servicio' + (m.folio ? ' folio ' + m.folio : '') + ' — Checklist de Soporte.';
  try {
    var res = await guardarPdfCapacitor(out.blob, out.name, texto);
    if (res === 'guardado') return;
  } catch (e) {
    showToast('No se pudo guardar el PDF: ' + (e && e.message ? e.message : 'error al escribir el archivo'));
    return;
  }
  var file = new File([out.blob], out.name, { type: 'application/pdf' });
  if (navigator.canShare && navigator.canShare({ files: [file] })) {
    navigator.share({ files: [file], title: 'Checklist de Soporte', text: texto }).catch(function () {});
    return;
  }
  var a = document.createElement('a');
  a.href = URL.createObjectURL(out.blob);
  a.download = out.name;
  a.click();
  setTimeout(function () { URL.revokeObjectURL(a.href); }, 5000);
  if (navigator.share) {
    navigator.share({ title: 'Checklist de Soporte', text: texto + ' El PDF se descargó, adjúntalo en WhatsApp.' }).catch(function () {});
  } else {
    showToast('PDF descargado: ' + out.name + '. Compártelo por WhatsApp desde tus archivos.');
  }
}
// Compartir copia con el usuario (share nativo como el Excel de renta):
// solo con ambas firmas.
async function shareMantCopy(m) {
  var falta = mantPdfFalta(m);
  if (falta) { showToast('Falta ' + falta + ' para compartir la copia.'); return; }
  var out = await mantPdfBlob(m);
  var saved = null;
  try {
    var Plugins = window.Capacitor && window.Capacitor.Plugins;
    if (!Plugins || !Plugins.Filesystem || !Plugins.Share) throw new Error('share-no-disponible');
    var base64 = await blobToBase64(out.blob);
    saved = await Plugins.Filesystem.writeFile({ path: out.name, data: base64, directory: 'CACHE' });
    await Plugins.Share.share({
      title: 'Checklist de Soporte',
      text: 'Orden de servicio' + (m.folio ? ' folio ' + m.folio : '') + ' — Checklist de Soporte.',
      url: saved.uri,
      dialogTitle: 'Compartir copia con el usuario'
    });
  } catch (e) {
    // (254) Si el archivo ya quedó escrito en CACHE (p. ej. el usuario
    // canceló el compartir), el PDF existe: avisar dónde está, no
    // prometer una descarga que en el teléfono no ocurre.
    if (saved) { showToast('PDF guardado en archivos temporales: ' + out.name + '.'); return; }
    // Sin Capacitor (navegador): intentar el share web con el archivo y,
    // si tampoco se puede, descargar el PDF y avisar de la descarga.
    try {
      var file2 = new File([out.blob], out.name, { type: 'application/pdf' });
      if (navigator.canShare && navigator.canShare({ files: [file2] })) {
        await navigator.share({ files: [file2], title: 'Checklist de Soporte', text: 'Orden de servicio' + (m.folio ? ' folio ' + m.folio : '') + ' — Checklist de Soporte.' });
        return;
      }
    } catch (e2) {}
    var a = document.createElement('a');
    a.href = URL.createObjectURL(out.blob);
    a.download = out.name;
    a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 5000);
    showToast('PDF descargado: ' + out.name + '. Compártelo por WhatsApp desde tus archivos.');
  }
}
// Firma del técnico: canvas con dedo o ratón.
function mantFirmaCanvasCtx() {
  var cv = document.getElementById('fM-firmaCanvas');
  if (!cv) return null;
  try { return cv.getContext('2d'); } catch (e) { return null; }
}
function initMantFirmaCanvas() {
  var cv = document.getElementById('fM-firmaCanvas');
  if (!cv) return;
  var ctx = mantFirmaCanvasCtx();
  if (!ctx) return;
  var drawing = false, lastX = 0, lastY = 0;
  function pos(e) {
    var r = (cv.getBoundingClientRect) ? cv.getBoundingClientRect() : { left: 0, top: 0, width: cv.width, height: cv.height };
    var x = (e.offsetX != null) ? e.offsetX : ((e.clientX - r.left) * (cv.width / (r.width || 1)));
    var y = (e.offsetY != null) ? e.offsetY : ((e.clientY - r.top) * (cv.height / (r.height || 1)));
    return { x: x, y: y };
  }
  cv.addEventListener('pointerdown', function (e) {
    e.preventDefault();
    drawing = true;
    var p = pos(e);
    lastX = p.x; lastY = p.y;
    if (cv.setPointerCapture) { try { cv.setPointerCapture(e.pointerId); } catch (e2) {} }
  });
  cv.addEventListener('pointermove', function (e) {
    if (!drawing) return;
    e.preventDefault();
    var p = pos(e);
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 2;
    ctx.lineCap = 'round';
    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(p.x, p.y);
    ctx.stroke();
    lastX = p.x; lastY = p.y;
  });
  function end() {
    if (!drawing) return;
    drawing = false;
    try { mantFirmaData = cv.toDataURL('image/png'); } catch (e2) { mantFirmaData = ''; }
  }
  cv.addEventListener('pointerup', end);
  cv.addEventListener('pointercancel', end);
}
function mantClearFirmaCanvas() {
  mantFirmaData = '';
  var cv = document.getElementById('fM-firmaCanvas');
  var ctx = mantFirmaCanvasCtx();
  if (cv && ctx) { try { ctx.clearRect(0, 0, cv.width, cv.height); } catch (e) {} }
}
function mantDrawFirmaOnCanvas(dataUrl) {
  var cv = document.getElementById('fM-firmaCanvas');
  var ctx = mantFirmaCanvasCtx();
  if (!cv || !ctx) return;
  try { ctx.clearRect(0, 0, cv.width, cv.height); } catch (e) {}
  if (!dataUrl || typeof Image === 'undefined') return;
  try {
    var img = new Image();
    img.onload = function () { try { ctx.drawImage(img, 0, 0, cv.width, cv.height); } catch (e) {} };
    img.src = dataUrl;
  } catch (e) {}
}
function refreshMantPolLine() {
  var el = document.getElementById('mantPolLine');
  if (!el) return;
  var txt = politicasText({ cambioDias: mantNum('fM-pol-cambio'), minLongitud: mantNum('fM-pol-long'), bloqueoIntentos: mantNum('fM-pol-intentos'), bloqueoSegundos: mantNum('fM-pol-bloqueo') });
  if (mantPolFuente) txt += ' · Fuente: ' + mantPolFuente;
  el.textContent = txt;
}
// Selector de sección (Inicio).
document.getElementById('btnGoPreparar').addEventListener('click', function () { showVista('preparar'); });
document.getElementById('btnGoRec').addEventListener('click', function () { showVista('rec'); });
document.getElementById('btnGoFor').addEventListener('click', function () { showVista('for'); });
document.getElementById('btnGoMant').addEventListener('click', function () { showVista('mant'); });
// Mantenimientos: lista, formulario y orden.
document.getElementById('btnMantNuevo').addEventListener('click', function () { mantOpenForm(null, null); });
document.getElementById('btnMantDet').addEventListener('click', function () { var b = document.getElementById('mantDetBox'); b.hidden = !b.hidden; if (!b.hidden) renderMantDetectados(); });
document.getElementById('btnMantDetectar').addEventListener('click', function () {
  detectarEquipo(document.getElementById('btnMantDetectar')).then(function (ok) {
    if (!ok) return;
    // (252) Al detectar desde Mantenimientos, el panel se abre solo
    // para que el usuario vea el equipo y le dé mantenimiento sin
    // tener que pulsar «Equipos detectados».
    var b = document.getElementById('mantDetBox');
    b.hidden = false;
    renderMantDetectados();
  });
});
document.getElementById('mantDetList').addEventListener('click', function (e) {
  var b = e.target.closest('[data-mant-det-use]');
  if (b) mantUseDetectado(b.getAttribute('data-mant-det-use'));
});
document.getElementById('mantAdminFilter').addEventListener('change', function (e) { mantAdminViewUid = e.target.value; renderMant(); });
document.getElementById('btnMantCrear').addEventListener('click', function () { mantCrearOrden(); });
// (255) Quitar la marca roja al escribir o cambiar el campo. Si se marca
// un checkbox de tipo, se quitan las dos (el tipo ya quedó cubierto).
['input', 'change'].forEach(function (ev) {
  document.getElementById('mantFormBox').addEventListener(ev, function (e) {
    var t = e.target;
    if (!t || !t.classList) return;
    t.classList.remove('campo-falta');
    if (t.id === 'fM-tipo-sw' || t.id === 'fM-tipo-hw') {
      var otro = document.getElementById(t.id === 'fM-tipo-sw' ? 'fM-tipo-hw' : 'fM-tipo-sw');
      if (otro && otro.classList) otro.classList.remove('campo-falta');
    }
  });
});
document.getElementById('btnMantGuardar').addEventListener('click', function () { mantGuardarBorrador(); });
document.getElementById('btnMantCancelar').addEventListener('click', function () { mantCancelarForm(); });
document.getElementById('btnMantFirmaLimpiar').addEventListener('click', function () { mantClearFirmaCanvas(); });
document.getElementById('btnMantWaLink').addEventListener('click', function () { mantEnviarLink(); });
document.getElementById('btnMantPdf').addEventListener('click', function () { var m = mantFind(mantOrderId); if (m) sharePdfMant(m); });
document.getElementById('btnMantActualizar').addEventListener('click', function () { mantActualizarOrden(); });
document.getElementById('btnMantCompartir').addEventListener('click', function () { var m = mantFind(mantOrderId); if (m) shareMantCopy(m); });
document.getElementById('btnMantCancelarOrden').addEventListener('click', function () { mantCancelarOrden(); });
document.getElementById('btnMantEliminarOrden').addEventListener('click', function () { mantEliminarOrden(mantOrderId); });
document.getElementById('btnMantVolver').addEventListener('click', function () { document.getElementById('mantOrderBox').hidden = true; mantOrderId = null; renderMant(); });
document.getElementById('mantList').addEventListener('click', function (e) {
  var t = e.target;
  var q = function (attr) { var el = t.closest('[' + attr + ']'); return el ? el.getAttribute(attr) : null; };
  var id = q('data-mant-edit') || q('data-mant-order') || q('data-mant-cancel-order') || q('data-mant-del') || q('data-mant-del-order');
  if (!id) return;
  var m = mantFind(id);
  if (!m) return;
  if (t.closest('[data-mant-edit]')) { mantOpenForm(m, null); return; }
  if (t.closest('[data-mant-order]')) { mantShowOrder(id); return; }
  if (t.closest('[data-mant-cancel-order]')) {
    showConfirm('¿Cancelar esta orden? Se conserva el registro y el folio ' + (m.folio || '—') + ' no se vuelve a usar.').then(function (ok) {
      if (!ok) return;
      m.estado = 'cancelada';
      mantSave(m);
      if (!document.getElementById('mantOrderBox').hidden) renderMantOrder(m);
      showToast('Orden cancelada. El folio no se reutiliza.');
    });
    return;
  }
  if (t.closest('[data-mant-del-order]')) {
    if (cloudRole !== 'admin') return;
    mantEliminarOrden(id);
    return;
  }
  if (t.closest('[data-mant-del]')) {
    showConfirm('¿Eliminar este borrador de mantenimiento?').then(function (ok) {
      if (!ok) return;
      mantenimientos = mantenimientos.filter(function (x) { return x.id !== id; });
      saveMantLocal();
      cloudDeleteMant(id);
      renderMant();
    });
  }
});
['fM-pol-cambio', 'fM-pol-long', 'fM-pol-intentos', 'fM-pol-bloqueo'].forEach(function (id) {
  var el = document.getElementById(id);
  if (el) el.addEventListener('input', refreshMantPolLine);
});
// Descripción del equipo (251): si sigue vacía, copia el hostname al
// teclearlo; lo escrito a mano nunca se sobrescribe.
(function () {
  var hn = document.getElementById('fM-hostname');
  if (hn) hn.addEventListener('input', function () {
    var de = document.getElementById('fM-descEquipo');
    if (de && !de.value.trim()) de.value = hn.value;
  });
})();
renderMantCheckboxes();
initMantFirmaCanvas();
loadMantLocal();

// (254) Bloqueo de Mantenimientos por usuario: el admin lo pone en
// users/{uid}.mantBloqueado. El bloqueo no desactiva al usuario y nunca
// aplica al admin ni en modo local (sin sesión).
function mantBloqueado() {
  return !!(CLOUD_ENABLED && cloudUser && cloudRole !== 'admin' && cloudUser.mantBloqueado);
}
function refreshMantAccess() {
  var b = mantBloqueado();
  var go = document.getElementById('btnGoMant');
  if (go) go.disabled = b;
  var tab = document.querySelector('#tabs .tab[data-v="mant"]');
  if (tab) tab.disabled = b;
}
// Menu de secciones (251): 'inicio' es el selector que se muestra al
// abrir la app, cada vez, sin recordar la última sección.
function showVista(v) {
  if (v === 'usuarios' && cloudRole !== 'admin') v = 'inicio';
  if (v === 'mant' && mantBloqueado()) { showToast('El acceso a Mantenimientos está bloqueado por el administrador.'); v = 'inicio'; }
  document.getElementById('viewInicio').hidden = v !== 'inicio';
  document.getElementById('viewPreparar').hidden = v !== 'preparar';
  document.getElementById('viewRenta-rec').hidden = v !== 'rec';
  document.getElementById('viewRenta-for').hidden = v !== 'for';
  document.getElementById('viewMant').hidden = v !== 'mant';
  document.getElementById('viewUsuarios').hidden = v !== 'usuarios';
  document.getElementById('viewEquipo').hidden = v !== 'equipo';
  document.getElementById('viewCuenta').hidden = true;
  document.getElementById('viewBio').hidden = true;
  if (v === 'usuarios') renderUsuarios();
  if (v === 'equipo') { renderEquipo(); refreshTeamUsers(); }
  if (v === 'preparar') prefillTecnico();
  if (v === 'mant') { prefillMantTecnico(); renderMant(); }
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
    if (!aiKey) { showToast(aiErrorText({ message: 'no-key' })); return; }
    if (!rec.fotoDanos) { showToast('Este equipo no tiene foto para revisar.'); return; }
    aiBusy = true;
    aiAnswers['renta-' + rec.id] = 'Revisando la foto...';
    render();
    askAI(danosPrompt(rec), rec.fotoDanos).then(function (txt) { rec.danosIA = txt || 'La IA no devolvió respuesta.'; delete aiAnswers['renta-' + rec.id]; cloudUpsert(rec); save(); render(); }).catch(function (e) { aiAnswers['renta-' + rec.id] = aiErrorText(e); render(); }).then(function () { aiBusy = false; });
    return;
  }
  if (t.hasAttribute('data-renta-next')) { rec.estado = rentaNext('rec', rec.estado); cloudUpsert(rec); save(); render(); return; }
  // Confirmación inline (251): solo con Sí se elimina el equipo de renta.
  if (t.hasAttribute('data-renta-del')) {
    showConfirm('¿Eliminar este equipo de renta?').then(function (ok) {
      if (!ok) return;
      state.renta = state.renta.filter(function (r) { return r.id !== id; });
      cloudDelete(id);
      save(); render();
    });
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
  if (t.closest('[data-renta-sel-all]')) { rentaSelTodosFor(true); return; }
  if (t.closest('[data-renta-sel-none]')) { rentaSelTodosFor(false); return; }
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
    rec.entregadoAt = Date.now();
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
  if (t.hasAttribute('data-renta-reopen')) { rec.estado = 'revisado'; rec.entregadoPor = ''; rec.entregadoAt = null; cloudUpsert(rec); save(); render(); return; }
  // Confirmación inline (251): solo con Sí se elimina el equipo de renta.
  if (t.hasAttribute('data-renta-del')) {
    showConfirm('¿Eliminar este equipo de renta?').then(function (ok) {
      if (!ok) return;
      state.renta = state.renta.filter(function (r) { return r.id !== id; });
      if (state.entregaActual === id) state.entregaActual = null;
      cloudDelete(id);
      save(); render();
    });
  }
});
document.getElementById('list-for').addEventListener('change', function (e) {
  var t = e.target;
  var cb = t.closest ? t.closest('[data-renta-sel]') : null;
  if (!cb) return;
  var id = cb.getAttribute('data-renta-sel');
  if (!id) return;
  if (cb.checked) rentaSelFor[id] = true; else delete rentaSelFor[id];
  rentaActualizarSelInfo();
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
  // Escritorio (251): sin huella en el .exe, aunque haya credencial guardada.
  if (window.Desktop) {
    btn.hidden = true;
    var disD = document.getElementById('btnBioDisable');
    var enaD = document.getElementById('btnBioEnable');
    if (disD) disD.hidden = true;
    if (enaD) enaD.hidden = true;
    return;
  }
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
    if (window.Desktop) return;
    if (localStorage.getItem('checklist-bio-declined') === '1') return;
    if (!await bioCheck()) return;
    if (await bioHasStored()) return;
    if (!sessionPassword) return;
    // Confirmación inline (251): offerBiometrics ya es async, así que
    // se espera al modal; solo con Sí se activa la huella.
    if (!await showConfirm('¿Activar el acceso con huella en este teléfono para entrar sin escribir tu contraseña?')) {
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
  var remember = window.Desktop ? false : document.getElementById('loginRemember').checked;
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
    if (!P || !P.NativeBiometric) { showToast('Este teléfono no tiene acceso biométrico.'); return; }
    if (!sessionPassword || !cloudUser) { showToast('Entra con tu contraseña primero y vuelve a intentarlo.'); return; }
    var av = await P.NativeBiometric.isAvailable();
    if (!av.isAvailable) { showToast('Este teléfono no tiene huella o rostro configurado.'); return; }
    await P.NativeBiometric.verifyIdentity({ reason: 'Activa el acceso con huella para Checklist de Soporte.', title: 'Checklist de Soporte', subtitle: 'Acceso con huella', negativeButtonText: 'Cancelar' });
    await P.NativeBiometric.setCredentials({ username: cloudUser.email, password: sessionPassword, server: BIO_SERVER });
    localStorage.removeItem('checklist-bio-declined');
    showToast('Acceso con huella activado en este teléfono.');
    refreshBioButton();
  } catch (e) { showToast('No se pudo activar el acceso con huella.'); }
});
document.getElementById('btnBioDisable').addEventListener('click', async function () {
  try { var P = window.Capacitor.Plugins; if (P && P.NativeBiometric) await P.NativeBiometric.deleteCredentials({ server: BIO_SERVER }); } catch (e) {}
  localStorage.setItem('checklist-bio-declined', '1');
  showToast('Acceso con huella desactivado en este teléfono.');
  refreshBioButton();
});
document.getElementById('btnPassSave').addEventListener('click', function () {
  var actual = document.getElementById('fPassActual').value;
  var nueva = document.getElementById('fPassNueva').value;
  var nueva2 = document.getElementById('fPassNueva2').value;
  if (nueva.length < 6) { showToast('La nueva contraseña debe tener al menos 6 caracteres.'); return; }
  if (nueva !== nueva2) { showToast('La nueva contraseña no coincide.'); return; }
  window.Cloud.changeOwnPassword(actual, nueva).then(async function () {
    sessionPassword = nueva;
    try {
      var P = window.Capacitor.Plugins;
      if (P && P.NativeBiometric && await bioHasStored()) await P.NativeBiometric.setCredentials({ username: cloudUser.email, password: nueva, server: BIO_SERVER });
    } catch (e) {}
    showToast('Contraseña cambiada.');
    document.getElementById('btnPassCancel').click();
  }).catch(function (er) {
    showToast((er && (er.code === 'auth/invalid-credential' || er.code === 'auth/wrong-password')) ? 'La contraseña actual no es correcta.' : 'No se pudo cambiar la contraseña. Revisa tu conexión.');
  });
});
document.getElementById('btnLogout').addEventListener('click', function () {
  stopEquipo();
  if (cloudUnsub) { cloudUnsub(); cloudUnsub = null; }
  if (cloudDetectadosUnsub) { cloudDetectadosUnsub(); cloudDetectadosUnsub = null; }
  if (cloudMantUnsub) { cloudMantUnsub(); cloudMantUnsub = null; }
  if (cloudUserUnsub) { cloudUserUnsub(); cloudUserUnsub = null; }
  mantenimientos = [];
  cloudUser = null; cloudRole = null; sessionPassword = null;
  showVista('inicio');
  if (window.Cloud) window.Cloud.signOut();
});
document.getElementById('btnAiGuardar').addEventListener('click', function () {
  var k = document.getElementById('fAiKey').value.trim();
  if (!k) { showToast('Pega primero tu clave de Google AI Studio.'); return; }
  window.Cloud.setAiKey(k).then(function () { aiKey = k; document.getElementById('fAiKey').value = ''; refreshAiStatus(); }).catch(function () { showToast('No se pudo guardar la clave. Revisa tu conexión.'); });
});
document.getElementById('btnAiQuitar').addEventListener('click', function () {
  // Confirmación inline (251): solo con Sí se quita la clave de la IA.
  showConfirm('¿Quitar la clave de la IA? La IA dejará de funcionar en todos los teléfonos.').then(function (ok) {
    if (!ok) return;
    window.Cloud.setAiKey('').then(function () { aiKey = ''; refreshAiStatus(); }).catch(function () { showToast('No se pudo quitar la clave. Revisa tu conexión.'); });
  });
});
document.getElementById('btnAiGuardarDs').addEventListener('click', function () {
  var k = document.getElementById('fAiKeyDs').value.trim();
  if (!k) { showToast('Pega primero tu clave de DeepSeek.'); return; }
  window.Cloud.setDeepseekKey(k).then(function () { aiKeyDs = k; document.getElementById('fAiKeyDs').value = ''; refreshAiStatus(); }).catch(function () { showToast('No se pudo guardar la clave. Revisa tu conexión.'); });
});
document.getElementById('btnAiQuitarDs').addEventListener('click', function () {
  // Confirmación inline (251): solo con Sí se quita la clave de DeepSeek.
  showConfirm('¿Quitar la clave de DeepSeek? Si Gemini falla, la IA dejará de tener respaldo.').then(function (ok) {
    if (!ok) return;
    window.Cloud.setDeepseekKey('').then(function () { aiKeyDs = ''; refreshAiStatus(); }).catch(function () { showToast('No se pudo quitar la clave. Revisa tu conexión.'); });
  });
});
document.getElementById('btnUserAdd').addEventListener('click', function () {
  var nombre = document.getElementById('newUserNombre').value.trim();
  var usuario = document.getElementById('newUserUsuario').value.trim().toLowerCase();
  var email = document.getElementById('newUserEmail').value.trim();
  var pass = document.getElementById('newUserPass').value;
  var rol = document.getElementById('newUserRol').value;
  if (!nombre || !usuario || pass.length < 6) { showToast('Escribe nombre, usuario y una contraseña de al menos 6 caracteres.'); return; }
  if (!/^[a-z0-9._-]+$/.test(usuario)) { showToast('El usuario solo puede tener letras, números, puntos, guiones y guion bajo, sin espacios.'); return; }
  if (email && email.indexOf('@') === -1) { showToast('El correo no es válido.'); return; }
  var authEmail = email || (usuario + '@checklist.local');
  window.Cloud.createUserByAdmin({ email: authEmail, password: pass, nombre: nombre, usuario: usuario, rol: rol }).then(function () {
    document.getElementById('newUserNombre').value = '';
    document.getElementById('newUserUsuario').value = '';
    document.getElementById('newUserEmail').value = '';
    document.getElementById('newUserPass').value = '';
    renderUsuarios();
  }).catch(function (er) {
    showToast((er && er.code === 'auth/email-already-in-use') ? 'Ese usuario o correo ya está registrado.' : 'No se pudo crear el usuario.');
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
  var blk = t.closest('[data-user-mantblock]');
  if (!tog && !rol && !del && !unl && !pas && !edt && !blk) return;
  var uid = (tog || rol || del || unl || pas || edt || blk).getAttribute(tog ? 'data-user-toggle' : rol ? 'data-user-role' : del ? 'data-user-del' : unl ? 'data-user-unlock' : pas ? 'data-user-pass' : edt ? 'data-user-edit' : 'data-user-mantblock');
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
  if (uid === cloudUser.uid) { showToast('No puedes cambiar tu propio usuario desde aquí.'); return; }
  if (blk) {
    // (254) Bloqueo de Mantenimientos: no desactiva al usuario, solo le
    // cierra Mantenimientos; un admin nunca se bloquea (ni a sí mismo).
    if (u.rol === 'admin') { showToast('No se puede bloquear a un administrador.'); return; }
    window.Cloud.setMantBloqueado(uid, !u.mantBloqueado).then(renderUsuarios).catch(function () { showToast('No se pudo cambiar el acceso a Mantenimientos.'); });
    return;
  }
  if (unl) {
    window.Cloud.unlockUser(uid).then(renderUsuarios).catch(function () { showToast('No se pudo desbloquear la cuenta.'); });
    return;
  }
  if (pas) {
    // Contraseña nueva con modal inline (251): el prompt nativo es otro
    // diálogo nativo y se elimina junto con los demás; Cancelar devuelve
    // null igual que antes y la contraseña corta avisa con toast.
    showPrompt('Nueva contraseña para ' + (u.nombre || u.email) + ' (mínimo 6 caracteres):').then(function (np) {
      if (np === null) return;
      if (np.length < 6) { showToast('La contraseña debe tener al menos 6 caracteres.'); return; }
      window.Cloud.adminResetPassword({ uid: uid, usuario: u.usuario || '', email: u.email, nombre: u.nombre || '', rol: u.rol || 'usuario', newPassword: np }).then(function () { showToast('Contraseña cambiada para ' + (u.nombre || u.email) + '.'); renderUsuarios(); }).catch(function () { showToast('No se pudo cambiar la contraseña.'); });
    });
    return;
  }
  if (del) {
    // Confirmación inline (251): solo con Sí se elimina el usuario.
    showConfirm('¿Eliminar a ' + (u.nombre || u.email) + '? Ya no podrá entrar a la app.').then(function (ok) {
      if (!ok) return;
      window.Cloud.deleteUserByAdmin(uid, u.usuario || '').then(renderUsuarios).catch(function () { showToast('No se pudo eliminar el usuario.'); });
    });
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
  if (!nombre || !usuario) { showToast('Escribe el nombre y el usuario.'); return; }
  if (!/^[a-z0-9._-]+$/.test(usuario)) { showToast('El usuario solo puede tener letras, números, puntos, guiones y guion bajo, sin espacios.'); return; }
  if (email && email.indexOf('@') === -1) { showToast('El correo no es válido.'); return; }
  window.Cloud.adminUpdateUser(uid, window._editUserOld || '', { nombre: nombre, usuario: usuario, email: email }).then(function () {
    document.getElementById('userEditBox').hidden = true;
    window._editUserUid = null;
    renderUsuarios();
  }).catch(function (er) {
    showToast((er && er.code === 'auth/email-already-in-use') ? 'Ese usuario ya está registrado por otro.' : 'No se pudo guardar los cambios.');
  });
});
document.getElementById('btnReportar').addEventListener('click', function () {
  window.location.href = 'mailto:gerardo.cruzhz@linux.com?subject=' + encodeURIComponent('Reporte de problema - Checklist de Soporte 255') + '&body=' + encodeURIComponent('Describe el problema:\n\n\nVersión de la app: 255');
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
