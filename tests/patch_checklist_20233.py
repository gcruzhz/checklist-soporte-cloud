#!/usr/bin/env python3
"""Parche 2.3.3: integración del teléfono (detector) — re-detección y botón
bloqueado por máquina.

- www/cloud/firebase.js: reportDetected usa info.machineId como id del
  documento cuando viene (serie real, si no hostname + '-' + MAC sin ':' ni
  '-'; lo calcula el detector de escritorio); si no viene machineId, el
  respaldo viejo: serie si existe, si no hostname + '-' + detectadoEn.
  En CADA detección nueva pone usado=false y detectadoEn=ahora (merge),
  así que volver a detectar un equipo ya usado lo trae de vuelta al panel.
  Se reconstruye el bundle con esbuild (paso aparte, fuera del script).
- www/index.html: botón 'Detectar este equipo' bloqueado por máquina —
  se deshabilita y muestra 'Equipo detectado ✓' cuando ESTA máquina tiene
  una detección pendiente sin usar (doc con id == machineId y usado !==
  true); la detección de otra PC no bloquea esta. machineId se pide con
  window.Desktop.getMachineId(); si no existe o falla, no hay bloqueo y
  el botón funciona como antes. El botón reacciona a la suscripción
  (renderDetectados lo refresca) y se vuelve a habilitar al usar o
  descartar la entrada. Se mantiene 'Detectando software...' +
  deshabilitado durante la detección.
- Versión 2.3.3 / versionCode 46: index.html (12 ocurrencias de 2.3.2),
  android/app/build.gradle, ios project.pbxproj (x2 c/u).
- tests: copia test20232.js a test20233.js, actualiza versión y extraído,
  añade serie AQ, extrae tests/checklist20233.js del index.html nuevo.
Cada reemplazo con assert: si el texto viejo no está, se para.
"""
import shutil

ROOT = '/home/hatch/workspace/android/checklist-cloud/'
HTML = ROOT + 'www/index.html'
FB = ROOT + 'www/cloud/firebase.js'
GRADLE = ROOT + 'android/app/build.gradle'
PBX = ROOT + 'ios/App/App.xcodeproj/project.pbxproj'
TEST_OLD = ROOT + 'tests/test20232.js'
TEST_NEW = ROOT + 'tests/test20233.js'
EXTRACT = ROOT + 'tests/checklist20233.js'


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


# ---------- 0. Backups 2.3.2 ----------
shutil.copyfile(HTML, ROOT + 'tests/checklist-2.3.2.html.bak')
shutil.copyfile(FB, ROOT + 'tests/firebase-2.3.2.js.bak')
print('OK: backups tests/checklist-2.3.2.html.bak y tests/firebase-2.3.2.js.bak')

# ---------- 0b. Copia del test ----------
shutil.copyfile(TEST_OLD, TEST_NEW)
print('OK: test20232.js copiado a test20233.js')

# ---------- 1. firebase.js: reportDetected con machineId + reseteo ----------
rep(FB,
    "// Equipos detectados (2.3.0): el detector de escritorio reporta los equipos\n"
    "// que ve en la red (colección detectados) y los teléfonos los listan para\n"
    "// usarlos en un equipo nuevo o descartarlos. El id es la serie si existe,\n"
    "// si no hostname + '-' + detectadoEn.\n"
    "async function reportDetected(info) {\n"
    "  const d = Object.assign({}, info || {});\n"
    "  if (!d.id) d.id = d.serie ? String(d.serie) : (d.hostname || '') + '-' + (d.detectadoEn || Date.now());\n"
    "  if (!d.detectadoEn) d.detectadoEn = Date.now();\n"
    "  if (d.usado === undefined) d.usado = false;\n"
    "  return setDoc(doc(db, 'detectados', String(d.id)), d, { merge: true });\n"
    "}",
    "// Equipos detectados (2.3.3): el detector de escritorio reporta los equipos\n"
    "// que ve en la red (colección detectados) y los teléfonos los listan para\n"
    "// usarlos en un equipo nuevo o descartarlos. El id es info.machineId cuando\n"
    "// viene (serie real, si no hostname + '-' + MAC sin ':' ni '-'; lo calcula\n"
    "// el detector de escritorio); si no viene, el respaldo viejo: la serie si\n"
    "// existe, si no hostname + '-' + detectadoEn. Cada detección nueva pone\n"
    "// usado=false y detectadoEn=ahora, así que volver a detectar un equipo ya\n"
    "// usado lo trae de vuelta al panel.\n"
    "async function reportDetected(info) {\n"
    "  const d = Object.assign({}, info || {});\n"
    "  if (d.machineId) d.id = String(d.machineId);\n"
    "  else if (!d.id) d.id = d.serie ? String(d.serie) : (d.hostname || '') + '-' + (d.detectadoEn || Date.now());\n"
    "  d.detectadoEn = Date.now();\n"
    "  d.usado = false;\n"
    "  return setDoc(doc(db, 'detectados', String(d.id)), d, { merge: true });\n"
    "}")

