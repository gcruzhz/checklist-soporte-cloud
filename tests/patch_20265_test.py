# Parche de pruebas 2.5.15: test20264.js -> test20265.js.
# 1) Extrae el <script> actual de www/index.html a
# tests/checklist20265.js (el JavaScript de esta version, que evalua el
# harness). 2) Copia test20264.js a test20265.js y actualiza la version
# (2.5.14 -> 2.5.15, 2.5.13 -> 2.5.14, mailto 264 -> 265, n264 ->
# n265). 3) Actualiza 263C y 264B al comportamiento nuevo de
# respEnviarEnBlanco (2.5.15): 263C ahora pone el número en el campo y
# espera wa.me/525512345678; 264B pone el campo vacío y espera el
# chooser con el toast nuevo. 4) Agrega la serie 265: enviar en blanco
# al número del campo (con 52, inválido, con formato, y el envío
# directo sigue igual); el bundle de Firebase NO cambia (md5
# f9c4918d…).
# Uso: python3 patch_20265_test.py (corre desde tests/)
import os
import shutil

BASE = '/home/hatch/workspace/android/checklist-cloud'
TESTS = os.path.join(BASE, 'tests')
SRC = os.path.join(TESTS, 'test20264.js')
P = os.path.join(TESTS, 'test20265.js')

# --- Extraer el <script> actual de www/index.html.
html = open(os.path.join(BASE, 'www/index.html'), encoding='utf-8').read()
i = html.index('<script>', html.index('firebase-config'))
j = html.index('</script>', i)
open(os.path.join(TESTS, 'checklist20265.js'), 'w', encoding='utf-8').write(html[i + len('<script>'):j])
print('checklist20265.js extraido:', j - i - len('<script>'), 'bytes')

shutil.copyfile(SRC, P)
s = open(P, encoding='utf-8').read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'NO ENCONTRADO x%d (esperado %d): %r' % (c, n, old[:120])
    s = s.replace(old, new)


def repall(old, new, n):
    global s
    c = s.count(old)
    assert c == n, 'NO ENCONTRADO x%d (esperado %d): %r' % (c, n, old[:120])
    s = s.replace(old, new)


# --- SRC y version 2.5.15 (orden: primero 2.5.14 -> 2.5.15, luego
# 2.5.13 -> 2.5.14 para las referencias a la version anterior).
rep("const SRC = fs.readFileSync(__dirname + '/checklist20264.js', 'utf8');",
    "const SRC = fs.readFileSync(__dirname + '/checklist20265.js', 'utf8');")
repall("2.5.14", "2.5.15", 14)
repall("2.5.13", "2.5.14", 10)
repall("n264", "n265", 3)
repall("Soporte 264", "Soporte 265", 3)
repall("mailto 264", "mailto 265", 3)
# El regex lleva la versión con barras escapadas: el reemplazo plano
# de "2.5.14" no lo toca, hay que actualizarlo aparte.
BS = chr(92)
rep("var n265 = (html.match(/2" + BS + ".5" + BS + ".14/g) || []).length;",
    "var n265 = (html.match(/2" + BS + ".5" + BS + ".15/g) || []).length;")

# --- 263C: con el número en el campo, el envío en blanco ahora abre
# wa.me/525512345678?text= con la invitación y el enlace (2.5.15).
rep("""  // 263C: con Cloud simulado crea la responsiva (con el nombre del
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
    txt263c.indexOf('Por favor llena tus datos para crear tu responsiva') !== -1 && toastTxt().indexOf('Responsiva creada') !== -1;
  CLOUD_ENABLED = false;
  console.log('263C) crea con el nombre del tecnico y abre wa.me con el enlace:', c263);""",
"""  // 263C: con Cloud simulado crea la responsiva (con el nombre del
  // tecnico) y, con el número del campo #fResp-wa, abre
  // wa.me/525512345678?text= con la invitación y el enlace
  // responsiva.html?id=... (2.5.15: al número configurado).
  doLogin('usuario');
  var cloud263 = [];
  global.Cloud.crearResponsiva = async function (nombre) { cloud263.push(nombre); return 'RESP-ABC123'; };
  CLOUD_ENABLED = true;
  opened259.length = 0;
  document.getElementById('fResp-wa').value = '5512345678';
  var ok263c = await respEnviarEnBlanco();
  var url263c = opened259.length === 1 ? opened259[0] : '';
  var txt263c = url263c.indexOf('https://wa.me/525512345678?text=') === 0 ? decodeURIComponent(url263c.split('text=')[1]) : '';
  var c263 = ok263c === true && cloud263.length === 1 && cloud263[0] === 'Test User' &&
    opened259.length === 1 && url263c.indexOf('https://wa.me/525512345678?text=') === 0 &&
    txt263c.indexOf('Por favor llena tus datos para crear tu responsiva: https://checklist-soporte.web.app/responsiva.html?id=RESP-ABC123') === 0 &&
    toastTxt().indexOf('Responsiva creada, enviada al número de WhatsApp.') !== -1;
  CLOUD_ENABLED = false;
  console.log('263C) crea con el nombre del tecnico y abre wa.me al número configurado:', c263);""")

