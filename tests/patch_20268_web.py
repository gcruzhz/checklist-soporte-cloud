# Parche web 2.5.18: folio automático AL ABRIR en Acuse y Carta +
# cajas con borde visible en el PDF de la Carta (como la imagen del
# formato original FO-SI-10).
# 1) Versión 2.5.18 / versionCode 72 (HTML x2, gradle, pbx x2).
# 2) Carta PDF: DATOS DEL SOLICITANTE con cada campo en su CELDA CON
# BORDE (izq.: Nombre/Número/Sucursal/Puesto apilados; der.: Ip de Red
# —2 filas— y «Área: Jefe Directo:» —un solo campo del original, con
# los dos valores del formulario—; Observaciones caja larga de ancho
# completo). Seguridad/Fecha/FOLIO en una línea como el original.
# Tabla Exclusivo de Sistemas: divisores verticales entre columnas
# (el docx tiene insideV; el verde #9BBB59 ya estaba bien).
# Acuse PDF: folio arriba a la derecha, junto a la fecha. PARA/DE/
# ANEXO sin cajas (el docx no tiene bordes ahí) y RECIBE con bordes
# ya estaban bien; no se tocan.
# 3) Folio al abrir: campo fAc-folio nuevo (readonly, «Se asigna al
# abrir»); fCa-folio cambia su placeholder. Al entrar a la vista se
# asigna el folio (nube: transacción; local: contador) y se ve en el
# formulario y en el PDF. Guardar ya NO asigna: usa el folio del
# formulario. Secuencias INDEPENDIENTES acuse/carta. Si se abandona
# sin guardar, el folio queda consumido (hueco, no se devuelve).
# 4) firebase.js: asignarFolioAcuse() (config/foliosAcuse) espejo de
# asignarFolioCarta(); crearAcuse/crearCarta aceptan el folio ya
# asignado (si no viene, lo asignan como antes). firestore.rules:
# regla config/foliosAcuse espejo de foliosCarta (el archivo sigue
# incluyendo TODO: acuses, cartas y ambos contadores — Gerardo aún
# no pega las reglas en la consola).
# Uso: python3 patch_20268_web.py [ruta-base-del-proyecto]
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '/home/hatch/workspace/android/checklist-cloud'
HTML = os.path.join(BASE, 'www/index.html')
FB = os.path.join(BASE, 'www/cloud/firebase.js')
RULES = os.path.join(BASE, 'firestore.rules')
GRADLE = os.path.join(BASE, 'android/app/build.gradle')
PBX = os.path.join(BASE, 'ios/App/App.xcodeproj/project.pbxproj')
DATAMODEL = os.path.join(BASE, 'docs/DATA_MODEL.md')


def read(path):
    return open(path, encoding='utf-8').read()


def write(path, s):
    open(path, 'w', encoding='utf-8').write(s)


def rep(path, old, new, n=1):
    s = read(path)
    if s.count(new) >= 1:
        print('ya aplicado, salto:', old[:60].replace('\n', ' '))
        return
    c = s.count(old)
    assert c == n, '%s: NO ENCONTRADO x%d (esperado %d): %r' % (path, c, n, old[:120])
    write(path, s.replace(old, new))


def span_replace(path, start_marker, end_marker, new_text):
    s = read(path)
    if s.count(start_marker) == 0:
        print('span ya aplicado, salto:', start_marker[:60].replace('\n', ' '))
        return
    assert s.count(start_marker) == 1, '%s: marcador inicial x%d: %r' % (path, s.count(start_marker), start_marker[:80])
    assert s.count(end_marker) == 1, '%s: marcador final x%d: %r' % (path, s.count(end_marker), end_marker[:80])
    a = s.index(start_marker)
    b = s.index(end_marker, a)
    assert b > a, '%s: marcador final antes que el inicial' % path
    write(path, s[:a] + new_text + s[b:])


# --- Versión 2.5.18. ---
rep(HTML, '<p class="login-sub" style="font-size:11px;color:#999">Versión 2.5.17</p>',
    '<p class="login-sub" style="font-size:11px;color:#999">Versión 2.5.18</p>')
rep(HTML, '<div class="line">Versión: 2.5.17</div>',
    '<div class="line">Versión: 2.5.18</div>')
rep(HTML, 'Checklist de Soporte 267', 'Checklist de Soporte 268')
rep(HTML, 'Versión de la app: 267', 'Versión de la app: 268')
rep(GRADLE, 'versionCode 71', 'versionCode 72')
rep(GRADLE, 'versionName "2.5.17"', 'versionName "2.5.18"')
rep(PBX, 'CURRENT_PROJECT_VERSION = 71;', 'CURRENT_PROJECT_VERSION = 72;', 2)
rep(PBX, 'MARKETING_VERSION = 2.5.17;', 'MARKETING_VERSION = 2.5.18;', 2)

