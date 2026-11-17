#!/usr/bin/env python3
"""Parche 2.0.19b: vista Equipo — quién está en línea + chat interno."""
import re
P = '/home/hatch/workspace/android/checklist-cloud/www/index.html'
s = open(P).read()
orig = s

def rep(old, new, n=1):
    global s
    assert old in s, 'NO ENCONTRADO: ' + old[:90]
    s = s.replace(old, new, n)

# 1. Version visible
rep('Versión 2.0.18', 'Versión 2.0.19')
rep('Versión: 2.0.18', 'Versión: 2.0.19')
rep("Checklist de Soporte 2.0.18", "Checklist de Soporte 2.0.19")
rep('Versión de la app: 2.0.18', 'Versión de la app: 2.0.19')

# 2. CSS: punto de en línea, filas de usuario, caja de chat
rep("  .todo-row { background: #fff; border: 1px solid #e3e3e3; border-radius: 10px; padding: 10px 12px; margin-top: 8px; font-size: 14px; cursor: pointer; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }",
    "  .todo-row { background: #fff; border: 1px solid #e3e3e3; border-radius: 10px; padding: 10px 12px; margin-top: 8px; font-size: 14px; cursor: pointer; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }\n  .dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: #bbb; margin-right: 8px; flex: none; }\n  .dot.on { background: #73BA25; box-shadow: 0 0 0 3px rgba(115,186,37,.2); }\n  .user-row { display: flex; align-items: center; background: #fff; border: 1px solid #e3e3e3; border-radius: 10px; padding: 10px 12px; margin-top: 8px; font-size: 14px; }\n  .user-row .who { flex: 1; min-width: 0; }\n  .user-row .st { color: #888; font-size: 12px; white-space: nowrap; }\n  .chat-box { background: #fff; border: 1px solid #e3e3e3; border-radius: 12px; padding: 10px; margin-top: 8px; max-height: 320px; overflow-y: auto; }\n  .msg { margin-bottom: 10px; }\n  .msg .meta { font-size: 12px; color: #888; }\n  .msg .txt { font-size: 14px; word-wrap: break-word; }\n  .msg.mine .txt { background: #e8f3df; border-radius: 10px; padding: 6px 9px; display: inline-block; }")

# 3. Pestaña Equipo (para todos los usuarios)
rep("""    <button class="tab" data-v="usuarios" id="tabUsuarios" hidden>👥 Usuarios</button>""",
"""    <button class="tab" data-v="usuarios" id="tabUsuarios" hidden>👥 Usuarios</button>
    <button class="tab" data-v="equipo" id="tabEquipo">💬 Equipo</button>""")

# 4. Vista Equipo antes de </main>
rep("""    <div id="userList"></div>
  </div></main>""",
"""    <div id="userList"></div>
  </div>
  <div id="viewEquipo" hidden>
    <div class="card">
      <b>Equipo</b>
      <div class="share-note">Quién está en línea ahora y el chat interno del equipo. Los mensajes los ven todos los usuarios activos.</div>
    </div>
    <div class="sub"><b>En línea ahora</b></div>
    <div id="onlineList"><div class="empty">Cargando…</div></div>
    <div class="sub" style="margin-top:14px"><b>Chat del equipo</b></div>
    <div class="chat-box" id="chatBox"><div class="empty">Aún no hay mensajes.</div></div>
    <div class="row" style="margin-top:8px">
      <input id="chatInput" type="text" placeholder="Escribe un mensaje…" maxlength="500" style="flex:1">
      <button class="btn-dark" id="btnChatSend">Enviar</button>
    </div>
  </div></main>""")

