# Parche tests 2.5.1: actualiza AM0/AP0/AR0/BA0 a 2.5.1 y añade la serie BB.
import io

P = '/home/hatch/workspace/android/checklist-cloud/tests/test20251.js'
s = io.open(P, encoding='utf-8').read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'NO ENCONTRADO o repetido (%d): %r' % (c, old[:100])
    s = s.replace(old, new)

rep("// este archivo y cambiar checklist20240.js por el nuevo extraído.",
    "// este archivo y cambiar checklist20250.js por el nuevo extraído.")
rep("const SRC = fs.readFileSync(__dirname + '/checklist20250.js', 'utf8');",
    "const SRC = fs.readFileSync(__dirname + '/checklist20251.js', 'utf8');")
rep("console.log('AM0) versión 2.5.0:', html.includes('Versión 2.5.0'), '| sin 2.4.0:', !html.includes('Versión 2.4.0')",
    "console.log('AM0) versión 2.5.1:', html.includes('Versión 2.5.1'), '| sin 2.5.0:', !html.includes('Versión 2.5.0')")
rep("console.log('AP0) estáticos 2.5.0: versión:', html.includes('Versión 2.5.0') && !html.includes('Versión 2.4.0')",
    "console.log('AP0) estáticos 2.5.1: versión:', html.includes('Versión 2.5.1') && !html.includes('Versión 2.5.0')")
rep("  var n250 = (html.match(/2\\.5\\.0/g) || []).length;",
    "  var n251 = (html.match(/2\\.5\\.1/g) || []).length;")
rep("console.log('AR0) versión 2.5.0 visible:', html.includes('Versión 2.5.0') && html.includes('Versión: 2.5.0'), '| 0 de 2.4.0:', !html.includes('2.4.0'), '| ocurrencias 2.5.0:', n250 === 52);",
    "console.log('AR0) versión 2.5.1 visible:', html.includes('Versión 2.5.1') && html.includes('Versión: 2.5.1'), '| 0 de 2.5.0:', !html.includes('2.5.0'), '| ocurrencias 2.5.1:', n251 === 2);")
rep("  // BA: serie nueva 2.5.0 — Mantenimientos Preventivos.",
    "  // BA: serie 2.5.0 — Mantenimientos Preventivos (sin cambios en 2.5.1 salvo BB).")
rep("  var ba0html = html.includes('Versión 2.5.0') && html.includes('Versión: 2.5.0') && !html.includes('2.4.0');",
    "  var ba0html = html.includes('Versión 2.5.1') && html.includes('Versión: 2.5.1') && !html.includes('2.5.0');")
rep("var ba0form = ['fM-serie', 'fM-hostname', 'fM-modelo', 'fM-tecnico', 'fM-tipo', 'fM-area', 'fM-responsable', 'fM-titulo', 'fM-tipoFalla', 'fM-descEquipo', 'fM-observaciones', 'fM-obsDet', 'fM-whatsapp', 'fM-firmaCanvas', 'btnMantCrear', 'btnMantGuardar', 'btnMantCancelar', 'mantDetList', 'mantAdminFilter', 'mantOrderBox', 'btnMantWaLink', 'btnMantPdf', 'btnMantCompartir', 'btnMantCancelarOrden'].every(function (id) { return html.includes('id=\"' + id + '\"'); });",
    "var ba0form = ['fM-serie', 'fM-hostname', 'fM-modelo', 'fM-tecnico', 'fM-empresa', 'fM-tipo-sw', 'fM-tipo-hw', 'fM-anio', 'fM-area', 'fM-responsable', 'fM-titulo', 'fM-tipoFalla', 'fM-descEquipo', 'fM-observaciones', 'fM-obsDet', 'fM-whatsapp', 'fM-firmaCanvas', 'btnMantCrear', 'btnMantGuardar', 'btnMantCancelar', 'mantDetList', 'mantAdminFilter', 'mantOrderBox', 'btnMantWaLink', 'btnMantPdf', 'btnMantCompartir', 'btnMantCancelarOrden', 'btnMantEliminarOrden'].every(function (id) { return html.includes('id=\"' + id + '\"'); });")
