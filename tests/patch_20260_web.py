# Parche web 2.5.10: compartir un equipo detectado — WhatsApp recortado
# hasta Impresora, correo completo. detShareText(d, corto): con
# corto=true (WhatsApp) vuelve tras la línea de Impresora; sin el
# parámetro (correo, vía detShareMail) construye el texto completo de
# 2.5.9. El panel en pantalla no cambia.
# Uso: python3 patch_20260_web.py [ruta-a-index.html]
import sys

P = sys.argv[1] if len(sys.argv) > 1 else '/home/hatch/workspace/android/checklist-cloud/www/index.html'
s = open(P, encoding='utf-8').read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'NO ENCONTRADO x%d (esperado %d): %r' % (c, n, old[:120])
    s = s.replace(old, new)

# --- 1. detShareText con parámetro corto: el retorno temprano va justo
# después de la línea de Impresora; el resto (políticas, usuario
# sistemas, escritorio, SO detectado por, puntos, fecha) queda igual.
rep("""function detShareText(d) {
  d = d || {};""",
"""function detShareText(d, corto) {
  d = d || {};""")
rep("""  var imp = d.impresora || det.impresora || '';
  if (imp) lines.push('Impresora: ' + imp);
  var pol = d.politicas || det.politicas || null;""",
"""  var imp = d.impresora || det.impresora || '';
  if (imp) lines.push('Impresora: ' + imp);
  // WhatsApp (corto=true) termina aquí, en la línea de Impresora.
  // El correo usa el texto completo, con lo que sigue.
  if (corto) return lines.join('\\n');
  var pol = d.politicas || det.politicas || null;""")

# --- 2. Los dos botones de WhatsApp (Por preparar y Mantenimientos)
# usan la variante corta; el correo sigue con detShareMail (completo).
rep("if (wa) shareText(detShareText(dd)); else detShareMail(dd);",
    "if (wa) shareText(detShareText(dd, true)); else detShareMail(dd);", n=2)

# --- 3. Versión 2.5.10.
rep("Versión 2.5.9", "Versión 2.5.10")
rep("Versión: 2.5.9", "Versión: 2.5.10")
rep("Soporte 259", "Soporte 260")
rep("Versión de la app: 259", "Versión de la app: 260")

open(P, 'w', encoding='utf-8').write(s)
print('parche web 2.5.10 aplicado a ' + P)
