# Parche web 2.5.14: texto de invitación a llenar la responsiva, botón
# Archivar y «Ver responsivas anteriores».
# 1) Texto exacto «Por favor llena tus datos para crear tu responsiva»
# en TRES sitios: (a) subtítulo en la vista Responsiva, junto al botón
# «Enviar formulario en blanco»; (b) mensaje de WhatsApp del enlace en
# blanco (antes del enlace, sustituye el «Hola, llena tu responsiva…»);
# (c) encabezado de hosting/public/responsiva.html, antes de los 6
# campos. El texto de «Copiar enlace» NO se toca (no es el mensaje del
# enlace en blanco).
# 2) Botón «📥 Archivar» en cada tarjeta activa de «Responsivas
# enviadas» (pendiente y llenada): pide confirmación con showConfirm
# («¿Archivar esta responsiva? Podrás verla en Responsivas
# anteriores.») y llama a la nueva Cloud.archivarResponsiva(id, true).
# Archivar NO borra: solo marca archivado + archivadoEn.
# 3) Botón/toggle «📂 Ver responsivas anteriores» debajo de la lista
# principal: muestra la sección «Responsivas archivadas» con las
# tarjetas archivadas (mismos datos, estado y fecha de archivado) y un
# botón «↩️ Restaurar» por tarjeta (archivado=false, vuelve a la lista
# principal). Sin archivadas muestra «No hay responsivas archivadas».
# El toggle vive solo durante la sesión (variable, no se persiste).
# Las tarjetas archivadas viven en #respArchList con el MISMO dispatch
# delegado que #respList (respListClick registrado en ambas).
# 4) firebase.js: archivarResponsiva(id, archivado) con update/merge
# (archivado + archivadoEn; restaurar pone archivado=false y
# archivadoEn=null), expuesta en window.Cloud. firestore.rules NO se
# toca: la rama update propio/admin no restringe campos, así que
# archivar ya está permitido para el dueño y el admin.
# 5) Versión 2.5.14 / versionCode 68 en www/index.html (login y Acerca
# de, mailto 263 -> 264), android/app/build.gradle e iOS
# (MARKETING_VERSION 2.5.14 / CURRENT_PROJECT_VERSION 68, Debug y
# Release). El bundle de Firebase SÍ cambia esta vez: reconstruir con
# pnpm build:cloud + npx cap sync ANTES de compilar.
# Uso: python3 patch_20264_web.py [ruta-base-del-proyecto]
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '/home/hatch/workspace/android/checklist-cloud'
HTML = os.path.join(BASE, 'www/index.html')
FBJS = os.path.join(BASE, 'www/cloud/firebase.js')
RESP = os.path.join(BASE, 'hosting/public/responsiva.html')
GRADLE = os.path.join(BASE, 'android/app/build.gradle')
PBX = os.path.join(BASE, 'ios/App/App.xcodeproj/project.pbxproj')


def patch(path, pairs):
    s = open(path, encoding='utf-8').read()
    for old, new, n in pairs:
        c = s.count(old)
        assert c == n, '%s: NO ENCONTRADO x%d (esperado %d): %r' % (path, c, n, old[:120])
        s = s.replace(old, new)
    open(path, 'w', encoding='utf-8').write(s)
    return s


# --- www/index.html: versión y mailto.
patch(HTML, [
    ('<p class="login-sub" style="font-size:11px;color:#999">Versión 2.5.13</p>',
     '<p class="login-sub" style="font-size:11px;color:#999">Versión 2.5.14</p>', 1),
    ('<div class="line">Versión: 2.5.13</div>',
     '<div class="line">Versión: 2.5.14</div>', 1),
    ("encodeURIComponent('Reporte de problema - Checklist de Soporte 263')",
     "encodeURIComponent('Reporte de problema - Checklist de Soporte 264')", 1),
    ("encodeURIComponent('Describe el problema:\\n\\n\\nVersión de la app: 263')",
     "encodeURIComponent('Describe el problema:\\n\\n\\nVersión de la app: 264')", 1),
])

