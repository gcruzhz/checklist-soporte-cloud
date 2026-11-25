# Parche web 2.5.17: PDF del Acuse Sistemas como el formato real y
# re-verificación del PDF de la Carta Responsiva FO-SI-10.
# 1) Motor de PDF (assemblePdfOps): fuentes F3 Helvetica-Oblique y F4
# Helvetica-BoldOblique (la negrita cursiva del Acuse: PARA/DE/ANEXO y
# etiquetas RECIBE); color en texto ('red', gris 0..1 o [r,g,b]),
# relleno RGB en rectángulos y grosor/color en líneas (línea naranja
# 2.5 pt, encabezado verde #9BBB59 de la Carta). Sin tocar assemblePdf
# (el viejo, de filas) ni buildPdfMant.
# 2) Logo Lapi como asset compartido: www/assets/logo-lapi.jpg
# (276x161, recortado del encabezado original FO-SI-10,
# word/media/image1.jpeg del docx) + base64 incrustado en
# www/index.html (LOGO_LAPI_JPEG_B64 + logoLapiImg()) para que el PDF
# lo lleve sin depender de fetch. El logo del docx del Acuse
# (image1.png, "Certificado ISO 9001:2000") es otra variante y NO se
# usa: el formato real de la captura es el de "Laboratorio Médico".
# 3) fmtFechaLarga: "30 de Octubre de 2026" (día sin cero + "de" + mes
# CON MAYÚSCULA + "de" + año), como el formato real; antes era
# "Septiembre 01, 2026". Afecta al Acuse, a la Carta ("Fecha de
# solicitud:") y a las tarjetas de la lista.
# 4) buildPdfAcuse reescrito como el formato real (medidas del docx +
# captura): márgenes izq 57 pt / der 38 pt; logo 94x55 pt + título
# "ACUSE DE RECIBO" en caja gris 0.93 + línea naranja 2.5 pt #F60;
# fecha a la derecha; PARA/DE en negrita cursiva 24 pt y ANEXO con
# valor en negrita cursiva 14 pt subrayado, con aire entre filas;
# tabla RECIBE de ancho completo con encabezado gris C0C0C0 (0.75) y
# 3 filas altas (54 pt) con la etiqueta en gris y la celda blanca
# vacía para escribir a mano.
# 5) buildPdfCarta: encabezado con el logo como imagen (mismo asset),
# tabla Código con bordes internos y etiquetas/valores en negrita
# (la fila "Fecha de actualización:" es más alta, con la etiqueta en
# 2 líneas, como el original); tabla "Exclusivo de Sistemas" con
# encabezado VERDE #9BBB59 (antes gris 0.88) y anchos del docx
# (Modelo 21.6%, Marca 21.6%, Número de serie 28.4%, Concepto 28.4%);
# campo nuevo "Área" (del original: "Puesto: ... Área: Jefe Directo:")
# en el formulario, en cartaLeerForm/cartaLimpiarForm/cartaCargarEnForm
# y en DATOS DEL SOLICITANTE. El texto legal sigue VERBATIM (8
# párrafos) y el PDF sigue en 2 páginas carta.
# 6) Versión 2.5.17 / versionCode 71 en www/index.html (login y Acerca
# de, mailto 266 -> 267), android/app/build.gradle e iOS
# (MARKETING_VERSION 2.5.17 / CURRENT_PROJECT_VERSION 71, Debug y
# Release). firebase.js NO cambia: el bundle queda igual
# (md5 d8ad9d102d13ef69925d7bdab65b9e33). firestore.rules NO cambia.
# Uso: python3 patch_20267_web.py [ruta-base-del-proyecto]
import base64
import hashlib
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '/home/hatch/workspace/android/checklist-cloud'
HTML = os.path.join(BASE, 'www/index.html')
GRADLE = os.path.join(BASE, 'android/app/build.gradle')
PBX = os.path.join(BASE, 'ios/App/App.xcodeproj/project.pbxproj')
LOGO = os.path.join(BASE, 'www/assets/logo-lapi.jpg')


def read(path):
    return open(path, encoding='utf-8').read()


def write(path, s):
    open(path, 'w', encoding='utf-8').write(s)


