#!/usr/bin/env python3
"""Parche 2.1a: Firebase — colección preparations (Por preparar sincronizado)."""
P = '/home/hatch/workspace/android/checklist-cloud/www/cloud/firebase.js'
s = open(P).read()
orig = s

def rep(old, new, n=1):
    global s
    assert old in s, 'NO ENCONTRADO: ' + old[:90]
    s = s.replace(old, new, n)

# 1. Funciones de preparations después de getAllRenta
rep("""async function getAllRenta() {
  const snap = await getDocs(collection(db, 'renta'));
  return snap.docs.map((d) => Object.assign({ id: d.id }, d.data()));
}""",
"""async function getAllRenta() {
  const snap = await getDocs(collection(db, 'renta'));
  return snap.docs.map((d) => Object.assign({ id: d.id }, d.data()));
}

// Preparaciones (Por preparar): se sincronizan entre todos los teléfonos,
// igual que la renta.
function subscribePreparations(cb) {
  return onSnapshot(
    collection(db, 'preparations'),
    (snap) => cb(snap.docs.map((d) => Object.assign({ id: d.id }, d.data()))),
    (err) => console.warn('[Cloud] Error en snapshot de preparaciones:', err)
  );
}
async function upsertPrep(prep) {
  return setDoc(
    doc(db, 'preparations', prep.id),
    Object.assign({}, prep, { updatedAt: Date.now() }),
    { merge: true }
  );
}
async function deletePrep(id) {
  return deleteDoc(doc(db, 'preparations', id));
}
async function getAllPreparations() {
  const snap = await getDocs(collection(db, 'preparations'));
  return snap.docs.map((d) => Object.assign({ id: d.id }, d.data()));
}""")

# 2. Exportarlas en window.Cloud
rep("""  subscribeRenta,
  upsertRenta,
  deleteRenta,
  getAllRenta,""",
"""  subscribeRenta,
  upsertRenta,
  deleteRenta,
  getAllRenta,
  subscribePreparations,
  upsertPrep,
  deletePrep,
  getAllPreparations,""")

assert s != orig
open(P, 'w').write(s)
print('OK parche 2.1a (firebase.js) aplicado')
