#!/usr/bin/env python3
"""Parche 2.3.4: integración (solo versión + pruebas).

- www/index.html: versión 2.3.3 -> 2.3.4 (13 ocurrencias: 2 visibles +
  10 comentarios históricos + 2 en el mailto de reporte). Sin cambios de
  código: la edición de un equipo guardado NO existe (ver serie AR) y el
  diagnóstico de edición en escritorio NO se reproduce (smoke-write
  2.3.4 pasa), así que no hay causa que corregir.
- www/cloud/firebase.js: SIN cambios en 2.3.4 -> NO se reconstruye el
  bundle (firebase.bundle.js queda como está).
- android/app/build.gradle: versionCode 46 -> 47, versionName 2.3.4.
- ios project.pbxproj: MARKETING_VERSION 2.3.4 (x2), CURRENT_PROJECT_VERSION 47 (x2).
- Escritorio (~/workspace/android/checklist-desktop/): package.json
  version + description a 2.3.4; main.js y preload.js solo su línea 1
  (cabecera). Los comentarios "(2.3.3)" son marcas históricas de la
  versión que introdujo machineId y NO se tocan (igual que en 2.3.3 no
  se tocaron los "(2.3.2)").
- tests: copia test20233.js a test20234.js, actualiza versión y extraído,
  añade serie AR, extrae tests/checklist20234.js del index.html nuevo.
Cada reemplazo con assert: si el texto viejo no está, se para.
"""
import shutil

CLOUD = '/home/hatch/workspace/android/checklist-cloud/'
DESK = '/home/hatch/workspace/android/checklist-desktop/'
HTML = CLOUD + 'www/index.html'
FB = CLOUD + 'www/cloud/firebase.js'
GRADLE = CLOUD + 'android/app/build.gradle'
PBX = CLOUD + 'ios/App/App.xcodeproj/project.pbxproj'
TEST_OLD = CLOUD + 'tests/test20233.js'
TEST_NEW = CLOUD + 'tests/test20234.js'
EXTRACT = CLOUD + 'tests/checklist20234.js'
DPKG = DESK + 'package.json'
DMAIN = DESK + 'main.js'
DPRE = DESK + 'preload.js'


def rep(path, old, new, count=1):
    with open(path, encoding='utf-8') as f:
        s = f.read()
    assert old in s, 'NO ENCONTRADO en %s: %r' % (path, old[:90])
    assert s.count(old) == count, 'OCURRENCIAS=%d (esperadas %d) en %s: %r' % (s.count(old), count, path, old[:90])
    with open(path, 'w', encoding='utf-8') as f:
        f.write(s.replace(old, new, count) if count == 1 else s.replace(old, new))
    print('OK:', path.split('/')[-1], '->', new[:70].replace('\n', ' '))


# ---------- 0. Backups 2.3.3 ----------
shutil.copyfile(HTML, CLOUD + 'tests/checklist-2.3.3.html.bak')
shutil.copyfile(FB, CLOUD + 'tests/firebase-2.3.3.js.bak')
print('OK: backups tests/checklist-2.3.3.html.bak y tests/firebase-2.3.3.js.bak')

# ---------- 0b. Copia del test ----------
shutil.copyfile(TEST_OLD, TEST_NEW)
print('OK: test20233.js copiado a test20234.js')

# ---------- 1. www/index.html: versión 2.3.3 -> 2.3.4 (13 ocurrencias) ----------
with open(HTML, encoding='utf-8') as f:
    html = f.read()
assert html.count('2.3.3') == 13, 'OCURRENCIAS 2.3.3=%d (esperadas 13)' % html.count('2.3.3')
assert '2.3.4' not in html, 'Ya hay 2.3.4 en index.html'
with open(HTML, 'w', encoding='utf-8') as f:
    f.write(html.replace('2.3.3', '2.3.4'))
print('OK: index.html versión 2.3.4 (13 ocurrencias)')

# ---------- 2. android/app/build.gradle ----------
rep(GRADLE, '        versionCode 46\n', '        versionCode 47\n')
rep(GRADLE, '        versionName "2.3.3"\n', '        versionName "2.3.4"\n')

# ---------- 3. iOS project.pbxproj ----------
rep(PBX, 'MARKETING_VERSION = 2.3.3;', 'MARKETING_VERSION = 2.3.4;', count=2)
rep(PBX, 'CURRENT_PROJECT_VERSION = 46;', 'CURRENT_PROJECT_VERSION = 47;', count=2)

