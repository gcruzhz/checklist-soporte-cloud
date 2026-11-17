# Parche Checklist 2.5.1 (puntos 1-13 de Mantenimientos Preventivos).
import io

P = '/home/hatch/workspace/android/checklist-cloud/www/index.html'
s = io.open(P, encoding='utf-8').read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'NO ENCONTRADO o repetido (%d): %r' % (c, old[:120])
    s = s.replace(old, new)

# ---- Versiones: '2.5.0' -> '251' en comentarios; solo 2 sitios reales 2.5.1.
if s.count('2.5.0') == 52:
    s = s.replace('2.5.0', '251')
    s = s.replace('Versión 251', 'Versión 2.5.1')
    s = s.replace('Versión: 251', 'Versión: 2.5.1')
elif s.count('2.5.0') == 0 and s.count('2.5.1') == 2:
    pass  # parte A ya aplicada
else:
    raise AssertionError('conteo 2.5.0/2.5.1 inesperado: %d/%d' % (s.count('2.5.0'), s.count('2.5.1')))

# ---- Constantes y helpers 251 (empresa, año, título compuesto, defaults).
rep('''var FIRMA_URL_BASE = 'https://checklist-soporte.web.app/firma.html';''',
'''var FIRMA_URL_BASE = 'https://checklist-soporte.web.app/firma.html';
// Defaults del formulario de mantenimientos (251): solo se prellenan
// cuando el campo está vacío al abrir el formulario; un valor guardado
// por el técnico nunca se sobrescribe.
var MANT_TITULO_DEF = 'Mantenimiento Preventivo sistemas';
var MANT_DESC_CAMBIOS_DEF = 'se realiza mantenimiento preventivo en hardware y software, sopleteo y limpieza general, instalación de actualización, revisión de políticas y antivirus, desinstalación de software no permitido';
function mantAnioActual() { return new Date().getFullYear(); }
function mantTituloBase(t) { return String(t || '').replace(/\\s+(19|20)\\d\\d\\s*$/, '').trim(); }
function mantAnioOf(m) {
  if (m && m.anio) return Number(m.anio);
  var mm = /((?:19|20)\\d\\d)\\s*$/.exec(String((m && m.tituloCaso) || ''));
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
  var inRange = [String(y - 1), String(y), String(y + 1), String(y + 2)].indexOf(cur) !== -1;
  var target = inRange ? cur : String(y);
  var opts = '';
  for (var yy = y - 1; yy <= y + 2; yy++) opts += '<option value="' + yy + '"' + (String(yy) === target ? ' selected' : '') + '>' + yy + '</option>';
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
}''')

# ---- newMantBlank: empresa, año y ambos tipos por default.
rep('''    tecnicoUid: cloudUser ? cloudUser.uid : '', tecnico: technicianName(),
    tipo: 'SOFTWARE', area: '', responsable: '',
''',
'''    tecnicoUid: cloudUser ? cloudUser.uid : '', tecnico: technicianName(),
    empresa: 'Lapi', anio: mantAnioActual(),
    tipo: 'SOFTWARE/HARDWARE', area: '', responsable: '',
''')

# ---- mantToCloudDoc / mantFromCloud: empresa y año viajan a la nube.
rep('''    tecnicoUid: m.tecnicoUid || '', tecnico: m.tecnico || '',
    tipo: m.tipo || '', area: m.area || '', responsable: m.responsable || '',
''',
'''    tecnicoUid: m.tecnicoUid || '', tecnico: m.tecnico || '',
    empresa: m.empresa || 'Lapi', anio: (m.anio == null ? mantAnioActual() : m.anio),
    tipo: m.tipo || '', area: m.area || '', responsable: m.responsable || '',
''')
rep('''  m.tecnico = d.tecnico || '';
  m.tipo = d.tipo || 'SOFTWARE';''',
'''  m.tecnico = d.tecnico || '';
  m.empresa = d.empresa || 'Lapi';
  m.anio = d.anio || null;
  if (!m.anio) { var mmAnio = /((?:19|20)\\d\\d)\\s*$/.exec(String(d.tituloCaso || '')); m.anio = mmAnio ? Number(mmAnio[1]) : mantAnioActual(); }
  m.tipo = d.tipo || 'SOFTWARE/HARDWARE';''')

