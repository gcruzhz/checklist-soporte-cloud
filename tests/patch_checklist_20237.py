#!/usr/bin/env python3
"""Parche 2.3.7 (teléfono): permisos por analista, pestañas por usuario,
asignación de equipos y solicitud de asignación.

Interpretaciones documentadas (para que Gerardo las corrija):
- 'Reagendado' se interpreta como 'Reasignado' (pestaña de equipos propios
  con al menos una reasignación en su historial).
- 'Propio' = prep.tecnicoUid == uid del usuario, con respaldo al nombre
  prep.tecnico para equipos viejos sin tecnicoUid; también cuenta como
  propio un equipo cuya reasignación registró ese analista
  (reasignaciones[].analista == su nombre). La reasignación cambia el
  TITULAR (usuario.nombre); la asignación cambia el ANALISTA responsable
  (tecnico/tecnicoUid) y se registra en prep.asignaciones (NO en
  reasignaciones, para no mezclar ambos historiales).
- Para el admin, las pestañas Nuevo/Reasignado/Devuelto muestran los
  equipos de todos (tiene permisos totales); el selector 'Todos los
  usuarios' afina por analista. El admin ve todos los equipos en orden
  de preparación (createdAt ascendente), sin el orden propio-primero.
- Equipo ajeno: solo WhatsApp y correo en la tarjeta; el resto se oculta
  Y se bloquea en los handlers (guarda defensiva con alert breve).
- Asignar a...: el selector excluye al responsable actual del equipo
  (para el admin que asigna un equipo ajeno, excluye a su responsable,
  no al admin). Asignar limpia cualquier solicitud pendiente.
- Solicitud: una sola pendiente por equipo; aprobar transfiere como una
  asignación (registra en asignaciones) y limpia la solicitud.

- www/cloud/firebase.js: SIN cambios -> NO se reconstruye el bundle
  (queda en 496,903 bytes, md5 dabab404a2c6f4065639dc6f808d1bb3).
- android/app/build.gradle: versionCode 49 -> 50, versionName 2.3.7.
- ios project.pbxproj: MARKETING_VERSION 2.3.7 (x2), CURRENT_PROJECT_VERSION 50 (x2).
- tests: copia test20236.js a test20237.js, actualiza versión y extraído,
  mkPrep pasa a ser equipo propio del usuario de pruebas (tecnicoUid u1,
  tecnico 'Test User': antes no tenía dueño explícito y con el nuevo
  modelo de permisos los fixtures viejos serían 'ajenos' y la regresión
  se bloquearía por las guardas; W4 y compañía no cambian de sentido),
  añade serie AU, extrae tests/checklist20237.js.
Cada reemplazo con assert: si el texto viejo no está, se para.
"""
import shutil

CLOUD = '/home/hatch/workspace/android/checklist-cloud/'
HTML = CLOUD + 'www/index.html'
FB = CLOUD + 'www/cloud/firebase.js'
GRADLE = CLOUD + 'android/app/build.gradle'
PBX = CLOUD + 'ios/App/App.xcodeproj/project.pbxproj'
TEST_OLD = CLOUD + 'tests/test20236.js'
TEST_NEW = CLOUD + 'tests/test20237.js'
EXTRACT = CLOUD + 'tests/checklist20237.js'


def rep(path, old, new, count=1):
    with open(path, encoding='utf-8') as f:
        s = f.read()
    assert old in s, 'NO ENCONTRADO en %s: %r' % (path, old[:90])
    assert s.count(old) == count, 'OCURRENCIAS=%d (esperadas %d) en %s: %r' % (s.count(old), count, path, old[:90])
    with open(path, 'w', encoding='utf-8') as f:
        f.write(s.replace(old, new, count) if count == 1 else s.replace(old, new))
    print('OK:', path.split('/')[-1], '->', new[:70].replace('\n', ' '))


# ---------- 0. Backups 2.3.6 ----------
shutil.copyfile(HTML, CLOUD + 'tests/checklist-2.3.6.html.bak')
shutil.copyfile(FB, CLOUD + 'tests/firebase-2.3.6.js.bak')
print('OK: backups tests/checklist-2.3.6.html.bak y tests/firebase-2.3.6.js.bak')

# ---------- 0b. Copia del test ----------
shutil.copyfile(TEST_OLD, TEST_NEW)
print('OK: test20236.js copiado a test20237.js')

# ---------- 1. www/index.html: versión 2.3.6 -> 2.3.7 (13 ocurrencias) ----------
with open(HTML, encoding='utf-8') as f:
    html = f.read()
assert html.count('2.3.6') == 13, 'OCURRENCIAS 2.3.6=%d (esperadas 13)' % html.count('2.3.6')
assert '2.3.7' not in html, 'Ya hay 2.3.7 en index.html'
with open(HTML, 'w', encoding='utf-8') as f:
    f.write(html.replace('2.3.6', '2.3.7'))
print('OK: index.html versión 2.3.7 (13 ocurrencias)')

# ---------- 2. android/app/build.gradle ----------
rep(GRADLE, '        versionCode 49\n', '        versionCode 50\n')
rep(GRADLE, '        versionName "2.3.6"\n', '        versionName "2.3.7"\n')

# ---------- 3. iOS project.pbxproj ----------
rep(PBX, 'MARKETING_VERSION = 2.3.6;', 'MARKETING_VERSION = 2.3.7;', count=2)
rep(PBX, 'CURRENT_PROJECT_VERSION = 49;', 'CURRENT_PROJECT_VERSION = 50;', count=2)

# ---------- 4. HTML: pestañas nuevas + selector de admin ----------
rep(HTML,
    '    <button class="chip" data-f="entregado">Entregados</button>\n'
    '  </div>\n',
    '    <button class="chip" data-f="entregado">Entregados</button>\n'
    '    <button class="chip" data-f="nuevo">Nuevo</button>\n'
    '    <button class="chip" data-f="reasignado">Reasignado</button>\n'
    '    <button class="chip" data-f="devuelto">Devuelto</button>\n'
    '  </div>\n'
    '  <div class="row" id="adminUserRow" hidden>\n'
    '    <select id="adminUserFilter" style="flex:1"><option value="todos">Todos los usuarios</option></select>\n'
    '  </div>\n')

# ---------- 5. prepToCloudDoc / prepFromCloud: campos nuevos ----------
rep(HTML,
    '    checks: p.checks || {}, extraItems: p.extraItems || [], reasignaciones: p.reasignaciones || [],\n',
    '    checks: p.checks || {}, extraItems: p.extraItems || [], reasignaciones: p.reasignaciones || [],\n'
    "    tecnicoUid: p.tecnicoUid || '', asignaciones: p.asignaciones || [], solicitudAsignacion: p.solicitudAsignacion || null,\n")
rep(HTML,
    '    checks: doc.checks || {}, extraItems: doc.extraItems || [], reasignaciones: doc.reasignaciones || [],\n',
    '    checks: doc.checks || {}, extraItems: doc.extraItems || [], reasignaciones: doc.reasignaciones || [],\n'
    "    tecnicoUid: doc.tecnicoUid || '', asignaciones: doc.asignaciones || [], solicitudAsignacion: doc.solicitudAsignacion || null,\n")

