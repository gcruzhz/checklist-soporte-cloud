# Parche 2.5.5 para www/index.html — retroalimentación de Gerardo 2026-11-17:
# 1) Responsable/Área no obligatorios al crear la orden; se llenan con la
#    firma del usuario (fallback + write-back desde la app).
# 2) Campo obligatorio faltante se marca en rojo + toast con los nombres.
# 3) (detector, en detect.js) políticas desde gpedit.
# 4) PDF: DESCRIPCIÓN DEL EQUIPO solo hostname; el resto al final.
# 5) PDF: una hoja tamaño carta (612x792).
# Uso: python3 tests/patch_20255.py  (desde ~/workspace/android/checklist-cloud)
import re
import sys

P = '/home/hatch/workspace/android/checklist-cloud/www/index.html'
s = open(P, encoding='utf-8').read()
orig = s

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'esperaba %d ocurrencia(s) de %r, hay %d' % (n, old[:70], c)
    s = s.replace(old, new)

def rep_re(pat, new, n=1):
    global s
    found = re.findall(pat, s, flags=re.DOTALL)
    assert len(found) == n, 'esperaba %d coincidencia(s) de %r, hay %d' % (n, pat[:70], len(found))
    s = re.sub(pat, new, s, count=n, flags=re.DOTALL)

# --- Versión 2.5.5 ---
rep('Versión 2.5.4', 'Versión 2.5.5')
rep('Versión: 2.5.4', 'Versión: 2.5.5')
rep('Reporte de problema - Checklist de Soporte 254', 'Reporte de problema - Checklist de Soporte 255')
rep('Versión de la app: 254', 'Versión de la app: 255')

# --- (2) CSS: campo obligatorio faltante en rojo ---
rep("  .field label { display: block; font-size: 12px; color: #666; margin-bottom: 3px; }",
    "  .field label { display: block; font-size: 12px; color: #666; margin-bottom: 3px; }\n"
    "  .campo-falta { border: 2px solid #c0392b !important; background: #fdecea !important; }")

# --- (1) Etiquetas del formulario: Área y Responsable ya no obligatorios ---
rep('<label>Área *</label>', '<label>Área</label>')
rep('<label>Responsable *</label>', '<label>Responsable</label>')

# --- (3-detector en teléfono) bloqueoManual + politicasFuente ---
rep("""  var cambio = num(pol.cambioDias), lon = num(pol.minLongitud), inten = num(pol.bloqueoIntentos), bloq = num(pol.bloqueoSegundos);
  var cC = cambio == null ? null : cambio <= 90;
  var cL = lon == null ? null : lon >= 10;
  var cI = inten == null ? null : inten <= 5;
  var cB = bloq == null ? null : bloq >= 350;
  var vals = [cC, cL, cI, cB].filter(function (v) { return v !== null; });
  return { cambioDias: cambio, minLongitud: lon, bloqueoIntentos: inten, bloqueoSegundos: bloq, cumpleCambio: cC, cumpleLongitud: cL, cumpleIntentos: cI, cumpleBloqueo: cB, cumple: vals.length ? vals.every(function (v) { return v === true; }) : null };""",
"""  var cambio = num(pol.cambioDias), lon = num(pol.minLongitud), inten = num(pol.bloqueoIntentos), bloq = num(pol.bloqueoSegundos);
  // (255) Bloqueo manual (LockoutDuration 0 en la directiva): el equipo
  // queda bloqueado hasta que un administrador lo desbloquee, así que
  // cumple el bloqueo sin importar los segundos.
  var manual = !!pol.bloqueoManual;
  var cC = cambio == null ? null : cambio <= 90;
  var cL = lon == null ? null : lon >= 10;
  var cI = inten == null ? null : inten <= 5;
  var cB = manual ? true : (bloq == null ? null : bloq >= 350);
  var vals = [cC, cL, cI, cB].filter(function (v) { return v !== null; });
  return { cambioDias: cambio, minLongitud: lon, bloqueoIntentos: inten, bloqueoSegundos: bloq, bloqueoManual: manual, cumpleCambio: cC, cumpleLongitud: cL, cumpleIntentos: cI, cumpleBloqueo: cB, cumple: vals.length ? vals.every(function (v) { return v === true; }) : null };""")
rep("  parts.push('bloqueo ' + (c.bloqueoSegundos == null ? '—' : c.bloqueoSegundos + ' s') + (c.cumpleBloqueo == null ? '' : (c.cumpleBloqueo ? ' ✓' : ' ✗')));",
    "  parts.push(c.bloqueoManual ? 'bloqueo hasta desbloqueo manual ✓' : ('bloqueo ' + (c.bloqueoSegundos == null ? '—' : c.bloqueoSegundos + ' s') + (c.cumpleBloqueo == null ? '' : (c.cumpleBloqueo ? ' ✓' : ' ✗'))));")
