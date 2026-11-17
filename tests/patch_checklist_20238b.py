#!/usr/bin/env python3
"""Parche 238b (teléfono): borradores + ocultar equipos de otros analistas.

Alcance adicional DENTRO de la 2.3.8 (sin subir versión: sigue 2.3.8 /
versionCode 51). Dos pedidos de Gerardo (2026-11-15 ~07:40 y ~07:41).

(A) BORRADOR: 'Guardar para después' un equipo detectado y retomarlo
después con 'Completar datos'.
Interpretaciones / decisiones documentadas:
- Campo nuevo prep.borrador (boolean). Viaja en prepToCloudDoc /
  prepFromCloud (borrador: ... || false) y se sincroniza como cualquier
  prep; save() local lo persiste gratis (serializa state entero).
- 'Guardar para después' (data-det-save, botón btn-dark junto a 'Usar este
  equipo' y 'Descartar') crea DE INMEDIATO el equipo en En preparación
  con todos los datos detectados (checks filtrados, hardware, versiones,
  autoDetectado) y los datos del formulario vacíos (inventario, usuario,
  área, correo), con tecnico/tecnicoUid del analista actual. Se marca
  usado=true en local (d.usado = true) y en la nube
  (cloudMarkDetectadoUsado), se cierra detBox y se pasa al filtro
  En preparación para que se vea el borrador. Si el borrador se elimina,
  se acabó: la detección sigue usado=true y no vuelve al panel.
- El borrador aparece en En preparación propio (pestaña Nuevo) con la
  etiqueta 'Borrador' y la línea '📝 Borrador — faltan datos: inventario,
  usuario, área, correo' (lista calculada de lo que falta). Botón
  '📝 Completar datos' (data-completar) solo para el dueño o el admin
  (canEditPrep + guarda defensiva EDIT_ATTRS); un ajeno no lo ve y el
  handler directo lo bloquea con el aviso de la 2.3.7.
- 'Completar datos' abre Nuevo equipo prellenado con los datos detectados,
  marca window._completarBorradorId y cambia el botón Guardar a
  '💾 Guardar datos completos'. Guardar actualiza ESE MISMO equipo
  (equipo/usuario/tecnico + foto si se tomó) y borra la marca (delete
  ex.borrador), sin tocar los checks (se conservan los detectados y los
  marcados a mano en la tarjeta) y sin duplicar. Si el borrador ya no
  existe o ya no es borrador, se sigue como equipo nuevo con lo del
  formulario. Abrir 'Nuevo equipo' en blanco (btnShowNew) cancela la
  compleción y restaura el botón Guardar.
- Edición LIMITADA solo a borradores: los equipos completos siguen sin
  edición general (serie AR2: sin 'data-edit-prep', sin 'editPrep', sin
  'Editar equipo' en html ni en SRC). 'Completar datos' no existe para
  ellos y el handler lo ignora si !prep.borrador.
- Convivencia con 'Equipo con pendientes' (2.3.8): NO coexisten en una
  misma tarjeta. El letrero de pendientes solo existe en Listo (readyAt),
  y un borrador nunca llega a Listo: los botones Listo y Entregar están
  ocultos mientras sea borrador (aunque llegue al 100% de avance, la
  etiqueta es 'Borrador', no 'Listo para entregar'). Al completarlo
  vuelve al flujo normal. Compartir avance / No listo se dejan como
  están en borradores (no afirman que esté listo).

(B) OCULTAR OTROS ANALISTAS: Por preparar muestra SOLO los propios por
defecto; interruptor '👀 Ver equipos de otros analistas' revela la
sección de ajenos en solo lectura.
Interpretaciones / decisiones documentadas:
- El filtro vive en currentList() (no en el render): para un usuario
  normal con el interruptor apagado los ajenos no existen en la lista.
  Así el interruptor controla TODOS los filtros (Todos, Nuevo,
  Reasignado, Devuelto, preparación, listos, entregados), la búsqueda
  (solo busca entre lo visible) y el compartir general (Excel/WhatsApp/
  correo usan currentList(), así que comparten solo lo que se ve, como
  dice la nota de la barra). Renta no cambia.
- El estado SE RECUERDA por teléfono (localStorage, clave
  'checklist-soporte-ver-otros-v1', '1'/'0'): quien lo enciende lo
  vuelve a encontrar encendido al abrir la app; sin valor guardado,
  apagado (oculto). Lectura al arrancar con try/catch.
- Al ADMIN no le aplica el interruptor: el botón se oculta para él y
  sigue usando su selector 'Todos los usuarios' (con 'Todos' ve todos,
  sin cambio; con un analista elegido, solo los suyos). En modo local
  (sin sesión) tampoco se muestra: no hay ajenos (isOwnPrep true).
- El botón está en su propia fila (id othersRow) debajo de los chips,
  fuera de #chips para que setFilter() no lo toque. Apagado dice
  '👀 Ver equipos de otros analistas'; encendido, '🙈 Ocultar equipos
  de otros analistas' + clase 'on'. La sección de ajenos, cuando se ve,
  sigue siendo la de la 2.3.7 (encabezado 'Equipos de otros analistas
  (solo lectura)', solo WhatsApp/correo + Solicitar asignación).

Adaptaciones de tests existentes (cambio de comportamiento INTENCIONADO,
no regresión): AU1 y AV7 comprobaban ajenos visibles por defecto en
'Todos'; ahora encienden el interruptor (showOthers = true) antes de
esas comprobaciones. La conducta por defecto (ocultos) la cubre la
serie nueva AX.
- www/cloud/firebase.js: SIN cambios -> NO se reconstruye el bundle
  (queda en 496,903 bytes, md5 dabab404a2c6f4065639dc6f808d1bb3).
- NO se toca la versión (2.3.8 / versionCode 51 en todos los lugares).
Cada reemplazo con assert: si el texto viejo no está, se para.
"""
import os
import shutil

CLOUD = '/home/hatch/workspace/android/checklist-cloud/'
HTML = CLOUD + 'www/index.html'
FB = CLOUD + 'www/cloud/firebase.js'
TEST = CLOUD + 'tests/test20238.js'
EXTRACT = CLOUD + 'tests/checklist20238.js'
BAK = CLOUD + 'tests/checklist-2.3.8.html.bak'


