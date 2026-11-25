# Parche web 2.5.16: Acuse Sistemas y Carta Responsiva FO-SI-10.
# 1) Dos botones en Inicio (grid, patrón Responsiva): "Acuse Sistemas"
# (dark) y "Carta Responsiva" (green); dos vistas nuevas viewAcuse y
# viewCarta (formulario + lista de guardados con PDF / WhatsApp /
# Correo / Eliminar + volver), sin tabs nuevas.
# 2) www/cloud/firebase.js: crearAcuse, subscribeAcuses, upsertAcuse,
# deleteAcuse, getAcuse, asignarFolioCarta (transacción en
# config/foliosCarta, folio de 5 dígitos, espejo de asignarFolio),
# crearCarta (asigna el folio al guardar), subscribeCartas, upsertCarta,
# deleteCarta, getCarta + exports en window.Cloud. Colecciones nuevas
# 'acuses' y 'cartas' (minúsculas, como 'responsivas').
# 3) firestore.rules: match /acuses/{id}, /cartas/{id} (list/get/create/
# update/delete solo activo y admin o creadoPor propio; create exige
# creadoPor == uid; get NO público, no hay página pública) y
# /config/foliosCarta (espejo de /config/folios). ATENCIÓN: las reglas
# NO se publican por CLI desde este sandbox (firebaserules.googleapis.com
# inalcanzable): hay que pegarlas en la consola de Firebase antes de que
# los acuses/cartas se puedan guardar (sin eso darán permiso denegado).
# 4) PDFs con el modelo de ops de buildPdfMant (pages, need, T, R, LN,
# wrapLines) y el guardado/compartido de sharePdfMant
# (guardarPdfCapacitor + share web + descarga): buildPdfAcuse (1 página
# carta: fecha larga "Septiembre 01, 2026" arriba, tabla PARA/DE/ANEXO,
# bloque RECIBE con Nombre/Fecha/Firma en blanco) y buildPdfCarta (2
# páginas carta: encabezado fijo FO-SI-10, Datos del solicitante, tabla
# Exclusivo de Sistemas, responsabilidades VERBATIM del docx, firma
# final). El folio de la Carta se asigna al GUARDAR y se muestra solo
# lectura en el formulario; el Acuse NO lleva folio. Modo local (sin
# nube): PDF igual y guardados en localStorage.
# 5) Versión 2.5.16 / versionCode 70 en www/index.html (login y Acerca
# de, mailto 265 -> 266), android/app/build.gradle e iOS
# (MARKETING_VERSION 2.5.16 / CURRENT_PROJECT_VERSION 70, Debug y
# Release).
# Uso: python3 patch_20266_web.py [ruta-base-del-proyecto]
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '/home/hatch/workspace/android/checklist-cloud'
HTML = os.path.join(BASE, 'www/index.html')
GRADLE = os.path.join(BASE, 'android/app/build.gradle')
PBX = os.path.join(BASE, 'ios/App/App.xcodeproj/project.pbxproj')
FB = os.path.join(BASE, 'www/cloud/firebase.js')
RULES = os.path.join(BASE, 'firestore.rules')


def patch(path, pairs):
    s = open(path, encoding='utf-8').read()
    for old, new, n in pairs:
        c = s.count(old)
        assert c == n, '%s: NO ENCONTRADO x%d (esperado %d): %r' % (path, c, n, old[:120])
        s = s.replace(old, new)
    open(path, 'w', encoding='utf-8').write(s)
    return s


# --- www/index.html: versión y mailto.
patch(HTML, [
    ('<p class="login-sub" style="font-size:11px;color:#999">Versión 2.5.15</p>',
     '<p class="login-sub" style="font-size:11px;color:#999">Versión 2.5.16</p>', 1),
    ('<div class="line">Versión: 2.5.15</div>',
     '<div class="line">Versión: 2.5.16</div>', 1),
    ("encodeURIComponent('Reporte de problema - Checklist de Soporte 265')",
     "encodeURIComponent('Reporte de problema - Checklist de Soporte 266')", 1),
    ("encodeURIComponent('Describe el problema:\\n\\n\\nVersión de la app: 265')",
     "encodeURIComponent('Describe el problema:\\n\\n\\nVersión de la app: 266')", 1),
])

# --- www/index.html: botones en Inicio.
patch(HTML, [
    ("""      <button class="menu-btn green" id="btnGoResp"><span class="ic">📋</span><span>Responsiva<small>formulario para el colaborador</small></span></button>""",
     """      <button class="menu-btn green" id="btnGoResp"><span class="ic">📋</span><span>Responsiva<small>formulario para el colaborador</small></span></button>
      <button class="menu-btn dark" id="btnGoAcuse"><span class="ic">📄</span><span>Acuse Sistemas<small>acuse de recibido de documentos</small></span></button>
      <button class="menu-btn green" id="btnGoCarta"><span class="ic">📑</span><span>Carta Responsiva<small>resguardo de equipo de cómputo</small></span></button>""", 1),
])

# --- www/index.html: vistas viewAcuse y viewCarta (después de viewResp).
patch(HTML, [
    ("""      <div id="respArchList"></div>
      </div>
    </div>
  </div>
  <div id="viewUsuarios" hidden>""",
     r"""      <div id="respArchList"></div>
      </div>
    </div>
  </div>
  <div id="viewAcuse" hidden>
    <div class="card">
      <b>Acuse Sistemas</b>
      <div class="share-note">Acuse de recibido de documentos de Sistemas: se guarda en este teléfono o en la nube y genera su PDF para imprimir o compartir.</div>
    </div>
    <div class="panel" id="acuseFormBox">
      <div class="field"><label>Fecha *</label><input id="fAc-fecha" type="date"></div>
      <div class="field"><label>Para *</label><input id="fAc-para" placeholder="Nombre y área de quien recibe"></div>
      <div class="field"><label>De *</label><input id="fAc-de" placeholder="SISTEMAS"></div>
      <div class="field"><label>Anexo</label><input id="fAc-anexo" placeholder="Documentación anexa (opcional)"></div>
      <div class="actions">
        <button class="btn-green" id="btnAcuseGuardar">💾 Guardar acuse</button>
        <button class="btn-dark" id="btnAcusePdf">📄 Generar PDF</button>
        <button class="btn-ghost" id="btnAcuseLimpiar">Limpiar</button>
        <button class="btn-ghost" id="btnAcuseVolver">← Volver a Inicio</button>
      </div>
    </div>
    <div class="panel">
      <b>Acuses guardados</b>
      <div id="acuseList"><div class="empty">Aún no hay acuses guardados.</div></div>
    </div>
  </div>
  <div id="viewCarta" hidden>
    <div class="card">
      <b>Carta Responsiva</b>
      <div class="share-note">Carta responsiva para resguardo y uso de equipo de cómputo (FO-SI-10). El folio se asigna al guardar; el PDF reproduce el formato original en 2 páginas.</div>
    </div>
    <div class="panel" id="cartaFormBox">
      <div class="field"><label>Fecha de solicitud *</label><input id="fCa-fecha" type="date"></div>
      <div class="field"><label>Folio</label><input id="fCa-folio" readonly placeholder="Se asigna al guardar"></div>
      <div class="field"><label>Nombre del colaborador *</label><input id="fCa-nombre" placeholder="Nombre completo del colaborador"></div>
      <div class="field"><label>Número de colaborador</label><input id="fCa-colaborador" placeholder="Número de colaborador"></div>
      <div class="field"><label>Sucursal</label><input id="fCa-sucursal" placeholder="Sucursal"></div>
      <div class="field"><label>Puesto</label><input id="fCa-puesto" placeholder="Puesto"></div>
      <div class="field"><label>Jefe Directo</label><input id="fCa-jefe" placeholder="Jefe directo"></div>
      <div class="field"><label>Ip de Red</label><input id="fCa-ip" placeholder="Ip de red (opcional)"></div>
      <div class="field"><label>Observaciones</label><textarea id="fCa-observaciones" placeholder="Observaciones (opcional)"></textarea></div>
      <b>Equipo (Exclusivo de Sistemas)</b>
      <div id="cartaEqRows"></div>
      <div class="actions"><button class="btn-dark" id="btnCartaEqAdd">➕ Agregar equipo</button></div>
      <div class="actions">
        <button class="btn-green" id="btnCartaGuardar">💾 Guardar carta</button>
        <button class="btn-dark" id="btnCartaPdf">📄 Generar PDF</button>
        <button class="btn-ghost" id="btnCartaLimpiar">Limpiar</button>
        <button class="btn-ghost" id="btnCartaVolver">← Volver a Inicio</button>
      </div>
    </div>
    <div class="panel">
      <b>Cartas guardadas</b>
      <div id="cartaList"><div class="empty">Aún no hay cartas guardadas.</div></div>
    </div>
  </div>
  <div id="viewUsuarios" hidden>""", 1),
])