# --- Formulario Acuse: campo Folio (readonly) tras la Fecha. ---
rep(HTML, '''      <div class="field"><label>Fecha *</label><input id="fAc-fecha" type="date"></div>
      <div class="field"><label>Para *</label><input id="fAc-para" placeholder="Nombre y área de quien recibe"></div>''',
'''      <div class="field"><label>Fecha *</label><input id="fAc-fecha" type="date"></div>
      <div class="field"><label>Folio</label><input id="fAc-folio" readonly placeholder="Se asigna al abrir"></div>
      <div class="field"><label>Para *</label><input id="fAc-para" placeholder="Nombre y área de quien recibe"></div>''')

# --- Formulario Carta: folio «al abrir» (placeholder + nota). ---
rep(HTML, '<div class="share-note">Carta responsiva para resguardo y uso de equipo de cómputo (FO-SI-10). El folio se asigna al guardar; el PDF reproduce el formato original en 2 páginas.</div>',
    '<div class="share-note">Carta responsiva para resguardo y uso de equipo de cómputo (FO-SI-10). El folio se asigna al abrir el formulario; el PDF reproduce el formato original en 2 páginas.</div>')
rep(HTML, '<div class="field"><label>Folio</label><input id="fCa-folio" readonly placeholder="Se asigna al guardar"></div>',
    '<div class="field"><label>Folio</label><input id="fCa-folio" readonly placeholder="Se asigna al abrir"></div>')

# --- Comentario del flujo (266) -> (268): folio al abrir. ---
rep(HTML, '''// (266) Acuse Sistemas y Carta Responsiva FO-SI-10: dos formularios
// con PDF que reproducen los formatos originales. Sin nube (modo
// local) los guardados van a localStorage; con nube van a Firestore
// (colecciones 'acuses' y 'cartas') y la lista llega por suscripción,
// igual que Responsivas (cada técnico ve los suyos, el admin todos).
// El folio de la Carta se asigna al guardar (nube: transacción
// asignarFolioCarta vía crearCarta; local: contador en localStorage).
// El Acuse no lleva folio. Al guardar, el formulario queda con los
// datos y el folio (carta) para generar el PDF enseguida; Limpiar lo
// vacía para el siguiente. Tocar un guardado lo carga en el formulario
// para reimprimir o compartir; Eliminar es admin o dueño.''',
'''// (268) Acuse Sistemas y Carta Responsiva FO-SI-10: dos formularios
// con PDF que reproducen los formatos originales. Sin nube (modo
// local) los guardados van a localStorage; con nube van a Firestore
// (colecciones 'acuses' y 'cartas') y la lista llega por suscripción,
// igual que Responsivas (cada técnico ve los suyos, el admin todos).
// El FOLIO se asigna AL ABRIR el formulario (nube: transacción
// asignarFolioAcuse / asignarFolioCarta; local: contador en
// localStorage; secuencias INDEPENDIENTES, config/foliosAcuse y
// config/foliosCarta). Si se abandona sin guardar, el folio queda
// consumido (hueco en la numeración, no se devuelve). Al guardar, el
// formulario queda con los datos y el folio para generar el PDF
// enseguida; Limpiar lo vacía y asigna el folio del siguiente.
// Tocar un guardado lo carga en el formulario para reimprimir o
// compartir; Eliminar es admin o dueño.''')

# --- Constante del contador local del Acuse. ---
rep(HTML, "var CARTA_FOLIO_LOCAL_KEY = 'checklist-soporte-folios-carta-local-v1';",
"""var CARTA_FOLIO_LOCAL_KEY = 'checklist-soporte-folios-carta-local-v1';
var ACUSE_FOLIO_LOCAL_KEY = 'checklist-soporte-folios-acuse-local-v1';""")

# --- showVista: asignar el folio al entrar a cada vista. ---
rep(HTML, "  if (v === 'acuse') { acusePrefillFecha(); renderAcuseList(); acuseSuscribir(); }",
    "  if (v === 'acuse') { acusePrefillFecha(); acuseAsignarFolio(); renderAcuseList(); acuseSuscribir(); }")
rep(HTML, "  if (v === 'carta') { cartaPrefillFecha(); cartaEqRender(); renderCartaList(); cartaSuscribir(); }",
    "  if (v === 'carta') { cartaPrefillFecha(); cartaAsignarFolio(); cartaEqRender(); renderCartaList(); cartaSuscribir(); }")

