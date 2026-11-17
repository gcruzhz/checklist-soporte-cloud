#!/usr/bin/env python3
"""Parche 2.1.3b: la interfaz no se muestra antes de decidir si hay sesión."""
P = '/home/hatch/workspace/android/checklist-cloud/www/index.html'
s = open(P).read()
orig = s

def rep(old, new, n=1):
    global s
    assert old in s, 'NO ENCONTRADO: ' + old[:90]
    s = s.replace(old, new, n)

# ---------- 1. Versión visible ----------
rep('Versión 2.1.2', 'Versión 2.1.3')
rep('Versión: 2.1.2', 'Versión: 2.1.3')
rep('Checklist de Soporte 2.1.2', 'Checklist de Soporte 2.1.3')
rep('Versión de la app: 2.1.2', 'Versión de la app: 2.1.3')

# ---------- 2. La interfaz nace oculta: solo se muestra con sesión (o en modo local) ----------
rep('<header id="appHeader">', '<header id="appHeader" hidden>')
rep('<main id="mainApp">', '<main id="mainApp" hidden>')

# ---------- 3. El splash espera a que la app decida qué mostrar ----------
rep("""async function onAuthChanged(user) {
  if (!user) {
    cloudUser = null; cloudRole = null;
    if (cloudUnsub) { cloudUnsub(); cloudUnsub = null; }
    if (cloudPrepUnsub) { cloudPrepUnsub(); cloudPrepUnsub = null; }
    document.getElementById('mainApp').hidden = true;
    document.getElementById('appHeader').hidden = true;
    document.getElementById('loginView').hidden = false;
    checkBootstrap();
    return;
  }""",
"""async function onAuthChanged(user) {
  if (!user) {
    cloudUser = null; cloudRole = null;
    if (cloudUnsub) { cloudUnsub(); cloudUnsub = null; }
    if (cloudPrepUnsub) { cloudPrepUnsub(); cloudPrepUnsub = null; }
    document.getElementById('mainApp').hidden = true;
    document.getElementById('appHeader').hidden = true;
    document.getElementById('loginView').hidden = false;
    checkBootstrap();
    _authReady = true;
    return;
  }""")
rep("""    if (doc && doc.activo === false) {
      document.getElementById('loginError').textContent = 'Tu usuario está desactivado. Contacta al administrador.';
      await window.Cloud.signOut();
      return;
    }""",
"""    if (doc && doc.activo === false) {
      document.getElementById('loginError').textContent = 'Tu usuario está desactivado. Contacta al administrador.';
      await window.Cloud.signOut();
      _authReady = true;
      return;
    }""")
rep("""    document.getElementById('btnReintentarLogin').hidden = false;
    return;
  }""",
"""    document.getElementById('btnReintentarLogin').hidden = false;
    _authReady = true;
    return;
  }""")
rep("""    startEquipo();
    render();
  } catch (e) {
    document.getElementById('loginError').textContent = 'No se pudo verificar tu usuario. Revisa tu conexión.' + (e && e.code ? ' (' + e.code + ')' : '');
  }
}""",
"""    startEquipo();
    render();
    _authReady = true;
  } catch (e) {
    document.getElementById('loginError').textContent = 'No se pudo verificar tu usuario. Revisa tu conexión.' + (e && e.code ? ' (' + e.code + ')' : '');
    _authReady = true;
  }
}""")

# ---------- 4. boot(): en modo local se muestra la interfaz; si no, se espera al login ----------
rep("""async function boot() {
  if (!CLOUD_ENABLED) { render(); return; }
  var ok = false;
  try { ok = window.Cloud && await window.Cloud.init(window.FIREBASE_CONFIG); } catch (e) { ok = false; }
  if (!ok) { CLOUD_ENABLED = false; render(); return; }""",
"""var _authReady = false;
async function boot() {
  if (!CLOUD_ENABLED) { document.getElementById('mainApp').hidden = false; document.getElementById('appHeader').hidden = false; _authReady = true; render(); return; }
  var ok = false;
  try { ok = window.Cloud && await window.Cloud.init(window.FIREBASE_CONFIG); } catch (e) { ok = false; }
  if (!ok) { CLOUD_ENABLED = false; document.getElementById('mainApp').hidden = false; document.getElementById('appHeader').hidden = false; _authReady = true; render(); return; }""")

# ---------- 5. El splash no se quita hasta que ya se decidió qué mostrar ----------
rep("""boot();
setTimeout(function () { document.getElementById('atom').classList.add('form'); }, 1400);
setTimeout(function () { document.getElementById('splash').classList.add('hide'); }, 2400);
setTimeout(function () { var s = document.getElementById('splash'); if (s) s.remove(); }, 3000);""",
"""boot();
// El splash no se quita hasta que la app ya decidió qué mostrar (login o
// interfaz): si se quitara antes, se vería la interfaz como si la sesión
// ya estuviera iniciada. Último recurso: a los 9 s se quita de todos modos.
function hideSplash() {
  var s = document.getElementById('splash');
  if (!s) return;
  if (!_authReady) { setTimeout(hideSplash, 400); return; }
  s.classList.add('hide');
  setTimeout(function () { var s2 = document.getElementById('splash'); if (s2) s2.remove(); }, 500);
}
setTimeout(function () { document.getElementById('atom').classList.add('form'); }, 1400);
setTimeout(hideSplash, 2400);
setTimeout(function () { _authReady = true; hideSplash(); }, 9000);""")

assert s != orig
open(P, 'w').write(s)
print('OK parche 2.1.3b (index.html) aplicado')
print('Quedan "2.1.2":', len(__import__('re').findall(r'2\.1\.2', s)))