# --- www/index.html: texto de invitación junto al botón de enviar en
# blanco + toggle y sección de archivadas debajo de la lista principal.
patch(HTML, [
    ("""      <div class="share-note">El número de WhatsApp se guarda solo en este teléfono, no se manda a la nube. Si está vacío, al enviar se te pedirá elegir el contacto en WhatsApp.</div>
      <div class="actions">
        <button class="btn-green" id="btnRespEnviar">📲 Enviar por WhatsApp</button>
        <button class="btn-green" id="btnRespBlanco">📤 Enviar formulario en blanco</button>""",
     """      <div class="share-note">El número de WhatsApp se guarda solo en este teléfono, no se manda a la nube. Si está vacío, al enviar se te pedirá elegir el contacto en WhatsApp.</div>
      <div class="share-note">Por favor llena tus datos para crear tu responsiva</div>
      <div class="actions">
        <button class="btn-green" id="btnRespEnviar">📲 Enviar por WhatsApp</button>
        <button class="btn-green" id="btnRespBlanco">📤 Enviar formulario en blanco</button>""", 1),
    ("""      <div id="respList"><div class="empty">Aún no hay responsivas enviadas.</div></div>
    </div>
  </div>""",
     """      <div id="respList"><div class="empty">Aún no hay responsivas enviadas.</div></div>
    </div>
    <div class="panel">
      <button class="btn-ghost" id="btnRespVerAnt">📂 Ver responsivas anteriores</button>
      <div id="respArchBox" hidden>
        <b>Responsivas archivadas</b>
        <div class="share-note">Archivar no borra nada: la responsiva se puede restaurar a la lista principal.</div>
        <div id="respArchList"></div>
      </div>
    </div>
  </div>""", 1),
])

# --- www/index.html: texto de invitación en el mensaje de WhatsApp del
# enlace en blanco (antes del enlace).
patch(HTML, [
    ("""    window.open('https://wa.me/?text=' + encodeURIComponent('Hola, llena tu responsiva de Checklist de Soporte aquí: ' + url), '_blank');""",
     """    window.open('https://wa.me/?text=' + encodeURIComponent('Por favor llena tus datos para crear tu responsiva: ' + url), '_blank');""", 1),
])