# --- Acuse: Limpiar asigna el folio del siguiente; Cargar muestra el
# del guardado (y asigna uno si el guardado viejo no tenía). ---
rep(HTML, '''function acuseLimpiarForm() {
  ['fAc-para', 'fAc-de', 'fAc-anexo'].forEach(function (id) {
    var el = document.getElementById(id);
    if (el) { el.value = ''; el.classList.remove('campo-falta'); }
  });
  acuseEditId = null;
  acusePrefillFecha();
}''',
'''function acuseLimpiarForm() {
  ['fAc-folio', 'fAc-para', 'fAc-de', 'fAc-anexo'].forEach(function (id) {
    var el = document.getElementById(id);
    if (el) { el.value = ''; el.classList.remove('campo-falta'); }
  });
  acuseEditId = null;
  acusePrefillFecha();
  acuseAsignarFolio();
}''')
rep(HTML, '''  set('fAc-fecha', d.fecha || hoyISO());
  set('fAc-para', d.para);
  set('fAc-de', d.de);
  set('fAc-anexo', d.anexo);
  acuseEditId = a.id;
}''',
'''  set('fAc-fecha', d.fecha || hoyISO());
  set('fAc-folio', a.folio || '');
  set('fAc-para', d.para);
  set('fAc-de', d.de);
  set('fAc-anexo', d.anexo);
  acuseEditId = a.id;
  if (!a.folio) acuseAsignarFolio();
}''')

# --- Acuse: Guardar usa el folio del formulario (ya asignado al
# abrir); si viene vacío (p. ej. nube lenta) lo asigna ahora. ---
rep(HTML, '''async function acuseGuardar() {
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
}''',
'''async function acuseGuardar() {
  var d = acuseLeerForm();
  if (!acuseValidar(d)) { showToast('Faltan datos obligatorios: Para y De.'); return false; }
  // (268) El folio ya viene del formulario (asignado al abrir); si
  // está vacío se asigna ahora como respaldo, nunca al revés.
  var folioEl = document.getElementById('fAc-folio');
  var folio = (folioEl && folioEl.value) || '';
  if (!folio) folio = await acuseAsignarFolio();
  var a = null;
  if (acuseEditId) acuses.forEach(function (x) { if (x.id === acuseEditId) a = x; });
  if (!a) {
    if (CLOUD_ENABLED && cloudUser && window.Cloud && window.Cloud.crearAcuse) {
      try {
        var newId = await window.Cloud.crearAcuse(d, technicianName(), folio);
        a = { id: newId, folio: folio, creadoEn: Date.now(), creadoPor: cloudUser.uid, creadoPorNombre: technicianName(), datos: d };
        acuses.push(a);
      } catch (e) { showToast('No se pudo guardar el acuse en la nube. Revisa tu conexión.'); return false; }
    } else {
      a = { id: uid(), folio: folio, creadoEn: Date.now(), creadoPor: (cloudUser && cloudUser.uid) || '', creadoPorNombre: technicianName(), datos: d };
      acuses.push(a);
    }
  } else {
    a.datos = d;
    if (!a.folio && folio) a.folio = folio;
    if (CLOUD_ENABLED && cloudUser && window.Cloud && window.Cloud.upsertAcuse) {
      try { await window.Cloud.upsertAcuse(a); } catch (e) { showToast('No se pudo guardar el acuse en la nube. Revisa tu conexión.'); return false; }
    }
  }
  if (folioEl) folioEl.value = a.folio || '';
  saveAcuseLocal();
  acuseEditId = a.id;
  renderAcuseList();
  showToast('Acuse guardado con folio ' + (a.folio || '—') + '.');
  return true;
}''')

# --- Acuse: tarjeta con folio y texto para compartir con folio. ---
rep(HTML, '  var html = \'<div class="card"><b>Acuse · \' + esc(fmtFechaLarga(d.fecha)) + \'</b>\' +',
    '  var html = \'<div class="card"><b>Acuse · Folio \' + esc(a.folio || \'—\') + \' · \' + esc(fmtFechaLarga(d.fecha)) + \'</b>\' +')
rep(HTML, """  return 'Acuse Sistemas — Checklist de Soporte. Para: ' + (d.para || '—') + ', De: ' + (d.de || '—') + (d.anexo ? ', Anexo: ' + d.anexo : '') + '.';""",
    """  return 'Acuse Sistemas — Checklist de Soporte. Folio ' + (a.folio || '—') + '. Para: ' + (d.para || '—') + ', De: ' + (d.de || '—') + (d.anexo ? ', Anexo: ' + d.anexo : '') + '.';""")

# --- Acuse: PDF desde el formulario lleva el folio. ---
rep(HTML, '''  var a = acuseEditId ? acuseFind(acuseEditId) : null;
  acuseCompartirPdf({ id: (a && a.id) || 'borrador', datos: d }, 'pdf');''',
'''  var a = acuseEditId ? acuseFind(acuseEditId) : null;
  var folioEl = document.getElementById('fAc-folio');
  acuseCompartirPdf({ id: (a && a.id) || 'borrador', folio: (a && a.folio) || (folioEl && folioEl.value) || '', datos: d }, 'pdf');''')

