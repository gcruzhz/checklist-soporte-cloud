// Módulo Firebase para Checklist de Soporte 2.0 (nube).
// Entry point ESM; se empaqueta con esbuild a www/cloud/firebase.bundle.js
// y expone window.Cloud. Sin config real (PLACEHOLDER) la app sigue en modo LOCAL.
import { initializeApp, getApp } from 'firebase/app';
import {
  getAuth,
  setPersistence,
  browserLocalPersistence,
  browserSessionPersistence,
  onAuthStateChanged,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signOut as firebaseSignOut,
  EmailAuthProvider,
  reauthenticateWithCredential,
  updatePassword,
  sendPasswordResetEmail
} from 'firebase/auth';
import {
  initializeFirestore,
  getFirestore,
  persistentLocalCache,
  collection,
  doc,
  getDoc,
  getDocFromServer,
  getDocs,
  setDoc,
  updateDoc,
  deleteDoc,
  onSnapshot,
  query,
  where,
  addDoc,
  orderBy,
  limit,
  runTransaction,
  serverTimestamp
} from 'firebase/firestore';

let auth = null;
let db = null;
let config = null;

async function init(cfg) {
  if (!cfg || !cfg.apiKey || cfg.apiKey === 'TU_API_KEY') return false;
  config = cfg;
  const app = initializeApp(config);
  auth = getAuth(app);
  try {
    await setPersistence(auth, browserLocalPersistence);
  } catch (e) {
    console.warn('[Cloud] No se pudo fijar persistencia local de auth:', e);
  }
  try {
    db = initializeFirestore(app, { localCache: persistentLocalCache({}) });
  } catch (e) {
    console.warn('[Cloud] persistentLocalCache no disponible, usando Firestore normal:', e);
    db = getFirestore(app);
  }
  return true;
}

function onAuth(cb) {
  return onAuthStateChanged(auth, cb);
}

function currentUser() {
  return auth ? auth.currentUser : null;
}

async function signIn(email, password) {
  return signInWithEmailAndPassword(auth, email, password);
}

async function signOut() {
  return firebaseSignOut(auth);
}

// Recordar sesión: true = la sesión sobrevive al cerrar la app (local),
// false = la sesión termina al cerrar la app (session).
async function setPersistenceMode(remember) {
  await setPersistence(auth, remember ? browserLocalPersistence : browserSessionPersistence);
}

// Resuelve un nombre de usuario a su registro de acceso
// { email (correo de Auth), uid, rol } o null si no existe.
async function resolveUsername(username) {
  const snap = await getDoc(doc(db, 'usernames', String(username || '').toLowerCase()));
  return snap.exists() ? snap.data() : null;
}

// Resuelve un correo (real o de acceso) a su registro de acceso.
// Busca por el correo de Auth y por el correo real guardado en el mapeo.
async function resolveEmail(email) {
  const em = String(email || '').toLowerCase();
  let snap = await getDocs(query(collection(db, 'usernames'), where('email', '==', em)));
  if (snap.empty) {
    snap = await getDocs(query(collection(db, 'usernames'), where('emailReal', '==', em)));
  }
  if (snap.empty) return null;
  return snap.docs[0].data();
}

async function getUserDoc(uid) {
  // Lectura directa del servidor: la caché local puede guardar que el
  // documento "no existe" si se leyó durante el alta, antes de guardarse.
  const snap = await getDocFromServer(doc(db, 'users', uid));
  return snap.exists() ? snap.data() : null;
}

// (254) Suscripción en vivo al documento del usuario: el bloqueo de
// Mantenimientos aplica sin cerrar sesión (el admin lo cambia y la app
// del usuario lo ve llegar).
function subscribeUserDoc(uid, cb) {
  return onSnapshot(doc(db, 'users', uid),
    (snap) => cb(snap.exists() ? snap.data() : null),
    (err) => console.warn('[Cloud] Error en snapshot de usuario:', err));
}

async function getRole(uid) {
  const data = await getUserDoc(uid);
  return data ? (data.rol || null) : null;
}

async function isInitialized() {
  const snap = await getDocFromServer(doc(db, 'config', 'admin'));
  const data = snap.exists() ? snap.data() : null;
  return !!(data && data.initialized === true);
}

