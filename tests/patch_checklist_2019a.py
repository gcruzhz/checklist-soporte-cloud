#!/usr/bin/env python3
"""Parche 2.0.19a: Firebase — presencia (quién está en línea) y chat interno."""
P = '/home/hatch/workspace/android/checklist-cloud/www/cloud/firebase.js'
s = open(P).read()
orig = s

def rep(old, new, n=1):
    global s
    assert old in s, 'NO ENCONTRADO: ' + old[:90]
    s = s.replace(old, new, n)

# 1. Imports nuevos: addDoc, orderBy, limit, serverTimestamp
rep("""  onSnapshot,
  query,
  where
} from 'firebase/firestore';""",
"""  onSnapshot,
  query,
  where,
  addDoc,
  orderBy,
  limit,
  serverTimestamp
} from 'firebase/firestore';""")

# 2. Funciones de presencia y chat, después de getAllRenta
rep("""async function getAllRenta() {
  const snap = await getDocs(collection(db, 'renta'));
  return snap.docs.map((d) => Object.assign({ id: d.id }, d.data()));
}""",
"""async function getAllRenta() {
  const snap = await getDocs(collection(db, 'renta'));
  return snap.docs.map((d) => Object.assign({ id: d.id }, d.data()));
}

// Presencia: latido que dice "estoy en línea" (se escribe cada 2 minutos
// mientras la app está abierta) y escucha en vivo de quién está conectado.
async function heartbeat(nombre, rol) {
  const u = auth.currentUser;
  if (!u) return;
  try {
    await setDoc(doc(db, 'presence', u.uid), {
      uid: u.uid,
      nombre: nombre || u.email || '',
      rol: rol || 'usuario',
      lastSeen: serverTimestamp()
    }, { merge: true });
  } catch (e) { console.warn('[Cloud] Error en heartbeat:', e); }
}

function subscribePresence(cb) {
  return onSnapshot(
    collection(db, 'presence'),
    (snap) => cb(snap.docs.map((d) => Object.assign({ id: d.id }, d.data()))),
    (err) => console.warn('[Cloud] Error en snapshot de presencia:', err)
  );
}

async function clearPresence() {
  const u = auth.currentUser;
  if (!u) return;
  try { await deleteDoc(doc(db, 'presence', u.uid)); } catch (e) {}
}

// Chat interno: últimos 50 mensajes, en vivo, en orden cronológico.
function subscribeChat(cb) {
  return onSnapshot(
    query(collection(db, 'chat'), orderBy('createdAt', 'desc'), limit(50)),
    (snap) => cb(snap.docs.map((d) => Object.assign({ id: d.id }, d.data())).reverse()),
    (err) => console.warn('[Cloud] Error en snapshot de chat:', err)
  );
}

async function sendChat(texto, nombre) {
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
}""")

# 3. Exportarlas en window.Cloud
rep("""  subscribeRenta,
  upsertRenta,
  deleteRenta,
  getAllRenta
};""",
"""  subscribeRenta,
  upsertRenta,
  deleteRenta,
  getAllRenta,
  heartbeat,
  subscribePresence,
  clearPresence,
  subscribeChat,
  sendChat
};""")

assert s != orig
open(P, 'w').write(s)
print('OK parche 2.0.19a (firebase.js) aplicado')