# 5. fmtTime junto a fmtDate
rep("""function fmtDate(ts) {
  var d = new Date(ts);
  return d.toLocaleDateString('es-MX', { day: '2-digit', month: 'short', year: 'numeric' }) +
    ' ' + d.toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' });
}""",
"""function fmtDate(ts) {
  var d = new Date(ts);
  return d.toLocaleDateString('es-MX', { day: '2-digit', month: 'short', year: 'numeric' }) +
    ' ' + d.toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' });
}
function fmtTime(ts) {
  return new Date(ts).toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' });
}
function timeAgo(ms) {
  if (!ms) return 'sin registro';
  var d = Date.now() - ms;
  if (d < 60 * 1000) return 'hace un momento';
  if (d < 60 * 60 * 1000) return 'hace ' + Math.floor(d / 60000) + ' min';
  if (d < 24 * 60 * 60 * 1000) return 'hace ' + Math.floor(d / 3600000) + ' h';
  return fmtDate(ms);
}""")

# 6. Estado y funciones de Equipo, antes del menú de vistas
rep("""// Menu de 3 secciones.
function showVista(v) {""",
"""// Equipo: quién está en línea + chat interno.
var presenceList = [];
var chatMessages = [];
var teamUsers = [];
var presenceUnsub = null, chatUnsub = null, heartbeatTimer = null;
var ONLINE_MS = 3 * 60 * 1000;
var HEARTBEAT_MS = 120 * 1000;

function tsMs(ts) {
  if (!ts) return 0;
  if (typeof ts.toMillis === 'function') return ts.toMillis();
  if (typeof ts === 'number') return ts;
  if (ts.seconds) return ts.seconds * 1000;
  return 0;
}
function renderEquipo() {
  var box = document.getElementById('onlineList');
  var now = Date.now();
  var online = [], offline = [];
  function pushUser(u, pr) {
    var ms = pr ? tsMs(pr.lastSeen) : 0;
    var isOn = !!ms && (now - ms) <= ONLINE_MS;
    (isOn ? online : offline).push({ u: u, ms: ms, isOn: isOn });
  }
  teamUsers.forEach(function (u) {
    var pr = null;
    presenceList.forEach(function (p) { if (p.uid === u.uid || p.id === u.uid) pr = p; });
    pushUser(u, pr);
  });
  presenceList.forEach(function (p) {
    var seen = teamUsers.some(function (u) { return u.uid === p.uid || u.uid === p.id; });
    if (!seen) pushUser({ uid: p.uid || p.id, nombre: p.nombre || p.uid, rol: p.rol || 'usuario' }, p);
  });
  function row(x) {
    return '<div class="user-row"><span class="dot' + (x.isOn ? ' on' : '') + '"></span><span class="who"><b>' + esc(x.u.nombre || x.u.email || 'Usuario') + '</b>' + (x.u.rol === 'admin' ? ' · Administrador' : '') + (cloudUser && x.u.uid === cloudUser.uid ? ' (tú)' : '') + '</span><span class="st">' + (x.isOn ? 'en línea' : timeAgo(x.ms)) + '</span></div>';
  }
  var html = '';
  if (online.length) html += '<div class="sub">En línea (' + online.length + ')</div>' + online.map(row).join('');
  if (offline.length) html += '<div class="sub" style="margin-top:10px">Sin conexión</div>' + offline.map(row).join('');
  if (!online.length && !offline.length) html = '<div class="empty">No hay usuarios todavía.</div>';
  box.innerHTML = html;
  var cb = document.getElementById('chatBox');
  if (!chatMessages.length) { cb.innerHTML = '<div class="empty">Aún no hay mensajes.</div>'; }
  else {
    cb.innerHTML = chatMessages.map(function (m) {
      var mine = cloudUser && m.uid === cloudUser.uid;
      var ms = tsMs(m.createdAt);
      return '<div class="msg' + (mine ? ' mine' : '') + '"><div class="meta">' + esc(m.nombre || 'Usuario') + ' · ' + (ms ? fmtTime(ms) : 'enviando…') + '</div><div class="txt">' + esc(m.texto || '') + '</div></div>';
    }).join('');
    cb.scrollTop = cb.scrollHeight;
  }
}
function refreshTeamUsers() {
  if (!window.Cloud || !CLOUD_ENABLED) return;
  window.Cloud.listUsers().then(function (us) { teamUsers = us || []; renderEquipo(); }).catch(function () {});
}
function startEquipo() {
  if (!window.Cloud || !CLOUD_ENABLED || !cloudUser) return;
  stopEquipo();
  var beat = function () { window.Cloud.heartbeat(technicianName(), cloudRole || 'usuario'); };
  beat();
  heartbeatTimer = setInterval(beat, HEARTBEAT_MS);
  presenceUnsub = window.Cloud.subscribePresence(function (docs) { presenceList = docs; if (!document.getElementById('viewEquipo').hidden) renderEquipo(); });
  chatUnsub = window.Cloud.subscribeChat(function (docs) { chatMessages = docs; if (!document.getElementById('viewEquipo').hidden) renderEquipo(); });
  refreshTeamUsers();
}
function stopEquipo() {
  if (heartbeatTimer) { clearInterval(heartbeatTimer); heartbeatTimer = null; }
  if (presenceUnsub) { presenceUnsub(); presenceUnsub = null; }
  if (chatUnsub) { chatUnsub(); chatUnsub = null; }
  if (window.Cloud) window.Cloud.clearPresence();
}
function sendChatMsg() {
  if (!window.Cloud || !CLOUD_ENABLED) { alert('El chat necesita conexión a la nube.'); return; }
  var inp = document.getElementById('chatInput');
  var t = inp.value.trim();
  if (!t) return;
  inp.value = '';
  window.Cloud.sendChat(t, technicianName()).catch(function () { alert('No se pudo enviar el mensaje. Revisa tu conexión.'); });
}
document.getElementById('btnChatSend').addEventListener('click', sendChatMsg);
document.getElementById('chatInput').addEventListener('keydown', function (e) { if (e.key === 'Enter') sendChatMsg(); });

// Menu de 3 secciones.
function showVista(v) {""")

