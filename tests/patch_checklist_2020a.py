#!/usr/bin/env python3
"""Parche 2.0.20a: Firebase — limpieza del chat (mensajes de más de 24 h se borran)."""
P = '/home/hatch/workspace/android/checklist-cloud/www/cloud/firebase.js'
s = open(P).read()
orig = s

def rep(old, new, n=1):
    global s
    assert old in s, 'NO ENCONTRADO: ' + old[:90]
    s = s.replace(old, new, n)

# 1. pruneChat después de sendChat
rep("""async function sendChat(texto, nombre) {
  const u = auth.currentUser;
  if (!u) throw new Error('no-auth');
  const t = (texto || '').trim();
  if (!t) return;
  await addDoc(collection(db, 'chat'), {
    uid: u.uid,
    nombre: nombre || u.email || '',
    texto: t.slice(0, 500),
    createdAt: serverTimestamp()
  });
}""",
"""async function sendChat(texto, nombre) {
  const u = auth.currentUser;
  if (!u) throw new Error('no-auth');
  const t = (texto || '').trim();
  if (!t) return;
  await addDoc(collection(db, 'chat'), {
    uid: u.uid,
    nombre: nombre || u.email || '',
    texto: t.slice(0, 500),
    createdAt: serverTimestamp()
  });
}

// Chat efímero: borra los mensajes de más de 24 horas (el chat no guarda historial).
async function pruneChat() {
  try {
    const cutoff = new Date(Date.now() - 24 * 60 * 60 * 1000);
    const snap = await getDocs(query(collection(db, 'chat'), where('createdAt', '<', cutoff), limit(50)));
    for (const d of snap.docs) { await deleteDoc(d.ref); }
  } catch (e) { console.warn('[Cloud] Error al limpiar el chat:', e); }
}""")

# 2. Exportarla en window.Cloud
rep("""  subscribeChat,
  sendChat
};""",
"""  subscribeChat,
  sendChat,
  pruneChat
};""")

assert s != orig
open(P, 'w').write(s)
print('OK parche 2.0.20a (firebase.js) aplicado')