def rep(path, old, new, n=1):
    s = read(path)
    c = s.count(old)
    assert c == n, '%s: NO ENCONTRADO x%d (esperado %d): %r' % (path, c, n, old[:120])
    write(path, s.replace(old, new))


def rep_occ(path, old, new, occ):
    s = read(path)
    idxs = []
    i = s.find(old)
    while i != -1:
        idxs.append(i)
        i = s.find(old, i + 1)
    assert len(idxs) > occ, '%s: solo %d ocurrencias de %r (se pedía la #%d)' % (path, len(idxs), old[:80], occ)
    i = idxs[occ]
    write(path, s[:i] + new + s[i + len(old):])


def span_replace(path, start_marker, end_marker, new_text):
    s = read(path)
    assert s.count(start_marker) == 1, '%s: marcador inicial x%d: %r' % (path, s.count(start_marker), start_marker[:80])
    assert s.count(end_marker) == 1, '%s: marcador final x%d: %r' % (path, s.count(end_marker), end_marker[:80])
    a = s.index(start_marker)
    b = s.index(end_marker, a)
    assert b > a, '%s: marcador final antes que el inicial' % path
    write(path, s[:a] + new_text + s[b:])


# --- Logo: base64 desde el asset (se verifica el md5). ---
logo_bytes = open(LOGO, 'rb').read()
assert hashlib.md5(logo_bytes).hexdigest() == 'b9f5fb0c610a42aa47332a07d622f4c3', 'md5 del logo inesperado'
LOGO_B64 = base64.b64encode(logo_bytes).decode('ascii')
print('logo-lapi.jpg:', len(logo_bytes), 'bytes, base64:', len(LOGO_B64))

# --- Versión 2.5.17. ---
rep(HTML, '<p class="login-sub" style="font-size:11px;color:#999">Versión 2.5.16</p>',
    '<p class="login-sub" style="font-size:11px;color:#999">Versión 2.5.17</p>')
rep(HTML, '<div class="line">Versión: 2.5.16</div>',
    '<div class="line">Versión: 2.5.17</div>')
rep(HTML, 'Checklist de Soporte 266', 'Checklist de Soporte 267')
rep(HTML, 'Versión de la app: 266', 'Versión de la app: 267')
rep(GRADLE, 'versionCode 70', 'versionCode 71')
rep(GRADLE, 'versionName "2.5.16"', 'versionName "2.5.17"')
rep(PBX, 'CURRENT_PROJECT_VERSION = 70;', 'CURRENT_PROJECT_VERSION = 71;', 2)
rep(PBX, 'MARKETING_VERSION = 2.5.16;', 'MARKETING_VERSION = 2.5.17;', 2)

# --- fmtFechaLarga: "30 de Octubre de 2026". ---
rep(HTML, r'''// (266) Fecha larga del Acuse y la Carta, como en el formato original:
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
}''', r'''// (267) Fecha larga del Acuse y la Carta, como en el formato real:
// "30 de Octubre de 2026" (día sin cero + "de" + mes CON MAYÚSCULA +
// "de" + año). Acepta 'AAAA-MM-DD' (el valor del input date) o
// cualquier valor de fechaDe. Se parsea por partes para no depender
// de la zona horaria.
var MESES_ES = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
function fmtFechaLarga(v) {
  var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(v || ''));
  if (m) {
    var mi = Number(m[2]);
    if (mi < 1 || mi > 12) return '-';
    return Number(m[3]) + ' de ' + MESES_ES[mi - 1] + ' de ' + m[1];
  }
  var d = fechaDe(v);
  if (!d) return '-';
  return d.getDate() + ' de ' + MESES_ES[d.getMonth()] + ' de ' + d.getFullYear();
}''')

