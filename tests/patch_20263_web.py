# Parche web 2.5.13: Responsiva en blanco por WhatsApp (mismo patrón que
# la firma de Mantenimientos, firma.html).
# 1) firebase.js: crearResponsiva() (doc en 'responsivas', estado
# 'pendiente', sin datos, creadoPor = uid actual) y
# subscribeResponsivas(cb, uidOpcional) (admin ve todas, usuario normal
# solo las que creó, mismo patrón que subscribeMantenimientos); ambas en
# window.Cloud. 2) firestore.rules: bloque nuevo 'responsivas' (list
# propio/admin, get público por id, create propio con estado
# 'pendiente', update propio/admin O público restringido a
# datos+estado+llenadoEn con estado 'llenada' y los 6 campos no vacíos,
# delete propio/admin). SOLO se añade ese bloque; el resto no se toca.
# NO se publica: lo publica mi padre desde la consola de Firebase.
# 3) www/index.html: botón nuevo «📤 Enviar formulario en blanco»
# (#btnRespBlanco) que crea la responsiva y abre wa.me/?text= con el
# enlace responsiva.html?id=<id> para elegir contacto; sección nueva
# «Responsivas enviadas» (#respList) suscrita en vivo: tarjeta pendiente
# con «🔗 Copiar enlace», tarjeta llenada con los 6 datos y botones
# «📲 Compartir por WhatsApp», «✉️ Enviar por correo» (mailto
# «Responsiva: <nombre>») y «💾 Guardar en Excel» (.xlsx real con el
# patrón buildXlsxFromTable; Capacitor Share si está, si no descarga
# por <a>, si no toast honesto). El formulario directo del técnico
# (2.5.11/2.5.12) NO se toca. Los botones por tarjeta van por dispatch
# delegado en #respList (lección 2.2.1). 4) Versión 2.5.13 /
# versionCode 67 en www/index.html (login y Acerca de, mailto 262 ->
# 263), android/app/build.gradle e iOS (MARKETING_VERSION 2.5.13 /
# CURRENT_PROJECT_VERSION 67, Debug y Release). El bundle de Firebase
# SÍ cambia esta vez: reconstruir con pnpm build:cloud + npx cap sync
# ANTES de compilar.
# Uso: python3 patch_20263_web.py [ruta-base-del-proyecto]
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '/home/hatch/workspace/android/checklist-cloud'
HTML = os.path.join(BASE, 'www/index.html')
FBJS = os.path.join(BASE, 'www/cloud/firebase.js')
RULES = os.path.join(BASE, 'firestore.rules')
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
    ('<p class="login-sub" style="font-size:11px;color:#999">Versión 2.5.12</p>',
     '<p class="login-sub" style="font-size:11px;color:#999">Versión 2.5.13</p>', 1),
    ('<div class="line">Versión: 2.5.12</div>',
     '<div class="line">Versión: 2.5.13</div>', 1),
    ("encodeURIComponent('Reporte de problema - Checklist de Soporte 262')",
     "encodeURIComponent('Reporte de problema - Checklist de Soporte 263')", 1),
    ("encodeURIComponent('Describe el problema:\\n\\n\\nVersión de la app: 262')",
     "encodeURIComponent('Describe el problema:\\n\\n\\nVersión de la app: 263')", 1),
])

# --- www/index.html: botón «Enviar formulario en blanco» + sección
# «Responsivas enviadas» (#respList) en #viewResp.
patch(HTML, [
    ("""        <button class="btn-green" id="btnRespEnviar">📲 Enviar por WhatsApp</button>
        <button class="btn-ghost" id="btnRespGuardar">💾 Guardar y cerrar</button>
        <button class="btn-ghost" id="btnRespLimpiar">Limpiar</button>
      </div>
    </div>
  </div>""",
     """        <button class="btn-green" id="btnRespEnviar">📲 Enviar por WhatsApp</button>
        <button class="btn-green" id="btnRespBlanco">📤 Enviar formulario en blanco</button>
        <button class="btn-ghost" id="btnRespGuardar">💾 Guardar y cerrar</button>
        <button class="btn-ghost" id="btnRespLimpiar">Limpiar</button>
      </div>
    </div>
    <div class="panel">
      <b>Responsivas enviadas</b>
      <div class="share-note">Las responsivas en blanco que enviaste por WhatsApp. Cuando el colaborador llena el formulario en la página, aparece aquí como «Llenada» con sus datos; no hace falta recargar.</div>
      <div id="respList"><div class="empty">Aún no hay responsivas enviadas.</div></div>
    </div>
  </div>""", 1),
])