rep("politicas: { cambioDias: '', minLongitud: '', bloqueoIntentos: '', bloqueoSegundos: '', cumpleCambio: null, cumpleLongitud: null, cumpleIntentos: null, cumpleBloqueo: null, cumple: null }, usuarioSistemas: false",
    "politicas: { cambioDias: '', minLongitud: '', bloqueoIntentos: '', bloqueoSegundos: '', bloqueoManual: false, cumpleCambio: null, cumpleLongitud: null, cumpleIntentos: null, cumpleBloqueo: null, cumple: null }, politicasFuente: '', usuarioSistemas: false")
rep("bloqueoSegundos: (pol.bloqueoSegundos == null ? '' : pol.bloqueoSegundos), cumpleCambio:",
    "bloqueoSegundos: (pol.bloqueoSegundos == null ? '' : pol.bloqueoSegundos), bloqueoManual: !!pol.bloqueoManual, cumpleCambio:")
rep("cumple: (pol.cumple == null ? null : !!pol.cumple) }, usuarioSistemas: !!eq.usuarioSistemas",
    "cumple: (pol.cumple == null ? null : !!pol.cumple) }, politicasFuente: eq.politicasFuente || '', usuarioSistemas: !!eq.usuarioSistemas")
rep("""  m.equipo.politicas.cumple = (pol.cumple == null ? null : !!pol.cumple);
  m.equipo.usuarioSistemas = !!eq.usuarioSistemas;""",
"""  m.equipo.politicas.cumple = (pol.cumple == null ? null : !!pol.cumple);
  m.equipo.politicas.bloqueoManual = !!pol.bloqueoManual;
  m.equipo.politicasFuente = eq.politicasFuente || '';
  m.equipo.usuarioSistemas = !!eq.usuarioSistemas;""")
rep("  if (pol) m.equipo.politicas = mantPoliticasCumple(pol);",
    "  if (pol) m.equipo.politicas = mantPoliticasCumple(pol);\n  m.equipo.politicasFuente = det.politicasFuente || '';")
rep("  eq.politicas = mantPoliticasCumple({ cambioDias: mantNum('fM-pol-cambio'), minLongitud: mantNum('fM-pol-long'), bloqueoIntentos: mantNum('fM-pol-intentos'), bloqueoSegundos: mantNum('fM-pol-bloqueo') });",
    "  eq.politicas = mantPoliticasCumple({ cambioDias: mantNum('fM-pol-cambio'), minLongitud: mantNum('fM-pol-long'), bloqueoIntentos: mantNum('fM-pol-intentos'), bloqueoSegundos: mantNum('fM-pol-bloqueo'), bloqueoManual: !!(m.equipo.politicas && m.equipo.politicas.bloqueoManual) });")
rep("""  el.textContent = politicasText({ cambioDias: mantNum('fM-pol-cambio'), minLongitud: mantNum('fM-pol-long'), bloqueoIntentos: mantNum('fM-pol-intentos'), bloqueoSegundos: mantNum('fM-pol-bloqueo') });""",
"""  var txt = politicasText({ cambioDias: mantNum('fM-pol-cambio'), minLongitud: mantNum('fM-pol-long'), bloqueoIntentos: mantNum('fM-pol-intentos'), bloqueoSegundos: mantNum('fM-pol-bloqueo') });
  if (mantPolFuente) txt += ' · Fuente: ' + mantPolFuente;
  el.textContent = txt;""")
rep("var mantFirmaData = '';     // data URL de la firma del técnico dibujada",
    "var mantFirmaData = '';     // data URL de la firma del técnico dibujada\nvar mantPolFuente = '';       // de dónde salieron las políticas (gpedit / secedit / net accounts)")
rep("""  refreshMantPolLine();
  mantFirmaData = m.firmaTecnico || '';""",
"""  mantPolFuente = (m.equipo && m.equipo.politicasFuente) || '';
  refreshMantPolLine();
  mantFirmaData = m.firmaTecnico || '';""")

