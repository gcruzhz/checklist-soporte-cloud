#!/usr/bin/env python3
"""Parche 240 (telefono): sin dialogos nativos + bug latente del borrador +
diagnostico de foco - Checklist de Soporte 2.4.0 (versionCode 53).

Pedido del coordinador (2026-11-15): eliminar TODOS los dialogos nativos
de www/index.html (71 alert( en 69 lineas y 11 confirm(, conteo real
medido en el archivo 2.3.9: dos lineas traen 2 alert( cada una, 2514 y
3515) y corregir el bug latente del borrador y anadir el diagnostico de
foco. La APK NO se compila aqui.

Decisiones documentadas:
- showToast(msg): div fijo no modal con pointer-events none, se
  auto-oculta a los ~3 s, SIN robar el foco (nunca .focus()) y SIN
  bloquear la ejecucion. Sustituye a los 71 alert( con reemplazo global
  (los 8 que vivian dentro de los textos viejos de confirm/prompt se
  reescriben antes con showToast directo; el reemplazo global afirma
  que quedan 63).
- showConfirm(msg): modal inline propio (div + botones Si/No) que
  devuelve Promise<boolean>. confirm() era sincrono y el modal es
  asincrono: los 11 call sites se adaptan a .then (o await en
  offerBiometrics, que ya era async) y solo continuan con Si. El modal
  solo recibe foco cuando el usuario hace clic en el; al cerrarlo no se
  fuerza el foco a ningun lado. No se cierra tocando fuera: igual que
  el dialogo nativo, exige elegir Si o No.
- showPrompt(msg): el unico prompt( (nueva contrasena del admin, 3512)
  es de la misma clase de riesgo (dialogo nativo que roba el foco) y se
  elimina tambien, con modal inline propio con input tipo password;
  Cancelar resuelve null igual que antes.
- Dependencia del bloqueo del alert: revisados los 71 sitios. Ningun
  flujo dependia de que el usuario leyera el aviso antes de seguir:
  casi todos son `alert(...); return;` o colas de promesa; los dos con
  codigo despues (btnPassSave: click en Cancelar tras 'Contrasena
  cambiada'; adminResetPassword: showToast + renderUsuarios) siguen
  funcionando porque el toast es un div fijo fuera de lo que se
  re-renderiza. En Detectar (2514) el boton se restaura de inmediato y
  el toast queda visible mientras tanto (antes el boton quedaba
  bloqueado hasta cerrar el dialogo).
- Bug latente del borrador: 'Usar este equipo' no limpiaba
  window._completarBorradorId ni el texto de #btnAdd (btnShowNew si
  lo hace, linea 2485). Se anaden las dos lineas copiadas tal cual de
  btnShowNew al inicio del handler 'Usar este equipo', antes de
  rellenar el formulario y de updateSaveBtn(). 'Guardar para despues'
  no abre el formulario (crea el borrador directo), asi que no deja
  ese estado pendiente: para abrir el form solo quedan btnShowNew
  (limpia), 'Usar este equipo' (ahora limpia) y 'Completar datos'
  (pone su propio id).
- Diagnostico de foco: linea #focusDiag en Acerca de con
  `Foco: si/no - Elemento activo: <id>`, actualizada por
  updateFocusDiag() en cada render() y en focus/blur de la ventana
  (con guarda typeof, para no romper el harness node).
- firebase.js SIN cambios -> NO se reconstruye el bundle (queda en
  496,903 bytes, md5 dabab404a2c6f4065639dc6f808d1bb3). No hay
  www/cloud/detect.js en el proyecto: no hay backup detect-*.bak.
- Version 2.3.9 -> 2.4.0 (27 ocurrencias en index.html, reemplazo
  global como en la 2.3.8/2.3.9: incluye los comentarios historicos);
  versionCode 52 -> 53; iOS MARKETING_VERSION y
  CURRENT_PROJECT_VERSION en sus dos lugares.
- tests: copia test20239.js a test20240.js, actualiza version y
  extraido, actualiza los tests viejos que usaban los stubs de
  alert/confirm al nuevo mecanismo (toast/modal, sin borrarlos) y
  anade la serie AZ; extrae tests/checklist20240.js.
Cada reemplazo con assert: si el texto viejo no esta, se para.
"""
import os
import shutil

CLOUD = '/home/hatch/workspace/android/checklist-cloud/'
HTML = CLOUD + 'www/index.html'
FB = CLOUD + 'www/cloud/firebase.js'
GRADLE = CLOUD + 'android/app/build.gradle'
PBX = CLOUD + 'ios/App/App.xcodeproj/project.pbxproj'
TEST_OLD = CLOUD + 'tests/test20239.js'
TEST_NEW = CLOUD + 'tests/test20240.js'
EXTRACT = CLOUD + 'tests/checklist20240.js'
BAK_HTML = CLOUD + 'tests/checklist-2.3.9.html.bak'
BAK_FB = CLOUD + 'tests/firebase-2.3.9.js.bak'


def rep(path, old, new, count=1):
    with open(path, encoding='utf-8') as f:
        s = f.read()
    assert old in s, 'NO ENCONTRADO en %s: %r' % (path, old[:90])
    assert s.count(old) == count, 'OCURRENCIAS=%d (esperadas %d) en %s: %r' % (s.count(old), count, path, old[:90])
    with open(path, 'w', encoding='utf-8') as f:
        f.write(s.replace(old, new, count) if count == 1 else s.replace(old, new))
    print('OK:', path.split('/')[-1], '->', new[:70].replace('\n', ' '))


# ---------- 0. Backups ----------
assert not os.path.exists(BAK_HTML), 'Ya existe %s' % BAK_HTML
shutil.copyfile(HTML, BAK_HTML)
print('OK: backup tests/checklist-2.3.9.html.bak')
assert not os.path.exists(BAK_FB), 'Ya existe %s' % BAK_FB
shutil.copyfile(FB, BAK_FB)
print('OK: backup tests/firebase-2.3.9.js.bak')

# ---------- 0b. Copia del test ----------
shutil.copyfile(TEST_OLD, TEST_NEW)
print('OK: test20239.js copiado a test20240.js')

# ---------- 0c. Conteos de partida ----------
with open(HTML, encoding='utf-8') as f:
    html0 = f.read()
assert html0.count('alert(') == 71, 'alert(=%d (esperados 71)' % html0.count('alert(')
assert html0.count('confirm(') == 11, 'confirm(=%d (esperados 11)' % html0.count('confirm(')
assert html0.count('prompt(') == 1, 'prompt(=%d (esperado 1)' % html0.count('prompt(')
assert html0.count('2.3.9') == 27, '2.3.9=%d (esperadas 27)' % html0.count('2.3.9')
print('OK: partida 71 alert(, 11 confirm(, 1 prompt(, 27 x 2.3.9')

