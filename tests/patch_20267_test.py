# Parche de pruebas 2.5.17: test20266.js -> test20267.js.
# 1) Extrae el <script> actual de www/index.html a
# tests/checklist20267.js (el JavaScript de esta version, que evalua el
# harness). 2) Copia test20266.js a test20267.js y actualiza la version
# (2.5.16 -> 2.5.17, 2.5.15 -> 2.5.16, n266 -> n267, mailto 266 ->
# 267). 3) Actualiza la serie 266 al comportamiento nuevo: 266A ya no
# dice "bundle nuevo" (el bundle NO cambia en 2.5.17, md5 d8ad9d10…);
# 266C/266D usan la fecha nueva "1 de Septiembre de 2026"; 266H lee
# "Versión: 3" y "Página: 1 de 2" del texto unido (la tabla Código
# ahora tiene etiqueta y valor en dos ops). 4) Agrega la serie 267 (6
# casos): versión 2.5.17 + bundle sin cambio + logo Lapi en repo y
# base64; PDF del acuse con los datos de la captura del formato real
# ("30 de Octubre de 2026", Satelite/SISTEMAS/Bam); estructura visual
# del PDF del acuse (logo /ImLapi, línea naranja 2.5 pt, caja gris
# 0.93, RECIBE 0.75, F4 Helvetica-BoldOblique); PARA largo en 2
# líneas y 1 página; Carta re-verificada (logo, Código con bordes,
# verde #9BBB59, Área, fecha nueva); campo Área en el formulario
# (guardar/limpiar/reabrir).
# Uso: python3 patch_20267_test.py (corre desde tests/)
import os
import shutil

BASE = '/home/hatch/workspace/android/checklist-cloud'
TESTS = os.path.join(BASE, 'tests')
SRC = os.path.join(TESTS, 'test20266.js')
P = os.path.join(TESTS, 'test20267.js')
LOGO_MD5 = 'b9f5fb0c610a42aa47332a07d622f4c3'
BUNDLE_MD5 = 'd8ad9d102d13ef69925d7bdab65b9e33'

# --- Extraer el <script> actual de www/index.html.
html = open(os.path.join(BASE, 'www/index.html'), encoding='utf-8').read()
i = html.index('<script>', html.index('firebase-config'))
j = html.index('</script>', i)
open(os.path.join(TESTS, 'checklist20267.js'), 'w', encoding='utf-8').write(html[i + len('<script>'):j])
print('checklist20267.js extraido:', j - i - len('<script>'), 'bytes')

shutil.copyfile(SRC, P)
s = open(P, encoding='utf-8').read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'NO ENCONTRADO x%d (esperado %d): %r' % (c, n, old[:120])
    s = s.replace(old, new)


def repall(old, new, n):
    rep(old, new, n)


# --- SRC y version 2.5.17 (orden: primero 2.5.16 -> 2.5.17, luego
# 2.5.15 -> 2.5.16 para las referencias a la version anterior).
rep("const SRC = fs.readFileSync(__dirname + '/checklist20266.js', 'utf8');",
    "const SRC = fs.readFileSync(__dirname + '/checklist20267.js', 'utf8');")
repall("2.5.16", "2.5.17", 27)
repall("2.5.15", "2.5.16", 13)
repall("n266", "n267", 7)
repall("Soporte 266", "Soporte 267", 3)
repall("mailto 266", "mailto 267", 5)
# El regex lleva la versión con barras escapadas: el reemplazo plano
# de "2.5.16" no lo toca, hay que actualizarlo aparte.
BS = chr(92)
rep("var n267 = (html.match(/2" + BS + ".5" + BS + ".16/g) || []).length;",
    "var n267 = (html.match(/2" + BS + ".5" + BS + ".17/g) || []).length;")

# --- 266A: el bundle NO cambia en 2.5.17 (sigue d8ad9d10…).
rep("  // 266A: versión 2.5.17 en los 2 sitios, mailto 267, bundle nuevo",
    "  // 266A: versión 2.5.17 en los 2 sitios, mailto 267, bundle sin cambio")