# ---------- 6. Helpers de permisos (tras visiblePreps) ----------
rep(HTML,
    'function visiblePreps() { return state.preparations.filter(deliveredVisible); }\n',
    '''function visiblePreps() { return state.preparations.filter(deliveredVisible); }
// Permisos por analista (2.3.7): cada equipo tiene un analista responsable
// (prep.tecnicoUid + prep.tecnico). El admin puede con todos; un usuario
// normal solo edita los suyos; los de otros son solo lectura (WhatsApp y
// correo). Sin sesión (modo local) no hay restricciones.
var adminViewUid = 'todos'; // admin: 'todos' = Todos los usuarios, o el uid de un analista
function isOwnPrep(p) {
  if (!cloudUser) return true;
  if (p.tecnicoUid) return p.tecnicoUid === cloudUser.uid;
  // Equipos viejos sin tecnicoUid: respaldo por el nombre del analista.
  if (p.tecnico && (p.tecnico === technicianName() || p.tecnico === cloudUser.nombre)) return true;
  // Participó en una reasignación: fue el analista que la registró.
  var tn = technicianName();
  return (p.reasignaciones || []).some(function (r) { return r.analista === tn || r.analista === cloudUser.nombre; });
}
function isPrepOfAnalyst(p, uid) {
  if (p.tecnicoUid) return p.tecnicoUid === uid;
  var u = null;
  teamUsers.forEach(function (x) { if (x.uid === uid) u = x; });
  if (u && p.tecnico) return p.tecnico === (u.nombre || u.email);
  return false;
}
function canEditPrep(p) { return cloudRole === 'admin' || isOwnPrep(p); }
// Uid del analista responsable por su nombre: el propio usuario, o un
// compañero de teamUsers si se escribió su nombre a mano en el formulario.
function tecnicoUidFor(nombre) {
  if (!nombre) return cloudUser ? cloudUser.uid : '';
  if (cloudUser && (nombre === cloudUser.nombre || nombre === cloudUser.email)) return cloudUser.uid;
  var hit = null;
  teamUsers.forEach(function (u) { if (u.nombre === nombre || u.email === nombre) hit = u; });
  if (hit) return hit.uid;
  return '';
}
function analystOptionsHtml(excludeUid) {
  return teamUsers.filter(function (u) { return u.uid !== excludeUid; }).map(function (u) {
    return '<option value="' + esc(u.uid) + '">' + esc(u.nombre || u.email || 'Usuario') + '</option>';
  }).join('');
}
function refreshAdminUserFilter() {
  var sel = document.getElementById('adminUserFilter');
  if (!sel) return;
  var cur = adminViewUid || 'todos';
  sel.innerHTML = '<option value="todos">Todos los usuarios</option>' + teamUsers.map(function (u) {
    return '<option value="' + esc(u.uid) + '"' + (u.uid === cur ? ' selected' : '') + '>' + esc(u.nombre || u.email || 'Usuario') + '</option>';
  }).join('');
  sel.value = cur;
}
function asignacionesText(p) {
  return (p.asignaciones || []).map(function (a) { return (a.de || '—') + ' → ' + (a.a || '—') + ' (' + fmtDate(a.fecha) + ')'; }).join('; ');
}
// Asignar (2.3.7): transfiere la responsabilidad al nuevo analista y lo
// registra en prep.asignaciones (distinto de reasignaciones, que cambia el
// TITULAR del equipo). El traspaso resuelve cualquier solicitud pendiente.
function doAssign(prep, newUid, newNombre) {
  if (!prep.asignaciones) prep.asignaciones = [];
  prep.asignaciones.push({ de: prep.tecnico || '', a: newNombre, fecha: Date.now() });
  prep.tecnicoUid = newUid;
  prep.tecnico = newNombre;
  prep.solicitudAsignacion = null;
}
''')

# ---------- 7. currentList: pestañas por usuario + propios primero ----------
rep(HTML,
    '''function currentList() {
  var q = searchText.trim().toLowerCase();
  var list = state.preparations.filter(function (p) {
    if (!deliveredVisible(p)) return false;
    if (filterStatus !== 'todos' && statusOf(p) !== filterStatus) return false;
    if (!q) return true;
    var hay = [p.equipo.tipo, p.equipo.marca, p.equipo.modelo, p.equipo.serie, p.equipo.inventario, p.equipo.hostname,
      p.usuario.nombre, p.usuario.area, p.usuario.correo, p.tecnico,
      (p.reasignaciones || []).map(function (r) { return (r.de || '') + ' ' + (r.a || ''); }).join(' ')].join(' ').toLowerCase();
    return hay.indexOf(q) !== -1;
  });
  // Más recientes primero
  list.sort(function (a, b) { return b.createdAt - a.createdAt; });
  return list;
}''',
    '''function currentList() {
  var q = searchText.trim().toLowerCase();
  var list = state.preparations.filter(function (p) {
    if (!deliveredVisible(p)) return false;
    // Admin con un analista elegido: solo los equipos de ese analista.
    if (cloudRole === 'admin' && adminViewUid && adminViewUid !== 'todos' && !isPrepOfAnalyst(p, adminViewUid)) return false;
    // Pestañas por usuario (2.3.7): solo equipos propios. 'Nuevo' = propio
    // en preparación o listo, sin reasignaciones; 'Reasignado' = propio con
    // al menos una reasignación; 'Devuelto' = propio ya entregado. El admin
    // ve en estas pestañas los equipos de todos (permisos totales).
    if (filterStatus === 'nuevo') {
      if (cloudRole !== 'admin' && !isOwnPrep(p)) return false;
      if (statusOf(p) === 'entregado') return false;
      if ((p.reasignaciones || []).length) return false;
    } else if (filterStatus === 'reasignado') {
      if (cloudRole !== 'admin' && !isOwnPrep(p)) return false;
      if (!(p.reasignaciones || []).length) return false;
    } else if (filterStatus === 'devuelto') {
      if (cloudRole !== 'admin' && !isOwnPrep(p)) return false;
      if (statusOf(p) !== 'entregado') return false;
    } else if (filterStatus !== 'todos' && statusOf(p) !== filterStatus) return false;
    if (!q) return true;
    var hay = [p.equipo.tipo, p.equipo.marca, p.equipo.modelo, p.equipo.serie, p.equipo.inventario, p.equipo.hostname,
      p.usuario.nombre, p.usuario.area, p.usuario.correo, p.tecnico,
      (p.reasignaciones || []).map(function (r) { return (r.de || '') + ' ' + (r.a || ''); }).join(' ')].join(' ').toLowerCase();
    return hay.indexOf(q) !== -1;
  });
  // Vista principal (2.3.7): primero los propios, en el orden en que se
  // prepararon (createdAt ascendente, el más antiguo primero), y luego los
  // de otros analistas. El admin no usa este orden: ve todos en orden de
  // preparación.
  if (cloudRole === 'admin') {
    list.sort(function (a, b) { return a.createdAt - b.createdAt; });
  } else {
    list.sort(function (a, b) {
      var ao = isOwnPrep(a) ? 0 : 1, bo = isOwnPrep(b) ? 0 : 1;
      if (ao !== bo) return ao - bo;
      return a.createdAt - b.createdAt;
    });
  }
  return list;
}''')

# ---------- 8. Tarjetas con sección aparte para equipos ajenos ----------
rep(HTML,
    '''function todosListHtml(list) {
  var activos = list.filter(function (p) { return statusOf(p) !== 'entregado'; });
  var entregados = list.filter(function (p) { return statusOf(p) === 'entregado'; });
  var html = activos.map(cardHtml).join('');''',
    '''// Tarjetas con sección aparte para los equipos de otros analistas
// (solo lectura): primero los propios, luego el encabezado y los ajenos.
function sectionedCards(list) {
  if (cloudRole === 'admin') return list.map(cardHtml).join('');
  var own = list.filter(isOwnPrep);
  var other = list.filter(function (p) { return !isOwnPrep(p); });
  var html = own.map(cardHtml).join('');
  if (other.length) html += '<div class="group-title">Equipos de otros analistas (solo lectura)</div>' + other.map(cardHtml).join('');
  return html;
}
function todosListHtml(list) {
  var activos = list.filter(function (p) { return statusOf(p) !== 'entregado'; });
  var entregados = list.filter(function (p) { return statusOf(p) === 'entregado'; });
  var html = sectionedCards(activos);''')