# --- Logo Lapi incrustado (base64), antes del ensamblador de PDF. ---
rep(HTML, r'''  if (cur) lines.push(cur);
  return lines.length ? lines : [''];
}
// Ensamblador de PDF (251): buildPdf y buildPdfMant comparten la''', r'''  if (cur) lines.push(cur);
  return lines.length ? lines : [''];
}
// (267) Logo Lapi para los PDFs del Acuse y la Carta: recortado del
// encabezado original FO-SI-10 (word/media/image1.jpeg del docx): "Lapi"
// naranja + "Salud Integral" + "Laboratorio Médico" teal. El archivo
// canónico es www/assets/logo-lapi.jpg (276x161, md5
// b9f5fb0c610a42aa47332a07d622f4c3); aquí va en base64 para que el PDF lo
// lleve incrustado sin depender de fetch (la app es un solo
// www/index.html y los tests de node evalúan este script). El logo del
// docx del Acuse (word/media/image1.png) es otra variante ("Certificado
// ISO 9001:2000") y NO se usa: el formato real que muestra la captura
// es el de "Laboratorio Médico".
var LOGO_LAPI_JPEG_B64 = 'LOGO_B64_PLACEHOLDER';
var LOGO_LAPI_W = 276, LOGO_LAPI_H = 161;
var _logoLapiImg = null;
function logoLapiImg() {
  if (_logoLapiImg) return _logoLapiImg;
  try {
    var bin = atob(LOGO_LAPI_JPEG_B64);
    var bytes = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    _logoLapiImg = { bytes: bytes, w: LOGO_LAPI_W, h: LOGO_LAPI_H };
  } catch (e) { _logoLapiImg = null; }
  return _logoLapiImg;
}
// Ensamblador de PDF (251): buildPdf y buildPdfMant comparten la'''.replace('LOGO_B64_PLACEHOLDER', LOGO_B64))

# --- Motor de PDF: comentario de operaciones. ---
rep(HTML, r'''// Operaciones: {k:'t', x, y, f, s, str, a, color} texto (y = línea base
// desde abajo; a = 'C' centrado en x, 'R' borde derecho en x, color 'red');
// {k:'r', x, y, w, h, fill} rectángulo (y = borde inferior; fill = gris
// 0..1 o null, siempre con borde); {k:'ln', x1, y1, x2, y2} línea;
// {k:'img', name, x, y, w, h} imagen (y = borde inferior).''', r'''// Operaciones: {k:'t', x, y, f, s, str, a, color} texto (y = línea base
// desde abajo; a = 'C' centrado en x, 'R' borde derecho en x;
// color: 'red', gris 0..1 o [r, g, b] 0..1); {k:'r', x, y, w, h, fill}
// rectángulo (y = borde inferior; fill = gris 0..1, [r, g, b] o null,
// siempre con borde); {k:'ln', x1, y1, x2, y2, w, color} línea
// (w = grosor en pt, por defecto 0.6; color como en 't');
// {k:'img', name, x, y, w, h} imagen (y = borde inferior).
// (267) Fuentes F3 Helvetica-Oblique y F4 Helvetica-BoldOblique para
// la negrita cursiva del Acuse (PARA/DE/ANEXO y etiquetas RECIBE).''')

# --- Motor de PDF: nextId 5 -> 7 (fuentes F3/F4 en 5 y 6). ---
rep(HTML, r'''function assemblePdfOps(pages, images, pageSize) {
  images = images || {};
  var W = (pageSize && pageSize.w) || 595, H = (pageSize && pageSize.h) || 842;
  var objs = [];
  objs[1] = '<< /Type /Catalog /Pages 2 0 R >>';
  var kidRefs = [];
  var nextId = 5;''', r'''function assemblePdfOps(pages, images, pageSize) {
  images = images || {};
  var W = (pageSize && pageSize.w) || 595, H = (pageSize && pageSize.h) || 842;
  var objs = [];
  objs[1] = '<< /Type /Catalog /Pages 2 0 R >>';
  var kidRefs = [];
  var nextId = 7;''')

# --- Motor de PDF: color en texto. ---
rep(HTML, r'''        if (op.color === 'red') cs += '1 0 0 rg ';
        cs += 'BT /' + op.f + ' ' + op.s + ' Tf ' + tx.toFixed(1) + ' ' + op.y.toFixed(1) + ' Td (' + pdfEsc(op.str) + ') Tj ET\n';
        if (op.color === 'red') cs += '0 g\n';''', r'''        if (op.color === 'red') cs += '1 0 0 rg ';
        else if (typeof op.color === 'number') cs += op.color + ' g ';
        else if (Array.isArray(op.color)) cs += op.color.join(' ') + ' rg ';
        cs += 'BT /' + op.f + ' ' + op.s + ' Tf ' + tx.toFixed(1) + ' ' + op.y.toFixed(1) + ' Td (' + pdfEsc(op.str) + ') Tj ET\n';
        if (op.color != null) cs += '0 g\n';''')

