#!/usr/bin/env python3
"""Parche 2.3.6 (teléfono): redes + fuente del SO, N/A y quitar por punto,
compartir avance + No listo, entrega con reapertura (<100% con panel).

Diseño confirmado (aclaración de Gerardo: hoy 'Entregado' entrega sin más,
como si estuviera al 100%, sin avisar ni dar opción):
- Al pulsar 'Entregado' con avance <100% NO se entrega: la tarjeta muestra
  un panel con el porcentaje y las casillas que faltan y dos botones:
  'Reabrir para completar' (no entrega, vuelve a preparación para marcar
  lo que falta) y 'Entregar así' (entrega consciente de que no está al 100%).
  Al 100% entrega directo como antes.
- 'Reabrir' de un equipo ya entregado limpia deliveredAt Y readyAt: vuelve
  a preparación para completar al 100% (antes solo limpiaba deliveredAt y
  quedaba en listo). CAMBIO INTENCIONAL frente a la serie P de 2.0.10, que
  mantenía readyAt: la única aserción que lo cubría en el harness actual
  es AA4 (Reabrir sube con deliveredAt null); se actualiza en test20236.js
  para exigir también readyAt null y status 'preparacion'. No existe
  ninguna línea de log 'P...' en test20235.js: la serie P no sobrevivió
  como tal al harness actual.
- AA4 también cambia por el panel: 'Entregado' con avance <100% ya no
  entrega directo, así que AA4 ahora comprueba panel + 'Entregar así'.

- www/cloud/firebase.js: SIN cambios -> NO se reconstruye el bundle.
- android/app/build.gradle: versionCode 48 -> 49, versionName 2.3.6.
- ios project.pbxproj: MARKETING_VERSION 2.3.6 (x2), CURRENT_PROJECT_VERSION 49 (x2).
- tests: copia test20235.js a test20236.js, actualiza versión y extraído,
  actualiza AA4, añade serie AT, extrae tests/checklist20236.js.
Cada reemplazo con assert: si el texto viejo no está, se para.
"""
import shutil

CLOUD = '/home/hatch/workspace/android/checklist-cloud/'
HTML = CLOUD + 'www/index.html'
FB = CLOUD + 'www/cloud/firebase.js'
GRADLE = CLOUD + 'android/app/build.gradle'
PBX = CLOUD + 'ios/App/App.xcodeproj/project.pbxproj'
TEST_OLD = CLOUD + 'tests/test20235.js'
TEST_NEW = CLOUD + 'tests/test20236.js'
EXTRACT = CLOUD + 'tests/checklist20236.js'


def rep(path, old, new, count=1):
    with open(path, encoding='utf-8') as f:
        s = f.read()
    assert old in s, 'NO ENCONTRADO en %s: %r' % (path, old[:90])
    assert s.count(old) == count, 'OCURRENCIAS=%d (esperadas %d) en %s: %r' % (s.count(old), count, path, old[:90])
    with open(path, 'w', encoding='utf-8') as f:
        f.write(s.replace(old, new, count) if count == 1 else s.replace(old, new))
    print('OK:', path.split('/')[-1], '->', new[:70].replace('\n', ' '))


# ---------- 0. Backups 2.3.5 ----------
shutil.copyfile(HTML, CLOUD + 'tests/checklist-2.3.5.html.bak')
shutil.copyfile(FB, CLOUD + 'tests/firebase-2.3.5.js.bak')
print('OK: backups tests/checklist-2.3.5.html.bak y tests/firebase-2.3.5.js.bak')

# ---------- 0b. Copia del test ----------
shutil.copyfile(TEST_OLD, TEST_NEW)
print('OK: test20235.js copiado a test20236.js')

# ---------- 1. www/index.html: versión 2.3.5 -> 2.3.6 (13 ocurrencias) ----------
with open(HTML, encoding='utf-8') as f:
    html = f.read()
assert html.count('2.3.5') == 13, 'OCURRENCIAS 2.3.5=%d (esperadas 13)' % html.count('2.3.5')
assert '2.3.6' not in html, 'Ya hay 2.3.6 en index.html'
with open(HTML, 'w', encoding='utf-8') as f:
    f.write(html.replace('2.3.5', '2.3.6'))
print('OK: index.html versión 2.3.6 (13 ocurrencias)')

# ---------- 2. android/app/build.gradle ----------
rep(GRADLE, '        versionCode 48\n', '        versionCode 49\n')
rep(GRADLE, '        versionName "2.3.5"\n', '        versionName "2.3.6"\n')

# ---------- 3. iOS project.pbxproj ----------
rep(PBX, 'MARKETING_VERSION = 2.3.5;', 'MARKETING_VERSION = 2.3.6;', count=2)
rep(PBX, 'CURRENT_PROJECT_VERSION = 48;', 'CURRENT_PROJECT_VERSION = 49;', count=2)

# ---------- 4. CSS: botón mini + badge N/A ----------
rep(HTML,
    '  .btn-danger { background: #fbe9e7; color: #b3261e; }\n',
    '  .btn-danger { background: #fbe9e7; color: #b3261e; }\n'
    '  .btn-mini { padding: 4px 8px; font-size: 12px; border-radius: 6px; }\n'
    '  .badge-na { background: #e3e8ef; color: #445; }\n')

# ---------- 5. Helpers: redes, fuente del SO, N/A / quitados, avance ----------
HELPERS = '''// Redes del equipo: el detector trae redes [{nombre, ip, ipTipo}] (ipTipo
// 'Estática'|'Dinámica' o ''); la ip/ipTipo sueltas del adaptador principal
// se siguen mostrando por hardwareLine. Sin redes (o sin ip en ninguna)
// no hay línea en ningún sitio.
function redesText(eq) {
  var list = (eq && eq.redes) || [];
  if (!Array.isArray(list)) return '';
  return list.filter(function (r) { return r && r.ip; }).map(function (r) {
    return (r.nombre ? r.nombre + ': ' : '') + r.ip + (r.ipTipo ? ' (' + r.ipTipo + ')' : '');
  }).join(' \\u00b7 ');
}
function redesLine(eq) {
  var t = redesText(eq);
  return t ? 'Redes: ' + t : '';
}
// Fuente del SO: el detector dice en detalles.osFuente de dónde sacó el
// nombre del sistema operativo ('registro' | 'cim' | 'computerinfo' | 'si').
function osFuenteLine(d) {
  var det = (d && d.detalles) || {};
  var v = det.osFuente;
  if (!v) return '';
  var names = { registro: 'Registro de Windows', cim: 'CIM (WMI)', computerinfo: 'Get-ComputerInfo', si: 'Información del sistema' };
  return 'SO detectado por: ' + (names[v] || v);
}
// Puntos N/A o quitados por equipo: naItems {id:true} no cuenta en el
// avance (ni numerador ni denominador) y no lo pide '¿Qué falta?';
// removedItems [id] oculta el punto de la tarjeta. Defaults {} / [] para
// equipos viejos que no traen estos campos (ver prepFromCloud).
function isNA(p, id) { return !!(p.naItems && p.naItems[id]); }
function isRemoved(p, id) { return (p.removedItems || []).indexOf(id) !== -1; }
function naText(p) {
  return allItems(p).filter(function (it) { return isNA(p, it.id); }).map(function (it) { return it.text; }).join('; ');
}
function pendingRequired(p) {
  return requiredItems(p).filter(function (it) { return !p.checks[it.id]; });
}
// El marcador 'No listo' se limpia solo al llegar al 100% (o al pulsar
// 'Listo' de nuevo, en su handler): al marcar/quitar un punto, al poner o
// quitar un N/A, o al elegir una opción, el avance puede llegar a 100%.
function clearNoListoIfDone(p) {
  if (p.noListo && progress(p) === 100) delete p.noListo;
}
'''
rep(HTML,
    "  if (!parts.length) return '';\n  return parts.join(' \\u00b7 ');\n}\n",
    "  if (!parts.length) return '';\n  return parts.join(' \\u00b7 ');\n}\n" + HELPERS)

