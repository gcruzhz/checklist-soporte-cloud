#!/usr/bin/env python3
"""Parche 2.1b: Por preparar sincronizado (nuevo y reasignado) + chat individual."""
P = '/home/hatch/workspace/android/checklist-cloud/www/index.html'
s = open(P).read()
orig = s

def rep(old, new, n=1):
    global s
    assert old in s, 'NO ENCONTRADO: ' + old[:90]
    s = s.replace(old, new, n)

# ---------- 1. Versión visible ----------
rep('Versión 2.0.20', 'Versión 2.1')
rep('Versión: 2.0.20', 'Versión: 2.1')
rep('Checklist de Soporte 2.0.20', 'Checklist de Soporte 2.1')
rep('Versión de la app: 2.0.20', 'Versión de la app: 2.1')

# ---------- 2. Nota de sincronización en Por preparar ----------
rep('  <div class="share-note" id="tecnicoLine"></div>',
    '  <div class="share-note" id="tecnicoLine"></div>\n  <div class="share-note">Los equipos en preparación se sincronizan entre todos los teléfonos.</div>')

# ---------- 3. Chat individual: HTML en la vista Equipo ----------
rep("""    <div class="row" style="margin-top:8px">
      <input id="chatInput" type="text" placeholder="Escribe un mensaje…" maxlength="500" style="flex:1">
      <button class="btn-dark" id="btnChatSend">Enviar</button>
    </div>
  </div></main>""",
"""    <div class="row" style="margin-top:8px">
      <input id="chatInput" type="text" placeholder="Escribe un mensaje…" maxlength="500" style="flex:1">
      <button class="btn-dark" id="btnChatSend">Enviar</button>
    </div>
    <div class="sub" style="margin-top:14px"><b>Chat individual</b></div>
    <div id="dmList"><div class="empty">Cargando…</div></div>
    <div id="dmBox" hidden>
      <div class="row" style="align-items:center">
        <button class="btn-ghost" id="btnDmBack">← Volver</button>
        <b id="dmTitle" style="flex:1"></b>
      </div>
      <div class="chat-box" id="dmChatBox"><div class="empty">Aún no hay mensajes.</div></div>
      <div class="row" style="margin-top:8px">
        <input id="dmInput" type="text" placeholder="Escribe un mensaje…" maxlength="500" style="flex:1">
        <button class="btn-dark" id="btnDmSend">Enviar</button>
      </div>
    </div>
  </div></main>""")

