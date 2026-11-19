# Parche web 2.5.15: «Enviar formulario en blanco» al número de
# WhatsApp del campo #fResp-wa.
# 1) respEnviarEnBlanco: si el campo trae un número válido, abre
# wa.me/<número>?text= con el mismo mensaje (invitación + enlace)
# usando mantWaNumber (mismo normalizador que el envío directo: 10
# dígitos → prefijo 52). Si el campo está vacío o el número es
# inválido (<10 dígitos tras normalizar), cae al chooser
# wa.me/?text= con el toast «No hay número de WhatsApp configurado,
# elige el contacto.». El número se lee del campo al pulsar; no cambia
# cómo se guarda el número ni el envío directo del técnico.
# 2) Nada más cambia: ni responsiva.html, ni firebase.js, ni
# firestore.rules. El bundle de Firebase NO cambia esta vez.
# 3) Versión 2.5.15 / versionCode 69 en www/index.html (login y Acerca
# de, mailto 264 -> 265), android/app/build.gradle e iOS
# (MARKETING_VERSION 2.5.15 / CURRENT_PROJECT_VERSION 69, Debug y
# Release).
# Uso: python3 patch_20265_web.py [ruta-base-del-proyecto]
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
    ('<p class="login-sub" style="font-size:11px;color:#999">Versión 2.5.14</p>',
     '<p class="login-sub" style="font-size:11px;color:#999">Versión 2.5.15</p>', 1),
    ('<div class="line">Versión: 2.5.14</div>',
     '<div class="line">Versión: 2.5.15</div>', 1),
    ("encodeURIComponent('Reporte de problema - Checklist de Soporte 264')",
     "encodeURIComponent('Reporte de problema - Checklist de Soporte 265')", 1),
    ("encodeURIComponent('Describe el problema:\\n\\n\\nVersión de la app: 264')",
     "encodeURIComponent('Describe el problema:\\n\\n\\nVersión de la app: 265')", 1),
])

# --- www/index.html: respEnviarEnBlanco al número del campo #fResp-wa.
patch(HTML, [
    ("""// (263) Responsivas en blanco por WhatsApp: mismo patrón que la firma
// de Mantenimientos (firma.html). Se crea el documento en Firestore
// (estado 'pendiente', sin datos) y se comparte el enlace público
// responsiva.html?id=<id> para elegir el contacto en WhatsApp; el
// colaborador lo llena en la página web y la lista se actualiza sola
// por la suscripción. Nada de borrador local para esto: el documento
// vive en la nube desde que se crea.""",
     """// (263) Responsivas en blanco por WhatsApp: mismo patrón que la firma
// de Mantenimientos (firma.html). Se crea el documento en Firestore
// (estado 'pendiente', sin datos) y se comparte el enlace público
// responsiva.html?id=<id>; el colaborador lo llena en la página web y
// la lista se actualiza sola por la suscripción. Nada de borrador
// local para esto: el documento vive en la nube desde que se crea.
// (265) El enlace se manda AL NÚMERO del campo #fResp-wa (mismo
// normalizador mantWaNumber que el envío directo: 10 dígitos →
 // prefijo 52). Sin número o inválido, cae al chooser wa.me/?text=.""",
     1),
    ("""    var url = RESP_URL_BASE + '?id=' + encodeURIComponent(id);
    window.open('https://wa.me/?text=' + encodeURIComponent('Por favor llena tus datos para crear tu responsiva: ' + url), '_blank');
    showToast('Responsiva creada, elige el contacto en WhatsApp.');
    return true;""",
     """    var url = RESP_URL_BASE + '?id=' + encodeURIComponent(id);
    var texto = 'Por favor llena tus datos para crear tu responsiva: ' + url;
    var waEl = document.getElementById('fResp-wa');
    var num = mantWaNumber(waEl ? waEl.value : '');
    if (!num || num.length < 10) {
      window.open('https://wa.me/?text=' + encodeURIComponent(texto), '_blank');
      showToast('No hay número de WhatsApp configurado, elige el contacto.');
      return true;
    }
    window.open('https://wa.me/' + num + '?text=' + encodeURIComponent(texto), '_blank');
    showToast('Responsiva creada, enviada al número de WhatsApp.');
    return true;""", 1),
])

# --- android/app/build.gradle: versionCode 69 / versionName 2.5.15.
patch(GRADLE, [
    ('        versionCode 68\n', '        versionCode 69\n', 1),
    ('        versionName "2.5.14"\n', '        versionName "2.5.15"\n', 1),
])

# --- iOS: MARKETING_VERSION 2.5.15 / CURRENT_PROJECT_VERSION 69 (Debug y Release).
patch(PBX, [
    ('MARKETING_VERSION = 2.5.14;', 'MARKETING_VERSION = 2.5.15;', 2),
    ('CURRENT_PROJECT_VERSION = 68;', 'CURRENT_PROJECT_VERSION = 69;', 2),
])

print('parche 2.5.15 aplicado')