# --- www/index.html: estado del toggle (solo sesión) + render con
# activas/archivadas + respCardHtml + respArchivar.
patch(HTML, [
    ("""var responsivas = [];
var cloudRespUnsub = null;""",
     """var responsivas = [];
var respMostrarArchivadas = false;
var cloudRespUnsub = null;""", 1),
    ("""function renderRespList() {
  var box = document.getElementById('respList');
  if (!box) return;
  if (!responsivas.length) { box.innerHTML = '<div class="empty">Aún no hay responsivas enviadas.</div>'; return; }
  var list = responsivas.slice().sort(function (a, b) { return (b.creadoEn || 0) - (a.creadoEn || 0); });
  box.innerHTML = list.map(function (r) {
    var llenada = r.estado === 'llenada' && r.datos;
    var html = '<div class="card"><b>Responsiva · ' + esc(respEstadoLabel(r)) + '</b>' +
      '<div class="sub">Creada por ' + esc(r.creadoPorNombre || '—') + (r.creadoEn ? ' · ' + fmtDate(r.creadoEn) : '') + '</div>';
    if (llenada) {
      html += '<div class="sub">' + RESP_CAMPOS.map(function (c) {
        return esc(c[1]) + ': ' + esc(r.datos[RESP_DATOS_KEYS[c[0]]] || '—');
      }).join('<br>') + '</div>';
      html += '<div class="actions"><button class="btn-green" data-resp-wa="' + esc(r.id) + '">📲 Compartir por WhatsApp</button>' +
        '<button class="btn-dark" data-resp-mail="' + esc(r.id) + '">✉️ Enviar por correo</button>' +
        '<button class="btn-dark" data-resp-xlsx="' + esc(r.id) + '">💾 Guardar en Excel</button></div>';
    } else {
      html += '<div class="sub">Pendiente de llenar por el colaborador.</div>' +
        '<div class="actions"><button class="btn-dark" data-resp-copy="' + esc(r.id) + '">🔗 Copiar enlace</button></div>';
    }
    return html + '</div>';
  }).join('');
}""",
     """// (264) Tarjeta de responsiva: la activa trae «📥 Archivar», la
// archivada trae «↩️ Restaurar» y la fecha de archivado. Mismos datos
// y estado en ambas.
function respCardHtml(r, archivada) {
  var llenada = r.estado === 'llenada' && r.datos;
  var html = '<div class="card"><b>Responsiva · ' + esc(respEstadoLabel(r)) + '</b>' +
    '<div class="sub">Creada por ' + esc(r.creadoPorNombre || '—') + (r.creadoEn ? ' · ' + fmtDate(r.creadoEn) : '') + '</div>';
  if (archivada) {
    html += '<div class="sub">Archivada' + (r.archivadoEn ? ' · ' + fmtDate(r.archivadoEn) : '') + '</div>';
  }
  var finBtn = archivada
    ? '<button class="btn-ghost" data-resp-restaurar="' + esc(r.id) + '">↩️ Restaurar</button>'
    : '<button class="btn-ghost" data-resp-archivar="' + esc(r.id) + '">📥 Archivar</button>';
  if (llenada) {
    html += '<div class="sub">' + RESP_CAMPOS.map(function (c) {
      return esc(c[1]) + ': ' + esc(r.datos[RESP_DATOS_KEYS[c[0]]] || '—');
    }).join('<br>') + '</div>';
    html += '<div class="actions"><button class="btn-green" data-resp-wa="' + esc(r.id) + '">📲 Compartir por WhatsApp</button>' +
      '<button class="btn-dark" data-resp-mail="' + esc(r.id) + '">✉️ Enviar por correo</button>' +
      '<button class="btn-dark" data-resp-xlsx="' + esc(r.id) + '">💾 Guardar en Excel</button>' + finBtn + '</div>';
  } else {
    html += '<div class="sub">Pendiente de llenar por el colaborador.</div>' +
      '<div class="actions"><button class="btn-dark" data-resp-copy="' + esc(r.id) + '">🔗 Copiar enlace</button>' + finBtn + '</div>';
  }
  return html + '</div>';
}
function renderRespList() {
  var box = document.getElementById('respList');
  if (!box) return;
  var activas = responsivas.filter(function (r) { return !r.archivado; });
  var archivadas = responsivas.filter(function (r) { return !!r.archivado; });
  if (!activas.length) { box.innerHTML = '<div class="empty">Aún no hay responsivas enviadas.</div>'; }
  else {
    var list = activas.slice().sort(function (a, b) { return (b.creadoEn || 0) - (a.creadoEn || 0); });
    box.innerHTML = list.map(function (r) { return respCardHtml(r, false); }).join('');
  }
  var archBox = document.getElementById('respArchBox');
  var archList = document.getElementById('respArchList');
  if (archBox) archBox.hidden = !respMostrarArchivadas;
  if (archList) {
    if (!respMostrarArchivadas) { archList.innerHTML = ''; }
    else if (!archivadas.length) { archList.innerHTML = '<div class="empty">No hay responsivas archivadas.</div>'; }
    else {
      var alist = archivadas.slice().sort(function (a, b) { return (b.archivadoEn || b.creadoEn || 0) - (a.archivadoEn || a.creadoEn || 0); });
      archList.innerHTML = alist.map(function (r) { return respCardHtml(r, true); }).join('');
    }
  }
}
function respArchivar(id, archivado) {
  if (!CLOUD_ENABLED || !window.Cloud || !window.Cloud.archivarResponsiva) {
    showToast('Archivar necesita conexión a la nube.');
    return Promise.resolve(false);
  }
  return Promise.resolve(window.Cloud.archivarResponsiva(id, archivado)).then(function () {
    showToast(archivado ? 'Responsiva archivada.' : 'Responsiva restaurada.');
    return true;
  }).catch(function () {
    showToast(archivado ? 'No se pudo archivar la responsiva. Revisa tu conexión.' : 'No se pudo restaurar la responsiva. Revisa tu conexión.');
    return false;
  });
}""", 1),
])

