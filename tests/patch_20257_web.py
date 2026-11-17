# Parche web 2.5.7: contraseña del usuario sistemas (solo escritorio).
import sys

P = '/home/hatch/workspace/android/checklist-cloud/www/index.html'
s = open(P, encoding='utf-8').read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'NO ENCONTRADO x%d (esperado %d): %r' % (c, n, old[:120])
    s = s.replace(old, new)

# --- 1. Botón junto a Detectar (Por preparar).
rep("""    <button class="menu-btn dark" id="btnDetectar" hidden><span class="ic">&#128187;</span><span>Detectar este equipo<small>solo en escritorio</small></span></button>""",
"""    <button class="menu-btn dark" id="btnDetectar" hidden><span class="ic">&#128187;</span><span>Detectar este equipo<small>solo en escritorio</small></span></button>
    <button class="menu-btn dark" id="btnPassSistemas" hidden><span class="ic">&#128273;</span><span>Contraseña de sistemas<small>solo en escritorio</small></span></button>""")

# --- 2. Panel con los campos (después del panel de detectados).
rep("""  <div class="panel" id="detBox" hidden>
    <b>&#128187; Equipos detectados</b>""",
"""  <div class="panel" id="detBox" hidden>
    <b>&#128187; Equipos detectados</b>""")
rep("""    <div id="detList"></div>
  </div>""",
"""    <div id="detList"></div>
  </div>

  <div class="panel" id="passBox" hidden>
    <b>&#128273; Contraseña del usuario sistemas</b>
    <div class="share-note">Cambia la contraseña del usuario local de Windows en esta PC. La contraseña nunca se guarda ni se manda a la nube; solo se usa aquí para verificarla o cambiarla. El cambio pide permiso de administrador.</div>
    <div class="grid2">
      <div class="field"><label>Usuario de Windows</label><input id="fPsUser" value="sistemas" placeholder="sistemas"></div>
      <div class="field"><label>Contraseña actual</label><input id="fPsActual" type="password" placeholder="Contraseña actual" autocomplete="off"></div>
      <div class="field"><label>Contraseña nueva</label><input id="fPsNueva" type="password" placeholder="Contraseña nueva" autocomplete="new-password"></div>
      <div class="field"><label>Confirmar contraseña nueva</label><input id="fPsConfirm" type="password" placeholder="Repite la contraseña nueva" autocomplete="new-password"></div>
    </div>
    <div class="actions">
      <button class="btn-dark" id="btnPsVerificar">&#128269; Verificar contraseña actual</button>
      <button class="btn-green" id="btnPsCambiar">&#128273; Cambiar contraseña</button>
    </div>
  </div>""")

# --- 3. togglePanel cierra también passBox.
rep("['newBox', 'tplBox', 'reBox', 'detBox'].forEach(function (p) { if (p !== id) document.getElementById(p).hidden = true; });",
    "['newBox', 'tplBox', 'reBox', 'detBox', 'passBox'].forEach(function (p) { if (p !== id) document.getElementById(p).hidden = true; });")

# --- 4. refreshDetectarBtn también muestra/oculta el botón de contraseña.
rep("""    if (btn.innerHTML.indexOf('Detectando software...') !== -1 || btn.innerHTML.indexOf('Equipo detectado') !== -1) btn.innerHTML = defHtml;
  });
}
function loadMachineId() {""",
"""    if (btn.innerHTML.indexOf('Detectando software...') !== -1 || btn.innerHTML.indexOf('Equipo detectado') !== -1) btn.innerHTML = defHtml;
  });
  // (257) Botón de contraseña: solo se muestra en escritorio; no depende
  // del estado de detección.
  var psBtn = document.getElementById('btnPassSistemas');
  if (psBtn) psBtn.hidden = !window.Desktop;
}
function loadMachineId() {""")

