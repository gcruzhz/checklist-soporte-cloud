#!/usr/bin/env python3
"""Parche 2.3.2: integración del teléfono (detector) + login siempre en el .exe
+ IP (estática/dinámica) + AnyDesk.

- www/index.html: versión 2.3.2 en todos los sitios; t12 (Invgate) pasa a
  DETECTABLE_IDS (17) con nombre corto 'Invgate'; nunca-marcar queda en
  t1, t2, t13-t17, t26; detLineFor usa detalles.adobe (Acrobat/Reader) y
  detalles.invgate ('Agente de Invgate detectado'); 'Usar este equipo'
  lleva a la preparación equipo.cpu/ramGB/discoGB/discoTipo/ip/ipTipo/
  anydeskId/anydeskAlias y prep.versiones {so, antivirus, chrome};
  prepToCloudDoc/prepFromCloud llevan esos campos con defaults vacíos;
  tarjeta de preparación y de detectado muestran línea de hardware,
  bloque 'Versiones detectadas', IP y AnyDesk; PDF, WhatsApp y Excel
  (buildXlsx: columnas CPU, RAM, Disco, IP, AnyDesk) los incluyen.
- Escritorio (window.Desktop): boot() cierra la sesión guardada
  (Cloud.signOut) ANTES de registrar onAuth, para que el .exe siempre
  pida iniciar sesión; oculta huella (#btnBiometric) y 'Recordar sesión'
  (#loginRememberRow); en el teléfono nada cambia.
- android/app/build.gradle: versionCode 45, versionName 2.3.2.
- ios: MARKETING_VERSION 2.3.2, CURRENT_PROJECT_VERSION 45 (x2 c/u).
- firebase.js: NO cambia (reportDetected ya pasa el objeto entero con
  setDoc + merge, así que versiones/discoTipo/ip/anydesk viajan tal cual);
  se verifica que sigue idéntico al backup y NO se reconstruye el bundle.
- tests: copia test20231.js a test20232.js, actualiza versión y series
  AO1/AO1e/AO2 (t12 ahora detectable), añade serie AP y extrae
  tests/checklist20232.js del index.html nuevo.
Cada reemplazo con assert: si el texto viejo no está, se para.
"""
import hashlib
import shutil

ROOT = '/home/hatch/workspace/android/checklist-cloud/'
HTML = ROOT + 'www/index.html'
FB = ROOT + 'www/cloud/firebase.js'
FB_BAK = ROOT + 'tests/firebase-2.3.1.js.bak'
GRADLE = ROOT + 'android/app/build.gradle'
PBX = ROOT + 'ios/App/App.xcodeproj/project.pbxproj'
TEST_OLD = ROOT + 'tests/test20231.js'
TEST_NEW = ROOT + 'tests/test20232.js'
EXTRACT = ROOT + 'tests/checklist20232.js'


def rep(path, old, new, count=1):
    with open(path, encoding='utf-8') as f:
        s = f.read()
    assert old in s, 'NO ENCONTRADO en %s: %r' % (path, old[:90])
    assert s.count(old) == count, 'OCURRENCIAS=%d (esperadas %d) en %s: %r' % (s.count(old), count, path, old[:90])
    with open(path, 'w', encoding='utf-8') as f:
        f.write(s.replace(old, new, count) if count == 1 else s.replace(old, new))
    print('OK:', path.split('/')[-1], '->', new[:70].replace('\n', ' '))


def rep_all(path, old, new, count):
    rep(path, old, new, count)


# ---------- 0. Copia del test ----------
shutil.copyfile(TEST_OLD, TEST_NEW)
print('OK: test20231.js copiado a test20232.js')

# ---------- 1. www/index.html: versión ----------
rep(HTML, 'Versión 2.3.1</p>', 'Versión 2.3.2</p>')
rep(HTML, 'Versión: 2.3.1</div>', 'Versión: 2.3.2</div>')
rep(HTML,
    "// Checks del detector (2.3.1): el detector de escritorio reporta qué\n"
    "// software y hardware encontró (d.checks) y detalles (d.detalles, p. ej.\n"
    "// officeDetectado). Solo los ids detectables de la plantilla actual\n"
    "// pueden nacer marcados (t3/t4 de hardware y el software); datos,\n"
    "// Invgate y la limpieza nunca.",
    "// Checks del detector (2.3.2): el detector de escritorio reporta qué\n"
    "// software y hardware encontró (d.checks), versiones (d.versiones) y\n"
    "// detalles (d.detalles, p. ej. officeDetectado, invgate, adobe).\n"
    "// Solo los ids detectables de la plantilla actual pueden nacer\n"
    "// marcados (t3/t4 de hardware, el software e Invgate t12); datos\n"
    "// (t13-t17), t1/t2 y la limpieza (t26) nunca.")
rep(HTML, '// Equipos detectados (2.3.1): solo se listan los NO usados, con sus datos',
    '// Equipos detectados (2.3.2): solo se listan los NO usados, con sus datos')
rep(HTML,
    "  window.location.href = 'mailto:gerardo.cruzhz@linux.com?subject=' + encodeURIComponent('Reporte de problema - Checklist de Soporte 2.3.1') + '&body=' + encodeURIComponent('Describe el problema:\\n\\n\\nVersión de la app: 2.3.1');",
    "  window.location.href = 'mailto:gerardo.cruzhz@linux.com?subject=' + encodeURIComponent('Reporte de problema - Checklist de Soporte 2.3.2') + '&body=' + encodeURIComponent('Describe el problema:\\n\\n\\nVersión de la app: 2.3.2');")

# ---------- 2. Login: fila de 'Recordar sesión' con id (para ocultarla en escritorio) ----------
rep(HTML,
    '<label style="display:flex;align-items:center;gap:6px;font-size:13px;color:#555;margin:2px 0 10px"><input type="checkbox" id="loginRemember" checked> Recordar sesión en este teléfono</label>',
    '<label id="loginRememberRow" style="display:flex;align-items:center;gap:6px;font-size:13px;color:#555;margin:2px 0 10px"><input type="checkbox" id="loginRemember" checked> Recordar sesión en este teléfono</label>')

# ---------- 3. prepToCloudDoc / prepFromCloud: hardware, versiones, IP, AnyDesk ----------
rep(HTML,
    "function prepToCloudDoc(p) {\n"
    "  var eq = p.equipo || {};\n"
    "  var foto = eq.fotoSerie || null;",
    "function prepToCloudDoc(p) {\n"
    "  var eq = p.equipo || {};\n"
    "  var v = p.versiones || {};\n"
    "  var foto = eq.fotoSerie || null;")
rep(HTML,
    "    autoDetectado: p.autoDetectado || [],\n"
    "    equipo: { tipo: eq.tipo || '', marca: eq.marca || '', modelo: eq.modelo || '', serie: eq.serie || '', inventario: eq.inventario || '', hostname: eq.hostname || '', fotoSerie: foto },",
    "    autoDetectado: p.autoDetectado || [],\n"
    "    versiones: { so: v.so || '', antivirus: v.antivirus || '', chrome: v.chrome || '' },\n"
    "    equipo: { tipo: eq.tipo || '', marca: eq.marca || '', modelo: eq.modelo || '', serie: eq.serie || '', inventario: eq.inventario || '', hostname: eq.hostname || '', cpu: eq.cpu || '', ramGB: (eq.ramGB == null ? '' : eq.ramGB), discoGB: (eq.discoGB == null ? '' : eq.discoGB), discoTipo: eq.discoTipo || '', ip: eq.ip || '', ipTipo: eq.ipTipo || '', anydeskId: eq.anydeskId || '', anydeskAlias: eq.anydeskAlias || '', fotoSerie: foto },")
