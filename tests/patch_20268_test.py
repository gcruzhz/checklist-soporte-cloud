# Parche de pruebas 2.5.18: test20267.js -> test20268.js.
# 1) Extrae el <script> actual de www/index.html a
# tests/checklist20268.js (el JavaScript de esta version, que evalua el
# harness). 2) Copia test20267.js a test20268.js y actualiza la version
# (2.5.17 -> 2.5.18, 2.5.16 -> 2.5.17, n267 -> n268, mailto 267 ->
# 268). 3) El bundle CAMBIA en 2.5.18 (firebase.js con
# asignarFolioAcuse): md5 nuevo 9d4f0a81f3108d0f92f50f08fc48c752 en
# 265A/266A/267A. 4) Actualiza la serie 266 al comportamiento nuevo:
# 266B ya no espera el folio vacío con «Se asigna al guardar» (ahora
# el folio viene asignado al abrir, «Se asigna al abrir»). 266F sigue
# válido (crearCarta mock devuelve 00042; el folio del formulario se
# pasa como tercer argumento y el guardado usa el devuelto). 5) Agrega
# la serie 268 (6 casos): versión 2.5.18 + bundle nuevo + firebase.js
# con folio Acuse + reglas con foliosAcuse; PDF de la Carta con cajas
# con borde visible en los campos (rectángulos 're S' en sus
# posiciones), divisores verticales en Exclusivo y «Área: Jefe
# Directo:»; folio al abrir en la Carta (local); folio al abrir en el
# Acuse (local) con secuencias independientes; folio consumido si se
# abandona sin guardar (hueco); Acuse PDF con FOLIO y RECIBE con
# bordes.
# Uso: python3 patch_20268_test.py (corre desde tests/)
import os
import shutil

BASE = '/home/hatch/workspace/android/checklist-cloud'
TESTS = os.path.join(BASE, 'tests')
SRC = os.path.join(TESTS, 'test20267.js')
P = os.path.join(TESTS, 'test20268.js')
BUNDLE_MD5 = '9d4f0a81f3108d0f92f50f08fc48c752'
BUNDLE_MD5_OLD = 'd8ad9d102d13ef69925d7bdab65b9e33'

# --- Extraer el <script> actual de www/index.html.
html = open(os.path.join(BASE, 'www/index.html'), encoding='utf-8').read()
i = html.index('<script>', html.index('firebase-config'))
j = html.index('</script>', i)
open(os.path.join(TESTS, 'checklist20268.js'), 'w', encoding='utf-8').write(html[i + len('<script>'):j])
print('checklist20268.js extraido:', j - i - len('<script>'), 'bytes')

shutil.copyfile(SRC, P)
s = open(P, encoding='utf-8').read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'NO ENCONTRADO x%d (esperado %d): %r' % (c, n, old[:120])
    s = s.replace(old, new)


def repall(old, new, n):
    rep(old, new, n)


# --- SRC y version 2.5.18 (orden: primero 2.5.17 -> 2.5.18, luego
# 2.5.16 -> 2.5.17 para las referencias a la version anterior).
rep("const SRC = fs.readFileSync(__dirname + '/checklist20267.js', 'utf8');",
    "const SRC = fs.readFileSync(__dirname + '/checklist20268.js', 'utf8');")
repall("2.5.17", "2.5.18", 33)
repall("2.5.16", "2.5.17", 14)
repall("n267", "n268", 7)
repall("Soporte 267", "Soporte 268", 3)
repall("mailto 267", "mailto 268", 5)
# El regex lleva la versión con barras escapadas: el reemplazo plano
# de "2.5.17" no lo toca, hay que actualizarlo aparte.
BS = chr(92)
rep("var n268 = (html.match(/2" + BS + ".5" + BS + ".17/g) || []).length;",
    "var n268 = (html.match(/2" + BS + ".5" + BS + ".18/g) || []).length;")