# --- www/index.html: suscripción en vivo al entrar con sesión (mismo
# sitio que mantenimientos) y al entrar a la vista.
patch(HTML, [
    ("""      }, cloudRole === 'admin' ? null : (cloudUser ? cloudUser.uid : null));
    }
    if (window.Cloud.subscribeUserDoc) {""",
     """      }, cloudRole === 'admin' ? null : (cloudUser ? cloudUser.uid : null));
    }
    if (window.Cloud.subscribeResponsivas) {
      if (cloudRespUnsub) cloudRespUnsub();
      cloudRespUnsub = window.Cloud.subscribeResponsivas(function (docs) {
        responsivas = docs || [];
        renderRespList();
      }, cloudRole === 'admin' ? null : (cloudUser ? cloudUser.uid : null));
    }
    if (window.Cloud.subscribeUserDoc) {""", 1),
    ("  if (v === 'resp') { respCargarWa(); respCargarBorrador(); }",
     "  if (v === 'resp') { respCargarWa(); respCargarBorrador(); respSuscribir(); renderRespList(); }", 1),
])

# --- www/index.html: funciones de la responsiva en blanco (263), tras
# respLimpiar y antes del listener del número de WhatsApp.
patch(HTML, [
    ("""function respLimpiar() {
  respBorrarBorrador();
  RESP_CAMPOS.forEach(function (c) {
    var el = document.getElementById(c[0]);
    if (el) { el.value = ''; el.classList.remove('campo-falta'); }
  });
}""",
     """function respLimpiar() {
  respBorrarBorrador();
  RESP_CAMPOS.forEach(function (c) {
    var el = document.getElementById(c[0]);
    if (el) { el.value = ''; el.classList.remove('campo-falta'); }
  });
}
// (263) Responsivas en blanco por WhatsApp: mismo patrón que la firma
// de Mantenimientos (firma.html). Se crea el documento en Firestore
// (estado 'pendiente', sin datos) y se comparte el enlace público
// responsiva.html?id=<id> para elegir el contacto en WhatsApp; el
// colaborador lo llena en la página web y la lista se actualiza sola
// por la suscripción. Nada de borrador local para esto: el documento
// vive en la nube desde que se crea.
var RESP_URL_BASE = 'https://checklist-soporte.web.app/responsiva.html';
var responsivas = [];
var cloudRespUnsub = null;
var RESP_DATOS_KEYS = {
  'fResp-nombre': 'nombre',
  'fResp-colaborador': 'colaborador',
  'fResp-sucursal': 'sucursal',
  'fResp-puesto': 'puesto',
  'fResp-jefe': 'jefe',
  'fResp-area': 'area'
};
function respUrl(r) { return RESP_URL_BASE + '?id=' + encodeURIComponent(r.id); }
function respDatosTexto(r) {
  var d = (r && r.datos) || {};
  var lines = ['Responsiva — Checklist de Soporte'];
  RESP_CAMPOS.forEach(function (c) {
    lines.push(c[1] + ': ' + (d[RESP_DATOS_KEYS[c[0]]] || ''));
  });
  return lines.join('\\n');
}
function respSuscribir() {
  if (!CLOUD_ENABLED || !window.Cloud || !window.Cloud.subscribeResponsivas) return;
  if (cloudRespUnsub) return;
  cloudRespUnsub = window.Cloud.subscribeResponsivas(function (docs) {
    responsivas = docs || [];
    renderRespList();
  }, cloudRole === 'admin' ? null : (cloudUser ? cloudUser.uid : null));
}
function respEnviarEnBlanco() {
  if (!CLOUD_ENABLED || !window.Cloud || !window.Cloud.crearResponsiva) {
    showToast('La responsiva en blanco necesita conexión a la nube.');
    return Promise.resolve(false);
  }
  return Promise.resolve(window.Cloud.crearResponsiva(technicianName())).then(function (id) {
    if (!id) { showToast('No se pudo crear la responsiva.'); return false; }
    var url = RESP_URL_BASE + '?id=' + encodeURIComponent(id);
    window.open('https://wa.me/?text=' + encodeURIComponent('Hola, llena tu responsiva de Checklist de Soporte aquí: ' + url), '_blank');
    showToast('Responsiva creada, elige el contacto en WhatsApp.');
    return true;
  }).catch(function () {
    showToast('No se pudo crear la responsiva. Revisa tu conexión.');
    return false;
  });
}
function respEstadoLabel(r) {
  if (r.estado === 'llenada') return 'Llenada' + (r.llenadoEn ? ' · ' + fmtDate(r.llenadoEn) : '');
  return 'Pendiente';
}
function renderRespList() {
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
}
function respEnviarCorreo(r) {
  var d = (r && r.datos) || {};
  window.location.href = 'mailto:?subject=' + encodeURIComponent('Responsiva: ' + (d.nombre || '')) + '&body=' + encodeURIComponent(respDatosTexto(r));
}
function respCopiarEnlace(r) {
  var url = respUrl(r);
  var texto = 'Llena tu responsiva de Checklist de Soporte aquí: ' + url;
  try {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      Promise.resolve(navigator.clipboard.writeText(url)).then(function () {
        showToast('Enlace copiado.');
      }).catch(function () {
        window.open('https://wa.me/?text=' + encodeURIComponent(texto), '_blank');
      });
      return;
    }
  } catch (e) {}
  window.open('https://wa.me/?text=' + encodeURIComponent(texto), '_blank');
}
// Excel real (.xlsx) de una responsiva llenada, con el mismo patrón
// buildXlsxFromTable que el resto de la app: Capacitor Share si está,
// si no descarga por <a>, si no toast honesto.
function respXlsxBlob(r) {
  var d = (r && r.datos) || {};
  var headers = ['Nombre Completo', 'Número de colaborador', 'Sucursal', 'Puesto', 'Jefe Directo', 'Área'];
  var row = [d.nombre || '', d.colaborador || '', d.sucursal || '', d.puesto || '', d.jefe || '', d.area || ''];
  return buildXlsxFromTable(headers, [row], 'Responsiva');
}
async function respGuardarExcel(r) {
  var d = (r && r.datos) || {};
  var name = 'responsiva-' + (cleanName(d.nombre) || 'colaborador') + '.xlsx';
  var blob = respXlsxBlob(r);
  try {
    var Plugins = window.Capacitor && window.Capacitor.Plugins;
    if (!Plugins || !Plugins.Filesystem || !Plugins.Share) throw new Error('share-no-disponible');
    var base64 = await blobToBase64(blob);
    var saved = await Plugins.Filesystem.writeFile({ path: name, data: base64, directory: 'CACHE' });
    await Plugins.Share.share({
      title: 'Checklist de Soporte',
      text: 'Responsiva — Checklist de Soporte.',
      url: saved.uri,
      dialogTitle: 'Guardar en Excel'
    });
  } catch (e) {
    try {
      var a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = name;
      a.click();
      showToast('Excel descargado: ' + name);
    } catch (e2) { showToast('No se pudo guardar el Excel.'); }
  }
}""", 1),
])