# ---------- 1. CSS del toast y los modales ----------
rep(HTML,
    "  .line { font-size: 14px; margin-bottom: 4px; }\n</style>",
    r"""  .line { font-size: 14px; margin-bottom: 4px; }
  #toast { position: fixed; left: 50%; bottom: 24px; transform: translateX(-50%); max-width: 92vw; background: #0C322C; color: #fff; padding: 12px 16px; border-radius: 10px; font-size: 14px; box-shadow: 0 2px 10px rgba(0,0,0,.3); z-index: 70; pointer-events: none; }
  #toast[hidden] { display: none; }
  .modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,.45); z-index: 80; display: flex; align-items: center; justify-content: center; padding: 16px; }
  .modal-overlay[hidden] { display: none; }
  .confirm-box { background: #fff; border-radius: 12px; padding: 18px; max-width: 420px; width: 100%; box-shadow: 0 4px 20px rgba(0,0,0,.3); }
  .confirm-box p { margin: 0 0 14px; font-size: 15px; }
  .confirm-box .actions { justify-content: flex-end; margin-top: 0; }
  .confirm-box input { margin-bottom: 12px; }
</style>""")

# ---------- 2. Divs del toast y los modales, justo tras <body> ----------
rep(HTML,
    "<body>\n<div id=\"loginView\" hidden>",
    r"""<body>
<div id="toast" hidden></div>
<div class="modal-overlay" id="confirmModal" hidden>
  <div class="confirm-box">
    <p id="confirmMsg"></p>
    <div class="actions"><button class="btn-danger" id="confirmYes">Sí</button><button class="btn-ghost" id="confirmNo">No</button></div>
  </div>
</div>
<div class="modal-overlay" id="promptModal" hidden>
  <div class="confirm-box">
    <p id="promptMsg"></p>
    <input id="promptInput" type="password" placeholder="Escribe aquí">
    <div class="actions"><button class="btn-green" id="promptOk">Aceptar</button><button class="btn-ghost" id="promptCancel">Cancelar</button></div>
  </div>
</div>
<div id="loginView" hidden>""")

# ---------- 3. Diagnóstico de foco en Acerca de ----------
rep(HTML,
    "    <div class=\"line\">Versión: 2.3.9</div>",
    "    <div class=\"line\">Versión: 2.3.9</div>\n    <div class=\"line\" id=\"focusDiag\">Foco: — · Elemento activo: —</div>")

# ---------- 4. showToast / showConfirm / showPrompt / updateFocusDiag ----------
rep(HTML,
    "<script>\nvar LS_KEY = 'checklist-soporte-v1';",
    r"""<script>
// Avisos y confirmaciones sin diálogos nativos (2.4.0): los diálogos
// nativos del navegador roban el foco en el escritorio y podían dejar
// los campos sin tecleo; a partir de aquí todo aviso es un toast
// in-app y toda confirmación es un modal inline propio. El toast no es
// modal, no bloquea la ejecución y nunca recibe el foco: solo se
// muestra ~3 s y se auto-oculta. El modal solo recibe el foco cuando
// el usuario hace clic en él; al cerrarlo no se fuerza el foco a
// ningún lado.
function showToast(msg) {
  var t = document.getElementById('toast');
  if (!t) return;
  t.textContent = String(msg == null ? '' : msg);
  t.hidden = false;
  if (window._toastTimer) clearTimeout(window._toastTimer);
  window._toastTimer = setTimeout(function () { t.hidden = true; }, 3000);
}
function showConfirm(msg) {
  return new Promise(function (resolve) {
    var m = document.getElementById('confirmModal');
    var msgEl = document.getElementById('confirmMsg');
    var yes = document.getElementById('confirmYes');
    var no = document.getElementById('confirmNo');
    if (!m || !msgEl || !yes || !no) { resolve(false); return; }
    msgEl.textContent = String(msg == null ? '' : msg);
    m.hidden = false;
    function done(v) { m.hidden = true; yes.onclick = null; no.onclick = null; resolve(v); }
    yes.onclick = function () { done(true); };
    no.onclick = function () { done(false); };
  });
}
function showPrompt(msg) {
  return new Promise(function (resolve) {
    var m = document.getElementById('promptModal');
    var msgEl = document.getElementById('promptMsg');
    var inp = document.getElementById('promptInput');
    var ok = document.getElementById('promptOk');
    var cancel = document.getElementById('promptCancel');
    if (!m || !msgEl || !inp || !ok || !cancel) { resolve(null); return; }
    msgEl.textContent = String(msg == null ? '' : msg);
    inp.value = '';
    m.hidden = false;
    function done(v) { m.hidden = true; ok.onclick = null; cancel.onclick = null; resolve(v); }
    ok.onclick = function () { done(inp.value); };
    cancel.onclick = function () { done(null); };
  });
}
// Diagnóstico de foco (2.4.0): línea en Acerca de que muestra si el
// documento tiene el foco y qué elemento está activo, actualizada en
// cada render y cuando el foco entra o sale de la ventana.
function updateFocusDiag() {
  var el = document.getElementById('focusDiag');
  if (!el) return;
  var has = (typeof document.hasFocus === 'function') ? document.hasFocus() : true;
  var ae = document.activeElement;
  var id = (ae && ae.id) ? ae.id : 'ninguno';
  el.textContent = 'Foco: ' + (has ? 'sí' : 'no') + ' · Elemento activo: ' + id;
}
if (typeof window.addEventListener === 'function') {
  window.addEventListener('focus', updateFocusDiag);
  window.addEventListener('blur', updateFocusDiag);
}
var LS_KEY = 'checklist-soporte-v1';""")

# ---------- 5. Bug latente del borrador en 'Usar este equipo' ----------
rep(HTML,
    "  if (use) {\n"
    "    var d = detectados.find(function (x) { return String(x.id) === String(id); });\n"
    "    if (!d) return;\n"
    "    document.getElementById('fTipo').value = d.tipo || 'Desktop';",
    "  if (use) {\n"
    "    var d = detectados.find(function (x) { return String(x.id) === String(id); });\n"
    "    if (!d) return;\n"
    "    // Borrador latente (2.4.0): si antes se abrió 'Completar datos' y se\n"
    "    // cerró sin guardar, _completarBorradorId seguía puesto y Guardar\n"
    "    // actualizaría ese borrador viejo en vez de crear un equipo nuevo.\n"
    "    // Se limpia aquí igual que en btnShowNew, antes de rellenar el form.\n"
    "    window._completarBorradorId = null; document.getElementById('btnAdd').textContent = '💾 Guardar equipo';\n"
    "    document.getElementById('fTipo').value = d.tipo || 'Desktop';")

# ---------- 6. updateFocusDiag() en cada render() ----------
rep(HTML,
    "  renderTemplate();\n"
    "  renderRenta('rec');\n"
    "  renderEntrega();\n"
    "}",
    "  renderTemplate();\n"
    "  renderRenta('rec');\n"
    "  renderEntrega();\n"
    "  updateFocusDiag();\n"
    "}")

