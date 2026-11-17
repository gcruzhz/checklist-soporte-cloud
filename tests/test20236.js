// Harness de pruebas node para Checklist de Soporte (nube).
// Archivo auto-contenido: el harness es todo lo que hay antes de la línea
// `eval(SRC);` (marcada con >>> EVAL). Para la siguiente versión, copiar
// este archivo y cambiar checklist20231.js por el nuevo extraído.
// Para probar la migración, sembrar localStorage ANTES de la línea eval.
const fs = require('fs');
const SRC = fs.readFileSync(__dirname + '/checklist20236.js', 'utf8');

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
global.alert = (m) => { global.lastAlert = m; };
global.confirm = () => true;
global.prompt = () => null;
global.Blob = global.Blob || class Blob { constructor(parts) { this.parts = parts; } };
global.URL = global.URL || {};
if (!global.URL.createObjectURL) global.URL.createObjectURL = () => 'blob:x';
if (!global.URL.revokeObjectURL) global.URL.revokeObjectURL = () => {};

const sleep = (ms) => new Promise(r => setTimeout(r, ms));
function mkPrep(over) {
  return Object.assign({ id: 'p1', createdAt: Date.now(), deliveredAt: null, readyAt: null, checks: {}, extraItems: [], reasignaciones: [],
    equipo: { tipo: 'Laptop', marca: 'Dell', modelo: 'Inspiron 3501', serie: 'S1', inventario: '100' },
    usuario: { nombre: 'Ana', area: 'Sistemas', correo: '' }, tecnico: 'Juan Pérez' }, over || {});
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

(async () => {
  await sleep(50);
  const html = fs.readFileSync('/home/hatch/workspace/android/checklist-cloud/www/index.html', 'utf8');
  const dt = defaultTemplate();
  console.log('AM0) versión 2.3.6:', html.includes('Versión 2.3.6'), '| sin 2.3.5:', !html.includes('Versión 2.3.5'), '| sin Cuenta de red creada:', !dt.some(t => t.text.includes('Cuenta de red')), '| t26 Limpieza solo reasignación:', !!dt.find(t => t.id === 't26' && t.reassignOnly && t.text === 'Limpieza física del equipo'));
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
  // AA6: eliminar borra el equipo en la nube.
  fakeClick('data-del-prep', 'p1');
  console.log('AA6) eliminar borra en la nube:', deletedPrep.indexOf('p1') !== -1 && !state.preparations.some(function (p) { return p.id === 'p1'; }));
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
  console.log('AC3) borrar en el chat del equipo borra el mensaje:', delChat.length === 1 && delChat[0] === 'm1');
  // AC4: tocar borrar en el chat individual borra ese mensaje.
  var delDm = [];
  global.Cloud.deleteDmMessage = async function (id) { delDm.push(id); };
  document.getElementById('dmChatBox')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-del-dm]' ? { getAttribute: function () { return 'd1'; } } : null; } } });
  console.log('AC4) borrar en el chat individual borra el mensaje:', delDm.length === 1 && delDm[0] === 'd1');

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
  // AN2: 'Descartar' pide confirmación y borra; si se cancela, no borra.
  deletedDet.length = 0;
  document.getElementById('detList')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-det-del]' ? { getAttribute: function () { return 'SERIE123'; } } : null; } } });
  var discOk = deletedDet.indexOf('SERIE123') !== -1;
  deletedDet.length = 0;
  global.confirm = function () { return false; };
  document.getElementById('detList')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-det-del]' ? { getAttribute: function () { return 'SERIE123'; } } : null; } } });
  global.confirm = function () { return true; };
  console.log('AN2) Descartar borra con confirmación:', discOk, '| sin confirmación no borra:', deletedDet.length === 0);
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
  var detAlertOk = global.lastAlert === 'Equipo detectado, ya aparece en los teléfonos';
  global.Desktop = { detect: async function () { throw new Error('sin red'); } };
  document.getElementById('btnDetectar')._h.click[0]();
  await sleep(20);
  var detFailOk = (global.lastAlert || '').indexOf('No se pudo detectar el equipo') === 0;
  cloudUser = null;
  global.Desktop = { detect: async function () { return {}; } };
  document.getElementById('btnDetectar')._h.click[0]();
  await sleep(20);
  var detNoSessionOk = (global.lastAlert || '').indexOf('Inicia sesión') === 0 && reported.length === 1;
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
  var progReportOk = repDet.length === 1 && repDet[0].hostname === 'PC-PROG' && global.lastAlert === 'Equipo detectado, ya aparece en los teléfonos';
  global.Desktop = { detect: async function () { throw new Error('sin red'); } };
  btnDetEl.innerHTML = 'Detectar este equipo';
  document.getElementById('btnDetectar')._h.click[0]();
  await sleep(20);
  var failRestoredOk = btnDetEl.disabled === false && btnDetEl.innerHTML === 'Detectar este equipo' && (global.lastAlert || '').indexOf('No se pudo detectar el equipo') === 0;
  global.Desktop = undefined;
  console.log('AO7) Detectar muestra progreso y deshabilita:', progOk, '| al terminar restaura el botón:', restoredOk, '| y reporta el equipo:', progReportOk, '| si falla también restaura y avisa:', failRestoredOk);


  // AP0: estáticos 2.3.5 (versión, 17 detectables, nunca-marcar, defaults viejos).
  var all17 = filterDetectedChecks({ t3: true, t4: true, t6: true, t7: true, t8: 'Office 365', t9: true, t10: true, t11: true, t12: true, t18: true, t19: true, t20: true, t21: true, t22: true, t23: true, t24: true, t25: true });
  var oldBack = prepFromCloud(prepToCloudDoc(mkPrep()));
  console.log('AP0) estáticos 2.3.6: versión:', html.includes('Versión 2.3.6') && !html.includes('Versión 2.3.5'), '| 17 detectables con t12:', all17.ids.length === 17, '| nombre corto Invgate:', detShortName('t12') === 'Invgate', '| nunca-marcar solo t1/t2/t13-t17/t26:', filterDetectedChecks({ t1: true, t2: true, t13: true, t14: true, t15: true, t16: true, t17: true, t26: true }).ids.length === 0, '| equipos viejos con defaults vacíos:', oldBack.equipo.cpu === '' && oldBack.equipo.ramGB === '' && oldBack.equipo.discoGB === '' && oldBack.equipo.discoTipo === '' && oldBack.equipo.ip === '' && oldBack.equipo.ipTipo === '' && oldBack.equipo.anydeskId === '' && oldBack.equipo.anydeskAlias === '' && oldBack.versiones.so === '' && oldBack.versiones.antivirus === '' && oldBack.versiones.chrome === '');
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
  var n236 = (html.match(/2\.3\.6/g) || []).length;
  console.log('AR0) versión 2.3.6 visible:', html.includes('Versión 2.3.6') && html.includes('Versión: 2.3.6'), '| 0 de 2.3.5:', !html.includes('2.3.5'), '| ocurrencias 2.3.6:', n236 === 13);
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
  process.exit(0);
})();
