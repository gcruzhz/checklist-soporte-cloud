# Parche de pruebas 2.5.13: test20262.js -> test20263.js.
# 1) Extrae el <script> actual de www/index.html a
# tests/checklist20263.js (el JavaScript de esta version, que evalua el
# harness). 2) Copia test20262.js a test20263.js y actualiza la version
# (2.5.12 -> 2.5.13, mailto 262 -> 263). 3) Agrega la serie 263:
# Responsiva en blanco por WhatsApp (mismo patron que la firma de
# Mantenimientos): boton nuevo crea la responsiva en Cloud (simulado)
# y abre wa.me/?text= con responsiva.html?id=...; sin nube avisa con
# toast y no abre nada; la lista suscrita muestra pendientes y
# llenadas (con los 6 datos y los 4 botones por tarjeta); el dispatch
# delegado copia el enlace de una pendiente, comparte por WhatsApp y
# por correo una llenada, y guarda su Excel (.xlsx real con los 6
# datos); la lista se actualiza sola al llegar el llenado; el
# formulario directo del tecnico (2.5.11/2.5.12) sigue intacto.
# Uso: python3 patch_test_20263.py (corre desde tests/)
import os
import shutil

BASE = '/home/hatch/workspace/android/checklist-cloud'
TESTS = os.path.join(BASE, 'tests')
SRC = os.path.join(TESTS, 'test20262.js')
P = os.path.join(TESTS, 'test20263.js')

# --- Extraer el <script> actual de www/index.html.
html = open(os.path.join(BASE, 'www/index.html'), encoding='utf-8').read()
i = html.index('<script>', html.index('firebase-config'))
j = html.index('</script>', i)
open(os.path.join(TESTS, 'checklist20263.js'), 'w', encoding='utf-8').write(html[i + len('<script>'):j])
print('checklist20263.js extraido:', j - i - len('<script>'), 'bytes')

shutil.copyfile(SRC, P)
s = open(P, encoding='utf-8').read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'NO ENCONTRADO x%d (esperado %d): %r' % (c, n, old[:120])
    s = s.replace(old, new)


# --- SRC y version 2.5.13 (orden: primero 2.5.12 -> 2.5.13, luego 2.5.11 -> 2.5.12).
rep("const SRC = fs.readFileSync(__dirname + '/checklist20262.js', 'utf8');",
    "const SRC = fs.readFileSync(__dirname + '/checklist20263.js', 'utf8');")
rep("html.includes('Versión 2.5.12')", "html.includes('Versión 2.5.13')", n=4)
rep("html.includes('Versión: 2.5.12')", "html.includes('Versión: 2.5.13')", n=2)
rep("html.includes('Versión 2.5.11')", "html.includes('Versión 2.5.12')", n=2)
rep("!html.includes('2.5.11')", "!html.includes('2.5.12')", n=3)
rep("(html.match(/2\\.5\\.12/g) || []).length", "(html.match(/2\\.5\\.13/g) || []).length")
rep("var n262 = ", "var n263 = ")
rep("n262 === 2", "n263 === 2", n=2)
rep("'AM0) versión 2.5.12:'", "'AM0) versión 2.5.13:'")
rep("'AP0) estáticos 2.5.12:", "'AP0) estáticos 2.5.13:")
rep("'AR0) versión 2.5.12 visible:'", "'AR0) versión 2.5.13 visible:'")
rep("'| 0 de 2.5.11:'", "'| 0 de 2.5.12:'", n=2)
rep("'| ocurrencias 2.5.12:'", "'| ocurrencias 2.5.13:'")
rep("'BA0) versión 2.5.12 sin 2.5.11:'", "'BA0) versión 2.5.13 sin 2.5.12:'")
rep("'BB0) 2.5.12 en 2 sitios:'", "'BB0) 2.5.13 en 2 sitios:'")
rep("html.indexOf('Soporte 262')", "html.indexOf('Soporte 263')", n=3)
rep("'| mailto 262:'", "'| mailto 263:'", n=3)

