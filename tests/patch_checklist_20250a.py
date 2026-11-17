# Parche 2.5.0a: firebase.js — mantenimientos (subscribe/upsert/delete/get/
# asignarFolio/guardarFirma/getAllMantenimientos) + runTransaction.
import io, sys

P = '/home/hatch/workspace/android/checklist-cloud/www/cloud/firebase.js'
s = io.open(P, encoding='utf-8').read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'NO ENCONTRADO o repetido (%d): %r' % (c, old[:90])
    s = s.replace(old, new)

# 1. Import runTransaction.
rep("""  addDoc,
  orderBy,
  limit,
  serverTimestamp
} from 'firebase/firestore';""",
"""  addDoc,
  orderBy,
  limit,
  runTransaction,
  serverTimestamp
} from 'firebase/firestore';""")

# 2. Funciones de mantenimientos, tras getAllPreparations.
rep("""async function getAllPreparations() {
  const snap = await getDocs(collection(db, 'preparations'));
  return snap.docs.map((d) => Object.assign({ id: d.id }, d.data()));
}""",
"""async function getAllPreparations() {
  const snap = await getDocs(collection(db, 'preparations'));
  return snap.docs.map((d) => Object.assign({ id: d.id }, d.data()));
}

// Mantenimientos preventivos (2.5.0): órdenes de servicio con folio.
// uidOpcional filtra por tecnicoUid (lo usan los usuarios normales para
// que las reglas permitan la lectura); sin él el admin suscribe todo.
function subscribeMantenimientos(cb, uidOpcional) {
  const q = uidOpcional
    ? query(collection(db, 'mantenimientos'), where('tecnicoUid', '==', uidOpcional))
    : collection(db, 'mantenimientos');
  return onSnapshot(
    q,
    (snap) => cb(snap.docs.map((d) => Object.assign({ id: d.id }, d.data()))),
    (err) => console.warn('[Cloud] Error en snapshot de mantenimientos:', err)
  );
}

async function upsertMant(m) {
  return setDoc(
    doc(db, 'mantenimientos', m.id),
    Object.assign({}, m, { updatedAt: Date.now() }),
    { merge: true }
  );
}

async function deleteMant(id) {
  return deleteDoc(doc(db, 'mantenimientos', id));
}

async function getMantenimiento(id) {
  const snap = await getDoc(doc(db, 'mantenimientos', id));
  return snap.exists() ? Object.assign({ id: snap.id }, snap.data()) : null;
}

async function getAllMantenimientos() {
  const snap = await getDocs(collection(db, 'mantenimientos'));
  return snap.docs.map((d) => Object.assign({ id: d.id }, d.data()));
}

// Folio de la orden de servicio (2.5.0): config/folios.siguiente empieza
// en 1; la transacción lee, asigna el folio con 5 dígitos y sube el
// contador, así dos teléfonos no repiten folio. El folio nunca se reutiliza.
async function asignarFolio() {
  const ref = doc(db, 'config', 'folios');
  return runTransaction(db, async (tx) => {
    const snap = await tx.get(ref);
    const n = (snap.exists() && typeof snap.data().siguiente === 'number') ? snap.data().siguiente : 1;
    tx.set(ref, { siguiente: n + 1 });
    return String(n).padStart(5, '0');
  });
}

// Firma del usuario desde la página pública de firma (2.5.0): guarda la
// firma y marca la orden como firmada. Las reglas solo permiten cambiar
// 'firma' y 'estado' (a 'firmada') sin sesión de técnico.
async function guardarFirma(id, firmaData) {
  return updateDoc(doc(db, 'mantenimientos', id), { firma: firmaData, estado: 'firmada' });
}""")

# 3. Exportar en window.Cloud.
rep("""  subscribePreparations,
  upsertPrep,
  deletePrep,
  getAllPreparations,""",
"""  subscribePreparations,
  upsertPrep,
  deletePrep,
  getAllPreparations,
  subscribeMantenimientos,
  upsertMant,
  deleteMant,
  getMantenimiento,
  getAllMantenimientos,
  asignarFolio,
  guardarFirma,""")

io.open(P, 'w', encoding='utf-8').write(s)
print('firebase.js OK')
