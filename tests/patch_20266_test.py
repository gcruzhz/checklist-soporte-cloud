# Parche de pruebas 2.5.16: test20265.js -> test20266.js.
# 1) Extrae el <script> actual de www/index.html a
# tests/checklist20266.js (el JavaScript de esta version, que evalua el
# harness). 2) Copia test20265.js a test20266.js y actualiza la version
# (2.5.15 -> 2.5.16, 2.5.14 -> 2.5.15, mailto 265 -> 266, n265 ->
# n266). 3) Actualiza 265A al bundle nuevo de 2.5.16 (md5
# d8ad9d102d13ef69925d7bdab65b9e33, 508 719 B; cambió por las funciones
# nuevas de acuses/cartas/foliosCarta). 4) Agrega la serie 266 (12
# casos): acuse vacío por defecto, fecha "Septiembre 01, 2026", PDF del
# acuse con PARA/DE/ANEXO/RECIBE, validación de obligatorios, carta con
# folio de 5 dígitos vía crearCarta (transacción mockeada), filas de
# equipo agregar/quitar, PDF de carta FO-SI-10 con encabezado + campos
# + tabla de equipos + texto legal verbatim + 2 páginas, visibilidad
# propia vs admin, reabrir/eliminar, compartir PDF por WhatsApp/correo
# y folio local 00001/00002.
# Uso: python3 patch_20266_test.py (corre desde tests/)
import os
import shutil

BASE = '/home/hatch/workspace/android/checklist-cloud'
TESTS = os.path.join(BASE, 'tests')
SRC = os.path.join(TESTS, 'test20265.js')
P = os.path.join(TESTS, 'test20266.js')
NEW_BUNDLE_MD5 = 'd8ad9d102d13ef69925d7bdab65b9e33'

# --- Extraer el <script> actual de www/index.html.
html = open(os.path.join(BASE, 'www/index.html'), encoding='utf-8').read()
i = html.index('<script>', html.index('firebase-config'))
j = html.index('</script>', i)
open(os.path.join(TESTS, 'checklist20266.js'), 'w', encoding='utf-8').write(html[i + len('<script>'):j])
print('checklist20266.js extraido:', j - i - len('<script>'), 'bytes')

shutil.copyfile(SRC, P)
s = open(P, encoding='utf-8').read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'NO ENCONTRADO x%d (esperado %d): %r' % (c, n, old[:120])
    s = s.replace(old, new)


def repall(old, new, n):
    global s
    c = s.count(old)
    assert c == n, 'NO ENCONTRADO x%d (esperado %d): %r' % (c, n, old[:120])
    s = s.replace(old, new)


# --- SRC y version 2.5.16 (orden: primero 2.5.15 -> 2.5.16, luego
# 2.5.14 -> 2.5.15 para las referencias a la version anterior).
rep("const SRC = fs.readFileSync(__dirname + '/checklist20265.js', 'utf8');",
    "const SRC = fs.readFileSync(__dirname + '/checklist20266.js', 'utf8');")
repall("2.5.15", "2.5.16", 21)
repall("2.5.14", "2.5.15", 12)
repall("n265", "n266", 3)
repall("Soporte 265", "Soporte 266", 3)
repall("mailto 265", "mailto 266", 4)
# El regex lleva la versión con barras escapadas: el reemplazo plano
# de "2.5.15" no lo toca, hay que actualizarlo aparte.
BS = chr(92)
rep("var n266 = (html.match(/2" + BS + ".5" + BS + ".15/g) || []).length;",
    "var n266 = (html.match(/2" + BS + ".5" + BS + ".16/g) || []).length;")

# --- 265A: el bundle de Firebase SÍ cambia en 2.5.16 (funciones nuevas
# de acuses/cartas/foliosCarta): md5 nuevo d8ad9d10… (508 719 B).
rep("var a265bundle = md5bundle265 === 'f9c4918d91bfbf4057433c43c54d708a';",
    "var a265bundle = md5bundle265 === '" + NEW_BUNDLE_MD5 + "';")
