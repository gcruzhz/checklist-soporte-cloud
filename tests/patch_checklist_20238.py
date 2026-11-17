#!/usr/bin/env python3
"""Parche 2.3.8 (teléfono): Listo con pendientes.

Petición de Gerardo (2026-11-15 ~07:21): 'cuando agregue un nuevo equipo
al presionar el botón listo si faltan campos no aparezca listo para
entregar, que diga equipo con pendientes'.

Interpretaciones documentadas (para que Gerardo las corrija):
- 'faltan campos' = puntos del checklist sin marcar (avance < 100%), NO
  los datos del formulario. Un equipo nuevo sin puntos marcados también
  cae aquí (avance 0% < 100%).
- Al pulsar Listo con avance < 100% el flujo NO cambia: se pone readyAt
  y se cambia a la pestaña Listos (como antes). Lo que cambia es la
  PRESENTACIÓN: la tarjeta muestra '⚠️ Equipo con pendientes — faltan N
  puntos' (N = puntos requeridos pendientes en ese momento, mismo estilo
  visible que el marcador 'No listo' de la 2.3.6) y su etiqueta de estado
  dice 'Equipo con pendientes' en lugar de 'Listo para entregar'.
- El botón de entrega en ese equipo dice 'Entregar' (no 'Entregado') y al
  pulsarlo sigue apareciendo el panel de confirmación de la 2.3.6
  ('Este equipo no está al 100%... Reabrir para completar / Entregar
  así'). Sin cambios en ese panel ni en sus handlers.
- El letrero es DERIVADO (readyAt + avance < 100%), no un campo nuevo:
  se actualiza solo al marcar/quitar puntos, poner N/A o quitar puntos
  (cada render lo recalcula). Al completar el último punto el letrero se
  quita y la etiqueta vuelve a ser literalmente 'Listo para entregar'
  con su botón 'Entregado' normal. Al desmarcar vuelve a aparecer.
  Aclaración de Gerardo (2026-11-15 ~07:24): al 100% SÍ debe decir
  'listo para entregar' — la etiqueta al 100% ya era 'Listo para
  entregar' vía statusLabel('listo'), así que no hubo que cambiarla;
  la serie AV verifica el texto literal.
- Aplica a CUALQUIER equipo marcado Listo con avance < 100%, no solo a
  los recién agregados. Vale en la tarjeta, en Todos y en la pestaña
  Nuevo (todas usan cardHtml, así que el letrero sale gratis ahí).
- Convivencia con 'No listo' (2.3.6): un solo letrero. Si el equipo está
  Listo con pendientes manda ese letrero; el de 'No listo' solo se ve en
  preparación. En la práctica no coexisten (Listo borra noListo y 'No
  listo' limpia readyAt); la supresión es defensa por si un documento
  sincronizado trae ambos campos.
- 'Quitar listo' sigue igual (vuelve a preparación, sin letrero).
- Listo al 100% y entrega al 100% sin cambios. Guardas de equipos ajenos
  de la 2.3.7 sin cambios: un equipo ajeno listo-con-pendientes se ve
  solo lectura con su letrero, sin botones de edición.
- NO cambia statusLabel() global: WhatsApp, correo, PDF y Excel siguen
  diciendo 'Listo para entregar' para un equipo listo (el cambio es solo
  la presentación de la tarjeta). Los contadores de la parte superior
  (cListo) siguen contando el equipo como listo: sigue en la pestaña
  Listos, solo que marcado con pendientes.
- www/cloud/firebase.js: SIN cambios -> NO se reconstruye el bundle
  (queda en 496,903 bytes, md5 dabab404a2c6f4065639dc6f808d1bb3).
- No hay www/cloud/detect.js en el proyecto (el detector vive en el
  programa de escritorio): no hay backup detect-2.3.7.js.bak que hacer.
- android/app/build.gradle: versionCode 50 -> 51, versionName 2.3.8.
- ios project.pbxproj: MARKETING_VERSION 2.3.8 (x2), CURRENT_PROJECT_VERSION 51 (x2).
- tests: copia test20237.js a test20238.js, actualiza versión y extraído,
  añade serie AV, extrae tests/checklist20238.js.
Cada reemplazo con assert: si el texto viejo no está, se para.
"""
import shutil

