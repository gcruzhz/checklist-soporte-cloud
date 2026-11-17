#!/usr/bin/env python3
"""Parche 2.1.2a: Firebase — el admin edita nombre, usuario y correo de un usuario."""
P = '/home/hatch/workspace/android/checklist-cloud/www/cloud/firebase.js'
s = open(P).read()
orig = s

def rep(old, new, n=1):
    global s
    assert old in s, 'NO ENCONTRADO: ' + old[:90]
    s = s.replace(old, new, n)

# adminUpdateUser después de deleteUserByAdmin
rep("""async function deleteUserByAdmin(uid, usuario) {
  await deleteDoc(doc(db, 'users', uid));
  if (usuario) {
    await deleteDoc(doc(db, 'usernames', String(usuario).toLowerCase()));
  }
}""",
"""async function deleteUserByAdmin(uid, usuario) {
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
}""")

# Exportarla en window.Cloud (junto a las demás de admin)
rep("""  deleteUserByAdmin,""",
"""  deleteUserByAdmin,
  adminUpdateUser,""")

assert s != orig
open(P, 'w').write(s)
print('OK parche 2.1.2a (firebase.js) aplicado')
