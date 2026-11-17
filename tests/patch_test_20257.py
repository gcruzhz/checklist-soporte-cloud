# Parche de pruebas 2.5.7: test20256.js -> test20257.js (ya copiado).
P = '/home/hatch/workspace/android/checklist-cloud/tests/test20257.js'
s = open(P, encoding='utf-8').read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'NO ENCONTRADO x%d (esperado %d): %r' % (c, n, old[:120])
    s = s.replace(old, new)

# --- SRC y versión 2.5.7 (orden: primero 2.5.6 -> 2.5.7, luego 2.5.5 -> 2.5.6).
rep("const SRC = fs.readFileSync(__dirname + '/checklist20256.js', 'utf8');",
    "const SRC = fs.readFileSync(__dirname + '/checklist20257.js', 'utf8');")
rep("html.includes('Versión 2.5.6')", "html.includes('Versión 2.5.7')", n=4)
rep("html.includes('Versión: 2.5.6')", "html.includes('Versión: 2.5.7')", n=2)
rep("html.includes('Versión 2.5.5')", "html.includes('Versión 2.5.6')", n=2)
rep("!html.includes('2.5.5')", "!html.includes('2.5.6')", n=3)
rep("(html.match(/2\\.5\\.6/g) || []).length", "(html.match(/2\\.5\\.7/g) || []).length")
rep("var n256 = ", "var n257 = ")
rep("n256 === 2", "n257 === 2", n=2)
rep("'AM0) versión 2.5.6:'", "'AM0) versión 2.5.7:'")
rep("'AP0) estáticos 2.5.6:", "'AP0) estáticos 2.5.7:")
rep("'AR0) versión 2.5.6 visible:'", "'AR0) versión 2.5.7 visible:'")
rep("'| 0 de 2.5.5:'", "'| 0 de 2.5.6:'", n=2)
rep("'| ocurrencias 2.5.6:'", "'| ocurrencias 2.5.7:'")
rep("'BA0) versión 2.5.6 sin 2.5.5:'", "'BA0) versión 2.5.7 sin 2.5.6:'")
rep("'BB0) 2.5.6 en 2 sitios:'", "'BB0) 2.5.7 en 2 sitios:'")