rep(HTML,
    "function prepFromCloud(doc) {\n"
    "  var eq = doc.equipo || {};\n"
    "  return {",
    "function prepFromCloud(doc) {\n"
    "  var eq = doc.equipo || {};\n"
    "  var v = doc.versiones || {};\n"
    "  return {")
rep(HTML,
    "    autoDetectado: doc.autoDetectado || [],\n"
    "    equipo: { tipo: eq.tipo || '', marca: eq.marca || '', modelo: eq.modelo || '', serie: eq.serie || '', inventario: eq.inventario || '', hostname: eq.hostname || '', fotoSerie: eq.fotoSerie || null },",
    "    autoDetectado: doc.autoDetectado || [],\n"
    "    versiones: { so: v.so || '', antivirus: v.antivirus || '', chrome: v.chrome || '' },\n"
    "    equipo: { tipo: eq.tipo || '', marca: eq.marca || '', modelo: eq.modelo || '', serie: eq.serie || '', inventario: eq.inventario || '', hostname: eq.hostname || '', cpu: eq.cpu || '', ramGB: (eq.ramGB == null ? '' : eq.ramGB), discoGB: (eq.discoGB == null ? '' : eq.discoGB), discoTipo: eq.discoTipo || '', ip: eq.ip || '', ipTipo: eq.ipTipo || '', anydeskId: eq.anydeskId || '', anydeskAlias: eq.anydeskAlias || '', fotoSerie: eq.fotoSerie || null },")

# ---------- 4. t12 detectable + nombre corto ----------
rep(HTML,
    "var DETECTABLE_IDS = ['t3', 't4', 't6', 't7', 't8', 't9', 't10', 't11', 't18', 't19', 't20', 't21', 't22', 't23', 't24', 't25'];",
    "var DETECTABLE_IDS = ['t3', 't4', 't6', 't7', 't8', 't9', 't10', 't11', 't12', 't18', 't19', 't20', 't21', 't22', 't23', 't24', 't25'];")
rep(HTML,
    "  t10: 'VPN', t11: 'Inicio rápido desactivado', t18: 'Chrome',",
    "  t10: 'VPN', t11: 'Inicio rápido desactivado', t12: 'Invgate', t18: 'Chrome',")

# ---------- 5. detLineFor: Adobe (Acrobat/Reader) e Invgate por detalles ----------
rep(HTML,
    "function detLineFor(d) {\n"
    "  var f = filterDetectedChecks(d.checks || {});\n"
    "  var parts = detectedNames(f.checks, f.ids);\n"
    "  if (d.detalles && d.detalles.officeDetectado && !f.checks.t8) parts.push('Office instalado, activación sin verificar');\n"
    "  if (!parts.length) return '';\n"
    "  return 'Detectado: ' + parts.map(function (n) { return esc(n); }).join(', ');\n"
    "}",
    "function detLineFor(d) {\n"
    "  var f = filterDetectedChecks(d.checks || {});\n"
    "  var parts = detectedNames(f.checks, f.ids);\n"
    "  if (f.checks.t19 && d.detalles && d.detalles.adobe) {\n"
    "    var ad = d.detalles.adobe === 'Acrobat' ? 'Adobe Acrobat' : 'Adobe Reader';\n"
    "    for (var i = 0; i < parts.length; i++) if (parts[i] === 'Adobe Reader') parts[i] = ad;\n"
    "  }\n"
    "  if (d.detalles && d.detalles.officeDetectado && !f.checks.t8) parts.push('Office instalado, activación sin verificar');\n"
    "  if (d.detalles && d.detalles.invgate && !f.checks.t12) parts.push('Agente de Invgate detectado');\n"
    "  if (!parts.length) return '';\n"
    "  return 'Detectado: ' + parts.map(function (n) { return esc(n); }).join(', ');\n"
    "}\n"
    "// Versiones detectadas (2.3.2): solo las conocidas, en el orden SO,\n"
    "// antivirus, Chrome. Vacío si no se conoce ninguna.\n"
    "function versionesLine(v) {\n"
    "  v = v || {};\n"
    "  var parts = [];\n"
    "  if (v.so) parts.push('SO: ' + v.so);\n"
    "  if (v.antivirus) parts.push('Antivirus: ' + v.antivirus);\n"
    "  if (v.chrome) parts.push('Chrome: ' + v.chrome);\n"
    "  if (!parts.length) return '';\n"
    "  return 'Versiones detectadas: ' + parts.join(' • ');\n"
    "}\n"
    "// Línea de hardware (2.3.2): solo los datos conocidos; vacía si no hay\n"
    "// ninguno. Disco con su tipo (HDD/SSD/NVMe) e IP con su tipo cuando se\n"
    "// conocen ('IP: 192.168.1.45 (Dinámica)').\n"
    "function hardwareLine(eq) {\n"
    "  eq = eq || {};\n"
    "  var parts = [];\n"
    "  if (eq.cpu) parts.push('Procesador: ' + eq.cpu);\n"
    "  if (eq.ramGB != null && eq.ramGB !== '') parts.push('RAM: ' + eq.ramGB + ' GB');\n"
    "  if (eq.discoGB != null && eq.discoGB !== '') parts.push('Disco: ' + eq.discoGB + ' GB' + (eq.discoTipo ? ' ' + eq.discoTipo : ''));\n"
    "  if (eq.ip) parts.push('IP: ' + eq.ip + (eq.ipTipo ? ' (' + eq.ipTipo + ')' : ''));\n"
    "  return parts.join(' • ');\n"
    "}\n"
    "// AnyDesk (2.3.2): el ID de 9 dígitos se muestra agrupado ('123 456 789')\n"
    "// y con su alias si se conoce. Vacío si no hay ID.\n"
    "function anydeskDisplay(id) {\n"
    "  var d = String(id || '').replace(/\\D/g, '');\n"
    "  if (d.length === 9) return d.slice(0, 3) + ' ' + d.slice(3, 6) + ' ' + d.slice(6);\n"
    "  return String(id || '');\n"
    "}\n"
    "function anydeskLine(eq) {\n"
    "  eq = eq || {};\n"
    "  if (!eq.anydeskId) return '';\n"
    "  var s = 'AnyDesk: ' + anydeskDisplay(eq.anydeskId);\n"
    "  if (eq.anydeskAlias) s += ' (' + eq.anydeskAlias + ')';\n"
    "  return s;\n"
    "}")

