// Harness de pruebas node para Checklist de Soporte (nube).
// Archivo auto-contenido: el harness es todo lo que hay antes de la línea
// `eval(SRC);` (marcada con >>> EVAL). Para la siguiente versión, copiar
// este archivo y cambiar checklist20220.js por el nuevo extraído.
// Para probar la migración, sembrar localStorage ANTES de la línea eval.
const fs = require('fs');
const SRC = fs.readFileSync(__dirname + '/checklist20220.js', 'utf8');

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
  console.log('AF0) versión 2.2.0:', html.includes('Versión 2.2.0'), '| sin 2.1.3:', !html.includes('Versión 2.1.3'), '| sin Cuenta de red creada:', !dt.some(t => t.text.includes('Cuenta de red')), '| t26 Limpieza solo reasignación:', !!dt.find(t => t.id === 't26' && t.reassignOnly && t.text === 'Limpieza física del equipo'));
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
  // AA4: Listo / Entregado / Reabrir suben el equipo.
  upserted.length = 0;
  fakeClick('data-ready', 'p1');
  var listoOk = upserted.length === 1 && !!upserted[0].readyAt;
  upserted.length = 0;
  fakeClick('data-deliver', 'p1');
  var entrOk = upserted.length === 1 && !!upserted[0].deliveredAt;
  upserted.length = 0;
  fakeClick('data-reopen', 'p1');
  var reabOk = upserted.length === 1 && upserted[0].deliveredAt === null;
  console.log('AA4) Listo sube:', listoOk, '| Entregado sube:', entrOk, '| Reabrir sube:', reabOk);
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
  console.log('AF1) askAI llama a Gemini y devuelve el texto:', fetchCalls.length === 1 && fetchCalls[0][0] === 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent' && fetchCalls[0][1].headers['x-goog-api-key'] === 'CLAVE-PRUEBA' && JSON.parse(fetchCalls[0][1].body).contents[0].parts[0].text === '¿Qué falta?' && ans === 'Falta instalar Office y configurar la VPN.');
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
  process.exit(0);
})();
