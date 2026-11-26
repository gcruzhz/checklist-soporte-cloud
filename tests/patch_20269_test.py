# Parche de pruebas 2.5.19: test20268.js -> test20269.js.
# 1) Extrae el <script> actual de www/index.html a
# tests/checklist20269.js (el JavaScript de esta version, que evalua el
# harness). 2) Copia test20268.js a test20269.js y actualiza la version
# (2.5.18 -> 2.5.19, 2.5.17 -> 2.5.18, n268 -> n269, mailto 268 ->
# 269). 3) El bundle NO cambia en 2.5.19 (firebase.js intacto): md5
# 9d4f0a81f3108d0f92f50f08fc48c752; las etiquetas de 265A/266A/267A/268A
# pasan de «bundle nuevo» a «bundle sin cambio». 4) Actualiza BA0
# (la barra superior ya no tiene pestaña de Mantenimientos) y W5
# (Usuarios ya no es pestaña: botón btnUsuarios de la barra de
# sesión). 5) Actualiza 268B al comportamiento nuevo: Área y Jefe
# Directo en DOS cajas apiladas con borde (dos rectángulos 410/166/22
# con distinta y, cada etiqueta en la fila de su valor, sin la celda
# combinada «Área: Jefe Directo:»). 6) Agrega la serie 269 (7 casos):
# versión 2.5.19 + bundle sin cambio + reglas; mensaje de error según
# la causa real (permiso denegado / sin red / otro código); carta que
# falla con permission-denied queda guardada en el teléfono marcada
# pendiente; reintento que sincroniza sin duplicar folio y sin subir
# el marcador; acuse que falla sin red y se reintenta desde su
# tarjeta; reintento automático al abrir la vista (y no sin nube);
# barra superior solo con Inicio y Equipo, tarjetas de Inicio
# intactas y navegación en todas las vistas.
# Uso: python3 patch_20269_test.py (corre desde tests/)
import os
import shutil

BASE = '/home/hatch/workspace/android/checklist-cloud'
TESTS = os.path.join(BASE, 'tests')
SRC = os.path.join(TESTS, 'test20268.js')
P = os.path.join(TESTS, 'test20269.js')
BUNDLE_MD5 = '9d4f0a81f3108d0f92f50f08fc48c752'

# --- Extraer el <script> actual de www/index.html.
html = open(os.path.join(BASE, 'www/index.html'), encoding='utf-8').read()
i = html.index('<script>', html.index('firebase-config'))
j = html.index('</script>', i)
open(os.path.join(TESTS, 'checklist20269.js'), 'w', encoding='utf-8').write(html[i + len('<script>'):j])
print('checklist20269.js extraido:', j - i - len('<script>'), 'bytes')

shutil.copyfile(SRC, P)
s = open(P, encoding='utf-8').read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'NO ENCONTRADO x%d (esperado %d): %r' % (c, n, old[:120])
    s = s.replace(old, new)


def repall(old, new, n):
    rep(old, new, n)


# --- SRC y version 2.5.19 (orden: primero 2.5.18 -> 2.5.19, luego
# 2.5.17 -> 2.5.18 para las referencias a la version anterior).
rep("const SRC = fs.readFileSync(__dirname + '/checklist20268.js', 'utf8');",
    "const SRC = fs.readFileSync(__dirname + '/checklist20269.js', 'utf8');")
repall("2.5.18", "2.5.19", 44)
repall("2.5.17", "2.5.18", 16)
repall("n268", "n269", 7)
repall("Soporte 268", "Soporte 269", 3)
repall("mailto 268", "mailto 269", 5)
# El regex lleva la versión con barras escapadas: el reemplazo plano
# de "2.5.18" no lo toca, hay que actualizarlo aparte.
BS = chr(92)
rep("var n269 = (html.match(/2" + BS + ".5" + BS + ".18/g) || []).length;",
    "var n269 = (html.match(/2" + BS + ".5" + BS + ".19/g) || []).length;")

