# Parche 2.5.0e: www/index.html — assemblePdf (buildPdf lo reutiliza),
# showVista con 'inicio'/'mant', suscripción de mantenimientos al entrar,
# selector al abrir (login y modo local), logout y applyRoleUI.
import io

P = '/home/hatch/workspace/android/checklist-cloud/www/index.html'
s = io.open(P, encoding='utf-8').read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'NO ENCONTRADO o repetido (%d): %r' % (c, old[:100])
    s = s.replace(old, new)

ASSEMBLE = r'''// Ensamblador de PDF (2.5.0): buildPdf y buildPdfMant comparten la
// paginación y el xref. Las filas pueden llevar una imagen JPEG
// (r.img = {name, w, h} en puntos): el texto va arriba y la imagen debajo,
// en el mismo bloque, sin partirse entre páginas. images = {nombre:
// {bytes, w, h}} con bytes JPEG.
function binStrFromBytes(bytes) {
  var s = '';
  var CH = 8192;
  for (var i = 0; i < bytes.length; i += CH) {
    var chunk = [];
    for (var j = i; j < Math.min(i + CH, bytes.length); j++) chunk.push(bytes[j]);
    s += String.fromCharCode.apply(null, chunk);
  }
  return s;
}
function assemblePdf(rows, images) {
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
}
'''

# 1. Insertar assemblePdf antes de buildPdf.
rep("function buildPdf(prep) {", ASSEMBLE + "function buildPdf(prep) {")

# 2. buildPdf: su cola de paginación pasa a ser assemblePdf(rows).
start = s.index("  var W = 595, H = 842, M = 48, usable = H - M * 2;")
end = s.index("  return new Blob([pdfBytes(pdf)], { type: 'application/pdf' });\n}", start) + len("  return new Blob([pdfBytes(pdf)], { type: 'application/pdf' });\n}")
s = s[:start] + "  return assemblePdf(rows);\n}" + s[end:]
print('buildPdf -> assemblePdf OK')

# 3. showVista con inicio y mant.
rep("""// Menu de 3 secciones.
function showVista(v) {
  if (v === 'usuarios' && cloudRole !== 'admin') v = 'preparar';
  document.getElementById('viewPreparar').hidden = v !== 'preparar';
  document.getElementById('viewRenta-rec').hidden = v !== 'rec';
  document.getElementById('viewRenta-for').hidden = v !== 'for';
  document.getElementById('viewUsuarios').hidden = v !== 'usuarios';
  document.getElementById('viewEquipo').hidden = v !== 'equipo';
  document.getElementById('viewCuenta').hidden = true;
  document.getElementById('viewBio').hidden = true;
  if (v === 'usuarios') renderUsuarios();
  if (v === 'equipo') { renderEquipo(); refreshTeamUsers(); }
  if (v === 'preparar') prefillTecnico();""",
"""// Menu de secciones (2.5.0): 'inicio' es el selector que se muestra al
// abrir la app, cada vez, sin recordar la última sección.
function showVista(v) {
  if (v === 'usuarios' && cloudRole !== 'admin') v = 'inicio';
  document.getElementById('viewInicio').hidden = v !== 'inicio';
  document.getElementById('viewPreparar').hidden = v !== 'preparar';
  document.getElementById('viewRenta-rec').hidden = v !== 'rec';
  document.getElementById('viewRenta-for').hidden = v !== 'for';
  document.getElementById('viewMant').hidden = v !== 'mant';
  document.getElementById('viewUsuarios').hidden = v !== 'usuarios';
  document.getElementById('viewEquipo').hidden = v !== 'equipo';
  document.getElementById('viewCuenta').hidden = true;
  document.getElementById('viewBio').hidden = true;
  if (v === 'usuarios') renderUsuarios();
  if (v === 'equipo') { renderEquipo(); refreshTeamUsers(); }
  if (v === 'preparar') prefillTecnico();
  if (v === 'mant') { prefillMantTecnico(); renderMant(); }""")