# ---------- 6. Tarjeta del equipo detectado: hardware, AnyDesk, versiones ----------
rep(HTML,
    "  box.innerHTML = list.map(function (d) {\n"
    "    var detLine = detLineFor(d);\n"
    "    return '<div class=\"card\"><h2>' + esc(d.hostname || 'Equipo') + '</h2>' +\n"
    "      '<div class=\"sub\">' + esc((d.marca || '') + ' ' + (d.modelo || '')) + ' · Serie: ' + esc(d.serie || '—') + '</div>' +\n"
    "      '<div class=\"sub\">CPU: ' + esc(d.cpu || '—') + ' · RAM: ' + (d.ramGB != null ? esc(d.ramGB) + ' GB' : '—') + ' · Disco: ' + (d.discoGB != null ? esc(d.discoGB) + ' GB' : '—') + ' · SO: ' + esc(d.so || '—') + '</div>' +",
    "  box.innerHTML = list.map(function (d) {\n"
    "    var detLine = detLineFor(d);\n"
    "    var hwLine = hardwareLine(d);\n"
    "    if (d.so) hwLine = hwLine ? hwLine + ' • SO: ' + d.so : 'SO: ' + d.so;\n"
    "    var verLine = versionesLine(d.versiones);\n"
    "    var adLine = anydeskLine(d);\n"
    "    return '<div class=\"card\"><h2>' + esc(d.hostname || 'Equipo') + '</h2>' +\n"
    "      '<div class=\"sub\">' + esc((d.marca || '') + ' ' + (d.modelo || '')) + ' · Serie: ' + esc(d.serie || '—') + '</div>' +\n"
    "      (hwLine ? '<div class=\"sub\">' + esc(hwLine) + '</div>' : '') +\n"
    "      (adLine ? '<div class=\"sub\">' + esc(adLine) + '</div>' : '') +\n"
    "      (verLine ? '<div class=\"sub\">' + esc(verLine) + '</div>' : '') +")

# ---------- 7. PDF: hardware, IP, AnyDesk y versiones ----------
rep(HTML,
    "  row('Hostname: ' + (prep.equipo.hostname || '—'), 'F1', 11);",
    "  row('Hostname: ' + (prep.equipo.hostname || '—'), 'F1', 11);\n"
    "  if (prep.equipo.cpu) row('Procesador: ' + prep.equipo.cpu, 'F1', 11);\n"
    "  if (prep.equipo.ramGB != null && prep.equipo.ramGB !== '') row('RAM: ' + prep.equipo.ramGB + ' GB', 'F1', 11);\n"
    "  if (prep.equipo.discoGB != null && prep.equipo.discoGB !== '') row('Disco: ' + prep.equipo.discoGB + ' GB' + (prep.equipo.discoTipo ? ' ' + prep.equipo.discoTipo : ''), 'F1', 11);\n"
    "  if (prep.equipo.ip) row('IP: ' + prep.equipo.ip + (prep.equipo.ipTipo ? ' (' + prep.equipo.ipTipo + ')' : ''), 'F1', 11);\n"
    "  if (prep.equipo.anydeskId) row(anydeskLine(prep.equipo), 'F1', 11);\n"
    "  var vv = prep.versiones || {};\n"
    "  if (vv.so || vv.antivirus || vv.chrome) {\n"
    "    row('Versiones detectadas:', 'F2', 12);\n"
    "    if (vv.so) row('SO: ' + vv.so, 'F1', 11);\n"
    "    if (vv.antivirus) row('Antivirus: ' + vv.antivirus, 'F1', 11);\n"
    "    if (vv.chrome) row('Chrome: ' + vv.chrome, 'F1', 11);\n"
    "  }")

# ---------- 8. Excel: columnas CPU, RAM, Disco, IP, AnyDesk ----------
rep(HTML,
    "  var headers = ['Tipo', 'Marca', 'Modelo', 'No. de serie', 'No. de inventario', 'Hostname', 'Usuario', 'Área', 'Correo', 'Analista', 'Estado', 'Avance %', 'Creado', 'Entregado', 'Reasignaciones'];",
    "  var headers = ['Tipo', 'Marca', 'Modelo', 'No. de serie', 'No. de inventario', 'Hostname', 'CPU', 'RAM', 'Disco', 'IP', 'AnyDesk', 'Usuario', 'Área', 'Correo', 'Analista', 'Estado', 'Avance %', 'Creado', 'Entregado', 'Reasignaciones'];")
rep(HTML,
    "    return [p.equipo.tipo, p.equipo.marca, p.equipo.modelo, p.equipo.serie, p.equipo.inventario, p.equipo.hostname,\n"
    "      p.usuario.nombre, p.usuario.area, p.usuario.correo, p.tecnico,",
    "    return [p.equipo.tipo, p.equipo.marca, p.equipo.modelo, p.equipo.serie, p.equipo.inventario, p.equipo.hostname,\n"
    "      p.equipo.cpu || '', (p.equipo.ramGB != null && p.equipo.ramGB !== '' ? p.equipo.ramGB + ' GB' : ''),\n"
    "      (p.equipo.discoGB != null && p.equipo.discoGB !== '' ? p.equipo.discoGB + ' GB' + (p.equipo.discoTipo ? ' ' + p.equipo.discoTipo : '') : ''),\n"
    "      (p.equipo.ip ? p.equipo.ip + (p.equipo.ipTipo ? ' (' + p.equipo.ipTipo + ')' : '') : ''),\n"
    "      (p.equipo.anydeskId ? anydeskDisplay(p.equipo.anydeskId) + (p.equipo.anydeskAlias ? ' (' + p.equipo.anydeskAlias + ')' : '') : ''),\n"
    "      p.usuario.nombre, p.usuario.area, p.usuario.correo, p.tecnico,")

# ---------- 9. WhatsApp individual ----------
rep(HTML,
    "    'Estado: ' + statusLabel(statusOf(p)) + ' — ' + progress(p) + '% (' + done + '/' + items.length + ' puntos)'];",
    "    'Estado: ' + statusLabel(statusOf(p)) + ' — ' + progress(p) + '% (' + done + '/' + items.length + ' puntos)'];\n"
    "  var hwOne = hardwareLine(p.equipo || {});\n"
    "  if (hwOne) lines.push(hwOne);\n"
    "  var adOne = anydeskLine(p.equipo || {});\n"
    "  if (adOne) lines.push(adOne);\n"
    "  var verOne = versionesLine(p.versiones);\n"
    "  if (verOne) lines.push(verOne);")

# ---------- 10. WhatsApp general ----------
rep(HTML,
    "  list.forEach(function (p) {\n"
    "    lines.push('• ' + (p.equipo.marca || 'Equipo') + ' ' + (p.equipo.modelo || '') +\n"
    "      ' — Serie: ' + (p.equipo.serie || '—') +\n"
    "      (p.equipo.hostname ? ' — Host: ' + p.equipo.hostname : '') +\n"
    "      ' — ' + (p.usuario.nombre || 'sin usuario') +\n"
    "      ' — ' + statusLabel(statusOf(p)) + ' ' + progress(p) + '%');\n"
    "  });",
    "  list.forEach(function (p) {\n"
    "    var extra = [];\n"
    "    var hwAll = hardwareLine(p.equipo || {});\n"
    "    if (hwAll) extra.push(hwAll);\n"
    "    var adAll = anydeskLine(p.equipo || {});\n"
    "    if (adAll) extra.push(adAll);\n"
    "    var verAll = versionesLine(p.versiones);\n"
    "    if (verAll) extra.push(verAll);\n"
    "    lines.push('• ' + (p.equipo.marca || 'Equipo') + ' ' + (p.equipo.modelo || '') +\n"
    "      ' — Serie: ' + (p.equipo.serie || '—') +\n"
    "      (p.equipo.hostname ? ' — Host: ' + p.equipo.hostname : '') +\n"
    "      ' — ' + (p.usuario.nombre || 'sin usuario') +\n"
    "      ' — ' + statusLabel(statusOf(p)) + ' ' + progress(p) + '%' + (extra.length ? ' — ' + extra.join(' — ') : ''));\n"
    "  });")

