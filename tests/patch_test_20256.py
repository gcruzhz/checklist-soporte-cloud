# Parche de pruebas 2.5.6: test20255.js -> test20256.js (ya copiado).
import sys

P = '/home/hatch/workspace/android/checklist-cloud/tests/test20256.js'
s = open(P, encoding='utf-8').read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'NO ENCONTRADO x%d (esperado %d): %r' % (c, n, old[:120])
    s = s.replace(old, new)

# --- SRC y versión 2.5.6.
rep("const SRC = fs.readFileSync(__dirname + '/checklist20255.js', 'utf8');",
    "const SRC = fs.readFileSync(__dirname + '/checklist20256.js', 'utf8');")
rep("html.includes('Versión 2.5.5')", "html.includes('Versión 2.5.6')", n=4)
rep("html.includes('Versión: 2.5.5')", "html.includes('Versión: 2.5.6')", n=2)
rep("html.includes('Versión 2.5.4')", "html.includes('Versión 2.5.5')", n=2)
rep("!html.includes('2.5.4')", "!html.includes('2.5.5')", n=3)
rep("(html.match(/2\\.5\\.5/g) || []).length", "(html.match(/2\\.5\\.6/g) || []).length")
rep("var n255 = ", "var n256 = ")
rep("n255 === 2", "n256 === 2", n=2)
rep("'AM0) versión 2.5.5:'", "'AM0) versión 2.5.6:'")
rep("'AP0) estáticos 2.5.5:", "'AP0) estáticos 2.5.6:")
rep("'AR0) versión 2.5.5 visible:'", "'AR0) versión 2.5.6 visible:'")
rep("'| 0 de 2.5.4:'", "'| 0 de 2.5.5:'", n=2)
rep("'| ocurrencias 2.5.5:'", "'| ocurrencias 2.5.6:'")
rep("'BA0) versión 2.5.5 sin 2.5.4:'", "'BA0) versión 2.5.6 sin 2.5.5:'")
rep("'BB0) 2.5.5 en 2 sitios:'", "'BB0) 2.5.6 en 2 sitios:'")

# --- BA9: los datos ya no van como "Datos detectados" ni "Observaciones
# del técnico" en el PDF; van en el cuadro COMENTARIOS. El procesador
# ahora viene del bloque estructurado ("Intel Core i5"), no del texto
# detectado viejo ("Intel i5"); y el título de conformidad ya no lleva HORA.
rep("'Políticas: cambio cada 90 días', 'Procesador: Intel i5', 'Impresora: HP LaserJet'",
    "'Políticas: cambio cada 90 días', 'Procesador: Intel Core i5', 'Impresora: HP LaserJet'")
rep("'FECHA, HORA, NOMBRE Y FIRMA DE CONFORMIDAD', 'Ana López'",
    "'FECHA, NOMBRE Y FIRMA DE CONFORMIDAD', 'Ana López'")
rep("'Usuario de sistemas: Sí', 'Observaciones del técnico:', 'Datos detectados:'];",
    "'Usuario de sistemas: Sí', 'Observaciones: Sin observaciones', 'Datos del equipo:', 'Comentarios del usuario: Todo bien'];")

# --- BB7: la conformidad ya no lleva hora; la fecha es solo fecha.
rep("pdfBB7.indexOf('Fecha: ' + fmtDate(mBB7.firma.firmadoEn)) !== -1",
    "pdfBB7.indexOf('Fecha: ' + fmtFecha(mBB7.firma.firmadoEn)) !== -1")