# --- android/app/build.gradle: versionCode 70 / versionName 2.5.16.
patch(GRADLE, [
    ('        versionCode 69\n', '        versionCode 70\n', 1),
    ('        versionName "2.5.15"\n', '        versionName "2.5.16"\n', 1),
])

# --- iOS: MARKETING_VERSION 2.5.16 / CURRENT_PROJECT_VERSION 70 (Debug y Release).
patch(PBX, [
    ('MARKETING_VERSION = 2.5.15;', 'MARKETING_VERSION = 2.5.16;', 2),
    ('CURRENT_PROJECT_VERSION = 69;', 'CURRENT_PROJECT_VERSION = 70;', 2),
])

# --- www/cloud/firebase.js: acuses, cartas y folio de carta.
patch(FB, [
    ("""async function archivarResponsiva(id, archivado) {
  return updateDoc(doc(db, 'responsivas', id), archivado
    ? { archivado: true, archivadoEn: Date.now() }
    : { archivado: false, archivadoEn: null });
}""",
     """async function archivarResponsiva(id, archivado) {
  return updateDoc(doc(db, 'responsivas', id), archivado
    ? { archivado: true, archivadoEn: Date.now() }
    : { archivado: false, archivadoEn: null });
}

// Acuses de Sistemas (2.5.16): acuse de recibido de documentos, sin
// folio y sin página pública. El documento lleva creadoPor,
// creadoPorNombre, creadoEn y datos {fecha, para, de, anexo}.
// uidOpcional filtra por creadoPor (lo usan los usuarios normales para
// que las reglas permitan la lectura); sin él el admin suscribe todo.
async function crearAcuse(datos, creadoPorNombre) {
  const u = auth.currentUser;
  if (!u) throw new Error('no-auth');
  const ref = doc(collection(db, 'acuses'));
  await setDoc(ref, {
    creadoPor: u.uid,
    creadoPorNombre: creadoPorNombre || u.email || '',
    creadoEn: Date.now(),
    datos: datos || {}
  });
  return ref.id;
}

function subscribeAcuses(cb, uidOpcional) {
  const q = uidOpcional
    ? query(collection(db, 'acuses'), where('creadoPor', '==', uidOpcional))
    : collection(db, 'acuses');
  return onSnapshot(
    q,
    (snap) => cb(snap.docs.map((d) => Object.assign({ id: d.id }, d.data()))),
    (err) => console.warn('[Cloud] Error en snapshot de acuses:', err)
  );
}

async function upsertAcuse(rec) {
  return setDoc(
    doc(db, 'acuses', rec.id),
    Object.assign({}, rec, { updatedAt: Date.now() }),
    { merge: true }
  );
}

async function deleteAcuse(id) {
  return deleteDoc(doc(db, 'acuses', id));
}

async function getAcuse(id) {
  const snap = await getDoc(doc(db, 'acuses', id));
  return snap.exists() ? Object.assign({ id: snap.id }, snap.data()) : null;
}

// Folio de la carta responsiva (2.5.16): config/foliosCarta.siguiente
// empieza en 1; la transacción lee, asigna el folio con 5 dígitos y
// sube el contador, así dos teléfonos no repiten folio. Espejo de
// asignarFolio() (config/folios de Mantenimientos).
async function asignarFolioCarta() {
  const ref = doc(db, 'config', 'foliosCarta');
  return runTransaction(db, async (tx) => {
    const snap = await tx.get(ref);
    const n = (snap.exists() && typeof snap.data().siguiente === 'number') ? snap.data().siguiente : 1;
    tx.set(ref, { siguiente: n + 1 });
    return String(n).padStart(5, '0');
  });
}

// Cartas Responsivas FO-SI-10 (2.5.16): resguardo y uso de equipo de
// cómputo. El folio se asigna al guardar (crearCarta lo pide con
// asignarFolioCarta); el documento lleva creadoPor, creadoPorNombre,
// creadoEn, folio y datos {fecha, nombre, colaborador, sucursal,
// puesto, jefe, ip, observaciones, equipos: [{modelo, marca, serie,
// concepto}]}. Sin página pública: solo el técnico y el admin.
async function crearCarta(datos, creadoPorNombre) {
  const u = auth.currentUser;
  if (!u) throw new Error('no-auth');
  const folio = await asignarFolioCarta();
  const ref = doc(collection(db, 'cartas'));
  await setDoc(ref, {
    creadoPor: u.uid,
    creadoPorNombre: creadoPorNombre || u.email || '',
    creadoEn: Date.now(),
    folio: folio,
    datos: datos || {}
  });
  return { id: ref.id, folio: folio };
}

function subscribeCartas(cb, uidOpcional) {
  const q = uidOpcional
    ? query(collection(db, 'cartas'), where('creadoPor', '==', uidOpcional))
    : collection(db, 'cartas');
  return onSnapshot(
    q,
    (snap) => cb(snap.docs.map((d) => Object.assign({ id: d.id }, d.data()))),
    (err) => console.warn('[Cloud] Error en snapshot de cartas:', err)
  );
}

async function upsertCarta(rec) {
  return setDoc(
    doc(db, 'cartas', rec.id),
    Object.assign({}, rec, { updatedAt: Date.now() }),
    { merge: true }
  );
}

async function deleteCarta(id) {
  return deleteDoc(doc(db, 'cartas', id));
}

async function getCarta(id) {
  const snap = await getDoc(doc(db, 'cartas', id));
  return snap.exists() ? Object.assign({ id: snap.id }, snap.data()) : null;
}""", 1),
    ("""  archivarResponsiva,
""",
     """  archivarResponsiva,
  crearAcuse,
  subscribeAcuses,
  upsertAcuse,
  deleteAcuse,
  getAcuse,
  asignarFolioCarta,
  crearCarta,
  subscribeCartas,
  upsertCarta,
  deleteCarta,
  getCarta,
""", 1),
])

# --- firestore.rules: acuses, cartas y foliosCarta.
patch(RULES, [
    ("""    // Folios de órdenes de servicio (2.5.0): config/folios.siguiente es el""",
     """    // Acuses de Sistemas (2.5.16): acuse de recibido de documentos,
    // sin folio y sin página pública. Un usuario normal solo ve los que
    // creó (creadoPor propio); el admin ve todos. Crear: usuario activo
    // con su propio creadoPor. Actualizar/borrar: admin o propio.
    match /acuses/{id} {
      allow list, get: if isActive() && (isAdmin() || resource.data.creadoPor == request.auth.uid);
      allow create: if isActive() && request.resource.data.creadoPor == request.auth.uid;
      allow update, delete: if isActive() && (isAdmin() || resource.data.creadoPor == request.auth.uid);
    }

    // Cartas Responsivas FO-SI-10 (2.5.16): resguardo y uso de equipo
    // de cómputo, con folio de 5 dígitos asignado al guardar. Mismo
    // patrón que acuses: sin página pública, solo el técnico y el admin.
    match /cartas/{id} {
      allow list, get: if isActive() && (isAdmin() || resource.data.creadoPor == request.auth.uid);
      allow create: if isActive() && request.resource.data.creadoPor == request.auth.uid;
      allow update, delete: if isActive() && (isAdmin() || resource.data.creadoPor == request.auth.uid);
    }

    // Folios de órdenes de servicio (2.5.0): config/folios.siguiente es el""", 1),
    ("""    match /config/folios {
      allow read: if isActive();
      allow create: if isActive() && request.resource.data.siguiente is int;
      allow update: if isActive()
        && request.resource.data.diff(resource.data).changedKeys().hasOnly(['siguiente'])
        && request.resource.data.siguiente == resource.data.siguiente + 1;
      allow delete: if false;
    }""",
     """    match /config/folios {
      allow read: if isActive();
      allow create: if isActive() && request.resource.data.siguiente is int;
      allow update: if isActive()
        && request.resource.data.diff(resource.data).changedKeys().hasOnly(['siguiente'])
        && request.resource.data.siguiente == resource.data.siguiente + 1;
      allow delete: if false;
    }

    // Folios de cartas responsivas (2.5.16): config/foliosCarta.siguiente
    // es el próximo folio a asignar (empieza en 1). Espejo de
    // config/folios: leer activos; crear con siguiente entero;
    // actualizar solo subir el contador de uno en uno.
    match /config/foliosCarta {
      allow read: if isActive();
      allow create: if isActive() && request.resource.data.siguiente is int;
      allow update: if isActive()
        && request.resource.data.diff(resource.data).changedKeys().hasOnly(['siguiente'])
        && request.resource.data.siguiente == resource.data.siguiente + 1;
      allow delete: if false;
    }""", 1),
])