# --- Funciones de folio al abrir (Acuse + Carta) y contador local del
# Acuse, tras cartaFolioLocal(). ---
rep(HTML, '''// Folio local (sin nube): contador en localStorage, empieza en 1, 5 dígitos.
function cartaFolioLocal() {
  var n = 1;
  try {
    var raw = localStorage.getItem(CARTA_FOLIO_LOCAL_KEY);
    if (raw) { var p = parseInt(raw, 10); if (!isNaN(p) && p >= 1) n = p; }
    localStorage.setItem(CARTA_FOLIO_LOCAL_KEY, String(n + 1));
  } catch (e) {}
  return String(n).padStart(5, '0');
}''',
'''// Folio local (sin nube): contador en localStorage, empieza en 1, 5 dígitos.
function cartaFolioLocal() {
  var n = 1;
  try {
    var raw = localStorage.getItem(CARTA_FOLIO_LOCAL_KEY);
    if (raw) { var p = parseInt(raw, 10); if (!isNaN(p) && p >= 1) n = p; }
    localStorage.setItem(CARTA_FOLIO_LOCAL_KEY, String(n + 1));
  } catch (e) {}
  return String(n).padStart(5, '0');
}
// Folio local del Acuse (sin nube): mismo patrón, secuencia
// INDEPENDIENTE de la de cartas.
function acuseFolioLocal() {
  var n = 1;
  try {
    var raw = localStorage.getItem(ACUSE_FOLIO_LOCAL_KEY);
    if (raw) { var p = parseInt(raw, 10); if (!isNaN(p) && p >= 1) n = p; }
    localStorage.setItem(ACUSE_FOLIO_LOCAL_KEY, String(n + 1));
  } catch (e) {}
  return String(n).padStart(5, '0');
}
// (268) Folio AL ABRIR el formulario: si el campo está vacío se
// asigna uno y se muestra. Nube: transacción (asignarFolioAcuse /
// asignarFolioCarta); sin nube, o si la transacción falla: contador
// local. Si se abandona el formulario sin guardar, el folio queda
// consumido (hueco en la numeración): es lo normal en folios, no se
// devuelve. No reasigna si el campo ya tiene folio (p. ej. al volver
// a la vista con el formulario a medias o con un guardado cargado).
async function acuseAsignarFolio() {
  var el = document.getElementById('fAc-folio');
  if (!el || el.value) return el ? el.value : '';
  var folio = '';
  if (CLOUD_ENABLED && cloudUser && window.Cloud && window.Cloud.asignarFolioAcuse) {
    try { folio = await window.Cloud.asignarFolioAcuse(); } catch (e) { folio = ''; }
  }
  if (!folio) folio = acuseFolioLocal();
  if (el) el.value = folio;
  return folio;
}
async function cartaAsignarFolio() {
  var el = document.getElementById('fCa-folio');
  if (!el || el.value) return el ? el.value : '';
  var folio = '';
  if (CLOUD_ENABLED && cloudUser && window.Cloud && window.Cloud.asignarFolioCarta) {
    try { folio = await window.Cloud.asignarFolioCarta(); } catch (e) { folio = ''; }
  }
  if (!folio) folio = cartaFolioLocal();
  if (el) el.value = folio;
  return folio;
}''')

# --- Carta: Limpiar asigna el folio del siguiente; Cargar asigna uno
# si el guardado viejo no tenía folio. ---
rep(HTML, '''  var fEl = document.getElementById('fCa-folio');
  if (fEl) fEl.value = '';
  cartaEditId = null;
  cartaEqFilas = [cartaEqFilaVacia()];
  cartaEqRender();
  cartaPrefillFecha();
}''',
'''  var fEl = document.getElementById('fCa-folio');
  if (fEl) fEl.value = '';
  cartaEditId = null;
  cartaEqFilas = [cartaEqFilaVacia()];
  cartaEqRender();
  cartaPrefillFecha();
  cartaAsignarFolio();
}''')
rep(HTML, '''  set('fCa-fecha', d.fecha || hoyISO());
  set('fCa-folio', c.folio || '');''',
'''  set('fCa-fecha', d.fecha || hoyISO());
  set('fCa-folio', c.folio || '');
  if (!c.folio) cartaAsignarFolio();''')