rep("console.log('BA0) versión 2.5.0 sin 2.4.0:', ba0html,",
    "console.log('BA0) versión 2.5.1 sin 2.5.0:', ba0html,")
# mkMant: empresa y año (el título 'Laptop lenta' sigue sin año: se deduce 2026).
rep("tecnicoUid: 'u1', tecnico: 'Test User', tipo: 'SOFTWARE', area: 'Sistemas'",
    "tecnicoUid: 'u1', tecnico: 'Test User', empresa: 'Lapi', anio: 2026, tipo: 'SOFTWARE', area: 'Sistemas'")
# BA7b: el título guardado ahora es el compuesto con el año.
rep("var ba7b = !!borBA7b && borBA7b.estado === 'borrador' && borBA7b.folio === null && borBA7b.equipo.serie === '' && borBA7b.equipo.hostname === '' && borBA7b.equipo.modelo === '' && toastTxt().indexOf('Borrador guardado') !== -1;",
    "var ba7b = !!borBA7b && borBA7b.estado === 'borrador' && borBA7b.folio === null && borBA7b.equipo.serie === '' && borBA7b.equipo.hostname === '' && borBA7b.equipo.modelo === '' && borBA7b.tituloCaso === 'Borrador sin ids 2026' && borBA7b.anio === 2026 && toastTxt().indexOf('Borrador guardado') !== -1;")

