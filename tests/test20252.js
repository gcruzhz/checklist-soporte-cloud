// Harness de pruebas node para Checklist de Soporte (nube).
// Archivo auto-contenido: el harness es todo lo que hay antes de la línea
// `eval(SRC);` (marcada con >>> EVAL). Para la siguiente versión, copiar
// este archivo y cambiar checklist20250.js por el nuevo extraído.
// Para probar la migración, sembrar localStorage ANTES de la línea eval.
const fs = require('fs');
const SRC = fs.readFileSync(__dirname + '/checklist20252.js', 'utf8');

function makeEl(id) {
  const el = {
    id: id || '', _h: {}, hidden: false, value: '', textContent: '', innerHTML: '',
    checked: false, disabled: false, style: {}, dataset: {}, files: [],
    classList: { _s: new Set(),
      add(c) { this._s.add(c); }, remove(c) { this._s.delete(c); },
      toggle(c, f) { if (f === undefined) f = !this._s.has(c); f ? this._s.add(c) : this._s.delete(c); },
      contains(c) { return this._s.has(c); } },
    addEventListener(ev, fn) { (this._h[ev] = this._h[ev] || []).push(fn); },
    removeEventListener() {},
    getAttribute(a) { return ('_attr_' + a) in this ? this['_attr_' + a] : null; },
    setAttribute(a, v) { this['_attr_' + a] = v; },
    hasAttribute(a) { return ('_attr_' + a) in this; },
    closest() { return null; },
    querySelector() { return makeEl(''); },
    querySelectorAll() { return []; },
    appendChild(c) { return c; },
    remove() {}, click() {}, focus() {}, select() {},
    getContext() { return null; },
  };
  return el;
}
const els = {};
global.localStorage = { _d: {}, getItem(k) { return this._d[k] || null; }, setItem(k, v) { this._d[k] = v; }, removeItem(k) { delete this._d[k]; } };
global.document = {
  getElementById(id) { if (!els[id]) els[id] = makeEl(id); return els[id]; },
  querySelector() { return makeEl(''); },
  querySelectorAll() { return []; },
  createElement() { return makeEl(''); },
  addEventListener() {},
  body: makeEl('body'),
  documentElement: makeEl('html'),
};
global.window = global;
global.Cloud = {
  signIn: async () => ({ uid: 'u1', email: 't@checklist.local', nombre: 'Test' }),
  signOut: async () => {}, listUsers: async () => [], listLoginLocks: async () => [],
  createUser: async () => ({}), deleteUser: async () => {}, setUserActive: async () => {},
  adminResetPassword: async () => {}, changePassword: async () => {},
  sendPasswordReset: async () => {}, recordLoginFailure: async () => 0,
  resolveEmail: async (id) => id + '@checklist.local',
  subscribeRenta: () => () => {}, saveRenta: async () => {}, deleteRenta: async () => {},
};
global.navigator = {};
global.location = { reload() {}, href: '' };
global.scrollTo = function () {};
// 2.4.0: la app ya no usa diálogos nativos; si alguno quedara, el test
// debe fallar en voz alta en vez de tragarlo con un stub silencioso.
global.alert = (m) => { throw new Error('alert() nativo llamado: ' + m); };
global.confirm = () => { throw new Error('confirm() nativo llamado'); };
global.prompt = () => { throw new Error('prompt() nativo llamado'); };
global.Blob = global.Blob || class Blob { constructor(parts) { this.parts = parts; } };
global.URL = global.URL || {};
if (!global.URL.createObjectURL) global.URL.createObjectURL = () => 'blob:x';
if (!global.URL.revokeObjectURL) global.URL.revokeObjectURL = () => {};

const sleep = (ms) => new Promise(r => setTimeout(r, ms));
function mkPrep(over) {
  return Object.assign({ id: 'p1', createdAt: Date.now(), deliveredAt: null, readyAt: null, checks: {}, extraItems: [], reasignaciones: [],
    equipo: { tipo: 'Laptop', marca: 'Dell', modelo: 'Inspiron 3501', serie: 'S1', inventario: '100' },
    usuario: { nombre: 'Ana', area: 'Sistemas', correo: '' }, tecnico: 'Test User', tecnicoUid: 'u1' }, over || {});
}
function fakeClick(attr, id, val) {
  const t = { classList: { contains() { return false; } },
    closest(sel) {
      if (sel === '[data-prep]') return { getAttribute() { return 'p1'; } };
      return sel === '[' + attr + ']' ? { getAttribute(a) { return a === 'data-value' ? val : id; } } : null;
    },
    hasAttribute(a) { return a === attr; },
    getAttribute(a) { return a === 'data-choice' ? id : a === 'data-value' ? val : a === 'data-prep' ? 'p1' : null; } };
  els['list']._h.click[0]({ target: t });
}
function doLogin(role) {
  cloudUser = { uid: 'u1', email: 'test@checklist.local', nombre: 'Test User' };
  cloudRole = role || 'usuario';
  applyRoleUI();
  els['loginView'].hidden = true;
  els['mainApp'].hidden = false;
}
const entered = () => els['loginView'].hidden === true && els['mainApp'].hidden === false;

// Sembrar la plantilla 2.0.15 (como la tendría un teléfono ya instalado) ANTES del eval.
const TPL2015 = [
  { id: 't1', group: 'hardware', text: 'Equipo enciende y sin daños físicos' },
  { id: 't2', group: 'hardware', text: 'Teclado, pantalla y puertos funcionando' },
  { id: 't3', group: 'hardware', text: 'Batería y cargador en buen estado' },
  { id: 't4', group: 'hardware', text: 'Etiqueta de inventario y número de serie registrados' },
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
  { id: 't14', group: 'datos', text: 'Cuenta de red creada' },
  { id: 't15', group: 'datos', text: 'Contraseña inicial entregada al usuario' },
  { id: 't16', group: 'datos', text: 'Archivos y perfil del usuario migrados' },
  { id: 't17', group: 'datos', text: 'Firma de resguardo recabada' },
  { id: 'idXYZ', group: 'software', text: 'Punto personal del analista' },
];
global.localStorage._d['checklist-soporte-v1'] = JSON.stringify({ template: TPL2015, templateVersion: 2, preparations: [] });

// >>> EVAL
eval(SRC);

// Helpers 2.4.0 para los tests del toast y los modales inline.
function toastTxt() { return document.getElementById('toast').textContent || ''; }
function answerConfirm(yes) {
  var b = document.getElementById(yes ? 'confirmYes' : 'confirmNo');
  if (b && typeof b.onclick === 'function') b.onclick();
}
function answerPrompt(value) {
  if (value === null) {
    var c = document.getElementById('promptCancel');
    if (c && typeof c.onclick === 'function') c.onclick();
  } else {
    document.getElementById('promptInput').value = value;
    var o = document.getElementById('promptOk');
    if (o && typeof o.onclick === 'function') o.onclick();
  }
}