print('parche 2.5.16 (parte 1: versiones, vistas, firebase.js, reglas) aplicado')

# --- www/index.html: fmtFechaLarga + hoyISO (después de fmtFecha).
patch(HTML, [
    ("""function fmtFecha(v) {
  var d = fechaDe(v);
  return d ? d.toLocaleDateString('es-MX', { day: '2-digit', month: 'short', year: 'numeric' }) : '-';
}""",
     r"""function fmtFecha(v) {
  var d = fechaDe(v);
  return d ? d.toLocaleDateString('es-MX', { day: '2-digit', month: 'short', year: 'numeric' }) : '-';
}
// Fecha de hoy en formato de <input type="date"> (AAAA-MM-DD) con la
// fecha local del teléfono, sin depender de la zona horaria.
function hoyISO() {
  var d = new Date();
  function p(n) { return (n < 10 ? '0' : '') + n; }
  return d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate());
}
// (266) Fecha larga del Acuse y la Carta, como en el formato original:
// "Septiembre 01, 2026" (mes en español, día a 2 dígitos, año). Acepta
// 'AAAA-MM-DD' (el valor del input date) o cualquier valor de fechaDe.
// Se parsea por partes para no depender de la zona horaria.
var MESES_ES = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
function fmtFechaLarga(v) {
  var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(v || ''));
  if (m) {
    var mi = Number(m[2]);
    if (mi < 1 || mi > 12) return '-';
    return MESES_ES[mi - 1] + ' ' + m[3] + ', ' + m[1];
  }
  var d = fechaDe(v);
  if (!d) return '-';
  function p2(n) { return (n < 10 ? '0' : '') + n; }
  return MESES_ES[d.getMonth()] + ' ' + p2(d.getDate()) + ', ' + d.getFullYear();
}""", 1),
])

# --- www/index.html: listeners de los botones del menú Inicio.
patch(HTML, [
    ("""document.getElementById('btnGoResp').addEventListener('click', function () { showVista('resp'); });""",
     """document.getElementById('btnGoResp').addEventListener('click', function () { showVista('resp'); });
document.getElementById('btnGoAcuse').addEventListener('click', function () { showVista('acuse'); });
document.getElementById('btnGoCarta').addEventListener('click', function () { showVista('carta'); });""", 1),
])

# --- www/index.html: suscripciones cloud al entrar (después de Responsivas).
patch(HTML, [
    ("""    if (window.Cloud.subscribeResponsivas) {
      if (cloudRespUnsub) cloudRespUnsub();
      cloudRespUnsub = window.Cloud.subscribeResponsivas(function (docs) {
        responsivas = docs || [];
        renderRespList();
      }, cloudRole === 'admin' ? null : (cloudUser ? cloudUser.uid : null));
    }""",
     """    if (window.Cloud.subscribeResponsivas) {
      if (cloudRespUnsub) cloudRespUnsub();
      cloudRespUnsub = window.Cloud.subscribeResponsivas(function (docs) {
        responsivas = docs || [];
        renderRespList();
      }, cloudRole === 'admin' ? null : (cloudUser ? cloudUser.uid : null));
    }
    if (window.Cloud.subscribeAcuses) {
      if (cloudAcuseUnsub) cloudAcuseUnsub();
      cloudAcuseUnsub = window.Cloud.subscribeAcuses(function (docs) {
        acuses = mergeAcuseWithLocal(docs);
        saveAcuseLocal();
        renderAcuseList();
      }, cloudRole === 'admin' ? null : (cloudUser ? cloudUser.uid : null));
    }
    if (window.Cloud.subscribeCartas) {
      if (cloudCartaUnsub) cloudCartaUnsub();
      cloudCartaUnsub = window.Cloud.subscribeCartas(function (docs) {
        cartas = mergeCartaWithLocal(docs);
        saveCartaLocal();
        renderCartaList();
      }, cloudRole === 'admin' ? null : (cloudUser ? cloudUser.uid : null));
    }""", 1),
])

# --- www/index.html: showVista (vistas nuevas + hooks al entrar).
patch(HTML, [
    ("""  document.getElementById('viewResp').hidden = v !== 'resp';""",
     """  document.getElementById('viewResp').hidden = v !== 'resp';
  document.getElementById('viewAcuse').hidden = v !== 'acuse';
  document.getElementById('viewCarta').hidden = v !== 'carta';""", 1),
    ("""  if (v === 'resp') { respCargarWa(); respCargarBorrador(); respSuscribir(); renderRespList(); }""",
     """  if (v === 'resp') { respCargarWa(); respCargarBorrador(); respSuscribir(); renderRespList(); }
  if (v === 'acuse') { acusePrefillFecha(); renderAcuseList(); acuseSuscribir(); }
  if (v === 'carta') { cartaPrefillFecha(); cartaEqRender(); renderCartaList(); cartaSuscribir(); }""", 1),
])

