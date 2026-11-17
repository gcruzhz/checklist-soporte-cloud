# Reparación 2.5.0e2: el paso 2 del parche 20250e tomó el primer
# 'var W = 595...' (dentro de assemblePdf) en vez del de buildPdf.
# Restaura assemblePdf y aplica el reemplazo solo dentro de buildPdf.
import io

P = '/home/hatch/workspace/android/checklist-cloud/www/index.html'
s = io.open(P, encoding='utf-8').read()

BROKEN = """function assemblePdf(rows, images) {
  images = images || {};
  return assemblePdf(rows);
}"""
assert s.count(BROKEN) == 1, 'stub roto no encontrado'

FULL = r'''function assemblePdf(rows, images) {
  images = images || {};
  var W = 595, H = 842, M = 48, usable = H - M * 2;
  var pages = [], cur = [], y = 0;
  function rowH(r) { return r.s * 1.45 + (r.img ? r.img.h + 6 : 0); }
  rows.forEach(function (r) {
    var lh = rowH(r);
    if (y + lh > usable && cur.length) { pages.push(cur); cur = []; y = 0; }
    cur.push(r); y += lh;
  });
  if (cur.length) pages.push(cur);
  var objs = [];
  objs[1] = '<< /Type /Catalog /Pages 2 0 R >>';
  var kidRefs = [];
  var nextId = 5;
  var imgIds = {};
  Object.keys(images).forEach(function (name) {
    var im = images[name];
    if (!im || !im.bytes) return;
    imgIds[name] = nextId++;
  });
  pages.forEach(function (pg) {
    var contentId = nextId++, pageId = nextId++;
    var cs = '';
    var yy = H - M;
    pg.forEach(function (r) {
      var lh = r.s * 1.45;
      var imgH = r.img ? r.img.h + 6 : 0;
      yy -= (lh + imgH);
      cs += 'BT /' + r.f + ' ' + r.s + ' Tf ' + M + ' ' + (yy + imgH).toFixed(1) + ' Td (' + pdfEsc(r.t) + ') Tj ET\n';
      if (r.img && imgIds[r.img.name]) {
        cs += 'q ' + r.img.w + ' 0 0 ' + r.img.h + ' ' + M + ' ' + yy.toFixed(1) + ' cm /Im' + r.img.name + ' Do Q\n';
      }
    });
    objs[contentId] = '<< /Length ' + pdfBytes(cs).length + ' >>\nstream\n' + cs + '\nendstream';
    var res = '<< /Font << /F1 3 0 R /F2 4 0 R >>';
    var xobjs = Object.keys(imgIds).map(function (n) { return '/Im' + n + ' ' + imgIds[n] + ' 0 R'; }).join(' ');
    if (xobjs) res += ' /XObject << ' + xobjs + ' >>';
    res += ' >>';
    objs[pageId] = '<< /Type /Page /Parent 2 0 R /MediaBox [0 0 ' + W + ' ' + H + '] /Resources ' + res + ' /Contents ' + contentId + ' 0 R >>';
    kidRefs.push(pageId + ' 0 R');
  });
  Object.keys(imgIds).forEach(function (name) {
    var im = images[name];
    objs[imgIds[name]] = '<< /Type /XObject /Subtype /Image /Width ' + im.w + ' /Height ' + im.h + ' /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length ' + im.bytes.length + ' >>\nstream\n' + binStrFromBytes(im.bytes) + '\nendstream';
  });
  objs[2] = '<< /Type /Pages /Kids [' + kidRefs.join(' ') + '] /Count ' + pages.length + ' >>';
  objs[3] = '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>';
  objs[4] = '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>';
  var pdf = '%PDF-1.4\n';
  var offsets = [0];
  for (var i = 1; i < nextId; i++) {
    offsets[i] = pdfBytes(pdf).length;
    pdf += i + ' 0 obj\n' + objs[i] + '\nendobj\n';
  }
  var xrefPos = pdfBytes(pdf).length;
  var n = nextId;
  pdf += 'xref\n0 ' + n + '\n';
  pdf += '0000000000 65535 f \n';
  for (var j = 1; j < n; j++) {
    pdf += ('0000000000' + offsets[j]).slice(-10) + ' 00000 n \n';
  }
  pdf += 'trailer\n<< /Size ' + n + ' /Root 1 0 R >>\nstartxref\n' + xrefPos + '\n%%EOF';
  return new Blob([pdfBytes(pdf)], { type: 'application/pdf' });
}'''

s = s.replace(BROKEN, FULL)

# Ahora la cola de buildPdf: buscar el marcador DESPUÉS de 'function buildPdf'.
bp = s.index('function buildPdf(prep) {')
start = s.index('  var W = 595, H = 842, M = 48, usable = H - M * 2;', bp)
end = s.index("  return new Blob([pdfBytes(pdf)], { type: 'application/pdf' });\n}", start) + len("  return new Blob([pdfBytes(pdf)], { type: 'application/pdf' });\n}")
s = s[:start] + '  return assemblePdf(rows);\n}' + s[end:]

# Verificación: buildPdf ya no tiene su cola vieja; assemblePdf está completo.
assert s.count('function assemblePdf(rows, images)') == 1
assert s.count('return assemblePdf(rows);') == 1
assert 'binStrFromBytes(im.bytes)' in s
io.open(P, 'w', encoding='utf-8').write(s)
print('reparación 2.5.0e2 OK')