# --- Bundle SIN cambio en 2.5.19 (firebase.js no se tocó): las
# etiquetas de 265A/266A/267A/268A pasan de «nuevo» a «sin cambio».
rep("console.log('265A) versión 2.5.19:', a265ver, '| bundle nuevo 2.5.19 (9d4f0a81…):'",
    "console.log('265A) versión 2.5.19:', a265ver, '| bundle sin cambio (9d4f0a81…):'")
rep("  // 266A: versión 2.5.19 en los 2 sitios, mailto 269, bundle nuevo 2.5.19",
    "  // 266A: versión 2.5.19 en los 2 sitios, mailto 269, bundle sin cambio 2.5.18")
rep("console.log('266A) versión 2.5.19:', a266ver, '| bundle nuevo 2.5.19 (9d4f0a81…):'",
    "console.log('266A) versión 2.5.19:', a266ver, '| bundle sin cambio (9d4f0a81…):'")
rep("  // 267A: versión 2.5.19 en los 2 sitios, bundle NUEVO 2.5.19",
    "  // 267A: versión 2.5.19 en los 2 sitios, bundle SIN cambio 2.5.18")
rep("console.log('267A) versión 2.5.19:', a267ver, '| bundle nuevo 2.5.19 (9d4f0a81…):'",
    "console.log('267A) versión 2.5.19:', a267ver, '| bundle sin cambio (9d4f0a81…):'")
rep("""  // 268A: versión 2.5.19 en los 2 sitios, bundle NUEVO (firebase.js
  // cambió: asignarFolioAcuse) y reglas con el contador nuevo.""",
    """  // 268A: versión 2.5.19 en los 2 sitios, bundle SIN cambio en
  // 2.5.19 (firebase.js con asignarFolioAcuse es de 2.5.18) y reglas
  // con el contador nuevo.""")
rep("console.log('268A) versión 2.5.19:', a268ver, '| bundle nuevo (9d4f0a81…):'",
    "console.log('268A) versión 2.5.19:', a268ver, '| bundle sin cambio (9d4f0a81…):'")

# --- BA0: la barra superior ya no tiene pestaña de Mantenimientos
# (2.5.19: solo Inicio y Equipo; Mantenimientos se abre desde la
# tarjeta grande de Inicio). ---
rep("""  var ba0sel = html.includes('id="viewInicio"') && html.includes('id="btnGoMant"') && html.includes('Mantenimientos Preventivos') && html.includes('data-v="inicio"') && html.includes('data-v="mant"');""",
    """  // (2.5.19) La barra superior solo tiene Inicio y Equipo: ya no hay
  // pestaña de Mantenimientos (se entra desde la tarjeta de Inicio).
  var ba0sel = html.includes('id="viewInicio"') && html.includes('id="btnGoMant"') && html.includes('Mantenimientos Preventivos') && html.includes('data-v="inicio"') && html.includes('data-v="equipo"') && !html.includes('data-v="mant"') && !html.includes('data-v="preparar"');""")
rep("console.log('BA0) versión 2.5.19 sin 2.5.18:', ba0html, '| selector y tabs Inicio/Mant:', ba0sel,",
    "console.log('BA0) versión 2.5.19 sin 2.5.18:', ba0html, '| selector y tabs solo Inicio/Equipo:', ba0sel,")

