# Parche de pruebas 2.5.14: test20263.js -> test20264.js.
# 1) Extrae el <script> actual de www/index.html a
# tests/checklist20264.js (el JavaScript de esta version, que evalua el
# harness). 2) Copia test20263.js a test20264.js y actualiza la version
# (2.5.13 -> 2.5.14, mailto 263 -> 264) y la asercion 263C del mensaje
# de WhatsApp en blanco (ahora lleva el texto de invitacion). 3)
# Agrega la serie 264: texto «Por favor llena tus datos para crear tu
# responsiva» en la vista, en el mensaje de WhatsApp del enlace en
# blanco y en responsiva.html (servida en local por HTTP);
# archivarResponsiva en firebase.js; boton Archivar con confirmacion
# (si dice que no, no archiva); archivar quita la tarjeta de la lista
# principal y la pone en archivadas; toggle «Ver responsivas
# anteriores» muestra/oculta la seccion; restaurar la devuelve;
# sin archivadas el mensaje vacio; sin nube archivar avisa y no
# llama; el formulario directo y la suscripcion siguen intactos.
# Uso: python3 patch_test_20264.py (corre desde tests/)
import os
import shutil

BASE = '/home/hatch/workspace/android/checklist-cloud'
TESTS = os.path.join(BASE, 'tests')
SRC = os.path.join(TESTS, 'test20263.js')
P = os.path.join(TESTS, 'test20264.js')

# --- Extraer el <script> actual de www/index.html.
html = open(os.path.join(BASE, 'www/index.html'), encoding='utf-8').read()
i = html.index('<script>', html.index('firebase-config'))
j = html.index('</script>', i)
open(os.path.join(TESTS, 'checklist20264.js'), 'w', encoding='utf-8').write(html[i + len('<script>'):j])
print('checklist20264.js extraido:', j - i - len('<script>'), 'bytes')

shutil.copyfile(SRC, P)
s = open(P, encoding='utf-8').read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'NO ENCONTRADO x%d (esperado %d): %r' % (c, n, old[:120])
    s = s.replace(old, new)


# --- SRC y version 2.5.14 (orden: primero 2.5.13 -> 2.5.14, luego 2.5.12 -> 2.5.13).
rep("const SRC = fs.readFileSync(__dirname + '/checklist20263.js', 'utf8');",
    "const SRC = fs.readFileSync(__dirname + '/checklist20264.js', 'utf8');")
rep("html.includes('Versión 2.5.13')", "html.includes('Versión 2.5.14')", n=5)
rep("html.includes('Versión: 2.5.13')", "html.includes('Versión: 2.5.14')", n=2)
rep("html.includes('Versión 2.5.12')", "html.includes('Versión 2.5.13')", n=2)
rep("!html.includes('2.5.12')", "!html.includes('2.5.13')", n=4)
BS = chr(92)
rep("(html.match(/2" + BS + ".5" + BS + ".13/g) || []).length",
    "(html.match(/2" + BS + ".5" + BS + ".14/g) || []).length")
rep("var n263 = ", "var n264 = ")
rep("n263 === 2", "n264 === 2", n=2)
rep("'AM0) versión 2.5.13:'", "'AM0) versión 2.5.14:'")
rep("'AP0) estáticos 2.5.13:", "'AP0) estáticos 2.5.14:")
rep("'AR0) versión 2.5.13 visible:'", "'AR0) versión 2.5.14 visible:'")
rep("'| 0 de 2.5.12:'", "'| 0 de 2.5.13:'", n=2)
rep("'| ocurrencias 2.5.13:'", "'| ocurrencias 2.5.14:'")
rep("'BA0) versión 2.5.13 sin 2.5.12:'", "'BA0) versión 2.5.14 sin 2.5.13:'")
rep("'BB0) 2.5.13 en 2 sitios:'", "'BB0) 2.5.14 en 2 sitios:'")
rep("html.indexOf('Soporte 263')", "html.indexOf('Soporte 264')", n=3)
rep("'| mailto 263:'", "'| mailto 264:'", n=3)

# --- 263C: el mensaje de WhatsApp en blanco ahora lleva el texto de
# invitación antes del enlace.
rep("txt263c.indexOf('llena tu responsiva') !== -1",
    "txt263c.indexOf('Por favor llena tus datos para crear tu responsiva') !== -1")