# --- www/index.html: lógica de Acuse y Carta (antes de los listeners de Mant).
patch(HTML, [
    ("""respCargarWa();
document.getElementById('btnMantGuardar').addEventListener('click', function () { mantGuardarBorrador(); });""",
     r"""respCargarWa();
// (266) Acuse Sistemas y Carta Responsiva FO-SI-10: dos formularios
// con PDF que reproducen los formatos originales. Sin nube (modo
// local) los guardados van a localStorage; con nube van a Firestore
// (colecciones 'acuses' y 'cartas') y la lista llega por suscripción,
// igual que Responsivas (cada técnico ve los suyos, el admin todos).
// El folio de la Carta se asigna al guardar (nube: transacción
// asignarFolioCarta vía crearCarta; local: contador en localStorage).
// El Acuse no lleva folio. Al guardar, el formulario queda con los
// datos y el folio (carta) para generar el PDF enseguida; Limpiar lo
// vacía para el siguiente. Tocar un guardado lo carga en el formulario
// para reimprimir o compartir; Eliminar es admin o dueño.
var ACUSE_LS_KEY = 'checklist-soporte-acuses-v1';
var CARTA_LS_KEY = 'checklist-soporte-cartas-v1';
var CARTA_FOLIO_LOCAL_KEY = 'checklist-soporte-folios-carta-local-v1';
var acuses = [];
var cartas = [];
var cloudAcuseUnsub = null;
var cloudCartaUnsub = null;
var acuseEditId = null;
var cartaEditId = null;
var cartaEqFilas = [{ modelo: '', marca: '', serie: '', concepto: '' }];

function cartaEqFilaVacia() { return { modelo: '', marca: '', serie: '', concepto: '' }; }
function loadAcuseLocal() {
  try {
    var raw = localStorage.getItem(ACUSE_LS_KEY);
    if (raw) { var arr = JSON.parse(raw); if (Array.isArray(arr)) acuses = arr; }
  } catch (e) {}
}
function saveAcuseLocal() {
  try { localStorage.setItem(ACUSE_LS_KEY, JSON.stringify(acuses)); } catch (e) {}
}
function loadCartaLocal() {
  try {
    var raw = localStorage.getItem(CARTA_LS_KEY);
    if (raw) { var arr = JSON.parse(raw); if (Array.isArray(arr)) cartas = arr; }
  } catch (e) {}
}
function saveCartaLocal() {
  try { localStorage.setItem(CARTA_LS_KEY, JSON.stringify(cartas)); } catch (e) {}
}
// Al recibir la lista de la nube, conservar los guardados locales que
// la nube aún no trae (igual que mergeMantWithLocal).
function mergeAcuseWithLocal(docs) {
  var byId = {};
  acuses.forEach(function (a) { byId[a.id] = a; });
  var out = (docs || []).slice();
  var ids = {};
  out.forEach(function (a) { ids[a.id] = true; });
  Object.keys(byId).forEach(function (id) { if (!ids[id]) out.push(byId[id]); });
  return out;
}
function mergeCartaWithLocal(docs) {
  var byId = {};
  cartas.forEach(function (c) { byId[c.id] = c; });
  var out = (docs || []).slice();
  var ids = {};
  out.forEach(function (c) { ids[c.id] = true; });
  Object.keys(byId).forEach(function (id) { if (!ids[id]) out.push(byId[id]); });
  return out;
}
function acuseSuscribir() {
  if (!CLOUD_ENABLED || !window.Cloud || !window.Cloud.subscribeAcuses) return;
  if (cloudAcuseUnsub) return;
  cloudAcuseUnsub = window.Cloud.subscribeAcuses(function (docs) {
    acuses = mergeAcuseWithLocal(docs);
    saveAcuseLocal();
    renderAcuseList();
  }, cloudRole === 'admin' ? null : (cloudUser ? cloudUser.uid : null));
}
function cartaSuscribir() {
  if (!CLOUD_ENABLED || !window.Cloud || !window.Cloud.subscribeCartas) return;
  if (cloudCartaUnsub) return;
  cloudCartaUnsub = window.Cloud.subscribeCartas(function (docs) {
    cartas = mergeCartaWithLocal(docs);
    saveCartaLocal();
    renderCartaList();
  }, cloudRole === 'admin' ? null : (cloudUser ? cloudUser.uid : null));
}
// --- Acuse: formulario.
function acusePrefillFecha() {
  var el = document.getElementById('fAc-fecha');
  if (el && !el.value) el.value = hoyISO();
}
function acuseLeerForm() {
  function v(id) { var el = document.getElementById(id); return el ? el.value : ''; }
  return { fecha: v('fAc-fecha'), para: v('fAc-para').trim(), de: v('fAc-de').trim(), anexo: v('fAc-anexo').trim() };
}
function acuseValidar(d) {
  var ok = true;
  [['fAc-para', d.para], ['fAc-de', d.de]].forEach(function (p) {
    var el = document.getElementById(p[0]);
    if (el) el.classList.toggle('campo-falta', !p[1]);
    if (!p[1]) ok = false;
  });
  return ok;
}
function acuseLimpiarForm() {
  ['fAc-para', 'fAc-de', 'fAc-anexo'].forEach(function (id) {
    var el = document.getElementById(id);
    if (el) { el.value = ''; el.classList.remove('campo-falta'); }
  });
  acuseEditId = null;
  acusePrefillFecha();
}
function acuseCargarEnForm(a) {
  var d = (a && a.datos) || {};
  function set(id, val) { var el = document.getElementById(id); if (el) el.value = val || ''; }
  set('fAc-fecha', d.fecha || hoyISO());
  set('fAc-para', d.para);
  set('fAc-de', d.de);
  set('fAc-anexo', d.anexo);
  acuseEditId = a.id;
}
function acuseFind(id) { var f = null; acuses.forEach(function (x) { if (x.id === id) f = x; }); return f; }
async function acuseGuardar() {
  var d = acuseLeerForm();
  if (!acuseValidar(d)) { showToast('Faltan datos obligatorios: Para y De.'); return false; }
  var a = null;
  if (acuseEditId) acuses.forEach(function (x) { if (x.id === acuseEditId) a = x; });
  if (!a) {
    if (CLOUD_ENABLED && cloudUser && window.Cloud && window.Cloud.crearAcuse) {
      try {
        var newId = await window.Cloud.crearAcuse(d, technicianName());
        a = { id: newId, creadoEn: Date.now(), creadoPor: cloudUser.uid, creadoPorNombre: technicianName(), datos: d };
        acuses.push(a);
      } catch (e) { showToast('No se pudo guardar el acuse en la nube. Revisa tu conexión.'); return false; }
    } else {
      a = { id: uid(), creadoEn: Date.now(), creadoPor: (cloudUser && cloudUser.uid) || '', creadoPorNombre: technicianName(), datos: d };
      acuses.push(a);
    }
  } else {
    a.datos = d;
    if (CLOUD_ENABLED && cloudUser && window.Cloud && window.Cloud.upsertAcuse) {
      try { await window.Cloud.upsertAcuse(a); } catch (e) { showToast('No se pudo guardar el acuse en la nube. Revisa tu conexión.'); return false; }
    }
  }
  saveAcuseLocal();
  acuseEditId = a.id;
  renderAcuseList();
  showToast('Acuse guardado.');
  return true;
}
function acusePuedeBorrar(a) {
  if (!CLOUD_ENABLED || !cloudUser) return true;
  return cloudRole === 'admin' || !a.creadoPor || a.creadoPor === cloudUser.uid;
}
function acuseCardHtml(a) {
  var d = a.datos || {};
  var html = '<div class="card"><b>Acuse · ' + esc(fmtFechaLarga(d.fecha)) + '</b>' +
    '<div class="sub">Para: ' + esc(d.para || '—') + ' · De: ' + esc(d.de || '—') + '</div>';
  if (d.anexo) html += '<div class="sub">Anexo: ' + esc(d.anexo) + '</div>';
  html += '<div class="sub">Creado por ' + esc(a.creadoPorNombre || '—') + (a.creadoEn ? ' · ' + fmtDate(a.creadoEn) : '') + '</div>';
  html += '<div class="actions"><button class="btn-green" data-acuse-open="' + esc(a.id) + '">📝 Abrir</button>' +
    '<button class="btn-dark" data-acuse-pdf="' + esc(a.id) + '">📄 PDF</button>' +
    '<button class="btn-green" data-acuse-wa="' + esc(a.id) + '">📲 PDF por WhatsApp</button>' +
    '<button class="btn-dark" data-acuse-mail="' + esc(a.id) + '">✉️ PDF por correo</button>';
  if (acusePuedeBorrar(a)) html += '<button class="btn-danger" data-acuse-del="' + esc(a.id) + '">🗑️ Eliminar</button>';
  return html + '</div></div>';
}
function renderAcuseList() {
  var box = document.getElementById('acuseList');
  if (!box) return;
  if (!acuses.length) { box.innerHTML = '<div class="empty">Aún no hay acuses guardados.</div>'; return; }
  var list = acuses.slice().sort(function (x, y) { return (y.creadoEn || 0) - (x.creadoEn || 0); });
  box.innerHTML = list.map(acuseCardHtml).join('');
}
function acuseEliminar(id) {
  acuses = acuses.filter(function (x) { return x.id !== id; });
  saveAcuseLocal();
  if (CLOUD_ENABLED && cloudUser && window.Cloud && window.Cloud.deleteAcuse) {
    window.Cloud.deleteAcuse(id).catch(function (e) { console.warn('No se pudo borrar el acuse en la nube', e); });
  }
  renderAcuseList();
  showToast('Acuse eliminado.');
}
function acuseTexto(a) {
  var d = (a && a.datos) || {};
  return 'Acuse Sistemas — Checklist de Soporte. Para: ' + (d.para || '—') + ', De: ' + (d.de || '—') + (d.anexo ? ', Anexo: ' + d.anexo : '') + '.';
}
function acusePdfDesdeForm() {
  var d = acuseLeerForm();
  if (!acuseValidar(d)) { showToast('Faltan datos obligatorios: Para y De.'); return; }
  var a = acuseEditId ? acuseFind(acuseEditId) : null;
  acuseCompartirPdf({ id: (a && a.id) || 'borrador', datos: d }, 'pdf');
}
async function acuseCompartirPdf(a, via) {
  var out = acusePdfBlob(a);
  await compartirPdfDoc(out, acuseTexto(a), via, 'Acuse Sistemas — Checklist de Soporte');
}
function acuseListClick(e) {
  var t = e.target;
  var q = function (attr) { var el = t.closest('[' + attr + ']'); return el ? el.getAttribute(attr) : null; };
  var id = q('data-acuse-open') || q('data-acuse-pdf') || q('data-acuse-wa') || q('data-acuse-mail') || q('data-acuse-del');
  if (!id) return;
  var a = acuseFind(id);
  if (!a) return;
  if (t.closest('[data-acuse-open]')) { acuseCargarEnForm(a); window.scrollTo(0, 0); return; }
  if (t.closest('[data-acuse-pdf]')) { acuseCompartirPdf(a, 'pdf'); return; }
  if (t.closest('[data-acuse-wa]')) { acuseCompartirPdf(a, 'wa'); return; }
  if (t.closest('[data-acuse-mail]')) { acuseCompartirPdf(a, 'mail'); return; }
  if (t.closest('[data-acuse-del]')) {
    if (!acusePuedeBorrar(a)) return;
    showConfirm('¿Eliminar este acuse?').then(function (ok) { if (ok) acuseEliminar(id); });
  }
}
// --- Carta: formulario y filas de equipo.
function cartaPrefillFecha() {
  var el = document.getElementById('fCa-fecha');
  if (el && !el.value) el.value = hoyISO();
}
function cartaEqRender() {
  var box = document.getElementById('cartaEqRows');
  if (!box) return;
  if (!cartaEqFilas.length) cartaEqFilas = [cartaEqFilaVacia()];
  box.innerHTML = cartaEqFilas.map(function (r, i) {
    function inp(campo, label, ph) {
      return '<div class="field"><label>' + label + '</label><input data-eq-field="' + campo + '" data-eq-row="' + i + '" value="' + esc(r[campo] || '') + '" placeholder="' + ph + '"></div>';
    }
    return '<div class="panel"><div class="grid2">' + inp('modelo', 'Modelo', 'Modelo') + inp('marca', 'Marca', 'Marca') + inp('serie', 'Número de serie', 'Número de serie') + inp('concepto', 'Concepto', 'Concepto') + '</div>' +
      '<div class="actions"><button class="btn-ghost" type="button" data-eq-del="' + i + '">✕ Quitar equipo</button></div></div>';
  }).join('');
}
function cartaEqAddRow() { cartaEqFilas.push(cartaEqFilaVacia()); cartaEqRender(); }
function cartaEqRemoveRow(i) {
  if (cartaEqFilas.length <= 1) { cartaEqFilas = [cartaEqFilaVacia()]; }
  else { cartaEqFilas.splice(i, 1); }
  cartaEqRender();
}
function cartaEqSyncFromDom() {
  var box = document.getElementById('cartaEqRows');
  if (!box || !box.querySelectorAll) return;
  var inputs = box.querySelectorAll('[data-eq-field]');
  if (!inputs || !inputs.length) return;
  var rows = [];
  for (var k = 0; k < inputs.length; k++) {
    var inp = inputs[k];
    var ri = Number(inp.getAttribute('data-eq-row'));
    var f = inp.getAttribute('data-eq-field');
    if (isNaN(ri) || !f) continue;
    if (!rows[ri]) rows[ri] = cartaEqFilaVacia();
    rows[ri][f] = inp.value || '';
  }
  if (rows.length) cartaEqFilas = rows;
}
function cartaLeerForm() {
  function v(id) { var el = document.getElementById(id); return el ? el.value : ''; }
  cartaEqSyncFromDom();
  var equipos = cartaEqFilas.map(function (r) {
    return { modelo: (r.modelo || '').trim(), marca: (r.marca || '').trim(), serie: (r.serie || '').trim(), concepto: (r.concepto || '').trim() };
  });
  return { fecha: v('fCa-fecha'), nombre: v('fCa-nombre').trim(), colaborador: v('fCa-colaborador').trim(), sucursal: v('fCa-sucursal').trim(), puesto: v('fCa-puesto').trim(), jefe: v('fCa-jefe').trim(), ip: v('fCa-ip').trim(), observaciones: v('fCa-observaciones').trim(), equipos: equipos };
}
function cartaValidar(d) {
  var ok = true;
  var elN = document.getElementById('fCa-nombre');
  if (elN) elN.classList.toggle('campo-falta', !d.nombre);
  if (!d.nombre) ok = false;
  var conEquipo = (d.equipos || []).some(function (r) { return r.modelo || r.serie; });
  var box = document.getElementById('cartaEqRows');
  if (box) box.classList.toggle('campo-falta', !conEquipo);
  if (!conEquipo) ok = false;
  return ok;
}
// Folio local (sin nube): contador en localStorage, empieza en 1, 5 dígitos.
function cartaFolioLocal() {
  var n = 1;
  try {
    var raw = localStorage.getItem(CARTA_FOLIO_LOCAL_KEY);
    if (raw) { var p = parseInt(raw, 10); if (!isNaN(p) && p >= 1) n = p; }
    localStorage.setItem(CARTA_FOLIO_LOCAL_KEY, String(n + 1));
  } catch (e) {}
  return String(n).padStart(5, '0');
}
function cartaLimpiarForm() {
  ['fCa-nombre', 'fCa-colaborador', 'fCa-sucursal', 'fCa-puesto', 'fCa-jefe', 'fCa-ip', 'fCa-observaciones'].forEach(function (id) {
    var el = document.getElementById(id);
    if (el) { el.value = ''; el.classList.remove('campo-falta'); }
  });
  var fEl = document.getElementById('fCa-folio');
  if (fEl) fEl.value = '';
  cartaEditId = null;
  cartaEqFilas = [cartaEqFilaVacia()];
  cartaEqRender();
  cartaPrefillFecha();
}
function cartaCargarEnForm(c) {
  var d = (c && c.datos) || {};
  function set(id, val) { var el = document.getElementById(id); if (el) el.value = val || ''; }
  set('fCa-fecha', d.fecha || hoyISO());
  set('fCa-folio', c.folio || '');
  set('fCa-nombre', d.nombre);
  set('fCa-colaborador', d.colaborador);
  set('fCa-sucursal', d.sucursal);
  set('fCa-puesto', d.puesto);
  set('fCa-jefe', d.jefe);
  set('fCa-ip', d.ip);
  set('fCa-observaciones', d.observaciones);
  cartaEqFilas = (Array.isArray(d.equipos) && d.equipos.length ? d.equipos : [cartaEqFilaVacia()]).map(function (r) {
    return { modelo: r.modelo || '', marca: r.marca || '', serie: r.serie || '', concepto: r.concepto || '' };
  });
  cartaEqRender();
  cartaEditId = c.id;
}
function cartaFind(id) { var f = null; cartas.forEach(function (x) { if (x.id === id) f = x; }); return f; }
async function cartaGuardar() {
  var d = cartaLeerForm();
  if (!cartaValidar(d)) { showToast('Faltan datos obligatorios: nombre del colaborador y al menos un equipo con modelo o número de serie.'); return false; }
  var c = null;
  if (cartaEditId) cartas.forEach(function (x) { if (x.id === cartaEditId) c = x; });
  if (!c) {
    if (CLOUD_ENABLED && cloudUser && window.Cloud && window.Cloud.crearCarta) {
      try {
        var created = await window.Cloud.crearCarta(d, technicianName());
        c = { id: created.id, folio: created.folio, creadoEn: Date.now(), creadoPor: cloudUser.uid, creadoPorNombre: technicianName(), datos: d };
        cartas.push(c);
      } catch (e) { showToast('No se pudo guardar la carta en la nube. Revisa tu conexión.'); return false; }
    } else {
      c = { id: uid(), folio: cartaFolioLocal(), creadoEn: Date.now(), creadoPor: (cloudUser && cloudUser.uid) || '', creadoPorNombre: technicianName(), datos: d };
      cartas.push(c);
    }
  } else {
    c.datos = d;
    if (CLOUD_ENABLED && cloudUser && window.Cloud && window.Cloud.upsertCarta) {
      try { await window.Cloud.upsertCarta(c); } catch (e) { showToast('No se pudo guardar la carta en la nube. Revisa tu conexión.'); return false; }
    }
  }
  var fEl = document.getElementById('fCa-folio');
  if (fEl) fEl.value = c.folio || '';
  saveCartaLocal();
  cartaEditId = c.id;
  renderCartaList();
  showToast('Carta guardada con folio ' + (c.folio || '—') + '.');
  return true;
}
function cartaPuedeBorrar(c) {
  if (!CLOUD_ENABLED || !cloudUser) return true;
  return cloudRole === 'admin' || !c.creadoPor || c.creadoPor === cloudUser.uid;
}
function cartaCardHtml(c) {
  var d = c.datos || {};
  var nEq = (d.equipos || []).length;
  var html = '<div class="card"><b>Carta Responsiva · Folio ' + esc(c.folio || '—') + '</b>' +
    '<div class="sub">' + esc(d.nombre || '—') + (d.sucursal ? ' · ' + esc(d.sucursal) : '') + ' · ' + nEq + (nEq === 1 ? ' equipo' : ' equipos') + '</div>' +
    '<div class="sub">Creada por ' + esc(c.creadoPorNombre || '—') + (c.creadoEn ? ' · ' + fmtDate(c.creadoEn) : '') + '</div>' +
    '<div class="actions"><button class="btn-green" data-carta-open="' + esc(c.id) + '">📝 Abrir</button>' +
    '<button class="btn-dark" data-carta-pdf="' + esc(c.id) + '">📄 PDF</button>' +
    '<button class="btn-green" data-carta-wa="' + esc(c.id) + '">📲 PDF por WhatsApp</button>' +
    '<button class="btn-dark" data-carta-mail="' + esc(c.id) + '">✉️ PDF por correo</button>';
  if (cartaPuedeBorrar(c)) html += '<button class="btn-danger" data-carta-del="' + esc(c.id) + '">🗑️ Eliminar</button>';
  return html + '</div></div>';
}
function renderCartaList() {
  var box = document.getElementById('cartaList');
  if (!box) return;
  if (!cartas.length) { box.innerHTML = '<div class="empty">Aún no hay cartas guardadas.</div>'; return; }
  var list = cartas.slice().sort(function (x, y) { return (y.creadoEn || 0) - (x.creadoEn || 0); });
  box.innerHTML = list.map(cartaCardHtml).join('');
}
function cartaEliminar(id) {
  cartas = cartas.filter(function (x) { return x.id !== id; });
  saveCartaLocal();
  if (CLOUD_ENABLED && cloudUser && window.Cloud && window.Cloud.deleteCarta) {
    window.Cloud.deleteCarta(id).catch(function (e) { console.warn('No se pudo borrar la carta en la nube', e); });
  }
  renderCartaList();
  showToast('Carta eliminada.');
}
function cartaTexto(c) {
  var d = (c && c.datos) || {};
  return 'Carta Responsiva' + (c.folio ? ' folio ' + c.folio : '') + ' — Checklist de Soporte. Colaborador: ' + (d.nombre || '—') + '.';
}
function cartaPdfDesdeForm() {
  var d = cartaLeerForm();
  if (!cartaValidar(d)) { showToast('Faltan datos obligatorios: nombre del colaborador y al menos un equipo con modelo o número de serie.'); return; }
  var c = cartaEditId ? cartaFind(cartaEditId) : null;
  cartaCompartirPdf({ id: (c && c.id) || 'borrador', folio: (c && c.folio) || '', datos: d }, 'pdf');
}
async function cartaCompartirPdf(c, via) {
  var out = cartaPdfBlob(c);
  await compartirPdfDoc(out, cartaTexto(c), via, 'Carta Responsiva' + (c.folio ? ' folio ' + c.folio : '') + ' — Checklist de Soporte');
}
function cartaListClick(e) {
  var t = e.target;
  var q = function (attr) { var el = t.closest('[' + attr + ']'); return el ? el.getAttribute(attr) : null; };
  var id = q('data-carta-open') || q('data-carta-pdf') || q('data-carta-wa') || q('data-carta-mail') || q('data-carta-del');
  if (!id) return;
  var c = cartaFind(id);
  if (!c) return;
  if (t.closest('[data-carta-open]')) { cartaCargarEnForm(c); window.scrollTo(0, 0); return; }
  if (t.closest('[data-carta-pdf]')) { cartaCompartirPdf(c, 'pdf'); return; }
  if (t.closest('[data-carta-wa]')) { cartaCompartirPdf(c, 'wa'); return; }
  if (t.closest('[data-carta-mail]')) { cartaCompartirPdf(c, 'mail'); return; }
  if (t.closest('[data-carta-del]')) {
    if (!cartaPuedeBorrar(c)) return;
    showConfirm('¿Eliminar esta carta?').then(function (ok) { if (ok) cartaEliminar(id); });
  }
}
document.getElementById('btnAcuseGuardar').addEventListener('click', function () { acuseGuardar(); });
document.getElementById('btnAcusePdf').addEventListener('click', function () { acusePdfDesdeForm(); });
document.getElementById('btnAcuseLimpiar').addEventListener('click', function () { acuseLimpiarForm(); });
document.getElementById('btnAcuseVolver').addEventListener('click', function () { showVista('inicio'); });
document.getElementById('acuseList').addEventListener('click', acuseListClick);
document.getElementById('btnCartaEqAdd').addEventListener('click', function () { cartaEqAddRow(); });
document.getElementById('btnCartaGuardar').addEventListener('click', function () { cartaGuardar(); });
document.getElementById('btnCartaPdf').addEventListener('click', function () { cartaPdfDesdeForm(); });
document.getElementById('btnCartaLimpiar').addEventListener('click', function () { cartaLimpiarForm(); });
document.getElementById('btnCartaVolver').addEventListener('click', function () { showVista('inicio'); });
document.getElementById('cartaList').addEventListener('click', cartaListClick);
document.getElementById('cartaEqRows').addEventListener('input', function (e) {
  var t = e.target;
  if (!t || !t.getAttribute) return;
  var ri = Number(t.getAttribute('data-eq-row'));
  var f = t.getAttribute('data-eq-field');
  if (isNaN(ri) || !f || !cartaEqFilas[ri]) return;
  cartaEqFilas[ri][f] = t.value || '';
});
document.getElementById('cartaEqRows').addEventListener('click', function (e) {
  var t = e.target;
  var el = t.closest ? t.closest('[data-eq-del]') : null;
  if (!el) return;
  cartaEqRemoveRow(Number(el.getAttribute('data-eq-del')));
});
// Quitar la marca roja al escribir (patrón 255).
['input', 'change'].forEach(function (ev) {
  document.getElementById('acuseFormBox').addEventListener(ev, function (e) {
    var t = e.target;
    if (!t || !t.classList) return;
    t.classList.remove('campo-falta');
  });
  document.getElementById('cartaFormBox').addEventListener(ev, function (e) {
    var t = e.target;
    if (!t || !t.classList) return;
    t.classList.remove('campo-falta');
  });
});
loadAcuseLocal();
loadCartaLocal();
document.getElementById('btnMantGuardar').addEventListener('click', function () { mantGuardarBorrador(); });""", 1),
])

