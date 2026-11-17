  // 255: serie nueva 2.5.5 — responsable/área no obligatorios, campo en
  // rojo, gpedit, PDF con solo hostname en Descripción y carta, renta.
  // 255A: crear orden sin responsable ni área pasa la validación; con la
  // firma llegada, la vista y el PDF muestran firma.nombre/area y el
  // write-back los guarda; sin firma, la vista dice "Pendiente de firma".
  loginAs('u1', 'Test User', 'usuario');
  CLOUD_ENABLED = true;
  fillMantFormBA('S-255A', 'PC-255A', 'Modelo 255A');
  document.getElementById('fM-area').value = '';
  document.getElementById('fM-responsable').value = '';
  var m255aForm = mantReadForm();
  var a255sinResp = mantFaltantesCrear(m255aForm).length === 0 && mantFaltaCrear(m255aForm) === null;
  var nMant255a = mantenimientos.length;
  await mantCrearOrden();
  var m255aSaved = mantenimientos.find(function (x) { return x.equipo && x.equipo.serie === 'S-255A'; });
  var a255creada = !!m255aSaved && m255aSaved.responsable === '' && m255aSaved.area === '' && mantenimientos.length === nMant255a + 1 && toastTxt().indexOf('Falta') === -1;
  var upsertMant255 = [];
  global.Cloud.upsertMant = async function (doc) { upsertMant255.push(doc); return {}; };
  m255aSaved.firma = { nombre: 'Ana López', area: 'Ventas', comentarios: '', satisfaccion: 9, firma: 'data:image/png;base64,iVBORw0KGgo=', firmadoEn: Date.now() };
  var a255wbRet = mantFillFromFirma(m255aSaved);
  var a255wb = a255wbRet === true && m255aSaved.responsable === 'Ana López' && m255aSaved.area === 'Ventas' && upsertMant255.length === 1 && upsertMant255[0].responsable === 'Ana López' && upsertMant255[0].area === 'Ventas';
  var a255wbNoLoop = mantFillFromFirma(m255aSaved) === false && upsertMant255.length === 1;
  mantenimientos = [m255aSaved];
  mantShowOrder(m255aSaved.id);
  var a255vista = document.getElementById('mantOrderBody').innerHTML.indexOf('Responsable: Ana López') !== -1 && document.getElementById('mantOrderBody').innerHTML.indexOf('Área: Ventas') !== -1;
  var pdf255a = await pdfStrOf(m255aSaved);
  var a255pdf = pdf255a.indexOf('Ana López') !== -1 && pdf255a.indexOf('Ventas') !== -1;
  var m255aExt = mkMant({ id: 'ext255', tecnicoUid: 'uAxel', responsable: '', area: '', firma: null });
  m255aExt.firma = { nombre: 'Luis Pérez', area: 'Compras', comentarios: '', satisfaccion: 8, firma: 'data:image/png;base64,iVBORw0KGgo=', firmadoEn: Date.now() };
  var nUp255 = upsertMant255.length;
  var a255ext = mantFillFromFirma(m255aExt) === true && m255aExt.responsable === 'Luis Pérez' && upsertMant255.length === nUp255;
  mantenimientos = [m255aExt];
  mantShowOrder('ext255');
  var a255fb = document.getElementById('mantOrderBody').innerHTML.indexOf('Responsable: Luis Pérez') !== -1 && document.getElementById('mantOrderBody').innerHTML.indexOf('Área: Compras') !== -1;
  var pdf255afb = await pdfStrOf(m255aExt);
  var a255pdfFb = pdf255afb.indexOf('Luis P') !== -1 && pdf255afb.indexOf('Compras') !== -1;
  var m255aPend = mkMant({ id: 'pend255', responsable: '', area: '', firma: null });
  mantenimientos = [m255aPend];
  mantShowOrder('pend255');
  var bodyPend255 = document.getElementById('mantOrderBody').innerHTML;
  var a255pend = bodyPend255.indexOf('Área: Pendiente de firma') !== -1 && bodyPend255.indexOf('Responsable: Pendiente de firma') !== -1;
  delete global.Cloud.upsertMant;
  console.log('255A) crear sin responsable/área pasa validación:', a255sinResp, '| orden creada sin ellos:', a255creada, '| write-back guarda firma:', a255wb, '| sin reescritura en bucle:', a255wbNoLoop, '| vista muestra firma:', a255vista, '| PDF muestra firma:', a255pdf, '| orden ajena se llena local sin subir:', a255ext, '| fallback en vista:', a255fb, '| fallback en PDF:', a255pdfFb, '| sin firma dice Pendiente de firma:', a255pend);
  // 255B: validación fallida marca en rojo exactamente los campos vacíos
  // obligatorios y el toast los nombra; al escribir se quita la marca.
  loginAs('u1', 'Test User', 'usuario');
  mantOpenForm(null, null);
  document.getElementById('fM-serie').value = 'S-255B';
  document.getElementById('fM-modelo').value = 'Modelo 255B';
  document.getElementById('fM-hostname').value = '';
  document.getElementById('fM-titulo').value = '';
  document.getElementById('fM-tipoFalla').value = '';
  document.getElementById('fM-descEquipo').value = '';
  document.getElementById('fM-fechaServ').value = '';
  document.getElementById('fM-whatsapp').value = '';
  mantFirmaData = '';
  // El harness devuelve [] en querySelectorAll, así que las marcas viejas
  // de BA5 (serie/modelo) no se limpian solas como en la app real; se
  // quitan a mano para comprobar que ESTA llamada marca exactamente los 7.
  ['fM-serie', 'fM-hostname', 'fM-modelo', 'fM-titulo', 'fM-tipoFalla', 'fM-descEquipo', 'fM-fechaServ', 'fM-whatsapp', 'fM-firmaCanvas', 'fM-area', 'fM-responsable', 'fM-tipo-sw', 'fM-tipo-hw'].forEach(function (id) { document.getElementById(id).classList.remove('campo-falta'); });
  var nMant255b = mantenimientos.length;
  await mantCrearOrden();
  var b255ids = ['fM-hostname', 'fM-titulo', 'fM-tipoFalla', 'fM-descEquipo', 'fM-fechaServ', 'fM-whatsapp', 'fM-firmaCanvas'];
  var b255marcados = b255ids.every(function (id) { return document.getElementById(id).classList.contains('campo-falta'); });
  var b255noExtras = ['fM-serie', 'fM-modelo', 'fM-area', 'fM-responsable', 'fM-tipo-sw', 'fM-tipo-hw'].every(function (id) { return !document.getElementById(id).classList.contains('campo-falta'); });
  var b255toast = toastTxt().indexOf('hostname') !== -1 && toastTxt().indexOf('título del caso') !== -1 && toastTxt().indexOf('tipo de falla') !== -1 && toastTxt().indexOf('descripción del equipo') !== -1 && toastTxt().indexOf('fecha del servicio') !== -1 && toastTxt().indexOf('WhatsApp') !== -1 && toastTxt().indexOf('firma del técnico') !== -1;
  var b255noCrea = mantenimientos.length === nMant255b;
  document.getElementById('mantFormBox')._h.input[0]({ target: document.getElementById('fM-hostname') });
  var b255quita = !document.getElementById('fM-hostname').classList.contains('campo-falta') && document.getElementById('fM-titulo').classList.contains('campo-falta');
  document.getElementById('fM-hostname').value = 'PC-255B';
  document.getElementById('fM-titulo').value = 'Caso 255B';
  document.getElementById('fM-tipoFalla').value = 'Software';
  document.getElementById('fM-descEquipo').value = 'Equipo 255B';
  document.getElementById('fM-fechaServ').value = '2026-11-16';
  document.getElementById('fM-whatsapp').value = '5512345678';
  mantFirmaData = 'data:image/png;base64,iVBORw0KGgo=';
  document.getElementById('fM-tipo-sw').checked = false;
  document.getElementById('fM-tipo-hw').checked = false;
  await mantCrearOrden();
  var b255tipo = document.getElementById('fM-tipo-sw').classList.contains('campo-falta') && document.getElementById('fM-tipo-hw').classList.contains('campo-falta') && toastTxt().indexOf('tipo de mantenimiento') !== -1;
  document.getElementById('mantFormBox')._h.change[0]({ target: document.getElementById('fM-tipo-sw') });
  var b255tipoQuita = !document.getElementById('fM-tipo-sw').classList.contains('campo-falta') && !document.getElementById('fM-tipo-hw').classList.contains('campo-falta');
  console.log('255B) marca en rojo los 7 vacíos:', b255marcados, '| no marca los llenos ni área/responsable:', b255noExtras, '| toast los nombra:', b255toast, '| no crea la orden:', b255noCrea, '| al escribir se quita solo esa marca:', b255quita, '| tipo vacío marca ambos:', b255tipo, '| al cambiar uno se quitan ambos:', b255tipoQuita);
  // 255C: políticas del detector con bloqueo manual y fuente gpedit en el teléfono.
  var pol255 = { cambioDias: 60, minLongitud: 12, bloqueoIntentos: 3, bloqueoSegundos: 0, bloqueoManual: true };
  var c255 = mantPoliticasCumple(pol255);
  var c255manual = c255.cumpleBloqueo === true && c255.cumple === true && c255.bloqueoManual === true;
  var c255txt = politicasText(pol255).indexOf('bloqueo hasta desbloqueo manual ✓') !== -1;
  var det255 = { tipo: 'Laptop', marca: 'Dell', modelo: 'ProBook', serie: 'S-DET', hostname: 'PC-DET', detalles: { politicas: pol255, politicasFuente: 'gpedit (Registry.pol) + directiva (secedit)' } };
  var m255c = mantFromDetectado(det255);
  var c255det = m255c.equipo.politicas.bloqueoManual === true && m255c.equipo.politicasFuente === 'gpedit (Registry.pol) + directiva (secedit)' && politicasText(m255c.equipo.politicas).indexOf('bloqueo hasta desbloqueo manual ✓') !== -1;
  var c255reg = mantPoliticasCumple({ cambioDias: 90, minLongitud: 10, bloqueoIntentos: 5, bloqueoSegundos: 300 }).cumpleBloqueo === false;
  console.log('255C) bloqueo manual cumple en el teléfono:', c255manual, '| texto manual:', c255txt, '| detectado conserva manual y fuente:', c255det, '| umbrales sin cambio (300 s no cumple):', c255reg);
  // 255D: PDF de mantenimiento en carta, Descripción solo hostname, los
  // demás datos al final en Conclusión; el PDF de preparación sigue en A4.
  var m255d = mkMant({});
  var pdf255d = await pdfStrOf(m255d);
  var d255carta = pdf255d.indexOf('/MediaBox [0 0 612 792]') !== -1 && pdf255d.indexOf('/MediaBox [0 0 595 842]') === -1;
  var d255pag = (pdf255d.match(/\/Type \/Page[^s]/g) || []).length === 1;
  var rows255d = pdfTextRows(pdf255d);
  function rowIdx255(txt) { for (var i = 0; i < rows255d.length; i++) if (rows255d[i].t.indexOf(txt) !== -1) return i; return -1; }
  var iDesc255 = rowIdx255('DESCRIPCIÓN DEL EQUIPO');
  var iHost255 = rowIdx255('Hostname: PC-01');
  var iCond255 = rowIdx255('CONDICIONES GENERALES');
  var iConcl255 = rowIdx255('CONCLUSIÓN Y/O COMENTARIOS');
  var iSerie255 = rowIdx255('Serie: S1, Modelo: Inspiron 3501');
  var d255soloHost = iDesc255 !== -1 && iHost255 === iDesc255 + 1 && iHost255 < iCond255;
  var d255alFinal = iConcl255 !== -1 && iSerie255 > iConcl255;
  var d255datos = pdf255d.indexOf('Procesador: Intel Core i5') !== -1 && pdf255d.indexOf('192.168.1.45') !== -1 && pdf255d.indexOf('HP LaserJet') !== -1 && pdf255d.indexOf('123 456 789') !== -1 && pdf255d.indexOf('Windows 11 Pro 26H2') !== -1 && pdf255d.indexOf('Políticas:') !== -1 && pdf255d.indexOf('Usuario de sistemas:') !== -1 && pdf255d.indexOf('Descripción: Laptop Dell Inspiron') !== -1;
  var d255casillas = (pdf255d.match(/\(X\)/g) || []).length === 14;
  var pdfPrep255 = Buffer.from(await buildPdf(mkPrep({})).arrayBuffer()).toString('latin1');
  var d255prepA4 = pdfPrep255.indexOf('/MediaBox [0 0 595 842]') !== -1 && pdfPrep255.indexOf('/MediaBox [0 0 612 792]') === -1;
  console.log('255D) MediaBox carta 612x792:', d255carta, '| 1 página:', d255pag, '| Descripción solo hostname:', d255soloHost, '| serie/modelo al final en Conclusión:', d255alFinal, '| ningún dato perdido:', d255datos, '| 14 casillas:', d255casillas, '| preparación sigue en A4:', d255prepA4);
  // 255E: regresión serie 254 (Actualizar, guardado de PDF con Capacitor,
  // formato de papel, bloqueo por usuario).
  var m255e = mkMant({ id: 'e255', folio: '00001', estado: 'creada', firmaTecnico: 'data:image/png;base64,iVBORw0KGgo=' });
  mantenimientos = [m255e];
  mantShowOrder('e255');
  var e255btn = (document.getElementById('btnMantActualizar')._h.click || []).length >= 1;
  var signed255e = mkMant({ id: 'e255', folio: '00001', estado: 'firmada', firmaTecnico: 'data:image/png;base64,iVBORw0KGgo=' });
  signed255e.firma = { nombre: 'Ana López', area: 'Ventas', comentarios: '', satisfaccion: 9, firma: 'data:image/png;base64,iVBORw0KGgo=', firmadoEn: Date.now() };
  global.Cloud.getMantenimiento = async function () { return signed255e; };
  await mantActualizarOrden();
  var e255act = toastTxt().indexOf('El usuario ya firmó') !== -1 && mantenimientos[0].firma && mantenimientos[0].firma.nombre === 'Ana López';
  delete global.Cloud.getMantenimiento;
  var m255eb = mkMant({ id: 'eb255', folio: '00001', estado: 'creada', firmaTecnico: 'data:image/png;base64,iVBORw0KGgo=' });
  m255eb.firma = { nombre: 'Ana López', area: 'Ventas', comentarios: '', satisfaccion: 9, firma: 'data:image/png;base64,iVBORw0KGgo=', firmadoEn: Date.now() };
  var cap255 = { write: [], stat: [], open: [] };
  global.Capacitor = { getPlatform: function () { return 'android'; }, Plugins: { Filesystem: { writeFile: async function (o) { cap255.write.push(o); return { uri: 'file:///documents/' + o.path }; }, stat: async function (o) { cap255.stat.push(o); return { uri: 'file:///documents/' + o.path, size: 1234 }; } }, FileOpener: { open: async function (o) { cap255.open.push(o); } }, Share: { share: async function () {} } } };
  await sharePdfMant(m255eb);
  var e255pdf = cap255.write.length === 1 && cap255.write[0].directory === 'DOCUMENTS' && cap255.stat.length === 1 && cap255.open.length === 1 && toastTxt().indexOf('PDF guardado: orden-servicio-00001.pdf (en Documentos).') !== -1;
  global.Capacitor = undefined;
  var pdfLudi255 = await pdfStrOf(mkMant({ empresa: 'Ludi' }));
  var e255fmt = pdfLudi255.indexOf('Ludi') !== -1 && pdfLudi255.indexOf('Rosa Blanca 63') === -1 && (pdfLudi255.match(/\(X\)/g) || []).length === 14;
  users254[2].mantBloqueado = false;
  blkCalls254.length = 0;
  loginAs('uAdmin', 'Gerardo', 'admin');
  await renderUsuarios();
  var box255e = document.getElementById('userList').innerHTML;
  var e255btns = box255e.indexOf('data-user-mantblock="u1"') !== -1 && box255e.indexOf('data-user-mantblock="uAdmin"') === -1;
  clickUser254('u1');
  await sleep(20);
  var e255blk = blkCalls254.length === 1 && blkCalls254[0][0] === 'u1' && blkCalls254[0][1] === true;
  loginAs('u1', 'Test User', 'usuario');
  cloudUser.mantBloqueado = true;
  refreshMantAccess();
  showVista('mant');
  var e255fuera = document.getElementById('viewInicio').hidden === false && document.getElementById('viewMant').hidden === true && toastTxt().indexOf('bloqueado') !== -1;
  loginAs('uAdmin', 'Gerardo', 'admin');
  cloudUser.mantBloqueado = true;
  showVista('mant');
  var e255admin = document.getElementById('viewMant').hidden === false;
  console.log('255E) Actualizar existe y re-renderiza con firma:', e255btn && e255act, '| PDF Capacitor en Documentos:', e255pdf, '| formato Ludi sin contacto y 14 casillas:', e255fmt, '| bloqueo: botón solo en usuario y clic bloquea:', e255btns && e255blk, '| bloqueado fuera, admin entra:', e255fuera && e255admin);
  // 255F: punto 6 — Exportar a Excel aparece en Recibir y Entrega renta
  // y el constructor del Excel agrupa por tipo con sus columnas.
  var f255html = html.indexOf('id="btnAbrirRec">📊 Exportar a Excel') !== -1 && html.indexOf('id="btnAbrirFor">📊 Exportar a Excel') !== -1;
  state.renta = [{ id: 'r255f', flujo: 'rec', tipo: 'Laptop', modelo: 'ProBook 440', inventario: 'INV-1', accesorios: { cargador: true, mouse: true, maletin: true }, sinDanos: true, danos: '', obs: '', estado: 'recibido', recibidoPor: 'Test User', entregadoPor: '', entregadoAt: null, creadoPor: null, createdAt: Date.now(), fotoDanos: null, danosIA: '' }];
  render();
  var f255btn = document.getElementById('btnAbrirRec').disabled === false;
  var blob255f = buildXlsxRenta(state.renta, 'rec');
  var txt255f = new TextDecoder().decode(await blob255f.arrayBuffer());
  var f255xlsx = txt255f.indexOf('Recibir renta') !== -1 && txt255f.indexOf('*INV-1*') !== -1 && txt255f.indexOf('PROBOOK 440') !== -1 && txt255f.indexOf('Test User') !== -1 && txt255f.indexOf('# Inventario') !== -1 && txt255f.indexOf('Laptop') !== -1;
  var blob255fFor = buildXlsxRenta([{ id: 'r255f2', flujo: 'rec', tipo: 'iPad', modelo: 'iPad 2 Air', inventario: 'INV-9', capacidad: '16 GB', accesorios: {}, sinDanos: true, danos: '', obs: '', estado: 'entregado', recibidoPor: 'Test User', entregadoPor: 'Test User', entregadoAt: Date.now(), creadoPor: null, createdAt: Date.now(), fotoDanos: null, danosIA: '' }], 'for');
  var txt255fFor = new TextDecoder().decode(await blob255fFor.arrayBuffer());
  var f255ipad = txt255fFor.indexOf('Entrega Renta') !== -1 && txt255fFor.indexOf('*INV-9*') !== -1 && txt255fFor.indexOf('IPAD 2 AIR') !== -1;
  state.renta = [];
  render();
  var f255vacio = document.getElementById('btnAbrirRec').disabled === true && document.getElementById('btnAbrirFor').disabled === true;
  console.log('255F) botón Exportar a Excel en ambas vistas:', f255html, '| habilitado con datos:', f255btn, '| Excel Recibir agrupa Laptop con inventario y analista:', f255xlsx, '| Excel Entrega agrupa iPad:', f255ipad, '| deshabilitado sin datos:', f255vacio);
  // 255G: punto 7 — selección y 15 días en Entrega Renta.
  loginAs('u1', 'Test User', 'usuario');
  CLOUD_ENABLED = true;
  global.Cloud.upsertRenta = async function () { return {}; };
  var T255g = Date.now();
  function mkRenta255(id, estado, daysAgo, entregadoPor) {
    return { id: id, flujo: 'rec', tipo: 'Laptop', modelo: 'Modelo ' + id, inventario: 'INV-' + id, accesorios: {}, sinDanos: true, danos: '', obs: '', estado: estado, recibidoPor: 'Test User', entregadoPor: entregadoPor || '', entregadoAt: estado === 'entregado' ? T255g - daysAgo * 86400000 : null, creadoPor: null, createdAt: T255g - daysAgo * 86400000, fotoDanos: null, danosIA: '' };
  }
  function clickListFor255(target) { document.getElementById('list-for')._h.click[0]({ target: target }); }
  state.renta = [
    mkRenta255('g1', 'entregado', 10, 'Test User'),
    mkRenta255('g2', 'entregado', 16, 'Test User'),
    mkRenta255('g3', 'entregado', 2, 'Test User'),
    mkRenta255('g4', 'recibido', 1, ''),
  ];
  render();
  var g255vis10 = rentaList('for').some(function (r) { return r.id === 'g1'; });
  var g255hid16 = !rentaList('for').some(function (r) { return r.id === 'g2'; });
  var g255cola = entregaCola().some(function (r) { return r.id === 'g1'; }) && !entregaCola().some(function (r) { return r.id === 'g2'; });
  loginAs('uAdmin', 'Gerardo', 'admin');
  var g255admin = rentaList('for').some(function (r) { return r.id === 'g2'; });
  loginAs('u1', 'Test User', 'usuario');
  var g5 = mkRenta255('g5', 'entregado', 0, 'Test User');
  g5.entregadoAt = null; g5.createdAt = T255g - 20 * 86400000;
  state.renta.push(g5);
  var g255fbViejo = !rentaList('for').some(function (r) { return r.id === 'g5'; });
  var g6 = mkRenta255('g6', 'entregado', 0, 'Test User');
  g6.entregadoAt = null; g6.createdAt = T255g - 10 * 86400000;
  state.renta.push(g6);
  var g255fbNuevo = rentaList('for').some(function (r) { return r.id === 'g6'; });
  var g4 = state.renta.find(function (r) { return r.id === 'g4'; });
  var btnDel255 = { getAttribute: function (a) { return a === 'data-renta-deliver' ? 'g4' : null; } };
  clickListFor255({ closest: function (sel) { return sel === '[data-renta-deliver]' ? btnDel255 : null; }, hasAttribute: function (a) { return a === 'data-renta-deliver'; } });
  var g255at = g4.estado === 'entregado' && typeof g4.entregadoAt === 'number' && Math.abs(g4.entregadoAt - Date.now()) < 60000 && g4.entregadoPor === 'Test User';
  var btnRe255 = { getAttribute: function (a) { return a === 'data-renta-reopen' ? 'g4' : null; } };
  clickListFor255({ closest: function (sel) { return sel === '[data-renta-reopen]' ? btnRe255 : null; }, hasAttribute: function (a) { return a === 'data-renta-reopen'; } });
  var g255re = g4.estado === 'revisado' && g4.entregadoAt === null && g4.entregadoPor === '';
  state.renta = [
    mkRenta255('s1', 'entregado', 1, 'Test User'),
    mkRenta255('s2', 'entregado', 1, 'Test User'),
    mkRenta255('s3', 'entregado', 1, 'Test User'),
  ];
  render();
  var listForHtml255 = document.getElementById('list-for').innerHTML;
  var g255checks = (listForHtml255.match(/data-renta-sel="/g) || []).length === 3 && listForHtml255.indexOf('data-renta-sel-all') !== -1 && listForHtml255.indexOf('data-renta-sel-none') !== -1;
  var g255btnFor = document.getElementById('btnAbrirFor').disabled === false;
  function changeSel255(id, checked) {
    var cb = { getAttribute: function (a) { return a === 'data-renta-sel' ? id : null; }, checked: checked, closest: function (sel) { return sel === '[data-renta-sel]' ? cb : null; } };
    document.getElementById('list-for')._h.change[0]({ target: cb });
  }
  changeSel255('s1', true);
  changeSel255('s3', true);
  var sel255 = rentaSelListFor();
  var g255sel = sel255.sel.length === 2 && sel255.sel.some(function (r) { return r.id === 's1'; }) && sel255.sel.some(function (r) { return r.id === 's3'; });
  var g255info = document.getElementById('rentaSelInfo').textContent.indexOf('Seleccionados: 2 de 3') !== -1;
  var lastBlob255 = null;
  global.URL.createObjectURL = function (b) { lastBlob255 = b; return 'blob:x'; };
  global.open = function () { return null; };
  await openXlsxRenta('for');
  var txtSel255 = new TextDecoder().decode(await lastBlob255.arrayBuffer());
  var g255expSel = txtSel255.indexOf('*INV-s1*') !== -1 && txtSel255.indexOf('*INV-s3*') !== -1 && txtSel255.indexOf('*INV-s2*') === -1;
  clickListFor255({ closest: function (sel) { return sel === '[data-renta-sel-all]' ? { getAttribute: function () { return ''; } } : null; } });
  var g255all = rentaSelListFor().sel.length === 3;
  clickListFor255({ closest: function (sel) { return sel === '[data-renta-sel-none]' ? { getAttribute: function () { return ''; } } : null; } });
  var g255none = rentaSelListFor().sel.length === 0;
  await openXlsxRenta('for');
  var g255todos = toastTxt().indexOf('Sin selección: se exportan todos los equipos entregados.') !== -1;
  var txtTodos255 = new TextDecoder().decode(await lastBlob255.arrayBuffer());
  var g255expTodos = txtTodos255.indexOf('*INV-s1*') !== -1 && txtTodos255.indexOf('*INV-s2*') !== -1 && txtTodos255.indexOf('*INV-s3*') !== -1;
  var capShare255 = { write: [], share: [] };
  global.Capacitor = { getPlatform: function () { return 'android'; }, Plugins: { Filesystem: { writeFile: async function (o) { capShare255.write.push(o); return { uri: 'file:///cache/' + o.path }; } }, Share: { share: async function (o) { capShare255.share.push(o); } } } };
  changeSel255('s2', true);
  await shareRentaFile('for', 'wa');
  var txtShare255 = Buffer.from(capShare255.write[0].data, 'base64').toString('latin1');
  var g255shareSel = capShare255.share.length === 1 && txtShare255.indexOf('*INV-s2*') !== -1 && txtShare255.indexOf('*INV-s1*') === -1 && txtShare255.indexOf('*INV-s3*') === -1;
  global.Capacitor = undefined;
  delete global.Cloud.upsertRenta;
  console.log('255G) entregado hace 10 días visible:', g255vis10, '| hace 16 días oculto:', g255hid16, '| mismo filtro en la cola:', g255cola, '| admin ve el de 16 días:', g255admin, '| sin entregadoAt usa createdAt (20 días oculto):', g255fbViejo, '| (10 días visible):', g255fbNuevo, '| entregadoAt se guarda al entregar:', g255at, '| reabrir lo limpia:', g255re, '| 3 checkboxes + todos/ninguno:', g255checks, '| exportar habilitado con entregados:', g255btnFor, '| selección 2 de 3:', g255sel, '| contador dice 2 de 3:', g255info, '| exportar con selección trae solo esos 2:', g255expSel, '| seleccionar todos:', g255all, '| ninguno:', g255none, '| sin selección avisa y exporta todos:', g255todos && g255expTodos, '| WhatsApp con selección trae solo ese:', g255shareSel);