# --- Carta: Guardar usa el folio del formulario (ya asignado al
# abrir); la nube recibe el folio y lo guarda tal cual. ---
rep(HTML, '''async function cartaGuardar() {
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
  }''',
'''async function cartaGuardar() {
  var d = cartaLeerForm();
  if (!cartaValidar(d)) { showToast('Faltan datos obligatorios: nombre del colaborador y al menos un equipo con modelo o número de serie.'); return false; }
  // (268) El folio ya viene del formulario (asignado al abrir); si
  // está vacío se asigna ahora como respaldo, nunca al revés.
  var folioEl = document.getElementById('fCa-folio');
  var folio = (folioEl && folioEl.value) || '';
  if (!folio) folio = await cartaAsignarFolio();
  var c = null;
  if (cartaEditId) cartas.forEach(function (x) { if (x.id === cartaEditId) c = x; });
  if (!c) {
    if (CLOUD_ENABLED && cloudUser && window.Cloud && window.Cloud.crearCarta) {
      try {
        var created = await window.Cloud.crearCarta(d, technicianName(), folio);
        c = { id: created.id, folio: created.folio, creadoEn: Date.now(), creadoPor: cloudUser.uid, creadoPorNombre: technicianName(), datos: d };
        cartas.push(c);
      } catch (e) { showToast('No se pudo guardar la carta en la nube. Revisa tu conexión.'); return false; }
    } else {
      c = { id: uid(), folio: folio, creadoEn: Date.now(), creadoPor: (cloudUser && cloudUser.uid) || '', creadoPorNombre: technicianName(), datos: d };
      cartas.push(c);
    }
  } else {
    c.datos = d;
    if (!c.folio && folio) c.folio = folio;
    if (CLOUD_ENABLED && cloudUser && window.Cloud && window.Cloud.upsertCarta) {
      try { await window.Cloud.upsertCarta(c); } catch (e) { showToast('No se pudo guardar la carta en la nube. Revisa tu conexión.'); return false; }
    }
  }''')

# --- Carta: PDF desde el formulario lleva el folio del campo. ---
rep(HTML, '''  var c = cartaEditId ? cartaFind(cartaEditId) : null;
  cartaCompartirPdf({ id: (c && c.id) || 'borrador', folio: (c && c.folio) || '', datos: d }, 'pdf');''',
'''  var c = cartaEditId ? cartaFind(cartaEditId) : null;
  var folioEl = document.getElementById('fCa-folio');
  cartaCompartirPdf({ id: (c && c.id) || 'borrador', folio: (c && c.folio) || (folioEl && folioEl.value) || '', datos: d }, 'pdf');''')

# --- PDF Acuse: folio arriba a la derecha, junto a la fecha. ---
rep(HTML, '''// logo 111x65 pt, caja del título 235x30 pt, línea naranja 2.5 pt.''',
'''// logo 111x65 pt, caja del título 235x30 pt, línea naranja 2.5 pt.
// (268) Folio arriba a la derecha, junto a la fecha (asignado al abrir
// el formulario; ver acuseAsignarFolio).''')
rep(HTML, '''  // Fecha arriba, a la derecha, en español largo.
  T(fmtFechaLarga(d.fecha), X1, 118, 'F1', 11, null, 'R');''',
'''  // Fecha arriba, a la derecha, en español largo.
  T(fmtFechaLarga(d.fecha), X1, 118, 'F1', 11, null, 'R');
  // (268) Folio arriba a la derecha, junto a la fecha.
  var folioAc = (a && a.folio) || (d && d.folio) || '';
  if (folioAc) T('FOLIO: ' + folioAc, X1, 136, 'F2', 11, null, 'R');''')

# --- PDF Carta: comentario (267) -> (268). ---
rep(HTML, '''// (267) PDF de la Carta Responsiva (2 páginas carta): p1 con el
// encabezado fijo del formato (logo Lapi como imagen — el mismo asset
// que el Acuse —, título y tabla Código FO-SI-10, Versión 3, Fecha de
// actualización 25-sep-23, Página 1 de 2, con bordes y negritas),
// Datos del solicitante (con Área), tabla Exclusivo de Sistemas con
// encabezado VERDE #9BBB59 y Nombre y firma del usuario; p2 con las
// responsabilidades verbatim y la firma final.''',
'''// (268) PDF de la Carta Responsiva (2 páginas carta): p1 con el
// encabezado fijo del formato (logo Lapi como imagen — el mismo asset
// que el Acuse —, título y tabla Código FO-SI-10, Versión 3, Fecha de
// actualización 25-sep-23, Página 1 de 2, con bordes y negritas),
// Seguridad/Fecha/FOLIO en una línea, DATOS DEL SOLICITANTE con cada
// campo en su CELDA CON BORDE como el original (izq.: Nombre, Número,
// Sucursal, Puesto; der.: Ip de Red y «Área: Jefe Directo:»;
// Observaciones en caja larga), tabla Exclusivo de Sistemas con
// encabezado VERDE #9BBB59 y divisores verticales, y Nombre y firma
// del usuario; p2 con las responsabilidades verbatim y la firma final.
// El folio ya viene asignado al abrir el formulario (no al guardar).''')