# --- Serie 257 nueva, antes de process.exit(0).
serie257 = """
  // 257: serie nueva — contraseña del usuario sistemas (solo escritorio).
  // 257A: botón oculto sin Desktop, visible con Desktop; el panel abre y
  // cierra los demás paneles; campos de contraseña y usuario por defecto.
  global.Desktop = undefined;
  refreshDetectarBtn();
  var a257oculto = document.getElementById('btnPassSistemas').hidden === true;
  var a257panelOculto = document.getElementById('passBox').hidden === true;
  var a257html = html.indexOf('id="btnPassSistemas"') !== -1 && html.indexOf('id="passBox"') !== -1 && html.indexOf('id="fPsUser"') !== -1 && html.indexOf('id="fPsActual"') !== -1 && html.indexOf('id="fPsNueva"') !== -1 && html.indexOf('id="fPsConfirm"') !== -1 && html.indexOf('id="btnPsVerificar"') !== -1 && html.indexOf('id="btnPsCambiar"') !== -1;
  var a257pass = (html.match(/type="password"/g) || []).length >= 3 && html.indexOf('value="sistemas"') !== -1;
  global.Desktop = { verificarPasswordSistemas: async function () { return { ok: true }; }, cambiarPasswordSistemas: async function () { return { ok: true }; } };
  render();
  var a257visible = document.getElementById('btnPassSistemas').hidden === false;
  document.getElementById('passBox').scrollIntoView = function () {};
  document.getElementById('detBox').scrollIntoView = function () {};
  document.getElementById('btnPassSistemas')._h.click[0]();
  var a257abre = document.getElementById('passBox').hidden === false && document.getElementById('detBox').hidden === true;
  document.getElementById('btnPassSistemas')._h.click[0]();
  var a257cierra = document.getElementById('passBox').hidden === true;
  console.log('257A) sin Desktop oculto:', a257oculto, '| panel oculto al inicio:', a257panelOculto, '| HTML con botón+panel+campos:', a257html, '| 3+ campos password y usuario sistemas:', a257pass, '| con Desktop visible:', a257visible, '| clic abre el panel y cierra detBox:', a257abre, '| segundo clic lo cierra:', a257cierra);
  // 257B: Verificar con Desktop simulado: correcta, incorrecta, sin actual.
  var llamadas257 = [];
  global.Desktop = {
    verificarPasswordSistemas: async function (u, a) { llamadas257.push(['ver', u, a]); return { ok: true }; },
    cambiarPasswordSistemas: async function (u, a, n) { llamadas257.push(['cam', u, a, n]); return { ok: true }; }
  };
  document.getElementById('fPsUser').value = 'sistemas';
  document.getElementById('fPsActual').value = 'ContraseñaVieja123';
  document.getElementById('toast').textContent = '';
  document.getElementById('btnPsVerificar')._h.click[0]();
  await sleep(20);
  var b257ok = toastTxt() === 'Contraseña actual correcta ✓' && llamadas257.length === 1 && llamadas257[0][0] === 'ver' && llamadas257[0][1] === 'sistemas' && llamadas257[0][2] === 'ContraseñaVieja123';
  var b257limpio = document.getElementById('fPsActual').value === '';
  global.Desktop.verificarPasswordSistemas = async function (u, a) { llamadas257.push(['ver', u, a]); return { ok: false, error: 'Contraseña actual incorrecta.' }; };
  document.getElementById('fPsActual').value = 'ContraseñaMala123';
  document.getElementById('toast').textContent = '';
  document.getElementById('btnPsVerificar')._h.click[0]();
  await sleep(20);
  var b257mal = toastTxt() === 'Contraseña actual incorrecta.' && llamadas257.length === 2;
  document.getElementById('fPsActual').value = '';
  document.getElementById('toast').textContent = '';
  document.getElementById('btnPsVerificar')._h.click[0]();
  await sleep(20);
  var b257vacio = toastTxt() === 'Escribe la contraseña actual.' && llamadas257.length === 2;
  console.log('257B) verificar correcta avisa y llama con usuario+actual:', b257ok, '| campos limpios después:', b257limpio, '| verificar incorrecta avisa:', b257mal, '| sin actual no llama y avisa:', b257vacio);
  // 257C: Cambiar: validación local (vacía / no coinciden) sin tocar
  // Windows; con confirmación correcta llama y avisa; error del admin.
  document.getElementById('fPsActual').value = 'ContraseñaVieja123';
  document.getElementById('fPsNueva').value = '';
  document.getElementById('fPsConfirm').value = '';
  document.getElementById('toast').textContent = '';
  document.getElementById('btnPsCambiar')._h.click[0]();
  await sleep(20);
  var c257vacia = toastTxt() === 'Escribe la contraseña nueva.' && llamadas257.length === 2;
  document.getElementById('fPsNueva').value = 'NuevaPass123';
  document.getElementById('fPsConfirm').value = 'OtraPass123';
  document.getElementById('toast').textContent = '';
  document.getElementById('btnPsCambiar')._h.click[0]();
  await sleep(20);
  var c257noCoin = toastTxt() === 'La contraseña nueva y su confirmación no coinciden.' && llamadas257.length === 2;
  document.getElementById('fPsNueva').value = 'NuevaPass123';
  document.getElementById('fPsConfirm').value = 'NuevaPass123';
  document.getElementById('toast').textContent = '';
  document.getElementById('btnPsCambiar')._h.click[0]();
  await sleep(20);
  var c257ok = toastTxt() === 'Contraseña cambiada ✓' && llamadas257.length === 3 && llamadas257[2][0] === 'cam' && llamadas257[2][3] === 'NuevaPass123';
  var c257limpio = document.getElementById('fPsActual').value === '' && document.getElementById('fPsNueva').value === '' && document.getElementById('fPsConfirm').value === '';
  global.Desktop.cambiarPasswordSistemas = async function (u, a, n) { llamadas257.push(['cam', u, a, n]); return { ok: false, error: 'Se necesita permiso de administrador para cambiar la contraseña.' }; };
  document.getElementById('fPsActual').value = 'ContraseñaVieja123';
  document.getElementById('fPsNueva').value = 'NuevaPass123';
  document.getElementById('fPsConfirm').value = 'NuevaPass123';
  document.getElementById('toast').textContent = '';
  document.getElementById('btnPsCambiar')._h.click[0]();
  await sleep(20);
  var c257admin = toastTxt() === 'Se necesita permiso de administrador para cambiar la contraseña.' && llamadas257.length === 4;
  console.log('257C) nueva vacía no llama y avisa:', c257vacia, '| no coinciden no llama y avisa:', c257noCoin, '| coinciden llama y avisa cambiada:', c257ok, '| campos limpios después:', c257limpio, '| error de admin avisa:', c257admin);
  // 257D: sin Desktop los botones avisan y no llaman; nada con
  // contraseñas se guarda en localStorage ni se manda a la nube.
  global.Desktop = undefined;
  var nLlam257 = llamadas257.length;
  document.getElementById('fPsActual').value = 'ContraseñaVieja123';
  document.getElementById('fPsNueva').value = 'NuevaPass123';
  document.getElementById('fPsConfirm').value = 'NuevaPass123';
  document.getElementById('toast').textContent = '';
  document.getElementById('btnPsVerificar')._h.click[0]();
  await sleep(20);
  var d257ver = toastTxt() === 'La verificación solo funciona en la app de escritorio.' && llamadas257.length === nLlam257;
  document.getElementById('toast').textContent = '';
  document.getElementById('btnPsCambiar')._h.click[0]();
  await sleep(20);
  var d257cam = toastTxt() === 'El cambio de contraseña solo funciona en la app de escritorio.' && llamadas257.length === nLlam257;
  var ls257 = JSON.stringify(global.localStorage._d);
  var d257noguarda = ls257.indexOf('ContraseñaVieja123') === -1 && ls257.indexOf('NuevaPass123') === -1 && ls257.indexOf('ContraseñaMala123') === -1 && ls257.indexOf('OtraPass123') === -1;
  var d257mailto = html.indexOf('Soporte 257') !== -1;
  console.log('257D) sin Desktop verificar avisa sin llamar:', d257ver, '| cambiar avisa sin llamar:', d257cam, '| nada guardado en localStorage:', d257noguarda, '| mailto 257:', d257mailto);
"""
rep("  process.exit(0);", serie257 + "\n  process.exit(0);")

open(P, 'w', encoding='utf-8').write(s)
print('OK test20257.js, bytes:', len(s))
print('2.5.7 en tests:', s.count('2.5.7'), '| 2.5.6 restante:', s.count('2.5.6'), '| 2.5.5 restante:', s.count('2.5.5'))