# --- 5. Lógica del panel (después del listener de btnDetectar).
rep("""document.getElementById('btnDetectar').addEventListener('click', function () { detectarEquipo(document.getElementById('btnDetectar')); });""",
"""document.getElementById('btnDetectar').addEventListener('click', function () { detectarEquipo(document.getElementById('btnDetectar')); });
// Contraseña del usuario sistemas (257): solo escritorio. Las
// contraseñas nunca se guardan (ni localStorage ni nube): solo viajan
// a window.Desktop para verificarlas o cambiarlas en esta PC, y los
// campos se limpian en cuanto termina la llamada.
function psLimpiar() {
  ['fPsActual', 'fPsNueva', 'fPsConfirm'].forEach(function (id) { var el = document.getElementById(id); if (el) el.value = ''; });
}
function psUsuario() { var v = (document.getElementById('fPsUser').value || '').trim(); return v || 'sistemas'; }
function psValidarNueva() {
  var nueva = document.getElementById('fPsNueva').value;
  var conf = document.getElementById('fPsConfirm').value;
  if (!nueva) { showToast('Escribe la contraseña nueva.'); return null; }
  if (nueva !== conf) { showToast('La contraseña nueva y su confirmación no coinciden.'); return null; }
  return nueva;
}
document.getElementById('btnPassSistemas').addEventListener('click', function () { togglePanel('passBox'); });
document.getElementById('btnPsVerificar').addEventListener('click', function () {
  if (!window.Desktop || typeof window.Desktop.verificarPasswordSistemas !== 'function') { showToast('La verificación solo funciona en la app de escritorio.'); return; }
  var actual = document.getElementById('fPsActual').value;
  if (!actual) { showToast('Escribe la contraseña actual.'); return; }
  var btn = document.getElementById('btnPsVerificar');
  btn.disabled = true;
  Promise.resolve(window.Desktop.verificarPasswordSistemas(psUsuario(), actual)).then(function (r) {
    psLimpiar();
    if (r && r.ok) showToast('Contraseña actual correcta ✓');
    else showToast((r && r.error) || 'Contraseña actual incorrecta.');
  }).catch(function () { psLimpiar(); showToast('No se pudo verificar la contraseña.'); }).then(function () { btn.disabled = false; });
});
document.getElementById('btnPsCambiar').addEventListener('click', function () {
  if (!window.Desktop || typeof window.Desktop.cambiarPasswordSistemas !== 'function') { showToast('El cambio de contraseña solo funciona en la app de escritorio.'); return; }
  var actual = document.getElementById('fPsActual').value;
  if (!actual) { showToast('Escribe la contraseña actual.'); return; }
  var nueva = psValidarNueva();
  if (nueva === null) return;
  var btn = document.getElementById('btnPsCambiar');
  btn.disabled = true;
  Promise.resolve(window.Desktop.cambiarPasswordSistemas(psUsuario(), actual, nueva)).then(function (r) {
    psLimpiar();
    if (r && r.ok) showToast('Contraseña cambiada ✓');
    else showToast((r && r.error) || 'No se pudo cambiar la contraseña.');
  }).catch(function () { psLimpiar(); showToast('No se pudo cambiar la contraseña.'); }).then(function () { btn.disabled = false; });
});""")

# --- 6. Versiones 2.5.7 + mailto 257.
rep('Versión 2.5.6', 'Versión 2.5.7')
rep('Versión: 2.5.6', 'Versión: 2.5.7')
rep('Reporte de problema - Checklist de Soporte 256', 'Reporte de problema - Checklist de Soporte 257')
rep('Versión de la app: 256', 'Versión de la app: 257')

open(P, 'w', encoding='utf-8').write(s)
print('OK index.html, bytes:', len(s))
print('2.5.7:', s.count('2.5.7'), '| 2.5.6 restante:', s.count('2.5.6'), '| 256 mailto restante:', s.count('Soporte 256'))
print('btnPassSistemas:', s.count('btnPassSistemas'), '| passBox:', s.count('passBox'), '| verificarPasswordSistemas:', s.count('verificarPasswordSistemas'), '| cambiarPasswordSistemas:', s.count('cambiarPasswordSistemas'))
