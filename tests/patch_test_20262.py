# Parche de pruebas 2.5.12: test20261.js -> test20262.js.
# 1) Copia test20261.js a test20262.js y actualiza la versión (2.5.11 ->
# 2.5.12, mailto 261 -> 262). 2) Ajusta la serie 261 al nuevo
# comportamiento: Enviar (261C) ya vacía los campos, así que 261D
# rellena el formulario antes de probar sin número y antes de probar el
# número corto; el comentario de 261E aclara que el formulario solo se
# guarda con Guardar y cerrar. 3) Agrega la serie 262: Guardar y cerrar
# guarda el borrador (incluso incompleto) y vuelve a Inicio sin tocar
# el número; al reabrir la vista el borrador se restaura; Enviar (con
# número o sin él) borra el borrador y vacía los campos; Enviar con
# validación fallida no borra el borrador; Limpiar borra el borrador.
# Uso: python3 patch_test_20262.py (corre desde tests/)
import shutil

SRC = '/home/hatch/workspace/android/checklist-cloud/tests/test20261.js'
P = '/home/hatch/workspace/android/checklist-cloud/tests/test20262.js'
shutil.copyfile(SRC, P)
s = open(P, encoding='utf-8').read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'NO ENCONTRADO x%d (esperado %d): %r' % (c, n, old[:120])
    s = s.replace(old, new)


# --- SRC y versión 2.5.12 (orden: primero 2.5.11 -> 2.5.12, luego 2.5.10 -> 2.5.11).
rep("const SRC = fs.readFileSync(__dirname + '/checklist20261.js', 'utf8');",
    "const SRC = fs.readFileSync(__dirname + '/checklist20262.js', 'utf8');")
rep("html.includes('Versión 2.5.11')", "html.includes('Versión 2.5.12')", n=4)
rep("html.includes('Versión: 2.5.11')", "html.includes('Versión: 2.5.12')", n=2)
rep("html.includes('Versión 2.5.10')", "html.includes('Versión 2.5.11')", n=2)
rep("!html.includes('2.5.10')", "!html.includes('2.5.11')", n=3)
rep("(html.match(/2\\.5\\.11/g) || []).length", "(html.match(/2\\.5\\.12/g) || []).length")
rep("var n261 = ", "var n262 = ")
rep("n261 === 2", "n262 === 2", n=2)
rep("'AM0) versión 2.5.11:'", "'AM0) versión 2.5.12:'")
rep("'AP0) estáticos 2.5.11:", "'AP0) estáticos 2.5.12:")
rep("'AR0) versión 2.5.11 visible:'", "'AR0) versión 2.5.12 visible:'")
rep("'| 0 de 2.5.10:'", "'| 0 de 2.5.11:'", n=2)
rep("'| ocurrencias 2.5.11:'", "'| ocurrencias 2.5.12:'")
rep("'BA0) versión 2.5.11 sin 2.5.10:'", "'BA0) versión 2.5.12 sin 2.5.11:'")
rep("'BB0) 2.5.11 en 2 sitios:'", "'BB0) 2.5.12 en 2 sitios:'")
rep("html.indexOf('Soporte 261')", "html.indexOf('Soporte 262')", n=3)
rep("'| mailto 258:'", "'| mailto 262:'", n=2)
rep("'| mailto 260:'", "'| mailto 262:'")

# --- 261D: Enviar (261C) ya vació los campos en 2.5.12: rellenarlos
# antes de probar sin número y antes de probar el número corto.
relleno261 = """  document.getElementById('fResp-nombre').value = 'Juan Pérez López';
  document.getElementById('fResp-colaborador').value = '98765';
  document.getElementById('fResp-sucursal').value = 'Polanco';
  document.getElementById('fResp-puesto').value = 'Técnico';
  document.getElementById('fResp-jefe').value = 'María García';
  document.getElementById('fResp-area').value = 'Sistemas';
"""
rep("""  // 261D: sin número configurado abre wa.me/?text= para elegir contacto
  // y avisa con toast; con número corto (menos de 10 dígitos) no abre nada.
  document.getElementById('fResp-wa').value = '';""",
    """  // 261D: sin número configurado abre wa.me/?text= para elegir contacto
  // y avisa con toast; con número corto (menos de 10 dígitos) no abre nada.
  // (262) Enviar ya vació los campos en 261C: rellenarlos para probar.
""" + relleno261 + """  document.getElementById('fResp-wa').value = '';""")
rep("""  document.getElementById('fResp-wa').value = '12345';
  opened259.length = 0;
  document.getElementById('btnRespEnviar')._h.click[0]();
  var d261corto = opened259.length === 0 && toastTxt().indexOf('al menos 10 dígitos') !== -1;""",
    relleno261 + """  document.getElementById('fResp-wa').value = '12345';
  opened259.length = 0;
  document.getElementById('btnRespEnviar')._h.click[0]();
  var d261corto = opened259.length === 0 && toastTxt().indexOf('al menos 10 dígitos') !== -1;""")

