# Parche de pruebas 2.5.20: test20269.js -> test20270.js.
# 1) Extrae el <script> actual de www/index.html a
# tests/checklist20270.js. 2) Copia test20269.js a test20270.js y
# actualiza la versión (2.5.19 -> 2.5.20, 2.5.18 -> 2.5.19, n269 ->
# n270, mailto 269 -> 270). 3) El bundle SÍ cambia en 2.5.20
# (firebase.js: crearAcuse ya no asigna folio): md5 nuevo
# c4fb1cce63c0d71ae96b1aee931ee740; las etiquetas de 265A/266A/267A/
# 268A/269A pasan de «bundle sin cambio» a «bundle nuevo 2.5.20».
# 4) Actualiza 268D/268E/268F y 269E al comportamiento nuevo (el
# Acuse YA NO lleva folio) y refuerza 266D/267B (PDF del Acuse sin
# ninguna línea FOLIO). 5) Agrega la serie 270 (6 casos): versión y
# bundle nuevo + crearAcuse sin folio; dedupe sin duplicados
# (merge mismo id / mismo folio otro id / lista con copias);
# doble Guardar no duplica (carta y acuse); Acuse sin folio de
# extremo a extremo + Carta con folio; botón Imprimir (formulario:
# iframe + print); Imprimir desde la tarjeta + reintento sin
# duplicar.
# Uso: python3 patch_20270_test.py (corre desde tests/)
import os
import shutil

BASE = '/home/hatch/workspace/android/checklist-cloud'
TESTS = os.path.join(BASE, 'tests')
SRC = os.path.join(TESTS, 'test20269.js')
P = os.path.join(TESTS, 'test20270.js')
BUNDLE_MD5 = 'c4fb1cce63c0d71ae96b1aee931ee740'
BUNDLE_MD5_SHORT = 'c4fb1cce'

# --- Extraer el <script> actual de www/index.html.
html = open(os.path.join(BASE, 'www/index.html'), encoding='utf-8').read()
i = html.index('<script>', html.index('firebase-config'))
j = html.index('</script>', i)
open(os.path.join(TESTS, 'checklist20270.js'), 'w', encoding='utf-8').write(html[i + len('<script>'):j])
print('checklist20270.js extraido:', j - i - len('<script>'), 'bytes')

shutil.copyfile(SRC, P)
s = open(P, encoding='utf-8').read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'NO ENCONTRADO x%d (esperado %d): %r' % (c, n, old[:120])
    s = s.replace(old, new)


def repall(old, new):
    global s
    c = s.count(old)
    print('repall %r -> %r: %d ocurrencias' % (old[:60], new[:60], c))
    s = s.replace(old, new)


# --- SRC y versión 2.5.20.
rep("const SRC = fs.readFileSync(__dirname + '/checklist20269.js', 'utf8');",
    "const SRC = fs.readFileSync(__dirname + '/checklist20270.js', 'utf8');")
repall('2.5.19', '2.5.20')
repall('2.5.18', '2.5.19')
repall('n269', 'n270')
repall('Soporte 269', 'Soporte 270')
repall('mailto 269', 'mailto 270')
BS = chr(92)
rep("var n270 = (html.match(/2" + BS + ".5" + BS + ".19/g) || []).length;",
    "var n270 = (html.match(/2" + BS + ".5" + BS + ".20/g) || []).length;")

# --- Bundle NUEVO en 2.5.20 (firebase.js cambió).
repall('9d4f0a81f3108d0f92f50f08fc48c752', BUNDLE_MD5)
repall('9d4f0a81…', BUNDLE_MD5_SHORT + '…')
repall('bundle sin cambio (' + BUNDLE_MD5_SHORT + '…)', 'bundle nuevo 2.5.20 (' + BUNDLE_MD5_SHORT + '…)')
repall('bundle SIN cambio 2.5.19', 'bundle NUEVO 2.5.20')
rep("  // (firebase.js no cambió en 2.5.20: md5 c4fb1cce…) y reglas con",
    "  // (firebase.js CAMBIÓ en 2.5.20: crearAcuse ya no asigna folio;\n  // md5 c4fb1cce…) y reglas con")