(async () => {
  await sleep(50);
  const html = fs.readFileSync('/home/hatch/workspace/android/checklist-cloud/www/index.html', 'utf8');
  const dt = defaultTemplate();
  console.log('AM0) versión 2.5.2:', html.includes('Versión 2.5.2'), '| sin 2.5.0:', !html.includes('Versión 2.5.0'), '| sin Cuenta de red creada:', !dt.some(t => t.text.includes('Cuenta de red')), '| t26 Limpieza solo reasignación:', !!dt.find(t => t.id === 't26' && t.reassignOnly && t.text === 'Limpieza física del equipo'));
  // V1: migración de la plantilla 2.0.15 guardada.
  const ids = state.template.map(t => t.id);
  console.log('W1) migración: sin t14:', !ids.includes('t14'), '| con t26:', ids.includes('t26'), '| punto personal conservado:', ids.includes('idXYZ'), '| templateVersion 3:', state.templateVersion === 3);
  // V2: la limpieza solo aparece en equipos reasignados.
  const pNew = mkPrep();
  const pRe = mkPrep({ id: 'p2', reasignaciones: [{ de: 'Ana', a: 'Luis', fecha: Date.now(), analista: 'Juan' }] });
  console.log('W2) equipo nuevo: sin limpieza:', !allItems(pNew).some(x => x.id === 't26'), '| equipo reasignado: con limpieza:', allItems(pRe).some(x => x.id === 't26' && x.group === 'hardware'));
  // V3: la limpieza cuenta para el progreso solo en reasignados.
  const reqRe = requiredItems(pRe);
  const allDoneRe = {}; reqRe.forEach(it => allDoneRe[it.id] = true);
  const pReFull = mkPrep({ id: 'p2', reasignaciones: [{ de: 'Ana', a: 'Luis', fecha: Date.now(), analista: 'Juan' }], checks: allDoneRe });
  const pReNoLimp = mkPrep({ id: 'p2', reasignaciones: [{ de: 'Ana', a: 'Luis', fecha: Date.now(), analista: 'Juan' }], checks: Object.assign({}, allDoneRe, { t26: false }) });
  console.log('W3) reasignado con limpieza hecha = 100%:', progress(pReFull) === 100, '| reasignado sin limpieza < 100%:', progress(pReNoLimp) < 100, '| nuevo con sus obligatorios = 100%:', progress(mkPrep({ checks: (() => { const c = {}; requiredItems(pNew).forEach(it => c[it.id] = true); return c; })() })) === 100);
  // V4: PDF / Compartir, Reasignar y Eliminar solo para el admin.
  const pEnt = mkPrep({ deliveredAt: Date.now() - 86400000, readyAt: Date.now() - 2 * 86400000 });
  cloudRole = 'usuario';
  const cardU = cardHtml(pEnt);
  cloudRole = 'admin';
  const cardA = cardHtml(pEnt);
  console.log('W4) usuario: sin PDF:', !cardU.includes('data-pdf'), '| sin Reasignar:', !cardU.includes('data-reassign'), '| sin Eliminar:', !cardU.includes('data-del-prep'), '| pero con Excel:', cardU.includes('data-xlsx'), '| admin: con los tres:', cardA.includes('data-pdf') && cardA.includes('data-reassign') && cardA.includes('data-del-prep'));
  // W5: el botón grande Reasignar Equipo lo ven todos (solo Usuarios sigue siendo admin).
  document.getElementById('viewUsuarios').hidden = true;
  cloudRole = 'usuario'; applyRoleUI();
  const bigU = document.getElementById('btnShowRe').hidden === false && document.getElementById('tabUsuarios').hidden === true;
  cloudRole = 'admin'; applyRoleUI();
  const bigA = document.getElementById('btnShowRe').hidden === false && document.getElementById('tabUsuarios').hidden === false;
  console.log('W5) usuario: botón grande visible:', bigU, '| admin: visible:', bigA);
  // W6: un usuario normal SÍ puede guardar una reasignación con el botón grande.
  cloudRole = 'usuario';
  const nBefore = state.preparations.length;
  document.getElementById('fReEquipo').value = '__nuevo__'; document.getElementById('fReA').value = 'Luis'; document.getElementById('fReDe').value = 'Ana';
  document.getElementById('fReTipo').value = 'Laptop'; document.getElementById('fReMarca').value = 'Dell'; document.getElementById('fReModelo').value = 'Latitude'; document.getElementById('fReSerie').value = 'S9'; document.getElementById('fReInv').value = '999';
  document.getElementById('btnReGuardar')._h.click[0]();
  const created = state.preparations[state.preparations.length - 1];
  console.log('W6) usuario: crea el equipo reasignado:', state.preparations.length === nBefore + 1 && !!created && created.reasignaciones.length === 1, '| y su checklist trae la limpieza:', !!created && allItems(created).some(x => x.id === 't26'));
  // V7: el editor de plantilla marca el punto solo-reasignación.
  renderTemplate();
  console.log('W7) editor: marca (solo reasignación):', document.getElementById('tplList').innerHTML.includes('solo reasignación'), '| sin Cuenta de red:', !document.getElementById('tplList').innerHTML.includes('Cuenta de red'));

  // Y0b: firebase.js y reglas traen presencia y chat.
  const fb = fs.readFileSync('/home/hatch/workspace/android/checklist-cloud/www/cloud/firebase.js', 'utf8');
  const rules = fs.readFileSync('/home/hatch/workspace/android/checklist-cloud/firestore.rules', 'utf8');
  console.log('Y0b) firebase.js: heartbeat/subscribePresence/clearPresence/subscribeChat/sendChat:', ['heartbeat', 'subscribePresence', 'clearPresence', 'subscribeChat', 'sendChat'].every(f => fb.includes(f)), '| reglas: presencia y chat:', rules.includes('match /presence/{uid}') && rules.includes('match /chat/{id}'));
  console.log('AA0) nota de sincronización y chat individual en el HTML:', html.includes('se sincronizan entre todos los teléfonos') && html.includes('id="dmList"') && html.includes('id="dmBox"') && html.includes('id="dmChatBox"') && html.includes('id="btnDmSend"'));
  console.log('AA0b) firebase.js: preparations + dm:', ['subscribePreparations', 'upsertPrep', 'deletePrep', 'getAllPreparations', 'subscribeDm', 'sendDm'].every(f => fb.includes(f)), '| pruneChat limpia ambos chats:', fb.includes("['chat', 'dm']"), '| reglas: preparations y dm:', rules.includes('match /preparations/{id}') && rules.includes('match /dm/{id}'));
  console.log('Z0b) pruneChat en firebase.js y borrado a 24 h en reglas:', fb.includes('pruneChat') && rules.includes("duration.value(24, 'h')"), '| aviso de opción en el HTML:', html.includes('choice-hint') && html.includes('Elige una opción'), '| nota de 24 horas en Equipo:', html.includes('se borran solos después de 24 horas'));
  // Y1: timeAgo.
  const now = Date.now();
  console.log('Y1) timeAgo: ahora:', timeAgo(now) === 'hace un momento', '| 5 min:', timeAgo(now - 5 * 60000) === 'hace 5 min', '| 2 h:', timeAgo(now - 2 * 3600000) === 'hace 2 h', '| sin registro:', timeAgo(0) === 'sin registro');
  // Y2: lista de en línea.
  teamUsers = [
    { uid: 'uGer', nombre: 'Gerardo', rol: 'admin', email: 'gerardo@checklist.local' },
    { uid: 'uAxel', nombre: 'Axel Danyael Pérez Arredondo', rol: 'usuario', email: 'axel@checklist.local' },
    { uid: 'uAle', nombre: 'Alejandro', rol: 'usuario', email: 'alejandro@checklist.local' },
  ];
  cloudUser = { uid: 'uGer', email: 'gerardo@checklist.local', nombre: 'Gerardo' };
  cloudRole = 'admin';
  presenceList = [
    { uid: 'uGer', nombre: 'Gerardo', rol: 'admin', lastSeen: now },
    { uid: 'uAxel', nombre: 'Axel Danyael Pérez Arredondo', rol: 'usuario', lastSeen: now - 10 * 60000 },
  ];
  chatMessages = [];
  renderEquipo();
  const ol = document.getElementById('onlineList').innerHTML;
  console.log('Y2) en línea: Gerardo con punto verde y (tú):', ol.includes('dot on') && ol.includes('Gerardo') && ol.includes('(tú)') && ol.includes('en línea'), '| Axel hace 10 min:', ol.includes('hace 10 min'), '| Alejandro sin registro:', ol.includes('sin registro'));
  // Y3: el umbral de 3 minutos.
  presenceList = [{ uid: 'uGer', nombre: 'Gerardo', rol: 'admin', lastSeen: now - 5 * 60000 }];
  renderEquipo();
  console.log('Y3) latido de hace 5 min ya no es en línea:', !document.getElementById('onlineList').innerHTML.includes('en línea'));
  // Y4: chat.
  chatMessages = [
    { uid: 'uAxel', nombre: 'Axel Danyael Pérez Arredondo', texto: 'Hola, ¿alguien tiene el cargador?', createdAt: now - 3600000 },
    { uid: 'uGer', nombre: 'Gerardo', texto: 'Yo lo tengo', createdAt: now - 60000 },
  ];
  renderEquipo();
  const cb = document.getElementById('chatBox').innerHTML;
  console.log('Y4) chat: muestra los dos mensajes:', cb.includes('cargador') && cb.includes('Yo lo tengo'), '| el mío marcado:', cb.includes('msg mine'), '| con nombres:', cb.includes('Axel') && cb.includes('Gerardo'));
  // Y5: enviar mensaje.
  CLOUD_ENABLED = true;
  const sent = [];
  global.Cloud.sendChat = async function (t, n) { sent.push([t, n]); };
  document.getElementById('chatInput').value = 'Hola equipo';
  document.getElementById('btnChatSend')._h.click[0]();
  const sentOk = sent.length === 1 && sent[0][0] === 'Hola equipo' && sent[0][1] === 'Gerardo' && document.getElementById('chatInput').value === '';
  document.getElementById('chatInput').value = '   ';
  document.getElementById('btnChatSend')._h.click[0]();
  console.log('Y5) enviar: manda el texto con mi nombre y limpia:', sentOk, '| vacío no se manda:', sent.length === 1);
  // Y6: start/stop Equipo.
  const hb = [], unsubs = [];
  global.Cloud.heartbeat = function (n, r) { hb.push([n, r]); };
  global.Cloud.subscribePresence = function (f) { unsubs.push('presence'); return function () { unsubs.push('unsub-presence'); }; };
  global.Cloud.subscribeChat = function (f) { unsubs.push('chat'); return function () { unsubs.push('unsub-chat'); }; };
  global.Cloud.subscribeDm = function (f) { unsubs.push('dm'); return function () { unsubs.push('unsub-dm'); }; };
  global.Cloud.subscribePreparations = function (f) { unsubs.push('prep'); return function () { unsubs.push('unsub-prep'); }; };
  global.Cloud.clearPresence = function () { unsubs.push('clear'); };
  global.Cloud.pruneChat = function () { unsubs.push('prune'); };
  global.Cloud.listUsers = async function () { return teamUsers; };
  cloudUser = { uid: 'uGer', email: 'gerardo@checklist.local', nombre: 'Gerardo' };
  cloudRole = 'admin';
  startEquipo();
  const started = hb.length === 1 && hb[0][0] === 'Gerardo' && heartbeatTimer !== null && unsubs.includes('presence') && unsubs.includes('chat');
  stopEquipo();
  console.log('Y6) start: latido inmediato + suscripciones:', started, '| stop: desuscribe, limpia presencia y para el temporizador:', heartbeatTimer === null && unsubs.includes('unsub-presence') && unsubs.includes('unsub-chat') && unsubs.includes('clear'));
  console.log('Z4) startEquipo limpia el chat viejo:', unsubs.includes('prune'));
  // Y7: la vista Equipo se abre desde las pestañas.
  showVista('equipo');
  console.log('Y7) vista Equipo visible y Preparar oculta:', document.getElementById('viewEquipo').hidden === false && document.getElementById('viewPreparar').hidden === true);

  // Z1: el 95% era Office sin elegir (todas las casillas marcadas, sin opción).
  const pZ = mkPrep();
  const reqZ = requiredItems(pZ);
  const cz = {};
  reqZ.forEach(it => { if (it.id !== 't8') cz[it.id] = true; });
  console.log('Z1) todas las casillas sin Office -> 95%:', progress(mkPrep({ checks: cz })) === 95, '| + Office 365 -> 100%:', progress(mkPrep({ checks: Object.assign({}, cz, { t8: 'Office 365' }) })) === 100);
  // Z2: lo mismo en un equipo reasignado.
  const reZ = [{ de: 'A', a: 'B', fecha: Date.now(), analista: 'X' }];
  const reqReZ = requiredItems(mkPrep({ reasignaciones: reZ }));
  const czRe = {};
  reqReZ.forEach(it => { if (it.id !== 't8') czRe[it.id] = true; });
  console.log('Z2) reasignado sin Office -> 95%:', progress(mkPrep({ reasignaciones: reZ, checks: czRe })) === 95, '| + LibreOffice -> 100%:', progress(mkPrep({ reasignaciones: reZ, checks: Object.assign({}, czRe, { t8: 'LibreOffice' }) })) === 100);
  // Z3: la tarjeta avisa cuando falta elegir Office.
  const cardNoOff = cardHtml(mkPrep({ checks: cz }));
  const cardOff = cardHtml(mkPrep({ checks: Object.assign({}, cz, { t8: 'Office 365' }) }));
  console.log('Z3) sin Office la tarjeta avisa:', cardNoOff.includes('Elige una opción'), '| con Office ya no avisa:', !cardOff.includes('Elige una opción'));
  // Z5: la nota del chat dice lo de las 24 horas.
  console.log('Z5) nota de Equipo con 24 horas:', html.includes('se borran solos después de 24 horas'));

  // AA1: Nuevo equipo se sube a la nube al guardarlo.
  document.getElementById('loginView');
  document.getElementById('mainApp');
  doLogin('usuario');
  var upserted = [];
  var deletedPrep = [];
  global.Cloud.upsertPrep = async function (d) { upserted.push(d); };
  global.Cloud.deletePrep = async function (id) { deletedPrep.push(id); };
  document.getElementById('fTipo').value = 'Laptop';
  document.getElementById('fMarca').value = 'Dell';
  document.getElementById('fModelo').value = 'Inspiron 3501';
  document.getElementById('fSerie').value = 'S1';
  document.getElementById('fInv').value = '100';
  document.getElementById('fUser').value = 'Ana';
  document.getElementById('fArea').value = 'Sistemas';
  document.getElementById('fCorreo').value = '';
  document.getElementById('fTec').value = 'Test User';
  document.getElementById('btnAdd')._h.click[0]();
  console.log('AA1) nuevo equipo se sube a la nube:', upserted.length === 1 && upserted[0].equipo.modelo === 'Inspiron 3501' && upserted[0].tecnico === 'Test User');
  // AA2: marcar una casilla sube el equipo.
  state.preparations.push(mkPrep());
  upserted.length = 0;
  var t2 = { hasAttribute: function (a) { return a === 'data-check'; }, getAttribute: function (a) { return a === 'data-check' ? 't1' : a === 'data-prep' ? 'p1' : null; }, checked: true };
  document.getElementById('list')._h.change[0]({ target: t2 });
  console.log('AA2) marcar casilla sube el equipo:', upserted.length === 1 && upserted[0].checks.t1 === true);
  // AA3: elegir Office sube el equipo.
  upserted.length = 0;
  fakeClick('data-choice', 't8', 'Office 365');
  console.log('AA3) elegir Office sube el equipo:', upserted.length === 1 && upserted[0].checks.t8 === 'Office 365');
  // AA4 (ACTUALIZADO en esta versión, cambio intencional): 'Entregado' con
  // avance <100% ya NO entrega directo: abre el panel de confirmación
  // (ver AT6); aquí se confirma con 'Entregar así'. Y 'Reabrir' de un
  // entregado ahora limpia deliveredAt Y readyAt: vuelve a preparación,
  // no a listo (antes, serie P de 2.0.10, mantenía readyAt).
  upserted.length = 0;
  fakeClick('data-ready', 'p1');
  var listoOk = upserted.length === 1 && !!upserted[0].readyAt;
  upserted.length = 0;
  fakeClick('data-deliver', 'p1');
  var panelOk = window._deliverConfirmFor === 'p1' && upserted.length === 0;
  var pAA4 = state.preparations.find(function (p) { return p.id === 'p1'; });
  var noEntrOk = !!pAA4 && !pAA4.deliveredAt;
  fakeClick('data-deliver-confirm', 'p1');
  var entrOk = upserted.length === 1 && !!upserted[0].deliveredAt;
  upserted.length = 0;
  fakeClick('data-reopen', 'p1');
  var reabOk = upserted.length === 1 && upserted[0].deliveredAt === null && upserted[0].readyAt === null;
  var pAA4b = state.preparations.find(function (p) { return p.id === 'p1'; });
  var reabPrepOk = !!pAA4b && statusOf(pAA4b) === 'preparacion' && filterStatus === 'preparacion';
  console.log('AA4) Listo sube:', listoOk, '| Entregado <100% abre el panel sin entregar:', panelOk && noEntrOk, '| Entregar así sube:', entrOk, '| Reabrir sube y limpia readyAt:', reabOk, '| Reabrir vuelve a preparación:', reabPrepOk);
  // AA5: reasignación desde la tarjeta sube el equipo.
  document.getElementById('reDe').value = 'Ana';
  document.getElementById('reA').value = 'Luis';
  upserted.length = 0;
  fakeClick('data-save-reassign', 'p1');
  var p5 = state.preparations.find(function (p) { return p.id === 'p1'; });
  console.log('AA5) reasignación sube el equipo:', upserted.length === 1 && p5.usuario.nombre === 'Luis' && p5.reasignaciones.length === 1);
  // AA6: eliminar abre el modal inline y borra solo con Sí.
  fakeClick('data-del-prep', 'p1');
  var aa6modal = document.getElementById('confirmModal').hidden === false && document.getElementById('confirmMsg').textContent === '¿Eliminar este equipo y su checklist?';
  answerConfirm(true);
  await sleep(20);
  console.log('AA6) eliminar abre el modal con su pregunta:', aa6modal, '| con Sí borra en la nube:', deletedPrep.indexOf('p1') !== -1 && !state.preparations.some(function (p) { return p.id === 'p1'; }));
  // AA7: al recibir la lista de la nube, la foto local se conserva.
  state.preparations = [mkPrep({ equipo: { tipo: 'Laptop', marca: 'Dell', modelo: 'X', serie: 'S', inventario: '1', fotoSerie: 'data:image/jpeg;base64,LOCAL' } })];
  var merged = mergePrepsWithLocal([{ id: 'p1', createdAt: Date.now(), checks: { t1: true }, equipo: { tipo: 'Laptop', marca: 'Dell', modelo: 'X', serie: 'S', inventario: '1' }, usuario: { nombre: 'Ana' }, tecnico: 'Test User' }]);
  console.log('AA7) la foto local se conserva al llegar la nube:', merged[0].equipo.fotoSerie === 'data:image/jpeg;base64,LOCAL' && merged[0].checks.t1 === true);
  // AA8: la foto gigante no viaja, la chica sí.
  var big = prepToCloudDoc(mkPrep({ equipo: { tipo: 'Laptop', marca: 'Dell', modelo: 'X', serie: 'S', inventario: '1', fotoSerie: 'x'.repeat(800000) } }));
  var small = prepToCloudDoc(mkPrep({ equipo: { tipo: 'Laptop', marca: 'Dell', modelo: 'X', serie: 'S', inventario: '1', fotoSerie: 'data:image/jpeg;base64,AAA' } }));
  console.log('AA8) foto gigante no viaja:', big.equipo.fotoSerie === null, '| foto chica sí viaja:', small.equipo.fotoSerie === 'data:image/jpeg;base64,AAA');
  // AA9: migración sube los equipos locales que faltan en la nube, una sola vez.
  var migUp = [];
  global.Cloud.getAllPreparations = async function () { return []; };
  global.Cloud.upsertPrep = async function (d) { migUp.push(d); };
  localStorage.setItem('checklist-soporte-migrado-preps-v1:u1', '');
  state.preparations = [mkPrep({ id: 'm1' }), mkPrep({ id: 'm2' })];
  await migrateLocalPreparations();
  var firstRun = migUp.length;
  await migrateLocalPreparations();
  console.log('AA9) migración sube los locales que faltan:', firstRun === 2, '| segunda vez ya no repite:', migUp.length === 2);
  // AB1: mensaje individual se envía al compañero con mi nombre.
  var sentDm = [];
  global.Cloud.sendDm = async function (to, t, n) { sentDm.push([to, t, n]); };
  teamUsers = [{ uid: 'u1', nombre: 'Test User', rol: 'usuario' }, { uid: 'u2', nombre: 'Alejandro', rol: 'usuario' }, { uid: 'u3', nombre: 'Axel Danyael', rol: 'usuario' }];
  presenceList = [];
  chatMessages = [];
  dmPeer = 'u2';
  document.getElementById('dmInput').value = 'Hola Alejandro';
  sendDmMsg();
  var dmOk = sentDm.length === 1 && sentDm[0][0] === 'u2' && sentDm[0][1] === 'Hola Alejandro' && sentDm[0][2] === 'Test User' && document.getElementById('dmInput').value === '';
  document.getElementById('dmInput').value = '   ';
  sendDmMsg();
  console.log('AB1) mensaje individual al compañero con mi nombre:', dmOk, '| vacío no se envía:', sentDm.length === 1);
  // AB2: la conversación muestra solo los mensajes con ese compañero.
  dmMessages = [
    { id: 'd1', participants: ['u1', 'u2'], from: 'u2', nombre: 'Alejandro', texto: 'Hola', createdAt: Date.now() - 60000 },
    { id: 'd2', participants: ['u1', 'u2'], from: 'u1', nombre: 'Test User', texto: 'Qué tal', createdAt: Date.now() },
    { id: 'd3', participants: ['u1', 'u3'], from: 'u3', nombre: 'Axel Danyael', texto: 'Esto es con Axel', createdAt: Date.now() }
  ];
  dmPeer = 'u2';
  renderEquipo();
  var dmHtml = document.getElementById('dmChatBox').innerHTML;
  console.log('AB2) conversación solo con ese compañero:', dmHtml.indexOf('Hola') !== -1 && dmHtml.indexOf('Qué tal') !== -1 && dmHtml.indexOf('Esto es con Axel') === -1, '| el mío marcado:', dmHtml.indexOf('msg mine') !== -1);
  // AB3: la lista muestra a los demás, no a mí.
  dmPeer = null;
  dmMessages = [{ id: 'd1', participants: ['u1', 'u2'], from: 'u2', nombre: 'Alejandro', texto: 'Hola, ¿cómo va?', createdAt: Date.now() }];
  renderEquipo();
  var dmListHtml = document.getElementById('dmList').innerHTML;
  console.log('AB3) lista de chat individual sin mí y con los demás:', dmListHtml.indexOf('Alejandro') !== -1 && dmListHtml.indexOf('Axel Danyael') !== -1 && dmListHtml.indexOf('Test User') === -1);
  // AB4: tocar un compañero abre su conversación.
  dmPeer = null;
  document.getElementById('dmList')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-dm-user]' ? { getAttribute: function () { return 'u3'; } } : null; } } });
  console.log('AB4) tocar un compañero abre su conversación:', dmPeer === 'u3');
  // AB5: al entrar se suscribe al chat individual y a preparaciones; al salir se desuscribe.
  var unsubs2 = [];
  global.Cloud.heartbeat = function () {};
  global.Cloud.pruneChat = function () {};
  global.Cloud.subscribePresence = function () { unsubs2.push('presence'); return function () { unsubs2.push('unsub-presence'); }; };
  global.Cloud.subscribeChat = function () { unsubs2.push('chat'); return function () { unsubs2.push('unsub-chat'); }; };
  global.Cloud.subscribeDm = function () { unsubs2.push('dm'); return function () { unsubs2.push('unsub-dm'); }; };
  global.Cloud.clearPresence = function () {};
  global.Cloud.listUsers = async function () { return []; };
  startEquipo();
  var started2 = unsubs2.indexOf('dm') !== -1;
  stopEquipo();
  console.log('AB5) al entrar se suscribe al chat individual:', started2, '| al salir se desuscribe:', unsubs2.indexOf('unsub-dm') !== -1);
  // AB5b: al entrar (login), migra las preparaciones locales y se suscribe a ellas.
  var migUp2 = [];
  var prepCb2 = null;
  global.Cloud.getUserDoc = async function () { return { activo: true, rol: 'admin', nombre: 'Test User', email: 'test@checklist.local' }; };
  global.Cloud.isInitialized = async function () { return true; };
  global.Cloud.getAllRenta = async function () { return []; };
  global.Cloud.upsertRenta = async function () {};
  global.Cloud.getAllPreparations = async function () { return []; };
  global.Cloud.upsertPrep = async function (d) { migUp2.push(d); };
  global.Cloud.subscribeRenta = function () { return function () {}; };
  global.Cloud.subscribePreparations = function (cb) { prepCb2 = cb; return function () { unsubs2.push('unsub-prep'); }; };
  global.Cloud.subscribePresence = function () { return function () {}; };
  global.Cloud.subscribeChat = function () { return function () {}; };
  global.Cloud.subscribeDm = function () { return function () {}; };
  global.Cloud.heartbeat = function () {};
  global.Cloud.pruneChat = function () {};
  global.Cloud.clearPresence = function () {};
  global.Cloud.listUsers = async function () { return []; };
  localStorage.setItem('checklist-soporte-migrado-v2:u1', '1');
  localStorage.setItem('checklist-soporte-migrado-preps-v1:u1', '');
  state.preparations = [mkPrep({ id: 'm9' })];
  state.renta = [];
  await onAuthChanged({ uid: 'u1', email: 'test@checklist.local' });
  console.log('AB5b) al entrar migra las preparaciones locales:', migUp2.length === 1, '| y se suscribe a preparaciones:', typeof prepCb2 === 'function');

  // AC0b: funciones de borrado en firebase.js y botón en el HTML.
  console.log('AC0b) firebase.js: borrar mensajes:', fb.includes('deleteChatMessage') && fb.includes('deleteDmMessage'), '| botón de borrar en el HTML:', html.includes('data-del-chat') && html.includes('data-del-dm') && html.includes('msg-del'));
  // AC1: el admin ve el botón de borrar en el chat del equipo; el usuario no.
  cloudUser = { uid: 'u1', email: 'test@checklist.local', nombre: 'Test User' };
  cloudRole = 'admin';
  chatMessages = [{ id: 'm1', uid: 'u2', nombre: 'Alejandro', texto: 'Hola equipo', createdAt: Date.now() - 60000 }];
  dmMessages = [];
  dmPeer = null;
  teamUsers = [{ uid: 'u1', nombre: 'Test User', rol: 'usuario' }, { uid: 'u2', nombre: 'Alejandro', rol: 'usuario' }];
  presenceList = [];
  renderEquipo();
  var adminDel = document.getElementById('chatBox').innerHTML.indexOf('data-del-chat="m1"') !== -1;
  cloudRole = 'usuario';
  renderEquipo();
  var userNoDel = document.getElementById('chatBox').innerHTML.indexOf('data-del-chat') === -1;
  console.log('AC1) admin ve borrar en el chat del equipo:', adminDel, '| usuario no lo ve:', userNoDel);
  // AC2: lo mismo en el chat individual.
  cloudRole = 'admin';
  dmPeer = 'u2';
  dmMessages = [{ id: 'd1', participants: ['u1', 'u2'], from: 'u2', nombre: 'Alejandro', texto: 'Hola', createdAt: Date.now() }];
  renderEquipo();
  var adminDmDel = document.getElementById('dmChatBox').innerHTML.indexOf('data-del-dm="d1"') !== -1;
  cloudRole = 'usuario';
  renderEquipo();
  var userDmNoDel = document.getElementById('dmChatBox').innerHTML.indexOf('data-del-dm') === -1;
  console.log('AC2) admin ve borrar en el chat individual:', adminDmDel, '| usuario no lo ve:', userDmNoDel);
  // AC3: tocar borrar en el chat del equipo borra ese mensaje.
  var delChat = [];
  global.Cloud.deleteChatMessage = async function (id) { delChat.push(id); };
  document.getElementById('chatBox')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-del-chat]' ? { getAttribute: function () { return 'm1'; } } : null; } } });
  var ac3modal = document.getElementById('confirmModal').hidden === false && document.getElementById('confirmMsg').textContent === '¿Borrar este mensaje para todos?';
  answerConfirm(true);
  await sleep(20);
  console.log('AC3) borrar abre el modal con su pregunta:', ac3modal, '| con Sí borra el mensaje:', delChat.length === 1 && delChat[0] === 'm1');
  // AC4: tocar borrar en el chat individual borra ese mensaje.
  var delDm = [];
  global.Cloud.deleteDmMessage = async function (id) { delDm.push(id); };
  document.getElementById('dmChatBox')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-del-dm]' ? { getAttribute: function () { return 'd1'; } } : null; } } });
  var ac4modal = document.getElementById('confirmModal').hidden === false && document.getElementById('confirmMsg').textContent === '¿Borrar este mensaje para los dos?';
  answerConfirm(true);
  await sleep(20);
  console.log('AC4) borrar abre el modal con su pregunta:', ac4modal, '| con Sí borra el mensaje:', delDm.length === 1 && delDm[0] === 'd1');

  // AD0b: editar usuarios en firebase.js y en el HTML; descripción y animación de login.
  console.log('AD0b) firebase.js: adminUpdateUser:', fb.includes('adminUpdateUser'), '| descripción nueva:', html.includes('Ingresa con tu usuario para ver y registrar equipos'), '| animación de login:', html.includes('login-logo') && html.includes('loginFloat') && html.includes('loginIn'), '| panel de edición:', html.includes('id="userEditBox"') && html.includes('id="fEuNombre"') && html.includes('id="fEuUsuario"') && html.includes('id="fEuCorreo"') && html.includes('id="btnEuGuardar"') && html.includes('data-user-edit'));
  // AD1: tocar Editar abre el panel con los datos del usuario.
  cloudUser = { uid: 'u1', email: 'test@checklist.local', nombre: 'Test User' };
  cloudRole = 'admin';
  lastUsers = [{ uid: 'u2', nombre: 'Alejandro', usuario: 'alejandro', email: 'alejandro@x.com', rol: 'usuario', activo: true }];
  document.getElementById('userList')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-user-edit]' ? { getAttribute: function () { return 'u2'; } } : null; } } });
  console.log('AD1) Editar abre el panel con sus datos:', document.getElementById('userEditBox').hidden === false && document.getElementById('fEuNombre').value === 'Alejandro' && document.getElementById('fEuUsuario').value === 'alejandro' && document.getElementById('fEuCorreo').value === 'alejandro@x.com');
  // AD2: Guardar llama a adminUpdateUser con los datos nuevos y cierra el panel.
  var editCalls = [];
  global.Cloud.adminUpdateUser = async function (uid, oldU, data) { editCalls.push([uid, oldU, data]); };
  document.getElementById('fEuNombre').value = 'Alejandro Ruiz';
  document.getElementById('fEuUsuario').value = 'alejandror';
  document.getElementById('fEuCorreo').value = 'aruiz@x.com';
  document.getElementById('btnEuGuardar')._h.click[0]();
  await sleep(10);
  console.log('AD2) Guardar actualiza al usuario:', editCalls.length === 1 && editCalls[0][0] === 'u2' && editCalls[0][1] === 'alejandro' && editCalls[0][2].nombre === 'Alejandro Ruiz' && editCalls[0][2].usuario === 'alejandror' && editCalls[0][2].email === 'aruiz@x.com', '| cierra el panel:', document.getElementById('userEditBox').hidden === true);
  // AD3: validación — no guarda sin nombre, con usuario inválido ni con correo inválido.
  window._editUserUid = 'u2';
  document.getElementById('userEditBox').hidden = false;
  editCalls.length = 0;
  document.getElementById('fEuNombre').value = '';
  document.getElementById('fEuUsuario').value = 'alejandror';
  document.getElementById('fEuCorreo').value = 'aruiz@x.com';
  document.getElementById('btnEuGuardar')._h.click[0]();
  var noNombre = editCalls.length === 0;
  document.getElementById('fEuNombre').value = 'Alejandro Ruiz';
  document.getElementById('fEuUsuario').value = 'ale jandro';
  document.getElementById('btnEuGuardar')._h.click[0]();
  var malUsuario = editCalls.length === 0;
  document.getElementById('fEuUsuario').value = 'alejandror';
  document.getElementById('fEuCorreo').value = 'aruizsinarroba';
  document.getElementById('btnEuGuardar')._h.click[0]();
  var malCorreo = editCalls.length === 0;
  console.log('AD3) no guarda sin nombre:', noNombre, '| ni con usuario con espacios:', malUsuario, '| ni con correo sin @:', malCorreo);
  // AD4: si el usuario ya existe, no cierra el panel.
  global.Cloud.adminUpdateUser = async function () { var e = new Error('duplicate'); e.code = 'auth/email-already-in-use'; throw e; };
  document.getElementById('fEuNombre').value = 'Alejandro Ruiz';
  document.getElementById('fEuUsuario').value = 'otro';
  document.getElementById('fEuCorreo').value = 'aruiz@x.com';
  document.getElementById('btnEuGuardar')._h.click[0]();
  await sleep(10);
  console.log('AD4) usuario duplicado no cierra el panel:', document.getElementById('userEditBox').hidden === false);

  // AE0b: la interfaz nace oculta y el splash espera a que la app decida.
  console.log('AE0b) interfaz oculta por defecto:', html.includes('<header id="appHeader" hidden>') && html.includes('<main id="mainApp" hidden>'), '| splash con espera:', html.includes('function hideSplash') && html.includes('_authReady'));
  // AE1: en modo local (sin nube) la interfaz sí se muestra al arrancar.
  console.log('AE1) modo local muestra la interfaz:', document.getElementById('mainApp').hidden === false && document.getElementById('appHeader').hidden === false, '| y ya decidió:', _authReady === true);
  // AE2: en modo nube sin sesión, al arrancar se muestra el login, no la interfaz.
  var authCb = null;
  global.Cloud.init = async function () { return true; };
  global.Cloud.onAuth = function (cb) { authCb = cb; };
  global.Cloud.isInitialized = async function () { return true; };
  CLOUD_ENABLED = true;
  _authReady = false;
  await boot();
  var bootOk = document.getElementById('mainApp').hidden === true && document.getElementById('appHeader').hidden === true && document.getElementById('loginView').hidden === false;
  await authCb(null);
  console.log('AE2) sin sesión muestra el login, no la interfaz:', bootOk, '| y al confirmar que no hay sesión ya decidió:', _authReady === true && document.getElementById('loginView').hidden === false && document.getElementById('mainApp').hidden === true);
  // AE3: el splash no se quita hasta que la app decide.
  _authReady = false;
  hideSplash();
  var sigue = !document.getElementById('splash').classList.contains('hide');
  _authReady = true;
  hideSplash();
  console.log('AE3) el splash espera a que la app decida:', sigue, '| y se quita cuando ya decidió:', document.getElementById('splash').classList.contains('hide'));

  // AF0b: la IA está en el código (firebase.js + HTML + reglas).
  console.log('AF0b) firebase.js: getAiKey/setAiKey:', fb.includes('getAiKey') && fb.includes('setAiKey'), '| botones de IA:', html.includes('data-ai-falta') && html.includes('data-ai-wa') && html.includes('data-ai-danos'), '| panel de la clave:', html.includes('id="fAiKey"') && html.includes('id="btnAiGuardar"') && html.includes('id="aiKeyStatus"'), '| foto de daños:', html.includes('id="btnFotoDanos"') && html.includes('id="fotoDanosPreview"'), '| reglas config/ai:', rules.includes('match /config/ai') && rules.includes('isAdmin()'));
  // AF1: askAI llama a Gemini con la clave en el encabezado y devuelve el texto.
  var fetchCalls = [];
  global.fetch = async function (url, opts) {
    fetchCalls.push([url, opts]);
    return { ok: true, json: async function () { return { candidates: [{ content: { parts: [{ text: 'Falta instalar Office y configurar la VPN.' }] } }] }; } };
  };
  aiKey = 'CLAVE-PRUEBA';
  var ans = await askAI('¿Qué falta?');
  console.log('AF1) askAI llama a Gemini y devuelve el texto:', fetchCalls.length === 1 && fetchCalls[0][0] === 'https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent' && fetchCalls[0][1].headers['x-goog-api-key'] === 'CLAVE-PRUEBA' && JSON.parse(fetchCalls[0][1].body).contents[0].parts[0].text === '¿Qué falta?' && ans === 'Falta instalar Office y configurar la VPN.');
  // AF1b: con foto, la imagen viaja como inline_data.
  fetchCalls.length = 0;
  await askAI('Revisa daños', 'data:image/jpeg;base64,/9j/ABC');
  var body = JSON.parse(fetchCalls[0][1].body);
  console.log('AF1b) con foto manda inline_data:', body.contents[0].parts.length === 2 && body.contents[0].parts[1].inline_data.mime_type === 'image/jpeg' && body.contents[0].parts[1].inline_data.data === '/9j/ABC');
  // AF1c: sin clave no llama a la red.
  aiKey = '';
  fetchCalls.length = 0;
  var noKey = false;
  try { await askAI('hola'); } catch (e) { noKey = e.message === 'no-key'; }
  console.log('AF1c) sin clave no llama a la red:', noKey && fetchCalls.length === 0, '| y el aviso lo dice:', aiErrorText({ message: 'no-key' }).indexOf('Falta la clave') === 0);
  // AF2: ¿Qué falta? muestra la respuesta de la IA en la tarjeta.
  aiKey = 'CLAVE-PRUEBA';
  state.preparations = [mkPrep({ checks: { t1: true, t2: true } })];
  state.template = defaultTemplate();
  filterStatus = 'preparacion';
  render();
  global.fetch = async function () { return { ok: true, json: async function () { return { candidates: [{ content: { parts: [{ text: 'Falta Office y la VPN, en ese orden.' }] } }] }; } }; };
  fakeClick('data-ai-falta', 'p1');
  await sleep(10);
  console.log('AF2) ¿Qué falta? muestra la respuesta en la tarjeta:', (aiAnswers['p1'] || '').indexOf('Falta Office') === 0);
  // AF3: Revisar daños con IA guarda el resultado en el equipo de renta.
  cloudUser = { uid: 'u1', email: 'test@checklist.local', nombre: 'Test User' };
  state.renta = [{ id: 'r1', flujo: 'rec', tipo: 'Laptop', modelo: 'ProBook', inventario: '123', accesorios: {}, sinDanos: false, danos: '', obs: '', estado: 'recibido', fotoDanos: 'data:image/jpeg;base64,/9j/XYZ', danosIA: '' }];
  var upserts = [];
  global.Cloud.upsertRenta = async function (rec) { upserts.push(rec); };
  global.fetch = async function () { return { ok: true, json: async function () { return { candidates: [{ content: { parts: [{ text: 'Rayón en la tapa, sin daños en pantalla.' }] } }] }; } }; };
  document.getElementById('list-rec')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-ai-danos]' ? { getAttribute: function () { return 'r1'; }, hasAttribute: function (a) { return a === 'data-ai-danos'; } } : null; }, hasAttribute: function (a) { return a === 'data-ai-danos'; } } });
  await sleep(10);
  console.log('AF3) daños con IA se guardan en el equipo:', state.renta[0].danosIA.indexOf('Rayón en la tapa') === 0 && upserts.length === 1);
  // AF4: Resumen con IA comparte el texto que escribe la IA.
  var shared = [];
  global.navigator.share = async function (o) { shared.push(o.text); };
  global.fetch = async function () { return { ok: true, json: async function () { return { candidates: [{ content: { parts: [{ text: 'Hola, tu equipo ya está listo. ¡Gracias!' }] } }] }; } }; };
  fakeClick('data-ai-wa', 'p1');
  await sleep(10);
  console.log('AF4) resumen con IA se comparte por WhatsApp:', shared.length === 1 && shared[0].indexOf('tu equipo ya está listo') !== -1);
  // AF5: guardar la clave la registra y actualiza el estado.
  var savedKeys = [];
  global.Cloud.setAiKey = async function (k) { savedKeys.push(k); };
  document.getElementById('fAiKey').value = 'NUEVA-CLAVE';
  document.getElementById('btnAiGuardar')._h.click[0]();
  await sleep(10);
  console.log('AF5) guardar la clave la registra:', savedKeys.length === 1 && savedKeys[0] === 'NUEVA-CLAVE' && aiKey === 'NUEVA-CLAVE');

  // AF6: el botón de IA funciona con el botón real (sin data-prep en el DOM).
  aiKey = 'CLAVE-PRUEBA';
  aiBusy = false;
  delete aiAnswers['p1'];
  global.fetch = async function () { return { ok: true, json: async function () { return { candidates: [{ content: { parts: [{ text: 'Falta Office.' }] } }] }; } }; };
  document.getElementById('list')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-ai-falta]' ? { getAttribute: function () { return 'p1'; } } : null; }, hasAttribute: function (a) { return a === 'data-ai-falta'; } } });
  await sleep(10);
  console.log('AF6) ¿Qué falta? funciona con el botón real:', (aiAnswers['p1'] || '').indexOf('Falta Office') === 0);
  // AF6b: Resumen con IA funciona con el botón real.
  shared.length = 0;
  global.fetch = async function () { return { ok: true, json: async function () { return { candidates: [{ content: { parts: [{ text: 'Resumen real de prueba.' }] } }] }; } }; };
  document.getElementById('list')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-ai-wa]' ? { getAttribute: function () { return 'p1'; } } : null; }, hasAttribute: function (a) { return a === 'data-ai-wa'; } } });
  await sleep(10);
  console.log('AF6b) Resumen con IA funciona con el botón real:', shared.length === 1 && shared[0] === 'Resumen real de prueba.');

  // AH1: un 403 dice que la clave no tiene permiso (Google Cloud / API de Gemini).
  aiKey = 'CLAVE-PRUEBA';
  global.fetch = async function () { return { ok: false, status: 403, json: async function () { return { error: { message: 'Permission denied.' } }; } }; };
  var err403 = null;
  try { await askAI('hola'); } catch (e) { err403 = e; }
  console.log('AH1) un 403 dice que la clave no tiene permiso:', !!err403 && err403.status === 403 && aiErrorText(err403).indexOf('Google Cloud') !== -1 && aiErrorText(err403).indexOf('Generative Language API') !== -1);
  // AH2: otro error trae el código y el mensaje de Google.
  global.fetch = async function () { return { ok: false, status: 500, json: async function () { return { error: { message: 'Internal error.' } }; } }; };
  var err500 = null;
  try { await askAI('hola'); } catch (e) { err500 = e; }
  console.log('AH2) otro error trae el código y el mensaje:', !!err500 && aiErrorText(err500).indexOf('500') !== -1 && aiErrorText(err500).indexOf('Internal error.') !== -1);
  // AH3: si la red falla una vez, reintenta y responde.
  var tries = 0;
  global.fetch = async function () { tries++; if (tries === 1) throw new Error('Network error'); return { ok: true, json: async function () { return { candidates: [{ content: { parts: [{ text: 'Respuesta tras reintento.' }] } }] }; } }; };
  var ans3 = await askAI('hola');
  console.log('AH3) si la red falla una vez, reintenta y responde:', tries === 2 && ans3 === 'Respuesta tras reintento.');
  // AH4: si la red falla dos veces, avisa que revises la conexión.
  global.fetch = async function () { throw new Error('Network error'); };
  var errNet = null;
  try { await askAI('hola'); } catch (e) { errNet = e; }
  console.log('AH4) si la red falla dos veces, avisa de la conexión:', !!errNet && aiErrorText(errNet).indexOf('Revisa tu conexión') !== -1);
  // AH5: un 400 sigue diciendo que la clave no es válida.
  global.fetch = async function () { return { ok: false, status: 400, json: async function () { return { error: { message: 'API key not valid.' } }; } }; };
  var err400 = null;
  try { await askAI('hola'); } catch (e) { err400 = e; }
  console.log('AH5) un 400 sigue diciendo que la clave no es válida:', !!err400 && aiErrorText(err400).indexOf('no es válida') !== -1);

  // AI1: askAI usa el modelo actual gemini-3.8-flash.
  aiKey = 'CLAVE-PRUEBA';
  var calls38 = [];
  global.fetch = async function (url) { calls38.push(url); return { ok: true, json: async function () { return { candidates: [{ content: { parts: [{ text: 'Respuesta 3.8.' }] } }] }; } }; };
  var ans38 = await askAI('hola');
  console.log('AI1) askAI usa gemini-3.8-flash:', calls38.length === 1 && calls38[0] === 'https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent' && ans38 === 'Respuesta 3.8.');
  // AI2: si el modelo principal da 404, intenta con gemini-flash-latest.
  var callsFb = [];
  global.fetch = async function (url) {
    callsFb.push(url);
    if (url.indexOf('gemini-3.8-flash') !== -1) return { ok: false, status: 404, json: async function () { return { error: { message: 'Model not found.' } }; } };
    return { ok: true, json: async function () { return { candidates: [{ content: { parts: [{ text: 'Respuesta del respaldo.' }] } }] }; } };
  };
  var ansFb = await askAI('hola');
  console.log('AI2) si el modelo da 404, usa el ligero y luego el alias:', callsFb.length === 2 && callsFb[1] === 'https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent' && ansFb === 'Respuesta del respaldo.');
  // AI3: si los dos dan 404, el error es de modelo no disponible.
  global.fetch = async function () { return { ok: false, status: 404, json: async function () { return { error: { message: 'Model not found.' } }; } }; };
  var err404 = null;
  try { await askAI('hola'); } catch (e) { err404 = e; }
  console.log('AI3) si los dos dan 404, avisa que el modelo no está disponible:', !!err404 && err404.status === 404 && aiErrorText(err404).indexOf('no está disponible') !== -1);

  // AJ1: 503 en el principal -> usa el modelo ligero y responde.
  aiKey = 'CLAVE-PRUEBA';
  var calls503 = [];
  global.fetch = async function (url) {
    calls503.push(url);
    if (url.indexOf('gemini-3.8-flash') !== -1) return { ok: false, status: 503, json: async function () { return { error: { message: 'This model is currently experiencing high demand.' } }; } };
    return { ok: true, json: async function () { return { candidates: [{ content: { parts: [{ text: 'Respuesta del modelo ligero.' }] } }] }; } };
  };
  var ans503 = await askAI('hola');
  console.log('AJ1) 503 en el principal, usa gemini-3.5-flash-lite:', calls503.length === 2 && calls503[1] === 'https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent' && ans503 === 'Respuesta del modelo ligero.');
  // AJ2: 503 en los dos primeros -> usa el alias.
  var calls503b = [];
  global.fetch = async function (url) {
    calls503b.push(url);
    if (url.indexOf('gemini-flash-latest') !== -1) return { ok: true, json: async function () { return { candidates: [{ content: { parts: [{ text: 'Respuesta del alias.' }] } }] }; } };
    return { ok: false, status: 503, json: async function () { return { error: { message: 'This model is currently experiencing high demand.' } }; } };
  };
  var ans503b = await askAI('hola');
  console.log('AJ2) 503 en los dos primeros, usa gemini-flash-latest:', calls503b.length === 3 && calls503b[2] === 'https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent' && ans503b === 'Respuesta del alias.');
  // AJ3: 503 en los tres -> el error avisa que la IA está saturada.
  global.fetch = async function () { return { ok: false, status: 503, json: async function () { return { error: { message: 'This model is currently experiencing high demand.' } }; } }; };
  var err503 = null;
  try { await askAI('hola'); } catch (e) { err503 = e; }
  console.log('AJ3) 503 en los tres, avisa que la IA está saturada:', !!err503 && err503.status === 503 && aiErrorText(err503).indexOf('saturada') !== -1);
  // AJ4: 400 en el principal -> no prueba otros modelos.
  var calls400 = [];
  global.fetch = async function (url) { calls400.push(url); return { ok: false, status: 400, json: async function () { return { error: { message: 'API key not valid.' } }; } }; };
  var err400 = null;
  try { await askAI('hola'); } catch (e) { err400 = e; }
  console.log('AJ4) 400 en el principal, no prueba otros modelos:', calls400.length === 1 && !!err400 && err400.status === 400 && aiErrorText(err400).indexOf('no es válida') !== -1);
  // AJ5: 429 en el principal -> prueba el siguiente modelo.
  var calls429 = [];
  global.fetch = async function (url) {
    calls429.push(url);
    if (url.indexOf('gemini-3.8-flash') !== -1) return { ok: false, status: 429, json: async function () { return { error: { message: 'Quota exceeded.' } }; } };
    return { ok: true, json: async function () { return { candidates: [{ content: { parts: [{ text: 'Respuesta con cupo.' }] } }] }; } };
  };
  var ans429 = await askAI('hola');
  console.log('AJ5) 429 en el principal, prueba el siguiente modelo:', calls429.length === 2 && ans429 === 'Respuesta con cupo.');

  // AK1: Gemini 503 en sus tres modelos + clave DeepSeek -> usa DeepSeek y responde.
  aiKey = 'CLAVE-GEMINI'; aiKeyDs = 'CLAVE-DS';
  var callsDs = [];
  global.fetch = async function (url, opts) {
    callsDs.push([url, opts]);
    if (url.indexOf('api.deepseek.com') !== -1) return { ok: true, json: async function () { return { choices: [{ message: { content: 'Respuesta de DeepSeek.' } }] }; } };
    return { ok: false, status: 503, json: async function () { return { error: { message: 'This model is currently experiencing high demand.' } }; } };
  };
  var ansDs = await askAI('hola');
  var dsCall = callsDs[callsDs.length - 1];
  var dsBody = JSON.parse(dsCall[1].body);
  console.log('AK1) Gemini saturado, usa DeepSeek y responde:', callsDs.length === 4 && dsCall[0] === 'https://api.deepseek.com/chat/completions' && dsBody.model === 'deepseek-flash' && dsCall[1].headers.Authorization === 'Bearer CLAVE-DS' && ansDs === 'Respuesta de DeepSeek.');
  // AK2: Gemini responde -> DeepSeek no se llama.
  aiKey = 'CLAVE-GEMINI'; aiKeyDs = 'CLAVE-DS';
  var callsOk = [];
  global.fetch = async function (url) { callsOk.push(url); return { ok: true, json: async function () { return { candidates: [{ content: { parts: [{ text: 'Respuesta de Gemini.' }] } }] }; } }; };
  var ansOk = await askAI('hola');
  console.log('AK2) Gemini responde, DeepSeek no se llama:', callsOk.length === 1 && ansOk === 'Respuesta de Gemini.');
  // AK3: Gemini falla y no hay clave DeepSeek -> el error es el de Gemini (saturada).
  aiKey = 'CLAVE-GEMINI'; aiKeyDs = '';
  global.fetch = async function () { return { ok: false, status: 503, json: async function () { return { error: { message: 'This model is currently experiencing high demand.' } }; } }; };
  var errNoDs = null;
  try { await askAI('hola'); } catch (e) { errNoDs = e; }
  console.log('AK3) Gemini falla sin DeepSeek, avisa saturada:', !!errNoDs && !errNoDs.provider && errNoDs.status === 503 && aiErrorText(errNoDs).indexOf('saturada') !== -1);
  // AK4: Gemini falla y DeepSeek 401 -> el error dice que la clave de DeepSeek no es válida.
  aiKey = 'CLAVE-GEMINI'; aiKeyDs = 'CLAVE-MALA';
  global.fetch = async function (url) {
    if (url.indexOf('api.deepseek.com') !== -1) return { ok: false, status: 401, json: async function () { return { error: { message: 'Incorrect API key provided.' } }; } };
    return { ok: false, status: 503, json: async function () { return { error: { message: 'This model is currently experiencing high demand.' } }; } };
  };
  var err401 = null;
  try { await askAI('hola'); } catch (e) { err401 = e; }
  console.log('AK4) DeepSeek 401, avisa que su clave no es válida:', !!err401 && err401.provider === 'deepseek' && err401.status === 401 && aiErrorText(err401).indexOf('DeepSeek no es válida') !== -1);
  // AK5: foto de daños, Gemini falla -> DeepSeek recibe la foto (visión) y responde.
  aiKey = 'CLAVE-GEMINI'; aiKeyDs = 'CLAVE-DS';
  var dsImgBody = null;
  global.fetch = async function (url, opts) {
    if (url.indexOf('api.deepseek.com') !== -1) { dsImgBody = JSON.parse(opts.body); return { ok: true, json: async function () { return { choices: [{ message: { content: 'Se ve una abolladura.' } }] }; } }; }
    return { ok: false, status: 503, json: async function () { return { error: { message: 'This model is currently experiencing high demand.' } }; } };
  };
  var ansImg = await askAI('describe los daños', 'data:image/jpeg;base64,AAAA');
  var imgPart = dsImgBody && dsImgBody.messages[0].content[1];
  console.log('AK5) foto de daños, DeepSeek recibe la imagen y responde:', ansImg === 'Se ve una abolladura.' && !!imgPart && imgPart.type === 'image_url' && imgPart.image_url.url === 'data:image/jpeg;base64,AAAA');
  // AK6: panel de DeepSeek y funciones en el bundle.
  console.log('AK6) panel DeepSeek y funciones en firebase.js:', html.includes('id="fAiKeyDs"') && html.includes('btnAiGuardarDs') && html.includes('btnAiQuitarDs') && html.includes('aiKeyDsStatus') && fb.includes('getDeepseekKey') && fb.includes('setDeepseekKey') && fb.includes("setDoc(doc(db, 'config', 'ai'), { key: key || '' }, { merge: true })"));
  // AK7: sin clave de Gemini pero con DeepSeek -> va directo a DeepSeek.
  aiKey = ''; aiKeyDs = 'CLAVE-DS';
  var callsOnly = [];
  global.fetch = async function (url) { callsOnly.push(url); return { ok: true, json: async function () { return { choices: [{ message: { content: 'Solo DeepSeek.' } }] }; } }; };
  var ansOnly = await askAI('hola');
  console.log('AK7) sin Gemini, va directo a DeepSeek:', callsOnly.length === 1 && callsOnly[0] === 'https://api.deepseek.com/chat/completions' && ansOnly === 'Solo DeepSeek.');

  // AL1: con el plugin de cámara, el botón de foto de serie abre el menú nativo.
  var capturedOpts = null;
  global.Capacitor = { Plugins: { Camera: { getPhoto: function (opts) { capturedOpts = opts; return new Promise(function () {}); } } } };
  document.getElementById('btnFotoSerie')._h.click[0]();
  console.log('AL1) botón foto serie abre el menú nativo (PROMPT, dataUrl):', !!capturedOpts && capturedOpts.source === 'PROMPT' && capturedOpts.resultType === 'dataUrl');
  // AL2: sin el plugin, el botón usa el selector de archivos.
  global.Capacitor = undefined;
  var fallbackClicked = false;
  document.getElementById('fFotoSerie').click = function () { fallbackClicked = true; };
  document.getElementById('btnFotoSerie')._h.click[0]();
  console.log('AL2) sin plugin, el botón usa el selector de archivos:', fallbackClicked === true);
  // AL3: el botón de foto de daños también usa el menú nativo.
  capturedOpts = null;
  global.Capacitor = { Plugins: { Camera: { getPhoto: function (opts) { capturedOpts = opts; return new Promise(function () {}); } } } };
  document.getElementById('btnFotoDanos')._h.click[0]();
  console.log('AL3) botón foto daños abre el menú nativo (PROMPT):', !!capturedOpts && capturedOpts.source === 'PROMPT');
  // AL4: si el usuario cancela el menú, no pasa nada y no se rompe.
  global.Capacitor = { Plugins: { Camera: { getPhoto: function () { return Promise.reject(new Error('User cancelled')); } } } };
  window._fotoSerie = null;
  document.getElementById('btnFotoSerie')._h.click[0]();
  await sleep(20);
  console.log('AL4) cancelar el menú no rompe nada y no guarda foto:', window._fotoSerie === null);
  global.Capacitor = undefined;
  // AL5: estáticos — sin capture, con script del plugin y plugin sincronizado.
  var pluginsJson = fs.readFileSync(__dirname + '/../android/app/src/main/assets/capacitor.plugins.json', 'utf8');
  console.log('AL5) sin capture, script y plugin de cámara sincronizado:', !html.includes('capture="environment"') && html.includes('cap-plugins/camera-plugin.js') && html.includes('pickPhoto') && pluginsJson.includes('@capacitor/camera') && fs.existsSync(__dirname + '/../www/cap-plugins/camera-plugin.js'));

  // AM1: los formularios tienen el campo Hostname.
  console.log('AM1) campo Hostname en equipo nuevo y en reasignado:', html.includes('id="fHostname"') && html.includes('id="fReHostname"'));
  // AM2: guardar equipo nuevo guarda el hostname y se sube a la nube.
  doLogin('usuario');
  var upH = [];
  global.Cloud.upsertPrep = async function (d) { upH.push(d); };
  document.getElementById('fTipo').value = 'Laptop';
  document.getElementById('fMarca').value = 'Dell';
  document.getElementById('fModelo').value = 'Inspiron 3501';
  document.getElementById('fSerie').value = 'S1';
  document.getElementById('fInv').value = '100';
  document.getElementById('fHostname').value = 'PC-SOPORTE-01';
  document.getElementById('fUser').value = 'Ana';
  document.getElementById('fTec').value = 'Test User';
  document.getElementById('btnAdd')._h.click[0]();
  var newPrep = state.preparations[state.preparations.length - 1];
  console.log('AM2) equipo nuevo guarda el hostname:', !!newPrep && newPrep.equipo.hostname === 'PC-SOPORTE-01' && upH.length === 1 && upH[0].equipo.hostname === 'PC-SOPORTE-01');
  // AM3: el hostname se ve en la tarjeta, el WhatsApp, el Excel y el PDF.
  var pH = mkPrep({ equipo: { tipo: 'Laptop', marca: 'Dell', modelo: 'Inspiron', serie: 'S1', inventario: '100', hostname: 'PC-SOPORTE-01' } });
  state.preparations.push(pH);
  render();
  var cardHas = document.getElementById('list').innerHTML.indexOf('Host: PC-SOPORTE-01') !== -1;
  var waHas = waTextOne(pH).indexOf('Hostname: PC-SOPORTE-01') !== -1;
  var waAllHas = waTextAll([pH]).indexOf('Host: PC-SOPORTE-01') !== -1;
  var xlsxHas = SRC.includes("'Hostname'") && SRC.includes('p.equipo.hostname');
  console.log('AM3) hostname en tarjeta, WhatsApp y Excel:', cardHas && waHas && waAllHas && xlsxHas);
  // AM4: la nube guarda y restaura el hostname.
  var docH = prepToCloudDoc(pH);
  var backH = prepFromCloud(docH);
  console.log('AM4) la nube guarda y restaura el hostname:', docH.equipo.hostname === 'PC-SOPORTE-01' && backH.equipo.hostname === 'PC-SOPORTE-01');
  // AM5: se puede buscar por hostname.
  searchText = 'soporte-01';
  var foundH = currentList().some(function (p) { return p.id === pH.id; });
  searchText = '';
  console.log('AM5) se puede buscar por hostname:', foundH === true);
  // AM6: reasignar 'Otro equipo' guarda el hostname.
  var nBeforeH = state.preparations.length;
  document.getElementById('fReEquipo').value = '__nuevo__'; document.getElementById('fReA').value = 'Luis'; document.getElementById('fReDe').value = 'Ana';
  document.getElementById('fReTipo').value = 'Desktop'; document.getElementById('fReMarca').value = 'HP'; document.getElementById('fReModelo').value = 'EliteDesk'; document.getElementById('fReSerie').value = 'S2'; document.getElementById('fReInv').value = '200'; document.getElementById('fReHostname').value = 'PC-VENTAS-02';
  document.getElementById('btnReGuardar')._h.click[0]();
  var reH = state.preparations[state.preparations.length - 1];
  console.log('AM6) reasignado guarda el hostname:', state.preparations.length === nBeforeH + 1 && !!reH && reH.equipo.hostname === 'PC-VENTAS-02');
  // AN0: funciones de detectados en firebase.js, en el bundle y reglas.
  const fbBundle = fs.readFileSync(__dirname + '/../www/cloud/firebase.bundle.js', 'utf8');
  console.log('AN0) firebase.js y bundle traen las 4 funciones:', ['reportDetected', 'subscribeDetectados', 'deleteDetectado', 'markDetectadoUsado'].every(f => fb.includes(f) && fbBundle.includes(f)), '| reglas detectados:', rules.includes('match /detectados/{id}'));
  // AN1: 'Usar este equipo' llena el formulario y marca usado.
  document.getElementById('loginView');
  document.getElementById('mainApp');
  doLogin('usuario');
  CLOUD_ENABLED = true;
  var markedUsed = [];
  var deletedDet = [];
  global.Cloud.markDetectadoUsado = async function (id) { markedUsed.push(id); };
  global.Cloud.deleteDetectado = async function (id) { deletedDet.push(id); };
  detectados = [
    { id: 'SERIE123', hostname: 'PC-01', marca: 'HP', modelo: 'EliteDesk 800', serie: 'SERIE123', cpu: 'Intel Core i7-10700', ramGB: 16, discoGB: 512, so: 'Windows 11 Pro', tipo: 'Desktop', mac: 'AA:BB:CC:DD:EE:FF', detectadoEn: Date.now() - 3600000, detectadoPor: 'Gerardo', usado: false }
  ];
  renderDetectados();
  var detHtml = document.getElementById('detList').innerHTML;
  var detShows = detHtml.includes('PC-01') && detHtml.includes('HP') && detHtml.includes('EliteDesk 800') && detHtml.includes('SERIE123') && detHtml.includes('Intel Core i7-10700') && detHtml.includes('16 GB') && detHtml.includes('512 GB') && detHtml.includes('Windows 11 Pro') && detHtml.includes('hace 1 h') && detHtml.includes('Gerardo') && detHtml.includes('Usar este equipo') && detHtml.includes('Descartar');
  document.getElementById('detList')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-det-use]' ? { getAttribute: function () { return 'SERIE123'; } } : null; } } });
  console.log('AN1) lista muestra hostname, marca/modelo, serie, CPU, RAM, disco, SO, hace cuánto y por quién:', detShows, '| Usar llena el formulario:', document.getElementById('fTipo').value === 'Desktop' && document.getElementById('fMarca').value === 'HP' && document.getElementById('fModelo').value === 'EliteDesk 800' && document.getElementById('fSerie').value === 'SERIE123' && document.getElementById('fHostname').value === 'PC-01', '| marca usado:', markedUsed.indexOf('SERIE123') !== -1, '| cierra el panel y abre Nuevo equipo:', document.getElementById('detBox').hidden === true && document.getElementById('newBox').hidden === false);
  // AN2: 'Descartar' abre el modal inline y borra solo con Sí; con No no borra.
  deletedDet.length = 0;
  document.getElementById('detList')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-det-del]' ? { getAttribute: function () { return 'SERIE123'; } } : null; } } });
  var discModal = document.getElementById('confirmModal').hidden === false && document.getElementById('confirmMsg').textContent === '¿Descartar este equipo detectado?';
  var discBefore = deletedDet.length === 0;
  answerConfirm(true);
  await sleep(20);
  var discOk = deletedDet.indexOf('SERIE123') !== -1;
  deletedDet.length = 0;
  document.getElementById('detList')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-det-del]' ? { getAttribute: function () { return 'SERIE123'; } } : null; } } });
  answerConfirm(false);
  await sleep(20);
  console.log('AN2) Descartar abre el modal con su pregunta:', discModal, '| antes de Sí no borra:', discBefore, '| con Sí borra:', discOk, '| con No no borra:', deletedDet.length === 0);
  // AN3: 'Detectar este equipo' solo visible con window.Desktop.
  global.Desktop = undefined;
  render();
  var detHiddenNoDesk = document.getElementById('btnDetectar').hidden === true;
  var reported = [];
  global.Cloud.reportDetected = async function (info) { reported.push(info); };
  global.Desktop = { detect: async function () { return { hostname: 'PC-DETECTADA', marca: 'Lenovo', modelo: 'ThinkCentre', serie: 'SERIE999', cpu: 'Intel i5', ramGB: 8, discoGB: 256, so: 'Windows 11', tipo: 'Desktop', mac: '11:22:33:44:55:66', detectadoEn: Date.now() }; } };
  render();
  var detShownDesk = document.getElementById('btnDetectar').hidden === false;
  document.getElementById('btnDetectar')._h.click[0]();
  await sleep(20);
  var detReportOk = reported.length === 1 && reported[0].hostname === 'PC-DETECTADA' && reported[0].detectadoPor === 'Test User';
  var detAlertOk = toastTxt() === 'Equipo detectado, ya aparece en los teléfonos';
  global.Desktop = { detect: async function () { throw new Error('sin red'); } };
  document.getElementById('btnDetectar')._h.click[0]();
  await sleep(20);
  var detFailOk = toastTxt().indexOf('No se pudo detectar el equipo') === 0;
  cloudUser = null;
  global.Desktop = { detect: async function () { return {}; } };
  document.getElementById('btnDetectar')._h.click[0]();
  await sleep(20);
  var detNoSessionOk = toastTxt().indexOf('Inicia sesión') === 0 && reported.length === 1;
  global.Desktop = undefined;
  console.log('AN3) sin Desktop el botón está oculto:', detHiddenNoDesk, '| con Desktop visible:', detShownDesk, '| Detectar reporta con el técnico:', detReportOk, '| avisa que ya aparece:', detAlertOk, '| si detect() falla avisa sin romper:', detFailOk, '| sin sesión no reporta y avisa:', detNoSessionOk);
  // AN4: los detectados usados (viejos o recientes) no se listan; el pendiente sí.
  detectados = [
    { id: 'VIEJO1', hostname: 'PC-VIEJA', marca: 'Dell', modelo: 'OptiPlex', serie: 'VIEJO1', cpu: 'i3', ramGB: 4, discoGB: 128, so: 'Windows 10', tipo: 'Desktop', detectadoEn: Date.now() - 30 * 86400000, detectadoPor: 'Gerardo', usado: true },
    { id: 'USADO1', hostname: 'PC-USADA', marca: 'HP', modelo: 'ProDesk', serie: 'USADO1', cpu: 'i5', ramGB: 8, discoGB: 256, so: 'Windows 11', tipo: 'Desktop', detectadoEn: Date.now() - 3600000, detectadoPor: 'Alejandro', usado: true },
    { id: 'NUEVO1', hostname: 'PC-NUEVA', marca: 'Lenovo', modelo: 'ThinkPad', serie: 'NUEVO1', cpu: 'i7', ramGB: 16, discoGB: 512, so: 'Windows 11', tipo: 'Laptop', detectadoEn: Date.now() - 60000, detectadoPor: 'Gerardo', usado: false }
  ];
  renderDetectados();
  var detHtml4 = document.getElementById('detList').innerHTML;
  console.log('AN4) usados no se listan (ni viejo ni reciente):', detHtml4.indexOf('PC-VIEJA') === -1 && detHtml4.indexOf('PC-USADA') === -1, '| pendiente sí se lista:', detHtml4.indexOf('PC-NUEVA') !== -1 && detHtml4.indexOf('ThinkPad') !== -1);
  // AN5: al entrar se suscribe a detectados; al salir se desuscribe.
  var detCb = null;
  var detUnsubCalled = false;
  global.Cloud.getUserDoc = async function () { return { activo: true, rol: 'usuario', nombre: 'Test User', email: 'test@checklist.local' }; };
  global.Cloud.isInitialized = async function () { return true; };
  global.Cloud.getAllRenta = async function () { return []; };
  global.Cloud.upsertRenta = async function () {};
  global.Cloud.getAllPreparations = async function () { return []; };
  global.Cloud.upsertPrep = async function () {};
  global.Cloud.subscribeRenta = function () { return function () {}; };
  global.Cloud.subscribePreparations = function () { return function () {}; };
  global.Cloud.subscribeDetectados = function (cb) { detCb = cb; return function () { detUnsubCalled = true; }; };
  global.Cloud.subscribePresence = function () { return function () {}; };
  global.Cloud.subscribeChat = function () { return function () {}; };
  global.Cloud.subscribeDm = function () { return function () {}; };
  global.Cloud.heartbeat = function () {};
  global.Cloud.pruneChat = function () {};
  global.Cloud.clearPresence = function () {};
  global.Cloud.listUsers = async function () { return []; };
  localStorage.setItem('checklist-soporte-migrado-v2:u1', '1');
  localStorage.setItem('checklist-soporte-migrado-preps-v1:u1', '1');
  state.preparations = [];
  state.renta = [];
  await onAuthChanged({ uid: 'u1', email: 'test@checklist.local' });
  var subOk = typeof detCb === 'function';
  detCb([{ id: 'D1', hostname: 'PC-CLOUD', marca: 'HP', modelo: 'EliteBook', serie: 'D1', cpu: 'i7', ramGB: 16, discoGB: 512, so: 'Windows 11', tipo: 'Laptop', detectadoEn: Date.now(), detectadoPor: 'Gerardo', usado: false }]);
  var cbOk = detectados.length === 1 && detectados[0].hostname === 'PC-CLOUD' && document.getElementById('detList').innerHTML.indexOf('PC-CLOUD') !== -1;
  await onAuthChanged(null);
  console.log('AN5) al entrar se suscribe a detectados:', subOk, '| la lista llega y se muestra:', cbOk, '| al salir se desuscribe:', detUnsubCalled === true);


  // AO0: estáticos 2.3.1 (helpers, nota, línea, progreso, nube tal cual).
  console.log('AO0) estáticos 2.3.1: nota en tarjeta:', html.includes('Puntos marcados por el detector'), '| línea Detectado: y helper:', SRC.includes("return 'Detectado: '") && SRC.includes('detLineFor(d)'), '| progreso Detectando software:', html.includes('Detectando software...'), '| helpers de filtro:', ['filterDetectedChecks', 'detShortName', 'detLineFor', 'detectedNames'].every(function (f) { return SRC.includes(f); }), '| autoDetectado en prepToCloudDoc/prepFromCloud:', SRC.includes('autoDetectado: p.autoDetectado || []') && SRC.includes('autoDetectado: doc.autoDetectado || []'), '| firebase.js pasa checks/detalles tal cual:', fb.includes("return setDoc(doc(db, 'detectados', String(d.id)), d, { merge: true })"), '| bundle trae reportDetected:', fbBundle.includes('reportDetected'));
  // AO1: mapeo de cada chequeo con salidas simuladas del detector.
  const detFull = { t3: true, t4: true, t6: true, t7: true, t8: 'Office 365', t9: true, t10: true, t11: true, t12: true, t18: true, t19: true, t20: true, t21: true, t22: true, t23: true, t24: true, t25: true };
  const fFull = filterDetectedChecks(detFull);
  console.log('AO1) mapeo completo: 17 puntos:', fFull.ids.length === 17, '| Office 365:', fFull.checks.t8 === 'Office 365', '| t3/t4 de hardware:', fFull.checks.t3 === true && fFull.checks.t4 === true, '| t12 Invgate:', fFull.checks.t12 === true, '| nombres cortos en orden de plantilla:', detectedNames(fFull.checks, fFull.ids).join(', ') === 'Batería y cargador, Etiqueta y serie, SO actualizado, Antivirus, Office 365, Impresoras, VPN, Inicio rápido desactivado, Invgate, Chrome, Adobe Reader, WinRAR, Lapi Fox, Alfaweb, Alfaprinter, Accesos directos, AnyDesk Gris');
  const fLibre = filterDetectedChecks({ t8: 'LibreOffice', t18: true });
  console.log('AO1b) LibreOffice se marca:', fLibre.checks.t8 === 'LibreOffice', '| y Chrome:', fLibre.checks.t18 === true);
  const fNoOff = filterDetectedChecks({ t18: true, t8: true });
  console.log('AO1c) Office sin activar (booleano) no se marca:', fNoOff.checks.t8 === undefined && fNoOff.ids.indexOf('t8') === -1);
  const fBad = filterDetectedChecks({ t8: 'Office 2019' });
  console.log('AO1d) Office con valor fuera de opciones se ignora:', fBad.ids.length === 0);
  const fNever = filterDetectedChecks({ t1: true, t2: true, t12: true, t13: true, t15: true, t16: true, t17: true, t26: true, t99: true, foo: true, t18: true });
  console.log('AO1e) nunca t1/t2/t13-t17/t26 ni desconocidos:', fNever.ids.length === 2 && fNever.ids[0] === 't12' && fNever.ids[1] === 't18', '| quedan Invgate y Chrome:', Object.keys(fNever.checks).length === 2);
  // AO2: 'Usar este equipo' aplica checks y autoDetectado al guardar.
  doLogin('usuario');
  CLOUD_ENABLED = true;
  cloudUser = { uid: 'u1', email: 'test@checklist.local', nombre: 'Test User' };
  var upDet = [];
  global.Cloud.upsertPrep = async function (d) { upDet.push(d); };
  global.Cloud.markDetectadoUsado = async function () {};
  detectados = [{ id: 'DET1', hostname: 'PC-DET', marca: 'HP', modelo: 'EliteDesk 800', serie: 'DET1', cpu: 'i7', ramGB: 16, discoGB: 512, so: 'Windows 11', tipo: 'Desktop', detectadoEn: Date.now() - 60000, detectadoPor: 'Gerardo', usado: false, checks: { t3: true, t4: true, t18: true, t19: true, t20: true, t8: 'Office 365', t1: true, t12: true, t99: true }, detalles: { officeDetectado: true } }];
  document.getElementById('detList')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-det-use]' ? { getAttribute: function () { return 'DET1'; } } : null; } } });
  var stashOk = window._detectedChecks && window._detectedChecks.t18 === true && window._detectedDetalles && window._detectedDetalles.officeDetectado === true;
  document.getElementById('fUser').value = 'Ana';
  document.getElementById('fTec').value = 'Test User';
  document.getElementById('btnAdd')._h.click[0]();
  var savedDet = state.preparations[state.preparations.length - 1];
  console.log('AO2) Usar guarda el stash:', stashOk, '| preparación nace con checks detectados:', !!savedDet && savedDet.checks.t3 === true && savedDet.checks.t4 === true && savedDet.checks.t12 === true && savedDet.checks.t18 === true && savedDet.checks.t19 === true && savedDet.checks.t20 === true && savedDet.checks.t8 === 'Office 365', '| sin t1 ni t99:', !!savedDet && savedDet.checks.t1 === undefined && savedDet.checks.t99 === undefined, '| autoDetectado:', !!savedDet && savedDet.autoDetectado.join(',') === 't3,t4,t8,t12,t18,t19,t20', '| sube a la nube con autoDetectado:', upDet.length === 1 && upDet[0].autoDetectado.join(',') === 't3,t4,t8,t12,t18,t19,t20', '| stash limpio tras guardar:', window._detectedChecks === null && window._detectedDetalles === null);
  // AO3: Nuevo equipo en blanco limpia el guardado.
  window._detectedChecks = { t18: true };
  window._detectedDetalles = {};
  document.getElementById('newBox').scrollIntoView = function () {};
  document.getElementById('btnShowNew')._h.click[0]();
  var clearedOk = window._detectedChecks === null && window._detectedDetalles === null;
  document.getElementById('fTipo').value = 'Laptop';
  document.getElementById('fMarca').value = 'Dell';
  document.getElementById('fModelo').value = 'XPS 13';
  document.getElementById('fSerie').value = 'S-BLANCO';
  document.getElementById('fUser').value = 'Luis';
  document.getElementById('fTec').value = 'Test User';
  upDet.length = 0;
  document.getElementById('btnAdd')._h.click[0]();
  var blankPrep = state.preparations[state.preparations.length - 1];
  console.log('AO3) Nuevo en blanco limpia el guardado:', clearedOk, '| y guarda sin checks ni autoDetectado:', !!blankPrep && Object.keys(blankPrep.checks).length === 0 && blankPrep.autoDetectado.length === 0);
  // AO4: autoDetectado viaja a la nube y vuelve (merge incluido).
  var pDet = mkPrep({ checks: { t18: true, t8: 'Office 365' }, autoDetectado: ['t8', 't18'] });
  var docDet = prepToCloudDoc(pDet);
  var backDet = prepFromCloud(docDet);
  var mergedDet = mergePrepsWithLocal([docDet]);
  console.log('AO4) la nube guarda y restaura autoDetectado:', docDet.autoDetectado.join(',') === 't8,t18' && backDet.autoDetectado.join(',') === 't8,t18' && backDet.checks.t8 === 'Office 365', '| merge lo conserva:', mergedDet[0].autoDetectado.join(',') === 't8,t18', '| sin autoDetectado queda []:', prepFromCloud(prepToCloudDoc(mkPrep())).autoDetectado.length === 0);
  // AO5: la tarjeta del detectado muestra la línea 'Detectado:'.
  function mkDet(over) { return Object.assign({ id: 'DX', hostname: 'PC-X', marca: 'HP', modelo: 'EliteDesk', serie: 'DX', cpu: 'i5', ramGB: 8, discoGB: 256, so: 'Windows 11', tipo: 'Desktop', detectadoEn: Date.now() - 60000, detectadoPor: 'Gerardo', usado: false, checks: {}, detalles: {} }, over || {}); }
  detectados = [mkDet({ id: 'D-A', checks: { t18: true, t20: true, t8: 'Office 365' } })];
  renderDetectados();
  var detLineHtml = document.getElementById('detList').innerHTML;
  detectados = [mkDet({ id: 'D-B', checks: { t18: true }, detalles: { officeDetectado: true } })];
  renderDetectados();
  var detOffHtml = document.getElementById('detList').innerHTML;
  detectados = [mkDet({ id: 'D-C' })];
  renderDetectados();
  var detNoneHtml = document.getElementById('detList').innerHTML;
  console.log('AO5) tarjeta del detectado muestra lo detectado:', detLineHtml.includes('Detectado: Office 365, Chrome, WinRAR'), '| Office sin activar avisa:', detOffHtml.includes('Detectado: Chrome') && detOffHtml.includes('Office instalado, activación sin verificar'), '| sin checks no hay línea:', detNoneHtml.indexOf('Detectado:') === -1);
  // AO6: la tarjeta de la preparación muestra la nota del detector (no la fila resumida).
  cloudRole = 'usuario';
  var pNote = mkPrep({ checks: { t18: true, t20: true, t8: 'Office 365' }, autoDetectado: ['t8', 't18', 't20'] });
  var cardNote = cardHtml(pNote);
  var pEntDet = mkPrep({ id: 'pEntDet', deliveredAt: Date.now() - 86400000, readyAt: Date.now() - 2 * 86400000, checks: { t18: true }, autoDetectado: ['t18'] });
  todosPage = 0;
  window._expandedId = null;
  var todosHtml = todosListHtml([pEntDet]);
  console.log('AO6) tarjeta muestra la nota del detector:', cardNote.includes('Puntos marcados por el detector: Office 365, Chrome, WinRAR'), '| fila resumida de Todos no la muestra:', todosHtml.indexOf('Puntos marcados por el detector') === -1, '| tarjeta sin autoDetectado no muestra nota:', cardHtml(mkPrep()).indexOf('Puntos marcados por el detector') === -1);
  // AO7: Detectar muestra progreso, deshabilita y restaura al terminar o fallar.
  doLogin('usuario');
  CLOUD_ENABLED = true;
  var repDet = [];
  global.Cloud.reportDetected = async function (info) { repDet.push(info); return {}; };
  var btnDetEl = document.getElementById('btnDetectar');
  btnDetEl.innerHTML = 'Detectar este equipo';
  var resolveDet = null;
  global.Desktop = { detect: function () { return new Promise(function (res) { resolveDet = res; }); } };
  document.getElementById('btnDetectar')._h.click[0]();
  var progOk = btnDetEl.disabled === true && btnDetEl.innerHTML.indexOf('Detectando software...') !== -1;
  resolveDet({ hostname: 'PC-PROG', marca: 'Lenovo', modelo: 'ThinkCentre', serie: 'SPROG', cpu: 'i5', ramGB: 8, discoGB: 256, so: 'Windows 11', tipo: 'Desktop', detectadoEn: Date.now() });
  await sleep(20);
  var restoredOk = btnDetEl.disabled === false && btnDetEl.innerHTML === 'Detectar este equipo';
  var progReportOk = repDet.length === 1 && repDet[0].hostname === 'PC-PROG' && toastTxt() === 'Equipo detectado, ya aparece en los teléfonos';
  global.Desktop = { detect: async function () { throw new Error('sin red'); } };
  btnDetEl.innerHTML = 'Detectar este equipo';
  document.getElementById('btnDetectar')._h.click[0]();
  await sleep(20);
  var failRestoredOk = btnDetEl.disabled === false && btnDetEl.innerHTML === 'Detectar este equipo' && toastTxt().indexOf('No se pudo detectar el equipo') === 0;
  global.Desktop = undefined;
  console.log('AO7) Detectar muestra progreso y deshabilita:', progOk, '| al terminar restaura el botón:', restoredOk, '| y reporta el equipo:', progReportOk, '| si falla también restaura y avisa:', failRestoredOk);


  // AP0: estáticos 2.3.5 (versión, 17 detectables, nunca-marcar, defaults viejos).
  var all17 = filterDetectedChecks({ t3: true, t4: true, t6: true, t7: true, t8: 'Office 365', t9: true, t10: true, t11: true, t12: true, t18: true, t19: true, t20: true, t21: true, t22: true, t23: true, t24: true, t25: true });
  var oldBack = prepFromCloud(prepToCloudDoc(mkPrep()));
  console.log('AP0) estáticos 2.5.2: versión:', html.includes('Versión 2.5.2') && !html.includes('Versión 2.5.0'), '| 17 detectables con t12:', all17.ids.length === 17, '| nombre corto Invgate:', detShortName('t12') === 'Invgate', '| nunca-marcar solo t1/t2/t13-t17/t26:', filterDetectedChecks({ t1: true, t2: true, t13: true, t14: true, t15: true, t16: true, t17: true, t26: true }).ids.length === 0, '| equipos viejos con defaults vacíos:', oldBack.equipo.cpu === '' && oldBack.equipo.ramGB === '' && oldBack.equipo.discoGB === '' && oldBack.equipo.discoTipo === '' && oldBack.equipo.ip === '' && oldBack.equipo.ipTipo === '' && oldBack.equipo.anydeskId === '' && oldBack.equipo.anydeskAlias === '' && oldBack.versiones.so === '' && oldBack.versiones.antivirus === '' && oldBack.versiones.chrome === '');
  // AP1: t12 con agente Invgate (servicio/proceso/clave en el escritorio).
  var fT12 = filterDetectedChecks({ t12: true });
  var lineInv = detLineFor({ checks: { t12: true }, detalles: { invgate: 'InvGate Agent 9.5.1' } });
  var lineInvOnly = detLineFor({ checks: {}, detalles: { invgate: 'InvGate Agent 9.5.1' } });
  var lineNoInv = detLineFor({ checks: { t18: true }, detalles: {} });
  console.log('AP1) t12 detectable por el detector:', fT12.checks.t12 === true && fT12.ids.length === 1, '| línea con agente Invgate:', lineInv === 'Detectado: Invgate', '| solo detalles.invgate avisa:', lineInvOnly === 'Detectado: Agente de Invgate detectado', '| sin Invgate no lo inventa:', lineNoInv === 'Detectado: Chrome');
  // AP2: t19 con Acrobat (y Reader sigue).
  var lineAcr = detLineFor({ checks: { t19: true }, detalles: { adobe: 'Acrobat' } });
  var lineRea = detLineFor({ checks: { t19: true }, detalles: { adobe: 'Reader' } });
  var lineAdDef = detLineFor({ checks: { t19: true }, detalles: {} });
  console.log('AP2) t19 con Acrobat:', lineAcr === 'Detectado: Adobe Acrobat', '| con Reader:', lineRea === 'Detectado: Adobe Reader', '| sin detalle sigue Reader:', lineAdDef === 'Detectado: Adobe Reader');
  // AP3: t22 por .lnk y t24 con hcweb+gabinete (y negativo si falta uno).
  var fLnk = filterDetectedChecks({ t22: true });
  var fHc = filterDetectedChecks({ t24: true });
  var fHcUno = filterDetectedChecks({ t24: false });
  console.log('AP3) t22 por .lnk:', fLnk.checks.t22 === true, '| t24 con hcweb+gabinete:', fHc.checks.t24 === true, '| si falta uno no se marca t24:', fHcUno.checks.t24 === undefined && fHcUno.ids.indexOf('t24') === -1);
  // AP4: versiones (Get-ComputerInfo/SecurityCenter2/Chrome) viajan a la prep y se muestran.
  function mkDet2(over) { return Object.assign({ id: 'DX2', hostname: 'PC-X', marca: 'HP', modelo: 'EliteDesk', serie: 'DX2', cpu: 'Intel Core i5-10500', ramGB: 8, discoGB: 256, discoTipo: 'SSD', so: 'Windows 11 Pro', tipo: 'Desktop', detectadoEn: Date.now() - 60000, detectadoPor: 'Gerardo', usado: false, checks: {}, detalles: {}, versiones: {}, ip: '', ipTipo: '', anydeskId: '', anydeskAlias: '' }, over || {}); }
  function useDet(id) {
    document.getElementById('detList')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-det-use]' ? { getAttribute: function () { return id; } } : null; } } });
  }
  doLogin('usuario');
  CLOUD_ENABLED = true;
  cloudUser = { uid: 'u1', email: 'test@checklist.local', nombre: 'Test User' };
  var upVer = [];
  global.Cloud.upsertPrep = async function (d) { upVer.push(d); };
  global.Cloud.markDetectadoUsado = async function () {};
  detectados = [mkDet2({ id: 'DET-VER', hostname: 'PC-VER', serie: 'DET-VER', cpu: 'Intel Core i7-10700', ramGB: 16, discoGB: 512, discoTipo: 'SSD', checks: { t18: true }, versiones: { so: 'Windows 11 Pro 26H2 (compilación 26200)', antivirus: 'ESET NOD32 Antivirus 18.0.12', chrome: '141.0.7390.65' } })];
  useDet('DET-VER');
  var stashVer = window._detectedVersiones;
  document.getElementById('fUser').value = 'Ana';
  document.getElementById('fTec').value = 'Test User';
  document.getElementById('btnAdd')._h.click[0]();
  var savedVer = state.preparations[state.preparations.length - 1];
  var cardVer = cardHtml(savedVer);
  console.log('AP4) versiones en el guardado:', !!stashVer && stashVer.so === 'Windows 11 Pro 26H2 (compilación 26200)' && stashVer.antivirus === 'ESET NOD32 Antivirus 18.0.12' && stashVer.chrome === '141.0.7390.65', '| viajan a la prep:', !!savedVer && savedVer.versiones.so === 'Windows 11 Pro 26H2 (compilación 26200)' && savedVer.versiones.antivirus === 'ESET NOD32 Antivirus 18.0.12' && savedVer.versiones.chrome === '141.0.7390.65', '| y suben a la nube:', upVer.length === 1 && upVer[0].versiones.chrome === '141.0.7390.65', '| tarjeta muestra el bloque:', cardVer.includes('Versiones detectadas: SO: Windows 11 Pro 26H2') && cardVer.includes('Antivirus: ESET NOD32 Antivirus 18.0.12') && cardVer.includes('Chrome: 141.0.7390.65'), '| hardware en tarjeta:', cardVer.includes('Procesador: Intel Core i7-10700 • RAM: 16 GB • Disco: 512 GB SSD'));
  // AP4b: solo una versión conocida muestra solo esa; sin versiones no hay bloque.
  var pParc = mkPrep({ versiones: { so: '', antivirus: '', chrome: '141.0.7390.65' } });
  var cardParc = cardHtml(pParc);
  console.log('AP4b) solo Chrome muestra solo Chrome:', cardParc.includes('Versiones detectadas: Chrome: 141.0.7390.65') && cardParc.indexOf('SO: Windows') === -1 && cardParc.indexOf('Antivirus: ESET') === -1, '| sin versiones no hay bloque:', cardHtml(mkPrep()).indexOf('Versiones detectadas') === -1);
  // AP5: discoTipo HDD/SSD/NVMe viaja a la prep y se muestra.
  var pHdd = mkPrep({ equipo: { tipo: 'Laptop', marca: 'Dell', modelo: 'X', serie: 'S', inventario: '1', cpu: 'Intel Core i5-1135G7', ramGB: 8, discoGB: 1000, discoTipo: 'HDD' } });
  var pSsd = mkPrep({ equipo: { tipo: 'Laptop', marca: 'Dell', modelo: 'X', serie: 'S', inventario: '1', cpu: 'Intel Core i5-1135G7', ramGB: 8, discoGB: 512, discoTipo: 'SSD' } });
  var pNv = mkPrep({ equipo: { tipo: 'Laptop', marca: 'Dell', modelo: 'X', serie: 'S', inventario: '1', cpu: 'Intel Core i5-1135G7', ramGB: 8, discoGB: 256, discoTipo: 'NVMe' } });
  var backHdd = prepFromCloud(prepToCloudDoc(pHdd));
  console.log('AP5) discoTipo viaja a la nube y vuelve:', prepToCloudDoc(pHdd).equipo.discoTipo === 'HDD' && backHdd.equipo.discoTipo === 'HDD' && prepFromCloud(prepToCloudDoc(pNv)).equipo.discoTipo === 'NVMe', '| tarjeta HDD:', cardHtml(pHdd).includes('Disco: 1000 GB HDD'), '| SSD:', cardHtml(pSsd).includes('Disco: 512 GB SSD'), '| NVMe:', cardHtml(pNv).includes('Disco: 256 GB NVMe'), '| sin datos no hay línea:', cardHtml(mkPrep()).indexOf('Procesador:') === -1);
  // AP6: hardware, versiones, IP y AnyDesk en PDF, WhatsApp y Excel.
  var pFull = mkPrep({ equipo: { tipo: 'Laptop', marca: 'Dell', modelo: 'Inspiron 3501', serie: 'S1', inventario: '100', hostname: 'PC-01', cpu: 'Intel Core i7-10700', ramGB: 16, discoGB: 512, discoTipo: 'SSD', ip: '192.168.1.45', ipTipo: 'Dinámica', anydeskId: '123456789', anydeskAlias: 'Oficina' }, versiones: { so: 'Windows 11 Pro 26H2 (compilación 26200)', antivirus: 'ESET NOD32 Antivirus 18.0.12', chrome: '141.0.7390.65' } });
  var pdfTxt = Buffer.from(await buildPdf(pFull).arrayBuffer()).toString('latin1');
  var waOne = waTextOne(pFull);
  var waAll = waTextAll([pFull]);
  var xlsxTxt = Buffer.from(await buildXlsx([pFull]).arrayBuffer()).toString('latin1');
  var pdfNeed = ['Procesador: Intel Core i7-10700', 'RAM: 16 GB', 'Disco: 512 GB SSD', 'SO: Windows 11 Pro 26H2', 'Antivirus: ESET NOD32 Antivirus 18.0.12', 'Chrome: 141.0.7390.65', 'IP: 192.168.1.45', 'AnyDesk: 123 456 789'];
  console.log('AP6) PDF con hardware, versiones, IP y AnyDesk:', pdfNeed.every(function (s) { return pdfTxt.indexOf(s) !== -1; }), '| WhatsApp individual:', pdfNeed.every(function (s) { return waOne.indexOf(s) !== -1; }) && waOne.indexOf('Versiones detectadas:') !== -1, '| WhatsApp general:', waAll.indexOf('Procesador: Intel Core i7-10700') !== -1 && waAll.indexOf('AnyDesk: 123 456 789') !== -1 && waAll.indexOf('Versiones detectadas:') !== -1, '| Excel con columnas y valores:', ['CPU', 'RAM', 'Disco', 'IP', 'AnyDesk', '16 GB', '512 GB SSD', '192.168.1.45', '123 456 789'].every(function (s) { return xlsxTxt.indexOf(s) !== -1; }));
  // AP7: IP dinámica (dhcp) e IP estática viajan con 'Usar este equipo'.
  detectados = [mkDet2({ id: 'DET-IP-DIN', serie: 'DET-IP-DIN', ip: '192.168.1.45', ipTipo: 'Dinámica' })];
  useDet('DET-IP-DIN');
  document.getElementById('fUser').value = 'Ana';
  document.getElementById('fTec').value = 'Test User';
  document.getElementById('btnAdd')._h.click[0]();
  var savedIpD = state.preparations[state.preparations.length - 1];
  detectados = [mkDet2({ id: 'DET-IP-EST', serie: 'DET-IP-EST', ip: '10.0.0.20', ipTipo: 'Estática' })];
  useDet('DET-IP-EST');
  document.getElementById('fUser').value = 'Luis';
  document.getElementById('fTec').value = 'Test User';
  document.getElementById('btnAdd')._h.click[0]();
  var savedIpE = state.preparations[state.preparations.length - 1];
  console.log('AP7) IP dinámica viaja a la prep:', savedIpD.equipo.ip === '192.168.1.45' && savedIpD.equipo.ipTipo === 'Dinámica', '| tarjeta dinámica:', cardHtml(savedIpD).includes('IP: 192.168.1.45 (Dinámica)'), '| IP estática viaja:', savedIpE.equipo.ip === '10.0.0.20' && savedIpE.equipo.ipTipo === 'Estática', '| tarjeta estática:', cardHtml(savedIpE).includes('IP: 10.0.0.20 (Estática)'), '| nube guarda y restaura IP:', prepFromCloud(prepToCloudDoc(savedIpD)).equipo.ip === '192.168.1.45' && prepFromCloud(prepToCloudDoc(savedIpD)).equipo.ipTipo === 'Dinámica');
  // AP7b: sin IPv4 no se muestra nada; solo IP sin tipo muestra solo la IP;
  // la interfaz por defecto ya la elige el detector: el teléfono toma doc.ip tal cual.
  detectados = [mkDet2({ id: 'DET-IP-NO', serie: 'DET-IP-NO' })];
  useDet('DET-IP-NO');
  document.getElementById('fUser').value = 'Ana';
  document.getElementById('fTec').value = 'Test User';
  document.getElementById('btnAdd')._h.click[0]();
  var savedIpN = state.preparations[state.preparations.length - 1];
  var cardIpSolo = cardHtml(mkPrep({ equipo: { tipo: 'Laptop', marca: 'Dell', modelo: 'X', serie: 'S', inventario: '1', ip: '192.168.1.99' } }));
  detectados = [mkDet2({ id: 'DET-IP-DEF', serie: 'DET-IP-DEF', ip: '192.168.1.45', ipTipo: 'Dinámica' })];
  renderDetectados();
  var detIpHtml = document.getElementById('detList').innerHTML;
  console.log('AP7b) sin IPv4 no se muestra nada:', savedIpN.equipo.ip === '' && cardHtml(savedIpN).indexOf('IP:') === -1, '| solo IP sin tipo muestra solo la IP:', cardIpSolo.includes('IP: 192.168.1.99') && cardIpSolo.indexOf('(Dinámica)') === -1 && cardIpSolo.indexOf('(Estática)') === -1, '| tarjeta del detectado con la IP por defecto:', detIpHtml.includes('IP: 192.168.1.45 (Dinámica)'));
  // AP8: AnyDesk viaja a la prep y se muestra (o no se muestra si no hay).
  detectados = [mkDet2({ id: 'DET-AD', serie: 'DET-AD', anydeskId: '123456789', anydeskAlias: 'Oficina-Gerardo' })];
  renderDetectados();
  var detAdHtml = document.getElementById('detList').innerHTML;
  useDet('DET-AD');
  document.getElementById('fUser').value = 'Ana';
  document.getElementById('fTec').value = 'Test User';
  document.getElementById('btnAdd')._h.click[0]();
  var savedAd = state.preparations[state.preparations.length - 1];
  console.log('AP8) AnyDesk viaja a la prep:', savedAd.equipo.anydeskId === '123456789' && savedAd.equipo.anydeskAlias === 'Oficina-Gerardo', '| agrupado 123 456 789:', anydeskDisplay('123456789') === '123 456 789', '| tarjeta de la prep:', cardHtml(savedAd).includes('AnyDesk: 123 456 789 (Oficina-Gerardo)'), '| tarjeta del detectado:', detAdHtml.includes('AnyDesk: 123 456 789'), '| sin AnyDesk no se muestra nada:', cardHtml(mkPrep()).indexOf('AnyDesk:') === -1);
  // AP9: escritorio (.exe) siempre pide iniciar sesión al abrirse.
  var orderDesk = [];
  var signOutDesk = [];
  global.Cloud.signOut = async function () { orderDesk.push('signOut'); signOutDesk.push(1); };
  global.Cloud.init = async function () { return true; };
  var authCbDesk = null;
  global.Cloud.onAuth = function (cb) { orderDesk.push('onAuth'); authCbDesk = cb; };
  global.Cloud.isInitialized = async function () { return true; };
  global.Desktop = {};
  CLOUD_ENABLED = true;
  _authReady = false;
  await boot();
  await sleep(20);
  var deskBootOk = signOutDesk.length === 1 && orderDesk.join(',') === 'signOut,onAuth' && document.getElementById('loginView').hidden === false && document.getElementById('mainApp').hidden === true && document.getElementById('appHeader').hidden === true;
  await authCbDesk(null);
  console.log('AP9) escritorio: signOut al arrancar antes de escuchar auth:', deskBootOk, '| muestra el login, no la interfaz:', document.getElementById('loginView').hidden === false && document.getElementById('mainApp').hidden === true && _authReady === true, '| huella y recordar ocultos:', document.getElementById('btnBiometric').hidden === true && document.getElementById('loginRememberRow').hidden === true && document.getElementById('loginRemember').checked === false);
  // AP9b: si el signOut falla, igual muestra el login sin romperse.
  orderDesk.length = 0; signOutDesk.length = 0;
  global.Cloud.signOut = async function () { signOutDesk.push(1); throw new Error('sin red'); };
  _authReady = false;
  await boot();
  await sleep(20);
  await authCbDesk(null);
  console.log('AP9b) escritorio: si signOut falla, igual llega al login:', signOutDesk.length === 1 && document.getElementById('loginView').hidden === false && _authReady === true);
  global.Desktop = undefined;
  // AP9c: teléfono sin Desktop: sin signOut forzado, huella y recordar como siempre.
  var signOutTel = [];
  global.Cloud.signOut = async function () { signOutTel.push(1); };
  global.Capacitor = { Plugins: { NativeBiometric: { isAvailable: async function () { return { isAvailable: true }; }, getCredentials: async function () { return { username: 'u', password: 'p' }; } } } };
  _authReady = false;
  await boot();
  await sleep(30);
  await authCbDesk(null);
  console.log('AP9c) teléfono: sin signOut forzado:', signOutTel.length === 0, '| huella visible con credencial guardada:', document.getElementById('btnBiometric').hidden === false, '| recordar visible:', document.getElementById('loginRememberRow').hidden === false, '| y llega al login:', document.getElementById('loginView').hidden === false && _authReady === true);
  global.Capacitor = undefined;
  global.Cloud.signOut = async function () {};


  // AQ0: reportDetected (firebase.js) usa machineId como id y resetea usado/detectadoEn.
  var repMatch = fb.match(/async function reportDetected\(info\) \{[\s\S]*?\n\}/);
  var __savedDet = [];
  var reportDetected = repMatch ? new Function('db', 'doc', 'setDoc', repMatch[0] + '\nreturn reportDetected;')({}, function (db, col, id) { return { col: col, id: id }; }, async function (ref, data, opts) { __savedDet.push([ref, data, opts]); }) : null;
  var beforeAq = Date.now();
  await reportDetected({ machineId: 'SERIE123', hostname: 'PC-01', marca: 'HP', modelo: 'EliteDesk', serie: 'SERIE123', detectadoEn: beforeAq - 86400000, detectadoPor: 'Gerardo', usado: true });
  var saveAq1 = __savedDet[0];
  __savedDet.length = 0;
  await reportDetected({ machineId: 'PC-02-AABBCCDDEEFF', hostname: 'PC-02', serie: '', detectadoEn: beforeAq - 3600000, usado: true });
  var saveAq2 = __savedDet[0];
  __savedDet.length = 0;
  await reportDetected({ hostname: 'PC-03', serie: 'SERIE789', detectadoEn: beforeAq - 60000 });
  var saveAq3 = __savedDet[0];
  __savedDet.length = 0;
  await reportDetected({ hostname: 'PC-04', detectadoEn: 1700000000000 });
  var saveAq4 = __savedDet[0];
  console.log('AQ0) reportDetected extraído:', !!reportDetected, '| machineId por serie como id:', saveAq1[0].id === 'SERIE123' && saveAq1[1].machineId === 'SERIE123', '| machineId por hostname+MAC como id:', saveAq2[0].id === 'PC-02-AABBCCDDEEFF', '| sin machineId, serie como id:', saveAq3[0].id === 'SERIE789', '| sin serie, hostname+detectadoEn:', saveAq4[0].id === 'PC-04-1700000000000', '| re-detectar resetea usado:', saveAq1[1].usado === false && saveAq2[1].usado === false, '| detectadoEn es ahora:', saveAq1[1].detectadoEn >= beforeAq && saveAq1[1].detectadoEn <= Date.now(), '| merge:', saveAq1[2] && saveAq1[2].merge === true, '| bundle trae el machineId:', fbBundle.includes('machineId'));
  // AQ1: el botón se bloquea con detección pendiente de ESTA máquina.
  doLogin('usuario');
  CLOUD_ENABLED = true;
  cloudUser = { uid: 'u1', email: 'test@checklist.local', nombre: 'Test User' };
  var btnAq = document.getElementById('btnDetectar');
  global.Desktop = { getMachineId: async function () { return 'SERIE-AAA'; }, detect: async function () { return {}; } };
  await loadMachineId();
  var midOk = machineId === 'SERIE-AAA';
  detectados = [{ id: 'SERIE-AAA', hostname: 'PC-AAA', marca: 'HP', modelo: 'EliteDesk', serie: 'SERIE-AAA', tipo: 'Desktop', detectadoEn: Date.now() - 60000, detectadoPor: 'Gerardo', usado: false }];
  renderDetectados();
  var blockedOk = btnAq.disabled === true && btnAq.innerHTML.indexOf('Equipo detectado') !== -1;
  // AQ2: la detección de OTRA máquina no bloquea esta.
  detectados = [{ id: 'PC-OTRA-AABBCCDDEEFF', hostname: 'PC-OTRA', marca: 'Dell', modelo: 'OptiPlex', serie: 'OTRA1', tipo: 'Desktop', detectadoEn: Date.now() - 60000, detectadoPor: 'Alejandro', usado: false }];
  renderDetectados();
  var otherOk = btnAq.disabled === false && btnAq.innerHTML.indexOf('Equipo detectado') === -1;
  console.log('AQ1) machineId de esta PC:', midOk, '| pendiente de esta máquina bloquea el botón:', blockedOk, '| AQ2) pendiente de otra máquina no bloquea:', otherOk);
  // AQ3: al usar o descartar la entrada, el botón se vuelve a habilitar.
  detectados = [{ id: 'SERIE-AAA', hostname: 'PC-AAA', marca: 'HP', modelo: 'EliteDesk', serie: 'SERIE-AAA', tipo: 'Desktop', detectadoEn: Date.now() - 60000, detectadoPor: 'Gerardo', usado: false }];
  renderDetectados();
  var wasBlocked = btnAq.disabled === true;
  detectados = [{ id: 'SERIE-AAA', hostname: 'PC-AAA', marca: 'HP', modelo: 'EliteDesk', serie: 'SERIE-AAA', tipo: 'Desktop', detectadoEn: Date.now() - 60000, detectadoPor: 'Gerardo', usado: true }];
  renderDetectados();
  var unblockedUse = btnAq.disabled === false && btnAq.innerHTML.indexOf('Equipo detectado') === -1;
  detectados = [{ id: 'SERIE-AAA', hostname: 'PC-AAA', marca: 'HP', modelo: 'EliteDesk', serie: 'SERIE-AAA', tipo: 'Desktop', detectadoEn: Date.now() - 60000, detectadoPor: 'Gerardo', usado: false }];
  renderDetectados();
  detectados = [];
  renderDetectados();
  var unblockedDel = btnAq.disabled === false && btnAq.innerHTML.indexOf('Detectar este equipo') !== -1;
  console.log('AQ3) bloqueado antes de usar:', wasBlocked, '| al marcar usado se habilita:', unblockedUse, '| al descartar se habilita y vuelve la etiqueta:', unblockedDel);
  // AQ4: con el botón bloqueado, hacer clic no vuelve a detectar; desbloqueado sí.
  var repAq = [];
  global.Cloud.reportDetected = async function (info) { repAq.push(info); };
  detectados = [{ id: 'SERIE-AAA', hostname: 'PC-AAA', marca: 'HP', modelo: 'EliteDesk', serie: 'SERIE-AAA', tipo: 'Desktop', detectadoEn: Date.now() - 60000, detectadoPor: 'Gerardo', usado: false }];
  renderDetectados();
  document.getElementById('btnDetectar')._h.click[0]();
  await sleep(20);
  var noRedetect = repAq.length === 0;
  detectados = [];
  renderDetectados();
  document.getElementById('btnDetectar')._h.click[0]();
  await sleep(20);
  var redetectOk = repAq.length === 1 && repAq[0].detectadoPor === 'Test User';
  console.log('AQ4) bloqueado no re-detecta:', noRedetect, '| desbloqueado sí detecta con el técnico:', redetectOk);
  // AQ5: sin getMachineId (o si falla) no hay bloqueo y nada se rompe.
  global.Desktop = { detect: async function () { return {}; } };
  await loadMachineId();
  var noMid = machineId === null;
  detectados = [{ id: 'SERIE-AAA', hostname: 'PC-AAA', marca: 'HP', modelo: 'EliteDesk', serie: 'SERIE-AAA', tipo: 'Desktop', detectadoEn: Date.now() - 60000, detectadoPor: 'Gerardo', usado: false }];
  renderDetectados();
  var noBlockNoMid = btnAq.disabled === false;
  global.Desktop = { getMachineId: async function () { throw new Error('sin detector'); }, detect: async function () { return {}; } };
  await loadMachineId();
  var noMidErr = machineId === null;
  renderDetectados();
  var noBlockErr = btnAq.disabled === false;
  global.Desktop = undefined;
  console.log('AQ5) sin getMachineId no hay machineId:', noMid, '| y no bloquea:', noBlockNoMid, '| si getMachineId falla no hay machineId:', noMidErr, '| y no bloquea ni rompe:', noBlockErr);
  // AQ6: la suscripción de detectados actualiza el botón al llegar cambios.
  global.Desktop = { getMachineId: async function () { return 'SERIE-AAA'; }, detect: async function () { return {}; } };
  var detCbAq = null;
  global.Cloud.getUserDoc = async function () { return { activo: true, rol: 'usuario', nombre: 'Test User', email: 'test@checklist.local' }; };
  global.Cloud.isInitialized = async function () { return true; };
  global.Cloud.getAllRenta = async function () { return []; };
  global.Cloud.upsertRenta = async function () {};
  global.Cloud.getAllPreparations = async function () { return []; };
  global.Cloud.upsertPrep = async function () {};
  global.Cloud.subscribeRenta = function () { return function () {}; };
  global.Cloud.subscribePreparations = function () { return function () {}; };
  global.Cloud.subscribeDetectados = function (cb) { detCbAq = cb; return function () {}; };
  global.Cloud.subscribePresence = function () { return function () {}; };
  global.Cloud.subscribeChat = function () { return function () {}; };
  global.Cloud.subscribeDm = function () { return function () {}; };
  global.Cloud.heartbeat = function () {};
  global.Cloud.pruneChat = function () {};
  global.Cloud.clearPresence = function () {};
  global.Cloud.listUsers = async function () { return []; };
  localStorage.setItem('checklist-soporte-migrado-v2:u1', '1');
  localStorage.setItem('checklist-soporte-migrado-preps-v1:u1', '1');
  state.preparations = [];
  state.renta = [];
  await onAuthChanged({ uid: 'u1', email: 'test@checklist.local' });
  await sleep(20);
  var subOk = typeof detCbAq === 'function' && machineId === 'SERIE-AAA';
  detCbAq([{ id: 'SERIE-AAA', hostname: 'PC-AAA', marca: 'HP', modelo: 'EliteDesk', serie: 'SERIE-AAA', tipo: 'Desktop', detectadoEn: Date.now(), detectadoPor: 'Gerardo', usado: false }]);
  var subBlocked = btnAq.disabled === true && btnAq.innerHTML.indexOf('Equipo detectado') !== -1;
  detCbAq([]);
  var subUnblocked = btnAq.disabled === false;
  global.Desktop = undefined;
  console.log('AQ6) suscripción llega y machineId cargado:', subOk, '| pendiente de esta máquina bloquea:', subBlocked, '| al vaciarse se desbloquea:', subUnblocked);


  // AR0: versión 2.3.5 en los lugares visibles y 0 de 2.3.4 en todo el html.
  var n252 = (html.match(/2\.5\.2/g) || []).length;
  console.log('AR0) versión 2.5.2 visible:', html.includes('Versión 2.5.2') && html.includes('Versión: 2.5.2'), '| 0 de 2.5.0:', !html.includes('2.5.0'), '| ocurrencias 2.5.2:', n252 === 2);
  // AR1: formReady / botón Guardar (2.3.5, sin cambios): solo modelo, serie o
  // usuario habilitan Guardar. Marca, inventario, hostname, área, correo y
  // analista NO habilitan por sí solos: si Gerardo llenó solo esos campos,
  // el botón sigue deshabilitado con el hint 'Completa al menos el modelo...'.
  // Eso explica el reporte de "no se puede editar/guardar" sin que haya bug.
  var setF = function (id, v) { document.getElementById(id).value = v; };
  var allForm = ['fMarca', 'fModelo', 'fSerie', 'fInv', 'fHostname', 'fTec', 'fUser', 'fArea', 'fCorreo'];
  allForm.forEach(function (id) { setF(id, ''); });
  updateSaveBtn();
  var disVacio = document.getElementById('btnAdd').disabled === true && formReady() === false;
  setF('fMarca', 'HP'); setF('fInv', '100'); setF('fHostname', 'PC-01');
  setF('fArea', 'Soporte'); setF('fCorreo', 'a@empresa.com'); setF('fTec', 'Juan Pérez');
  updateSaveBtn();
  var disSoloOtros = document.getElementById('btnAdd').disabled === true && formReady() === false;
  var hintOtros = document.getElementById('saveHint').textContent.indexOf('Completa al menos el modelo') === 0;
  setF('fModelo', '   '); updateSaveBtn();
  var disBlancos = document.getElementById('btnAdd').disabled === true && formReady() === false;
  setF('fModelo', 'ProBook 440'); updateSaveBtn();
  var enModelo = document.getElementById('btnAdd').disabled === false && formReady() === true;
  setF('fModelo', ''); setF('fSerie', 'S-123'); updateSaveBtn();
  var enSerie = document.getElementById('btnAdd').disabled === false && formReady() === true;
  setF('fSerie', ''); setF('fUser', 'Ana'); updateSaveBtn();
  var enUser = document.getElementById('btnAdd').disabled === false && formReady() === true;
  var hintListo = document.getElementById('saveHint').textContent.indexOf('Datos listos') === 0;
  allForm.forEach(function (id) { setF(id, ''); });
  updateSaveBtn();
  console.log('AR1) Guardar deshabilitado vacío:', disVacio, '| solo marca/inv/host/área/correo/analista:', disSoloOtros, '| hint pide modelo/serie/usuario:', hintOtros, '| solo espacios no habilita:', disBlancos, '| habilita con modelo:', enModelo, '| con serie:', enSerie, '| con usuario:', enUser, '| hint cambia a Datos listos:', hintListo);
  // AR2: NO existe edición de un equipo ya guardado (2.3.5). No hay botón ni
  // handler de edición en la tarjeta: sin data-edit-prep, sin editPrep, sin
  // 'Editar equipo' en el html ni en el script renderizado. Las acciones de
  // la tarjeta son solo: Listo, Entregado, Quitar listo, Reabrir, + Punto
  // extra, PDF, ¿Qué falta?, Excel, WhatsApp, Resumen IA, correo, Reasignar
  // (admin) y Eliminar (admin). Lo único que cambia la asignación es
  // Reasignar, que solo cambia el nombre y BORRA área y correo (doReassign).
  var noEditHtml = html.indexOf('data-edit-prep') === -1 && html.indexOf('editPrep') === -1 && html.indexOf('Editar equipo') === -1;
  var noEditSrc = SRC.indexOf('data-edit-prep') === -1 && SRC.indexOf('editPrep') === -1 && SRC.indexOf('Editar equipo') === -1;
  var cardHas = function (a) { return SRC.indexOf(a) !== -1; };
  var cardActions = cardHas("data-ready=") && cardHas("data-deliver=") && cardHas("data-unready=") && cardHas("data-reopen=") && cardHas("data-add-extra=") && cardHas("data-pdf=") && cardHas("data-xlsx=") && cardHas("data-wa=") && cardHas("data-mail=") && cardHas("data-reassign=") && cardHas("data-del-prep=");
  var reassignWipes = SRC.indexOf("prep.usuario.nombre = a; prep.usuario.area = ''; prep.usuario.correo = '';") !== -1;
  console.log('AR2) sin edición en html:', noEditHtml, '| sin edición en script:', noEditSrc, '| acciones de tarjeta completas (sin editar):', cardActions, '| Reasignar cambia solo nombre y borra área/correo:', reassignWipes);

  // AS0-AS3: camino 'Usar este equipo' (2.3.5). La prueba de escritura de
  // la 2.3.4 solo abrió el formulario EN BLANCO (btnShowNew); aquí se
  // recorre Detectar -> panel -> 'Usar este equipo' -> formulario, con
  // un target realista hecho a mano (closest/getAttribute), NO fakeClick:
  // el clic se dispara por el handler de #detList como en AN1/AO2.
  // OJO: en este harness invocar _h.click[0]() ejecuta el handler aunque
  // el botón esté disabled, así que la habilitación de Guardar se
  // comprueba leyendo btnAdd.disabled, no por que el clic funcione.
  doLogin('usuario');
  CLOUD_ENABLED = true;
  cloudUser = { uid: 'u1', email: 'test@checklist.local', nombre: 'Test User' };
  var markedAS = [];
  global.Cloud.markDetectadoUsado = async function (id) { markedAS.push(id); };
  var upAS = [];
  global.Cloud.upsertPrep = async function (d) { upAS.push(d); };
  var detAS = { id: 'AS-DET', hostname: 'PC-AS', marca: 'HP', modelo: 'EliteDesk 800', serie: 'AS-DET', cpu: 'Intel Core i7-10700', ramGB: 16, discoGB: 512, so: 'Windows 11 Pro', tipo: 'Desktop', detectadoEn: Date.now() - 60000, detectadoPor: 'Gerardo', usado: false, checks: { t18: true, t8: 'Office 365' }, detalles: { officeDetectado: true, escritorioRutas: ['C:\\Users\\gerardo\\Desktop', 'C:\\Users\\gerardo\\OneDrive - Empresa\\Desktop'], atajosVistos: 3 }, versiones: { so: 'Windows 11 Pro 26H2 (compilación 26200)' } };
  ['fTipo', 'fMarca', 'fModelo', 'fSerie', 'fInv', 'fHostname', 'fTec', 'fUser', 'fArea', 'fCorreo'].forEach(function (id) { document.getElementById(id).value = ''; });
  window._detectedChecks = null; window._detectedDetalles = null; window._detectedVersiones = null; window._detectedHardware = null;
  document.getElementById('detBox').hidden = false;
  document.getElementById('newBox').hidden = true;
  detectados = [detAS];
  renderDetectados();
  document.getElementById('detList')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-det-use]' ? { getAttribute: function () { return 'AS-DET'; } } : null; } } });
  var asFilled = document.getElementById('fTipo').value === 'Desktop' && document.getElementById('fMarca').value === 'HP' && document.getElementById('fModelo').value === 'EliteDesk 800' && document.getElementById('fSerie').value === 'AS-DET' && document.getElementById('fHostname').value === 'PC-AS';
  var asPanels = document.getElementById('detBox').hidden === true && document.getElementById('newBox').hidden === false;
  var asStash = window._detectedChecks && window._detectedChecks.t18 === true && window._detectedChecks.t8 === 'Office 365' && window._detectedDetalles && window._detectedDetalles.officeDetectado === true && window._detectedVersiones && window._detectedVersiones.so === 'Windows 11 Pro 26H2 (compilación 26200)' && window._detectedHardware && window._detectedHardware.cpu === 'Intel Core i7-10700';
  var asMarked = markedAS.indexOf('AS-DET') !== -1;
  var asSaveOn = document.getElementById('btnAdd').disabled === false && formReady() === true;
  var asHint = document.getElementById('saveHint').textContent.indexOf('Datos listos') === 0;
  console.log('AS0) Usar llena el formulario:', asFilled, '| cierra detBox y abre newBox:', asPanels, '| stash checks/detalles/versiones/hardware:', asStash, '| marca usado:', asMarked, '| Guardar habilitado con modelo/serie detectados:', asSaveOn, '| hint Datos listos:', asHint);
  // AS1: los campos de inventario, usuario, área y correo aceptan tecleo
  // y lo conservan. En el html son <input> planos, sin disabled ni
  // readonly; en el harness el tecleo se modela asignando .value y, para
  // fUser, disparando su listener 'input' real (updateSaveBtn).
  document.getElementById('fInv').value = 'INV-777';
  document.getElementById('fUser').value = 'Ana Pérez';
  document.getElementById('fArea').value = 'Soporte';
  document.getElementById('fCorreo').value = 'ana@empresa.com';
  document.getElementById('fUser')._h.input[0]();
  var asTyped = document.getElementById('fInv').value === 'INV-777' && document.getElementById('fUser').value === 'Ana Pérez' && document.getElementById('fArea').value === 'Soporte' && document.getElementById('fCorreo').value === 'ana@empresa.com';
  var asNotDis = ['fInv', 'fUser', 'fArea', 'fCorreo'].every(function (id) { return document.getElementById(id).disabled === false; });
  var asNotDisHtml = ['fInv', 'fUser', 'fArea', 'fCorreo'].every(function (id) { return html.indexOf('id="' + id + '" disabled') === -1 && html.indexOf('id="' + id + '" readonly') === -1; });
  var asSaveStill = document.getElementById('btnAdd').disabled === false && formReady() === true;
  console.log('AS1) inventario/usuario/área/correo aceptan tecleo y lo conservan:', asTyped, '| ninguno deshabilitado:', asNotDis, '| sin disabled/readonly en el html:', asNotDisHtml, '| Guardar sigue habilitado tras teclear:', asSaveStill);
  // AS2: un render() disparado por la suscripción de detectados NO borra
  // lo tecleado ni cierra el formulario. Se usa el callback vivo de la
  // suscripción (detCbAq, de AQ6): llega el eco de usado=true, que
  // re-renderiza detList, y luego render() completo.
  var asCbLive = typeof detCbAq === 'function';
  if (asCbLive) detCbAq([Object.assign({}, detAS, { usado: true })]);
  var asDetGone = document.getElementById('detList').innerHTML.indexOf('PC-AS') === -1;
  render();
  var asTypedKept = document.getElementById('fInv').value === 'INV-777' && document.getElementById('fUser').value === 'Ana Pérez' && document.getElementById('fArea').value === 'Soporte' && document.getElementById('fCorreo').value === 'ana@empresa.com' && document.getElementById('fModelo').value === 'EliteDesk 800' && document.getElementById('fSerie').value === 'AS-DET';
  var asFormOpen = document.getElementById('newBox').hidden === false && document.getElementById('detBox').hidden === true;
  var asSaveKept = document.getElementById('btnAdd').disabled === false;
  console.log('AS2) callback de suscripción vivo:', asCbLive, '| el usado desaparece del panel:', asDetGone, '| lo tecleado y lo detectado se conservan tras render():', asTypedKept, '| el formulario sigue abierto:', asFormOpen, '| Guardar sigue habilitado:', asSaveKept);
  // AS3: Guardar conserva inventario/usuario/área/correo + autoDetectado.
  // Se vuelve a comprobar btnAdd.disabled ANTES de pulsar: el handler
  // del harness no respeta disabled, así que el clic solo no probaría nada.
  var asCanSave = document.getElementById('btnAdd').disabled === false;
  var nBeforeAS = state.preparations.length;
  upAS.length = 0;
  document.getElementById('btnAdd')._h.click[0]();
  var savedAS = state.preparations[state.preparations.length - 1];
  var asSaved = state.preparations.length === nBeforeAS + 1 && !!savedAS && savedAS.equipo.inventario === 'INV-777' && savedAS.usuario.nombre === 'Ana Pérez' && savedAS.usuario.area === 'Soporte' && savedAS.usuario.correo === 'ana@empresa.com' && savedAS.equipo.modelo === 'EliteDesk 800' && savedAS.equipo.serie === 'AS-DET' && savedAS.equipo.hostname === 'PC-AS' && savedAS.checks.t18 === true && savedAS.checks.t8 === 'Office 365' && savedAS.autoDetectado.join(',') === 't8,t18';
  var asCloud = upAS.length === 1 && upAS[0].autoDetectado.join(',') === 't8,t18' && upAS[0].equipo.inventario === 'INV-777' && upAS[0].usuario.correo === 'ana@empresa.com';
  var asStashClean = window._detectedChecks === null && window._detectedDetalles === null && window._detectedVersiones === null && window._detectedHardware === null;
  var asClosed = document.getElementById('newBox').hidden === true;
  console.log('AS3) Guardar habilitado antes de pulsar:', asCanSave, '| guardado conserva inventario/usuario/área/correo + autoDetectado:', asSaved, '| sube a la nube igual:', asCloud, '| stash limpio tras guardar:', asStashClean, '| el formulario se cierra:', asClosed);
  // AS4: línea 'Escritorio revisado' en la tarjeta del detectado.
  var mkDetAS = function (over) { return Object.assign({ id: 'AS-ESC', hostname: 'PC-ESC', marca: 'HP', modelo: 'EliteDesk', serie: 'AS-ESC', tipo: 'Desktop', detectadoEn: Date.now(), detectadoPor: 'Gerardo', usado: false }, over || {}); };
  detectados = [mkDetAS({ detalles: { escritorioRutas: ['C:\\Users\\gerardo\\Desktop', 'C:\\Users\\gerardo\\OneDrive - Empresa\\Desktop'], atajosVistos: 3 } })];
  renderDetectados();
  var hEscA = document.getElementById('detList').innerHTML;
  var asEscA = hEscA.indexOf('Escritorio revisado: C:\\Users\\gerardo\\Desktop, C:\\Users\\gerardo\\OneDrive - Empresa\\Desktop') !== -1 && hEscA.indexOf('· 3 atajos vistos') !== -1;
  detectados = [mkDetAS({ detalles: { escritorioRutas: ['D:\\Escritorio'] } })];
  renderDetectados();
  var hEscB = document.getElementById('detList').innerHTML;
  var asEscB = hEscB.indexOf('Escritorio revisado: D:\\Escritorio') !== -1 && hEscB.indexOf('atajos vistos') === -1;
  detectados = [mkDetAS({ detalles: { atajosVistos: 5 } })];
  renderDetectados();
  var hEscC = document.getElementById('detList').innerHTML;
  var asEscC = hEscC.indexOf('Atajos vistos: 5') !== -1 && hEscC.indexOf('Escritorio revisado') === -1;
  detectados = [mkDetAS({ detalles: { escritorioRutas: ['C:\\Users\\x\\Desktop'], atajosVistos: 0 } })];
  renderDetectados();
  var hEscD = document.getElementById('detList').innerHTML;
  var asEscD = hEscD.indexOf('Escritorio revisado: C:\\Users\\x\\Desktop') !== -1 && hEscD.indexOf('· 0 atajos vistos') !== -1;
  console.log('AS4) rutas + conteo:', asEscA, '| solo rutas (sin conteo):', asEscB, '| solo conteo:', asEscC, '| conteo 0 también se muestra:', asEscD);
  // AS5: sin esos campos no hay línea; helper y campos existen en el código.
  detectados = [mkDetAS({ detalles: {} })];
  renderDetectados();
  var hEscE = document.getElementById('detList').innerHTML;
  var asEscE = hEscE.indexOf('Escritorio revisado') === -1 && hEscE.indexOf('atajos vistos') === -1;
  detectados = [mkDetAS({ detalles: { escritorioRutas: [] } })];
  renderDetectados();
  var hEscF = document.getElementById('detList').innerHTML;
  var asEscF = hEscF.indexOf('Escritorio revisado') === -1 && hEscF.indexOf('atajos vistos') === -1;
  var asEscStatic = SRC.indexOf('escritorioLine') !== -1 && SRC.indexOf('escritorioRutas') !== -1 && SRC.indexOf('atajosVistos') !== -1 && html.indexOf('escritorioLine(d)') !== -1;
  console.log('AS5) sin detalles no hay línea:', asEscE, '| array vacío no hay línea:', asEscF, '| helper y campos en el código:', asEscStatic);

  // AT: serie nueva versión. Clic realista hecho a mano (sin fakeClick):
  // el botón lleva data-prep y su propio atributo; closest devuelve el
  // botón solo para ese selector y hasAttribute solo para ese atributo.
  function realClick(attr, prepId, itemId) {
    var btn = {
      getAttribute: function (a) { if (a === 'data-prep') return prepId; if (a === attr) return (itemId === undefined ? prepId : itemId); return null; },
      hasAttribute: function (a) { return a === attr; },
      closest: function (sel) { if (sel === '[' + attr + ']') return btn; if (sel === '[data-prep]') return btn; return null; },
      classList: { contains: function () { return false; } }
    };
    document.getElementById('list')._h.click[0]({ target: btn });
  }
  function mkPrepAT(over) { return mkPrep(Object.assign({ id: 'at2' }, over || {})); }
  // AT0: redes y fuente del SO (helpers).
  var redesVacio = redesText({}) === '' && redesLine({}) === '' && redesText({ redes: [] }) === '' && redesText({ redes: [{ nombre: 'Wi-Fi', ip: '' }] }) === '';
  var redesDos = redesText({ redes: [{ nombre: 'Wi-Fi', ip: '192.168.1.45', ipTipo: 'Dinámica' }, { nombre: 'Ethernet', ip: '10.0.0.20', ipTipo: 'Estática' }] });
  var redesOk = redesDos === 'Wi-Fi: 192.168.1.45 (Dinámica) · Ethernet: 10.0.0.20 (Estática)' && redesLine({ redes: [{ ip: '192.168.1.99' }] }) === 'Redes: 192.168.1.99';
  var osfOk = osFuenteLine({ detalles: { osFuente: 'registro' } }) === 'SO detectado por: Registro de Windows' && osFuenteLine({ detalles: { osFuente: 'cim' } }) === 'SO detectado por: CIM (WMI)' && osFuenteLine({ detalles: { osFuente: 'computerinfo' } }) === 'SO detectado por: Get-ComputerInfo' && osFuenteLine({ detalles: { osFuente: 'si' } }) === 'SO detectado por: Información del sistema' && osFuenteLine({ detalles: {} }) === '' && osFuenteLine({}) === '';
  console.log('AT0) redes: vacío nada:', redesVacio, '| dos redes con tipo:', redesOk, '| fuente del SO legible:', osfOk);
  // AT1: redes y fuente del SO en la tarjeta del detectado; viajan con 'Usar este equipo'.
  doLogin('usuario');
  CLOUD_ENABLED = true;
  cloudUser = { uid: 'u1', email: 'test@checklist.local', nombre: 'Test User' };
  var upAT = [];
  global.Cloud.upsertPrep = async function (d) { upAT.push(d); };
  global.Cloud.markDetectadoUsado = async function () {};
  var detAT = { id: 'AT-DET', hostname: 'PC-AT', marca: 'HP', modelo: 'EliteDesk 800', serie: 'AT-DET', tipo: 'Desktop', detectadoEn: Date.now() - 60000, detectadoPor: 'Gerardo', usado: false, checks: { t18: true }, detalles: { osFuente: 'registro' }, versiones: {}, ip: '192.168.1.45', ipTipo: 'Dinámica', redes: [{ nombre: 'Wi-Fi', ip: '192.168.1.45', ipTipo: 'Dinámica' }, { nombre: 'Ethernet', ip: '10.0.0.20', ipTipo: 'Estática' }] };
  detectados = [detAT];
  renderDetectados();
  var detHtmlAT = document.getElementById('detList').innerHTML;
  var detCardOk = detHtmlAT.indexOf('Redes: Wi-Fi: 192.168.1.45 (Dinámica) · Ethernet: 10.0.0.20 (Estática)') !== -1 && detHtmlAT.indexOf('SO detectado por: Registro de Windows') !== -1;
  document.getElementById('detList')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-det-use]' ? { getAttribute: function () { return 'AT-DET'; } } : null; } } });
  var stashRedesOk = window._detectedHardware && Array.isArray(window._detectedHardware.redes) && window._detectedHardware.redes.length === 2 && window._detectedHardware.redes[0].ip === '192.168.1.45';
  document.getElementById('fUser').value = 'Ana';
  document.getElementById('fTec').value = 'Test User';
  upAT.length = 0;
  document.getElementById('btnAdd')._h.click[0]();
  var savedAT = state.preparations[state.preparations.length - 1];
  var savedRedesOk = !!savedAT && Array.isArray(savedAT.equipo.redes) && savedAT.equipo.redes.length === 2 && savedAT.equipo.redes[1].nombre === 'Ethernet';
  var cloudRedesOk = upAT.length === 1 && Array.isArray(upAT[0].equipo.redes) && upAT[0].equipo.redes.length === 2;
  var cardAT = cardHtml(savedAT);
  var pdfAT = Buffer.from(await buildPdf(savedAT).arrayBuffer()).toString('latin1');
  var waOneAT = waTextOne(savedAT);
  var waAllAT = waTextAll([savedAT]);
  var xlsxAT = Buffer.from(await buildXlsx([savedAT]).arrayBuffer()).toString('latin1');
  var redesEnSalidas = cardAT.indexOf('Redes: Wi-Fi: 192.168.1.45 (Dinámica)') !== -1 && pdfAT.indexOf('Redes: Wi-Fi: 192.168.1.45') !== -1 && waOneAT.indexOf('Redes: Wi-Fi: 192.168.1.45 (Dinámica)') !== -1 && waAllAT.indexOf('Redes: Wi-Fi: 192.168.1.45 (Dinámica)') !== -1 && xlsxAT.indexOf('Redes') !== -1 && xlsxAT.indexOf('192.168.1.45') !== -1 && xlsxAT.indexOf('10.0.0.20') !== -1;
  var sinRedesOk = cardHtml(mkPrep()).indexOf('Redes:') === -1 && waTextOne(mkPrep()).indexOf('Redes:') === -1;
  console.log('AT1) detectado muestra redes y fuente:', detCardOk, '| stash con redes:', stashRedesOk, '| prep guarda redes:', savedRedesOk, '| nube con redes:', cloudRedesOk, '| tarjeta/PDF/WA/Excel con redes:', redesEnSalidas, '| sin redes no se muestra nada:', sinRedesOk);
  // AT2: N/A por punto: no cuenta en el avance, no lo pide '¿Qué falta?',
  // se muestra en tarjeta/PDF/WhatsApp/Excel y se deshace; viaja a la nube.
  var reqAT = requiredItems(mkPrepAT());
  var halfChecks = {};
  reqAT.slice(0, 11).forEach(function (it) { halfChecks[it.id] = true; });
  var pNA = mkPrepAT({ checks: Object.assign({}, halfChecks) });
  var basePct = progress(pNA);
  var uncheckedId = reqAT[11].id;
  var uncheckedTxt = reqAT[11].text;
  pNA.naItems = {}; pNA.naItems[uncheckedId] = true;
  var pctNaUnchecked = progress(pNA);
  var checkedId = reqAT[0].id;
  pNA.naItems[checkedId] = true;
  var pctNaChecked = progress(pNA);
  var faltaOk = faltaPrompt(pNA).indexOf(uncheckedTxt) === -1 && faltaPrompt(mkPrepAT({ checks: halfChecks })).indexOf(uncheckedTxt) !== -1;
  var rtNA = prepFromCloud(prepToCloudDoc(pNA));
  var syncNaOk = rtNA.naItems && rtNA.naItems[uncheckedId] === true && rtNA.naItems[checkedId] === true;
  state.preparations.push(mkPrepAT({ id: 'at2b', checks: Object.assign({}, halfChecks) }));
  realClick('data-na', 'at2b', uncheckedId);
  var pNA2 = state.preparations.find(function (p) { return p.id === 'at2b'; });
  var cardNaOk = cardHtml(pNA2).indexOf('N/A') !== -1 && cardHtml(pNA2).indexOf(uncheckedTxt) !== -1;
  var pctAfterClick = progress(pNA2);
  realClick('data-na', 'at2b', uncheckedId);
  var undoOk = !pNA2.naItems[uncheckedId] && cardHtml(pNA2).indexOf('badge-na') === -1;
  var pdfNa = Buffer.from(await buildPdf(pNA).arrayBuffer()).toString('latin1');
  var waNa = waTextOne(pNA);
  var xlsxNa = Buffer.from(await buildXlsx([pNA]).arrayBuffer()).toString('latin1');
  var naEnSalidas = pdfNa.indexOf('[N/A] ' + uncheckedTxt) !== -1 && waNa.indexOf('No aplica (N/A):') !== -1 && waNa.indexOf(uncheckedTxt) !== -1 && xlsxNa.indexOf('Puntos N/A') !== -1 && xlsxNa.indexOf(uncheckedTxt) !== -1;
  console.log('AT2) avance base:', basePct === Math.round(11 / reqAT.length * 100), '| N/A sin marcar sube el avance:', pctNaUnchecked === Math.round(11 / (reqAT.length - 1) * 100), '| N/A marcado baja numerador y denominador:', pctNaChecked === Math.round(10 / (reqAT.length - 2) * 100), '| ¿Qué falta? no lo pide:', faltaOk, '| sincroniza N/A:', syncNaOk, '| tarjeta con badge N/A:', cardNaOk, '| clic N/A cambia el avance:', pctAfterClick === Math.round(11 / (reqAT.length - 1) * 100), '| tocar de nuevo lo deshace:', undoOk, '| PDF/WA/Excel con N/A:', naEnSalidas);
  // AT3: quitar por punto: se oculta, no cuenta y se restaura; viaja a la nube.
  var pQ = mkPrepAT({ id: 'at3', checks: Object.assign({}, halfChecks) });
  var qTxt = reqAT[11].text;
  var qId = reqAT[11].id;
  var baseQ = progress(pQ);
  state.preparations.push(pQ);
  realClick('data-remove-item', 'at3', qId);
  var pQ2 = state.preparations.find(function (p) { return p.id === 'at3'; });
  var cardQ = cardHtml(pQ2);
  var quitOk = cardQ.indexOf(qTxt) === -1 && cardQ.indexOf('Puntos quitados: 1') !== -1 && cardQ.indexOf('Restaurar') !== -1;
  var pctQ = progress(pQ2);
  var rtQ = prepFromCloud(prepToCloudDoc(pQ2));
  var syncQOk = rtQ.removedItems && rtQ.removedItems.indexOf(qId) !== -1;
  realClick('data-restore-removed', 'at3');
  var restOk = pQ2.removedItems.length === 0 && cardHtml(pQ2).indexOf(qTxt) !== -1 && cardHtml(pQ2).indexOf('Puntos quitados:') === -1;
  console.log('AT3) quitar oculta el punto y avisa:', quitOk, '| avance sin el punto:', pctQ === Math.round(11 / (reqAT.length - 1) * 100), '| base era:', baseQ === Math.round(11 / reqAT.length * 100), '| sincroniza quitados:', syncQOk, '| Restaurar lo devuelve:', restOk);
  // AT4: Compartir avance: texto con porcentaje y faltantes, por WhatsApp y por correo.
  var pAv = mkPrepAT({ id: 'at4', checks: Object.assign({}, halfChecks) });
  state.preparations.push(pAv);
  var txtAv = avanceText(pAv);
  var avTxtOk = txtAv.indexOf(progress(pAv) + '%') !== -1 && txtAv.indexOf('11/' + requiredItems(pAv).length + ' puntos') !== -1 && txtAv.indexOf('Falta:') !== -1 && txtAv.indexOf(reqAT[11].text) !== -1;
  var sharedAv = [];
  global.navigator.share = async function (o) { sharedAv.push(o.text); };
  realClick('data-share-avance', 'at4');
  var waAvOk = sharedAv.length === 1 && sharedAv[0] === txtAv;
  global.location.href = '';
  realClick('data-mail-avance', 'at4');
  var mailAvOk = global.location.href.indexOf('mailto:?subject=Avance') === 0 && decodeURIComponent(global.location.href).indexOf('Falta:') !== -1 && decodeURIComponent(global.location.href).indexOf(progress(pAv) + '%') !== -1;
  var fullAv = mkPrepAT({ id: 'at4f', checks: (function () { var c = {}; requiredItems(mkPrepAT({})).forEach(function (it) { c[it.id] = true; }); return c; })() });
  var noBtnFull = cardHtml(fullAv).indexOf('data-share-avance') === -1 && cardHtml(fullAv).indexOf('data-nolisto') === -1;
  var btnPart = cardHtml(pAv).indexOf('data-share-avance') !== -1 && cardHtml(pAv).indexOf('data-mail-avance') !== -1 && cardHtml(pAv).indexOf('data-nolisto') !== -1;
  console.log('AT4) texto con % y faltantes:', avTxtOk, '| WhatsApp comparte el avance:', waAvOk, '| correo abre mailto con el avance:', mailAvOk, '| a 100% no hay botones:', noBtnFull, '| con avance <100% sí:', btnPart);
  // AT5: 'No listo': marca visible, vuelve a preparación y se limpia al 100% o con 'Listo'.
  var pNL = mkPrepAT({ id: 'at5', readyAt: Date.now() - 60000, checks: Object.assign({}, halfChecks) });
  state.preparations.push(pNL);
  var upNL = [];
  global.Cloud.upsertPrep = async function (d) { upNL.push(d); };
  realClick('data-nolisto', 'at5');
  var nlOk = pNL.readyAt === null && statusOf(pNL) === 'preparacion' && !!pNL.noListo && pNL.noListo.faltan === (requiredItems(pNL).length - 11) && cardHtml(pNL).indexOf('⚠️ No listo — faltan ' + (requiredItems(pNL).length - 11) + ' puntos') !== -1 && filterStatus === 'preparacion';
  var cloudNlOk = upNL.length === 1 && !!upNL[0].noListo && upNL[0].noListo.faltan === (requiredItems(pNL).length - 11);
  var rtNL = prepFromCloud(prepToCloudDoc(pNL));
  var syncNlOk = !!rtNL.noListo && rtNL.noListo.faltan === (requiredItems(pNL).length - 11);
  var lastId = reqAT[reqAT.length - 1].id;
  var remaining = requiredItems(pNL).filter(function (it) { return !pNL.checks[it.id]; });
  remaining.slice(0, remaining.length - 1).forEach(function (it) { pNL.checks[it.id] = true; });
  document.getElementById('list')._h.change[0]({ target: { hasAttribute: function (a) { return a === 'data-check'; }, getAttribute: function (a) { return a === 'data-check' ? lastId : a === 'data-prep' ? 'at5' : null; }, checked: true } });
  var clear100Ok = progress(pNL) === 100 && !pNL.noListo;
  pNL.checks = Object.assign({}, halfChecks);
  pNL.noListo = { fecha: Date.now(), faltan: 10 };
  pNL.readyAt = null;
  realClick('data-ready', 'at5');
  var clearListoOk = !pNL.noListo && !!pNL.readyAt;
  console.log('AT5) No listo vuelve a preparación y marca:', nlOk, '| sube a la nube:', cloudNlOk, '| sincroniza:', syncNlOk, '| se limpia al 100%:', clear100Ok, '| se limpia con Listo:', clearListoOk);
  // AT6: entrega con avance <100%: panel con faltantes; 'Reabrir para
  // completar' no entrega y 'Entregar así' sí; al 100% entrega directo.
  var pE = mkPrepAT({ id: 'at6', readyAt: Date.now() - 60000, checks: Object.assign({}, halfChecks) });
  state.preparations.push(pE);
  var upE = [];
  global.Cloud.upsertPrep = async function (d) { upE.push(d); };
  realClick('data-deliver', 'at6');
  var panelOk = window._deliverConfirmFor === 'at6' && !pE.deliveredAt && upE.length === 0;
  var cardPanel = cardHtml(pE);
  var panelTxtOk = cardPanel.indexOf('Reabrir para completar') !== -1 && cardPanel.indexOf('Entregar así') !== -1 && cardPanel.indexOf(progress(pE) + '%') !== -1 && cardPanel.indexOf(reqAT[11].text) !== -1;
  realClick('data-deliver-reopen', 'at6');
  var reopenOk = !pE.deliveredAt && pE.readyAt === null && statusOf(pE) === 'preparacion' && filterStatus === 'preparacion' && window._deliverConfirmFor !== 'at6';
  realClick('data-ready', 'at6');
  realClick('data-deliver', 'at6');
  var panelAgainOk = window._deliverConfirmFor === 'at6' && !pE.deliveredAt;
  realClick('data-deliver-confirm', 'at6');
  var confirmOk = !!pE.deliveredAt && filterStatus === 'entregado' && upE.length >= 1 && !!upE[upE.length - 1].deliveredAt;
  var pF = mkPrepAT({ id: 'at6f', readyAt: Date.now() - 60000, checks: (function () { var c = {}; requiredItems(mkPrepAT({})).forEach(function (it) { c[it.id] = true; }); return c; })() });
  state.preparations.push(pF);
  window._deliverConfirmFor = null;
  upE.length = 0;
  realClick('data-deliver', 'at6f');
  var directOk = !!pF.deliveredAt && window._deliverConfirmFor !== 'at6f' && upE.length === 1;
  console.log('AT6) Entregado <100% abre el panel sin entregar:', panelOk, '| panel con % y faltantes:', panelTxtOk, '| Reabrir para completar vuelve a preparación:', reopenOk, '| el panel vuelve a salir:', panelAgainOk, '| Entregar así entrega:', confirmOk, '| al 100% entrega directo:', directOk);
  // AT7: 'Reabrir' de un entregado lo devuelve a preparación (limpia
  // deliveredAt Y readyAt), sincronizado y con filtro en preparación.
  var pR = mkPrepAT({ id: 'at7', deliveredAt: Date.now() - 60000, readyAt: Date.now() - 120000, checks: Object.assign({}, halfChecks) });
  state.preparations.push(pR);
  var upR = [];
  global.Cloud.upsertPrep = async function (d) { upR.push(d); };
  realClick('data-reopen', 'at7');
  var reOk = pR.deliveredAt === null && pR.readyAt === null && statusOf(pR) === 'preparacion' && filterStatus === 'preparacion' && upR.length === 1 && upR[0].deliveredAt === null && upR[0].readyAt === null;
  console.log('AT7) Reabrir vuelve a preparación (sin readyAt):', reOk);
  // AT8: la cadena de prepId del handler de #list incluye los botones nuevos.
  var chainOk = ['data-na', 'data-remove-item', 'data-restore-removed', 'data-share-avance', 'data-mail-avance', 'data-nolisto', 'data-deliver-reopen', 'data-deliver-confirm'].every(function (a) { return SRC.indexOf("q('" + a + "')") !== -1; });
  var btnsOk = ['data-share-avance', 'data-mail-avance', 'data-nolisto', 'data-deliver-reopen', 'data-deliver-confirm'].every(function (a) { return SRC.indexOf(a + '="') !== -1; });
  console.log('AT8) cadena prepId con botones nuevos:', chainOk, '| botones en el código:', btnsOk);

  // AU: serie nueva 2.3.7 — permisos por analista, pestañas por usuario,
  // asignación y solicitud de asignación. realClick (serie AT) reutilizado:
  // botón realista hecho a mano, sin fakeClick.
  function mkPrepAU(over) {
    var base = mkPrep({ id: 'au1', tecnicoUid: 'u1', tecnico: 'Test User' });
    return Object.assign(base, over || {});
  }
  function loginAs(uid, nombre, rol) {
    cloudUser = { uid: uid, email: nombre.toLowerCase().replace(/ /g, '') + '@checklist.local', nombre: nombre };
    cloudRole = rol || 'usuario';
    applyRoleUI();
  }
  teamUsers = [
    { uid: 'u1', nombre: 'Test User', rol: 'usuario', email: 'test@checklist.local' },
    { uid: 'uAxel', nombre: 'Axel Danyael', rol: 'usuario', email: 'axel@checklist.local' },
    { uid: 'uAle', nombre: 'Alejandro', rol: 'usuario', email: 'alejandro@checklist.local' },
  ];
  // AU0: estáticos — pestañas, selector de admin, campos nuevos en la nube.
  var au0Chips = html.includes('data-f="nuevo"') && html.includes('data-f="reasignado"') && html.includes('data-f="devuelto"');
  var au0Admin = html.includes('id="adminUserRow"') && html.includes('id="adminUserFilter"') && html.includes('Todos los usuarios');
  var au0Sync = SRC.includes("tecnicoUid: p.tecnicoUid || ''") && SRC.includes("tecnicoUid: doc.tecnicoUid || ''") &&
    SRC.includes('asignaciones: p.asignaciones || []') && SRC.includes('asignaciones: doc.asignaciones || []') &&
    SRC.includes('solicitudAsignacion: p.solicitudAsignacion || null') && SRC.includes('solicitudAsignacion: doc.solicitudAsignacion || null');
  var au0Fn = SRC.includes('function isOwnPrep') && SRC.includes('function canEditPrep') && SRC.includes('function doAssign') &&
    SRC.includes('Equipos de otros analistas (solo lectura)') && SRC.includes('data-asignar="') && SRC.includes('data-solicitar-asignacion="') && SRC.includes('data-aprobar-solicitud="');
  console.log('AU0) pestañas Nuevo/Reasignado/Devuelto:', au0Chips, '| selector Todos los usuarios:', au0Admin, '| tecnicoUid/asignaciones/solicitud en prepToCloudDoc/prepFromCloud:', au0Sync, '| helpers y botones:', au0Fn);
  // AU1: vista principal — propios primero en orden de preparación.
  loginAs('u1', 'Test User', 'usuario');
  CLOUD_ENABLED = true;
  adminViewUid = 'todos';
  var TAU = Date.now();
  var eqAU = function (modelo) { return { tipo: 'Laptop', marca: 'Dell', modelo: modelo, serie: 'S-' + modelo, inventario: '1' }; };
  state.preparations = [
    mkPrepAU({ id: 'au-own-old', createdAt: TAU - 300000, tecnicoUid: 'u1', tecnico: 'Test User', equipo: eqAU('ModeloPropioViejo') }),
    mkPrepAU({ id: 'au-foreign', createdAt: TAU - 200000, tecnicoUid: 'uAxel', tecnico: 'Axel Danyael', equipo: eqAU('ModeloAjeno') }),
    mkPrepAU({ id: 'au-own-new', createdAt: TAU - 100000, tecnicoUid: 'u1', tecnico: 'Test User', equipo: eqAU('ModeloPropioNuevo') }),
  ];
  // 238b: los ajenos están ocultos por defecto; esta serie comprueba el
  // orden propios-primero con el interruptor encendido (serie AX: apagado).
  showOthers = true;
  filterStatus = 'todos'; searchText = ''; todosPage = 0;
  var ordAU1 = currentList().map(function (p) { return p.id; });
  filterStatus = 'preparacion';
  var ordAU1b = currentList().map(function (p) { return p.id; });
  filterStatus = 'todos';
  render();
  var listHtmlAU1 = document.getElementById('list').innerHTML;
  var iViejo = listHtmlAU1.indexOf('ModeloPropioViejo'), iNuevo = listHtmlAU1.indexOf('ModeloPropioNuevo'),
    iHead = listHtmlAU1.indexOf('Equipos de otros analistas (solo lectura)'), iAjeno = listHtmlAU1.indexOf('ModeloAjeno');
  console.log('AU1) propios primero en orden de preparación:', ordAU1.join(',') === 'au-own-old,au-own-new,au-foreign', '| también en En preparación:', ordAU1b.join(',') === 'au-own-old,au-own-new,au-foreign', '| sección ajena con encabezado y después de los propios:', iViejo !== -1 && iViejo < iNuevo && iNuevo < iHead && iHead < iAjeno);
  // AU2: pestañas Nuevo / Reasignado / Devuelto (solo propios; 15 días).
  state.preparations = [
    mkPrepAU({ id: 'au2-nuevo', createdAt: TAU - 300000 }),
    mkPrepAU({ id: 'au2-re', createdAt: TAU - 200000, reasignaciones: [{ de: 'Ana', a: 'Luis', fecha: TAU - 100000, analista: 'Test User' }] }),
    mkPrepAU({ id: 'au2-dev', createdAt: TAU - 100000, deliveredAt: TAU - 86400000, readyAt: TAU - 2 * 86400000 }),
    mkPrepAU({ id: 'au2-for', createdAt: TAU - 50000, tecnicoUid: 'uAxel', tecnico: 'Axel Danyael', reasignaciones: [{ de: 'Ana', a: 'Luis', fecha: TAU - 100000, analista: 'Axel Danyael' }] }),
    mkPrepAU({ id: 'au2-dev-old', createdAt: TAU - 25 * 86400000, deliveredAt: TAU - 20 * 86400000, readyAt: TAU - 21 * 86400000 }),
  ];
  loginAs('u1', 'Test User', 'usuario');
  filterStatus = 'nuevo';
  var tabNuevo = currentList().map(function (p) { return p.id; });
  filterStatus = 'reasignado';
  var tabRe = currentList().map(function (p) { return p.id; });
  filterStatus = 'devuelto';
  var tabDev = currentList().map(function (p) { return p.id; });
  loginAs('uGer', 'Gerardo', 'admin');
  filterStatus = 'devuelto';
  var tabDevAdmin = currentList().map(function (p) { return p.id; });
  console.log('AU2) Nuevo solo propio sin reasignar:', tabNuevo.join(',') === 'au2-nuevo', '| Reasignado solo propio con historial:', tabRe.join(',') === 'au2-re', '| Devuelto solo propio entregado reciente:', tabDev.join(',') === 'au2-dev', '| admin en Devuelto ve también el de hace 20 días:', tabDevAdmin.indexOf('au2-dev') !== -1 && tabDevAdmin.indexOf('au2-dev-old') !== -1);
  // AU3: equipo ajeno solo comparte por WA/correo; ni siquiera por handler directo.
  loginAs('u1', 'Test User', 'usuario');
  var fAU3 = mkPrepAU({ id: 'au3', tecnicoUid: 'uAxel', tecnico: 'Axel Danyael', checks: { t1: true } });
  state.preparations = [fAU3];
  var cardF = cardHtml(fAU3);
  var noEditAU3 = ['data-ready', 'data-deliver', 'data-na', 'data-remove-item', 'data-reassign', 'data-del-prep', 'data-pdf', 'data-xlsx', 'data-ai-falta', 'data-ai-wa', 'data-share-avance', 'data-mail-avance', 'data-nolisto', 'data-add-extra', 'data-unready'].every(function (a) { return cardF.indexOf(a + '="') === -1; });
  var shareOnlyAU3 = cardF.indexOf('data-wa="au3"') !== -1 && cardF.indexOf('data-mail="au3"') !== -1 && cardF.indexOf('data-solicitar-asignacion="au3"') !== -1;
  var fAU3d = mkPrepAU({ id: 'au3d', tecnicoUid: 'uAxel', tecnico: 'Axel Danyael', deliveredAt: TAU - 86400000, readyAt: TAU - 2 * 86400000 });
  var cardFD = cardHtml(fAU3d);
  var delShareAU3 = cardFD.indexOf('data-wa="au3d"') !== -1 && cardFD.indexOf('data-mail="au3d"') !== -1 && cardFD.indexOf('data-xlsx') === -1 && cardFD.indexOf('data-ai-wa') === -1 && cardFD.indexOf('data-pdf') === -1;
  var up3 = [];
  global.Cloud.upsertPrep = async function (d) { up3.push(d); };
  document.getElementById('toast').textContent = '';
  realClick('data-ready', 'au3');
  var guardReady = !fAU3.readyAt && up3.length === 0 && toastTxt().indexOf('otro analista') !== -1;
  realClick('data-na', 'au3', 't2');
  var guardNa = !fAU3.naItems || !fAU3.naItems.t2;
  document.getElementById('list')._h.change[0]({ target: { hasAttribute: function (a) { return a === 'data-check'; }, getAttribute: function (a) { return a === 'data-check' ? 't2' : a === 'data-prep' ? 'au3' : null; }, checked: true } });
  var guardCheck = fAU3.checks.t2 !== true;
  var shared3 = [];
  global.navigator.share = async function (o) { shared3.push(o.text); };
  realClick('data-wa', 'au3');
  var waOkAU3 = shared3.length === 1 && shared3[0].indexOf('Inspiron 3501') !== -1;
  console.log('AU3) ajeno sin botones de edición:', noEditAU3, '| solo WA/correo + solicitar:', shareOnlyAU3, '| entregado ajeno sin Excel/PDF/IA:', delShareAU3, '| Listo directo bloqueado con aviso:', guardReady, '| N/A directo bloqueado:', guardNa, '| casilla directa bloqueada:', guardCheck, '| WhatsApp sí se comparte:', waOkAU3);
  // AU4: admin — selector 'Todos los usuarios', todos los permisos, sin orden propio-primero.
  loginAs('uGer', 'Gerardo', 'admin');
  adminViewUid = 'todos';
  refreshAdminUserFilter();
  var selHtmlAU4 = document.getElementById('adminUserFilter').innerHTML;
  var selOkAU4 = selHtmlAU4.indexOf('Todos los usuarios') !== -1 && selHtmlAU4.indexOf('value="uAxel"') !== -1 && selHtmlAU4.indexOf('Axel Danyael') !== -1 && selHtmlAU4.indexOf('Alejandro') !== -1;
  var cardFA = cardHtml(fAU3);
  var adminBtns = cardFA.indexOf('data-pdf') !== -1 && cardFA.indexOf('data-reassign') !== -1 && cardFA.indexOf('data-del-prep') !== -1 && cardFA.indexOf('data-ready') !== -1 && cardFA.indexOf('data-asignar') !== -1;
  state.preparations = [
    mkPrepAU({ id: 'au4-own', createdAt: TAU - 100000, tecnicoUid: 'u1', tecnico: 'Test User', equipo: eqAU('ModeloAdminPropio') }),
    mkPrepAU({ id: 'au4-axel', createdAt: TAU - 300000, tecnicoUid: 'uAxel', tecnico: 'Axel Danyael', equipo: eqAU('ModeloAdminAxel') }),
    mkPrepAU({ id: 'au4-ale', createdAt: TAU - 200000, tecnicoUid: 'uAle', tecnico: 'Alejandro', equipo: eqAU('ModeloAdminAle') }),
  ];
  filterStatus = 'todos';
  adminViewUid = 'todos';
  var ordAdmin = currentList().map(function (p) { return p.id; });
  adminViewUid = 'uAxel';
  var onlyAxel = currentList().map(function (p) { return p.id; });
  adminViewUid = 'todos';
  var up4 = [];
  global.Cloud.upsertPrep = async function (d) { up4.push(d); };
  var pAxel4 = state.preparations.find(function (p) { return p.id === 'au4-axel'; });
  realClick('data-ready', 'au4-axel');
  var adminEdit = !!pAxel4.readyAt && up4.length === 1;
  console.log('AU4) selector con Todos + analistas:', selOkAU4, '| admin ve todos los botones en equipo ajeno:', adminBtns, '| admin sin propio-primero (orden de preparación):', ordAdmin.join(',') === 'au4-axel,au4-ale,au4-own', '| con Axel elegido solo sus equipos:', onlyAxel.join(',') === 'au4-axel', '| admin edita equipo ajeno:', adminEdit);
  // AU5: Asignar a otro analista transfiere la propiedad y conserva el avance.
  loginAs('u1', 'Test User', 'usuario');
  adminViewUid = 'todos';
  var pA5 = mkPrepAU({ id: 'au5', checks: { t1: true, t2: true } });
  state.preparations = [pA5];
  var up5 = [];
  global.Cloud.upsertPrep = async function (d) { up5.push(d); };
  realClick('data-asignar', 'au5');
  var panelAU5 = window._asignarFor === 'au5' && cardHtml(pA5).indexOf('id="asignarSelect"') !== -1 &&
    cardHtml(pA5).indexOf('<option value="uAxel">Axel Danyael</option>') !== -1 && cardHtml(pA5).indexOf('<option value="u1"') === -1;
  document.getElementById('asignarSelect').value = 'uAxel';
  realClick('data-save-asignar', 'au5');
  var asgOk = pA5.tecnicoUid === 'uAxel' && pA5.tecnico === 'Axel Danyael' && pA5.asignaciones.length === 1 &&
    pA5.asignaciones[0].de === 'Test User' && pA5.asignaciones[0].a === 'Axel Danyael' && pA5.checks.t1 === true && pA5.checks.t2 === true;
  var upAsg = up5.length === 1 && up5[0].tecnicoUid === 'uAxel' && up5[0].asignaciones.length === 1;
  var cardAsg = cardHtml(pA5).indexOf('Asignaciones: Test User → Axel Danyael') !== -1;
  var nowForeign = !isOwnPrep(pA5) && cardHtml(pA5).indexOf('data-solicitar-asignacion') !== -1 && cardHtml(pA5).indexOf('data-ready') === -1;
  loginAs('uAxel', 'Axel Danyael', 'usuario');
  var nowOwnAxel = isOwnPrep(pA5) && cardHtml(pA5).indexOf('data-ready') !== -1;
  loginAs('uGer', 'Gerardo', 'admin');
  var pA5b = mkPrepAU({ id: 'au5b', tecnicoUid: 'uAxel', tecnico: 'Axel Danyael' });
  state.preparations = [pA5b];
  realClick('data-asignar', 'au5b');
  document.getElementById('asignarSelect').value = 'uAle';
  realClick('data-save-asignar', 'au5b');
  var adminAsg = pA5b.tecnicoUid === 'uAle' && pA5b.tecnico === 'Alejandro';
  console.log('AU5) panel con los demás analistas (sin mí):', panelAU5, '| asigna y registra el traspaso:', asgOk, '| sube a la nube:', upAsg, '| historial en la tarjeta:', cardAsg, '| para mí ya es ajeno (solo lectura + solicitar):', nowForeign, '| para Axel ya es propio:', nowOwnAxel, '| el admin asigna cualquier equipo:', adminAsg);
  // AU6: Solicitar asignación + aprobar / rechazar / cancelar + una sola pendiente.
  loginAs('u1', 'Test User', 'usuario');
  var pS6 = mkPrepAU({ id: 'au6', tecnicoUid: 'uAxel', tecnico: 'Axel Danyael' });
  state.preparations = [pS6];
  var up6 = [];
  global.Cloud.upsertPrep = async function (d) { up6.push(d); };
  var btnSol = cardHtml(pS6).indexOf('data-solicitar-asignacion="au6"') !== -1;
  realClick('data-solicitar-asignacion', 'au6');
  var solOk = !!pS6.solicitudAsignacion && pS6.solicitudAsignacion.deUid === 'u1' && pS6.solicitudAsignacion.deNombre === 'Test User' && pS6.solicitudAsignacion.estado === 'pendiente' && up6.length === 1;
  var cardS1 = cardHtml(pS6);
  var cancelShown = cardS1.indexOf('data-cancel-solicitud="au6"') !== -1 && cardS1.indexOf('data-solicitar-asignacion="au6"') === -1;
  var fecha1 = pS6.solicitudAsignacion.fecha;
  realClick('data-solicitar-asignacion', 'au6');
  var oneOnly = pS6.solicitudAsignacion.fecha === fecha1 && up6.length === 1;
  loginAs('uAle', 'Alejandro', 'usuario');
  var cardS2 = cardHtml(pS6);
  var pendingOther = cardS2.indexOf('Solicitud pendiente de Test User') !== -1 && cardS2.indexOf('data-solicitar-asignacion') === -1 && cardS2.indexOf('data-cancel-solicitud') === -1;
  realClick('data-solicitar-asignacion', 'au6');
  var stillOne = pS6.solicitudAsignacion.deUid === 'u1' && up6.length === 1;
  loginAs('uGer', 'Gerardo', 'admin');
  var cardS3 = cardHtml(pS6);
  var adminSol = cardS3.indexOf('data-aprobar-solicitud="au6"') !== -1 && cardS3.indexOf('data-rechazar-solicitud="au6"') !== -1;
  realClick('data-aprobar-solicitud', 'au6');
  var apprOk = pS6.tecnicoUid === 'u1' && pS6.tecnico === 'Test User' && !pS6.solicitudAsignacion && pS6.asignaciones.length === 1 && pS6.asignaciones[0].a === 'Test User';
  loginAs('uAle', 'Alejandro', 'usuario');
  realClick('data-solicitar-asignacion', 'au6');
  var sol2 = !!pS6.solicitudAsignacion && pS6.solicitudAsignacion.deUid === 'uAle';
  loginAs('uGer', 'Gerardo', 'admin');
  realClick('data-rechazar-solicitud', 'au6');
  var rejOk = !pS6.solicitudAsignacion && pS6.tecnicoUid === 'u1';
  loginAs('uAle', 'Alejandro', 'usuario');
  realClick('data-solicitar-asignacion', 'au6');
  realClick('data-cancel-solicitud', 'au6');
  var cancelOk = !pS6.solicitudAsignacion;
  var rt6 = prepFromCloud(prepToCloudDoc(pS6));
  var syncOk6 = rt6.tecnicoUid === 'u1' && rt6.asignaciones.length === 1 && rt6.asignaciones[0].a === 'Test User';
  var pS6b = mkPrepAU({ id: 'au6b', tecnicoUid: 'uAxel', tecnico: 'Axel Danyael', solicitudAsignacion: { deUid: 'u1', deNombre: 'Test User', fecha: 123, estado: 'pendiente' } });
  var rt6b = prepFromCloud(prepToCloudDoc(pS6b));
  var syncSol6 = !!rt6b.solicitudAsignacion && rt6b.solicitudAsignacion.deUid === 'u1' && rt6b.solicitudAsignacion.estado === 'pendiente';
  console.log('AU6) botón Solicitar en equipo ajeno:', btnSol, '| solicitud guardada en el equipo:', solOk, '| mía muestra Cancelar:', cancelShown, '| no se duplica:', oneOnly, '| otro ve de quién es sin botón:', pendingOther, '| otro no la pisa:', stillOne, '| admin ve Aprobar/Rechazar:', adminSol, '| aprobar transfiere y limpia:', apprOk, '| segunda solicitud:', sol2, '| rechazar limpia sin transferir:', rejOk, '| cancelar limpia:', cancelOk, '| sincroniza asignaciones:', syncOk6, '| sincroniza solicitud:', syncSol6);
  // AU7: crear equipo guarda tecnicoUid; equipos viejos sin tecnicoUid usan el nombre.
  loginAs('u1', 'Test User', 'usuario');
  CLOUD_ENABLED = true;
  var up7 = [];
  global.Cloud.upsertPrep = async function (d) { up7.push(d); };
  document.getElementById('fTipo').value = 'Laptop';
  document.getElementById('fMarca').value = 'Dell';
  document.getElementById('fModelo').value = 'Inspiron 3501';
  document.getElementById('fSerie').value = 'S1';
  document.getElementById('fInv').value = '100';
  document.getElementById('fUser').value = 'Ana';
  document.getElementById('fTec').value = 'Test User';
  document.getElementById('btnAdd')._h.click[0]();
  var created7 = state.preparations[state.preparations.length - 1];
  var addUid = !!created7 && created7.tecnicoUid === 'u1' && up7.length === 1 && up7[0].tecnicoUid === 'u1';
  var oldOwn = mkPrep({ id: 'au7old', tecnico: 'Test User' }); delete oldOwn.tecnicoUid;
  var oldForeign = mkPrep({ id: 'au7for', tecnico: 'Axel Danyael' }); delete oldForeign.tecnicoUid;
  var fbOk = isOwnPrep(oldOwn) === true && isOwnPrep(oldForeign) === false;
  var oldPart = mkPrep({ id: 'au7part', tecnico: 'Axel Danyael', reasignaciones: [{ de: 'Ana', a: 'Luis', fecha: Date.now(), analista: 'Test User' }] }); delete oldPart.tecnicoUid;
  var partOk = isOwnPrep(oldPart) === true;
  var nBefore7 = state.preparations.length;
  document.getElementById('fReEquipo').value = '__nuevo__'; document.getElementById('fReA').value = 'Luis'; document.getElementById('fReDe').value = 'Ana';
  document.getElementById('fReTipo').value = 'Laptop'; document.getElementById('fReMarca').value = 'Dell'; document.getElementById('fReModelo').value = 'Latitude'; document.getElementById('fReSerie').value = 'S9'; document.getElementById('fReInv').value = '999';
  document.getElementById('btnReGuardar')._h.click[0]();
  var re7 = state.preparations[state.preparations.length - 1];
  var reUidOk = state.preparations.length === nBefore7 + 1 && !!re7 && re7.tecnicoUid === 'u1';
  console.log('AU7) Nuevo equipo guarda tecnicoUid:', addUid, '| viejo por nombre propio:', fbOk, '| viejo con reasignación mía es propio:', partOk, '| reasignado nuevo guarda tecnicoUid:', reUidOk);
  // AU8: la cadena de prepId incluye los botones nuevos.
  var chainAU8 = ['data-asignar', 'data-save-asignar', 'data-solicitar-asignacion', 'data-cancel-solicitud', 'data-aprobar-solicitud', 'data-rechazar-solicitud'].every(function (a) { return SRC.indexOf("q('" + a + "')") !== -1; });
  var btnsAU8 = ['data-asignar', 'data-save-asignar', 'data-solicitar-asignacion', 'data-cancel-solicitud', 'data-aprobar-solicitud', 'data-rechazar-solicitud'].every(function (a) { return SRC.indexOf(a + '="') !== -1; });
  console.log('AU8) cadena prepId con botones nuevos:', chainAU8, '| botones en el código:', btnsAU8);

  // AV: serie nueva 2.3.8 — Listo con pendientes: al pulsar Listo con
  // avance <100% la tarjeta dice 'Equipo con pendientes — faltan N
  // puntos' (no 'Listo para entregar'); al llegar al 100% el letrero se
  // quita y la etiqueta es literalmente 'Listo para entregar' con su
  // botón 'Entregado' normal. realClick reutilizado (serie AT).
  loginAs('u1', 'Test User', 'usuario');
  CLOUD_ENABLED = true;
  adminViewUid = 'todos';
  var upAV = [];
  global.Cloud.upsertPrep = async function (d) { upAV.push(d); };
  var reqAV = requiredItems(mkPrep({}));
  var nReqAV = reqAV.length;
  var checksAlmostAV = {};
  reqAV.slice(0, nReqAV - 1).forEach(function (it) { checksAlmostAV[it.id] = true; });
  var lastIdAV = reqAV[nReqAV - 1].id;
  var checksFullAV = {};
  reqAV.forEach(function (it) { checksFullAV[it.id] = true; });
  function changeCheckAV(prepId, itemId, checked) {
    document.getElementById('list')._h.change[0]({ target: { hasAttribute: function (a) { return a === 'data-check'; }, getAttribute: function (a) { return a === 'data-check' ? itemId : a === 'data-prep' ? prepId : null; }, checked: checked } });
  }
  // AV0: estáticos — letrero, derivado y botón en el código.
  var av0 = SRC.includes('Equipo con pendientes') && SRC.includes('conPendientes') && SRC.includes("pct < 100 ? 'Entregar' : 'Entregado'");
  console.log('AV0) letrero y botón en el código:', av0);
  // AV1: Listo a <100% muestra 'Equipo con pendientes' con el conteo y NO
  // estado 'Listo' ni botón de entrega como si fuera 100%.
  var pAV1 = mkPrepAU({ id: 'av1', checks: Object.assign({}, checksAlmostAV) });
  state.preparations = [pAV1];
  filterStatus = 'preparacion'; searchText = ''; todosPage = 0;
  realClick('data-ready', 'av1');
  var cardAV1 = cardHtml(pAV1);
  var av1 = !!pAV1.readyAt && statusOf(pAV1) === 'listo' && filterStatus === 'listo' &&
    cardAV1.indexOf('⚠️ Equipo con pendientes — faltan 1 puntos') !== -1 &&
    cardAV1.indexOf('>Equipo con pendientes<') !== -1 &&
    cardAV1.indexOf('Listo para entregar') === -1 &&
    cardAV1.indexOf('data-deliver="av1">Entregar<') !== -1 &&
    cardAV1.indexOf('>Entregado<') === -1 &&
    cardAV1.indexOf('data-unready="av1"') !== -1;
  console.log('AV1) Listo a <100%: letrero con faltan 1, sin Listo para entregar ni Entregado:', av1);
  // AV2: Listo al 100% se ve normal: etiqueta literal 'Listo para
  // entregar' (no 'Listo' a secas ni 'Equipo con pendientes') y botón
  // 'Entregado' normal, sin letrero ni 'Quitar listo'.
  var pAV2 = mkPrepAU({ id: 'av2', checks: Object.assign({}, checksFullAV) });
  state.preparations = [pAV2];
  filterStatus = 'preparacion';
  realClick('data-ready', 'av2');
  var cardAV2 = cardHtml(pAV2);
  var av2 = !!pAV2.readyAt && statusOf(pAV2) === 'listo' && progress(pAV2) === 100 &&
    cardAV2.indexOf('>Listo para entregar<') !== -1 &&
    cardAV2.indexOf('>Listo<') === -1 &&
    cardAV2.indexOf('Equipo con pendientes') === -1 &&
    cardAV2.indexOf('data-deliver="av2">Entregado<') !== -1 &&
    cardAV2.indexOf('data-unready="av2"') === -1;
  console.log('AV2) Listo al 100%: etiqueta literal Listo para entregar + Entregado:', av2);
  // AV3: completar el último punto quita el letrero (queda Listo para
  // entregar + Entregado).
  state.preparations = [pAV1];
  changeCheckAV('av1', lastIdAV, true);
  var cardAV3 = cardHtml(pAV1);
  var av3 = progress(pAV1) === 100 && statusOf(pAV1) === 'listo' &&
    cardAV3.indexOf('Equipo con pendientes') === -1 &&
    cardAV3.indexOf('>Listo para entregar<') !== -1 &&
    cardAV3.indexOf('data-deliver="av1">Entregado<') !== -1;
  console.log('AV3) último punto marcado: letrero fuera, Listo para entregar:', av3);
  // AV4: desmarcar un punto trae el letrero de vuelta.
  changeCheckAV('av1', lastIdAV, false);
  var cardAV4 = cardHtml(pAV1);
  var av4 = progress(pAV1) < 100 && statusOf(pAV1) === 'listo' && !!pAV1.readyAt &&
    cardAV4.indexOf('⚠️ Equipo con pendientes — faltan 1 puntos') !== -1 &&
    cardAV4.indexOf('>Equipo con pendientes<') !== -1 &&
    cardAV4.indexOf('data-deliver="av1">Entregar<') !== -1;
  console.log('AV4) punto desmarcado: letrero de vuelta:', av4);
  // AV5: 'Quitar listo' sigue funcionando (vuelve a preparación, sin letrero).
  realClick('data-unready', 'av1');
  var cardAV5 = cardHtml(pAV1);
  var av5 = !pAV1.readyAt && statusOf(pAV1) === 'preparacion' && filterStatus === 'preparacion' &&
    cardAV5.indexOf('Equipo con pendientes') === -1 &&
    cardAV5.indexOf('data-ready="av1"') !== -1 &&
    cardAV5.indexOf('data-deliver="av1"') === -1;
  console.log('AV5) Quitar listo: vuelve a preparación:', av5);
  // AV6: al pulsar Entregar con pendientes sigue apareciendo el panel de
  // confirmación de la 2.3.6; 'Entregar así' entrega.
  realClick('data-ready', 'av1');
  realClick('data-deliver', 'av1');
  var cardAV6 = cardHtml(pAV1);
  var av6a = window._deliverConfirmFor === 'av1' && !pAV1.deliveredAt &&
    cardAV6.indexOf('Este equipo no está al 100%') !== -1 &&
    cardAV6.indexOf('data-deliver-reopen="av1"') !== -1 &&
    cardAV6.indexOf('data-deliver-confirm="av1"') !== -1 &&
    cardAV6.indexOf('Reabrir para completar') !== -1 &&
    cardAV6.indexOf('Entregar así') !== -1;
  realClick('data-deliver-confirm', 'av1');
  var av6b = !!pAV1.deliveredAt && window._deliverConfirmFor === null && filterStatus === 'entregado';
  console.log('AV6) panel de entrega a <100%:', av6a, '| Entregar así entrega:', av6b);
  // AV7: en Todos y en Nuevo el letrero se ve; un equipo ajeno
  // listo-con-pendientes se ve solo lectura con su letrero.
  var pAV7 = mkPrepAU({ id: 'av7', checks: Object.assign({}, checksAlmostAV), readyAt: Date.now() - 60000, equipo: { tipo: 'Laptop', marca: 'Dell', modelo: 'ModeloPendiente', serie: 'S-AV7', inventario: '1' } });
  var pAV7f = mkPrepAU({ id: 'av7f', tecnicoUid: 'uAxel', tecnico: 'Axel Danyael', checks: Object.assign({}, checksAlmostAV), readyAt: Date.now() - 60000, equipo: { tipo: 'Laptop', marca: 'HP', modelo: 'ModeloAjenoPend', serie: 'S-AV7F', inventario: '2' } });
  state.preparations = [pAV7, pAV7f];
  // 238b: en 'Todos' los ajenos solo se ven con el interruptor
  // encendido (serie AX: apagado, solo el propio).
  showOthers = true;
  filterStatus = 'todos'; searchText = ''; todosPage = 0; window._expandedId = null;
  render();
  var listTodosAV7 = document.getElementById('list').innerHTML;
  var av7todos = (listTodosAV7.match(/⚠️ Equipo con pendientes — faltan 1 puntos/g) || []).length === 2 &&
    listTodosAV7.indexOf('ModeloPendiente') !== -1 && listTodosAV7.indexOf('ModeloAjenoPend') !== -1;
  filterStatus = 'nuevo';
  render();
  var listNuevoAV7 = document.getElementById('list').innerHTML;
  var av7nuevo = (listNuevoAV7.match(/⚠️ Equipo con pendientes — faltan 1 puntos/g) || []).length === 1 &&
    listNuevoAV7.indexOf('ModeloPendiente') !== -1 && listNuevoAV7.indexOf('ModeloAjenoPend') === -1;
  var cardAV7f = cardHtml(pAV7f);
  var av7f = cardAV7f.indexOf('⚠️ Equipo con pendientes — faltan 1 puntos') !== -1 &&
    ['data-ready', 'data-deliver', 'data-unready', 'data-nolisto', 'data-na', 'data-remove-item', 'data-add-extra', 'data-pdf', 'data-del-prep', 'data-asignar'].every(function (a) { return cardAV7f.indexOf(a + '="') === -1; }) &&
    cardAV7f.indexOf('data-wa="av7f"') !== -1 && cardAV7f.indexOf('data-solicitar-asignacion="av7f"') !== -1;
  console.log('AV7) Todos con letrero en los dos:', av7todos, '| Nuevo solo propio con letrero:', av7nuevo, '| ajeno solo lectura con letrero:', av7f);

  // AW: serie nueva 238b — borrador 'Guardar para después' + 'Completar
  // datos'. Un detectado se guarda como borrador en En preparación y se
  // retoma después sin crear otro equipo; es la ÚNICA forma de cambiar
  // los datos de un equipo ya guardado (serie AR2: sin edición general).
  loginAs('u1', 'Test User', 'usuario');
  CLOUD_ENABLED = true;
  adminViewUid = 'todos';
  showOthers = false;
  var upAW = [];
  global.Cloud.upsertPrep = async function (d) { upAW.push(d); };
  var markedAW = [];
  global.Cloud.markDetectadoUsado = async function (id) { markedAW.push(id); };
  var delAW = [];
  global.Cloud.deletePrep = async function (id) { delAW.push(id); };
  var detAW = { id: 'AW-DET', hostname: 'PC-AW', marca: 'HP', modelo: 'EliteDesk 800', serie: 'AW-DET', cpu: 'Intel Core i7-10700', ramGB: 16, discoGB: 512, so: 'Windows 11 Pro', tipo: 'Desktop', detectadoEn: Date.now() - 60000, detectadoPor: 'Gerardo', usado: false, checks: { t18: true, t8: 'Office 365' }, detalles: {}, versiones: { so: 'Windows 11 Pro 26H2 (compilación 26200)' } };
  // AW0: estáticos — botón, campo borrador en la nube, 'Completar datos'.
  var aw0 = html.includes('data-det-save="') && html.includes('Guardar para después') &&
    SRC.includes('borrador: p.borrador || false') && SRC.includes('borrador: doc.borrador || false') &&
    SRC.includes('data-completar="') && SRC.includes('Completar datos') && SRC.includes("q('data-completar')") &&
    SRC.includes('prepFromDetectado') && SRC.includes('Borrador — faltan datos');
  console.log('AW0) botón Guardar para después:', aw0);
  // AW1: 'Guardar para después' crea el borrador con los datos detectados.
  var nBeforeAW = state.preparations.length;
  detectados = [detAW];
  renderDetectados();
  var detHtmlAW = document.getElementById('detList').innerHTML;
  var awBtn = detHtmlAW.indexOf('data-det-save="AW-DET"') !== -1 && detHtmlAW.indexOf('Guardar para después') !== -1 && detHtmlAW.indexOf('Usar este equipo') !== -1 && detHtmlAW.indexOf('Descartar') !== -1;
  upAW.length = 0; markedAW.length = 0;
  document.getElementById('detList')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-det-save]' ? { getAttribute: function () { return 'AW-DET'; } } : null; } } });
  var draftAW = state.preparations[state.preparations.length - 1];
  var aw1 = state.preparations.length === nBeforeAW + 1 && !!draftAW && draftAW.borrador === true &&
    draftAW.equipo.modelo === 'EliteDesk 800' && draftAW.equipo.serie === 'AW-DET' && draftAW.equipo.hostname === 'PC-AW' &&
    draftAW.equipo.inventario === '' && draftAW.usuario.nombre === '' && draftAW.usuario.area === '' && draftAW.usuario.correo === '' &&
    draftAW.checks.t18 === true && draftAW.checks.t8 === 'Office 365' && draftAW.autoDetectado.join(',') === 't8,t18' &&
    draftAW.versiones.so === 'Windows 11 Pro 26H2 (compilación 26200)' && draftAW.equipo.cpu === 'Intel Core i7-10700' && draftAW.equipo.ramGB === 16 &&
    draftAW.tecnicoUid === 'u1' && draftAW.tecnico === 'Test User' && !draftAW.deliveredAt && !draftAW.readyAt &&
    upAW.length === 1 && upAW[0].borrador === true && upAW[0].autoDetectado.join(',') === 't8,t18' &&
    markedAW.indexOf('AW-DET') !== -1 && detAW.usado === true &&
    document.getElementById('detBox').hidden === true && filterStatus === 'preparacion';
  console.log('AW1) botón en la tarjeta:', awBtn, '| borrador creado con datos detectados y vacíos:', aw1);
  // AW2: el borrador aparece en En preparación propio (pestaña Nuevo) con
  // su marcador, sin botón Listo ni letrero de pendientes.
  var draftIdAW = draftAW.id;
  filterStatus = 'preparacion'; searchText = ''; todosPage = 0;
  var aw2prep = currentList().some(function (p) { return p.id === draftIdAW; });
  filterStatus = 'nuevo';
  var aw2nuevo = currentList().some(function (p) { return p.id === draftIdAW; });
  filterStatus = 'todos';
  render();
  var listAW2 = document.getElementById('list').innerHTML;
  var cardAW2 = cardHtml(draftAW);
  var aw2 = aw2prep && aw2nuevo && listAW2.indexOf('📝 Borrador — faltan datos') !== -1 &&
    listAW2.indexOf('data-completar="' + draftIdAW + '"') !== -1 &&
    cardAW2.indexOf('>Borrador<') !== -1 && cardAW2.indexOf('Borrador — faltan datos: inventario, usuario, área, correo') !== -1 &&
    cardAW2.indexOf('data-ready="' + draftIdAW + '"') === -1 && cardAW2.indexOf('data-deliver="' + draftIdAW + '"') === -1 &&
    cardAW2.indexOf('Equipo con pendientes') === -1;
  console.log('AW2) en En preparación y en Nuevo:', aw2prep && aw2nuevo, '| marcador + Completar datos, sin Listo ni pendientes:', aw2);
  // AW3: 'Completar datos' abre el formulario prellenado y Guardar
  // actualiza EL MISMO equipo y quita el borrador, sin duplicarlo.
  upAW.length = 0;
  realClick('data-completar', draftIdAW);
  var aw3open = window._completarBorradorId === draftIdAW && document.getElementById('newBox').hidden === false && document.getElementById('detBox').hidden === true &&
    document.getElementById('fModelo').value === 'EliteDesk 800' && document.getElementById('fSerie').value === 'AW-DET' && document.getElementById('fHostname').value === 'PC-AW' &&
    document.getElementById('fInv').value === '' && document.getElementById('fUser').value === '' &&
    document.getElementById('btnAdd').textContent.indexOf('Guardar datos completos') !== -1 &&
    document.getElementById('btnAdd').disabled === false && formReady() === true;
  document.getElementById('fInv').value = 'INV-777';
  document.getElementById('fUser').value = 'Ana Pérez';
  document.getElementById('fArea').value = 'Soporte';
  document.getElementById('fCorreo').value = 'ana@empresa.com';
  var nBeforeAW3 = state.preparations.length;
  document.getElementById('btnAdd')._h.click[0]();
  var doneAW = state.preparations.find(function (p) { return p.id === draftIdAW; });
  var aw3 = state.preparations.length === nBeforeAW3 && !!doneAW && !doneAW.borrador &&
    doneAW.equipo.inventario === 'INV-777' && doneAW.usuario.nombre === 'Ana Pérez' && doneAW.usuario.area === 'Soporte' && doneAW.usuario.correo === 'ana@empresa.com' &&
    doneAW.equipo.modelo === 'EliteDesk 800' && doneAW.checks.t18 === true && doneAW.checks.t8 === 'Office 365' &&
    upAW.length === 1 && upAW[0].borrador === false && upAW[0].equipo.inventario === 'INV-777' &&
    window._completarBorradorId === null && document.getElementById('newBox').hidden === true &&
    cardHtml(doneAW).indexOf('Borrador — faltan datos') === -1 && cardHtml(doneAW).indexOf('data-completar=') === -1 &&
    cardHtml(doneAW).indexOf('data-ready="' + draftIdAW + '"') !== -1;
  console.log('AW3) Completar abre prellenado:', aw3open, '| Guardar actualiza el mismo sin duplicar y quita el borrador:', aw3);
  // AW4: un ajeno no ve 'Completar datos' ni puede completarlo por handler
  // directo; el admin sí lo ve (respeta las guardas de la 2.3.7).
  var fAW4 = mkPrepAU({ id: 'aw4', borrador: true, tecnicoUid: 'uAxel', tecnico: 'Axel Danyael', equipo: { tipo: 'Laptop', marca: 'HP', modelo: 'ModeloBorradorAjeno', serie: 'S-AW4', inventario: '' }, usuario: { nombre: '', area: '', correo: '' } });
  state.preparations = [fAW4];
  loginAs('u1', 'Test User', 'usuario');
  upAW.length = 0; document.getElementById('toast').textContent = '';
  var cardAW4 = cardHtml(fAW4);
  var aw4hide = cardAW4.indexOf('data-completar=') === -1 && cardAW4.indexOf('📝 Borrador — faltan datos') !== -1 &&
    cardAW4.indexOf('data-wa="aw4"') !== -1 && cardAW4.indexOf('data-solicitar-asignacion="aw4"') !== -1;
  realClick('data-completar', 'aw4');
  var aw4block = fAW4.borrador === true && upAW.length === 0 && window._completarBorradorId !== 'aw4' && toastTxt().indexOf('otro analista') !== -1;
  loginAs('uGer', 'Gerardo', 'admin');
  var aw4admin = cardHtml(fAW4).indexOf('data-completar="aw4"') !== -1;
  console.log('AW4) ajeno sin Completar datos (marcador sí, WA + solicitar sí):', aw4hide, '| directo bloqueado con aviso:', aw4block, '| admin sí lo ve:', aw4admin);
  // AW5: eliminar el borrador no lo resucita en el panel de detectados.
  loginAs('u1', 'Test User', 'usuario');
  var detAW5 = { id: 'AW5-DET', hostname: 'PC-AW5', marca: 'Dell', modelo: 'Latitude 5420', serie: 'AW5-DET', tipo: 'Laptop', detectadoEn: Date.now() - 60000, detectadoPor: 'Gerardo', usado: false, checks: { t18: true }, detalles: {}, versiones: {} };
  detectados = [detAW5];
  renderDetectados();
  document.getElementById('detList')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-det-save]' ? { getAttribute: function () { return 'AW5-DET'; } } : null; } } });
  var draftAW5 = state.preparations[state.preparations.length - 1];
  var aw5saved = !!draftAW5 && draftAW5.borrador === true && draftAW5.equipo.serie === 'AW5-DET' && detAW5.usado === true;
  loginAs('uGer', 'Gerardo', 'admin');
  delAW.length = 0;
  realClick('data-del-prep', draftAW5.id);
  answerConfirm(true);
  await sleep(20);
  var aw5gone = state.preparations.every(function (p) { return p.id !== draftAW5.id; }) && delAW.indexOf(draftAW5.id) !== -1;
  var aw5cb = typeof detCbAq === 'function';
  if (aw5cb) detCbAq([Object.assign({}, detAW5, { usado: true })]);
  var panelAW5 = document.getElementById('detList').innerHTML;
  var aw5panel = panelAW5.indexOf('PC-AW5') === -1 && panelAW5.indexOf('No hay equipos detectados pendientes.') !== -1;
  console.log('AW5) borrador guardado y marcado usado:', aw5saved, '| eliminar lo borra (nube):', aw5gone, '| suscripción viva:', aw5cb, '| no vuelve al panel:', aw5panel);

  // AX: serie nueva 238b — equipos de otros analistas OCULTOS por defecto
  // en Por preparar, con interruptor para verlos. El interruptor se
  // recuerda por teléfono (localStorage); al admin no le aplica (usa su
  // selector 'Todos los usuarios'). Renta no cambia.
  loginAs('u1', 'Test User', 'usuario');
  CLOUD_ENABLED = true;
  adminViewUid = 'todos';
  var TAXB = Date.now();
  var eqAXB = function (modelo) { return { tipo: 'Laptop', marca: 'Dell', modelo: modelo, serie: 'S-' + modelo, inventario: '1' }; };
  var pAXown = mkPrepAU({ id: 'ax-own', createdAt: TAXB - 300000, tecnicoUid: 'u1', tecnico: 'Test User', equipo: eqAXB('ModeloPropioAX') });
  var pAXfor = mkPrepAU({ id: 'ax-for', createdAt: TAXB - 200000, tecnicoUid: 'uAxel', tecnico: 'Axel Danyael', equipo: eqAXB('ModeloAjenoAX') });
  // AX0: estáticos — botón, persistencia, filtro en currentList.
  var ax0 = html.includes('id="btnVerOtros"') && html.includes('Ver equipos de otros analistas') && html.includes('id="othersRow"') &&
    SRC.includes('SHOW_OTHERS_KEY') && SRC.includes('checklist-soporte-ver-otros-v1') &&
    SRC.includes("localStorage.getItem(SHOW_OTHERS_KEY) === '1'") && SRC.includes("localStorage.setItem(SHOW_OTHERS_KEY, showOthers ? '1' : '0')") &&
    SRC.includes("if (cloudRole !== 'admin' && !showOthers && !isOwnPrep(p)) return false;");
  console.log('AX0) botón + persistencia + filtro en currentList:', ax0);
  // AX1: por defecto (apagado) solo se ven los propios en Todos y en
  // En preparación, aunque existan ajenos.
  showOthers = false;
  state.preparations = [pAXown, pAXfor];
  filterStatus = 'todos'; searchText = ''; todosPage = 0;
  var ax1todos = currentList().map(function (p) { return p.id; }).join(',') === 'ax-own';
  filterStatus = 'preparacion';
  var ax1prep = currentList().map(function (p) { return p.id; }).join(',') === 'ax-own';
  filterStatus = 'todos';
  render();
  var listAX1 = document.getElementById('list').innerHTML;
  var ax1html = listAX1.indexOf('ModeloPropioAX') !== -1 && listAX1.indexOf('ModeloAjenoAX') === -1 && listAX1.indexOf('Equipos de otros analistas (solo lectura)') === -1;
  var ax1btn = document.getElementById('btnVerOtros').hidden === false && document.getElementById('btnVerOtros').textContent.indexOf('Ver equipos de otros analistas') !== -1;
  console.log('AX1) Todos solo propio:', ax1todos, '| En preparación solo propio:', ax1prep, '| lista sin ajeno ni encabezado:', ax1html, '| botón visible con su texto:', ax1btn);
  // AX2: al encender el interruptor aparecen los ajenos en solo lectura
  // (WhatsApp/correo + Solicitar asignación) y se recuerda en localStorage.
  document.getElementById('btnVerOtros')._h.click[0]();
  var ax2on = showOthers === true && global.localStorage.getItem('checklist-soporte-ver-otros-v1') === '1';
  filterStatus = 'todos'; searchText = ''; todosPage = 0;
  var ax2list = currentList().map(function (p) { return p.id; }).join(',') === 'ax-own,ax-for';
  var listAX2 = document.getElementById('list').innerHTML;
  var iHeadAX2 = listAX2.indexOf('Equipos de otros analistas (solo lectura)'), iForAX2 = listAX2.indexOf('ModeloAjenoAX'), iOwnAX2 = listAX2.indexOf('ModeloPropioAX');
  var ax2html = iOwnAX2 !== -1 && iOwnAX2 < iHeadAX2 && iHeadAX2 < iForAX2;
  var cardAX2 = cardHtml(pAXfor);
  var ax2ro = cardAX2.indexOf('data-wa="ax-for"') !== -1 && cardAX2.indexOf('data-mail="ax-for"') !== -1 && cardAX2.indexOf('data-solicitar-asignacion="ax-for"') !== -1 && cardAX2.indexOf('data-ready="ax-for"') === -1;
  var ax2label = document.getElementById('btnVerOtros').textContent.indexOf('Ocultar equipos de otros analistas') !== -1;
  console.log('AX2) interruptor encendido y recordado:', ax2on, '| lista con los dos:', ax2list, '| sección ajena tras los propios:', ax2html, '| ajeno solo lectura:', ax2ro, '| botón ahora dice Ocultar:', ax2label);
  // AX3: al apagarlo desaparecen de nuevo.
  document.getElementById('btnVerOtros')._h.click[0]();
  var ax3off = showOthers === false && global.localStorage.getItem('checklist-soporte-ver-otros-v1') === '0';
  filterStatus = 'todos'; searchText = '';
  var ax3list = currentList().map(function (p) { return p.id; }).join(',') === 'ax-own';
  var listAX3 = document.getElementById('list').innerHTML;
  var ax3html = listAX3.indexOf('ModeloAjenoAX') === -1 && listAX3.indexOf('ModeloPropioAX') !== -1;
  console.log('AX3) interruptor apagado y recordado:', ax3off, '| lista solo propio:', ax3list, '| HTML sin ajeno:', ax3html);
  // AX4: al admin no le aplica el interruptor (ni lo ve): con 'Todos' ve
  // todos, y con un analista elegido solo los de ese analista.
  loginAs('uGer', 'Gerardo', 'admin');
  adminViewUid = 'todos';
  showOthers = false;
  filterStatus = 'todos'; searchText = '';
  var ax4all = currentList().map(function (p) { return p.id; }).join(',') === 'ax-own,ax-for';
  adminViewUid = 'uAxel';
  var ax4axel = currentList().map(function (p) { return p.id; }).join(',') === 'ax-for';
  adminViewUid = 'todos';
  render();
  var ax4btn = document.getElementById('btnVerOtros').hidden === true;
  console.log('AX4) admin con Todos ve todos en orden de preparación:', ax4all, '| con Axel solo los suyos:', ax4axel, '| botón oculto para el admin:', ax4btn);
  // AX5: las pestañas Nuevo/Reasignado/Devuelto de un usuario normal solo
  // muestran propios con la opción apagada.
  loginAs('u1', 'Test User', 'usuario');
  adminViewUid = 'todos';
  showOthers = false;
  state.preparations = [
    mkPrepAU({ id: 'ax5-nuevo', createdAt: TAXB - 300000, equipo: eqAXB('ModeloAXNuevo') }),
    mkPrepAU({ id: 'ax5-re', createdAt: TAXB - 200000, reasignaciones: [{ de: 'Ana', a: 'Luis', fecha: TAXB - 100000, analista: 'Test User' }], equipo: eqAXB('ModeloAXRe') }),
    mkPrepAU({ id: 'ax5-dev', createdAt: TAXB - 100000, deliveredAt: TAXB - 86400000, readyAt: TAXB - 2 * 86400000, equipo: eqAXB('ModeloAXDev') }),
    mkPrepAU({ id: 'ax5-for', createdAt: TAXB - 50000, tecnicoUid: 'uAxel', tecnico: 'Axel Danyael', reasignaciones: [{ de: 'Ana', a: 'Luis', fecha: TAXB - 100000, analista: 'Axel Danyael' }], equipo: eqAXB('ModeloAXFor') }),
  ];
  filterStatus = 'nuevo'; searchText = '';
  var ax5n = currentList().map(function (p) { return p.id; }).join(',') === 'ax5-nuevo';
  filterStatus = 'reasignado';
  var ax5r = currentList().map(function (p) { return p.id; }).join(',') === 'ax5-re';
  filterStatus = 'devuelto';
  var ax5d = currentList().map(function (p) { return p.id; }).join(',') === 'ax5-dev';
  console.log('AX5) Nuevo solo propio:', ax5n, '| Reasignado solo propio:', ax5r, '| Devuelto solo propio:', ax5d);
  // AX6: la búsqueda respeta el interruptor (un ajeno no aparece al
  // buscarlo con la opción apagada; con ella encendida, sí).
  state.preparations = [pAXown, pAXfor];
  showOthers = false;
  filterStatus = 'todos'; searchText = 'modeloajenoax';
  var ax6off = currentList().length === 0;
  showOthers = true;
  var ax6on = currentList().map(function (p) { return p.id; }).join(',') === 'ax-for';
  searchText = '';
  console.log('AX6) buscar ajeno con opción apagada no lo encuentra:', ax6off, '| encendida sí:', ax6on);
  // AX7: el botón refleja el estado (texto + clase 'on').
  showOthers = false; render();
  var ax7off = document.getElementById('btnVerOtros').textContent.indexOf('Ver equipos de otros analistas') !== -1 && !document.getElementById('btnVerOtros').classList.contains('on');
  showOthers = true; render();
  var ax7on = document.getElementById('btnVerOtros').textContent.indexOf('Ocultar equipos de otros analistas') !== -1 && document.getElementById('btnVerOtros').classList.contains('on');
  showOthers = false; render();
  console.log('AX7) apagado dice Ver sin clase on:', ax7off, '| encendido dice Ocultar con clase on:', ax7on);

  // AY: serie nueva 2.3.9 — botón '💾 Guardar avance' en la tarjeta del
  // equipo en revisión (preparación o listo, propio o admin). Guardado
  // explícito: save() local + cloudUpsertPrep, sin cambiar el estado ni
  // duplicar el equipo, con confirmación visible en el propio botón
  // ('✓ Avance guardado', deshabilitado ~2 s, sin alert). Nunca en
  // equipos ajenos ni en entregados; en borradores sí (su checklist
  // también se revisa). El guardado automático por cambio sigue igual.
  // Clic realista hecho a mano (sin fakeClick): el botón lleva data-prep
  // y su propio atributo; closest devuelve el botón solo para ese
  // selector y hasAttribute solo para ese atributo.
  function clickGuardar(prepId) {
    var btn = { textContent: '💾 Guardar avance', disabled: false,
      getAttribute: function (a) { return (a === 'data-guardar-avance' || a === 'data-prep') ? prepId : null; },
      hasAttribute: function (a) { return a === 'data-guardar-avance'; },
      closest: function (sel) { if (sel === '[data-guardar-avance]' || sel === '[data-prep]') return btn; return null; },
      classList: { contains: function () { return false; } } };
    document.getElementById('list')._h.click[0]({ target: btn });
    return btn;
  }
  // AY0: estáticos — botón en la tarjeta, atributo en la cadena q() del
  // handler de #list, rama de manejo, y en EDIT_ATTRS (guarda defensiva).
  var ay0btn = html.includes('data-guardar-avance="') && html.includes('💾 Guardar avance') && html.includes('✓ Avance guardado');
  var ay0chain = SRC.includes("q('data-guardar-avance')") && SRC.includes("t.hasAttribute('data-guardar-avance')");
  var ay0edit = SRC.includes("'data-completar', 'data-guardar-avance'");
  var ay0place = SRC.includes("if (st === 'preparacion' || st === 'listo') actions += '<button class=\"btn-ghost\" data-guardar-avance=\"'");
  console.log('AY0) botón en tarjeta + confirmación:', ay0btn, '| en cadena q() y rama del handler:', ay0chain, '| en EDIT_ATTRS:', ay0edit, '| solo preparación/listo:', ay0place);
  // AY1: visibilidad por estado y propiedad (cardHtml directo).
  loginAs('u1', 'Test User', 'usuario');
  CLOUD_ENABLED = true;
  adminViewUid = 'todos';
  var TAY = Date.now();
  var eqAY = function (modelo) { return { tipo: 'Laptop', marca: 'Dell', modelo: modelo, serie: 'S-' + modelo, inventario: '1' }; };
  var pAYown = mkPrepAU({ id: 'ay-own', createdAt: TAY - 300000, equipo: eqAY('ModeloPropioAY') });
  var pAYlisto = mkPrepAU({ id: 'ay-listo', createdAt: TAY - 200000, readyAt: TAY - 100000, equipo: eqAY('ModeloListoAY') });
  var pAYentr = mkPrepAU({ id: 'ay-entr', createdAt: TAY - 400000, readyAt: TAY - 200000, deliveredAt: TAY - 86400000, equipo: eqAY('ModeloEntregadoAY') });
  var pAYfor = mkPrepAU({ id: 'ay-for', createdAt: TAY - 100000, tecnicoUid: 'uAxel', tecnico: 'Axel Danyael', equipo: eqAY('ModeloAjenoAY') });
  var pAYbor = mkPrepAU({ id: 'ay-bor', createdAt: TAY - 50000, borrador: true, equipo: eqAY('ModeloBorradorAY') });
  var ay1prep = cardHtml(pAYown).indexOf('data-guardar-avance="ay-own"') !== -1;
  var ay1listo = cardHtml(pAYlisto).indexOf('data-guardar-avance="ay-listo"') !== -1;
  var ay1entr = cardHtml(pAYentr).indexOf('data-guardar-avance') === -1;
  var ay1for = cardHtml(pAYfor).indexOf('data-guardar-avance') === -1;
  var ay1bor = cardHtml(pAYbor).indexOf('data-guardar-avance="ay-bor"') !== -1;
  loginAs('uGer', 'Gerardo', 'admin');
  var ay1admin = cardHtml(pAYfor).indexOf('data-guardar-avance="ay-for"') !== -1;
  console.log('AY1) propio en preparación:', ay1prep, '| propio listo:', ay1listo, '| entregado no:', ay1entr, '| ajeno no:', ay1for, '| borrador sí:', ay1bor, '| admin en ajeno sí:', ay1admin);
  // AY1b: en la lista renderizada (con ajenos visibles) el botón está solo
  // en la tarjeta propia, nunca en la ajena ni en la entregada.
  loginAs('u1', 'Test User', 'usuario');
  showOthers = true;
  state.preparations = [pAYown, pAYfor, pAYentr];
  filterStatus = 'todos'; searchText = ''; todosPage = 0;
  render();
  var listAY1 = document.getElementById('list').innerHTML;
  var ay1b = listAY1.indexOf('data-guardar-avance="ay-own"') !== -1 && listAY1.indexOf('data-guardar-avance="ay-for"') === -1 && listAY1.indexOf('data-guardar-avance="ay-entr"') === -1;
  console.log('AY1b) lista renderizada: botón solo en propio:', ay1b);
  // AY2: al pulsar guarda local + nube, sin duplicar ni cambiar el estado,
  // y confirma en el propio botón (texto + deshabilitado).
  var upAY = [];
  global.Cloud.upsertPrep = async function (d) { upAY.push(d); };
  var pAY2 = mkPrepAU({ id: 'ay2', createdAt: TAY - 300000, checks: { t18: true }, equipo: eqAY('ModeloAY2') });
  state.preparations = [pAY2];
  filterStatus = 'todos'; searchText = ''; todosPage = 0; showOthers = false;
  render();
  global.localStorage.removeItem('checklist-soporte-v1');
  var nAY2 = state.preparations.length;
  var btnAY2 = clickGuardar('ay2');
  var savedAY2 = JSON.parse(global.localStorage.getItem('checklist-soporte-v1') || '{}');
  var lsAY2 = savedAY2.preparations && savedAY2.preparations.length === 1 && savedAY2.preparations[0].id === 'ay2' && savedAY2.preparations[0].checks && savedAY2.preparations[0].checks.t18 === true;
  var upAY2 = upAY.length === 1 && upAY[0].id === 'ay2';
  var nodupAY2 = state.preparations.length === nAY2 && state.preparations.filter(function (p) { return p.id === 'ay2'; }).length === 1;
  var stAY2 = statusOf(pAY2) === 'preparacion' && !pAY2.deliveredAt && !pAY2.readyAt;
  var confAY2 = btnAY2.textContent === '✓ Avance guardado' && btnAY2.disabled === true;
  console.log('AY2) guardado local con sus checks:', lsAY2, '| nube con el equipo:', upAY2, '| sin duplicar:', nodupAY2, '| estado sin cambio:', stAY2, '| confirmación visible y deshabilitado:', confAY2);
  // AY2b: a los 2 s el botón vuelve a su texto y se habilita.
  await sleep(2100);
  var restAY2 = btnAY2.textContent === '💾 Guardar avance' && btnAY2.disabled === false;
  console.log('AY2b) a los 2 s el botón vuelve a su texto y se habilita:', restAY2);
  // AY3: el guardado automático por cambio sigue funcionando (marcar una
  // casilla guarda local + nube y la tarjeta re-renderizada sigue con el
  // botón 'Guardar avance').
  upAY.length = 0;
  global.localStorage.removeItem('checklist-soporte-v1');
  var reqAY = requiredItems(pAY2);
  var chkAY = reqAY[0].id;
  document.getElementById('list')._h.change[0]({ target: { hasAttribute: function (a) { return a === 'data-check'; }, getAttribute: function (a) { return a === 'data-check' ? chkAY : 'ay2'; }, checked: true, classList: { contains: function () { return false; } } } });
  var savedAY3 = JSON.parse(global.localStorage.getItem('checklist-soporte-v1') || '{}');
  var lsAY3 = savedAY3.preparations && savedAY3.preparations[0].checks && savedAY3.preparations[0].checks[chkAY] === true;
  var upAY3 = upAY.length === 1 && upAY[0].id === 'ay2';
  var btnAY3 = document.getElementById('list').innerHTML.indexOf('data-guardar-avance="ay2"') !== -1;
  console.log('AY3) cambio guarda local:', lsAY3, '| cambio sube a nube:', upAY3, '| tarjeta re-renderizada con el botón:', btnAY3);
  // AY4: en un borrador propio el botón guarda el avance (checks
  // detectados incluidos) sin quitar la marca de borrador ni duplicar, y
  // convive con 'Completar datos'.
  var pAY4 = mkPrepAU({ id: 'ay4', createdAt: TAY - 200000, borrador: true, checks: { t18: true }, equipo: eqAY('ModeloAY4') });
  state.preparations = [pAY4];
  filterStatus = 'todos'; searchText = '';
  render();
  var cardAY4 = cardHtml(pAY4);
  var ay4btn = cardAY4.indexOf('data-guardar-avance="ay4"') !== -1 && cardAY4.indexOf('data-completar="ay4"') !== -1;
  upAY.length = 0;
  global.localStorage.removeItem('checklist-soporte-v1');
  var btnAY4 = clickGuardar('ay4');
  var savedAY4 = JSON.parse(global.localStorage.getItem('checklist-soporte-v1') || '{}');
  var lsAY4 = savedAY4.preparations && savedAY4.preparations.length === 1 && savedAY4.preparations[0].borrador === true && savedAY4.preparations[0].checks.t18 === true;
  var upAY4 = upAY.length === 1 && upAY[0].id === 'ay4';
  var confAY4 = btnAY4.textContent === '✓ Avance guardado' && btnAY4.disabled === true;
  console.log('AY4) borrador con botón y Completar datos:', ay4btn, '| guarda local sin quitar borrador:', lsAY4, '| nube:', upAY4, '| confirmación:', confAY4);
  // AY5: el admin puede guardar el avance de un equipo ajeno (canEditPrep).
  loginAs('uGer', 'Gerardo', 'admin');
  adminViewUid = 'todos';
  state.preparations = [pAYfor];
  filterStatus = 'todos'; searchText = '';
  render();
  upAY.length = 0;
  global.localStorage.removeItem('checklist-soporte-v1');
  var btnAY5 = clickGuardar('ay-for');
  var savedAY5 = JSON.parse(global.localStorage.getItem('checklist-soporte-v1') || '{}');
  var lsAY5 = savedAY5.preparations && savedAY5.preparations.length === 1 && savedAY5.preparations[0].id === 'ay-for';
  var upAY5 = upAY.length === 1 && upAY[0].id === 'ay-for';
  var confAY5 = btnAY5.textContent === '✓ Avance guardado' && btnAY5.disabled === true;
  console.log('AY5) admin guarda avance de ajeno: local:', lsAY5, '| nube:', upAY5, '| confirmación:', confAY5);
  // AY6: un usuario normal NO puede guardar el avance de un equipo ajeno
  // ni llamando directo al handler: la guarda defensiva (EDIT_ATTRS) lo
  // bloquea con el aviso de solo lectura, sin guardar nada.
  loginAs('u1', 'Test User', 'usuario');
  adminViewUid = 'todos';
  state.preparations = [pAYfor];
  filterStatus = 'todos'; searchText = ''; showOthers = true;
  render();
  upAY.length = 0;
  global.localStorage.removeItem('checklist-soporte-v1');
  document.getElementById('toast').textContent = '';
  var btnAY6 = clickGuardar('ay-for');
  var noSaveAY6 = global.localStorage.getItem('checklist-soporte-v1') === null;
  var noUpAY6 = upAY.length === 0;
  var toastAY6 = toastTxt().indexOf('otro analista') !== -1;
  var btnAY6ok = btnAY6.textContent === '💾 Guardar avance' && btnAY6.disabled === false;
  console.log('AY6) ajeno bloqueado: sin guardado local:', noSaveAY6, '| sin subida a nube:', noUpAY6, '| aviso de solo lectura:', toastAY6, '| botón sin tocar:', btnAY6ok);

  // AZ: serie nueva 2.4.0 — sin diálogos nativos: toast no modal para
  // avisos, modal inline para confirmaciones y para pedir la contraseña
  // nueva; borrador: 'Usar este equipo' ya no hereda el borrador de
  // 'Completar datos'; diagnóstico de foco en Acerca de.
  // AZ0: estáticos — toast, modal de confirmación y modal de prompt en
  // el HTML; funciones en el script; cero llamadas nativas en el código.
  var az0html = html.includes('id="toast"') && html.includes('id="confirmModal"') && html.includes('id="confirmMsg"') && html.includes('id="confirmYes"') && html.includes('id="confirmNo"') && html.includes('id="promptModal"') && html.includes('id="promptInput"') && html.includes('id="focusDiag"');
  var az0src = SRC.includes('function showToast(') && SRC.includes('function showConfirm(') && SRC.includes('function showPrompt(') && SRC.includes('function updateFocusDiag(') && SRC.includes("document.getElementById('toast')") && SRC.includes("document.getElementById('confirmModal')");
  var az0zero = (SRC.match(/alert\(/g) || []).length === 0 && (SRC.match(/confirm\(/g) || []).length === 0 && (SRC.match(/prompt\(/g) || []).length === 0;
  var az0zeroHtml = (html.match(/alert\(/g) || []).length === 0 && (html.match(/confirm\(/g) || []).length === 0 && (html.match(/prompt\(/g) || []).length === 0;
  console.log('AZ0) toast + modales + foco en HTML:', az0html, '| funciones en el script:', az0src, '| cero nativos en el script:', az0zero, '| cero nativos en todo el HTML:', az0zeroHtml);
  // AZ1: el toast aparece con el mensaje, no roba el foco y se
  // auto-oculta a los ~3 s; no bloquea la ejecución (la línea siguiente
  // corre de inmediato).
  var toastElAZ = document.getElementById('toast');
  toastElAZ.focus = function () { global.toastFocusedAZ = true; };
  global.toastFocusedAZ = false;
  showToast('Aviso de prueba AZ1');
  var az1after = true;
  var az1show = toastElAZ.textContent === 'Aviso de prueba AZ1' && toastElAZ.hidden === false && global.toastFocusedAZ === false && az1after === true;
  await sleep(3100);
  var az1hide = toastElAZ.hidden === true && toastElAZ.textContent === 'Aviso de prueba AZ1';
  console.log('AZ1) toast visible con el mensaje y sin robar foco:', az1show, '| se auto-oculta a los ~3 s:', az1hide);
  // AZ2a: eliminar equipo — modal con su pregunta; con No no borra y
  // cierra; con Sí borra en la nube.
  loginAs('u1', 'Test User', 'usuario');
  CLOUD_ENABLED = true;
  var pAZ2 = mkPrepAU({ id: 'az2', createdAt: Date.now() - 100000 });
  state.preparations = [pAZ2];
  filterStatus = 'todos'; searchText = ''; todosPage = 0; showOthers = false;
  render();
  var delPrepAZ = [];
  global.Cloud.deletePrep = async function (id) { delPrepAZ.push(id); };
  realClick('data-del-prep', 'az2');
  var az2aModal = document.getElementById('confirmModal').hidden === false && document.getElementById('confirmMsg').textContent === '¿Eliminar este equipo y su checklist?';
  var az2aBefore = state.preparations.some(function (p) { return p.id === 'az2'; }) && delPrepAZ.length === 0;
  answerConfirm(false);
  await sleep(20);
  var az2aNo = state.preparations.some(function (p) { return p.id === 'az2'; }) && delPrepAZ.length === 0 && document.getElementById('confirmModal').hidden === true;
  realClick('data-del-prep', 'az2');
  answerConfirm(true);
  await sleep(20);
  var az2aSi = !state.preparations.some(function (p) { return p.id === 'az2'; }) && delPrepAZ.indexOf('az2') !== -1;
  console.log('AZ2a) eliminar equipo: abre el modal con su pregunta:', az2aModal, '| antes de responder no borra:', az2aBefore, '| con No no borra y cierra:', az2aNo, '| con Sí borra en la nube:', az2aSi);
  // AZ2b: borrar mensaje del chat del equipo — solo con Sí.
  cloudUser = { uid: 'u1', email: 'test@checklist.local', nombre: 'Test User' };
  cloudRole = 'admin';
  chatMessages = [{ id: 'mAZ', uid: 'u2', nombre: 'Alejandro', texto: 'Hola', createdAt: Date.now() - 60000 }];
  dmMessages = []; dmPeer = null;
  teamUsers = [{ uid: 'u1', nombre: 'Test User', rol: 'usuario' }, { uid: 'u2', nombre: 'Alejandro', rol: 'usuario' }];
  presenceList = [];
  renderEquipo();
  var delChatAZ = [];
  global.Cloud.deleteChatMessage = async function (id) { delChatAZ.push(id); };
  function clickDelChatAZ() {
    document.getElementById('chatBox')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-del-chat]' ? { getAttribute: function () { return 'mAZ'; } } : null; } } });
  }
  clickDelChatAZ();
  var az2bModal = document.getElementById('confirmModal').hidden === false && document.getElementById('confirmMsg').textContent === '¿Borrar este mensaje para todos?';
  answerConfirm(false);
  await sleep(20);
  var az2bNo = delChatAZ.length === 0;
  clickDelChatAZ();
  answerConfirm(true);
  await sleep(20);
  var az2bSi = delChatAZ.length === 1 && delChatAZ[0] === 'mAZ';
  console.log('AZ2b) borrar mensaje: abre el modal con su pregunta:', az2bModal, '| con No no borra:', az2bNo, '| con Sí borra:', az2bSi);
  // AZ2c: borrar usuario (admin) — solo con Sí.
  cloudUser = { uid: 'u1', email: 'test@checklist.local', nombre: 'Test User' };
  cloudRole = 'admin';
  lastUsers = [{ uid: 'uAZ', nombre: 'Borrar Yo', usuario: 'borraryo', email: 'b@x.com', rol: 'usuario', activo: true }];
  var delUserAZ = [];
  global.Cloud.deleteUserByAdmin = async function (uid) { delUserAZ.push(uid); };
  function clickUserDelAZ() {
    document.getElementById('userList')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-user-del]' ? { getAttribute: function () { return 'uAZ'; } } : null; } } });
  }
  clickUserDelAZ();
  var az2cModal = document.getElementById('confirmModal').hidden === false && document.getElementById('confirmMsg').textContent === '¿Eliminar a Borrar Yo? Ya no podrá entrar a la app.';
  answerConfirm(false);
  await sleep(20);
  var az2cNo = delUserAZ.length === 0;
  clickUserDelAZ();
  answerConfirm(true);
  await sleep(20);
  var az2cSi = delUserAZ.length === 1 && delUserAZ[0] === 'uAZ';
  console.log('AZ2c) borrar usuario: abre el modal con su pregunta:', az2cModal, '| con No no borra:', az2cNo, '| con Sí borra:', az2cSi);
  // AZ2d: quitar la clave de la IA — solo con Sí.
  var setAiAZ = [];
  global.Cloud.setAiKey = async function (k) { setAiAZ.push(k); };
  document.getElementById('btnAiQuitar')._h.click[0]();
  var az2dModal = document.getElementById('confirmModal').hidden === false && document.getElementById('confirmMsg').textContent === '¿Quitar la clave de la IA? La IA dejará de funcionar en todos los teléfonos.';
  answerConfirm(false);
  await sleep(20);
  var az2dNo = setAiAZ.length === 0;
  document.getElementById('btnAiQuitar')._h.click[0]();
  answerConfirm(true);
  await sleep(20);
  var az2dSi = setAiAZ.length === 1 && setAiAZ[0] === '';
  console.log('AZ2d) quitar clave IA: abre el modal con su pregunta:', az2dModal, '| con No no la quita:', az2dNo, '| con Sí la quita:', az2dSi);
  // AZ3: 'Usar este equipo' tras 'Completar datos' sin guardar crea un
  // equipo NUEVO y no toca el borrador (bug latente de la 2.3.9).
  loginAs('u1', 'Test User', 'usuario');
  CLOUD_ENABLED = true;
  var upAZ3 = [];
  global.Cloud.upsertPrep = async function (d) { upAZ3.push(d); };
  global.Cloud.markDetectadoUsado = async function () {};
  var borAZ3 = mkPrepAU({ id: 'az3-bor', borrador: true, equipo: { tipo: 'Laptop', marca: 'HP', modelo: 'ModeloBorradorAZ3', serie: 'S-AZ3', inventario: '9' }, usuario: { nombre: 'Viejo', area: '', correo: '' } });
  state.preparations = [borAZ3];
  filterStatus = 'todos'; searchText = ''; todosPage = 0; showOthers = false;
  render();
  realClick('data-completar', 'az3-bor');
  var az3open = window._completarBorradorId === 'az3-bor' && document.getElementById('btnAdd').textContent === '💾 Guardar datos completos';
  detectados = [{ id: 'AZ3-DET', hostname: 'PC-AZ3', marca: 'Lenovo', modelo: 'ThinkCentre AZ3', serie: 'AZ3-DET', cpu: 'i5', ramGB: 8, discoGB: 256, so: 'Windows 11', tipo: 'Desktop', detectadoEn: Date.now() - 60000, detectadoPor: 'Gerardo', usado: false, checks: { t18: true }, detalles: {}, versiones: {} }];
  renderDetectados();
  document.getElementById('detList')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-det-use]' ? { getAttribute: function () { return 'AZ3-DET'; } } : null; } } });
  var az3clean = window._completarBorradorId === null && document.getElementById('btnAdd').textContent === '💾 Guardar equipo';
  document.getElementById('fUser').value = 'Ana AZ3';
  document.getElementById('fTec').value = 'Test User';
  var nAZ3 = state.preparations.length;
  document.getElementById('btnAdd')._h.click[0]();
  var newAZ3 = state.preparations.find(function (p) { return p.equipo && p.equipo.modelo === 'ThinkCentre AZ3'; });
  var borAZ3after = state.preparations.find(function (p) { return p.id === 'az3-bor'; });
  var az3new = state.preparations.length === nAZ3 + 1 && !!newAZ3 && newAZ3.id !== 'az3-bor';
  var az3bor = !!borAZ3after && borAZ3after.borrador === true && borAZ3after.equipo.modelo === 'ModeloBorradorAZ3' && borAZ3after.usuario.nombre === 'Viejo';
  console.log('AZ3) Completar abre el borrador:', az3open, '| Usar limpia el borrador pendiente y el botón:', az3clean, '| Guardar crea un equipo nuevo:', az3new, '| el borrador viejo intacto:', az3bor);
  // AZ4: diagnóstico de foco en Acerca de, actualizado en cada render.
  render();
  var fdAZ4 = document.getElementById('focusDiag').textContent;
  var az4 = fdAZ4.indexOf('Foco: sí') !== -1 && fdAZ4.indexOf('Elemento activo: ninguno') !== -1;
  var az4html = html.includes('id="focusDiag"') && html.includes('Foco:');
  console.log('AZ4) diagnóstico de foco en Acerca de:', az4html, '| actualizado en render:', az4, '| texto:', fdAZ4);
  // AZ5: la contraseña nueva del usuario se pide con modal inline
  // (no prompt nativo): Cancelar no cambia nada, la corta avisa con
  // toast y no cambia, la válida la cambia.
  cloudUser = { uid: 'u1', email: 'test@checklist.local', nombre: 'Test User' };
  cloudRole = 'admin';
  lastUsers = [{ uid: 'uAZ5', nombre: 'Clave Yo', usuario: 'clvyo', email: 'c@x.com', rol: 'usuario', activo: true }];
  var resetAZ5 = [];
  global.Cloud.adminResetPassword = async function (o) { resetAZ5.push(o); };
  function clickUserPassAZ() {
    document.getElementById('userList')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-user-pass]' ? { getAttribute: function () { return 'uAZ5'; } } : null; } } });
  }
  clickUserPassAZ();
  var az5Modal = document.getElementById('promptModal').hidden === false && document.getElementById('promptMsg').textContent.indexOf('Nueva contraseña para Clave Yo') !== -1;
  answerPrompt(null);
  await sleep(20);
  var az5Cancel = resetAZ5.length === 0;
  clickUserPassAZ();
  answerPrompt('corta');
  await sleep(20);
  var az5Short = resetAZ5.length === 0 && toastTxt().indexOf('al menos 6 caracteres') !== -1;
  clickUserPassAZ();
  answerPrompt('nueva123');
  await sleep(20);
  var az5Ok = resetAZ5.length === 1 && resetAZ5[0].newPassword === 'nueva123' && resetAZ5[0].uid === 'uAZ5';
  console.log('AZ5) pedir contraseña abre el modal con su pregunta:', az5Modal, '| Cancelar no cambia nada:', az5Cancel, '| corta avisa y no cambia:', az5Short, '| válida la cambia:', az5Ok);

  // BA: serie 2.5.0 — Mantenimientos Preventivos (sin cambios en 2.5.1/2.5.2 salvo BB).
  function mkMant(over) {
    return mantFromCloud(Object.assign({ id: 'm1', createdAt: Date.now(), folio: null, estado: 'borrador', tecnicoUid: 'u1', tecnico: 'Test User', empresa: 'Lapi', anio: 2026, tipo: 'SOFTWARE', area: 'Sistemas', responsable: 'Ana', tiempoReparacion: '2 horas', tiempoViaje: '30 min', tiempoSistemaCaido: '1 hora', fechaServicio: '2026-11-15', fechaTermino: '2026-11-15', tituloCaso: 'Laptop lenta', tipoFalla: 'Software', identificacion: { impresora: true, cpu: true, monitor: true, teclado: true, mouse: true, noBreak: false }, descripcionEquipo: 'Laptop Dell Inspiron', condiciones: { impresora: true, cpu: true, monitor: true, teclado: true, mouse: true, noBreak: false, notas: '' }, preventivo: { impresora: true, cpu: true, monitor: false, teclado: false, mouse: false, noBreak: false }, descripcionCambios: 'Se reinstaló el SO', conclusion: 'Equipo listo', comentarios: '', fechaPlaneacion: '2026-11-14', fechaCompromiso: '2026-11-15', periodoPrueba: '5 días', fechaLiberacion: '2026-11-20', observaciones: 'Sin observaciones', observacionesDetectadas: 'Procesador: Intel i5', equipo: { tipo: 'Laptop', marca: 'Dell', modelo: 'Inspiron 3501', serie: 'S1', hostname: 'PC-01', cpu: 'Intel Core i5', ramGB: 8, discoGB: 256, discoTipo: 'SSD', ip: '192.168.1.45', redes: [{ nombre: 'Wi-Fi', ip: '192.168.1.45', ipTipo: 'Dinámica' }], impresora: 'HP LaserJet', anydeskId: '123456789', anydeskAlias: 'Oficina', antivirus: 'ESET NOD32', politicas: { cambioDias: 90, minLongitud: 10, bloqueoIntentos: 5, bloqueoSegundos: 350, cumpleCambio: true, cumpleLongitud: true, cumpleIntentos: true, cumpleBloqueo: true, cumple: true }, usuarioSistemas: true, so: 'Windows 11 Pro', versiones: { so: 'Windows 11 Pro 26H2', antivirus: 'ESET NOD32 Antivirus 18.0.12', esetAgent: '', chrome: '141.0.7390.65' } }, whatsappUsuario: '5512345678', firmaTecnico: '', firma: null }, over || {}));
  }
  function fillMantFormBA(serie, host, modelo) {
    mantOpenForm(null, null);
    document.getElementById('fM-tecnico').value = 'Test User';
    document.getElementById('fM-serie').value = serie;
    document.getElementById('fM-hostname').value = host;
    document.getElementById('fM-modelo').value = modelo;
    document.getElementById('fM-area').value = 'Sistemas';
    document.getElementById('fM-responsable').value = 'Ana';
    document.getElementById('fM-titulo').value = 'Caso ' + serie;
    document.getElementById('fM-tipoFalla').value = 'Software';
    document.getElementById('fM-descEquipo').value = 'Equipo ' + serie;
    document.getElementById('fM-fechaServ').value = '2026-11-15';
    document.getElementById('fM-whatsapp').value = '5512345678';
    mantFirmaData = 'data:image/png;base64,iVBORw0KGgo=';
  }
  // BA0: estáticos — selector, tabs, formulario, firebase.js y reglas.
  var ba0html = html.includes('Versión 2.5.2') && html.includes('Versión: 2.5.2') && !html.includes('2.5.0');
  var ba0sel = html.includes('id="viewInicio"') && html.includes('id="btnGoMant"') && html.includes('Mantenimientos Preventivos') && html.includes('data-v="inicio"') && html.includes('data-v="mant"');
  var ba0form = ['fM-serie', 'fM-hostname', 'fM-modelo', 'fM-tecnico', 'fM-empresa', 'fM-tipo-sw', 'fM-tipo-hw', 'fM-anio', 'fM-area', 'fM-responsable', 'fM-titulo', 'fM-tipoFalla', 'fM-descEquipo', 'fM-observaciones', 'fM-obsDet', 'fM-whatsapp', 'fM-firmaCanvas', 'btnMantCrear', 'btnMantGuardar', 'btnMantCancelar', 'mantDetList', 'mantAdminFilter', 'mantOrderBox', 'btnMantWaLink', 'btnMantPdf', 'btnMantCompartir', 'btnMantCancelarOrden', 'btnMantEliminarOrden'].every(function (id) { return html.includes('id="' + id + '"'); });
  var ba0fb = ['subscribeMantenimientos', 'upsertMant', 'deleteMant', 'getMantenimiento', 'getAllMantenimientos', 'asignarFolio', 'guardarFirma'].every(function (f) { return fb.includes(f); });
  var ba0rules = rules.includes('match /mantenimientos/{id}') && rules.includes('match /config/folios') && rules.includes('allow get: if true') && rules.includes('resource.data.siguiente + 1');
  console.log('BA0) versión 2.5.2 sin 2.5.0:', ba0html, '| selector y tabs Inicio/Mant:', ba0sel, '| formulario y orden completos:', ba0form, '| firebase.js con mantenimientos y folio:', ba0fb, '| reglas mantenimientos y folios:', ba0rules);
  // BA1: el selector es la vista al abrir; los 4 botones navegan; un
  // usuario normal no entra a Usuarios (va al selector, no a Preparar).
  loginAs('u1', 'Test User', 'usuario');
  showVista('inicio');
  var ba1inicio = document.getElementById('viewInicio').hidden === false && document.getElementById('viewPreparar').hidden === true && document.getElementById('viewMant').hidden === true && document.getElementById('viewRenta-rec').hidden === true;
  document.getElementById('btnGoMant')._h.click[0]();
  var ba1mant = document.getElementById('viewMant').hidden === false && document.getElementById('viewInicio').hidden === true;
  document.getElementById('btnGoPreparar')._h.click[0]();
  var ba1prep = document.getElementById('viewPreparar').hidden === false;
  cloudRole = 'usuario';
  showVista('usuarios');
  var ba1nouser = document.getElementById('viewInicio').hidden === false && document.getElementById('viewUsuarios').hidden === true;
  console.log('BA1) al abrir: selector visible:', ba1inicio, '| botón Mantenimientos abre la vista:', ba1mant, '| botón Por preparar navega:', ba1prep, '| usuario normal fuera de Usuarios va al selector:', ba1nouser);
  // BA2: políticas cumple/no cumple (90 días, 10 caracteres, 5 intentos, 350 s).
  var polOk = mantPoliticasCumple({ cambioDias: 90, minLongitud: 10, bloqueoIntentos: 5, bloqueoSegundos: 350 });
  var polOk2 = mantPoliticasCumple({ cambioDias: 30, minLongitud: 12, bloqueoIntentos: 3, bloqueoSegundos: 600 });
  var polBad = mantPoliticasCumple({ cambioDias: 180, minLongitud: 8, bloqueoIntentos: 10, bloqueoSegundos: 60 });
  var polVacio = mantPoliticasCumple({});
  var ba2 = polOk.cumple === true && polOk2.cumple === true && polBad.cumple === false && polBad.cumpleCambio === false && polBad.cumpleLongitud === false && polBad.cumpleIntentos === false && polBad.cumpleBloqueo === false && polVacio.cumple === null;
  var ba2card = mantCardHtml(mkMant()).includes('Políticas: ✓ Cumple');
  var mBad = mkMant();
  mBad.equipo.politicas = { cambioDias: 180, minLongitud: 8, bloqueoIntentos: 10, bloqueoSegundos: 60, cumpleCambio: false, cumpleLongitud: false, cumpleIntentos: false, cumpleBloqueo: false, cumple: false };
  var ba2cardBad = mantCardHtml(mBad).includes('Políticas: ✗ No cumple');
  var ba2txt = politicasText({ cambioDias: 90, minLongitud: 10, bloqueoIntentos: 5, bloqueoSegundos: 350 }).indexOf('Cumple') !== -1;
  console.log('BA2) políticas: justo en lo esperado cumple:', ba2, '| tarjeta cumple:', ba2card, '| tarjeta no cumple:', ba2cardBad, '| texto compilado:', ba2txt);
  // BA3: observaciones detectadas compiladas (software, IPs, AnyDesk,
  // impresora, antivirus, políticas, usuario de sistemas, ids).
  var detBA3 = { id: 'BA3-DET', hostname: 'PC-BA3', marca: 'HP', modelo: 'EliteDesk 800', serie: 'BA3-DET', cpu: 'Intel Core i7-10700', ramGB: 16, discoGB: 512, discoTipo: 'SSD', so: 'Windows 11 Pro', tipo: 'Desktop', detectadoEn: Date.now() - 60000, detectadoPor: 'Gerardo', usado: false, checks: { t18: true }, detalles: { impresora: 'HP LaserJet' }, versiones: { so: 'Windows 11 Pro 26H2 (compilación 26200)', antivirus: 'ESET NOD32 Antivirus 18.0.12', chrome: '141.0.7390.65' }, ip: '192.168.1.45', ipTipo: 'Dinámica', redes: [{ nombre: 'Wi-Fi', ip: '192.168.1.45', ipTipo: 'Dinámica' }, { nombre: 'Ethernet', ip: '10.0.0.20', ipTipo: 'Estática' }], anydeskId: '123456789', anydeskAlias: 'Oficina', politicas: { cambioDias: 90, minLongitud: 10, bloqueoIntentos: 5, bloqueoSegundos: 350 }, usuarioSistemas: true };
  var obsBA3 = compileObservacionesDetectadas(detBA3);
  var ba3 = ['Procesador: Intel Core i7-10700', 'RAM: 16 GB', 'Disco: 512 GB SSD', 'IP: 192.168.1.45', 'Redes: Wi-Fi: 192.168.1.45 (Dinámica) · Ethernet: 10.0.0.20 (Estática)', 'Versiones detectadas: SO: Windows 11 Pro 26H2', 'Antivirus: ESET NOD32 Antivirus 18.0.12', 'Chrome: 141.0.7390.65', 'AnyDesk: 123 456 789 (Oficina)', 'Impresora: HP LaserJet', 'Políticas: cambio cada 90 días ✓', 'Usuario de sistemas: Sí', 'Hostname: PC-BA3', 'Serie: BA3-DET', 'Modelo: HP EliteDesk 800'].every(function (s) { return obsBA3.indexOf(s) !== -1; });
  var mBA3 = mantFromDetectado(detBA3);
  var ba3b = mBA3.equipo.serie === 'BA3-DET' && mBA3.equipo.hostname === 'PC-BA3' && mBA3.equipo.modelo === 'EliteDesk 800' && mBA3.observacionesDetectadas === obsBA3 && mBA3.equipo.politicas.cumple === true && mBA3.equipo.redes.length === 2;
  console.log('BA3) observaciones compiladas con todo:', ba3, '| mantFromDetectado llena serie/host/modelo y políticas:', ba3b);
  // BA4: 'Usar este equipo' en Mantenimientos llena el formulario.
  loginAs('u1', 'Test User', 'usuario');
  CLOUD_ENABLED = true;
  detectados = [detBA3];
  renderMantDetectados();
  document.getElementById('mantDetList')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-mant-det-use]' ? { getAttribute: function () { return 'BA3-DET'; } } : null; } } });
  var ba4form = document.getElementById('mantFormBox').hidden === false && document.getElementById('fM-serie').value === 'BA3-DET' && document.getElementById('fM-hostname').value === 'PC-BA3' && document.getElementById('fM-modelo').value === 'EliteDesk 800' && document.getElementById('fM-obsDet').value.indexOf('Procesador: Intel Core i7-10700') !== -1 && document.getElementById('fM-tecnico').value === 'Test User' && document.getElementById('fM-eq-redes').value.indexOf('192.168.1.45') !== -1;
  console.log('BA4) Usar este equipo llena el formulario (serie/host/modelo/obs/tecnico/redes):', ba4form);
  // BA5: crear orden bloqueada sin serie, sin hostname y sin modelo (el
  // toast dice cuál falta); con los tres, crea la orden.
  var upBA5 = [];
  global.Cloud.upsertMant = async function (d) { upBA5.push(d); };
  global.Cloud.asignarFolio = async function () { return '00001'; };
  var nBA5 = mantenimientos.length;
  fillMantFormBA('', '', '');
  document.getElementById('btnMantCrear')._h.click[0](); await sleep(20);
  var ba5sinSerie = mantenimientos.length === nBA5 && toastTxt().indexOf('número de serie') !== -1;
  document.getElementById('fM-serie').value = 'S-BA5';
  document.getElementById('btnMantCrear')._h.click[0](); await sleep(20);
  var ba5sinHost = mantenimientos.length === nBA5 && toastTxt().indexOf('hostname') !== -1;
  document.getElementById('fM-hostname').value = 'PC-BA5';
  document.getElementById('btnMantCrear')._h.click[0](); await sleep(20);
  var ba5sinMod = mantenimientos.length === nBA5 && toastTxt().indexOf('modelo') !== -1;
  document.getElementById('fM-modelo').value = 'Inspiron 3501';
  document.getElementById('btnMantCrear')._h.click[0](); await sleep(20);
  var creadaBA5 = mantenimientos.find(function (m) { return m.folio === '00001'; });
  var ba5creada = !!creadaBA5 && creadaBA5.estado === 'creada' && creadaBA5.equipo.serie === 'S-BA5' && creadaBA5.equipo.hostname === 'PC-BA5' && upBA5.length >= 1 && document.getElementById('mantOrderBox').hidden === false;
  console.log('BA5) sin serie bloquea:', ba5sinSerie, '| sin hostname bloquea:', ba5sinHost, '| sin modelo bloquea:', ba5sinMod, '| con los tres crea la orden con folio:', ba5creada);
  // BA6: folio 00001 y siguiente 00002 (contador simulado de la transacción).
  mantenimientos = [];
  var siguienteBA6 = 1;
  global.Cloud.asignarFolio = async function () { var n = siguienteBA6; siguienteBA6 = n + 1; return String(n).padStart(5, '0'); };
  fillMantFormBA('S-BA6A', 'PC-BA6A', 'Modelo A');
  document.getElementById('btnMantCrear')._h.click[0](); await sleep(20);
  var ordA = mantenimientos.find(function (m) { return m.equipo.serie === 'S-BA6A'; });
  fillMantFormBA('S-BA6B', 'PC-BA6B', 'Modelo B');
  document.getElementById('btnMantCrear')._h.click[0](); await sleep(20);
  var ordB = mantenimientos.find(function (m) { return m.equipo.serie === 'S-BA6B'; });
  var ba6 = !!ordA && ordA.folio === '00001' && !!ordB && ordB.folio === '00002' && siguienteBA6 === 3;
  console.log('BA6) primera orden folio 00001:', ba6, '| segunda orden folio 00002 y contador en 3:', !!ordB && ordB.folio === '00002' && siguienteBA6 === 3);
  // BA7: sin conexión no hay folio: se guarda como borrador sin folio; el
  // borrador también se guarda sin serie/hostname/modelo.
  global.Cloud.asignarFolio = async function () { throw new Error('offline'); };
  fillMantFormBA('S-BA7', 'PC-BA7', 'Modelo BA7');
  document.getElementById('btnMantCrear')._h.click[0](); await sleep(20);
  var borBA7 = mantenimientos.find(function (m) { return m.equipo.serie === 'S-BA7'; });
  var ba7 = !!borBA7 && borBA7.estado === 'borrador' && borBA7.folio === null && toastTxt().indexOf('Sin conexión') !== -1 && toastTxt().indexOf('borrador') !== -1;
  mantOpenForm(null, null);
  document.getElementById('fM-titulo').value = 'Borrador sin ids';
  document.getElementById('btnMantGuardar')._h.click[0]();
  var borBA7b = mantenimientos.find(function (m) { return m.tituloCaso === 'Borrador sin ids 2026'; });
  var ba7b = !!borBA7b && borBA7b.estado === 'borrador' && borBA7b.folio === null && borBA7b.equipo.serie === '' && borBA7b.equipo.hostname === '' && borBA7b.equipo.modelo === '' && borBA7b.tituloCaso === 'Borrador sin ids 2026' && borBA7b.anio === 2026 && toastTxt().indexOf('Borrador guardado') !== -1;
  console.log('BA7) sin conexión: borrador sin folio:', ba7, '| borrador sin serie/host/modelo sí guarda:', ba7b);
  // BA8: link de firma con id y WhatsApp con 52 antepuesto a 10 dígitos.
  var mBA8 = mkMant({ id: 'ba8', folio: '00003', estado: 'creada', whatsappUsuario: '55 1234-5678' });
  var ba8url = mantFirmaUrl(mBA8) === 'https://checklist-soporte.web.app/firma.html?id=ba8';
  var waBA8 = mantFirmaWaUrl(mBA8);
  var ba8wa = waBA8.indexOf('https://wa.me/525512345678?text=') === 0 && decodeURIComponent(waBA8.split('text=')[1]).indexOf('https://checklist-soporte.web.app/firma.html?id=ba8') !== -1 && decodeURIComponent(waBA8.split('text=')[1]).indexOf('folio 00003') !== -1;
  var ba8num = mantWaNumber('5512345678') === '525512345678' && mantWaNumber('+52 55 1234 5678') === '525512345678' && mantWaNumber('123456789012') === '123456789012';
  var openedBA8 = [];
  global.open = function (url, target) { openedBA8.push([url, target]); };
  mantenimientos = [mBA8];
  mantOrderId = 'ba8';
  mantEnviarLink();
  var ba8open = openedBA8.length === 1 && openedBA8[0][0] === waBA8 && openedBA8[0][1] === '_blank';
  console.log('BA8) link de firma con id:', ba8url, '| wa.me con 52 y link:', ba8wa, '| normalización de números:', ba8num, '| Enviar abre wa.me:', ba8open);
  // BA9: PDF bloqueado sin firma del técnico y sin firma del usuario; con
  // ambas, PDF con encabezado, secciones, ids en Descripción y en
  // Observaciones, firmas y satisfacción; imágenes JPEG incrustadas.
  var mBA9 = mkMant({ id: 'ba9', folio: '00001', estado: 'creada' });
  mBA9.firmaTecnico = '';
  var ba9sinTec = mantPdfFalta(mBA9) === 'la firma del técnico';
  mBA9.firmaTecnico = 'data:image/png;base64,iVBORw0KGgo=';
  var ba9sinUsr = mantPdfFalta(mBA9) === 'la firma del usuario';
  mBA9.firma = { nombre: 'Ana López', area: 'Ventas', comentarios: 'Todo bien', satisfaccion: 9, firma: 'data:image/png;base64,iVBORw0KGgo=', firmadoEn: Date.now() };
  var ba9ok = mantPdfFalta(mBA9) === null;
  await sharePdfMant(mkMant({ id: 'ba9b', folio: '00002', estado: 'creada', firmaTecnico: '' }));
  var ba9toast = toastTxt().indexOf('firma del técnico') !== -1;
  var pdfBA9 = Buffer.from(await buildPdfMant(mBA9, {}).arrayBuffer()).toString('latin1');
  var ba9need = ['Lapi Sistemas', 'Rosa Blanca 63', 'ORDEN DE SERVICIO', 'Folio: 00001', 'Formato F0.S1.01 Rev0', 'Título del caso: Laptop lenta', 'Descripción del equipo', 'Observaciones', 'Datos detectados:', 'Procesador: Intel i5', 'Observaciones del técnico:', 'Sin observaciones', 'Conformidad del usuario', 'Ana López', 'Escala de satisfacción', '9 \\(EXCELENTE\\)', '[9]', 'INACEPTABLE 0-3', 'Políticas: cambio cada 90 días', 'Firma: Test User \\(guardada en la app\\)', 'Firma: Ana López \\(guardada en la app\\)'];
  var ba9pdf = ba9need.every(function (s) { return pdfBA9.indexOf(s) !== -1; }) && pdfBA9.indexOf('Sistemas') !== -1 && pdfBA9.indexOf('Planeación') !== -1 && pdfBA9.indexOf('Área solicitante') !== -1 && pdfBA9.indexOf('Liberación') !== -1;
  var ba9ambos = (pdfBA9.match(/Serie: S1/g) || []).length >= 2 && (pdfBA9.match(/Hostname: PC-01/g) || []).length >= 2 && (pdfBA9.match(/Modelo: Inspiron 3501/g) || []).length >= 2;
  var JPEG1X1 = '/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAP//////////////////////////////////////////////////////////////////////////////////////2wBDAf//////////////////////////////////////////////////////////////////////////////////////wAARCAABAAEDASIAAhEBAxEB/8QAFAABAAAAAAAAAAAAAAAAAAAACf/EABQQAQAAAAAAAAAAAAAAAAAAAAD/xAAUAQEAAAAAAAAAAAAAAAAAAAAA/8QAFBEBAAAAAAAAAAAAAAAAAAAAAP/aAAwDAQACEQMRAD8AvwH/2Q==';
  var jpgBytes = new Uint8Array(Buffer.from(JPEG1X1, 'base64'));
  var pdfImg = Buffer.from(await buildPdfMant(mBA9, { tecnico: { bytes: jpgBytes, w: 1, h: 1 }, usuario: { bytes: jpgBytes, w: 1, h: 1 } }).arrayBuffer()).toString('latin1');
  var ba9img = pdfImg.indexOf('/Subtype /Image') !== -1 && pdfImg.indexOf('/DCTDecode') !== -1 && pdfImg.indexOf('/Imtecnico Do') !== -1 && pdfImg.indexOf('/Imusuario Do') !== -1 && (pdfImg.match(/\/Subtype \/Image/g) || []).length === 2;
  console.log('BA9) sin firma técnico bloquea:', ba9sinTec, '| sin firma usuario bloquea:', ba9sinUsr, '| con ambas listo:', ba9ok, '| botón avisa con toast:', ba9toast, '| PDF con todo:', ba9pdf, '| ids en Descripción y en Observaciones:', ba9ambos, '| firmas JPEG incrustadas:', ba9img);
  // BA10: compartir copia solo con ambas firmas (botón deshabilitado sin
  // la del usuario; share nativo con el PDF cuando están las dos).
  var mBA10 = mkMant({ id: 'ba10', folio: '00004', estado: 'creada', firmaTecnico: 'data:image/png;base64,iVBORw0KGgo=' });
  mantenimientos = [mBA10];
  mantShowOrder('ba10');
  var ba10dis = document.getElementById('btnMantCompartir').disabled === true && document.getElementById('mantOrderNote').textContent.indexOf('firma del usuario') !== -1;
  await shareMantCopy(mBA10);
  var ba10toast = toastTxt().indexOf('firma del usuario') !== -1;
  mBA10.firma = { nombre: 'Ana López', area: 'Ventas', comentarios: '', satisfaccion: 8, firma: 'data:image/png;base64,iVBORw0KGgo=', firmadoEn: Date.now() };
  var sharedBA10 = [];
  global.Capacitor = { Plugins: { Filesystem: { writeFile: async function (o) { return { uri: 'file:///cache/' + o.path }; } }, Share: { share: async function (o) { sharedBA10.push(o); } } } };
  global.FileReader = class { constructor() { this.result = null; } readAsDataURL(blob) { var self = this; blob.arrayBuffer().then(function (ab) { self.result = 'data:application/pdf;base64,' + Buffer.from(ab).toString('base64'); if (self.onload) self.onload(); }); } };
  mantShowOrder('ba10');
  var ba10en = document.getElementById('btnMantCompartir').disabled === false;
  await shareMantCopy(mBA10);
  var ba10share = sharedBA10.length === 1 && sharedBA10[0].url === 'file:///cache/orden-servicio-00004.pdf' && sharedBA10[0].dialogTitle === 'Compartir copia con el usuario';
  console.log('BA10) sin firma usuario: botón deshabilitado y nota:', ba10dis, '| intento avisa con toast:', ba10toast, '| con ambas: botón habilitado:', ba10en, '| share nativo con el PDF:', ba10share);
  // BA11: visibilidad — el usuario normal solo ve los suyos (con respaldo
  // por nombre para registros viejos); el admin ve todos y filtra por usuario.
  teamUsers = [
    { uid: 'u1', nombre: 'Test User', rol: 'usuario', email: 'test@checklist.local' },
    { uid: 'uAxel', nombre: 'Axel Danyael', rol: 'usuario', email: 'axel@checklist.local' },
    { uid: 'uAle', nombre: 'Alejandro', rol: 'usuario', email: 'alejandro@checklist.local' },
  ];
  mantenimientos = [
    mkMant({ id: 'ba11-own', tecnicoUid: 'u1', tecnico: 'Test User', tituloCaso: 'Mío' }),
    mkMant({ id: 'ba11-axel', tecnicoUid: 'uAxel', tecnico: 'Axel Danyael', tituloCaso: 'De Axel' }),
    mkMant({ id: 'ba11-old', tecnicoUid: '', tecnico: 'Test User', tituloCaso: 'Viejo sin uid' }),
  ];
  loginAs('u1', 'Test User', 'usuario');
  renderMant();
  var htmlU = document.getElementById('mantList').innerHTML;
  var ba11u = htmlU.indexOf('Mío') !== -1 && htmlU.indexOf('De Axel') === -1 && htmlU.indexOf('Viejo sin uid') !== -1 && document.getElementById('mantAdminRow').hidden === true;
  loginAs('uGer', 'Gerardo', 'admin');
  mantAdminViewUid = 'todos';
  renderMant();
  var htmlA = document.getElementById('mantList').innerHTML;
  var ba11a = htmlA.indexOf('Mío') !== -1 && htmlA.indexOf('De Axel') !== -1 && htmlA.indexOf('Viejo sin uid') !== -1 && document.getElementById('mantAdminRow').hidden === false;
  mantAdminViewUid = 'uAxel';
  renderMant();
  var htmlAx = document.getElementById('mantList').innerHTML;
  var ba11ax = htmlAx.indexOf('De Axel') !== -1 && htmlAx.indexOf('Mío') === -1;
  mantAdminViewUid = 'todos';
  var ba11noToggle = html.indexOf('Ver mantenimientos de otros') === -1 && !html.includes('btnVerOtrosMant');
  console.log('BA11) usuario solo ve los suyos (+ respaldo por nombre):', ba11u, '| admin ve todos:', ba11a, '| admin filtra por analista:', ba11ax, '| sin toggle de ver otros:', ba11noToggle);
  // BA12: cancelar orden conserva el registro y el folio.
  var mBA12 = mkMant({ id: 'ba12', folio: '00005', estado: 'creada', tituloCaso: 'Para cancelar' });
  mantenimientos = [mBA12];
  loginAs('u1', 'Test User', 'usuario');
  var btnBA12 = {
    getAttribute: function (a) { return a === 'data-mant-cancel-order' ? 'ba12' : null; },
    hasAttribute: function (a) { return a === 'data-mant-cancel-order'; },
    closest: function (sel) { return sel === '[data-mant-cancel-order]' ? btnBA12 : null; },
    classList: { contains: function () { return false; } }
  };
  document.getElementById('mantList')._h.click[0]({ target: btnBA12 });
  var ba12modal = document.getElementById('confirmModal').hidden === false && document.getElementById('confirmMsg').textContent.indexOf('00005') !== -1;
  answerConfirm(false);
  await sleep(20);
  var ba12no = mantenimientos[0].estado === 'creada';
  document.getElementById('mantList')._h.click[0]({ target: btnBA12 });
  answerConfirm(true);
  await sleep(20);
  var ba12si = mantenimientos[0].estado === 'cancelada' && mantenimientos[0].folio === '00005' && mantenimientos.length === 1;
  console.log('BA12) cancelar pide confirmar con el folio:', ba12modal, '| con No no cancela:', ba12no, '| con Sí cancela y conserva folio:', ba12si);
  // BA13: serie, hostname y modelo arriba de la tarjeta y del formulario.
  var mBA13 = mkMant({ id: 'ba13', tituloCaso: 'Tarjeta ids' });
  var cardBA13 = mantCardHtml(mBA13);
  var ba13card = cardBA13.indexOf('Serie: S1 · Hostname: PC-01 · Modelo: Inspiron 3501') !== -1 && cardBA13.indexOf('mant-id-line') !== -1 && cardBA13.indexOf('mant-id-line') < cardBA13.indexOf('Técnico:');
  var ba13hero = html.indexOf('mant-hero') !== -1 && html.indexOf('id="fM-serie"') < html.indexOf('id="fM-tecnico"') && html.indexOf('id="fM-hostname"') < html.indexOf('id="fM-tecnico"') && html.indexOf('id="fM-modelo"') < html.indexOf('id="fM-tecnico"') && html.includes('No. de serie *') && html.includes('Hostname *') && html.includes('Modelo *');
  console.log('BA13) tarjeta con serie/host/modelo arriba:', ba13card, '| formulario con cuadro destacado arriba:', ba13hero);
  // BA14: al entrar, la suscripción filtra por tecnicoUid para usuarios
  // normales y sin filtro para el admin; el login cae en el selector.
  var subBA14 = [];
  global.Cloud.subscribeMantenimientos = function (cb, uid) { subBA14.push(uid); return function () {}; };
  global.Cloud.subscribeRenta = function () { return function () {}; };
  global.Cloud.subscribePreparations = function () { return function () {}; };
  global.Cloud.subscribeDetectados = function () { return function () {}; };
  global.Cloud.subscribePresence = function () { return function () {}; };
  global.Cloud.subscribeChat = function () { return function () {}; };
  global.Cloud.subscribeDm = function () { return function () {}; };
  global.Cloud.heartbeat = function () {};
  global.Cloud.pruneChat = function () {};
  global.Cloud.clearPresence = function () {};
  global.Cloud.listUsers = async function () { return []; };
  global.Cloud.getAllMantenimientos = async function () { return []; };
  global.Cloud.getUserDoc = async function () { return { activo: true, rol: 'usuario', nombre: 'Test User', email: 'test@checklist.local' }; };
  localStorage.setItem('checklist-soporte-migrado-v2:u1', '1');
  localStorage.setItem('checklist-soporte-migrado-preps-v1:u1', '1');
  localStorage.setItem('checklist-soporte-migrado-mant-v1:u1', '1');
  await onAuthChanged({ uid: 'u1', email: 'test@checklist.local' });
  await sleep(20);
  var ba14user = subBA14.length === 1 && subBA14[0] === 'u1' && document.getElementById('viewInicio').hidden === false;
  global.Cloud.getUserDoc = async function () { return { activo: true, rol: 'admin', nombre: 'Gerardo', email: 'gerardo@checklist.local' }; };
  localStorage.setItem('checklist-soporte-migrado-v2:uGer', '1');
  localStorage.setItem('checklist-soporte-migrado-preps-v1:uGer', '1');
  localStorage.setItem('checklist-soporte-migrado-mant-v1:uGer', '1');
  subBA14.length = 0;
  await onAuthChanged({ uid: 'uGer', email: 'gerardo@checklist.local' });
  await sleep(20);
  var ba14admin = subBA14.length === 1 && subBA14[0] === null;
  console.log('BA14) usuario suscribe solo sus mantenimientos y cae en el selector:', ba14user, '| admin suscribe todo:', ba14admin);
  // BA15: el técnico se pre-llena con el login y lo escrito a mano se respeta.
  loginAs('u1', 'Test User', 'usuario');
  mantOpenForm(null, null);
  var ba15auto = document.getElementById('fM-tecnico').value === 'Test User';
  document.getElementById('fM-tecnico').value = 'Otro Nombre';
  prefillMantTecnico();
  var ba15manual = document.getElementById('fM-tecnico').value === 'Otro Nombre';
  document.getElementById('fM-tecnico').value = '';
  prefillMantTecnico();
  var ba15refill = document.getElementById('fM-tecnico').value === 'Test User';
  console.log('BA15) técnico auto con el login:', ba15auto, '| escrito a mano se respeta:', ba15manual, '| vacío se vuelve a llenar:', ba15refill);
  // BA16: cancelar el formulario pide confirmar solo si tiene datos.
  mantOpenForm(null, null);
  document.getElementById('fM-titulo').value = 'Algo';
  document.getElementById('btnMantCancelar')._h.click[0]();
  var ba16modal = document.getElementById('confirmModal').hidden === false;
  answerConfirm(false);
  await sleep(20);
  var ba16no = document.getElementById('mantFormBox').hidden === false;
  document.getElementById('btnMantCancelar')._h.click[0]();
  answerConfirm(true);
  await sleep(20);
  var ba16si = document.getElementById('mantFormBox').hidden === true;
  mantOpenForm(null, null);
  document.getElementById('btnMantCancelar')._h.click[0]();
  var ba16vacio = document.getElementById('mantFormBox').hidden === true && document.getElementById('confirmModal').hidden === true;
  console.log('BA16) con datos pide confirmar:', ba16modal, '| con No sigue abierto:', ba16no, '| con Sí se descarta:', ba16si, '| vacío se cierra sin preguntar:', ba16vacio);
  // BA17: ida y vuelta a la nube + la firma de más de 700 KB no viaja.
  var mBA17 = mkMant();
  mBA17.firmaTecnico = 'x'.repeat(700001);
  var docBA17 = mantToCloudDoc(mBA17);
  var backBA17 = mantFromCloud(docBA17);
  var ba17 = docBA17.firmaTecnico === '' && backBA17.firmaTecnico === '' && backBA17.equipo.serie === 'S1' && backBA17.equipo.politicas.cumple === true && backBA17.identificacion.impresora === true && backBA17.condiciones.notas === '' && backBA17.firma === null && docBA17.folio === null;
  var mBA17b = mkMant();
  mBA17b.firmaTecnico = 'data:image/png;base64,abc';
  var ba17b = mantToCloudDoc(mBA17b).firmaTecnico === 'data:image/png;base64,abc';
  console.log('BA17) firma >700KB no viaja y el resto vuelve intacto:', ba17, '| firma pequeña sí viaja:', ba17b);
  // BA18: reglas exactas de mantenimientos y folios.
  var ba18 = rules.includes('allow list: if isActive() && (isAdmin() || resource.data.tecnicoUid == request.auth.uid)') && rules.includes("changedKeys().hasOnly(['firma', 'estado'])") && rules.includes("request.resource.data.estado == 'firmada'") && rules.includes('match /config/folios') && rules.includes('request.resource.data.siguiente == resource.data.siguiente + 1') && rules.includes('allow create: if isActive() && request.resource.data.siguiente is int');
  console.log('BA18) reglas: lista propia/admin, firma pública solo firma+estado, folios +1:', ba18);

  // BB: serie nueva 2.5.1 — 12 cambios + punto 13 (conformidad abajo a la derecha).
  var DESC_CAMBIOS_DEF = 'se realiza mantenimiento preventivo en hardware y software, sopleteo y limpieza general, instalación de actualización, revisión de políticas y antivirus, desinstalación de software no permitido';
  function pdfTextRows(pdfStr) {
    var out = [], re = /BT \/(F\d) (\d+) Tf ([\d.]+) ([\d.]+) Td \(((?:\\.|[^()\\])*)\) Tj ET/g, mm;
    while ((mm = re.exec(pdfStr))) out.push({ f: mm[1], s: Number(mm[2]), x: Number(mm[3]), y: Number(mm[4]), t: mm[5] });
    return out;
  }
  async function pdfStrOf(m, imgs) {
    return Buffer.from(await buildPdfMant(m, imgs || {}).arrayBuffer()).toString('latin1');
  }
  // BB0: versión 2.5.2 en 2 sitios exactos, 0 de 2.5.0 y 0 diálogos nativos.
  var bb0nat = (html.match(/alert\(/g) || []).length === 0 && (html.match(/confirm\(/g) || []).length === 0 && (html.match(/prompt\(/g) || []).length === 0;
  console.log('BB0) 2.5.2 en 2 sitios:', n252 === 2, '| 0 de 2.5.0:', !html.includes('2.5.0'), '| 0 alert/confirm/prompt:', bb0nat);
  // BB1: empresa — default Lapi, se guarda, se ve en tarjeta/orden/PDF;
  // con Ludi el PDF NO lleva el bloque de contacto de Lapi.
  loginAs('u1', 'Test User', 'usuario');
  mantOpenForm(null, null);
  var bb1def = document.getElementById('fM-empresa').value === 'Lapi';
  document.getElementById('fM-empresa').value = 'Ludi';
  var mBB1 = mantReadForm();
  var bb1read = mBB1.empresa === 'Ludi';
  var mBB1ludi = mkMant({ empresa: 'Ludi', tituloCaso: 'Caso Ludi' });
  var bb1card = mantCardHtml(mBB1ludi).indexOf('Ludi') !== -1;
  mantenimientos = [mBB1ludi];
  mantShowOrder(mBB1ludi.id);
  var bb1ord = document.getElementById('mantOrderBody').innerHTML.indexOf('Empresa: Ludi') !== -1;
  var pdfLudi = await pdfStrOf(mBB1ludi);
  var bb1pdfLudi = pdfLudi.indexOf('Ludi') !== -1 && pdfLudi.indexOf('Rosa Blanca 63') === -1 && pdfLudi.indexOf('sistemas@lapi.com.mx') === -1 && pdfLudi.indexOf('Lapi Sistemas') === -1;
  var pdfLapi = await pdfStrOf(mkMant({}));
  var bb1pdfLapi = pdfLapi.indexOf('Lapi Sistemas') !== -1 && pdfLapi.indexOf('Rosa Blanca 63') !== -1 && pdfLapi.indexOf('sistemas@lapi.com.mx') !== -1 && pdfLapi.indexOf('Empresa: Lapi') !== -1;
  console.log('BB1) empresa default Lapi:', bb1def, '| se lee Ludi:', bb1read, '| tarjeta muestra Ludi:', bb1card, '| vista de orden muestra Ludi:', bb1ord, '| PDF Ludi sin contacto Lapi:', bb1pdfLudi, '| PDF Lapi con contacto:', bb1pdfLapi);
  // BB2: tipo — ambos checkboxes marcados al abrir (nuevo y detectado);
  // quitar uno deja solo el otro; quitar los dos bloquea la creación.
  mantOpenForm(null, null);
  var bb2def = document.getElementById('fM-tipo-sw').checked === true && document.getElementById('fM-tipo-hw').checked === true;
  document.getElementById('fM-tipo-hw').checked = false;
  var bb2sw = mantReadForm().tipo === 'SOFTWARE';
  document.getElementById('fM-tipo-sw').checked = false;
  var bb2none = mantReadForm().tipo === '' && mantFaltaCrear(Object.assign(mantReadForm(), { equipo: { serie: 'S', hostname: 'H', modelo: 'M' }, area: 'A', responsable: 'R', tituloCaso: 'T', tipoFalla: 'F', descripcionEquipo: 'D', fechaServicio: '2026-11-16', whatsappUsuario: '5512345678', firmaTecnico: 'data:image/png;base64,xx' })) === 'el tipo de mantenimiento';
  var mBB2old = mkMant({ tipo: 'HARDWARE' });
  mantOpenForm(mBB2old, null);
  var bb2old = document.getElementById('fM-tipo-sw').checked === false && document.getElementById('fM-tipo-hw').checked === true;
  console.log('BB2) ambos marcados al abrir:', bb2def, '| solo SOFTWARE al quitar HARDWARE:', bb2sw, '| ninguno bloquea crear:', bb2none, '| orden vieja HARDWARE marca solo ese:', bb2old);
  // BB3: diagonales — tiempos, tipo de falla y fechas plan/compromiso/
  // periodo se prellenan con '/' solo si están vacíos; lo guardado se respeta.
  mantOpenForm(null, null);
  var bb3def = ['fM-tRep', 'fM-tViaje', 'fM-tCaido', 'fM-tipoFalla', 'fM-fechaPlan', 'fM-fechaComp', 'fM-periodoPrueba'].every(function (id) { return document.getElementById(id).value === '/'; });
  var mBB3 = mkMant({ tiempoReparacion: '3 horas', tiempoViaje: '', tiempoSistemaCaido: '', tipoFalla: 'Disco', fechaPlaneacion: '2026-11-10', fechaCompromiso: '', periodoPrueba: '7 días' });
  mantOpenForm(mBB3, null);
  var bb3keep = document.getElementById('fM-tRep').value === '3 horas' && document.getElementById('fM-tipoFalla').value === 'Disco' && document.getElementById('fM-fechaPlan').value === '2026-11-10' && document.getElementById('fM-periodoPrueba').value === '7 días' && document.getElementById('fM-tViaje').value === '/' && document.getElementById('fM-tCaido').value === '/' && document.getElementById('fM-fechaComp').value === '/';
  console.log('BB3) diagonales por default:', bb3def, '| valores guardados se respetan:', bb3keep);
  // BB4: título compuesto con año — default, año actual, deducción en viejas.
  mantOpenForm(null, null);
  var bb4def = document.getElementById('fM-titulo').value === 'Mantenimiento Preventivo sistemas' && String(document.getElementById('fM-anio').value) === '2026';
  document.getElementById('fM-serie').value = 'S-BB4'; document.getElementById('fM-hostname').value = 'PC-BB4'; document.getElementById('fM-modelo').value = 'Modelo BB4';
  document.getElementById('fM-area').value = 'Sistemas'; document.getElementById('fM-responsable').value = 'Ana';
  document.getElementById('fM-tipoFalla').value = 'Preventivo'; document.getElementById('fM-fechaServ').value = '2026-11-16'; document.getElementById('fM-whatsapp').value = '5512345678';
  mantFirmaData = 'data:image/png;base64,iVBORw0KGgo=';
  var mBB4 = mantReadForm();
  var bb4comp = mBB4.tituloCaso === 'Mantenimiento Preventivo sistemas 2026' && mBB4.anio === 2026;
  var mBB4old = mkMant({ tituloCaso: 'Caso viejo' });
  mantOpenForm(mBB4old, null);
  var bb4old = String(document.getElementById('fM-anio').value) === '2026' && document.getElementById('fM-titulo').value === 'Caso viejo' && mantReadForm().tituloCaso === 'Caso viejo 2026';
  var mBB4y = mkMant({ tituloCaso: 'Mantenimiento Preventivo sistemas 2024', anio: undefined });
  mantOpenForm(mBB4y, null);
  var bb4y = String(document.getElementById('fM-anio').value) === '2024' && mantReadForm().tituloCaso === 'Mantenimiento Preventivo sistemas 2024';
  console.log('BB4) título y año por default:', bb4def, '| guardado compuesto 2026:', bb4comp, '| vieja sin año deduce 2026:', bb4old, '| título con 2024 deduce 2024:', bb4y);
  // BB5: descripción del equipo = hostname (al abrir y al teclear).
  mantOpenForm(mantFromDetectado(detBA3), detBA3.id);
  var bb5det = document.getElementById('fM-descEquipo').value === 'PC-BA3';
  mantOpenForm(null, null);
  document.getElementById('fM-descEquipo').value = '';
  document.getElementById('fM-hostname').value = 'PC-NUEVO';
  document.getElementById('fM-hostname')._h.input[0]();
  var bb5type = document.getElementById('fM-descEquipo').value === 'PC-NUEVO';
  document.getElementById('fM-descEquipo').value = 'Descripción manual';
  document.getElementById('fM-hostname').value = 'PC-OTRO';
  document.getElementById('fM-hostname')._h.input[0]();
  var bb5manual = document.getElementById('fM-descEquipo').value === 'Descripción manual';
  console.log('BB5) detectado llena descripción con hostname:', bb5det, '| teclear hostname la copia si está vacía:', bb5type, '| escrita a mano se respeta:', bb5manual);
  // BB6: descripción de cambios por default (texto exacto), editable.
  mantOpenForm(null, null);
  var bb6def = document.getElementById('fM-descCambios').value === DESC_CAMBIOS_DEF;
  var mBB6 = mkMant({ descripcionCambios: 'Cambios míos' });
  mantOpenForm(mBB6, null);
  var bb6keep = document.getElementById('fM-descCambios').value === 'Cambios míos';
  console.log('BB6) cambios por default exacto:', bb6def, '| guardado se respeta:', bb6keep);
  // BB7: PDF — bloques Planeación/Compromiso/Periodo con '/', Liberación
  // con fecha elegida y ambas firmas.
  var mBB7 = mkMant({ id: 'bb7', folio: '00007', estado: 'creada', fechaPlaneacion: '/', fechaCompromiso: '/', periodoPrueba: '/', fechaLiberacion: '2026-11-20', firmaTecnico: 'data:image/png;base64,iVBORw0KGgo=' });
  mBB7.firma = { nombre: 'Ana López', area: 'Ventas', comentarios: '', satisfaccion: 9, firma: 'data:image/png;base64,iVBORw0KGgo=', firmadoEn: Date.now() };
  var pdfBB7 = await pdfStrOf(mBB7);
  var bb7slash = (pdfBB7.match(/Fecha: \//g) || []).length >= 3 && pdfBB7.indexOf('Firma Sistemas: /') !== -1 && pdfBB7.indexOf('Firma Área solicitante: /') !== -1;
  var bb7lib = pdfBB7.indexOf('Fecha: 2026-11-20') !== -1 && pdfBB7.indexOf('Liberación:') !== -1 && pdfBB7.indexOf('Área solicitante') !== -1 && pdfBB7.indexOf('Firma: Test User \\(guardada en la app\\)') !== -1 && pdfBB7.indexOf('Firma: Ana López \\(guardada en la app\\)') !== -1;
  console.log('BB7) bloques con diagonales:', bb7slash, '| Liberación con fecha y ambas firmas:', bb7lib);
  // BB8: admin elimina órdenes (tarjeta y vista); el usuario no ve el botón.
  var delCloudBB8 = [];
  global.Cloud.deleteMant = async function (id) { delCloudBB8.push(id); };
  var mBB8 = mkMant({ id: 'bb8', folio: '00008', estado: 'creada', tituloCaso: 'Para borrar' });
  cloudRole = 'usuario';
  var bb8nouser = mantCardHtml(mBB8).indexOf('data-mant-del-order') === -1;
  cloudRole = 'admin';
  var bb8admin = mantCardHtml(mBB8).indexOf('data-mant-del-order="bb8"') !== -1;
  mantenimientos = [mBB8];
  mantShowOrder('bb8');
  var bb8view = document.getElementById('btnMantEliminarOrden').hidden === false;
  loginAs('u1', 'Test User', 'usuario');
  mantenimientos = [mBB8];
  mantShowOrder('bb8');
  var bb8viewUser = document.getElementById('btnMantEliminarOrden').hidden === true;
  loginAs('uGer', 'Gerardo', 'admin');
  mantenimientos = [mBB8];
  var btnBB8 = {
    getAttribute: function (a) { return a === 'data-mant-del-order' ? 'bb8' : null; },
    hasAttribute: function (a) { return a === 'data-mant-del-order'; },
    closest: function (sel) { return sel === '[data-mant-del-order]' ? btnBB8 : null; },
    classList: { contains: function () { return false; } }
  };
  document.getElementById('mantList')._h.click[0]({ target: btnBB8 });
  var bb8modal = document.getElementById('confirmModal').hidden === false && document.getElementById('confirmMsg').textContent.indexOf('no se puede deshacer') !== -1;
  answerConfirm(false);
  await sleep(20);
  var bb8no = mantenimientos.length === 1;
  document.getElementById('mantList')._h.click[0]({ target: btnBB8 });
  answerConfirm(true);
  await sleep(20);
  var bb8si = mantenimientos.length === 0 && delCloudBB8.indexOf('bb8') !== -1 && toastTxt().indexOf('eliminada') !== -1;
  console.log('BB8) usuario sin botón en tarjeta:', bb8nouser, '| admin con botón:', bb8admin, '| vista admin muestra Eliminar:', bb8view, '| vista usuario lo oculta:', bb8viewUser, '| pide confirmar:', bb8modal, '| con No no borra:', bb8no, '| con Sí borra local+nube:', bb8si);
  // BB9: firma.html — botón Cerrar, window.close a los 800 ms, aviso y empresa.
  var firmaHtml = fs.readFileSync('/home/hatch/workspace/android/checklist-cloud/hosting/public/firma.html', 'utf8');
  var bb9btn = firmaHtml.includes('id="btnCerrarSigned"') && firmaHtml.includes('id="btnCerrarDone"') && firmaHtml.includes('>Cerrar</button>');
  var bb9close = firmaHtml.includes('window.close()') && firmaHtml.includes('}, 800);') && firmaHtml.includes('Ya puedes cerrar esta ventana');
  var bb9emp = firmaHtml.includes("['Empresa', o.empresa || 'Lapi']");
  console.log('BB9) firma.html botón Cerrar en ambas vistas:', bb9btn, '| close + 800 ms + aviso:', bb9close, '| muestra la empresa:', bb9emp);
  // BB10: PDF válido con ambas firmas (bytes > 0 y folio) y compartir
  // habilitado; sin ambas, PDF bloqueado con toast y botón deshabilitado.
  var mBB10 = mkMant({ id: 'bb10', folio: '00010', estado: 'creada', firmaTecnico: 'data:image/png;base64,iVBORw0KGgo=' });
  mBB10.firma = { nombre: 'Ana López', area: 'Ventas', comentarios: '', satisfaccion: 8, firma: 'data:image/png;base64,iVBORw0KGgo=', firmadoEn: Date.now() };
  var blobBB10 = buildPdfMant(mBB10, {});
  var bufBB10 = Buffer.from(await blobBB10.arrayBuffer());
  var bb10pdf = bufBB10.length > 0 && bufBB10.toString('latin1').indexOf('%PDF') === 0 && bufBB10.toString('latin1').indexOf('Folio: 00010') !== -1;
  mantenimientos = [mBB10];
  mantShowOrder('bb10');
  var bb10en = document.getElementById('btnMantCompartir').disabled === false;
  var mBB10b = mkMant({ id: 'bb10b', folio: '00011', estado: 'creada', firmaTecnico: '' });
  mantenimientos = [mBB10b];
  mantShowOrder('bb10b');
  var bb10dis = document.getElementById('btnMantCompartir').disabled === true && document.getElementById('mantOrderNote').textContent.indexOf('firma del técnico') !== -1;
  await sharePdfMant(mBB10b);
  var bb10toast = toastTxt().indexOf('firma del técnico') !== -1;
  console.log('BB10) PDF válido con folio:', bb10pdf, '| compartir habilitado con ambas:', bb10en, '| sin firma: botón deshabilitado y nota:', bb10dis, '| intento avisa con toast:', bb10toast);
  // BB11: compartir sin Capacitor no miente: descarga el PDF y lo avisa.
  global.Capacitor = undefined;
  global.FileReader = global.FileReader || class { constructor() { this.result = null; } readAsDataURL(blob) { var self = this; blob.arrayBuffer().then(function (ab) { self.result = 'data:application/pdf;base64,' + Buffer.from(ab).toString('base64'); if (self.onload) self.onload(); }); } };
  await shareMantCopy(mBB10);
  var bb11 = toastTxt().indexOf('PDF descargado: orden-servicio-00010.pdf') !== -1;
  console.log('BB11) sin Capacitor: descarga el PDF y avisa (no dice que compartió):', bb11);
  // BB12: punto 13 — la conformidad es el cierre final, abajo a la derecha.
  var JPEG1X1_BB = '/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAP//////////////////////////////////////////////////////////////////////////////////////2wBDAf//////////////////////////////////////////////////////////////////////////////////////wAARCAABAAEDASIAAhEBAxEB/8QAFAABAAAAAAAAAAAAAAAAAAAACf/EABQQAQAAAAAAAAAAAAAAAAAAAAD/xAAUAQEAAAAAAAAAAAAAAAAAAAAA/8QAFBEBAAAAAAAAAAAAAAAAAAAAAP/aAAwDAQACEQMRAD8AvwH/2Q==';
  var jpgBB = new Uint8Array(Buffer.from(JPEG1X1_BB, 'base64'));
  var pdfBB12 = await pdfStrOf(mBB10, { tecnico: { bytes: jpgBB, w: 1, h: 1 }, usuario: { bytes: jpgBB, w: 1, h: 1 } });
  var rowsBB12 = pdfTextRows(pdfBB12);
  var confBB12 = rowsBB12.find(function (r) { return r.t.indexOf('Conformidad del usuario') === 0; });
  var nomBB12 = rowsBB12.find(function (r) { return r.t.indexOf('Nombre: Ana L') === 0; });
  var fecBB12 = rowsBB12.find(function (r) { return r.t.indexOf('Fecha: ') === 0 && r.x > 297; });
  var horBB12 = rowsBB12.find(function (r) { return r.t.indexOf('Hora: ') === 0 && r.x > 297; });
  var firBB12 = rowsBB12.find(function (r) { return r.t.indexOf('Firma de conformidad:') === 0; });
  var expX = confBB12 ? 595 - 48 - pdfTextWidth(confBB12.t, 'F2', 12) : -1;
  var bb12x = !!confBB12 && Math.abs(confBB12.x - expX) < 1.5 && Math.abs((confBB12.x + pdfTextWidth(confBB12.t, 'F2', 12)) - 547) < 1.5;
  var bb12order = pdfBB12.indexOf('Conformidad del usuario') > pdfBB12.indexOf('Generado el') && pdfBB12.indexOf('Conformidad del usuario') > pdfBB12.indexOf('Liberación') && pdfBB12.lastIndexOf('/Imusuario Do') > pdfBB12.indexOf('Conformidad del usuario');
  var bb12rows = !!nomBB12 && nomBB12.x > 297 && !!fecBB12 && !!horBB12 && !!firBB12 && firBB12.x > 297;
  var pdfBB12b = await pdfStrOf(mkMant({ id: 'bb12b', folio: '00012', estado: 'creada', firmaTecnico: 'data:image/png;base64,iVBORw0KGgo=' }));
  var rowsBB12b = pdfTextRows(pdfBB12b);
  var pendBB12 = rowsBB12b.find(function (r) { return r.t === 'Pendiente de firma.'; });
  var bb12pend = !!pendBB12 && pendBB12.x > 297;
  console.log('BB12) conformidad a la derecha (x=' + (confBB12 ? confBB12.x : '—') + ' esperado ' + expX.toFixed(1) + ', borde derecho 547):', bb12x, '| es el cierre final tras Liberación y Generado:', bb12order, '| nombre/fecha/hora/firma a la derecha:', bb12rows, '| sin firma del usuario: pendiente a la derecha:', bb12pend);

  // 252: serie nueva 2.5.2 — #btnMantDetectar en Mantenimientos.
  function det252(over) { return Object.assign({ id: 'SERIE-M1', hostname: 'PC-MANT-1', marca: 'HP', modelo: 'EliteDesk 800', serie: 'SERIE-M1', cpu: 'Intel i5', ramGB: 8, discoGB: 256, so: 'Windows 11', tipo: 'Desktop', detectadoEn: Date.now() - 60000, detectadoPor: 'Test User', usado: false }, over || {}); }
  // 252A: el botón existe en el HTML y se oculta sin Desktop (patrón AN3).
  var btnMantDet252 = document.getElementById('btnMantDetectar');
  var btnDet252 = document.getElementById('btnDetectar');
  var htmlMantBtn252 = html.includes('id="btnMantDetectar" hidden') && html.includes('Detectar equipo') && html.includes('solo en escritorio');
  machineId = null; detectingNow = false; detectados = [];
  global.Desktop = undefined;
  refreshDetectarBtn();
  var hidNoDesk252 = btnMantDet252.hidden === true && btnDet252.hidden === true;
  global.Desktop = { getMachineId: async function () { return 'M1-MACHINE'; }, detect: async function () { return {}; } };
  refreshDetectarBtn();
  var shownDesk252 = btnMantDet252.hidden === false && btnDet252.hidden === false;
  console.log('252A) botón en HTML (id + oculto + texto + small):', htmlMantBtn252, '| sin Desktop ambos ocultos:', hidNoDesk252, '| con Desktop ambos visibles:', shownDesk252);
  // 252B: refreshDetectarBtn() pone a AMBOS botones el mismo estado.
  loginAs('u1', 'Test User', 'usuario');
  CLOUD_ENABLED = true;
  global.Desktop = { getMachineId: async function () { return 'MANT-1'; }, detect: async function () { return {}; } };
  await loadMachineId();
  var mid252 = machineId === 'MANT-1';
  detectados = [det252({ id: 'MANT-1', serie: 'MANT-1' })];
  renderDetectados();
  var blocked252 = btnDet252.disabled === true && btnDet252.innerHTML.indexOf('Equipo detectado') !== -1 && btnMantDet252.disabled === true && btnMantDet252.innerHTML.indexOf('Equipo detectado') !== -1;
  detectados = [];
  renderDetectados();
  var freed252 = btnDet252.disabled === false && btnDet252.innerHTML.indexOf('Detectar este equipo') !== -1 && btnMantDet252.disabled === false && btnMantDet252.innerHTML.indexOf('Detectar equipo') !== -1 && btnMantDet252.innerHTML.indexOf('Detectar este equipo') === -1;
  var rep252b = [];
  global.Cloud.reportDetected = async function (info) { rep252b.push(info); return {}; };
  var resolve252 = null;
  global.Desktop = { getMachineId: async function () { return 'MANT-1'; }, detect: function () { return new Promise(function (res) { resolve252 = res; }); } };
  machineId = null; detectados = [];
  btnDet252.innerHTML = 'Detectar este equipo';
  btnMantDet252.innerHTML = 'Detectar equipo';
  document.getElementById('btnDetectar')._h.click[0]();
  var prog252 = btnDet252.disabled === true && btnDet252.innerHTML.indexOf('Detectando software...') !== -1 && btnMantDet252.disabled === true && btnMantDet252.innerHTML.indexOf('Detectando software...') !== -1;
  resolve252({ hostname: 'PC-PROG252', marca: 'Lenovo', modelo: 'ThinkCentre', serie: 'SPROG252', cpu: 'i5', ramGB: 8, discoGB: 256, so: 'Windows 11', tipo: 'Desktop', detectadoEn: Date.now() });
  await sleep(20);
  var rest252 = btnDet252.disabled === false && btnDet252.innerHTML === 'Detectar este equipo' && btnMantDet252.disabled === false && btnMantDet252.innerHTML.indexOf('Detectar equipo') !== -1 && btnMantDet252.innerHTML.indexOf('Detectar este equipo') === -1;
  console.log('252B) machineId cargado:', mid252, '| pendiente bloquea AMBOS con Equipo detectado:', blocked252, '| al liberar cada uno recupera su etiqueta:', freed252, '| detectando AMBOS en progreso:', prog252, '| al terminar cada uno restaura su etiqueta:', rest252);
  // 252C: pulsar #btnMantDetectar detecta, reporta con el técnico y abre el panel.
  loginAs('u1', 'Test User', 'usuario');
  showVista('mant');
  machineId = null; machineIdTried = false; machineIdDesktop = null; detectingNow = false; detectados = [];
  var reported252 = [];
  global.Desktop = { getMachineId: async function () { return 'M1-MACHINE'; }, detect: async function () { return { hostname: 'PC-MANT-1', marca: 'HP', modelo: 'EliteDesk 800', serie: 'SERIE-M1', cpu: 'Intel i5', ramGB: 8, discoGB: 256, so: 'Windows 11', tipo: 'Desktop', detectadoEn: Date.now() }; } };
  global.Cloud.reportDetected = async function (d) { reported252.push(d); detectados.push(Object.assign({}, d, { id: d.serie || 'X', usado: false })); };
  document.getElementById('mantDetBox').hidden = true;
  document.getElementById('btnMantDetectar')._h.click[0]();
  await sleep(30);
  var rep252c = reported252.length === 1 && reported252[0].hostname === 'PC-MANT-1' && reported252[0].detectadoPor === 'Test User';
  var open252c = document.getElementById('mantDetBox').hidden === false && document.getElementById('mantDetList').innerHTML.indexOf('PC-MANT-1') !== -1;
  var detCb252 = null;
  global.Cloud.getUserDoc = async function () { return { activo: true, rol: 'usuario', nombre: 'Test User', email: 'test@checklist.local' }; };
  global.Cloud.isInitialized = async function () { return true; };
  global.Cloud.getAllRenta = async function () { return []; };
  global.Cloud.upsertRenta = async function () {};
  global.Cloud.getAllPreparations = async function () { return []; };
  global.Cloud.upsertPrep = async function () {};
  global.Cloud.subscribeRenta = function () { return function () {}; };
  global.Cloud.subscribePreparations = function () { return function () {}; };
  global.Cloud.subscribeDetectados = function (cb) { detCb252 = cb; return function () {}; };
  global.Cloud.subscribeMantenimientos = function () { return function () {}; };
  global.Cloud.subscribePresence = function () { return function () {}; };
  global.Cloud.subscribeChat = function () { return function () {}; };
  global.Cloud.subscribeDm = function () { return function () {}; };
  global.Cloud.heartbeat = function () {};
  global.Cloud.pruneChat = function () {};
  global.Cloud.clearPresence = function () {};
  global.Cloud.listUsers = async function () { return []; };
  localStorage.setItem('checklist-soporte-migrado-v2:u1', '1');
  localStorage.setItem('checklist-soporte-migrado-preps-v1:u1', '1');
  localStorage.setItem('checklist-soporte-migrado-mant-v1:u1', '1');
  state.preparations = [];
  state.renta = [];
  await onAuthChanged({ uid: 'u1', email: 'test@checklist.local' });
  await sleep(20);
  var sub252 = typeof detCb252 === 'function';
  var stillOpen252 = document.getElementById('mantDetBox').hidden === false;
  detCb252(detectados.concat([det252({ id: 'SERIE-M2', hostname: 'PC-MANT-2', modelo: 'OptiPlex', serie: 'SERIE-M2', detectadoPor: 'Alejandro' })]));
  var rerender252 = document.getElementById('mantDetList').innerHTML.indexOf('PC-MANT-2') !== -1 && document.getElementById('mantDetList').innerHTML.indexOf('PC-MANT-1') !== -1;
  document.getElementById('mantDetBox').hidden = true;
  detCb252([det252({ id: 'SERIE-M3', hostname: 'PC-MANT-3', modelo: 'ThinkCentre', serie: 'SERIE-M3', detectadoPor: 'Gerardo' })]);
  var noRerender252 = document.getElementById('mantDetList').innerHTML.indexOf('PC-MANT-3') === -1 && document.getElementById('mantDetList').innerHTML.indexOf('PC-MANT-2') !== -1;
  console.log('252C) Detectar desde mant reporta con el técnico:', rep252c, '| abre el panel y lista el equipo:', open252c, '| suscripción capturada:', sub252, '| panel sigue abierto tras entrar:', stillOpen252, '| la suscripción re-renderiza el panel abierto:', rerender252, '| con el panel cerrado no re-renderiza:', noRerender252);
  // 252D: el panel ofrece dar mantenimiento al detectado y prellena el formulario (patrón BA4).
  detectados = [det252()];
  renderMantDetectados();
  var mantList252 = document.getElementById('mantDetList').innerHTML;
  var hasBtn252d = mantList252.indexOf('🔧 Dar mantenimiento a este equipo') !== -1 && mantList252.indexOf('data-mant-det-use="SERIE-M1"') !== -1;
  document.getElementById('mantDetList')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-mant-det-use]' ? { getAttribute: function () { return 'SERIE-M1'; } } : null; } } });
  var form252d = document.getElementById('mantFormBox').hidden === false && document.getElementById('fM-serie').value === 'SERIE-M1' && document.getElementById('fM-hostname').value === 'PC-MANT-1' && document.getElementById('fM-modelo').value === 'EliteDesk 800';
  console.log('252D) panel muestra Dar mantenimiento con data-mant-det-use:', hasBtn252d, '| al pulsar abre el formulario prellenado (serie/host/modelo):', form252d);
  // 252E: #btnMantDet sigue alternando el panel y renderiza al abrir.
  document.getElementById('mantDetBox').hidden = true;
  detectados = [det252()];
  document.getElementById('btnMantDet')._h.click[0]();
  var open252e = document.getElementById('mantDetBox').hidden === false && document.getElementById('mantDetList').innerHTML.indexOf('PC-MANT-1') !== -1;
  document.getElementById('btnMantDet')._h.click[0]();
  var closed252e = document.getElementById('mantDetBox').hidden === true;
  document.getElementById('btnMantDet')._h.click[0]();
  var reopen252e = document.getElementById('mantDetBox').hidden === false && document.getElementById('mantDetList').innerHTML.indexOf('PC-MANT-1') !== -1;
  console.log('252E) primer clic abre y renderiza:', open252e, '| segundo clic cierra:', closed252e, '| tercer clic reabre y renderiza:', reopen252e);
  // 252F: detectar desde Por preparar sigue igual y NO abre el panel de mant.
  loginAs('u1', 'Test User', 'usuario');
  machineId = null; detectingNow = false; detectados = [];
  var reported252f = [];
  global.Desktop = { getMachineId: async function () { return 'M1-MACHINE'; }, detect: async function () { return { hostname: 'PC-PREP-1', marca: 'Dell', modelo: 'OptiPlex', serie: 'SERIE-F1', cpu: 'i5', ramGB: 8, discoGB: 256, so: 'Windows 11', tipo: 'Desktop', detectadoEn: Date.now() }; } };
  global.Cloud.reportDetected = async function (d) { reported252f.push(d); return {}; };
  document.getElementById('mantDetBox').hidden = true;
  refreshDetectarBtn();
  document.getElementById('btnDetectar')._h.click[0]();
  await sleep(30);
  var rep252f = reported252f.length === 1 && reported252f[0].hostname === 'PC-PREP-1' && toastTxt() === 'Equipo detectado, ya aparece en los teléfonos';
  var noMant252f = document.getElementById('mantDetBox').hidden === true;
  global.Desktop = undefined;
  console.log('252F) Detectar desde Por preparar reporta y avisa:', rep252f, '| el panel de mant sigue cerrado:', noMant252f);

  process.exit(0);
})();
