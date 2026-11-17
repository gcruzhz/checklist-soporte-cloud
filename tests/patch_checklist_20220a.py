#!/usr/bin/env python3
"""Parche 2.2.0a: Firebase — clave de la IA (Gemini) en config/ai."""
P = '/home/hatch/workspace/android/checklist-cloud/www/cloud/firebase.js'
s = open(P).read()
orig = s

def rep(old, new, n=1):
    global s
    assert old in s, 'NO ENCONTRADO: ' + old[:90]
    s = s.replace(old, new, n)

# getAiKey / setAiKey después de adminUpdateUser (la clave la guarda el admin
# una vez en Firestore y todos los teléfonos la leen al entrar).
rep("""  deleteUserByAdmin,
  adminUpdateUser,""",
"""  deleteUserByAdmin,
  adminUpdateUser,
  getAiKey,
  setAiKey,""")

rep("""async function adminUpdateUser(uid, oldUsuario, { nombre, usuario, email }) {""",
"""// Clave de la IA (Gemini): el admin la guarda una vez en config/ai y todos
// los teléfonos la leen al entrar. La clave en sí la crea el admin gratis
// en Google AI Studio.
async function getAiKey() {
  const snap = await getDoc(doc(db, 'config', 'ai'));
  return snap.exists() ? (snap.data().key || '') : '';
}
async function setAiKey(key) {
  await setDoc(doc(db, 'config', 'ai'), { key: key || '' });
}

async function adminUpdateUser(uid, oldUsuario, { nombre, usuario, email }) {""")

assert s != orig
open(P, 'w').write(s)
print('OK parche 2.2.0a (firebase.js) aplicado')
