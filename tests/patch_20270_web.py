# Parche web 2.5.20: P1 duplicado en Cartas/Acuses guardados, P2 Acuse SIN
# folio (corrección: el formato original del Acuse no lleva folio; la
# Carta SÍ lo conserva), P3 botón Imprimir en Carta y Acuse.
# Uso: python3 patch_20270_web.py (corre desde tests/)
import os

BASE = '/home/hatch/workspace/android/checklist-cloud'
P = os.path.join(BASE, 'www/index.html')
FB = os.path.join(BASE, 'www/cloud/firebase.js')
s = open(P, encoding='utf-8').read()
fb = open(FB, encoding='utf-8').read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'NO ENCONTRADO x%d (esperado %d): %r' % (c, n, old[:140])
    s = s.replace(old, new)


def repfb(old, new, n=1):
    global fb
    c = fb.count(old)
    assert c == n, 'FB NO ENCONTRADO x%d (esperado %d): %r' % (c, n, old[:140])
    fb = fb.replace(old, new)


# --- Versión 2.5.19 -> 2.5.20 (2 sitios) y Serie 269 -> 270 (mailto).
rep('Versión 2.5.19', 'Versión 2.5.20')
rep('Versión: 2.5.19', 'Versión: 2.5.20')
rep("Checklist de Soporte 269')", "Checklist de Soporte 270')")
rep('Versión de la app: 269', 'Versión de la app: 270')

# --- P2: formulario del Acuse SIN campo de folio; botón Imprimir.
rep('      <div class="field"><label>Folio</label><input id="fAc-folio" readonly placeholder="Se asigna al abrir"></div>\n',
    '')
rep('''        <button class="btn-green" id="btnAcuseGuardar">💾 Guardar acuse</button>
        <button class="btn-dark" id="btnAcusePdf">📄 Generar PDF</button>''',
    '''        <button class="btn-green" id="btnAcuseGuardar">💾 Guardar acuse</button>
        <button class="btn-dark" id="btnAcusePdf">📄 Generar PDF</button>
        <button class="btn-dark" id="btnAcuseImprimir">🖨️ Imprimir</button>''')
# --- P3: botón Imprimir en el formulario de la Carta.
rep('''        <button class="btn-green" id="btnCartaGuardar">💾 Guardar carta</button>
        <button class="btn-dark" id="btnCartaPdf">📄 Generar PDF</button>''',
    '''        <button class="btn-green" id="btnCartaGuardar">💾 Guardar carta</button>
        <button class="btn-dark" id="btnCartaPdf">📄 Generar PDF</button>
        <button class="btn-dark" id="btnCartaImprimir">🖨️ Imprimir</button>''')

# --- P2: PDF del Acuse SIN la línea FOLIO (2.5.18 la agregó; el
# formato original no la lleva). El PDF ignora el folio aunque un
# documento viejo lo traiga.
rep('''// (268) Folio arriba a la derecha, junto a la fecha (asignado al abrir
// el formulario; ver acuseAsignarFolio).''',
    '''// (270) El Acuse NO lleva folio: el formato original no lo tiene
// y Gerardo lo confirmó (2.5.18 lo agregó por error). Ni el PDF, ni
// el texto para compartir, ni la tarjeta, ni el formulario lo llevan;
// tampoco se asigna ni se consume folio al abrir el Acuse.''')
rep('''  // (268) Folio arriba a la derecha, junto a la fecha.
  var folioAc = (a && a.folio) || (d && d.folio) || '';
  if (folioAc) T('FOLIO: ' + folioAc, X1, 136, 'F2', 11, null, 'R');
''', '')