# --- 255D reescrita: los datos del equipo van en COMENTARIOS (256), no
# en Conclusión.
old255d = """  // 255D: PDF de mantenimiento en carta, Descripción solo hostname, los
  // demás datos al final en Conclusión; el PDF de preparación sigue en A4.
  var m255d = mkMant({});
  var pdf255d = await pdfStrOf(m255d);
  var d255carta = pdf255d.indexOf('/MediaBox [0 0 612 792]') !== -1 && pdf255d.indexOf('/MediaBox [0 0 595 842]') === -1;
  var d255pag = (pdf255d.match(/\\/Type \\/Page[^s]/g) || []).length === 1;
  var rows255d = pdfTextRows(pdf255d);
  function rowIdx255(txt) { for (var i = 0; i < rows255d.length; i++) if (rows255d[i].t.indexOf(txt) !== -1) return i; return -1; }
  var iDesc255 = rowIdx255('DESCRIPCIÓN DEL EQUIPO');
  var iHost255 = rowIdx255('Hostname: PC-01');
  var iCond255 = rowIdx255('CONDICIONES GENERALES');
  var iConcl255 = rowIdx255('CONCLUSIÓN Y/O COMENTARIOS');
  var iSerie255 = rowIdx255('Serie: S1, Modelo: Inspiron 3501');
  var d255soloHost = iDesc255 !== -1 && iHost255 === iDesc255 + 1 && iHost255 < iCond255;
  var d255alFinal = iConcl255 !== -1 && iSerie255 > iConcl255;
  var d255datos = pdf255d.indexOf('Procesador: Intel Core i5') !== -1 && pdf255d.indexOf('192.168.1.45') !== -1 && pdf255d.indexOf('HP LaserJet') !== -1 && pdf255d.indexOf('123 456 789') !== -1 && pdf255d.indexOf('Windows 11 Pro 26H2') !== -1 && pdf255d.indexOf('Políticas:') !== -1 && pdf255d.indexOf('Usuario de sistemas:') !== -1 && pdf255d.indexOf('Descripción: Laptop Dell Inspiron') !== -1;
  var d255casillas = (pdf255d.match(/\\(X\\)/g) || []).length === 14;
  var pdfPrep255 = Buffer.from(await buildPdf(mkPrep({})).arrayBuffer()).toString('latin1');
  var d255prepA4 = pdfPrep255.indexOf('/MediaBox [0 0 595 842]') !== -1 && pdfPrep255.indexOf('/MediaBox [0 0 612 792]') === -1;
  console.log('255D) MediaBox carta 612x792:', d255carta, '| 1 página:', d255pag, '| Descripción solo hostname:', d255soloHost, '| serie/modelo al final en Conclusión:', d255alFinal, '| ningún dato perdido:', d255datos, '| 14 casillas:', d255casillas, '| preparación sigue en A4:', d255prepA4);"""
new255d = """  // 255D (reescrita en 256): PDF de mantenimiento en carta, Descripción
  // solo hostname, los demás datos al final en el cuadro COMENTARIOS
  // (abajo a la izquierda, ya no en Conclusión); el PDF de preparación
  // sigue en A4.
  var m255d = mkMant({});
  var pdf255d = await pdfStrOf(m255d);
  var d255carta = pdf255d.indexOf('/MediaBox [0 0 612 792]') !== -1 && pdf255d.indexOf('/MediaBox [0 0 595 842]') === -1;
  var d255pag = (pdf255d.match(/\\/Type \\/Page[^s]/g) || []).length === 1;
  var rows255d = pdfTextRows(pdf255d);
  function rowIdx255(txt) { for (var i = 0; i < rows255d.length; i++) if (rows255d[i].t.indexOf(txt) !== -1) return i; return -1; }
  function rowExact255(txt) { for (var i = 0; i < rows255d.length; i++) if (rows255d[i].t === txt) return i; return -1; }
  var iDesc255 = rowIdx255('DESCRIPCIÓN DEL EQUIPO');
  var iHost255 = rowIdx255('Hostname: PC-01');
  var iCond255 = rowIdx255('CONDICIONES GENERALES');
  var iConcl255 = rowIdx255('CONCLUSIÓN Y/O COMENTARIOS');
  var iCom255 = rowExact255('COMENTARIOS');
  var iSerie255 = rowIdx255('Serie: S1, Modelo: Inspiron 3501');
  var d255soloHost = iDesc255 !== -1 && iHost255 === iDesc255 + 1 && iHost255 < iCond255;
  var d255enComent = iCom255 !== -1 && iSerie255 > iCom255;
  var d255noConcl = (function () { for (var i = iConcl255 + 1; i < rows255d.length && rows255d[i].t.indexOf('FECHA DE PLANEACIÓN') === -1; i++) if (rows255d[i].t.indexOf('Serie:') !== -1 || rows255d[i].t.indexOf('Procesador:') !== -1 || rows255d[i].t.indexOf('Datos del equipo') !== -1) return false; return true; })();
  var d255datos = pdf255d.indexOf('Procesador: Intel Core i5') !== -1 && pdf255d.indexOf('192.168.1.45') !== -1 && pdf255d.indexOf('HP LaserJet') !== -1 && pdf255d.indexOf('123 456 789') !== -1 && pdf255d.indexOf('Windows 11 Pro 26H2') !== -1 && pdf255d.indexOf('Políticas:') !== -1 && pdf255d.indexOf('Usuario de sistemas:') !== -1 && pdf255d.indexOf('Descripción: Laptop Dell Inspiron') !== -1;
  var d255casillas = (pdf255d.match(/\\(X\\)/g) || []).length === 14;
  var pdfPrep255 = Buffer.from(await buildPdf(mkPrep({})).arrayBuffer()).toString('latin1');
  var d255prepA4 = pdfPrep255.indexOf('/MediaBox [0 0 595 842]') !== -1 && pdfPrep255.indexOf('/MediaBox [0 0 612 792]') === -1;
  console.log('255D) MediaBox carta 612x792:', d255carta, '| 1 página:', d255pag, '| Descripción solo hostname:', d255soloHost, '| serie/modelo en COMENTARIOS y fuera de Conclusión:', d255enComent && d255noConcl, '| ningún dato perdido:', d255datos, '| 14 casillas:', d255casillas, '| preparación sigue en A4:', d255prepA4);"""
