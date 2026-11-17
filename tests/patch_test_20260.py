# Parche de pruebas 2.5.10: test20259.js -> test20260.js.
# 1) Copia test20259.js a test20260.js y actualiza la versión (2.5.9 ->
# 2.5.10, mailto 259 -> 260). 2) Agrega la serie 260: WhatsApp recortado
# hasta Impresora, correo completo, sin impresora no hay línea Impresora,
# panel en pantalla sin cambios. La serie 259 queda intacta (el texto
# completo de detShareText(d) sigue siendo el del correo).
# Uso: python3 patch_test_20260.py (corre desde tests/)
import shutil

SRC = '/home/hatch/workspace/android/checklist-cloud/tests/test20259.js'
P = '/home/hatch/workspace/android/checklist-cloud/tests/test20260.js'
shutil.copyfile(SRC, P)
s = open(P, encoding='utf-8').read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'NO ENCONTRADO x%d (esperado %d): %r' % (c, n, old[:120])
    s = s.replace(old, new)

# --- SRC y versión 2.5.10 (orden: primero 2.5.9 -> 2.5.10, luego 2.5.8 -> 2.5.9).
rep("const SRC = fs.readFileSync(__dirname + '/checklist20259.js', 'utf8');",
    "const SRC = fs.readFileSync(__dirname + '/checklist20260.js', 'utf8');")
rep("html.includes('Versión 2.5.9')", "html.includes('Versión 2.5.10')", n=4)
rep("html.includes('Versión: 2.5.9')", "html.includes('Versión: 2.5.10')", n=2)
rep("html.includes('Versión 2.5.8')", "html.includes('Versión 2.5.9')", n=2)
rep("!html.includes('2.5.8')", "!html.includes('2.5.9')", n=3)
rep("(html.match(/2\\.5\\.9/g) || []).length", "(html.match(/2\\.5\\.10/g) || []).length")
rep("var n259 = ", "var n260 = ")
rep("n259 === 2", "n260 === 2", n=2)
rep("'AM0) versión 2.5.9:'", "'AM0) versión 2.5.10:'")
rep("'AP0) estáticos 2.5.9:", "'AP0) estáticos 2.5.10:")
rep("'AR0) versión 2.5.9 visible:'", "'AR0) versión 2.5.10 visible:'")
rep("'| 0 de 2.5.8:'", "'| 0 de 2.5.9:'", n=2)
rep("'| ocurrencias 2.5.9:'", "'| ocurrencias 2.5.10:'")
rep("'BA0) versión 2.5.9 sin 2.5.8:'", "'BA0) versión 2.5.10 sin 2.5.9:'")
rep("'BB0) 2.5.9 en 2 sitios:'", "'BB0) 2.5.10 en 2 sitios:'")
rep("html.indexOf('Soporte 259')", "html.indexOf('Soporte 260')", n=3)
rep("console.log('259D) nada guardado en localStorage:', d259noguarda, '| mailto 259:'",
    "console.log('259D) nada guardado en localStorage:', d259noguarda, '| mailto 260:'")