# ---------- 4. Sincronización de preparaciones: helpers tras cloudDelete ----------
rep("""function cloudDelete(id) {
  if (!CLOUD_ENABLED || !cloudUser || !window.Cloud) return;
  window.Cloud.deleteRenta(id).catch(function (e) { console.warn('No se pudo borrar en la nube', e); });
}""",
"""function cloudDelete(id) {
  if (!CLOUD_ENABLED || !cloudUser || !window.Cloud) return;
  window.Cloud.deleteRenta(id).catch(function (e) { console.warn('No se pudo borrar en la nube', e); });
}

// ---------- Por preparar sincronizado ----------
// Los equipos en preparación (nuevos o reasignados) viven en Firestore
// (colección preparations) y se ven en todos los teléfonos, igual que la
// renta. La plantilla del checklist sigue siendo local de cada teléfono.
var cloudPrepUnsub = null;
var PREP_MIG_KEY = 'checklist-soporte-migrado-preps-v1';
var MAX_FOTO_CLOUD = 700000; // la foto de serie no viaja si pasa de ~700 KB (límite de 1 MB por documento)
// La foto del número de serie es una imagen en base64 que puede pesar
// cientos de KB; si viajara entera, el documento pasaría el límite de
// 1 MB de Firestore y la escritura fallaría sin avisar.
function prepToCloudDoc(p) {
  var eq = p.equipo || {};
  var foto = eq.fotoSerie || null;
  if (foto && foto.length > MAX_FOTO_CLOUD) foto = null;
  return {
    id: p.id, createdAt: p.createdAt || Date.now(), deliveredAt: p.deliveredAt || null, readyAt: p.readyAt || null,
    checks: p.checks || {}, extraItems: p.extraItems || [], reasignaciones: p.reasignaciones || [],
    equipo: { tipo: eq.tipo || '', marca: eq.marca || '', modelo: eq.modelo || '', serie: eq.serie || '', inventario: eq.inventario || '', fotoSerie: foto },
    usuario: { nombre: (p.usuario && p.usuario.nombre) || '', area: (p.usuario && p.usuario.area) || '', correo: (p.usuario && p.usuario.correo) || '' },
    tecnico: p.tecnico || '',
    updatedAt: Date.now()
  };
}
function prepFromCloud(doc) {
  var eq = doc.equipo || {};
  return {
    id: doc.id, createdAt: doc.createdAt || 0, deliveredAt: doc.deliveredAt || null, readyAt: doc.readyAt || null,
    checks: doc.checks || {}, extraItems: doc.extraItems || [], reasignaciones: doc.reasignaciones || [],
    equipo: { tipo: eq.tipo || '', marca: eq.marca || '', modelo: eq.modelo || '', serie: eq.serie || '', inventario: eq.inventario || '', fotoSerie: eq.fotoSerie || null },
    usuario: { nombre: (doc.usuario && doc.usuario.nombre) || '', area: (doc.usuario && doc.usuario.area) || '', correo: (doc.usuario && doc.usuario.correo) || '' },
    tecnico: doc.tecnico || ''
  };
}
function cloudUpsertPrep(prep) {
  if (!CLOUD_ENABLED || !cloudUser || !window.Cloud) return;
  window.Cloud.upsertPrep(prepToCloudDoc(prep)).catch(function (e) { console.warn('No se pudo guardar el equipo en la nube', e); });
}
function cloudDeletePrep(id) {
  if (!CLOUD_ENABLED || !cloudUser || !window.Cloud) return;
  window.Cloud.deletePrep(id).catch(function (e) { console.warn('No se pudo borrar el equipo en la nube', e); });
}
async function migrateLocalPreparations() {
  try {
    var flag = PREP_MIG_KEY + ':' + cloudUser.uid;
    if (localStorage.getItem(flag)) return;
    var inCloud = await window.Cloud.getAllPreparations();
    var ids = {};
    inCloud.forEach(function (d) { ids[d.id] = true; });
    var pendientes = state.preparations.filter(function (p) { return !ids[p.id]; });
    for (var i = 0; i < pendientes.length; i++) {
      await window.Cloud.upsertPrep(prepToCloudDoc(pendientes[i]));
    }
    localStorage.setItem(flag, '1');
  } catch (e) { console.warn('Migración de preparaciones pendiente', e); }
}
// Al recibir la lista de la nube, conservar la foto de serie que cada
// teléfono ya tenía si la nube no la trae (la foto no siempre viaja).
function mergePrepsWithLocal(docs) {
  var localById = {};
  state.preparations.forEach(function (p) { localById[p.id] = p; });
  return docs.map(function (d) {
    var p = prepFromCloud(d);
    var local = localById[p.id];
    if (local && local.equipo && local.equipo.fotoSerie && !p.equipo.fotoSerie) p.equipo.fotoSerie = local.equipo.fotoSerie;
    return p;
  });
}""")

# ---------- 5. Cerrar la suscripción de preparaciones al salir ----------
rep("""    if (cloudUnsub) { cloudUnsub(); cloudUnsub = null; }""",
"""    if (cloudUnsub) { cloudUnsub(); cloudUnsub = null; }
    if (cloudPrepUnsub) { cloudPrepUnsub(); cloudPrepUnsub = null; }""")

# ---------- 6. Al entrar: migrar y suscribirse a las preparaciones ----------
rep("""    await migrateLocalRenta();
    if (cloudUnsub) cloudUnsub();
    cloudUnsub = window.Cloud.subscribeRenta(function (docs) {
      state.renta = docs.map(rentaFromCloud);
      save(); render();
    });""",
"""    await migrateLocalRenta();
    await migrateLocalPreparations();
    if (cloudUnsub) cloudUnsub();
    cloudUnsub = window.Cloud.subscribeRenta(function (docs) {
      state.renta = docs.map(rentaFromCloud);
      save(); render();
    });
    if (cloudPrepUnsub) cloudPrepUnsub();
    cloudPrepUnsub = window.Cloud.subscribePreparations(function (docs) {
      state.preparations = mergePrepsWithLocal(docs);
      save(); render();
    });""")