# --- P3: imprimirPdfDoc (después de compartirPdfDoc, antes de la firma).
rep('''// Firma del técnico: canvas con dedo o ratón.''',
    '''// (270) Imprimir el PDF generado (Carta y Acuse): se abre el PDF en
// un iframe oculto y se llama a print() en su ventana, lo que abre el
// diálogo de impresión del sistema (WebView del teléfono y Electron
// de escritorio). Si el iframe no puede imprimir, se usa window.print
// como respaldo. La impresión en una impresora física real sigue
// pendiente de prueba por Gerardo.
function imprimirPdfDoc(out) {
  try {
    var url = URL.createObjectURL(out.blob);
    var fr = document.createElement('iframe');
    fr.style.position = 'fixed'; fr.style.right = '0'; fr.style.bottom = '0';
    fr.style.width = '0'; fr.style.height = '0'; fr.style.border = '0';
    fr.src = url;
    fr.onload = function () {
      try {
        if (fr.contentWindow) { fr.contentWindow.focus(); fr.contentWindow.print(); }
        else { window.print(); }
      } catch (e) { try { window.print(); } catch (e2) {} }
      setTimeout(function () {
        try { URL.revokeObjectURL(url); } catch (e) {}
        if (fr.parentNode && fr.parentNode.removeChild) fr.parentNode.removeChild(fr);
      }, 1000);
    };
    document.body.appendChild(fr);
    return true;
  } catch (e) {
    try { window.print(); return true; }
    catch (e2) { showToast('No se pudo abrir la impresión.'); return false; }
  }
}
// Firma del técnico: canvas con dedo o ratón.''')

# --- Cabecera del bloque Acuse/Carta: Acuse sin folio, Carta con folio.
rep('''// El FOLIO se asigna AL ABRIR el formulario (nube: transacción
// asignarFolioAcuse / asignarFolioCarta; local: contador en
// localStorage; secuencias INDEPENDIENTES, config/foliosAcuse y
// config/foliosCarta). Si se abandona sin guardar, el folio queda
// consumido (hueco en la numeración, no se devuelve). Al guardar, el
// formulario queda con los datos y el folio para generar el PDF
// enseguida; Limpiar lo vacía y asigna el folio del siguiente.''',
    '''// El FOLIO de la CARTA se asigna AL ABRIR el formulario (nube:
// transacción asignarFolioCarta; local: contador en localStorage,
// config/foliosCarta). Si se abandona sin guardar, el folio queda
// consumido (hueco en la numeración, no se devuelve). Al guardar, el
// formulario queda con los datos y el folio para generar el PDF
// enseguida; Limpiar lo vacía y asigna el folio del siguiente.
// El ACUSE no lleva folio (270): ni formulario, ni PDF, ni tarjeta,
// ni textos; tampoco se asigna ni se consume folio al abrirlo.''')
rep("var ACUSE_FOLIO_LOCAL_KEY = 'checklist-soporte-folios-acuse-local-v1';\n", '')

