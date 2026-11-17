# Parche tests 2.5.0: actualiza AM0/AP0/AR0 a 2.5.0 y añade la serie BA.
import io

P = '/home/hatch/workspace/android/checklist-cloud/tests/test20250.js'
s = io.open(P, encoding='utf-8').read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'NO ENCONTRADO o repetido (%d): %r' % (c, old[:100])
    s = s.replace(old, new)

rep("// este archivo y cambiar checklist20231.js por el nuevo extraído.",
    "// este archivo y cambiar checklist20240.js por el nuevo extraído.")
rep("const SRC = fs.readFileSync(__dirname + '/checklist20240.js', 'utf8');",
    "const SRC = fs.readFileSync(__dirname + '/checklist20250.js', 'utf8');")
rep("console.log('AM0) versión 2.4.0:', html.includes('Versión 2.4.0'), '| sin 2.3.9:', !html.includes('Versión 2.3.9')",
    "console.log('AM0) versión 2.5.0:', html.includes('Versión 2.5.0'), '| sin 2.4.0:', !html.includes('Versión 2.4.0')")
rep("console.log('AP0) estáticos 2.4.0: versión:', html.includes('Versión 2.4.0') && !html.includes('Versión 2.3.9')",
    "console.log('AP0) estáticos 2.5.0: versión:', html.includes('Versión 2.5.0') && !html.includes('Versión 2.4.0')")
rep("  var n240 = (html.match(/2\\.4\\.0/g) || []).length;",
    "  var n250 = (html.match(/2\\.5\\.0/g) || []).length;")
rep("console.log('AR0) versión 2.4.0 visible:', html.includes('Versión 2.4.0') && html.includes('Versión: 2.4.0'), '| 0 de 2.3.9:', !html.includes('2.3.9'), '| ocurrencias 2.4.0:', n240 === 42);",
    "console.log('AR0) versión 2.5.0 visible:', html.includes('Versión 2.5.0') && html.includes('Versión: 2.5.0'), '| 0 de 2.4.0:', !html.includes('2.4.0'), '| ocurrencias 2.5.0:', n250 === 52);")