# --- (1)+(2) Validación: sin área/responsable; lista completa para marcar en rojo ---
rep("""function mantFaltaCrear(m) {
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
}""",
"""// (255) Obligatorios para crear la orden: serie, hostname, modelo, tipo,
// título, tipo de falla, descripción, fecha del servicio, WhatsApp y
// firma del técnico. Área y Responsable YA NO son obligatorios: se llenan
// con lo que el usuario envía al firmar (mantFillFromFirma). La lista
// completa sirve para marcar en rojo cada campo vacío (punto 2); la
// función vieja sigue devolviendo el primero para el toast.
function mantFaltantesCrear(m) {
  var out = [];
  function falta(id, label, ok) { if (!ok) out.push({ id: id, label: label }); }
  falta('fM-serie', 'el número de serie del equipo', m.equipo.serie);
  falta('fM-hostname', 'el hostname del equipo', m.equipo.hostname);
  falta('fM-modelo', 'el modelo del equipo', m.equipo.modelo);
  if (!m.tipo) { out.push({ id: 'fM-tipo-sw', label: 'el tipo de mantenimiento' }); out.push({ id: 'fM-tipo-hw', label: 'el tipo de mantenimiento' }); }
  falta('fM-titulo', 'el título del caso', m.tituloCaso);
  falta('fM-tipoFalla', 'el tipo de falla', m.tipoFalla);
  falta('fM-descEquipo', 'la descripción del equipo', m.descripcionEquipo);
  falta('fM-fechaServ', 'la fecha del servicio', m.fechaServicio);
  falta('fM-whatsapp', 'el WhatsApp del usuario', m.whatsappUsuario);
  falta('fM-firmaCanvas', 'la firma del técnico', m.firmaTecnico);
  return out;
}
function mantFaltaCrear(m) {
  var f = mantFaltantesCrear(m);
  return f.length ? f[0].label : null;
}
// (255) Marca en rojo los campos obligatorios vacíos; se quita al
// escribir o cambiar el campo (listener en #mantFormBox).
function mantMarcarFaltantes(list) {
  var prev = document.querySelectorAll('.campo-falta');
  for (var i = 0; i < prev.length; i++) prev[i].classList.remove('campo-falta');
  list.forEach(function (f) { var el = document.getElementById(f.id); if (el && el.classList) el.classList.add('campo-falta'); });
}
function mantLimpiarFaltantes() { mantMarcarFaltantes([]); }""")
rep("""  var m = mantReadForm();
  var falta = mantFaltaCrear(m);
  if (falta) { showToast('Falta ' + falta + ' para crear la orden.'); return; }""",
"""  var m = mantReadForm();
  var faltantes = mantFaltantesCrear(m);
  if (faltantes.length) {
    mantMarcarFaltantes(faltantes);
    var nombres = [];
    faltantes.forEach(function (f) { if (nombres.indexOf(f.label) === -1) nombres.push(f.label); });
    showToast('Falta ' + nombres.join(', ') + ' para crear la orden.');
    return;
  }""")
rep("""  if (m) mantFillForm(m); else { mantClearForm(); prefillMantTecnico(); }
  mantApplyDefaults();""",
"""  if (m) mantFillForm(m); else { mantClearForm(); prefillMantTecnico(); }
  mantLimpiarFaltantes();
  mantApplyDefaults();""")
rep("""document.getElementById('btnMantCrear').addEventListener('click', function () { mantCrearOrden(); });""",
"""document.getElementById('btnMantCrear').addEventListener('click', function () { mantCrearOrden(); });
// (255) Quitar la marca roja al escribir o cambiar el campo. Si se marca
// un checkbox de tipo, se quitan las dos (el tipo ya quedó cubierto).
['input', 'change'].forEach(function (ev) {
  document.getElementById('mantFormBox').addEventListener(ev, function (e) {
    var t = e.target;
    if (!t || !t.classList) return;
    t.classList.remove('campo-falta');
    if (t.id === 'fM-tipo-sw' || t.id === 'fM-tipo-hw') {
      var otro = document.getElementById(t.id === 'fM-tipo-sw' ? 'fM-tipo-hw' : 'fM-tipo-sw');
      if (otro && otro.classList) otro.classList.remove('campo-falta');
    }
  });
});""")

# --- (1) Fallback responsable/área + write-back ---
rep("""function renderMantOrder(m) {""",
"""// (255) Responsable y Área sin llenar al crear la orden: se toman de lo
// que el usuario envió al firmar (nombre y área del formulario de firma).
function mantRespOf(m) { return (m.responsable || (m.firma && m.firma.nombre) || ''); }
function mantAreaOf(m) { return (m.area || (m.firma && m.firma.area) || ''); }
// (255) Llena responsable/área con la firma llegada y lo guarda (update
// autenticado de la propia orden; nunca en firma.html, cuya regla pública
// solo deja tocar firma+estado). Solo si faltan: la guarda impide
// reescribir en bucle cuando la suscripción vuelva a disparar.
function mantFillFromFirma(m) {
  if (!m || !m.firma || !m.firma.firma) return false;
  if (m.estado === 'cancelada') return false;
  var cambio = false;
  if (!m.responsable && m.firma.nombre) { m.responsable = m.firma.nombre; cambio = true; }
  if (!m.area && m.firma.area) { m.area = m.firma.area; cambio = true; }
  if (!cambio) return false;
  if (CLOUD_ENABLED && cloudUser && (cloudRole === 'admin' || !m.tecnicoUid || m.tecnicoUid === cloudUser.uid)) mantSave(m);
  return true;
}
function renderMantOrder(m) {""")
rep("' · Área: ' + esc(m.area || '—') + '</div>' +",
    "' · Área: ' + esc(mantAreaOf(m) || 'Pendiente de firma') + '</div>' +")