rep("console.log('265A) versión 2.5.16:', a265ver, '| bundle sin cambio (f9c4918d…):', a265bundle, '| lógica nueva en la app:', a265src);",
    "console.log('265A) versión 2.5.16:', a265ver, '| bundle nuevo 2.5.16 (d8ad9d10…):', a265bundle, '| lógica nueva en la app:', a265src);")

# --- Serie 266 nueva, antes de process.exit(0).
serie266 = """
  // 266: serie nueva — Acuse Sistemas y Carta Responsiva FO-SI-10
  // (2.5.16): dos formularios con PDF que reproducen los formatos
  // originales; folio de carta de 5 dígitos asignado al guardar.
  async function pdfStrOf266(blob) { return Buffer.from(await blob.arrayBuffer()).toString('latin1'); }
  function fakeListTarget266(attr, id) {
    return { closest: function (sel) { return sel === '[' + attr + ']' ? { getAttribute: function () { return id; } } : null; } };
  }
  CLOUD_ENABLED = false;
  // 266A: versión 2.5.16 en los 2 sitios, mailto 266, bundle nuevo
  // (md5 d8ad9d10…), firebase.js con las 11 funciones nuevas y reglas
  // con acuses/cartas/foliosCarta.
  var crypto266 = require('crypto');
  var bundle266 = fs.readFileSync('/home/hatch/workspace/android/checklist-cloud/www/cloud/firebase.bundle.js');
  var md5bundle266 = crypto266.createHash('md5').update(bundle266).digest('hex');
  var fb266 = fs.readFileSync('/home/hatch/workspace/android/checklist-cloud/www/cloud/firebase.js', 'utf8');
  var rules266 = fs.readFileSync('/home/hatch/workspace/android/checklist-cloud/firestore.rules', 'utf8');
  var a266ver = html.includes('Versión 2.5.16') && html.includes('Versión: 2.5.16') && !html.includes('2.5.15');
  var a266bundle = md5bundle266 === 'd8ad9d102d13ef69925d7bdab65b9e33';
  var a266fb = ['asignarFolioCarta', 'crearAcuse', 'subscribeAcuses', 'upsertAcuse', 'deleteAcuse', 'getAcuse', 'crearCarta', 'subscribeCartas', 'upsertCarta', 'deleteCarta', 'getCarta', 'foliosCarta'].every(function (f) { return fb266.includes(f); });
  var a266rules = rules266.includes('match /acuses/{id}') && rules266.includes('match /cartas/{id}') && rules266.includes('match /config/foliosCarta') && rules266.includes('request.resource.data.creadoPor == request.auth.uid');
  console.log('266A) versión 2.5.16:', a266ver, '| bundle nuevo (d8ad9d10…):', a266bundle, '| firebase.js con acuses/cartas/folio:', a266fb, '| reglas acuses/cartas/foliosCarta:', a266rules);
  // 266B: el Acuse empieza VACÍO (los datos del ejemplo no se
  // prellenan) y la fecha es la de hoy; la vista Carta existe.
  doLogin('usuario');
  showVista('acuse');
  var b266 = document.getElementById('viewAcuse').hidden === false && document.getElementById('viewCarta').hidden === true &&
    document.getElementById('fAc-para').value === '' && document.getElementById('fAc-de').value === '' && document.getElementById('fAc-anexo').value === '' &&
    document.getElementById('fAc-fecha').value === hoyISO();
  showVista('carta');
  var b266c = document.getElementById('viewCarta').hidden === false && document.getElementById('fCa-nombre').value === '' &&
    document.getElementById('fCa-ip').value === '' && document.getElementById('fCa-folio').value === '' &&
    html.includes('placeholder="Se asigna al guardar"');
  console.log('266B) acuse vacío por defecto y fecha de hoy:', b266, '| carta vacía, Ip vacía y folio "Se asigna al guardar":', b266c);
  // 266C: fecha larga del formato: "Septiembre 01, 2026".
  var c266 = fmtFechaLarga('2026-09-01') === 'Septiembre 01, 2026' && fmtFechaLarga('2026-01-05') === 'Enero 05, 2026' &&
    fmtFechaLarga('2026-12-31') === 'Diciembre 31, 2026' && fmtFechaLarga('') === '-' && fmtFechaLarga('2026-13-01') === '-';
  console.log('266C) fmtFechaLarga: Septiembre 01, 2026 y casos borde:', c266);
  // 266D: PDF del acuse (1 página carta) con fecha larga, PARA/DE/ANEXO
  // con los valores y bloque RECIBE con Nombre/Fecha/Firma.
  var a266d = { id: 'ac1', creadoEn: Date.now(), creadoPor: 'u1', creadoPorNombre: 'Test User', datos: { fecha: '2026-09-01', para: 'Beatriz Garduño Dominguez RH - Revolución', de: 'SISTEMAS', anexo: 'Documentacion' } };
  var pdf266d = await pdfStrOf266(buildPdfAcuse(a266d));
  var d266 = (pdf266d.match(/\\/Type \\/Page[^s]/g) || []).length === 1 && pdf266d.indexOf('/MediaBox [0 0 612 792]') !== -1 &&
    pdf266d.indexOf('Septiembre 01, 2026') !== -1 && pdf266d.indexOf('PARA:') !== -1 && pdf266d.indexOf('Beatriz Gardu') !== -1 &&
    pdf266d.indexOf('DE:') !== -1 && pdf266d.indexOf('SISTEMAS') !== -1 && pdf266d.indexOf('ANEXO:') !== -1 &&
    pdf266d.indexOf('Documentacion') !== -1 && pdf266d.indexOf('RECIBE:') !== -1 && pdf266d.indexOf('Nombre:') !== -1 &&
    pdf266d.indexOf('Firma:') !== -1;
  console.log('266D) PDF acuse: 1 página carta, fecha larga, PARA/DE/ANEXO y RECIBE:', d266);
  // 266E: validación del acuse: sin Para/De no guarda y marca en rojo;
  // con datos guarda en local y aparece en la lista.
  CLOUD_ENABLED = false;
  showVista('acuse');
  document.getElementById('fAc-fecha').value = '2026-09-01';
  document.getElementById('fAc-para').value = '';
  document.getElementById('fAc-de').value = '';
  var ok266e1 = await acuseGuardar();
  var e266val = ok266e1 === false && toastTxt().indexOf('Faltan datos obligatorios') !== -1 && document.getElementById('fAc-para').classList.contains('campo-falta');
  document.getElementById('fAc-para').value = 'Beatriz Garduño Dominguez RH - Revolución';
  document.getElementById('fAc-de').value = 'SISTEMAS';
  document.getElementById('fAc-anexo').value = 'Documentacion';
  var n266eBefore = acuses.length;
  var ok266e2 = await acuseGuardar();
  var saved266e = acuses[acuses.length - 1];
  var e266save = ok266e2 === true && acuses.length === n266eBefore + 1 && saved266e.datos.para === 'Beatriz Garduño Dominguez RH - Revolución' &&
    saved266e.datos.de === 'SISTEMAS' && document.getElementById('acuseList').innerHTML.indexOf('Beatriz Gardu') !== -1 &&
    toastTxt().indexOf('Acuse guardado') !== -1;
  console.log('266E) validación: sin Para/De no guarda y marca en rojo:', e266val, '| con datos guarda en local y en lista:', e266save);
  // 266F: carta con nube mockeada: crearCarta asigna el folio 00042
  // (5 dígitos, como lo haría la transacción asignarFolioCarta en
  // config/foliosCarta) y el folio queda visible en el formulario.
  CLOUD_ENABLED = true;
  doLogin('usuario');
  showVista('carta');
  document.getElementById('fCa-fecha').value = '2026-09-01';
  document.getElementById('fCa-nombre').value = 'Juan Pérez López';
  document.getElementById('fCa-colaborador').value = '12345';
  document.getElementById('fCa-sucursal').value = 'Polanco';
  document.getElementById('fCa-puesto').value = 'Técnico';
  document.getElementById('fCa-jefe').value = 'María García';
  document.getElementById('fCa-ip').value = '192.168.1.50';
  document.getElementById('fCa-observaciones').value = 'Sin observaciones';
  cartaEqFilas = [{ modelo: 'Latitude 5420', marca: 'Dell', serie: 'ABC123', concepto: 'Laptop' }];
  cartaEqRender();
  var crear266f = [];
  global.Cloud.crearCarta = async function (datos, nombre) { crear266f.push([datos, nombre]); return { id: 'CARTA-266F', folio: '00042' }; };
  var ok266f = await cartaGuardar();
  var saved266f = cartas.find(function (x) { return x.id === 'CARTA-266F'; });
  var f266 = ok266f === true && crear266f.length === 1 && crear266f[0][0].nombre === 'Juan Pérez López' && crear266f[0][0].equipos.length === 1 &&
    crear266f[0][1] === 'Test User' && !!saved266f && saved266f.folio === '00042' && /^\\d{5}$/.test(saved266f.folio) &&
    document.getElementById('fCa-folio').value === '00042' && toastTxt().indexOf('folio 00042') !== -1 &&
    fb266.indexOf("doc(db, 'config', 'foliosCarta')") !== -1 && fb266.indexOf("String(n).padStart(5, '0')") !== -1 &&
    fb266.indexOf('runTransaction') !== -1;
  CLOUD_ENABLED = false;
  console.log('266F) carta: folio 00042 (5 dígitos) vía crearCarta y visible en el formulario:', f266);
  // 266G: filas de equipo: empieza con 1, agregar → 2, quitar → 1
  // (queda la segunda); sin equipo con modelo o serie no guarda.
  cartaLimpiarForm();
  var g266a = cartaEqFilas.length === 1;
  cartaEqAddRow();
  var g266b = cartaEqFilas.length === 2;
  cartaEqFilas[0] = { modelo: 'Latitude 5420', marca: 'Dell', serie: 'ABC123', concepto: 'Laptop' };
  cartaEqFilas[1] = { modelo: 'OptiPlex 7010', marca: 'Dell', serie: 'DEF456', concepto: 'CPU' };
  cartaEqRemoveRow(0);
  var g266c = cartaEqFilas.length === 1 && cartaEqFilas[0].serie === 'DEF456';
  cartaEqFilas = [{ modelo: '', marca: '', serie: '', concepto: '' }];
  document.getElementById('fCa-nombre').value = 'Juan Pérez López';
  CLOUD_ENABLED = false;
  var ok266g = await cartaGuardar();
  var g266d = ok266g === false && toastTxt().indexOf('Faltan datos obligatorios') !== -1;
  console.log('266G) filas: 1 → agregar 2 → quitar 1 (queda la segunda):', g266a && g266b && g266c, '| sin equipo con modelo/serie no guarda:', g266d);
  // 266H: PDF de la carta: 2 páginas carta, encabezado FO-SI-10,
  // campos, tabla de equipos, texto legal verbatim y 2 firmas.
  var c266h = { id: 'CARTA-266H', folio: '00042', creadoEn: Date.now(), creadoPor: 'u1', creadoPorNombre: 'Test User', datos: { fecha: '2026-09-01', nombre: 'Juan Pérez López', colaborador: '12345', sucursal: 'Polanco', puesto: 'Técnico', jefe: 'María García', ip: '192.168.1.50', observaciones: 'Sin observaciones', equipos: [{ modelo: 'Latitude 5420', marca: 'Dell', serie: 'ABC123', concepto: 'Laptop' }, { modelo: 'OptiPlex 7010', marca: 'Dell', serie: 'DEF456', concepto: 'CPU' }] } };
  var pdf266h = await pdfStrOf266(buildPdfCarta(c266h));
  var rows266h = pdfTextRows(pdf266h);
  var txt266h = rows266h.map(function (r) { return r.t; }).join(' ');
  var h266 = (pdf266h.match(/\\/Type \\/Page[^s]/g) || []).length === 2 && pdf266h.indexOf('/MediaBox [0 0 612 792]') !== -1 &&
    pdf266h.indexOf('FO-SI-10') !== -1 && pdf266h.indexOf('Versión: 3') !== -1 && pdf266h.indexOf('25-sep-23') !== -1 &&
    pdf266h.indexOf('Página: 1 de 2') !== -1 && pdf266h.indexOf('Página: 2 de 2') !== -1 &&
    pdf266h.indexOf('Juan P') !== -1 && pdf266h.indexOf('Polanco') !== -1 && pdf266h.indexOf('192.168.1.50') !== -1 &&
    pdf266h.indexOf('Latitude 5420') !== -1 && pdf266h.indexOf('ABC123') !== -1 && pdf266h.indexOf('OptiPlex 7010') !== -1 &&
    pdf266h.indexOf('DEF456') !== -1 && pdf266h.indexOf('FOLIO: 00042') !== -1 &&
    txt266h.indexOf('RESPONSABILIDADES DEL USUARIO RESGUARDATARIO') !== -1 &&
    txt266h.indexOf('presta sus servicios laborales para LAPI S.A. DE C.V.') !== -1 &&
    txt266h.indexOf('escritos,electrónicos') !== -1 &&
    txt266h.indexOf('Ley Federal de Protección de Datos Personales') !== -1 &&
    CARTA_RESPONSABILIDADES.length === 8 &&
    (pdf266h.match(/NOMBRE Y FIRMA DEL USUARIO/g) || []).length === 2;
  console.log('266H) PDF carta: 2 páginas carta, FO-SI-10, campos, equipos, texto legal verbatim y 2 firmas:', h266);
  // 266I: visibilidad: el usuario suscribe solo lo propio (uid u1) y
  // el admin todo (null); la tarjeta ajena no trae Eliminar para el
  // usuario y sí para el admin.
  var sub266i = [];
  global.Cloud.subscribeAcuses = function (cb, uidOp) { sub266i.push(['acuses', uidOp]); return function () {}; };
  global.Cloud.subscribeCartas = function (cb, uidOp) { sub266i.push(['cartas', uidOp]); return function () {}; };
  CLOUD_ENABLED = true;
  cloudAcuseUnsub = null; cloudCartaUnsub = null;
  doLogin('usuario');
  acuseSuscribir(); cartaSuscribir();
  var i266u = sub266i.length === 2 && sub266i[0][1] === 'u1' && sub266i[1][1] === 'u1';
  cloudAcuseUnsub = null; cloudCartaUnsub = null;
  sub266i.length = 0;
  doLogin('admin');
  acuseSuscribir(); cartaSuscribir();
  var i266a = sub266i.length === 2 && sub266i[0][1] === null && sub266i[1][1] === null;
  doLogin('usuario');
  var cardU266 = acuseCardHtml({ id: 'ax', creadoEn: Date.now(), creadoPor: 'u2', creadoPorNombre: 'Otro', datos: { fecha: '2026-09-01', para: 'Alguien', de: 'SISTEMAS', anexo: '' } });
  doLogin('admin');
  var cardA266 = acuseCardHtml({ id: 'ax', creadoEn: Date.now(), creadoPor: 'u2', creadoPorNombre: 'Otro', datos: { fecha: '2026-09-01', para: 'Alguien', de: 'SISTEMAS', anexo: '' } });
  var i266del = cardU266.indexOf('data-acuse-del') === -1 && cardA266.indexOf('data-acuse-del') !== -1;
  CLOUD_ENABLED = false;
  console.log('266I) visibilidad: usuario suscribe solo lo propio (u1):', i266u, '| admin suscribe todo (null):', i266a, '| Eliminar ajeno solo admin:', i266del);
  // 266J: reabrir un acuse guardado carga sus datos en el formulario;
  // eliminar con confirmación lo borra.
  CLOUD_ENABLED = false;
  doLogin('usuario');
  var saved266j = acuses[acuses.length - 1];
  acuseLimpiarForm();
  acuseListClick({ target: fakeListTarget266('data-acuse-open', saved266j.id) });
  var j266open = document.getElementById('fAc-para').value === 'Beatriz Garduño Dominguez RH - Revolución' && document.getElementById('fAc-de').value === 'SISTEMAS' && acuseEditId === saved266j.id;
  var n266jBefore = acuses.length;
  acuseListClick({ target: fakeListTarget266('data-acuse-del', saved266j.id) });
  answerConfirm(true);
  await sleep(10);
  var j266del = acuses.length === n266jBefore - 1 && !acuseFind(saved266j.id) && toastTxt().indexOf('Acuse eliminado') !== -1;
  console.log('266J) reabrir: carga los datos en el formulario:', j266open, '| eliminar con confirmación borra el acuse:', j266del);
  // 266K: compartir PDF: la carta por correo abre mailto con el folio
  // y descarga el PDF; por WhatsApp (sin share nativo) descarga el PDF
  // y avisa; el acuse por WhatsApp descarga su PDF.
  CLOUD_ENABLED = false;
  cartaLimpiarForm();
  document.getElementById('fCa-nombre').value = 'Juan Pérez López';
  cartaEqFilas = [{ modelo: 'Latitude 5420', marca: 'Dell', serie: 'ABC123', concepto: 'Laptop' }];
  var ok266k = await cartaGuardar();
  var c266k = cartas[cartas.length - 1];
  global.location.href = '';
  await cartaCompartirPdf(c266k, 'mail');
  var k266mail = ok266k === true && global.location.href.indexOf('mailto:?subject=') === 0 &&
    decodeURIComponent(global.location.href.split('subject=')[1].split('&')[0]).indexOf('Carta Responsiva folio ' + c266k.folio) !== -1;
  await cartaCompartirPdf(c266k, 'wa');
  var k266wa = toastTxt().indexOf('PDF descargado: carta-responsiva-' + c266k.folio + '.pdf') !== -1;
  var a266k = { id: 'ac-k', creadoEn: Date.now(), creadoPor: 'u1', creadoPorNombre: 'Test User', datos: { fecha: '2026-09-01', para: 'Beatriz Garduño Dominguez RH - Revolución', de: 'SISTEMAS', anexo: '' } };
  await acuseCompartirPdf(a266k, 'wa');
  var k266ac = toastTxt().indexOf('PDF descargado: acuse-sistemas-ac-k.pdf') !== -1;
  console.log('266K) compartir: carta por correo abre mailto con folio:', k266mail, '| carta por WhatsApp descarga el PDF:', k266wa, '| acuse por WhatsApp descarga su PDF:', k266ac);
  // 266L: modo local: el segundo folio es 00002 y ambas cartas quedan
  // en la lista local.
  cartaLimpiarForm();
  document.getElementById('fCa-nombre').value = 'Ana López';
  cartaEqFilas = [{ modelo: 'X1', marca: 'Lenovo', serie: 'ZZ9', concepto: 'Laptop' }];
  var ok266l = await cartaGuardar();
  var c266l = cartas[cartas.length - 1];
  var l266 = ok266l === true && c266l.folio === '00002' &&
    document.getElementById('cartaList').innerHTML.indexOf('Folio 00002') !== -1 &&
    document.getElementById('cartaList').innerHTML.indexOf('Folio 00001') !== -1;
  console.log('266L) modo local: segundo folio 00002, ambas cartas en la lista:', l266);
"""
rep("  process.exit(0);\n})();\n", serie266 + "\n  process.exit(0);\n})();\n")

open(P, 'w', encoding='utf-8').write(s)
print('test20266.js generado')