BA = r'''
  // BA: serie nueva 2.5.0 — Mantenimientos Preventivos.
  function mkMant(over) {
    return mantFromCloud(Object.assign({ id: 'm1', createdAt: Date.now(), folio: null, estado: 'borrador', tecnicoUid: 'u1', tecnico: 'Test User', tipo: 'SOFTWARE', area: 'Sistemas', responsable: 'Ana', tiempoReparacion: '2 horas', tiempoViaje: '30 min', tiempoSistemaCaido: '1 hora', fechaServicio: '2026-11-15', fechaTermino: '2026-11-15', tituloCaso: 'Laptop lenta', tipoFalla: 'Software', identificacion: { impresora: true, cpu: true, monitor: true, teclado: true, mouse: true, noBreak: false }, descripcionEquipo: 'Laptop Dell Inspiron', condiciones: { impresora: true, cpu: true, monitor: true, teclado: true, mouse: true, noBreak: false, notas: '' }, preventivo: { impresora: true, cpu: true, monitor: false, teclado: false, mouse: false, noBreak: false }, descripcionCambios: 'Se reinstaló el SO', conclusion: 'Equipo listo', comentarios: '', fechaPlaneacion: '2026-11-14', fechaCompromiso: '2026-11-15', periodoPrueba: '5 días', fechaLiberacion: '2026-11-20', observaciones: 'Sin observaciones', observacionesDetectadas: 'Procesador: Intel i5', equipo: { tipo: 'Laptop', marca: 'Dell', modelo: 'Inspiron 3501', serie: 'S1', hostname: 'PC-01', cpu: 'Intel Core i5', ramGB: 8, discoGB: 256, discoTipo: 'SSD', ip: '192.168.1.45', redes: [{ nombre: 'Wi-Fi', ip: '192.168.1.45', ipTipo: 'Dinámica' }], impresora: 'HP LaserJet', anydeskId: '123456789', anydeskAlias: 'Oficina', antivirus: 'ESET NOD32', politicas: { cambioDias: 90, minLongitud: 10, bloqueoIntentos: 5, bloqueoSegundos: 350, cumpleCambio: true, cumpleLongitud: true, cumpleIntentos: true, cumpleBloqueo: true, cumple: true }, usuarioSistemas: true, so: 'Windows 11 Pro', versiones: { so: 'Windows 11 Pro 26H2', antivirus: 'ESET NOD32 Antivirus 18.0.12', esetAgent: '', chrome: '141.0.7390.65' } }, whatsappUsuario: '5512345678', firmaTecnico: '', firma: null }, over || {}));
  }
  function fillMantFormBA(serie, host, modelo) {
    mantOpenForm(null, null);
    document.getElementById('fM-tecnico').value = 'Test User';
    document.getElementById('fM-serie').value = serie;
    document.getElementById('fM-hostname').value = host;
    document.getElementById('fM-modelo').value = modelo;
    document.getElementById('fM-area').value = 'Sistemas';
    document.getElementById('fM-responsable').value = 'Ana';
    document.getElementById('fM-titulo').value = 'Caso ' + serie;
    document.getElementById('fM-tipoFalla').value = 'Software';
    document.getElementById('fM-descEquipo').value = 'Equipo ' + serie;
    document.getElementById('fM-fechaServ').value = '2026-11-15';
    document.getElementById('fM-whatsapp').value = '5512345678';
    mantFirmaData = 'data:image/png;base64,iVBORw0KGgo=';
  }
  // BA0: estáticos — selector, tabs, formulario, firebase.js y reglas.
  var ba0html = html.includes('Versión 2.5.0') && html.includes('Versión: 2.5.0') && !html.includes('2.4.0');
  var ba0sel = html.includes('id="viewInicio"') && html.includes('id="btnGoMant"') && html.includes('Mantenimientos Preventivos') && html.includes('data-v="inicio"') && html.includes('data-v="mant"');
  var ba0form = ['fM-serie', 'fM-hostname', 'fM-modelo', 'fM-tecnico', 'fM-tipo', 'fM-area', 'fM-responsable', 'fM-titulo', 'fM-tipoFalla', 'fM-descEquipo', 'fM-observaciones', 'fM-obsDet', 'fM-whatsapp', 'fM-firmaCanvas', 'btnMantCrear', 'btnMantGuardar', 'btnMantCancelar', 'mantDetList', 'mantAdminFilter', 'mantOrderBox', 'btnMantWaLink', 'btnMantPdf', 'btnMantCompartir', 'btnMantCancelarOrden'].every(function (id) { return html.includes('id="' + id + '"'); });
  var ba0fb = ['subscribeMantenimientos', 'upsertMant', 'deleteMant', 'getMantenimiento', 'getAllMantenimientos', 'asignarFolio', 'guardarFirma'].every(function (f) { return fb.includes(f); });
  var ba0rules = rules.includes('match /mantenimientos/{id}') && rules.includes('match /config/folios') && rules.includes('allow get: if true') && rules.includes('resource.data.siguiente + 1');
  console.log('BA0) versión 2.5.0 sin 2.4.0:', ba0html, '| selector y tabs Inicio/Mant:', ba0sel, '| formulario y orden completos:', ba0form, '| firebase.js con mantenimientos y folio:', ba0fb, '| reglas mantenimientos y folios:', ba0rules);
  // BA1: el selector es la vista al abrir; los 4 botones navegan; un
  // usuario normal no entra a Usuarios (va al selector, no a Preparar).
  loginAs('u1', 'Test User', 'usuario');
  showVista('inicio');
  var ba1inicio = document.getElementById('viewInicio').hidden === false && document.getElementById('viewPreparar').hidden === true && document.getElementById('viewMant').hidden === true && document.getElementById('viewRenta-rec').hidden === true;
  document.getElementById('btnGoMant')._h.click[0]();
  var ba1mant = document.getElementById('viewMant').hidden === false && document.getElementById('viewInicio').hidden === true;
  document.getElementById('btnGoPreparar')._h.click[0]();
  var ba1prep = document.getElementById('viewPreparar').hidden === false;
  cloudRole = 'usuario';
  showVista('usuarios');
  var ba1nouser = document.getElementById('viewInicio').hidden === false && document.getElementById('viewUsuarios').hidden === true;
  console.log('BA1) al abrir: selector visible:', ba1inicio, '| botón Mantenimientos abre la vista:', ba1mant, '| botón Por preparar navega:', ba1prep, '| usuario normal fuera de Usuarios va al selector:', ba1nouser);
  // BA2: políticas cumple/no cumple (90 días, 10 caracteres, 5 intentos, 350 s).
  var polOk = mantPoliticasCumple({ cambioDias: 90, minLongitud: 10, bloqueoIntentos: 5, bloqueoSegundos: 350 });
  var polOk2 = mantPoliticasCumple({ cambioDias: 30, minLongitud: 12, bloqueoIntentos: 3, bloqueoSegundos: 600 });
  var polBad = mantPoliticasCumple({ cambioDias: 180, minLongitud: 8, bloqueoIntentos: 10, bloqueoSegundos: 60 });
  var polVacio = mantPoliticasCumple({});
  var ba2 = polOk.cumple === true && polOk2.cumple === true && polBad.cumple === false && polBad.cumpleCambio === false && polBad.cumpleLongitud === false && polBad.cumpleIntentos === false && polBad.cumpleBloqueo === false && polVacio.cumple === null;
  var ba2card = mantCardHtml(mkMant()).includes('Políticas: ✓ Cumple');
  var mBad = mkMant();
  mBad.equipo.politicas = { cambioDias: 180, minLongitud: 8, bloqueoIntentos: 10, bloqueoSegundos: 60, cumpleCambio: false, cumpleLongitud: false, cumpleIntentos: false, cumpleBloqueo: false, cumple: false };
  var ba2cardBad = mantCardHtml(mBad).includes('Políticas: ✗ No cumple');
  var ba2txt = politicasText({ cambioDias: 90, minLongitud: 10, bloqueoIntentos: 5, bloqueoSegundos: 350 }).indexOf('Cumple') !== -1;
  console.log('BA2) políticas: justo en lo esperado cumple:', ba2, '| tarjeta cumple:', ba2card, '| tarjeta no cumple:', ba2cardBad, '| texto compilado:', ba2txt);
  // BA3: observaciones detectadas compiladas (software, IPs, AnyDesk,
  // impresora, antivirus, políticas, usuario de sistemas, ids).
  var detBA3 = { id: 'BA3-DET', hostname: 'PC-BA3', marca: 'HP', modelo: 'EliteDesk 800', serie: 'BA3-DET', cpu: 'Intel Core i7-10700', ramGB: 16, discoGB: 512, discoTipo: 'SSD', so: 'Windows 11 Pro', tipo: 'Desktop', detectadoEn: Date.now() - 60000, detectadoPor: 'Gerardo', usado: false, checks: { t18: true }, detalles: { impresora: 'HP LaserJet' }, versiones: { so: 'Windows 11 Pro 26H2 (compilación 26200)', antivirus: 'ESET NOD32 Antivirus 18.0.12', chrome: '141.0.7390.65' }, ip: '192.168.1.45', ipTipo: 'Dinámica', redes: [{ nombre: 'Wi-Fi', ip: '192.168.1.45', ipTipo: 'Dinámica' }, { nombre: 'Ethernet', ip: '10.0.0.20', ipTipo: 'Estática' }], anydeskId: '123456789', anydeskAlias: 'Oficina', politicas: { cambioDias: 90, minLongitud: 10, bloqueoIntentos: 5, bloqueoSegundos: 350 }, usuarioSistemas: true };
  var obsBA3 = compileObservacionesDetectadas(detBA3);
  var ba3 = ['Procesador: Intel Core i7-10700', 'RAM: 16 GB', 'Disco: 512 GB SSD', 'IP: 192.168.1.45', 'Redes: Wi-Fi: 192.168.1.45 (Dinámica) · Ethernet: 10.0.0.20 (Estática)', 'Versiones detectadas: SO: Windows 11 Pro 26H2', 'Antivirus: ESET NOD32 Antivirus 18.0.12', 'Chrome: 141.0.7390.65', 'AnyDesk: 123 456 789 (Oficina)', 'Impresora: HP LaserJet', 'Políticas: cambio cada 90 días ✓', 'Usuario de sistemas: Sí', 'Hostname: PC-BA3', 'Serie: BA3-DET', 'Modelo: HP EliteDesk 800'].every(function (s) { return obsBA3.indexOf(s) !== -1; });
  var mBA3 = mantFromDetectado(detBA3);
  var ba3b = mBA3.equipo.serie === 'BA3-DET' && mBA3.equipo.hostname === 'PC-BA3' && mBA3.equipo.modelo === 'EliteDesk 800' && mBA3.observacionesDetectadas === obsBA3 && mBA3.equipo.politicas.cumple === true && mBA3.equipo.redes.length === 2;
  console.log('BA3) observaciones compiladas con todo:', ba3, '| mantFromDetectado llena serie/host/modelo y políticas:', ba3b);
  // BA4: 'Usar este equipo' en Mantenimientos llena el formulario.
  loginAs('u1', 'Test User', 'usuario');
  CLOUD_ENABLED = true;
  detectados = [detBA3];
  renderMantDetectados();
  document.getElementById('mantDetList')._h.click[0]({ target: { closest: function (sel) { return sel === '[data-mant-det-use]' ? { getAttribute: function () { return 'BA3-DET'; } } : null; } } });
  var ba4form = document.getElementById('mantFormBox').hidden === false && document.getElementById('fM-serie').value === 'BA3-DET' && document.getElementById('fM-hostname').value === 'PC-BA3' && document.getElementById('fM-modelo').value === 'EliteDesk 800' && document.getElementById('fM-obsDet').value.indexOf('Procesador: Intel Core i7-10700') !== -1 && document.getElementById('fM-tecnico').value === 'Test User' && document.getElementById('fM-eq-redes').value.indexOf('192.168.1.45') !== -1;
  console.log('BA4) Usar este equipo llena el formulario (serie/host/modelo/obs/tecnico/redes):', ba4form);
  // BA5: crear orden bloqueada sin serie, sin hostname y sin modelo (el
  // toast dice cuál falta); con los tres, crea la orden.
  var upBA5 = [];
  global.Cloud.upsertMant = async function (d) { upBA5.push(d); };
  global.Cloud.asignarFolio = async function () { return '00001'; };
  var nBA5 = mantenimientos.length;
  fillMantFormBA('', '', '');
  document.getElementById('btnMantCrear')._h.click[0](); await sleep(20);
  var ba5sinSerie = mantenimientos.length === nBA5 && toastTxt().indexOf('número de serie') !== -1;
  document.getElementById('fM-serie').value = 'S-BA5';
  document.getElementById('btnMantCrear')._h.click[0](); await sleep(20);
  var ba5sinHost = mantenimientos.length === nBA5 && toastTxt().indexOf('hostname') !== -1;
  document.getElementById('fM-hostname').value = 'PC-BA5';
  document.getElementById('btnMantCrear')._h.click[0](); await sleep(20);
  var ba5sinMod = mantenimientos.length === nBA5 && toastTxt().indexOf('modelo') !== -1;
  document.getElementById('fM-modelo').value = 'Inspiron 3501';
  document.getElementById('btnMantCrear')._h.click[0](); await sleep(20);
  var creadaBA5 = mantenimientos.find(function (m) { return m.folio === '00001'; });
  var ba5creada = !!creadaBA5 && creadaBA5.estado === 'creada' && creadaBA5.equipo.serie === 'S-BA5' && creadaBA5.equipo.hostname === 'PC-BA5' && upBA5.length >= 1 && document.getElementById('mantOrderBox').hidden === false;
  console.log('BA5) sin serie bloquea:', ba5sinSerie, '| sin hostname bloquea:', ba5sinHost, '| sin modelo bloquea:', ba5sinMod, '| con los tres crea la orden con folio:', ba5creada);
  // BA6: folio 00001 y siguiente 00002 (contador simulado de la transacción).
  mantenimientos = [];
  var siguienteBA6 = 1;
  global.Cloud.asignarFolio = async function () { var n = siguienteBA6; siguienteBA6 = n + 1; return String(n).padStart(5, '0'); };
  fillMantFormBA('S-BA6A', 'PC-BA6A', 'Modelo A');
  document.getElementById('btnMantCrear')._h.click[0](); await sleep(20);
  var ordA = mantenimientos.find(function (m) { return m.equipo.serie === 'S-BA6A'; });
  fillMantFormBA('S-BA6B', 'PC-BA6B', 'Modelo B');
  document.getElementById('btnMantCrear')._h.click[0](); await sleep(20);
  var ordB = mantenimientos.find(function (m) { return m.equipo.serie === 'S-BA6B'; });
  var ba6 = !!ordA && ordA.folio === '00001' && !!ordB && ordB.folio === '00002' && siguienteBA6 === 3;
  console.log('BA6) primera orden folio 00001:', ba6, '| segunda orden folio 00002 y contador en 3:', !!ordB && ordB.folio === '00002' && siguienteBA6 === 3);
  // BA7: sin conexión no hay folio: se guarda como borrador sin folio; el
  // borrador también se guarda sin serie/hostname/modelo.
  global.Cloud.asignarFolio = async function () { throw new Error('offline'); };
  fillMantFormBA('S-BA7', 'PC-BA7', 'Modelo BA7');
  document.getElementById('btnMantCrear')._h.click[0](); await sleep(20);
  var borBA7 = mantenimientos.find(function (m) { return m.equipo.serie === 'S-BA7'; });
  var ba7 = !!borBA7 && borBA7.estado === 'borrador' && borBA7.folio === null && toastTxt().indexOf('Sin conexión') !== -1 && toastTxt().indexOf('borrador') !== -1;
  mantOpenForm(null, null);
  document.getElementById('fM-titulo').value = 'Borrador sin ids';
  document.getElementById('btnMantGuardar')._h.click[0]();
  var borBA7b = mantenimientos.find(function (m) { return m.tituloCaso === 'Borrador sin ids'; });
  var ba7b = !!borBA7b && borBA7b.estado === 'borrador' && borBA7b.folio === null && borBA7b.equipo.serie === '' && borBA7b.equipo.hostname === '' && borBA7b.equipo.modelo === '' && toastTxt().indexOf('Borrador guardado') !== -1;
  console.log('BA7) sin conexión: borrador sin folio:', ba7, '| borrador sin serie/host/modelo sí guarda:', ba7b);
  // BA8: link de firma con id y WhatsApp con 52 antepuesto a 10 dígitos.
  var mBA8 = mkMant({ id: 'ba8', folio: '00003', estado: 'creada', whatsappUsuario: '55 1234-5678' });
  var ba8url = mantFirmaUrl(mBA8) === 'https://checklist-soporte.web.app/firma.html?id=ba8';
  var waBA8 = mantFirmaWaUrl(mBA8);
  var ba8wa = waBA8.indexOf('https://wa.me/525512345678?text=') === 0 && decodeURIComponent(waBA8.split('text=')[1]).indexOf('https://checklist-soporte.web.app/firma.html?id=ba8') !== -1 && decodeURIComponent(waBA8.split('text=')[1]).indexOf('folio 00003') !== -1;
  var ba8num = mantWaNumber('5512345678') === '525512345678' && mantWaNumber('+52 55 1234 5678') === '525512345678' && mantWaNumber('123456789012') === '123456789012';
  var openedBA8 = [];
  global.open = function (url, target) { openedBA8.push([url, target]); };
  mantenimientos = [mBA8];
  mantOrderId = 'ba8';
  mantEnviarLink();
  var ba8open = openedBA8.length === 1 && openedBA8[0][0] === waBA8 && openedBA8[0][1] === '_blank';
  console.log('BA8) link de firma con id:', ba8url, '| wa.me con 52 y link:', ba8wa, '| normalización de números:', ba8num, '| Enviar abre wa.me:', ba8open);
  // BA9: PDF bloqueado sin firma del técnico y sin firma del usuario; con
  // ambas, PDF con encabezado, secciones, ids en Descripción y en
  // Observaciones, firmas y satisfacción; imágenes JPEG incrustadas.
  var mBA9 = mkMant({ id: 'ba9', folio: '00001', estado: 'creada' });
  mBA9.firmaTecnico = '';
  var ba9sinTec = mantPdfFalta(mBA9) === 'la firma del técnico';
  mBA9.firmaTecnico = 'data:image/png;base64,iVBORw0KGgo=';
  var ba9sinUsr = mantPdfFalta(mBA9) === 'la firma del usuario';
  mBA9.firma = { nombre: 'Ana López', area: 'Ventas', comentarios: 'Todo bien', satisfaccion: 9, firma: 'data:image/png;base64,iVBORw0KGgo=', firmadoEn: Date.now() };
  var ba9ok = mantPdfFalta(mBA9) === null;
  await sharePdfMant(mkMant({ id: 'ba9b', folio: '00002', estado: 'creada', firmaTecnico: '' }));
  var ba9toast = toastTxt().indexOf('firma del técnico') !== -1;
  var pdfBA9 = Buffer.from(await buildPdfMant(mBA9, {}).arrayBuffer()).toString('latin1');
  var ba9need = ['Lapi Sistemas', 'Rosa Blanca 63', 'ORDEN DE SERVICIO', 'Folio: 00001', 'Formato F0.S1.01 Rev0', 'Título del caso: Laptop lenta', 'Descripción del equipo', 'Observaciones', 'Datos detectados:', 'Procesador: Intel i5', 'Observaciones del técnico:', 'Sin observaciones', 'Conformidad del usuario', 'Ana López', 'Escala de satisfacción', '9 \\(EXCELENTE\\)', '[9]', 'INACEPTABLE 0-3', 'Políticas: cambio cada 90 días', 'Firma: Test User \\(guardada en la app\\)', 'Firma: Ana López \\(guardada en la app\\)'];
  var ba9pdf = ba9need.every(function (s) { return pdfBA9.indexOf(s) !== -1; }) && pdfBA9.indexOf('Sistemas') !== -1 && pdfBA9.indexOf('Planeación') !== -1 && pdfBA9.indexOf('Área solicitante') !== -1 && pdfBA9.indexOf('Liberación') !== -1;
  var ba9ambos = (pdfBA9.match(/Serie: S1/g) || []).length >= 2 && (pdfBA9.match(/Hostname: PC-01/g) || []).length >= 2 && (pdfBA9.match(/Modelo: Inspiron 3501/g) || []).length >= 2;
  var JPEG1X1 = '/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAP//////////////////////////////////////////////////////////////////////////////////////2wBDAf//////////////////////////////////////////////////////////////////////////////////////wAARCAABAAEDASIAAhEBAxEB/8QAFAABAAAAAAAAAAAAAAAAAAAACf/EABQQAQAAAAAAAAAAAAAAAAAAAAD/xAAUAQEAAAAAAAAAAAAAAAAAAAAA/8QAFBEBAAAAAAAAAAAAAAAAAAAAAP/aAAwDAQACEQMRAD8AvwH/2Q==';
  var jpgBytes = new Uint8Array(Buffer.from(JPEG1X1, 'base64'));
  var pdfImg = Buffer.from(await buildPdfMant(mBA9, { tecnico: { bytes: jpgBytes, w: 1, h: 1 }, usuario: { bytes: jpgBytes, w: 1, h: 1 } }).arrayBuffer()).toString('latin1');
  var ba9img = pdfImg.indexOf('/Subtype /Image') !== -1 && pdfImg.indexOf('/DCTDecode') !== -1 && pdfImg.indexOf('/Imtecnico Do') !== -1 && pdfImg.indexOf('/Imusuario Do') !== -1 && (pdfImg.match(/\/Subtype \/Image/g) || []).length === 2;
  console.log('BA9) sin firma técnico bloquea:', ba9sinTec, '| sin firma usuario bloquea:', ba9sinUsr, '| con ambas listo:', ba9ok, '| botón avisa con toast:', ba9toast, '| PDF con todo:', ba9pdf, '| ids en Descripción y en Observaciones:', ba9ambos, '| firmas JPEG incrustadas:', ba9img);
  // BA10: compartir copia solo con ambas firmas (botón deshabilitado sin
  // la del usuario; share nativo con el PDF cuando están las dos).
  var mBA10 = mkMant({ id: 'ba10', folio: '00004', estado: 'creada', firmaTecnico: 'data:image/png;base64,iVBORw0KGgo=' });
  mantenimientos = [mBA10];
  mantShowOrder('ba10');
  var ba10dis = document.getElementById('btnMantCompartir').disabled === true && document.getElementById('mantOrderNote').textContent.indexOf('firma del usuario') !== -1;
  await shareMantCopy(mBA10);
  var ba10toast = toastTxt().indexOf('firma del usuario') !== -1;
  mBA10.firma = { nombre: 'Ana López', area: 'Ventas', comentarios: '', satisfaccion: 8, firma: 'data:image/png;base64,iVBORw0KGgo=', firmadoEn: Date.now() };
  var sharedBA10 = [];
  global.Capacitor = { Plugins: { Filesystem: { writeFile: async function (o) { return { uri: 'file:///cache/' + o.path }; } }, Share: { share: async function (o) { sharedBA10.push(o); } } } };
  global.FileReader = class { constructor() { this.result = null; } readAsDataURL(blob) { var self = this; blob.arrayBuffer().then(function (ab) { self.result = 'data:application/pdf;base64,' + Buffer.from(ab).toString('base64'); if (self.onload) self.onload(); }); } };
  mantShowOrder('ba10');
  var ba10en = document.getElementById('btnMantCompartir').disabled === false;
  await shareMantCopy(mBA10);
  var ba10share = sharedBA10.length === 1 && sharedBA10[0].url === 'file:///cache/orden-servicio-00004.pdf' && sharedBA10[0].dialogTitle === 'Compartir copia con el usuario';
  console.log('BA10) sin firma usuario: botón deshabilitado y nota:', ba10dis, '| intento avisa con toast:', ba10toast, '| con ambas: botón habilitado:', ba10en, '| share nativo con el PDF:', ba10share);
  // BA11: visibilidad — el usuario normal solo ve los suyos (con respaldo
  // por nombre para registros viejos); el admin ve todos y filtra por usuario.
  teamUsers = [
    { uid: 'u1', nombre: 'Test User', rol: 'usuario', email: 'test@checklist.local' },
    { uid: 'uAxel', nombre: 'Axel Danyael', rol: 'usuario', email: 'axel@checklist.local' },
    { uid: 'uAle', nombre: 'Alejandro', rol: 'usuario', email: 'alejandro@checklist.local' },
  ];
  mantenimientos = [
    mkMant({ id: 'ba11-own', tecnicoUid: 'u1', tecnico: 'Test User', tituloCaso: 'Mío' }),
    mkMant({ id: 'ba11-axel', tecnicoUid: 'uAxel', tecnico: 'Axel Danyael', tituloCaso: 'De Axel' }),
    mkMant({ id: 'ba11-old', tecnicoUid: '', tecnico: 'Test User', tituloCaso: 'Viejo sin uid' }),
  ];
  loginAs('u1', 'Test User', 'usuario');
  renderMant();
  var htmlU = document.getElementById('mantList').innerHTML;
  var ba11u = htmlU.indexOf('Mío') !== -1 && htmlU.indexOf('De Axel') === -1 && htmlU.indexOf('Viejo sin uid') !== -1 && document.getElementById('mantAdminRow').hidden === true;
  loginAs('uGer', 'Gerardo', 'admin');
  mantAdminViewUid = 'todos';
  renderMant();
  var htmlA = document.getElementById('mantList').innerHTML;
  var ba11a = htmlA.indexOf('Mío') !== -1 && htmlA.indexOf('De Axel') !== -1 && htmlA.indexOf('Viejo sin uid') !== -1 && document.getElementById('mantAdminRow').hidden === false;
  mantAdminViewUid = 'uAxel';
  renderMant();
  var htmlAx = document.getElementById('mantList').innerHTML;
  var ba11ax = htmlAx.indexOf('De Axel') !== -1 && htmlAx.indexOf('Mío') === -1;
  mantAdminViewUid = 'todos';
  var ba11noToggle = html.indexOf('Ver mantenimientos de otros') === -1 && !html.includes('btnVerOtrosMant');
  console.log('BA11) usuario solo ve los suyos (+ respaldo por nombre):', ba11u, '| admin ve todos:', ba11a, '| admin filtra por analista:', ba11ax, '| sin toggle de ver otros:', ba11noToggle);
  // BA12: cancelar orden conserva el registro y el folio.
  var mBA12 = mkMant({ id: 'ba12', folio: '00005', estado: 'creada', tituloCaso: 'Para cancelar' });
  mantenimientos = [mBA12];
  loginAs('u1', 'Test User', 'usuario');
  var btnBA12 = {
    getAttribute: function (a) { return a === 'data-mant-cancel-order' ? 'ba12' : null; },
    hasAttribute: function (a) { return a === 'data-mant-cancel-order'; },
    closest: function (sel) { return sel === '[data-mant-cancel-order]' ? btnBA12 : null; },
    classList: { contains: function () { return false; } }
  };
  document.getElementById('mantList')._h.click[0]({ target: btnBA12 });
  var ba12modal = document.getElementById('confirmModal').hidden === false && document.getElementById('confirmMsg').textContent.indexOf('00005') !== -1;
  answerConfirm(false);
  await sleep(20);
  var ba12no = mantenimientos[0].estado === 'creada';
  document.getElementById('mantList')._h.click[0]({ target: btnBA12 });
  answerConfirm(true);
  await sleep(20);
  var ba12si = mantenimientos[0].estado === 'cancelada' && mantenimientos[0].folio === '00005' && mantenimientos.length === 1;
  console.log('BA12) cancelar pide confirmar con el folio:', ba12modal, '| con No no cancela:', ba12no, '| con Sí cancela y conserva folio:', ba12si);
  // BA13: serie, hostname y modelo arriba de la tarjeta y del formulario.
  var mBA13 = mkMant({ id: 'ba13', tituloCaso: 'Tarjeta ids' });
  var cardBA13 = mantCardHtml(mBA13);
  var ba13card = cardBA13.indexOf('Serie: S1 · Hostname: PC-01 · Modelo: Inspiron 3501') !== -1 && cardBA13.indexOf('mant-id-line') !== -1 && cardBA13.indexOf('mant-id-line') < cardBA13.indexOf('Técnico:');
  var ba13hero = html.indexOf('mant-hero') !== -1 && html.indexOf('id="fM-serie"') < html.indexOf('id="fM-tecnico"') && html.indexOf('id="fM-hostname"') < html.indexOf('id="fM-tecnico"') && html.indexOf('id="fM-modelo"') < html.indexOf('id="fM-tecnico"') && html.includes('No. de serie *') && html.includes('Hostname *') && html.includes('Modelo *');
  console.log('BA13) tarjeta con serie/host/modelo arriba:', ba13card, '| formulario con cuadro destacado arriba:', ba13hero);
  // BA14: al entrar, la suscripción filtra por tecnicoUid para usuarios
  // normales y sin filtro para el admin; el login cae en el selector.
  var subBA14 = [];
  global.Cloud.subscribeMantenimientos = function (cb, uid) { subBA14.push(uid); return function () {}; };
  global.Cloud.subscribeRenta = function () { return function () {}; };
  global.Cloud.subscribePreparations = function () { return function () {}; };
  global.Cloud.subscribeDetectados = function () { return function () {}; };
  global.Cloud.subscribePresence = function () { return function () {}; };
  global.Cloud.subscribeChat = function () { return function () {}; };
  global.Cloud.subscribeDm = function () { return function () {}; };
  global.Cloud.heartbeat = function () {};
  global.Cloud.pruneChat = function () {};
  global.Cloud.clearPresence = function () {};
  global.Cloud.listUsers = async function () { return []; };
  global.Cloud.getAllMantenimientos = async function () { return []; };
  global.Cloud.getUserDoc = async function () { return { activo: true, rol: 'usuario', nombre: 'Test User', email: 'test@checklist.local' }; };
  localStorage.setItem('checklist-soporte-migrado-v2:u1', '1');
  localStorage.setItem('checklist-soporte-migrado-preps-v1:u1', '1');
  localStorage.setItem('checklist-soporte-migrado-mant-v1:u1', '1');
  await onAuthChanged({ uid: 'u1', email: 'test@checklist.local' });
  await sleep(20);
  var ba14user = subBA14.length === 1 && subBA14[0] === 'u1' && document.getElementById('viewInicio').hidden === false;
  global.Cloud.getUserDoc = async function () { return { activo: true, rol: 'admin', nombre: 'Gerardo', email: 'gerardo@checklist.local' }; };
  localStorage.setItem('checklist-soporte-migrado-v2:uGer', '1');
  localStorage.setItem('checklist-soporte-migrado-preps-v1:uGer', '1');
  localStorage.setItem('checklist-soporte-migrado-mant-v1:uGer', '1');
  subBA14.length = 0;
  await onAuthChanged({ uid: 'uGer', email: 'gerardo@checklist.local' });
  await sleep(20);
  var ba14admin = subBA14.length === 1 && subBA14[0] === null;
  console.log('BA14) usuario suscribe solo sus mantenimientos y cae en el selector:', ba14user, '| admin suscribe todo:', ba14admin);
  // BA15: el técnico se pre-llena con el login y lo escrito a mano se respeta.
  loginAs('u1', 'Test User', 'usuario');
  mantOpenForm(null, null);
  var ba15auto = document.getElementById('fM-tecnico').value === 'Test User';
  document.getElementById('fM-tecnico').value = 'Otro Nombre';
  prefillMantTecnico();
  var ba15manual = document.getElementById('fM-tecnico').value === 'Otro Nombre';
  document.getElementById('fM-tecnico').value = '';
  prefillMantTecnico();
  var ba15refill = document.getElementById('fM-tecnico').value === 'Test User';
  console.log('BA15) técnico auto con el login:', ba15auto, '| escrito a mano se respeta:', ba15manual, '| vacío se vuelve a llenar:', ba15refill);
  // BA16: cancelar el formulario pide confirmar solo si tiene datos.
  mantOpenForm(null, null);
  document.getElementById('fM-titulo').value = 'Algo';
  document.getElementById('btnMantCancelar')._h.click[0]();
  var ba16modal = document.getElementById('confirmModal').hidden === false;
  answerConfirm(false);
  await sleep(20);
  var ba16no = document.getElementById('mantFormBox').hidden === false;
  document.getElementById('btnMantCancelar')._h.click[0]();
  answerConfirm(true);
  await sleep(20);
  var ba16si = document.getElementById('mantFormBox').hidden === true;
  mantOpenForm(null, null);
  document.getElementById('btnMantCancelar')._h.click[0]();
  var ba16vacio = document.getElementById('mantFormBox').hidden === true && document.getElementById('confirmModal').hidden === true;
  console.log('BA16) con datos pide confirmar:', ba16modal, '| con No sigue abierto:', ba16no, '| con Sí se descarta:', ba16si, '| vacío se cierra sin preguntar:', ba16vacio);
  // BA17: ida y vuelta a la nube + la firma de más de 700 KB no viaja.
  var mBA17 = mkMant();
  mBA17.firmaTecnico = 'x'.repeat(700001);
  var docBA17 = mantToCloudDoc(mBA17);
  var backBA17 = mantFromCloud(docBA17);
  var ba17 = docBA17.firmaTecnico === '' && backBA17.firmaTecnico === '' && backBA17.equipo.serie === 'S1' && backBA17.equipo.politicas.cumple === true && backBA17.identificacion.impresora === true && backBA17.condiciones.notas === '' && backBA17.firma === null && docBA17.folio === null;
  var mBA17b = mkMant();
  mBA17b.firmaTecnico = 'data:image/png;base64,abc';
  var ba17b = mantToCloudDoc(mBA17b).firmaTecnico === 'data:image/png;base64,abc';
  console.log('BA17) firma >700KB no viaja y el resto vuelve intacto:', ba17, '| firma pequeña sí viaja:', ba17b);
  // BA18: reglas exactas de mantenimientos y folios.
  var ba18 = rules.includes('allow list: if isActive() && (isAdmin() || resource.data.tecnicoUid == request.auth.uid)') && rules.includes("changedKeys().hasOnly(['firma', 'estado'])") && rules.includes("request.resource.data.estado == 'firmada'") && rules.includes('match /config/folios') && rules.includes('request.resource.data.siguiente == resource.data.siguiente + 1') && rules.includes('allow create: if isActive() && request.resource.data.siguiente is int');
  console.log('BA18) reglas: lista propia/admin, firma pública solo firma+estado, folios +1:', ba18);
'''

anchor = "  process.exit(0);"
assert s.count(anchor) == 1, 'ancla process.exit no encontrada'
s = s.replace(anchor, BA + anchor)
io.open(P, 'w', encoding='utf-8').write(s)
print('test20250.js OK')
