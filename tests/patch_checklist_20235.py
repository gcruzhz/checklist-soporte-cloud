#!/usr/bin/env python3
"""Parche 2.3.5: versión + línea 'Escritorio revisado' en detectados + serie AS.

AUDITORÍA 'Usar este equipo' (sin causa DEFINIDA en el código del teléfono,
así que NO hay parche de comportamiento para ese camino; ver serie AS):
- Handler detList (index.html:2130-2158): rellena fTipo/fMarca/fModelo/
  fSerie/fHostname (2139-2143), guarda stashes (2144-2148), marca usado
  (2154), detBox.hidden=true + newBox.hidden=false (2155-2156) y llama
  updateSaveBtn() (2157). NO toca fInv/fUser/fArea/fCorreo: ni los limpia,
  ni los deshabilita, ni los marca readonly.
- Sospechoso (a) REFUTADO: subscribeDetectados (1072-1078) solo hace
  `detectados = docs; renderDetectados();` y renderDetectados() (873-897)
  solo reescribe #detList.innerHTML + refreshDetectarBtn() (solo toca
  #btnDetectar). NUNCA llama a render(). render() (1809-1829) reescribe
  solo #list, #tplList, renta/entrega y contadores; #newBox (HTML
  estático, líneas 257-278) no está dentro de ningún contenedor que
  render()/renderDetectados() reescriban. Lo tecleado no se puede borrar
  por la suscripción.
- Sospechoso (b) REFUTADO en lo que importa: el rellenado por código no
  dispara 'input', pero el handler llama updateSaveBtn() al final, y
  formReady() (1941-1943) habilita Guardar con modelo/serie/usuario
  detectados. Los listeners 'input' existen en fModelo/fSerie/fUser
  (1952-1954). Queda el matiz documentado en AR1: teclear SOLO
  inventario/área/correo NO habilita Guardar (por diseño), pero eso no
  impide teclear.
- Sospechoso (c) REFUTADO: detBox se cierra con hidden=true (2155) y el
  CSS `[hidden] { display: none !important; }` (línea 134) lo oculta de
  verdad; .panel es estático, sin overlay ni z-index.
- Sospechoso (d) REFUTADO: cloudMarkDetectadoUsado (728-730) está
  guardado y con .catch interno, nunca lanza; si algo fallara antes de
  2155 el formulario quedaría vacío, no lleno-pero-bloqueado. No hay
  disabled/readonly en fInv/fUser/fArea/fCorreo (grep: solo #btnAdd y
  #btnDetectar se deshabilitan), no hay <form> alrededor de newBox, ni
  handlers de focus/blur/preventDefault sobre esos campos.
- La copia de escritorio (checklist-desktop/www/index.html) es idéntica
  a la del cloud (mismo md5 e1b216c07fa77d2151f0f2d98e169119): el .exe no
  lleva un www viejo. Lo que queda fuera del código del teléfono es el
  diagnóstico de Electron real (foco/overlay en Chromium): lo lleva el
  agente de escritorio en paralelo.
- NUEVO (adición 2.3.5): el detector guarda en detalles.escritorioRutas
  (array de rutas de Escritorio escaneadas) y detalles.atajosVistos
  (número de .lnk/.url). renderDetectados() muestra ahora la línea
  'Escritorio revisado: <ruta1, ruta2> · N atajos vistos' solo cuando
  esos campos existen (helper escritorioLine()).
- www/cloud/firebase.js: SIN cambios en 2.3.5 -> NO se reconstruye el
  bundle (firebase.bundle.js queda como está).
- android/app/build.gradle: versionCode 47 -> 48, versionName 2.3.5.
- ios project.pbxproj: MARKETING_VERSION 2.3.5 (x2), CURRENT_PROJECT_VERSION 48 (x2).
- tests: copia test20234.js a test20235.js, actualiza versión y extraído,
  añade serie AS, extrae tests/checklist20235.js del index.html nuevo.
Cada reemplazo con assert: si el texto viejo no está, se para.
"""
import shutil

CLOUD = '/home/hatch/workspace/android/checklist-cloud/'
HTML = CLOUD + 'www/index.html'
FB = CLOUD + 'www/cloud/firebase.js'
GRADLE = CLOUD + 'android/app/build.gradle'
PBX = CLOUD + 'ios/App/App.xcodeproj/project.pbxproj'
TEST_OLD = CLOUD + 'tests/test20234.js'
TEST_NEW = CLOUD + 'tests/test20235.js'
EXTRACT = CLOUD + 'tests/checklist20235.js'