CLOUD = '/home/hatch/workspace/android/checklist-cloud/'
HTML = CLOUD + 'www/index.html'
FB = CLOUD + 'www/cloud/firebase.js'
GRADLE = CLOUD + 'android/app/build.gradle'
PBX = CLOUD + 'ios/App/App.xcodeproj/project.pbxproj'
TEST_OLD = CLOUD + 'tests/test20237.js'
TEST_NEW = CLOUD + 'tests/test20238.js'
EXTRACT = CLOUD + 'tests/checklist20238.js'


def rep(path, old, new, count=1):
    with open(path, encoding='utf-8') as f:
        s = f.read()
    assert old in s, 'NO ENCONTRADO en %s: %r' % (path, old[:90])
    assert s.count(old) == count, 'OCURRENCIAS=%d (esperadas %d) en %s: %r' % (s.count(old), count, path, old[:90])
    with open(path, 'w', encoding='utf-8') as f:
        f.write(s.replace(old, new, count) if count == 1 else s.replace(old, new))
    print('OK:', path.split('/')[-1], '->', new[:70].replace('\n', ' '))


# ---------- 0. Backups 2.3.7 (detect.js no existe en el proyecto) ----------
shutil.copyfile(HTML, CLOUD + 'tests/checklist-2.3.7.html.bak')
shutil.copyfile(FB, CLOUD + 'tests/firebase-2.3.7.js.bak')
print('OK: backups tests/checklist-2.3.7.html.bak y tests/firebase-2.3.7.js.bak (sin detect.js: no existe)')

# ---------- 0b. Copia del test ----------
shutil.copyfile(TEST_OLD, TEST_NEW)
print('OK: test20237.js copiado a test20238.js')

# ---------- 1. www/index.html: versión 2.3.7 -> 2.3.8 (22 ocurrencias) ----------
with open(HTML, encoding='utf-8') as f:
    html = f.read()
assert html.count('2.3.7') == 22, 'OCURRENCIAS 2.3.7=%d (esperadas 22)' % html.count('2.3.7')
assert '2.3.8' not in html, 'Ya hay 2.3.8 en index.html'
with open(HTML, 'w', encoding='utf-8') as f:
    f.write(html.replace('2.3.7', '2.3.8'))
print('OK: index.html versión 2.3.8 (22 ocurrencias)')

# ---------- 2. android/app/build.gradle ----------
rep(GRADLE, '        versionCode 50\n', '        versionCode 51\n')
rep(GRADLE, '        versionName "2.3.7"\n', '        versionName "2.3.8"\n')

# ---------- 3. iOS project.pbxproj ----------
rep(PBX, 'MARKETING_VERSION = 2.3.7;', 'MARKETING_VERSION = 2.3.8;', count=2)
rep(PBX, 'CURRENT_PROJECT_VERSION = 50;', 'CURRENT_PROJECT_VERSION = 51;', count=2)

# ---------- 4. cardHtml: estado derivado 'Listo con pendientes' ----------
rep(HTML,
    'function cardHtml(p) {\n'
    '  var st = statusOf(p);\n'
    '  var pct = progress(p);\n',
    'function cardHtml(p) {\n'
    '  var st = statusOf(p);\n'
    '  var pct = progress(p);\n'
    '  // Listo con pendientes (2.3.8): marcado Listo con avance <100% — la\n'
    '  // tarjeta NO se presenta como lista para entregar: letrero prominente\n'
    '  // y etiqueta \'Equipo con pendientes\'. Derivado de readyAt + avance,\n'
    '  // así que se actualiza solo al marcar/quitar puntos (cada render lo\n'
    '  // recalcula). Al llegar al 100% vuelve a \'Listo para entregar\' con su\n'
    '  // botón \'Entregado\' normal.\n'
    '  var conPendientes = st === \'listo\' && p.readyAt && pct < 100;\n'
    '  var pendientesN = conPendientes ? pendingRequired(p).length : 0;\n'
    '  var stateLabel = conPendientes ? \'Equipo con pendientes\' : statusLabel(st);\n')