# ---------- 6. requiredItems: N/A y quitados no cuentan ----------
rep(HTML,
    'function requiredItems(prep) {\n'
    "  return allItems(prep).filter(function (it) { return !it.optional; });\n"
    '}\n',
    'function requiredItems(prep) {\n'
    '  // N/A y quitados quedan fuera: progress(), faltaPrompt(), waTextOne()\n'
    "  // y avanceText() los heredan gratis al usar requiredItems().\n"
    "  return allItems(prep).filter(function (it) { return !it.optional && !isNA(prep, it.id) && !isRemoved(prep, it.id); });\n"
    '}\n')

# ---------- 7. prepToCloudDoc / prepFromCloud: redes, naItems, removedItems, noListo ----------
rep(HTML,
    '    checks: p.checks || {}, extraItems: p.extraItems || [], reasignaciones: p.reasignaciones || [],\n'
    '    autoDetectado: p.autoDetectado || [],\n',
    '    checks: p.checks || {}, extraItems: p.extraItems || [], reasignaciones: p.reasignaciones || [],\n'
    '    naItems: p.naItems || {}, removedItems: p.removedItems || [], noListo: p.noListo || null,\n'
    '    autoDetectado: p.autoDetectado || [],\n')
rep(HTML,
    "anydeskId: eq.anydeskId || '', anydeskAlias: eq.anydeskAlias || '', fotoSerie: foto },",
    "anydeskId: eq.anydeskId || '', anydeskAlias: eq.anydeskAlias || '', "
    "redes: Array.isArray(eq.redes) ? eq.redes.map(function (r) { return { nombre: r.nombre || '', ip: r.ip || '', ipTipo: r.ipTipo || '' }; }) : [], fotoSerie: foto },")
rep(HTML,
    '    checks: doc.checks || {}, extraItems: doc.extraItems || [], reasignaciones: doc.reasignaciones || [],\n'
    '    autoDetectado: doc.autoDetectado || [],\n',
    '    checks: doc.checks || {}, extraItems: doc.extraItems || [], reasignaciones: doc.reasignaciones || [],\n'
    '    naItems: doc.naItems || {}, removedItems: doc.removedItems || [], noListo: doc.noListo || null,\n'
    '    autoDetectado: doc.autoDetectado || [],\n')
rep(HTML,
    "anydeskId: eq.anydeskId || '', anydeskAlias: eq.anydeskAlias || '', fotoSerie: eq.fotoSerie || null },",
    "anydeskId: eq.anydeskId || '', anydeskAlias: eq.anydeskAlias || '', "
    "redes: Array.isArray(eq.redes) ? eq.redes.map(function (r) { return { nombre: r.nombre || '', ip: r.ip || '', ipTipo: r.ipTipo || '' }; }) : [], fotoSerie: eq.fotoSerie || null },")

# ---------- 8. PDF: redes + N/A / quitados ----------
rep(HTML,
    "  if (prep.equipo.anydeskId) row(anydeskLine(prep.equipo), 'F1', 11);\n",
    "  if (prep.equipo.anydeskId) row(anydeskLine(prep.equipo), 'F1', 11);\n"
    "  if (redesLine(prep.equipo)) row(redesLine(prep.equipo), 'F1', 11);\n")
rep(HTML,
    '    gi.forEach(function (it) {\n'
    "      var mark = prep.checks[it.id] ? '[x] ' : '[ ] ';\n",
    '    gi.forEach(function (it) {\n'
    '      if (isRemoved(prep, it.id)) return;\n'
    "      var mark = isNA(prep, it.id) ? '[N/A] ' : (prep.checks[it.id] ? '[x] ' : '[ ] ');\n")

# ---------- 9. Excel: columna 'Redes' tras AnyDesk + columna 'Puntos N/A' ----------
rep(HTML,
    "  var headers = ['Tipo', 'Marca', 'Modelo', 'No. de serie', 'No. de inventario', 'Hostname', 'CPU', 'RAM', 'Disco', 'IP', 'AnyDesk', 'Usuario', 'Área', 'Correo', 'Analista', 'Estado', 'Avance %', 'Creado', 'Entregado', 'Reasignaciones'];\n",
    "  var headers = ['Tipo', 'Marca', 'Modelo', 'No. de serie', 'No. de inventario', 'Hostname', 'CPU', 'RAM', 'Disco', 'IP', 'AnyDesk', 'Redes', 'Usuario', 'Área', 'Correo', 'Analista', 'Estado', 'Avance %', 'Puntos N/A', 'Creado', 'Entregado', 'Reasignaciones'];\n")
rep(HTML,
    "      (p.equipo.anydeskId ? anydeskDisplay(p.equipo.anydeskId) + (p.equipo.anydeskAlias ? ' (' + p.equipo.anydeskAlias + ')' : '') : ''),\n"
    "      p.usuario.nombre, p.usuario.area, p.usuario.correo, p.tecnico,\n"
    "      statusLabel(statusOf(p)), progress(p), fmtDate(p.createdAt), p.deliveredAt ? fmtDate(p.deliveredAt) : '', reassignText(p)];\n",
    "      (p.equipo.anydeskId ? anydeskDisplay(p.equipo.anydeskId) + (p.equipo.anydeskAlias ? ' (' + p.equipo.anydeskAlias + ')' : '') : ''),\n"
    "      redesText(p.equipo || {}),\n"
    "      p.usuario.nombre, p.usuario.area, p.usuario.correo, p.tecnico,\n"
    "      statusLabel(statusOf(p)), progress(p), naText(p), fmtDate(p.createdAt), p.deliveredAt ? fmtDate(p.deliveredAt) : '', reassignText(p)];\n")

# ---------- 10. WhatsApp individual y general: redes + N/A ----------
rep(HTML,
    '  var adOne = anydeskLine(p.equipo || {});\n'
    '  if (adOne) lines.push(adOne);\n',
    '  var adOne = anydeskLine(p.equipo || {});\n'
    '  if (adOne) lines.push(adOne);\n'
    '  var redesOne = redesLine(p.equipo || {});\n'
    '  if (redesOne) lines.push(redesOne);\n')
rep(HTML,
    "  } else {\n"
    "    lines.push('', 'Checklist completo \\u2713');\n"
    "  }\n"
    "  return lines.join('\\n');\n"
    '}\n'
    'function waTextAll(list) {',
    "  } else {\n"
    "    lines.push('', 'Checklist completo \\u2713');\n"
    "  }\n"
    "  var naOne = naText(p);\n"
    "  if (naOne) lines.push('No aplica (N/A): ' + naOne);\n"
    "  return lines.join('\\n');\n"
    '}\n'
    'function waTextAll(list) {')
rep(HTML,
    '    var adAll = anydeskLine(p.equipo || {});\n'
    '    if (adAll) extra.push(adAll);\n',
    '    var adAll = anydeskLine(p.equipo || {});\n'
    '    if (adAll) extra.push(adAll);\n'
    '    var redesAll = redesLine(p.equipo || {});\n'
    '    if (redesAll) extra.push(redesAll);\n')