# ---------- 7. Cada cambio en un equipo se sube a la nube ----------
# Nuevo equipo (btnAdd)
rep("""  state.preparations.push(prep);
  save();
  ['fMarca', 'fModelo', 'fSerie', 'fInv', 'fTec', 'fUser', 'fArea', 'fCorreo'].forEach(function (id) { document.getElementById(id).value = ''; });""",
"""  state.preparations.push(prep);
  cloudUpsertPrep(prep);
  save();
  ['fMarca', 'fModelo', 'fSerie', 'fInv', 'fTec', 'fUser', 'fArea', 'fCorreo'].forEach(function (id) { document.getElementById(id).value = ''; });""")
# Reasignar Equipo (panel): nuevo o existente, prep queda en alcance en ambas ramas
rep("""    doReassign(prep, de, a);
  }
  save();""",
"""    doReassign(prep, de, a);
  }
  cloudUpsertPrep(prep);
  save();""")
# Elección de Office
rep("""    prep.checks[cid] = (prep.checks[cid] === cval) ? false : cval;
    save(); render(); return;""",
"""    prep.checks[cid] = (prep.checks[cid] === cval) ? false : cval;
    cloudUpsertPrep(prep);
    save(); render(); return;""")
# Reasignación desde la tarjeta
rep("""    doReassign(prep, reDe, reA);
    window._reassignFor = null;
    save(); setFilter(statusOf(prep)); render(); return;""",
"""    doReassign(prep, reDe, reA);
    window._reassignFor = null;
    cloudUpsertPrep(prep);
    save(); setFilter(statusOf(prep)); render(); return;""")
# Entregado / Listo / Quitar listo / Reabrir
rep("""  if (t.hasAttribute('data-deliver') && prep) { prep.deliveredAt = Date.now(); save(); setFilter('entregado'); render(); return; }
  if (t.hasAttribute('data-ready') && prep) { prep.readyAt = Date.now(); save(); setFilter('listo'); render(); return; }
  if (t.hasAttribute('data-unready') && prep) { prep.readyAt = null; save(); setFilter('preparacion'); render(); return; }
  if (t.hasAttribute('data-reopen') && prep) { prep.deliveredAt = null; save(); setFilter(statusOf(prep)); render(); return; }""",
"""  if (t.hasAttribute('data-deliver') && prep) { prep.deliveredAt = Date.now(); cloudUpsertPrep(prep); save(); setFilter('entregado'); render(); return; }
  if (t.hasAttribute('data-ready') && prep) { prep.readyAt = Date.now(); cloudUpsertPrep(prep); save(); setFilter('listo'); render(); return; }
  if (t.hasAttribute('data-unready') && prep) { prep.readyAt = null; cloudUpsertPrep(prep); save(); setFilter('preparacion'); render(); return; }
  if (t.hasAttribute('data-reopen') && prep) { prep.deliveredAt = null; cloudUpsertPrep(prep); save(); setFilter(statusOf(prep)); render(); return; }""")
# Eliminar equipo
rep("""    if (confirm('¿Eliminar este equipo y su checklist?')) {
      state.preparations = state.preparations.filter(function (p) { return p.id !== prep.id; });
      save(); render();
    }""",
"""    if (confirm('¿Eliminar este equipo y su checklist?')) {
      state.preparations = state.preparations.filter(function (p) { return p.id !== prep.id; });
      cloudDeletePrep(prep.id);
      save(); render();
    }""")
# Punto extra: agregar y borrar
rep("""    prep.extraItems.push({ id: uid(), group: document.getElementById('extraGroup').value, text: txt });
    window._extraFor = null;
    save(); render(); return;""",
"""    prep.extraItems.push({ id: uid(), group: document.getElementById('extraGroup').value, text: txt });
    window._extraFor = null;
    cloudUpsertPrep(prep);
    save(); render(); return;""")
