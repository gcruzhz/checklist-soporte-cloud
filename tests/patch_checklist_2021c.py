#!/usr/bin/env python3
"""Parche 2.1c: Firebase — chat individual (dm) y limpieza de ambos chats a 24 h."""
P = '/home/hatch/workspace/android/checklist-cloud/www/cloud/firebase.js'
s = open(P).read()
orig = s

def rep(old, new, n=1):
    global s
    assert old in s, 'NO ENCONTRADO: ' + old[:90]
    s = s.replace(old, new, n)

# 1. pruneChat también limpia los mensajes directos (el chat no guarda historial)
rep("""// Chat efímero: borra los mensajes de más de 24 horas (el chat no guarda historial).
async function pruneChat() {
  try {
    const cutoff = new Date(Date.now() - 24 * 60 * 60 * 1000);
    const snap = await getDocs(query(collection(db, 'chat'), where('createdAt', '<', cutoff), limit(50)));
    for (const d of snap.docs) { await deleteDoc(d.ref); }
  } catch (e) { console.warn('[Cloud] Error al limpiar el chat:', e); }
}""",
"""// Chat efímero: borra los mensajes de más de 24 horas (el chat no guarda
// historial), tanto del chat del equipo como de los chats individuales.
async function pruneChat() {
  try {
    const cutoff = new Date(Date.now() - 24 * 60 * 60 * 1000);
    for (const col of ['chat', 'dm']) {
      const snap = await getDocs(query(collection(db, col), where('createdAt', '<', cutoff), limit(50)));
      for (const d of snap.docs) { await deleteDoc(d.ref); }
    }
  } catch (e) { console.warn('[Cloud] Error al limpiar el chat:', e); }
}

// Chat individual (1 a 1): cada mensaje lleva los dos participantes
// (ordenados) para que solo ellos dos puedan leerlo.
function subscribeDm(cb) {
  const u = auth.currentUser;
  if (!u) return () => {};
  return onSnapshot(
    query(collection(db, 'dm'), where('participants', 'array-contains', u.uid), limit(100)),
    (snap) => cb(snap.docs.map((d) => Object.assign({ id: d.id }, d.data()))),
    (err) => console.warn('[Cloud] Error en snapshot de mensajes directos:', err)
  );
}
async function sendDm(toUid, texto, nombre) {
  const u = auth.currentUser;
  if (!u) throw new Error('no-auth');
  const t = (texto || '').trim();
  if (!t) return;
  const parts = [u.uid, toUid].sort();
  await addDoc(collection(db, 'dm'), {
    participants: parts,
    from: u.uid,
    to: toUid,
    nombre: nombre || u.email || '',
    texto: t.slice(0, 500),
    createdAt: serverTimestamp()
  });
}""")

# 2. Exportarlas en window.Cloud
rep("""  subscribeChat,
  sendChat,
  pruneChat
};""",
"""  subscribeChat,
  sendChat,
  pruneChat,
  subscribeDm,
  sendDm
};""")

assert s != orig
open(P, 'w').write(s)
print('OK parche 2.1c (firebase.js, chat individual) aplicado')