rep("  // 266A: versión 2.5.20 en los 2 sitios, mailto 270, bundle sin cambio 2.5.19",
    "  // 266A: versión 2.5.20 en los 2 sitios, mailto 270, bundle NUEVO 2.5.20")
rep("  // 268A: versión 2.5.20 en los 2 sitios, bundle SIN cambio en",
    "  // 268A: versión 2.5.20 en los 2 sitios, bundle NUEVO 2.5.20 en")
rep("  // 269A: versión 2.5.20 en los 2 sitios, bundle SIN cambio",
    "  // 269A: versión 2.5.20 en los 2 sitios, bundle NUEVO 2.5.20")

# --- 266D y 267B: el PDF del Acuse NO lleva ninguna línea FOLIO.
rep("    pdf266d.indexOf('Documentacion') !== -1 && pdf266d.indexOf('RECIBE:') !== -1 && pdf266d.indexOf('Nombre:') !== -1 &&\n    pdf266d.indexOf('Firma:') !== -1;",
    "    pdf266d.indexOf('Documentacion') !== -1 && pdf266d.indexOf('RECIBE:') !== -1 && pdf266d.indexOf('Nombre:') !== -1 &&\n    pdf266d.indexOf('Firma:') !== -1 && pdf266d.indexOf('FOLIO:') === -1;")
rep("    pdf267b.indexOf('ACUSE DE RECIBO') !== -1 && pdf267b.indexOf('RECIBE:') !== -1 &&\n    pdf267b.indexOf('Nombre:') !== -1 && pdf267b.indexOf('Fecha:') !== -1 && pdf267b.indexOf('Firma:') !== -1;",
    "    pdf267b.indexOf('ACUSE DE RECIBO') !== -1 && pdf267b.indexOf('RECIBE:') !== -1 &&\n    pdf267b.indexOf('Nombre:') !== -1 && pdf267b.indexOf('Fecha:') !== -1 && pdf267b.indexOf('Firma:') !== -1 &&\n    pdf267b.indexOf('FOLIO:') === -1;")

# --- 268D (ACTUALIZADO en 2.5.20): el Acuse YA NO lleva folio.
old268d = """  // 268D: folio AL ABRIR en el Acuse (local) y secuencias
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
  console.log('268D) acuse: folio al abrir 00001:', d268open, '| guardar usa 00001 y tarjeta lo muestra:', d268save, '| PDF con FOLIO: 00001:', d268pdf, '| Limpiar asigna 00002:', d268limpiar);"""
new268d = """  // 268D (ACTUALIZADO en 2.5.20): el Acuse YA NO lleva folio en
  // ningún lado: sin campo en el formulario, sin asignar al abrir
  // (no se consume ningún número), la tarjeta no lo muestra, el PDF
  // no lleva la línea FOLIO y el texto para compartir tampoco.
  acuseEditId = null;
  showVista('acuse');
  var d268nofield = html.indexOf('id="fAc-folio"') === -1 && html.indexOf('acuseAsignarFolio') === -1 &&
    html.indexOf('ACUSE_FOLIO_LOCAL_KEY') === -1 && localStorage.getItem('checklist-soporte-folios-acuse-local-v1') === null;
  document.getElementById('fAc-para').value = 'Beatriz Garduño Dominguez RH - Revolución';
  document.getElementById('fAc-de').value = 'SISTEMAS';
  var ok268d = await acuseGuardar();
  var saved268d = acuses[acuses.length - 1];
  var d268save = ok268d === true && !!saved268d && saved268d.folio === undefined &&
    document.getElementById('acuseList').innerHTML.indexOf('Folio') === -1 &&
    acuseTexto(saved268d).indexOf('Folio') === -1 &&
    toastTxt().indexOf('Acuse guardado.') !== -1 && toastTxt().indexOf('folio') === -1;
  var pdf268d = await pdfStrOf268(buildPdfAcuse(saved268d));
  var d268pdf = pdf268d.indexOf('FOLIO:') === -1;
  acuseLimpiarForm();
  var d268limpiar = document.getElementById('fAc-para').value === '' && document.getElementById('fAc-de').value === '';
  console.log('268D) acuse SIN folio: sin campo ni asignación al abrir:', d268nofield, '| guardar sin folio y tarjeta/texto sin folio:', d268save, '| PDF sin FOLIO:', d268pdf, '| Limpiar vacía el formulario:', d268limpiar);"""