# ---------- 2. www/index.html: versión 2.3.2 -> 2.3.3 (12 ocurrencias) ----------
with open(HTML, encoding='utf-8') as f:
    html = f.read()
assert html.count('2.3.2') == 12, 'OCURRENCIAS 2.3.2=%d (esperadas 12)' % html.count('2.3.2')
assert '2.3.3' not in html, 'Ya hay 2.3.3 en index.html'
with open(HTML, 'w', encoding='utf-8') as f:
    f.write(html.replace('2.3.2', '2.3.3'))
print('OK: index.html versión 2.3.3 (12 ocurrencias)')

# ---------- 3. Estado + helpers del botón bloqueado por máquina ----------
rep(HTML,
    "function cloudDeleteDetectado(id) {\n"
    "  if (!CLOUD_ENABLED || !cloudUser || !window.Cloud || !window.Cloud.deleteDetectado) return;\n"
    "  window.Cloud.deleteDetectado(id).catch(function (e) { console.warn('No se pudo descartar el equipo detectado', e); });\n"
    "}",
    "function cloudDeleteDetectado(id) {\n"
    "  if (!CLOUD_ENABLED || !cloudUser || !window.Cloud || !window.Cloud.deleteDetectado) return;\n"
    "  window.Cloud.deleteDetectado(id).catch(function (e) { console.warn('No se pudo descartar el equipo detectado', e); });\n"
    "}\n"
    "// Botón Detectar bloqueado por máquina (2.3.3): se deshabilita cuando ESTA\n"
    "// máquina ya tiene una detección pendiente sin usar (un documento en\n"
    "// 'detectados' con id == machineId de esta PC y usado !== true) y muestra\n"
    "// 'Equipo detectado ✓'; la detección de otra PC no bloquea esta. El\n"
    "// machineId lo expone el detector de escritorio (window.Desktop.\n"
    "// getMachineId()); si no existe o falla, no hay bloqueo y el botón funciona\n"
    "// como antes. El botón reacciona a la suscripción: al usarse o descartarse\n"
    "// la entrada, la suscripción lo refleja y se vuelve a habilitar.\n"
    "var machineId = null;        // id de esta máquina, si el detector lo expone\n"
    "var machineIdTried = false;  // ya se pidió getMachineId a este Desktop\n"
    "var machineIdDesktop = null; // Desktop al que se le pidió (si cambia, reintentar)\n"
    "var detectingNow = false;    // detección en curso (progreso)\n"
    "var DETECTAR_HTML = '<span class=\"ic\">&#128187;</span><span>Detectar este equipo<small>solo en escritorio</small></span>';\n"
    "function thisMachinePending() {\n"
    "  if (!machineId) return false;\n"
    "  return detectados.some(function (d) { return String(d.id) === String(machineId) && !d.usado; });\n"
    "}\n"
    "function refreshDetectarBtn() {\n"
    "  var btn = document.getElementById('btnDetectar');\n"
    "  if (!btn) return;\n"
    "  btn.hidden = !window.Desktop;\n"
    "  if (detectingNow) {\n"
    "    btn.disabled = true;\n"
    "    btn.innerHTML = '<span class=\"ic\">&#128187;</span><span>Detectando software...</span>';\n"
    "    return;\n"
    "  }\n"
    "  if (thisMachinePending()) {\n"
    "    btn.disabled = true;\n"
    "    btn.innerHTML = '<span class=\"ic\">&#128187;</span><span>Equipo detectado ✓</span>';\n"
    "    return;\n"
    "  }\n"
    "  btn.disabled = false;\n"
    "  // Solo se restaura la etiqueta por defecto si la puso este control\n"
    "  // (progreso o bloqueo); si otro código puso su propio texto, se respeta.\n"
    "  if (btn.innerHTML.indexOf('Detectando software...') !== -1 || btn.innerHTML.indexOf('Equipo detectado') !== -1) btn.innerHTML = DETECTAR_HTML;\n"
    "}\n"
    "function loadMachineId() {\n"
    "  if (window.Desktop !== machineIdDesktop) { machineIdTried = false; machineId = null; machineIdDesktop = window.Desktop || null; }\n"
    "  if (machineIdTried || !window.Desktop || typeof window.Desktop.getMachineId !== 'function') { machineIdTried = true; return Promise.resolve(machineId); }\n"
    "  machineIdTried = true;\n"
    "  var p;\n"
    "  try { p = Promise.resolve(window.Desktop.getMachineId()); } catch (e) { refreshDetectarBtn(); return Promise.resolve(null); }\n"
    "  return p.then(function (id) { machineId = id ? String(id) : null; refreshDetectarBtn(); return machineId; }).catch(function () { machineId = null; refreshDetectarBtn(); return null; });\n"
    "}")