# --- 261E: el formulario ya no es "no se guarda nunca": solo se guarda
# con Guardar y cerrar (262); al teclear o al enviar no se guarda.
rep("""  // 261E: el número se persiste en localStorage al escribir y se carga
  // al abrir la vista; el formulario no se guarda en localStorage.""",
    """  // 261E: el número se persiste en localStorage al escribir y se carga
  // al abrir la vista; el formulario solo se guarda con Guardar y cerrar
  // (262), no al teclear ni al enviar (261C/261D borraron el borrador).""")

# --- Serie 262 nueva, antes de process.exit(0).
serie262 = """
  // 262: serie nueva — Responsiva con guardar y cerrar (borrador local).
  // 262A: Guardar y cerrar guarda los 6 campos en localStorage (clave
  // del borrador), muestra el toast y vuelve a Inicio; el número de
  // WhatsApp no forma parte del borrador y queda intacto.
  document.getElementById('fResp-nombre').value = 'Juan Pérez López';
  document.getElementById('fResp-colaborador').value = '98765';
  document.getElementById('fResp-sucursal').value = 'Polanco';
  document.getElementById('fResp-puesto').value = 'Técnico';
  document.getElementById('fResp-jefe').value = 'María García';
  document.getElementById('fResp-area').value = 'Sistemas';
  document.getElementById('fResp-wa').value = '5512345678';
  opened259.length = 0;
  document.getElementById('btnRespGuardar')._h.click[0]();
  var borr262 = null;
  try { borr262 = JSON.parse(global.localStorage.getItem('checklist-soporte-resp-borrador-v1') || 'null'); } catch (e) { borr262 = null; }
  var a262 = !!borr262 && borr262['fResp-nombre'] === 'Juan Pérez López' && borr262['fResp-colaborador'] === '98765' && borr262['fResp-sucursal'] === 'Polanco' && borr262['fResp-puesto'] === 'Técnico' && borr262['fResp-jefe'] === 'María García' && borr262['fResp-area'] === 'Sistemas' && !('fResp-wa' in borr262) && toastTxt().indexOf('Responsiva guardada') !== -1 && document.getElementById('viewInicio').hidden === false && document.getElementById('viewResp').hidden === true && opened259.length === 0;
  var a262wa = global.localStorage.getItem('checklist-soporte-resp-wa-v1') === '5512345678' && document.getElementById('fResp-wa').value === '5512345678';
  console.log('262A) Guardar y cerrar guarda el borrador y vuelve a Inicio:', a262, '| número de WhatsApp intacto:', a262wa);
  // 262B: el borrador puede estar incompleto: se guarda a medias y al
  // reabrir la vista se restaura tal cual (aquí se simula el arranque
  // vaciando los campos a mano y volviendo a abrir la vista).
  document.getElementById('fResp-nombre').value = 'Ana Ruiz';
  document.getElementById('fResp-colaborador').value = '';
  document.getElementById('fResp-sucursal').value = 'Roma Norte';
  document.getElementById('fResp-puesto').value = '';
  document.getElementById('fResp-jefe').value = '';
  document.getElementById('fResp-area').value = '';
  document.getElementById('btnRespGuardar')._h.click[0]();
  var borr262b = null;
  try { borr262b = JSON.parse(global.localStorage.getItem('checklist-soporte-resp-borrador-v1') || 'null'); } catch (e) { borr262b = null; }
  var b262guarda = !!borr262b && borr262b['fResp-nombre'] === 'Ana Ruiz' && borr262b['fResp-colaborador'] === '' && borr262b['fResp-sucursal'] === 'Roma Norte' && borr262b['fResp-puesto'] === '' && borr262b['fResp-jefe'] === '' && borr262b['fResp-area'] === '';
  ids261.forEach(function (id) { document.getElementById(id).value = ''; });
  showVista('resp');
  var b262restaura = document.getElementById('viewResp').hidden === false && document.getElementById('fResp-nombre').value === 'Ana Ruiz' && document.getElementById('fResp-colaborador').value === '' && document.getElementById('fResp-sucursal').value === 'Roma Norte' && document.getElementById('fResp-puesto').value === '' && document.getElementById('fResp-jefe').value === '' && document.getElementById('fResp-area').value === '';
  console.log('262B) borrador incompleto se guarda a medias:', b262guarda, '| al reabrir se restaura:', b262restaura);
  // 262C: Enviar con número abre wa.me y luego borra el borrador y vacía
  // los 6 campos; al reabrir, la vista sigue vacía.
  document.getElementById('fResp-nombre').value = 'Juan Pérez López';
  document.getElementById('fResp-colaborador').value = '98765';
  document.getElementById('fResp-sucursal').value = 'Polanco';
  document.getElementById('fResp-puesto').value = 'Técnico';
  document.getElementById('fResp-jefe').value = 'María García';
  document.getElementById('fResp-area').value = 'Sistemas';
  document.getElementById('fResp-wa').value = '5512345678';
  opened259.length = 0;
  document.getElementById('btnRespEnviar')._h.click[0]();
  var c262abre = opened259.length === 1 && opened259[0].indexOf('https://wa.me/525512345678?text=') === 0;
  var c262limpio = global.localStorage.getItem('checklist-soporte-resp-borrador-v1') === null && ids261.every(function (id) { return document.getElementById(id).value === ''; });
  showVista('resp');
  var c262vacia = ids261.every(function (id) { return document.getElementById(id).value === ''; });
  console.log('262C) Enviar con número abre wa.me:', c262abre, '| borra el borrador y vacía los campos:', c262limpio, '| al reabrir sigue vacía:', c262vacia);
  // 262D: Enviar sin número (shareText, wa.me/?text=) también borra el
  // borrador y vacía los campos.
  document.getElementById('fResp-nombre').value = 'Juan Pérez López';
  document.getElementById('fResp-colaborador').value = '98765';
  document.getElementById('fResp-sucursal').value = 'Polanco';
  document.getElementById('fResp-puesto').value = 'Técnico';
  document.getElementById('fResp-jefe').value = 'María García';
  document.getElementById('fResp-area').value = 'Sistemas';
  document.getElementById('btnRespGuardar')._h.click[0]();
  var d262hay = global.localStorage.getItem('checklist-soporte-resp-borrador-v1') !== null;
  document.getElementById('fResp-wa').value = '';
  opened259.length = 0;
  document.getElementById('btnRespEnviar')._h.click[0]();
  var d262abre = opened259.length === 1 && opened259[0].indexOf('https://wa.me/?text=') === 0;
  var d262limpio = global.localStorage.getItem('checklist-soporte-resp-borrador-v1') === null && ids261.every(function (id) { return document.getElementById(id).value === ''; });
  console.log('262D) había borrador guardado:', d262hay, '| Enviar sin número abre wa.me/?text=:', d262abre, '| borra el borrador y vacía los campos:', d262limpio);
  // 262E: Enviar con validación fallida NO borra el borrador: al reabrir
  // la vista el borrador sigue ahí.
  document.getElementById('fResp-nombre').value = 'Luis Torres';
  document.getElementById('fResp-colaborador').value = '';
  document.getElementById('fResp-sucursal').value = '';
  document.getElementById('fResp-puesto').value = '';
  document.getElementById('fResp-jefe').value = '';
  document.getElementById('fResp-area').value = '';
  document.getElementById('btnRespGuardar')._h.click[0]();
  ids261.forEach(function (id) { document.getElementById(id).value = ''; });
  opened259.length = 0;
  document.getElementById('btnRespEnviar')._h.click[0]();
  var e262falla = opened259.length === 0 && toastTxt().indexOf('Faltan:') !== -1;
  var e262queda = global.localStorage.getItem('checklist-soporte-resp-borrador-v1') !== null;
  showVista('resp');
  var e262restaura = document.getElementById('fResp-nombre').value === 'Luis Torres' && document.getElementById('fResp-colaborador').value === '';
  console.log('262E) validación fallida no abre WhatsApp:', e262falla, '| el borrador sigue guardado:', e262queda, '| al reabrir se restaura:', e262restaura);
  // 262F: Limpiar vacía los 6 campos y borra el borrador, sin tocar el número.
  document.getElementById('fResp-wa').value = '5512345678';
  document.getElementById('btnRespLimpiar')._h.click[0]();
  var f262 = ids261.every(function (id) { return document.getElementById(id).value === ''; }) && global.localStorage.getItem('checklist-soporte-resp-borrador-v1') === null && document.getElementById('fResp-wa').value === '5512345678';
  console.log('262F) Limpiar vacía los campos, borra el borrador y conserva el número:', f262);
"""
rep("  process.exit(0);\n})();\n", serie262 + "\n  process.exit(0);\n})();\n")

open(P, 'w', encoding='utf-8').write(s)
print('test20262.js generado')