# 7. showVista: vista equipo
rep("""  document.getElementById('viewUsuarios').hidden = v !== 'usuarios';
  document.getElementById('viewCuenta').hidden = true;
  document.getElementById('viewBio').hidden = true;
  if (v === 'usuarios') renderUsuarios();""",
"""  document.getElementById('viewUsuarios').hidden = v !== 'usuarios';
  document.getElementById('viewEquipo').hidden = v !== 'equipo';
  document.getElementById('viewCuenta').hidden = true;
  document.getElementById('viewBio').hidden = true;
  if (v === 'usuarios') renderUsuarios();
  if (v === 'equipo') { renderEquipo(); refreshTeamUsers(); }""")

# 8. Al entrar: arrancar presencia y chat
rep("""    cloudUnsub = window.Cloud.subscribeRenta(function (docs) {
      state.renta = docs.map(rentaFromCloud);
      save(); render();
    });
    render();""",
"""    cloudUnsub = window.Cloud.subscribeRenta(function (docs) {
      state.renta = docs.map(rentaFromCloud);
      save(); render();
    });
    startEquipo();
    render();""")

# 9. Al salir: parar presencia y chat
rep("""document.getElementById('btnLogout').addEventListener('click', function () {
  if (cloudUnsub) { cloudUnsub(); cloudUnsub = null; }""",
"""document.getElementById('btnLogout').addEventListener('click', function () {
  stopEquipo();
  if (cloudUnsub) { cloudUnsub(); cloudUnsub = null; }""")

# 10. La pestaña Equipo solo existe con nube
rep("""function render() {
  var counts = { preparacion: 0, listo: 0, entregado: 0 };""",
"""function render() {
  document.getElementById('tabEquipo').hidden = !CLOUD_ENABLED;
  var counts = { preparacion: 0, listo: 0, entregado: 0 };""")

assert s != orig
open(P, 'w').write(s)
print('OK parche 2.0.19b (index.html) aplicado')
print('Quedan "2.0.18":', len(re.findall(r'2\.0\.18', s)))