# --- Serie 260 nueva, antes de process.exit(0).
serie260 = """
  // 260: serie nueva — WhatsApp recortado hasta Impresora, correo completo.
  // 260A: detShareText(d, true) termina en Impresora; detShareText(d)
  // (correo) sigue completo; sin impresora no hay línea de Impresora.
  detectados = [det259()];
  var txt260corto = detShareText(detectados[0], true);
  var a260corto = txt260corto.indexOf('Dell Pro 14 PC14250') !== -1 && txt260corto.indexOf('Serie: 8TKKQJ4') !== -1 && txt260corto.indexOf('Hostname: PC-SHARE') !== -1 && txt260corto.indexOf('Procesador: Intel Core Ultra 5 235U') !== -1 && txt260corto.indexOf('RAM: 16 GB') !== -1 && txt260corto.indexOf('Disco: 512 GB NVMe') !== -1 && txt260corto.indexOf('IP: 192.168.1.78 (Dinámica)') !== -1 && txt260corto.indexOf('Wi-Fi: 192.168.1.78 (Dinámica)') !== -1 && txt260corto.indexOf('AnyDesk: 123 456 789 (ROBIT5)') !== -1 && txt260corto.indexOf('ESET Security 13.1.2036.0') !== -1 && txt260corto.indexOf('Agente ESET: 13.3.1192.0') !== -1 && txt260corto.indexOf('Chrome: 157.0.8103.79') !== -1 && txt260corto.indexOf('Impresora: HP LaserJet Pro') !== -1 && txt260corto.trim().split('\\n').pop() === 'Impresora: HP LaserJet Pro' && txt260corto.indexOf('Políticas:') === -1 && txt260corto.indexOf('Usuario de sistemas:') === -1 && txt260corto.indexOf('Escritorio revisado') === -1 && txt260corto.indexOf('SO detectado por') === -1 && txt260corto.indexOf('Detectado') === -1 && txt260corto.indexOf('por Gerardo') === -1;
  var txt260full = detShareText(detectados[0]);
  var a260full = txt260full.indexOf('Impresora: HP LaserJet Pro') !== -1 && txt260full.indexOf('Políticas:') !== -1 && txt260full.indexOf('cambio cada 42 días') !== -1 && txt260full.indexOf('Usuario de sistemas: Sí') !== -1 && txt260full.indexOf('por Gerardo') !== -1 && (txt260full.match(/Detectado:/g) || []).length === 2;
  var d260sinImp = det259({ impresora: '', detalles: { impresora: '', politicas: { cambioDias: 42, minLongitud: 0, bloqueoIntentos: 10, bloqueoSegundos: 300, bloqueoManual: false }, politicasFuente: 'directiva (secedit)', usuarioSistemas: true, escritorioRutas: ['C:\\\\Users\\\\Gerardo\\\\Desktop'], atajosVistos: 5, osFuente: 'registro' } });
  var txt260sinImp = detShareText(d260sinImp, true);
  var a260sinImp = txt260sinImp.indexOf('Impresora:') === -1 && txt260sinImp.indexOf('Chrome: 157.0.8103.79') !== -1 && txt260sinImp.trim().endsWith('Chrome: 157.0.8103.79') && txt260sinImp.slice(-1) !== '\\n';
  console.log('260A) WhatsApp corto termina en Impresora:', a260corto, '| correo completo:', a260full, '| sin impresora no hay línea Impresora:', a260sinImp);
  // 260B: clic en WhatsApp abre wa.me con el texto CORTO (ambos paneles);
  // el detectado sigue sin usar y sin llamadas a Cloud.
  opened259.length = 0; cloud259.length = 0;
  clickDet259('[data-det-wa]', 'DET-SHARE');
  var wa260txt = opened259.length === 1 && opened259[0].indexOf('https://wa.me/?text=') === 0 ? decodeURIComponent(opened259[0].split('text=')[1]) : '';
  var b260wa = opened259.length === 1 && wa260txt.indexOf('Impresora: HP LaserJet Pro') !== -1 && wa260txt.trim().split('\\n').pop() === 'Impresora: HP LaserJet Pro' && wa260txt.indexOf('Políticas:') === -1 && wa260txt.indexOf('Detectado') === -1 && detectados[0].usado === false && cloud259.length === 0;
  opened259.length = 0; cloud259.length = 0;
  clickMant259('[data-mant-det-wa]', 'DET-SHARE');
  var wa260mant = opened259.length === 1 && opened259[0].indexOf('https://wa.me/?text=') === 0 ? decodeURIComponent(opened259[0].split('text=')[1]) : '';
  var b260mantWa = opened259.length === 1 && wa260mant.trim().split('\\n').pop() === 'Impresora: HP LaserJet Pro' && wa260mant.indexOf('Políticas:') === -1 && detectados[0].usado === false && cloud259.length === 0;
  console.log('260B) WhatsApp #detList texto corto:', b260wa, '| WhatsApp #mantDetList texto corto:', b260mantWa);
  // 260C: clic en correo abre mailto con el texto COMPLETO (ambos paneles).
  clickDet259('[data-det-mail]', 'DET-SHARE');
  var mail260 = global.location.href;
  var c260body = decodeURIComponent(mail260.split('&body=')[1]);
  var c260mail = mail260.indexOf('mailto:?subject=') === 0 && decodeURIComponent(mail260.split('subject=')[1].split('&body=')[0]) === 'Equipo detectado: PC-SHARE' && c260body.indexOf('Políticas:') !== -1 && c260body.indexOf('cambio cada 42 días') !== -1 && c260body.indexOf('Usuario de sistemas: Sí') !== -1 && c260body.indexOf('por Gerardo') !== -1 && detectados[0].usado === false && cloud259.length === 0;
  clickMant259('[data-mant-det-mail]', 'DET-SHARE');
  var c260mantBody = decodeURIComponent(global.location.href.split('&body=')[1]);
  var c260mantMail = global.location.href.indexOf('mailto:?subject=') === 0 && c260mantBody.indexOf('Políticas:') !== -1 && c260mantBody.indexOf('por Gerardo') !== -1;
  console.log('260C) correo #detList cuerpo completo:', c260mail, '| correo #mantDetList cuerpo completo:', c260mantMail);
  // 260D: el panel en pantalla no cambió (el recorte es solo del texto
  // compartido por WhatsApp): sigue con versiones, detectado por y los
  // dos botones de compartir; nada nuevo en localStorage.
  var d260panel = html259det.indexOf('ESET Security 13.1.2036.0') !== -1 && html259det.indexOf('por Gerardo') !== -1 && html259det.indexOf('Chrome: 157.0.8103.79') !== -1 && html259det.indexOf('data-det-wa="DET-SHARE"') !== -1 && html259det.indexOf('data-det-mail="DET-SHARE"') !== -1;
  var ls260 = JSON.stringify(global.localStorage._d);
  var d260noguarda = ls260.indexOf('PC-SHARE') === -1 && ls260.indexOf('8TKKQJ4') === -1;
  console.log('260D) panel en pantalla sigue completo:', d260panel, '| nada guardado en localStorage:', d260noguarda);

"""
anchor = "\n  process.exit(0);"
assert s.count(anchor) == 1
s = s.replace(anchor, serie260 + anchor)
open(P, 'w', encoding='utf-8').write(s)
print('parche de pruebas 2.5.10 aplicado a ' + P)