# --- Serie 263 nueva, antes de process.exit(0).
serie263 = """
  // 263: serie nueva — Responsiva en blanco por WhatsApp (mismo patron
  // que la firma de Mantenimientos): se crea en Firestore y se comparte
  // el enlace responsiva.html?id=<id>; el colaborador la llena en la
  // pagina y la lista se actualiza sola por suscripcion.
  // 263A: el boton, la seccion y la lista existen en el HTML; el codigo
  // (app, firebase.js y reglas) trae lo nuevo.
  var fb263 = fs.readFileSync('/home/hatch/workspace/android/checklist-cloud/www/cloud/firebase.js', 'utf8');
  var rules263 = fs.readFileSync('/home/hatch/workspace/android/checklist-cloud/firestore.rules', 'utf8');
  var a263html = html.indexOf('id="btnRespBlanco"') !== -1 && html.indexOf('Enviar formulario en blanco') !== -1 &&
    html.indexOf('Responsivas enviadas') !== -1 && html.indexOf('id="respList"') !== -1 &&
    html.includes('Versión 2.5.13') && !html.includes('2.5.12');
  var a263src = SRC.indexOf('function respEnviarEnBlanco') !== -1 && SRC.indexOf('function renderRespList') !== -1 &&
    SRC.indexOf('function respGuardarExcel') !== -1 && SRC.indexOf('function respXlsxBlob') !== -1 &&
    SRC.indexOf('function respCopiarEnlace') !== -1 && SRC.indexOf('function respEnviarCorreo') !== -1 &&
    SRC.indexOf('data-resp-wa') !== -1 && SRC.indexOf('data-resp-mail') !== -1 &&
    SRC.indexOf('data-resp-xlsx') !== -1 && SRC.indexOf('data-resp-copy') !== -1 &&
    SRC.indexOf('responsiva.html?id=') !== -1 && SRC.indexOf('RESP_URL_BASE') !== -1;
  var a263fb = fb263.indexOf('async function crearResponsiva') !== -1 &&
    fb263.indexOf('function subscribeResponsivas') !== -1 &&
    fb263.indexOf("estado: 'pendiente'") !== -1 && fb263.indexOf('crearResponsiva,') !== -1 &&
    fb263.indexOf('subscribeResponsivas,') !== -1;
  var a263rules = rules263.indexOf('match /responsivas/{id}') !== -1 &&
    rules263.indexOf('allow get: if true;') !== -1 &&
    rules263.indexOf("changedKeys().hasOnly(['datos', 'estado', 'llenadoEn'])") !== -1 &&
    rules263.indexOf("request.resource.data.estado == 'llenada'") !== -1 &&
    rules263.indexOf('request.resource.data.datos.nombre is string') !== -1 &&
    rules263.indexOf('request.resource.data.datos.area is string') !== -1;
  console.log('263A) boton + lista en HTML:', a263html, '| funciones en la app:', a263src, '| crearResponsiva + subscribe en firebase.js:', a263fb, '| bloque responsivas en reglas:', a263rules);
  // 263B: sin nube (modo local del harness) el boton avisa con toast y
  // no abre WhatsApp ni llama a Cloud.
  opened259.length = 0;
  document.getElementById('btnRespBlanco')._h.click[0]();
  var b263 = opened259.length === 0 && toastTxt().indexOf('necesita conexión a la nube') !== -1;
  console.log('263B) sin nube: no abre WhatsApp y avisa:', b263);
  // 263C: con Cloud simulado crea la responsiva (con el nombre del
  // tecnico) y abre wa.me/?text= con el enlace responsiva.html?id=...
  // para elegir contacto (sin numero fijo).
  doLogin('usuario');
  var cloud263 = [];
  global.Cloud.crearResponsiva = async function (nombre) { cloud263.push(nombre); return 'RESP-ABC123'; };
  CLOUD_ENABLED = true;
  opened259.length = 0;
  var ok263c = await respEnviarEnBlanco();
  var url263c = opened259.length === 1 ? opened259[0] : '';
  var txt263c = url263c.indexOf('https://wa.me/?text=') === 0 ? decodeURIComponent(url263c.split('text=')[1]) : '';
  var c263 = ok263c === true && cloud263.length === 1 && cloud263[0] === 'Test User' &&
    opened259.length === 1 && url263c.indexOf('https://wa.me/?text=') === 0 &&
    txt263c.indexOf('https://checklist-soporte.web.app/responsiva.html?id=RESP-ABC123') !== -1 &&
    txt263c.indexOf('llena tu responsiva') !== -1 && toastTxt().indexOf('Responsiva creada') !== -1;
  CLOUD_ENABLED = false;
  console.log('263C) crea con el nombre del tecnico y abre wa.me con el enlace:', c263);
  // 263D: la lista suscrita muestra pendientes y llenadas: la llenada
  // trae los 6 datos y los 3 botones; la pendiente trae Copiar enlace.
  // El usuario normal suscribe solo con su uid.
  var cb263 = null; var uid263 = null;
  global.Cloud.subscribeResponsivas = function (cb, uid) { cb263 = cb; uid263 = uid; return function () {}; };
  CLOUD_ENABLED = true;
  showVista('resp');
  var d263sub = typeof cb263 === 'function' && uid263 === 'u1';
  var r263pend = { id: 'R1', creadoPor: 'u1', creadoPorNombre: 'Test User', creadoEn: Date.now() - 60000, estado: 'pendiente', datos: null };
  var r263llen = { id: 'R2', creadoPor: 'u1', creadoPorNombre: 'Test User', creadoEn: Date.now(), estado: 'llenada', llenadoEn: Date.now(),
    datos: { nombre: 'Juan Pérez López', colaborador: '98765', sucursal: 'Polanco', puesto: 'Técnico', jefe: 'María García', area: 'Sistemas' } };
  cb263([r263pend, r263llen]);
  var list263 = document.getElementById('respList').innerHTML;
  var d263lista = list263.indexOf('Pendiente') !== -1 && list263.indexOf('Llenada') !== -1 &&
    list263.indexOf('Juan Pérez López') !== -1 && list263.indexOf('Número de colaborador: 98765') !== -1 &&
    list263.indexOf('Sucursal: Polanco') !== -1 && list263.indexOf('Puesto: Técnico') !== -1 &&
    list263.indexOf('Jefe Directo: María García') !== -1 && list263.indexOf('Área: Sistemas') !== -1 &&
    list263.indexOf('data-resp-copy="R1"') !== -1 && list263.indexOf('data-resp-wa="R2"') !== -1 &&
    list263.indexOf('data-resp-mail="R2"') !== -1 && list263.indexOf('data-resp-xlsx="R2"') !== -1 &&
    list263.indexOf('Copiar enlace') !== -1 && list263.indexOf('Compartir por WhatsApp') !== -1 &&
    list263.indexOf('Enviar por correo') !== -1 && list263.indexOf('Guardar en Excel') !== -1 &&
    list263.indexOf('data-resp-xlsx') < list263.indexOf('data-resp-copy');
  console.log('263D) suscribe con uid propio:', d263sub, '| lista con pendiente y llenada:', d263lista);
  // 263E: el dispatch delegado de la lista: copiar el enlace de una
  // pendiente, compartir por WhatsApp y por correo una llenada, y
  // guardar su Excel (.xlsx real con los 6 datos); al llegar el
  // llenado, la tarjeta se actualiza sola.
  function clickResp263(attr, id) {
    var t = { classList: { contains() { return false; } },
      closest(sel) { return sel === '[' + attr + ']' ? { getAttribute(a) { return id; } } : null; },
      hasAttribute(a) { return a === attr; },
      getAttribute(a) { return id; } };
    els['respList']._h.click[0]({ target: t });
  }
  opened259.length = 0;
  clickResp263('data-resp-copy', 'R1');
  var url263copy = opened259.length === 1 ? opened259[0] : '';
  var e263copy = opened259.length === 1 && url263copy.indexOf('https://wa.me/?text=') === 0 &&
    decodeURIComponent(url263copy.split('text=')[1]).indexOf('https://checklist-soporte.web.app/responsiva.html?id=R1') !== -1;
  opened259.length = 0;
  clickResp263('data-resp-wa', 'R2');
  var wa263 = opened259.length === 1 && opened259[0].indexOf('https://wa.me/?text=') === 0 ? decodeURIComponent(opened259[0].split('text=')[1]) : '';
  var e263wa = opened259.length === 1 && wa263.indexOf('Responsiva — Checklist de Soporte') !== -1 &&
    wa263.indexOf('Nombre Completo: Juan Pérez López') !== -1 && wa263.indexOf('Número de colaborador: 98765') !== -1 &&
    wa263.indexOf('Sucursal: Polanco') !== -1 && wa263.indexOf('Puesto: Técnico') !== -1 &&
    wa263.indexOf('Jefe Directo: María García') !== -1 && wa263.indexOf('Área: Sistemas') !== -1;
  global.location.href = '';
  clickResp263('data-resp-mail', 'R2');
  var mail263 = global.location.href;
  var e263mail = mail263.indexOf('mailto:?subject=Responsiva%3A%20Juan%20P%C3%A9rez%20L%C3%B3pez') === 0 &&
    decodeURIComponent(mail263.split('&body=')[1]).indexOf('Nombre Completo: Juan Pérez López') !== -1 &&
    decodeURIComponent(mail263.split('&body=')[1]).indexOf('Área: Sistemas') !== -1;
  global.location.href = '';
  var blob263 = respXlsxBlob(r263llen);
  var txt263xlsx = Buffer.from(await blob263.arrayBuffer()).toString('utf8');
  var e263blob = txt263xlsx.indexOf('Juan Pérez López') !== -1 && txt263xlsx.indexOf('98765') !== -1 &&
    txt263xlsx.indexOf('Polanco') !== -1 && txt263xlsx.indexOf('Técnico') !== -1 &&
    txt263xlsx.indexOf('María García') !== -1 && txt263xlsx.indexOf('Sistemas') !== -1 &&
    txt263xlsx.indexOf('Nombre Completo') !== -1 && txt263xlsx.indexOf('Número de colaborador') !== -1;
  clickResp263('data-resp-xlsx', 'R2');
  await sleep(50);
  var e263xlsx = e263blob && toastTxt().indexOf('Excel descargado: responsiva-juan-p-rez-l-pez.xlsx') !== -1;
  var r263pendLlen = { id: 'R1', creadoPor: 'u1', creadoPorNombre: 'Test User', creadoEn: Date.now() - 60000, estado: 'llenada', llenadoEn: Date.now(),
    datos: { nombre: 'Ana Ruiz', colaborador: '11111', sucursal: 'Roma Norte', puesto: 'Analista', jefe: 'Luis Torres', area: 'Ventas' } };
  cb263([r263pendLlen, r263llen]);
  var list263b = document.getElementById('respList').innerHTML;
  var e263vivo = list263b.indexOf('data-resp-copy="R1"') === -1 && list263b.indexOf('Ana Ruiz') !== -1 &&
    list263b.indexOf('data-resp-wa="R1"') !== -1 && list263b.indexOf('data-resp-xlsx="R1"') !== -1;
  console.log('263E) copiar enlace de pendiente:', e263copy, '| WhatsApp de llenada:', e263wa, '| correo de llenada:', e263mail, '| Excel .xlsx con los 6 datos:', e263xlsx, '| al llenarse se actualiza sola:', e263vivo);
  // 263F: el formulario directo del técnico (2.5.11/2.5.12) sigue
  // intacto: Enviar por WhatsApp con número y Guardar y cerrar.
  document.getElementById('fResp-nombre').value = 'Juan Pérez López';
  document.getElementById('fResp-colaborador').value = '98765';
  document.getElementById('fResp-sucursal').value = 'Polanco';
  document.getElementById('fResp-puesto').value = 'Técnico';
  document.getElementById('fResp-jefe').value = 'María García';
  document.getElementById('fResp-area').value = 'Sistemas';
  document.getElementById('fResp-wa').value = '5512345678';
  opened259.length = 0;
  document.getElementById('btnRespEnviar')._h.click[0]();
  var wa263f = opened259.length === 1 && opened259[0].indexOf('https://wa.me/525512345678?text=') === 0 ? decodeURIComponent(opened259[0].split('text=')[1]) : '';
  var f263enviar = opened259.length === 1 && wa263f.indexOf('Responsiva — Checklist de Soporte') !== -1 && wa263f.indexOf('Nombre Completo: Juan Pérez López') !== -1;
  document.getElementById('fResp-nombre').value = 'Juan Pérez López';
  document.getElementById('fResp-colaborador').value = '98765';
  document.getElementById('fResp-sucursal').value = 'Polanco';
  document.getElementById('fResp-puesto').value = 'Técnico';
  document.getElementById('fResp-jefe').value = 'María García';
  document.getElementById('fResp-area').value = 'Sistemas';
  document.getElementById('btnRespGuardar')._h.click[0]();
  var borr263f = null;
  try { borr263f = JSON.parse(global.localStorage.getItem('checklist-soporte-resp-borrador-v1') || 'null'); } catch (e) { borr263f = null; }
  var f263guardar = !!borr263f && borr263f['fResp-nombre'] === 'Juan Pérez López' && toastTxt().indexOf('Responsiva guardada') !== -1;
  CLOUD_ENABLED = false;
  console.log('263F) formulario directo: Enviar por WhatsApp sigue igual:', f263enviar, '| Guardar y cerrar sigue igual:', f263guardar);
"""
rep("  process.exit(0);\n})();\n", serie263 + "\n  process.exit(0);\n})();\n")

open(P, 'w', encoding='utf-8').write(s)
print('test20263.js generado')