# --- Bundle NUEVO en 2.5.18 (firebase.js cambió): md5 en 265A/266A/267A.
repall(BUNDLE_MD5_OLD, BUNDLE_MD5, 3)
repall("(md5 d8ad9d10…)", "(md5 9d4f0a81…)", 2)
rep("console.log('265A) versión 2.5.18:', a265ver, '| bundle nuevo 2.5.18 (d8ad9d10…):'",
    "console.log('265A) versión 2.5.18:', a265ver, '| bundle nuevo 2.5.18 (9d4f0a81…):'")
rep("  // 266A: versión 2.5.18 en los 2 sitios, mailto 268, bundle sin cambio",
    "  // 266A: versión 2.5.18 en los 2 sitios, mailto 268, bundle nuevo 2.5.18")
rep("console.log('266A) versión 2.5.18:', a266ver, '| bundle sin cambio (d8ad9d10…):'",
    "console.log('266A) versión 2.5.18:', a266ver, '| bundle nuevo 2.5.18 (9d4f0a81…):'")
rep("  // 267A: versión 2.5.18 en los 2 sitios, bundle SIN cambio",
    "  // 267A: versión 2.5.18 en los 2 sitios, bundle NUEVO 2.5.18")
rep("console.log('267A) versión 2.5.18:', a267ver, '| bundle sin cambio (d8ad9d10…):'",
    "console.log('267A) versión 2.5.18:', a267ver, '| bundle nuevo 2.5.18 (9d4f0a81…):'")

# --- 266B: el folio ya NO viene vacío al abrir la Carta (2.5.18: se
# asigna al abrir, «Se asigna al abrir», 5 dígitos). ---
rep("  // 266B: el Acuse empieza VACÍO (los datos del ejemplo no se\n  // prellenan) y la fecha es la de hoy; la vista Carta existe.",
    "  // 266B: el Acuse empieza VACÍO (los datos del ejemplo no se\n  // prellenan) y la fecha es la de hoy; la vista Carta existe.\n  // (2.5.18: al abrir la Carta el folio YA viene asignado, 5 dígitos,\n  // «Se asigna al abrir»; ya no viene vacío como en 2.5.17).")
rep("""  var b266c = document.getElementById('viewCarta').hidden === false && document.getElementById('fCa-nombre').value === '' &&
    document.getElementById('fCa-ip').value === '' && document.getElementById('fCa-folio').value === '' &&
    html.includes('placeholder="Se asigna al guardar"');
  console.log('266B) acuse vacío por defecto y fecha de hoy:', b266, '| carta vacía, Ip vacía y folio "Se asigna al guardar":', b266c);""",
"""  var b266c = document.getElementById('viewCarta').hidden === false && document.getElementById('fCa-nombre').value === '' &&
    document.getElementById('fCa-ip').value === '' && /^\\d{5}$/.test(document.getElementById('fCa-folio').value) &&
    html.includes('placeholder="Se asigna al abrir"');
  console.log('266B) acuse vacío por defecto y fecha de hoy:', b266, '| carta vacía, Ip vacía y folio ya asignado al abrir:', b266c);""")