# ---------- 7. Los 11 confirm() -> showConfirm().then(...) ----------
# C1: descartar detectado.
rep(HTML,
    "  if (del) {\n"
    "    if (!confirm('¿Descartar este equipo detectado?')) return;\n"
    "    cloudDeleteDetectado(id);\n"
    "  }",
    "  if (del) {\n"
    "    // Confirmación inline (2.4.0): el modal es asíncrono; solo con Sí se\n"
    "    // descarta el equipo detectado.\n"
    "    showConfirm('¿Descartar este equipo detectado?').then(function (ok) { if (!ok) return; cloudDeleteDetectado(id); });\n"
    "  }")
# C2: eliminar equipo.
rep(HTML,
    "  if (t.hasAttribute('data-del-prep') && prep) {\n"
    "    if (confirm('¿Eliminar este equipo y su checklist?')) {\n"
    "      state.preparations = state.preparations.filter(function (p) { return p.id !== prep.id; });\n"
    "      cloudDeletePrep(prep.id);\n"
    "      save(); render();\n"
    "    }\n"
    "    return;\n"
    "  }",
    "  if (t.hasAttribute('data-del-prep') && prep) {\n"
    "    // Confirmación inline (2.4.0): el modal es asíncrono; solo con Sí se\n"
    "    // elimina el equipo y su checklist.\n"
    "    showConfirm('¿Eliminar este equipo y su checklist?').then(function (ok) {\n"
    "      if (!ok) return;\n"
    "      state.preparations = state.preparations.filter(function (p) { return p.id !== prep.id; });\n"
    "      cloudDeletePrep(prep.id);\n"
    "      save(); render();\n"
    "    });\n"
    "    return;\n"
    "  }")
# C3: restaurar plantilla.
rep(HTML,
    "document.getElementById('tplReset').addEventListener('click', function () {\n"
    "  if (confirm('¿Restaurar la plantilla predeterminada?')) {\n"
    "    state.template = defaultTemplate();\n"
    "    save(); render();\n"
    "  }\n"
    "});",
    "document.getElementById('tplReset').addEventListener('click', function () {\n"
    "  // Confirmación inline (2.4.0): solo con Sí se restaura la plantilla.\n"
    "  showConfirm('¿Restaurar la plantilla predeterminada?').then(function (ok) {\n"
    "    if (!ok) return;\n"
    "    state.template = defaultTemplate();\n"
    "    save(); render();\n"
    "  });\n"
    "});")
# C4: borrar mensaje del chat del equipo.
rep(HTML,
    "  if (!confirm('¿Borrar este mensaje para todos?')) return;\n"
    "  window.Cloud.deleteChatMessage(b.getAttribute('data-del-chat')).catch(function () { alert('No se pudo borrar el mensaje.'); });",
    "  // Confirmación inline (2.4.0): solo con Sí se borra el mensaje.\n"
    "  showConfirm('¿Borrar este mensaje para todos?').then(function (ok) {\n"
    "    if (!ok) return;\n"
    "    window.Cloud.deleteChatMessage(b.getAttribute('data-del-chat')).catch(function () { showToast('No se pudo borrar el mensaje.'); });\n"
    "  });")
# C5: borrar mensaje del chat individual.
rep(HTML,
    "  if (!confirm('¿Borrar este mensaje para los dos?')) return;\n"
    "  window.Cloud.deleteDmMessage(b.getAttribute('data-del-dm')).catch(function () { alert('No se pudo borrar el mensaje.'); });",
    "  // Confirmación inline (2.4.0): solo con Sí se borra el mensaje.\n"
    "  showConfirm('¿Borrar este mensaje para los dos?').then(function (ok) {\n"
    "    if (!ok) return;\n"
    "    window.Cloud.deleteDmMessage(b.getAttribute('data-del-dm')).catch(function () { showToast('No se pudo borrar el mensaje.'); });\n"
    "  });")
# C6: eliminar equipo de renta (Recibir renta).
rep(HTML,
    "  if (t.hasAttribute('data-renta-del') && confirm('¿Eliminar este equipo de renta?')) {\n"
    "    state.renta = state.renta.filter(function (r) { return r.id !== id; });\n"
    "    cloudDelete(id);\n"
    "    save(); render();\n"
    "  }",
    "  // Confirmación inline (2.4.0): solo con Sí se elimina el equipo de renta.\n"
    "  if (t.hasAttribute('data-renta-del')) {\n"
    "    showConfirm('¿Eliminar este equipo de renta?').then(function (ok) {\n"
    "      if (!ok) return;\n"
    "      state.renta = state.renta.filter(function (r) { return r.id !== id; });\n"
    "      cloudDelete(id);\n"
    "      save(); render();\n"
    "    });\n"
    "  }")
# C7: eliminar equipo de renta (Entrega Renta).
rep(HTML,
    "  if (t.hasAttribute('data-renta-del') && confirm('¿Eliminar este equipo de renta?')) {\n"
    "    state.renta = state.renta.filter(function (r) { return r.id !== id; });\n"
    "    if (state.entregaActual === id) state.entregaActual = null;\n"
    "    cloudDelete(id);\n"
    "    save(); render();\n"
    "  }",
    "  // Confirmación inline (2.4.0): solo con Sí se elimina el equipo de renta.\n"
    "  if (t.hasAttribute('data-renta-del')) {\n"
    "    showConfirm('¿Eliminar este equipo de renta?').then(function (ok) {\n"
    "      if (!ok) return;\n"
    "      state.renta = state.renta.filter(function (r) { return r.id !== id; });\n"
    "      if (state.entregaActual === id) state.entregaActual = null;\n"
    "      cloudDelete(id);\n"
    "      save(); render();\n"
    "    });\n"
    "  }")
# C8: ofrecer huella (async: await al modal).
rep(HTML,
    "    if (!confirm('¿Activar el acceso con huella en este teléfono para entrar sin escribir tu contraseña?')) {\n"
    "      localStorage.setItem('checklist-bio-declined', '1');\n"
    "      return;\n"
    "    }",
    "    // Confirmación inline (2.4.0): offerBiometrics ya es async, así que\n"
    "    // se espera al modal; solo con Sí se activa la huella.\n"
    "    if (!await showConfirm('¿Activar el acceso con huella en este teléfono para entrar sin escribir tu contraseña?')) {\n"
    "      localStorage.setItem('checklist-bio-declined', '1');\n"
    "      return;\n"
    "    }")
# C9: quitar clave de la IA (Gemini).
rep(HTML,
    "document.getElementById('btnAiQuitar').addEventListener('click', function () {\n"
    "  if (!confirm('¿Quitar la clave de la IA? La IA dejará de funcionar en todos los teléfonos.')) return;\n"
    "  window.Cloud.setAiKey('').then(function () { aiKey = ''; refreshAiStatus(); }).catch(function () { alert('No se pudo quitar la clave. Revisa tu conexión.'); });\n"
    "});",
    "document.getElementById('btnAiQuitar').addEventListener('click', function () {\n"
    "  // Confirmación inline (2.4.0): solo con Sí se quita la clave de la IA.\n"
    "  showConfirm('¿Quitar la clave de la IA? La IA dejará de funcionar en todos los teléfonos.').then(function (ok) {\n"
    "    if (!ok) return;\n"
    "    window.Cloud.setAiKey('').then(function () { aiKey = ''; refreshAiStatus(); }).catch(function () { showToast('No se pudo quitar la clave. Revisa tu conexión.'); });\n"
    "  });\n"
    "});")