def rep(path, old, new, count=1):
    with open(path, encoding='utf-8') as f:
        s = f.read()
    assert old in s, 'NO ENCONTRADO en %s: %r' % (path, old[:90])
    assert s.count(old) == count, 'OCURRENCIAS=%d (esperadas %d) en %s: %r' % (s.count(old), count, path, old[:90])
    with open(path, 'w', encoding='utf-8') as f:
        f.write(s.replace(old, new, count) if count == 1 else s.replace(old, new))
    print('OK:', path.split('/')[-1], '->', new[:70].replace('\n', ' '))


# ---------- 0. Backup (solo si no existe) ----------
if not os.path.exists(BAK):
    shutil.copyfile(HTML, BAK)
    print('OK: backup tests/checklist-2.3.8.html.bak')
else:
    print('OK: backup ya existía, no se sobrescribe')

# ---------- 1. prepToCloudDoc / prepFromCloud: campo borrador ----------
rep(HTML,
    "    naItems: p.naItems || {}, removedItems: p.removedItems || [], noListo: p.noListo || null,\n"
    "    autoDetectado: p.autoDetectado || [],",
    "    naItems: p.naItems || {}, removedItems: p.removedItems || [], noListo: p.noListo || null,\n"
    "    autoDetectado: p.autoDetectado || [], borrador: p.borrador || false,")
rep(HTML,
    "    naItems: doc.naItems || {}, removedItems: doc.removedItems || [], noListo: doc.noListo || null,\n"
    "    autoDetectado: doc.autoDetectado || [],",
    "    naItems: doc.naItems || {}, removedItems: doc.removedItems || [], noListo: doc.noListo || null,\n"
    "    autoDetectado: doc.autoDetectado || [], borrador: doc.borrador || false,")

# ---------- 2. Nota del panel de detectados ----------
rep(HTML,
    '    <div class="share-note">Equipos que el detector vio en la red. Toca «Usar este equipo» para llenar el formulario de Nuevo equipo con sus datos.</div>',
    '    <div class="share-note">Equipos que el detector vio en la red. Toca «Usar este equipo» para llenar el formulario de Nuevo equipo con sus datos, o «Guardar para después» para dejarlo en En preparación como borrador y completarlo luego.</div>')

# ---------- 3. Botón interruptor 'Ver equipos de otros analistas' ----------
rep(HTML,
    '    <button class="chip" data-f="devuelto">Devuelto</button>\n'
    '  </div>\n'
    '  <div class="row" id="adminUserRow" hidden>',
    '    <button class="chip" data-f="devuelto">Devuelto</button>\n'
    '  </div>\n'
    '  <div class="row" id="othersRow">\n'
    '    <button class="chip" id="btnVerOtros" style="flex:1">👀 Ver equipos de otros analistas</button>\n'
    '  </div>\n'
    '  <div class="row" id="adminUserRow" hidden>')

# ---------- 4. Estado showOthers (persistente, por defecto apagado) ----------
rep(HTML,
    "var filterStatus = 'todos';\n"
    "var todosPage = 0;\n"
    "var searchText = '';",
    "var filterStatus = 'todos';\n"
    "var todosPage = 0;\n"
    "var searchText = '';\n"
    "// Ver equipos de otros analistas (238b): por defecto OCULTOS. El estado\n"
    "// se recuerda por teléfono (localStorage): quien lo enciende lo vuelve a\n"
    "// encontrar encendido al abrir la app; sin valor guardado, apagado.\n"
    "var SHOW_OTHERS_KEY = 'checklist-soporte-ver-otros-v1';\n"
    "var showOthers = false;\n"
    "try { showOthers = localStorage.getItem(SHOW_OTHERS_KEY) === '1'; } catch (e) { showOthers = false; }")

# ---------- 5. currentList: ajenos ocultos por defecto (no admin) ----------
rep(HTML,
    "    // Admin con un analista elegido: solo los equipos de ese analista.\n"
    "    if (cloudRole === 'admin' && adminViewUid && adminViewUid !== 'todos' && !isPrepOfAnalyst(p, adminViewUid)) return false;",
    "    // Admin con un analista elegido: solo los equipos de ese analista.\n"
    "    if (cloudRole === 'admin' && adminViewUid && adminViewUid !== 'todos' && !isPrepOfAnalyst(p, adminViewUid)) return false;\n"
    "    // Equipos de otros analistas ocultos por defecto (238b): solo se ven\n"
    "    // con el interruptor 'Ver equipos de otros analistas'. Al admin no le\n"
    "    // aplica: usa el selector 'Todos los usuarios'. Sin sesión (modo\n"
    "    // local) no hay ajenos: isOwnPrep devuelve true para todos.\n"
    "    if (cloudRole !== 'admin' && !showOthers && !isOwnPrep(p)) return false;")

# ---------- 6. Helper prepFromDetectado (antes de renderDetectados) ----------
rep(HTML,
    "// Equipos detectados (2.3.8): solo se listan los NO usados, con sus datos\n"
    "// y dos acciones: usarlo (llena Nuevo equipo) o descartarlo.\n"
    "function renderDetectados() {",
    "// Borrador (238b): un equipo detectado guardado para después nace como\n"
    "// prep en En preparación con los datos detectados (checks, hardware,\n"
    "// versiones, autoDetectado) y los datos del formulario vacíos\n"
    "// (inventario, usuario, área, correo), marcado borrador: true.\n"
    "function prepFromDetectado(d) {\n"
    "  var det = filterDetectedChecks(d.checks || {});\n"
    "  var ver = d.versiones || {};\n"
    "  return {\n"
    "    id: uid(), createdAt: Date.now(), deliveredAt: null, readyAt: null,\n"
    "    checks: det.checks, autoDetectado: det.ids, extraItems: [], reasignaciones: [], naItems: {}, removedItems: [],\n"
    "    borrador: true,\n"
    "    versiones: { so: (typeof ver.so === 'string' ? ver.so : ''), antivirus: (typeof ver.antivirus === 'string' ? ver.antivirus : ''), chrome: (typeof ver.chrome === 'string' ? ver.chrome : '') },\n"
    "    equipo: { tipo: d.tipo || 'Desktop', marca: d.marca || '', modelo: d.modelo || '', serie: d.serie || '', inventario: '', hostname: d.hostname || '', cpu: d.cpu || '', ramGB: (d.ramGB == null ? '' : d.ramGB), discoGB: (d.discoGB == null ? '' : d.discoGB), discoTipo: d.discoTipo || '', ip: d.ip || '', ipTipo: d.ipTipo || '', anydeskId: d.anydeskId || '', anydeskAlias: d.anydeskAlias || '', redes: Array.isArray(d.redes) ? d.redes : [], fotoSerie: null },\n"
    "    usuario: { nombre: '', area: '', correo: '' },\n"
    "    tecnico: technicianName(),\n"
    "    tecnicoUid: tecnicoUidFor(technicianName())\n"
    "  };\n"
    "}\n"
    "// Equipos detectados (2.3.8): solo se listan los NO usados, con sus datos\n"
    "// y dos acciones: usarlo (llena Nuevo equipo) o descartarlo.\n"
    "function renderDetectados() {")