# ---- Tarjeta: título compuesto, empresa y botón Eliminar (admin, no borrador).
rep('''  return '<div class="card"><h2>' + esc(m.tituloCaso || 'Mantenimiento sin título') + '</h2>' +
    '<div class="mant-id-line">' + esc(idLine) + '</div>' +
    '<div class="sub">' + esc((m.tipo || '') + ' · ' + (m.area || '—') + ' · Responsable: ' + (m.responsable || '—')) + '</div>' +''',
'''  return '<div class="card"><h2>' + esc(m.tituloCaso ? mantTituloCompuesto(m) : 'Mantenimiento sin título') + '</h2>' +
    '<div class="mant-id-line">' + esc(idLine) + '</div>' +
    '<div class="sub">' + esc((m.empresa || 'Lapi') + ' · ' + (m.tipo || '') + ' · ' + (m.area || '—') + ' · Responsable: ' + (m.responsable || '—')) + '</div>' +''')
rep('''    (m.estado === 'borrador' ? '<button class="btn-danger" data-mant-del="' + esc(m.id) + '">Eliminar</button>' : '') +''',
'''    (m.estado === 'borrador' ? '<button class="btn-danger" data-mant-del="' + esc(m.id) + '">Eliminar</button>' : '') +
    ((cloudRole === 'admin' && m.estado !== 'borrador') ? '<button class="btn-danger" data-mant-del-order="' + esc(m.id) + '">Eliminar</button>' : '') +''')

# ---- Vista de la orden: empresa, título compuesto y botón Eliminar (admin).
rep('''    '<div class="sub">Estado: ' + esc(mantEstadoLabel(m)) + ' · Tipo: ' + esc(m.tipo || '—') + ' · Área: ' + esc(m.area || '—') + '</div>' +''',
'''    '<div class="sub">Estado: ' + esc(mantEstadoLabel(m)) + ' · Empresa: ' + esc(mantEmpresaOf(m)) + ' · Tipo: ' + esc(m.tipo || '—') + ' · Área: ' + esc(m.area || '—') + '</div>' +''')
rep('''    '<div class="sub">Título del caso: ' + esc(m.tituloCaso || '—') + ' · Tipo de falla: ' + esc(m.tipoFalla || '—') + '</div>' +''',
'''    '<div class="sub">Título del caso: ' + esc(mantTituloCompuesto(m)) + ' · Tipo de falla: ' + esc(m.tipoFalla || '—') + '</div>' +''')
rep('''  var cancelBtn = document.getElementById('btnMantCancelarOrden');
  if (cancelBtn) cancelBtn.hidden = !(m.estado === 'creada' || m.estado === 'firmada');''',
'''  var cancelBtn = document.getElementById('btnMantCancelarOrden');
  if (cancelBtn) cancelBtn.hidden = !(m.estado === 'creada' || m.estado === 'firmada');
  var delBtn = document.getElementById('btnMantEliminarOrden');
  if (delBtn) delBtn.hidden = !(cloudRole === 'admin' && m.estado !== 'borrador');''')

# ---- mantReadForm: empresa, año, tipo por checkboxes, título compuesto.
rep('''  m.tipo = mantVal('fM-tipo') || 'SOFTWARE';''',
'''  m.empresa = mantVal('fM-empresa') || 'Lapi';
  var anioSel = Number(mantVal('fM-anio')) || mantAnioActual();
  m.anio = anioSel;
  var swTipo = mantCheck('fM-tipo-sw'), hwTipo = mantCheck('fM-tipo-hw');
  m.tipo = (swTipo && hwTipo) ? 'SOFTWARE/HARDWARE' : (swTipo ? 'SOFTWARE' : (hwTipo ? 'HARDWARE' : ''));''')
rep('''  m.tituloCaso = mantVal('fM-titulo').trim();''',
'''  var titBase = mantTituloBase(mantVal('fM-titulo'));
  m.tituloCaso = titBase ? titBase + ' ' + anioSel : '';''')