async function bootstrapAdmin({ nombre, email, password }) {
  const cred = await createUserWithEmailAndPassword(auth, email, password);
  const user = cred.user;
  await setDoc(doc(db, 'users', user.uid), {
    email,
    nombre,
    rol: 'admin',
    activo: true,
    createdAt: Date.now()
  });
  await setDoc(doc(db, 'config', 'admin'), { initialized: true });
  return user;
}

// Completa el alta de un administrador que quedó a medio crear:
// el usuario ya existe en Auth pero su documento en 'users' no se guardó
// (o el flag config/admin tampoco). Lo deja como admin y marca inicializado.
async function repairAdmin(uid, email) {
  const nombre = (email || 'Admin').split('@')[0] || 'Admin';
  await setDoc(doc(db, 'users', uid), {
    email,
    nombre,
    rol: 'admin',
    activo: true,
    createdAt: Date.now()
  });
  await setDoc(doc(db, 'config', 'admin'), { initialized: true });
  return true;
}

async function listUsers() {
  const snap = await getDocs(collection(db, 'users'));
  const users = snap.docs.map((d) => Object.assign({ uid: d.id }, d.data()));
  users.sort((a, b) => (a.createdAt || 0) - (b.createdAt || 0));
  return users;
}

async function createUserByAdmin({ email, password, nombre, usuario, rol }) {
  // Segunda instancia de app para no cerrar la sesión del admin principal.
  let secondaryApp;
  try {
    secondaryApp = getApp('admin-helper');
  } catch (e) {
    secondaryApp = initializeApp(config, 'admin-helper');
  }
  const secondaryAuth = getAuth(secondaryApp);
  // Duplicado: mismo usuario o mismo correo que un usuario activo.
  // Se revisa ANTES de crear la cuenta: si el correo es nuevo pero el
  // usuario ya existe, Auth lo aceptaría y se robaría el nombre.
  const existing = await listUsers();
  const dup = existing.some((u) =>
    (u.email || '').toLowerCase() === String(email).toLowerCase() ||
    (usuario && (u.usuario || '').toLowerCase() === String(usuario).toLowerCase()));
  if (dup) {
    const err = new Error('duplicate');
    err.code = 'auth/email-already-in-use';
    throw err;
  }
  let authEmail = email;
  let uid;
  try {
    const cred = await createUserWithEmailAndPassword(secondaryAuth, email, password);
    uid = cred.user.uid;
  } catch (e) {
    if (e.code !== 'auth/email-already-in-use') throw e;
    // El correo ya existe en Auth pero sin perfil: es un huérfano de un
    // borrado anterior. Intentar entrar con la contraseña escrita para
    // recuperar su uid y que siga con esa contraseña.
    try {
      const rec = await signInWithEmailAndPassword(secondaryAuth, email, password);
      uid = rec.user.uid;
      await firebaseSignOut(secondaryAuth);
    } catch (e2) {
      // Contraseña distinta: crear cuenta nueva con correo versionado
      // (usuario.2@checklist.local, .3, ...) y que el acceso siga
      // funcionando por nombre de usuario.
      const base = (usuario || String(email).split('@')[0]).toLowerCase();
      let n = String(email).endsWith('@checklist.local') ? 2 : 1;
      while (true) {
        const cand = n === 1 ? base + '@checklist.local' : base + '.' + n + '@checklist.local';
        try {
          const c = await createUserWithEmailAndPassword(secondaryAuth, cand, password);
          uid = c.user.uid;
          authEmail = cand;
          break;
        } catch (e3) {
          if (e3.code === 'auth/email-already-in-use') {
            n++;
            if (n > 20) throw e3;
            continue;
          }
          throw e3;
        }
      }
    }
  }
  await setDoc(doc(db, 'users', uid), {
    email,
    nombre,
    usuario: usuario || '',
    rol,
    activo: true,
    createdAt: Date.now()
  });
  if (usuario) {
    await setDoc(doc(db, 'usernames', String(usuario).toLowerCase()), { email: authEmail, uid, rol, emailReal: email });
  }
  await firebaseSignOut(secondaryAuth);
  return uid;
}

// Cambia la contraseña de un usuario (lo hace el admin): borra su perfil
// y lo vuelve a crear con la contraseña nueva. Si el usuario tenía una
// cuenta huérfana con otra contraseña, se crea con correo versionado y
// el acceso por nombre de usuario sigue funcionando.
async function adminResetPassword({ uid, usuario, email, nombre, rol, newPassword }) {
  await deleteUserByAdmin(uid, usuario);
  await unlockUser(uid);
  const newUid = await createUserByAdmin({ email, password: newPassword, nombre, usuario, rol });
  await unlockUser(newUid);
  return newUid;
}