# ---------- 7. Botón 'Guardar para después' en la tarjeta del detectado ----------
rep(HTML,
    "      '<div class=\"actions\"><button class=\"btn-green\" data-det-use=\"' + esc(d.id) + '\">Usar este equipo</button>' +\n"
    "      '<button class=\"btn-ghost\" data-det-del=\"' + esc(d.id) + '\">Descartar</button></div></div>';",
    "      '<div class=\"actions\"><button class=\"btn-green\" data-det-use=\"' + esc(d.id) + '\">Usar este equipo</button>' +\n"
    "      '<button class=\"btn-dark\" data-det-save=\"' + esc(d.id) + '\">💾 Guardar para después</button>' +\n"
    "      '<button class=\"btn-ghost\" data-det-del=\"' + esc(d.id) + '\">Descartar</button></div></div>';")

# ---------- 8. Handler de detList: rama data-det-save ----------
rep(HTML,
    "  var use = t.closest('[data-det-use]');\n"
    "  var del = t.closest('[data-det-del]');\n"
    "  if (!use && !del) return;\n"
    "  var id = (use || del).getAttribute(use ? 'data-det-use' : 'data-det-del');",
    "  var use = t.closest('[data-det-use]');\n"
    "  var del = t.closest('[data-det-del]');\n"
    "  var sav = t.closest('[data-det-save]');\n"
    "  if (!use && !del && !sav) return;\n"
    "  var id = (use || del || sav).getAttribute(use ? 'data-det-use' : del ? 'data-det-del' : 'data-det-save');\n"
    "  // Guardar para después (238b): crea el borrador en En preparación y\n"
    "  // marca la detección como usada (sale del panel, igual que 'Usar este\n"
    "  // equipo'). Si el borrador se elimina después, no vuelve al panel:\n"
    "  // la detección sigue usada.\n"
    "  if (sav) {\n"
    "    var dd = detectados.find(function (x) { return String(x.id) === String(id); });\n"
    "    if (!dd) return;\n"
    "    var draft = prepFromDetectado(dd);\n"
    "    state.preparations.push(draft);\n"
    "    dd.usado = true;\n"
    "    cloudMarkDetectadoUsado(dd.id);\n"
    "    cloudUpsertPrep(draft);\n"
    "    save();\n"
    "    document.getElementById('detBox').hidden = true;\n"
    "    setFilter('preparacion');\n"
    "    render();\n"
    "    return;\n"
    "  }")

# ---------- 9. render(): botón del interruptor (visible/etiqueta) ----------
rep(HTML,
    "  document.getElementById('shareBar').hidden = filterStatus !== 'entregado' && filterStatus !== 'devuelto';",
    "  var voBtn = document.getElementById('btnVerOtros');\n"
    "  if (voBtn) {\n"
    "    voBtn.hidden = (cloudRole === 'admin' || !cloudUser);\n"
    "    voBtn.textContent = showOthers ? '🙈 Ocultar equipos de otros analistas' : '👀 Ver equipos de otros analistas';\n"
    "    voBtn.classList.toggle('on', !!showOthers);\n"
    "  }\n"
    "  document.getElementById('shareBar').hidden = filterStatus !== 'entregado' && filterStatus !== 'devuelto';")

# ---------- 10. Handler del interruptor (antes del handler de chips) ----------
rep(HTML,
    "document.getElementById('chips').addEventListener('click', function (e) {",
    "// Interruptor 'Ver equipos de otros analistas' (238b): revela u oculta\n"
    "// la sección de ajenos en todos los filtros de Por preparar. Se recuerda\n"
    "// por teléfono (localStorage); el admin no lo ve (usa su selector).\n"
    "document.getElementById('btnVerOtros').addEventListener('click', function () {\n"
    "  showOthers = !showOthers;\n"
    "  try { localStorage.setItem(SHOW_OTHERS_KEY, showOthers ? '1' : '0'); } catch (e) { /* sin persistencia */ }\n"
    "  render();\n"
    "});\n"
    "document.getElementById('chips').addEventListener('click', function (e) {")

# ---------- 11. cardHtml: etiqueta 'Borrador' ----------
rep(HTML,
    "  var stateLabel = conPendientes ? 'Equipo con pendientes' : statusLabel(st);",
    "  // Borrador (238b): la etiqueta es 'Borrador' sea cual sea el avance\n"
    "  // (un borrador al 100% tampoco se presenta como listo para entregar:\n"
    "  // le faltan los datos del usuario). La línea de abajo dice qué falta.\n"
    "  var stateLabel = p.borrador ? 'Borrador' : (conPendientes ? 'Equipo con pendientes' : statusLabel(st));\n"
    "  var stateClass = p.borrador ? 'b-prep' : statusClass(st);")
rep(HTML,
    "    '<span class=\"badge ' + statusClass(st) + '\">' + stateLabel + '</span>' +",
    "    '<span class=\"badge ' + stateClass + '\">' + stateLabel + '</span>' +")

# ---------- 12. cardHtml: línea 'Borrador — faltan datos' ----------
rep(HTML,
    "  var pendientesLine = conPendientes ? '<div class=\"sub\">⚠️ Equipo con pendientes — faltan ' + pendientesN + ' puntos</div>' : '';",
    "  // Borrador (238b): qué datos faltan (inventario, usuario, área,\n"
    "  // correo). Convive con 'Equipo con pendientes' sin confundirse: ese\n"
    "  // letrero solo existe en Listo (readyAt), y un borrador nunca llega a\n"
    "  // Listo (el botón Listo está oculto hasta completarlo), así que en una\n"
    "  // misma tarjeta solo se ve uno de los dos.\n"
    "  var faltanDatos = [];\n"
    "  if (p.borrador) {\n"
    "    if (!p.equipo.inventario) faltanDatos.push('inventario');\n"
    "    if (!p.usuario.nombre) faltanDatos.push('usuario');\n"
    "    if (!p.usuario.area) faltanDatos.push('área');\n"
    "    if (!p.usuario.correo) faltanDatos.push('correo');\n"
    "  }\n"
    "  var borradorLine = p.borrador ? '<div class=\"sub\">📝 Borrador — faltan datos' + (faltanDatos.length ? ': ' + faltanDatos.join(', ') : '') + '</div>' : '';\n"
    "  var pendientesLine = conPendientes ? '<div class=\"sub\">⚠️ Equipo con pendientes — faltan ' + pendientesN + ' puntos</div>' : '';")