# --- W5: Usuarios ya no es pestaña (2.5.19): es el botón btnUsuarios
# de la barra de sesión, solo para el admin. ---
rep("""  // W5: el botón grande Reasignar Equipo lo ven todos (solo Usuarios sigue siendo admin).
  document.getElementById('viewUsuarios').hidden = true;
  cloudRole = 'usuario'; applyRoleUI();
  const bigU = document.getElementById('btnShowRe').hidden === false && document.getElementById('tabUsuarios').hidden === true;
  cloudRole = 'admin'; applyRoleUI();
  const bigA = document.getElementById('btnShowRe').hidden === false && document.getElementById('tabUsuarios').hidden === false;
  console.log('W5) usuario: botón grande visible:', bigU, '| admin: visible:', bigA);""",
    """  // W5: el botón grande Reasignar Equipo lo ven todos (solo Usuarios sigue siendo admin).
  // (2.5.19) Usuarios ya no es pestaña: es el botón btnUsuarios de la
  // barra de sesión, solo para el admin.
  document.getElementById('viewUsuarios').hidden = true;
  cloudRole = 'usuario'; applyRoleUI();
  const bigU = document.getElementById('btnShowRe').hidden === false && document.getElementById('btnUsuarios').hidden === true;
  cloudRole = 'admin'; applyRoleUI();
  const bigA = document.getElementById('btnShowRe').hidden === false && document.getElementById('btnUsuarios').hidden === false;
  console.log('W5) usuario: botón grande visible:', bigU, '| admin: visible:', bigA);""")

# --- 268B: Área y Jefe Directo en DOS cajas apiladas con borde
# (2.5.19), ya no juntos en una sola celda. ---
rep("""  // 268B: PDF de la Carta con CAJAS CON BORDE VISIBLE en los campos:
  // rectángulos con borde ('x y w h re S') en las posiciones de la
  // captura (izq. x=146 w=184; der. x=410 w=166, Ip de 44 pt y Jefe de
  // 22 pt; Observaciones x=36 w=540 h=22), divisores verticales en la
  // tabla Exclusivo (líneas x=153/270/423), verde #9BBB59, y el campo
  // «Área: Jefe Directo:» con los dos valores del formulario.""",
    """  // 268B (ACTUALIZADO en 2.5.19): PDF de la Carta con CAJAS CON BORDE
  // VISIBLE en los campos: rectángulos con borde ('x y w h re S') en
  // las posiciones de la captura (izq. x=146 w=184; der. x=410 w=166,
  // Ip de 44 pt y Área y Jefe Directo de 22 pt CADA UNO en su propia
  // caja apilada — antes iban juntos en una sola celda «Área: Jefe
  // Directo:»; Observaciones x=36 w=540 h=22), divisores verticales
  // en la tabla Exclusivo (líneas x=153/270/423), verde #9BBB59.""")