// Envía el correo para restablecer la contraseña (olvidó su contraseña).
async function sendPasswordReset(email) {
  return sendPasswordResetEmail(auth, email);
}

// El usuario cambia su propia contraseña: pide la actual para verificar.
async function changeOwnPassword(currentPassword, newPassword) {
  const user = auth.currentUser;
  if (!user) throw new Error('no-session');
  const cred = EmailAuthProvider.credential(user.email, currentPassword);
  await reauthenticateWithCredential(user, cred);
  await updatePassword(user, newPassword);
}

async function setUserActive(uid, activo) {
  return updateDoc(doc(db, 'users', uid), { activo });
}

async function setUserRole(uid, rol) {
  await setDoc(doc(db, 'users', uid), { rol }, { merge: true });
  const snap = await getDoc(doc(db, 'users', uid));
  const usuario = snap.exists() ? (snap.data().usuario || '') : '';
  if (usuario) {
    await setDoc(doc(db, 'usernames', String(usuario).toLowerCase()), { rol }, { merge: true });
  }
}

// (254) Bloqueo de Mantenimientos por usuario (solo admin; las reglas ya
// permiten update de users/{uid} solo al admin). No desactiva al usuario:
// solo le cierra Mantenimientos. El admin nunca se bloquea a sí mismo
// (la app no muestra el botón en su propia fila ni en otros admins).
async function setMantBloqueado(uid, bloqueado) {
  return updateDoc(doc(db, 'users', uid), { mantBloqueado: !!bloqueado });
}

// Elimina al usuario de la app: borra su perfil y su nombre de usuario.
// Sin perfil ya no puede entrar (aunque su registro de acceso en Firebase
// siga existiendo, queda inservible y se puede borrar desde la consola).
async function deleteUserByAdmin(uid, usuario) {
  await deleteDoc(doc(db, 'users', uid));
  if (usuario) {
    await deleteDoc(doc(db, 'usernames', String(usuario).toLowerCase()));
  }
}

// El admin edita nombre, usuario y correo de un usuario.
// El correo que se cambia es el de contacto (users.email y emailReal del
// mapeo, que es el que se usa para recuperar la contraseña); el correo de
// acceso (Auth y mapping.email) no cambia, porque solo el propio usuario
// puede cambiarlo. Si después el admin le cambia la contraseña, la cuenta
// se recrea con el correo nuevo y ese pasa a ser también el de acceso.
// Clave de la IA (Gemini): el admin la guarda una vez en config/ai y todos
// los teléfonos la leen al entrar. La clave en sí la crea el admin gratis
// en Google AI Studio.
async function getAiKey() {
  const snap = await getDoc(doc(db, 'config', 'ai'));
  return snap.exists() ? (snap.data().key || '') : '';
}
async function setAiKey(key) {
  await setDoc(doc(db, 'config', 'ai'), { key: key || '' }, { merge: true });
}
// Clave de DeepSeek (respaldo): mismo documento config/ai, otro campo, para
// que guardar una clave no borre la otra. DeepSeek cobra por uso (muy barato).
async function getDeepseekKey() {
  const snap = await getDoc(doc(db, 'config', 'ai'));
  return snap.exists() ? (snap.data().deepseekKey || '') : '';
}
async function setDeepseekKey(key) {
  await setDoc(doc(db, 'config', 'ai'), { deepseekKey: key || '' }, { merge: true });
}