rep("""    prep.extraItems = prep.extraItems.filter(function (x) { return x.id !== xid; });
    delete prep.checks[xid];
    save(); render(); return;""",
"""    prep.extraItems = prep.extraItems.filter(function (x) { return x.id !== xid; });
    delete prep.checks[xid];
    cloudUpsertPrep(prep);
    save(); render(); return;""")
# Casilla marcada/desmarcada
rep("""  prep.checks[t.getAttribute('data-check')] = t.checked;
  save(); render();""",
"""  prep.checks[t.getAttribute('data-check')] = t.checked;
  cloudUpsertPrep(prep);
  save(); render();""")

# ---------- 8. Chat individual: estado y render en Equipo ----------
rep("""var presenceList = [];
var chatMessages = [];
var teamUsers = [];
var presenceUnsub = null, chatUnsub = null, heartbeatTimer = null;""",
"""var presenceList = [];
var chatMessages = [];
var dmMessages = [];
var dmPeer = null;
var teamUsers = [];
var presenceUnsub = null, chatUnsub = null, dmUnsub = null, heartbeatTimer = null;""")

rep("""  var cb = document.getElementById('chatBox');
  if (!chatMessages.length) { cb.innerHTML = '<div class="empty">Aún no hay mensajes.</div>'; }
  else {
    cb.innerHTML = chatMessages.map(function (m) {
      var mine = cloudUser && m.uid === cloudUser.uid;
      var ms = tsMs(m.createdAt);
      return '<div class="msg' + (mine ? ' mine' : '') + '"><div class="meta">' + esc(m.nombre || 'Usuario') + ' · ' + (ms ? fmtTime(ms) : 'enviando…') + '</div><div class="txt">' + esc(m.texto || '') + '</div></div>';
    }).join('');
    cb.scrollTop = cb.scrollHeight;
  }
}""",
"""  var cb = document.getElementById('chatBox');
  if (!chatMessages.length) { cb.innerHTML = '<div class="empty">Aún no hay mensajes.</div>'; }
  else {
    cb.innerHTML = chatMessages.map(function (m) {
      var mine = cloudUser && m.uid === cloudUser.uid;
      var ms = tsMs(m.createdAt);
      return '<div class="msg' + (mine ? ' mine' : '') + '"><div class="meta">' + esc(m.nombre || 'Usuario') + ' · ' + (ms ? fmtTime(ms) : 'enviando…') + '</div><div class="txt">' + esc(m.texto || '') + '</div></div>';
    }).join('');
    cb.scrollTop = cb.scrollHeight;
  }
  // Chat individual: lista de compañeros o conversación con uno.
  var dl = document.getElementById('dmList');
  var db = document.getElementById('dmBox');
  if (dmPeer) {
    dl.hidden = true; db.hidden = false;
    var peer = null;
    teamUsers.forEach(function (u) { if (u.uid === dmPeer) peer = u; });
    peer = peer || { nombre: 'Usuario' };
    document.getElementById('dmTitle').textContent = peer.nombre || peer.email || 'Usuario';
    var conv = dmMessages.filter(function (m) { return m.participants && m.participants.indexOf(dmPeer) !== -1; })
      .sort(function (a, b) { return tsMs(a.createdAt) - tsMs(b.createdAt); });
    var dcb = document.getElementById('dmChatBox');
    if (!conv.length) { dcb.innerHTML = '<div class="empty">Aún no hay mensajes con ' + esc(peer.nombre || peer.email || 'este usuario') + '.</div>'; }
    else {
      dcb.innerHTML = conv.map(function (m) {
        var mine = cloudUser && m.from === cloudUser.uid;
        var ms = tsMs(m.createdAt);
        return '<div class="msg' + (mine ? ' mine' : '') + '"><div class="meta">' + esc(m.nombre || 'Usuario') + ' · ' + (ms ? fmtTime(ms) : 'enviando…') + '</div><div class="txt">' + esc(m.texto || '') + '</div></div>';
      }).join('');
      dcb.scrollTop = dcb.scrollHeight;
    }
  } else {
    dl.hidden = false; db.hidden = true;
    var others = teamUsers.filter(function (u) { return !cloudUser || u.uid !== cloudUser.uid; });
    if (!others.length) { dl.innerHTML = '<div class="empty">No hay otros usuarios todavía.</div>'; }
    else {
      dl.innerHTML = others.map(function (u) {
        var pr = null;
        presenceList.forEach(function (p) { if (p.uid === u.uid || p.id === u.uid) pr = p; });
        var ms = pr ? tsMs(pr.lastSeen) : 0;
        var isOn = !!ms && (Date.now() - ms) <= ONLINE_MS;
        var last = dmMessages.filter(function (m) { return m.participants && m.participants.indexOf(u.uid) !== -1; })
          .sort(function (a, b) { return tsMs(b.createdAt) - tsMs(a.createdAt); })[0];
        return '<div class="user-row" data-dm-user="' + u.uid + '" style="cursor:pointer"><span class="dot' + (isOn ? ' on' : '') + '"></span><span class="who"><b>' + esc(u.nombre || u.email || 'Usuario') + '</b>' + (u.rol === 'admin' ? ' · Administrador' : '') + '</span><span class="st">' + (last ? esc((last.texto || '').slice(0, 30)) : (isOn ? 'en línea' : timeAgo(ms))) + '</span></div>';
      }).join('');
    }
  }
}""")