rep(HTML,
    "    '<div class=\"pct\">' + pct + '% completado</div>' + deliveredLine + noListoLine + pendientesLine + reassignLine + asignLine + detNote +",
    "    '<div class=\"pct\">' + pct + '% completado</div>' + deliveredLine + noListoLine + pendientesLine + borradorLine + reassignLine + asignLine + detNote +")

# ---------- 13. cardHtml: acciones — 'Completar datos'; Listo/Entregar ocultos en borrador ----------
rep(HTML,
    "    if (st === 'preparacion') actions += '<button class=\"btn-green\" data-ready=\"' + p.id + '\">Listo</button>';",
    "    // Borrador (238b): solo el dueño o el admin (editable) lo ve; un\n"
    "    // equipo ajeno nunca muestra este botón (su tarjeta es solo lectura).\n"
    "    if (p.borrador) actions += '<button class=\"btn-green\" data-completar=\"' + p.id + '\">📝 Completar datos</button>';\n"
    "    // Borrador sin Listo (238b): hasta completarlo no sigue el flujo\n"
    "    // (así nunca muestra 'Equipo con pendientes' siendo borrador).\n"
    "    if (st === 'preparacion' && !p.borrador) actions += '<button class=\"btn-green\" data-ready=\"' + p.id + '\">Listo</button>';")
rep(HTML,
    "    if (st === 'listo') actions += '<button class=\"btn-green\" data-deliver=\"' + p.id + '\">' + (pct < 100 ? 'Entregar' : 'Entregado') + '</button>';",
    "    if (st === 'listo' && !p.borrador) actions += '<button class=\"btn-green\" data-deliver=\"' + p.id + '\">' + (pct < 100 ? 'Entregar' : 'Entregado') + '</button>';")

# ---------- 14. Cadena prepId + guarda defensiva: data-completar ----------
rep(HTML,
    " || q('data-aprobar-solicitud') || q('data-rechazar-solicitud');",
    " || q('data-aprobar-solicitud') || q('data-rechazar-solicitud') || q('data-completar');")
rep(HTML,
    " 'data-asignar', 'data-save-asignar'];",
    " 'data-asignar', 'data-save-asignar', 'data-completar'];")

# ---------- 15. Handler de #list: rama data-completar ----------
rep(HTML,
    "  if (t.hasAttribute('data-choice') && prep) {",
    "  // Completar datos de un borrador (238b): abre Nuevo equipo prellenado\n"
    "  // con los datos detectados; Guardar (btnAdd) actualiza ese mismo equipo\n"
    "  // y quita la marca. Solo borradores: un equipo completo no tiene este\n"
    "  // botón y aquí se ignora (no hay edición general, como hasta ahora).\n"
    "  if (t.hasAttribute('data-completar') && prep) {\n"
    "    if (!canEditPrep(prep)) { alert('Este equipo es de otro analista: solo puedes compartirlo por WhatsApp o correo.'); return; }\n"
    "    if (!prep.borrador) return;\n"
    "    document.getElementById('fTipo').value = prep.equipo.tipo || 'Laptop';\n"
    "    document.getElementById('fMarca').value = prep.equipo.marca || '';\n"
    "    document.getElementById('fModelo').value = prep.equipo.modelo || '';\n"
    "    document.getElementById('fSerie').value = prep.equipo.serie || '';\n"
    "    document.getElementById('fInv').value = prep.equipo.inventario || '';\n"
    "    document.getElementById('fHostname').value = prep.equipo.hostname || '';\n"
    "    document.getElementById('fTec').value = prep.tecnico || '';\n"
    "    document.getElementById('fUser').value = prep.usuario.nombre || '';\n"
    "    document.getElementById('fArea').value = prep.usuario.area || '';\n"
    "    document.getElementById('fCorreo').value = prep.usuario.correo || '';\n"
    "    window._detectedChecks = null; window._detectedDetalles = null; window._detectedVersiones = null; window._detectedHardware = null;\n"
    "    window._completarBorradorId = prep.id;\n"
    "    document.getElementById('btnAdd').textContent = '💾 Guardar datos completos';\n"
    "    document.getElementById('detBox').hidden = true;\n"
    "    document.getElementById('newBox').hidden = false;\n"
    "    updateSaveBtn();\n"
    "    return;\n"
    "  }\n"
    "  if (t.hasAttribute('data-choice') && prep) {")