rep("console.log('266A) versión 2.5.17:', a266ver, '| bundle nuevo (d8ad9d10…):'",
    "console.log('266A) versión 2.5.17:', a266ver, '| bundle sin cambio (d8ad9d10…):'")

# --- 266C/266D: fecha larga nueva "1 de Septiembre de 2026". ---
rep("  // 266C: fecha larga del formato: \"Septiembre 01, 2026\".",
    "  // 266C: fecha larga del formato: \"1 de Septiembre de 2026\" (2.5.17: \"día de Mes de año\").")
rep("  var c266 = fmtFechaLarga('2026-09-01') === 'Septiembre 01, 2026' && fmtFechaLarga('2026-01-05') === 'Enero 05, 2026' &&\n    fmtFechaLarga('2026-12-31') === 'Diciembre 31, 2026' && fmtFechaLarga('') === '-' && fmtFechaLarga('2026-13-01') === '-';",
    "  var c266 = fmtFechaLarga('2026-09-01') === '1 de Septiembre de 2026' && fmtFechaLarga('2026-01-05') === '5 de Enero de 2026' &&\n    fmtFechaLarga('2026-12-31') === '31 de Diciembre de 2026' && fmtFechaLarga('2026-10-30') === '30 de Octubre de 2026' && fmtFechaLarga('') === '-' && fmtFechaLarga('2026-13-01') === '-';")
rep("console.log('266C) fmtFechaLarga: Septiembre 01, 2026 y casos borde:', c266);",
    "console.log('266C) fmtFechaLarga: 1 de Septiembre de 2026 y casos borde:', c266);")
rep("pdf266d.indexOf('Septiembre 01, 2026') !== -1",
    "pdf266d.indexOf('1 de Septiembre de 2026') !== -1")

# --- 266H: "Versión: 3" y "Página: 1 de 2" ahora se leen del texto
# unido (la tabla Código tiene etiqueta y valor en dos ops). ---
rep("pdf266h.indexOf('Versión: 3') !== -1",
    "txt266h.indexOf('Versión: 3') !== -1")
rep("pdf266h.indexOf('Página: 1 de 2') !== -1",
    "txt266h.indexOf('Página: 1 de 2') !== -1")