rep("' · Responsable: ' + esc(m.responsable || '—') + '</div>' +",
    "' · Responsable: ' + esc(mantRespOf(m) || 'Pendiente de firma') + '</div>' +")
rep("(m.empresa || 'Lapi') + ' · ' + (m.tipo || '') + ' · ' + (m.area || '—') + ' · Responsable: ' + (m.responsable || '—')",
    "(m.empresa || 'Lapi') + ' · ' + (m.tipo || '') + ' · ' + (mantAreaOf(m) || '—') + ' · Responsable: ' + (mantRespOf(m) || '—')")
rep("""        if (mantOrderId && !document.getElementById('mantOrderBox').hidden) {
          var mo = mantFind(mantOrderId);
          if (mo) renderMantOrder(mo);
        }""",
"""        if (mantOrderId && !document.getElementById('mantOrderBox').hidden) {
          var mo = mantFind(mantOrderId);
          if (mo) { mantFillFromFirma(mo); renderMantOrder(mo); }
        }""")
rep("""    saveMantLocal();
    renderMant();
    renderMantOrder(m);""",
"""    saveMantLocal();
    renderMant();
    mantFillFromFirma(m);
    renderMantOrder(m);""")

# --- (5) assemblePdfOps: tamaño de página opcional (carta por defecto A4) ---
rep("""function assemblePdfOps(pages, images) {
  images = images || {};
  var W = 595, H = 842;""",
"""// (255) Tamaño de página opcional: carta (612x792) para la orden de
// servicio; por defecto A4 (595x842).
function assemblePdfOps(pages, images, pageSize) {
  images = images || {};
  var W = (pageSize && pageSize.w) || 595, H = (pageSize && pageSize.h) || 842;""")

# --- (5)+(4) buildPdfMant: carta + descripción solo hostname ---
rep("""// (254) Orden de servicio con el formato de papel F0.S1.01 Rev0: encabezado
// con las tres empresas, folio en rojo, casillas SOFTWARE/HARDWARE, los
// campos del formato y las firmas en sus bloques. Ningún dato actual se
// pierde: políticas, versiones, impresora, AnyDesk y observaciones
// detectadas van en Descripción del equipo / Conclusión. Si el contenido
// se desborda, fluye limpio a la página 2 (need() mueve la sección).""",
"""// (254) Orden de servicio con el formato de papel F0.S1.01 Rev0: encabezado
// con las tres empresas, folio en rojo, casillas SOFTWARE/HARDWARE, los
// campos del formato y las firmas en sus bloques. (255) Una hoja tamaño
// carta (612x792): la descripción del equipo lleva solo el hostname y los
// demás datos del equipo van al final, en Conclusión/Comentarios; ningún
// dato se pierde. Si el contenido se desborda, fluye limpio a la página 2
// (need() mueve la sección).""")
rep("""  var W = 595, H = 842, M = 36, USABLE = H - M * 2;""",
"""  var W = 612, H = 792, M = 36, USABLE = H - M * 2;""")
# Sección 1: encabezado más compacto y a lo ancho de carta.
rep("""  need(90);
  var y0 = yt;
  R(36, y0, 168, 90, null);""",
"""  need(84);
  var y0 = yt;
  R(36, y0, 168, 84, null);""")
rep("""    T('SISTEMAS', 44, y0 + 58, 'F2', 7);
    T('Rosa Blanca 63, Col. Molino de Rosas', 44, y0 + 66, 'F1', 7);
    T('C.P. 01470 Tel. 53371283 y 53370207', 44, y0 + 74, 'F1', 7);
    T('sistemas@lapi.com.mx, info@lapi.com.mx', 44, y0 + 82, 'F1', 6.5);""",
"""    T('SISTEMAS', 44, y0 + 56, 'F2', 7);
    T('Rosa Blanca 63, Col. Molino de Rosas', 44, y0 + 63, 'F1', 7);
    T('C.P. 01470 Tel. 53371283 y 53370207', 44, y0 + 70, 'F1', 7);
    T('sistemas@lapi.com.mx, info@lapi.com.mx', 44, y0 + 77, 'F1', 6.5);""")