# ---------- 11. Tarjeta de preparación: bloque de versiones en Software ----------
rep(HTML,
    "    return '<div class=\"group\"><h3>' + GROUPS[g] + '</h3>' + rows + '</div>';",
    "    var verBlock = '';\n"
    "    if (g === 'software') { var vlCard = versionesLine(p.versiones); if (vlCard) verBlock = '<div class=\"sub\">' + esc(vlCard) + '</div>'; }\n"
    "    return '<div class=\"group\"><h3>' + GROUPS[g] + '</h3>' + rows + verBlock + '</div>';")

# ---------- 12. Tarjeta de preparación: líneas de hardware y AnyDesk ----------
rep(HTML,
    "  var detNote = (p.autoDetectado && p.autoDetectado.length)\n"
    "    ? '<div class=\"sub\">Puntos marcados por el detector: ' + esc(detectedNames(p.checks, p.autoDetectado).join(', ')) + '</div>' : '';",
    "  var detNote = (p.autoDetectado && p.autoDetectado.length)\n"
    "    ? '<div class=\"sub\">Puntos marcados por el detector: ' + esc(detectedNames(p.checks, p.autoDetectado).join(', ')) + '</div>' : '';\n"
    "  var hwLine = hardwareLine(p.equipo || {});\n"
    "  var adLine = anydeskLine(p.equipo || {});")
rep(HTML,
    "    '<div class=\"sub\">' + esc(p.equipo.tipo) + ' · Serie: ' + esc(p.equipo.serie || '—') + ' · Inv: ' + esc(p.equipo.inventario || '—') + (p.equipo.hostname ? ' · Host: ' + esc(p.equipo.hostname) : '') + '</div>' +",
    "    '<div class=\"sub\">' + esc(p.equipo.tipo) + ' · Serie: ' + esc(p.equipo.serie || '—') + ' · Inv: ' + esc(p.equipo.inventario || '—') + (p.equipo.hostname ? ' · Host: ' + esc(p.equipo.hostname) : '') + '</div>' +\n"
    "    (hwLine ? '<div class=\"sub\">' + esc(hwLine) + '</div>' : '') +\n"
    "    (adLine ? '<div class=\"sub\">' + esc(adLine) + '</div>' : '') +")

# ---------- 13. 'Usar este equipo': guardar versiones y hardware del detectado ----------
rep(HTML,
    "document.getElementById('btnShowNew').addEventListener('click', function () { window._detectedChecks = null; window._detectedDetalles = null; togglePanel('newBox'); });",
    "document.getElementById('btnShowNew').addEventListener('click', function () { window._detectedChecks = null; window._detectedDetalles = null; window._detectedVersiones = null; window._detectedHardware = null; togglePanel('newBox'); });")
rep(HTML,
    "    window._detectedChecks = d.checks || {};\n"
    "    window._detectedDetalles = d.detalles || {};",
    "    window._detectedChecks = d.checks || {};\n"
    "    window._detectedDetalles = d.detalles || {};\n"
    "    window._detectedVersiones = d.versiones || {};\n"
    "    window._detectedHardware = { cpu: d.cpu || '', ramGB: (d.ramGB == null ? '' : d.ramGB), discoGB: (d.discoGB == null ? '' : d.discoGB), discoTipo: d.discoTipo || '', ip: d.ip || '', ipTipo: d.ipTipo || '', anydeskId: d.anydeskId || '', anydeskAlias: d.anydeskAlias || '' };")

# ---------- 14. Nuevo equipo: la preparación nace con hardware, versiones, IP y AnyDesk ----------
rep(HTML,
    "  var det = filterDetectedChecks(window._detectedChecks || {});\n"
    "  var prep = {\n"
    "    id: uid(), createdAt: Date.now(), deliveredAt: null, readyAt: null, checks: det.checks, autoDetectado: det.ids, extraItems: [], reasignaciones: [],\n"
    "    equipo: { tipo: v('fTipo'), marca: v('fMarca'), modelo: v('fModelo'), serie: v('fSerie'), inventario: v('fInv'), hostname: v('fHostname'), fotoSerie: window._fotoSerie || null },",
    "  var det = filterDetectedChecks(window._detectedChecks || {});\n"
    "  var detHw = window._detectedHardware || {};\n"
    "  var detVer = window._detectedVersiones || {};\n"
    "  var prep = {\n"
    "    id: uid(), createdAt: Date.now(), deliveredAt: null, readyAt: null, checks: det.checks, autoDetectado: det.ids, extraItems: [], reasignaciones: [],\n"
    "    versiones: { so: (typeof detVer.so === 'string' ? detVer.so : ''), antivirus: (typeof detVer.antivirus === 'string' ? detVer.antivirus : ''), chrome: (typeof detVer.chrome === 'string' ? detVer.chrome : '') },\n"
    "    equipo: { tipo: v('fTipo'), marca: v('fMarca'), modelo: v('fModelo'), serie: v('fSerie'), inventario: v('fInv'), hostname: v('fHostname'), cpu: detHw.cpu || '', ramGB: (detHw.ramGB == null ? '' : detHw.ramGB), discoGB: (detHw.discoGB == null ? '' : detHw.discoGB), discoTipo: detHw.discoTipo || '', ip: detHw.ip || '', ipTipo: detHw.ipTipo || '', anydeskId: detHw.anydeskId || '', anydeskAlias: detHw.anydeskAlias || '', fotoSerie: window._fotoSerie || null },")
rep(HTML,
    "  state.preparations.push(prep);\n"
    "  window._detectedChecks = null;\n"
    "  window._detectedDetalles = null;",
    "  state.preparations.push(prep);\n"
    "  window._detectedChecks = null;\n"
    "  window._detectedDetalles = null;\n"
    "  window._detectedVersiones = null;\n"
    "  window._detectedHardware = null;")

# ---------- 15. Escritorio (.exe): signOut forzado al arrancar, antes de onAuth ----------
rep(HTML,
    "  if (!ok) { CLOUD_ENABLED = false; document.getElementById('mainApp').hidden = false; document.getElementById('appHeader').hidden = false; _authReady = true; render(); return; }\n"
    "  document.getElementById('mainApp').hidden = true;",
    "  if (!ok) { CLOUD_ENABLED = false; document.getElementById('mainApp').hidden = false; document.getElementById('appHeader').hidden = false; _authReady = true; render(); return; }\n"
    "  // Escritorio (2.3.2): el .exe siempre pide iniciar sesión al abrirse.\n"
    "  // Se cierra cualquier sesión guardada ANTES de escuchar el estado de\n"
    "  // autenticación, para que onAuthChanged nunca vea una sesión vieja ni\n"
    "  // parpadee la interfaz. Si el cierre falla, se sigue al login igual.\n"
    "  if (window.Desktop && window.Cloud && window.Cloud.signOut) {\n"
    "    try { await window.Cloud.signOut(); } catch (e) { /* seguir al login */ }\n"
    "  }\n"
    "  document.getElementById('mainApp').hidden = true;")