# --- P1: deduplicación (UN documento = UNA entrada). merge* ya
# dedupaba por id SOLO si la copia local estaba en el array al llegar
# la suscripción; fallaba en 3 casos reales: (a) la suscripción llega
# entre el crearCarta/crearAcuse en la nube y el push local (el push
# incondicional metía la 2ª copia con el MISMO id); (b) doble toque en
# Guardar: dos crear* concurrentes -> dos ids distintos, mismo folio;
# (c) el crear* falla DESPUÉS de escribir en la nube y el respaldo
# local toma un id nuevo: el reintento con upsert crea el 2º documento
# con el mismo folio. Ahora: dedupe por id (gana la copia no
# pendiente) y por folio (Carta; en Acuse cubre documentos viejos con
# folio), aplicado en merge, al guardar, al cargar local y al
# renderizar; y guarda en curso que bloquea el doble toque.
rep('''// Al recibir la lista de la nube, conservar los guardados locales que
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
}''',
    '''// (270) UN documento = UNA entrada. Deduplica por id (si hay dos
// copias del mismo id gana la que ya NO está pendiente) y por folio
// (mismo folio = mismo documento aunque el id difiera: es el caso del
// respaldo local creado tras un crear* que falló después de escribir
// en la nube). Se aplica en merge, al guardar, al cargar local y al
// renderizar, así ningún camino deja ver el documento dos veces.
function dedupeDocs(arr, porFolio) {
  var chosen = {};
  var order = [];
  (arr || []).forEach(function (x) {
    if (!x || !x.id) return;
    if (!chosen[x.id]) { chosen[x.id] = x; order.push(x.id); }
    else if (chosen[x.id].pendienteSync && !x.pendienteSync) chosen[x.id] = x;
  });
  var out = [];
  var seenFolio = {};
  order.forEach(function (id) {
    var x = chosen[id];
    if (porFolio && x.folio && seenFolio[x.folio]) return;
    if (porFolio && x.folio) seenFolio[x.folio] = true;
    out.push(x);
  });
  return out;
}
function dedupeAcuses(arr) { return dedupeDocs(arr, true); }
function dedupeCartas(arr) { return dedupeDocs(arr, true); }
// Al recibir la lista de la nube, conservar los guardados locales que
// la nube aún no trae (igual que mergeMantWithLocal).
function mergeAcuseWithLocal(docs) {
  var byId = {};
  acuses.forEach(function (a) { byId[a.id] = a; });
  var out = (docs || []).slice();
  var ids = {};
  out.forEach(function (a) { ids[a.id] = true; });
  Object.keys(byId).forEach(function (id) { if (!ids[id]) out.push(byId[id]); });
  return dedupeAcuses(out);
}
function mergeCartaWithLocal(docs) {
  var byId = {};
  cartas.forEach(function (c) { byId[c.id] = c; });
  var out = (docs || []).slice();
  var ids = {};
  out.forEach(function (c) { ids[c.id] = true; });
  Object.keys(byId).forEach(function (id) { if (!ids[id]) out.push(byId[id]); });
  return dedupeCartas(out);
}''')
rep('''    if (raw) { var arr = JSON.parse(raw); if (Array.isArray(arr)) acuses = arr; }''',
    '''    if (raw) { var arr = JSON.parse(raw); if (Array.isArray(arr)) acuses = dedupeAcuses(arr); }''')
rep('''    if (raw) { var arr = JSON.parse(raw); if (Array.isArray(arr)) cartas = arr; }''',
    '''    if (raw) { var arr = JSON.parse(raw); if (Array.isArray(arr)) cartas = dedupeCartas(arr); }''')

# --- P2: acuseLimpiarForm sin folio ni asignación.
rep('''function acuseLimpiarForm() {
  ['fAc-folio', 'fAc-para', 'fAc-de', 'fAc-anexo'].forEach(function (id) {
    var el = document.getElementById(id);
    if (el) { el.value = ''; el.classList.remove('campo-falta'); }
  });
  acuseEditId = null;
  acusePrefillFecha();
  acuseAsignarFolio();
}''',
    '''function acuseLimpiarForm() {
  ['fAc-para', 'fAc-de', 'fAc-anexo'].forEach(function (id) {
    var el = document.getElementById(id);
    if (el) { el.value = ''; el.classList.remove('campo-falta'); }
  });
  acuseEditId = null;
  acusePrefillFecha();
}''')
# --- P2: acuseCargarEnForm sin folio.
rep('''  set('fAc-fecha', d.fecha || hoyISO());
  set('fAc-folio', a.folio || '');
  set('fAc-para', d.para);
  set('fAc-de', d.de);
  set('fAc-anexo', d.anexo);
  acuseEditId = a.id;
  if (!a.folio) acuseAsignarFolio();
}''',
    '''  set('fAc-fecha', d.fecha || hoyISO());
  set('fAc-para', d.para);
  set('fAc-de', d.de);
  set('fAc-anexo', d.anexo);
  acuseEditId = a.id;
}''')