# ---------- 9. render: barra de compartir también en Devuelto + sección ----------
rep(HTML,
    "  document.getElementById('shareBar').hidden = filterStatus !== 'entregado';\n",
    "  document.getElementById('shareBar').hidden = filterStatus !== 'entregado' && filterStatus !== 'devuelto';\n")
rep(HTML,
    "  } else {\n    box.innerHTML = list.map(cardHtml).join('');\n  }\n",
    "  } else {\n    box.innerHTML = sectionedCards(list);\n  }\n")

# ---------- 10. applyRoleUI: fila del selector de admin ----------
rep(HTML,
    """function applyRoleUI() {
  var isAdmin = cloudRole === 'admin';
  document.getElementById('tabUsuarios').hidden = !isAdmin;
""",
    """function applyRoleUI() {
  var isAdmin = cloudRole === 'admin';
  document.getElementById('tabUsuarios').hidden = !isAdmin;
  var auRow = document.getElementById('adminUserRow');
  if (auRow) auRow.hidden = !isAdmin;
  if (isAdmin) refreshAdminUserFilter();
""")

# ---------- 11. Selector de admin: listener + refresco con teamUsers ----------
rep(HTML,
    "document.getElementById('chips').addEventListener('click', function (e) {\n",
    """document.getElementById('adminUserFilter').addEventListener('change', function (e) {
  adminViewUid = e.target.value || 'todos';
  todosPage = 0;
  window._expandedId = null;
  render();
});
document.getElementById('chips').addEventListener('click', function (e) {
""")
rep(HTML,
    "  window.Cloud.listUsers().then(function (us) { teamUsers = us || []; renderEquipo(); }).catch(function () {});\n",
    "  window.Cloud.listUsers().then(function (us) { teamUsers = us || []; refreshAdminUserFilter(); renderEquipo(); }).catch(function () {});\n")

# ---------- 12. cardHtml: editable, botones según permisos ----------
rep(HTML,
    """function cardHtml(p) {
  var st = statusOf(p);
  var pct = progress(p);
  var items = allItems(p);
  var locked = !!p.deliveredAt;
""",
    """function cardHtml(p) {
  var st = statusOf(p);
  var pct = progress(p);
  var items = allItems(p);
  var locked = !!p.deliveredAt;
  var editable = canEditPrep(p);
""")
rep(HTML,
    """      var del = it.extra ? '<button class="x" data-del-extra="' + it.id + '" data-prep="' + p.id + '" title="Quitar punto">×</button>' : '';""",
    """      var del = (it.extra && editable) ? '<button class="x" data-del-extra="' + it.id + '" data-prep="' + p.id + '" title="Quitar punto">×</button>' : '';""")
rep(HTML,
    """          (locked ? '' : ' <button class="btn-ghost btn-mini" data-na="' + it.id + '" data-prep="' + p.id + '">N/A</button>') + del + '</div>';""",
    """          ((locked || !editable) ? '' : ' <button class="btn-ghost btn-mini" data-na="' + it.id + '" data-prep="' + p.id + '">N/A</button>') + del + '</div>';""")
rep(HTML,
    """      var naBtns = (!locked && !checked)
""",
    """      var naBtns = (!locked && editable && !checked)
""")
rep(HTML,
    """          return '<button class="chip' + (sel ? ' on' : '') + '" data-choice="' + it.id + '" data-prep="' + p.id + '" data-value="' + esc(o) + '"' + (locked ? ' disabled' : '') + '>' + esc(o) + '</button>';""",
    """          return '<button class="chip' + (sel ? ' on' : '') + '" data-choice="' + it.id + '" data-prep="' + p.id + '" data-value="' + esc(o) + '"' + ((locked || !editable) ? ' disabled' : '') + '>' + esc(o) + '</button>';""")
rep(HTML,
    """        '<input type="checkbox" data-check="' + it.id + '" data-prep="' + p.id + '"' +
        (checked ? ' checked' : '') + (locked ? ' disabled' : '') + '>' +""",
    """        '<input type="checkbox" data-check="' + it.id + '" data-prep="' + p.id + '"' +
        (checked ? ' checked' : '') + ((locked || !editable) ? ' disabled' : '') + '>' +""")
rep(HTML,
    """  var actions = '';
  if (st === 'preparacion') actions += '<button class="btn-green" data-ready="' + p.id + '">Listo</button>';
  if (st === 'listo') actions += '<button class="btn-green" data-deliver="' + p.id + '">Entregado</button>';
  if ((st === 'preparacion' || st === 'listo') && pct < 100) {
    actions += '<button class="btn-ghost" data-share-avance="' + p.id + '">📤 Compartir avance</button>';
    actions += '<button class="btn-ghost" data-mail-avance="' + p.id + '">✉️ Avance por correo</button>';
    actions += '<button class="btn-ghost" data-nolisto="' + p.id + '">No listo</button>';
  }
  if (st === 'listo' && p.readyAt && pct < 100) actions += '<button class="btn-ghost" data-unready="' + p.id + '">Quitar listo</button>';
  if (st === 'entregado') actions += '<button class="btn-ghost" data-reopen="' + p.id + '">Reabrir</button>';
  if (!locked) actions += '<button class="btn-ghost" data-add-extra="' + p.id + '">+ Punto extra</button>';
  if (cloudRole === 'admin') actions += '<button class="btn-dark" data-pdf="' + p.id + '">PDF / Compartir</button>';
  if (st !== 'entregado') actions += '<button class="btn-ghost" data-ai-falta="' + p.id + '">✨ ¿Qué falta?</button>';
  if (st === 'entregado') {
    actions += '<button class="btn-ghost" data-xlsx="' + p.id + '">Exportar a Excel</button>';
    actions += '<button class="btn-ghost" data-wa="' + p.id + '">Enviar datos por WhatsApp</button>';
    actions += '<button class="btn-ghost" data-ai-wa="' + p.id + '">✨ Resumen con IA</button>';
    actions += '<button class="btn-ghost" data-mail="' + p.id + '">Enviar por correo</button>';
  }
  if (cloudRole === 'admin') actions += '<button class="btn-ghost" data-reassign="' + p.id + '">Reasignar</button>';
  if (cloudRole === 'admin') actions += '<button class="btn-danger" data-del-prep="' + p.id + '">Eliminar</button>';""",
    """  // Equipo ajeno (2.3.7): solo lectura — solo WhatsApp y correo, más
  // 'Solicitar asignación' (ver solicitudHtml más abajo). Nada de editar:
  // ni casillas, ni N/A/quitar, ni Listo/Entregado, ni Reasignar, ni
  // Eliminar, ni PDF, ni Excel, ni IA, ni Compartir avance ni No listo.
  var actions = '';
  if (!editable) {
    actions += '<button class="btn-ghost" data-wa="' + p.id + '">Enviar datos por WhatsApp</button>';
    actions += '<button class="btn-ghost" data-mail="' + p.id + '">Enviar por correo</button>';
  } else {
    if (st === 'preparacion') actions += '<button class="btn-green" data-ready="' + p.id + '">Listo</button>';
    if (st === 'listo') actions += '<button class="btn-green" data-deliver="' + p.id + '">Entregado</button>';
    if ((st === 'preparacion' || st === 'listo') && pct < 100) {
      actions += '<button class="btn-ghost" data-share-avance="' + p.id + '">📤 Compartir avance</button>';
      actions += '<button class="btn-ghost" data-mail-avance="' + p.id + '">✉️ Avance por correo</button>';
      actions += '<button class="btn-ghost" data-nolisto="' + p.id + '">No listo</button>';
    }
    if (st === 'listo' && p.readyAt && pct < 100) actions += '<button class="btn-ghost" data-unready="' + p.id + '">Quitar listo</button>';
    if (st === 'entregado') actions += '<button class="btn-ghost" data-reopen="' + p.id + '">Reabrir</button>';
    if (!locked) actions += '<button class="btn-ghost" data-add-extra="' + p.id + '">+ Punto extra</button>';
    if ((st === 'preparacion' || st === 'listo') && !locked) actions += '<button class="btn-dark" data-asignar="' + p.id + '">Asignar a…</button>';
    if (cloudRole === 'admin') actions += '<button class="btn-dark" data-pdf="' + p.id + '">PDF / Compartir</button>';
    if (st !== 'entregado') actions += '<button class="btn-ghost" data-ai-falta="' + p.id + '">✨ ¿Qué falta?</button>';
    if (st === 'entregado') {
      actions += '<button class="btn-ghost" data-xlsx="' + p.id + '">Exportar a Excel</button>';
      actions += '<button class="btn-ghost" data-wa="' + p.id + '">Enviar datos por WhatsApp</button>';
      actions += '<button class="btn-ghost" data-ai-wa="' + p.id + '">✨ Resumen con IA</button>';
      actions += '<button class="btn-ghost" data-mail="' + p.id + '">Enviar por correo</button>';
    }
    if (cloudRole === 'admin') actions += '<button class="btn-ghost" data-reassign="' + p.id + '">Reasignar</button>';
    if (cloudRole === 'admin') actions += '<button class="btn-danger" data-del-prep="' + p.id + '">Eliminar</button>';
  }""")