# ---- mantFillForm: empresa, checkboxes, título base + año.
rep('''  mantSetVal('fM-tecnico', m.tecnico);
  mantSetVal('fM-tipo', m.tipo);''',
'''  mantSetVal('fM-tecnico', m.tecnico);
  mantSetVal('fM-empresa', mantEmpresaOf(m));
  mantSetCheck('fM-tipo-sw', !m.tipo || String(m.tipo).indexOf('SOFTWARE') !== -1);
  mantSetCheck('fM-tipo-hw', !m.tipo || String(m.tipo).indexOf('HARDWARE') !== -1);''')
rep('''  mantSetVal('fM-titulo', m.tituloCaso);''',
'''  mantSetVal('fM-titulo', mantTituloBase(m.tituloCaso) || MANT_TITULO_DEF);
  mantSetVal('fM-anio', String(mantAnioOf(m)));''')

# ---- mantFormHasData: los valores por default no cuentan como datos.
rep('''  for (var i = 0; i < ids.length; i++) { if (mantVal(ids[i]).trim()) return true; }''',
'''  var defVals = { 'fM-tRep': '/', 'fM-tViaje': '/', 'fM-tCaido': '/', 'fM-tipoFalla': '/', 'fM-fechaPlan': '/', 'fM-fechaComp': '/', 'fM-periodoPrueba': '/', 'fM-titulo': MANT_TITULO_DEF, 'fM-descCambios': MANT_DESC_CAMBIOS_DEF };
  for (var i = 0; i < ids.length; i++) { var vv = mantVal(ids[i]).trim(); if (vv && defVals[ids[i]] !== vv) return true; }''')

# ---- mantOpenForm: aplicar defaults al abrir (nuevo o edición).
rep('''  if (m) mantFillForm(m); else { mantClearForm(); prefillMantTecnico(); }
  mantScrollTo('mantFormBox');''',
'''  if (m) mantFillForm(m); else { mantClearForm(); prefillMantTecnico(); }
  mantApplyDefaults();
  mantScrollTo('mantFormBox');''')

# ---- 10. Eliminar orden (admin): local + nube, con confirmación.
rep('''// Escala de satisfacción (251, interpretación): 0–3 INACEPTABLE,''',
'''function mantEliminarOrden(id) {
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
// Escala de satisfacción (251, interpretación): 0–3 INACEPTABLE,''')
rep('''document.getElementById('btnMantCancelarOrden').addEventListener('click', function () { mantCancelarOrden(); });''',
'''document.getElementById('btnMantCancelarOrden').addEventListener('click', function () { mantCancelarOrden(); });
document.getElementById('btnMantEliminarOrden').addEventListener('click', function () { mantEliminarOrden(mantOrderId); });''')
rep('''  var id = q('data-mant-edit') || q('data-mant-order') || q('data-mant-cancel-order') || q('data-mant-del');''',
'''  var id = q('data-mant-edit') || q('data-mant-order') || q('data-mant-cancel-order') || q('data-mant-del') || q('data-mant-del-order');''')
rep('''  if (t.closest('[data-mant-del]')) {
    showConfirm('¿Eliminar este borrador de mantenimiento?').then(function (ok) {''',
'''  if (t.closest('[data-mant-del-order]')) {
    if (cloudRole !== 'admin') return;
    mantEliminarOrden(id);
    return;
  }
  if (t.closest('[data-mant-del]')) {
    showConfirm('¿Eliminar este borrador de mantenimiento?').then(function (ok) {''')

# ---- 6. Hostname -> descripción del equipo al teclear (si sigue vacía).
rep('''['fM-pol-cambio', 'fM-pol-long', 'fM-pol-intentos', 'fM-pol-bloqueo'].forEach(function (id) {
  var el = document.getElementById(id);
  if (el) el.addEventListener('input', refreshMantPolLine);
});''',
'''['fM-pol-cambio', 'fM-pol-long', 'fM-pol-intentos', 'fM-pol-bloqueo'].forEach(function (id) {
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
})();''')

# ---- 12. Compartir copia: sin Capacitor, probar share web y si no,
# descargar el PDF y avisar (nunca decir que se compartió sin compartir).
rep('''  } catch (e) {
    showToast('No se pudo compartir la copia. Genera el PDF y compártelo desde tus archivos.');
  }
}''',
'''  } catch (e) {
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
}''')

io.open(P, 'w', encoding='utf-8').write(s)
print('parte B ok, 2.5.1:', s.count('2.5.1'), '2.5.0:', s.count('2.5.0'))