def rep(path, old, new, count=1):
    with open(path, encoding='utf-8') as f:
        s = f.read()
    assert old in s, 'NO ENCONTRADO en %s: %r' % (path, old[:90])
    assert s.count(old) == count, 'OCURRENCIAS=%d (esperadas %d) en %s: %r' % (s.count(old), count, path, old[:90])
    with open(path, 'w', encoding='utf-8') as f:
        f.write(s.replace(old, new, count) if count == 1 else s.replace(old, new))
    print('OK:', path.split('/')[-1], '->', new[:70].replace('\n', ' '))


# ---------- 0. Backups 2.3.4 ----------
shutil.copyfile(HTML, CLOUD + 'tests/checklist-2.3.4.html.bak')
shutil.copyfile(FB, CLOUD + 'tests/firebase-2.3.4.js.bak')
print('OK: backups tests/checklist-2.3.4.html.bak y tests/firebase-2.3.4.js.bak')

# ---------- 0b. Copia del test ----------
shutil.copyfile(TEST_OLD, TEST_NEW)
print('OK: test20234.js copiado a test20235.js')

# ---------- 1. www/index.html: versión 2.3.4 -> 2.3.5 (13 ocurrencias, 12 líneas) ----------
with open(HTML, encoding='utf-8') as f:
    html = f.read()
assert html.count('2.3.4') == 13, 'OCURRENCIAS 2.3.4=%d (esperadas 13)' % html.count('2.3.4')
assert '2.3.5' not in html, 'Ya hay 2.3.5 en index.html'
with open(HTML, 'w', encoding='utf-8') as f:
    f.write(html.replace('2.3.4', '2.3.5'))
print('OK: index.html versión 2.3.5 (13 ocurrencias)')

# ---------- 2. android/app/build.gradle ----------
rep(GRADLE, '        versionCode 47\n', '        versionCode 48\n')
rep(GRADLE, '        versionName "2.3.4"\n', '        versionName "2.3.5"\n')

# ---------- 3. iOS project.pbxproj ----------
rep(PBX, 'MARKETING_VERSION = 2.3.4;', 'MARKETING_VERSION = 2.3.5;', count=2)
rep(PBX, 'CURRENT_PROJECT_VERSION = 47;', 'CURRENT_PROJECT_VERSION = 48;', count=2)

# ---------- 4. Línea 'Escritorio revisado' en la tarjeta de detectados ----------
HELPER = '''// Escritorio revisado: el detector guarda en detalles las rutas de
// Escritorio realmente escaneadas (escritorioRutas, array de strings) y
// cuántos .lnk/.url encontró (atajosVistos, número). Solo se muestra
// cuando esos campos existen en el equipo detectado: 'Escritorio
// revisado: <ruta1, ruta2>' y, si hay conteo, '· N atajos vistos'. Sin
// rutas ni conteo no hay línea. Una ruta suelta (string) se acepta como
// una sola ruta; el conteo solo vale si es número (0 incluido).
function escritorioLine(d) {
  var det = (d && d.detalles) || {};
  var rutas = det.escritorioRutas;
  if (typeof rutas === 'string' && rutas) rutas = [rutas];
  var n = det.atajosVistos;
  var parts = [];
  if (Array.isArray(rutas) && rutas.length) parts.push('Escritorio revisado: ' + rutas.join(', '));
  if (typeof n === 'number') parts.push(parts.length ? n + ' atajos vistos' : 'Atajos vistos: ' + n);
  if (!parts.length) return '';
  return parts.join(' \\u00b7 ');
}
'''
rep(HTML,
    "// Equipos detectados (2.3.5): solo se listan los NO usados, con sus datos\n"
    "// y dos acciones: usarlo (llena Nuevo equipo) o descartarlo.\n"
    "function renderDetectados() {",
    HELPER +
    "// Equipos detectados (2.3.5): solo se listan los NO usados, con sus datos\n"
    "// y dos acciones: usarlo (llena Nuevo equipo) o descartarlo.\n"
    "function renderDetectados() {")