rep(old268d, new268d)

# --- 268E (ACTUALIZADO en 2.5.20): abrir el Acuse no consume folios.
old268e = """  // 268E: folio consumido si se abandona sin guardar (hueco): abrir
  // asigna 00003, se sale sin guardar, el siguiente es 00004.
  acuseLimpiarForm();
  var e268abandona = document.getElementById('fAc-folio').value === '00003';
  acuseLimpiarForm();
  var e268hueco = document.getElementById('fAc-folio').value === '00004';
  console.log('268E) folio abandonado 00003 queda consumido, siguiente 00004:', e268abandona && e268hueco);"""
new268e = """  // 268E (ACTUALIZADO en 2.5.20): abrir el Acuse varias veces NO
  // consume folios: ya no existe contador de acuse (el de la Carta
  // sigue intacto e independiente).
  showVista('acuse');
  var e268a = localStorage.getItem('checklist-soporte-folios-acuse-local-v1') === null;
  showVista('acuse');
  var e268b = localStorage.getItem('checklist-soporte-folios-acuse-local-v1') === null;
  console.log('268E) abrir el Acuse no consume folio (sin contador de acuse):', e268a, '| segunda apertura tampoco:', e268b);"""
rep(old268e, new268e)

# --- 268F (ACTUALIZADO en 2.5.20): PDF del Acuse sin FOLIO aunque el
# documento traiga un folio viejo (00007, de 2.5.18/2.5.19).
old268f = """  // 268F: Acuse PDF sigue en 1 página con FOLIO y tabla RECIBE con
  // bordes (celda gris x=57 w=76 h=54 y celda blanca x=133 w=441).
  var a268f = { id: 'ac1', creadoEn: Date.now(), creadoPor: 'u1', creadoPorNombre: 'Test User', folio: '00007', datos: { fecha: '2026-09-01', para: 'Beatriz Garduño Dominguez RH - Revolución', de: 'SISTEMAS', anexo: 'Documentacion' } };
  var pdf268f = await pdfStrOf268(buildPdfAcuse(a268f));
  var rs268f = rects268(pdf268f);
  var f268 = (pdf268f.match(/\\/Type \\/Page[^s]/g) || []).length === 1 &&
    pdf268f.indexOf('FOLIO: 00007') !== -1 && pdf268f.indexOf('RECIBE:') !== -1 &&
    hasRect268(rs268f, 57, 76, 54) && hasRect268(rs268f, 133, 441, 54);
  console.log('268F) acuse: 1 página, FOLIO: 00007, RECIBE con bordes:', f268);"""