# ---- buildPdfMant: row() con alineación + helpers de fila derecha.
rep('''  function row(t, f, s, img) { var r = { t: t, f: f || 'F1', s: s || 11 }; if (img) r.img = img; rows.push(r); }''',
'''  function row(t, f, s, img, a) { var r = { t: t, f: f || 'F1', s: s || 11 }; if (img) r.img = img; if (a) r.a = a; rows.push(r); }
  function rrow(t, f, s, img) { row(t, f, s, img, 'R'); }
  function rkv(label, val) { wrapText(label + ': ' + (val == null || val === '' ? '—' : String(val)), 82).forEach(function (ln) { rrow(ln, 'F1', 11); }); }''')

# ---- 1. Encabezado del PDF: nombre de la empresa; contacto solo con Lapi.
rep('''  row('Lapi Sistemas', 'F2', 16);
  row('Rosa Blanca 63, Col. Molino de Rosas, C.P. 01470', 'F1', 11);
  row('Tels. 53371283 y 53370207', 'F1', 11);
  row('sistemas@lapi.com.mx · info@lapi.com.mx', 'F1', 11);
  row('', 'F1', 11);''',
'''  // Encabezado (251): el nombre es la empresa elegida; el bloque de
  // contacto (dirección, teléfonos y correos de Lapi) solo va con Lapi.
  var empPdf = mantEmpresaOf(m);
  row(empPdf === 'Lapi' ? 'Lapi Sistemas' : empPdf, 'F2', 16);
  if (empPdf === 'Lapi') {
    row('Rosa Blanca 63, Col. Molino de Rosas, C.P. 01470', 'F1', 11);
    row('Tels. 53371283 y 53370207', 'F1', 11);
    row('sistemas@lapi.com.mx · info@lapi.com.mx', 'F1', 11);
  }
  row('', 'F1', 11);''')
rep('''  kv('Nombre de quien presta el servicio', m.tecnico);''',
'''  kv('Nombre de quien presta el servicio', m.tecnico);
  kv('Empresa', mantEmpresaOf(m));''')
rep('''  kv('Título del caso', m.tituloCaso);''',
'''  kv('Título del caso', mantTituloCompuesto(m));''')