# --- Serie 267 nueva, antes de process.exit(0). ---
serie267 = """
  // 267: serie nueva — PDF del Acuse como el formato real (2.5.17):
  // logo Lapi, título "ACUSE DE RECIBO", línea naranja, fecha en
  // español largo, tabla RECIBE gris; Carta re-verificada (logo,
  // tabla Código con bordes, encabezado verde, campo Área).
  async function pdfStrOf267(blob) { return Buffer.from(await blob.arrayBuffer()).toString('latin1'); }
  CLOUD_ENABLED = false;
  // 267A: versión 2.5.17 en los 2 sitios, bundle SIN cambio
  // (md5 d8ad9d10…), logo Lapi en www/assets + base64 en el script.
  var crypto267 = require('crypto');
  var bundle267 = fs.readFileSync('/home/hatch/workspace/android/checklist-cloud/www/cloud/firebase.bundle.js');
  var md5bundle267 = crypto267.createHash('md5').update(bundle267).digest('hex');
  var logo267 = fs.readFileSync('/home/hatch/workspace/android/checklist-cloud/www/assets/logo-lapi.jpg');
  var md5logo267 = crypto267.createHash('md5').update(logo267).digest('hex');
  var a267ver = html.includes('Versión 2.5.17') && html.includes('Versión: 2.5.17') && !html.includes('2.5.16');
  var a267bundle = md5bundle267 === 'BUNDLE_MD5';
  var a267logo = md5logo267 === 'LOGO_MD5' && html.includes('LOGO_LAPI_JPEG_B64') && html.includes('www/assets/logo-lapi.jpg');
  var img267 = logoLapiImg();
  var a267img = !!img267 && img267.w === 276 && img267.h === 161 && img267.bytes && img267.bytes.length === logo267.length;
  console.log('267A) versión 2.5.17:', a267ver, '| bundle sin cambio (d8ad9d10…):', a267bundle, '| logo Lapi en repo + base64:', a267logo, '| logoLapiImg() 276x161:', a267img);
  // 267B: PDF del acuse con los datos de la captura del formato real:
  // fecha "30 de Octubre de 2026", PARA "Satelite (RECEPCION)", DE
  // "SISTEMAS", ANEXO "Bam"; sin el formato viejo en inglés.
  var a267b = { id: 'ac267', creadoEn: Date.now(), creadoPor: 'u1', creadoPorNombre: 'Test User', datos: { fecha: '2026-10-30', para: 'Satelite (RECEPCION)', de: 'SISTEMAS', anexo: 'Bam' } };
  var pdf267b = await pdfStrOf267(buildPdfAcuse(a267b));
  var b267 = (pdf267b.match(/PAGE_RE) || []).length === 1 && pdf267b.indexOf('/MediaBox [0 0 612 792]') !== -1 &&
    pdf267b.indexOf('30 de Octubre de 2026') !== -1 && pdf267b.indexOf('Noviembre 25, 2026') === -1 &&
    pdf267b.indexOf('Satelite') !== -1 && pdf267b.indexOf('RECEPCION') !== -1 &&
    pdf267b.indexOf('SISTEMAS') !== -1 && pdf267b.indexOf('Bam') !== -1 &&
    pdf267b.indexOf('ACUSE DE RECIBO') !== -1 && pdf267b.indexOf('RECIBE:') !== -1 &&
    pdf267b.indexOf('Nombre:') !== -1 && pdf267b.indexOf('Fecha:') !== -1 && pdf267b.indexOf('Firma:') !== -1;
  console.log('267B) PDF acuse real: fecha 30 de Octubre de 2026, Satelite/SISTEMAS/Bam, título y RECIBE:', b267);
  // 267C: el PDF del acuse lleva el logo como imagen JPEG, la línea
  // naranja de 2.5 pt, la caja gris del título y la tabla RECIBE gris;
  // usa Helvetica-BoldOblique (F4) en PARA/DE/ANEXO y RECIBE.
  var c267 = pdf267b.indexOf('/ImLapi Do') !== -1 && pdf267b.indexOf('/Subtype /Image') !== -1 &&
    pdf267b.indexOf('/DCTDecode') !== -1 && pdf267b.indexOf('1 0.4 0 RG') !== -1 &&
    pdf267b.indexOf('2.5 w') !== -1 && pdf267b.indexOf('0.93 g') !== -1 &&
    pdf267b.indexOf('0.75 g') !== -1 && pdf267b.indexOf('/F4 6 0 R') !== -1 &&
    pdf267b.indexOf('/BaseFont /Helvetica-BoldOblique') !== -1 &&
    pdf267b.indexOf('/F4 24 Tf') !== -1 && pdf267b.indexOf('/F4 11 Tf') !== -1;
  console.log('267C) PDF acuse: logo /ImLapi, línea naranja 2.5 pt, caja gris 0.93, RECIBE 0.75, F4:', c267);
  // 267D: PARA largo ("Beatriz Garduño Dominguez RH - Revolución") se
  // parte en 2 líneas sin salirse de la página; fecha nueva.
  var a267d = { id: 'ac267d', creadoEn: Date.now(), creadoPor: 'u1', creadoPorNombre: 'Test User', datos: { fecha: '2026-09-01', para: 'Beatriz Garduño Dominguez RH - Revolución', de: 'SISTEMAS', anexo: '' } };
  var pdf267d = await pdfStrOf267(buildPdfAcuse(a267d));
  var rows267d = pdfTextRows(pdf267d);
  var txt267d = rows267d.map(function (r) { return r.t; }).join(' ');
  var d267 = (pdf267d.match(/PAGE_RE) || []).length === 1 &&
    txt267d.indexOf('Beatriz Gardu') !== -1 && txt267d.indexOf('Revolución') !== -1 &&
    txt267d.indexOf('1 de Septiembre de 2026') !== -1 &&
    pdf267d.indexOf('ANEXO:') !== -1;
  console.log('267D) PARA largo en 2 líneas, 1 página, fecha nueva:', d267);
  // 267E: PDF de la carta re-verificado contra el original: logo
  // /ImLapi, tabla Código con bordes y negritas, encabezado verde
  // #9BBB59, campo Área con su valor y fecha en español largo.
  var c267e = { id: 'CARTA-267E', folio: '00043', creadoEn: Date.now(), creadoPor: 'u1', creadoPorNombre: 'Test User', datos: { fecha: '2026-09-01', nombre: 'Juan Pérez López', colaborador: '12345', sucursal: 'Polanco', puesto: 'Técnico', area: 'Sistemas', jefe: 'María García', ip: '192.168.1.50', observaciones: 'Sin observaciones', equipos: [{ modelo: 'Latitude 5420', marca: 'Dell', serie: 'ABC123', concepto: 'Laptop' }] } };
  var pdf267e = await pdfStrOf267(buildPdfCarta(c267e));
  var rows267e = pdfTextRows(pdf267e);
  var txt267e = rows267e.map(function (r) { return r.t; }).join(' ');
  var e267 = (pdf267e.match(/PAGE_RE) || []).length === 2 &&
    pdf267e.indexOf('/ImLapi Do') !== -1 &&
    txt267e.indexOf('Código: FO-SI-10') !== -1 && txt267e.indexOf('Versión: 3') !== -1 &&
    txt267e.indexOf('Fecha de actualización: 25-sep-23') !== -1 && txt267e.indexOf('Página: 1 de 2') !== -1 &&
    pdf267e.indexOf('0.608 0.733 0.349 rg') !== -1 &&
    txt267e.indexOf('Área:') !== -1 && pdf267e.indexOf('Sistemas') !== -1 &&
    txt267e.indexOf('1 de Septiembre de 2026') !== -1 &&
    txt267e.indexOf('FOLIO: 00043') !== -1;
  console.log('267E) PDF carta: logo, Código con bordes, verde #9BBB59, Área y fecha nueva:', e267);
  // 267F: el campo Área del formulario se lee al guardar, se limpia
  // con Limpiar y se recarga al reabrir la carta guardada.
  doLogin('usuario');
  showVista('carta');
  cartaLimpiarForm();
  document.getElementById('fCa-nombre').value = 'Juan Pérez López';
  document.getElementById('fCa-area').value = 'Sistemas';
  cartaEqFilas = [{ modelo: 'Latitude 5420', marca: 'Dell', serie: 'ABC123', concepto: 'Laptop' }];
  var ok267f = await cartaGuardar();
  var saved267f = cartas[cartas.length - 1];
  var f267a = ok267f === true && !!saved267f && saved267f.datos.area === 'Sistemas';
  cartaLimpiarForm();
  var f267b = document.getElementById('fCa-area').value === '';
  cartaCargarEnForm(saved267f);
  var f267c = document.getElementById('fCa-area').value === 'Sistemas' && document.getElementById('fCa-nombre').value === 'Juan Pérez López';
  console.log('267F) Área: se guarda:', f267a, '| Limpiar la vacía:', f267b, '| reabrir la recarga:', f267c);

"""
serie267 = serie267.replace('BUNDLE_MD5', BUNDLE_MD5).replace('LOGO_MD5', LOGO_MD5)
serie267 = serie267.replace('PAGE_RE', chr(92) + '/Type ' + chr(92) + '/Page[^s]/g')
assert 'PAGE_RE' not in serie267 and 'BUNDLE_MD5' not in serie267 and 'LOGO_MD5' not in serie267
assert s.count('  process.exit(0);') == 1, 'ancla process.exit no única'
s = s.replace('  process.exit(0);', serie267 + '  process.exit(0);', 1)

open(P, 'w', encoding='utf-8').write(s)
print('test20267.js escrito:', len(s), 'bytes')