# ---------- 13. cardHtml: líneas de asignaciones/solicitud + formularios ----------
rep(HTML,
    """  var reassignLine = (p.reasignaciones && p.reasignaciones.length)
    ? '<div class="sub">Reasignaciones: ' + esc(reassignText(p)) + '</div>' : '';""",
    """  var reassignLine = (p.reasignaciones && p.reasignaciones.length)
    ? '<div class="sub">Reasignaciones: ' + esc(reassignText(p)) + '</div>' : '';
  var asignLine = (p.asignaciones && p.asignaciones.length)
    ? '<div class="sub">Asignaciones: ' + esc(asignacionesText(p)) + '</div>' : '';
  // Solicitud de asignación (2.3.7): solo hay una pendiente a la vez. El
  // admin ve Aprobar/Rechazar; el solicitante ve Cancelar solicitud; otro
  // usuario solo ve de quién es la solicitud pendiente.
  var sol = p.solicitudAsignacion && p.solicitudAsignacion.estado === 'pendiente' ? p.solicitudAsignacion : null;
  var solicitudHtml = '';
  if (sol) {
    if (cloudRole === 'admin') {
      solicitudHtml = '<div class="sub">📩 ' + esc(sol.deNombre || 'Un analista') + ' pide que se le asigne este equipo para terminarlo.</div>' +
        '<div class="actions"><button class="btn-green" data-aprobar-solicitud="' + p.id + '">Aprobar asignación</button>' +
        '<button class="btn-ghost" data-rechazar-solicitud="' + p.id + '">Rechazar</button></div>';
    } else if (cloudUser && sol.deUid === cloudUser.uid) {
      solicitudHtml = '<div class="sub">📩 Solicitud de asignación enviada (pendiente).</div>' +
        '<div class="actions"><button class="btn-ghost" data-cancel-solicitud="' + p.id + '">Cancelar solicitud</button></div>';
    } else {
      solicitudHtml = '<div class="sub">📩 Solicitud pendiente de ' + esc(sol.deNombre || 'otro analista') + '</div>';
    }
  } else if (!editable && cloudUser) {
    solicitudHtml = '<div class="actions"><button class="btn-dark" data-solicitar-asignacion="' + p.id + '">Solicitar asignación</button></div>';
  }
  var asignarForm = (editable && window._asignarFor === p.id && (st === 'preparacion' || st === 'listo'))
    ? '<div class="row" style="margin-top:10px"><select id="asignarSelect" style="flex:1">' + analystOptionsHtml(p.tecnicoUid || (cloudUser && cloudUser.uid)) + '</select>' +
      '<button class="btn-dark" data-save-asignar="' + p.id + '">Asignar</button></div>' +
      (teamUsers.filter(function (u) { return u.uid !== (p.tecnicoUid || (cloudUser && cloudUser.uid)); }).length ? '' : '<div class="sub">No hay otros analistas todavía.</div>') : '';""")
rep(HTML,
    "  var reassignForm = (window._reassignFor === p.id)\n",
    "  var reassignForm = (cloudRole === 'admin' && window._reassignFor === p.id)\n")
rep(HTML,
    "  var extraForm = (!locked && window._extraFor === p.id)\n",
    "  var extraForm = (!locked && editable && window._extraFor === p.id)\n")
rep(HTML,
    "  var removedLine = (!locked && p.removedItems && p.removedItems.length)\n",
    "  var removedLine = (!locked && editable && p.removedItems && p.removedItems.length)\n")
rep(HTML,
    "    '<div class=\"pct\">' + pct + '% completado</div>' + deliveredLine + noListoLine + reassignLine + detNote +\n",
    "    '<div class=\"pct\">' + pct + '% completado</div>' + deliveredLine + noListoLine + reassignLine + asignLine + detNote +\n")
rep(HTML,
    "    groupsHtml + removedLine + deliverPanel + extraForm + reassignForm +\n",
    "    groupsHtml + removedLine + deliverPanel + extraForm + reassignForm + solicitudHtml + asignarForm +\n")

# ---------- 14. btnAdd / btnReGuardar: tecnicoUid al crear ----------
rep(HTML,
    """    usuario: { nombre: v('fUser'), area: v('fArea'), correo: v('fCorreo') },
    tecnico: v('fTec') || technicianName()
  };""",
    """    usuario: { nombre: v('fUser'), area: v('fArea'), correo: v('fCorreo') },
    tecnico: v('fTec') || technicianName(),
    tecnicoUid: tecnicoUidFor(v('fTec') || technicianName())
  };""")
rep(HTML,
    """      usuario: { nombre: a, area: '', correo: '' },
      tecnico: technicianName()
    };""",
    """      usuario: { nombre: a, area: '', correo: '' },
      tecnico: technicianName(),
      tecnicoUid: tecnicoUidFor(technicianName())
    };""")

# ---------- 15. Handler de #list: cadena, guarda defensiva, acciones nuevas ----------
rep(HTML,
    " || q('data-deliver-confirm');\n",
    " || q('data-deliver-confirm') || q('data-asignar') || q('data-save-asignar') || q('data-solicitar-asignacion') || q('data-cancel-solicitud') || q('data-aprobar-solicitud') || q('data-rechazar-solicitud');\n")