# --- Motor de PDF: relleno RGB en rectángulos. ---
rep(HTML, r'''      } else if (op.k === 'r') {
        if (op.fill != null) cs += op.fill + ' g ' + op.x.toFixed(1) + ' ' + op.y.toFixed(1) + ' ' + op.w.toFixed(1) + ' ' + op.h.toFixed(1) + ' re f\n0 g\n';
        cs += '0.6 w ' + op.x.toFixed(1) + ' ' + op.y.toFixed(1) + ' ' + op.w.toFixed(1) + ' ' + op.h.toFixed(1) + ' re S\n';''', r'''      } else if (op.k === 'r') {
        if (op.fill != null) {
          if (Array.isArray(op.fill)) cs += op.fill.join(' ') + ' rg ';
          else cs += op.fill + ' g ';
          cs += op.x.toFixed(1) + ' ' + op.y.toFixed(1) + ' ' + op.w.toFixed(1) + ' ' + op.h.toFixed(1) + ' re f\n0 g\n';
        }
        cs += '0.6 w ' + op.x.toFixed(1) + ' ' + op.y.toFixed(1) + ' ' + op.w.toFixed(1) + ' ' + op.h.toFixed(1) + ' re S\n';''')

# --- Motor de PDF: grosor y color en líneas. ---
rep(HTML, r'''      } else if (op.k === 'ln') {
        cs += '0.6 w ' + op.x1.toFixed(1) + ' ' + op.y1.toFixed(1) + ' m ' + op.x2.toFixed(1) + ' ' + op.y2.toFixed(1) + ' l S\n';''', r'''      } else if (op.k === 'ln') {
        cs += (op.w || 0.6) + ' w ';
        if (Array.isArray(op.color)) cs += op.color.join(' ') + ' RG ';
        else if (typeof op.color === 'number') cs += op.color + ' G ';
        cs += op.x1.toFixed(1) + ' ' + op.y1.toFixed(1) + ' m ' + op.x2.toFixed(1) + ' ' + op.y2.toFixed(1) + ' l S\n';
        if (op.color != null) cs += '0 G\n';''')

# --- Motor de PDF: F3/F4 en los recursos (2ª ocurrencia: assemblePdfOps). ---
rep_occ(HTML, r'''    var res = '<< /Font << /F1 3 0 R /F2 4 0 R >>';''',
        r'''    var res = '<< /Font << /F1 3 0 R /F2 4 0 R /F3 5 0 R /F4 6 0 R >>';''', 1)

# --- Motor de PDF: objetos de fuente F3/F4 (2ª ocurrencia). ---
rep_occ(HTML, r'''  objs[3] = '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>';
  objs[4] = '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>';''',
        r'''  objs[3] = '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>';
  objs[4] = '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>';
  objs[5] = '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Oblique /Encoding /WinAnsiEncoding >>';
  objs[6] = '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-BoldOblique /Encoding /WinAnsiEncoding >>';''', 1)