rep(old255d, new255d)

# --- Serie 256 nueva, antes de process.exit(0).
serie256 = """
  // 256: serie nueva 2.5.6 — una sola hoja carta con orden completa,
  // datos del equipo en COMENTARIOS sin duplicar, fecha de conformidad
  // válida (Timestamp/ISO/ausente) y sin hora en el bloque.
  // 256A: orden completa estilo ROBIT5 (cambios 2 líneas, conclusión,
  // equipo detectado completo, comentarios del usuario) en 1 página carta;
  // y una orden de estrés (falla/cambios/conclusión de 3 líneas, notas
  // largas) también en 1 página.
  var m256a = mkMant({ id: 'a256', folio: '00004', estado: 'firmada',
    descripcionCambios: 'se realiza mantenimiento preventivo en hardware y software, sopleteo y limpieza general, instalación de actualización, revisión de políticas y antivirus, desinstalación de software no permitido',
    conclusion: 'Equipo listo para entregar', observaciones: 'Sin observaciones',
    observacionesDetectadas: 'Procesador: Intel Core i5 · RAM: 8 GB · Disco: 256 GB SSD · IP: 192.168.1.45' });
  m256a.firma = { nombre: 'Ana López', area: 'Ventas', comentarios: 'Todo bien', satisfaccion: 10, firma: 'data:image/png;base64,iVBORw0KGgo=', firmadoEn: { seconds: 1794000000, nanoseconds: 0 } };
  var pdf256a = await pdfStrOf(m256a);
  var a256pag = (pdf256a.match(/\\/Type \\/Page[^s]/g) || []).length === 1;
  var a256carta = pdf256a.indexOf('/MediaBox [0 0 612 792]') !== -1;
  var m256aStress = mkMant({ id: 'a256s', folio: '00005', estado: 'creada',
    tipoFalla: 'El equipo se apaga solo varias veces al día y tarda mucho en arrancar por las mañanas cuando se enciende',
    descripcionCambios: 'Se realizó mantenimiento preventivo completo en hardware y software con sopleteo y limpieza general, instalación de actualizaciones pendientes y revisión de políticas',
    conclusion: 'Se dejó el equipo funcionando correctamente después de las pruebas de encendido y apagado realizadas en el área',
    condiciones: { impresora: true, cpu: true, monitor: true, teclado: true, mouse: true, noBreak: false, notas: 'Se encontró polvo acumulado en los ventiladores y el teclado tenía dos teclas duras' } });
  var pdf256aStress = await pdfStrOf(m256aStress);
  var a256stressPag = (pdf256aStress.match(/\\/Type \\/Page[^s]/g) || []).length === 1;
  console.log('256A) orden completa ROBIT5 en 1 página carta:', a256pag && a256carta, '| orden de estrés también en 1 página:', a256stressPag);
  // 256B: datos del equipo en COMENTARIOS (abajo a la izquierda), fuera
  // de Conclusión, cada dato una sola vez y sin "Datos detectados".
  var rows256b = pdfTextRows(pdf256a);
  function rowIdx256(txt) { for (var i = 0; i < rows256b.length; i++) if (rows256b[i].t.indexOf(txt) !== -1) return i; return -1; }
  function rowExact256(txt) { for (var i = 0; i < rows256b.length; i++) if (rows256b[i].t === txt) return i; return -1; }
  function count256(s) { return pdf256a.split(s).length - 1; }
  var iConcl256 = rowIdx256('CONCLUSIÓN Y/O COMENTARIOS');
  var iCom256 = rowExact256('COMENTARIOS');
  var iSerie256 = rowIdx256('Serie: S1, Modelo: Inspiron 3501');
  var b256ubic = iCom256 !== -1 && iSerie256 > iCom256;
  var b256fuera = (function () { for (var i = iConcl256 + 1; i < rows256b.length && rows256b[i].t.indexOf('FECHA DE PLANEACIÓN') === -1; i++) if (rows256b[i].t.indexOf('Serie:') !== -1 || rows256b[i].t.indexOf('Procesador:') !== -1 || rows256b[i].t.indexOf('Datos del equipo') !== -1) return false; return true; })();
  var b256soloConcl = rowIdx256('Conclusión: Equipo listo para entregar') === iConcl256 + 1;
  var b256unaVez = count256('Serie: S1, Modelo: Inspiron 3501') === 1 && count256('Hostname: PC-01') === 1 && count256('Procesador: Intel Core i5') === 1 && count256('RAM: 8 GB') === 1 && count256('HP LaserJet') === 1 && count256('123 456 789') === 1 && count256('Windows 11 Pro 26H2') === 1 && count256('Políticas:') === 1 && count256('Usuario de sistemas:') === 1 && count256('Chrome: 141.0.7390.65') === 1 && count256('Descripción: Laptop Dell Inspiron') === 1 && count256('IP: 192.168.1.45') === 1;
  var b256sinDup = pdf256a.indexOf('Datos detectados') === -1;
  console.log('256B) datos en COMENTARIOS:', b256ubic, '| fuera de Conclusión:', b256fuera, '| Conclusión solo con la conclusión:', b256soloConcl, '| cada dato una sola vez:', b256unaVez, '| sin "Datos detectados":', b256sinDup);
  // 256C: fecha de conformidad válida con firmadoEn como Timestamp de
  // Firestore, string ISO y ausente; sin "Hora:" en el bloque (256).
  var ts256 = { seconds: 1794000000, nanoseconds: 0 };
  var c256tsOk = fmtDate(ts256) !== '-' && fmtDate(ts256).indexOf('Invalid Date') === -1 && fmtFecha(ts256) !== '-' && fmtFecha(ts256).indexOf('Invalid Date') === -1;
  var c256iso = fmtDate('2026-11-17T10:30:00') !== '-' && fmtDate('2026-11-17T10:30:00').indexOf('Invalid Date') === -1;
  var c256nulo = fmtDate(null) === '-' && fmtDate(undefined) === '-' && fmtDate('basura') === '-' && fmtTime(null) === '-' && fmtFecha(null) === '-';
  var c256toDate = fmtDate({ toDate: function () { return new Date(1794000000000); } }) !== '-' && fmtDate({ toDate: function () { return new Date(1794000000000); } }).indexOf('Invalid Date') === -1;
  var c256pdfFecha = pdf256a.indexOf('Fecha: ' + fmtFecha(ts256)) !== -1 && pdf256a.indexOf('Invalid Date') === -1;
  var c256sinHora = pdf256a.indexOf('Hora:') === -1 && pdf256a.indexOf('FECHA, NOMBRE Y FIRMA DE CONFORMIDAD') !== -1 && pdf256a.indexOf('FECHA, HORA,') === -1;
  var c256pie = pdf256a.indexOf('Generado el ') !== -1 && pdf256a.indexOf('Checklist de Soporte') !== -1;
  var m256c2 = mkMant({ id: 'c256b', folio: '00007', estado: 'firmada' });
  m256c2.firma = { nombre: 'Ana López', area: 'Ventas', comentarios: '', satisfaccion: 9, firma: 'data:image/png;base64,iVBORw0KGgo=', firmadoEn: undefined };
  var pdf256c2 = await pdfStrOf(m256c2);
  var c256sinFecha = pdf256c2.indexOf('Fecha: -') !== -1 && pdf256c2.indexOf('Invalid Date') === -1;
  mantenimientos = [m256a];
  mantShowOrder('a256');
  var c256vista = document.getElementById('mantOrderBody').innerHTML.indexOf('Invalid Date') === -1 && document.getElementById('mantOrderBody').innerHTML.indexOf(fmtDate(ts256)) !== -1;
  console.log('256C) Timestamp válido:', c256tsOk, '| ISO válido:', c256iso, '| nulo/basura es "-":', c256nulo, '| toDate() válido:', c256toDate, '| PDF fecha válida:', c256pdfFecha, '| sin "Hora:" y título nuevo:', c256sinHora, '| pie sin cambio:', c256pie, '| sin firmadoEn es "Fecha: -":', c256sinFecha, '| vista de orden sin Invalid Date:', c256vista);
"""
rep("  process.exit(0);", serie256 + "\n  process.exit(0);")

open(P, 'w', encoding='utf-8').write(s)
print('OK test20256.js, bytes:', len(s))
print('2.5.6 en tests:', s.count('2.5.6'), '| 2.5.5 restante:', s.count('2.5.5'), '| 2.5.4 restante:', s.count('2.5.4'))
