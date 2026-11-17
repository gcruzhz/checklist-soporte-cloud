#!/usr/bin/env python3
"""Parche 239 (teléfono): botón '💾 Guardar avance' mientras se revisa el
checklist — Checklist de Soporte 2.3.9 (versionCode 52).

Pedido de Gerardo (2026-11-15 ~08:47): 'Hace falta un botón que diga
guardar avance cuando se está revisando el checklist'. Hoy cada cambio se
guarda solo al marcar/desmarcar (save local + cloudUpsertPrep), sin
confirmación visible. Lo pedido es un botón explícito en la tarjeta del
equipo MIENTRAS se revisa su checklist (en preparación y listo) que guarde
el avance en ese momento y lo confirme visiblemente.

Interpretaciones / decisiones documentadas:
- El botón es guardado EXPLÍCITO + confirmación ENCIMA del guardado
  automático actual, que NO cambia (sigue guardando en cada cambio de
  casilla / N/A / quitar punto). No duplica el equipo ni cambia su estado.
- Ubicación: en la tarjeta, junto a las demás acciones, justo antes de
  'Compartir avance' (primero de las acciones de avance). Solo cuando
  st === 'preparacion' o 'listo' (sin condición de pct: a 100% en listo
  también hay avance que guardar antes de entregar).
- Solo en equipos PROPIOS (rama editable) y para el admin en cualquiera:
  la rama !editable (ajeno, solo lectura) no lo muestra ni como
  deshabilitado; en entregados/bloqueados no aparece (st !== entregado).
- Borradores: SÍ aparece. El borrador también tiene checklist que se
  revisa (checks detectados + marcados a mano) y se guarda igual con
  save()/cloudUpsertPrep; 'Completar datos' no guarda los checks, así
  que el botón cubre ese hueco. No quita la marca de borrador.
- Al pulsar: cloudUpsertPrep(prep) + save() (si no hay sesión/nube,
  cloudUpsertPrep no hace nada y guarda local igual), y confirmación
  visible EN EL PROPIO BOTÓN: '✓ Avance guardado', deshabilitado ~2 s
  (evita doble toque), sin alert (que interrumpe). No re-renderiza de
  inmediato para que la confirmación se vea; a los 2 s restaura el texto
  y re-renderiza. El handler revisa canEditPrep como defensa en
  profundidad (la tarjeta ya lo oculta en ajenos).
- Cableado (lección de la 2.2.1: un botón sin su atributo en la cadena
  nunca dispara): 'data-guardar-avance' añadido a la cadena q(...) de
  resolución de prepId en el handler de #list, y rama de manejo junto a
  data-share-avance.
- EDIT_ATTRS: SÍ se añade 'data-guardar-avance'. La lista no es solo de
  edición de puntos (ya incluye data-share-avance, data-mail-avance,
  data-pdf...): es la lista de acciones bloqueadas en equipos ajenos por
  la guarda defensiva. Guardar avance escribe en la nube (upsert), así
  que una llamada directa al handler sobre un equipo ajeno debe
  bloquearse con el aviso de solo lectura, no guardarse en silencio.
- firebase.js SIN cambios -> NO se reconstruye el bundle (queda en
  496,903 bytes, md5 dabab404a2c6f4065639dc6f808d1bb3).
- No hay www/cloud/detect.js en el proyecto (el detector vive en el
  programa de escritorio): no hay backup detect-2.3.8.js.bak que hacer.
- Versión 2.3.8 -> 2.3.9 (25 ocurrencias en index.html, reemplazo global
  como en la 2.3.8: incluye los comentarios históricos '(2.3.8)', que
  pasan a '(2.3.9)' por convención del proyecto); versionCode 51 -> 52;
  iOS MARKETING_VERSION y CURRENT_PROJECT_VERSION en sus dos lugares.
- tests: copia test20238.js a test20239.js, actualiza versión y extraído,
  añade serie AY, extrae tests/checklist20239.js.
Cada reemplazo con assert: si el texto viejo no está, se para.
"""
import os
import shutil