# ---------- 9. Chat individual: suscribirse al entrar y soltar al salir ----------
rep("""  presenceUnsub = window.Cloud.subscribePresence(function (docs) { presenceList = docs; if (!document.getElementById('viewEquipo').hidden) renderEquipo(); });
  chatUnsub = window.Cloud.subscribeChat(function (docs) { chatMessages = docs; if (!document.getElementById('viewEquipo').hidden) renderEquipo(); });""",
"""  presenceUnsub = window.Cloud.subscribePresence(function (docs) { presenceList = docs; if (!document.getElementById('viewEquipo').hidden) renderEquipo(); });
  chatUnsub = window.Cloud.subscribeChat(function (docs) { chatMessages = docs; if (!document.getElementById('viewEquipo').hidden) renderEquipo(); });
  dmUnsub = window.Cloud.subscribeDm(function (docs) { dmMessages = docs; if (!document.getElementById('viewEquipo').hidden) renderEquipo(); });""")
rep("""  if (presenceUnsub) { presenceUnsub(); presenceUnsub = null; }
  if (chatUnsub) { chatUnsub(); chatUnsub = null; }""",
"""  if (presenceUnsub) { presenceUnsub(); presenceUnsub = null; }
  if (chatUnsub) { chatUnsub(); chatUnsub = null; }
  if (dmUnsub) { dmUnsub(); dmUnsub = null; }""")

# ---------- 10. Chat individual: enviar y abrir conversación ----------
rep("""document.getElementById('btnChatSend').addEventListener('click', sendChatMsg);
document.getElementById('chatInput').addEventListener('keydown', function (e) { if (e.key === 'Enter') sendChatMsg(); });""",
"""document.getElementById('btnChatSend').addEventListener('click', sendChatMsg);
document.getElementById('chatInput').addEventListener('keydown', function (e) { if (e.key === 'Enter') sendChatMsg(); });
function sendDmMsg() {
  if (!window.Cloud || !CLOUD_ENABLED || !dmPeer) return;
  var inp = document.getElementById('dmInput');
  var t = inp.value.trim();
  if (!t) return;
  inp.value = '';
  window.Cloud.sendDm(dmPeer, t, technicianName()).catch(function () { alert('No se pudo enviar el mensaje. Revisa tu conexión.'); });
}
document.getElementById('btnDmSend').addEventListener('click', sendDmMsg);
document.getElementById('dmInput').addEventListener('keydown', function (e) { if (e.key === 'Enter') sendDmMsg(); });
document.getElementById('dmList').addEventListener('click', function (e) {
  var row = e.target.closest('[data-dm-user]');
  if (!row) return;
  dmPeer = row.getAttribute('data-dm-user');
  renderEquipo();
});
document.getElementById('btnDmBack').addEventListener('click', function () { dmPeer = null; renderEquipo(); });""")

assert s != orig
open(P, 'w').write(s)
print('OK parche 2.1b (index.html) aplicado')
print('Quedan "2.0.20":', len(__import__('re').findall(r'2\.0\.20', s)))