rep("""  T('ORDEN DE SERVICIO', 385, y0 + 4, 'F2', 15, null, 'C');
  R(475, y0 + 24, 84, 24, null);
  T('FOLIO', 468, y0 + 30, 'F2', 8, null, 'R');
  T(val(m.folio), 517, y0 + 28, 'F2', 13, 'red', 'C');
  check(300, y0 + 56, tipoSW, 'SOFTWARE', 9);
  check(400, y0 + 56, tipoHW, 'HARDWARE', 9);
  yt += 90 + 4;""",
"""  T('ORDEN DE SERVICIO', 390, y0 + 4, 'F2', 15, null, 'C');
  R(492, y0 + 24, 84, 24, null);
  T('FOLIO', 485, y0 + 30, 'F2', 8, null, 'R');
  T(val(m.folio), 534, y0 + 28, 'F2', 13, 'red', 'C');
  check(308, y0 + 56, tipoSW, 'SOFTWARE', 9);
  check(408, y0 + 56, tipoHW, 'HARDWARE', 9);
  yt += 84 + 3;""")
# Sección 2: área/responsable con fallback de la firma.
rep("""  need(30);
  y0 = yt;
  R(36, y0, 257, 30, null); R(302, y0, 257, 30, null);
  T('ÁREA / UNIDAD', 42, y0 + 4, 'F2', 7);
  T(val(m.area), 42, y0 + 15, 'F1', 9);
  T('RESPONSABLE', 308, y0 + 4, 'F2', 7);
  T(val(m.responsable), 308, y0 + 15, 'F1', 9);
  yt += 30 + 4;""",
"""  need(28);
  y0 = yt;
  R(36, y0, 264, 28, null); R(312, y0, 264, 28, null);
  T('ÁREA / UNIDAD', 42, y0 + 4, 'F2', 7);
  T(val(mantAreaOf(m)), 42, y0 + 14, 'F1', 9);
  T('RESPONSABLE', 318, y0 + 4, 'F2', 7);
  T(val(mantRespOf(m)), 318, y0 + 14, 'F1', 9);
  yt += 28 + 3;""")
# Sección 3: tiempos a lo ancho de carta.
rep("""  need(34);
  y0 = yt;""",
"""  need(32);
  y0 = yt;""")
rep("""    ['NOMBRE DE QUIEN PRESTA EL SERVICIO', val(m.tecnico), 140],""",
"""    ['NOMBRE DE QUIEN PRESTA EL SERVICIO', val(m.tecnico), 145],""")
rep("""    R(x3, y0, c[2], 34, null);
    T(c[0], x3 + 3, y0 + 4, 'F2', i === 0 ? 6 : 5);
    T(c[1], x3 + 5, y0 + 16, 'F1', 8.5);
    x3 += c[2] + (i < campos3.length - 1 ? 3 : 0);
  });
  yt += 34 + 4;""",
"""    R(x3, y0, c[2], 32, null);
    T(c[0], x3 + 3, y0 + 4, 'F2', i === 0 ? 6 : 5);
    T(c[1], x3 + 5, y0 + 15, 'F1', 8.5);
    x3 += c[2] + (i < campos3.length - 1 ? 6 : 0);
  });
  yt += 32 + 3;""")
# Sección 4: título.
rep("""  R(36, y0 + 9, 523, 19, null);
  T(mantTituloCompuesto(m), 42, y0 + 13, 'F1', 9.5);
  yt += 28 + 4;""",
"""  R(36, y0 + 9, 540, 19, null);
  T(mantTituloCompuesto(m), 42, y0 + 13, 'F1', 9.5);
  yt += 28 + 3;""")
# Sección 5: tipo de falla.
rep("""  var fallaLines = wrapLines(val(m.tipoFalla), 511, 9);""",
"""  var fallaLines = wrapLines(val(m.tipoFalla), 528, 9);""")
rep("""  R(36, y0 + 9, 523, h5 - 9, 0.88);
  fallaLines.forEach(function (ln, i) { T(ln, 42, y0 + 13 + i * 11, 'F1', 9); });
  yt += h5 + 4;""",
"""  R(36, y0 + 9, 540, h5 - 9, 0.88);
  fallaLines.forEach(function (ln, i) { T(ln, 42, y0 + 13 + i * 11, 'F1', 9); });
  yt += h5 + 3;""")
# Sección 6: identificación.
rep("""    check(36 + i * 87, y0 + 10, !!(m.identificacion && m.identificacion[c[0]]), c[1], 9);
  });
  yt += 22 + 4;

  // 7. Descripción del equipo""",
"""    check(36 + i * 90, y0 + 10, !!(m.identificacion && m.identificacion[c[0]]), c[1], 9);
  });
  yt += 20 + 3;

  // 7. Descripción del equipo""")