# --- www/index.html: cablear el botón de enviar en blanco y el dispatch
# delegado de la lista (lección 2.2.1: sin dispatch, los botones por
# tarjeta nunca disparan).
patch(HTML, [
    ("""document.getElementById('btnRespEnviar').addEventListener('click', function () { respEnviar(); });""",
     """document.getElementById('btnRespEnviar').addEventListener('click', function () { respEnviar(); });
document.getElementById('btnRespBlanco').addEventListener('click', function () { respEnviarEnBlanco(); });
document.getElementById('respList').addEventListener('click', function (e) {
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
});""", 1),
])

# --- www/cloud/firebase.js: crearResponsiva + subscribeResponsivas.
patch(FBJS, [
    ("""// Firma del usuario desde la página pública de firma (2.5.0): guarda la
// firma y marca la orden como firmada. Las reglas solo permiten cambiar
// 'firma' y 'estado' (a 'firmada') sin sesión de técnico.
async function guardarFirma(id, firmaData) {
  return updateDoc(doc(db, 'mantenimientos', id), { firma: firmaData, estado: 'firmada' });
}""",
     """// Firma del usuario desde la página pública de firma (2.5.0): guarda la
// firma y marca la orden como firmada. Las reglas solo permiten cambiar
// 'firma' y 'estado' (a 'firmada') sin sesión de técnico.
async function guardarFirma(id, firmaData) {
  return updateDoc(doc(db, 'mantenimientos', id), { firma: firmaData, estado: 'firmada' });
}

// Responsivas en blanco (2.5.13): el técnico crea el documento (estado
// 'pendiente', sin datos) y comparte el enlace público
// responsiva.html?id=<id>; el colaborador lo llena sin sesión y la app
// lo ve llegar por la suscripción. El id aleatorio del documento es el
// secreto del enlace, igual que la firma de Mantenimientos.
// uidOpcional filtra por creadoPor (lo usan los usuarios normales para
// que las reglas permitan la lectura); sin él el admin suscribe todo.
async function crearResponsiva(creadoPorNombre) {
  const u = auth.currentUser;
  if (!u) throw new Error('no-auth');
  const ref = doc(collection(db, 'responsivas'));
  await setDoc(ref, {
    creadoPor: u.uid,
    creadoPorNombre: creadoPorNombre || u.email || '',
    creadoEn: Date.now(),
    estado: 'pendiente',
    datos: null
  });
  return ref.id;
}

function subscribeResponsivas(cb, uidOpcional) {
  const q = uidOpcional
    ? query(collection(db, 'responsivas'), where('creadoPor', '==', uidOpcional))
    : collection(db, 'responsivas');
  return onSnapshot(
    q,
    (snap) => cb(snap.docs.map((d) => Object.assign({ id: d.id }, d.data()))),
    (err) => console.warn('[Cloud] Error en snapshot de responsivas:', err)
  );
}""", 1),
    ("""  asignarFolio,
  guardarFirma,""",
     """  asignarFolio,
  guardarFirma,
  crearResponsiva,
  subscribeResponsivas,""", 1),
])

