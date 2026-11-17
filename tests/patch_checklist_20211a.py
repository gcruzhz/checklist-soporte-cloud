#!/usr/bin/env python3
"""Parche 2.1.1a: Firebase — el admin puede borrar cualquier mensaje (moderación)."""
P = '/home/hatch/workspace/android/checklist-cloud/www/cloud/firebase.js'
s = open(P).read()
orig = s

def rep(old, new, n=1):
    global s
    assert old in s, 'NO ENCONTRADO: ' + old[:90]
    s = s.replace(old, new, n)

# Borrar mensajes (moderación del admin) después de sendDm
rep("""async function sendDm(toUid, texto, nombre) {
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
}""",
"""async function sendDm(toUid, texto, nombre) {
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
}

// Moderación: el admin puede borrar cualquier mensaje, del chat del
// equipo o de un chat individual (las reglas ya lo permiten).
async function deleteChatMessage(id) {
  return deleteDoc(doc(db, 'chat', id));
}
async function deleteDmMessage(id) {
  return deleteDoc(doc(db, 'dm', id));
}""")

# Exportarlas en window.Cloud
rep("""  subscribeDm,
  sendDm
};""",
"""  subscribeDm,
  sendDm,
  deleteChatMessage,
  deleteDmMessage
};""")

assert s != orig
open(P, 'w').write(s)
print('OK parche 2.1.1a (firebase.js) aplicado')