new268f = """  // 268F (ACTUALIZADO en 2.5.20): Acuse PDF sigue en 1 página con
  // tabla RECIBE con bordes (celda gris x=57 w=76 h=54 y celda blanca
  // x=133 w=441), pero SIN ninguna línea FOLIO aunque el documento
  // traiga un folio viejo (00007, de 2.5.18/2.5.19).
  var a268f = { id: 'ac1', creadoEn: Date.now(), creadoPor: 'u1', creadoPorNombre: 'Test User', folio: '00007', datos: { fecha: '2026-09-01', para: 'Beatriz Garduño Dominguez RH - Revolución', de: 'SISTEMAS', anexo: 'Documentacion' } };
  var pdf268f = await pdfStrOf268(buildPdfAcuse(a268f));
  var rs268f = rects268(pdf268f);
  var f268 = (pdf268f.match(/\\/Type \\/Page[^s]/g) || []).length === 1 &&
    pdf268f.indexOf('FOLIO:') === -1 && pdf268f.indexOf('00007') === -1 && pdf268f.indexOf('RECIBE:') !== -1 &&
    hasRect268(rs268f, 57, 76, 54) && hasRect268(rs268f, 133, 441, 54);
  console.log('268F) acuse: 1 página, SIN FOLIO ni 00007 aunque el documento lo traiga, RECIBE con bordes:', f268);"""
rep(old268f, new268f)

# --- 269E (ACTUALIZADO en 2.5.20): acuse sin red, SIN folio.
old269e = """  // 269E: el acuse que falla SIN RED queda en el teléfono con el
  // aviso de sin conexión, y se reintenta desde el botón de su
  // tarjeta.
  localStorage.setItem(ACUSE_FOLIO_LOCAL_KEY, '1');
  acuseEditId = null;
  document.getElementById('fAc-folio').value = '';
  global.Cloud.crearAcuse = async function () { var e = new Error('offline'); e.code = 'unavailable'; throw e; };"""
new269e = """  // 269E (ACTUALIZADO en 2.5.20): el acuse que falla SIN RED queda
  // en el teléfono SIN folio, con el aviso de sin conexión, y se
  // reintenta desde el botón de su tarjeta (el reintento sube el
  // documento sin folio y sin el marcador pendiente).
  acuseEditId = null;
  global.Cloud.crearAcuse = async function () { var e = new Error('offline'); e.code = 'unavailable'; throw e; };"""
rep(old269e, new269e)
rep("""  var e269a = ok269e === true && acuses.length === nAcuses269e + 1 && !!saved269e &&
    saved269e.folio === '00001' && saved269e.pendienteSync === true &&""",
    """  var e269a = ok269e === true && acuses.length === nAcuses269e + 1 && !!saved269e &&
    saved269e.folio === undefined && saved269e.pendienteSync === true &&""")
rep("""  var e269b = up269e.length === 1 && up269e[0].id === saved269e.id && up269e[0].folio === '00001' && up269e[0].pendienteSync === undefined &&""",
    """  var e269b = up269e.length === 1 && up269e[0].id === saved269e.id && up269e[0].folio === undefined && up269e[0].pendienteSync === undefined &&""")
rep("  console.log('269E) acuse sin red: queda pendiente con aviso de sin conexión:', e269a, '| botón Reintentar lo sincroniza:', e269b);",
    "  console.log('269E) acuse sin red: queda pendiente sin folio, aviso de sin conexión:', e269a, '| botón Reintentar lo sincroniza sin folio:', e269b);")

