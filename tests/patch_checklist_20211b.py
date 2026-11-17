#!/usr/bin/env python3
"""Parche 2.1.1b: el admin ve un botón para borrar mensajes en ambos chats."""
P = '/home/hatch/workspace/android/checklist-cloud/www/index.html'
s = open(P).read()
orig = s

def rep(old, new, n=1):
    global s
    assert old in s, 'NO ENCONTRADO: ' + old[:90]
    s = s.replace(old, new, n)

# ---------- 1. Versión visible ----------
rep('Versión 2.1', 'Versión 2.1.1')
rep('Versión: 2.1', 'Versión: 2.1.1')
rep('Checklist de Soporte 2.1', 'Checklist de Soporte 2.1.1')
rep('Versión de la app: 2.1', 'Versión de la app: 2.1.1')

# ---------- 2. CSS del botón de borrar ----------
rep("  .msg.mine .txt { background: #e8f3df; border-radius: 10px; padding: 6px 9px; display: inline-block; }",
    "  .msg.mine .txt { background: #e8f3df; border-radius: 10px; padding: 6px 9px; display: inline-block; }\n  .msg-del { background: none; border: 0; color: #b3261e; cursor: pointer; font-size: 13px; padding: 0 2px; }")

# ---------- 3. Botón de borrar en el chat del equipo (solo admin) ----------
rep("""  var cb = document.getElementById('chatBox');
  if (!chatMessages.length) { cb.innerHTML = '<div class="empty">Aún no hay mensajes.</div>'; }
  else {
    cb.innerHTML = chatMessages.map(function (m) {
      var mine = cloudUser && m.uid === cloudUser.uid;
      var ms = tsMs(m.createdAt);
      return '<div class="msg' + (mine ? ' mine' : '') + '"><div class="meta">' + esc(m.nombre || 'Usuario') + ' · ' + (ms ? fmtTime(ms) : 'enviando…') + '</div><div class="txt">' + esc(m.texto || '') + '</div></div>';
    }).join('');
    cb.scrollTop = cb.scrollHeight;
  }""",
"""  var isAdmin = cloudRole === 'admin';
  var cb = document.getElementById('chatBox');
  if (!chatMessages.length) { cb.innerHTML = '<div class="empty">Aún no hay mensajes.</div>'; }
  else {
    cb.innerHTML = chatMessages.map(function (m) {
      var mine = cloudUser && m.uid === cloudUser.uid;
      var ms = tsMs(m.createdAt);
      return '<div class="msg' + (mine ? ' mine' : '') + '"><div class="meta">' + esc(m.nombre || 'Usuario') + ' · ' + (ms ? fmtTime(ms) : 'enviando…') + (isAdmin ? ' <button class="msg-del" data-del-chat="' + m.id + '" title="Borrar mensaje">🗑️</button>' : '') + '</div><div class="txt">' + esc(m.texto || '') + '</div></div>';
    }).join('');
    cb.scrollTop = cb.scrollHeight;
  }""")

# ---------- 4. Botón de borrar en el chat individual (solo admin) ----------
rep("""      dcb.innerHTML = conv.map(function (m) {
        var mine = cloudUser && m.from === cloudUser.uid;
        var ms = tsMs(m.createdAt);
        return '<div class="msg' + (mine ? ' mine' : '') + '"><div class="meta">' + esc(m.nombre || 'Usuario') + ' · ' + (ms ? fmtTime(ms) : 'enviando…') + '</div><div class="txt">' + esc(m.texto || '') + '</div></div>';
      }).join('');""",
"""      dcb.innerHTML = conv.map(function (m) {
        var mine = cloudUser && m.from === cloudUser.uid;
        var ms = tsMs(m.createdAt);
        return '<div class="msg' + (mine ? ' mine' : '') + '"><div class="meta">' + esc(m.nombre || 'Usuario') + ' · ' + (ms ? fmtTime(ms) : 'enviando…') + (isAdmin ? ' <button class="msg-del" data-del-dm="' + m.id + '" title="Borrar mensaje">🗑️</button>' : '') + '</div><div class="txt">' + esc(m.texto || '') + '</div></div>';
      }).join('');""")

# ---------- 5. Borrar al tocar el botón (con confirmación) ----------
rep("""document.getElementById('btnDmBack').addEventListener('click', function () { dmPeer = null; renderEquipo(); });""",
"""document.getElementById('btnDmBack').addEventListener('click', function () { dmPeer = null; renderEquipo(); });
// Moderación: solo el admin ve el botón de borrar; borra el mensaje para todos.
document.getElementById('chatBox').addEventListener('click', function (e) {
  var b = e.target.closest('[data-del-chat]');
  if (!b) return;
  if (!confirm('¿Borrar este mensaje para todos?')) return;
  window.Cloud.deleteChatMessage(b.getAttribute('data-del-chat')).catch(function () { alert('No se pudo borrar el mensaje.'); });
});
document.getElementById('dmChatBox').addEventListener('click', function (e) {
  var b = e.target.closest('[data-del-dm]');
  if (!b) return;
  if (!confirm('¿Borrar este mensaje para los dos?')) return;
  window.Cloud.deleteDmMessage(b.getAttribute('data-del-dm')).catch(function () { alert('No se pudo borrar el mensaje.'); });
});""")

assert s != orig
open(P, 'w').write(s)
print('OK parche 2.1.1b (index.html) aplicado')
print('Quedan "2.1" sin ".1":', len(__import__('re').findall(r'Versión 2\.1(?!\\.1)', s)))