# ---------- 11. avanceText + shareAvanceMail; shareWhatsApp acepta texto ----------
AVANCE = '''// Resumen de avance para equipos sin terminar: porcentaje, marcados/total
// y la lista de lo que falta (sin contar los N/A ni los quitados, que ya
// excluye requiredItems()). Lo usan 'Compartir avance' (WhatsApp) y
// 'Avance por correo' (mailto).
function avanceText(p) {
  var items = requiredItems(p);
  var done = items.filter(function (it) { return p.checks[it.id]; }).length;
  var pend = items.filter(function (it) { return !p.checks[it.id]; }).map(function (it) { return it.text; });
  var lines = ['Checklist de Soporte — Avance', '',
    (p.equipo.marca || 'Equipo') + ' ' + (p.equipo.modelo || ''),
    'Usuario: ' + (p.usuario.nombre || '—') + (p.usuario.area ? ' (' + p.usuario.area + ')' : ''),
    'Analista: ' + (p.tecnico || '—'),
    'Estado: ' + statusLabel(statusOf(p)) + ' — ' + progress(p) + '% (' + done + '/' + items.length + ' puntos)'];
  if (pend.length) {
    lines.push('', 'Falta:');
    pend.forEach(function (t) { lines.push('• ' + t); });
  } else {
    lines.push('', 'Checklist completo ✓');
  }
  var na = naText(p);
  if (na) lines.push('', 'No aplica (N/A): ' + na);
  return lines.join('\\n');
}
// Avance por correo: abre el correo con el resumen como cuerpo del mensaje.
function shareAvanceMail(p) {
  var asunto = 'Avance — ' + (p.equipo.marca || 'Equipo') + ' ' + (p.equipo.modelo || '');
  window.location.href = 'mailto:?subject=' + encodeURIComponent(asunto) + '&body=' + encodeURIComponent(avanceText(p));
}
'''
rep(HTML,
    "  return lines.join('\\n');\n}\nfunction shareText(texto) {",
    "  return lines.join('\\n');\n}\n" + AVANCE + "function shareText(texto) {")
rep(HTML,
    'function shareWhatsApp(preps) {\n'
    "  if (!preps.length) { alert('No hay equipos para compartir.'); return; }\n"
    "  shareText(preps.length === 1 ? waTextOne(preps[0]) : waTextAll(preps));\n"
    '}\n',
    'function shareWhatsApp(preps, texto) {\n'
    '  // Con texto (avanceText) se comparte ese resumen; sin texto, el\n'
    '  // resumen normal del equipo o de la lista, como antes.\n'
    "  if (!preps.length && !texto) { alert('No hay equipos para compartir.'); return; }\n"
    "  shareText(texto || (preps.length === 1 ? waTextOne(preps[0]) : waTextAll(preps)));\n"
    '}\n')

print('Parche 2.3.6 parte 1 aplicada (helpers, nube, PDF, Excel, WhatsApp, avance).')

# ---------- 12. Tarjeta del detectado: redes + fuente del SO ----------
rep(HTML,
    '    var adLine = anydeskLine(d);\n'
    '    var escLine = escritorioLine(d);\n',
    '    var adLine = anydeskLine(d);\n'
    '    var redesDet = redesLine(d);\n'
    '    var osfLine = osFuenteLine(d);\n'
    '    var escLine = escritorioLine(d);\n')
rep(HTML,
    "      (adLine ? '<div class=\"sub\">' + esc(adLine) + '</div>' : '') +\n"
    "      (verLine ? '<div class=\"sub\">' + esc(verLine) + '</div>' : '') +\n"
    "      (escLine ? '<div class=\"sub\">' + esc(escLine) + '</div>' : '') +\n",
    "      (adLine ? '<div class=\"sub\">' + esc(adLine) + '</div>' : '') +\n"
    "      (redesDet ? '<div class=\"sub\">' + esc(redesDet) + '</div>' : '') +\n"
    "      (verLine ? '<div class=\"sub\">' + esc(verLine) + '</div>' : '') +\n"
    "      (osfLine ? '<div class=\"sub\">' + esc(osfLine) + '</div>' : '') +\n"
    "      (escLine ? '<div class=\"sub\">' + esc(escLine) + '</div>' : '') +\n")

# ---------- 13. cardHtml: botones N/A / quitar por punto ----------
rep(HTML,
    '    var rows = gi.map(function (it) {\n'
    '      var checked = !!p.checks[it.id];\n'
    "      var del = it.extra ? '<button class=\"x\" data-del-extra=\"' + it.id + '\" data-prep=\"' + p.id + '\" title=\"Quitar punto\">×</button>' : '';\n",
    '    var rows = gi.map(function (it) {\n'
    '      if (isRemoved(p, it.id)) return \'\';\n'
    '      var checked = !!p.checks[it.id];\n'
    "      var del = it.extra ? '<button class=\"x\" data-del-extra=\"' + it.id + '\" data-prep=\"' + p.id + '\" title=\"Quitar punto\">×</button>' : '';\n"
    '      // N/A: el punto no cuenta y no se pide; tocar de nuevo lo deshace.\n'
    '      // Quitar (✕, solo puntos de plantilla: los extra ya tienen su ×):\n'
    '      // el punto se oculta y se puede restaurar desde la tarjeta.\n'
    '      var na = isNA(p, it.id);\n'
    '      if (na) {\n'
    "        return '<div class=\"item\"><label>' + esc(it.text) + '</label> <span class=\"badge badge-na\">N/A</span>' +\n"
    "          (locked ? '' : ' <button class=\"btn-ghost btn-mini\" data-na=\"' + it.id + '\" data-prep=\"' + p.id + '\">N/A</button>') + del + '</div>';\n"
    '      }\n'
    '      var naBtns = (!locked && !checked)\n'
    "        ? ' <button class=\"btn-ghost btn-mini\" data-na=\"' + it.id + '\" data-prep=\"' + p.id + '\">N/A</button>' +\n"
    "          (it.extra ? '' : ' <button class=\"btn-ghost btn-mini\" data-remove-item=\"' + it.id + '\" data-prep=\"' + p.id + '\" title=\"Quitar punto\">✕</button>') : '';\n")
rep(HTML,
    "        var hint = checked ? '' : ' <span class=\"choice-hint\">⚠️ Elige una opción</span>';\n"
    "        return '<div class=\"item' + (checked ? ' done' : '') + '\" style=\"flex-wrap:wrap\">' +\n"
    "          '<label>' + esc(it.text) + '</label> ' + opts + hint + del + '</div>';\n",
    "        var hint = checked ? '' : ' <span class=\"choice-hint\">⚠️ Elige una opción</span>';\n"
    "        return '<div class=\"item' + (checked ? ' done' : '') + '\" style=\"flex-wrap:wrap\">' +\n"
    "          '<label>' + esc(it.text) + '</label> ' + opts + hint + naBtns + del + '</div>';\n")
rep(HTML,
    "      return '<div class=\"item' + (checked ? ' done' : '') + '\">' +\n"
    "        '<input type=\"checkbox\" data-check=\"' + it.id + '\" data-prep=\"' + p.id + '\"' +\n"
    "        (checked ? ' checked' : '') + (locked ? ' disabled' : '') + '>' +\n"
    "        '<label>' + esc(it.text) + '</label>' + del + '</div>';\n",
    "      return '<div class=\"item' + (checked ? ' done' : '') + '\">' +\n"
    "        '<input type=\"checkbox\" data-check=\"' + it.id + '\" data-prep=\"' + p.id + '\"' +\n"
    "        (checked ? ' checked' : '') + (locked ? ' disabled' : '') + '>' +\n"
    "        '<label>' + esc(it.text) + '</label>' + naBtns + del + '</div>';\n")

