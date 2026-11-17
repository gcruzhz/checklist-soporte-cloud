#!/usr/bin/env python3
"""Parche 2.1.2b: descripción inicial, animación de login y editar usuarios (admin)."""
P = '/home/hatch/workspace/android/checklist-cloud/www/index.html'
s = open(P).read()
orig = s

def rep(old, new, n=1):
    global s
    assert old in s, 'NO ENCONTRADO: ' + old[:90]
    s = s.replace(old, new, n)

# ---------- 1. Versión visible ----------
rep('Versión 2.1.1', 'Versión 2.1.2')
rep('Versión: 2.1.1', 'Versión: 2.1.2')
rep('Checklist de Soporte 2.1.1', 'Checklist de Soporte 2.1.2')
rep('Versión de la app: 2.1.1', 'Versión de la app: 2.1.2')

# ---------- 2. Descripción inicial ----------
rep('Entra con tu usuario para ver y registrar los equipos de renta.',
    'Ingresa con tu usuario para ver y registrar equipos.')

# ---------- 3. Animación del login: logo flotante + entrada de la tarjeta ----------
rep("  #loginView .login-card { background: #fff; border-radius: 14px; padding: 20px; width: 100%; max-width: 380px; box-shadow: 0 4px 20px rgba(0,0,0,.3); }",
    "  #loginView .login-card { background: #fff; border-radius: 14px; padding: 20px; width: 100%; max-width: 380px; box-shadow: 0 4px 20px rgba(0,0,0,.3); animation: loginIn .45s ease both; }\n  #loginView .login-logo { width: 76px; height: 76px; object-fit: contain; display: block; margin: 0 auto 10px; animation: loginFloat 3s ease-in-out infinite; }\n  @keyframes loginFloat { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }\n  @keyframes loginIn { from { opacity: 0; transform: translateY(14px) scale(.98); } to { opacity: 1; transform: translateY(0) scale(1); } }")
rep("""  <div class="login-card">
    <h1>Checklist de Soporte</h1>""",
"""  <div class="login-card">
    <img class="login-logo" src="lab-icon.png" alt="Checklist de Soporte">
    <h1>Checklist de Soporte</h1>""")

# ---------- 4. Nota de Usuarios + panel de edición ----------
rep('Solo el administrador ve esta sección. Aquí se crean usuarios, se activan o desactivan y se cambia su rol.',
    'Solo el administrador ve esta sección. Aquí se crean usuarios, se editan sus datos, se activan o desactivan y se cambia su rol.')
rep("""      <button class="btn-green" id="btnUserAdd" style="width:100%">➕ Crear usuario</button>
    </div>
    <div id="userList"></div>""",
"""      <button class="btn-green" id="btnUserAdd" style="width:100%">➕ Crear usuario</button>
    </div>
    <div class="panel" id="userEditBox" hidden>
      <b>Editar usuario</b>
      <div class="grid2">
        <div class="field"><label>Nombre</label><input id="fEuNombre" placeholder="Nombre del usuario"></div>
        <div class="field"><label>Usuario</label><input id="fEuUsuario" placeholder="juanp (sin espacios)"></div>
        <div class="field"><label>Correo electrónico</label><input id="fEuCorreo" type="email" placeholder="usuario@correo.com"></div>
      </div>
      <div class="share-note">El correo con el que entra el usuario no cambia: este correo es el de contacto y para recuperar la contraseña.</div>
      <div class="actions"><button class="btn-green" id="btnEuGuardar">Guardar cambios</button><button class="btn-ghost" id="btnEuCancelar">Cancelar</button></div>
    </div>
    <div id="userList"></div>""")

# ---------- 5. Botón Editar en cada tarjeta de usuario ----------
rep("""        '<button class="btn-ghost" data-user-pass="' + u.uid + '">Contraseña</button>' +""",
"""        '<button class="btn-ghost" data-user-pass="' + u.uid + '">Contraseña</button>' +
        '<button class="btn-ghost" data-user-edit="' + u.uid + '">Editar</button>' +""")