# --- P1+P2: reescribir acuseGuardar completo (sin folio; guarda en
# curso; push con dedupe en vez de push incondicional).
old_acuse_guardar = s[s.index('async function acuseGuardar() {'):s.index('// (269) Reintento de sincronización del acuse')]
new_acuse_guardar = '''var acuseGuardando = false;
async function acuseGuardar() {
  // (270) Guarda en curso: un segundo toque en Guardar mientras el
  // primero sigue en la nube NO crea otro documento (era una de las
  // causas del duplicado).
  if (acuseGuardando) return false;
  acuseGuardando = true;
  try {
  var d = acuseLeerForm();
  if (!acuseValidar(d)) { showToast('Faltan datos obligatorios: Para y De.'); return false; }
  var a = null;
  if (acuseEditId) acuses.forEach(function (x) { if (x.id === acuseEditId) a = x; });
  if (!a) {
    if (CLOUD_ENABLED && cloudUser && window.Cloud && window.Cloud.crearAcuse) {
      try {
        var newId = await window.Cloud.crearAcuse(d, technicianName());
        a = { id: newId, creadoEn: Date.now(), creadoPor: cloudUser.uid, creadoPorNombre: technicianName(), datos: d };
        // (270) Dedupe, no push: la suscripción puede haber metido ya
        // este mismo id mientras se esperaba a la nube.
        acuses = dedupeAcuses(acuses.concat([a]));
      } catch (e) {
        // (269) La nube falló: el acuse queda guardado EN EL TELÉFONO
        // (marcado pendiente de sincronizar) para que nada se pierda;
        // se reintenta solo al abrir la vista o al volver la red, o
        // con el botón «Reintentar» de la tarjeta.
        a = { id: uid(), creadoEn: Date.now(), creadoPor: cloudUser.uid, creadoPorNombre: technicianName(), datos: d, pendienteSync: true };
        acuses = dedupeAcuses(acuses.concat([a]));
        saveAcuseLocal();
        acuseEditId = a.id;
        renderAcuseList();
        showToast(mensajeErrorNube(e, 'el acuse'));
        return true;
      }
    } else {
      a = { id: uid(), creadoEn: Date.now(), creadoPor: (cloudUser && cloudUser.uid) || '', creadoPorNombre: technicianName(), datos: d };
      acuses = dedupeAcuses(acuses.concat([a]));
    }
  } else {
    a.datos = d;
    if (CLOUD_ENABLED && cloudUser && window.Cloud && window.Cloud.upsertAcuse) {
      try { await window.Cloud.upsertAcuse(acuseDocNube(a)); a.pendienteSync = false; }
      catch (e) { a.pendienteSync = true; saveAcuseLocal(); renderAcuseList(); showToast(mensajeErrorNube(e, 'el acuse')); acuseEditId = a.id; return true; }
    }
  }
  saveAcuseLocal();
  acuseEditId = a.id;
  renderAcuseList();
  showToast('Acuse guardado.');
  return true;
  } finally { acuseGuardando = false; }
}
'''
assert old_acuse_guardar.startswith('async function acuseGuardar() {')
s = s.replace(old_acuse_guardar, new_acuse_guardar)

# --- P2: toast de reintento del acuse sin folio.
rep("    showToast('Acuse con folio ' + (a.folio || '—') + ' sincronizado.');",
    "    showToast('Acuse sincronizado.');")
# --- P2+P3: tarjeta del Acuse: título sin folio + botón Imprimir.
rep('''  var html = '<div class="card"><b>Acuse · Folio ' + esc(a.folio || '—') + ' · ' + esc(fmtFechaLarga(d.fecha)) + '</b>' +''',
    '''  var html = '<div class="card"><b>Acuse · ' + esc(fmtFechaLarga(d.fecha)) + '</b>' +''')