# ---------- 4. renderDetectados refresca el botón (también sin pendientes) ----------
rep(HTML,
    "  if (!list.length) { box.innerHTML = '<div class=\"empty\">No hay equipos detectados pendientes.</div>'; return; }",
    "  if (!list.length) { box.innerHTML = '<div class=\"empty\">No hay equipos detectados pendientes.</div>'; refreshDetectarBtn(); return; }")
rep(HTML,
    "      '<div class=\"actions\"><button class=\"btn-green\" data-det-use=\"' + esc(d.id) + '\">Usar este equipo</button>' +\n"
    "      '<button class=\"btn-ghost\" data-det-del=\"' + esc(d.id) + '\">Descartar</button></div></div>';\n"
    "  }).join('');\n"
    "}",
    "      '<div class=\"actions\"><button class=\"btn-green\" data-det-use=\"' + esc(d.id) + '\">Usar este equipo</button>' +\n"
    "      '<button class=\"btn-ghost\" data-det-del=\"' + esc(d.id) + '\">Descartar</button></div></div>';\n"
    "  }).join('');\n"
    "  refreshDetectarBtn();\n"
    "}")

# ---------- 5. render(): refresca el botón y pide el machineId ----------
rep(HTML,
    "  var btnDet = document.getElementById('btnDetectar');\n"
    "  if (btnDet) btnDet.hidden = !window.Desktop;",
    "  refreshDetectarBtn();\n"
    "  if (window.Desktop) loadMachineId();")

# ---------- 6. Al cerrar sesión se limpia la lista de detectados ----------
rep(HTML,
    "    if (cloudDetectadosUnsub) { cloudDetectadosUnsub(); cloudDetectadosUnsub = null; }\n"
    "    document.getElementById('mainApp').hidden = true;",
    "    if (cloudDetectadosUnsub) { cloudDetectadosUnsub(); cloudDetectadosUnsub = null; }\n"
    "    detectados = [];\n"
    "    refreshDetectarBtn();\n"
    "    document.getElementById('mainApp').hidden = true;")