# --- Serie 270 (nueva), antes de process.exit(0).
serie270 = '''
  // 270: serie nueva — 2.5.20: sin duplicados en Cartas/Acuses
  // guardados; Acuse SIN folio en ningún lado; botón Imprimir en
  // Carta y Acuse (formulario y lista).
  CLOUD_ENABLED = false;
  // 270A: versión 2.5.20 en los 2 sitios, bundle NUEVO 2.5.20
  // (firebase.js cambió: crearAcuse ya no asigna folio) y reglas con
  // foliosAcuse intactas (no se tocaron).
  var crypto270 = require('crypto');
  var bundle270 = fs.readFileSync('/home/hatch/workspace/android/checklist-cloud/www/cloud/firebase.bundle.js');
  var md5bundle270 = crypto270.createHash('md5').update(bundle270).digest('hex');
  var fb270 = fs.readFileSync('/home/hatch/workspace/android/checklist-cloud/www/cloud/firebase.js', 'utf8');
  var rules270 = fs.readFileSync('/home/hatch/workspace/android/checklist-cloud/firestore.rules', 'utf8');
  var a270ver = html.includes('Versión 2.5.20') && html.includes('Versión: 2.5.20') && !html.includes('2.5.19');
  var a270bundle = md5bundle270 === 'c4fb1cce63c0d71ae96b1aee931ee740';
  var a270fb = fb270.indexOf('folio || (await asignarFolioAcuse())') === -1 && fb270.indexOf('if (folio) data.folio = folio') !== -1 &&
    fb270.includes('asignarFolioCarta') && fb270.includes('crearCarta(datos, creadoPorNombre, folio)');
  var a270rules = rules270.includes('match /config/foliosAcuse') && rules270.includes('match /config/foliosCarta') &&
    rules270.includes('match /acuses/{id}') && rules270.includes('match /cartas/{id}');
  console.log('270A) versión 2.5.20:', a270ver, '| bundle nuevo 2.5.20 (c4fb1cce…):', a270bundle, '| crearAcuse ya no asigna folio:', a270fb, '| reglas con foliosAcuse intactas:', a270rules);
  // 270B: UN documento = UNA entrada. (a) La suscripción trae la
  // carta con el mismo id que la copia local: el merge deja UNA.
  // (b) Mismo folio con otro id (respaldo tras crear* fallido
  // después de escribir en la nube): el merge deja UNA (gana la de
  // la nube, sin pendiente). (c) La lista renderiza UNA tarjeta
  // aunque el array traiga la carta tres veces; igual para acuses.
  var c270nube = { id: 'C-270B', folio: '00050', creadoEn: Date.now(), creadoPor: 'u1', creadoPorNombre: 'Test User', datos: { fecha: '2026-09-01', nombre: 'Juan Pérez López', equipos: [{ modelo: 'X1', marca: 'Lenovo', serie: 'ZZ9', concepto: 'Laptop' }] } };
  var c270local = Object.assign({}, c270nube, { pendienteSync: true });
  cartas = [c270local];
  var m270a = mergeCartaWithLocal([c270nube]);
  var b270a = m270a.length === 1 && m270a[0].id === 'C-270B' && m270a[0].pendienteSync !== true;
  var c270otroId = Object.assign({}, c270nube, { id: 'C-270B-LOCAL', pendienteSync: true });
  cartas = [c270otroId];
  var m270b = mergeCartaWithLocal([c270nube]);
  var b270b = m270b.length === 1 && m270b[0].id === 'C-270B';
  cartas = [c270nube, c270local, c270otroId];
  renderCartaList();
  var b270c = (document.getElementById('cartaList').innerHTML.match(/data-carta-open/g) || []).length === 1;
  var a270nube = { id: 'A-270B', creadoEn: Date.now(), creadoPor: 'u1', creadoPorNombre: 'Test User', datos: { fecha: '2026-09-01', para: 'Alguien', de: 'SISTEMAS', anexo: '' } };
  var a270local = Object.assign({}, a270nube, { pendienteSync: true });
  acuses = [a270local];
  var m270d = mergeAcuseWithLocal([a270nube]);
  var b270d = m270d.length === 1 && m270d[0].id === 'A-270B' && m270d[0].pendienteSync !== true;
  acuses = [a270nube, a270local];
  renderAcuseList();
  var b270e = (document.getElementById('acuseList').innerHTML.match(/data-acuse-open/g) || []).length === 1;
  console.log('270B) merge mismo id deja 1:', b270a, '| mismo folio otro id deja 1 (gana nube):', b270b, '| lista carta con 3 copias renderiza 1:', b270c, '| merge acuse mismo id deja 1:', b270d, '| lista acuse con 2 copias renderiza 1:', b270e);
  // 270C: doble toque en Guardar NO duplica: dos cartaGuardar()
  // concurrentes llaman a crearCarta UNA sola vez y dejan UNA carta;
  // igual para el Acuse con crearAcuse (y sin pasarle folio).
  CLOUD_ENABLED = true;
  doLogin('usuario');
  localStorage.setItem(CARTA_FOLIO_LOCAL_KEY, '1');
  cartaEditId = null;
  document.getElementById('fCa-folio').value = '';
  showVista('carta');
  document.getElementById('fCa-nombre').value = 'Juan Pérez López';
  cartaEqFilas = [{ modelo: 'Latitude 5420', marca: 'Dell', serie: 'ABC123', concepto: 'Laptop' }];
  var crear270c = [];
  global.Cloud.crearCarta = async function (datos, nombre, folio) { crear270c.push(folio); await sleep(30); return { id: 'CARTA-270C', folio: folio || '00001' }; };
  cartas = dedupeCartas(cartas);
  var nCartas270c = cartas.length;
  var res270c = await Promise.all([cartaGuardar(), cartaGuardar()]);
  var c270d = crear270c.length === 1 && res270c[0] === true && res270c[1] === false && cartas.length === nCartas270c + 1 &&
    cartas.filter(function (x) { return x.id === 'CARTA-270C'; }).length === 1;
  var crear270a = [];
  global.Cloud.crearAcuse = async function (datos, nombre, folio) { crear270a.push([datos, nombre, folio]); await sleep(30); return 'ACUSE-270C'; };
  acuseEditId = null;
  showVista('acuse');
  document.getElementById('fAc-para').value = 'Beatriz Garduño Dominguez RH - Revolución';
  document.getElementById('fAc-de').value = 'SISTEMAS';
  acuses = dedupeAcuses(acuses);
  var nAcuses270c = acuses.length;
  var res270a = await Promise.all([acuseGuardar(), acuseGuardar()]);
  var saved270a = acuses.find(function (x) { return x.id === 'ACUSE-270C'; });
  var c270e = crear270a.length === 1 && res270a[0] === true && res270a[1] === false && acuses.length === nAcuses270c + 1 &&
    !!saved270a && saved270a.folio === undefined && crear270a[0][2] === undefined;
  CLOUD_ENABLED = false;
  console.log('270C) doble Guardar carta: crearCarta 1 vez, 1 carta:', c270d, '| doble Guardar acuse: crearAcuse 1 vez, 1 acuse sin folio:', c270e);
  // 270D: Acuse SIN folio de extremo a extremo: sin campo en el
  // formulario, abrir la vista no asigna ni consume nada, el PDF no
  // lleva FOLIO, la tarjeta y el texto tampoco; la Carta SÍ conserva
  // su folio en formulario, PDF, tarjeta y texto.
  var d270html = html.indexOf('id="fAc-folio"') === -1 && html.indexOf('acuseAsignarFolio') === -1 &&
    html.indexOf('acuseFolioLocal') === -1 && html.indexOf('ACUSE_FOLIO_LOCAL_KEY') === -1;
  var pdf270ac = await pdfStrOf268(buildPdfAcuse({ id: 'ac270', creadoEn: Date.now(), creadoPor: 'u1', creadoPorNombre: 'Test User', datos: { fecha: '2026-09-01', para: 'Beatriz Garduño Dominguez RH - Revolución', de: 'SISTEMAS', anexo: 'Documentacion' } }));
  var d270pdf = pdf270ac.indexOf('FOLIO:') === -1 && pdf270ac.indexOf('RECIBE:') !== -1;
  var card270ac = acuseCardHtml({ id: 'ac270', creadoEn: Date.now(), creadoPor: 'u1', creadoPorNombre: 'Test User', datos: { fecha: '2026-09-01', para: 'Beatriz Garduño Dominguez RH - Revolución', de: 'SISTEMAS', anexo: '' } });
  var d270card = card270ac.indexOf('Folio') === -1 && card270ac.indexOf('Beatriz Gardu') !== -1 &&
    acuseTexto({ datos: { fecha: '2026-09-01', para: 'Beatriz Garduño Dominguez RH - Revolución', de: 'SISTEMAS', anexo: '' } }).indexOf('Folio') === -1;
  localStorage.setItem(CARTA_FOLIO_LOCAL_KEY, '1');
  cartaEditId = null;
  document.getElementById('fCa-folio').value = '';
  showVista('carta');
  var d270carta = document.getElementById('fCa-folio').value === '00001' &&
    html.indexOf('id="fCa-folio"') !== -1 && html.indexOf('cartaAsignarFolio') !== -1;
  var pdf270ca = await pdfStrOf268(buildPdfCarta({ id: 'ca270', folio: '00001', creadoEn: Date.now(), creadoPor: 'u1', creadoPorNombre: 'Test User', datos: { fecha: '2026-09-01', nombre: 'Juan Pérez López', equipos: [{ modelo: 'X1', marca: 'Lenovo', serie: 'ZZ9', concepto: 'Laptop' }] } }));
  var d270cartaPdf = pdf270ca.indexOf('FOLIO: 00001') !== -1 &&
    cartaTexto({ folio: '00001', datos: { nombre: 'Juan Pérez López' } }).indexOf('folio 00001') !== -1 &&
    cartaCardHtml({ id: 'ca270', folio: '00001', creadoEn: Date.now(), creadoPor: 'u1', creadoPorNombre: 'Test User', datos: { nombre: 'Juan Pérez López', equipos: [{ modelo: 'X1', marca: 'Lenovo', serie: 'ZZ9', concepto: 'Laptop' }] } }).indexOf('Folio 00001') !== -1;
  console.log('270D) acuse: sin campo ni asignación en el HTML:', d270html, '| PDF sin FOLIO:', d270pdf, '| tarjeta y texto sin Folio:', d270card, '| carta conserva folio al abrir:', d270carta, '| PDF/tarjeta/texto de carta con folio:', d270cartaPdf);
  // 270E: botón Imprimir en Carta y Acuse, en el formulario: abre
  // el PDF en un iframe oculto y llama a print() de su ventana
  // (diálogo de impresión del sistema).
  var e270btns = html.indexOf('id="btnAcuseImprimir"') !== -1 && html.indexOf('id="btnCartaImprimir"') !== -1 &&
    html.indexOf('🖨️ Imprimir') !== -1 && html.indexOf('data-acuse-print') !== -1 && html.indexOf('data-carta-print') !== -1 &&
    html.indexOf('imprimirPdfDoc') !== -1 && html.indexOf('contentWindow.print()') !== -1;
  var e270wired = (document.getElementById('btnAcuseImprimir')._h.click || []).length === 1 &&
    (document.getElementById('btnCartaImprimir')._h.click || []).length === 1;
  var printed270 = [];
  var origCreate270 = document.createElement;
  var iframe270 = null;
  document.createElement = function (tag) {
    if (tag === 'iframe') {
      iframe270 = { tagName: 'IFRAME', style: {}, src: '', parentNode: null,
        contentWindow: { focus: function () {}, print: function () { printed270.push('print'); } } };
      return iframe270;
    }
    return origCreate270(tag);
  };
  CLOUD_ENABLED = false;
  doLogin('usuario');
  showVista('acuse');
  document.getElementById('fAc-para').value = 'Beatriz Garduño Dominguez RH - Revolución';
  document.getElementById('fAc-de').value = 'SISTEMAS';
  document.getElementById('btnAcuseImprimir')._h.click[0]();
  var e270a = !!iframe270 && iframe270.src === 'blob:x';
  if (iframe270 && iframe270.onload) iframe270.onload();
  var e270b = printed270.length === 1;
  showVista('carta');
  cartaLimpiarForm();
  document.getElementById('fCa-nombre').value = 'Juan Pérez López';
  cartaEqFilas = [{ modelo: 'Latitude 5420', marca: 'Dell', serie: 'ABC123', concepto: 'Laptop' }];
  iframe270 = null;
  document.getElementById('btnCartaImprimir')._h.click[0]();
  var e270c = !!iframe270 && iframe270.src === 'blob:x';
  if (iframe270 && iframe270.onload) iframe270.onload();
  var e270d = printed270.length === 2;
  document.createElement = origCreate270;
  console.log('270E) botones Imprimir en HTML (formulario y lista):', e270btns, '| cableados:', e270wired, '| imprimir acuse abre iframe del PDF:', e270a, '| y llama a print():', e270b, '| imprimir carta abre iframe del PDF:', e270c, '| y llama a print():', e270d);
  // 270F: Imprimir desde la tarjeta guardada (Carta y Acuse) llama
  // a print() con el PDF de ese documento; el reintento de un
  // pendiente NO duplica la entrada aunque la nube ya lo traiga.
  var printed270f = [];
  var origCreate270f = document.createElement;
  var iframe270f = null;
  document.createElement = function (tag) {
    if (tag === 'iframe') {
      iframe270f = { tagName: 'IFRAME', style: {}, src: '', parentNode: null,
        contentWindow: { focus: function () {}, print: function () { printed270f.push('print'); } } };
      return iframe270f;
    }
    return origCreate270f(tag);
  };
  var c270f = { id: 'CARTA-270F', folio: '00077', creadoEn: Date.now(), creadoPor: 'u1', creadoPorNombre: 'Test User', datos: { fecha: '2026-09-01', nombre: 'Juan Pérez López', equipos: [{ modelo: 'X1', marca: 'Lenovo', serie: 'ZZ9', concepto: 'Laptop' }] } };
  cartas.push(c270f);
  cartaListClick({ target: fakeListTarget266('data-carta-print', 'CARTA-270F') });
  var f270a = !!iframe270f && iframe270f.src === 'blob:x';
  if (iframe270f && iframe270f.onload) iframe270f.onload();
  var f270b = printed270f.length === 1;
  var a270f = { id: 'ACUSE-270F', creadoEn: Date.now(), creadoPor: 'u1', creadoPorNombre: 'Test User', datos: { fecha: '2026-09-01', para: 'Beatriz Garduño Dominguez RH - Revolución', de: 'SISTEMAS', anexo: '' } };
  acuses.push(a270f);
  iframe270f = null;
  acuseListClick({ target: fakeListTarget266('data-acuse-print', 'ACUSE-270F') });
  var f270c = !!iframe270f && iframe270f.src === 'blob:x';
  if (iframe270f && iframe270f.onload) iframe270f.onload();
  var f270d = printed270f.length === 2;
  document.createElement = origCreate270f;
  var pend270f = { id: 'pend270f', folio: '00078', creadoEn: Date.now(), creadoPor: 'u1', creadoPorNombre: 'Test User', datos: { fecha: '2026-09-01', nombre: 'Ana López', equipos: [{ modelo: 'X1', marca: 'Lenovo', serie: 'ZZ9', concepto: 'Laptop' }] }, pendienteSync: true };
  cartas.push(pend270f);
  CLOUD_ENABLED = true;
  doLogin('usuario');
  global.Cloud.upsertCarta = async function (rec) {};
  var ok270f = await cartaReintentarSync('pend270f');
  cartas = [pend270f];
  var m270f = mergeCartaWithLocal([Object.assign({}, pend270f)]);
  var f270e = ok270f === true && pend270f.pendienteSync === false && m270f.length === 1;
  console.log('270F) imprimir carta desde tarjeta abre iframe:', f270a, '| y llama a print():', f270b, '| imprimir acuse desde tarjeta abre iframe:', f270c, '| y llama a print():', f270d, '| reintento con copia en nube deja 1:', f270e);
'''
rep('  process.exit(0);', serie270 + '\n  process.exit(0);')

open(P, 'w', encoding='utf-8').write(s)
print('test20270.js escrito')