rep('''  html += '<div class="actions"><button class="btn-green" data-acuse-open="' + esc(a.id) + '">📝 Abrir</button>' +
    '<button class="btn-dark" data-acuse-pdf="' + esc(a.id) + '">📄 PDF</button>' +
    '<button class="btn-green" data-acuse-wa="' + esc(a.id) + '">📲 PDF por WhatsApp</button>' +
    '<button class="btn-dark" data-acuse-mail="' + esc(a.id) + '">✉️ PDF por correo</button>';''',
    '''  html += '<div class="actions"><button class="btn-green" data-acuse-open="' + esc(a.id) + '">📝 Abrir</button>' +
    '<button class="btn-dark" data-acuse-pdf="' + esc(a.id) + '">📄 PDF</button>' +
    '<button class="btn-dark" data-acuse-print="' + esc(a.id) + '">🖨️ Imprimir</button>' +
    '<button class="btn-green" data-acuse-wa="' + esc(a.id) + '">📲 PDF por WhatsApp</button>' +
    '<button class="btn-dark" data-acuse-mail="' + esc(a.id) + '">✉️ PDF por correo</button>';''')
# --- P1: renderAcuseList con dedupe.
rep('''  var list = acuses.slice().sort(function (x, y) { return (y.creadoEn || 0) - (x.creadoEn || 0); });
  box.innerHTML = list.map(acuseCardHtml).join('');''',
    '''  var list = dedupeAcuses(acuses).sort(function (x, y) { return (y.creadoEn || 0) - (x.creadoEn || 0); });
  box.innerHTML = list.map(acuseCardHtml).join('');''')
# --- P2: texto para compartir del Acuse sin folio.
rep("""  return 'Acuse Sistemas — Checklist de Soporte. Folio ' + (a.folio || '—') + '. Para: ' + (d.para || '—') + ', De: ' + (d.de || '—') + (d.anexo ? ', Anexo: ' + d.anexo : '') + '.';""",
    """  return 'Acuse Sistemas — Checklist de Soporte. Para: ' + (d.para || '—') + ', De: ' + (d.de || '—') + (d.anexo ? ', Anexo: ' + d.anexo : '') + '.';""")
# --- P2+P3: PDF desde el formulario del Acuse (sin folio) + imprimir.
rep('''function acusePdfDesdeForm() {
  var d = acuseLeerForm();
  if (!acuseValidar(d)) { showToast('Faltan datos obligatorios: Para y De.'); return; }
  var a = acuseEditId ? acuseFind(acuseEditId) : null;
  var folioEl = document.getElementById('fAc-folio');
  acuseCompartirPdf({ id: (a && a.id) || 'borrador', folio: (a && a.folio) || (folioEl && folioEl.value) || '', datos: d }, 'pdf');
}''',
    '''function acusePdfDesdeForm() {
  var d = acuseLeerForm();
  if (!acuseValidar(d)) { showToast('Faltan datos obligatorios: Para y De.'); return; }
  var a = acuseEditId ? acuseFind(acuseEditId) : null;
  acuseCompartirPdf({ id: (a && a.id) || 'borrador', datos: d }, 'pdf');
}
// (270) Imprimir el Acuse desde el formulario (con los datos en
// pantalla, guardado o no) o desde su tarjeta guardada.
function acuseImprimir(a) { imprimirPdfDoc(acusePdfBlob(a)); }
function acuseImprimirDesdeForm() {
  var d = acuseLeerForm();
  if (!acuseValidar(d)) { showToast('Faltan datos obligatorios: Para y De.'); return; }
  var a = acuseEditId ? acuseFind(acuseEditId) : null;
  acuseImprimir({ id: (a && a.id) || 'borrador', datos: d });
}''')
# --- P3: clic en Imprimir de la tarjeta del Acuse.
rep("  var id = q('data-acuse-open') || q('data-acuse-pdf') || q('data-acuse-wa') || q('data-acuse-mail') || q('data-acuse-retry') || q('data-acuse-del');",
    "  var id = q('data-acuse-open') || q('data-acuse-pdf') || q('data-acuse-print') || q('data-acuse-wa') || q('data-acuse-mail') || q('data-acuse-retry') || q('data-acuse-del');")