CLOUD = '/home/hatch/workspace/android/checklist-cloud/'
HTML = CLOUD + 'www/index.html'
FB = CLOUD + 'www/cloud/firebase.js'
GRADLE = CLOUD + 'android/app/build.gradle'
PBX = CLOUD + 'ios/App/App.xcodeproj/project.pbxproj'
TEST_OLD = CLOUD + 'tests/test20238.js'
TEST_NEW = CLOUD + 'tests/test20239.js'
EXTRACT = CLOUD + 'tests/checklist20239.js'
BAK_HTML = CLOUD + 'tests/checklist-2.3.8b.html.bak'
BAK_FB = CLOUD + 'tests/firebase-2.3.8.js.bak'


def rep(path, old, new, count=1):
    with open(path, encoding='utf-8') as f:
        s = f.read()
    assert old in s, 'NO ENCONTRADO en %s: %r' % (path, old[:90])
    assert s.count(old) == count, 'OCURRENCIAS=%d (esperadas %d) en %s: %r' % (s.count(old), count, path, old[:90])
    with open(path, 'w', encoding='utf-8') as f:
        f.write(s.replace(old, new, count) if count == 1 else s.replace(old, new))
    print('OK:', path.split('/')[-1], '->', new[:70].replace('\n', ' '))


# ---------- 0. Backups (sin sobrescribir el .bak de 2.3.8 que ya existe) ----------
assert not os.path.exists(BAK_HTML), 'Ya existe %s' % BAK_HTML
shutil.copyfile(HTML, BAK_HTML)
print('OK: backup tests/checklist-2.3.8b.html.bak')
if not os.path.exists(BAK_FB):
    shutil.copyfile(FB, BAK_FB)
    print('OK: backup tests/firebase-2.3.8.js.bak')
else:
    print('OK: backup firebase-2.3.8.js.bak ya existía, no se sobrescribe')

# ---------- 0b. Copia del test ----------
shutil.copyfile(TEST_OLD, TEST_NEW)
print('OK: test20238.js copiado a test20239.js')

# ---------- 1. www/index.html: versión 2.3.8 -> 2.3.9 (25 ocurrencias) ----------
with open(HTML, encoding='utf-8') as f:
    html = f.read()
assert html.count('2.3.8') == 25, 'OCURRENCIAS 2.3.8=%d (esperadas 25)' % html.count('2.3.8')
assert '2.3.9' not in html, 'Ya hay 2.3.9 en index.html'
with open(HTML, 'w', encoding='utf-8') as f:
    f.write(html.replace('2.3.8', '2.3.9'))
print('OK: index.html versión 2.3.9 (25 ocurrencias)')

# ---------- 2. android/app/build.gradle ----------
rep(GRADLE, '        versionCode 51\n', '        versionCode 52\n')
rep(GRADLE, '        versionName "2.3.8"\n', '        versionName "2.3.9"\n')

# ---------- 3. iOS project.pbxproj ----------
rep(PBX, 'MARKETING_VERSION = 2.3.8;', 'MARKETING_VERSION = 2.3.9;', count=2)
rep(PBX, 'CURRENT_PROJECT_VERSION = 51;', 'CURRENT_PROJECT_VERSION = 52;', count=2)

# ---------- 4. Botón 'Guardar avance' en cardHtml (antes de Compartir avance) ----------
rep(HTML,
    "    if ((st === 'preparacion' || st === 'listo') && pct < 100) {\n"
    "      actions += '<button class=\"btn-ghost\" data-share-avance=\"' + p.id + '\">📤 Compartir avance</button>';",
    "    // Guardar avance (2.3.9): guardado explícito del checklist mientras se\n"
    "    // revisa (en preparación o listo, propio o admin; nunca ajeno — la rama\n"
    "    // !editable no lo muestra — ni entregado). El guardado automático por\n"
    "    // cambio sigue igual; este botón solo añade la confirmación visible.\n"
    "    // Borradores: sí aparece (su checklist también se revisa y se guarda).\n"
    "    if (st === 'preparacion' || st === 'listo') actions += '<button class=\"btn-ghost\" data-guardar-avance=\"' + p.id + '\">💾 Guardar avance</button>';\n"
    "    if ((st === 'preparacion' || st === 'listo') && pct < 100) {\n"
    "      actions += '<button class=\"btn-ghost\" data-share-avance=\"' + p.id + '\">📤 Compartir avance</button>';")

# ---------- 5. Cadena q(...) del handler de #list ----------
rep(HTML,
    "|| q('data-completar');",
    "|| q('data-completar') || q('data-guardar-avance');")