# ---------- 5. cardHtml: botón de entrega dice 'Entregar' con pendientes ----------
rep(HTML,
    "    if (st === 'listo') actions += '<button class=\"btn-green\" data-deliver=\"' + p.id + '\">Entregado</button>';\n",
    "    // Entrega (2.3.8): con pendientes el botón dice 'Entregar', no\n"
    "    // 'Entregado': no debe leerse como si estuviera al 100%. El handler\n"
    "    // data-deliver ya muestra el panel de confirmación a <100%.\n"
    "    if (st === 'listo') actions += '<button class=\"btn-green\" data-deliver=\"' + p.id + '\">' + (pct < 100 ? 'Entregar' : 'Entregado') + '</button>';\n")

# ---------- 6. cardHtml: letrero de pendientes; 'No listo' no se duplica ----------
rep(HTML,
    "  var noListoLine = p.noListo ? '<div class=\"sub\">⚠️ No listo — faltan ' + (p.noListo.faltan || 0) + ' puntos</div>' : '';\n",
    "  // Listo con pendientes (2.3.8): letrero prominente, mismo estilo visible\n"
    "  // que el marcador 'No listo' de la 2.3.6. Si el equipo ya tiene el\n"
    "  // marcador 'No listo', no se duplica: manda el letrero de pendientes\n"
    "  // (el de 'No listo' solo se ve en preparación). En la práctica no\n"
    "  // coexisten (Listo borra noListo y 'No listo' limpia readyAt).\n"
    "  var pendientesLine = conPendientes ? '<div class=\"sub\">⚠️ Equipo con pendientes — faltan ' + pendientesN + ' puntos</div>' : '';\n"
    "  var noListoLine = (!conPendientes && p.noListo) ? '<div class=\"sub\">⚠️ No listo — faltan ' + (p.noListo.faltan || 0) + ' puntos</div>' : '';\n")

# ---------- 7. cardHtml: etiqueta de estado y letrero en la tarjeta ----------
rep(HTML,
    "    '<span class=\"badge ' + statusClass(st) + '\">' + statusLabel(st) + '</span>' +\n",
    "    '<span class=\"badge ' + statusClass(st) + '\">' + stateLabel + '</span>' +\n")
rep(HTML,
    "    '<div class=\"pct\">' + pct + '% completado</div>' + deliveredLine + noListoLine + reassignLine + asignLine + detNote +\n",
    "    '<div class=\"pct\">' + pct + '% completado</div>' + deliveredLine + noListoLine + pendientesLine + reassignLine + asignLine + detNote +\n")

# ---------- 8. Contar ocurrencias 2.3.8 para la aserción AR0 ----------
with open(HTML, encoding='utf-8') as f:
    n238 = f.read().count('2.3.8')
assert n238 == 25, 'OCURRENCIAS 2.3.8=%d (esperadas 25: 22 de versión + 3 comentarios nuevos)' % n238
assert '2.3.7' not in open(HTML, encoding='utf-8').read(), 'Queda 2.3.7 en index.html'
print('OK: index.html trae 2.3.8 x%d y 0 de 2.3.7' % n238)

# ---------- 9. test20238.js: extraído y versiones ----------
rep(TEST_NEW,
    "const SRC = fs.readFileSync(__dirname + '/checklist20237.js', 'utf8');",
    "const SRC = fs.readFileSync(__dirname + '/checklist20238.js', 'utf8');")
rep(TEST_NEW,
    "console.log('AM0) versión 2.3.7:', html.includes('Versión 2.3.7'), '| sin 2.3.6:', !html.includes('Versión 2.3.6'),",
    "console.log('AM0) versión 2.3.8:', html.includes('Versión 2.3.8'), '| sin 2.3.7:', !html.includes('Versión 2.3.7'),")