# ---------- 7. Click en Detectar: progreso vía refreshDetectarBtn + guarda anti-doble-clic ----------
rep(HTML,
    "document.getElementById('btnDetectar').addEventListener('click', function () {\n"
    "  var btn = document.getElementById('btnDetectar');\n"
    "  if (!window.Desktop || !window.Desktop.detect) { alert('La detección solo funciona en la app de escritorio.'); return; }\n"
    "  if (!cloudUser) { alert('Inicia sesión para reportar el equipo detectado.'); return; }\n"
    "  var oldHtml = btn.innerHTML;\n"
    "  btn.disabled = true;\n"
    "  btn.innerHTML = '<span class=\"ic\">&#128187;</span><span>Detectando software...</span>';\n"
    "  var p;\n"
    "  try { p = Promise.resolve(window.Desktop.detect()); } catch (e) { btn.disabled = false; btn.innerHTML = oldHtml; alert('No se pudo detectar el equipo.'); return; }\n"
    "  p.then(function (info) {\n"
    "    if (!window.Cloud || !window.Cloud.reportDetected) throw new Error('sin-nube');\n"
    "    var data = Object.assign({}, info || {});\n"
    "    data.detectadoPor = technicianName();\n"
    "    return window.Cloud.reportDetected(data);\n"
    "  }).then(function () { alert('Equipo detectado, ya aparece en los teléfonos'); }).catch(function (e) { alert('No se pudo detectar el equipo.' + (e && e.message ? ' ' + e.message : '')); }).then(function () { btn.disabled = false; btn.innerHTML = oldHtml; });\n"
    "});",
    "document.getElementById('btnDetectar').addEventListener('click', function () {\n"
    "  var btn = document.getElementById('btnDetectar');\n"
    "  if (!window.Desktop || !window.Desktop.detect) { alert('La detección solo funciona en la app de escritorio.'); return; }\n"
    "  if (!cloudUser) { alert('Inicia sesión para reportar el equipo detectado.'); return; }\n"
    "  if (btn.disabled) return; // ya detectando, o esta máquina ya tiene una detección pendiente\n"
    "  var oldHtml = btn.innerHTML;\n"
    "  detectingNow = true;\n"
    "  refreshDetectarBtn();\n"
    "  var p;\n"
    "  try { p = Promise.resolve(window.Desktop.detect()); } catch (e) { detectingNow = false; btn.disabled = false; btn.innerHTML = oldHtml; refreshDetectarBtn(); alert('No se pudo detectar el equipo.'); return; }\n"
    "  p.then(function (info) {\n"
    "    if (!window.Cloud || !window.Cloud.reportDetected) throw new Error('sin-nube');\n"
    "    var data = Object.assign({}, info || {});\n"
    "    data.detectadoPor = technicianName();\n"
    "    return window.Cloud.reportDetected(data);\n"
    "  }).then(function () { alert('Equipo detectado, ya aparece en los teléfonos'); }).catch(function (e) { alert('No se pudo detectar el equipo.' + (e && e.message ? ' ' + e.message : '')); }).then(function () { detectingNow = false; btn.disabled = false; btn.innerHTML = oldHtml; refreshDetectarBtn(); });\n"
    "});")

# ---------- 8. android/app/build.gradle ----------
rep(GRADLE, '        versionCode 45\n', '        versionCode 46\n')
rep(GRADLE, '        versionName "2.3.2"\n', '        versionName "2.3.3"\n')

# ---------- 9. iOS ----------
rep_all(PBX, '\t\t\t\tCURRENT_PROJECT_VERSION = 45;\n', '\t\t\t\tCURRENT_PROJECT_VERSION = 46;\n', 2)
rep_all(PBX, '\t\t\t\tMARKETING_VERSION = 2.3.2;\n', '\t\t\t\tMARKETING_VERSION = 2.3.3;\n', 2)

# ---------- 10. Verificación: sin restos de 2.3.2 en index.html ----------
with open(HTML, encoding='utf-8') as f:
    html = f.read()
assert '2.3.2' not in html, 'Quedan restos de 2.3.2 en index.html'
assert html.count('2.3.3') == 13, 'OCURRENCIAS 2.3.3=%d (esperadas 13: 12 de versión + 1 del comentario nuevo)' % html.count('2.3.3')
assert 'Versión 2.3.3' in html and 'Versión: 2.3.3' in html
print('OK: index.html sin restos de 2.3.2; 12 menciones de 2.3.3')

# ---------- 11. tests/test20233.js: versión y extraído ----------
rep(TEST_NEW, "fs.readFileSync(__dirname + '/checklist20232.js', 'utf8')",
    "fs.readFileSync(__dirname + '/checklist20233.js', 'utf8')")