# C10: quitar clave de DeepSeek.
rep(HTML,
    "document.getElementById('btnAiQuitarDs').addEventListener('click', function () {\n"
    "  if (!confirm('¿Quitar la clave de DeepSeek? Si Gemini falla, la IA dejará de tener respaldo.')) return;\n"
    "  window.Cloud.setDeepseekKey('').then(function () { aiKeyDs = ''; refreshAiStatus(); }).catch(function () { alert('No se pudo quitar la clave. Revisa tu conexión.'); });\n"
    "});",
    "document.getElementById('btnAiQuitarDs').addEventListener('click', function () {\n"
    "  // Confirmación inline (2.4.0): solo con Sí se quita la clave de DeepSeek.\n"
    "  showConfirm('¿Quitar la clave de DeepSeek? Si Gemini falla, la IA dejará de tener respaldo.').then(function (ok) {\n"
    "    if (!ok) return;\n"
    "    window.Cloud.setDeepseekKey('').then(function () { aiKeyDs = ''; refreshAiStatus(); }).catch(function () { showToast('No se pudo quitar la clave. Revisa tu conexión.'); });\n"
    "  });\n"
    "});")
# C11: eliminar usuario.
rep(HTML,
    "  if (del) {\n"
    "    if (!confirm('¿Eliminar a ' + (u.nombre || u.email) + '? Ya no podrá entrar a la app.')) return;\n"
    "    window.Cloud.deleteUserByAdmin(uid, u.usuario || '').then(renderUsuarios).catch(function () { alert('No se pudo eliminar el usuario.'); });\n"
    "    return;\n"
    "  }",
    "  if (del) {\n"
    "    // Confirmación inline (2.4.0): solo con Sí se elimina el usuario.\n"
    "    showConfirm('¿Eliminar a ' + (u.nombre || u.email) + '? Ya no podrá entrar a la app.').then(function (ok) {\n"
    "      if (!ok) return;\n"
    "      window.Cloud.deleteUserByAdmin(uid, u.usuario || '').then(renderUsuarios).catch(function () { showToast('No se pudo eliminar el usuario.'); });\n"
    "    });\n"
    "    return;\n"
    "  }")

# ---------- 7b. El único prompt() -> showPrompt().then(...) ----------
rep(HTML,
    "  if (pas) {\n"
    "    var np = prompt('Nueva contraseña para ' + (u.nombre || u.email) + ' (mínimo 6 caracteres):');\n"
    "    if (np === null) return;\n"
    "    if (np.length < 6) { alert('La contraseña debe tener al menos 6 caracteres.'); return; }\n"
    "    window.Cloud.adminResetPassword({ uid: uid, usuario: u.usuario || '', email: u.email, nombre: u.nombre || '', rol: u.rol || 'usuario', newPassword: np }).then(function () { alert('Contraseña cambiada para ' + (u.nombre || u.email) + '.'); renderUsuarios(); }).catch(function () { alert('No se pudo cambiar la contraseña.'); });\n"
    "    return;\n"
    "  }",
    "  if (pas) {\n"
    "    // Contraseña nueva con modal inline (2.4.0): el prompt nativo es otro\n"
    "    // diálogo nativo y se elimina junto con los demás; Cancelar devuelve\n"
    "    // null igual que antes y la contraseña corta avisa con toast.\n"
    "    showPrompt('Nueva contraseña para ' + (u.nombre || u.email) + ' (mínimo 6 caracteres):').then(function (np) {\n"
    "      if (np === null) return;\n"
    "      if (np.length < 6) { showToast('La contraseña debe tener al menos 6 caracteres.'); return; }\n"
    "      window.Cloud.adminResetPassword({ uid: uid, usuario: u.usuario || '', email: u.email, nombre: u.nombre || '', rol: u.rol || 'usuario', newPassword: np }).then(function () { showToast('Contraseña cambiada para ' + (u.nombre || u.email) + '.'); renderUsuarios(); }).catch(function () { showToast('No se pudo cambiar la contraseña.'); });\n"
    "    });\n"
    "    return;\n"
    "  }")

# ---------- 8. Reemplazo global alert( -> showToast( ----------
# Quedaban 71 - 8 = 63 (los 8 de los textos viejos de C4/C5/C9/C10/C11/P1
# ya se reescribieron con showToast directo en el paso 7).
with open(HTML, encoding='utf-8') as f:
    html = f.read()
assert html.count('alert(') == 63, 'alert( restantes=%d (esperados 63)' % html.count('alert(')
assert html.count('confirm(') == 0, 'confirm( restantes=%d (esperados 0)' % html.count('confirm(')
assert html.count('prompt(') == 0, 'prompt( restantes=%d (esperados 0)' % html.count('prompt(')
with open(HTML, 'w', encoding='utf-8') as f:
    f.write(html.replace('alert(', 'showToast('))
print('OK: 63 alert( -> showToast(; confirm( y prompt( ya en 0')

# ---------- 9. Versión 2.3.9 -> 2.4.0 ----------
with open(HTML, encoding='utf-8') as f:
    html = f.read()
assert html.count('2.3.9') == 27, 'OCURRENCIAS 2.3.9=%d (esperadas 27)' % html.count('2.3.9')
assert '2.4.0' not in html.replace('(2.4.0)', ''), 'Ya hay 2.4.0 fuera de los comentarios nuevos'
with open(HTML, 'w', encoding='utf-8') as f:
    f.write(html.replace('2.3.9', '2.4.0'))
print('OK: index.html versión 2.4.0 (27 ocurrencias convertidas)')
with open(HTML, encoding='utf-8') as f:
    n240 = f.read().count('2.4.0')
print('OK: ocurrencias finales de 2.4.0 en index.html: %d (27 convertidas + 15 en comentarios nuevos)' % n240)
assert n240 == 42, 'Ocurrencias 2.4.0=%d (esperadas 42)' % n240

# ---------- 10. android/app/build.gradle ----------
rep(GRADLE, '        versionCode 52\n', '        versionCode 53\n')
rep(GRADLE, '        versionName "2.3.9"\n', '        versionName "2.4.0"\n')

# ---------- 11. iOS project.pbxproj ----------
rep(PBX, 'MARKETING_VERSION = 2.3.9;', 'MARKETING_VERSION = 2.4.0;', count=2)
rep(PBX, 'CURRENT_PROJECT_VERSION = 52;', 'CURRENT_PROJECT_VERSION = 53;', count=2)