# --- Serie 264 nueva, antes de process.exit(0).
serie264 = """
  // 264: serie nueva — texto de invitación a llenar la responsiva,
  // botón Archivar y «Ver responsivas anteriores».
  // 264A: el texto exacto está en la vista (junto al botón de enviar
  // en blanco), en el código (mensaje de WhatsApp y render) y en
  // responsiva.html (encabezado, servida en local por HTTP); el
  // toggle y la sección de archivadas existen en el HTML; firebase.js
  // trae archivarResponsiva y la app la expone.
  var fb264 = fs.readFileSync('/home/hatch/workspace/android/checklist-cloud/www/cloud/firebase.js', 'utf8');
  var respHtml264 = fs.readFileSync('/home/hatch/workspace/android/checklist-cloud/hosting/public/responsiva.html', 'utf8');
  var a264html = html.indexOf('Por favor llena tus datos para crear tu responsiva') !== -1 &&
    html.indexOf('id="btnRespVerAnt"') !== -1 && html.indexOf('Ver responsivas anteriores') !== -1 &&
    html.indexOf('id="respArchBox"') !== -1 && html.indexOf('id="respArchList"') !== -1 &&
    html.indexOf('Responsivas archivadas') !== -1 &&
    html.includes('Versión 2.5.14') && !html.includes('2.5.13');
  var a264src = SRC.indexOf('function respCardHtml') !== -1 && SRC.indexOf('function respArchivar') !== -1 &&
    SRC.indexOf('function respListClick') !== -1 && SRC.indexOf('respMostrarArchivadas') !== -1 &&
    SRC.indexOf('data-resp-archivar') !== -1 && SRC.indexOf('data-resp-restaurar') !== -1 &&
    SRC.indexOf('No hay responsivas archivadas') !== -1 &&
    SRC.indexOf('¿Archivar esta responsiva? Podrás verla en Responsivas anteriores.') !== -1 &&
    SRC.indexOf('Por favor llena tus datos para crear tu responsiva: ') !== -1;
  var a264fb = fb264.indexOf('async function archivarResponsiva') !== -1 &&
    fb264.indexOf('archivado: true') !== -1 && fb264.indexOf('archivadoEn: Date.now()') !== -1 &&
    fb264.indexOf('archivado: false') !== -1 && fb264.indexOf('archivarResponsiva,') !== -1;
  var a264respFile = respHtml264.indexOf('Por favor llena tus datos para crear tu responsiva') !== -1 &&
    respHtml264.indexOf('Llena tus datos para la responsiva del equipo.') === -1;
  var http264 = require('http');
  var srv264 = http264.createServer(function (req, res) { res.writeHead(200, { 'Content-Type': 'text/html' }); res.end(respHtml264); });
  await new Promise(function (res2) { srv264.listen(0, '127.0.0.1', res2); });
  var port264 = srv264.address().port;
  var body264 = await new Promise(function (res2, rej) {
    http264.get({ host: '127.0.0.1', port: port264, path: '/responsiva.html' }, function (r) {
      var b = '';
      r.on('data', function (c) { b += c; });
      r.on('end', function () { res2({ status: r.statusCode, body: b }); });
    }).on('error', rej);
  });
  srv264.close();
  var a264served = body264.status === 200 && body264.body.indexOf('Por favor llena tus datos para crear tu responsiva') !== -1;
  console.log('264A) texto en vista + toggle y archivadas en HTML:', a264html, '| funciones y botones en la app:', a264src, '| archivarResponsiva en firebase.js:', a264fb, '| texto en responsiva.html:', a264respFile, '| servida en local (HTTP 200 con el texto):', a264served);
  // 264B: el mensaje de WhatsApp del enlace en blanco lleva el texto
  // de invitación ANTES del enlace.
  doLogin('usuario');
  var cloud264b = [];
  global.Cloud.crearResponsiva = async function (nombre) { cloud264b.push(nombre); return 'RESP-ABC264'; };
  CLOUD_ENABLED = true;
  opened259.length = 0;
  var ok264b = await respEnviarEnBlanco();
  var url264b = opened259.length === 1 ? opened259[0] : '';
  var txt264b = url264b.indexOf('https://wa.me/?text=') === 0 ? decodeURIComponent(url264b.split('text=')[1]) : '';
  var b264 = ok264b === true && cloud264b.length === 1 && opened259.length === 1 &&
    txt264b.indexOf('Por favor llena tus datos para crear tu responsiva: https://checklist-soporte.web.app/responsiva.html?id=RESP-ABC264') === 0 &&
    txt264b.indexOf('Hola, llena tu responsiva') === -1;
  CLOUD_ENABLED = false;
  console.log('264B) WhatsApp en blanco: texto de invitación antes del enlace:', b264);
  // 264C: la lista principal muestra solo las activas (con Archivar);
  // la archivada no está ahí; el toggle muestra la sección con la
  // archivada (datos, estado, fecha de archivado y Restaurar).
  var cb264 = null;
  global.Cloud.subscribeResponsivas = function (cb, uid) { cb264 = cb; return function () {}; };
  global.Cloud.archivarResponsiva = async function (id, arch) { (global.__arch264 = global.__arch264 || []).push([id, arch]); return true; };
  global.__arch264 = [];
  cloudRespUnsub = null;
  CLOUD_ENABLED = true;
  showVista('resp');
  var r264pend = { id: 'R1', creadoPor: 'u1', creadoPorNombre: 'Test User', creadoEn: Date.now() - 60000, estado: 'pendiente', datos: null };
  var r264llen = { id: 'R2', creadoPor: 'u1', creadoPorNombre: 'Test User', creadoEn: Date.now(), estado: 'llenada', llenadoEn: Date.now(),
    datos: { nombre: 'Juan Pérez López', colaborador: '98765', sucursal: 'Polanco', puesto: 'Técnico', jefe: 'María García', area: 'Sistemas' } };
  var r264arch = { id: 'R3', creadoPor: 'u1', creadoPorNombre: 'Test User', creadoEn: Date.now() - 120000, estado: 'llenada', llenadoEn: Date.now() - 120000,
    archivado: true, archivadoEn: Date.now() - 10000,
    datos: { nombre: 'Ana Ruiz', colaborador: '11111', sucursal: 'Roma Norte', puesto: 'Analista', jefe: 'Luis Torres', area: 'Ventas' } };
  cb264([r264pend, r264llen, r264arch]);
  var list264 = document.getElementById('respList').innerHTML;
  var c264main = list264.indexOf('data-resp-archivar="R1"') !== -1 && list264.indexOf('data-resp-archivar="R2"') !== -1 &&
    list264.indexOf('R3') === -1 && list264.indexOf('Ana Ruiz') === -1 &&
    list264.indexOf('Juan Pérez López') !== -1 && list264.indexOf('Pendiente') !== -1 &&
    document.getElementById('respArchBox').hidden === true && document.getElementById('respArchList').innerHTML === '';
  document.getElementById('btnRespVerAnt')._h.click[0]();
  var arch264 = document.getElementById('respArchList').innerHTML;
  var c264arch = document.getElementById('respArchBox').hidden === false &&
    arch264.indexOf('Ana Ruiz') !== -1 && arch264.indexOf('Llenada') !== -1 && arch264.indexOf('Archivada') !== -1 &&
    arch264.indexOf('Número de colaborador: 11111') !== -1 && arch264.indexOf('data-resp-restaurar="R3"') !== -1 &&
    arch264.indexOf('data-resp-wa="R3"') !== -1 && arch264.indexOf('data-resp-xlsx="R3"') !== -1 &&
    document.getElementById('respList').innerHTML.indexOf('R3') === -1;
  console.log('264C) lista principal solo activas con Archivar:', c264main, '| toggle muestra archivada con datos y Restaurar:', c264arch);
  // 264D: Archivar pide confirmación: si dice que no, no archiva; si
  // dice que sí, llama a Cloud y al llegar por suscripción la tarjeta
  // sale de la principal y entra en archivadas.
  function clickResp264(attr, id, listId) {
    var t = { classList: { contains() { return false; } },
      closest(sel) { return sel === '[' + attr + ']' ? { getAttribute(a) { return id; } } : null; },
      hasAttribute(a) { return a === attr; },
      getAttribute(a) { return id; } };
    els[listId || 'respList']._h.click[0]({ target: t });
  }
  global.__arch264 = [];
  clickResp264('data-resp-archivar', 'R2');
  await sleep(10);
  var msg264d = document.getElementById('confirmMsg').textContent || '';
  var d264preg = msg264d.indexOf('¿Archivar esta responsiva? Podrás verla en Responsivas anteriores.') !== -1;
  answerConfirm(false);
  await sleep(10);
  var d264no = global.__arch264.length === 0;
  clickResp264('data-resp-archivar', 'R2');
  await sleep(10);
  answerConfirm(true);
  await sleep(50);
  var d264si = global.__arch264.length === 1 && global.__arch264[0][0] === 'R2' && global.__arch264[0][1] === true &&
    toastTxt().indexOf('Responsiva archivada.') !== -1;
  var r264llenArch = Object.assign({}, r264llen, { archivado: true, archivadoEn: Date.now() });
  cb264([r264pend, r264llenArch, r264arch]);
  var list264d = document.getElementById('respList').innerHTML;
  var arch264d = document.getElementById('respArchList').innerHTML;
  var d264mueve = list264d.indexOf('R2') === -1 && list264d.indexOf('Juan Pérez López') === -1 &&
    list264d.indexOf('data-resp-archivar="R1"') !== -1 &&
    arch264d.indexOf('Juan Pérez López') !== -1 && arch264d.indexOf('data-resp-restaurar="R2"') !== -1 &&
    arch264d.indexOf('Archivada') !== -1;
  console.log('264D) confirmación pedida:', d264preg, '| No no archiva:', d264no, '| Sí archiva y avisa:', d264si, '| sale de principal y entra en archivadas:', d264mueve);
  // 264E: Restaurar desde archivadas vuelve la tarjeta a la lista
  // principal (sin confirmación) y sale de archivadas.
  global.__arch264 = [];
  clickResp264('data-resp-restaurar', 'R2', 'respArchList');
  await sleep(50);
  var e264llama = global.__arch264.length === 1 && global.__arch264[0][0] === 'R2' && global.__arch264[0][1] === false &&
    toastTxt().indexOf('Responsiva restaurada.') !== -1;
  cb264([r264pend, r264llen, r264arch]);
  var list264e = document.getElementById('respList').innerHTML;
  var arch264e = document.getElementById('respArchList').innerHTML;
  var e264vuelve = list264e.indexOf('Juan Pérez López') !== -1 && list264e.indexOf('data-resp-archivar="R2"') !== -1 &&
    arch264e.indexOf('Juan Pérez López') === -1 && arch264e.indexOf('Ana Ruiz') !== -1;
  console.log('264E) restaurar llama con false y avisa:', e264llama, '| vuelve a principal y sale de archivadas:', e264vuelve);
  // 264F: el toggle oculta la sección; sin archivadas muestra el
  // mensaje vacío; con la lista vacía la principal también avisa.
  document.getElementById('btnRespVerAnt')._h.click[0]();
  var f264off = document.getElementById('respArchBox').hidden === true && document.getElementById('respArchList').innerHTML === '';
  cb264([r264pend, r264llen]);
  document.getElementById('btnRespVerAnt')._h.click[0]();
  var f264vacio = document.getElementById('respArchBox').hidden === false &&
    document.getElementById('respArchList').innerHTML.indexOf('No hay responsivas archivadas') !== -1;
  cb264([]);
  var f264nada = document.getElementById('respList').innerHTML.indexOf('Aún no hay responsivas enviadas.') !== -1 &&
    document.getElementById('respArchList').innerHTML.indexOf('No hay responsivas archivadas') !== -1;
  console.log('264F) toggle oculta la sección:', f264off, '| sin archivadas el mensaje vacío:', f264vacio, '| lista vacía: principal y archivadas avisan:', f264nada);
  // 264G: sin nube archivar avisa y no llama; el formulario directo
  // del técnico y la suscripción siguen intactos.
  CLOUD_ENABLED = false;
  global.__arch264 = [];
  var g264sin = await respArchivar('R1', true);
  var g264avisa = g264sin === false && global.__arch264.length === 0 && toastTxt().indexOf('Archivar necesita conexión a la nube.') !== -1;
  document.getElementById('fResp-nombre').value = 'Juan Pérez López';
  document.getElementById('fResp-colaborador').value = '98765';
  document.getElementById('fResp-sucursal').value = 'Polanco';
  document.getElementById('fResp-puesto').value = 'Técnico';
  document.getElementById('fResp-jefe').value = 'María García';
  document.getElementById('fResp-area').value = 'Sistemas';
  document.getElementById('fResp-wa').value = '5512345678';
  opened259.length = 0;
  document.getElementById('btnRespEnviar')._h.click[0]();
  var wa264g = opened259.length === 1 && opened259[0].indexOf('https://wa.me/525512345678?text=') === 0 ? decodeURIComponent(opened259[0].split('text=')[1]) : '';
  var g264directo = opened259.length === 1 && wa264g.indexOf('Responsiva — Checklist de Soporte') !== -1 && wa264g.indexOf('Nombre Completo: Juan Pérez López') !== -1;
  var g264fb = fb264.indexOf('async function crearResponsiva') !== -1 && fb264.indexOf('function subscribeResponsivas') !== -1;
  CLOUD_ENABLED = false;
  console.log('264G) sin nube archivar avisa y no llama:', g264avisa, '| formulario directo sigue igual:', g264directo, '| crear + subscribe intactos:', g264fb);
"""
rep("  process.exit(0);\n})();\n", serie264 + "\n  process.exit(0);\n})();\n")

open(P, 'w', encoding='utf-8').write(s)
print('test20264.js generado')