rep(TEST_NEW,
    "console.log('AM0) versión 2.3.2:', html.includes('Versión 2.3.2'), '| sin 2.3.1:', !html.includes('Versión 2.3.1'),",
    "console.log('AM0) versión 2.3.3:', html.includes('Versión 2.3.3'), '| sin 2.3.2:', !html.includes('Versión 2.3.2'),")
rep(TEST_NEW,
    "  // AP0: estáticos 2.3.2 (versión, 17 detectables, nunca-marcar, defaults viejos).",
    "  // AP0: estáticos 2.3.3 (versión, 17 detectables, nunca-marcar, defaults viejos).")
rep(TEST_NEW,
    "console.log('AP0) estáticos 2.3.2: versión:', html.includes('Versión 2.3.2') && !html.includes('Versión 2.3.1'),",
    "console.log('AP0) estáticos 2.3.3: versión:', html.includes('Versión 2.3.3') && !html.includes('Versión 2.3.2'),")

# ---------- 12. Serie AQ ----------
AQ = '''
  // AQ0: reportDetected (firebase.js) usa machineId como id y resetea usado/detectadoEn.
  var repMatch = fb.match(/async function reportDetected\\(info\\) \\{[\\s\\S]*?\\n\\}/);
  var __savedDet = [];
  var reportDetected = repMatch ? new Function('db', 'doc', 'setDoc', repMatch[0] + '\\nreturn reportDetected;')({}, function (db, col, id) { return { col: col, id: id }; }, async function (ref, data, opts) { __savedDet.push([ref, data, opts]); }) : null;
  var beforeAq = Date.now();
  await reportDetected({ machineId: 'SERIE123', hostname: 'PC-01', marca: 'HP', modelo: 'EliteDesk', serie: 'SERIE123', detectadoEn: beforeAq - 86400000, detectadoPor: 'Gerardo', usado: true });
  var saveAq1 = __savedDet[0];
  __savedDet.length = 0;
  await reportDetected({ machineId: 'PC-02-AABBCCDDEEFF', hostname: 'PC-02', serie: '', detectadoEn: beforeAq - 3600000, usado: true });
  var saveAq2 = __savedDet[0];
  __savedDet.length = 0;
  await reportDetected({ hostname: 'PC-03', serie: 'SERIE789', detectadoEn: beforeAq - 60000 });
  var saveAq3 = __savedDet[0];
  __savedDet.length = 0;
  await reportDetected({ hostname: 'PC-04', detectadoEn: 1700000000000 });
  var saveAq4 = __savedDet[0];
  console.log('AQ0) reportDetected extraído:', !!reportDetected, '| machineId por serie como id:', saveAq1[0].id === 'SERIE123' && saveAq1[1].machineId === 'SERIE123', '| machineId por hostname+MAC como id:', saveAq2[0].id === 'PC-02-AABBCCDDEEFF', '| sin machineId, serie como id:', saveAq3[0].id === 'SERIE789', '| sin serie, hostname+detectadoEn:', saveAq4[0].id === 'PC-04-1700000000000', '| re-detectar resetea usado:', saveAq1[1].usado === false && saveAq2[1].usado === false, '| detectadoEn es ahora:', saveAq1[1].detectadoEn >= beforeAq && saveAq1[1].detectadoEn <= Date.now(), '| merge:', saveAq1[2] && saveAq1[2].merge === true, '| bundle trae el machineId:', fbBundle.includes('machineId'));
  // AQ1: el botón se bloquea con detección pendiente de ESTA máquina.
  doLogin('usuario');
  CLOUD_ENABLED = true;
  cloudUser = { uid: 'u1', email: 'test@checklist.local', nombre: 'Test User' };
  var btnAq = document.getElementById('btnDetectar');
  global.Desktop = { getMachineId: async function () { return 'SERIE-AAA'; }, detect: async function () { return {}; } };
  await loadMachineId();
  var midOk = machineId === 'SERIE-AAA';
  detectados = [{ id: 'SERIE-AAA', hostname: 'PC-AAA', marca: 'HP', modelo: 'EliteDesk', serie: 'SERIE-AAA', tipo: 'Desktop', detectadoEn: Date.now() - 60000, detectadoPor: 'Gerardo', usado: false }];
  renderDetectados();
  var blockedOk = btnAq.disabled === true && btnAq.innerHTML.indexOf('Equipo detectado') !== -1;
  // AQ2: la detección de OTRA máquina no bloquea esta.
  detectados = [{ id: 'PC-OTRA-AABBCCDDEEFF', hostname: 'PC-OTRA', marca: 'Dell', modelo: 'OptiPlex', serie: 'OTRA1', tipo: 'Desktop', detectadoEn: Date.now() - 60000, detectadoPor: 'Alejandro', usado: false }];
  renderDetectados();
  var otherOk = btnAq.disabled === false && btnAq.innerHTML.indexOf('Equipo detectado') === -1;
  console.log('AQ1) machineId de esta PC:', midOk, '| pendiente de esta máquina bloquea el botón:', blockedOk, '| AQ2) pendiente de otra máquina no bloquea:', otherOk);
  // AQ3: al usar o descartar la entrada, el botón se vuelve a habilitar.
  detectados = [{ id: 'SERIE-AAA', hostname: 'PC-AAA', marca: 'HP', modelo: 'EliteDesk', serie: 'SERIE-AAA', tipo: 'Desktop', detectadoEn: Date.now() - 60000, detectadoPor: 'Gerardo', usado: false }];
  renderDetectados();
  var wasBlocked = btnAq.disabled === true;
  detectados = [{ id: 'SERIE-AAA', hostname: 'PC-AAA', marca: 'HP', modelo: 'EliteDesk', serie: 'SERIE-AAA', tipo: 'Desktop', detectadoEn: Date.now() - 60000, detectadoPor: 'Gerardo', usado: true }];
  renderDetectados();
  var unblockedUse = btnAq.disabled === false && btnAq.innerHTML.indexOf('Equipo detectado') === -1;
  detectados = [{ id: 'SERIE-AAA', hostname: 'PC-AAA', marca: 'HP', modelo: 'EliteDesk', serie: 'SERIE-AAA', tipo: 'Desktop', detectadoEn: Date.now() - 60000, detectadoPor: 'Gerardo', usado: false }];
  renderDetectados();
  detectados = [];
  renderDetectados();
  var unblockedDel = btnAq.disabled === false && btnAq.innerHTML.indexOf('Detectar este equipo') !== -1;
  console.log('AQ3) bloqueado antes de usar:', wasBlocked, '| al marcar usado se habilita:', unblockedUse, '| al descartar se habilita y vuelve la etiqueta:', unblockedDel);
  // AQ4: con el botón bloqueado, hacer clic no vuelve a detectar; desbloqueado sí.
  var repAq = [];
  global.Cloud.reportDetected = async function (info) { repAq.push(info); };
  detectados = [{ id: 'SERIE-AAA', hostname: 'PC-AAA', marca: 'HP', modelo: 'EliteDesk', serie: 'SERIE-AAA', tipo: 'Desktop', detectadoEn: Date.now() - 60000, detectadoPor: 'Gerardo', usado: false }];
  renderDetectados();
  document.getElementById('btnDetectar')._h.click[0]();
  await sleep(20);
  var noRedetect = repAq.length === 0;
  detectados = [];
  renderDetectados();
  document.getElementById('btnDetectar')._h.click[0]();
  await sleep(20);
  var redetectOk = repAq.length === 1 && repAq[0].detectadoPor === 'Test User';
  console.log('AQ4) bloqueado no re-detecta:', noRedetect, '| desbloqueado sí detecta con el técnico:', redetectOk);
  // AQ5: sin getMachineId (o si falla) no hay bloqueo y nada se rompe.
  global.Desktop = { detect: async function () { return {}; } };
  await loadMachineId();
  var noMid = machineId === null;
  detectados = [{ id: 'SERIE-AAA', hostname: 'PC-AAA', marca: 'HP', modelo: 'EliteDesk', serie: 'SERIE-AAA', tipo: 'Desktop', detectadoEn: Date.now() - 60000, detectadoPor: 'Gerardo', usado: false }];
  renderDetectados();
  var noBlockNoMid = btnAq.disabled === false;
  global.Desktop = { getMachineId: async function () { throw new Error('sin detector'); }, detect: async function () { return {}; } };
  await loadMachineId();
  var noMidErr = machineId === null;
  renderDetectados();
  var noBlockErr = btnAq.disabled === false;
  global.Desktop = undefined;
  console.log('AQ5) sin getMachineId no hay machineId:', noMid, '| y no bloquea:', noBlockNoMid, '| si getMachineId falla no hay machineId:', noMidErr, '| y no bloquea ni rompe:', noBlockErr);
  // AQ6: la suscripción de detectados actualiza el botón al llegar cambios.
  global.Desktop = { getMachineId: async function () { return 'SERIE-AAA'; }, detect: async function () { return {}; } };
  var detCbAq = null;
  global.Cloud.getUserDoc = async function () { return { activo: true, rol: 'usuario', nombre: 'Test User', email: 'test@checklist.local' }; };
  global.Cloud.isInitialized = async function () { return true; };
  global.Cloud.getAllRenta = async function () { return []; };
  global.Cloud.upsertRenta = async function () {};
  global.Cloud.getAllPreparations = async function () { return []; };
  global.Cloud.upsertPrep = async function () {};
  global.Cloud.subscribeRenta = function () { return function () {}; };
  global.Cloud.subscribePreparations = function () { return function () {}; };
  global.Cloud.subscribeDetectados = function (cb) { detCbAq = cb; return function () {}; };
  global.Cloud.subscribePresence = function () { return function () {}; };
  global.Cloud.subscribeChat = function () { return function () {}; };
  global.Cloud.subscribeDm = function () { return function () {}; };
  global.Cloud.heartbeat = function () {};
  global.Cloud.pruneChat = function () {};
  global.Cloud.clearPresence = function () {};
  global.Cloud.listUsers = async function () { return []; };
  localStorage.setItem('checklist-soporte-migrado-v2:u1', '1');
  localStorage.setItem('checklist-soporte-migrado-preps-v1:u1', '1');
  state.preparations = [];
  state.renta = [];
  await onAuthChanged({ uid: 'u1', email: 'test@checklist.local' });
  await sleep(20);
  var subOk = typeof detCbAq === 'function' && machineId === 'SERIE-AAA';
  detCbAq([{ id: 'SERIE-AAA', hostname: 'PC-AAA', marca: 'HP', modelo: 'EliteDesk', serie: 'SERIE-AAA', tipo: 'Desktop', detectadoEn: Date.now(), detectadoPor: 'Gerardo', usado: false }]);
  var subBlocked = btnAq.disabled === true && btnAq.innerHTML.indexOf('Equipo detectado') !== -1;
  detCbAq([]);
  var subUnblocked = btnAq.disabled === false;
  global.Desktop = undefined;
  console.log('AQ6) suscripción llega y machineId cargado:', subOk, '| pendiente de esta máquina bloquea:', subBlocked, '| al vaciarse se desbloquea:', subUnblocked);
'''
with open(TEST_NEW, encoding='utf-8') as f:
    t = f.read()
anchor = '  process.exit(0);'
assert t.count(anchor) == 1, 'Ancla process.exit no única'
t = t.replace(anchor, AQ + '\n' + anchor, 1)
with open(TEST_NEW, 'w', encoding='utf-8') as f:
    f.write(t)
print('OK: serie AQ añadida a test20233.js')

# ---------- 13. Extraer tests/checklist20233.js del index.html nuevo ----------
with open(HTML, encoding='utf-8') as f:
    lines = f.read().split('\n')
start = next(i for i, ln in enumerate(lines) if ln == '<script>')
end = next(i for i, ln in enumerate(lines) if ln == '</script>')
assert end > start, 'No se encontró el script inline'
with open(EXTRACT, 'w', encoding='utf-8') as f:
    f.write('\n' + '\n'.join(lines[start + 1:end]) + '\n')
print('OK: extraído tests/checklist20233.js (script inline, líneas %d-%d)' % (start + 2, end))

print('Parche 2.3.3 aplicado (bundle pendiente de reconstruir con esbuild).')