rep("  if (t.closest('[data-acuse-pdf]')) { acuseCompartirPdf(a, 'pdf'); return; }",
    "  if (t.closest('[data-acuse-pdf]')) { acuseCompartirPdf(a, 'pdf'); return; }\n  if (t.closest('[data-acuse-print]')) { acuseImprimir(a); return; }")

# --- P2: borrar acuseFolioLocal + acuseAsignarFolio (el Acuse ya no
# asigna folio; la Carta conserva cartaAsignarFolio/cartaFolioLocal).
old_folio_acuse = s[s.index('// Folio local del Acuse (sin nube)'):s.index('function cartaLimpiarForm()')]
assert 'acuseAsignarFolio' in old_folio_acuse and 'cartaAsignarFolio' in old_folio_acuse
s = s.replace(old_folio_acuse, '''// (268) Folio AL ABRIR el formulario de la CARTA: si el campo está
// vacío se asigna uno y se muestra. Nube: transacción
// (asignarFolioCarta); sin nube, o si la transacción falla: contador
// local. Si se abandona el formulario sin guardar, el folio queda
// consumido (hueco en la numeración): es lo normal en folios, no se
// devuelve. No reasigna si el campo ya tiene folio (p. ej. al volver
// a la vista con el formulario a medias o con un guardado cargado).
// (270) El Acuse YA NO tiene estas funciones: no lleva folio.
// La Carta conserva su asignación al abrir:
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
}
''')

# --- P1+P3: cartaGuardar con guarda en curso y dedupe en el push.
old_carta_guardar = s[s.index('async function cartaGuardar() {'):s.index('// (269) Reintento de sincronización de la carta')]
new_carta_guardar = '''var cartaGuardando = false;
async function cartaGuardar() {
  // (270) Guarda en curso: un segundo toque en Guardar mientras el
  // primero sigue en la nube NO crea otro documento (era una de las
  // causas del duplicado en «Cartas guardadas»).
  if (cartaGuardando) return false;
  cartaGuardando = true;
  try {
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
        // (270) Dedupe, no push: la suscripción puede haber metido ya
        // este mismo id (o el mismo folio con otro id) mientras se
        // esperaba a la nube.
        cartas = dedupeCartas(cartas.concat([c]));
      } catch (e) {
        // (269) La nube falló: la carta queda guardada EN EL TELÉFONO
        // (mismo folio, marcada pendiente de sincronizar) para que
        // nada se pierda; se reintenta solo al abrir la vista o al
        // volver la red, o con el botón «Reintentar» de la tarjeta.
        c = { id: uid(), folio: folio, creadoEn: Date.now(), creadoPor: cloudUser.uid, creadoPorNombre: technicianName(), datos: d, pendienteSync: true };
        cartas = dedupeCartas(cartas.concat([c]));
        saveCartaLocal();
        cartaEditId = c.id;
        renderCartaList();
        showToast(mensajeErrorNube(e, 'la carta'));
        return true;
      }
    } else {
      c = { id: uid(), folio: folio, creadoEn: Date.now(), creadoPor: (cloudUser && cloudUser.uid) || '', creadoPorNombre: technicianName(), datos: d };
      cartas = dedupeCartas(cartas.concat([c]));
    }
  } else {
    c.datos = d;
    if (!c.folio && folio) c.folio = folio;
    if (CLOUD_ENABLED && cloudUser && window.Cloud && window.Cloud.upsertCarta) {
      try { await window.Cloud.upsertCarta(cartaDocNube(c)); c.pendienteSync = false; }
      catch (e) { c.pendienteSync = true; saveCartaLocal(); renderCartaList(); showToast(mensajeErrorNube(e, 'la carta')); cartaEditId = c.id; return true; }
    }
  }
  var fEl = document.getElementById('fCa-folio');
  if (fEl) fEl.value = c.folio || '';
  saveCartaLocal();
  cartaEditId = c.id;
  renderCartaList();
  showToast('Carta guardada con folio ' + (c.folio || '—') + '.');
  return true;
  } finally { cartaGuardando = false; }
}
'''
assert old_carta_guardar.startswith('async function cartaGuardar() {')
s = s.replace(old_carta_guardar, new_carta_guardar)