# 4. onAuthChanged: salir limpia la suscripción de mantenimientos.
rep("""    if (cloudDetectadosUnsub) { cloudDetectadosUnsub(); cloudDetectadosUnsub = null; }
    detectados = [];""",
"""    if (cloudDetectadosUnsub) { cloudDetectadosUnsub(); cloudDetectadosUnsub = null; }
    if (cloudMantUnsub) { cloudMantUnsub(); cloudMantUnsub = null; }
    mantenimientos = [];
    detectados = [];""")

# 5. onAuthChanged: migrar borradores locales de mantenimientos.
rep("""    await migrateLocalRenta();
    await migrateLocalPreparations();""",
"""    await migrateLocalRenta();
    await migrateLocalPreparations();
    await migrateLocalMants();""")

# 6. onAuthChanged: suscribir mantenimientos (filtrado por tecnicoUid para
# usuarios normales, para que las reglas lo permitan) y abrir el selector.
rep("""    if (window.Cloud.subscribeDetectados) {
      if (cloudDetectadosUnsub) cloudDetectadosUnsub();
      cloudDetectadosUnsub = window.Cloud.subscribeDetectados(function (docs) {
        detectados = docs || [];
        renderDetectados();
      });
    }
    startEquipo();
    render();
    loadAiKey();""",
"""    if (window.Cloud.subscribeDetectados) {
      if (cloudDetectadosUnsub) cloudDetectadosUnsub();
      cloudDetectadosUnsub = window.Cloud.subscribeDetectados(function (docs) {
        detectados = docs || [];
        renderDetectados();
      });
    }
    if (window.Cloud.subscribeMantenimientos) {
      if (cloudMantUnsub) cloudMantUnsub();
      cloudMantUnsub = window.Cloud.subscribeMantenimientos(function (docs) {
        mantenimientos = mergeMantWithLocal(docs);
        saveMantLocal();
        renderMant();
      }, cloudRole === 'admin' ? null : (cloudUser ? cloudUser.uid : null));
    }
    startEquipo();
    render();
    showVista('inicio');
    loadAiKey();""")

# 7. boot(): en modo local también se abre el selector.
rep("""  if (!CLOUD_ENABLED) { document.getElementById('mainApp').hidden = false; document.getElementById('appHeader').hidden = false; _authReady = true; render(); return; }""",
"""  if (!CLOUD_ENABLED) { document.getElementById('mainApp').hidden = false; document.getElementById('appHeader').hidden = false; _authReady = true; render(); showVista('inicio'); return; }""")
rep("""  if (!ok) { CLOUD_ENABLED = false; document.getElementById('mainApp').hidden = false; document.getElementById('appHeader').hidden = false; _authReady = true; render(); return; }""",
"""  if (!ok) { CLOUD_ENABLED = false; document.getElementById('mainApp').hidden = false; document.getElementById('appHeader').hidden = false; _authReady = true; render(); showVista('inicio'); return; }""")

# 8. applyRoleUI: un no-admin fuera de Usuarios va al selector.
rep("""  if (!isAdmin && !document.getElementById('viewUsuarios').hidden) showVista('preparar');""",
"""  if (!isAdmin && !document.getElementById('viewUsuarios').hidden) showVista('inicio');""")

# 9. Logout: limpia mantenimientos y vuelve al selector.
rep("""document.getElementById('btnLogout').addEventListener('click', function () {
  stopEquipo();
  if (cloudUnsub) { cloudUnsub(); cloudUnsub = null; }
  if (cloudDetectadosUnsub) { cloudDetectadosUnsub(); cloudDetectadosUnsub = null; }
  cloudUser = null; cloudRole = null; sessionPassword = null;
  showVista('preparar');""",
"""document.getElementById('btnLogout').addEventListener('click', function () {
  stopEquipo();
  if (cloudUnsub) { cloudUnsub(); cloudUnsub = null; }
  if (cloudDetectadosUnsub) { cloudDetectadosUnsub(); cloudDetectadosUnsub = null; }
  if (cloudMantUnsub) { cloudMantUnsub(); cloudMantUnsub = null; }
  mantenimientos = [];
  cloudUser = null; cloudRole = null; sessionPassword = null;
  showVista('inicio');""")

io.open(P, 'w', encoding='utf-8').write(s)
print('parche 2.5.0e OK')
