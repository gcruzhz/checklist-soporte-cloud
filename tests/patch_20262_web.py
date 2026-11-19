# Parche web 2.5.12: Responsiva con guardar y cerrar (borrador local).
# 1) Botón nuevo «💾 Guardar y cerrar» (#btnRespGuardar) en #viewResp:
# guarda los 6 campos tal como están (aunque estén incompletos) en
# localStorage (checklist-soporte-resp-borrador-v1), muestra el toast
# «Responsiva guardada» y vuelve a Inicio. El número de WhatsApp NO
# forma parte del borrador (persiste aparte, en su propia clave).
# 2) Al abrir la vista (showVista('resp')) el borrador, si existe, se
# restaura en los 6 campos (también la primera vez tras arrancar).
# 3) Enviar (con número o sin él, vía shareText) borra el borrador y
# vacía los 6 campos; si la validación falla o el número es inválido,
# no se borra nada. 4) Limpiar vacía los 6 campos y borra el borrador.
# 5) Versión 2.5.12 / versionCode 66 en www/index.html (login y Acerca
# de, mailto 261 -> 262), android/app/build.gradle e iOS
# (MARKETING_VERSION 2.5.12 / CURRENT_PROJECT_VERSION 66, Debug y
# Release). El bundle de Firebase NO se toca.
# Uso: python3 patch_20262_web.py [ruta-base-del-proyecto]
import os
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else '/home/hatch/workspace/android/checklist-cloud'
HTML = os.path.join(BASE, 'www/index.html')
GRADLE = os.path.join(BASE, 'android/app/build.gradle')
PBX = os.path.join(BASE, 'ios/App/App.xcodeproj/project.pbxproj')


def patch(path, pairs):
    s = open(path, encoding='utf-8').read()
    for old, new, n in pairs:
        c = s.count(old)
        assert c == n, '%s: NO ENCONTRADO x%d (esperado %d): %r' % (path, c, n, old[:120])
        s = s.replace(old, new)
    open(path, 'w', encoding='utf-8').write(s)
    return s


# --- www/index.html: versión y mailto.
patch(HTML, [
    ('<p class="login-sub" style="font-size:11px;color:#999">Versión 2.5.11</p>',
     '<p class="login-sub" style="font-size:11px;color:#999">Versión 2.5.12</p>', 1),
    ('<div class="line">Versión: 2.5.11</div>',
     '<div class="line">Versión: 2.5.12</div>', 1),
    ("encodeURIComponent('Reporte de problema - Checklist de Soporte 261')",
     "encodeURIComponent('Reporte de problema - Checklist de Soporte 262')", 1),
    ("encodeURIComponent('Describe el problema:\\n\\n\\nVersión de la app: 261')",
     "encodeURIComponent('Describe el problema:\\n\\n\\nVersión de la app: 262')", 1),
])

# --- www/index.html: nota de la vista (el borrador sí se guarda en el teléfono).
patch(HTML, [
    ('Formulario de responsiva del colaborador: se envía por WhatsApp al número configurado. No se guarda en la nube ni en el teléfono (solo el número se recuerda en este teléfono).',
     'Formulario de responsiva del colaborador: se envía por WhatsApp al número configurado. No se guarda en la nube; el borrador y el número se guardan solo en este teléfono.', 1),
])

# --- www/index.html: botón Guardar y cerrar junto a Enviar y Limpiar.
patch(HTML, [
    ("""        <button class="btn-green" id="btnRespEnviar">📲 Enviar por WhatsApp</button>
        <button class="btn-ghost" id="btnRespLimpiar">Limpiar</button>""",
     """        <button class="btn-green" id="btnRespEnviar">📲 Enviar por WhatsApp</button>
        <button class="btn-ghost" id="btnRespGuardar">💾 Guardar y cerrar</button>
        <button class="btn-ghost" id="btnRespLimpiar">Limpiar</button>""", 1),
])

# --- www/index.html: comentario y clave del borrador.
patch(HTML, [
    ("""// (261) Responsiva: formulario que se envía por WhatsApp al número
// configurado. El formulario NO se guarda en la nube ni en localStorage:
// solo el número de WhatsApp persiste, en este teléfono.
// Los 6 campos son obligatorios; los que falten se marcan con
// .campo-falta y el toast los nombra (mismo patrón que Mantenimientos).
var RESP_WA_KEY = 'checklist-soporte-resp-wa-v1';""",
     """// (262) Responsiva: formulario que se envía por WhatsApp al número
// configurado. El formulario NO se guarda en la nube: solo vive en este
// teléfono como borrador en localStorage (RESP_BORRADOR_KEY), que se
// guarda con «Guardar y cerrar» aunque esté incompleto, se restaura al
// abrir la vista y se borra al enviar o al Limpiar. El número de
// WhatsApp persiste aparte, en su propia clave (RESP_WA_KEY).
// Los 6 campos son obligatorios; los que falten se marcan con
// .campo-falta y el toast los nombra (mismo patrón que Mantenimientos).
var RESP_WA_KEY = 'checklist-soporte-resp-wa-v1';
var RESP_BORRADOR_KEY = 'checklist-soporte-resp-borrador-v1';""", 1),
])