print('parche 2.5.16 (parte 2: JS de Acuse y Carta) aplicado')

# --- www/index.html: PDFs de Acuse y Carta (antes de la firma del técnico).
patch(HTML, [
    ("""// Firma del técnico: canvas con dedo o ratón.""",
     r"""// (266) PDF del Acuse Sistemas (1 página carta): fecha larga arriba,
// tabla PARA / DE / ANEXO con etiquetas en negrita y bloque RECIBE con
// Nombre / Fecha / Firma en blanco para llenar a mano.
function buildPdfAcuse(a) {
  var d = (a && a.datos) || {};
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
  function LN(x1, y1, x2, y2) { cur().push({ k: 'ln', x1: x1, y1: py(y1), x2: x2, y2: py(y2) }); }
  function wrapLines(str, w, s) {
    return wrapText(pdfSafe(str), Math.max(10, Math.floor(w / ((s || 9) * 0.5))));
  }
  function val(v) { return (v == null || v === '') ? '-' : String(v); }
  // Fecha arriba, a la derecha.
  need(20);
  T(fmtFechaLarga(d.fecha), 576, yt, 'F1', 11, null, 'R');
  yt += 26;
  // Tabla PARA / DE / ANEXO.
  var filas = [['PARA:', val(d.para)], ['DE:', val(d.de)], ['ANEXO:', val(d.anexo)]];
  filas.forEach(function (f) {
    var lines = wrapLines(f[1], 460, 10);
    var h = Math.max(24, lines.length * 13 + 10);
    need(h);
    var y0 = yt;
    R(36, y0, 540, h, null);
    T(f[0], 44, y0 + 6, 'F2', 10);
    lines.forEach(function (ln, i) { T(ln, 104, y0 + 6 + i * 13, 'F1', 10); });
    yt += h + 4;
  });
  yt += 30;
  // Bloque RECIBE con líneas en blanco para llenar a mano.
  need(120);
  var y0 = yt;
  T('RECIBE:', 36, y0, 'F2', 11);
  ['Nombre:', 'Fecha:', 'Firma:'].forEach(function (lab, i) {
    var yy = y0 + 24 + i * 28;
    T(lab, 36, yy, 'F2', 10);
    LN(110, yy + 10, 540, yy + 10);
  });
  yt += 24 + 3 * 28;
  return assemblePdfOps(pages, {}, { w: 612, h: 792 });
}
// (266) Texto legal de la Carta Responsiva FO-SI-10, VERBATIM del
// documento original ("RESPONSABILIDADES DEL USUARIO RESGUARDATARIO"),
// con sus rarezas de puntuación (p. ej. "escritos,electrónicos" y
// "comercial,soluciones" sin espacio tras la coma).
var CARTA_RESPONSABILIDADES = [
  'El suscrito (a), quien presta sus servicios laborales para LAPI S.A. DE C.V., en adelante (LAPI), con domicilio en Rosa Blanca No. 63, Colonia Molino de Rosas, Delegación Álvaro Obregón, código postal 01470, Ciudad de México; hago constar que se me entregó el equipo de cómputo antes descrito y me comprometo a resguardarlo así como sus accesorios y toda la información confidencial contenida en el mismo, que en conjunto es de exclusiva propiedad de LAPI S.A. DE C.V., y el cual se me asigna con la única finalidad de apoyar en el cumplimiento de mis actividades laborales por lo que entiendo que queda estrictamente prohibido utilizar el equipo señalado para fines distintos.',
  'Asimismo, acepto y reconozco que tengo acceso a información sensible, confidencial, escrita, oral, gráfica o contenida en medios escritos,electrónicos o electromagnéticos; que incluye de manera enunciativa más no limitativa, información jurídica, contable, financiera y comercial,soluciones, software, datos personales de los clientes, contraseñas y password personalizados, estructura organizacional, composición corporativa, documentos de trabajo, compilaciones, marcas registradas o no registradas, y cualquier otra documentación preparada y conservada con carácter confidencial por "LAPI", o de sus clientes, sean pasados, presentes o potenciales, es clasificada como "INFORMACIÓN CONFIDENCIAL".',
  'Por lo anterior, reconozco que la Información Confidencial que manejo y de la que haya tenido conocimiento antes o después de la fecha de suscripción de este resguardo y que se contenga en mi equipo de cómputo y cualquier medio o dispositivo otorgado para desempeñar mis funciones, será de la exclusiva propiedad de LAPI, y no podrá ser divulgada en forma alguna por el suscrito (a), sin el previo consentimiento, expreso y por escrito de LAPI. No obstante, las obligaciones y derechos del suscrito respecto de la información confidencial y sensible continuarán vigentes aún concluida la relación de trabajo o de colaboración con LAPI, ya que la terminación de relación entre LAPI y el suscrito(a), no me exime de todas las obligaciones contraídas en tiempo y forma aquí contenidas.',
  'El suscrito (a) me comprometo a no utilizar la Información Confidencial y/o sensible para mi beneficio, ni para el beneficio de terceros, incluyendo, pero no limitado, a superiores, socios, familiares sin importar el grado, amigos, colaboradores, representantes y/o clientes, y a no divulgar la información confidencial y/o sensible por ningún medio, así como para evitar su divulgación o reproducción por parte de cualquier tercera persona.',
  'Para el caso de que el suscrito (a), o cualquier persona allegada a mí, incumpla algunas de las estipulaciones previstas, el suscrito (a) pagará a LAPI, los daños y perjuicios que tal evento le ocasionare, sin perjuicio de las demás acciones legales que procedan, por violación a los derechos de propiedad intelectual y derechos de autor que prevé la Ley de la Propiedad Industrial, así como el delito de revelación de secreto o comunicación que prevé el artículo 213 y demás relativos del Código Penal para el Distrito Federal, y finalmente por los delitos en materia del tratamiento indebido de datos personales, que contempla el capítulo XI de la Ley Federal de Protección de Datos Personales en Posesión de los Particulares.',
  'En este acto me hago sabedor, que el equipo de cómputo cuenta con el software institucional debidamente licenciado por lo que queda estrictamente prohibido instalar software adicional al incluido en la configuración original sin contar con la autorización escrita del responsable del área de sistemas.',
  'Acepto que en caso de detectarse mal uso y/o daños al equipo que tengo bajo mi resguardo seré considerado como responsable. Por lo anterior, es imprescindible que, salvo autorizaciones específicas, se evite la utilización de equipamiento por parte de personal no autorizado, ajeno al área solicitante y/o a LAPI S.A. de C.V.',
  'Finalmente, acepto y reconozco que, una vez concluida mi relación laboral con LAPI, tengo la obligación de entregar el equipo bajo mi resguardo, así como la información contenida en el mismo y sus accesorios, en caso contrario, me hago sabedor de la responsabilidad civil por los daños y perjuicios que cause por mi omisión, así como de las acciones penales que puedan derivar por los delitos que ello conlleve.'
];
// (266) PDF de la Carta Responsiva (2 páginas carta): p1 con el
// encabezado fijo del formato (Lapi / Laboratorio Médico, título y
// tabla Código FO-SI-10, Versión 3, Fecha de actualización 25-sep-23,
// Página 1 de 2), Datos del solicitante, tabla Exclusivo de Sistemas y
// Nombre y firma del usuario; p2 con las responsabilidades verbatim y
// la firma final. No hay asset de logo Lapi en el repo: el encabezado
// se reproduce con texto.
function buildPdfCarta(c) {
  var d = (c && c.datos) || {};
  var equipos = Array.isArray(d.equipos) ? d.equipos : [];
  var W = 612, H = 792, M = 36, USABLE = H - M * 2;
  var pages = [[]];
  var yt = 0;
  function cur() { return pages[pages.length - 1]; }
  function need(h) { if (yt + h > USABLE) { pages.push([]); yt = 0; } }
  function newPage() { pages.push([]); yt = 0; }
  function py(ytop) { return H - M - ytop; }
  function T(str, x, ytop, f, s, color, align) {
    cur().push({ k: 't', x: x, y: py(ytop) - (s || 9) * 0.8, f: f || 'F1', s: s || 9, str: pdfSafe(str), color: color || null, a: align || 'L' });
  }
  function R(x, ytop, w, h, fill) {
    cur().push({ k: 'r', x: x, y: py(ytop) - h, w: w, h: h, fill: (fill == null ? null : fill) });
  }
  function LN(x1, y1, x2, y2) { cur().push({ k: 'ln', x1: x1, y1: py(y1), x2: x2, y2: py(y2) }); }
  function wrapLines(str, w, s) {
    return wrapText(pdfSafe(str), Math.max(10, Math.floor(w / ((s || 9) * 0.5))));
  }
  function val(v) { return (v == null || v === '') ? '-' : String(v); }
  function campo(label, value, x, ytop, w) {
    T(label, x, ytop, 'F2', 9);
    var lw = label.length * 5.4 + 4;
    var lines = wrapLines(val(value), w - lw, 9);
    lines.forEach(function (ln, i) { T(ln, x + lw, ytop + i * 11, 'F1', 9); });
  }
  // --- Página 1: encabezado fijo del formato.
  need(66);
  var y0 = yt;
  T('Lapi', 36, y0, 'F2', 20);
  T('Laboratorio Médico', 36, y0 + 23, 'F1', 9);
  var tit = wrapText('CARTA RESPONSIVA PARA RESGUARDO Y USO DE EQUIPO DE CÓMPUTO', 30);
  tit.forEach(function (ln, i) { T(ln, 306, y0 + 2 + i * 12, 'F2', 10, null, 'C'); });
  R(420, y0, 156, 58, null);
  T('Código: FO-SI-10', 426, y0 + 5, 'F1', 8);
  T('Versión: 3', 426, y0 + 17, 'F1', 8);
  T('Fecha de actualización: 25-sep-23', 426, y0 + 29, 'F1', 8);
  T('Página: 1 de 2', 426, y0 + 41, 'F1', 8);
  yt += 66 + 6;
  // Seguridad de la Información + fecha de solicitud + folio.
  need(32);
  y0 = yt;
  T('Seguridad de la Información', 36, y0, 'F2', 10);
  T('Fecha de solicitud: ' + fmtFechaLarga(d.fecha), 36, y0 + 14, 'F1', 9);
  T('FOLIO: ' + (c.folio || '-'), 420, y0 + 14, 'F2', 10);
  yt += 32 + 6;
  // Datos del solicitante.
  need(16);
  T('DATOS DEL SOLICITANTE', 36, yt, 'F2', 10);
  yt += 16;
  var filas = [
    [['Nombre del colaborador:', d.nombre, 540]],
    [['Número de colaborador:', d.colaborador, 264], ['Ip de Red:', d.ip, 264]],
    [['Sucursal:', d.sucursal, 264], ['Puesto:', d.puesto, 264]],
    [['Jefe Directo:', d.jefe, 540]]
  ];
  filas.forEach(function (fila) {
    var hMax = 11;
    fila.forEach(function (cc) {
      var lines = wrapLines(val(cc[1]), cc[2] - (cc[0].length * 5.4 + 4), 9);
      hMax = Math.max(hMax, lines.length * 11);
    });
    need(hMax + 3);
    var xx = 36;
    fila.forEach(function (cc) {
      campo(cc[0], cc[1], xx, yt, cc[2]);
      xx += cc[2] + 12;
    });
    yt += hMax + 3;
  });
  // Observaciones.
  var obsLines = wrapLines('Observaciones: ' + val(d.observaciones), 528, 9);
  var hObs = Math.max(11, obsLines.length * 11);
  need(hObs + 3);
  obsLines.forEach(function (ln, i) { T(ln, 36, yt + i * 11, 'F1', 9); });
  yt += hObs + 6;
  // Exclusivo de Sistemas: tabla de equipos.
  need(16);
  T('Exclusivo de Sistemas', 36, yt, 'F2', 10);
  yt += 16;
  var cols = [
    ['Modelo', 36, 150], ['Marca', 186, 120], ['Número de serie', 306, 150], ['Concepto', 456, 120]
  ];
  need(16);
  y0 = yt;
  R(36, y0, 540, 16, 0.88);
  cols.forEach(function (cc) { T(cc[0], cc[1] + 4, y0 + 3, 'F2', 8); });
  yt += 16;
  equipos.forEach(function (eq) {
    need(16);
    y0 = yt;
    R(36, y0, 540, 16, null);
    T(String(eq.modelo || '-').slice(0, 28), 40, y0 + 3, 'F1', 8);
    T(String(eq.marca || '-').slice(0, 22), 190, y0 + 3, 'F1', 8);
    T(String(eq.serie || '-').slice(0, 28), 310, y0 + 3, 'F1', 8);
    T(String(eq.concepto || '-').slice(0, 22), 460, y0 + 3, 'F1', 8);
    yt += 16;
  });
  yt += 6;
  // Nombre y firma del usuario (página 1).
  need(52);
  y0 = yt;
  T('NOMBRE Y FIRMA DEL USUARIO', 306, y0, 'F2', 10, null, 'C');
  LN(180, y0 + 30, 432, y0 + 30);
  T(val(d.nombre), 306, y0 + 36, 'F1', 9, null, 'C');
  yt += 52;
  // --- Página 2: responsabilidades verbatim + firma final.
  newPage();
  need(30);
  T('Página: 2 de 2', 576, yt, 'F1', 8, null, 'R');
  var tit2 = wrapText('RESPONSABILIDADES DEL USUARIO RESGUARDATARIO', 44);
  tit2.forEach(function (ln, i) { T(ln, 306, yt + 12 + i * 13, 'F2', 11, null, 'C'); });
  yt += 12 + tit2.length * 13 + 8;
  CARTA_RESPONSABILIDADES.forEach(function (p) {
    var lines = wrapLines(p, 528, 9);
    var h = lines.length * 11 + 6;
    need(h);
    lines.forEach(function (ln, i) { T(ln, 36, yt + i * 11, 'F1', 9); });
    yt += h;
  });
  yt += 8;
  need(52);
  y0 = yt;
  T('NOMBRE Y FIRMA DEL USUARIO', 306, y0, 'F2', 10, null, 'C');
  LN(180, y0 + 30, 432, y0 + 30);
  T(val(d.nombre), 306, y0 + 36, 'F1', 9, null, 'C');
  yt += 52;
  return assemblePdfOps(pages, {}, { w: 612, h: 792 });
}
function acusePdfBlob(a) {
  var blob = buildPdfAcuse(a);
  return { blob: blob, name: 'acuse-sistemas-' + (a.id || 'acuse') + '.pdf' };
}
function cartaPdfBlob(c) {
  var blob = buildPdfCarta(c);
  return { blob: blob, name: 'carta-responsiva-' + (c.folio || c.id || 'carta') + '.pdf' };
}
// Compartir un PDF de Acuse/Carta (patrón sharePdfMant): primero se
// intenta guardar en el teléfono (Filesystem + FileOpener/Share); si
// no hay Capacitor, según el destino: 'wa' comparte el archivo por el
// share web o lo descarga y avisa; 'mail' lo descarga y abre el correo
// con el texto; 'pdf' solo lo comparte o descarga.
async function compartirPdfDoc(out, texto, via, asunto) {
  try {
    var res = await guardarPdfCapacitor(out.blob, out.name, texto);
    if (res === 'guardado') return;
  } catch (e) {
    showToast('No se pudo guardar el PDF: ' + (e && e.message ? e.message : 'error al escribir el archivo'));
    return;
  }
  if (via === 'mail') {
    var a2 = document.createElement('a');
    a2.href = URL.createObjectURL(out.blob);
    a2.download = out.name;
    a2.click();
    setTimeout(function () { URL.revokeObjectURL(a2.href); }, 5000);
    window.location.href = 'mailto:?subject=' + encodeURIComponent(asunto || 'Checklist de Soporte') + '&body=' + encodeURIComponent(texto + ' El PDF se descargó, adjúntalo al correo.');
    showToast('PDF descargado: ' + out.name + '.');
    return;
  }
  var file = null;
  try { file = new File([out.blob], out.name, { type: 'application/pdf' }); } catch (e) {}
  if (file && navigator.canShare && navigator.canShare({ files: [file] })) {
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
// Firma del técnico: canvas con dedo o ratón.""", 1),
])

print('parche 2.5.16 (parte 3: PDFs de Acuse y Carta) aplicado')
print('parche 2.5.16 aplicado')