async function adminUpdateUser(uid, oldUsuario, { nombre, usuario, email }) {
  const users = await listUsers();
  const u = users.find((x) => x.uid === uid);
  if (!u) {
    const err = new Error('not-found');
    err.code = 'not-found';
    throw err;
  }
  const newUsuario = (usuario || '').trim().toLowerCase();
  const oldU = (oldUsuario || '').trim().toLowerCase();
  // El nuevo nombre de usuario no puede ser de otro usuario activo.
  if (newUsuario && newUsuario !== oldU) {
    const taken = users.some((x) => x.uid !== uid && (x.usuario || '').toLowerCase() === newUsuario);
    if (taken) {
      const err = new Error('duplicate');
      err.code = 'auth/email-already-in-use';
      throw err;
    }
  }
  const newEmail = (email || '').trim();
  await updateDoc(doc(db, 'users', uid), { nombre: nombre, usuario: newUsuario, email: newEmail });
  // Mapeo de nombre de usuario: renombrar o crear.
  if (newUsuario !== oldU) {
    let loginEmail = u.email || '';
    let rol = u.rol || 'usuario';
    if (oldU) {
      const oldSnap = await getDoc(doc(db, 'usernames', oldU));
      if (oldSnap.exists()) {
        const d = oldSnap.data();
        loginEmail = d.email || loginEmail;
        rol = d.rol || rol;
      }
      await deleteDoc(doc(db, 'usernames', oldU));
    }
    if (newUsuario) {
      await setDoc(doc(db, 'usernames', newUsuario), { email: loginEmail, uid: uid, rol: rol, emailReal: newEmail });
    }
  } else if (oldU) {
    // Mismo usuario, solo cambia el correo de contacto.
    await updateDoc(doc(db, 'usernames', oldU), { emailReal: newEmail });
  }
}

const MAX_LOGIN_ATTEMPTS = 10;

async function getLoginLock(uid) {
  const snap = await getDoc(doc(db, 'loginAttempts', uid));
  return snap.exists() ? snap.data() : null;
}

async function recordLoginFailure(uid, email) {
  const cur = await getLoginLock(uid);
  const count = (cur && cur.count ? cur.count : 0) + 1;
  const locked = count >= MAX_LOGIN_ATTEMPTS;
  await setDoc(doc(db, 'loginAttempts', uid), { count, locked, email: email || '', updatedAt: Date.now() });
  return { count, locked };
}

async function resetLoginLock(uid) {
  await setDoc(doc(db, 'loginAttempts', uid), { count: 0, locked: false, updatedAt: Date.now() });
}

// Desbloquea una cuenta (lo usa el admin): borra su registro de intentos.
async function unlockUser(uid) {
  await deleteDoc(doc(db, 'loginAttempts', uid));
}

async function listLoginLocks() {
  const snap = await getDocs(collection(db, 'loginAttempts'));
  return snap.docs.map((d) => Object.assign({ uid: d.id }, d.data()));
}

function subscribeRenta(cb) {
  return onSnapshot(
    collection(db, 'renta'),
    (snap) => cb(snap.docs.map((d) => Object.assign({ id: d.id }, d.data()))),
    (err) => console.warn('[Cloud] Error en snapshot de renta:', err)
  );
}

async function upsertRenta(rec) {
  return setDoc(
    doc(db, 'renta', rec.id),
    Object.assign({}, rec, { updatedAt: Date.now() }),
    { merge: true }
  );
}

async function deleteRenta(id) {
  return deleteDoc(doc(db, 'renta', id));
}

async function getAllRenta() {
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
}

// Responsivas en blanco (2.5.13): el técnico crea el documento (estado
// 'pendiente', sin datos) y comparte el enlace público
// responsiva.html?id=<id>; el colaborador lo llena sin sesión y la app
// lo ve llegar por la suscripción. El id aleatorio del documento es el
// secreto del enlace, igual que la firma de Mantenimientos.
// uidOpcional filtra por creadoPor (lo usan los usuarios normales para
// que las reglas permitan la lectura); sin él el admin suscribe todo.
async function crearResponsiva(creadoPorNombre) {
  const u = auth.currentUser;
  if (!u) throw new Error('no-auth');
  const ref = doc(collection(db, 'responsivas'));
  await setDoc(ref, {
    creadoPor: u.uid,
    creadoPorNombre: creadoPorNombre || u.email || '',
    creadoEn: Date.now(),
    estado: 'pendiente',
    datos: null
  });
  return ref.id;
}

function subscribeResponsivas(cb, uidOpcional) {
  const q = uidOpcional
    ? query(collection(db, 'responsivas'), where('creadoPor', '==', uidOpcional))
    : collection(db, 'responsivas');
  return onSnapshot(
    q,
    (snap) => cb(snap.docs.map((d) => Object.assign({ id: d.id }, d.data()))),
    (err) => console.warn('[Cloud] Error en snapshot de responsivas:', err)
  );
}