# --- PDF Carta: Seguridad/Fecha/FOLIO en UNA línea (como el original). ---
rep(HTML, '''  // Seguridad de la Información + fecha de solicitud + folio.
  need(32);
  y0 = yt;
  T('Seguridad de la Información', 36, y0, 'F2', 10);
  T('Fecha de solicitud: ' + fmtFechaLarga(d.fecha), 36, y0 + 14, 'F1', 9);
  T('FOLIO: ' + (c.folio || '-'), 420, y0 + 14, 'F2', 10);
  yt += 32 + 6;''',
'''  // Seguridad de la Información + fecha de solicitud + folio (268):
  // en UNA línea como el original (izquierda / centro / derecha).
  need(14);
  y0 = yt;
  T('Seguridad de la Información', 36, y0, 'F2', 10);
  T('Fecha de solicitud: ' + fmtFechaLarga(d.fecha), 315, y0, 'F1', 9, null, 'C');
  T('FOLIO: ' + (c.folio || '-'), 460, y0, 'F2', 10);
  yt += 14 + 8;''')

# --- PDF Carta: quitar el helper campo() (ya no se usa). ---
span_replace(HTML, '''  function campo(label, value, x, ytop, w) {''',
'''  // --- Página 1: encabezado fijo del formato.''', '')

# --- PDF Carta: DATOS DEL SOLICITANTE con cajas con borde. ---
span_replace(HTML, '''  // Datos del solicitante.
''',
'''  // Exclusivo de Sistemas: tabla de equipos.
''',
'''  // Datos del solicitante (268): como el formato original FO-SI-10 —
  // cada campo en su CELDA CON BORDE VISIBLE. Columna izquierda (4
  // cajas apiladas): Nombre, Número, Sucursal, Puesto; columna derecha:
  // Ip de Red (ocupa las 2 primeras filas) y «Área: Jefe Directo:»
  // (última fila; un solo campo del original que junta los dos valores
  // del formulario, Área y Jefe Directo). Observaciones como caja larga
  // de ancho completo con borde. Medidas de la captura del original:
  // etiquetas en negrita a la derecha de su caja, cajas izq. x=146
  // w=184, der. x=410 w=166, filas de 22 pt.
  need(16 + 88 + 4 + 12 + 22 + 6);
  T('DATOS DEL SOLICITANTE', 306, yt, 'F2', 10, null, 'C');
  yt += 16;
  var DAT_Y = yt;
  var DAT_RH = 22;
  function cajaCampo(etiqueta, valor, etiqDer, cajaX, cajaY, cajaW, cajaH) {
    // Etiqueta en negrita, alineada a la derecha, pegada a su caja.
    T(etiqueta, etiqDer, cajaY + (cajaH - 11) / 2 + 1, 'F2', 9, null, 'R');
    R(cajaX, cajaY, cajaW, cajaH, null);
    var lines = wrapLines(val(valor), cajaW - 10, 9).slice(0, 2);
    var yTxt = cajaY + (cajaH - lines.length * 11) / 2 + 1;
    if (yTxt < cajaY + 1) yTxt = cajaY + 1;
    lines.forEach(function (ln, i) { T(ln, cajaX + 5, yTxt + i * 11, 'F1', 9); });
  }
  cajaCampo('Nombre del colaborador:', d.nombre, 140, 146, DAT_Y, 184, DAT_RH);
  cajaCampo('Número de colaborador:', d.colaborador, 140, 146, DAT_Y + DAT_RH, 184, DAT_RH);
  cajaCampo('Sucursal:', d.sucursal, 140, 146, DAT_Y + 2 * DAT_RH, 184, DAT_RH);
  cajaCampo('Puesto:', d.puesto, 140, 146, DAT_Y + 3 * DAT_RH, 184, DAT_RH);
  cajaCampo('Ip de Red:', d.ip, 404, 410, DAT_Y, 166, 2 * DAT_RH);
  var jefeVal = [d.area, d.jefe].filter(function (s) { return s; }).join(' — ');
  cajaCampo('Área: Jefe Directo:', jefeVal, 404, 410, DAT_Y + 3 * DAT_RH, 166, DAT_RH);
  yt = DAT_Y + 4 * DAT_RH + 4;
  // Observaciones: etiqueta arriba, caja larga de ancho completo.
  T('Observaciones:', 82, yt, 'F2', 9);
  R(36, yt + 12, 540, 22, null);
  var obsLines = wrapLines(val(d.observaciones), 530, 9).slice(0, 2);
  obsLines.forEach(function (ln, i) { T(ln, 41, yt + 12 + 6 + i * 11, 'F1', 9); });
  yt += 12 + 22 + 6;
''')