# --- buildPdfAcuse reescrito como el formato real. ---
ACUSE_NUEVO = r'''// (267) PDF del Acuse Sistemas (1 página carta) como el formato real:
// encabezado con el logo Lapi (imagen) + "ACUSE DE RECIBO" en caja gris
// + línea naranja; fecha a la derecha en español largo ("30 de Octubre
// de 2026"); PARA/DE en negrita cursiva 24 pt y ANEXO con valor en
// negrita cursiva 14 pt subrayado, con aire entre filas; tabla RECIBE
// de ancho completo con encabezado gris C0C0C0 y 3 filas altas con la
// etiqueta en gris y la celda blanca vacía para escribir a mano.
// Medidas del original (docx + captura): márgenes izq 57 pt / der 38 pt,
// logo 111x65 pt, caja del título 235x30 pt, línea naranja 2.5 pt.
function buildPdfAcuse(a) {
  var d = (a && a.datos) || {};
  var W = 612, H = 792, USABLE = H - 14;
  var ML = 57, X1 = 574, CW = X1 - ML;
  var pages = [[]];
  var yt = 0;
  function cur() { return pages[pages.length - 1]; }
  function need(h) { if (yt + h > USABLE) { pages.push([]); yt = 0; } }
  function py(ytop) { return H - ytop; }
  function T(str, x, ytop, f, s, color, align) {
    cur().push({ k: 't', x: x, y: py(ytop) - (s || 9) * 0.8, f: f || 'F1', s: s || 9, str: pdfSafe(str), color: color || null, a: align || 'L' });
  }
  function R(x, ytop, w, h, fill) {
    cur().push({ k: 'r', x: x, y: py(ytop) - h, w: w, h: h, fill: (fill == null ? null : fill) });
  }
  function LN(x1, y1, x2, y2, w, color) { cur().push({ k: 'ln', x1: x1, y1: py(y1), x2: x2, y2: py(y2), w: w || null, color: color || null }); }
  function IMG(name, x, ytop, w, h) { cur().push({ k: 'img', name: name, x: x, y: py(ytop) - h, w: w, h: h }); }
  function wrapLines(str, w, s) {
    return wrapText(pdfSafe(str), Math.max(10, Math.floor(w / ((s || 9) * 0.5))));
  }
  function val(v) { return (v == null || v === '') ? '-' : String(v); }
  var ORANGE = [1, 0.4, 0];
  var TITULO_GRIS = [0.35, 0.35, 0.35];
  // Encabezado: logo Lapi a la izquierda y título en caja gris.
  var logo = logoLapiImg();
  if (logo) IMG('Lapi', 90, 8, 111, 65);
  R(249, 43, 235, 30, 0.93);
  T('ACUSE DE RECIBO', 367, 47, 'F2', 22, TITULO_GRIS, 'C');
  // Línea naranja bajo el encabezado, ancho del contenido.
  LN(ML, 102, 552, 102, 2.5, ORANGE);
  // Fecha arriba, a la derecha, en español largo.
  T(fmtFechaLarga(d.fecha), X1, 118, 'F1', 11, null, 'R');
  // PARA / DE / ANEXO: etiquetas a la izquierda, valores desde x=170.
  yt = 171;
  function filaAcuse(label, value, labelFont, labelSize, valueFont, valueSize, underline) {
    var lines = wrapLines(val(value), 404, valueSize);
    var lh = valueSize === 24 ? 29 : 17;
    var h = lines.length * lh;
    need(h);
    var y0 = yt;
    T(label, ML, y0, labelFont, labelSize);
    lines.forEach(function (ln, i) {
      T(ln, 170, y0 + i * lh, valueFont, valueSize);
      if (underline) LN(170, y0 + i * lh + valueSize * 0.8 + 2, 170 + pdfTextWidth(ln, valueFont, valueSize), y0 + i * lh + valueSize * 0.8 + 2);
    });
    return h;
  }
  var hP = filaAcuse('PARA:', d.para, 'F4', 24, 'F4', 24, false);
  yt += hP + 38;
  var hD = filaAcuse('DE:', d.de, 'F4', 24, 'F4', 24, false);
  yt += hD + 26;
  filaAcuse('ANEXO:', d.anexo, 'F1', 14, 'F4', 14, true);
  yt += 17 + 37;
  // Tabla RECIBE: encabezado gris C0C0C0 (0.75) y 3 filas altas.
  need(44 + 3 * 54);
  var y0 = yt;
  R(ML, y0, CW, 44, 0.75);
  T('RECIBE:', 315, y0 + 12, 'F2', 20, null, 'C');
  yt = y0 + 44;
  ['Nombre:', 'Fecha:', 'Firma:'].forEach(function (lab) {
    var yy = yt;
    R(ML, yy, 76, 54, 0.75);
    R(ML + 76, yy, CW - 76, 54, null);
    T(lab, ML + 6, yy + 21, 'F4', 11);
    yt += 54;
  });
  return assemblePdfOps(pages, { Lapi: logo }, { w: 612, h: 792 });
}
'''
span_replace(HTML,
             '// (266) PDF del Acuse Sistemas (1 página carta): fecha larga arriba,',
             '// (266) Texto legal de la Carta Responsiva FO-SI-10, VERBATIM del',
             ACUSE_NUEVO)