rep("""  function rects268(pdf) { var out = [], re = /([\\d.]+) ([\\d.]+) ([\\d.]+) ([\\d.]+) re S/g, m; while ((m = re.exec(pdf))) out.push([Number(m[1]), Number(m[2]), Number(m[3]), Number(m[4])]); return out; }
  function hasRect268(rs, x, w, h) { return rs.some(function (r) { return r[0] === x && r[2] === w && r[3] === h; }); }
  var rs268b = rects268(pdf268b);
  var b268 = (pdf268b.match(/\\/Type \\/Page[^s]/g) || []).length === 2 &&
    hasRect268(rs268b, 146, 184, 22) && hasRect268(rs268b, 410, 166, 44) && hasRect268(rs268b, 410, 166, 22) && hasRect268(rs268b, 36, 540, 22) &&
    /153\\.0 [\\d.]+ m 153\\.0 [\\d.]+ l S/.test(pdf268b) && /423\\.0 [\\d.]+ m 423\\.0 [\\d.]+ l S/.test(pdf268b) &&
    pdf268b.indexOf('0.608 0.733 0.349 rg') !== -1 &&
    txt268b.indexOf('Nombre del colaborador:') !== -1 && txt268b.indexOf('Rosa Blanca') !== -1 &&
    txt268b.indexOf('Área: Jefe Directo:') !== -1 && txt268b.indexOf('Sistemas') !== -1 && txt268b.indexOf('María García') !== -1 &&
    txt268b.indexOf('FOLIO: 00043') !== -1;
  console.log('268B) PDF carta: cajas con borde en los campos, divisores Exclusivo, Área: Jefe Directo:', b268);""",
    """  function rects268(pdf) { var out = [], re = /([\\d.]+) ([\\d.]+) ([\\d.]+) ([\\d.]+) re S/g, m; while ((m = re.exec(pdf))) out.push([Number(m[1]), Number(m[2]), Number(m[3]), Number(m[4])]); return out; }
  function hasRect268(rs, x, w, h) { return rs.some(function (r) { return r[0] === x && r[2] === w && r[3] === h; }); }
  function countRect268(rs, x, w, h) { return rs.filter(function (r) { return r[0] === x && r[2] === w && r[3] === h; }).length; }
  var rs268b = rects268(pdf268b);
  // (2.5.19) Cada etiqueta en su propia fila, con su valor en la
  // misma fila (misma y) y en fila distinta de la otra.
  var rowArea268 = rows268b.filter(function (r) { return r.t === 'Área:'; });
  var rowJefe268 = rows268b.filter(function (r) { return r.t === 'Jefe Directo:'; });
  var b268 = (pdf268b.match(/\\/Type \\/Page[^s]/g) || []).length === 2 &&
    hasRect268(rs268b, 146, 184, 22) && hasRect268(rs268b, 410, 166, 44) && countRect268(rs268b, 410, 166, 22) === 2 && hasRect268(rs268b, 36, 540, 22) &&
    /153\\.0 [\\d.]+ m 153\\.0 [\\d.]+ l S/.test(pdf268b) && /423\\.0 [\\d.]+ m 423\\.0 [\\d.]+ l S/.test(pdf268b) &&
    pdf268b.indexOf('0.608 0.733 0.349 rg') !== -1 &&
    txt268b.indexOf('Nombre del colaborador:') !== -1 && txt268b.indexOf('Rosa Blanca') !== -1 &&
    txt268b.indexOf('Área: Jefe Directo:') === -1 &&
    rowArea268.length === 1 && rowJefe268.length === 1 && rowArea268[0].y !== rowJefe268[0].y &&
    rows268b.some(function (r) { return r.t === 'Sistemas' && r.y === rowArea268[0].y; }) &&
    rows268b.some(function (r) { return r.t === 'María García' && r.y === rowJefe268[0].y; }) &&
    txt268b.indexOf('FOLIO: 00043') !== -1;
  console.log('268B) PDF carta: cajas con borde en los campos, divisores Exclusivo, Área y Jefe Directo en cajas separadas:', b268);""")