# --- www/index.html: dispatch delegado compartido por #respList y
# #respArchList (archivar con confirmación, restaurar directo) +
# toggle «Ver responsivas anteriores».
patch(HTML, [
    ("""document.getElementById('respList').addEventListener('click', function (e) {
  var t = e.target;
  var q = function (attr) { var el = t.closest('[' + attr + ']'); return el ? el.getAttribute(attr) : null; };
  var id = q('data-resp-wa') || q('data-resp-mail') || q('data-resp-xlsx') || q('data-resp-copy');
  if (!id) return;
  var r = null;
  responsivas.forEach(function (x) { if (x.id === id) r = x; });
  if (!r) return;
  if (t.closest('[data-resp-wa]')) { shareText(respDatosTexto(r)); return; }
  if (t.closest('[data-resp-mail]')) { respEnviarCorreo(r); return; }
  if (t.closest('[data-resp-xlsx]')) { respGuardarExcel(r); return; }
  if (t.closest('[data-resp-copy]')) { respCopiarEnlace(r); return; }
});""",
     """function respListClick(e) {
  var t = e.target;
  var q = function (attr) { var el = t.closest('[' + attr + ']'); return el ? el.getAttribute(attr) : null; };
  var id = q('data-resp-wa') || q('data-resp-mail') || q('data-resp-xlsx') || q('data-resp-copy') || q('data-resp-archivar') || q('data-resp-restaurar');
  if (!id) return;
  var r = null;
  responsivas.forEach(function (x) { if (x.id === id) r = x; });
  if (!r) return;
  if (t.closest('[data-resp-wa]')) { shareText(respDatosTexto(r)); return; }
  if (t.closest('[data-resp-mail]')) { respEnviarCorreo(r); return; }
  if (t.closest('[data-resp-xlsx]')) { respGuardarExcel(r); return; }
  if (t.closest('[data-resp-copy]')) { respCopiarEnlace(r); return; }
  if (t.closest('[data-resp-archivar]')) {
    showConfirm('¿Archivar esta responsiva? Podrás verla en Responsivas anteriores.').then(function (ok) {
      if (!ok) return;
      respArchivar(id, true);
    });
    return;
  }
  if (t.closest('[data-resp-restaurar]')) { respArchivar(id, false); return; }
}
document.getElementById('respList').addEventListener('click', respListClick);
document.getElementById('respArchList').addEventListener('click', respListClick);
document.getElementById('btnRespVerAnt').addEventListener('click', function () {
  respMostrarArchivadas = !respMostrarArchivadas;
  renderRespList();
});""", 1),
])

# --- www/cloud/firebase.js: archivarResponsiva + export.
patch(FBJS, [
    ("""function subscribeResponsivas(cb, uidOpcional) {
  const q = uidOpcional
    ? query(collection(db, 'responsivas'), where('creadoPor', '==', uidOpcional))
    : collection(db, 'responsivas');
  return onSnapshot(
    q,
    (snap) => cb(snap.docs.map((d) => Object.assign({ id: d.id }, d.data()))),
    (err) => console.warn('[Cloud] Error en snapshot de responsivas:', err)
  );
}""",
     """function subscribeResponsivas(cb, uidOpcional) {
  const q = uidOpcional
    ? query(collection(db, 'responsivas'), where('creadoPor', '==', uidOpcional))
    : collection(db, 'responsivas');
  return onSnapshot(
    q,
    (snap) => cb(snap.docs.map((d) => Object.assign({ id: d.id }, d.data()))),
    (err) => console.warn('[Cloud] Error en snapshot de responsivas:', err)
  );
}

// Archivar responsivas (2.5.14): archivar NO borra nada; solo marca
// archivado + archivadoEn (restaurar pone archivado=false y
// archivadoEn=null). Las reglas ya lo permiten: la rama update
// propio/admin no restringe campos, así que firestore.rules NO se
// toca. La suscripción devuelve los docs y el filtrado es en la app.
async function archivarResponsiva(id, archivado) {
  return updateDoc(doc(db, 'responsivas', id), archivado
    ? { archivado: true, archivadoEn: Date.now() }
    : { archivado: false, archivadoEn: null });
}""", 1),
    ("""  crearResponsiva,
  subscribeResponsivas,""",
     """  crearResponsiva,
  subscribeResponsivas,
  archivarResponsiva,""", 1),
])

# --- hosting/public/responsiva.html: encabezado con el texto exacto.
patch(RESP, [
    ('    <p>Llena tus datos para la responsiva del equipo.</p>',
     '    <p>Por favor llena tus datos para crear tu responsiva</p>', 1),
])

# --- android/app/build.gradle: versionCode 68 / versionName 2.5.14.
patch(GRADLE, [
    ('        versionCode 67\n', '        versionCode 68\n', 1),
    ('        versionName "2.5.13"\n', '        versionName "2.5.14"\n', 1),
])

# --- iOS: MARKETING_VERSION 2.5.14 / CURRENT_PROJECT_VERSION 68 (Debug y Release).
patch(PBX, [
    ('MARKETING_VERSION = 2.5.13;', 'MARKETING_VERSION = 2.5.14;', 2),
    ('CURRENT_PROJECT_VERSION = 67;', 'CURRENT_PROJECT_VERSION = 68;', 2),
])

print('parche 2.5.14 aplicado')