# ---------- 12. test20240.js: extraído, versión y stubs ----------
rep(TEST_NEW,
    "const SRC = fs.readFileSync(__dirname + '/checklist20239.js', 'utf8');",
    "const SRC = fs.readFileSync(__dirname + '/checklist20240.js', 'utf8');")
rep(TEST_NEW,
    "global.alert = (m) => { global.lastAlert = m; };\nglobal.confirm = () => true;\nglobal.prompt = () => null;",
    "// 2.4.0: la app ya no usa diálogos nativos; si alguno quedara, el test\n"
    "// debe fallar en voz alta en vez de tragarlo con un stub silencioso.\n"
    "global.alert = (m) => { throw new Error('alert() nativo llamado: ' + m); };\n"
    "global.confirm = () => { throw new Error('confirm() nativo llamado'); };\n"
    "global.prompt = () => { throw new Error('prompt() nativo llamado'); };")
rep(TEST_NEW,
    "// >>> EVAL\neval(SRC);",
    "// >>> EVAL\neval(SRC);\n"
    "\n"
    "// Helpers 2.4.0 para los tests del toast y los modales inline.\n"
    "function toastTxt() { return document.getElementById('toast').textContent || ''; }\n"
    "function answerConfirm(yes) {\n"
    "  var b = document.getElementById(yes ? 'confirmYes' : 'confirmNo');\n"
    "  if (b && typeof b.onclick === 'function') b.onclick();\n"
    "}\n"
    "function answerPrompt(value) {\n"
    "  if (value === null) {\n"
    "    var c = document.getElementById('promptCancel');\n"
    "    if (c && typeof c.onclick === 'function') c.onclick();\n"
    "  } else {\n"
    "    document.getElementById('promptInput').value = value;\n"
    "    var o = document.getElementById('promptOk');\n"
    "    if (o && typeof o.onclick === 'function') o.onclick();\n"
    "  }\n"
    "}")
rep(TEST_NEW,
    "  console.log('AM0) versión 2.3.9:', html.includes('Versión 2.3.9'), '| sin 2.3.8:', !html.includes('Versión 2.3.8')",
    "  console.log('AM0) versión 2.4.0:', html.includes('Versión 2.4.0'), '| sin 2.3.9:', !html.includes('Versión 2.3.9')")
rep(TEST_NEW,
    "  console.log('AP0) estáticos 2.3.9: versión:', html.includes('Versión 2.3.9') && !html.includes('Versión 2.3.8'), '| 17 detectables con t12:',",
    "  console.log('AP0) estáticos 2.4.0: versión:', html.includes('Versión 2.4.0') && !html.includes('Versión 2.3.9'), '| 17 detectables con t12:',")
rep(TEST_NEW,
    "  var n239 = (html.match(/2\\.3\\.9/g) || []).length;",
    "  var n240 = (html.match(/2\\.4\\.0/g) || []).length;")
rep(TEST_NEW,
    "  console.log('AR0) versión 2.3.9 visible:', html.includes('Versión 2.3.9') && html.includes('Versión: 2.3.9'), '| 0 de 2.3.8:', !html.includes('2.3.8'), '| ocurrencias 2.3.9:', n239 === 27);",
    "  console.log('AR0) versión 2.4.0 visible:', html.includes('Versión 2.4.0') && html.includes('Versión: 2.4.0'), '| 0 de 2.3.9:', !html.includes('2.3.9'), '| ocurrencias 2.4.0:', n240 === %d);" % n240)

# ---------- 13. Tests viejos con alert/confirm -> toast/modal ----------
# AN2: Descartar detectado con modal inline (Sí borra, No no borra).
rep(TEST_NEW,
    "  // AN2: 'Descartar' pide confirmación y borra; si se cancela, no borra.\n"
    "  deletedDet.length = 0;\n"
    "  document.getElementById('detList')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-det-del]' ? { getAttribute: function () { return 'SERIE123'; } } : null; } } });\n"
    "  var discOk = deletedDet.indexOf('SERIE123') !== -1;\n"
    "  deletedDet.length = 0;\n"
    "  global.confirm = function () { return false; };\n"
    "  document.getElementById('detList')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-det-del]' ? { getAttribute: function () { return 'SERIE123'; } } : null; } } });\n"
    "  global.confirm = function () { return true; };\n"
    "  console.log('AN2) Descartar borra con confirmación:', discOk, '| sin confirmación no borra:', deletedDet.length === 0);",
    "  // AN2: 'Descartar' abre el modal inline y borra solo con Sí; con No no borra.\n"
    "  deletedDet.length = 0;\n"
    "  document.getElementById('detList')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-det-del]' ? { getAttribute: function () { return 'SERIE123'; } } : null; } } });\n"
    "  var discModal = document.getElementById('confirmModal').hidden === false && document.getElementById('confirmMsg').textContent === '¿Descartar este equipo detectado?';\n"
    "  var discBefore = deletedDet.length === 0;\n"
    "  answerConfirm(true);\n"
    "  await sleep(20);\n"
    "  var discOk = deletedDet.indexOf('SERIE123') !== -1;\n"
    "  deletedDet.length = 0;\n"
    "  document.getElementById('detList')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-det-del]' ? { getAttribute: function () { return 'SERIE123'; } } : null; } } });\n"
    "  answerConfirm(false);\n"
    "  await sleep(20);\n"
    "  console.log('AN2) Descartar abre el modal con su pregunta:', discModal, '| antes de Sí no borra:', discBefore, '| con Sí borra:', discOk, '| con No no borra:', deletedDet.length === 0);")
# AN3: avisos de Detectar por toast.
rep(TEST_NEW,
    "  var detAlertOk = global.lastAlert === 'Equipo detectado, ya aparece en los teléfonos';",
    "  var detAlertOk = toastTxt() === 'Equipo detectado, ya aparece en los teléfonos';")
rep(TEST_NEW,
    "  var detFailOk = (global.lastAlert || '').indexOf('No se pudo detectar el equipo') === 0;",
    "  var detFailOk = toastTxt().indexOf('No se pudo detectar el equipo') === 0;")
rep(TEST_NEW,
    "  var detNoSessionOk = (global.lastAlert || '').indexOf('Inicia sesión') === 0 && reported.length === 1;",
    "  var detNoSessionOk = toastTxt().indexOf('Inicia sesión') === 0 && reported.length === 1;")
# AO7: avisos de Detectar por toast.
rep(TEST_NEW,
    "  var progReportOk = repDet.length === 1 && repDet[0].hostname === 'PC-PROG' && global.lastAlert === 'Equipo detectado, ya aparece en los teléfonos';",
    "  var progReportOk = repDet.length === 1 && repDet[0].hostname === 'PC-PROG' && toastTxt() === 'Equipo detectado, ya aparece en los teléfonos';")
