# Parche web 2.5.21: botón Imprimir roto en el teléfono (raíz: el
# WebView de Android ignora window.print() y no renderiza PDFs en
# iframes, así que el iframe+print() de 2.5.20 era un no-op silencioso).
# Nueva ruta nativa: Filesystem (CACHE) + @capgo/capacitor-printer
# (PrintManager de Android, printPdf) con fallback FileOpener/Share;
# en escritorio/navegador se conserva iframe+window.print().
# Uso: python3 patch_20271_web.py (corre desde tests/)
import os

BASE = '/home/hatch/workspace/android/checklist-cloud'
P = os.path.join(BASE, 'www/index.html')
G = os.path.join(BASE, 'android/app/build.gradle')
s = open(P, encoding='utf-8').read()
g = open(G, encoding='utf-8').read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'NO ENCONTRADO x%d (esperado %d): %r' % (c, n, old[:140])
    s = s.replace(old, new)


def repg(old, new, n=1):
    global g
    c = g.count(old)
    assert c == n, 'GRADLE NO ENCONTRADO x%d (esperado %d): %r' % (c, n, old[:140])
    g = g.replace(old, new)


# --- Versión 2.5.20 -> 2.5.21 (2 sitios) y serie mailto 270 -> 271.
rep('Versión 2.5.20', 'Versión 2.5.21')
rep('Versión: 2.5.20', 'Versión: 2.5.21')
rep('Checklist de Soporte 270', 'Checklist de Soporte 271')
rep('Versión de la app: 270', 'Versión de la app: 271')

# --- Script del plugin de impresión (copia de
# node_modules/@capgo/capacitor-printer/dist/plugin.js, mismo patrón
# que los demás cap-plugins/*.js; registrado en Android por cap sync).
rep('<script src="cap-plugins/camera-plugin.js"></script>',
    '<script src="cap-plugins/camera-plugin.js"></script>\n<script src="cap-plugins/printer-plugin.js"></script>')

# --- Reescritura de imprimirPdfDoc: 3 rutas según el entorno.
old = '''// (270) Imprimir el PDF generado (Carta y Acuse): se abre el PDF en
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
}'''
new = '''// (271) Imprimir el PDF generado (Carta y Acuse), 3 rutas según el
// entorno. La versión anterior usaba solo iframe+print() y en el teléfono no
// pasaba nada: el WebView de Android (Capacitor) ignora window.print()
// y no renderiza PDFs en iframes, así que contentWindow.print() es un
// no-op silencioso sin error. Ahora: (1) en Android/iOS nativo se
// guarda el PDF con Filesystem (CACHE) y se imprime con el plugin
// @capgo/capacitor-printer (PrintManager de Android, printPdf), que
// abre el diálogo de impresión del sistema; (2) si el plugin no está
// o falla, se abre el PDF guardado con FileOpener (el visor de PDF del
// sistema, que sí tiene Imprimir) y si tampoco hay visor se comparte
// con Share; en el teléfono NUNCA se usa el iframe. (3) En escritorio
// (Electron) y en el navegador se conserva el iframe oculto +
// window.print(), que ahí sí funciona. La impresión en una impresora
// física real sigue pendiente de prueba por Gerardo.
async function imprimirPdfDoc(out) {
  try {
    var Plugins = window.Capacitor && window.Capacitor.Plugins;
    var platform = 'web';
    try { if (window.Capacitor && window.Capacitor.getPlatform) platform = window.Capacitor.getPlatform(); } catch (e) {}
    if ((platform === 'android' || platform === 'ios') && Plugins && Plugins.Filesystem) {
      var resNat = await imprimirPdfNativo(out, Plugins);
      if (resNat === 'ok') return true;
      if (resNat === 'guardado') showToast('No se pudo abrir la impresión, pero el PDF quedó guardado; ábrelo desde tus archivos para imprimirlo.');
      else showToast('No se pudo abrir la impresión.');
      return false;
    }
    return imprimirPdfWeb(out);
  } catch (e) {
    showToast('No se pudo abrir la impresión.');
    return false;
  }
}
// (271) Ruta nativa: guarda el PDF en CACHE, lo imprime con
// Printer.printPdf y, si eso falla o el plugin no está, lo abre con
// FileOpener (visor del sistema) o lo comparte con Share. Devuelve
// 'ok' si alguna vía abrió algo, 'guardado' si el archivo quedó
// guardado pero nada pudo abrirlo, false si ni siquiera se pudo
// guardar (el llamador avisa con el toast que corresponde a cada caso).
async function imprimirPdfNativo(out, Plugins) {
  var uri = '';
  try {
    var base64 = await blobToBase64(out.blob);
    var saved = await Plugins.Filesystem.writeFile({ path: out.name, data: base64, directory: 'CACHE' });
    uri = (saved && saved.uri) || '';
    if (!uri) {
      var st = await Plugins.Filesystem.stat({ path: out.name, directory: 'CACHE' });
      uri = (st && st.uri) || '';
    }
  } catch (e) { return false; }
  if (!uri) return false;
  var jobName = String(out.name || 'documento').replace(/\\.pdf$/i, '');
  if (Plugins.Printer && Plugins.Printer.printPdf) {
    try { await Plugins.Printer.printPdf({ name: jobName, path: uri }); return 'ok'; } catch (eP) {}
  }
  if (Plugins.FileOpener) {
    try { await Plugins.FileOpener.open({ filePath: uri, contentType: 'application/pdf' }); return 'ok'; } catch (eF) {}
  }
  if (Plugins.Share) {
    try { await Plugins.Share.share({ title: 'Checklist de Soporte', text: 'PDF para imprimir: ' + out.name, url: uri, dialogTitle: 'Imprimir PDF' }); return 'ok'; } catch (eS) {}
  }
  return 'guardado';
}
// (271) Ruta escritorio/navegador: iframe oculto + print(), como en
// En Electron window.print() sí abre el diálogo del sistema.
function imprimirPdfWeb(out) {
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
}'''
rep(old, new)

# --- build.gradle: versionCode 74 -> 75, versionName 2.5.20 -> 2.5.21.
repg('versionCode 74', 'versionCode 75')
repg('versionName "2.5.20"', 'versionName "2.5.21"')

open(P, 'w', encoding='utf-8').write(s)
open(G, 'w', encoding='utf-8').write(g)
print('www/index.html y android/app/build.gradle parcheados a 2.5.21')