rep(HTML,
    "  if (localStorage.getItem('checklist-remember') === '0') document.getElementById('loginRemember').checked = false;\n"
    "  refreshBioButton();",
    "  if (localStorage.getItem('checklist-remember') === '0') document.getElementById('loginRemember').checked = false;\n"
    "  // Escritorio (2.3.2): la sesión nunca se recuerda ni hay huella en el\n"
    "  // .exe; en el teléfono todo sigue como siempre.\n"
    "  if (window.Desktop) {\n"
    "    var remRow = document.getElementById('loginRememberRow');\n"
    "    if (remRow) remRow.hidden = true;\n"
    "    document.getElementById('loginRemember').checked = false;\n"
    "  } else {\n"
    "    var remRow2 = document.getElementById('loginRememberRow');\n"
    "    if (remRow2) remRow2.hidden = false;\n"
    "  }\n"
    "  refreshBioButton();")

# ---------- 16. Huella: oculta en escritorio aunque haya credencial guardada ----------
rep(HTML,
    "async function refreshBioButton() {\n"
    "  var btn = document.getElementById('btnBiometric');\n"
    "  if (!btn) return;\n"
    "  bioAvailable = await bioCheck();",
    "async function refreshBioButton() {\n"
    "  var btn = document.getElementById('btnBiometric');\n"
    "  if (!btn) return;\n"
    "  // Escritorio (2.3.2): sin huella en el .exe, aunque haya credencial guardada.\n"
    "  if (window.Desktop) {\n"
    "    btn.hidden = true;\n"
    "    var disD = document.getElementById('btnBioDisable');\n"
    "    var enaD = document.getElementById('btnBioEnable');\n"
    "    if (disD) disD.hidden = true;\n"
    "    if (enaD) enaD.hidden = true;\n"
    "    return;\n"
    "  }\n"
    "  bioAvailable = await bioCheck();")
rep(HTML,
    "async function offerBiometrics(authEmail) {\n"
    "  try {\n"
    "    if (localStorage.getItem('checklist-bio-declined') === '1') return;",
    "async function offerBiometrics(authEmail) {\n"
    "  try {\n"
    "    if (window.Desktop) return;\n"
    "    if (localStorage.getItem('checklist-bio-declined') === '1') return;")
rep(HTML,
    "  var remember = document.getElementById('loginRemember').checked;",
    "  var remember = window.Desktop ? false : document.getElementById('loginRemember').checked;")

# ---------- 17. android/app/build.gradle ----------
rep(GRADLE, '        versionCode 44\n', '        versionCode 45\n')
rep(GRADLE, '        versionName "2.3.1"\n', '        versionName "2.3.2"\n')

# ---------- 18. iOS ----------
rep_all(PBX, '\t\t\t\tCURRENT_PROJECT_VERSION = 44;\n', '\t\t\t\tCURRENT_PROJECT_VERSION = 45;\n', 2)
rep_all(PBX, '\t\t\t\tMARKETING_VERSION = 2.3.1;\n', '\t\t\t\tMARKETING_VERSION = 2.3.2;\n', 2)

# ---------- 19. Verificación: firebase.js intacto y sin restos de 2.3.1 ----------
with open(HTML, encoding='utf-8') as f:
    html = f.read()
assert '2.3.1' not in html, 'Quedan restos de 2.3.1 en index.html'
assert 'Versión 2.3.2' in html and 'Versión: 2.3.2' in html
with open(FB, 'rb') as f:
    fb_now = f.read()
with open(FB_BAK, 'rb') as f:
    fb_bak = f.read()
assert fb_now == fb_bak, 'firebase.js cambió (no debía)'
assert b"return setDoc(doc(db, 'detectados', String(d.id)), d, { merge: true })" in fb_now
print('OK: firebase.js intacto (reportDetected ya pasa el objeto entero con merge); bundle sin reconstruir')

# ---------- 20. tests/test20232.js: versión y series AO afectadas por t12 ----------
rep(TEST_NEW, "fs.readFileSync(__dirname + '/checklist20231.js', 'utf8')",
    "fs.readFileSync(__dirname + '/checklist20232.js', 'utf8')")
rep(TEST_NEW,
    "console.log('AM0) versión 2.3.1:', html.includes('Versión 2.3.1'), '| sin 2.3.0:', !html.includes('Versión 2.3.0'),",
    "console.log('AM0) versión 2.3.2:', html.includes('Versión 2.3.2'), '| sin 2.3.1:', !html.includes('Versión 2.3.1'),")
rep(TEST_NEW,
    "const detFull = { t3: true, t4: true, t6: true, t7: true, t8: 'Office 365', t9: true, t10: true, t11: true, t18: true, t19: true, t20: true, t21: true, t22: true, t23: true, t24: true, t25: true };",
    "const detFull = { t3: true, t4: true, t6: true, t7: true, t8: 'Office 365', t9: true, t10: true, t11: true, t12: true, t18: true, t19: true, t20: true, t21: true, t22: true, t23: true, t24: true, t25: true };")
rep(TEST_NEW,
    "console.log('AO1) mapeo completo: 16 puntos:', fFull.ids.length === 16, '| Office 365:', fFull.checks.t8 === 'Office 365', '| t3/t4 de hardware:', fFull.checks.t3 === true && fFull.checks.t4 === true, '| nombres cortos en orden de plantilla:', detectedNames(fFull.checks, fFull.ids).join(', ') === 'Batería y cargador, Etiqueta y serie, SO actualizado, Antivirus, Office 365, Impresoras, VPN, Inicio rápido desactivado, Chrome, Adobe Reader, WinRAR, Lapi Fox, Alfaweb, Alfaprinter, Accesos directos, AnyDesk Gris');",
    "console.log('AO1) mapeo completo: 17 puntos:', fFull.ids.length === 17, '| Office 365:', fFull.checks.t8 === 'Office 365', '| t3/t4 de hardware:', fFull.checks.t3 === true && fFull.checks.t4 === true, '| t12 Invgate:', fFull.checks.t12 === true, '| nombres cortos en orden de plantilla:', detectedNames(fFull.checks, fFull.ids).join(', ') === 'Batería y cargador, Etiqueta y serie, SO actualizado, Antivirus, Office 365, Impresoras, VPN, Inicio rápido desactivado, Invgate, Chrome, Adobe Reader, WinRAR, Lapi Fox, Alfaweb, Alfaprinter, Accesos directos, AnyDesk Gris');")