# --- buildPdfCarta: comentario actualizado. ---
rep(HTML, r'''// (266) PDF de la Carta Responsiva (2 páginas carta): p1 con el
// encabezado fijo del formato (Lapi / Laboratorio Médico, título y
// tabla Código FO-SI-10, Versión 3, Fecha de actualización 25-sep-23,
// Página 1 de 2), Datos del solicitante, tabla Exclusivo de Sistemas y
// Nombre y firma del usuario; p2 con las responsabilidades verbatim y
// la firma final. No hay asset de logo Lapi en el repo: el encabezado
// se reproduce con texto.''', r'''// (267) PDF de la Carta Responsiva (2 páginas carta): p1 con el
// encabezado fijo del formato (logo Lapi como imagen — el mismo asset
// que el Acuse —, título y tabla Código FO-SI-10, Versión 3, Fecha de
// actualización 25-sep-23, Página 1 de 2, con bordes y negritas),
// Datos del solicitante (con Área), tabla Exclusivo de Sistemas con
// encabezado VERDE #9BBB59 y Nombre y firma del usuario; p2 con las
// responsabilidades verbatim y la firma final.''')

# --- buildPdfCarta: ayudantes LN con grosor/color + IMG. ---
rep(HTML, r'''  function LN(x1, y1, x2, y2) { cur().push({ k: 'ln', x1: x1, y1: py(y1), x2: x2, y2: py(y2) }); }
  function wrapLines(str, w, s) {
    return wrapText(pdfSafe(str), Math.max(10, Math.floor(w / ((s || 9) * 0.5))));
  }
  function val(v) { return (v == null || v === '') ? '-' : String(v); }
  function campo(label, value, x, ytop, w) {''', r'''  function LN(x1, y1, x2, y2, w, color) { cur().push({ k: 'ln', x1: x1, y1: py(y1), x2: x2, y2: py(y2), w: w || null, color: color || null }); }
  function IMG(name, x, ytop, w, h) { cur().push({ k: 'img', name: name, x: x, y: py(ytop) - h, w: w, h: h }); }
  function wrapLines(str, w, s) {
    return wrapText(pdfSafe(str), Math.max(10, Math.floor(w / ((s || 9) * 0.5))));
  }
  function val(v) { return (v == null || v === '') ? '-' : String(v); }
  function campo(label, value, x, ytop, w) {''')

# --- buildPdfCarta: encabezado con logo + tabla Código con bordes. ---
rep(HTML, r'''  need(66);
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
  yt += 66 + 6;''', r'''  need(66);
  var y0 = yt;
  var logoC = logoLapiImg();
  if (logoC) IMG('Lapi', 36, y0, 94, 55);
  var tit = wrapText('CARTA RESPONSIVA PARA RESGUARDO Y USO DE EQUIPO DE CÓMPUTO', 30);
  tit.forEach(function (ln, i) { T(ln, 306, y0 + 2 + i * 12, 'F2', 10, null, 'C'); });
  // Tabla Código (2 columnas, como el original): etiquetas en negrita a
  // la izquierda, valores en negrita centrados. La fila de "Fecha de
  // actualización:" es más alta porque la etiqueta va en 2 líneas.
  var codX0 = 420, codX1 = 503, codX2 = 576;
  var codTops = [y0, y0 + 13.5, y0 + 27, y0 + 50.5];
  var codBot = y0 + 64;
  R(codX0, y0, codX2 - codX0, 64, null);
  LN(codX1, y0, codX1, codBot);
  codTops.slice(1).forEach(function (yy) { LN(codX0, yy, codX2, yy); });
  T('Código:', codX0 + 5, codTops[0] + 3, 'F2', 8);
  T('FO-SI-10', (codX1 + codX2) / 2, codTops[0] + 3, 'F2', 8, null, 'C');
  T('Versión:', codX0 + 5, codTops[1] + 3, 'F2', 8);
  T('3', (codX1 + codX2) / 2, codTops[1] + 3, 'F2', 8, null, 'C');
  T('Fecha de', codX0 + 5, codTops[2] + 2, 'F2', 8);
  T('actualización:', codX0 + 5, codTops[2] + 11.5, 'F2', 8);
  T('25-sep-23', (codX1 + codX2) / 2, codTops[2] + 7, 'F2', 8, null, 'C');
  T('Página:', codX0 + 5, codTops[3] + 3, 'F2', 8);
  T('1 de 2', (codX1 + codX2) / 2, codTops[3] + 3, 'F2', 8, null, 'C');
  yt += 66 + 6;''')