rep(HTML,
    "    var verLine = versionesLine(d.versiones);\n"
    "    var adLine = anydeskLine(d);",
    "    var verLine = versionesLine(d.versiones);\n"
    "    var adLine = anydeskLine(d);\n"
    "    var escLine = escritorioLine(d);")
rep(HTML,
    "      (verLine ? '<div class=\"sub\">' + esc(verLine) + '</div>' : '') +\n",
    "      (verLine ? '<div class=\"sub\">' + esc(verLine) + '</div>' : '') +\n"
    "      (escLine ? '<div class=\"sub\">' + esc(escLine) + '</div>' : '') +\n")

# ---------- 5. Verificación: sin restos de 2.3.4 en index.html ----------
with open(HTML, encoding='utf-8') as f:
    html = f.read()
assert '2.3.4' not in html, 'Quedan restos de 2.3.4 en index.html'
assert html.count('2.3.5') == 13, 'OCURRENCIAS 2.3.5=%d (esperadas 13)' % html.count('2.3.5')
assert 'Versión 2.3.5' in html and 'Versión: 2.3.5' in html
assert 'escritorioLine' in html and 'escritorioRutas' in html and 'atajosVistos' in html
print('OK: index.html sin restos de 2.3.4; 13 menciones de 2.3.5; escritorioLine presente')

# ---------- 6. tests/test20235.js: versión y extraído ----------
rep(TEST_NEW, "fs.readFileSync(__dirname + '/checklist20234.js', 'utf8')",
    "fs.readFileSync(__dirname + '/checklist20235.js', 'utf8')")
rep(TEST_NEW,
    "console.log('AM0) versión 2.3.4:', html.includes('Versión 2.3.4'), '| sin 2.3.3:', !html.includes('Versión 2.3.3'),",
    "console.log('AM0) versión 2.3.5:', html.includes('Versión 2.3.5'), '| sin 2.3.4:', !html.includes('Versión 2.3.4'),")
rep(TEST_NEW,
    "  // AP0: estáticos 2.3.4 (versión, 17 detectables, nunca-marcar, defaults viejos).",
    "  // AP0: estáticos 2.3.5 (versión, 17 detectables, nunca-marcar, defaults viejos).")
rep(TEST_NEW,
    "console.log('AP0) estáticos 2.3.4: versión:', html.includes('Versión 2.3.4') && !html.includes('Versión 2.3.3'),",
    "console.log('AP0) estáticos 2.3.5: versión:', html.includes('Versión 2.3.5') && !html.includes('Versión 2.3.4'),")
rep(TEST_NEW,
    "  // AR0: versión 2.3.4 en los lugares visibles y 0 de 2.3.3 en todo el html.",
    "  // AR0: versión 2.3.5 en los lugares visibles y 0 de 2.3.4 en todo el html.")
rep(TEST_NEW,
    "  var n234 = (html.match(/2\\.3\\.4/g) || []).length;",
    "  var n235 = (html.match(/2\\.3\\.5/g) || []).length;")
rep(TEST_NEW,
    "console.log('AR0) versión 2.3.4 visible:', html.includes('Versión 2.3.4') && html.includes('Versión: 2.3.4'), '| 0 de 2.3.3:', !html.includes('2.3.3'), '| ocurrencias 2.3.4:', n234 === 13);",
    "console.log('AR0) versión 2.3.5 visible:', html.includes('Versión 2.3.5') && html.includes('Versión: 2.3.5'), '| 0 de 2.3.4:', !html.includes('2.3.4'), '| ocurrencias 2.3.5:', n235 === 13);")
rep(TEST_NEW,
    "  // AR1: formReady / botón Guardar (2.3.4, sin cambios): solo modelo, serie o",
    "  // AR1: formReady / botón Guardar (2.3.5, sin cambios): solo modelo, serie o")
rep(TEST_NEW,
    "  // AR2: NO existe edición de un equipo ya guardado (2.3.4). No hay botón ni",
    "  // AR2: NO existe edición de un equipo ya guardado (2.3.5). No hay botón ni")