# ---------- 14. cardHtml: acciones Compartir avance / correo / No listo ----------
rep(HTML,
    "  if (st === 'listo') actions += '<button class=\"btn-green\" data-deliver=\"' + p.id + '\">Entregado</button>';\n",
    "  if (st === 'listo') actions += '<button class=\"btn-green\" data-deliver=\"' + p.id + '\">Entregado</button>';\n"
    "  if ((st === 'preparacion' || st === 'listo') && pct < 100) {\n"
    "    actions += '<button class=\"btn-ghost\" data-share-avance=\"' + p.id + '\">📤 Compartir avance</button>';\n"
    "    actions += '<button class=\"btn-ghost\" data-mail-avance=\"' + p.id + '\">✉️ Avance por correo</button>';\n"
    "    actions += '<button class=\"btn-ghost\" data-nolisto=\"' + p.id + '\">No listo</button>';\n"
    "  }\n")

# ---------- 15. cardHtml: línea de redes, marcador No listo, quitados y panel de entrega ----------
rep(HTML,
    "  var deliveredLine = p.deliveredAt ? '<div class=\"delivered-line\">Entregado el ' + fmtDate(p.deliveredAt) + '</div>' : '';\n",
    "  var deliveredLine = p.deliveredAt ? '<div class=\"delivered-line\">Entregado el ' + fmtDate(p.deliveredAt) + '</div>' : '';\n"
    "  var redesCard = redesLine(p.equipo || {});\n"
    "  var noListoLine = p.noListo ? '<div class=\"sub\">⚠️ No listo — faltan ' + (p.noListo.faltan || 0) + ' puntos</div>' : '';\n")
rep(HTML,
    "      '<button class=\"btn-dark\" data-save-extra=\"' + p.id + '\">Agregar</button></div>' : '';\n",
    "      '<button class=\"btn-dark\" data-save-extra=\"' + p.id + '\">Agregar</button></div>' : '';\n"
    "  var removedLine = (!locked && p.removedItems && p.removedItems.length)\n"
    "    ? '<div class=\"sub\">Puntos quitados: ' + p.removedItems.length + ' <button class=\"btn-ghost btn-mini\" data-restore-removed=\"' + p.id + '\">Restaurar</button></div>' : '';\n"
    "  // Panel de entrega con avance <100%: qué falta (porcentaje y casillas)\n"
    "  // y dos salidas explícitas; al 100% no se muestra (entrega directa).\n"
    "  var deliverPanel = (window._deliverConfirmFor === p.id && st === 'listo' && pct < 100)\n"
    "    ? '<div class=\"sub\" style=\"margin-top:10px\"><b>⚠️ Este equipo no está al 100% (avance ' + pct + '%) — faltan ' + pendingRequired(p).length + ' puntos:</b></div>' +\n"
    "      pendingRequired(p).map(function (it) { return '<div class=\"sub\">• ' + esc(it.text) + '</div>'; }).join('') +\n"
    "      '<div class=\"actions\"><button class=\"btn-green\" data-deliver-reopen=\"' + p.id + '\">Reabrir para completar</button>' +\n"
    "      '<button class=\"btn-dark\" data-deliver-confirm=\"' + p.id + '\">Entregar así</button></div>' : '';\n")
rep(HTML,
    "    (hwLine ? '<div class=\"sub\">' + esc(hwLine) + '</div>' : '') +\n"
    "    (adLine ? '<div class=\"sub\">' + esc(adLine) + '</div>' : '') +\n",
    "    (hwLine ? '<div class=\"sub\">' + esc(hwLine) + '</div>' : '') +\n"
    "    (adLine ? '<div class=\"sub\">' + esc(adLine) + '</div>' : '') +\n"
    "    (redesCard ? '<div class=\"sub\">' + esc(redesCard) + '</div>' : '') +\n")
rep(HTML,
    "    '<div class=\"pct\">' + pct + '% completado</div>' + deliveredLine + reassignLine + detNote +\n"
    "    groupsHtml + extraForm + reassignForm +\n",
    "    '<div class=\"pct\">' + pct + '% completado</div>' + deliveredLine + noListoLine + reassignLine + detNote +\n"
    "    groupsHtml + removedLine + deliverPanel + extraForm + reassignForm +\n")

# ---------- 16. Handler de #list: cadena prepId + botones nuevos ----------
rep(HTML,
    "  var prepId = q('data-prep') || q('data-deliver') || q('data-ready') || q('data-unready') || q('data-reopen') || q('data-add-extra') || q('data-del-prep') || q('data-save-extra') || q('data-pdf') || q('data-xlsx') || q('data-wa') || q('data-mail') || q('data-reassign') || q('data-save-reassign') || q('data-expand') || q('data-collapse') || q('data-choice') || q('data-ai-falta') || q('data-ai-wa');\n",
    "  var prepId = q('data-prep') || q('data-deliver') || q('data-ready') || q('data-unready') || q('data-reopen') || q('data-add-extra') || q('data-del-prep') || q('data-save-extra') || q('data-pdf') || q('data-xlsx') || q('data-wa') || q('data-mail') || q('data-reassign') || q('data-save-reassign') || q('data-expand') || q('data-collapse') || q('data-choice') || q('data-ai-falta') || q('data-ai-wa') || q('data-na') || q('data-remove-item') || q('data-restore-removed') || q('data-share-avance') || q('data-mail-avance') || q('data-nolisto') || q('data-deliver-reopen') || q('data-deliver-confirm');\n")