# ---------- 6. EDIT_ATTRS: guarda defensiva también para guardar-avance ----------
rep(HTML,
    "'data-completar'];",
    "'data-completar', 'data-guardar-avance'];")

# ---------- 7. Rama de manejo junto a data-share-avance ----------
rep(HTML,
    "  if (t.hasAttribute('data-share-avance') && prep) { shareWhatsApp([prep], avanceText(prep)); return; }",
    "  // Guardar avance (2.3.9): guardado explícito del checklist en revisión.\n"
    "  // Guarda local (save) + nube (cloudUpsertPrep, si hay sesión) SIN cambiar\n"
    "  // el estado ni duplicar el equipo, y confirma en el propio botón ('✓\n"
    "  // Avance guardado', deshabilitado ~2 s, sin alert). No re-renderiza de\n"
    "  // inmediato para que la confirmación se vea; a los 2 s restaura el botón\n"
    "  // y re-renderiza. Sin sesión/nube guarda local y confirma igual.\n"
    "  if (t.hasAttribute('data-guardar-avance') && prep) {\n"
    "    if (!canEditPrep(prep)) { alert('Este equipo es de otro analista: solo puedes compartirlo por WhatsApp o correo.'); return; }\n"
    "    cloudUpsertPrep(prep);\n"
    "    save();\n"
    "    t.textContent = '✓ Avance guardado';\n"
    "    t.disabled = true;\n"
    "    setTimeout(function () { t.textContent = '💾 Guardar avance'; t.disabled = false; render(); }, 2000);\n"
    "    return;\n"
    "  }\n"
    "  if (t.hasAttribute('data-share-avance') && prep) { shareWhatsApp([prep], avanceText(prep)); return; }")

# ---------- 8. Conteo final de 2.3.9 en el html (para AR0) ----------
with open(HTML, encoding='utf-8') as f:
    n239 = f.read().count('2.3.9')
print('OK: ocurrencias finales de 2.3.9 en index.html: %d' % n239)

# ---------- 9. test20239.js: extraído, versión y serie AY ----------
rep(TEST_NEW,
    "const SRC = fs.readFileSync(__dirname + '/checklist20238.js', 'utf8');",
    "const SRC = fs.readFileSync(__dirname + '/checklist20239.js', 'utf8');")
rep(TEST_NEW,
    "'AM0) versión 2.3.8:', html.includes('Versión 2.3.8'), '| sin 2.3.7:', !html.includes('Versión 2.3.7')",
    "'AM0) versión 2.3.9:', html.includes('Versión 2.3.9'), '| sin 2.3.8:', !html.includes('Versión 2.3.8')")
rep(TEST_NEW,
    "'AP0) estáticos 2.3.8: versión:', html.includes('Versión 2.3.8') && !html.includes('Versión 2.3.7')",
    "'AP0) estáticos 2.3.9: versión:', html.includes('Versión 2.3.9') && !html.includes('Versión 2.3.8')")
rep(TEST_NEW,
    "  var n238 = (html.match(/2\\.3\\.8/g) || []).length;",
    "  var n239 = (html.match(/2\\.3\\.9/g) || []).length;")
rep(TEST_NEW,
    "  console.log('AR0) versión 2.3.8 visible:', html.includes('Versión 2.3.8') && html.includes('Versión: 2.3.8'), '| 0 de 2.3.7:', !html.includes('2.3.7'), '| ocurrencias 2.3.8:', n238 === 25);",
    "  console.log('AR0) versión 2.3.9 visible:', html.includes('Versión 2.3.9') && html.includes('Versión: 2.3.9'), '| 0 de 2.3.8:', !html.includes('2.3.8'), '| ocurrencias 2.3.9:', n239 === %d);" % n239)