# --- PDF Carta: título Exclusivo centrado + divisores verticales. ---
rep(HTML, """  T('Exclusivo de Sistemas', 36, yt, 'F2', 10);""",
    """  T('Exclusivo de Sistemas', 306, yt, 'F2', 10, null, 'C');""")
rep(HTML, '''  R(36, y0, 540, 16, [0.608, 0.733, 0.349]);
  cols.forEach(function (cc) { T(cc[0], cc[1] + 4, y0 + 3, 'F2', 8); });''',
'''  R(36, y0, 540, 16, [0.608, 0.733, 0.349]);
  // (268) Divisores verticales entre columnas, como el original
  // (el docx tiene insideV en esta tabla).
  LN(153, y0, 153, y0 + 16);
  LN(270, y0, 270, y0 + 16);
  LN(423, y0, 423, y0 + 16);
  cols.forEach(function (cc) { T(cc[0], cc[1] + 4, y0 + 3, 'F2', 8); });''')
rep(HTML, '''    R(36, y0, 540, 16, null);
    T(String(eq.modelo || '-').slice(0, 24), 40, y0 + 3, 'F1', 8);''',
'''    R(36, y0, 540, 16, null);
    LN(153, y0, 153, y0 + 16);
    LN(270, y0, 270, y0 + 16);
    LN(423, y0, 423, y0 + 16);
    T(String(eq.modelo || '-').slice(0, 24), 40, y0 + 3, 'F1', 8);''')

# ================= firebase.js =================
# --- crearAcuse con folio (2.5.18): recibe el folio asignado al abrir;
# si no viene, lo asigna con la transacción (como antes lo hacía
# crearCarta). El documento ahora lleva folio de 5 dígitos. ---
rep(FB, '''// Acuses de Sistemas (2.5.16): acuse de recibido de documentos, sin
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
}''',
'''// Acuses de Sistemas (2.5.16; folio desde 2.5.18): acuse de recibido
// de documentos, con folio de 5 dígitos asignado AL ABRIR el
// formulario (la app lo pasa ya asignado; si no viene, crearAcuse lo
// asigna con asignarFolioAcuse). Sin página pública. El documento
// lleva creadoPor, creadoPorNombre, creadoEn, folio y datos {fecha,
// para, de, anexo}. uidOpcional filtra por creadoPor (lo usan los
// usuarios normales para que las reglas permitan la lectura); sin él
// el admin suscribe todo.
async function crearAcuse(datos, creadoPorNombre, folio) {
  const u = auth.currentUser;
  if (!u) throw new Error('no-auth');
  const f = folio || (await asignarFolioAcuse());
  const ref = doc(collection(db, 'acuses'));
  await setDoc(ref, {
    creadoPor: u.uid,
    creadoPorNombre: creadoPorNombre || u.email || '',
    creadoEn: Date.now(),
    folio: f,
    datos: datos || {}
  });
  return ref.id;
}''')

# --- asignarFolioAcuse() espejo de asignarFolioCarta(). ---
rep(FB, '''async function asignarFolioCarta() {
  const ref = doc(db, 'config', 'foliosCarta');
  return runTransaction(db, async (tx) => {
    const snap = await tx.get(ref);
    const n = (snap.exists() && typeof snap.data().siguiente === 'number') ? snap.data().siguiente : 1;
    tx.set(ref, { siguiente: n + 1 });
    return String(n).padStart(5, '0');
  });
}''',
'''async function asignarFolioCarta() {
  const ref = doc(db, 'config', 'foliosCarta');
  return runTransaction(db, async (tx) => {
    const snap = await tx.get(ref);
    const n = (snap.exists() && typeof snap.data().siguiente === 'number') ? snap.data().siguiente : 1;
    tx.set(ref, { siguiente: n + 1 });
    return String(n).padStart(5, '0');
  });
}

// Folio del acuse de Sistemas (2.5.18): config/foliosAcuse.siguiente
// empieza en 1; la transacción lee, asigna el folio con 5 dígitos y
// sube el contador, así dos teléfonos no repiten folio. Secuencia
// INDEPENDIENTE de la de cartas (config/foliosCarta). Espejo de
// asignarFolioCarta().
async function asignarFolioAcuse() {
  const ref = doc(db, 'config', 'foliosAcuse');
  return runTransaction(db, async (tx) => {
    const snap = await tx.get(ref);
    const n = (snap.exists() && typeof snap.data().siguiente === 'number') ? snap.data().siguiente : 1;
    tx.set(ref, { siguiente: n + 1 });
    return String(n).padStart(5, '0');
  });
}''')