# --- 266L: el folio ya NO se asigna al guardar (2.5.18: se asigna
# al abrir/limpiar, así que los números exactos dependen de cuántas
# veces se abrió el formulario). Lo que se verifica ahora: la segunda
# carta guardada lleva el folio siguiente al de la primera
# (consecutivos, sin repetir) y ambas quedan en la lista. ---
rep("""  // 266L: modo local: el segundo folio es 00002 y ambas cartas quedan
  // en la lista local.
  cartaLimpiarForm();
  document.getElementById('fCa-nombre').value = 'Ana López';
  cartaEqFilas = [{ modelo: 'X1', marca: 'Lenovo', serie: 'ZZ9', concepto: 'Laptop' }];
  var ok266l = await cartaGuardar();
  var c266l = cartas[cartas.length - 1];
  var l266 = ok266l === true && c266l.folio === '00002' &&
    document.getElementById('cartaList').innerHTML.indexOf('Folio 00002') !== -1 &&
    document.getElementById('cartaList').innerHTML.indexOf('Folio 00001') !== -1;
  console.log('266L) modo local: segundo folio 00002, ambas cartas en la lista:', l266);""",
"""  // 266L: modo local (2.5.18): el folio se asigna al abrir/limpiar,
  // no al guardar: la segunda carta guardada lleva el folio siguiente
  // al de la primera (consecutivos, sin repetir) y ambas quedan en
  // la lista local.
  var prev266l = cartas[cartas.length - 1].folio;
  cartaLimpiarForm();
  document.getElementById('fCa-nombre').value = 'Ana López';
  cartaEqFilas = [{ modelo: 'X1', marca: 'Lenovo', serie: 'ZZ9', concepto: 'Laptop' }];
  var ok266l = await cartaGuardar();
  var c266l = cartas[cartas.length - 1];
  var l266 = ok266l === true && c266l.folio === String(Number(prev266l) + 1).padStart(5, '0') &&
    document.getElementById('cartaList').innerHTML.indexOf('Folio ' + c266l.folio) !== -1 &&
    document.getElementById('cartaList').innerHTML.indexOf('Folio ' + prev266l) !== -1;
  console.log('266L) modo local: folios consecutivos sin repetir, ambas cartas en la lista:', l266);""")

