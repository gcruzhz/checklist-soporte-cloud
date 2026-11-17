# Parche de pruebas 2.5.8: test20257.js -> test20258.js (ya copiado).
P = '/home/hatch/workspace/android/checklist-cloud/tests/test20258.js'
s = open(P, encoding='utf-8').read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'NO ENCONTRADO x%d (esperado %d): %r' % (c, n, old[:120])
    s = s.replace(old, new)

# --- SRC y versión 2.5.8 (orden: primero 2.5.7 -> 2.5.8, luego 2.5.6 -> 2.5.7).
rep("const SRC = fs.readFileSync(__dirname + '/checklist20257.js', 'utf8');",
    "const SRC = fs.readFileSync(__dirname + '/checklist20258.js', 'utf8');")
rep("html.includes('Versión 2.5.7')", "html.includes('Versión 2.5.8')", n=4)
rep("html.includes('Versión: 2.5.7')", "html.includes('Versión: 2.5.8')", n=2)
rep("html.includes('Versión 2.5.6')", "html.includes('Versión 2.5.7')", n=2)
rep("!html.includes('2.5.6')", "!html.includes('2.5.7')", n=3)
rep("(html.match(/2\\.5\\.7/g) || []).length", "(html.match(/2\\.5\\.8/g) || []).length")
rep("var n257 = ", "var n258 = ")
rep("n257 === 2", "n258 === 2", n=2)
rep("'AM0) versión 2.5.7:'", "'AM0) versión 2.5.8:'")
rep("'AP0) estáticos 2.5.7:", "'AP0) estáticos 2.5.8:")
rep("'AR0) versión 2.5.7 visible:'", "'AR0) versión 2.5.8 visible:'")
rep("'| 0 de 2.5.6:'", "'| 0 de 2.5.7:'", n=2)
rep("'| ocurrencias 2.5.7:'", "'| ocurrencias 2.5.8:'")
rep("'BA0) versión 2.5.7 sin 2.5.6:'", "'BA0) versión 2.5.8 sin 2.5.7:'")
rep("'BB0) 2.5.7 en 2 sitios:'", "'BB0) 2.5.8 en 2 sitios:'")
rep("html.indexOf('Soporte 257')", "html.indexOf('Soporte 258')")