rep(TEST_NEW,
    "console.log('AO1e) nunca t1/t2/t12/t13-t17/t26 ni desconocidos:', fNever.ids.length === 1 && fNever.ids[0] === 't18', '| solo queda Chrome:', Object.keys(fNever.checks).length === 1);",
    "console.log('AO1e) nunca t1/t2/t13-t17/t26 ni desconocidos:', fNever.ids.length === 2 && fNever.ids[0] === 't12' && fNever.ids[1] === 't18', '| quedan Invgate y Chrome:', Object.keys(fNever.checks).length === 2);")
rep(TEST_NEW,
    "'| preparación nace con checks detectados:', !!savedDet && savedDet.checks.t3 === true && savedDet.checks.t4 === true && savedDet.checks.t18 === true && savedDet.checks.t19 === true && savedDet.checks.t20 === true && savedDet.checks.t8 === 'Office 365', '| sin t1 ni t12 ni t99:', !!savedDet && savedDet.checks.t1 === undefined && savedDet.checks.t12 === undefined && savedDet.checks.t99 === undefined, '| autoDetectado:', !!savedDet && savedDet.autoDetectado.join(',') === 't3,t4,t8,t18,t19,t20', '| sube a la nube con autoDetectado:', upDet.length === 1 && upDet[0].autoDetectado.join(',') === 't3,t4,t8,t18,t19,t20',",
    "'| preparación nace con checks detectados:', !!savedDet && savedDet.checks.t3 === true && savedDet.checks.t4 === true && savedDet.checks.t12 === true && savedDet.checks.t18 === true && savedDet.checks.t19 === true && savedDet.checks.t20 === true && savedDet.checks.t8 === 'Office 365', '| sin t1 ni t99:', !!savedDet && savedDet.checks.t1 === undefined && savedDet.checks.t99 === undefined, '| autoDetectado:', !!savedDet && savedDet.autoDetectado.join(',') === 't3,t4,t8,t12,t18,t19,t20', '| sube a la nube con autoDetectado:', upDet.length === 1 && upDet[0].autoDetectado.join(',') === 't3,t4,t8,t12,t18,t19,t20',")