rep(TEST_NEW,
    "  var failRestoredOk = btnDetEl.disabled === false && btnDetEl.innerHTML === 'Detectar este equipo' && (global.lastAlert || '').indexOf('No se pudo detectar el equipo') === 0;",
    "  var failRestoredOk = btnDetEl.disabled === false && btnDetEl.innerHTML === 'Detectar este equipo' && toastTxt().indexOf('No se pudo detectar el equipo') === 0;")
# AU3: aviso de solo lectura por toast.
rep(TEST_NEW,
    "  global.lastAlert = '';\n  realClick('data-ready', 'au3');",
    "  document.getElementById('toast').textContent = '';\n  realClick('data-ready', 'au3');")
rep(TEST_NEW,
    "  var guardReady = !fAU3.readyAt && up3.length === 0 && (global.lastAlert || '').indexOf('otro analista') !== -1;",
    "  var guardReady = !fAU3.readyAt && up3.length === 0 && toastTxt().indexOf('otro analista') !== -1;")
# AW4: aviso de solo lectura por toast.
rep(TEST_NEW,
    "  upAW.length = 0; global.lastAlert = '';",
    "  upAW.length = 0; document.getElementById('toast').textContent = '';")
rep(TEST_NEW,
    "  var aw4block = fAW4.borrador === true && upAW.length === 0 && window._completarBorradorId !== 'aw4' && (global.lastAlert || '').indexOf('otro analista') !== -1;",
    "  var aw4block = fAW4.borrador === true && upAW.length === 0 && window._completarBorradorId !== 'aw4' && toastTxt().indexOf('otro analista') !== -1;")
# AY6: aviso de solo lectura por toast.
rep(TEST_NEW,
    "  global.lastAlert = null;",
    "  document.getElementById('toast').textContent = '';")
rep(TEST_NEW,
    "  var alertAY6 = (global.lastAlert || '').indexOf('otro analista') !== -1;",
    "  var toastAY6 = toastTxt().indexOf('otro analista') !== -1;")
rep(TEST_NEW,
    "  console.log('AY6) ajeno bloqueado: sin guardado local:', noSaveAY6, '| sin subida a nube:', noUpAY6, '| aviso de solo lectura:', alertAY6, '| botón sin tocar:', btnAY6ok);",
    "  console.log('AY6) ajeno bloqueado: sin guardado local:', noSaveAY6, '| sin subida a nube:', noUpAY6, '| aviso de solo lectura:', toastAY6, '| botón sin tocar:', btnAY6ok);")
# AA6: eliminar equipo con modal inline.
rep(TEST_NEW,
    "  // AA6: eliminar borra el equipo en la nube.\n"
    "  fakeClick('data-del-prep', 'p1');\n"
    "  console.log('AA6) eliminar borra en la nube:', deletedPrep.indexOf('p1') !== -1 && !state.preparations.some(function (p) { return p.id === 'p1'; }));",
    "  // AA6: eliminar abre el modal inline y borra solo con Sí.\n"
    "  fakeClick('data-del-prep', 'p1');\n"
    "  var aa6modal = document.getElementById('confirmModal').hidden === false && document.getElementById('confirmMsg').textContent === '¿Eliminar este equipo y su checklist?';\n"
    "  answerConfirm(true);\n"
    "  await sleep(20);\n"
    "  console.log('AA6) eliminar abre el modal con su pregunta:', aa6modal, '| con Sí borra en la nube:', deletedPrep.indexOf('p1') !== -1 && !state.preparations.some(function (p) { return p.id === 'p1'; }));")
# AC3: borrar mensaje del chat con modal inline.
rep(TEST_NEW,
    "  document.getElementById('chatBox')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-del-chat]' ? { getAttribute: function () { return 'm1'; } } : null; } } });\n"
    "  console.log('AC3) borrar en el chat del equipo borra el mensaje:', delChat.length === 1 && delChat[0] === 'm1');",
    "  document.getElementById('chatBox')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-del-chat]' ? { getAttribute: function () { return 'm1'; } } : null; } } });\n"
    "  var ac3modal = document.getElementById('confirmModal').hidden === false && document.getElementById('confirmMsg').textContent === '¿Borrar este mensaje para todos?';\n"
    "  answerConfirm(true);\n"
    "  await sleep(20);\n"
    "  console.log('AC3) borrar abre el modal con su pregunta:', ac3modal, '| con Sí borra el mensaje:', delChat.length === 1 && delChat[0] === 'm1');")
# AC4: borrar mensaje del chat individual con modal inline.
rep(TEST_NEW,
    "  document.getElementById('dmChatBox')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-del-dm]' ? { getAttribute: function () { return 'd1'; } } : null; } } });\n"
    "  console.log('AC4) borrar en el chat individual borra el mensaje:', delDm.length === 1 && delDm[0] === 'd1');",
    "  document.getElementById('dmChatBox')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-del-dm]' ? { getAttribute: function () { return 'd1'; } } : null; } } });\n"
    "  var ac4modal = document.getElementById('confirmModal').hidden === false && document.getElementById('confirmMsg').textContent === '¿Borrar este mensaje para los dos?';\n"
    "  answerConfirm(true);\n"
    "  await sleep(20);\n"
    "  console.log('AC4) borrar abre el modal con su pregunta:', ac4modal, '| con Sí borra el mensaje:', delDm.length === 1 && delDm[0] === 'd1');")
# AW5: eliminar el borrador con modal inline.
rep(TEST_NEW,
    "  loginAs('uGer', 'Gerardo', 'admin');\n"
    "  delAW.length = 0;\n"
    "  realClick('data-del-prep', draftAW5.id);\n"
    "  var aw5gone = state.preparations.every(function (p) { return p.id !== draftAW5.id; }) && delAW.indexOf(draftAW5.id) !== -1;",
    "  loginAs('uGer', 'Gerardo', 'admin');\n"
    "  delAW.length = 0;\n"
    "  realClick('data-del-prep', draftAW5.id);\n"
    "  answerConfirm(true);\n"
    "  await sleep(20);\n"
    "  var aw5gone = state.preparations.every(function (p) { return p.id !== draftAW5.id; }) && delAW.indexOf(draftAW5.id) !== -1;")

