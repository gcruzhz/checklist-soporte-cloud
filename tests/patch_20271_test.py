# Parche de pruebas 2.5.21: test20270.js -> test20271.js.
# 1) Extrae el <script> actual de www/index.html a
# tests/checklist20271.js. 2) Copia test20270.js a test20271.js y
# actualiza la versión (2.5.20 -> 2.5.21, 2.5.19 -> 2.5.20, n270 ->
# n271, mailto 270 -> 271). 3) firebase.js NO cambia en 2.5.21: el
# bundle sigue c4fb1cce…, así que las etiquetas de 265A–270A vuelven
# de «bundle nuevo 2.5.21» a «bundle sin cambio». 4) Agrega la serie
# 271 (6 casos): versión y registro del plugin Printer; ruta nativa
# Android (printPdf, sin iframe ni window.print); Printer falla ->
# FileOpener; sin Printer ni FileOpener -> Share; web/escritorio
# conserva iframe+print(); Filesystem falla -> false con toast.
# Uso: python3 patch_20271_test.py (corre desde tests/)
import os
import shutil

BASE = '/home/hatch/workspace/android/checklist-cloud'
TESTS = os.path.join(BASE, 'tests')
SRC = os.path.join(TESTS, 'test20270.js')
P = os.path.join(TESTS, 'test20271.js')

# --- Extraer el <script> actual de www/index.html.
html = open(os.path.join(BASE, 'www/index.html'), encoding='utf-8').read()
i = html.index('<script>', html.index('firebase-config'))
j = html.index('</script>', i)
open(os.path.join(TESTS, 'checklist20271.js'), 'w', encoding='utf-8').write(html[i + len('<script>'):j])
print('checklist20271.js extraido:', j - i - len('<script>'), 'bytes')

shutil.copyfile(SRC, P)
s = open(P, encoding='utf-8').read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'NO ENCONTRADO x%d (esperado %d): %r' % (c, n, old[:120])
    s = s.replace(old, new)


def repall(old, new):
    global s
    c = s.count(old)
    print('repall %r -> %r: %d ocurrencias' % (old[:60], new[:60], c))
    s = s.replace(old, new)


# --- SRC y versión 2.5.21.
rep("const SRC = fs.readFileSync(__dirname + '/checklist20270.js', 'utf8');",
    "const SRC = fs.readFileSync(__dirname + '/checklist20271.js', 'utf8');")
repall('2.5.20', '2.5.21')
repall('2.5.19', '2.5.20')
repall('n270', 'n271')
repall('Soporte 270', 'Soporte 271')
repall('mailto 270', 'mailto 271')
# --- El contador n271: el regex lleva la versión con backslashes
# escapados, así que repall no lo toca (como en 2.5.20): hay que
# cambiarlo explícito de contar 2.5.20 a contar 2.5.21.
BS = chr(92)
rep("var n271 = (html.match(/2" + BS + ".5" + BS + ".20/g) || []).length;",
    "var n271 = (html.match(/2" + BS + ".5" + BS + ".21/g) || []).length;")

# --- Bundle SIN cambio en 2.5.21 (firebase.js no se tocó): el md5
# sigue c4fb1cce…; las etiquetas que repall dejó como «nuevo 2.5.21»
# vuelven a «sin cambio».
repall('bundle nuevo 2.5.21 (c4fb1cce…)', 'bundle sin cambio (c4fb1cce…)')
repall('bundle NUEVO 2.5.21', 'bundle SIN cambio 2.5.20')
rep("  // (firebase.js CAMBIÓ en 2.5.21: crearAcuse ya no asigna folio;",
    "  // (firebase.js no cambió en 2.5.21; el cambio de 2.5.20 sigue:\n  // crearAcuse ya no asigna folio;")