# ---- 8+9+13. Firmas por fase y conformidad final abajo a la derecha.
rep('''  section('Firmas');
  var tecImg = hasImg(sigImgs.tecnico) ? { name: 'tecnico', w: 150, h: Math.max(20, Math.round(150 * sigImgs.tecnico.h / sigImgs.tecnico.w)) } : null;
  ['Planeación', 'Compromiso de instalación', 'Periodo de prueba', 'Liberación'].forEach(function (fase) {
    row('Sistemas — ' + fase + ':', 'F2', 12);
    if (tecImg) row('', 'F1', 11, tecImg);
    else row('Firma: ' + (m.tecnico || '—') + ' (guardada en la app)', 'F1', 11);
    row('Área solicitante — ' + fase + ': ________________________________________', 'F1', 11);
  });
  section('Conformidad del usuario');
  if (m.firma) {
    kv('Nombre', m.firma.nombre);
    kv('Área', m.firma.area);
    if (m.firma.comentarios) kv('Comentarios', m.firma.comentarios);
    kv('Fecha', m.firma.firmadoEn ? fmtDate(m.firma.firmadoEn) : '');
    kv('Hora', m.firma.firmadoEn ? fmtTime(m.firma.firmadoEn) : '');
    var sat = m.firma.satisfaccion;
    row('Escala de satisfacción (0–10): ' + satLabel(sat), 'F1', 11);
    if (sat != null && sat !== '') {
      var marks = [];
      for (var i = 0; i <= 10; i++) marks.push(i === Number(sat) ? '[' + i + ']' : String(i));
      row(marks.join('  '), 'F1', 11);
      row('INACEPTABLE 0-3 · ACEPTABLE 4-7 · EXCELENTE 8-10', 'F1', 10);
    }
    var usrImg = hasImg(sigImgs.usuario) ? { name: 'usuario', w: 150, h: Math.max(20, Math.round(150 * sigImgs.usuario.h / sigImgs.usuario.w)) } : null;
    row('Firma de conformidad:', 'F2', 12);
    if (usrImg) row('', 'F1', 11, usrImg);
    else row('Firma: ' + (m.firma.nombre || '—') + ' (guardada en la app)', 'F1', 11);
  } else {
    row('Pendiente de firma.', 'F1', 11);
  }
  row('', 'F1', 11);
  row('Generado el ' + fmtDate(Date.now()) + ' — Checklist de Soporte', 'F1', 10);
  return assemblePdf(rows, sigImgs);''',
'''  // Firmas por fase (251): Planeación, Compromiso y Periodo de prueba
  // llevan '/' en la fecha y en la línea de firma (sin firmar ahí); solo
  // la Liberación lleva la fecha elegida y ambas firmas.
  section('Firmas');
  var tecImg = hasImg(sigImgs.tecnico) ? { name: 'tecnico', w: 150, h: Math.max(20, Math.round(150 * sigImgs.tecnico.h / sigImgs.tecnico.w)) } : null;
  var usrImg = hasImg(sigImgs.usuario) ? { name: 'usuario', w: 150, h: Math.max(20, Math.round(150 * sigImgs.usuario.h / sigImgs.usuario.w)) } : null;
  ['Planeación', 'Compromiso de instalación', 'Periodo de prueba'].forEach(function (fase) {
    row('Sistemas — ' + fase + ':', 'F2', 12);
    row('Fecha: /', 'F1', 11);
    row('Firma Sistemas: /', 'F1', 11);
    row('Firma Área solicitante: /', 'F1', 11);
  });
  row('Sistemas — Liberación:', 'F2', 12);
  row('Fecha: ' + (m.fechaLiberacion || '—'), 'F1', 11);
  if (tecImg) row('', 'F1', 11, tecImg);
  else row('Firma: ' + (m.tecnico || '—') + ' (guardada en la app)', 'F1', 11);
  row('Área solicitante — Liberación:', 'F2', 12);
  if (usrImg) row('', 'F1', 11, usrImg);
  else if (m.firma) row('Firma: ' + (m.firma.nombre || '—') + ' (guardada en la app)', 'F1', 11);
  else row('Firma Área solicitante: pendiente', 'F1', 11);
  row('', 'F1', 11);
  row('Generado el ' + fmtDate(Date.now()) + ' — Checklist de Soporte', 'F1', 10);
  // Conformidad del usuario (251, punto 13): cierre final del documento,
  // en la parte inferior derecha (como la orden de papel: FECHA, HORA,
  // NOMBRE Y FIRMA DE CONFORMIDAD). Todas sus filas van alineadas a la
  // derecha (r.a = 'R'); la firma dibujada del usuario también.
  row('', 'F1', 11);
  rrow('Conformidad del usuario - FECHA, HORA, NOMBRE Y FIRMA DE CONFORMIDAD', 'F2', 12);
  if (m.firma) {
    rkv('Nombre', m.firma.nombre);
    rkv('Área', m.firma.area);
    if (m.firma.comentarios) rkv('Comentarios', m.firma.comentarios);
    rkv('Fecha', m.firma.firmadoEn ? fmtDate(m.firma.firmadoEn) : '');
    rkv('Hora', m.firma.firmadoEn ? fmtTime(m.firma.firmadoEn) : '');
    var sat = m.firma.satisfaccion;
    rrow('Escala de satisfacción (0–10): ' + satLabel(sat), 'F1', 11);
    if (sat != null && sat !== '') {
      var marks = [];
      for (var i = 0; i <= 10; i++) marks.push(i === Number(sat) ? '[' + i + ']' : String(i));
      rrow(marks.join('  '), 'F1', 11);
      rrow('INACEPTABLE 0-3 · ACEPTABLE 4-7 · EXCELENTE 8-10', 'F1', 10);
    }
    rrow('Firma de conformidad:', 'F2', 12);
    if (usrImg) rrow('', 'F1', 11, usrImg);
    else rrow('Firma: ' + (m.firma.nombre || '—') + ' (guardada en la app)', 'F1', 11);
  } else {
    rrow('Pendiente de firma.', 'F1', 11);
  }
  return assemblePdf(rows, sigImgs);''')

io.open(P, 'w', encoding='utf-8').write(s)
print('parte C ok, 2.5.1:', s.count('2.5.1'), '2.5.0:', s.count('2.5.0'))