AY = r"""
  // AY: serie nueva 2.3.9 — botón '💾 Guardar avance' en la tarjeta del
  // equipo en revisión (preparación o listo, propio o admin). Guardado
  // explícito: save() local + cloudUpsertPrep, sin cambiar el estado ni
  // duplicar el equipo, con confirmación visible en el propio botón
  // ('✓ Avance guardado', deshabilitado ~2 s, sin alert). Nunca en
  // equipos ajenos ni en entregados; en borradores sí (su checklist
  // también se revisa). El guardado automático por cambio sigue igual.
  // Clic realista hecho a mano (sin fakeClick): el botón lleva data-prep
  // y su propio atributo; closest devuelve el botón solo para ese
  // selector y hasAttribute solo para ese atributo.
  function clickGuardar(prepId) {
    var btn = { textContent: '💾 Guardar avance', disabled: false,
      getAttribute: function (a) { return (a === 'data-guardar-avance' || a === 'data-prep') ? prepId : null; },
      hasAttribute: function (a) { return a === 'data-guardar-avance'; },
      closest: function (sel) { if (sel === '[data-guardar-avance]' || sel === '[data-prep]') return btn; return null; },
      classList: { contains: function () { return false; } } };
    document.getElementById('list')._h.click[0]({ target: btn });
    return btn;
  }
  // AY0: estáticos — botón en la tarjeta, atributo en la cadena q() del
  // handler de #list, rama de manejo, y en EDIT_ATTRS (guarda defensiva).
  var ay0btn = html.includes('data-guardar-avance="') && html.includes('💾 Guardar avance') && html.includes('✓ Avance guardado');
  var ay0chain = SRC.includes("q('data-guardar-avance')") && SRC.includes("t.hasAttribute('data-guardar-avance')");
  var ay0edit = SRC.includes("'data-completar', 'data-guardar-avance'");
  var ay0place = SRC.includes("if (st === 'preparacion' || st === 'listo') actions += '<button class=\"btn-ghost\" data-guardar-avance=\"'");
  console.log('AY0) botón en tarjeta + confirmación:', ay0btn, '| en cadena q() y rama del handler:', ay0chain, '| en EDIT_ATTRS:', ay0edit, '| solo preparación/listo:', ay0place);
  // AY1: visibilidad por estado y propiedad (cardHtml directo).
  loginAs('u1', 'Test User', 'usuario');
  CLOUD_ENABLED = true;
  adminViewUid = 'todos';
  var TAY = Date.now();
  var eqAY = function (modelo) { return { tipo: 'Laptop', marca: 'Dell', modelo: modelo, serie: 'S-' + modelo, inventario: '1' }; };
  var pAYown = mkPrepAU({ id: 'ay-own', createdAt: TAY - 300000, equipo: eqAY('ModeloPropioAY') });
  var pAYlisto = mkPrepAU({ id: 'ay-listo', createdAt: TAY - 200000, readyAt: TAY - 100000, equipo: eqAY('ModeloListoAY') });
  var pAYentr = mkPrepAU({ id: 'ay-entr', createdAt: TAY - 400000, readyAt: TAY - 200000, deliveredAt: TAY - 86400000, equipo: eqAY('ModeloEntregadoAY') });
  var pAYfor = mkPrepAU({ id: 'ay-for', createdAt: TAY - 100000, tecnicoUid: 'uAxel', tecnico: 'Axel Danyael', equipo: eqAY('ModeloAjenoAY') });
  var pAYbor = mkPrepAU({ id: 'ay-bor', createdAt: TAY - 50000, borrador: true, equipo: eqAY('ModeloBorradorAY') });
  var ay1prep = cardHtml(pAYown).indexOf('data-guardar-avance="ay-own"') !== -1;
  var ay1listo = cardHtml(pAYlisto).indexOf('data-guardar-avance="ay-listo"') !== -1;
  var ay1entr = cardHtml(pAYentr).indexOf('data-guardar-avance') === -1;
  var ay1for = cardHtml(pAYfor).indexOf('data-guardar-avance') === -1;
  var ay1bor = cardHtml(pAYbor).indexOf('data-guardar-avance="ay-bor"') !== -1;
  loginAs('uGer', 'Gerardo', 'admin');
  var ay1admin = cardHtml(pAYfor).indexOf('data-guardar-avance="ay-for"') !== -1;
  console.log('AY1) propio en preparación:', ay1prep, '| propio listo:', ay1listo, '| entregado no:', ay1entr, '| ajeno no:', ay1for, '| borrador sí:', ay1bor, '| admin en ajeno sí:', ay1admin);
  // AY1b: en la lista renderizada (con ajenos visibles) el botón está solo
  // en la tarjeta propia, nunca en la ajena ni en la entregada.
  loginAs('u1', 'Test User', 'usuario');
  showOthers = true;
  state.preparations = [pAYown, pAYfor, pAYentr];
  filterStatus = 'todos'; searchText = ''; todosPage = 0;
  render();
  var listAY1 = document.getElementById('list').innerHTML;
  var ay1b = listAY1.indexOf('data-guardar-avance="ay-own"') !== -1 && listAY1.indexOf('data-guardar-avance="ay-for"') === -1 && listAY1.indexOf('data-guardar-avance="ay-entr"') === -1;
  console.log('AY1b) lista renderizada: botón solo en propio:', ay1b);
  // AY2: al pulsar guarda local + nube, sin duplicar ni cambiar el estado,
  // y confirma en el propio botón (texto + deshabilitado).
  var upAY = [];
  global.Cloud.upsertPrep = async function (d) { upAY.push(d); };
  var pAY2 = mkPrepAU({ id: 'ay2', createdAt: TAY - 300000, checks: { t18: true }, equipo: eqAY('ModeloAY2') });
  state.preparations = [pAY2];
  filterStatus = 'todos'; searchText = ''; todosPage = 0; showOthers = false;
  render();
  global.localStorage.removeItem('checklist-soporte-v1');
  var nAY2 = state.preparations.length;
  var btnAY2 = clickGuardar('ay2');
  var savedAY2 = JSON.parse(global.localStorage.getItem('checklist-soporte-v1') || '{}');
  var lsAY2 = savedAY2.preparations && savedAY2.preparations.length === 1 && savedAY2.preparations[0].id === 'ay2' && savedAY2.preparations[0].checks && savedAY2.preparations[0].checks.t18 === true;
  var upAY2 = upAY.length === 1 && upAY[0].id === 'ay2';
  var nodupAY2 = state.preparations.length === nAY2 && state.preparations.filter(function (p) { return p.id === 'ay2'; }).length === 1;
  var stAY2 = statusOf(pAY2) === 'preparacion' && !pAY2.deliveredAt && !pAY2.readyAt;
  var confAY2 = btnAY2.textContent === '✓ Avance guardado' && btnAY2.disabled === true;
  console.log('AY2) guardado local con sus checks:', lsAY2, '| nube con el equipo:', upAY2, '| sin duplicar:', nodupAY2, '| estado sin cambio:', stAY2, '| confirmación visible y deshabilitado:', confAY2);
  // AY2b: a los 2 s el botón vuelve a su texto y se habilita.
  await sleep(2100);
  var restAY2 = btnAY2.textContent === '💾 Guardar avance' && btnAY2.disabled === false;
  console.log('AY2b) a los 2 s el botón vuelve a su texto y se habilita:', restAY2);
  // AY3: el guardado automático por cambio sigue funcionando (marcar una
  // casilla guarda local + nube y la tarjeta re-renderizada sigue con el
  // botón 'Guardar avance').
  upAY.length = 0;
  global.localStorage.removeItem('checklist-soporte-v1');
  var reqAY = requiredItems(pAY2);
  var chkAY = reqAY[0].id;
  document.getElementById('list')._h.change[0]({ target: { hasAttribute: function (a) { return a === 'data-check'; }, getAttribute: function (a) { return a === 'data-check' ? chkAY : 'ay2'; }, checked: true, classList: { contains: function () { return false; } } } });
  var savedAY3 = JSON.parse(global.localStorage.getItem('checklist-soporte-v1') || '{}');
  var lsAY3 = savedAY3.preparations && savedAY3.preparations[0].checks && savedAY3.preparations[0].checks[chkAY] === true;
  var upAY3 = upAY.length === 1 && upAY[0].id === 'ay2';
  var btnAY3 = document.getElementById('list').innerHTML.indexOf('data-guardar-avance="ay2"') !== -1;
  console.log('AY3) cambio guarda local:', lsAY3, '| cambio sube a nube:', upAY3, '| tarjeta re-renderizada con el botón:', btnAY3);
  // AY4: en un borrador propio el botón guarda el avance (checks
  // detectados incluidos) sin quitar la marca de borrador ni duplicar, y
  // convive con 'Completar datos'.
  var pAY4 = mkPrepAU({ id: 'ay4', createdAt: TAY - 200000, borrador: true, checks: { t18: true }, equipo: eqAY('ModeloAY4') });
  state.preparations = [pAY4];
  filterStatus = 'todos'; searchText = '';
  render();
  var cardAY4 = cardHtml(pAY4);
  var ay4btn = cardAY4.indexOf('data-guardar-avance="ay4"') !== -1 && cardAY4.indexOf('data-completar="ay4"') !== -1;
  upAY.length = 0;
  global.localStorage.removeItem('checklist-soporte-v1');
  var btnAY4 = clickGuardar('ay4');
  var savedAY4 = JSON.parse(global.localStorage.getItem('checklist-soporte-v1') || '{}');
  var lsAY4 = savedAY4.preparations && savedAY4.preparations.length === 1 && savedAY4.preparations[0].borrador === true && savedAY4.preparations[0].checks.t18 === true;
  var upAY4 = upAY.length === 1 && upAY[0].id === 'ay4';
  var confAY4 = btnAY4.textContent === '✓ Avance guardado' && btnAY4.disabled === true;
  console.log('AY4) borrador con botón y Completar datos:', ay4btn, '| guarda local sin quitar borrador:', lsAY4, '| nube:', upAY4, '| confirmación:', confAY4);
  // AY5: el admin puede guardar el avance de un equipo ajeno (canEditPrep).
  loginAs('uGer', 'Gerardo', 'admin');
  adminViewUid = 'todos';
  state.preparations = [pAYfor];
  filterStatus = 'todos'; searchText = '';
  render();
  upAY.length = 0;
  global.localStorage.removeItem('checklist-soporte-v1');
  var btnAY5 = clickGuardar('ay-for');
  var savedAY5 = JSON.parse(global.localStorage.getItem('checklist-soporte-v1') || '{}');
  var lsAY5 = savedAY5.preparations && savedAY5.preparations.length === 1 && savedAY5.preparations[0].id === 'ay-for';
  var upAY5 = upAY.length === 1 && upAY[0].id === 'ay-for';
  var confAY5 = btnAY5.textContent === '✓ Avance guardado' && btnAY5.disabled === true;
  console.log('AY5) admin guarda avance de ajeno: local:', lsAY5, '| nube:', upAY5, '| confirmación:', confAY5);
  // AY6: un usuario normal NO puede guardar el avance de un equipo ajeno
  // ni llamando directo al handler: la guarda defensiva (EDIT_ATTRS) lo
  // bloquea con el aviso de solo lectura, sin guardar nada.
  loginAs('u1', 'Test User', 'usuario');
  adminViewUid = 'todos';
  state.preparations = [pAYfor];
  filterStatus = 'todos'; searchText = ''; showOthers = true;
  render();
  upAY.length = 0;
  global.localStorage.removeItem('checklist-soporte-v1');
  global.lastAlert = null;
  var btnAY6 = clickGuardar('ay-for');
  var noSaveAY6 = global.localStorage.getItem('checklist-soporte-v1') === null;
  var noUpAY6 = upAY.length === 0;
  var alertAY6 = (global.lastAlert || '').indexOf('otro analista') !== -1;
  var btnAY6ok = btnAY6.textContent === '💾 Guardar avance' && btnAY6.disabled === false;
  console.log('AY6) ajeno bloqueado: sin guardado local:', noSaveAY6, '| sin subida a nube:', noUpAY6, '| aviso de solo lectura:', alertAY6, '| botón sin tocar:', btnAY6ok);
"""
with open(TEST_NEW, encoding='utf-8') as f:
    t = f.read()
anchor = '  process.exit(0);'
assert t.count(anchor) == 1, 'Ancla process.exit no única'
t = t.replace(anchor, AY + anchor, 1)
with open(TEST_NEW, 'w', encoding='utf-8') as f:
    f.write(t)
print('OK: serie AY añadida a test20239.js')

# ---------- 10. Extraer tests/checklist20239.js del index.html nuevo ----------
with open(HTML, encoding='utf-8') as f:
    lines = f.read().split('\n')
start = next(i for i, ln in enumerate(lines) if ln == '<script>')
end = next(i for i, ln in enumerate(lines) if ln == '</script>')
assert end > start, 'No se encontró el script inline'
with open(EXTRACT, 'w', encoding='utf-8') as f:
    f.write('\n' + '\n'.join(lines[start + 1:end]) + '\n')
print('OK: extraído tests/checklist20239.js (script inline, líneas %d-%d)' % (start + 2, end))

print('Parche 239 aplicado (firebase.js sin cambios: bundle NO reconstruido; versión 2.3.9/52).')