# --- buildPdfCarta: Datos del solicitante con Área. ---
rep(HTML, r'''    [['Jefe Directo:', d.jefe, 540]]''', r'''    [['Área:', d.area, 264], ['Jefe Directo:', d.jefe, 264]]''')

# --- buildPdfCarta: Exclusivo de Sistemas, anchos del docx. ---
rep(HTML, r'''  var cols = [
    ['Modelo', 36, 150], ['Marca', 186, 120], ['Número de serie', 306, 150], ['Concepto', 456, 120]
  ];''', r'''  // Anchos del original (docx): Modelo 21.6%, Marca 21.6%,
  // Número de serie 28.4%, Concepto 28.4% de 540 pt.
  var cols = [
    ['Modelo', 36, 117], ['Marca', 153, 117], ['Número de serie', 270, 153], ['Concepto', 423, 153]
  ];''')
rep(HTML, r'''  R(36, y0, 540, 16, 0.88);''', r'''  // (267) Encabezado VERDE #9BBB59 del original (antes gris 0.88).
  R(36, y0, 540, 16, [0.608, 0.733, 0.349]);''')
rep(HTML, r'''    T(String(eq.modelo || '-').slice(0, 28), 40, y0 + 3, 'F1', 8);
    T(String(eq.marca || '-').slice(0, 22), 190, y0 + 3, 'F1', 8);
    T(String(eq.serie || '-').slice(0, 28), 310, y0 + 3, 'F1', 8);
    T(String(eq.concepto || '-').slice(0, 22), 460, y0 + 3, 'F1', 8);''', r'''    T(String(eq.modelo || '-').slice(0, 24), 40, y0 + 3, 'F1', 8);
    T(String(eq.marca || '-').slice(0, 22), 157, y0 + 3, 'F1', 8);
    T(String(eq.serie || '-').slice(0, 30), 274, y0 + 3, 'F1', 8);
    T(String(eq.concepto || '-').slice(0, 30), 427, y0 + 3, 'F1', 8);''')

# --- buildPdfCarta: el PDF lleva el logo (ya solo queda su return). ---
rep(HTML, r'''  return assemblePdfOps(pages, {}, { w: 612, h: 792 });''',
    r'''  return assemblePdfOps(pages, { Lapi: logoLapiImg() }, { w: 612, h: 792 });''')

# --- Formulario de Carta: campo Área (del original). ---
rep(HTML, r'''      <div class="field"><label>Puesto</label><input id="fCa-puesto" placeholder="Puesto"></div>''',
    r'''      <div class="field"><label>Puesto</label><input id="fCa-puesto" placeholder="Puesto"></div>
      <div class="field"><label>Área</label><input id="fCa-area" placeholder="Área"></div>''')
rep(HTML, r'''puesto: v('fCa-puesto').trim(), jefe:''',
    r'''puesto: v('fCa-puesto').trim(), area: v('fCa-area').trim(), jefe:''')
rep(HTML, r'''['fCa-nombre', 'fCa-colaborador', 'fCa-sucursal', 'fCa-puesto', 'fCa-jefe', 'fCa-ip', 'fCa-observaciones']''',
    r'''['fCa-nombre', 'fCa-colaborador', 'fCa-sucursal', 'fCa-puesto', 'fCa-area', 'fCa-jefe', 'fCa-ip', 'fCa-observaciones']''')
rep(HTML, r'''  set('fCa-puesto', d.puesto);
  set('fCa-jefe', d.jefe);''', r'''  set('fCa-puesto', d.puesto);
  set('fCa-area', d.area);
  set('fCa-jefe', d.jefe);''')

print('patch_20267_web OK')