SERIE271 = '''
  // 271: impresión nativa en Android (2.5.21): el botón ya NO usa
  // iframe+print() en el teléfono (el WebView lo ignora); usa
  // Printer.printPdf con el PDF guardado en CACHE, con fallback
  // FileOpener/Share; en web se conserva el iframe.
  // 271A: versión 2.5.21 en los 2 sitios, sin 2.5.20; plugin Printer
  // 8.1.11 registrado (package.json, capacitor.plugins.json,
  // cap-plugins/printer-plugin.js, script en el HTML, gradle 75).
  var pkg271 = JSON.parse(fs.readFileSync('/home/hatch/workspace/android/checklist-cloud/package.json', 'utf8'));
  var plugins271 = JSON.parse(fs.readFileSync('/home/hatch/workspace/android/checklist-cloud/android/app/src/main/assets/capacitor.plugins.json', 'utf8'));
  var gradle271 = fs.readFileSync('/home/hatch/workspace/android/checklist-cloud/android/app/build.gradle', 'utf8');
  var printerJs271 = '';
  try { printerJs271 = fs.readFileSync('/home/hatch/workspace/android/checklist-cloud/www/cap-plugins/printer-plugin.js', 'utf8'); } catch (e) {}
  var a271reg = pkg271.dependencies && pkg271.dependencies['@capgo/capacitor-printer'] === '^8.1.11' &&
    plugins271.some(function (p) { return p.pkg === '@capgo/capacitor-printer' && p.classpath === 'com.capgo.printer.PrinterPlugin'; }) &&
    printerJs271.indexOf("registerPlugin('Printer'") !== -1 &&
    html.indexOf('cap-plugins/printer-plugin.js') !== -1 &&
    gradle271.indexOf('versionCode 75') !== -1 && gradle271.indexOf('versionName "2.5.21"') !== -1;
  var a271ver = html.includes('Versión 2.5.21') && html.includes('Versión: 2.5.21') && !html.includes('2.5.20') && n271 === 2;
  var a271src = html.indexOf('imprimirPdfNativo') !== -1 && html.indexOf('imprimirPdfWeb') !== -1 &&
    html.indexOf('Printer.printPdf') !== -1 && html.indexOf("directory: 'CACHE'") !== -1;
  console.log('271A) versión 2.5.21 en 2 sitios, sin 2.5.20:', a271ver, '| plugin Printer 8.1.11 registrado (package.json, capacitor.plugins.json, cap-plugins, gradle 75):', a271reg, '| rutas nativa/web en la app:', a271src);
  // Stubs Capacitor-Android para 271B–271D y 271F: Filesystem guarda
  // en CACHE y devuelve URI, Printer/FileOpener/Share registran.
  global.FileReader = global.FileReader || class { constructor() { this.result = null; } readAsDataURL(blob) { var self = this; blob.arrayBuffer().then(function (ab) { self.result = 'data:application/pdf;base64,' + Buffer.from(ab).toString('base64'); if (self.onload) self.onload(); }); } };
  var calls271 = { write: [], printPdf: [], open: [], share: [] };
  var iframe271 = 0;
  var wprint271 = [];
  var origCreate271 = document.createElement;
  var hadPrint271 = ('print' in global);
  var origPrint271 = global.print;
  global.print = function () { wprint271.push('print'); };
  document.createElement = function (tag) { if (tag === 'iframe') iframe271++; return origCreate271(tag); };
  function capAndroid271(printerFn) {
    global.Capacitor = { getPlatform: function () { return 'android'; }, Plugins: {
      Filesystem: { writeFile: async function (o) { calls271.write.push(o); return { uri: 'file:///cache/' + o.path }; },
        stat: async function () { return { uri: 'file:///cache/x.pdf', size: 123 }; } },
      Printer: { printPdf: printerFn || (async function (o) { calls271.printPdf.push(o); }) },
      FileOpener: { open: async function (o) { calls271.open.push(o); } },
      Share: { share: async function (o) { calls271.share.push(o); } }
    } };
  }
  var a271 = { id: 'ACUSE-271', creadoEn: Date.now(), creadoPor: 'u1', creadoPorNombre: 'Test User', datos: { fecha: '2026-09-01', para: 'Beatriz Garduño Dominguez RH - Revolución', de: 'SISTEMAS', anexo: '' } };
  // 271B: Android con Printer: guarda el PDF en CACHE y llama a
  // printPdf con su URI; NO crea iframe, NO llama a window.print(),
  // NO abre FileOpener ni Share; devuelve true.
  capAndroid271();
  var ok271b = await imprimirPdfDoc(acusePdfBlob(a271));
  var b271 = ok271b === true && calls271.write.length === 1 && calls271.write[0].path === 'acuse-sistemas-ACUSE-271.pdf' &&
    calls271.write[0].directory === 'CACHE' && !!calls271.write[0].data &&
    calls271.printPdf.length === 1 && calls271.printPdf[0].path === 'file:///cache/acuse-sistemas-ACUSE-271.pdf' &&
    calls271.printPdf[0].name === 'acuse-sistemas-ACUSE-271' &&
    calls271.open.length === 0 && calls271.share.length === 0 && iframe271 === 0 && wprint271.length === 0;
  console.log('271B) Android con Printer: guarda en CACHE y printPdf con la URI:', b271, '| sin iframe:', iframe271 === 0, '| sin window.print:', wprint271.length === 0, '| sin FileOpener/Share:', calls271.open.length === 0 && calls271.share.length === 0);
  // 271C: el botón Imprimir de la Carta (formulario) con Printer que
  // falla: cae a FileOpener con el PDF guardado; sin iframe ni print().
  calls271.write.length = 0; calls271.printPdf.length = 0; calls271.open.length = 0; calls271.share.length = 0;
  capAndroid271(async function (o) { calls271.printPdf.push(o); throw new Error('sin servicio de impresión'); });
  CLOUD_ENABLED = false;
  doLogin('usuario');
  showVista('carta');
  cartaLimpiarForm();
  document.getElementById('fCa-nombre').value = 'Juan Pérez López';
  cartaEqFilas = [{ modelo: 'Latitude 5420', marca: 'Dell', serie: 'ABC123', concepto: 'Laptop' }];
  document.getElementById('btnCartaImprimir')._h.click[0]();
  await sleep(100);
  var c271 = calls271.printPdf.length === 1 && calls271.open.length === 1 &&
    calls271.open[0].contentType === 'application/pdf' && String(calls271.open[0].filePath).indexOf('file:///cache/carta-responsiva-') === 0 &&
    String(calls271.open[0].filePath).slice(-4) === '.pdf' && calls271.share.length === 0 &&
    iframe271 === 0 && wprint271.length === 0;
  console.log('271C) botón Carta con Printer fallido: abre FileOpener con el PDF:', c271, '| printPdf intentado 1 vez:', calls271.printPdf.length === 1, '| sin iframe ni window.print:', iframe271 === 0 && wprint271.length === 0);
  // 271D: sin Printer ni FileOpener: cae a Share con la URI del PDF.
  calls271.write.length = 0; calls271.printPdf.length = 0; calls271.open.length = 0; calls271.share.length = 0;
  capAndroid271();
  delete global.Capacitor.Plugins.Printer;
  delete global.Capacitor.Plugins.FileOpener;
  var ok271d = await imprimirPdfDoc(acusePdfBlob(a271));
  var d271 = ok271d === true && calls271.share.length === 1 && calls271.share[0].url === 'file:///cache/acuse-sistemas-ACUSE-271.pdf' &&
    iframe271 === 0 && wprint271.length === 0;
  console.log('271D) Android sin Printer ni FileOpener: comparte el PDF con Share:', d271, '| sin iframe ni window.print:', iframe271 === 0 && wprint271.length === 0);
  // 271E: sin Capacitor (web/escritorio) se conserva el iframe oculto
  // + window.print() del botón Imprimir del Acuse (formulario).
  delete global.Capacitor;
  var printed271e = [];
  var iframe271e = null;
  document.createElement = function (tag) {
    if (tag === 'iframe') {
      iframe271e = { tagName: 'IFRAME', style: {}, src: '', parentNode: null,
        contentWindow: { focus: function () {}, print: function () { printed271e.push('print'); } } };
      return iframe271e;
    }
    return origCreate271(tag);
  };
  CLOUD_ENABLED = false;
  doLogin('usuario');
  showVista('acuse');
  document.getElementById('fAc-para').value = 'Beatriz Garduño Dominguez RH - Revolución';
  document.getElementById('fAc-de').value = 'SISTEMAS';
  document.getElementById('btnAcuseImprimir')._h.click[0]();
  var e271a = !!iframe271e && iframe271e.src === 'blob:x';
  if (iframe271e && iframe271e.onload) iframe271e.onload();
  var e271b = printed271e.length === 1;
  var e271btns = html.indexOf('id="btnAcuseImprimir"') !== -1 && html.indexOf('id="btnCartaImprimir"') !== -1 &&
    html.indexOf('🖨️ Imprimir') !== -1 && html.indexOf('data-acuse-print') !== -1 && html.indexOf('data-carta-print') !== -1 &&
    (document.getElementById('btnAcuseImprimir')._h.click || []).length === 1 &&
    (document.getElementById('btnCartaImprimir')._h.click || []).length === 1;
  document.createElement = origCreate271;
  console.log('271E) web/escritorio: botón Acuse abre iframe del PDF:', e271a, '| y llama a print():', e271b, '| botones Imprimir en Carta y Acuse (formulario y lista) cableados:', e271btns);
  // 271F: si ni siquiera se puede guardar el PDF (Filesystem falla),
  // imprimirPdfDoc devuelve false, avisa con toast y NO usa iframe
  // ni window.print() (no promete un «guardado» que no ocurrió).
  document.createElement = function (tag) { if (tag === 'iframe') iframe271++; return origCreate271(tag); };
  global.Capacitor = { getPlatform: function () { return 'android'; }, Plugins: {
    Filesystem: { writeFile: async function () { throw new Error('sin almacenamiento'); } },
    Printer: { printPdf: async function (o) { calls271.printPdf.push(o); } },
    FileOpener: { open: async function (o) { calls271.open.push(o); } },
    Share: { share: async function (o) { calls271.share.push(o); } }
  } };
  var n271w = calls271.write.length, n271p = calls271.printPdf.length, n271o = calls271.open.length, n271s = calls271.share.length;
  var ok271f = await imprimirPdfDoc(acusePdfBlob(a271));
  var f271 = ok271f === false && calls271.write.length === n271w && calls271.printPdf.length === n271p &&
    calls271.open.length === n271o && calls271.share.length === n271s && iframe271 === 0 && wprint271.length === 0 &&
    document.getElementById('toast').textContent.indexOf('No se pudo abrir la impresión.') !== -1 &&
    document.getElementById('toast').textContent.indexOf('quedó guardado') === -1;
  document.createElement = origCreate271;
  if (hadPrint271) global.print = origPrint271; else delete global.print;
  delete global.Capacitor;
  console.log('271F) Filesystem falla: devuelve false con toast, sin prometer guardado:', f271, '| sin iframe ni window.print:', iframe271 === 0 && wprint271.length === 0);
'''

rep("\n  process.exit(0);\n})();\n", SERIE271 + "\n  process.exit(0);\n})();\n")

open(P, 'w', encoding='utf-8').write(s)
print('test20271.js generado')
