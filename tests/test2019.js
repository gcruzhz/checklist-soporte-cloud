// Harness de pruebas node para Checklist de Soporte (nube).
// Archivo auto-contenido: el harness es todo lo que hay antes de la línea
// `eval(SRC);` (marcada con >>> EVAL). Para la siguiente versión, copiar
// este archivo y cambiar checklist2019.js por el nuevo extraído.
// Para probar la migración, sembrar localStorage ANTES de la línea eval.
const fs = require('fs');
const SRC = fs.readFileSync(__dirname + '/checklist2019.js', 'utf8');

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
  console.log('Y0) versión 2.0.19:', html.includes('Versión 2.0.19'), '| sin 2.0.18:', !html.includes('2.0.15'), '| sin Cuenta de red creada:', !dt.some(t => t.text.includes('Cuenta de red')), '| t26 Limpieza solo reasignación:', !!dt.find(t => t.id === 't26' && t.reassignOnly && t.text === 'Limpieza física del equipo'));
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
  global.Cloud.clearPresence = function () { unsubs.push('clear'); };
  global.Cloud.listUsers = async function () { return teamUsers; };
  cloudUser = { uid: 'uGer', email: 'gerardo@checklist.local', nombre: 'Gerardo' };
  cloudRole = 'admin';
  startEquipo();
  const started = hb.length === 1 && hb[0][0] === 'Gerardo' && heartbeatTimer !== null && unsubs.includes('presence') && unsubs.includes('chat');
  stopEquipo();
  console.log('Y6) start: latido inmediato + suscripciones:', started, '| stop: desuscribe, limpia presencia y para el temporizador:', heartbeatTimer === null && unsubs.includes('unsub-presence') && unsubs.includes('unsub-chat') && unsubs.includes('clear'));
  // Y7: la vista Equipo se abre desde las pestañas.
  showVista('equipo');
  console.log('Y7) vista Equipo visible y Preparar oculta:', document.getElementById('viewEquipo').hidden === false && document.getElementById('viewPreparar').hidden === true);
  process.exit(0);
})();