# --- P3: tarjeta de la Carta con botón Imprimir.
rep('''    '<div class="actions"><button class="btn-green" data-carta-open="' + esc(c.id) + '">📝 Abrir</button>' +
    '<button class="btn-dark" data-carta-pdf="' + esc(c.id) + '">📄 PDF</button>' +
    '<button class="btn-green" data-carta-wa="' + esc(c.id) + '">📲 PDF por WhatsApp</button>' +
    '<button class="btn-dark" data-carta-mail="' + esc(c.id) + '">✉️ PDF por correo</button>';''',
    '''    '<div class="actions"><button class="btn-green" data-carta-open="' + esc(c.id) + '">📝 Abrir</button>' +
    '<button class="btn-dark" data-carta-pdf="' + esc(c.id) + '">📄 PDF</button>' +
    '<button class="btn-dark" data-carta-print="' + esc(c.id) + '">🖨️ Imprimir</button>' +
    '<button class="btn-green" data-carta-wa="' + esc(c.id) + '">📲 PDF por WhatsApp</button>' +
    '<button class="btn-dark" data-carta-mail="' + esc(c.id) + '">✉️ PDF por correo</button>';''')
# --- P1: renderCartaList con dedupe.
rep('''  var list = cartas.slice().sort(function (x, y) { return (y.creadoEn || 0) - (x.creadoEn || 0); });
  box.innerHTML = list.map(cartaCardHtml).join('');''',
    '''  var list = dedupeCartas(cartas).sort(function (x, y) { return (y.creadoEn || 0) - (x.creadoEn || 0); });
  box.innerHTML = list.map(cartaCardHtml).join('');''')
# --- P3: imprimir la Carta desde el formulario o su tarjeta.
rep('''async function cartaCompartirPdf(c, via) {
  var out = cartaPdfBlob(c);
  await compartirPdfDoc(out, cartaTexto(c), via, 'Carta Responsiva' + (c.folio ? ' folio ' + c.folio : '') + ' — Checklist de Soporte');
}''',
    '''async function cartaCompartirPdf(c, via) {
  var out = cartaPdfBlob(c);
  await compartirPdfDoc(out, cartaTexto(c), via, 'Carta Responsiva' + (c.folio ? ' folio ' + c.folio : '') + ' — Checklist de Soporte');
}
// (270) Imprimir la Carta desde el formulario (con el folio en
// pantalla) o desde su tarjeta guardada.
function cartaImprimir(c) { imprimirPdfDoc(cartaPdfBlob(c)); }
function cartaImprimirDesdeForm() {
  var d = cartaLeerForm();
  if (!cartaValidar(d)) { showToast('Faltan datos obligatorios: nombre del colaborador y al menos un equipo con modelo o número de serie.'); return; }
  var c = cartaEditId ? cartaFind(cartaEditId) : null;
  var folioEl = document.getElementById('fCa-folio');
  cartaImprimir({ id: (c && c.id) || 'borrador', folio: (c && c.folio) || (folioEl && folioEl.value) || '', datos: d });
}''')
rep("  var id = q('data-carta-open') || q('data-carta-pdf') || q('data-carta-wa') || q('data-carta-mail') || q('data-carta-retry') || q('data-carta-del');",
    "  var id = q('data-carta-open') || q('data-carta-pdf') || q('data-carta-print') || q('data-carta-wa') || q('data-carta-mail') || q('data-carta-retry') || q('data-carta-del');")