# ---------- 4. Escritorio: package.json (version + description), main.js / preload.js (línea 1) ----------
rep(DPKG, '  "version": "2.3.3",', '  "version": "2.3.4",')
rep(DPKG, 'Checklist de Soporte 2.3.3 para escritorio', 'Checklist de Soporte 2.3.4 para escritorio')
rep(DMAIN, '// Checklist de Soporte 2.3.3 — app de escritorio (Electron).',
    '// Checklist de Soporte 2.3.4 — app de escritorio (Electron).')
rep(DPRE, '// Preload de Checklist de Soporte 2.3.3 (Electron).',
    '// Preload de Checklist de Soporte 2.3.4 (Electron).')

# ---------- 5. Verificación: sin restos de 2.3.3 en index.html ----------
with open(HTML, encoding='utf-8') as f:
    html = f.read()
assert '2.3.3' not in html, 'Quedan restos de 2.3.3 en index.html'
assert html.count('2.3.4') == 13, 'OCURRENCIAS 2.3.4=%d (esperadas 13)' % html.count('2.3.4')
assert 'Versión 2.3.4' in html and 'Versión: 2.3.4' in html
print('OK: index.html sin restos de 2.3.3; 13 menciones de 2.3.4')

# ---------- 6. tests/test20234.js: versión y extraído ----------
rep(TEST_NEW, "fs.readFileSync(__dirname + '/checklist20233.js', 'utf8')",
    "fs.readFileSync(__dirname + '/checklist20234.js', 'utf8')")
rep(TEST_NEW,
    "console.log('AM0) versión 2.3.3:', html.includes('Versión 2.3.3'), '| sin 2.3.2:', !html.includes('Versión 2.3.2'),",
    "console.log('AM0) versión 2.3.4:', html.includes('Versión 2.3.4'), '| sin 2.3.3:', !html.includes('Versión 2.3.3'),")
rep(TEST_NEW,
    "  // AP0: estáticos 2.3.3 (versión, 17 detectables, nunca-marcar, defaults viejos).",
    "  // AP0: estáticos 2.3.4 (versión, 17 detectables, nunca-marcar, defaults viejos).")
rep(TEST_NEW,
    "console.log('AP0) estáticos 2.3.3: versión:', html.includes('Versión 2.3.3') && !html.includes('Versión 2.3.2'),",
    "console.log('AP0) estáticos 2.3.4: versión:', html.includes('Versión 2.3.4') && !html.includes('Versión 2.3.3'),")