# --- www/index.html: funciones del borrador, tras respCargarWa.
patch(HTML, [
    ("""function respCargarWa() {
  var el = document.getElementById('fResp-wa');
  if (!el) return;
  try { el.value = localStorage.getItem(RESP_WA_KEY) || ''; } catch (e) { el.value = ''; }
}""",
     """function respCargarWa() {
  var el = document.getElementById('fResp-wa');
  if (!el) return;
  try { el.value = localStorage.getItem(RESP_WA_KEY) || ''; } catch (e) { el.value = ''; }
}
function respGuardarBorrador() {
  var d = {};
  RESP_CAMPOS.forEach(function (c) {
    var el = document.getElementById(c[0]);
    d[c[0]] = el ? el.value : '';
  });
  try { localStorage.setItem(RESP_BORRADOR_KEY, JSON.stringify(d)); } catch (e) {}
}
function respCargarBorrador() {
  var d = null;
  try { d = JSON.parse(localStorage.getItem(RESP_BORRADOR_KEY) || 'null'); } catch (e) { d = null; }
  if (!d) return;
  RESP_CAMPOS.forEach(function (c) {
    var el = document.getElementById(c[0]);
    if (el) el.value = d[c[0]] || '';
  });
}
function respBorrarBorrador() {
  try { localStorage.removeItem(RESP_BORRADOR_KEY); } catch (e) {}
}
function respGuardarYCerrar() {
  respGuardarBorrador();
  showToast('Responsiva guardada');
  showVista('inicio');
}
// Tras enviar (con número o sin él): la responsiva ya se fue, el
// borrador se borra y el formulario queda vacío para la próxima.
function respDespuesDeEnviar() {
  respBorrarBorrador();
  RESP_CAMPOS.forEach(function (c) {
    var el = document.getElementById(c[0]);
    if (el) { el.value = ''; el.classList.remove('campo-falta'); }
  });
}""", 1),
])

# --- www/index.html: Enviar borra el borrador y vacía los campos tras
# abrir WhatsApp (en las dos ramas); la validación y el número inválido
# salen antes y no borran nada.
patch(HTML, [
    ("""  var texto = respTexto();
  if (!num) {
    showToast('No hay número de WhatsApp guardado: elige el contacto en WhatsApp.');
    shareText(texto);
    return;
  }
  window.open('https://wa.me/' + num + '?text=' + encodeURIComponent(texto), '_blank');
}""",
     """  var texto = respTexto();
  if (!num) {
    showToast('No hay número de WhatsApp guardado: elige el contacto en WhatsApp.');
    shareText(texto);
    respDespuesDeEnviar();
    return;
  }
  window.open('https://wa.me/' + num + '?text=' + encodeURIComponent(texto), '_blank');
  respDespuesDeEnviar();
}""", 1),
])

# --- www/index.html: Limpiar también borra el borrador.
patch(HTML, [
    ("""function respLimpiar() {
  RESP_CAMPOS.forEach(function (c) {""",
     """function respLimpiar() {
  respBorrarBorrador();
  RESP_CAMPOS.forEach(function (c) {""", 1),
])

# --- www/index.html: al abrir la vista se restaura el borrador.
patch(HTML, [
    ("  if (v === 'resp') { respCargarWa(); }",
     "  if (v === 'resp') { respCargarWa(); respCargarBorrador(); }", 1),
])

# --- www/index.html: cablear el botón Guardar y cerrar.
patch(HTML, [
    ("""document.getElementById('btnRespEnviar').addEventListener('click', function () { respEnviar(); });
document.getElementById('btnRespLimpiar').addEventListener('click', function () { respLimpiar(); });""",
     """document.getElementById('btnRespEnviar').addEventListener('click', function () { respEnviar(); });
document.getElementById('btnRespGuardar').addEventListener('click', function () { respGuardarYCerrar(); });
document.getElementById('btnRespLimpiar').addEventListener('click', function () { respLimpiar(); });""", 1),
])

# --- android/app/build.gradle: versionCode 66 / versionName 2.5.12.
patch(GRADLE, [
    ('        versionCode 65\n', '        versionCode 66\n', 1),
    ('        versionName "2.5.11"\n', '        versionName "2.5.12"\n', 1),
])

# --- iOS: MARKETING_VERSION 2.5.12 / CURRENT_PROJECT_VERSION 66 (Debug y Release).
patch(PBX, [
    ('MARKETING_VERSION = 2.5.11;', 'MARKETING_VERSION = 2.5.12;', 2),
    ('CURRENT_PROJECT_VERSION = 65;', 'CURRENT_PROJECT_VERSION = 66;', 2),
])

print('parche 2.5.12 aplicado')