# --- firestore.rules: bloque nuevo 'responsivas' (SOLO este bloque).
patch(RULES, [
    ("""    // Folios de órdenes de servicio (2.5.0): config/folios.siguiente es el""",
     """    // Responsivas (2.5.13): el técnico envía el formulario en blanco
    // por WhatsApp y el colaborador lo llena en responsiva.html (sin
    // sesión). Un usuario normal solo ve las que creó (creadoPor
    // propio); el admin ve todas. La lectura por id es pública para
    // que la página (sin sesión) pueda mostrar el formulario: el id
    // del documento es el secreto — cualquiera que lo conozca puede
    // leer esa responsiva y llenarla. Crear: usuario activo con su
    // propio creadoPor y estado 'pendiente'. Actualizar: admin o
    // propio, o el llenado público que solo toca 'datos', 'estado' (a
    // 'llenada') y 'llenadoEn', con los 6 campos de datos no vacíos.
    // Borrar: admin o propio.
    match /responsivas/{id} {
      allow list: if isActive() && (isAdmin() || resource.data.creadoPor == request.auth.uid);
      allow get: if true;
      allow create: if isActive() && request.resource.data.creadoPor == request.auth.uid
        && request.resource.data.estado == 'pendiente';
      allow update: if (isActive() && (isAdmin() || resource.data.creadoPor == request.auth.uid))
        || (request.resource.data.diff(resource.data).changedKeys().hasOnly(['datos', 'estado', 'llenadoEn'])
          && request.resource.data.estado == 'llenada'
          && request.resource.data.datos.nombre is string && request.resource.data.datos.nombre.size() > 0
          && request.resource.data.datos.colaborador is string && request.resource.data.datos.colaborador.size() > 0
          && request.resource.data.datos.sucursal is string && request.resource.data.datos.sucursal.size() > 0
          && request.resource.data.datos.puesto is string && request.resource.data.datos.puesto.size() > 0
          && request.resource.data.datos.jefe is string && request.resource.data.datos.jefe.size() > 0
          && request.resource.data.datos.area is string && request.resource.data.datos.area.size() > 0);
      allow delete: if isActive() && (isAdmin() || resource.data.creadoPor == request.auth.uid);
    }

    // Folios de órdenes de servicio (2.5.0): config/folios.siguiente es el""", 1),
])

# --- android/app/build.gradle: versionCode 67 / versionName 2.5.13.
patch(GRADLE, [
    ('        versionCode 66\n', '        versionCode 67\n', 1),
    ('        versionName "2.5.12"\n', '        versionName "2.5.13"\n', 1),
])

# --- iOS: MARKETING_VERSION 2.5.13 / CURRENT_PROJECT_VERSION 67 (Debug y Release).
patch(PBX, [
    ('MARKETING_VERSION = 2.5.12;', 'MARKETING_VERSION = 2.5.13;', 2),
    ('CURRENT_PROJECT_VERSION = 66;', 'CURRENT_PROJECT_VERSION = 67;', 2),
])

print('parche 2.5.13 aplicado')