# --- 264B: sin número en el campo, el envío en blanco cae al chooser
# wa.me/?text= con el toast nuevo (2.5.15).
rep("""  // 264B: el mensaje de WhatsApp del enlace en blanco lleva el texto
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
  console.log('264B) WhatsApp en blanco: texto de invitación antes del enlace:', b264);""",
"""  // 264B: el mensaje de WhatsApp del enlace en blanco lleva el texto
  // de invitación ANTES del enlace. Sin número en el campo, cae al
  // chooser wa.me/?text= con el toast que lo dice (2.5.15).
  doLogin('usuario');
  var cloud264b = [];
  global.Cloud.crearResponsiva = async function (nombre) { cloud264b.push(nombre); return 'RESP-ABC264'; };
  CLOUD_ENABLED = true;
  opened259.length = 0;
  document.getElementById('fResp-wa').value = '';
  var ok264b = await respEnviarEnBlanco();
  var url264b = opened259.length === 1 ? opened259[0] : '';
  var txt264b = url264b.indexOf('https://wa.me/?text=') === 0 ? decodeURIComponent(url264b.split('text=')[1]) : '';
  var b264 = ok264b === true && cloud264b.length === 1 && opened259.length === 1 &&
    txt264b.indexOf('Por favor llena tus datos para crear tu responsiva: https://checklist-soporte.web.app/responsiva.html?id=RESP-ABC264') === 0 &&
    txt264b.indexOf('Hola, llena tu responsiva') === -1 &&
    toastTxt().indexOf('No hay número de WhatsApp configurado, elige el contacto.') !== -1;
  CLOUD_ENABLED = false;
  console.log('264B) WhatsApp en blanco sin número: chooser con el texto de invitación:', b264);""")