# ---------- 6. Abrir la edición desde la lista (antes del bloqueo de cambios propios) ----------
rep("""  var tog = t.closest('[data-user-toggle]');
  var rol = t.closest('[data-user-role]');
  var del = t.closest('[data-user-del]');
  var unl = t.closest('[data-user-unlock]');
  var pas = t.closest('[data-user-pass]');
  if (!tog && !rol && !del && !unl && !pas) return;
  var uid = (tog || rol || del || unl || pas).getAttribute(tog ? 'data-user-toggle' : rol ? 'data-user-role' : del ? 'data-user-del' : unl ? 'data-user-unlock' : 'data-user-pass');
  var u = lastUsers.find(function (x) { return x.uid === uid; });
  if (!u) return;
  if (uid === cloudUser.uid) { alert('No puedes cambiar tu propio usuario desde aquí.'); return; }""",
"""  var tog = t.closest('[data-user-toggle]');
  var rol = t.closest('[data-user-role]');
  var del = t.closest('[data-user-del]');
  var unl = t.closest('[data-user-unlock]');
  var pas = t.closest('[data-user-pass]');
  var edt = t.closest('[data-user-edit]');
  if (!tog && !rol && !del && !unl && !pas && !edt) return;
  var uid = (tog || rol || del || unl || pas || edt).getAttribute(tog ? 'data-user-toggle' : rol ? 'data-user-role' : del ? 'data-user-del' : unl ? 'data-user-unlock' : pas ? 'data-user-pass' : 'data-user-edit');
  var u = lastUsers.find(function (x) { return x.uid === uid; });
  if (!u) return;
  if (edt) {
    window._editUserUid = uid;
    window._editUserOld = u.usuario || '';
    document.getElementById('fEuNombre').value = u.nombre || '';
    document.getElementById('fEuUsuario').value = u.usuario || '';
    document.getElementById('fEuCorreo').value = u.email || '';
    document.getElementById('userEditBox').hidden = false;
    return;
  }
  if (uid === cloudUser.uid) { alert('No puedes cambiar tu propio usuario desde aquí.'); return; }""")

# ---------- 7. Guardar / cancelar la edición ----------
rep("""document.getElementById('btnReportar').addEventListener('click', function () {""",
"""document.getElementById('btnEuCancelar').addEventListener('click', function () {
  document.getElementById('userEditBox').hidden = true;
  window._editUserUid = null;
});
document.getElementById('btnEuGuardar').addEventListener('click', function () {
  var uid = window._editUserUid;
  if (!uid) return;
  var nombre = document.getElementById('fEuNombre').value.trim();
  var usuario = document.getElementById('fEuUsuario').value.trim().toLowerCase();
  var email = document.getElementById('fEuCorreo').value.trim();
  if (!nombre || !usuario) { alert('Escribe el nombre y el usuario.'); return; }
  if (!/^[a-z0-9._-]+$/.test(usuario)) { alert('El usuario solo puede tener letras, números, puntos, guiones y guion bajo, sin espacios.'); return; }
  if (email && email.indexOf('@') === -1) { alert('El correo no es válido.'); return; }
  window.Cloud.adminUpdateUser(uid, window._editUserOld || '', { nombre: nombre, usuario: usuario, email: email }).then(function () {
    document.getElementById('userEditBox').hidden = true;
    window._editUserUid = null;
    renderUsuarios();
  }).catch(function (er) {
    alert((er && er.code === 'auth/email-already-in-use') ? 'Ese usuario ya está registrado por otro.' : 'No se pudo guardar los cambios.');
  });
});
document.getElementById('btnReportar').addEventListener('click', function () {""")

assert s != orig
open(P, 'w').write(s)
print('OK parche 2.1.2b (index.html) aplicado')
print('Quedan "2.1.1":', len(__import__('re').findall(r'2\.1\.1', s)))
print('Quedan descripción vieja:', 'equipos de renta.' in s)