rep(HTML,
    "  if (t.hasAttribute('data-deliver') && prep) { prep.deliveredAt = Date.now(); cloudUpsertPrep(prep); save(); setFilter('entregado'); render(); return; }\n"
    "  if (t.hasAttribute('data-ready') && prep) { prep.readyAt = Date.now(); cloudUpsertPrep(prep); save(); setFilter('listo'); render(); return; }\n"
    "  if (t.hasAttribute('data-unready') && prep) { prep.readyAt = null; cloudUpsertPrep(prep); save(); setFilter('preparacion'); render(); return; }\n"
    "  if (t.hasAttribute('data-reopen') && prep) { prep.deliveredAt = null; cloudUpsertPrep(prep); save(); setFilter(statusOf(prep)); render(); return; }\n",
    "  // N/A por punto: alterna; si el avance llega a 100% se limpia 'No listo'.\n"
    "  if (t.hasAttribute('data-na') && prep) {\n"
    "    var naId = t.getAttribute('data-na');\n"
    "    if (!prep.naItems) prep.naItems = {};\n"
    "    if (prep.naItems[naId]) delete prep.naItems[naId]; else prep.naItems[naId] = true;\n"
    "    clearNoListoIfDone(prep);\n"
    "    cloudUpsertPrep(prep);\n"
    "    save(); render(); return;\n"
    "  }\n"
    "  // Quitar punto: se oculta de la tarjeta (no cuenta en el avance).\n"
    "  if (t.hasAttribute('data-remove-item') && prep) {\n"
    "    var remId = t.getAttribute('data-remove-item');\n"
    "    if (!prep.removedItems) prep.removedItems = [];\n"
    "    if (prep.removedItems.indexOf(remId) === -1) prep.removedItems.push(remId);\n"
    "    clearNoListoIfDone(prep);\n"
    "    cloudUpsertPrep(prep);\n"
    "    save(); render(); return;\n"
    "  }\n"
    "  if (t.hasAttribute('data-restore-removed') && prep) {\n"
    "    prep.removedItems = [];\n"
    "    cloudUpsertPrep(prep);\n"
    "    save(); render(); return;\n"
    "  }\n"
    "  if (t.hasAttribute('data-share-avance') && prep) { shareWhatsApp([prep], avanceText(prep)); return; }\n"
    "  if (t.hasAttribute('data-mail-avance') && prep) { shareAvanceMail(prep); return; }\n"
    "  // 'No listo': si estaba listo, vuelve a preparación; marca cuántos\n"
    "  // puntos faltan. Distinto de 'Quitar listo' (deshacer silencioso).\n"
    "  if (t.hasAttribute('data-nolisto') && prep) {\n"
    "    if (prep.readyAt) prep.readyAt = null;\n"
    "    prep.noListo = { fecha: Date.now(), faltan: pendingRequired(prep).length };\n"
    "    cloudUpsertPrep(prep);\n"
    "    save(); setFilter('preparacion'); render(); return;\n"
    "  }\n"
    "  // Entrega con avance <100%: 'Reabrir para completar' no entrega y\n"
    "  // vuelve a preparación; 'Entregar así' entrega como está.\n"
    "  if (t.hasAttribute('data-deliver-reopen') && prep) {\n"
    "    prep.readyAt = null;\n"
    "    window._deliverConfirmFor = null;\n"
    "    cloudUpsertPrep(prep);\n"
    "    save(); setFilter('preparacion'); render(); return;\n"
    "  }\n"
    "  if (t.hasAttribute('data-deliver-confirm') && prep) {\n"
    "    prep.deliveredAt = Date.now();\n"
    "    window._deliverConfirmFor = null;\n"
    "    cloudUpsertPrep(prep);\n"
    "    save(); setFilter('entregado'); render(); return;\n"
    "  }\n"
    "  if (t.hasAttribute('data-deliver') && prep) {\n"
    "    if (progress(prep) < 100) { window._deliverConfirmFor = prep.id; render(); return; }\n"
    "    prep.deliveredAt = Date.now(); cloudUpsertPrep(prep); save(); setFilter('entregado'); render(); return;\n"
    "  }\n"
    "  if (t.hasAttribute('data-ready') && prep) { prep.readyAt = Date.now(); delete prep.noListo; window._deliverConfirmFor = null; cloudUpsertPrep(prep); save(); setFilter('listo'); render(); return; }\n"
    "  if (t.hasAttribute('data-unready') && prep) { prep.readyAt = null; window._deliverConfirmFor = null; cloudUpsertPrep(prep); save(); setFilter('preparacion'); render(); return; }\n"
    "  // 'Reabrir' de un entregado: limpia deliveredAt Y readyAt, vuelve a\n"
    "  // preparación para completar al 100% (antes quedaba en listo).\n"
    "  if (t.hasAttribute('data-reopen') && prep) { prep.deliveredAt = null; prep.readyAt = null; cloudUpsertPrep(prep); save(); setFilter('preparacion'); render(); return; }\n")

# ---------- 17. Limpieza de 'No listo' al marcar casilla o elegir opción ----------
rep(HTML,
    "    prep.checks[cid] = (prep.checks[cid] === cval) ? false : cval;\n"
    "    cloudUpsertPrep(prep);\n",
    "    prep.checks[cid] = (prep.checks[cid] === cval) ? false : cval;\n"
    "    clearNoListoIfDone(prep);\n"
    "    cloudUpsertPrep(prep);\n")
rep(HTML,
    "  prep.checks[t.getAttribute('data-check')] = t.checked;\n"
    "  cloudUpsertPrep(prep);\n",
    "  prep.checks[t.getAttribute('data-check')] = t.checked;\n"
    "  clearNoListoIfDone(prep);\n"
    "  cloudUpsertPrep(prep);\n")

# ---------- 18. 'Usar este equipo': redes al stash de hardware ----------
rep(HTML,
    "    window._detectedHardware = { cpu: d.cpu || '', ramGB: (d.ramGB == null ? '' : d.ramGB), discoGB: (d.discoGB == null ? '' : d.discoGB), discoTipo: d.discoTipo || '', ip: d.ip || '', ipTipo: d.ipTipo || '', anydeskId: d.anydeskId || '', anydeskAlias: d.anydeskAlias || '' };\n",
    "    window._detectedHardware = { cpu: d.cpu || '', ramGB: (d.ramGB == null ? '' : d.ramGB), discoGB: (d.discoGB == null ? '' : d.discoGB), discoTipo: d.discoTipo || '', ip: d.ip || '', ipTipo: d.ipTipo || '', anydeskId: d.anydeskId || '', anydeskAlias: d.anydeskAlias || '', redes: Array.isArray(d.redes) ? d.redes : [] };\n")

# ---------- 19. btnAdd y reasignación de equipo nuevo: redes + campos nuevos ----------
rep(HTML,
    "    id: uid(), createdAt: Date.now(), deliveredAt: null, readyAt: null, checks: det.checks, autoDetectado: det.ids, extraItems: [], reasignaciones: [],\n",
    "    id: uid(), createdAt: Date.now(), deliveredAt: null, readyAt: null, checks: det.checks, autoDetectado: det.ids, extraItems: [], reasignaciones: [], naItems: {}, removedItems: [],\n")
rep(HTML,
    "anydeskId: detHw.anydeskId || '', anydeskAlias: detHw.anydeskAlias || '', fotoSerie: window._fotoSerie || null },",
    "anydeskId: detHw.anydeskId || '', anydeskAlias: detHw.anydeskAlias || '', redes: Array.isArray(detHw.redes) ? detHw.redes : [], fotoSerie: window._fotoSerie || null },")
rep(HTML,
    "      id: uid(), createdAt: Date.now(), deliveredAt: null, readyAt: null, checks: {}, extraItems: [],\n"
    "      reasignaciones: [{ de: de, a: a, fecha: Date.now(), analista: technicianName() }],\n",
    "      id: uid(), createdAt: Date.now(), deliveredAt: null, readyAt: null, checks: {}, extraItems: [], naItems: {}, removedItems: [],\n"
    "      reasignaciones: [{ de: de, a: a, fecha: Date.now(), analista: technicianName() }],\n")

print('Parche 2.3.6 parte 2 aplicada (tarjetas, panel de entrega, handlers, redes en Usar).')

# ---------- 20. test20236.js: versión y extraído ----------
rep(TEST_NEW, "fs.readFileSync(__dirname + '/checklist20235.js', 'utf8')",
    "fs.readFileSync(__dirname + '/checklist20236.js', 'utf8')")
rep(TEST_NEW,
    "  console.log('AM0) versión 2.3.5:', html.includes('Versión 2.3.5'), '| sin 2.3.4:', !html.includes('Versión 2.3.4'),",
    "  console.log('AM0) versión 2.3.6:', html.includes('Versión 2.3.6'), '| sin 2.3.5:', !html.includes('Versión 2.3.5'),")
rep(TEST_NEW,
    "  console.log('AP0) estáticos 2.3.5: versión:', html.includes('Versión 2.3.5') && !html.includes('Versión 2.3.4'),",
    "  console.log('AP0) estáticos 2.3.6: versión:', html.includes('Versión 2.3.6') && !html.includes('Versión 2.3.5'),")
rep(TEST_NEW,
    "  var n235 = (html.match(/2\\.3\\.5/g) || []).length;\n"
    "  console.log('AR0) versión 2.3.5 visible:', html.includes('Versión 2.3.5') && html.includes('Versión: 2.3.5'), '| 0 de 2.3.4:', !html.includes('2.3.4'), '| ocurrencias 2.3.5:', n235 === 13);",
    "  var n236 = (html.match(/2\\.3\\.6/g) || []).length;\n"
    "  console.log('AR0) versión 2.3.6 visible:', html.includes('Versión 2.3.6') && html.includes('Versión: 2.3.6'), '| 0 de 2.3.5:', !html.includes('2.3.5'), '| ocurrencias 2.3.6:', n236 === 13);")