# --- crearCarta con folio ya asignado al abrir. ---
rep(FB, '''// Cartas Responsivas FO-SI-10 (2.5.16): resguardo y uso de equipo de
// cómputo. El folio se asigna al guardar (crearCarta lo pide con
// asignarFolioCarta); el documento lleva creadoPor, creadoPorNombre,
// creadoEn, folio y datos {fecha, nombre, colaborador, sucursal,
// puesto, jefe, ip, observaciones, equipos: [{modelo, marca, serie,
// concepto}]}. Sin página pública: solo el técnico y el admin.
async function crearCarta(datos, creadoPorNombre) {
  const u = auth.currentUser;
  if (!u) throw new Error('no-auth');
  const folio = await asignarFolioCarta();''',
'''// Cartas Responsivas FO-SI-10 (2.5.16; folio al abrir desde 2.5.18):
// resguardo y uso de equipo de cómputo. El folio se asigna AL ABRIR
// el formulario (la app lo pasa ya asignado; si no viene, crearCarta
// lo pide con asignarFolioCarta como antes); el documento lleva
// creadoPor, creadoPorNombre, creadoEn, folio y datos {fecha, nombre,
// colaborador, sucursal, puesto, jefe, ip, observaciones, equipos:
// [{modelo, marca, serie, concepto}]}. Sin página pública: solo el
// técnico y el admin.
async function crearCarta(datos, creadoPorNombre, folio) {
  const u = auth.currentUser;
  if (!u) throw new Error('no-auth');
  const f = folio || (await asignarFolioCarta());''')
rep(FB, '''  const ref = doc(collection(db, 'cartas'));
  await setDoc(ref, {
    creadoPor: u.uid,
    creadoPorNombre: creadoPorNombre || u.email || '',
    creadoEn: Date.now(),
    folio: folio,
    datos: datos || {}
  });
  return { id: ref.id, folio: folio };''',
'''  const ref = doc(collection(db, 'cartas'));
  await setDoc(ref, {
    creadoPor: u.uid,
    creadoPorNombre: creadoPorNombre || u.email || '',
    creadoEn: Date.now(),
    folio: f,
    datos: datos || {}
  });
  return { id: ref.id, folio: f };''')

# --- Exportar asignarFolioAcuse. ---
rep(FB, '''  asignarFolioCarta,
  crearCarta,''',
'''  asignarFolioCarta,
  asignarFolioAcuse,
  crearCarta,''')

# ================= firestore.rules =================
# --- Regla del contador nuevo config/foliosAcuse (espejo de
# foliosCarta). El archivo sigue incluyendo TODO (acuses, cartas y
# ambos contadores): Gerardo aún no pega las reglas en la consola. ---
rep(RULES, '''    // Folios de cartas responsivas (2.5.16): config/foliosCarta.siguiente
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
    }''',
'''    // Folios de cartas responsivas (2.5.16): config/foliosCarta.siguiente
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
    }

    // Folios de acuses de Sistemas (2.5.18): config/foliosAcuse.siguiente
    // es el próximo folio a asignar (empieza en 1). Espejo de
    // config/foliosCarta: leer activos; crear con siguiente entero;
    // actualizar solo subir el contador de uno en uno.
    match /config/foliosAcuse {
      allow read: if isActive();
      allow create: if isActive() && request.resource.data.siguiente is int;
      allow update: if isActive()
        && request.resource.data.diff(resource.data).changedKeys().hasOnly(['siguiente'])
        && request.resource.data.siguiente == resource.data.siguiente + 1;
      allow delete: if false;
    }''')

# ================= docs/DATA_MODEL.md =================
rep(DATAMODEL, '''Las reglas solo permiten subirlo de uno en uno y solo cambiar ese
campo.''',
'''Las reglas solo permiten subirlo de uno en uno y solo cambiar ese
campo.

## `config/foliosCarta` y `config/foliosAcuse` — contadores de folios de Carta y Acuse (2.5.18)

| Campo | Tipo / valor |
|---|---|
| `siguiente` | int. Próximo folio a asignar; empieza en 1. La transacción `asignarFolioCarta()` / `asignarFolioAcuse()` lo lee, devuelve el folio con 5 dígitos y lo sube en 1. |

Son secuencias INDEPENDIENTES: el folio de la Carta y el del Acuse
no se mezclan. El folio se asigna AL ABRIR el formulario (no al
guardar); si se abandona sin guardar, queda consumido (hueco en la
numeración). Los documentos `acuses/{id}` y `cartas/{id}` llevan el
folio en el campo `folio` (string de 5 dígitos). Las reglas son
espejo de `config/folios`: solo subir de uno en uno y solo ese campo.

⚠️ Las reglas de `acuses`, `cartas`, `config/foliosCarta` y
`config/foliosAcuse` (desde 2.5.16) siguen sin publicarse: Gerardo
las pega en la consola de Firebase antes de que el guardado en la
nube funcione.''')

print('patch 2.5.18 aplicado: www/index.html, www/cloud/firebase.js, firestore.rules, gradle, pbx, DATA_MODEL.md')