rep("  if (t.closest('[data-carta-pdf]')) { cartaCompartirPdf(c, 'pdf'); return; }",
    "  if (t.closest('[data-carta-pdf]')) { cartaCompartirPdf(c, 'pdf'); return; }\n  if (t.closest('[data-carta-print]')) { cartaImprimir(c); return; }")
# --- Listeners de los botones Imprimir del formulario.
rep("document.getElementById('btnAcusePdf').addEventListener('click', function () { acusePdfDesdeForm(); });",
    "document.getElementById('btnAcusePdf').addEventListener('click', function () { acusePdfDesdeForm(); });\ndocument.getElementById('btnAcuseImprimir').addEventListener('click', function () { acuseImprimirDesdeForm(); });")
rep("document.getElementById('btnCartaPdf').addEventListener('click', function () { cartaPdfDesdeForm(); });",
    "document.getElementById('btnCartaPdf').addEventListener('click', function () { cartaPdfDesdeForm(); });\ndocument.getElementById('btnCartaImprimir').addEventListener('click', function () { cartaImprimirDesdeForm(); });")
# --- P2: showVista('acuse') ya no asigna folio al abrir.
rep("  if (v === 'acuse') { acusePrefillFecha(); acuseAsignarFolio(); renderAcuseList(); acuseSuscribir(); acuseReintentarPendientes(); }",
    "  if (v === 'acuse') { acusePrefillFecha(); renderAcuseList(); acuseSuscribir(); acuseReintentarPendientes(); }")

# --- Verificación final: no queda ninguna referencia al folio del Acuse.
for bad in ['fAc-folio', 'acuseAsignarFolio', 'acuseFolioLocal', 'ACUSE_FOLIO_LOCAL_KEY',
            'FOLIO: \' + folioAc', 'Acuse · Folio', 'Acuse guardado con folio',
            'Acuse con folio']:
    assert bad not in s, 'QUEDÓ REFERENCIA AL FOLIO DEL ACUSE: %r' % bad
assert 'fCa-folio' in s and 'cartaAsignarFolio' in s, 'la Carta perdió su folio'
assert '🖨️ Imprimir' in s and 'imprimirPdfDoc' in s, 'falta Imprimir'
assert 'dedupeCartas' in s and 'dedupeAcuses' in s, 'falta dedupe'
assert '2.5.19' not in s, 'quedó 2.5.19 en index.html'
open(P, 'w', encoding='utf-8').write(s)
print('index.html parcheado OK,', len(s), 'bytes')

# --- firebase.js: crearAcuse YA NO asigna ni consume folio cuando no
# se le pasa uno (antes pedía asignarFolioAcuse() y gastaba un número
# que nadie ve). Si se le pasa folio (compat.), se guarda.
repfb('''// Acuses de Sistemas (2.5.16; folio desde 2.5.18): acuse de recibido
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
}''',
    '''// Acuses de Sistemas (2.5.16; SIN folio desde 2.5.20): acuse de
// recibido de documentos. El formato original no lleva folio y la app
// ya no asigna ni consume ninguno al abrir el formulario; crearAcuse
// solo guarda el folio si quien llama pasa uno explícito (compat. con
// documentos viejos). Sin página pública. El documento lleva
// creadoPor, creadoPorNombre, creadoEn y datos {fecha, para, de,
// anexo}. uidOpcional filtra por creadoPor (lo usan los usuarios
// normales para que las reglas permitan la lectura); sin él el admin
// suscribe todo.
async function crearAcuse(datos, creadoPorNombre, folio) {
  const u = auth.currentUser;
  if (!u) throw new Error('no-auth');
  const ref = doc(collection(db, 'acuses'));
  const data = {
    creadoPor: u.uid,
    creadoPorNombre: creadoPorNombre || u.email || '',
    creadoEn: Date.now(),
    datos: datos || {}
  };
  if (folio) data.folio = folio;
  await setDoc(ref, data);
  return ref.id;
}''')
open(FB, 'w', encoding='utf-8').write(fb)
print('firebase.js parcheado OK')