# ---------- 21. AA4 actualizado (cambio intencional: panel de entrega + Reabrir a preparación) ----------
AA4_OLD = """  // AA4: Listo / Entregado / Reabrir suben el equipo.
  upserted.length = 0;
  fakeClick('data-ready', 'p1');
  var listoOk = upserted.length === 1 && !!upserted[0].readyAt;
  upserted.length = 0;
  fakeClick('data-deliver', 'p1');
  var entrOk = upserted.length === 1 && !!upserted[0].deliveredAt;
  upserted.length = 0;
  fakeClick('data-reopen', 'p1');
  var reabOk = upserted.length === 1 && upserted[0].deliveredAt === null;
  console.log('AA4) Listo sube:', listoOk, '| Entregado sube:', entrOk, '| Reabrir sube:', reabOk);"""
AA4_NEW = """  // AA4 (ACTUALIZADO en esta versión, cambio intencional): 'Entregado' con
  // avance <100% ya NO entrega directo: abre el panel de confirmación
  // (ver AT6); aquí se confirma con 'Entregar así'. Y 'Reabrir' de un
  // entregado ahora limpia deliveredAt Y readyAt: vuelve a preparación,
  // no a listo (antes, serie P de 2.0.10, mantenía readyAt).
  upserted.length = 0;
  fakeClick('data-ready', 'p1');
  var listoOk = upserted.length === 1 && !!upserted[0].readyAt;
  upserted.length = 0;
  fakeClick('data-deliver', 'p1');
  var panelOk = window._deliverConfirmFor === 'p1' && upserted.length === 0;
  var pAA4 = state.preparations.find(function (p) { return p.id === 'p1'; });
  var noEntrOk = !!pAA4 && !pAA4.deliveredAt;
  fakeClick('data-deliver-confirm', 'p1');
  var entrOk = upserted.length === 1 && !!upserted[0].deliveredAt;
  upserted.length = 0;
  fakeClick('data-reopen', 'p1');
  var reabOk = upserted.length === 1 && upserted[0].deliveredAt === null && upserted[0].readyAt === null;
  var pAA4b = state.preparations.find(function (p) { return p.id === 'p1'; });
  var reabPrepOk = !!pAA4b && statusOf(pAA4b) === 'preparacion' && filterStatus === 'preparacion';
  console.log('AA4) Listo sube:', listoOk, '| Entregado <100% abre el panel sin entregar:', panelOk && noEntrOk, '| Entregar así sube:', entrOk, '| Reabrir sube y limpia readyAt:', reabOk, '| Reabrir vuelve a preparación:', reabPrepOk);"""
rep(TEST_NEW, AA4_OLD, AA4_NEW)