# ---------- 16. btnAdd: completar borrador (actualiza el mismo equipo) ----------
rep(HTML,
    "document.getElementById('btnAdd').addEventListener('click', function () {\n"
    "  var v = function (id) { return document.getElementById(id).value.trim(); };\n"
    "  var det = filterDetectedChecks(window._detectedChecks || {});",
    "document.getElementById('btnAdd').addEventListener('click', function () {\n"
    "  var v = function (id) { return document.getElementById(id).value.trim(); };\n"
    "  // Completar borrador (238b): si se abrió el formulario con\n"
    "  // 'Completar datos', Guardar actualiza ESE equipo (sin crear otro) y\n"
    "  // quita la marca de borrador. Los checks no se tocan: se conservan los\n"
    "  // detectados y los marcados a mano en la tarjeta. Si el borrador ya no\n"
    "  // existe (o ya no es borrador), se sigue como equipo nuevo.\n"
    "  var completarId = window._completarBorradorId || null;\n"
    "  if (completarId) {\n"
    "    var ex = state.preparations.find(function (x) { return x.id === completarId; });\n"
    "    window._completarBorradorId = null;\n"
    "    document.getElementById('btnAdd').textContent = '💾 Guardar equipo';\n"
    "    if (ex && ex.borrador && canEditPrep(ex)) {\n"
    "      if (!v('fModelo') && !v('fSerie') && !v('fUser')) { alert('Pon al menos el modelo, la serie o el nombre del usuario.'); return; }\n"
    "      ex.equipo.tipo = v('fTipo'); ex.equipo.marca = v('fMarca'); ex.equipo.modelo = v('fModelo'); ex.equipo.serie = v('fSerie'); ex.equipo.inventario = v('fInv'); ex.equipo.hostname = v('fHostname');\n"
    "      if (window._fotoSerie) ex.equipo.fotoSerie = window._fotoSerie;\n"
    "      ex.usuario.nombre = v('fUser'); ex.usuario.area = v('fArea'); ex.usuario.correo = v('fCorreo');\n"
    "      ex.tecnico = v('fTec') || technicianName(); ex.tecnicoUid = tecnicoUidFor(v('fTec') || technicianName());\n"
    "      delete ex.borrador;\n"
    "      window._detectedChecks = null; window._detectedDetalles = null; window._detectedVersiones = null; window._detectedHardware = null;\n"
    "      cloudUpsertPrep(ex);\n"
    "      save();\n"
    "      ['fMarca', 'fModelo', 'fSerie', 'fInv', 'fHostname', 'fTec', 'fUser', 'fArea', 'fCorreo'].forEach(function (id) { document.getElementById(id).value = ''; });\n"
    "      prefillTecnico();\n"
    "      window._fotoSerie = null;\n"
    "      document.getElementById('fotoSeriePreview').innerHTML = '';\n"
    "      document.getElementById('fFotoSerie').value = '';\n"
    "      updateSaveBtn();\n"
    "      document.getElementById('newBox').hidden = true;\n"
    "      setFilter('preparacion');\n"
    "      render();\n"
    "      return;\n"
    "    }\n"
    "    // Si no se pudo completar, se sigue abajo como equipo nuevo con lo\n"
    "    // que haya en el formulario (el borrador, si existe, queda intacto).\n"
    "  }\n"
    "  var det = filterDetectedChecks(window._detectedChecks || {});")

# ---------- 17. btnShowNew: cancelar una compleción en curso ----------
rep(HTML,
    "document.getElementById('btnShowNew').addEventListener('click', function () { window._detectedChecks = null; window._detectedDetalles = null; window._detectedVersiones = null; window._detectedHardware = null; togglePanel('newBox'); });",
    "document.getElementById('btnShowNew').addEventListener('click', function () { window._detectedChecks = null; window._detectedDetalles = null; window._detectedVersiones = null; window._detectedHardware = null; window._completarBorradorId = null; document.getElementById('btnAdd').textContent = '💾 Guardar equipo'; togglePanel('newBox'); });")

print('OK: www/index.html parcheado (borrador + ocultar otros)')

# ---------- 18. Tests: adaptación AU1 y AV7 (interruptor apagado por defecto) ----------
rep(TEST,
    "  filterStatus = 'todos'; searchText = ''; todosPage = 0;\n"
    "  var ordAU1 = currentList().map(function (p) { return p.id; });",
    "  // 238b: los ajenos están ocultos por defecto; esta serie comprueba el\n"
    "  // orden propios-primero con el interruptor encendido (serie AX: apagado).\n"
    "  showOthers = true;\n"
    "  filterStatus = 'todos'; searchText = ''; todosPage = 0;\n"
    "  var ordAU1 = currentList().map(function (p) { return p.id; });")
rep(TEST,
    "  state.preparations = [pAV7, pAV7f];\n"
    "  filterStatus = 'todos'; searchText = ''; todosPage = 0; window._expandedId = null;",
    "  state.preparations = [pAV7, pAV7f];\n"
    "  // 238b: en 'Todos' los ajenos solo se ven con el interruptor\n"
    "  // encendido (serie AX: apagado, solo el propio).\n"
    "  showOthers = true;\n"
    "  filterStatus = 'todos'; searchText = ''; todosPage = 0; window._expandedId = null;")