# --- Serie 258 nueva, antes de process.exit(0).
serie258 = """
  // 258: serie nueva — actualizaciones de Windows (solo escritorio).
  // 258A: botón oculto sin Desktop, visible con Desktop; el panel abre y
  // cierra los demás paneles; campos de estado y botones Buscar/Instalar.
  document.getElementById('winUpdBox').scrollIntoView = function () {};
  global.Desktop = undefined;
  refreshDetectarBtn();
  var a258oculto = document.getElementById('btnWinUpd').hidden === true;
  var a258panelOculto = document.getElementById('winUpdBox').hidden === true;
  var a258html = html.indexOf('id="btnWinUpd"') !== -1 && html.indexOf('id="winUpdBox"') !== -1 && html.indexOf('id="wuUltima"') !== -1 && html.indexOf('id="wuUltimaBusqueda"') !== -1 && html.indexOf('id="wuResumen"') !== -1 && html.indexOf('id="wuLista"') !== -1 && html.indexOf('id="wuEstado"') !== -1 && html.indexOf('id="btnWuBuscar"') !== -1 && html.indexOf('id="btnWuInstalar"') !== -1;
  var a258aviso = html.indexOf('NUNCA reinicia sola') !== -1;
  var llamadas258 = [];
  global.Desktop = {
    buscarActualizaciones: async function () { llamadas258.push(['buscar']); return { ok: true, pendientes: [{ kb: 'KB5034123', titulo: 'Actualización acumulada 2026-01' }, { kb: '', titulo: 'Actualización de .NET' }], ultimaInstalada: '2026-11-10', ultimaBusqueda: '2026-11-17' }; },
    instalarActualizaciones: async function () { llamadas258.push(['instalar']); return { ok: true, instaladas: 2, fallidas: 0, reinicioRequerido: true }; }
  };
  refreshDetectarBtn();
  var a258visible = document.getElementById('btnWinUpd').hidden === false;
  document.getElementById('btnWinUpd')._h.click[0]();
  var a258abre = document.getElementById('winUpdBox').hidden === false && document.getElementById('passBox').hidden === true;
  document.getElementById('btnWinUpd')._h.click[0]();
  var a258cierra = document.getElementById('winUpdBox').hidden === true;
  console.log('258A) sin Desktop oculto:', a258oculto, '| panel oculto al inicio:', a258panelOculto, '| HTML con botón+panel+campos:', a258html, '| aviso nunca reinicia:', a258aviso, '| con Desktop visible:', a258visible, '| clic abre el panel y cierra passBox:', a258abre, '| segundo clic lo cierra:', a258cierra);
  // 258B: Buscar con 2 pendientes, con 0, con error; botones bloqueados
  // mientras busca (la búsqueda tarda minutos en Windows real).
  var resuelveBuscar;
  global.Desktop.buscarActualizaciones = function () { llamadas258.push(['buscar']); return new Promise(function (res) { resuelveBuscar = res; }); };
  document.getElementById('btnWinUpd')._h.click[0]();
  document.getElementById('toast').textContent = '';
  document.getElementById('btnWuBuscar')._h.click[0]();
  var b258ocupado = document.getElementById('btnWuBuscar').disabled === true && document.getElementById('btnWuInstalar').disabled === true && document.getElementById('wuEstado').textContent.indexOf('Buscando') !== -1;
  resuelveBuscar({ ok: true, pendientes: [{ kb: 'KB5034123', titulo: 'Actualización acumulada 2026-01' }, { kb: '', titulo: 'Actualización de .NET' }], ultimaInstalada: '2026-11-10', ultimaBusqueda: '2026-11-17' });
  await sleep(20);
  var b258dos = document.getElementById('wuResumen').textContent === 'Actualizaciones pendientes: 2' && document.getElementById('wuLista').innerHTML.indexOf('KB5034123') !== -1 && document.getElementById('wuLista').innerHTML.indexOf('Actualización de .NET') !== -1 && document.getElementById('btnWuInstalar').disabled === false && document.getElementById('wuUltima').textContent.indexOf('2026-11-10') !== -1 && document.getElementById('wuUltimaBusqueda').textContent.indexOf('2026-11-17') !== -1 && toastTxt() === 'Se encontraron 2 actualizaciones pendientes.';
  global.Desktop.buscarActualizaciones = async function () { llamadas258.push(['buscar']); return { ok: true, pendientes: [], ultimaInstalada: '2026-11-17', ultimaBusqueda: '2026-11-17' }; };
  document.getElementById('btnWuBuscar')._h.click[0]();
  await sleep(20);
  var b258cero = document.getElementById('wuResumen').textContent === 'Sin actualizaciones pendientes ✓' && document.getElementById('btnWuInstalar').disabled === true && toastTxt() === 'Windows está actualizado ✓';
  global.Desktop.buscarActualizaciones = async function () { llamadas258.push(['buscar']); return { ok: false, error: 'Windows Update no respondió.' }; };
  document.getElementById('btnWuBuscar')._h.click[0]();
  await sleep(20);
  var b258err = toastTxt() === 'Windows Update no respondió.';
  console.log('258B) botones bloqueados mientras busca:', b258ocupado, '| 2 pendientes con KB y títulos:', b258dos, '| 0 pendientes deshabilita instalar:', b258cero, '| error avisa:', b258err);
  // 258C: Instalar sin pendientes no llama; con pendientes instala y
  // avisa reinicio; error de admin avisa.
  var nLlam258 = llamadas258.length;
  document.getElementById('toast').textContent = '';
  document.getElementById('btnWuInstalar')._h.click[0]();
  await sleep(20);
  var c258sin = toastTxt() === 'No hay actualizaciones pendientes para instalar.' && llamadas258.length === nLlam258;
  global.Desktop.buscarActualizaciones = async function () { llamadas258.push(['buscar']); return { ok: true, pendientes: [{ kb: 'KB5034123', titulo: 'Actualización acumulada 2026-01' }, { kb: 'KB5034444', titulo: 'Actualización de seguridad' }], ultimaInstalada: '2026-11-10', ultimaBusqueda: '2026-11-17' }; };
  document.getElementById('btnWuBuscar')._h.click[0]();
  await sleep(20);
  global.Desktop.instalarActualizaciones = async function () { llamadas258.push(['instalar']); return { ok: true, instaladas: 2, fallidas: 0, reinicioRequerido: true }; };
  document.getElementById('toast').textContent = '';
  document.getElementById('btnWuInstalar')._h.click[0]();
  var c258ocupadoInst = document.getElementById('btnWuBuscar').disabled === true && document.getElementById('btnWuInstalar').disabled === true;
  await sleep(20);
  var c258ok = toastTxt().indexOf('Actualizaciones instaladas: 2') !== -1 && toastTxt().indexOf('Windows pide reiniciar') !== -1 && llamadas258[llamadas258.length - 1][0] === 'instalar' && document.getElementById('wuEstado').textContent.indexOf('Windows pide reiniciar') !== -1 && document.getElementById('wuResumen').textContent.indexOf('Vuelve a buscar') !== -1;
  global.Desktop.buscarActualizaciones = async function () { llamadas258.push(['buscar']); return { ok: true, pendientes: [{ kb: 'KB1', titulo: 'U1' }], ultimaInstalada: '', ultimaBusqueda: '2026-11-17' }; };
  document.getElementById('btnWuBuscar')._h.click[0]();
  await sleep(20);
  global.Desktop.instalarActualizaciones = async function () { llamadas258.push(['instalar']); return { ok: false, error: 'Se necesita permiso de administrador para instalar las actualizaciones.' }; };
  document.getElementById('toast').textContent = '';
  document.getElementById('btnWuInstalar')._h.click[0]();
  await sleep(20);
  var c258admin = toastTxt() === 'Se necesita permiso de administrador para instalar las actualizaciones.';
  console.log('258C) sin pendientes no llama y avisa:', c258sin, '| botones bloqueados al instalar:', c258ocupadoInst, '| instaladas avisan con reinicio:', c258ok, '| error de admin avisa:', c258admin);
  // 258D: sin Desktop los botones avisan y no llaman; nada se guarda en
  // localStorage ni se manda a la nube; mailto 258.
  global.Desktop = undefined;
  var nLlam258b = llamadas258.length;
  document.getElementById('toast').textContent = '';
  document.getElementById('btnWuBuscar')._h.click[0]();
  await sleep(20);
  var d258buscar = toastTxt() === 'La búsqueda solo funciona en la app de escritorio.' && llamadas258.length === nLlam258b;
  document.getElementById('toast').textContent = '';
  document.getElementById('btnWuInstalar')._h.click[0]();
  await sleep(20);
  var d258instalar = toastTxt() === 'La instalación solo funciona en la app de escritorio.' && llamadas258.length === nLlam258b;
  var ls258 = JSON.stringify(global.localStorage._d);
  var d258noguarda = ls258.indexOf('KB5034123') === -1 && ls258.indexOf('Actualización acumulada') === -1;
  var d258mailto = html.indexOf('Soporte 258') !== -1;
  console.log('258D) sin Desktop buscar avisa sin llamar:', d258buscar, '| instalar avisa sin llamar:', d258instalar, '| nada guardado en localStorage:', d258noguarda, '| mailto 258:', d258mailto);
"""
rep("""  console.log('257D) sin Desktop verificar avisa sin llamar:', d257ver, '| cambiar avisa sin llamar:', d257cam, '| nada guardado en localStorage:', d257noguarda, '| mailto 257:', d257mailto);

  process.exit(0);""",
"""  console.log('257D) sin Desktop verificar avisa sin llamar:', d257ver, '| cambiar avisa sin llamar:', d257cam, '| nada guardado en localStorage:', d257noguarda, '| mailto 258:', d257mailto);
""" + serie258 + """
  process.exit(0);""")

open(P, 'w', encoding='utf-8').write(s)
print('OK test20258.js, bytes:', len(s))
print('258 refs:', s.count('258'), '| 257 refs:', s.count('257'))