# --- Serie 268 nueva, antes de process.exit(0). ---
serie268 = """
  // 268: serie nueva — folio automático AL ABRIR en Acuse y Carta
  // (2.5.18) y cajas con borde visible en el PDF de la Carta, como la
  // imagen del formato original FO-SI-10.
  async function pdfStrOf268(blob) { return Buffer.from(await blob.arrayBuffer()).toString('latin1'); }
  CLOUD_ENABLED = false;
  // 268A: versión 2.5.18 en los 2 sitios, bundle NUEVO (firebase.js
  // cambió: asignarFolioAcuse) y reglas con el contador nuevo.
  var crypto268 = require('crypto');
  var bundle268 = fs.readFileSync('/home/hatch/workspace/android/checklist-cloud/www/cloud/firebase.bundle.js');
  var md5bundle268 = crypto268.createHash('md5').update(bundle268).digest('hex');
  var fb268 = fs.readFileSync('/home/hatch/workspace/android/checklist-cloud/www/cloud/firebase.js', 'utf8');
  var rules268 = fs.readFileSync('/home/hatch/workspace/android/checklist-cloud/firestore.rules', 'utf8');
  var a268ver = html.includes('Versión 2.5.18') && html.includes('Versión: 2.5.18') && !html.includes('2.5.17');
  var a268bundle = md5bundle268 === 'BUNDLE_MD5';
  var a268fb = fb268.includes('asignarFolioAcuse') && fb268.includes("doc(db, 'config', 'foliosAcuse')") &&
    fb268.includes('crearAcuse(datos, creadoPorNombre, folio)') && fb268.includes('crearCarta(datos, creadoPorNombre, folio)') &&
    fb268.includes('runTransaction');
  var a268rules = rules268.includes('match /config/foliosAcuse') && rules268.includes('match /config/foliosCarta') &&
    rules268.includes('match /acuses/{id}') && rules268.includes('match /cartas/{id}');
  console.log('268A) versión 2.5.18:', a268ver, '| bundle nuevo (9d4f0a81…):', a268bundle, '| firebase.js con folio Acuse:', a268fb, '| reglas con foliosAcuse:', a268rules);
  // 268B: PDF de la Carta con CAJAS CON BORDE VISIBLE en los campos:
  // rectángulos con borde ('x y w h re S') en las posiciones de la
  // captura (izq. x=146 w=184; der. x=410 w=166, Ip de 44 pt y Jefe de
  // 22 pt; Observaciones x=36 w=540 h=22), divisores verticales en la
  // tabla Exclusivo (líneas x=153/270/423), verde #9BBB59, y el campo
  // «Área: Jefe Directo:» con los dos valores del formulario.
  var c268b = { id: 'CARTA-268B', folio: '00043', creadoEn: Date.now(), creadoPor: 'u1', creadoPorNombre: 'Test User', datos: { fecha: '2026-09-01', nombre: 'Juan Pérez López', colaborador: '12345', sucursal: 'Rosa Blanca', puesto: 'Técnico', area: 'Sistemas', jefe: 'María García', ip: '192.168.1.50', observaciones: 'Sin observaciones', equipos: [{ modelo: 'Latitude 5420', marca: 'Dell', serie: 'ABC123', concepto: 'Laptop' }] } };
  var pdf268b = await pdfStrOf268(buildPdfCarta(c268b));
  var rows268b = pdfTextRows(pdf268b);
  var txt268b = rows268b.map(function (r) { return r.t; }).join(' ');
  function rects268(pdf) { var out = [], re = /([\\d.]+) ([\\d.]+) ([\\d.]+) ([\\d.]+) re S/g, m; while ((m = re.exec(pdf))) out.push([Number(m[1]), Number(m[2]), Number(m[3]), Number(m[4])]); return out; }
  function hasRect268(rs, x, w, h) { return rs.some(function (r) { return r[0] === x && r[2] === w && r[3] === h; }); }
  var rs268b = rects268(pdf268b);
  var b268 = (pdf268b.match(/\\/Type \\/Page[^s]/g) || []).length === 2 &&
    hasRect268(rs268b, 146, 184, 22) && hasRect268(rs268b, 410, 166, 44) && hasRect268(rs268b, 410, 166, 22) && hasRect268(rs268b, 36, 540, 22) &&
    /153\\.0 [\\d.]+ m 153\\.0 [\\d.]+ l S/.test(pdf268b) && /423\\.0 [\\d.]+ m 423\\.0 [\\d.]+ l S/.test(pdf268b) &&
    pdf268b.indexOf('0.608 0.733 0.349 rg') !== -1 &&
    txt268b.indexOf('Nombre del colaborador:') !== -1 && txt268b.indexOf('Rosa Blanca') !== -1 &&
    txt268b.indexOf('Área: Jefe Directo:') !== -1 && txt268b.indexOf('Sistemas') !== -1 && txt268b.indexOf('María García') !== -1 &&
    txt268b.indexOf('FOLIO: 00043') !== -1;
  console.log('268B) PDF carta: cajas con borde en los campos, divisores Exclusivo, Área: Jefe Directo:', b268);
  // 268C: folio AL ABRIR en la Carta (local): al entrar a la vista el
  // campo ya trae folio; Limpiar asigna el siguiente; guardar usa ese
  // folio (no asigna otro); el PDF del formulario lleva ese folio.
  doLogin('usuario');
  localStorage.setItem(CARTA_FOLIO_LOCAL_KEY, '1');
  cartaEditId = null;
  document.getElementById('fCa-folio').value = '';
  showVista('carta');
  var c268open = document.getElementById('fCa-folio').value === '00001';
  cartaLimpiarForm();
  var c268limpiar = document.getElementById('fCa-folio').value === '00002';
  document.getElementById('fCa-nombre').value = 'Juan Pérez López';
  cartaEqFilas = [{ modelo: 'Latitude 5420', marca: 'Dell', serie: 'ABC123', concepto: 'Laptop' }];
  var ok268c = await cartaGuardar();
  var saved268c = cartas[cartas.length - 1];
  var c268save = ok268c === true && !!saved268c && saved268c.folio === '00002' && document.getElementById('fCa-folio').value === '00002';
  var pdf268c = await pdfStrOf268(buildPdfCarta({ id: saved268c.id, folio: document.getElementById('fCa-folio').value, datos: cartaLeerForm() }));
  var c268pdf = pdf268c.indexOf('FOLIO: 00002') !== -1;
  console.log('268C) carta: folio al abrir 00001:', c268open, '| Limpiar asigna 00002:', c268limpiar, '| guardar usa 00002:', c268save, '| PDF del formulario con 00002:', c268pdf);
  // 268D: folio AL ABRIR en el Acuse (local) y secuencias
  // INDEPENDIENTES: el acuse empieza en 00001 aunque la carta ya
  // consumió los suyos; la tarjeta muestra el folio y el PDF lo lleva
  // arriba a la derecha, junto a la fecha.
  localStorage.setItem(ACUSE_FOLIO_LOCAL_KEY, '1');
  acuseEditId = null;
  document.getElementById('fAc-folio').value = '';
  showVista('acuse');
  var d268open = document.getElementById('fAc-folio').value === '00001';
  document.getElementById('fAc-para').value = 'Beatriz Garduño Dominguez RH - Revolución';
  document.getElementById('fAc-de').value = 'SISTEMAS';
  var ok268d = await acuseGuardar();
  var saved268d = acuses[acuses.length - 1];
  var d268save = ok268d === true && !!saved268d && saved268d.folio === '00001' &&
    document.getElementById('acuseList').innerHTML.indexOf('Folio 00001') !== -1;
  var pdf268d = await pdfStrOf268(buildPdfAcuse(saved268d));
  var d268pdf = pdf268d.indexOf('FOLIO: 00001') !== -1;
  acuseLimpiarForm();
  var d268limpiar = document.getElementById('fAc-folio').value === '00002';
  console.log('268D) acuse: folio al abrir 00001:', d268open, '| guardar usa 00001 y tarjeta lo muestra:', d268save, '| PDF con FOLIO: 00001:', d268pdf, '| Limpiar asigna 00002:', d268limpiar);
  // 268E: folio consumido si se abandona sin guardar (hueco): abrir
  // asigna 00003, se sale sin guardar, el siguiente es 00004.
  acuseLimpiarForm();
  var e268abandona = document.getElementById('fAc-folio').value === '00003';
  acuseLimpiarForm();
  var e268hueco = document.getElementById('fAc-folio').value === '00004';
  console.log('268E) folio abandonado 00003 queda consumido, siguiente 00004:', e268abandona && e268hueco);
  // 268F: Acuse PDF sigue en 1 página con FOLIO y tabla RECIBE con
  // bordes (celda gris x=57 w=76 h=54 y celda blanca x=133 w=441).
  var a268f = { id: 'ac1', creadoEn: Date.now(), creadoPor: 'u1', creadoPorNombre: 'Test User', folio: '00007', datos: { fecha: '2026-09-01', para: 'Beatriz Garduño Dominguez RH - Revolución', de: 'SISTEMAS', anexo: 'Documentacion' } };
  var pdf268f = await pdfStrOf268(buildPdfAcuse(a268f));
  var rs268f = rects268(pdf268f);
  var f268 = (pdf268f.match(/\\/Type \\/Page[^s]/g) || []).length === 1 &&
    pdf268f.indexOf('FOLIO: 00007') !== -1 && pdf268f.indexOf('RECIBE:') !== -1 &&
    hasRect268(rs268f, 57, 76, 54) && hasRect268(rs268f, 133, 441, 54);
  console.log('268F) acuse: 1 página, FOLIO: 00007, RECIBE con bordes:', f268);

"""

serie268 = serie268.replace('BUNDLE_MD5', BUNDLE_MD5)
serie268 = serie268.replace('PAGE_RE', chr(92) + '/Type ' + chr(92) + '/Page[^s]/g')
assert 'PAGE_RE' not in serie268 and 'BUNDLE_MD5' not in serie268
assert s.count('  process.exit(0);') == 1, 'ancla process.exit no única'
s = s.replace('  process.exit(0);', serie268 + '  process.exit(0);', 1)

open(P, 'w', encoding='utf-8').write(s)
print('test20268.js escrito:', len(s), 'bytes')