rep(TEST_NEW,
    "console.log('AP0) estáticos 2.3.7: versión:', html.includes('Versión 2.3.7') && !html.includes('Versión 2.3.6'),",
    "console.log('AP0) estáticos 2.3.8: versión:', html.includes('Versión 2.3.8') && !html.includes('Versión 2.3.7'),")
rep(TEST_NEW,
    "  var n237 = (html.match(/2\\.3\\.7/g) || []).length;\n"
    "  console.log('AR0) versión 2.3.7 visible:', html.includes('Versión 2.3.7') && html.includes('Versión: 2.3.7'), '| 0 de 2.3.6:', !html.includes('2.3.6'), '| ocurrencias 2.3.7:', n237 === 22);",
    "  var n238 = (html.match(/2\\.3\\.8/g) || []).length;\n"
    "  console.log('AR0) versión 2.3.8 visible:', html.includes('Versión 2.3.8') && html.includes('Versión: 2.3.8'), '| 0 de 2.3.7:', !html.includes('2.3.7'), '| ocurrencias 2.3.8:', n238 === %d);" % n238)

# ---------- 10. Serie AV ----------
AV = """
  // AV: serie nueva 2.3.8 — Listo con pendientes: al pulsar Listo con
  // avance <100% la tarjeta dice 'Equipo con pendientes — faltan N
  // puntos' (no 'Listo para entregar'); al llegar al 100% el letrero se
  // quita y la etiqueta es literalmente 'Listo para entregar' con su
  // botón 'Entregado' normal. realClick reutilizado (serie AT).
  loginAs('u1', 'Test User', 'usuario');
  CLOUD_ENABLED = true;
  adminViewUid = 'todos';
  var upAV = [];
  global.Cloud.upsertPrep = async function (d) { upAV.push(d); };
  var reqAV = requiredItems(mkPrep({}));
  var nReqAV = reqAV.length;
  var checksAlmostAV = {};
  reqAV.slice(0, nReqAV - 1).forEach(function (it) { checksAlmostAV[it.id] = true; });
  var lastIdAV = reqAV[nReqAV - 1].id;
  var checksFullAV = {};
  reqAV.forEach(function (it) { checksFullAV[it.id] = true; });
  function changeCheckAV(prepId, itemId, checked) {
    document.getElementById('list')._h.change[0]({ target: { hasAttribute: function (a) { return a === 'data-check'; }, getAttribute: function (a) { return a === 'data-check' ? itemId : a === 'data-prep' ? prepId : null; }, checked: checked } });
  }
  // AV0: estáticos — letrero, derivado y botón en el código.
  var av0 = SRC.includes('Equipo con pendientes') && SRC.includes('conPendientes') && SRC.includes("pct < 100 ? 'Entregar' : 'Entregado'");
  console.log('AV0) letrero y botón en el código:', av0);
  // AV1: Listo a <100% muestra 'Equipo con pendientes' con el conteo y NO
  // estado 'Listo' ni botón de entrega como si fuera 100%.
  var pAV1 = mkPrepAU({ id: 'av1', checks: Object.assign({}, checksAlmostAV) });
  state.preparations = [pAV1];
  filterStatus = 'preparacion'; searchText = ''; todosPage = 0;
  realClick('data-ready', 'av1');
  var cardAV1 = cardHtml(pAV1);
  var av1 = !!pAV1.readyAt && statusOf(pAV1) === 'listo' && filterStatus === 'listo' &&
    cardAV1.indexOf('⚠️ Equipo con pendientes — faltan 1 puntos') !== -1 &&
    cardAV1.indexOf('>Equipo con pendientes<') !== -1 &&
    cardAV1.indexOf('Listo para entregar') === -1 &&
    cardAV1.indexOf('data-deliver="av1">Entregar<') !== -1 &&
    cardAV1.indexOf('>Entregado<') === -1 &&
    cardAV1.indexOf('data-unready="av1"') !== -1;
  console.log('AV1) Listo a <100%: letrero con faltan 1, sin Listo para entregar ni Entregado:', av1);
  // AV2: Listo al 100% se ve normal: etiqueta literal 'Listo para
  // entregar' (no 'Listo' a secas ni 'Equipo con pendientes') y botón
  // 'Entregado' normal, sin letrero ni 'Quitar listo'.
  var pAV2 = mkPrepAU({ id: 'av2', checks: Object.assign({}, checksFullAV) });
  state.preparations = [pAV2];
  filterStatus = 'preparacion';
  realClick('data-ready', 'av2');
  var cardAV2 = cardHtml(pAV2);
  var av2 = !!pAV2.readyAt && statusOf(pAV2) === 'listo' && progress(pAV2) === 100 &&
    cardAV2.indexOf('>Listo para entregar<') !== -1 &&
    cardAV2.indexOf('>Listo<') === -1 &&
    cardAV2.indexOf('Equipo con pendientes') === -1 &&
    cardAV2.indexOf('data-deliver="av2">Entregado<') !== -1 &&
    cardAV2.indexOf('data-unready="av2"') === -1;
  console.log('AV2) Listo al 100%: etiqueta literal Listo para entregar + Entregado:', av2);
  // AV3: completar el último punto quita el letrero (queda Listo para
  // entregar + Entregado).
  state.preparations = [pAV1];
  changeCheckAV('av1', lastIdAV, true);
  var cardAV3 = cardHtml(pAV1);
  var av3 = progress(pAV1) === 100 && statusOf(pAV1) === 'listo' &&
    cardAV3.indexOf('Equipo con pendientes') === -1 &&
    cardAV3.indexOf('>Listo para entregar<') !== -1 &&
    cardAV3.indexOf('data-deliver="av1">Entregado<') !== -1;
  console.log('AV3) último punto marcado: letrero fuera, Listo para entregar:', av3);
  // AV4: desmarcar un punto trae el letrero de vuelta.
  changeCheckAV('av1', lastIdAV, false);
  var cardAV4 = cardHtml(pAV1);
  var av4 = progress(pAV1) < 100 && statusOf(pAV1) === 'listo' && !!pAV1.readyAt &&
    cardAV4.indexOf('⚠️ Equipo con pendientes — faltan 1 puntos') !== -1 &&
    cardAV4.indexOf('>Equipo con pendientes<') !== -1 &&
    cardAV4.indexOf('data-deliver="av1">Entregar<') !== -1;
  console.log('AV4) punto desmarcado: letrero de vuelta:', av4);
  // AV5: 'Quitar listo' sigue funcionando (vuelve a preparación, sin letrero).
  realClick('data-unready', 'av1');
  var cardAV5 = cardHtml(pAV1);
  var av5 = !pAV1.readyAt && statusOf(pAV1) === 'preparacion' && filterStatus === 'preparacion' &&
    cardAV5.indexOf('Equipo con pendientes') === -1 &&
    cardAV5.indexOf('data-ready="av1"') !== -1 &&
    cardAV5.indexOf('data-deliver="av1"') === -1;
  console.log('AV5) Quitar listo: vuelve a preparación:', av5);
  // AV6: al pulsar Entregar con pendientes sigue apareciendo el panel de
  // confirmación de la 2.3.6; 'Entregar así' entrega.
  realClick('data-ready', 'av1');
  realClick('data-deliver', 'av1');
  var cardAV6 = cardHtml(pAV1);
  var av6a = window._deliverConfirmFor === 'av1' && !pAV1.deliveredAt &&
    cardAV6.indexOf('Este equipo no está al 100%') !== -1 &&
    cardAV6.indexOf('data-deliver-reopen="av1"') !== -1 &&
    cardAV6.indexOf('data-deliver-confirm="av1"') !== -1 &&
    cardAV6.indexOf('Reabrir para completar') !== -1 &&
    cardAV6.indexOf('Entregar así') !== -1;
  realClick('data-deliver-confirm', 'av1');
  var av6b = !!pAV1.deliveredAt && window._deliverConfirmFor === null && filterStatus === 'entregado';
  console.log('AV6) panel de entrega a <100%:', av6a, '| Entregar así entrega:', av6b);
  // AV7: en Todos y en Nuevo el letrero se ve; un equipo ajeno
  // listo-con-pendientes se ve solo lectura con su letrero.
  var pAV7 = mkPrepAU({ id: 'av7', checks: Object.assign({}, checksAlmostAV), readyAt: Date.now() - 60000, equipo: { tipo: 'Laptop', marca: 'Dell', modelo: 'ModeloPendiente', serie: 'S-AV7', inventario: '1' } });
  var pAV7f = mkPrepAU({ id: 'av7f', tecnicoUid: 'uAxel', tecnico: 'Axel Danyael', checks: Object.assign({}, checksAlmostAV), readyAt: Date.now() - 60000, equipo: { tipo: 'Laptop', marca: 'HP', modelo: 'ModeloAjenoPend', serie: 'S-AV7F', inventario: '2' } });
  state.preparations = [pAV7, pAV7f];
  filterStatus = 'todos'; searchText = ''; todosPage = 0; window._expandedId = null;
  render();
  var listTodosAV7 = document.getElementById('list').innerHTML;
  var av7todos = (listTodosAV7.match(/⚠️ Equipo con pendientes — faltan 1 puntos/g) || []).length === 2 &&
    listTodosAV7.indexOf('ModeloPendiente') !== -1 && listTodosAV7.indexOf('ModeloAjenoPend') !== -1;
  filterStatus = 'nuevo';
  render();
  var listNuevoAV7 = document.getElementById('list').innerHTML;
  var av7nuevo = (listNuevoAV7.match(/⚠️ Equipo con pendientes — faltan 1 puntos/g) || []).length === 1 &&
    listNuevoAV7.indexOf('ModeloPendiente') !== -1 && listNuevoAV7.indexOf('ModeloAjenoPend') === -1;
  var cardAV7f = cardHtml(pAV7f);
  var av7f = cardAV7f.indexOf('⚠️ Equipo con pendientes — faltan 1 puntos') !== -1 &&
    ['data-ready', 'data-deliver', 'data-unready', 'data-nolisto', 'data-na', 'data-remove-item', 'data-add-extra', 'data-pdf', 'data-del-prep', 'data-asignar'].every(function (a) { return cardAV7f.indexOf(a + '="') === -1; }) &&
    cardAV7f.indexOf('data-wa="av7f"') !== -1 && cardAV7f.indexOf('data-solicitar-asignacion="av7f"') !== -1;
  console.log('AV7) Todos con letrero en los dos:', av7todos, '| Nuevo solo propio con letrero:', av7nuevo, '| ajeno solo lectura con letrero:', av7f);
"""
with open(TEST_NEW, encoding='utf-8') as f:
    t = f.read()
anchor = '  process.exit(0);'
assert t.count(anchor) == 1, 'Ancla process.exit no única'
t = t.replace(anchor, AV + anchor, 1)
with open(TEST_NEW, 'w', encoding='utf-8') as f:
    f.write(t)
print('OK: serie AV añadida a test20238.js')

# ---------- 11. Extraer tests/checklist20238.js del index.html nuevo ----------
with open(HTML, encoding='utf-8') as f:
    lines = f.read().split('\n')
start = next(i for i, ln in enumerate(lines) if ln == '<script>')
end = next(i for i, ln in enumerate(lines) if ln == '</script>')
assert end > start, 'No se encontró el script inline'
with open(EXTRACT, 'w', encoding='utf-8') as f:
    f.write('\n' + '\n'.join(lines[start + 1:end]) + '\n')
print('OK: extraído tests/checklist20238.js (script inline, líneas %d-%d)' % (start + 2, end))

print('Parche 2.3.8 aplicado (firebase.js sin cambios: bundle NO reconstruido).')
