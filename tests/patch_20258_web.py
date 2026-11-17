# Parche web 2.5.8: actualizaciones de Windows (solo escritorio).
import sys

P = '/home/hatch/workspace/android/checklist-cloud/www/index.html'
s = open(P, encoding='utf-8').read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'NO ENCONTRADO x%d (esperado %d): %r' % (c, n, old[:120])
    s = s.replace(old, new)

# --- 1. Botón junto a Contraseña de sistemas (Por preparar).
rep("""    <button class="menu-btn dark" id="btnPassSistemas" hidden><span class="ic">&#128273;</span><span>Contraseña de sistemas<small>solo en escritorio</small></span></button>""",
"""    <button class="menu-btn dark" id="btnPassSistemas" hidden><span class="ic">&#128273;</span><span>Contraseña de sistemas<small>solo en escritorio</small></span></button>
    <button class="menu-btn dark" id="btnWinUpd" hidden><span class="ic">&#128260;</span><span>Actualizaciones de Windows<small>solo en escritorio</small></span></button>""")

# --- 2. Panel con el estado y los botones (después del panel de contraseña).
rep("""      <button class="btn-green" id="btnPsCambiar">&#128273; Cambiar contraseña</button>
    </div>
  </div>""",
"""      <button class="btn-green" id="btnPsCambiar">&#128273; Cambiar contraseña</button>
    </div>
  </div>

  <div class="panel" id="winUpdBox" hidden>
    <b>&#128260; Actualizaciones de Windows</b>
    <div class="share-note">Revisa si Windows tiene actualizaciones pendientes y las instala si tú lo pides. La búsqueda puede tardar varios minutos; la instalación puede tardar mucho más. Al final puede pedir reiniciar: la app NUNCA reinicia sola, tú decides cuándo.</div>
    <div class="line" id="wuUltima">Última actualización instalada: —</div>
    <div class="line" id="wuUltimaBusqueda">Última búsqueda: —</div>
    <div class="line" id="wuResumen">Sin buscar todavía.</div>
    <div id="wuLista"></div>
    <div class="line" id="wuEstado"></div>
    <div class="actions">
      <button class="btn-dark" id="btnWuBuscar">&#128269; Buscar actualizaciones</button>
      <button class="btn-green" id="btnWuInstalar" disabled>&#11015; Instalar actualizaciones</button>
    </div>
  </div>""")

# --- 3. togglePanel cierra también winUpdBox.
rep("['newBox', 'tplBox', 'reBox', 'detBox', 'passBox'].forEach(function (p) { if (p !== id) document.getElementById(p).hidden = true; });",
    "['newBox', 'tplBox', 'reBox', 'detBox', 'passBox', 'winUpdBox'].forEach(function (p) { if (p !== id) document.getElementById(p).hidden = true; });")

# --- 4. refreshDetectarBtn también muestra/oculta el botón de actualizaciones.
rep("""  // (257) Botón de contraseña: solo se muestra en escritorio; no depende
  // del estado de detección.
  var psBtn = document.getElementById('btnPassSistemas');
  if (psBtn) psBtn.hidden = !window.Desktop;
}""",
"""  // (257) Botón de contraseña: solo se muestra en escritorio; no depende
  // del estado de detección.
  var psBtn = document.getElementById('btnPassSistemas');
  if (psBtn) psBtn.hidden = !window.Desktop;
  // (258) Botón de actualizaciones: solo se muestra en escritorio; no
  // depende del estado de detección.
  var wuBtn = document.getElementById('btnWinUpd');
  if (wuBtn) wuBtn.hidden = !window.Desktop;
}""")