# Sección 7: SOLO hostname (reemplazo por regex entre los comentarios 7 y 8).
rep_re(r"  // 7\. Descripción del equipo \(con hardware, versiones y políticas\)\..*?  yt \+= h7 \+ 4;\n",
"""  // 7. Descripción del equipo: SOLO el hostname (255). Los demás datos
  // del equipo (marca, modelo, serie, hardware, versiones, políticas,
  // impresora, AnyDesk y observaciones detectadas) van al final, en
  // Conclusión/Comentarios. Nada se pierde, solo se reubica.
  var ver = eq.versiones || {};
  var h7 = 9 + 6 + 10 + 6;
  need(h7);
  y0 = yt;
  T('DESCRIPCIÓN DEL EQUIPO', 36, y0, 'F2', 8);
  R(36, y0 + 9, 540, h7 - 9, null);
  T('Hostname: ' + val(eq.hostname), 42, y0 + 13, 'F1', 8.5);
  yt += h7 + 3;
""")
# Sección 8: condiciones.
rep("""  var notaLines = wrapLines('Notas: ' + val((m.condiciones && m.condiciones.notas) || ''), 511, 8.5);
  var h8 = 22 + notaLines.length * 10 + 4;""",
"""  var notaLines = wrapLines('Notas: ' + val((m.condiciones && m.condiciones.notas) || ''), 528, 8.5);
  var h8 = 20 + notaLines.length * 9.5 + 4;""")
rep("""    check(36 + i * 87, y0 + 10, !!(m.condiciones && m.condiciones[c[0]]), c[1], 9);
  });
  notaLines.forEach(function (ln, i) { T(ln, 42, y0 + 24 + i * 10, 'F1', 8.5); });
  yt += h8 + 4;""",
"""    check(36 + i * 90, y0 + 10, !!(m.condiciones && m.condiciones[c[0]]), c[1], 9);
  });
  notaLines.forEach(function (ln, i) { T(ln, 42, y0 + 22 + i * 9.5, 'F1', 8.5); });
  yt += h8 + 3;""")
# Sección 9: preventivo.
rep("""    check(240 + i * 53, y0 + 10, !!(m.preventivo && m.preventivo[c[0]]), c[1], 8);
  });
  yt += 22 + 4;""",
"""    check(250 + i * 55, y0 + 10, !!(m.preventivo && m.preventivo[c[0]]), c[1], 8);
  });
  yt += 20 + 3;""")
# Sección 10: cambios.
rep("""  var cambLines = wrapLines(val(m.descripcionCambios), 511, 9);""",
"""  var cambLines = wrapLines(val(m.descripcionCambios), 528, 9);""")
rep("""  R(36, y0 + 9, 523, h10 - 9, 0.88);
  cambLines.forEach(function (ln, i) { T(ln, 42, y0 + 13 + i * 11, 'F1', 9); });
  yt += h10 + 4;""",
"""  R(36, y0 + 9, 540, h10 - 9, 0.88);
  cambLines.forEach(function (ln, i) { T(ln, 42, y0 + 13 + i * 11, 'F1', 9); });
  yt += h10 + 3;""")