# ---------- 14. Serie AZ nueva (2.4.0) ----------
AZ = r"""
  // AZ: serie nueva 2.4.0 — sin diálogos nativos: toast no modal para
  // avisos, modal inline para confirmaciones y para pedir la contraseña
  // nueva; borrador: 'Usar este equipo' ya no hereda el borrador de
  // 'Completar datos'; diagnóstico de foco en Acerca de.
  // AZ0: estáticos — toast, modal de confirmación y modal de prompt en
  // el HTML; funciones en el script; cero llamadas nativas en el código.
  var az0html = html.includes('id="toast"') && html.includes('id="confirmModal"') && html.includes('id="confirmMsg"') && html.includes('id="confirmYes"') && html.includes('id="confirmNo"') && html.includes('id="promptModal"') && html.includes('id="promptInput"') && html.includes('id="focusDiag"');
  var az0src = SRC.includes('function showToast(') && SRC.includes('function showConfirm(') && SRC.includes('function showPrompt(') && SRC.includes('function updateFocusDiag(') && SRC.includes("document.getElementById('toast')") && SRC.includes("document.getElementById('confirmModal')");
  var az0zero = (SRC.match(/alert\(/g) || []).length === 0 && (SRC.match(/confirm\(/g) || []).length === 0 && (SRC.match(/prompt\(/g) || []).length === 0;
  var az0zeroHtml = (html.match(/alert\(/g) || []).length === 0 && (html.match(/confirm\(/g) || []).length === 0 && (html.match(/prompt\(/g) || []).length === 0;
  console.log('AZ0) toast + modales + foco en HTML:', az0html, '| funciones en el script:', az0src, '| cero nativos en el script:', az0zero, '| cero nativos en todo el HTML:', az0zeroHtml);
  // AZ1: el toast aparece con el mensaje, no roba el foco y se
  // auto-oculta a los ~3 s; no bloquea la ejecución (la línea siguiente
  // corre de inmediato).
  var toastElAZ = document.getElementById('toast');
  toastElAZ.focus = function () { global.toastFocusedAZ = true; };
  global.toastFocusedAZ = false;
  showToast('Aviso de prueba AZ1');
  var az1after = true;
  var az1show = toastElAZ.textContent === 'Aviso de prueba AZ1' && toastElAZ.hidden === false && global.toastFocusedAZ === false && az1after === true;
  await sleep(3100);
  var az1hide = toastElAZ.hidden === true && toastElAZ.textContent === 'Aviso de prueba AZ1';
  console.log('AZ1) toast visible con el mensaje y sin robar foco:', az1show, '| se auto-oculta a los ~3 s:', az1hide);
  // AZ2a: eliminar equipo — modal con su pregunta; con No no borra y
  // cierra; con Sí borra en la nube.
  loginAs('u1', 'Test User', 'usuario');
  CLOUD_ENABLED = true;
  var pAZ2 = mkPrepAU({ id: 'az2', createdAt: Date.now() - 100000 });
  state.preparations = [pAZ2];
  filterStatus = 'todos'; searchText = ''; todosPage = 0; showOthers = false;
  render();
  var delPrepAZ = [];
  global.Cloud.deletePrep = async function (id) { delPrepAZ.push(id); };
  realClick('data-del-prep', 'az2');
  var az2aModal = document.getElementById('confirmModal').hidden === false && document.getElementById('confirmMsg').textContent === '¿Eliminar este equipo y su checklist?';
  var az2aBefore = state.preparations.some(function (p) { return p.id === 'az2'; }) && delPrepAZ.length === 0;
  answerConfirm(false);
  await sleep(20);
  var az2aNo = state.preparations.some(function (p) { return p.id === 'az2'; }) && delPrepAZ.length === 0 && document.getElementById('confirmModal').hidden === true;
  realClick('data-del-prep', 'az2');
  answerConfirm(true);
  await sleep(20);
  var az2aSi = !state.preparations.some(function (p) { return p.id === 'az2'; }) && delPrepAZ.indexOf('az2') !== -1;
  console.log('AZ2a) eliminar equipo: abre el modal con su pregunta:', az2aModal, '| antes de responder no borra:', az2aBefore, '| con No no borra y cierra:', az2aNo, '| con Sí borra en la nube:', az2aSi);
  // AZ2b: borrar mensaje del chat del equipo — solo con Sí.
  cloudUser = { uid: 'u1', email: 'test@checklist.local', nombre: 'Test User' };
  cloudRole = 'admin';
  chatMessages = [{ id: 'mAZ', uid: 'u2', nombre: 'Alejandro', texto: 'Hola', createdAt: Date.now() - 60000 }];
  dmMessages = []; dmPeer = null;
  teamUsers = [{ uid: 'u1', nombre: 'Test User', rol: 'usuario' }, { uid: 'u2', nombre: 'Alejandro', rol: 'usuario' }];
  presenceList = [];
  renderEquipo();
  var delChatAZ = [];
  global.Cloud.deleteChatMessage = async function (id) { delChatAZ.push(id); };
  function clickDelChatAZ() {
    document.getElementById('chatBox')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-del-chat]' ? { getAttribute: function () { return 'mAZ'; } } : null; } } });
  }
  clickDelChatAZ();
  var az2bModal = document.getElementById('confirmModal').hidden === false && document.getElementById('confirmMsg').textContent === '¿Borrar este mensaje para todos?';
  answerConfirm(false);
  await sleep(20);
  var az2bNo = delChatAZ.length === 0;
  clickDelChatAZ();
  answerConfirm(true);
  await sleep(20);
  var az2bSi = delChatAZ.length === 1 && delChatAZ[0] === 'mAZ';
  console.log('AZ2b) borrar mensaje: abre el modal con su pregunta:', az2bModal, '| con No no borra:', az2bNo, '| con Sí borra:', az2bSi);
  // AZ2c: borrar usuario (admin) — solo con Sí.
  cloudUser = { uid: 'u1', email: 'test@checklist.local', nombre: 'Test User' };
  cloudRole = 'admin';
  lastUsers = [{ uid: 'uAZ', nombre: 'Borrar Yo', usuario: 'borraryo', email: 'b@x.com', rol: 'usuario', activo: true }];
  var delUserAZ = [];
  global.Cloud.deleteUserByAdmin = async function (uid) { delUserAZ.push(uid); };
  function clickUserDelAZ() {
    document.getElementById('userList')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-user-del]' ? { getAttribute: function () { return 'uAZ'; } } : null; } } });
  }
  clickUserDelAZ();
  var az2cModal = document.getElementById('confirmModal').hidden === false && document.getElementById('confirmMsg').textContent === '¿Eliminar a Borrar Yo? Ya no podrá entrar a la app.';
  answerConfirm(false);
  await sleep(20);
  var az2cNo = delUserAZ.length === 0;
  clickUserDelAZ();
  answerConfirm(true);
  await sleep(20);
  var az2cSi = delUserAZ.length === 1 && delUserAZ[0] === 'uAZ';
  console.log('AZ2c) borrar usuario: abre el modal con su pregunta:', az2cModal, '| con No no borra:', az2cNo, '| con Sí borra:', az2cSi);
  // AZ2d: quitar la clave de la IA — solo con Sí.
  var setAiAZ = [];
  global.Cloud.setAiKey = async function (k) { setAiAZ.push(k); };
  document.getElementById('btnAiQuitar')._h.click[0]();
  var az2dModal = document.getElementById('confirmModal').hidden === false && document.getElementById('confirmMsg').textContent === '¿Quitar la clave de la IA? La IA dejará de funcionar en todos los teléfonos.';
  answerConfirm(false);
  await sleep(20);
  var az2dNo = setAiAZ.length === 0;
  document.getElementById('btnAiQuitar')._h.click[0]();
  answerConfirm(true);
  await sleep(20);
  var az2dSi = setAiAZ.length === 1 && setAiAZ[0] === '';
  console.log('AZ2d) quitar clave IA: abre el modal con su pregunta:', az2dModal, '| con No no la quita:', az2dNo, '| con Sí la quita:', az2dSi);
  // AZ3: 'Usar este equipo' tras 'Completar datos' sin guardar crea un
  // equipo NUEVO y no toca el borrador (bug latente de la 2.3.9).
  loginAs('u1', 'Test User', 'usuario');
  CLOUD_ENABLED = true;
  var upAZ3 = [];
  global.Cloud.upsertPrep = async function (d) { upAZ3.push(d); };
  global.Cloud.markDetectadoUsado = async function () {};
  var borAZ3 = mkPrepAU({ id: 'az3-bor', borrador: true, equipo: { tipo: 'Laptop', marca: 'HP', modelo: 'ModeloBorradorAZ3', serie: 'S-AZ3', inventario: '9' }, usuario: { nombre: 'Viejo', area: '', correo: '' } });
  state.preparations = [borAZ3];
  filterStatus = 'todos'; searchText = ''; todosPage = 0; showOthers = false;
  render();
  realClick('data-completar', 'az3-bor');
  var az3open = window._completarBorradorId === 'az3-bor' && document.getElementById('btnAdd').textContent === '💾 Guardar datos completos';
  detectados = [{ id: 'AZ3-DET', hostname: 'PC-AZ3', marca: 'Lenovo', modelo: 'ThinkCentre AZ3', serie: 'AZ3-DET', cpu: 'i5', ramGB: 8, discoGB: 256, so: 'Windows 11', tipo: 'Desktop', detectadoEn: Date.now() - 60000, detectadoPor: 'Gerardo', usado: false, checks: { t18: true }, detalles: {}, versiones: {} }];
  renderDetectados();
  document.getElementById('detList')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-det-use]' ? { getAttribute: function () { return 'AZ3-DET'; } } : null; } } });
  var az3clean = window._completarBorradorId === null && document.getElementById('btnAdd').textContent === '💾 Guardar equipo';
  document.getElementById('fUser').value = 'Ana AZ3';
  document.getElementById('fTec').value = 'Test User';
  var nAZ3 = state.preparations.length;
  document.getElementById('btnAdd')._h.click[0]();
  var newAZ3 = state.preparations.find(function (p) { return p.equipo && p.equipo.modelo === 'ThinkCentre AZ3'; });
  var borAZ3after = state.preparations.find(function (p) { return p.id === 'az3-bor'; });
  var az3new = state.preparations.length === nAZ3 + 1 && !!newAZ3 && newAZ3.id !== 'az3-bor';
  var az3bor = !!borAZ3after && borAZ3after.borrador === true && borAZ3after.equipo.modelo === 'ModeloBorradorAZ3' && borAZ3after.usuario.nombre === 'Viejo';
  console.log('AZ3) Completar abre el borrador:', az3open, '| Usar limpia el borrador pendiente y el botón:', az3clean, '| Guardar crea un equipo nuevo:', az3new, '| el borrador viejo intacto:', az3bor);
  // AZ4: diagnóstico de foco en Acerca de, actualizado en cada render.
  render();
  var fdAZ4 = document.getElementById('focusDiag').textContent;
  var az4 = fdAZ4.indexOf('Foco: sí') !== -1 && fdAZ4.indexOf('Elemento activo: ninguno') !== -1;
  var az4html = html.includes('id="focusDiag"') && html.includes('Foco:');
  console.log('AZ4) diagnóstico de foco en Acerca de:', az4html, '| actualizado en render:', az4, '| texto:', fdAZ4);
  // AZ5: la contraseña nueva del usuario se pide con modal inline
  // (no prompt nativo): Cancelar no cambia nada, la corta avisa con
  // toast y no cambia, la válida la cambia.
  cloudUser = { uid: 'u1', email: 'test@checklist.local', nombre: 'Test User' };
  cloudRole = 'admin';
  lastUsers = [{ uid: 'uAZ5', nombre: 'Clave Yo', usuario: 'clvyo', email: 'c@x.com', rol: 'usuario', activo: true }];
  var resetAZ5 = [];
  global.Cloud.adminResetPassword = async function (o) { resetAZ5.push(o); };
  function clickUserPassAZ() {
    document.getElementById('userList')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-user-pass]' ? { getAttribute: function () { return 'uAZ5'; } } : null; } } });
  }
  clickUserPassAZ();
  var az5Modal = document.getElementById('promptModal').hidden === false && document.getElementById('promptMsg').textContent.indexOf('Nueva contraseña para Clave Yo') !== -1;
  answerPrompt(null);
  await sleep(20);
  var az5Cancel = resetAZ5.length === 0;
  clickUserPassAZ();
  answerPrompt('corta');
  await sleep(20);
  var az5Short = resetAZ5.length === 0 && toastTxt().indexOf('al menos 6 caracteres') !== -1;
  clickUserPassAZ();
  answerPrompt('nueva123');
  await sleep(20);
  var az5Ok = resetAZ5.length === 1 && resetAZ5[0].newPassword === 'nueva123' && resetAZ5[0].uid === 'uAZ5';
  console.log('AZ5) pedir contraseña abre el modal con su pregunta:', az5Modal, '| Cancelar no cambia nada:', az5Cancel, '| corta avisa y no cambia:', az5Short, '| válida la cambia:', az5Ok);
"""
with open(TEST_NEW, encoding='utf-8') as f:
    t = f.read()