# ---------- 7. Serie AR: Guardar (formReady) y no-edición ----------
AR = '''
  // AR0: versión 2.3.4 en los lugares visibles y 0 de 2.3.3 en todo el html.
  var n234 = (html.match(/2\\.3\\.4/g) || []).length;
  console.log('AR0) versión 2.3.4 visible:', html.includes('Versión 2.3.4') && html.includes('Versión: 2.3.4'), '| 0 de 2.3.3:', !html.includes('2.3.3'), '| ocurrencias 2.3.4:', n234 === 13);
  // AR1: formReady / botón Guardar (2.3.4, sin cambios): solo modelo, serie o
  // usuario habilitan Guardar. Marca, inventario, hostname, área, correo y
  // analista NO habilitan por sí solos: si Gerardo llenó solo esos campos,
  // el botón sigue deshabilitado con el hint 'Completa al menos el modelo...'.
  // Eso explica el reporte de "no se puede editar/guardar" sin que haya bug.
  var setF = function (id, v) { document.getElementById(id).value = v; };
  var allForm = ['fMarca', 'fModelo', 'fSerie', 'fInv', 'fHostname', 'fTec', 'fUser', 'fArea', 'fCorreo'];
  allForm.forEach(function (id) { setF(id, ''); });
  updateSaveBtn();
  var disVacio = document.getElementById('btnAdd').disabled === true && formReady() === false;
  setF('fMarca', 'HP'); setF('fInv', '100'); setF('fHostname', 'PC-01');
  setF('fArea', 'Soporte'); setF('fCorreo', 'a@empresa.com'); setF('fTec', 'Juan Pérez');
  updateSaveBtn();
  var disSoloOtros = document.getElementById('btnAdd').disabled === true && formReady() === false;
  var hintOtros = document.getElementById('saveHint').textContent.indexOf('Completa al menos el modelo') === 0;
  setF('fModelo', '   '); updateSaveBtn();
  var disBlancos = document.getElementById('btnAdd').disabled === true && formReady() === false;
  setF('fModelo', 'ProBook 440'); updateSaveBtn();
  var enModelo = document.getElementById('btnAdd').disabled === false && formReady() === true;
  setF('fModelo', ''); setF('fSerie', 'S-123'); updateSaveBtn();
  var enSerie = document.getElementById('btnAdd').disabled === false && formReady() === true;
  setF('fSerie', ''); setF('fUser', 'Ana'); updateSaveBtn();
  var enUser = document.getElementById('btnAdd').disabled === false && formReady() === true;
  var hintListo = document.getElementById('saveHint').textContent.indexOf('Datos listos') === 0;
  allForm.forEach(function (id) { setF(id, ''); });
  updateSaveBtn();
  console.log('AR1) Guardar deshabilitado vacío:', disVacio, '| solo marca/inv/host/área/correo/analista:', disSoloOtros, '| hint pide modelo/serie/usuario:', hintOtros, '| solo espacios no habilita:', disBlancos, '| habilita con modelo:', enModelo, '| con serie:', enSerie, '| con usuario:', enUser, '| hint cambia a Datos listos:', hintListo);
  // AR2: NO existe edición de un equipo ya guardado (2.3.4). No hay botón ni
  // handler de edición en la tarjeta: sin data-edit-prep, sin editPrep, sin
  // 'Editar equipo' en el html ni en el script renderizado. Las acciones de
  // la tarjeta son solo: Listo, Entregado, Quitar listo, Reabrir, + Punto
  // extra, PDF, ¿Qué falta?, Excel, WhatsApp, Resumen IA, correo, Reasignar
  // (admin) y Eliminar (admin). Lo único que cambia la asignación es
  // Reasignar, que solo cambia el nombre y BORRA área y correo (doReassign).
  var noEditHtml = html.indexOf('data-edit-prep') === -1 && html.indexOf('editPrep') === -1 && html.indexOf('Editar equipo') === -1;
  var noEditSrc = SRC.indexOf('data-edit-prep') === -1 && SRC.indexOf('editPrep') === -1 && SRC.indexOf('Editar equipo') === -1;
  var cardHas = function (a) { return SRC.indexOf(a) !== -1; };
  var cardActions = cardHas("data-ready=") && cardHas("data-deliver=") && cardHas("data-unready=") && cardHas("data-reopen=") && cardHas("data-add-extra=") && cardHas("data-pdf=") && cardHas("data-xlsx=") && cardHas("data-wa=") && cardHas("data-mail=") && cardHas("data-reassign=") && cardHas("data-del-prep=");
  var reassignWipes = SRC.indexOf("prep.usuario.nombre = a; prep.usuario.area = ''; prep.usuario.correo = '';") !== -1;
  console.log('AR2) sin edición en html:', noEditHtml, '| sin edición en script:', noEditSrc, '| acciones de tarjeta completas (sin editar):', cardActions, '| Reasignar cambia solo nombre y borra área/correo:', reassignWipes);
'''
with open(TEST_NEW, encoding='utf-8') as f:
    t = f.read()
anchor = '  process.exit(0);'
assert t.count(anchor) == 1, 'Ancla process.exit no única'
t = t.replace(anchor, AR + anchor, 1)
with open(TEST_NEW, 'w', encoding='utf-8') as f:
    f.write(t)
print('OK: serie AR añadida a test20234.js')

# ---------- 8. Extraer tests/checklist20234.js del index.html nuevo ----------
with open(HTML, encoding='utf-8') as f:
    lines = f.read().split('\n')
start = next(i for i, ln in enumerate(lines) if ln == '<script>')
end = next(i for i, ln in enumerate(lines) if ln == '</script>')
assert end > start, 'No se encontró el script inline'
with open(EXTRACT, 'w', encoding='utf-8') as f:
    f.write('\n' + '\n'.join(lines[start + 1:end]) + '\n')
print('OK: extraído tests/checklist20234.js (script inline, líneas %d-%d)' % (start + 2, end))

print('Parche 2.3.4 aplicado (firebase.js sin cambios: bundle NO reconstruido).')