# ---------- 22. Serie AT ----------
AT = r'''
  // AT: serie nueva versión. Clic realista hecho a mano (sin fakeClick):
  // el botón lleva data-prep y su propio atributo; closest devuelve el
  // botón solo para ese selector y hasAttribute solo para ese atributo.
  function realClick(attr, prepId, itemId) {
    var btn = {
      getAttribute: function (a) { if (a === 'data-prep') return prepId; if (a === attr) return (itemId === undefined ? prepId : itemId); return null; },
      hasAttribute: function (a) { return a === attr; },
      closest: function (sel) { if (sel === '[' + attr + ']') return btn; if (sel === '[data-prep]') return btn; return null; },
      classList: { contains: function () { return false; } }
    };
    document.getElementById('list')._h.click[0]({ target: btn });
  }
  function mkPrepAT(over) { return mkPrep(Object.assign({ id: 'at2' }, over || {})); }
  // AT0: redes y fuente del SO (helpers).
  var redesVacio = redesText({}) === '' && redesLine({}) === '' && redesText({ redes: [] }) === '' && redesText({ redes: [{ nombre: 'Wi-Fi', ip: '' }] }) === '';
  var redesDos = redesText({ redes: [{ nombre: 'Wi-Fi', ip: '192.168.1.45', ipTipo: 'Dinámica' }, { nombre: 'Ethernet', ip: '10.0.0.20', ipTipo: 'Estática' }] });
  var redesOk = redesDos === 'Wi-Fi: 192.168.1.45 (Dinámica) · Ethernet: 10.0.0.20 (Estática)' && redesLine({ redes: [{ ip: '192.168.1.99' }] }) === 'Redes: 192.168.1.99';
  var osfOk = osFuenteLine({ detalles: { osFuente: 'registro' } }) === 'SO detectado por: Registro de Windows' && osFuenteLine({ detalles: { osFuente: 'cim' } }) === 'SO detectado por: CIM (WMI)' && osFuenteLine({ detalles: { osFuente: 'computerinfo' } }) === 'SO detectado por: Get-ComputerInfo' && osFuenteLine({ detalles: { osFuente: 'si' } }) === 'SO detectado por: Información del sistema' && osFuenteLine({ detalles: {} }) === '' && osFuenteLine({}) === '';
  console.log('AT0) redes: vacío nada:', redesVacio, '| dos redes con tipo:', redesOk, '| fuente del SO legible:', osfOk);
  // AT1: redes y fuente del SO en la tarjeta del detectado; viajan con 'Usar este equipo'.
  doLogin('usuario');
  CLOUD_ENABLED = true;
  cloudUser = { uid: 'u1', email: 'test@checklist.local', nombre: 'Test User' };
  var upAT = [];
  global.Cloud.upsertPrep = async function (d) { upAT.push(d); };
  global.Cloud.markDetectadoUsado = async function () {};
  var detAT = { id: 'AT-DET', hostname: 'PC-AT', marca: 'HP', modelo: 'EliteDesk 800', serie: 'AT-DET', tipo: 'Desktop', detectadoEn: Date.now() - 60000, detectadoPor: 'Gerardo', usado: false, checks: { t18: true }, detalles: { osFuente: 'registro' }, versiones: {}, ip: '192.168.1.45', ipTipo: 'Dinámica', redes: [{ nombre: 'Wi-Fi', ip: '192.168.1.45', ipTipo: 'Dinámica' }, { nombre: 'Ethernet', ip: '10.0.0.20', ipTipo: 'Estática' }] };
  detectados = [detAT];
  renderDetectados();
  var detHtmlAT = document.getElementById('detList').innerHTML;
  var detCardOk = detHtmlAT.indexOf('Redes: Wi-Fi: 192.168.1.45 (Dinámica) · Ethernet: 10.0.0.20 (Estática)') !== -1 && detHtmlAT.indexOf('SO detectado por: Registro de Windows') !== -1;
  document.getElementById('detList')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-det-use]' ? { getAttribute: function () { return 'AT-DET'; } } : null; } } });
  var stashRedesOk = window._detectedHardware && Array.isArray(window._detectedHardware.redes) && window._detectedHardware.redes.length === 2 && window._detectedHardware.redes[0].ip === '192.168.1.45';
  document.getElementById('fUser').value = 'Ana';
  document.getElementById('fTec').value = 'Test User';
  upAT.length = 0;
  document.getElementById('btnAdd')._h.click[0]();
  var savedAT = state.preparations[state.preparations.length - 1];
  var savedRedesOk = !!savedAT && Array.isArray(savedAT.equipo.redes) && savedAT.equipo.redes.length === 2 && savedAT.equipo.redes[1].nombre === 'Ethernet';
  var cloudRedesOk = upAT.length === 1 && Array.isArray(upAT[0].equipo.redes) && upAT[0].equipo.redes.length === 2;
  var cardAT = cardHtml(savedAT);
  var pdfAT = Buffer.from(await buildPdf(savedAT).arrayBuffer()).toString('latin1');
  var waOneAT = waTextOne(savedAT);
  var waAllAT = waTextAll([savedAT]);
  var xlsxAT = Buffer.from(await buildXlsx([savedAT]).arrayBuffer()).toString('latin1');
  var redesEnSalidas = cardAT.indexOf('Redes: Wi-Fi: 192.168.1.45 (Dinámica)') !== -1 && pdfAT.indexOf('Redes: Wi-Fi: 192.168.1.45') !== -1 && waOneAT.indexOf('Redes: Wi-Fi: 192.168.1.45 (Dinámica)') !== -1 && waAllAT.indexOf('Redes: Wi-Fi: 192.168.1.45 (Dinámica)') !== -1 && xlsxAT.indexOf('Redes') !== -1 && xlsxAT.indexOf('192.168.1.45') !== -1 && xlsxAT.indexOf('10.0.0.20') !== -1;
  var sinRedesOk = cardHtml(mkPrep()).indexOf('Redes:') === -1 && waTextOne(mkPrep()).indexOf('Redes:') === -1;
  console.log('AT1) detectado muestra redes y fuente:', detCardOk, '| stash con redes:', stashRedesOk, '| prep guarda redes:', savedRedesOk, '| nube con redes:', cloudRedesOk, '| tarjeta/PDF/WA/Excel con redes:', redesEnSalidas, '| sin redes no se muestra nada:', sinRedesOk);
  // AT2: N/A por punto: no cuenta en el avance, no lo pide '¿Qué falta?',
  // se muestra en tarjeta/PDF/WhatsApp/Excel y se deshace; viaja a la nube.
  var reqAT = requiredItems(mkPrepAT());
  var halfChecks = {};
  reqAT.slice(0, 11).forEach(function (it) { halfChecks[it.id] = true; });
  var pNA = mkPrepAT({ checks: Object.assign({}, halfChecks) });
  var basePct = progress(pNA);
  var uncheckedId = reqAT[11].id;
  var uncheckedTxt = reqAT[11].text;
  pNA.naItems = {}; pNA.naItems[uncheckedId] = true;
  var pctNaUnchecked = progress(pNA);
  var checkedId = reqAT[0].id;
  pNA.naItems[checkedId] = true;
  var pctNaChecked = progress(pNA);
  var faltaOk = faltaPrompt(pNA).indexOf(uncheckedTxt) === -1 && faltaPrompt(mkPrepAT({ checks: halfChecks })).indexOf(uncheckedTxt) !== -1;
  var rtNA = prepFromCloud(prepToCloudDoc(pNA));
  var syncNaOk = rtNA.naItems && rtNA.naItems[uncheckedId] === true && rtNA.naItems[checkedId] === true;
  state.preparations.push(mkPrepAT({ id: 'at2b', checks: Object.assign({}, halfChecks) }));
  realClick('data-na', 'at2b', uncheckedId);
  var pNA2 = state.preparations.find(function (p) { return p.id === 'at2b'; });
  var cardNaOk = cardHtml(pNA2).indexOf('N/A') !== -1 && cardHtml(pNA2).indexOf(uncheckedTxt) !== -1;
  var pctAfterClick = progress(pNA2);
  realClick('data-na', 'at2b', uncheckedId);
  var undoOk = !pNA2.naItems[uncheckedId] && cardHtml(pNA2).indexOf('badge-na') === -1;
  var pdfNa = Buffer.from(await buildPdf(pNA).arrayBuffer()).toString('latin1');
  var waNa = waTextOne(pNA);
  var xlsxNa = Buffer.from(await buildXlsx([pNA]).arrayBuffer()).toString('latin1');
  var naEnSalidas = pdfNa.indexOf('[N/A] ' + uncheckedTxt) !== -1 && waNa.indexOf('No aplica (N/A):') !== -1 && waNa.indexOf(uncheckedTxt) !== -1 && xlsxNa.indexOf('Puntos N/A') !== -1 && xlsxNa.indexOf(uncheckedTxt) !== -1;
  console.log('AT2) avance base:', basePct === Math.round(11 / reqAT.length * 100), '| N/A sin marcar sube el avance:', pctNaUnchecked === Math.round(11 / (reqAT.length - 1) * 100), '| N/A marcado baja numerador y denominador:', pctNaChecked === Math.round(10 / (reqAT.length - 2) * 100), '| ¿Qué falta? no lo pide:', faltaOk, '| sincroniza N/A:', syncNaOk, '| tarjeta con badge N/A:', cardNaOk, '| clic N/A cambia el avance:', pctAfterClick === Math.round(11 / (reqAT.length - 1) * 100), '| tocar de nuevo lo deshace:', undoOk, '| PDF/WA/Excel con N/A:', naEnSalidas);
  // AT3: quitar por punto: se oculta, no cuenta y se restaura; viaja a la nube.
  var pQ = mkPrepAT({ id: 'at3', checks: Object.assign({}, halfChecks) });
  var qTxt = reqAT[11].text;
  var qId = reqAT[11].id;
  var baseQ = progress(pQ);
  state.preparations.push(pQ);
  realClick('data-remove-item', 'at3', qId);
  var pQ2 = state.preparations.find(function (p) { return p.id === 'at3'; });
  var cardQ = cardHtml(pQ2);
  var quitOk = cardQ.indexOf(qTxt) === -1 && cardQ.indexOf('Puntos quitados: 1') !== -1 && cardQ.indexOf('Restaurar') !== -1;
  var pctQ = progress(pQ2);
  var rtQ = prepFromCloud(prepToCloudDoc(pQ2));
  var syncQOk = rtQ.removedItems && rtQ.removedItems.indexOf(qId) !== -1;
  realClick('data-restore-removed', 'at3');
  var restOk = pQ2.removedItems.length === 0 && cardHtml(pQ2).indexOf(qTxt) !== -1 && cardHtml(pQ2).indexOf('Puntos quitados:') === -1;
  console.log('AT3) quitar oculta el punto y avisa:', quitOk, '| avance sin el punto:', pctQ === Math.round(11 / (reqAT.length - 1) * 100), '| base era:', baseQ === Math.round(11 / reqAT.length * 100), '| sincroniza quitados:', syncQOk, '| Restaurar lo devuelve:', restOk);
  // AT4: Compartir avance: texto con porcentaje y faltantes, por WhatsApp y por correo.
  var pAv = mkPrepAT({ id: 'at4', checks: Object.assign({}, halfChecks) });
  state.preparations.push(pAv);
  var txtAv = avanceText(pAv);
  var avTxtOk = txtAv.indexOf(progress(pAv) + '%') !== -1 && txtAv.indexOf('11/' + requiredItems(pAv).length + ' puntos') !== -1 && txtAv.indexOf('Falta:') !== -1 && txtAv.indexOf(reqAT[11].text) !== -1;
  var sharedAv = [];
  global.navigator.share = async function (o) { sharedAv.push(o.text); };
  realClick('data-share-avance', 'at4');
  var waAvOk = sharedAv.length === 1 && sharedAv[0] === txtAv;
  global.location.href = '';
  realClick('data-mail-avance', 'at4');
  var mailAvOk = global.location.href.indexOf('mailto:?subject=Avance') === 0 && decodeURIComponent(global.location.href).indexOf('Falta:') !== -1 && decodeURIComponent(global.location.href).indexOf(progress(pAv) + '%') !== -1;
  var fullAv = mkPrepAT({ id: 'at4f', checks: (function () { var c = {}; requiredItems(mkPrepAT({})).forEach(function (it) { c[it.id] = true; }); return c; })() });
  var noBtnFull = cardHtml(fullAv).indexOf('data-share-avance') === -1 && cardHtml(fullAv).indexOf('data-nolisto') === -1;
  var btnPart = cardHtml(pAv).indexOf('data-share-avance') !== -1 && cardHtml(pAv).indexOf('data-mail-avance') !== -1 && cardHtml(pAv).indexOf('data-nolisto') !== -1;
  console.log('AT4) texto con % y faltantes:', avTxtOk, '| WhatsApp comparte el avance:', waAvOk, '| correo abre mailto con el avance:', mailAvOk, '| a 100% no hay botones:', noBtnFull, '| con avance <100% sí:', btnPart);
  // AT5: 'No listo': marca visible, vuelve a preparación y se limpia al 100% o con 'Listo'.
  var pNL = mkPrepAT({ id: 'at5', readyAt: Date.now() - 60000, checks: Object.assign({}, halfChecks) });
  state.preparations.push(pNL);
  var upNL = [];
  global.Cloud.upsertPrep = async function (d) { upNL.push(d); };
  realClick('data-nolisto', 'at5');
  var nlOk = pNL.readyAt === null && statusOf(pNL) === 'preparacion' && !!pNL.noListo && pNL.noListo.faltan === (requiredItems(pNL).length - 11) && cardHtml(pNL).indexOf('⚠️ No listo — faltan ' + (requiredItems(pNL).length - 11) + ' puntos') !== -1 && filterStatus === 'preparacion';
  var cloudNlOk = upNL.length === 1 && !!upNL[0].noListo && upNL[0].noListo.faltan === (requiredItems(pNL).length - 11);
  var rtNL = prepFromCloud(prepToCloudDoc(pNL));
  var syncNlOk = !!rtNL.noListo && rtNL.noListo.faltan === (requiredItems(pNL).length - 11);
  var lastId = reqAT[reqAT.length - 1].id;
  var remaining = requiredItems(pNL).filter(function (it) { return !pNL.checks[it.id]; });
  remaining.slice(0, remaining.length - 1).forEach(function (it) { pNL.checks[it.id] = true; });
  document.getElementById('list')._h.change[0]({ target: { hasAttribute: function (a) { return a === 'data-check'; }, getAttribute: function (a) { return a === 'data-check' ? lastId : a === 'data-prep' ? 'at5' : null; }, checked: true } });
  var clear100Ok = progress(pNL) === 100 && !pNL.noListo;
  pNL.checks = Object.assign({}, halfChecks);
  pNL.noListo = { fecha: Date.now(), faltan: 10 };
  pNL.readyAt = null;
  realClick('data-ready', 'at5');
  var clearListoOk = !pNL.noListo && !!pNL.readyAt;
  console.log('AT5) No listo vuelve a preparación y marca:', nlOk, '| sube a la nube:', cloudNlOk, '| sincroniza:', syncNlOk, '| se limpia al 100%:', clear100Ok, '| se limpia con Listo:', clearListoOk);
  // AT6: entrega con avance <100%: panel con faltantes; 'Reabrir para
  // completar' no entrega y 'Entregar así' sí; al 100% entrega directo.
  var pE = mkPrepAT({ id: 'at6', readyAt: Date.now() - 60000, checks: Object.assign({}, halfChecks) });
  state.preparations.push(pE);
  var upE = [];
  global.Cloud.upsertPrep = async function (d) { upE.push(d); };
  realClick('data-deliver', 'at6');
  var panelOk = window._deliverConfirmFor === 'at6' && !pE.deliveredAt && upE.length === 0;
  var cardPanel = cardHtml(pE);
  var panelTxtOk = cardPanel.indexOf('Reabrir para completar') !== -1 && cardPanel.indexOf('Entregar así') !== -1 && cardPanel.indexOf(progress(pE) + '%') !== -1 && cardPanel.indexOf(reqAT[11].text) !== -1;
  realClick('data-deliver-reopen', 'at6');
  var reopenOk = !pE.deliveredAt && pE.readyAt === null && statusOf(pE) === 'preparacion' && filterStatus === 'preparacion' && window._deliverConfirmFor !== 'at6';
  realClick('data-ready', 'at6');
  realClick('data-deliver', 'at6');
  var panelAgainOk = window._deliverConfirmFor === 'at6' && !pE.deliveredAt;
  realClick('data-deliver-confirm', 'at6');
  var confirmOk = !!pE.deliveredAt && filterStatus === 'entregado' && upE.length >= 1 && !!upE[upE.length - 1].deliveredAt;
  var pF = mkPrepAT({ id: 'at6f', readyAt: Date.now() - 60000, checks: (function () { var c = {}; requiredItems(mkPrepAT({})).forEach(function (it) { c[it.id] = true; }); return c; })() });
  state.preparations.push(pF);
  window._deliverConfirmFor = null;
  upE.length = 0;
  realClick('data-deliver', 'at6f');
  var directOk = !!pF.deliveredAt && window._deliverConfirmFor !== 'at6f' && upE.length === 1;
  console.log('AT6) Entregado <100% abre el panel sin entregar:', panelOk, '| panel con % y faltantes:', panelTxtOk, '| Reabrir para completar vuelve a preparación:', reopenOk, '| el panel vuelve a salir:', panelAgainOk, '| Entregar así entrega:', confirmOk, '| al 100% entrega directo:', directOk);
  // AT7: 'Reabrir' de un entregado lo devuelve a preparación (limpia
  // deliveredAt Y readyAt), sincronizado y con filtro en preparación.
  var pR = mkPrepAT({ id: 'at7', deliveredAt: Date.now() - 60000, readyAt: Date.now() - 120000, checks: Object.assign({}, halfChecks) });
  state.preparations.push(pR);
  var upR = [];
  global.Cloud.upsertPrep = async function (d) { upR.push(d); };
  realClick('data-reopen', 'at7');
  var reOk = pR.deliveredAt === null && pR.readyAt === null && statusOf(pR) === 'preparacion' && filterStatus === 'preparacion' && upR.length === 1 && upR[0].deliveredAt === null && upR[0].readyAt === null;
  console.log('AT7) Reabrir vuelve a preparación (sin readyAt):', reOk);
  // AT8: la cadena de prepId del handler de #list incluye los botones nuevos.
  var chainOk = ['data-na', 'data-remove-item', 'data-restore-removed', 'data-share-avance', 'data-mail-avance', 'data-nolisto', 'data-deliver-reopen', 'data-deliver-confirm'].every(function (a) { return SRC.indexOf("q('" + a + "')") !== -1; });
  var btnsOk = ['data-share-avance', 'data-mail-avance', 'data-nolisto', 'data-deliver-reopen', 'data-deliver-confirm'].every(function (a) { return SRC.indexOf(a + '="') !== -1; });
  console.log('AT8) cadena prepId con botones nuevos:', chainOk, '| botones en el código:', btnsOk);
'''
with open(TEST_NEW, encoding='utf-8') as f:
    t = f.read()
anchor = '  process.exit(0);'
assert t.count(anchor) == 1, 'Ancla process.exit no única'
t = t.replace(anchor, AT + anchor, 1)
with open(TEST_NEW, 'w', encoding='utf-8') as f:
    f.write(t)
print('OK: serie AT añadida a test20236.js')

# ---------- 23. Extraer tests/checklist20236.js del index.html nuevo ----------
with open(HTML, encoding='utf-8') as f:
    lines = f.read().split('\n')
start = next(i for i, ln in enumerate(lines) if ln == '<script>')
end = next(i for i, ln in enumerate(lines) if ln == '</script>')
assert end > start, 'No se encontró el script inline'
with open(EXTRACT, 'w', encoding='utf-8') as f:
    f.write('\n' + '\n'.join(lines[start + 1:end]) + '\n')
print('OK: extraído tests/checklist20236.js (script inline, líneas %d-%d)' % (start + 2, end))

print('Parche 2.3.6 aplicado (firebase.js sin cambios: bundle NO reconstruido).')