// Archivar responsivas (2.5.14): archivar NO borra nada; solo marca
// archivado + archivadoEn (restaurar pone archivado=false y
// archivadoEn=null). Las reglas ya lo permiten: la rama update
// propio/admin no restringe campos, así que firestore.rules NO se
// toca. La suscripción devuelve los docs y el filtrado es en la app.
async function archivarResponsiva(id, archivado) {
  return updateDoc(doc(db, 'responsivas', id), archivado
    ? { archivado: true, archivadoEn: Date.now() }
    : { archivado: false, archivadoEn: null });
}

// Acuses de Sistemas (2.5.16): acuse de recibido de documentos, sin
// folio y sin página pública. El documento lleva creadoPor,
// creadoPorNombre, creadoEn y datos {fecha, para, de, anexo}.
// uidOpcional filtra por creadoPor (lo usan los usuarios normales para
// que las reglas permitan la lectura); sin él el admin suscribe todo.
async function crearAcuse(datos, creadoPorNombre) {
  const u = auth.currentUser;
  if (!u) throw new Error('no-auth');
  const ref = doc(collection(db, 'acuses'));
  await setDoc(ref, {
    creadoPor: u.uid,
    creadoPorNombre: creadoPorNombre || u.email || '',
    creadoEn: Date.now(),
    datos: datos || {}
  });
  return ref.id;
}

function subscribeAcuses(cb, uidOpcional) {
  const q = uidOpcional
    ? query(collection(db, 'acuses'), where('creadoPor', '==', uidOpcional))
    : collection(db, 'acuses');
  return onSnapshot(
    q,
    (snap) => cb(snap.docs.map((d) => Object.assign({ id: d.id }, d.data()))),
    (err) => console.warn('[Cloud] Error en snapshot de acuses:', err)
  );
}

async function upsertAcuse(rec) {
  return setDoc(
    doc(db, 'acuses', rec.id),
    Object.assign({}, rec, { updatedAt: Date.now() }),
    { merge: true }
  );
}

async function deleteAcuse(id) {
  return deleteDoc(doc(db, 'acuses', id));
}

async function getAcuse(id) {
  const snap = await getDoc(doc(db, 'acuses', id));
  return snap.exists() ? Object.assign({ id: snap.id }, snap.data()) : null;
}

// Folio de la carta responsiva (2.5.16): config/foliosCarta.siguiente
// empieza en 1; la transacción lee, asigna el folio con 5 dígitos y
// sube el contador, así dos teléfonos no repiten folio. Espejo de
// asignarFolio() (config/folios de Mantenimientos).
async function asignarFolioCarta() {
  const ref = doc(db, 'config', 'foliosCarta');
  return runTransaction(db, async (tx) => {
    const snap = await tx.get(ref);
    const n = (snap.exists() && typeof snap.data().siguiente === 'number') ? snap.data().siguiente : 1;
    tx.set(ref, { siguiente: n + 1 });
    return String(n).padStart(5, '0');
  });
}

// Cartas Responsivas FO-SI-10 (2.5.16): resguardo y uso de equipo de
// cómputo. El folio se asigna al guardar (crearCarta lo pide con
// asignarFolioCarta); el documento lleva creadoPor, creadoPorNombre,
// creadoEn, folio y datos {fecha, nombre, colaborador, sucursal,
// puesto, jefe, ip, observaciones, equipos: [{modelo, marca, serie,
// concepto}]}. Sin página pública: solo el técnico y el admin.
async function crearCarta(datos, creadoPorNombre) {
  const u = auth.currentUser;
  if (!u) throw new Error('no-auth');
  const folio = await asignarFolioCarta();
  const ref = doc(collection(db, 'cartas'));
  await setDoc(ref, {
    creadoPor: u.uid,
    creadoPorNombre: creadoPorNombre || u.email || '',
    creadoEn: Date.now(),
    folio: folio,
    datos: datos || {}
  });
  return { id: ref.id, folio: folio };
}

function subscribeCartas(cb, uidOpcional) {
  const q = uidOpcional
    ? query(collection(db, 'cartas'), where('creadoPor', '==', uidOpcional))
    : collection(db, 'cartas');
  return onSnapshot(
    q,
    (snap) => cb(snap.docs.map((d) => Object.assign({ id: d.id }, d.data()))),
    (err) => console.warn('[Cloud] Error en snapshot de cartas:', err)
  );
}