# ---------- 7. Serie AS: camino 'Usar este equipo' + línea Escritorio revisado ----------
AS = r'''
  // AS0-AS3: camino 'Usar este equipo' (2.3.5). La prueba de escritura de
  // la 2.3.4 solo abrió el formulario EN BLANCO (btnShowNew); aquí se
  // recorre Detectar -> panel -> 'Usar este equipo' -> formulario, con
  // un target realista hecho a mano (closest/getAttribute), NO fakeClick:
  // el clic se dispara por el handler de #detList como en AN1/AO2.
  // OJO: en este harness invocar _h.click[0]() ejecuta el handler aunque
  // el botón esté disabled, así que la habilitación de Guardar se
  // comprueba leyendo btnAdd.disabled, no por que el clic funcione.
  doLogin('usuario');
  CLOUD_ENABLED = true;
  cloudUser = { uid: 'u1', email: 'test@checklist.local', nombre: 'Test User' };
  var markedAS = [];
  global.Cloud.markDetectadoUsado = async function (id) { markedAS.push(id); };
  var upAS = [];
  global.Cloud.upsertPrep = async function (d) { upAS.push(d); };
  var detAS = { id: 'AS-DET', hostname: 'PC-AS', marca: 'HP', modelo: 'EliteDesk 800', serie: 'AS-DET', cpu: 'Intel Core i7-10700', ramGB: 16, discoGB: 512, so: 'Windows 11 Pro', tipo: 'Desktop', detectadoEn: Date.now() - 60000, detectadoPor: 'Gerardo', usado: false, checks: { t18: true, t8: 'Office 365' }, detalles: { officeDetectado: true, escritorioRutas: ['C:\\Users\\gerardo\\Desktop', 'C:\\Users\\gerardo\\OneDrive - Empresa\\Desktop'], atajosVistos: 3 }, versiones: { so: 'Windows 11 Pro 26H2 (compilación 26200)' } };
  ['fTipo', 'fMarca', 'fModelo', 'fSerie', 'fInv', 'fHostname', 'fTec', 'fUser', 'fArea', 'fCorreo'].forEach(function (id) { document.getElementById(id).value = ''; });
  window._detectedChecks = null; window._detectedDetalles = null; window._detectedVersiones = null; window._detectedHardware = null;
  document.getElementById('detBox').hidden = false;
  document.getElementById('newBox').hidden = true;
  detectados = [detAS];
  renderDetectados();
  document.getElementById('detList')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-det-use]' ? { getAttribute: function () { return 'AS-DET'; } } : null; } } });
  var asFilled = document.getElementById('fTipo').value === 'Desktop' && document.getElementById('fMarca').value === 'HP' && document.getElementById('fModelo').value === 'EliteDesk 800' && document.getElementById('fSerie').value === 'AS-DET' && document.getElementById('fHostname').value === 'PC-AS';
  var asPanels = document.getElementById('detBox').hidden === true && document.getElementById('newBox').hidden === false;
  var asStash = window._detectedChecks && window._detectedChecks.t18 === true && window._detectedChecks.t8 === 'Office 365' && window._detectedDetalles && window._detectedDetalles.officeDetectado === true && window._detectedVersiones && window._detectedVersiones.so === 'Windows 11 Pro 26H2 (compilación 26200)' && window._detectedHardware && window._detectedHardware.cpu === 'Intel Core i7-10700';
  var asMarked = markedAS.indexOf('AS-DET') !== -1;
  var asSaveOn = document.getElementById('btnAdd').disabled === false && formReady() === true;
  var asHint = document.getElementById('saveHint').textContent.indexOf('Datos listos') === 0;
  console.log('AS0) Usar llena el formulario:', asFilled, '| cierra detBox y abre newBox:', asPanels, '| stash checks/detalles/versiones/hardware:', asStash, '| marca usado:', asMarked, '| Guardar habilitado con modelo/serie detectados:', asSaveOn, '| hint Datos listos:', asHint);
  // AS1: los campos de inventario, usuario, área y correo aceptan tecleo
  // y lo conservan. En el html son <input> planos, sin disabled ni
  // readonly; en el harness el tecleo se modela asignando .value y, para
  // fUser, disparando su listener 'input' real (updateSaveBtn).
  document.getElementById('fInv').value = 'INV-777';
  document.getElementById('fUser').value = 'Ana Pérez';
  document.getElementById('fArea').value = 'Soporte';
  document.getElementById('fCorreo').value = 'ana@empresa.com';
  document.getElementById('fUser')._h.input[0]();
  var asTyped = document.getElementById('fInv').value === 'INV-777' && document.getElementById('fUser').value === 'Ana Pérez' && document.getElementById('fArea').value === 'Soporte' && document.getElementById('fCorreo').value === 'ana@empresa.com';
  var asNotDis = ['fInv', 'fUser', 'fArea', 'fCorreo'].every(function (id) { return document.getElementById(id).disabled === false; });
  var asNotDisHtml = ['fInv', 'fUser', 'fArea', 'fCorreo'].every(function (id) { return html.indexOf('id="' + id + '" disabled') === -1 && html.indexOf('id="' + id + '" readonly') === -1; });
  var asSaveStill = document.getElementById('btnAdd').disabled === false && formReady() === true;
  console.log('AS1) inventario/usuario/área/correo aceptan tecleo y lo conservan:', asTyped, '| ninguno deshabilitado:', asNotDis, '| sin disabled/readonly en el html:', asNotDisHtml, '| Guardar sigue habilitado tras teclear:', asSaveStill);
  // AS2: un render() disparado por la suscripción de detectados NO borra
  // lo tecleado ni cierra el formulario. Se usa el callback vivo de la
  // suscripción (detCbAq, de AQ6): llega el eco de usado=true, que
  // re-renderiza detList, y luego render() completo.
  var asCbLive = typeof detCbAq === 'function';
  if (asCbLive) detCbAq([Object.assign({}, detAS, { usado: true })]);
  var asDetGone = document.getElementById('detList').innerHTML.indexOf('PC-AS') === -1;
  render();
  var asTypedKept = document.getElementById('fInv').value === 'INV-777' && document.getElementById('fUser').value === 'Ana Pérez' && document.getElementById('fArea').value === 'Soporte' && document.getElementById('fCorreo').value === 'ana@empresa.com' && document.getElementById('fModelo').value === 'EliteDesk 800' && document.getElementById('fSerie').value === 'AS-DET';
  var asFormOpen = document.getElementById('newBox').hidden === false && document.getElementById('detBox').hidden === true;
  var asSaveKept = document.getElementById('btnAdd').disabled === false;
  console.log('AS2) callback de suscripción vivo:', asCbLive, '| el usado desaparece del panel:', asDetGone, '| lo tecleado y lo detectado se conservan tras render():', asTypedKept, '| el formulario sigue abierto:', asFormOpen, '| Guardar sigue habilitado:', asSaveKept);
  // AS3: Guardar conserva inventario/usuario/área/correo + autoDetectado.
  // Se vuelve a comprobar btnAdd.disabled ANTES de pulsar: el handler
  // del harness no respeta disabled, así que el clic solo no probaría nada.
  var asCanSave = document.getElementById('btnAdd').disabled === false;
  var nBeforeAS = state.preparations.length;
  upAS.length = 0;
  document.getElementById('btnAdd')._h.click[0]();
  var savedAS = state.preparations[state.preparations.length - 1];
  var asSaved = state.preparations.length === nBeforeAS + 1 && !!savedAS && savedAS.equipo.inventario === 'INV-777' && savedAS.usuario.nombre === 'Ana Pérez' && savedAS.usuario.area === 'Soporte' && savedAS.usuario.correo === 'ana@empresa.com' && savedAS.equipo.modelo === 'EliteDesk 800' && savedAS.equipo.serie === 'AS-DET' && savedAS.equipo.hostname === 'PC-AS' && savedAS.checks.t18 === true && savedAS.checks.t8 === 'Office 365' && savedAS.autoDetectado.join(',') === 't8,t18';
  var asCloud = upAS.length === 1 && upAS[0].autoDetectado.join(',') === 't8,t18' && upAS[0].equipo.inventario === 'INV-777' && upAS[0].usuario.correo === 'ana@empresa.com';
  var asStashClean = window._detectedChecks === null && window._detectedDetalles === null && window._detectedVersiones === null && window._detectedHardware === null;
  var asClosed = document.getElementById('newBox').hidden === true;
  console.log('AS3) Guardar habilitado antes de pulsar:', asCanSave, '| guardado conserva inventario/usuario/área/correo + autoDetectado:', asSaved, '| sube a la nube igual:', asCloud, '| stash limpio tras guardar:', asStashClean, '| el formulario se cierra:', asClosed);
  // AS4: línea 'Escritorio revisado' en la tarjeta del detectado.
  var mkDetAS = function (over) { return Object.assign({ id: 'AS-ESC', hostname: 'PC-ESC', marca: 'HP', modelo: 'EliteDesk', serie: 'AS-ESC', tipo: 'Desktop', detectadoEn: Date.now(), detectadoPor: 'Gerardo', usado: false }, over || {}); };
  detectados = [mkDetAS({ detalles: { escritorioRutas: ['C:\\Users\\gerardo\\Desktop', 'C:\\Users\\gerardo\\OneDrive - Empresa\\Desktop'], atajosVistos: 3 } })];
  renderDetectados();
  var hEscA = document.getElementById('detList').innerHTML;
  var asEscA = hEscA.indexOf('Escritorio revisado: C:\\Users\\gerardo\\Desktop, C:\\Users\\gerardo\\OneDrive - Empresa\\Desktop') !== -1 && hEscA.indexOf('· 3 atajos vistos') !== -1;
  detectados = [mkDetAS({ detalles: { escritorioRutas: ['D:\\Escritorio'] } })];
  renderDetectados();
  var hEscB = document.getElementById('detList').innerHTML;
  var asEscB = hEscB.indexOf('Escritorio revisado: D:\\Escritorio') !== -1 && hEscB.indexOf('atajos vistos') === -1;
  detectados = [mkDetAS({ detalles: { atajosVistos: 5 } })];
  renderDetectados();
  var hEscC = document.getElementById('detList').innerHTML;
  var asEscC = hEscC.indexOf('Atajos vistos: 5') !== -1 && hEscC.indexOf('Escritorio revisado') === -1;
  detectados = [mkDetAS({ detalles: { escritorioRutas: ['C:\\Users\\x\\Desktop'], atajosVistos: 0 } })];
  renderDetectados();
  var hEscD = document.getElementById('detList').innerHTML;
  var asEscD = hEscD.indexOf('Escritorio revisado: C:\\Users\\x\\Desktop') !== -1 && hEscD.indexOf('· 0 atajos vistos') !== -1;
  console.log('AS4) rutas + conteo:', asEscA, '| solo rutas (sin conteo):', asEscB, '| solo conteo:', asEscC, '| conteo 0 también se muestra:', asEscD);
  // AS5: sin esos campos no hay línea; helper y campos existen en el código.
  detectados = [mkDetAS({ detalles: {} })];
  renderDetectados();
  var hEscE = document.getElementById('detList').innerHTML;
  var asEscE = hEscE.indexOf('Escritorio revisado') === -1 && hEscE.indexOf('atajos vistos') === -1;
  detectados = [mkDetAS({ detalles: { escritorioRutas: [] } })];
  renderDetectados();
  var hEscF = document.getElementById('detList').innerHTML;
  var asEscF = hEscF.indexOf('Escritorio revisado') === -1 && hEscF.indexOf('atajos vistos') === -1;
  var asEscStatic = SRC.indexOf('escritorioLine') !== -1 && SRC.indexOf('escritorioRutas') !== -1 && SRC.indexOf('atajosVistos') !== -1 && html.indexOf('escritorioLine(d)') !== -1;
  console.log('AS5) sin detalles no hay línea:', asEscE, '| array vacío no hay línea:', asEscF, '| helper y campos en el código:', asEscStatic);
'''
with open(TEST_NEW, encoding='utf-8') as f:
    t = f.read()
anchor = '  process.exit(0);'
assert t.count(anchor) == 1, 'Ancla process.exit no única'
t = t.replace(anchor, AS + anchor, 1)
with open(TEST_NEW, 'w', encoding='utf-8') as f:
    f.write(t)
print('OK: serie AS añadida a test20235.js')

# ---------- 8. Extraer tests/checklist20235.js del index.html nuevo ----------
with open(HTML, encoding='utf-8') as f:
    lines = f.read().split('\n')
start = next(i for i, ln in enumerate(lines) if ln == '<script>')
end = next(i for i, ln in enumerate(lines) if ln == '</script>')
assert end > start, 'No se encontró el script inline'
with open(EXTRACT, 'w', encoding='utf-8') as f:
    f.write('\n' + '\n'.join(lines[start + 1:end]) + '\n')
print('OK: extraído tests/checklist20235.js (script inline, líneas %d-%d)' % (start + 2, end))

print('Parche 2.3.5 aplicado (firebase.js sin cambios: bundle NO reconstruido).')