# Sección 11: conclusión + datos del equipo al final (reemplazo por regex).
rep_re(r"  // 11\. Conclusión y/o comentarios \(con observaciones\)\..*?  yt \+= h11 \+ 4;\n",
"""  // 11. Conclusión y/o comentarios (con observaciones).
  var conclLines = [];
  wrapLines('Conclusión: ' + val(m.conclusion), 528, 8.5).forEach(function (w) { conclLines.push(w); });
  if (m.comentarios) wrapLines('Comentarios: ' + m.comentarios, 528, 8.5).forEach(function (w) { conclLines.push(w); });
  if (m.observaciones) wrapLines('Observaciones del técnico: ' + m.observaciones, 528, 8.5).forEach(function (w) { conclLines.push(w); });
  if (m.observacionesDetectadas) wrapLines('Datos detectados: ' + m.observacionesDetectadas, 528, 8.5).forEach(function (w) { conclLines.push(w); });
  // (255) Datos del equipo al final: serie, modelo, tipo, marca, hardware,
  // IP/redes, impresora, AnyDesk, antivirus, SO, versiones, políticas y
  // usuario de sistemas — y la descripción escrita por el técnico.
  var eqLines = [];
  if (m.descripcionEquipo) eqLines.push('Descripción: ' + m.descripcionEquipo);
  eqLines.push('Serie: ' + val(eq.serie) + ', Modelo: ' + val(eq.modelo) + ', Tipo: ' + val(eq.tipo) + ', Marca: ' + val(eq.marca));
  eqLines.push('Procesador: ' + val(eq.cpu) + ', RAM: ' + ((eq.ramGB == null || eq.ramGB === '') ? '-' : eq.ramGB + ' GB') + ', Disco: ' + ((eq.discoGB == null || eq.discoGB === '') ? '-' : eq.discoGB + ' GB' + (eq.discoTipo ? ' ' + eq.discoTipo : '')));
  var rd11 = redesText(eq);
  eqLines.push('IP: ' + val(eq.ip) + (rd11 ? ', Redes: ' + rd11 : '') + ', Impresora: ' + val(eq.impresora));
  eqLines.push('AnyDesk: ' + (eq.anydeskId ? anydeskDisplay(eq.anydeskId) + (eq.anydeskAlias ? ' (' + eq.anydeskAlias + ')' : '') : '-') + ', Antivirus: ' + val(eq.antivirus) + ', SO: ' + val(eq.so));
  if (ver.so || ver.antivirus || ver.esetAgent || ver.chrome) {
    eqLines.push('Versiones: ' + [ver.so ? 'SO: ' + ver.so : '', ver.antivirus ? 'Antivirus: ' + ver.antivirus : '', ver.esetAgent ? 'Agente ESET: ' + ver.esetAgent : '', ver.chrome ? 'Chrome: ' + ver.chrome : ''].filter(Boolean).join(', '));
  }
  eqLines.push(pdfSafe(politicasText(pol)));
  eqLines.push('Usuario de sistemas: ' + (eq.usuarioSistemas ? 'Sí' : 'No'));
  eqLines.forEach(function (ln) { wrapLines(ln, 528, 8.5).forEach(function (w) { conclLines.push(w); }); });
  if (!conclLines.length) conclLines = ['-'];
  var h11 = 9 + 6 + conclLines.length * 9.5 + 6;
  need(h11);
  y0 = yt;
  T('CONCLUSIÓN Y/O COMENTARIOS DEL SERVICIO (SISTEMAS)', 36, y0, 'F2', 8);
  R(36, y0 + 9, 540, h11 - 9, null);
  conclLines.forEach(function (ln, i) { T(ln, 42, y0 + 13 + i * 9.5, 'F1', 8.5); });
  yt += h11 + 3;
""")
# Sección 12: cuatro bloques de fecha.
rep("""  need(64);
  y0 = yt;
  var fases = [""",
"""  need(58);
  y0 = yt;
  var fases = [""")
rep("""    var x = 36 + j * 132;""",
"""    var x = 36 + j * 135;""")
rep("""    R(x, y0 + 20, 61, 34, 0.88);
    R(x + 66, y0 + 20, 61, 34, 0.88);
    T('FIRMA', x + 30, y0 + 24, 'F1', 7, null, 'C');
    T('FIRMA', x + 96, y0 + 24, 'F1', 7, null, 'C');
    T('SISTEMAS', x + 30, y0 + 57, 'F1', 7, null, 'C');
    T('ÁREA SOLICITANTE', x + 96, y0 + 57, 'F1', 7, null, 'C');
    if (f[2]) { var d1 = fitImg(f[2], 57, 21); cur().push({ k: 'img', name: 'tecnico', x: x + 2, y: py(y0 + 31) - d1.h, w: d1.w, h: d1.h }); }
    else if (j === 3) T(m.tecnico || '-', x + 30, y0 + 32, 'F1', 7, null, 'C');
    if (f[3]) { var d2 = fitImg(f[3], 57, 21); cur().push({ k: 'img', name: 'usuario', x: x + 68, y: py(y0 + 31) - d2.h, w: d2.w, h: d2.h }); }
    else if (j === 3 && m.firma) T(m.firma.nombre || '-', x + 96, y0 + 32, 'F1', 7, null, 'C');
  });
  yt += 64 + 4;""",
"""    R(x, y0 + 19, 61, 32, 0.88);
    R(x + 66, y0 + 19, 61, 32, 0.88);
    T('FIRMA', x + 30, y0 + 22, 'F1', 7, null, 'C');
    T('FIRMA', x + 96, y0 + 22, 'F1', 7, null, 'C');
    T('SISTEMAS', x + 30, y0 + 54, 'F1', 7, null, 'C');
    T('ÁREA SOLICITANTE', x + 96, y0 + 54, 'F1', 7, null, 'C');
    if (f[2]) { var d1 = fitImg(f[2], 57, 18); cur().push({ k: 'img', name: 'tecnico', x: x + 2, y: py(y0 + 29) - d1.h, w: d1.w, h: d1.h }); }
    else if (j === 3) T(m.tecnico || '-', x + 30, y0 + 30, 'F1', 7, null, 'C');
    if (f[3]) { var d2 = fitImg(f[3], 57, 18); cur().push({ k: 'img', name: 'usuario', x: x + 68, y: py(y0 + 29) - d2.h, w: d2.w, h: d2.h }); }
    else if (j === 3 && m.firma) T(m.firma.nombre || '-', x + 96, y0 + 30, 'F1', 7, null, 'C');
  });
  yt += 58 + 3;""")