anchor = '  process.exit(0);'
assert t.count(anchor) == 1, 'Ancla process.exit no única'
t = t.replace(anchor, AZ + anchor, 1)
with open(TEST_NEW, 'w', encoding='utf-8') as f:
    f.write(t)
print('OK: serie AZ añadida a test20240.js')

# ---------- 15. Extraer tests/checklist20240.js del index.html nuevo ----------
with open(HTML, encoding='utf-8') as f:
    lines = f.read().split('\n')
start = next(i for i, ln in enumerate(lines) if ln == '<script>')
end = next(i for i, ln in enumerate(lines) if ln == '</script>')
assert end > start, 'No se encontró el script inline'
with open(EXTRACT, 'w', encoding='utf-8') as f:
    f.write('\n' + '\n'.join(lines[start + 1:end]) + '\n')
print('OK: extraído tests/checklist20240.js (script inline, líneas %d-%d)' % (start + 2, end))

# ---------- 16. Conteos finales ----------
with open(HTML, encoding='utf-8') as f:
    final = f.read()
print('FINAL index.html: alert(=%d confirm(=%d prompt(=%d 2.4.0=%d 2.3.9=%d' % (
    final.count('alert('), final.count('confirm('), final.count('prompt('),
    final.count('2.4.0'), final.count('2.3.9')))
assert final.count('alert(') == 0 and final.count('confirm(') == 0 and final.count('prompt(') == 0
assert final.count('2.3.9') == 0
print('Parche 240 aplicado (firebase.js sin cambios: bundle NO reconstruido; versión 2.4.0/53).')