async function upsertCarta(rec) {
  return setDoc(
    doc(db, 'cartas', rec.id),
    Object.assign({}, rec, { updatedAt: Date.now() }),
    { merge: true }
  );
}

async function deleteCarta(id) {
  return deleteDoc(doc(db, 'cartas', id));
}

async function getCarta(id) {
  const snap = await getDoc(doc(db, 'cartas', id));
  return snap.exists() ? Object.assign({ id: snap.id }, snap.data()) : null;
}

// Equipos detectados (2.3.3): el detector de escritorio reporta los equipos
// que ve en la red (colección detectados) y los teléfonos los listan para
// usarlos en un equipo nuevo o descartarlos. El id es info.machineId cuando
// viene (serie real, si no hostname + '-' + MAC sin ':' ni '-'; lo calcula
// el detector de escritorio); si no viene, el respaldo viejo: la serie si
// existe, si no hostname + '-' + detectadoEn. Cada detección nueva pone
// usado=false y detectadoEn=ahora, así que volver a detectar un equipo ya
// usado lo trae de vuelta al panel.
async function reportDetected(info) {
  const d = Object.assign({}, info || {});
  if (d.machineId) d.id = String(d.machineId);
  else if (!d.id) d.id = d.serie ? String(d.serie) : (d.hostname || '') + '-' + (d.detectadoEn || Date.now());
  d.detectadoEn = Date.now();
  d.usado = false;
  return setDoc(doc(db, 'detectados', String(d.id)), d, { merge: true });
}
function subscribeDetectados(cb) {
  return onSnapshot(
    query(collection(db, 'detectados'), orderBy('detectadoEn', 'desc'), limit(50)),
    (snap) => cb(snap.docs.map((d) => Object.assign({ id: d.id }, d.data()))),
    (err) => console.warn('[Cloud] Error en snapshot de detectados:', err)
  );
}
async function deleteDetectado(id) {
  return deleteDoc(doc(db, 'detectados', id));
}
async function markDetectadoUsado(id) {
  return updateDoc(doc(db, 'detectados', id), { usado: true });
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
}

// Chat efímero: borra los mensajes de más de 24 horas (el chat no guarda
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
}

// Moderación: el admin puede borrar cualquier mensaje, del chat del
// equipo o de un chat individual (las reglas ya lo permiten).
async function deleteChatMessage(id) {
  return deleteDoc(doc(db, 'chat', id));
}
async function deleteDmMessage(id) {
  return deleteDoc(doc(db, 'dm', id));
}

window.Cloud = {
  init,
  onAuth,
  currentUser,
  signIn,
  signOut,
  setPersistenceMode,
  resolveUsername,
  resolveEmail,
  getLoginLock,
  recordLoginFailure,
  resetLoginLock,
  unlockUser,
  listLoginLocks,
  adminResetPassword,
  changeOwnPassword,
  sendPasswordReset,
  getUserDoc,
  subscribeUserDoc,
  getRole,
  isInitialized,
  bootstrapAdmin,
  repairAdmin,
  listUsers,
  createUserByAdmin,
  setUserActive,
  setUserRole,
  setMantBloqueado,
  deleteUserByAdmin,
  adminUpdateUser,
  getAiKey,
  setAiKey,
  getDeepseekKey,
  setDeepseekKey,
  subscribeRenta,
  upsertRenta,
  deleteRenta,
  getAllRenta,
  subscribePreparations,
  upsertPrep,
  deletePrep,
  getAllPreparations,
  subscribeMantenimientos,
  upsertMant,
  deleteMant,
  getMantenimiento,
  getAllMantenimientos,
  asignarFolio,
  guardarFirma,
  crearResponsiva,
  subscribeResponsivas,
  archivarResponsiva,
  crearAcuse,
  subscribeAcuses,
  upsertAcuse,
  deleteAcuse,
  getAcuse,
  asignarFolioCarta,
  crearCarta,
  subscribeCartas,
  upsertCarta,
  deleteCarta,
  getCarta,
  reportDetected,
  subscribeDetectados,
  deleteDetectado,
  markDetectadoUsado,
  heartbeat,
  subscribePresence,
  clearPresence,
  subscribeChat,
  sendChat,
  pruneChat,
  subscribeDm,
  sendDm,
  deleteChatMessage,
  deleteDmMessage
};

export default window.Cloud;