# Sección 13: comentarios + escala + conformidad.
rep("""  need(124);
  y0 = yt;
  R(36, y0, 250, 124, 0.88);
  T('COMENTARIOS', 42, y0 + 5, 'F2', 8);
  var comLines = (m.firma && m.firma.comentarios) ? wrapLines(m.firma.comentarios, 238, 8.5) : ['-'];
  comLines.forEach(function (ln, i) { T(ln, 42, y0 + 16 + i * 10, 'F1', 8.5); });
  var xr = 294;""",
"""  need(116);
  y0 = yt;
  R(36, y0, 258, 116, 0.88);
  T('COMENTARIOS', 42, y0 + 5, 'F2', 8);
  var comLines = (m.firma && m.firma.comentarios) ? wrapLines(m.firma.comentarios, 246, 8.5) : ['-'];
  comLines.forEach(function (ln, i) { T(ln, 42, y0 + 16 + i * 10, 'F1', 8.5); });
  var xr = 302;""")
rep("""  escLines.forEach(function (ln, i) { T(ln, xr, y0 + i * 8, 'F1', 6.5); });
  var sat = m.firma ? m.firma.satisfaccion : null;
  var yEsc = y0 + escLines.length * 8 + 6;""",
"""  escLines.forEach(function (ln, i) { T(ln, xr, y0 + i * 7.5, 'F1', 6.5); });
  var sat = m.firma ? m.firma.satisfaccion : null;
  var yEsc = y0 + escLines.length * 7.5 + 5;""")
rep("""  T('Escala de satisfacción (0-10): ' + satLabel(sat), xr, yEsc + 19, 'F1', 8);
  if (sat != null && sat !== '') {
    var marks = [];
    for (var i2 = 0; i2 <= 10; i2++) marks.push(i2 === Number(sat) ? '[' + i2 + ']' : String(i2));
    T(marks.join('  '), xr, yEsc + 29, 'F1', 8);
  }
  T('INACEPTABLE 0-3, ACEPTABLE 4-7, EXCELENTE 8-10', xr, yEsc + 39, 'F1', 7.5);
  var yConf = yEsc + 50;
  R(xr, yConf, 265, 124 - (yConf - y0), 0.88);""",
"""  T('Escala de satisfacción (0-10): ' + satLabel(sat), xr, yEsc + 17, 'F1', 8);
  if (sat != null && sat !== '') {
    var marks = [];
    for (var i2 = 0; i2 <= 10; i2++) marks.push(i2 === Number(sat) ? '[' + i2 + ']' : String(i2));
    T(marks.join('  '), xr, yEsc + 26, 'F1', 8);
  }
  T('INACEPTABLE 0-3, ACEPTABLE 4-7, EXCELENTE 8-10', xr, yEsc + 35, 'F1', 7.5);
  var yConf = yEsc + 46;
  R(xr, yConf, 274, 116 - (yConf - y0), 0.88);""")
rep("""    if (usrImg) { var d3 = fitImg(usrImg, 120, 20); cur().push({ k: 'img', name: 'usuario', x: xr + 5, y: py(yConf + 32) - d3.h, w: d3.w, h: d3.h }); }
    else T('Firma: ' + (m.firma.nombre || '-') + ' (guardada en la app)', xr + 5, yConf + 32, 'F1', 7.5);""",
"""    if (usrImg) { var d3 = fitImg(usrImg, 120, 14); cur().push({ k: 'img', name: 'usuario', x: xr + 5, y: py(yConf + 28) - d3.h, w: d3.w, h: d3.h }); }
    else T('Firma: ' + (m.firma.nombre || '-') + ' (guardada en la app)', xr + 5, yConf + 30, 'F1', 7.5);""")
rep("""  yt += 124 + 4;

  // 14. Pie del formato.""",
"""  yt += 116 + 3;

  // 14. Pie del formato.""")
# Sección 14: pie.
rep("""  T('Generado el ' + fmtDate(Date.now()) + ' - Checklist de Soporte', 297, y0, 'F1', 8, null, 'C');
  T('Rev0.', 559, y0, 'F1', 8, null, 'R');""",
"""  T('Generado el ' + fmtDate(Date.now()) + ' - Checklist de Soporte', 306, y0, 'F1', 8, null, 'C');
  T('Rev0.', 576, y0, 'F1', 8, null, 'R');""")
rep("""  return assemblePdfOps(pages, sigImgs);
}""",
"""  return assemblePdfOps(pages, sigImgs, { w: 612, h: 792 });
}""")

open(P, 'w', encoding='utf-8').write(s)
print('OK parche 2.5.5 aplicado; bytes antes=%d después=%d' % (len(orig), len(s)))