# ---------- 19. Tests: series nuevas AW (borrador) y AX (ocultar otros) ----------
AWAX = r"""
  // AW: serie nueva 238b — borrador 'Guardar para después' + 'Completar
  // datos'. Un detectado se guarda como borrador en En preparación y se
  // retoma después sin crear otro equipo; es la ÚNICA forma de cambiar
  // los datos de un equipo ya guardado (serie AR2: sin edición general).
  loginAs('u1', 'Test User', 'usuario');
  CLOUD_ENABLED = true;
  adminViewUid = 'todos';
  showOthers = false;
  var upAW = [];
  global.Cloud.upsertPrep = async function (d) { upAW.push(d); };
  var markedAW = [];
  global.Cloud.markDetectadoUsado = async function (id) { markedAW.push(id); };
  var delAW = [];
  global.Cloud.deletePrep = async function (id) { delAW.push(id); };
  var detAW = { id: 'AW-DET', hostname: 'PC-AW', marca: 'HP', modelo: 'EliteDesk 800', serie: 'AW-DET', cpu: 'Intel Core i7-10700', ramGB: 16, discoGB: 512, so: 'Windows 11 Pro', tipo: 'Desktop', detectadoEn: Date.now() - 60000, detectadoPor: 'Gerardo', usado: false, checks: { t18: true, t8: 'Office 365' }, detalles: {}, versiones: { so: 'Windows 11 Pro 26H2 (compilación 26200)' } };
  // AW0: estáticos — botón, campo borrador en la nube, 'Completar datos'.
  var aw0 = html.includes('data-det-save="') && html.includes('Guardar para después') &&
    SRC.includes('borrador: p.borrador || false') && SRC.includes('borrador: doc.borrador || false') &&
    SRC.includes('data-completar="') && SRC.includes('Completar datos') && SRC.includes("q('data-completar')") &&
    SRC.includes('prepFromDetectado') && SRC.includes('Borrador — faltan datos');
  console.log('AW0) botón Guardar para después:', aw0);
  // AW1: 'Guardar para después' crea el borrador con los datos detectados.
  var nBeforeAW = state.preparations.length;
  detectados = [detAW];
  renderDetectados();
  var detHtmlAW = document.getElementById('detList').innerHTML;
  var awBtn = detHtmlAW.indexOf('data-det-save="AW-DET"') !== -1 && detHtmlAW.indexOf('Guardar para después') !== -1 && detHtmlAW.indexOf('Usar este equipo') !== -1 && detHtmlAW.indexOf('Descartar') !== -1;
  upAW.length = 0; markedAW.length = 0;
  document.getElementById('detList')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-det-save]' ? { getAttribute: function () { return 'AW-DET'; } } : null; } } });
  var draftAW = state.preparations[state.preparations.length - 1];
  var aw1 = state.preparations.length === nBeforeAW + 1 && !!draftAW && draftAW.borrador === true &&
    draftAW.equipo.modelo === 'EliteDesk 800' && draftAW.equipo.serie === 'AW-DET' && draftAW.equipo.hostname === 'PC-AW' &&
    draftAW.equipo.inventario === '' && draftAW.usuario.nombre === '' && draftAW.usuario.area === '' && draftAW.usuario.correo === '' &&
    draftAW.checks.t18 === true && draftAW.checks.t8 === 'Office 365' && draftAW.autoDetectado.join(',') === 't8,t18' &&
    draftAW.versiones.so === 'Windows 11 Pro 26H2 (compilación 26200)' && draftAW.equipo.cpu === 'Intel Core i7-10700' && draftAW.equipo.ramGB === 16 &&
    draftAW.tecnicoUid === 'u1' && draftAW.tecnico === 'Test User' && !draftAW.deliveredAt && !draftAW.readyAt &&
    upAW.length === 1 && upAW[0].borrador === true && upAW[0].autoDetectado.join(',') === 't8,t18' &&
    markedAW.indexOf('AW-DET') !== -1 && detAW.usado === true &&
    document.getElementById('detBox').hidden === true && filterStatus === 'preparacion';
  console.log('AW1) botón en la tarjeta:', awBtn, '| borrador creado con datos detectados y vacíos:', aw1);
  // AW2: el borrador aparece en En preparación propio (pestaña Nuevo) con
  // su marcador, sin botón Listo ni letrero de pendientes.
  var draftIdAW = draftAW.id;
  filterStatus = 'preparacion'; searchText = ''; todosPage = 0;
  var aw2prep = currentList().some(function (p) { return p.id === draftIdAW; });
  filterStatus = 'nuevo';
  var aw2nuevo = currentList().some(function (p) { return p.id === draftIdAW; });
  filterStatus = 'todos';
  render();
  var listAW2 = document.getElementById('list').innerHTML;
  var cardAW2 = cardHtml(draftAW);
  var aw2 = aw2prep && aw2nuevo && listAW2.indexOf('📝 Borrador — faltan datos') !== -1 &&
    listAW2.indexOf('data-completar="' + draftIdAW + '"') !== -1 &&
    cardAW2.indexOf('>Borrador<') !== -1 && cardAW2.indexOf('Borrador — faltan datos: inventario, usuario, área, correo') !== -1 &&
    cardAW2.indexOf('data-ready="' + draftIdAW + '"') === -1 && cardAW2.indexOf('data-deliver="' + draftIdAW + '"') === -1 &&
    cardAW2.indexOf('Equipo con pendientes') === -1;
  console.log('AW2) en En preparación y en Nuevo:', aw2prep && aw2nuevo, '| marcador + Completar datos, sin Listo ni pendientes:', aw2);
  // AW3: 'Completar datos' abre el formulario prellenado y Guardar
  // actualiza EL MISMO equipo y quita el borrador, sin duplicarlo.
  upAW.length = 0;
  realClick('data-completar', draftIdAW);
  var aw3open = window._completarBorradorId === draftIdAW && document.getElementById('newBox').hidden === false && document.getElementById('detBox').hidden === true &&
    document.getElementById('fModelo').value === 'EliteDesk 800' && document.getElementById('fSerie').value === 'AW-DET' && document.getElementById('fHostname').value === 'PC-AW' &&
    document.getElementById('fInv').value === '' && document.getElementById('fUser').value === '' &&
    document.getElementById('btnAdd').textContent.indexOf('Guardar datos completos') !== -1 &&
    document.getElementById('btnAdd').disabled === false && formReady() === true;
  document.getElementById('fInv').value = 'INV-777';
  document.getElementById('fUser').value = 'Ana Pérez';
  document.getElementById('fArea').value = 'Soporte';
  document.getElementById('fCorreo').value = 'ana@empresa.com';
  var nBeforeAW3 = state.preparations.length;
  document.getElementById('btnAdd')._h.click[0]();
  var doneAW = state.preparations.find(function (p) { return p.id === draftIdAW; });
  var aw3 = state.preparations.length === nBeforeAW3 && !!doneAW && !doneAW.borrador &&
    doneAW.equipo.inventario === 'INV-777' && doneAW.usuario.nombre === 'Ana Pérez' && doneAW.usuario.area === 'Soporte' && doneAW.usuario.correo === 'ana@empresa.com' &&
    doneAW.equipo.modelo === 'EliteDesk 800' && doneAW.checks.t18 === true && doneAW.checks.t8 === 'Office 365' &&
    upAW.length === 1 && upAW[0].borrador === false && upAW[0].equipo.inventario === 'INV-777' &&
    window._completarBorradorId === null && document.getElementById('newBox').hidden === true &&
    cardHtml(doneAW).indexOf('Borrador — faltan datos') === -1 && cardHtml(doneAW).indexOf('data-completar=') === -1 &&
    cardHtml(doneAW).indexOf('data-ready="' + draftIdAW + '"') !== -1;
  console.log('AW3) Completar abre prellenado:', aw3open, '| Guardar actualiza el mismo sin duplicar y quita el borrador:', aw3);
  // AW4: un ajeno no ve 'Completar datos' ni puede completarlo por handler
  // directo; el admin sí lo ve (respeta las guardas de la 2.3.7).
  var fAW4 = mkPrepAU({ id: 'aw4', borrador: true, tecnicoUid: 'uAxel', tecnico: 'Axel Danyael', equipo: { tipo: 'Laptop', marca: 'HP', modelo: 'ModeloBorradorAjeno', serie: 'S-AW4', inventario: '' }, usuario: { nombre: '', area: '', correo: '' } });
  state.preparations = [fAW4];
  loginAs('u1', 'Test User', 'usuario');
  upAW.length = 0; global.lastAlert = '';
  var cardAW4 = cardHtml(fAW4);
  var aw4hide = cardAW4.indexOf('data-completar=') === -1 && cardAW4.indexOf('📝 Borrador — faltan datos') !== -1 &&
    cardAW4.indexOf('data-wa="aw4"') !== -1 && cardAW4.indexOf('data-solicitar-asignacion="aw4"') !== -1;
  realClick('data-completar', 'aw4');
  var aw4block = fAW4.borrador === true && upAW.length === 0 && window._completarBorradorId !== 'aw4' && (global.lastAlert || '').indexOf('otro analista') !== -1;
  loginAs('uGer', 'Gerardo', 'admin');
  var aw4admin = cardHtml(fAW4).indexOf('data-completar="aw4"') !== -1;
  console.log('AW4) ajeno sin Completar datos (marcador sí, WA + solicitar sí):', aw4hide, '| directo bloqueado con aviso:', aw4block, '| admin sí lo ve:', aw4admin);
  // AW5: eliminar el borrador no lo resucita en el panel de detectados.
  loginAs('u1', 'Test User', 'usuario');
  var detAW5 = { id: 'AW5-DET', hostname: 'PC-AW5', marca: 'Dell', modelo: 'Latitude 5420', serie: 'AW5-DET', tipo: 'Laptop', detectadoEn: Date.now() - 60000, detectadoPor: 'Gerardo', usado: false, checks: { t18: true }, detalles: {}, versiones: {} };
  detectados = [detAW5];
  renderDetectados();
  document.getElementById('detList')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-det-save]' ? { getAttribute: function () { return 'AW5-DET'; } } : null; } } });
  var draftAW5 = state.preparations[state.preparations.length - 1];
  var aw5saved = !!draftAW5 && draftAW5.borrador === true && draftAW5.equipo.serie === 'AW5-DET' && detAW5.usado === true;
  loginAs('uGer', 'Gerardo', 'admin');
  delAW.length = 0;
  realClick('data-del-prep', draftAW5.id);
  var aw5gone = state.preparations.every(function (p) { return p.id !== draftAW5.id; }) && delAW.indexOf(draftAW5.id) !== -1;
  var aw5cb = typeof detCbAq === 'function';
  if (aw5cb) detCbAq([Object.assign({}, detAW5, { usado: true })]);
  var panelAW5 = document.getElementById('detList').innerHTML;
  var aw5panel = panelAW5.indexOf('PC-AW5') === -1 && panelAW5.indexOf('No hay equipos detectados pendientes.') !== -1;
  console.log('AW5) borrador guardado y marcado usado:', aw5saved, '| eliminar lo borra (nube):', aw5gone, '| suscripción viva:', aw5cb, '| no vuelve al panel:', aw5panel);

  // AX: serie nueva 238b — equipos de otros analistas OCULTOS por defecto
  // en Por preparar, con interruptor para verlos. El interruptor se
  // recuerda por teléfono (localStorage); al admin no le aplica (usa su
  // selector 'Todos los usuarios'). Renta no cambia.
  loginAs('u1', 'Test User', 'usuario');
  CLOUD_ENABLED = true;
  adminViewUid = 'todos';
  var TAXB = Date.now();
  var eqAXB = function (modelo) { return { tipo: 'Laptop', marca: 'Dell', modelo: modelo, serie: 'S-' + modelo, inventario: '1' }; };
  var pAXown = mkPrepAU({ id: 'ax-own', createdAt: TAXB - 300000, tecnicoUid: 'u1', tecnico: 'Test User', equipo: eqAXB('ModeloPropioAX') });
  var pAXfor = mkPrepAU({ id: 'ax-for', createdAt: TAXB - 200000, tecnicoUid: 'uAxel', tecnico: 'Axel Danyael', equipo: eqAXB('ModeloAjenoAX') });
  // AX0: estáticos — botón, persistencia, filtro en currentList.
  var ax0 = html.includes('id="btnVerOtros"') && html.includes('Ver equipos de otros analistas') && html.includes('id="othersRow"') &&
    SRC.includes('SHOW_OTHERS_KEY') && SRC.includes('checklist-soporte-ver-otros-v1') &&
    SRC.includes("localStorage.getItem(SHOW_OTHERS_KEY) === '1'") && SRC.includes("localStorage.setItem(SHOW_OTHERS_KEY, showOthers ? '1' : '0')") &&
    SRC.includes("if (cloudRole !== 'admin' && !showOthers && !isOwnPrep(p)) return false;");
  console.log('AX0) botón + persistencia + filtro en currentList:', ax0);
  // AX1: por defecto (apagado) solo se ven los propios en Todos y en
  // En preparación, aunque existan ajenos.
  showOthers = false;
  state.preparations = [pAXown, pAXfor];
  filterStatus = 'todos'; searchText = ''; todosPage = 0;
  var ax1todos = currentList().map(function (p) { return p.id; }).join(',') === 'ax-own';
  filterStatus = 'preparacion';
  var ax1prep = currentList().map(function (p) { return p.id; }).join(',') === 'ax-own';
  filterStatus = 'todos';
  render();
  var listAX1 = document.getElementById('list').innerHTML;
  var ax1html = listAX1.indexOf('ModeloPropioAX') !== -1 && listAX1.indexOf('ModeloAjenoAX') === -1 && listAX1.indexOf('Equipos de otros analistas (solo lectura)') === -1;
  var ax1btn = document.getElementById('btnVerOtros').hidden === false && document.getElementById('btnVerOtros').textContent.indexOf('Ver equipos de otros analistas') !== -1;
  console.log('AX1) Todos solo propio:', ax1todos, '| En preparación solo propio:', ax1prep, '| lista sin ajeno ni encabezado:', ax1html, '| botón visible con su texto:', ax1btn);
  // AX2: al encender el interruptor aparecen los ajenos en solo lectura
  // (WhatsApp/correo + Solicitar asignación) y se recuerda en localStorage.
  document.getElementById('btnVerOtros')._h.click[0]();
  var ax2on = showOthers === true && global.localStorage.getItem('checklist-soporte-ver-otros-v1') === '1';
  filterStatus = 'todos'; searchText = ''; todosPage = 0;
  var ax2list = currentList().map(function (p) { return p.id; }).join(',') === 'ax-own,ax-for';
  var listAX2 = document.getElementById('list').innerHTML;
  var iHeadAX2 = listAX2.indexOf('Equipos de otros analistas (solo lectura)'), iForAX2 = listAX2.indexOf('ModeloAjenoAX'), iOwnAX2 = listAX2.indexOf('ModeloPropioAX');
  var ax2html = iOwnAX2 !== -1 && iOwnAX2 < iHeadAX2 && iHeadAX2 < iForAX2;
  var cardAX2 = cardHtml(pAXfor);
  var ax2ro = cardAX2.indexOf('data-wa="ax-for"') !== -1 && cardAX2.indexOf('data-mail="ax-for"') !== -1 && cardAX2.indexOf('data-solicitar-asignacion="ax-for"') !== -1 && cardAX2.indexOf('data-ready="ax-for"') === -1;
  var ax2label = document.getElementById('btnVerOtros').textContent.indexOf('Ocultar equipos de otros analistas') !== -1;
  console.log('AX2) interruptor encendido y recordado:', ax2on, '| lista con los dos:', ax2list, '| sección ajena tras los propios:', ax2html, '| ajeno solo lectura:', ax2ro, '| botón ahora dice Ocultar:', ax2label);
  // AX3: al apagarlo desaparecen de nuevo.
  document.getElementById('btnVerOtros')._h.click[0]();
  var ax3off = showOthers === false && global.localStorage.getItem('checklist-soporte-ver-otros-v1') === '0';
  filterStatus = 'todos'; searchText = '';
  var ax3list = currentList().map(function (p) { return p.id; }).join(',') === 'ax-own';
  var listAX3 = document.getElementById('list').innerHTML;
  var ax3html = listAX3.indexOf('ModeloAjenoAX') === -1 && listAX3.indexOf('ModeloPropioAX') !== -1;
  console.log('AX3) interruptor apagado y recordado:', ax3off, '| lista solo propio:', ax3list, '| HTML sin ajeno:', ax3html);
  // AX4: al admin no le aplica el interruptor (ni lo ve): con 'Todos' ve
  // todos, y con un analista elegido solo los de ese analista.
  loginAs('uGer', 'Gerardo', 'admin');
  adminViewUid = 'todos';
  showOthers = false;
  filterStatus = 'todos'; searchText = '';
  var ax4all = currentList().map(function (p) { return p.id; }).join(',') === 'ax-own,ax-for';
  adminViewUid = 'uAxel';
  var ax4axel = currentList().map(function (p) { return p.id; }).join(',') === 'ax-for';
  adminViewUid = 'todos';
  render();
  var ax4btn = document.getElementById('btnVerOtros').hidden === true;
  console.log('AX4) admin con Todos ve todos en orden de preparación:', ax4all, '| con Axel solo los suyos:', ax4axel, '| botón oculto para el admin:', ax4btn);
  // AX5: las pestañas Nuevo/Reasignado/Devuelto de un usuario normal solo
  // muestran propios con la opción apagada.
  loginAs('u1', 'Test User', 'usuario');
  adminViewUid = 'todos';
  showOthers = false;
  state.preparations = [
    mkPrepAU({ id: 'ax5-nuevo', createdAt: TAXB - 300000, equipo: eqAXB('ModeloAXNuevo') }),
    mkPrepAU({ id: 'ax5-re', createdAt: TAXB - 200000, reasignaciones: [{ de: 'Ana', a: 'Luis', fecha: TAXB - 100000, analista: 'Test User' }], equipo: eqAXB('ModeloAXRe') }),
    mkPrepAU({ id: 'ax5-dev', createdAt: TAXB - 100000, deliveredAt: TAXB - 86400000, readyAt: TAXB - 2 * 86400000, equipo: eqAXB('ModeloAXDev') }),
    mkPrepAU({ id: 'ax5-for', createdAt: TAXB - 50000, tecnicoUid: 'uAxel', tecnico: 'Axel Danyael', reasignaciones: [{ de: 'Ana', a: 'Luis', fecha: TAXB - 100000, analista: 'Axel Danyael' }], equipo: eqAXB('ModeloAXFor') }),
  ];
  filterStatus = 'nuevo'; searchText = '';
  var ax5n = currentList().map(function (p) { return p.id; }).join(',') === 'ax5-nuevo';
  filterStatus = 'reasignado';
  var ax5r = currentList().map(function (p) { return p.id; }).join(',') === 'ax5-re';
  filterStatus = 'devuelto';
  var ax5d = currentList().map(function (p) { return p.id; }).join(',') === 'ax5-dev';
  console.log('AX5) Nuevo solo propio:', ax5n, '| Reasignado solo propio:', ax5r, '| Devuelto solo propio:', ax5d);
  // AX6: la búsqueda respeta el interruptor (un ajeno no aparece al
  // buscarlo con la opción apagada; con ella encendida, sí).
  state.preparations = [pAXown, pAXfor];
  showOthers = false;
  filterStatus = 'todos'; searchText = 'modeloajenoax';
  var ax6off = currentList().length === 0;
  showOthers = true;
  var ax6on = currentList().map(function (p) { return p.id; }).join(',') === 'ax-for';
  searchText = '';
  console.log('AX6) buscar ajeno con opción apagada no lo encuentra:', ax6off, '| encendida sí:', ax6on);
  // AX7: el botón refleja el estado (texto + clase 'on').
  showOthers = false; render();
  var ax7off = document.getElementById('btnVerOtros').textContent.indexOf('Ver equipos de otros analistas') !== -1 && !document.getElementById('btnVerOtros').classList.contains('on');
  showOthers = true; render();
  var ax7on = document.getElementById('btnVerOtros').textContent.indexOf('Ocultar equipos de otros analistas') !== -1 && document.getElementById('btnVerOtros').classList.contains('on');
  showOthers = false; render();
  console.log('AX7) apagado dice Ver sin clase on:', ax7off, '| encendido dice Ocultar con clase on:', ax7on);
"""
with open(TEST, encoding='utf-8') as f:
    t = f.read()
anchor = '  process.exit(0);'
assert t.count(anchor) == 1, 'Ancla process.exit no única'
t = t.replace(anchor, AWAX + anchor, 1)
with open(TEST, 'w', encoding='utf-8') as f:
    f.write(t)
print('OK: series AW y AX añadidas a test20238.js')

# ---------- 20. Extraer tests/checklist20238.js del index.html nuevo ----------
with open(HTML, encoding='utf-8') as f:
    lines = f.read().split('\n')
start = next(i for i, ln in enumerate(lines) if ln == '<script>')
end = next(i for i, ln in enumerate(lines) if ln == '</script>')
assert end > start, 'No se encontró el script inline'
with open(EXTRACT, 'w', encoding='utf-8') as f:
    f.write('\n' + '\n'.join(lines[start + 1:end]) + '\n')
print('OK: extraído tests/checklist20238.js (script inline, líneas %d-%d)' % (start + 2, end))

print('Parche 238b aplicado (firebase.js sin cambios: bundle NO reconstruido; versión 2.3.8/51 sin tocar).')