# --- 5. Lógica del panel (después del listener de btnPsCambiar).
rep("""  }).catch(function () { psLimpiar(); showToast('No se pudo cambiar la contraseña.'); }).then(function () { btn.disabled = false; });
});
document.getElementById('detList').addEventListener('click', function (e) {""",
"""  }).catch(function () { psLimpiar(); showToast('No se pudo cambiar la contraseña.'); }).then(function () { btn.disabled = false; });
});
// Actualizaciones de Windows (258): solo escritorio. Busca las pendientes
// con la API de Windows Update y, si el usuario lo pide, las instala (pide
// permiso de administrador). Nunca reinicia sola: si Windows pide
// reinicio, solo lo avisa. Nada de esto se guarda ni se manda a la nube.
var wuPendientes = [];
var wuOcupado = false;
function wuEstado(txt) { var el = document.getElementById('wuEstado'); if (el) el.textContent = txt || ''; }
function wuRefrescarBotones() {
  var b = document.getElementById('btnWuBuscar');
  var i = document.getElementById('btnWuInstalar');
  if (b) b.disabled = wuOcupado;
  if (i) i.disabled = wuOcupado || wuPendientes.length === 0;
}
function wuRenderLista() {
  var r = document.getElementById('wuResumen');
  var l = document.getElementById('wuLista');
  if (wuPendientes.length === 0) {
    if (r) r.textContent = 'Sin actualizaciones pendientes ✓';
    if (l) l.innerHTML = '';
  } else {
    if (r) r.textContent = 'Actualizaciones pendientes: ' + wuPendientes.length;
    if (l) l.innerHTML = wuPendientes.slice(0, 10).map(function (u) {
      return '<div>• ' + esc((u.kb ? u.kb + ' — ' : '') + (u.titulo || '')) + '</div>';
    }).join('') + (wuPendientes.length > 10 ? '<div>… y ' + (wuPendientes.length - 10) + ' más</div>' : '');
  }
  wuRefrescarBotones();
}
document.getElementById('btnWinUpd').addEventListener('click', function () { togglePanel('winUpdBox'); });
document.getElementById('btnWuBuscar').addEventListener('click', function () {
  if (!window.Desktop || typeof window.Desktop.buscarActualizaciones !== 'function') { showToast('La búsqueda solo funciona en la app de escritorio.'); return; }
  if (wuOcupado) return;
  wuOcupado = true; wuRefrescarBotones();
  wuEstado('Buscando actualizaciones… puede tardar varios minutos.');
  Promise.resolve(window.Desktop.buscarActualizaciones()).then(function (r) {
    wuOcupado = false;
    if (!r || !r.ok) { wuEstado(''); showToast((r && r.error) || 'Windows Update no respondió.'); wuRefrescarBotones(); return; }
    wuPendientes = (r.pendientes || []);
    var u = document.getElementById('wuUltima');
    if (u) u.textContent = 'Última actualización instalada: ' + (r.ultimaInstalada || '—');
    var b = document.getElementById('wuUltimaBusqueda');
    if (b) b.textContent = 'Última búsqueda: ' + (r.ultimaBusqueda || '—');
    wuEstado('');
    wuRenderLista();
    showToast(wuPendientes.length === 0 ? 'Windows está actualizado ✓' : 'Se encontraron ' + wuPendientes.length + ' actualizaciones pendientes.');
  }).catch(function () { wuOcupado = false; wuEstado(''); showToast('Windows Update no respondió.'); wuRefrescarBotones(); });
});
document.getElementById('btnWuInstalar').addEventListener('click', function () {
  if (!window.Desktop || typeof window.Desktop.instalarActualizaciones !== 'function') { showToast('La instalación solo funciona en la app de escritorio.'); return; }
  if (wuOcupado) return;
  if (wuPendientes.length === 0) { showToast('No hay actualizaciones pendientes para instalar.'); return; }
  wuOcupado = true; wuRefrescarBotones();
  wuEstado('Instalando actualizaciones… puede tardar mucho; no cierres la app.');
  Promise.resolve(window.Desktop.instalarActualizaciones()).then(function (r) {
    wuOcupado = false;
    if (!r || !r.ok) { wuEstado(''); showToast((r && r.error) || 'No se pudieron instalar las actualizaciones.'); wuRefrescarBotones(); return; }
    wuPendientes = [];
    var res = document.getElementById('wuResumen');
    if (res) res.textContent = 'Instalación terminada. Vuelve a buscar para ver si queda algo pendiente.';
    var li = document.getElementById('wuLista');
    if (li) li.innerHTML = '';
    wuRefrescarBotones();
    if ((r.instaladas || 0) === 0 && (r.fallidas || 0) === 0) { wuEstado(''); showToast('No había actualizaciones pendientes para instalar.'); return; }
    var msg = 'Actualizaciones instaladas: ' + (r.instaladas || 0);
    if (r.fallidas) msg += ' · fallaron: ' + r.fallidas;
    if (r.reinicioRequerido) msg += '. ⚠️ Windows pide reiniciar: la app no reinicia sola, reinicia cuando tú quieras.';
    wuEstado(r.reinicioRequerido ? '⚠️ Windows pide reiniciar para terminar. La app no reinicia sola.' : '');
    showToast(msg);
  }).catch(function () { wuOcupado = false; wuEstado(''); showToast('No se pudieron instalar las actualizaciones.'); wuRefrescarBotones(); });
});
document.getElementById('detList').addEventListener('click', function (e) {""")

# --- 6. Versiones 2.5.8 + mailto 258.
rep('Versión 2.5.7', 'Versión 2.5.8')
rep('Versión: 2.5.7', 'Versión: 2.5.8')
rep('Reporte de problema - Checklist de Soporte 257', 'Reporte de problema - Checklist de Soporte 258')
rep('Versión de la app: 257', 'Versión de la app: 258')

open(P, 'w', encoding='utf-8').write(s)
print('OK index.html, bytes:', len(s))
print('2.5.8:', s.count('2.5.8'), '| 2.5.7 restante:', s.count('2.5.7'), '| 257 mailto restante:', s.count('Soporte 257'))
print('btnWinUpd:', s.count('btnWinUpd'), '| winUpdBox:', s.count('winUpdBox'), '| buscarActualizaciones:', s.count('buscarActualizaciones'), '| instalarActualizaciones:', s.count('instalarActualizaciones'))
