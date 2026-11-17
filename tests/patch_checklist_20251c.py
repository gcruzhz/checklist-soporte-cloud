import io
P = '/home/hatch/workspace/android/checklist-cloud/www/index.html'
s = io.open(P, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'NO ENCONTRADO o repetido (%d): %r' % (c, old[:120])
    s = s.replace(old, new)

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