rep(HTML,
    """  if (t.hasAttribute('data-choice') && prep) {
""",
    """  // Guarda defensiva (2.3.7): un equipo ajeno es solo lectura para un
  // usuario normal. Solo WhatsApp y correo pasan; el resto se ignora con
  // un aviso breve. La tarjeta ya oculta esos botones; esto cubre
  // llamadas directas al handler.
  if (prep && !canEditPrep(prep)) {
    var EDIT_ATTRS = ['data-choice', 'data-pdf', 'data-xlsx', 'data-ai-falta', 'data-ai-wa', 'data-reassign', 'data-save-reassign', 'data-na', 'data-remove-item', 'data-restore-removed', 'data-share-avance', 'data-mail-avance', 'data-nolisto', 'data-deliver-reopen', 'data-deliver-confirm', 'data-deliver', 'data-ready', 'data-unready', 'data-reopen', 'data-del-prep', 'data-add-extra', 'data-save-extra', 'data-del-extra', 'data-asignar', 'data-save-asignar'];
    var blocked = EDIT_ATTRS.some(function (a) { return t.hasAttribute(a); });
    if (blocked) { alert('Este equipo es de otro analista: solo puedes compartirlo por WhatsApp o correo.'); return; }
  }
  if (t.hasAttribute('data-choice') && prep) {
""")
rep(HTML,
    """  // N/A por punto: alterna; si el avance llega a 100% se limpia 'No listo'.
""",
    """  // Asignar a otro analista (2.3.7): abre el selector; al confirmar
  // transfiere la responsabilidad y registra el traspaso en asignaciones.
  if (t.hasAttribute('data-asignar') && prep) {
    if (!canEditPrep(prep)) { alert('Solo el analista responsable o el administrador puede asignar este equipo.'); return; }
    window._asignarFor = (window._asignarFor === prep.id ? null : prep.id);
    render(); return;
  }
  if (t.hasAttribute('data-save-asignar') && prep) {
    if (!canEditPrep(prep)) { alert('Solo el analista responsable o el administrador puede asignar este equipo.'); return; }
    var selAs = document.getElementById('asignarSelect');
    var newUid = selAs ? selAs.value : '';
    var newUser = null;
    teamUsers.forEach(function (u) { if (u.uid === newUid) newUser = u; });
    if (!newUser) { alert('Elige a quién asignar el equipo.'); return; }
    doAssign(prep, newUid, newUser.nombre || newUser.email || '');
    window._asignarFor = null;
    cloudUpsertPrep(prep);
    save(); render(); return;
  }
  // Solicitar asignación (2.3.7): una sola solicitud pendiente por equipo,
  // guardada en el documento del equipo (sin colección nueva).
  if (t.hasAttribute('data-solicitar-asignacion') && prep) {
    if (canEditPrep(prep)) return; // propio: no hace falta pedirlo
    var cur = prep.solicitudAsignacion;
    if (cur && cur.estado === 'pendiente') return; // ya hay una: no se duplica
    prep.solicitudAsignacion = { deUid: cloudUser ? cloudUser.uid : '', deNombre: technicianName(), fecha: Date.now(), estado: 'pendiente' };
    cloudUpsertPrep(prep);
    save(); render(); return;
  }
  if (t.hasAttribute('data-cancel-solicitud') && prep) {
    var curC = prep.solicitudAsignacion;
    if (!curC || curC.estado !== 'pendiente') return;
    if (!cloudUser || curC.deUid !== cloudUser.uid) { alert('Solo quien pidió la asignación puede cancelarla.'); return; }
    prep.solicitudAsignacion = null;
    cloudUpsertPrep(prep);
    save(); render(); return;
  }
  if (t.hasAttribute('data-aprobar-solicitud') && prep) {
    if (cloudRole !== 'admin') { alert('Solo el administrador aprueba solicitudes.'); return; }
    var curA = prep.solicitudAsignacion;
    if (!curA || curA.estado !== 'pendiente') return;
    doAssign(prep, curA.deUid, curA.deNombre);
    cloudUpsertPrep(prep);
    save(); render(); return;
  }
  if (t.hasAttribute('data-rechazar-solicitud') && prep) {
    if (cloudRole !== 'admin') { alert('Solo el administrador rechaza solicitudes.'); return; }
    if (!prep.solicitudAsignacion || prep.solicitudAsignacion.estado !== 'pendiente') return;
    prep.solicitudAsignacion = null;
    cloudUpsertPrep(prep);
    save(); render(); return;
  }
  // N/A por punto: alterna; si el avance llega a 100% se limpia 'No listo'.
""")
rep(HTML,
    """document.getElementById('list').addEventListener('change', function (e) {
  var t = e.target;
  if (!t.hasAttribute('data-check')) return;
  var prep = state.preparations.find(function (p) { return p.id === t.getAttribute('data-prep'); });
  if (!prep) return;
""",
    """document.getElementById('list').addEventListener('change', function (e) {
  var t = e.target;
  if (!t.hasAttribute('data-check')) return;
  var prep = state.preparations.find(function (p) { return p.id === t.getAttribute('data-prep'); });
  if (!prep) return;
  if (!canEditPrep(prep)) { alert('Este equipo es de otro analista: solo puedes compartirlo por WhatsApp o correo.'); return; }
""")

# ---------- 16. Test 2.3.7: versión, extraído y fixture con dueño ----------
rep(TEST_NEW, "const SRC = fs.readFileSync(__dirname + '/checklist20236.js', 'utf8');",
    "const SRC = fs.readFileSync(__dirname + '/checklist20237.js', 'utf8');")
rep(TEST_NEW,
    "    usuario: { nombre: 'Ana', area: 'Sistemas', correo: '' }, tecnico: 'Juan Pérez' }, over || {});",
    "    usuario: { nombre: 'Ana', area: 'Sistemas', correo: '' }, tecnico: 'Test User', tecnicoUid: 'u1' }, over || {});")
rep(TEST_NEW,
    "  console.log('AM0) versión 2.3.6:', html.includes('Versión 2.3.6'), '| sin 2.3.5:', !html.includes('Versión 2.3.5'),",
    "  console.log('AM0) versión 2.3.7:', html.includes('Versión 2.3.7'), '| sin 2.3.6:', !html.includes('Versión 2.3.6'),")
rep(TEST_NEW,
    "  console.log('AP0) estáticos 2.3.6: versión:', html.includes('Versión 2.3.6') && !html.includes('Versión 2.3.5'),",
    "  console.log('AP0) estáticos 2.3.7: versión:', html.includes('Versión 2.3.7') && !html.includes('Versión 2.3.6'),")
rep(TEST_NEW,
    """  var n236 = (html.match(/2\\.3\\.6/g) || []).length;
  console.log('AR0) versión 2.3.6 visible:', html.includes('Versión 2.3.6') && html.includes('Versión: 2.3.6'), '| 0 de 2.3.5:', !html.includes('2.3.5'), '| ocurrencias 2.3.6:', n236 === 13);""",
    """  var n237 = (html.match(/2\\.3\\.7/g) || []).length;
  console.log('AR0) versión 2.3.7 visible:', html.includes('Versión 2.3.7') && html.includes('Versión: 2.3.7'), '| 0 de 2.3.6:', !html.includes('2.3.6'), '| ocurrencias 2.3.7:', n237 === 22);""")