# --- Serie 265 nueva, antes de process.exit(0).
serie265 = """
  // 265: serie nueva — «Enviar formulario en blanco» al número de
  // WhatsApp del campo #fResp-wa (2.5.15): con número válido abre
  // wa.me/<número>?text= con la invitación y el enlace; sin número o
  // inválido cae al chooser wa.me/?text= con el toast que lo dice.
  // 265A: versión 2.5.15 en los 2 sitios, mailto 265, el bundle de
  // Firebase NO cambia (mismo md5 f9c4918d… que en 2.5.14) y el código
  // trae la lógica nueva.
  var crypto265 = require('crypto');
  var bundle265 = fs.readFileSync('/home/hatch/workspace/android/checklist-cloud/www/cloud/firebase.bundle.js');
  var md5bundle265 = crypto265.createHash('md5').update(bundle265).digest('hex');
  var fb265 = fs.readFileSync('/home/hatch/workspace/android/checklist-cloud/www/cloud/firebase.js', 'utf8');
  var a265ver = html.includes('Versión 2.5.15') && html.includes('Versión: 2.5.15') && !html.includes('2.5.14');
  var a265bundle = md5bundle265 === 'f9c4918d91bfbf4057433c43c54d708a';
  var a265src = SRC.indexOf('No hay número de WhatsApp configurado, elige el contacto.') !== -1 &&
    SRC.indexOf("window.open('https://wa.me/' + num + '?text=' + encodeURIComponent(texto), '_blank');") !== -1 &&
    SRC.indexOf('Responsiva creada, enviada al número de WhatsApp.') !== -1 &&
    fb265.indexOf('async function crearResponsiva') !== -1 && fb265.indexOf('function subscribeResponsivas') !== -1;
  console.log('265A) versión 2.5.15:', a265ver, '| bundle sin cambio (f9c4918d…):', a265bundle, '| lógica nueva en la app:', a265src);
  // 265B: número ya con 52 en el campo: se respeta y abre
  // wa.me/525512345678?text= con la invitación y el enlace.
  doLogin('usuario');
  var cloud265b = [];
  global.Cloud.crearResponsiva = async function (nombre) { cloud265b.push(nombre); return 'RESP-ABC265'; };
  CLOUD_ENABLED = true;
  opened259.length = 0;
  document.getElementById('fResp-wa').value = '525512345678';
  var ok265b = await respEnviarEnBlanco();
  var url265b = opened259.length === 1 ? opened259[0] : '';
  var txt265b = url265b.indexOf('https://wa.me/525512345678?text=') === 0 ? decodeURIComponent(url265b.split('text=')[1]) : '';
  var b265 = ok265b === true && cloud265b.length === 1 && opened259.length === 1 &&
    url265b.indexOf('https://wa.me/525512345678?text=') === 0 &&
    txt265b.indexOf('Por favor llena tus datos para crear tu responsiva: https://checklist-soporte.web.app/responsiva.html?id=RESP-ABC265') === 0 &&
    toastTxt().indexOf('Responsiva creada, enviada al número de WhatsApp.') !== -1;
  CLOUD_ENABLED = false;
  console.log('265B) número con 52: abre wa.me/525512345678 con invitación y enlace:', b265);
  // 265C: número inválido (menos de 10 dígitos) en el campo: cae al
  // chooser con el toast.
  CLOUD_ENABLED = true;
  opened259.length = 0;
  document.getElementById('fResp-wa').value = '551234';
  var ok265c = await respEnviarEnBlanco();
  var url265c = opened259.length === 1 ? opened259[0] : '';
  var txt265c = url265c.indexOf('https://wa.me/?text=') === 0 ? decodeURIComponent(url265c.split('text=')[1]) : '';
  var c265 = ok265c === true && opened259.length === 1 && url265c.indexOf('https://wa.me/?text=') === 0 &&
    txt265c.indexOf('Por favor llena tus datos para crear tu responsiva: https://checklist-soporte.web.app/responsiva.html?id=RESP-ABC265') === 0 &&
    toastTxt().indexOf('No hay número de WhatsApp configurado, elige el contacto.') !== -1;
  CLOUD_ENABLED = false;
  console.log('265C) número inválido: chooser con el toast:', c265);
  // 265D: número con espacios y guiones: se normaliza a 10 dígitos y
  // abre wa.me/525512345678.
  CLOUD_ENABLED = true;
  opened259.length = 0;
  document.getElementById('fResp-wa').value = '55 1234-5678';
  var ok265d = await respEnviarEnBlanco();
  var url265d = opened259.length === 1 ? opened259[0] : '';
  var txt265d = url265d.indexOf('https://wa.me/525512345678?text=') === 0 ? decodeURIComponent(url265d.split('text=')[1]) : '';
  var d265 = ok265d === true && opened259.length === 1 && url265d.indexOf('https://wa.me/525512345678?text=') === 0 &&
    txt265d.indexOf('https://checklist-soporte.web.app/responsiva.html?id=RESP-ABC265') !== -1 &&
    toastTxt().indexOf('Responsiva creada, enviada al número de WhatsApp.') !== -1;
  CLOUD_ENABLED = false;
  console.log('265D) número con espacios y guiones: se normaliza y abre wa.me/525512345678:', d265);
  // 265E: el envío directo del técnico sigue usando el número del
  // campo como antes (wa.me/525512345678 con los 6 datos).
  document.getElementById('fResp-nombre').value = 'Juan Pérez López';
  document.getElementById('fResp-colaborador').value = '98765';
  document.getElementById('fResp-sucursal').value = 'Polanco';
  document.getElementById('fResp-puesto').value = 'Técnico';
  document.getElementById('fResp-jefe').value = 'María García';
  document.getElementById('fResp-area').value = 'Sistemas';
  document.getElementById('fResp-wa').value = '5512345678';
  opened259.length = 0;
  document.getElementById('btnRespEnviar')._h.click[0]();
  var wa265e = opened259.length === 1 && opened259[0].indexOf('https://wa.me/525512345678?text=') === 0 ? decodeURIComponent(opened259[0].split('text=')[1]) : '';
  var e265 = opened259.length === 1 && wa265e.indexOf('Responsiva — Checklist de Soporte') !== -1 && wa265e.indexOf('Nombre Completo: Juan Pérez López') !== -1;
  console.log('265E) envío directo sigue igual (al número configurado):', e265);
"""
rep("  process.exit(0);\n})();\n", serie265 + "\n  process.exit(0);\n})();\n")

open(P, 'w', encoding='utf-8').write(s)
print('test20265.js generado')