# ---------- 21. Serie AP ----------
AP = '''
  // AP0: estáticos 2.3.2 (versión, 17 detectables, nunca-marcar, defaults viejos).
  var all17 = filterDetectedChecks({ t3: true, t4: true, t6: true, t7: true, t8: 'Office 365', t9: true, t10: true, t11: true, t12: true, t18: true, t19: true, t20: true, t21: true, t22: true, t23: true, t24: true, t25: true });
  var oldBack = prepFromCloud(prepToCloudDoc(mkPrep()));
  console.log('AP0) estáticos 2.3.2: versión:', html.includes('Versión 2.3.2') && !html.includes('Versión 2.3.1'), '| 17 detectables con t12:', all17.ids.length === 17, '| nombre corto Invgate:', detShortName('t12') === 'Invgate', '| nunca-marcar solo t1/t2/t13-t17/t26:', filterDetectedChecks({ t1: true, t2: true, t13: true, t14: true, t15: true, t16: true, t17: true, t26: true }).ids.length === 0, '| equipos viejos con defaults vacíos:', oldBack.equipo.cpu === '' && oldBack.equipo.ramGB === '' && oldBack.equipo.discoGB === '' && oldBack.equipo.discoTipo === '' && oldBack.equipo.ip === '' && oldBack.equipo.ipTipo === '' && oldBack.equipo.anydeskId === '' && oldBack.equipo.anydeskAlias === '' && oldBack.versiones.so === '' && oldBack.versiones.antivirus === '' && oldBack.versiones.chrome === '');
  // AP1: t12 con agente Invgate (servicio/proceso/clave en el escritorio).
  var fT12 = filterDetectedChecks({ t12: true });
  var lineInv = detLineFor({ checks: { t12: true }, detalles: { invgate: 'InvGate Agent 9.5.1' } });
  var lineInvOnly = detLineFor({ checks: {}, detalles: { invgate: 'InvGate Agent 9.5.1' } });
  var lineNoInv = detLineFor({ checks: { t18: true }, detalles: {} });
  console.log('AP1) t12 detectable por el detector:', fT12.checks.t12 === true && fT12.ids.length === 1, '| línea con agente Invgate:', lineInv === 'Detectado: Invgate', '| solo detalles.invgate avisa:', lineInvOnly === 'Detectado: Agente de Invgate detectado', '| sin Invgate no lo inventa:', lineNoInv === 'Detectado: Chrome');
  // AP2: t19 con Acrobat (y Reader sigue).
  var lineAcr = detLineFor({ checks: { t19: true }, detalles: { adobe: 'Acrobat' } });
  var lineRea = detLineFor({ checks: { t19: true }, detalles: { adobe: 'Reader' } });
  var lineAdDef = detLineFor({ checks: { t19: true }, detalles: {} });
  console.log('AP2) t19 con Acrobat:', lineAcr === 'Detectado: Adobe Acrobat', '| con Reader:', lineRea === 'Detectado: Adobe Reader', '| sin detalle sigue Reader:', lineAdDef === 'Detectado: Adobe Reader');
  // AP3: t22 por .lnk y t24 con hcweb+gabinete (y negativo si falta uno).
  var fLnk = filterDetectedChecks({ t22: true });
  var fHc = filterDetectedChecks({ t24: true });
  var fHcUno = filterDetectedChecks({ t24: false });
  console.log('AP3) t22 por .lnk:', fLnk.checks.t22 === true, '| t24 con hcweb+gabinete:', fHc.checks.t24 === true, '| si falta uno no se marca t24:', fHcUno.checks.t24 === undefined && fHcUno.ids.indexOf('t24') === -1);
  // AP4: versiones (Get-ComputerInfo/SecurityCenter2/Chrome) viajan a la prep y se muestran.
  function mkDet2(over) { return Object.assign({ id: 'DX2', hostname: 'PC-X', marca: 'HP', modelo: 'EliteDesk', serie: 'DX2', cpu: 'Intel Core i5-10500', ramGB: 8, discoGB: 256, discoTipo: 'SSD', so: 'Windows 11 Pro', tipo: 'Desktop', detectadoEn: Date.now() - 60000, detectadoPor: 'Gerardo', usado: false, checks: {}, detalles: {}, versiones: {}, ip: '', ipTipo: '', anydeskId: '', anydeskAlias: '' }, over || {}); }
  function useDet(id) {
    document.getElementById('detList')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-det-use]' ? { getAttribute: function () { return id; } } : null; } } });
  }
  doLogin('usuario');
  CLOUD_ENABLED = true;
  cloudUser = { uid: 'u1', email: 'test@checklist.local', nombre: 'Test User' };
  var upVer = [];
  global.Cloud.upsertPrep = async function (d) { upVer.push(d); };
  global.Cloud.markDetectadoUsado = async function () {};
  detectados = [mkDet2({ id: 'DET-VER', hostname: 'PC-VER', serie: 'DET-VER', cpu: 'Intel Core i7-10700', ramGB: 16, discoGB: 512, discoTipo: 'SSD', checks: { t18: true }, versiones: { so: 'Windows 11 Pro 26H2 (compilación 26200)', antivirus: 'ESET NOD32 Antivirus 18.0.12', chrome: '141.0.7390.65' } })];
  useDet('DET-VER');
  var stashVer = window._detectedVersiones;
  document.getElementById('fUser').value = 'Ana';
  document.getElementById('fTec').value = 'Test User';
  document.getElementById('btnAdd')._h.click[0]();
  var savedVer = state.preparations[state.preparations.length - 1];
  var cardVer = cardHtml(savedVer);
  console.log('AP4) versiones en el guardado:', !!stashVer && stashVer.so === 'Windows 11 Pro 26H2 (compilación 26200)' && stashVer.antivirus === 'ESET NOD32 Antivirus 18.0.12' && stashVer.chrome === '141.0.7390.65', '| viajan a la prep:', !!savedVer && savedVer.versiones.so === 'Windows 11 Pro 26H2 (compilación 26200)' && savedVer.versiones.antivirus === 'ESET NOD32 Antivirus 18.0.12' && savedVer.versiones.chrome === '141.0.7390.65', '| y suben a la nube:', upVer.length === 1 && upVer[0].versiones.chrome === '141.0.7390.65', '| tarjeta muestra el bloque:', cardVer.includes('Versiones detectadas: SO: Windows 11 Pro 26H2') && cardVer.includes('Antivirus: ESET NOD32 Antivirus 18.0.12') && cardVer.includes('Chrome: 141.0.7390.65'), '| hardware en tarjeta:', cardVer.includes('Procesador: Intel Core i7-10700 • RAM: 16 GB • Disco: 512 GB SSD'));
  // AP4b: solo una versión conocida muestra solo esa; sin versiones no hay bloque.
  var pParc = mkPrep({ versiones: { so: '', antivirus: '', chrome: '141.0.7390.65' } });
  var cardParc = cardHtml(pParc);
  console.log('AP4b) solo Chrome muestra solo Chrome:', cardParc.includes('Versiones detectadas: Chrome: 141.0.7390.65') && cardParc.indexOf('SO: Windows') === -1 && cardParc.indexOf('Antivirus: ESET') === -1, '| sin versiones no hay bloque:', cardHtml(mkPrep()).indexOf('Versiones detectadas') === -1);
  // AP5: discoTipo HDD/SSD/NVMe viaja a la prep y se muestra.
  var pHdd = mkPrep({ equipo: { tipo: 'Laptop', marca: 'Dell', modelo: 'X', serie: 'S', inventario: '1', cpu: 'Intel Core i5-1135G7', ramGB: 8, discoGB: 1000, discoTipo: 'HDD' } });
  var pSsd = mkPrep({ equipo: { tipo: 'Laptop', marca: 'Dell', modelo: 'X', serie: 'S', inventario: '1', cpu: 'Intel Core i5-1135G7', ramGB: 8, discoGB: 512, discoTipo: 'SSD' } });
  var pNv = mkPrep({ equipo: { tipo: 'Laptop', marca: 'Dell', modelo: 'X', serie: 'S', inventario: '1', cpu: 'Intel Core i5-1135G7', ramGB: 8, discoGB: 256, discoTipo: 'NVMe' } });
  var backHdd = prepFromCloud(prepToCloudDoc(pHdd));
  console.log('AP5) discoTipo viaja a la nube y vuelve:', prepToCloudDoc(pHdd).equipo.discoTipo === 'HDD' && backHdd.equipo.discoTipo === 'HDD' && prepFromCloud(prepToCloudDoc(pNv)).equipo.discoTipo === 'NVMe', '| tarjeta HDD:', cardHtml(pHdd).includes('Disco: 1000 GB HDD'), '| SSD:', cardHtml(pSsd).includes('Disco: 512 GB SSD'), '| NVMe:', cardHtml(pNv).includes('Disco: 256 GB NVMe'), '| sin datos no hay línea:', cardHtml(mkPrep()).indexOf('Procesador:') === -1);
  // AP6: hardware, versiones, IP y AnyDesk en PDF, WhatsApp y Excel.
  var pFull = mkPrep({ equipo: { tipo: 'Laptop', marca: 'Dell', modelo: 'Inspiron 3501', serie: 'S1', inventario: '100', hostname: 'PC-01', cpu: 'Intel Core i7-10700', ramGB: 16, discoGB: 512, discoTipo: 'SSD', ip: '192.168.1.45', ipTipo: 'Dinámica', anydeskId: '123456789', anydeskAlias: 'Oficina' }, versiones: { so: 'Windows 11 Pro 26H2 (compilación 26200)', antivirus: 'ESET NOD32 Antivirus 18.0.12', chrome: '141.0.7390.65' } });
  var pdfTxt = Buffer.from(await buildPdf(pFull).arrayBuffer()).toString('latin1');
  var waOne = waTextOne(pFull);
  var waAll = waTextAll([pFull]);
  var xlsxTxt = Buffer.from(await buildXlsx([pFull]).arrayBuffer()).toString('latin1');
  var pdfNeed = ['Procesador: Intel Core i7-10700', 'RAM: 16 GB', 'Disco: 512 GB SSD', 'SO: Windows 11 Pro 26H2', 'Antivirus: ESET NOD32 Antivirus 18.0.12', 'Chrome: 141.0.7390.65', 'IP: 192.168.1.45', 'AnyDesk: 123 456 789'];
  console.log('AP6) PDF con hardware, versiones, IP y AnyDesk:', pdfNeed.every(function (s) { return pdfTxt.indexOf(s) !== -1; }), '| WhatsApp individual:', pdfNeed.every(function (s) { return waOne.indexOf(s) !== -1; }) && waOne.indexOf('Versiones detectadas:') !== -1, '| WhatsApp general:', waAll.indexOf('Procesador: Intel Core i7-10700') !== -1 && waAll.indexOf('AnyDesk: 123 456 789') !== -1 && waAll.indexOf('Versiones detectadas:') !== -1, '| Excel con columnas y valores:', ['CPU', 'RAM', 'Disco', 'IP', 'AnyDesk', '16 GB', '512 GB SSD', '192.168.1.45', '123 456 789'].every(function (s) { return xlsxTxt.indexOf(s) !== -1; }));
  // AP7: IP dinámica (dhcp) e IP estática viajan con 'Usar este equipo'.
  detectados = [mkDet2({ id: 'DET-IP-DIN', serie: 'DET-IP-DIN', ip: '192.168.1.45', ipTipo: 'Dinámica' })];
  useDet('DET-IP-DIN');
  document.getElementById('fUser').value = 'Ana';
  document.getElementById('fTec').value = 'Test User';
  document.getElementById('btnAdd')._h.click[0]();
  var savedIpD = state.preparations[state.preparations.length - 1];
  detectados = [mkDet2({ id: 'DET-IP-EST', serie: 'DET-IP-EST', ip: '10.0.0.20', ipTipo: 'Estática' })];
  useDet('DET-IP-EST');
  document.getElementById('fUser').value = 'Luis';
  document.getElementById('fTec').value = 'Test User';
  document.getElementById('btnAdd')._h.click[0]();
  var savedIpE = state.preparations[state.preparations.length - 1];
  console.log('AP7) IP dinámica viaja a la prep:', savedIpD.equipo.ip === '192.168.1.45' && savedIpD.equipo.ipTipo === 'Dinámica', '| tarjeta dinámica:', cardHtml(savedIpD).includes('IP: 192.168.1.45 (Dinámica)'), '| IP estática viaja:', savedIpE.equipo.ip === '10.0.0.20' && savedIpE.equipo.ipTipo === 'Estática', '| tarjeta estática:', cardHtml(savedIpE).includes('IP: 10.0.0.20 (Estática)'), '| nube guarda y restaura IP:', prepFromCloud(prepToCloudDoc(savedIpD)).equipo.ip === '192.168.1.45' && prepFromCloud(prepToCloudDoc(savedIpD)).equipo.ipTipo === 'Dinámica');
  // AP7b: sin IPv4 no se muestra nada; solo IP sin tipo muestra solo la IP;
  // la interfaz por defecto ya la elige el detector: el teléfono toma doc.ip tal cual.
  detectados = [mkDet2({ id: 'DET-IP-NO', serie: 'DET-IP-NO' })];
  useDet('DET-IP-NO');
  document.getElementById('fUser').value = 'Ana';
  document.getElementById('fTec').value = 'Test User';
  document.getElementById('btnAdd')._h.click[0]();
  var savedIpN = state.preparations[state.preparations.length - 1];
  var cardIpSolo = cardHtml(mkPrep({ equipo: { tipo: 'Laptop', marca: 'Dell', modelo: 'X', serie: 'S', inventario: '1', ip: '192.168.1.99' } }));
  detectados = [mkDet2({ id: 'DET-IP-DEF', serie: 'DET-IP-DEF', ip: '192.168.1.45', ipTipo: 'Dinámica' })];
  renderDetectados();
  var detIpHtml = document.getElementById('detList').innerHTML;
  console.log('AP7b) sin IPv4 no se muestra nada:', savedIpN.equipo.ip === '' && cardHtml(savedIpN).indexOf('IP:') === -1, '| solo IP sin tipo muestra solo la IP:', cardIpSolo.includes('IP: 192.168.1.99') && cardIpSolo.indexOf('(Dinámica)') === -1 && cardIpSolo.indexOf('(Estática)') === -1, '| tarjeta del detectado con la IP por defecto:', detIpHtml.includes('IP: 192.168.1.45 (Dinámica)'));
  // AP8: AnyDesk viaja a la prep y se muestra (o no se muestra si no hay).
  detectados = [mkDet2({ id: 'DET-AD', serie: 'DET-AD', anydeskId: '123456789', anydeskAlias: 'Oficina-Gerardo' })];
  renderDetectados();
  var detAdHtml = document.getElementById('detList').innerHTML;
  useDet('DET-AD');
  document.getElementById('fUser').value = 'Ana';
  document.getElementById('fTec').value = 'Test User';
  document.getElementById('btnAdd')._h.click[0]();
  var savedAd = state.preparations[state.preparations.length - 1];
  console.log('AP8) AnyDesk viaja a la prep:', savedAd.equipo.anydeskId === '123456789' && savedAd.equipo.anydeskAlias === 'Oficina-Gerardo', '| agrupado 123 456 789:', anydeskDisplay('123456789') === '123 456 789', '| tarjeta de la prep:', cardHtml(savedAd).includes('AnyDesk: 123 456 789 (Oficina-Gerardo)'), '| tarjeta del detectado:', detAdHtml.includes('AnyDesk: 123 456 789'), '| sin AnyDesk no se muestra nada:', cardHtml(mkPrep()).indexOf('AnyDesk:') === -1);
  // AP9: escritorio (.exe) siempre pide iniciar sesión al abrirse.
  var orderDesk = [];
  var signOutDesk = [];
  global.Cloud.signOut = async function () { orderDesk.push('signOut'); signOutDesk.push(1); };
  global.Cloud.init = async function () { return true; };
  var authCbDesk = null;
  global.Cloud.onAuth = function (cb) { orderDesk.push('onAuth'); authCbDesk = cb; };
  global.Cloud.isInitialized = async function () { return true; };
  global.Desktop = {};
  CLOUD_ENABLED = true;
  _authReady = false;
  await boot();
  await sleep(20);
  var deskBootOk = signOutDesk.length === 1 && orderDesk.join(',') === 'signOut,onAuth' && document.getElementById('loginView').hidden === false && document.getElementById('mainApp').hidden === true && document.getElementById('appHeader').hidden === true;
  await authCbDesk(null);
  console.log('AP9) escritorio: signOut al arrancar antes de escuchar auth:', deskBootOk, '| muestra el login, no la interfaz:', document.getElementById('loginView').hidden === false && document.getElementById('mainApp').hidden === true && _authReady === true, '| huella y recordar ocultos:', document.getElementById('btnBiometric').hidden === true && document.getElementById('loginRememberRow').hidden === true && document.getElementById('loginRemember').checked === false);
  // AP9b: si el signOut falla, igual muestra el login sin romperse.
  orderDesk.length = 0; signOutDesk.length = 0;
  global.Cloud.signOut = async function () { signOutDesk.push(1); throw new Error('sin red'); };
  _authReady = false;
  await boot();
  await sleep(20);
  await authCbDesk(null);
  console.log('AP9b) escritorio: si signOut falla, igual llega al login:', signOutDesk.length === 1 && document.getElementById('loginView').hidden === false && _authReady === true);
  global.Desktop = undefined;
  // AP9c: teléfono sin Desktop: sin signOut forzado, huella y recordar como siempre.
  var signOutTel = [];
  global.Cloud.signOut = async function () { signOutTel.push(1); };
  global.Capacitor = { Plugins: { NativeBiometric: { isAvailable: async function () { return { isAvailable: true }; }, getCredentials: async function () { return { username: 'u', password: 'p' }; } } } };
  _authReady = false;
  await boot();
  await sleep(30);
  await authCbDesk(null);
  console.log('AP9c) teléfono: sin signOut forzado:', signOutTel.length === 0, '| huella visible con credencial guardada:', document.getElementById('btnBiometric').hidden === false, '| recordar visible:', document.getElementById('loginRememberRow').hidden === false, '| y llega al login:', document.getElementById('loginView').hidden === false && _authReady === true);
  global.Capacitor = undefined;
  global.Cloud.signOut = async function () {};
'''
with open(TEST_NEW, encoding='utf-8') as f:
    t = f.read()
anchor = '  process.exit(0);'
assert t.count(anchor) == 1, 'Ancla process.exit no única'
t = t.replace(anchor, AP + '\n' + anchor, 1)
with open(TEST_NEW, 'w', encoding='utf-8') as f:
    f.write(t)
print('OK: serie AP añadida a test20232.js')

# ---------- 22. Extraer tests/checklist20232.js del index.html nuevo ----------
with open(HTML, encoding='utf-8') as f:
    lines = f.read().split('\n')
start = next(i for i, ln in enumerate(lines) if ln == '<script>')
end = next(i for i, ln in enumerate(lines) if ln == '</script>')
assert end > start, 'No se encontró el script inline'
with open(EXTRACT, 'w', encoding='utf-8') as f:
    f.write('\n' + '\n'.join(lines[start + 1:end]) + '\n')
print('OK: extraído tests/checklist20232.js (script inline, líneas %d-%d)' % (start + 2, end))

print('Parche 2.3.2 aplicado.')