# --- Serie 269 nueva, antes de process.exit(0). ---
serie269 = """
  // 269: serie nueva — 2.5.19: Área y Jefe Directo en cajas separadas
  // en el PDF de la Carta; aviso de guardado según la causa real con
  // respaldo local pendiente de sincronizar y reintento automático;
  // barra superior solo con Inicio y Equipo.
  CLOUD_ENABLED = false;
  // 269A: versión 2.5.19 en los 2 sitios, bundle SIN cambio
  // (firebase.js no cambió en 2.5.19: md5 9d4f0a81…) y reglas con
  // acuses/cartas y folios.
  var crypto269 = require('crypto');
  var bundle269 = fs.readFileSync('/home/hatch/workspace/android/checklist-cloud/www/cloud/firebase.bundle.js');
  var md5bundle269 = crypto269.createHash('md5').update(bundle269).digest('hex');
  var a269ver = html.includes('Versión 2.5.19') && html.includes('Versión: 2.5.19') && !html.includes('2.5.18');
  var a269bundle = md5bundle269 === 'BUNDLE_MD5';
  var rules269 = fs.readFileSync('/home/hatch/workspace/android/checklist-cloud/firestore.rules', 'utf8');
  var a269rules = rules269.includes('match /config/foliosAcuse') && rules269.includes('match /config/foliosCarta') &&
    rules269.includes('match /acuses/{id}') && rules269.includes('match /cartas/{id}');
  console.log('269A) versión 2.5.19:', a269ver, '| bundle sin cambio (9d4f0a81…):', a269bundle, '| reglas con acuses/cartas y folios:', a269rules);
  // 269B: el aviso de guardado distingue la causa real (nada de
  // aviso genérico): permission-denied habla de las reglas en la
  // consola; unavailable dice sin conexión y que quedó en el teléfono;
  // otro error muestra su código; y el aviso genérico viejo ya no
  // existe en el HTML.
  var m269perm = mensajeErrorNube({ code: 'permission-denied' }, 'la carta');
  var m269off = mensajeErrorNube({ code: 'unavailable' }, 'el acuse');
  var m269otro = mensajeErrorNube({ code: 'aborted', message: 'x' }, 'la carta');
  var m269sin = mensajeErrorNube(new Error('boom'), 'el acuse');
  var b269 = m269perm.indexOf('reglas') !== -1 && m269perm.indexOf('consola') !== -1 && m269perm.indexOf('teléfono') !== -1 &&
    m269off.indexOf('Sin conexión') === 0 && m269off.indexOf('teléfono') !== -1 &&
    m269otro.indexOf('aborted') !== -1 && m269otro.indexOf('teléfono') !== -1 &&
    m269sin.indexOf('boom') !== -1 &&
    !html.includes('No se pudo guardar la carta en la nube. Revisa tu conexión.') &&
    !html.includes('No se pudo guardar el acuse en la nube. Revisa tu conexión.');
  console.log('269B) aviso según la causa: reglas en consola / sin conexión / código del error:', b269);
  // 269C: la carta que falla con permission-denied queda guardada EN
  // EL TELÉFONO (mismo folio, marcada pendiente), aparece en la lista
  // con «Pendiente de sincronizar» y botón Reintentar, y el aviso
  // dice lo de las reglas; el folio del formulario se conserva.
  doLogin('usuario');
  CLOUD_ENABLED = true;
  global.Cloud.crearCarta = async function () { var e = new Error('Missing or insufficient permissions.'); e.code = 'permission-denied'; throw e; };
  localStorage.setItem(CARTA_FOLIO_LOCAL_KEY, '1');
  cartaEditId = null;
  document.getElementById('fCa-folio').value = '';
  showVista('carta');
  var folio269c = document.getElementById('fCa-folio').value;
  document.getElementById('fCa-nombre').value = 'Juan Pérez López';
  document.getElementById('fCa-area').value = 'Sistemas';
  document.getElementById('fCa-jefe').value = 'María García';
  cartaEqFilas = [{ modelo: 'Latitude 5420', marca: 'Dell', serie: 'ABC123', concepto: 'Laptop' }];
  var nCartas269c = cartas.length;
  var ok269c = await cartaGuardar();
  var saved269c = cartas[cartas.length - 1];
  var list269c = document.getElementById('cartaList').innerHTML;
  var ls269c = JSON.parse(localStorage.getItem(CARTA_LS_KEY) || '[]');
  var c269 = folio269c === '00001' && ok269c === true && cartas.length === nCartas269c + 1 &&
    !!saved269c && saved269c.folio === '00001' && saved269c.pendienteSync === true &&
    saved269c.datos.area === 'Sistemas' && saved269c.datos.jefe === 'María García' &&
    list269c.indexOf('Pendiente de sincronizar') !== -1 && list269c.indexOf('data-carta-retry') !== -1 &&
    toastTxt().indexOf('reglas') !== -1 && toastTxt().indexOf('consola') !== -1 &&
    ls269c.some(function (x) { return x.id === saved269c.id && x.pendienteSync === true; });
  console.log('269C) carta con permiso denegado: queda en el teléfono pendiente, folio 00001, aviso de reglas:', c269);
  // 269D: el reintento sincroniza SIN duplicar folio y SIN subir el
  // marcador pendiente; la tarjeta ya no muestra la marca.
  var up269d = [];
  global.Cloud.upsertCarta = async function (rec) { up269d.push(rec); };
  var ok269d = await cartaReintentarSync(saved269c.id);
  var list269d = document.getElementById('cartaList').innerHTML;
  var d269 = ok269d === true && up269d.length === 1 && up269d[0].id === saved269c.id && up269d[0].folio === '00001' &&
    up269d[0].pendienteSync === undefined && saved269c.pendienteSync === false &&
    cartas.length === nCartas269c + 1 && list269d.indexOf('Pendiente de sincronizar') === -1 &&
    (await cartaReintentarSync(saved269c.id)) === false;
  console.log('269D) reintento sincroniza con el mismo folio, sin marcador, sin duplicar:', d269);
  // 269E: el acuse que falla SIN RED queda en el teléfono con el
  // aviso de sin conexión, y se reintenta desde el botón de su
  // tarjeta.
  localStorage.setItem(ACUSE_FOLIO_LOCAL_KEY, '1');
  acuseEditId = null;
  document.getElementById('fAc-folio').value = '';
  global.Cloud.crearAcuse = async function () { var e = new Error('offline'); e.code = 'unavailable'; throw e; };
  showVista('acuse');
  document.getElementById('fAc-para').value = 'Beatriz Garduño Dominguez RH - Revolución';
  document.getElementById('fAc-de').value = 'SISTEMAS';
  var nAcuses269e = acuses.length;
  var ok269e = await acuseGuardar();
  var saved269e = acuses[acuses.length - 1];
  var list269e = document.getElementById('acuseList').innerHTML;
  var e269a = ok269e === true && acuses.length === nAcuses269e + 1 && !!saved269e &&
    saved269e.folio === '00001' && saved269e.pendienteSync === true &&
    list269e.indexOf('Pendiente de sincronizar') !== -1 && list269e.indexOf('data-acuse-retry') !== -1 &&
    toastTxt().indexOf('Sin conexión') === 0;
  var up269e = [];
  global.Cloud.upsertAcuse = async function (rec) { up269e.push(rec); };
  document.getElementById('acuseList')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-acuse-retry]' ? { getAttribute: function () { return saved269e.id; } } : null; } } });
  await sleep(20);
  var e269b = up269e.length === 1 && up269e[0].id === saved269e.id && up269e[0].folio === '00001' && up269e[0].pendienteSync === undefined &&
    saved269e.pendienteSync === false && document.getElementById('acuseList').innerHTML.indexOf('Pendiente de sincronizar') === -1;
  console.log('269E) acuse sin red: queda pendiente con aviso de sin conexión:', e269a, '| botón Reintentar lo sincroniza:', e269b);
  // 269F: al ABRIR la vista, los pendientes se reintentan SOLOS; sin
  // nube no se reintenta nada.
  var pend269f = { id: 'pend269f', folio: '00009', creadoEn: Date.now(), creadoPor: 'u1', creadoPorNombre: 'Test User', datos: { fecha: '2026-09-01', nombre: 'Ana López', equipos: [{ modelo: 'X1', marca: 'Lenovo', serie: 'ZZ9', concepto: 'Laptop' }] }, pendienteSync: true };
  cartas.push(pend269f);
  saveCartaLocal();
  var up269f = [];
  global.Cloud.upsertCarta = async function (rec) { up269f.push(rec); };
  showVista('carta');
  await sleep(30);
  var f269a = up269f.length === 1 && up269f[0].id === 'pend269f' && up269f[0].folio === '00009' && pend269f.pendienteSync === false;
  CLOUD_ENABLED = false;
  var pend269f2 = { id: 'pend269f2', folio: '00010', creadoEn: Date.now(), creadoPor: 'u1', creadoPorNombre: 'Test User', datos: { fecha: '2026-09-01', nombre: 'Luis Pérez', equipos: [{ modelo: 'X2', marca: 'HP', serie: 'YY8', concepto: 'Laptop' }] }, pendienteSync: true };
  cartas.push(pend269f2);
  saveCartaLocal();
  showVista('carta');
  await sleep(30);
  var f269b = up269f.length === 1 && pend269f2.pendienteSync === true;
  CLOUD_ENABLED = true;
  console.log('269F) al abrir la vista los pendientes se suben solos:', f269a, '| sin nube no se reintenta:', f269b);
  // 269G: barra superior solo con Inicio y Equipo (las pestañas del
  // medio ya no existen); las 7 tarjetas grandes de Inicio intactas;
  // la navegación funciona en todas las vistas, con «Volver a Inicio»
  // y con la pestaña Equipo; Usuarios se abre con el botón de la
  // barra de sesión (solo admin).
  var g269tabs = !html.includes('data-v="preparar"') && !html.includes('data-v="rec"') && !html.includes('data-v="for"') && !html.includes('data-v="mant"') && !html.includes('data-v="usuarios"') && html.includes('data-v="inicio"') && html.includes('data-v="equipo"');
  var g269cards = ['btnGoPreparar', 'btnGoRec', 'btnGoFor', 'btnGoMant', 'btnGoResp', 'btnGoAcuse', 'btnGoCarta'].every(function (id) { return html.includes('id="' + id + '"'); });
  function vistaVisible269(v, id) { showVista(v); return document.getElementById(id).hidden === false; }
  var g269nav = vistaVisible269('preparar', 'viewPreparar') && vistaVisible269('rec', 'viewRenta-rec') && vistaVisible269('for', 'viewRenta-for') && vistaVisible269('mant', 'viewMant') && vistaVisible269('resp', 'viewResp') && vistaVisible269('acuse', 'viewAcuse') && vistaVisible269('carta', 'viewCarta') && vistaVisible269('equipo', 'viewEquipo');
  showVista('acuse');
  document.getElementById('btnAcuseVolver')._h.click[0]();
  var g269volver = document.getElementById('viewInicio').hidden === false;
  showVista('carta');
  document.getElementById('btnCartaVolver')._h.click[0]();
  g269volver = g269volver && document.getElementById('viewInicio').hidden === false;
  document.getElementById('tabs')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-v]' ? { getAttribute: function () { return 'equipo'; } } : null; } } });
  var g269tabEq = document.getElementById('viewEquipo').hidden === false;
  document.getElementById('tabs')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-v]' ? { getAttribute: function () { return 'inicio'; } } : null; } } });
  var g269tabIn = document.getElementById('viewInicio').hidden === false;
  cloudRole = 'admin'; applyRoleUI();
  var g269usuBtn = document.getElementById('btnUsuarios').hidden === false;
  document.getElementById('btnUsuarios')._h.click[0]();
  var g269usuVista = document.getElementById('viewUsuarios').hidden === false;
  cloudRole = 'usuario'; applyRoleUI();
  var g269usuNo = document.getElementById('btnUsuarios').hidden === true;
  console.log('269G) barra solo Inicio y Equipo:', g269tabs, '| 7 tarjetas de Inicio intactas:', g269cards, '| navegación en todas las vistas:', g269nav, '| Volver a Inicio:', g269volver, '| pestañas Inicio/Equipo:', g269tabEq && g269tabIn, '| Usuarios por botón solo admin:', g269usuBtn && g269usuVista && g269usuNo);

"""

serie269 = serie269.replace('BUNDLE_MD5', BUNDLE_MD5)
assert 'BUNDLE_MD5' not in serie269
assert s.count('  process.exit(0);') == 1, 'ancla process.exit no única'
s = s.replace('  process.exit(0);', serie269 + '  process.exit(0);', 1)

open(P, 'w', encoding='utf-8').write(s)
print('test20269.js escrito:', len(s), 'bytes')
