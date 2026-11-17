# Parche 2.5.0d: www/index.html — módulo JS de Mantenimientos Preventivos
# (se inserta antes de "// Menu de 3 secciones.").
import io

P = '/home/hatch/workspace/android/checklist-cloud/www/index.html'
s = io.open(P, encoding='utf-8').read()

MODULE = r'''// ---------- Mantenimientos Preventivos (2.5.0) ----------
// Órdenes de servicio con folio: el técnico crea el mantenimiento (desde
// un equipo detectado o en blanco), lo guarda como borrador sin folio o
// crea la orden (asigna folio con transacción), y el usuario la firma
// desde el link que le llega por WhatsApp. Un usuario normal solo ve sus
// propios mantenimientos; el admin ve todos con su selector de usuario.
var MANT_COMPONENTES = [['impresora', 'Impresora'], ['cpu', 'CPU'], ['monitor', 'Monitor'], ['teclado', 'Teclado'], ['mouse', 'Mouse'], ['noBreak', 'No Break']];
var MANT_LS_KEY = 'checklist-soporte-mant-v1';
var MANT_MIG_KEY = 'checklist-soporte-migrado-mant-v1';
var mantenimientos = [];
var cloudMantUnsub = null;
var mantAdminViewUid = 'todos';
var mantFormId = null;      // id del mantenimiento que se está editando (null = nuevo)
var mantFormBase = null;    // objeto que se está editando (borrador o nuevo pre-llenado)
var mantFormFromDet = null; // id del detectado que llenó el formulario
var mantFirmaData = '';     // data URL de la firma del técnico dibujada
var mantOrderId = null;     // id de la orden que muestra la vista de orden
var prefillMantUserName = '';
var FIRMA_URL_BASE = 'https://checklist-soporte.web.app/firma.html';

function mantEmptyChecks() { return { impresora: false, cpu: false, monitor: false, teclado: false, mouse: false, noBreak: false }; }
function newMantBlank() {
  return {
    id: uid(), createdAt: Date.now(), folio: null, estado: 'borrador',
    tecnicoUid: cloudUser ? cloudUser.uid : '', tecnico: technicianName(),
    tipo: 'SOFTWARE', area: '', responsable: '',
    tiempoReparacion: '', tiempoViaje: '', tiempoSistemaCaido: '',
    fechaServicio: '', fechaTermino: '', tituloCaso: '', tipoFalla: '',
    identificacion: mantEmptyChecks(), descripcionEquipo: '',
    condiciones: Object.assign(mantEmptyChecks(), { notas: '' }),
    preventivo: mantEmptyChecks(),
    descripcionCambios: '', conclusion: '', comentarios: '',
    fechaPlaneacion: '', fechaCompromiso: '', periodoPrueba: '', fechaLiberacion: '',
    observaciones: '', observacionesDetectadas: '',
    equipo: { tipo: 'Laptop', marca: '', modelo: '', serie: '', hostname: '', cpu: '', ramGB: '', discoGB: '', discoTipo: '', ip: '', redes: [], impresora: '', anydeskId: '', anydeskAlias: '', antivirus: '', politicas: { cambioDias: '', minLongitud: '', bloqueoIntentos: '', bloqueoSegundos: '', cumpleCambio: null, cumpleLongitud: null, cumpleIntentos: null, cumpleBloqueo: null, cumple: null }, usuarioSistemas: false, so: '', versiones: { so: '', antivirus: '', esetAgent: '', chrome: '' } },
    whatsappUsuario: '', firmaTecnico: '', firma: null
  };
}
// Saneo como prepToCloudDoc/prepFromCloud: la firma (data URL) no viaja
// si pasa de ~700 KB (límite de 1 MB por documento), igual que fotoSerie.
function mantToCloudDoc(m) {
  var eq = m.equipo || {};
  var pol = eq.politicas || {};
  var firmaTec = m.firmaTecnico || '';
  if (firmaTec && firmaTec.length > MAX_FOTO_CLOUD) firmaTec = '';
  var firmaUsr = m.firma || null;
  if (firmaUsr && firmaUsr.firma && firmaUsr.firma.length > MAX_FOTO_CLOUD) firmaUsr = Object.assign({}, firmaUsr, { firma: '' });
  function ck(o) { return { impresora: !!(o && o.impresora), cpu: !!(o && o.cpu), monitor: !!(o && o.monitor), teclado: !!(o && o.teclado), mouse: !!(o && o.mouse), noBreak: !!(o && o.noBreak) }; }
  var cond = ck(m.condiciones);
  cond.notas = (m.condiciones && m.condiciones.notas) || '';
  return {
    id: m.id, createdAt: m.createdAt || Date.now(), folio: (m.folio == null ? null : m.folio), estado: m.estado || 'borrador',
    tecnicoUid: m.tecnicoUid || '', tecnico: m.tecnico || '',
    tipo: m.tipo || '', area: m.area || '', responsable: m.responsable || '',
    tiempoReparacion: m.tiempoReparacion || '', tiempoViaje: m.tiempoViaje || '', tiempoSistemaCaido: m.tiempoSistemaCaido || '',
    fechaServicio: m.fechaServicio || '', fechaTermino: m.fechaTermino || '',
    tituloCaso: m.tituloCaso || '', tipoFalla: m.tipoFalla || '',
    identificacion: ck(m.identificacion), descripcionEquipo: m.descripcionEquipo || '',
    condiciones: cond, preventivo: ck(m.preventivo),
    descripcionCambios: m.descripcionCambios || '', conclusion: m.conclusion || '', comentarios: m.comentarios || '',
    fechaPlaneacion: m.fechaPlaneacion || '', fechaCompromiso: m.fechaCompromiso || '', periodoPrueba: m.periodoPrueba || '', fechaLiberacion: m.fechaLiberacion || '',
    observaciones: m.observaciones || '', observacionesDetectadas: m.observacionesDetectadas || '',
    equipo: { tipo: eq.tipo || '', marca: eq.marca || '', modelo: eq.modelo || '', serie: eq.serie || '', hostname: eq.hostname || '', cpu: eq.cpu || '', ramGB: (eq.ramGB == null ? '' : eq.ramGB), discoGB: (eq.discoGB == null ? '' : eq.discoGB), discoTipo: eq.discoTipo || '', ip: eq.ip || '', redes: Array.isArray(eq.redes) ? eq.redes.map(function (r) { return { nombre: r.nombre || '', ip: r.ip || '', ipTipo: r.ipTipo || '' }; }) : [], impresora: eq.impresora || '', anydeskId: eq.anydeskId || '', anydeskAlias: eq.anydeskAlias || '', antivirus: eq.antivirus || '', politicas: { cambioDias: (pol.cambioDias == null ? '' : pol.cambioDias), minLongitud: (pol.minLongitud == null ? '' : pol.minLongitud), bloqueoIntentos: (pol.bloqueoIntentos == null ? '' : pol.bloqueoIntentos), bloqueoSegundos: (pol.bloqueoSegundos == null ? '' : pol.bloqueoSegundos), cumpleCambio: (pol.cumpleCambio == null ? null : !!pol.cumpleCambio), cumpleLongitud: (pol.cumpleLongitud == null ? null : !!pol.cumpleLongitud), cumpleIntentos: (pol.cumpleIntentos == null ? null : !!pol.cumpleIntentos), cumpleBloqueo: (pol.cumpleBloqueo == null ? null : !!pol.cumpleBloqueo), cumple: (pol.cumple == null ? null : !!pol.cumple) }, usuarioSistemas: !!eq.usuarioSistemas, so: eq.so || '', versiones: { so: ((eq.versiones && eq.versiones.so) || ''), antivirus: ((eq.versiones && eq.versiones.antivirus) || ''), esetAgent: ((eq.versiones && eq.versiones.esetAgent) || ''), chrome: ((eq.versiones && eq.versiones.chrome) || '') } },
    whatsappUsuario: m.whatsappUsuario || '',
    firmaTecnico: firmaTec,
    firma: firmaUsr,
    updatedAt: Date.now()
  };
}
function mantFromCloud(doc) {
  var m = newMantBlank();
  var d = doc || {};
  var eq = d.equipo || {};
  var pol = eq.politicas || {};
  var ver = eq.versiones || {};
  m.id = d.id || m.id;
  m.createdAt = d.createdAt || 0;
  m.folio = (d.folio == null ? null : d.folio);
  m.estado = d.estado || 'borrador';
  m.tecnicoUid = d.tecnicoUid || '';
  m.tecnico = d.tecnico || '';
  m.tipo = d.tipo || 'SOFTWARE';
  m.area = d.area || '';
  m.responsable = d.responsable || '';
  m.tiempoReparacion = d.tiempoReparacion || '';
  m.tiempoViaje = d.tiempoViaje || '';
  m.tiempoSistemaCaido = d.tiempoSistemaCaido || '';
  m.fechaServicio = d.fechaServicio || '';
  m.fechaTermino = d.fechaTermino || '';
  m.tituloCaso = d.tituloCaso || '';
  m.tipoFalla = d.tipoFalla || '';
  ['identificacion', 'preventivo'].forEach(function (k) { var o = d[k] || {}; MANT_COMPONENTES.forEach(function (c) { m[k][c[0]] = !!o[c[0]]; }); });
  var cond = d.condiciones || {};
  MANT_COMPONENTES.forEach(function (c) { m.condiciones[c[0]] = !!cond[c[0]]; });
  m.condiciones.notas = cond.notas || '';
  m.descripcionEquipo = d.descripcionEquipo || '';
  m.descripcionCambios = d.descripcionCambios || '';
  m.conclusion = d.conclusion || '';
  m.comentarios = d.comentarios || '';
  m.fechaPlaneacion = d.fechaPlaneacion || '';
  m.fechaCompromiso = d.fechaCompromiso || '';
  m.periodoPrueba = d.periodoPrueba || '';
  m.fechaLiberacion = d.fechaLiberacion || '';
  m.observaciones = d.observaciones || '';
  m.observacionesDetectadas = d.observacionesDetectadas || '';
  m.equipo.tipo = eq.tipo || 'Laptop';
  m.equipo.marca = eq.marca || '';
  m.equipo.modelo = eq.modelo || '';
  m.equipo.serie = eq.serie || '';
  m.equipo.hostname = eq.hostname || '';
  m.equipo.cpu = eq.cpu || '';
  m.equipo.ramGB = (eq.ramGB == null ? '' : eq.ramGB);
  m.equipo.discoGB = (eq.discoGB == null ? '' : eq.discoGB);
  m.equipo.discoTipo = eq.discoTipo || '';
  m.equipo.ip = eq.ip || '';
  m.equipo.redes = Array.isArray(eq.redes) ? eq.redes.map(function (r) { return { nombre: r.nombre || '', ip: r.ip || '', ipTipo: r.ipTipo || '' }; }) : [];
  m.equipo.impresora = eq.impresora || '';
  m.equipo.anydeskId = eq.anydeskId || '';
  m.equipo.anydeskAlias = eq.anydeskAlias || '';
  m.equipo.antivirus = eq.antivirus || '';
  m.equipo.politicas.cambioDias = (pol.cambioDias == null ? '' : pol.cambioDias);
  m.equipo.politicas.minLongitud = (pol.minLongitud == null ? '' : pol.minLongitud);
  m.equipo.politicas.bloqueoIntentos = (pol.bloqueoIntentos == null ? '' : pol.bloqueoIntentos);
  m.equipo.politicas.bloqueoSegundos = (pol.bloqueoSegundos == null ? '' : pol.bloqueoSegundos);
  m.equipo.politicas.cumpleCambio = (pol.cumpleCambio == null ? null : !!pol.cumpleCambio);
  m.equipo.politicas.cumpleLongitud = (pol.cumpleLongitud == null ? null : !!pol.cumpleLongitud);
  m.equipo.politicas.cumpleIntentos = (pol.cumpleIntentos == null ? null : !!pol.cumpleIntentos);
  m.equipo.politicas.cumpleBloqueo = (pol.cumpleBloqueo == null ? null : !!pol.cumpleBloqueo);
  m.equipo.politicas.cumple = (pol.cumple == null ? null : !!pol.cumple);
  m.equipo.usuarioSistemas = !!eq.usuarioSistemas;
  m.equipo.so = eq.so || ver.so || '';
  m.equipo.versiones = { so: ver.so || '', antivirus: ver.antivirus || '', esetAgent: ver.esetAgent || '', chrome: ver.chrome || '' };
  m.whatsappUsuario = d.whatsappUsuario || '';
  m.firmaTecnico = d.firmaTecnico || '';
  m.firma = d.firma || null;
  return m;
}
// Políticas de contraseña (2.5.0): lo esperado es cambio cada 90 días,
// longitud mínima 10, bloqueo a los 5 intentos y bloqueo de 350 s.
// Cumple si el valor detectado está dentro de lo esperado (cambio cada 90
// días o menos, longitud 10 o más, bloqueo con 5 intentos o menos,
// bloqueo de 350 s o más). Sin dato no se puede decir: null.
function mantPoliticasCumple(pol) {
  pol = pol || {};
  function num(v) { if (v == null || v === '') return null; var n = Number(v); return isNaN(n) ? null : n; }
  var cambio = num(pol.cambioDias), lon = num(pol.minLongitud), inten = num(pol.bloqueoIntentos), bloq = num(pol.bloqueoSegundos);
  var cC = cambio == null ? null : cambio <= 90;
  var cL = lon == null ? null : lon >= 10;
  var cI = inten == null ? null : inten <= 5;
  var cB = bloq == null ? null : bloq >= 350;
  var vals = [cC, cL, cI, cB].filter(function (v) { return v !== null; });
  return { cambioDias: cambio, minLongitud: lon, bloqueoIntentos: inten, bloqueoSegundos: bloq, cumpleCambio: cC, cumpleLongitud: cL, cumpleIntentos: cI, cumpleBloqueo: cB, cumple: vals.length ? vals.every(function (v) { return v === true; }) : null };
}
function politicasText(pol) {
  var c = mantPoliticasCumple(pol);
  var parts = [];
  parts.push('cambio cada ' + (c.cambioDias == null ? '—' : c.cambioDias + ' días') + (c.cumpleCambio == null ? '' : (c.cumpleCambio ? ' ✓' : ' ✗')));
  parts.push('longitud mínima ' + (c.minLongitud == null ? '—' : c.minLongitud) + (c.cumpleLongitud == null ? '' : (c.cumpleLongitud ? ' ✓' : ' ✗')));
  parts.push('bloqueo a los ' + (c.bloqueoIntentos == null ? '—' : c.bloqueoIntentos + ' intentos') + (c.cumpleIntentos == null ? '' : (c.cumpleIntentos ? ' ✓' : ' ✗')));
  parts.push('bloqueo ' + (c.bloqueoSegundos == null ? '—' : c.bloqueoSegundos + ' s') + (c.cumpleBloqueo == null ? '' : (c.cumpleBloqueo ? ' ✓' : ' ✗')));
  return 'Políticas: ' + parts.join(' · ') + (c.cumple == null ? '' : (c.cumple ? ' — Cumple' : ' — No cumple'));
}
// Observaciones detectadas (2.5.0): los datos detectados se compilan en
// un texto (software y versiones, IPs/redes, impresora, AnyDesk,
// antivirus, políticas con su cumplimiento, usuario de sistemas,
// hostname, serie, modelo), no como campos sueltos.
function compileObservacionesDetectadas(d) {
  d = d || {};
  var det = d.detalles || {};
  var ver = d.versiones || {};
  var lines = [];
  var hw = hardwareLine(d);
  if (hw) lines.push(hw);
  var rd = redesLine(d);
  if (rd) lines.push(rd);
  var vl = versionesLine(ver);
  if (vl) lines.push(vl);
  if (d.so && !ver.so) lines.push('SO: ' + d.so);
  var ad = anydeskLine(d);
  if (ad) lines.push(ad);
  var imp = d.impresora || det.impresora || '';
  if (imp) lines.push('Impresora: ' + imp);
  var av = ver.antivirus || d.antivirus || det.antivirus || '';
  if (av) lines.push('Antivirus: ' + av);
  var pol = d.politicas || det.politicas || null;
  if (pol) lines.push(politicasText(pol));
  var us = (typeof d.usuarioSistemas !== 'undefined') ? d.usuarioSistemas : det.usuarioSistemas;
  if (typeof us === 'boolean') lines.push('Usuario de sistemas: ' + (us ? 'Sí' : 'No'));
  if (d.hostname) lines.push('Hostname: ' + d.hostname);
  if (d.serie) lines.push('Serie: ' + d.serie);
  if (d.modelo) lines.push('Modelo: ' + ((d.marca ? d.marca + ' ' : '') + d.modelo));
  return lines.join('\n');
}
function mantFromDetectado(d) {
  var m = newMantBlank();
  var ver = d.versiones || {};
  var det = d.detalles || {};
  var pol = d.politicas || det.politicas || null;
  m.equipo.tipo = d.tipo || 'Desktop';
  m.equipo.marca = d.marca || '';
  m.equipo.modelo = d.modelo || '';
  m.equipo.serie = d.serie || '';
  m.equipo.hostname = d.hostname || '';
  m.equipo.cpu = d.cpu || '';
  m.equipo.ramGB = (d.ramGB == null ? '' : d.ramGB);
  m.equipo.discoGB = (d.discoGB == null ? '' : d.discoGB);
  m.equipo.discoTipo = d.discoTipo || '';
  m.equipo.ip = d.ip || '';
  m.equipo.redes = Array.isArray(d.redes) ? d.redes.map(function (r) { return { nombre: r.nombre || '', ip: r.ip || '', ipTipo: r.ipTipo || '' }; }) : [];
  m.equipo.impresora = d.impresora || det.impresora || '';
  m.equipo.anydeskId = d.anydeskId || '';
  m.equipo.anydeskAlias = d.anydeskAlias || '';
  m.equipo.antivirus = ver.antivirus || d.antivirus || det.antivirus || '';
  m.equipo.so = d.so || ver.so || '';
  m.equipo.versiones = { so: ver.so || '', antivirus: ver.antivirus || '', esetAgent: ver.esetAgent || '', chrome: ver.chrome || '' };
  if (pol) m.equipo.politicas = mantPoliticasCumple(pol);
  if (typeof d.usuarioSistemas !== 'undefined') m.equipo.usuarioSistemas = !!d.usuarioSistemas;
  else if (typeof det.usuarioSistemas !== 'undefined') m.equipo.usuarioSistemas = !!det.usuarioSistemas;
  m.observacionesDetectadas = compileObservacionesDetectadas(d);
  return m;
}
// Redes del formulario: "Wi-Fi: 192.168.1.45 (Dinámica), Ethernet:
// 10.0.0.20 (Estática)" o separadas con '·' (como las escribe
// redesText). Un segmento sin IP se guarda con su nombre y sin IP.
function parseRedesText(s) {
  var out = [];
  String(s || '').split(/[,·]/).forEach(function (seg) {
    seg = seg.trim();
    if (!seg) return;
    var m = /^(.*?):\s*([0-9]{1,3}(?:\.[0-9]{1,3}){3})\s*(?:\(([^)]*)\))?$/.exec(seg);
    if (m) { out.push({ nombre: (m[1] || '').trim(), ip: m[2], ipTipo: (m[3] || '').trim() }); return; }
    var ipOnly = /^([0-9]{1,3}(?:\.[0-9]{1,3}){3})$/.exec(seg);
    if (ipOnly) { out.push({ nombre: '', ip: ipOnly[1], ipTipo: '' }); return; }
    out.push({ nombre: seg, ip: '', ipTipo: '' });
  });
  return out;
}
// Visibilidad (2.5.0, más estricta que Por preparar): un usuario normal
// ve ÚNICAMENTE sus propios mantenimientos (tecnicoUid propio, con
// respaldo por nombre para registros viejos, igual que en Por preparar);
// los de otros analistas NO se ven en absoluto, sin toggle de 'ver otros'.
// El admin ve todos, con su selector de usuario.
function isOwnMant(m) {
  if (!cloudUser) return true;
  if (m.tecnicoUid) return m.tecnicoUid === cloudUser.uid;
  if (m.tecnico && (m.tecnico === technicianName() || m.tecnico === cloudUser.nombre)) return true;
  return false;
}
function isMantOfAnalyst(m, uid) {
  if (m.tecnicoUid) return m.tecnicoUid === uid;
  var u = null;
  teamUsers.forEach(function (x) { if (x.uid === uid) u = x; });
  if (u && m.tecnico) return m.tecnico === (u.nombre || u.email);
  return false;
}
function mantVisibleList() {
  var list = mantenimientos.slice().sort(function (a, b) { return (b.createdAt || 0) - (a.createdAt || 0); });
  if (cloudRole === 'admin') {
    if (mantAdminViewUid && mantAdminViewUid !== 'todos') list = list.filter(function (m) { return isMantOfAnalyst(m, mantAdminViewUid); });
    return list;
  }
  return list.filter(isOwnMant);
}
function mantEstadoLabel(m) {
  return { borrador: 'Borrador', creada: 'Creada', firmada: 'Firmada', cancelada: 'Cancelada' }[m.estado] || m.estado || '—';
}
function mantCardHtml(m) {
  var eq = m.equipo || {};
  var pol = mantPoliticasCumple(eq.politicas || {});
  var polTxt = pol.cumple == null ? '' : (pol.cumple ? 'Políticas: ✓ Cumple' : 'Políticas: ✗ No cumple');
  var firmaTxt = m.firma ? ('Firmada por ' + (m.firma.nombre || '—') + (m.firma.satisfaccion != null && m.firma.satisfaccion !== '' ? ' · Satisfacción: ' + m.firma.satisfaccion + '/10' : '')) : (m.firmaTecnico ? 'Firma del técnico: sí · Firma del usuario: pendiente' : 'Sin firmas');
  var idLine = 'Serie: ' + (eq.serie || '—') + ' · Hostname: ' + (eq.hostname || '—') + ' · Modelo: ' + (eq.modelo || '—');
  return '<div class="card"><h2>' + esc(m.tituloCaso || 'Mantenimiento sin título') + '</h2>' +
    '<div class="mant-id-line">' + esc(idLine) + '</div>' +
    '<div class="sub">' + esc((m.tipo || '') + ' · ' + (m.area || '—') + ' · Responsable: ' + (m.responsable || '—')) + '</div>' +
    '<div class="sub">Técnico: ' + esc(m.tecnico || '—') + ' · Fecha del servicio: ' + esc(m.fechaServicio || '—') + '</div>' +
    (polTxt ? '<div class="sub">' + esc(polTxt) + '</div>' : '') +
    '<div class="sub">' + esc(firmaTxt) + '</div>' +
    '<span class="badge ' + (m.estado === 'firmada' ? 'b-listo' : (m.estado === 'cancelada' ? 'b-prep' : 'b-entr')) + '">' + esc(mantEstadoLabel(m)) + (m.folio ? ' · Folio ' + esc(m.folio) : ' · Sin folio') + '</span>' +
    '<div class="actions">' +
    (m.estado === 'borrador' ? '<button class="btn-green" data-mant-edit="' + esc(m.id) + '">Editar</button>' : '<button class="btn-dark" data-mant-order="' + esc(m.id) + '">Ver orden</button>') +
    ((m.estado === 'creada' || m.estado === 'firmada') ? '<button class="btn-ghost" data-mant-cancel-order="' + esc(m.id) + '">Cancelar orden</button>' : '') +
    (m.estado === 'borrador' ? '<button class="btn-danger" data-mant-del="' + esc(m.id) + '">Eliminar</button>' : '') +
    '</div></div>';
}
function renderMant() {
  var box = document.getElementById('mantList');
  if (!box) return;
  var isAdmin = cloudRole === 'admin';
  var row = document.getElementById('mantAdminRow');
  if (row) row.hidden = !isAdmin;
  if (isAdmin) refreshMantAdminFilter();
  var list = mantVisibleList();
  if (!list.length) { box.innerHTML = '<div class="empty">No hay mantenimientos.</div>'; return; }
  box.innerHTML = list.map(mantCardHtml).join('');
}
function refreshMantAdminFilter() {
  var sel = document.getElementById('mantAdminFilter');
  if (!sel) return;
  var cur = mantAdminViewUid || 'todos';
  sel.innerHTML = '<option value="todos">Todos los usuarios</option>' + teamUsers.map(function (u) {
    return '<option value="' + esc(u.uid) + '"' + (u.uid === cur ? ' selected' : '') + '>' + esc(u.nombre || u.email || 'Usuario') + '</option>';
  }).join('');
  sel.value = cur;
}
function renderMantDetectados() {
  var box = document.getElementById('mantDetList');
  if (!box) return;
  var list = detectados.filter(function (d) { return !d.usado; });
  if (!list.length) { box.innerHTML = '<div class="empty">No hay equipos detectados pendientes.</div>'; return; }
  box.innerHTML = list.map(function (d) {
    var hwLine = hardwareLine(d);
    if (d.so) hwLine = hwLine ? hwLine + ' • SO: ' + d.so : 'SO: ' + d.so;
    return '<div class="card"><h2>' + esc(d.hostname || 'Equipo') + '</h2>' +
      '<div class="sub">' + esc((d.marca || '') + ' ' + (d.modelo || '')) + ' · Serie: ' + esc(d.serie || '—') + '</div>' +
      (hwLine ? '<div class="sub">' + esc(hwLine) + '</div>' : '') +
      '<div class="sub">Detectado ' + timeAgo(d.detectadoEn) + (d.detectadoPor ? ' por ' + esc(d.detectadoPor) : '') + '</div>' +
      '<div class="actions"><button class="btn-green" data-mant-det-use="' + esc(d.id) + '">Usar este equipo</button></div></div>';
  }).join('');
}
function renderMantCheckboxes() {
  function groupHtml(prefix) {
    return MANT_COMPONENTES.map(function (c) {
      return '<label><input type="checkbox" id="' + prefix + '-' + c[0] + '"> ' + c[1] + '</label>';
    }).join('');
  }
  var a = document.getElementById('accs-mant-id'); if (a) a.innerHTML = groupHtml('fM-id');
  var b = document.getElementById('accs-mant-cond'); if (b) b.innerHTML = groupHtml('fM-cond');
  var c = document.getElementById('accs-mant-prev'); if (c) c.innerHTML = groupHtml('fM-prev');
}
// Nombre de quien presta el servicio (2.5.0): mismo patrón prefillTecnico
// de la 2.0.18 — se llena solo con el login; si el técnico lo escribe a
// mano, se respeta.
function prefillMantTecnico() {
  var f = document.getElementById('fM-tecnico');
  var name = technicianName();
  if (f && name && (!f.value || f.value === prefillMantUserName)) { f.value = name; prefillMantUserName = name; }
}
function mantVal(id) { var el = document.getElementById(id); return el ? el.value : ''; }
function mantCheck(id) { var el = document.getElementById(id); return !!(el && el.checked); }
function mantSetVal(id, v) { var el = document.getElementById(id); if (el) el.value = (v == null ? '' : v); }
function mantSetCheck(id, v) { var el = document.getElementById(id); if (el) el.checked = !!v; }
function mantNum(id) { var s = mantVal(id).trim(); if (s === '') return ''; var n = Number(s); return isNaN(n) ? s : n; }
function mantScrollTo(id) { var el = document.getElementById(id); if (el && el.scrollIntoView) el.scrollIntoView(); }
function mantReadForm() {
  var m = mantFormBase ? mantFromCloud(mantToCloudDoc(mantFormBase)) : newMantBlank();
  m.tecnico = mantVal('fM-tecnico').trim() || technicianName();
  m.tecnicoUid = tecnicoUidFor(m.tecnico);
  m.tipo = mantVal('fM-tipo') || 'SOFTWARE';
  m.area = mantVal('fM-area').trim();
  m.responsable = mantVal('fM-responsable').trim();
  m.tiempoReparacion = mantVal('fM-tRep').trim();
  m.tiempoViaje = mantVal('fM-tViaje').trim();
  m.tiempoSistemaCaido = mantVal('fM-tCaido').trim();
  m.fechaServicio = mantVal('fM-fechaServ');
  m.fechaTermino = mantVal('fM-fechaTerm');
  m.tituloCaso = mantVal('fM-titulo').trim();
  m.tipoFalla = mantVal('fM-tipoFalla').trim();
  MANT_COMPONENTES.forEach(function (c) {
    m.identificacion[c[0]] = mantCheck('fM-id-' + c[0]);
    m.condiciones[c[0]] = mantCheck('fM-cond-' + c[0]);
    m.preventivo[c[0]] = mantCheck('fM-prev-' + c[0]);
  });
  m.descripcionEquipo = mantVal('fM-descEquipo').trim();
  m.condiciones.notas = mantVal('fM-condNotas').trim();
  m.descripcionCambios = mantVal('fM-descCambios').trim();
  m.conclusion = mantVal('fM-conclusion').trim();
  m.comentarios = mantVal('fM-comentarios').trim();
  m.fechaPlaneacion = mantVal('fM-fechaPlan');
  m.fechaCompromiso = mantVal('fM-fechaComp');
  m.periodoPrueba = mantVal('fM-periodoPrueba').trim();
  m.fechaLiberacion = mantVal('fM-fechaLib');
  m.observaciones = mantVal('fM-observaciones').trim();
  m.observacionesDetectadas = mantVal('fM-obsDet');
  m.whatsappUsuario = mantVal('fM-whatsapp').trim();
  var eq = m.equipo;
  eq.tipo = mantVal('fM-eq-tipo') || 'Laptop';
  eq.marca = mantVal('fM-eq-marca').trim();
  eq.modelo = mantVal('fM-modelo').trim();
  eq.serie = mantVal('fM-serie').trim();
  eq.hostname = mantVal('fM-hostname').trim();
  eq.cpu = mantVal('fM-eq-cpu').trim();
  eq.ramGB = mantNum('fM-eq-ram');
  eq.discoGB = mantNum('fM-eq-disco');
  eq.discoTipo = mantVal('fM-eq-discoTipo').trim();
  eq.ip = mantVal('fM-eq-ip').trim();
  eq.redes = parseRedesText(mantVal('fM-eq-redes'));
  eq.impresora = mantVal('fM-eq-impresora').trim();
  eq.anydeskId = mantVal('fM-eq-anydesk').trim();
  eq.anydeskAlias = mantVal('fM-eq-anydeskAlias').trim();
  eq.antivirus = mantVal('fM-eq-antivirus').trim();
  eq.so = mantVal('fM-eq-so').trim();
  eq.usuarioSistemas = mantCheck('fM-eq-usuarioSistemas');
  eq.politicas = mantPoliticasCumple({ cambioDias: mantNum('fM-pol-cambio'), minLongitud: mantNum('fM-pol-long'), bloqueoIntentos: mantNum('fM-pol-intentos'), bloqueoSegundos: mantNum('fM-pol-bloqueo') });
  if (mantFirmaData) m.firmaTecnico = mantFirmaData;
  return m;
}
function mantFillForm(m) {
  mantSetVal('fM-tecnico', m.tecnico);
  mantSetVal('fM-tipo', m.tipo);
  mantSetVal('fM-area', m.area);
  mantSetVal('fM-responsable', m.responsable);
  mantSetVal('fM-tRep', m.tiempoReparacion);
  mantSetVal('fM-tViaje', m.tiempoViaje);
  mantSetVal('fM-tCaido', m.tiempoSistemaCaido);
  mantSetVal('fM-fechaServ', m.fechaServicio);
  mantSetVal('fM-fechaTerm', m.fechaTermino);
  mantSetVal('fM-titulo', m.tituloCaso);
  mantSetVal('fM-tipoFalla', m.tipoFalla);
  MANT_COMPONENTES.forEach(function (c) {
    mantSetCheck('fM-id-' + c[0], m.identificacion[c[0]]);
    mantSetCheck('fM-cond-' + c[0], m.condiciones[c[0]]);
    mantSetCheck('fM-prev-' + c[0], m.preventivo[c[0]]);
  });
  mantSetVal('fM-descEquipo', m.descripcionEquipo);
  mantSetVal('fM-condNotas', m.condiciones.notas);
  mantSetVal('fM-descCambios', m.descripcionCambios);
  mantSetVal('fM-conclusion', m.conclusion);
  mantSetVal('fM-comentarios', m.comentarios);
  mantSetVal('fM-fechaPlan', m.fechaPlaneacion);
  mantSetVal('fM-fechaComp', m.fechaCompromiso);
  mantSetVal('fM-periodoPrueba', m.periodoPrueba);
  mantSetVal('fM-fechaLib', m.fechaLiberacion);
  mantSetVal('fM-observaciones', m.observaciones);
  mantSetVal('fM-obsDet', m.observacionesDetectadas);
  mantSetVal('fM-whatsapp', m.whatsappUsuario);
  var eq = m.equipo || {};
  mantSetVal('fM-eq-tipo', eq.tipo);
  mantSetVal('fM-eq-marca', eq.marca);
  mantSetVal('fM-modelo', eq.modelo);
  mantSetVal('fM-serie', eq.serie);
  mantSetVal('fM-hostname', eq.hostname);
  mantSetVal('fM-eq-cpu', eq.cpu);
  mantSetVal('fM-eq-ram', eq.ramGB);
  mantSetVal('fM-eq-disco', eq.discoGB);
  mantSetVal('fM-eq-discoTipo', eq.discoTipo);
  mantSetVal('fM-eq-ip', eq.ip);
  mantSetVal('fM-eq-redes', redesText(eq));
  mantSetVal('fM-eq-impresora', eq.impresora);
  mantSetVal('fM-eq-anydesk', eq.anydeskId);
  mantSetVal('fM-eq-anydeskAlias', eq.anydeskAlias);
  mantSetVal('fM-eq-antivirus', eq.antivirus);
  mantSetVal('fM-eq-so', eq.so);
  mantSetCheck('fM-eq-usuarioSistemas', eq.usuarioSistemas);
  var pol = eq.politicas || {};
  mantSetVal('fM-pol-cambio', pol.cambioDias);
  mantSetVal('fM-pol-long', pol.minLongitud);
  mantSetVal('fM-pol-intentos', pol.bloqueoIntentos);
  mantSetVal('fM-pol-bloqueo', pol.bloqueoSegundos);
  refreshMantPolLine();
  mantFirmaData = m.firmaTecnico || '';
  mantDrawFirmaOnCanvas(mantFirmaData);
}
function mantFormHasData() {
  var ids = ['fM-serie', 'fM-hostname', 'fM-modelo', 'fM-area', 'fM-responsable', 'fM-tRep', 'fM-tViaje', 'fM-tCaido', 'fM-fechaServ', 'fM-fechaTerm', 'fM-titulo', 'fM-tipoFalla', 'fM-descEquipo', 'fM-condNotas', 'fM-descCambios', 'fM-conclusion', 'fM-comentarios', 'fM-fechaPlan', 'fM-fechaComp', 'fM-periodoPrueba', 'fM-fechaLib', 'fM-observaciones', 'fM-obsDet', 'fM-whatsapp', 'fM-eq-marca', 'fM-eq-cpu', 'fM-eq-ram', 'fM-eq-disco', 'fM-eq-discoTipo', 'fM-eq-ip', 'fM-eq-redes', 'fM-eq-impresora', 'fM-eq-anydesk', 'fM-eq-anydeskAlias', 'fM-eq-antivirus', 'fM-eq-so'];
  for (var i = 0; i < ids.length; i++) { if (mantVal(ids[i]).trim()) return true; }
  var any = false;
  MANT_COMPONENTES.forEach(function (c) { if (mantCheck('fM-id-' + c[0]) || mantCheck('fM-cond-' + c[0]) || mantCheck('fM-prev-' + c[0])) any = true; });
  if (mantCheck('fM-eq-usuarioSistemas')) any = true;
  if (mantFirmaData) any = true;
  return any;
}
// Validación de 'Crear orden de servicio' (2.5.0): serie, hostname y
// modelo son obligatorios y destacados (aclaración de Gerardo 23:53) —
// si falta alguno, no se crea la orden y el toast dice cuál falta. El
// borrador SÍ se puede guardar sin ellos: lo que no se asigna es el folio.
function mantFaltaCrear(m) {
  if (!m.equipo.serie) return 'el número de serie del equipo';
  if (!m.equipo.hostname) return 'el hostname del equipo';
  if (!m.equipo.modelo) return 'el modelo del equipo';
  if (!m.tipo) return 'el tipo de mantenimiento';
  if (!m.area) return 'el área';
  if (!m.responsable) return 'el responsable';
  if (!m.tituloCaso) return 'el título del caso';
  if (!m.tipoFalla) return 'el tipo de falla';
  if (!m.descripcionEquipo) return 'la descripción del equipo';
  if (!m.fechaServicio) return 'la fecha del servicio';
  if (!m.whatsappUsuario) return 'el WhatsApp del usuario';
  if (!m.firmaTecnico) return 'la firma del técnico';
  return null;
}
function mantOpenForm(m, fromDetId) {
  mantFormBase = m || null;
  mantFormId = m ? m.id : null;
  mantFormFromDet = fromDetId || null;
  mantFirmaData = m ? (m.firmaTecnico || '') : '';
  document.getElementById('mantFormTitle').textContent = m ? 'Editar borrador' : 'Nuevo mantenimiento';
  document.getElementById('mantFormBox').hidden = false;
  document.getElementById('mantOrderBox').hidden = true;
  document.getElementById('mantDetBox').hidden = true;
  if (m) mantFillForm(m); else { mantClearForm(); prefillMantTecnico(); }
  mantScrollTo('mantFormBox');
}
function mantClearForm() {
  mantFormBase = null;
  mantFormId = null;
  mantFormFromDet = null;
  mantFirmaData = '';
  mantFillForm(newMantBlank());
  mantClearFirmaCanvas();
  prefillMantTecnico();
}
function mantCloseForm() {
  document.getElementById('mantFormBox').hidden = true;
  mantFormBase = null;
  mantFormId = null;
  mantFormFromDet = null;
  mantFirmaData = '';
  renderMant();
}
function mantSave(m) {
  var i = -1;
  mantenimientos.forEach(function (x, idx) { if (x.id === m.id) i = idx; });
  if (i === -1) mantenimientos.push(m); else mantenimientos[i] = m;
  saveMantLocal();
  cloudUpsertMant(m);
  renderMant();
}
function cloudUpsertMant(m) {
  if (!CLOUD_ENABLED || !cloudUser || !window.Cloud || !window.Cloud.upsertMant) return;
  window.Cloud.upsertMant(mantToCloudDoc(m)).catch(function (e) { console.warn('No se pudo guardar el mantenimiento en la nube', e); });
}
function cloudDeleteMant(id) {
  if (!CLOUD_ENABLED || !cloudUser || !window.Cloud || !window.Cloud.deleteMant) return;
  window.Cloud.deleteMant(id).catch(function (e) { console.warn('No se pudo borrar el mantenimiento en la nube', e); });
}
function loadMantLocal() {
  try {
    var raw = localStorage.getItem(MANT_LS_KEY);
    if (raw) { var arr = JSON.parse(raw); if (Array.isArray(arr)) mantenimientos = arr.map(mantFromCloud); }
  } catch (e) {}
}
function saveMantLocal() {
  try { localStorage.setItem(MANT_LS_KEY, JSON.stringify(mantenimientos.map(mantToCloudDoc))); } catch (e) {}
}
// Al recibir la lista de la nube, conservar los borradores locales que la
// nube aún no trae (igual que mergePrepsWithLocal).
function mergeMantWithLocal(docs) {
  var localById = {};
  mantenimientos.forEach(function (m) { localById[m.id] = m; });
  var out = docs.map(function (d) { return mantFromCloud(d); });
  var ids = {};
  out.forEach(function (m) { ids[m.id] = true; });
  Object.keys(localById).forEach(function (id) { if (!ids[id]) out.push(localById[id]); });
  return out;
}
async function migrateLocalMants() {
  try {
    if (!window.Cloud.getAllMantenimientos) return;
    var flag = MANT_MIG_KEY + ':' + cloudUser.uid;
    if (localStorage.getItem(flag)) return;
    var inCloud = await window.Cloud.getAllMantenimientos();
    var ids = {};
    inCloud.forEach(function (d) { ids[d.id] = true; });
    var pendientes = mantenimientos.filter(function (m) { return !ids[m.id]; });
    for (var i = 0; i < pendientes.length; i++) {
      await window.Cloud.upsertMant(mantToCloudDoc(pendientes[i]));
    }
    localStorage.setItem(flag, '1');
  } catch (e) { console.warn('Migración de mantenimientos pendiente', e); }
}
async function mantCrearOrden() {
  var m = mantReadForm();
  var falta = mantFaltaCrear(m);
  if (falta) { showToast('Falta ' + falta + ' para crear la orden.'); return; }
  var folio = null;
  if (window.Cloud && window.Cloud.asignarFolio && CLOUD_ENABLED && cloudUser) {
    try { folio = await window.Cloud.asignarFolio(); } catch (e) { folio = null; }
  }
  if (!folio) {
    // Sin conexión: no se puede asignar folio; se guarda como borrador sin folio.
    m.estado = 'borrador';
    m.folio = null;
    mantSave(m);
    mantFormBase = m;
    mantFormId = m.id;
    showToast('Sin conexión: no se pudo asignar folio. Se guardó como borrador sin folio.');
    return;
  }
  m.folio = folio;
  m.estado = 'creada';
  mantSave(m);
  if (mantFormFromDet) cloudMarkDetectadoUsado(mantFormFromDet);
  mantCloseForm();
  mantShowOrder(m.id);
  showToast('Orden de servicio creada con folio ' + folio + '.');
}
function mantGuardarBorrador() {
  var m = mantReadForm();
  if (!m.folio) { m.estado = 'borrador'; m.folio = null; }
  mantSave(m);
  mantFormBase = m;
  mantFormId = m.id;
  showToast(m.folio ? 'Orden guardada.' : 'Borrador guardado.');
}
function mantCancelarForm() {
  if (!mantFormHasData()) { mantCloseForm(); return; }
  showConfirm('¿Descartar los cambios sin guardar?').then(function (ok) {
    if (!ok) return;
    mantCloseForm();
  });
}
function mantUseDetectado(id) {
  var d = null;
  detectados.forEach(function (x) { if (String(x.id) === String(id)) d = x; });
  if (!d) { showToast('Ese equipo detectado ya no está en la lista.'); return; }
  var m = mantFromDetectado(d);
  mantOpenForm(m, d.id);
  showToast('Datos del equipo detectado cargados. Revisa la serie, el hostname y el modelo.');
}
function mantFind(id) { var f = null; mantenimientos.forEach(function (x) { if (x.id === id) f = x; }); return f; }
function mantFirmaUrl(m) { return FIRMA_URL_BASE + '?id=' + encodeURIComponent(m.id); }
// Número para wa.me: solo dígitos; si tiene 10 dígitos es de México y se
// le antepone 52 (interpretación 2.5.0).
function mantWaNumber(num) {
  var d = String(num || '').replace(/\D/g, '');
  if (d.length === 10) d = '52' + d;
  return d;
}
function mantFirmaWaUrl(m) {
  var num = mantWaNumber(m.whatsappUsuario);
  var txt = 'Hola, te comparto la orden de servicio' + (m.folio ? ' con folio ' + m.folio : '') + ' de Checklist de Soporte. Para firmarla abre este enlace: ' + mantFirmaUrl(m);
  return 'https://wa.me/' + num + '?text=' + encodeURIComponent(txt);
}
function mantEnviarLink() {
  var m = mantFind(mantOrderId);
  if (!m) return;
  if (!mantWaNumber(m.whatsappUsuario)) { showToast('Falta el WhatsApp del usuario para enviar el formulario.'); return; }
  window.open(mantFirmaWaUrl(m), '_blank');
}
function mantPdfFalta(m) {
  if (!m.firmaTecnico) return 'la firma del técnico';
  if (!m.firma || !m.firma.firma) return 'la firma del usuario';
  return null;
}
function renderMantOrder(m) {
  var eq = m.equipo || {};
  var body = document.getElementById('mantOrderBody');
  var both = !mantPdfFalta(m);
  var falta = mantPdfFalta(m);
  var html = '<h2>Orden de servicio' + (m.folio ? ' · Folio ' + esc(m.folio) : '') + '</h2>' +
    '<div class="sub">Estado: ' + esc(mantEstadoLabel(m)) + ' · Tipo: ' + esc(m.tipo || '—') + ' · Área: ' + esc(m.area || '—') + '</div>' +
    '<div class="mant-id-line">Serie: ' + esc(eq.serie || '—') + ' · Hostname: ' + esc(eq.hostname || '—') + ' · Modelo: ' + esc(eq.modelo || '—') + '</div>' +
    '<div class="sub">Técnico: ' + esc(m.tecnico || '—') + ' · Responsable: ' + esc(m.responsable || '—') + '</div>' +
    '<div class="sub">Título del caso: ' + esc(m.tituloCaso || '—') + ' · Tipo de falla: ' + esc(m.tipoFalla || '—') + '</div>' +
    '<div class="sub">Fecha del servicio: ' + esc(m.fechaServicio || '—') + (m.fechaTermino ? ' · Término: ' + esc(m.fechaTermino) : '') + '</div>' +
    '<div class="sub">Firma del técnico: ' + (m.firmaTecnico ? 'sí ✓' : 'pendiente') + ' · Firma del usuario: ' + (m.firma && m.firma.firma ? 'sí ✓ (' + esc(m.firma.nombre || '') + ')' : 'pendiente') + '</div>';
  if (m.firma && m.firma.firma) {
    html += '<div class="sub">El usuario firmó: ' + esc(m.firma.nombre || '—') + ' · Área: ' + esc(m.firma.area || '—') + ' · Satisfacción: ' + esc(String(m.firma.satisfaccion == null ? '—' : m.firma.satisfaccion)) + '/10' + (m.firma.firmadoEn ? ' · ' + fmtDate(m.firma.firmadoEn) : '') + '</div>';
    if (m.firma.comentarios) html += '<div class="sub">Comentarios del usuario: ' + esc(m.firma.comentarios) + '</div>';
  }
  html += '<div class="sub">Link de firma: <a href="' + esc(mantFirmaUrl(m)) + '">' + esc(mantFirmaUrl(m)) + '</a></div>';
  if (body) body.innerHTML = html;
  var shareBtn = document.getElementById('btnMantCompartir');
  if (shareBtn) shareBtn.disabled = !both;
  var note = document.getElementById('mantOrderNote');
  if (note) note.textContent = both ? 'La orden tiene ambas firmas: ya puedes compartir la copia y generar el PDF.' : ('Para compartir la copia y generar el PDF falta ' + falta + '.');
  var cancelBtn = document.getElementById('btnMantCancelarOrden');
  if (cancelBtn) cancelBtn.hidden = !(m.estado === 'creada' || m.estado === 'firmada');
}
function mantShowOrder(id) {
  var m = mantFind(id);
  if (!m) { showToast('Esa orden ya no está en la lista.'); return; }
  mantOrderId = id;
  document.getElementById('mantFormBox').hidden = true;
  document.getElementById('mantDetBox').hidden = true;
  renderMantOrder(m);
  document.getElementById('mantOrderBox').hidden = false;
  mantScrollTo('mantOrderBox');
}
function mantCancelarOrden() {
  var m = mantFind(mantOrderId);
  if (!m) return;
  showConfirm('¿Cancelar esta orden? Se conserva el registro y el folio ' + (m.folio || '—') + ' no se vuelve a usar.').then(function (ok) {
    if (!ok) return;
    m.estado = 'cancelada';
    mantSave(m);
    renderMantOrder(m);
    showToast('Orden cancelada. El folio no se reutiliza.');
  });
}
// Escala de satisfacción (2.5.0, interpretación): 0–3 INACEPTABLE,
// 4–7 ACEPTABLE, 8–10 EXCELENTE.
function satLabel(v) {
  if (v == null || v === '') return '—';
  var n = Number(v);
  if (isNaN(n)) return String(v);
  if (n <= 3) return n + ' (INACEPTABLE)';
  if (n <= 7) return n + ' (ACEPTABLE)';
  return n + ' (EXCELENTE)';
}
function buildPdfMant(m, sigImgs) {
  sigImgs = sigImgs || {};
  var eq = m.equipo || {};
  var pol = eq.politicas || {};
  var rows = [];
  function row(t, f, s, img) { var r = { t: t, f: f || 'F1', s: s || 11 }; if (img) r.img = img; rows.push(r); }
  function section(t) { row('', 'F1', 11); row(t, 'F2', 13); }
  function kv(label, val) { wrapText(label + ': ' + (val == null || val === '' ? '—' : String(val)), 82).forEach(function (ln) { row(ln, 'F1', 11); }); }
  function compLine(list) { return list.filter(function (x) { return x; }).join(', ') || '—'; }
  function checkedList(o) { return MANT_COMPONENTES.filter(function (c) { return o && o[c[0]]; }).map(function (c) { return c[1]; }); }
  function textBlock(txt) { String(txt || '—').split('\n').forEach(function (ln) { wrapText(ln, 82).forEach(function (w) { row(w, 'F1', 11); }); }); }
  function hasImg(im) { return !!(im && im.bytes && im.w && im.h); }
  row('Lapi Sistemas', 'F2', 16);
  row('Rosa Blanca 63, Col. Molino de Rosas, C.P. 01470', 'F1', 11);
  row('Tels. 53371283 y 53370207', 'F1', 11);
  row('sistemas@lapi.com.mx · info@lapi.com.mx', 'F1', 11);
  row('', 'F1', 11);
  row('ORDEN DE SERVICIO', 'F2', 16);
  row('Formato F0.S1.01 Rev0', 'F1', 11);
  row('Folio: ' + (m.folio || '—'), 'F2', 13);
  row('Estado: ' + mantEstadoLabel(m), 'F1', 11);
  section('Datos del servicio');
  kv('Nombre de quien presta el servicio', m.tecnico);
  kv('Tipo de mantenimiento', m.tipo);
  kv('Área', m.area);
  kv('Responsable', m.responsable);
  kv('Tiempo de reparación', m.tiempoReparacion);
  kv('Tiempo de viaje', m.tiempoViaje);
  kv('Tiempo de sistema caído', m.tiempoSistemaCaido);
  kv('Fecha del servicio', m.fechaServicio);
  kv('Fecha de término', m.fechaTermino);
  section('Caso');
  kv('Título del caso', m.tituloCaso);
  kv('Tipo de falla', m.tipoFalla);
  section('Descripción del equipo');
  kv('Serie', eq.serie);
  kv('Hostname', eq.hostname);
  kv('Modelo', eq.modelo);
  kv('Descripción', m.descripcionEquipo);
  kv('Tipo', eq.tipo);
  kv('Marca', eq.marca);
  kv('Procesador', eq.cpu);
  kv('RAM', (eq.ramGB == null || eq.ramGB === '') ? '' : eq.ramGB + ' GB');
  kv('Disco', (eq.discoGB == null || eq.discoGB === '') ? '' : eq.discoGB + ' GB' + (eq.discoTipo ? ' ' + eq.discoTipo : ''));
  kv('IP', eq.ip);
  var rd = redesText(eq);
  if (rd) kv('Redes', rd);
  kv('Impresora', eq.impresora);
  kv('AnyDesk', eq.anydeskId ? anydeskDisplay(eq.anydeskId) + (eq.anydeskAlias ? ' (' + eq.anydeskAlias + ')' : '') : '');
  kv('Antivirus', eq.antivirus);
  kv('Sistema operativo', eq.so);
  var ver = eq.versiones || {};
  if (ver.so || ver.antivirus || ver.esetAgent || ver.chrome) {
    kv('Versiones', [ver.so ? 'SO: ' + ver.so : '', ver.antivirus ? 'Antivirus: ' + ver.antivirus : '', ver.esetAgent ? 'Agente ESET: ' + ver.esetAgent : '', ver.chrome ? 'Chrome: ' + ver.chrome : ''].filter(Boolean).join(' · '));
  }
  kv('Usuario de sistemas', eq.usuarioSistemas ? 'Sí' : 'No');
  kv('Políticas', politicasText(pol).replace(/^Políticas: /, ''));
  section('Identificación del equipo');
  kv('Componentes', compLine(checkedList(m.identificacion)));
  section('Condiciones del equipo');
  kv('En buen estado', compLine(checkedList(m.condiciones)));
  kv('Notas', m.condiciones.notas);
  section('Mantenimiento preventivo');
  kv('Realizado en', compLine(checkedList(m.preventivo)));
  section('Descripción de cambios');
  textBlock(m.descripcionCambios);
  section('Conclusión');
  textBlock(m.conclusion);
  section('Comentarios');
  textBlock(m.comentarios);
  section('Planeación');
  kv('Fecha de planeación', m.fechaPlaneacion);
  kv('Fecha compromiso de instalación', m.fechaCompromiso);
  kv('Periodo de prueba', m.periodoPrueba);
  kv('Fecha de liberación', m.fechaLiberacion);
  section('Observaciones');
  kv('Equipo', 'Serie: ' + (eq.serie || '—') + ' · Hostname: ' + (eq.hostname || '—') + ' · Modelo: ' + (eq.modelo || '—'));
  if (m.observacionesDetectadas) { row('Datos detectados:', 'F2', 12); textBlock(m.observacionesDetectadas); }
  if (m.observaciones) { row('Observaciones del técnico:', 'F2', 12); textBlock(m.observaciones); }
  if (!m.observacionesDetectadas && !m.observaciones) row('Sin observaciones.', 'F1', 11);
  section('Firmas');
  var tecImg = hasImg(sigImgs.tecnico) ? { name: 'tecnico', w: 150, h: Math.max(20, Math.round(150 * sigImgs.tecnico.h / sigImgs.tecnico.w)) } : null;
  ['Planeación', 'Compromiso de instalación', 'Periodo de prueba', 'Liberación'].forEach(function (fase) {
    row('Sistemas — ' + fase + ':', 'F2', 12);
    if (tecImg) row('', 'F1', 11, tecImg);
    else row('Firma: ' + (m.tecnico || '—') + ' (guardada en la app)', 'F1', 11);
    row('Área solicitante — ' + fase + ': ________________________________________', 'F1', 11);
  });
  section('Conformidad del usuario');
  if (m.firma) {
    kv('Nombre', m.firma.nombre);
    kv('Área', m.firma.area);
    if (m.firma.comentarios) kv('Comentarios', m.firma.comentarios);
    kv('Fecha', m.firma.firmadoEn ? fmtDate(m.firma.firmadoEn) : '');
    kv('Hora', m.firma.firmadoEn ? fmtTime(m.firma.firmadoEn) : '');
    var sat = m.firma.satisfaccion;
    row('Escala de satisfacción (0–10): ' + satLabel(sat), 'F1', 11);
    if (sat != null && sat !== '') {
      var marks = [];
      for (var i = 0; i <= 10; i++) marks.push(i === Number(sat) ? '[' + i + ']' : String(i));
      row(marks.join('  '), 'F1', 11);
      row('INACEPTABLE 0-3 · ACEPTABLE 4-7 · EXCELENTE 8-10', 'F1', 10);
    }
    var usrImg = hasImg(sigImgs.usuario) ? { name: 'usuario', w: 150, h: Math.max(20, Math.round(150 * sigImgs.usuario.h / sigImgs.usuario.w)) } : null;
    row('Firma de conformidad:', 'F2', 12);
    if (usrImg) row('', 'F1', 11, usrImg);
    else row('Firma: ' + (m.firma.nombre || '—') + ' (guardada en la app)', 'F1', 11);
  } else {
    row('Pendiente de firma.', 'F1', 11);
  }
  row('', 'F1', 11);
  row('Generado el ' + fmtDate(Date.now()) + ' — Checklist de Soporte', 'F1', 10);
  return assemblePdf(rows, sigImgs);
}
// Convierte una firma (data URL PNG del canvas o de la página de firma)
// a JPEG sobre fondo blanco, que es lo que el PDF puede incrustar.
function dataUrlToJpeg(dataUrl, maxW) {
  return new Promise(function (resolve) {
    try {
      if (typeof Image === 'undefined') { resolve(null); return; }
      var img = new Image();
      img.onload = function () {
        try {
          var c = document.createElement('canvas');
          var scale = Math.min(1, (maxW || 400) / (img.width || 1));
          c.width = Math.max(1, Math.round((img.width || 1) * scale));
          c.height = Math.max(1, Math.round((img.height || 1) * scale));
          var ctx = c.getContext('2d');
          if (!ctx) { resolve(null); return; }
          ctx.fillStyle = '#ffffff';
          ctx.fillRect(0, 0, c.width, c.height);
          ctx.drawImage(img, 0, 0, c.width, c.height);
          var url = c.toDataURL('image/jpeg', 0.85);
          var b64 = (url || '').split(',')[1] || '';
          var bin = atob(b64);
          var bytes = new Uint8Array(bin.length);
          for (var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
          resolve({ bytes: bytes, w: c.width, h: c.height });
        } catch (e) { resolve(null); }
      };
      img.onerror = function () { resolve(null); };
      img.src = dataUrl;
    } catch (e) { resolve(null); }
  });
}
async function mantPdfBlob(m) {
  var imgs = {};
  try {
    var t = await dataUrlToJpeg(m.firmaTecnico, 400);
    if (t) imgs.tecnico = t;
    if (m.firma && m.firma.firma) {
      var u = await dataUrlToJpeg(m.firma.firma, 400);
      if (u) imgs.usuario = u;
    }
  } catch (e) {}
  var blob = buildPdfMant(m, imgs);
  return { blob: blob, name: 'orden-servicio-' + (m.folio || m.id) + '.pdf' };
}
// El PDF solo se genera con ambas firmas (técnico + usuario); si falta
// alguna, el botón avisa con toast cuál falta.
async function sharePdfMant(m) {
  var falta = mantPdfFalta(m);
  if (falta) { showToast('Falta ' + falta + ' para generar el PDF.'); return; }
  var out = await mantPdfBlob(m);
  var file = new File([out.blob], out.name, { type: 'application/pdf' });
  var texto = 'Orden de servicio' + (m.folio ? ' folio ' + m.folio : '') + ' — Checklist de Soporte.';
  if (navigator.canShare && navigator.canShare({ files: [file] })) {
    navigator.share({ files: [file], title: 'Checklist de Soporte', text: texto }).catch(function () {});
    return;
  }
  var a = document.createElement('a');
  a.href = URL.createObjectURL(out.blob);
  a.download = out.name;
  a.click();
  setTimeout(function () { URL.revokeObjectURL(a.href); }, 5000);
  if (navigator.share) {
    navigator.share({ title: 'Checklist de Soporte', text: texto + ' El PDF se descargó, adjúntalo en WhatsApp.' }).catch(function () {});
  } else {
    showToast('PDF descargado: ' + out.name + '. Compártelo por WhatsApp desde tus archivos.');
  }
}
// Compartir copia con el usuario (share nativo como el Excel de renta):
// solo con ambas firmas.
async function shareMantCopy(m) {
  var falta = mantPdfFalta(m);
  if (falta) { showToast('Falta ' + falta + ' para compartir la copia.'); return; }
  var out = await mantPdfBlob(m);
  try {
    var Plugins = window.Capacitor && window.Capacitor.Plugins;
    if (!Plugins || !Plugins.Filesystem || !Plugins.Share) throw new Error('share-no-disponible');
    var base64 = await blobToBase64(out.blob);
    var saved = await Plugins.Filesystem.writeFile({ path: out.name, data: base64, directory: 'CACHE' });
    await Plugins.Share.share({
      title: 'Checklist de Soporte',
      text: 'Orden de servicio' + (m.folio ? ' folio ' + m.folio : '') + ' — Checklist de Soporte.',
      url: saved.uri,
      dialogTitle: 'Compartir copia con el usuario'
    });
  } catch (e) {
    showToast('No se pudo compartir la copia. Genera el PDF y compártelo desde tus archivos.');
  }
}
// Firma del técnico: canvas con dedo o ratón.
function mantFirmaCanvasCtx() {
  var cv = document.getElementById('fM-firmaCanvas');
  if (!cv) return null;
  try { return cv.getContext('2d'); } catch (e) { return null; }
}
function initMantFirmaCanvas() {
  var cv = document.getElementById('fM-firmaCanvas');
  if (!cv) return;
  var ctx = mantFirmaCanvasCtx();
  if (!ctx) return;
  var drawing = false, lastX = 0, lastY = 0;
  function pos(e) {
    var r = (cv.getBoundingClientRect) ? cv.getBoundingClientRect() : { left: 0, top: 0, width: cv.width, height: cv.height };
    var x = (e.offsetX != null) ? e.offsetX : ((e.clientX - r.left) * (cv.width / (r.width || 1)));
    var y = (e.offsetY != null) ? e.offsetY : ((e.clientY - r.top) * (cv.height / (r.height || 1)));
    return { x: x, y: y };
  }
  cv.addEventListener('pointerdown', function (e) {
    e.preventDefault();
    drawing = true;
    var p = pos(e);
    lastX = p.x; lastY = p.y;
    if (cv.setPointerCapture) { try { cv.setPointerCapture(e.pointerId); } catch (e2) {} }
  });
  cv.addEventListener('pointermove', function (e) {
    if (!drawing) return;
    e.preventDefault();
    var p = pos(e);
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 2;
    ctx.lineCap = 'round';
    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(p.x, p.y);
    ctx.stroke();
    lastX = p.x; lastY = p.y;
  });
  function end() {
    if (!drawing) return;
    drawing = false;
    try { mantFirmaData = cv.toDataURL('image/png'); } catch (e2) { mantFirmaData = ''; }
  }
  cv.addEventListener('pointerup', end);
  cv.addEventListener('pointercancel', end);
}
function mantClearFirmaCanvas() {
  mantFirmaData = '';
  var cv = document.getElementById('fM-firmaCanvas');
  var ctx = mantFirmaCanvasCtx();
  if (cv && ctx) { try { ctx.clearRect(0, 0, cv.width, cv.height); } catch (e) {} }
}
function mantDrawFirmaOnCanvas(dataUrl) {
  var cv = document.getElementById('fM-firmaCanvas');
  var ctx = mantFirmaCanvasCtx();
  if (!cv || !ctx) return;
  try { ctx.clearRect(0, 0, cv.width, cv.height); } catch (e) {}
  if (!dataUrl || typeof Image === 'undefined') return;
  try {
    var img = new Image();
    img.onload = function () { try { ctx.drawImage(img, 0, 0, cv.width, cv.height); } catch (e) {} };
    img.src = dataUrl;
  } catch (e) {}
}
function refreshMantPolLine() {
  var el = document.getElementById('mantPolLine');
  if (!el) return;
  el.textContent = politicasText({ cambioDias: mantNum('fM-pol-cambio'), minLongitud: mantNum('fM-pol-long'), bloqueoIntentos: mantNum('fM-pol-intentos'), bloqueoSegundos: mantNum('fM-pol-bloqueo') });
}
// Selector de sección (Inicio).
document.getElementById('btnGoPreparar').addEventListener('click', function () { showVista('preparar'); });
document.getElementById('btnGoRec').addEventListener('click', function () { showVista('rec'); });
document.getElementById('btnGoFor').addEventListener('click', function () { showVista('for'); });
document.getElementById('btnGoMant').addEventListener('click', function () { showVista('mant'); });
// Mantenimientos: lista, formulario y orden.
document.getElementById('btnMantNuevo').addEventListener('click', function () { mantOpenForm(null, null); });
document.getElementById('btnMantDet').addEventListener('click', function () { var b = document.getElementById('mantDetBox'); b.hidden = !b.hidden; if (!b.hidden) renderMantDetectados(); });
document.getElementById('mantDetList').addEventListener('click', function (e) {
  var b = e.target.closest('[data-mant-det-use]');
  if (b) mantUseDetectado(b.getAttribute('data-mant-det-use'));
});
document.getElementById('mantAdminFilter').addEventListener('change', function (e) { mantAdminViewUid = e.target.value; renderMant(); });
document.getElementById('btnMantCrear').addEventListener('click', function () { mantCrearOrden(); });
document.getElementById('btnMantGuardar').addEventListener('click', function () { mantGuardarBorrador(); });
document.getElementById('btnMantCancelar').addEventListener('click', function () { mantCancelarForm(); });
document.getElementById('btnMantFirmaLimpiar').addEventListener('click', function () { mantClearFirmaCanvas(); });
document.getElementById('btnMantWaLink').addEventListener('click', function () { mantEnviarLink(); });
document.getElementById('btnMantPdf').addEventListener('click', function () { var m = mantFind(mantOrderId); if (m) sharePdfMant(m); });
document.getElementById('btnMantCompartir').addEventListener('click', function () { var m = mantFind(mantOrderId); if (m) shareMantCopy(m); });
document.getElementById('btnMantCancelarOrden').addEventListener('click', function () { mantCancelarOrden(); });
document.getElementById('btnMantVolver').addEventListener('click', function () { document.getElementById('mantOrderBox').hidden = true; mantOrderId = null; renderMant(); });
document.getElementById('mantList').addEventListener('click', function (e) {
  var t = e.target;
  var q = function (attr) { var el = t.closest('[' + attr + ']'); return el ? el.getAttribute(attr) : null; };
  var id = q('data-mant-edit') || q('data-mant-order') || q('data-mant-cancel-order') || q('data-mant-del');
  if (!id) return;
  var m = mantFind(id);
  if (!m) return;
  if (t.closest('[data-mant-edit]')) { mantOpenForm(m, null); return; }
  if (t.closest('[data-mant-order]')) { mantShowOrder(id); return; }
  if (t.closest('[data-mant-cancel-order]')) {
    showConfirm('¿Cancelar esta orden? Se conserva el registro y el folio ' + (m.folio || '—') + ' no se vuelve a usar.').then(function (ok) {
      if (!ok) return;
      m.estado = 'cancelada';
      mantSave(m);
      if (!document.getElementById('mantOrderBox').hidden) renderMantOrder(m);
      showToast('Orden cancelada. El folio no se reutiliza.');
    });
    return;
  }
  if (t.closest('[data-mant-del]')) {
    showConfirm('¿Eliminar este borrador de mantenimiento?').then(function (ok) {
      if (!ok) return;
      mantenimientos = mantenimientos.filter(function (x) { return x.id !== id; });
      saveMantLocal();
      cloudDeleteMant(id);
      renderMant();
    });
  }
});
['fM-pol-cambio', 'fM-pol-long', 'fM-pol-intentos', 'fM-pol-bloqueo'].forEach(function (id) {
  var el = document.getElementById(id);
  if (el) el.addEventListener('input', refreshMantPolLine);
});
renderMantCheckboxes();
initMantFirmaCanvas();
loadMantLocal();

'''

anchor = "// Menu de 3 secciones."
assert s.count(anchor) == 1, 'ancla menu no encontrada'
s = s.replace(anchor, MODULE + anchor)
io.open(P, 'w', encoding='utf-8').write(s)
print('JS modulo 2.5.0d OK')