# ---------- 17. Serie AU en test20237.js ----------
AU = '''
  // AU: serie nueva 2.3.7 — permisos por analista, pestañas por usuario,
  // asignación y solicitud de asignación. realClick (serie AT) reutilizado:
  // botón realista hecho a mano, sin fakeClick.
  function mkPrepAU(over) {
    var base = mkPrep({ id: 'au1', tecnicoUid: 'u1', tecnico: 'Test User' });
    return Object.assign(base, over || {});
  }
  function loginAs(uid, nombre, rol) {
    cloudUser = { uid: uid, email: nombre.toLowerCase().replace(/ /g, '') + '@checklist.local', nombre: nombre };
    cloudRole = rol || 'usuario';
    applyRoleUI();
  }
  teamUsers = [
    { uid: 'u1', nombre: 'Test User', rol: 'usuario', email: 'test@checklist.local' },
    { uid: 'uAxel', nombre: 'Axel Danyael', rol: 'usuario', email: 'axel@checklist.local' },
    { uid: 'uAle', nombre: 'Alejandro', rol: 'usuario', email: 'alejandro@checklist.local' },
  ];
  // AU0: estáticos — pestañas, selector de admin, campos nuevos en la nube.
  var au0Chips = html.includes('data-f="nuevo"') && html.includes('data-f="reasignado"') && html.includes('data-f="devuelto"');
  var au0Admin = html.includes('id="adminUserRow"') && html.includes('id="adminUserFilter"') && html.includes('Todos los usuarios');
  var au0Sync = SRC.includes("tecnicoUid: p.tecnicoUid || ''") && SRC.includes("tecnicoUid: doc.tecnicoUid || ''") &&
    SRC.includes('asignaciones: p.asignaciones || []') && SRC.includes('asignaciones: doc.asignaciones || []') &&
    SRC.includes('solicitudAsignacion: p.solicitudAsignacion || null') && SRC.includes('solicitudAsignacion: doc.solicitudAsignacion || null');
  var au0Fn = SRC.includes('function isOwnPrep') && SRC.includes('function canEditPrep') && SRC.includes('function doAssign') &&
    SRC.includes('Equipos de otros analistas (solo lectura)') && SRC.includes('data-asignar="') && SRC.includes('data-solicitar-asignacion="') && SRC.includes('data-aprobar-solicitud="');
  console.log('AU0) pestañas Nuevo/Reasignado/Devuelto:', au0Chips, '| selector Todos los usuarios:', au0Admin, '| tecnicoUid/asignaciones/solicitud en prepToCloudDoc/prepFromCloud:', au0Sync, '| helpers y botones:', au0Fn);
  // AU1: vista principal — propios primero en orden de preparación.
  loginAs('u1', 'Test User', 'usuario');
  CLOUD_ENABLED = true;
  adminViewUid = 'todos';
  var TAU = Date.now();
  var eqAU = function (modelo) { return { tipo: 'Laptop', marca: 'Dell', modelo: modelo, serie: 'S-' + modelo, inventario: '1' }; };
  state.preparations = [
    mkPrepAU({ id: 'au-own-old', createdAt: TAU - 300000, tecnicoUid: 'u1', tecnico: 'Test User', equipo: eqAU('ModeloPropioViejo') }),
    mkPrepAU({ id: 'au-foreign', createdAt: TAU - 200000, tecnicoUid: 'uAxel', tecnico: 'Axel Danyael', equipo: eqAU('ModeloAjeno') }),
    mkPrepAU({ id: 'au-own-new', createdAt: TAU - 100000, tecnicoUid: 'u1', tecnico: 'Test User', equipo: eqAU('ModeloPropioNuevo') }),
  ];
  filterStatus = 'todos'; searchText = ''; todosPage = 0;
  var ordAU1 = currentList().map(function (p) { return p.id; });
  filterStatus = 'preparacion';
  var ordAU1b = currentList().map(function (p) { return p.id; });
  filterStatus = 'todos';
  render();
  var listHtmlAU1 = document.getElementById('list').innerHTML;
  var iViejo = listHtmlAU1.indexOf('ModeloPropioViejo'), iNuevo = listHtmlAU1.indexOf('ModeloPropioNuevo'),
    iHead = listHtmlAU1.indexOf('Equipos de otros analistas (solo lectura)'), iAjeno = listHtmlAU1.indexOf('ModeloAjeno');
  console.log('AU1) propios primero en orden de preparación:', ordAU1.join(',') === 'au-own-old,au-own-new,au-foreign', '| también en En preparación:', ordAU1b.join(',') === 'au-own-old,au-own-new,au-foreign', '| sección ajena con encabezado y después de los propios:', iViejo !== -1 && iViejo < iNuevo && iNuevo < iHead && iHead < iAjeno);
  // AU2: pestañas Nuevo / Reasignado / Devuelto (solo propios; 15 días).
  state.preparations = [
    mkPrepAU({ id: 'au2-nuevo', createdAt: TAU - 300000 }),
    mkPrepAU({ id: 'au2-re', createdAt: TAU - 200000, reasignaciones: [{ de: 'Ana', a: 'Luis', fecha: TAU - 100000, analista: 'Test User' }] }),
    mkPrepAU({ id: 'au2-dev', createdAt: TAU - 100000, deliveredAt: TAU - 86400000, readyAt: TAU - 2 * 86400000 }),
    mkPrepAU({ id: 'au2-for', createdAt: TAU - 50000, tecnicoUid: 'uAxel', tecnico: 'Axel Danyael', reasignaciones: [{ de: 'Ana', a: 'Luis', fecha: TAU - 100000, analista: 'Axel Danyael' }] }),
    mkPrepAU({ id: 'au2-dev-old', createdAt: TAU - 25 * 86400000, deliveredAt: TAU - 20 * 86400000, readyAt: TAU - 21 * 86400000 }),
  ];
  loginAs('u1', 'Test User', 'usuario');
  filterStatus = 'nuevo';
  var tabNuevo = currentList().map(function (p) { return p.id; });
  filterStatus = 'reasignado';
  var tabRe = currentList().map(function (p) { return p.id; });
  filterStatus = 'devuelto';
  var tabDev = currentList().map(function (p) { return p.id; });
  loginAs('uGer', 'Gerardo', 'admin');
  filterStatus = 'devuelto';
  var tabDevAdmin = currentList().map(function (p) { return p.id; });
  console.log('AU2) Nuevo solo propio sin reasignar:', tabNuevo.join(',') === 'au2-nuevo', '| Reasignado solo propio con historial:', tabRe.join(',') === 'au2-re', '| Devuelto solo propio entregado reciente:', tabDev.join(',') === 'au2-dev', '| admin en Devuelto ve también el de hace 20 días:', tabDevAdmin.indexOf('au2-dev') !== -1 && tabDevAdmin.indexOf('au2-dev-old') !== -1);
  // AU3: equipo ajeno solo comparte por WA/correo; ni siquiera por handler directo.
  loginAs('u1', 'Test User', 'usuario');
  var fAU3 = mkPrepAU({ id: 'au3', tecnicoUid: 'uAxel', tecnico: 'Axel Danyael', checks: { t1: true } });
  state.preparations = [fAU3];
  var cardF = cardHtml(fAU3);
  var noEditAU3 = ['data-ready', 'data-deliver', 'data-na', 'data-remove-item', 'data-reassign', 'data-del-prep', 'data-pdf', 'data-xlsx', 'data-ai-falta', 'data-ai-wa', 'data-share-avance', 'data-mail-avance', 'data-nolisto', 'data-add-extra', 'data-unready'].every(function (a) { return cardF.indexOf(a + '="') === -1; });
  var shareOnlyAU3 = cardF.indexOf('data-wa="au3"') !== -1 && cardF.indexOf('data-mail="au3"') !== -1 && cardF.indexOf('data-solicitar-asignacion="au3"') !== -1;
  var fAU3d = mkPrepAU({ id: 'au3d', tecnicoUid: 'uAxel', tecnico: 'Axel Danyael', deliveredAt: TAU - 86400000, readyAt: TAU - 2 * 86400000 });
  var cardFD = cardHtml(fAU3d);
  var delShareAU3 = cardFD.indexOf('data-wa="au3d"') !== -1 && cardFD.indexOf('data-mail="au3d"') !== -1 && cardFD.indexOf('data-xlsx') === -1 && cardFD.indexOf('data-ai-wa') === -1 && cardFD.indexOf('data-pdf') === -1;
  var up3 = [];
  global.Cloud.upsertPrep = async function (d) { up3.push(d); };
  global.lastAlert = '';
  realClick('data-ready', 'au3');
  var guardReady = !fAU3.readyAt && up3.length === 0 && (global.lastAlert || '').indexOf('otro analista') !== -1;
  realClick('data-na', 'au3', 't2');
  var guardNa = !fAU3.naItems || !fAU3.naItems.t2;
  document.getElementById('list')._h.change[0]({ target: { hasAttribute: function (a) { return a === 'data-check'; }, getAttribute: function (a) { return a === 'data-check' ? 't2' : a === 'data-prep' ? 'au3' : null; }, checked: true } });
  var guardCheck = fAU3.checks.t2 !== true;
  var shared3 = [];
  global.navigator.share = async function (o) { shared3.push(o.text); };
  realClick('data-wa', 'au3');
  var waOkAU3 = shared3.length === 1 && shared3[0].indexOf('Inspiron 3501') !== -1;
  console.log('AU3) ajeno sin botones de edición:', noEditAU3, '| solo WA/correo + solicitar:', shareOnlyAU3, '| entregado ajeno sin Excel/PDF/IA:', delShareAU3, '| Listo directo bloqueado con aviso:', guardReady, '| N/A directo bloqueado:', guardNa, '| casilla directa bloqueada:', guardCheck, '| WhatsApp sí se comparte:', waOkAU3);
  // AU4: admin — selector 'Todos los usuarios', todos los permisos, sin orden propio-primero.
  loginAs('uGer', 'Gerardo', 'admin');
  adminViewUid = 'todos';
  refreshAdminUserFilter();
  var selHtmlAU4 = document.getElementById('adminUserFilter').innerHTML;
  var selOkAU4 = selHtmlAU4.indexOf('Todos los usuarios') !== -1 && selHtmlAU4.indexOf('value="uAxel"') !== -1 && selHtmlAU4.indexOf('Axel Danyael') !== -1 && selHtmlAU4.indexOf('Alejandro') !== -1;
  var cardFA = cardHtml(fAU3);
  var adminBtns = cardFA.indexOf('data-pdf') !== -1 && cardFA.indexOf('data-reassign') !== -1 && cardFA.indexOf('data-del-prep') !== -1 && cardFA.indexOf('data-ready') !== -1 && cardFA.indexOf('data-asignar') !== -1;
  state.preparations = [
    mkPrepAU({ id: 'au4-own', createdAt: TAU - 100000, tecnicoUid: 'u1', tecnico: 'Test User', equipo: eqAU('ModeloAdminPropio') }),
    mkPrepAU({ id: 'au4-axel', createdAt: TAU - 300000, tecnicoUid: 'uAxel', tecnico: 'Axel Danyael', equipo: eqAU('ModeloAdminAxel') }),
    mkPrepAU({ id: 'au4-ale', createdAt: TAU - 200000, tecnicoUid: 'uAle', tecnico: 'Alejandro', equipo: eqAU('ModeloAdminAle') }),
  ];
  filterStatus = 'todos';
  adminViewUid = 'todos';
  var ordAdmin = currentList().map(function (p) { return p.id; });
  adminViewUid = 'uAxel';
  var onlyAxel = currentList().map(function (p) { return p.id; });
  adminViewUid = 'todos';
  var up4 = [];
  global.Cloud.upsertPrep = async function (d) { up4.push(d); };
  var pAxel4 = state.preparations.find(function (p) { return p.id === 'au4-axel'; });
  realClick('data-ready', 'au4-axel');
  var adminEdit = !!pAxel4.readyAt && up4.length === 1;
  console.log('AU4) selector con Todos + analistas:', selOkAU4, '| admin ve todos los botones en equipo ajeno:', adminBtns, '| admin sin propio-primero (orden de preparación):', ordAdmin.join(',') === 'au4-axel,au4-ale,au4-own', '| con Axel elegido solo sus equipos:', onlyAxel.join(',') === 'au4-axel', '| admin edita equipo ajeno:', adminEdit);
  // AU5: Asignar a otro analista transfiere la propiedad y conserva el avance.
  loginAs('u1', 'Test User', 'usuario');
  adminViewUid = 'todos';
  var pA5 = mkPrepAU({ id: 'au5', checks: { t1: true, t2: true } });
  state.preparations = [pA5];
  var up5 = [];
  global.Cloud.upsertPrep = async function (d) { up5.push(d); };
  realClick('data-asignar', 'au5');
  var panelAU5 = window._asignarFor === 'au5' && cardHtml(pA5).indexOf('id="asignarSelect"') !== -1 &&
    cardHtml(pA5).indexOf('<option value="uAxel">Axel Danyael</option>') !== -1 && cardHtml(pA5).indexOf('<option value="u1"') === -1;
  document.getElementById('asignarSelect').value = 'uAxel';
  realClick('data-save-asignar', 'au5');
  var asgOk = pA5.tecnicoUid === 'uAxel' && pA5.tecnico === 'Axel Danyael' && pA5.asignaciones.length === 1 &&
    pA5.asignaciones[0].de === 'Test User' && pA5.asignaciones[0].a === 'Axel Danyael' && pA5.checks.t1 === true && pA5.checks.t2 === true;
  var upAsg = up5.length === 1 && up5[0].tecnicoUid === 'uAxel' && up5[0].asignaciones.length === 1;
  var cardAsg = cardHtml(pA5).indexOf('Asignaciones: Test User → Axel Danyael') !== -1;
  var nowForeign = !isOwnPrep(pA5) && cardHtml(pA5).indexOf('data-solicitar-asignacion') !== -1 && cardHtml(pA5).indexOf('data-ready') === -1;
  loginAs('uAxel', 'Axel Danyael', 'usuario');
  var nowOwnAxel = isOwnPrep(pA5) && cardHtml(pA5).indexOf('data-ready') !== -1;
  loginAs('uGer', 'Gerardo', 'admin');
  var pA5b = mkPrepAU({ id: 'au5b', tecnicoUid: 'uAxel', tecnico: 'Axel Danyael' });
  state.preparations = [pA5b];
  realClick('data-asignar', 'au5b');
  document.getElementById('asignarSelect').value = 'uAle';
  realClick('data-save-asignar', 'au5b');
  var adminAsg = pA5b.tecnicoUid === 'uAle' && pA5b.tecnico === 'Alejandro';
  console.log('AU5) panel con los demás analistas (sin mí):', panelAU5, '| asigna y registra el traspaso:', asgOk, '| sube a la nube:', upAsg, '| historial en la tarjeta:', cardAsg, '| para mí ya es ajeno (solo lectura + solicitar):', nowForeign, '| para Axel ya es propio:', nowOwnAxel, '| el admin asigna cualquier equipo:', adminAsg);
  // AU6: Solicitar asignación + aprobar / rechazar / cancelar + una sola pendiente.
  loginAs('u1', 'Test User', 'usuario');
  var pS6 = mkPrepAU({ id: 'au6', tecnicoUid: 'uAxel', tecnico: 'Axel Danyael' });
  state.preparations = [pS6];
  var up6 = [];
  global.Cloud.upsertPrep = async function (d) { up6.push(d); };
  var btnSol = cardHtml(pS6).indexOf('data-solicitar-asignacion="au6"') !== -1;
  realClick('data-solicitar-asignacion', 'au6');
  var solOk = !!pS6.solicitudAsignacion && pS6.solicitudAsignacion.deUid === 'u1' && pS6.solicitudAsignacion.deNombre === 'Test User' && pS6.solicitudAsignacion.estado === 'pendiente' && up6.length === 1;
  var cardS1 = cardHtml(pS6);
  var cancelShown = cardS1.indexOf('data-cancel-solicitud="au6"') !== -1 && cardS1.indexOf('data-solicitar-asignacion="au6"') === -1;
  var fecha1 = pS6.solicitudAsignacion.fecha;
  realClick('data-solicitar-asignacion', 'au6');
  var oneOnly = pS6.solicitudAsignacion.fecha === fecha1 && up6.length === 1;
  loginAs('uAle', 'Alejandro', 'usuario');
  var cardS2 = cardHtml(pS6);
  var pendingOther = cardS2.indexOf('Solicitud pendiente de Test User') !== -1 && cardS2.indexOf('data-solicitar-asignacion') === -1 && cardS2.indexOf('data-cancel-solicitud') === -1;
  realClick('data-solicitar-asignacion', 'au6');
  var stillOne = pS6.solicitudAsignacion.deUid === 'u1' && up6.length === 1;
  loginAs('uGer', 'Gerardo', 'admin');
  var cardS3 = cardHtml(pS6);
  var adminSol = cardS3.indexOf('data-aprobar-solicitud="au6"') !== -1 && cardS3.indexOf('data-rechazar-solicitud="au6"') !== -1;
  realClick('data-aprobar-solicitud', 'au6');
  var apprOk = pS6.tecnicoUid === 'u1' && pS6.tecnico === 'Test User' && !pS6.solicitudAsignacion && pS6.asignaciones.length === 1 && pS6.asignaciones[0].a === 'Test User';
  loginAs('uAle', 'Alejandro', 'usuario');
  realClick('data-solicitar-asignacion', 'au6');
  var sol2 = !!pS6.solicitudAsignacion && pS6.solicitudAsignacion.deUid === 'uAle';
  loginAs('uGer', 'Gerardo', 'admin');
  realClick('data-rechazar-solicitud', 'au6');
  var rejOk = !pS6.solicitudAsignacion && pS6.tecnicoUid === 'u1';
  loginAs('uAle', 'Alejandro', 'usuario');
  realClick('data-solicitar-asignacion', 'au6');
  realClick('data-cancel-solicitud', 'au6');
  var cancelOk = !pS6.solicitudAsignacion;
  var rt6 = prepFromCloud(prepToCloudDoc(pS6));
  var syncOk6 = rt6.tecnicoUid === 'u1' && rt6.asignaciones.length === 1 && rt6.asignaciones[0].a === 'Test User';
  var pS6b = mkPrepAU({ id: 'au6b', tecnicoUid: 'uAxel', tecnico: 'Axel Danyael', solicitudAsignacion: { deUid: 'u1', deNombre: 'Test User', fecha: 123, estado: 'pendiente' } });
  var rt6b = prepFromCloud(prepToCloudDoc(pS6b));
  var syncSol6 = !!rt6b.solicitudAsignacion && rt6b.solicitudAsignacion.deUid === 'u1' && rt6b.solicitudAsignacion.estado === 'pendiente';
  console.log('AU6) botón Solicitar en equipo ajeno:', btnSol, '| solicitud guardada en el equipo:', solOk, '| mía muestra Cancelar:', cancelShown, '| no se duplica:', oneOnly, '| otro ve de quién es sin botón:', pendingOther, '| otro no la pisa:', stillOne, '| admin ve Aprobar/Rechazar:', adminSol, '| aprobar transfiere y limpia:', apprOk, '| segunda solicitud:', sol2, '| rechazar limpia sin transferir:', rejOk, '| cancelar limpia:', cancelOk, '| sincroniza asignaciones:', syncOk6, '| sincroniza solicitud:', syncSol6);
  // AU7: crear equipo guarda tecnicoUid; equipos viejos sin tecnicoUid usan el nombre.
  loginAs('u1', 'Test User', 'usuario');
  CLOUD_ENABLED = true;
  var up7 = [];
  global.Cloud.upsertPrep = async function (d) { up7.push(d); };
  document.getElementById('fTipo').value = 'Laptop';
  document.getElementById('fMarca').value = 'Dell';
  document.getElementById('fModelo').value = 'Inspiron 3501';
  document.getElementById('fSerie').value = 'S1';
  document.getElementById('fInv').value = '100';
  document.getElementById('fUser').value = 'Ana';
  document.getElementById('fTec').value = 'Test User';
  document.getElementById('btnAdd')._h.click[0]();
  var created7 = state.preparations[state.preparations.length - 1];
  var addUid = !!created7 && created7.tecnicoUid === 'u1' && up7.length === 1 && up7[0].tecnicoUid === 'u1';
  var oldOwn = mkPrep({ id: 'au7old', tecnico: 'Test User' }); delete oldOwn.tecnicoUid;
  var oldForeign = mkPrep({ id: 'au7for', tecnico: 'Axel Danyael' }); delete oldForeign.tecnicoUid;
  var fbOk = isOwnPrep(oldOwn) === true && isOwnPrep(oldForeign) === false;
  var oldPart = mkPrep({ id: 'au7part', tecnico: 'Axel Danyael', reasignaciones: [{ de: 'Ana', a: 'Luis', fecha: Date.now(), analista: 'Test User' }] }); delete oldPart.tecnicoUid;
  var partOk = isOwnPrep(oldPart) === true;
  var nBefore7 = state.preparations.length;
  document.getElementById('fReEquipo').value = '__nuevo__'; document.getElementById('fReA').value = 'Luis'; document.getElementById('fReDe').value = 'Ana';
  document.getElementById('fReTipo').value = 'Laptop'; document.getElementById('fReMarca').value = 'Dell'; document.getElementById('fReModelo').value = 'Latitude'; document.getElementById('fReSerie').value = 'S9'; document.getElementById('fReInv').value = '999';
  document.getElementById('btnReGuardar')._h.click[0]();
  var re7 = state.preparations[state.preparations.length - 1];
  var reUidOk = state.preparations.length === nBefore7 + 1 && !!re7 && re7.tecnicoUid === 'u1';
  console.log('AU7) Nuevo equipo guarda tecnicoUid:', addUid, '| viejo por nombre propio:', fbOk, '| viejo con reasignación mía es propio:', partOk, '| reasignado nuevo guarda tecnicoUid:', reUidOk);
  // AU8: la cadena de prepId incluye los botones nuevos.
  var chainAU8 = ['data-asignar', 'data-save-asignar', 'data-solicitar-asignacion', 'data-cancel-solicitud', 'data-aprobar-solicitud', 'data-rechazar-solicitud'].every(function (a) { return SRC.indexOf("q('" + a + "')") !== -1; });
  var btnsAU8 = ['data-asignar', 'data-save-asignar', 'data-solicitar-asignacion', 'data-cancel-solicitud', 'data-aprobar-solicitud', 'data-rechazar-solicitud'].every(function (a) { return SRC.indexOf(a + '="') !== -1; });
  console.log('AU8) cadena prepId con botones nuevos:', chainAU8, '| botones en el código:', btnsAU8);
'''

with open(TEST_NEW, encoding='utf-8') as f:
    t = f.read()
anchor = '  process.exit(0);'
assert t.count(anchor) == 1, 'Ancla process.exit no única'
t = t.replace(anchor, AU + anchor, 1)
with open(TEST_NEW, 'w', encoding='utf-8') as f:
    f.write(t)
print('OK: serie AU añadida a test20237.js')

# ---------- 18. Extraer tests/checklist20237.js del index.html nuevo ----------
with open(HTML, encoding='utf-8') as f:
    lines = f.read().split('\n')
start = next(i for i, ln in enumerate(lines) if ln == '<script>')
end = next(i for i, ln in enumerate(lines) if ln == '</script>')
assert end > start, 'No se encontró el script inline'
with open(EXTRACT, 'w', encoding='utf-8') as f:
    f.write('\n' + '\n'.join(lines[start + 1:end]) + '\n')
print('OK: extraído tests/checklist20237.js (script inline, líneas %d-%d)' % (start + 2, end))

print('Parche 2.3.7 aplicado (firebase.js sin cambios: bundle NO reconstruido).')