BB = r'''
  // BB: serie nueva 2.5.1 — 12 cambios + punto 13 (conformidad abajo a la derecha).
  var DESC_CAMBIOS_DEF = 'se realiza mantenimiento preventivo en hardware y software, sopleteo y limpieza general, instalación de actualización, revisión de políticas y antivirus, desinstalación de software no permitido';
  function pdfTextRows(pdfStr) {
    var out = [], re = /BT \/(F\d) (\d+) Tf ([\d.]+) ([\d.]+) Td \(((?:\\.|[^()\\])*)\) Tj ET/g, mm;
    while ((mm = re.exec(pdfStr))) out.push({ f: mm[1], s: Number(mm[2]), x: Number(mm[3]), y: Number(mm[4]), t: mm[5] });
    return out;
  }
  async function pdfStrOf(m, imgs) {
    return Buffer.from(await buildPdfMant(m, imgs || {}).arrayBuffer()).toString('latin1');
  }
  // BB0: versión 2.5.1 en 2 sitios exactos, 0 de 2.5.0 y 0 diálogos nativos.
  var bb0nat = (html.match(/alert\(/g) || []).length === 0 && (html.match(/confirm\(/g) || []).length === 0 && (html.match(/prompt\(/g) || []).length === 0;
  console.log('BB0) 2.5.1 en 2 sitios:', n251 === 2, '| 0 de 2.5.0:', !html.includes('2.5.0'), '| 0 alert/confirm/prompt:', bb0nat);
  // BB1: empresa — default Lapi, se guarda, se ve en tarjeta/orden/PDF;
  // con Ludi el PDF NO lleva el bloque de contacto de Lapi.
  loginAs('u1', 'Test User', 'usuario');
  mantOpenForm(null, null);
  var bb1def = document.getElementById('fM-empresa').value === 'Lapi';
  document.getElementById('fM-empresa').value = 'Ludi';
  var mBB1 = mantReadForm();
  var bb1read = mBB1.empresa === 'Ludi';
  var mBB1ludi = mkMant({ empresa: 'Ludi', tituloCaso: 'Caso Ludi' });
  var bb1card = mantCardHtml(mBB1ludi).indexOf('Ludi') !== -1;
  mantenimientos = [mBB1ludi];
  mantShowOrder(mBB1ludi.id);
  var bb1ord = document.getElementById('mantOrderBody').innerHTML.indexOf('Empresa: Ludi') !== -1;
  var pdfLudi = await pdfStrOf(mBB1ludi);
  var bb1pdfLudi = pdfLudi.indexOf('Ludi') !== -1 && pdfLudi.indexOf('Rosa Blanca 63') === -1 && pdfLudi.indexOf('sistemas@lapi.com.mx') === -1 && pdfLudi.indexOf('Lapi Sistemas') === -1;
  var pdfLapi = await pdfStrOf(mkMant({}));
  var bb1pdfLapi = pdfLapi.indexOf('Lapi Sistemas') !== -1 && pdfLapi.indexOf('Rosa Blanca 63') !== -1 && pdfLapi.indexOf('sistemas@lapi.com.mx') !== -1 && pdfLapi.indexOf('Empresa: Lapi') !== -1;
  console.log('BB1) empresa default Lapi:', bb1def, '| se lee Ludi:', bb1read, '| tarjeta muestra Ludi:', bb1card, '| vista de orden muestra Ludi:', bb1ord, '| PDF Ludi sin contacto Lapi:', bb1pdfLudi, '| PDF Lapi con contacto:', bb1pdfLapi);
  // BB2: tipo — ambos checkboxes marcados al abrir (nuevo y detectado);
  // quitar uno deja solo el otro; quitar los dos bloquea la creación.
  mantOpenForm(null, null);
  var bb2def = document.getElementById('fM-tipo-sw').checked === true && document.getElementById('fM-tipo-hw').checked === true;
  document.getElementById('fM-tipo-hw').checked = false;
  var bb2sw = mantReadForm().tipo === 'SOFTWARE';
  document.getElementById('fM-tipo-sw').checked = false;
  var bb2none = mantReadForm().tipo === '' && mantFaltaCrear(Object.assign(mantReadForm(), { equipo: { serie: 'S', hostname: 'H', modelo: 'M' }, area: 'A', responsable: 'R', tituloCaso: 'T', tipoFalla: 'F', descripcionEquipo: 'D', fechaServicio: '2026-11-16', whatsappUsuario: '5512345678', firmaTecnico: 'data:image/png;base64,xx' })) === 'el tipo de mantenimiento';
  var mBB2old = mkMant({ tipo: 'HARDWARE' });
  mantOpenForm(mBB2old, null);
  var bb2old = document.getElementById('fM-tipo-sw').checked === false && document.getElementById('fM-tipo-hw').checked === true;
  console.log('BB2) ambos marcados al abrir:', bb2def, '| solo SOFTWARE al quitar HARDWARE:', bb2sw, '| ninguno bloquea crear:', bb2none, '| orden vieja HARDWARE marca solo ese:', bb2old);
  // BB3: diagonales — tiempos, tipo de falla y fechas plan/compromiso/
  // periodo se prellenan con '/' solo si están vacíos; lo guardado se respeta.
  mantOpenForm(null, null);
  var bb3def = ['fM-tRep', 'fM-tViaje', 'fM-tCaido', 'fM-tipoFalla', 'fM-fechaPlan', 'fM-fechaComp', 'fM-periodoPrueba'].every(function (id) { return document.getElementById(id).value === '/'; });
  var mBB3 = mkMant({ tiempoReparacion: '3 horas', tipoFalla: 'Disco', fechaPlaneacion: '2026-11-10', periodoPrueba: '7 días' });
  mantOpenForm(mBB3, null);
  var bb3keep = document.getElementById('fM-tRep').value === '3 horas' && document.getElementById('fM-tipoFalla').value === 'Disco' && document.getElementById('fM-fechaPlan').value === '2026-11-10' && document.getElementById('fM-periodoPrueba').value === '7 días' && document.getElementById('fM-tViaje').value === '/' && document.getElementById('fM-tCaido').value === '/';
  console.log('BB3) diagonales por default:', bb3def, '| valores guardados se respetan:', bb3keep);
  // BB4: título compuesto con año — default, año actual, deducción en viejas.
  mantOpenForm(null, null);
  var bb4def = document.getElementById('fM-titulo').value === 'Mantenimiento Preventivo sistemas' && String(document.getElementById('fM-anio').value) === '2026';
  document.getElementById('fM-serie').value = 'S-BB4'; document.getElementById('fM-hostname').value = 'PC-BB4'; document.getElementById('fM-modelo').value = 'Modelo BB4';
  document.getElementById('fM-area').value = 'Sistemas'; document.getElementById('fM-responsable').value = 'Ana';
  document.getElementById('fM-tipoFalla').value = 'Preventivo'; document.getElementById('fM-fechaServ').value = '2026-11-16'; document.getElementById('fM-whatsapp').value = '5512345678';
  mantFirmaData = 'data:image/png;base64,iVBORw0KGgo=';
  var mBB4 = mantReadForm();
  var bb4comp = mBB4.tituloCaso === 'Mantenimiento Preventivo sistemas 2026' && mBB4.anio === 2026;
  var mBB4old = mkMant({ tituloCaso: 'Caso viejo' });
  mantOpenForm(mBB4old, null);
  var bb4old = String(document.getElementById('fM-anio').value) === '2026' && document.getElementById('fM-titulo').value === 'Caso viejo' && mantReadForm().tituloCaso === 'Caso viejo 2026';
  var mBB4y = mkMant({ tituloCaso: 'Mantenimiento Preventivo sistemas 2024' });
  mantOpenForm(mBB4y, null);
  var bb4y = String(document.getElementById('fM-anio').value) === '2024' && mantReadForm().tituloCaso === 'Mantenimiento Preventivo sistemas 2024';
  console.log('BB4) título y año por default:', bb4def, '| guardado compuesto 2026:', bb4comp, '| vieja sin año deduce 2026:', bb4old, '| título con 2024 deduce 2024:', bb4y);
  // BB5: descripción del equipo = hostname (al abrir y al teclear).
  mantOpenForm(mantFromDetectado(detBA3), detBA3.id);
  var bb5det = document.getElementById('fM-descEquipo').value === 'PC-BA3';
  mantOpenForm(null, null);
  document.getElementById('fM-descEquipo').value = '';
  document.getElementById('fM-hostname').value = 'PC-NUEVO';
  document.getElementById('fM-hostname')._h.input[0]();
  var bb5type = document.getElementById('fM-descEquipo').value === 'PC-NUEVO';
  document.getElementById('fM-descEquipo').value = 'Descripción manual';
  document.getElementById('fM-hostname').value = 'PC-OTRO';
  document.getElementById('fM-hostname')._h.input[0]();
  var bb5manual = document.getElementById('fM-descEquipo').value === 'Descripción manual';
  console.log('BB5) detectado llena descripción con hostname:', bb5det, '| teclear hostname la copia si está vacía:', bb5type, '| escrita a mano se respeta:', bb5manual);
  // BB6: descripción de cambios por default (texto exacto), editable.
  mantOpenForm(null, null);
  var bb6def = document.getElementById('fM-descCambios').value === DESC_CAMBIOS_DEF;
  var mBB6 = mkMant({ descripcionCambios: 'Cambios míos' });
  mantOpenForm(mBB6, null);
  var bb6keep = document.getElementById('fM-descCambios').value === 'Cambios míos';
  console.log('BB6) cambios por default exacto:', bb6def, '| guardado se respeta:', bb6keep);
  // BB7: PDF — bloques Planeación/Compromiso/Periodo con '/', Liberación
  // con fecha elegida y ambas firmas.
  var mBB7 = mkMant({ id: 'bb7', folio: '00007', estado: 'creada', fechaPlaneacion: '/', fechaCompromiso: '/', periodoPrueba: '/', fechaLiberacion: '2026-11-20', firmaTecnico: 'data:image/png;base64,iVBORw0KGgo=' });
  mBB7.firma = { nombre: 'Ana López', area: 'Ventas', comentarios: '', satisfaccion: 9, firma: 'data:image/png;base64,iVBORw0KGgo=', firmadoEn: Date.now() };
  var pdfBB7 = await pdfStrOf(mBB7);
  var bb7slash = (pdfBB7.match(/Fecha: \//g) || []).length >= 3 && pdfBB7.indexOf('Firma Sistemas: /') !== -1 && pdfBB7.indexOf('Firma Área solicitante: /') !== -1;
  var bb7lib = pdfBB7.indexOf('Fecha: 2026-11-20') !== -1 && pdfBB7.indexOf('Sistemas — Liberación:') !== -1 && pdfBB7.indexOf('Área solicitante — Liberación:') !== -1 && pdfBB7.indexOf('Firma: Test User (guardada en la app)') !== -1 && pdfBB7.indexOf('Firma: Ana López (guardada en la app)') !== -1;
  console.log('BB7) bloques con diagonales:', bb7slash, '| Liberación con fecha y ambas firmas:', bb7lib);
  // BB8: admin elimina órdenes (tarjeta y vista); el usuario no ve el botón.
  var delCloudBB8 = [];
  global.Cloud.deleteMant = async function (id) { delCloudBB8.push(id); };
  var mBB8 = mkMant({ id: 'bb8', folio: '00008', estado: 'creada', tituloCaso: 'Para borrar' });
  cloudRole = 'usuario';
  var bb8nouser = mantCardHtml(mBB8).indexOf('data-mant-del-order') === -1;
  cloudRole = 'admin';
  var bb8admin = mantCardHtml(mBB8).indexOf('data-mant-del-order="bb8"') !== -1;
  mantenimientos = [mBB8];
  mantShowOrder('bb8');
  var bb8view = document.getElementById('btnMantEliminarOrden').hidden === false;
  loginAs('u1', 'Test User', 'usuario');
  mantenimientos = [mBB8];
  mantShowOrder('bb8');
  var bb8viewUser = document.getElementById('btnMantEliminarOrden').hidden === true;
  loginAs('uGer', 'Gerardo', 'admin');
  mantenimientos = [mBB8];
  var btnBB8 = {
    getAttribute: function (a) { return a === 'data-mant-del-order' ? 'bb8' : null; },
    hasAttribute: function (a) { return a === 'data-mant-del-order'; },
    closest: function (sel) { return sel === '[data-mant-del-order]' ? btnBB8 : null; },
    classList: { contains: function () { return false; } }
  };
  document.getElementById('mantList')._h.click[0]({ target: btnBB8 });
  var bb8modal = document.getElementById('confirmModal').hidden === false && document.getElementById('confirmMsg').textContent.indexOf('no se puede deshacer') !== -1;
  answerConfirm(false);
  await sleep(20);
  var bb8no = mantenimientos.length === 1;
  document.getElementById('mantList')._h.click[0]({ target: btnBB8 });
  answerConfirm(true);
  await sleep(20);
  var bb8si = mantenimientos.length === 0 && delCloudBB8.indexOf('bb8') !== -1 && toastTxt().indexOf('eliminada') !== -1;
  console.log('BB8) usuario sin botón en tarjeta:', bb8nouser, '| admin con botón:', bb8admin, '| vista admin muestra Eliminar:', bb8view, '| vista usuario lo oculta:', bb8viewUser, '| pide confirmar:', bb8modal, '| con No no borra:', bb8no, '| con Sí borra local+nube:', bb8si);
  // BB9: firma.html — botón Cerrar, window.close a los 800 ms, aviso y empresa.
  var firmaHtml = fs.readFileSync('/home/hatch/workspace/android/checklist-cloud/hosting/public/firma.html', 'utf8');
  var bb9btn = firmaHtml.includes('id="btnCerrarSigned"') && firmaHtml.includes('id="btnCerrarDone"') && firmaHtml.includes('>Cerrar</button>');
  var bb9close = firmaHtml.includes('window.close()') && firmaHtml.includes('}, 800);') && firmaHtml.includes('Ya puedes cerrar esta ventana');
  var bb9emp = firmaHtml.includes("['Empresa', o.empresa || 'Lapi']");
  console.log('BB9) firma.html botón Cerrar en ambas vistas:', bb9btn, '| close + 800 ms + aviso:', bb9close, '| muestra la empresa:', bb9emp);
  // BB10: PDF válido con ambas firmas (bytes > 0 y folio) y compartir
  // habilitado; sin ambas, PDF bloqueado con toast y botón deshabilitado.
  var mBB10 = mkMant({ id: 'bb10', folio: '00010', estado: 'creada', firmaTecnico: 'data:image/png;base64,iVBORw0KGgo=' });
  mBB10.firma = { nombre: 'Ana López', area: 'Ventas', comentarios: '', satisfaccion: 8, firma: 'data:image/png;base64,iVBORw0KGgo=', firmadoEn: Date.now() };
  var blobBB10 = buildPdfMant(mBB10, {});
  var bufBB10 = Buffer.from(await blobBB10.arrayBuffer());
  var bb10pdf = bufBB10.length > 0 && bufBB10.toString('latin1').indexOf('%PDF') === 0 && bufBB10.toString('latin1').indexOf('Folio: 00010') !== -1;
  mantenimientos = [mBB10];
  mantShowOrder('bb10');
  var bb10en = document.getElementById('btnMantCompartir').disabled === false;
  var mBB10b = mkMant({ id: 'bb10b', folio: '00011', estado: 'creada', firmaTecnico: '' });
  mantenimientos = [mBB10b];
  mantShowOrder('bb10b');
  var bb10dis = document.getElementById('btnMantCompartir').disabled === true && document.getElementById('mantOrderNote').textContent.indexOf('firma del técnico') !== -1;
  await sharePdfMant(mBB10b);
  var bb10toast = toastTxt().indexOf('firma del técnico') !== -1;
  console.log('BB10) PDF válido con folio:', bb10pdf, '| compartir habilitado con ambas:', bb10en, '| sin firma: botón deshabilitado y nota:', bb10dis, '| intento avisa con toast:', bb10toast);
  // BB11: compartir sin Capacitor no miente: descarga el PDF y lo avisa.
  global.Capacitor = undefined;
  global.FileReader = global.FileReader || class { constructor() { this.result = null; } readAsDataURL(blob) { var self = this; blob.arrayBuffer().then(function (ab) { self.result = 'data:application/pdf;base64,' + Buffer.from(ab).toString('base64'); if (self.onload) self.onload(); }); } };
  await shareMantCopy(mBB10);
  var bb11 = toastTxt().indexOf('PDF descargado: orden-servicio-00010.pdf') !== -1;
  console.log('BB11) sin Capacitor: descarga el PDF y avisa (no dice que compartió):', bb11);
  // BB12: punto 13 — la conformidad es el cierre final, abajo a la derecha.
  var pdfBB12 = await pdfStrOf(mBB10);
  var rowsBB12 = pdfTextRows(pdfBB12);
  var confBB12 = rowsBB12.find(function (r) { return r.t.indexOf('Conformidad del usuario') === 0; });
  var nomBB12 = rowsBB12.find(function (r) { return r.t.indexOf('Nombre: Ana L') === 0; });
  var fecBB12 = rowsBB12.find(function (r) { return r.t.indexOf('Fecha: ') === 0 && r.x > 297; });
  var horBB12 = rowsBB12.find(function (r) { return r.t.indexOf('Hora: ') === 0 && r.x > 297; });
  var firBB12 = rowsBB12.find(function (r) { return r.t.indexOf('Firma de conformidad:') === 0; });
  var expX = confBB12 ? 595 - 48 - pdfTextWidth(confBB12.t, 'F2', 12) : -1;
  var bb12x = !!confBB12 && confBB12.x > 297 && Math.abs(confBB12.x - expX) < 1.5;
  var bb12order = pdfBB12.indexOf('Conformidad del usuario') > pdfBB12.indexOf('Generado el') && pdfBB12.indexOf('Conformidad del usuario') > pdfBB12.indexOf('Liberación') && pdfBB12.lastIndexOf('/Imusuario Do') > pdfBB12.indexOf('Conformidad del usuario');
  var bb12rows = !!nomBB12 && nomBB12.x > 297 && !!fecBB12 && !!horBB12 && !!firBB12 && firBB12.x > 297;
  var pdfBB12b = await pdfStrOf(mkMant({ id: 'bb12b', folio: '00012', estado: 'creada', firmaTecnico: 'data:image/png;base64,iVBORw0KGgo=' }));
  var rowsBB12b = pdfTextRows(pdfBB12b);
  var pendBB12 = rowsBB12b.find(function (r) { return r.t === 'Pendiente de firma.'; });
  var bb12pend = !!pendBB12 && pendBB12.x > 297;
  console.log('BB12) conformidad a la derecha (x=' + (confBB12 ? confBB12.x : '—') + ' esperado ' + expX.toFixed(1) + '):', bb12x, '| es el cierre final tras Liberación y Generado:', bb12order, '| nombre/fecha/hora/firma a la derecha:', bb12rows, '| sin firma del usuario: pendiente a la derecha:', bb12pend);
'''
rep("  process.exit(0);", BB + "\n  process.exit(0);")

io.open(P, 'w', encoding='utf-8').write(s)
print('test 251 ok')
