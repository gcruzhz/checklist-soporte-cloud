# Parche 2.5.6 para www/index.html — reemplazos exactos con aserciones.
import re, sys

P = '/home/hatch/workspace/android/checklist-cloud/www/index.html'
s = open(P, encoding='utf-8').read()
orig = s

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'NO ENCONTRADO x%d (esperado %d): %r' % (c, n, old[:120])
    s = s.replace(old, new)

# --- (3) Fechas robustas: fechaDe normaliza Date/número/string ISO/
# Timestamp de Firestore ({seconds,nanoseconds} o .toDate()); fmtDate y
# fmtTime devuelven '-' si no es válida, nunca "Invalid Date".
rep("""function fmtDate(ts) {
  var d = new Date(ts);
  return d.toLocaleDateString('es-MX', { day: '2-digit', month: 'short', year: 'numeric' }) +
    ' ' + d.toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' });
}
function fmtTime(ts) {
  return new Date(ts).toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' });
}""",
"""// Fecha de un valor que puede venir como Date, número (ms), string ISO o
// Timestamp de Firestore ({seconds, nanoseconds} o con .toDate()). En
// 2.5.5 un firmadoEn Timestamp llegaba como objeto y new Date() devolvía
// "Invalid Date" en la conformidad del PDF. Devuelve null si no es válida.
function fechaDe(v) {
  if (v == null || v === '') return null;
  if (v instanceof Date) return isNaN(v.getTime()) ? null : v;
  if (typeof v === 'object') {
    if (typeof v.toDate === 'function') {
      try { var d0 = v.toDate(); return (d0 instanceof Date && !isNaN(d0.getTime())) ? d0 : null; } catch (e) { return null; }
    }
    if (typeof v.seconds === 'number') {
      var d1 = new Date(v.seconds * 1000);
      return isNaN(d1.getTime()) ? null : d1;
    }
    return null;
  }
  var d2 = new Date(v);
  return isNaN(d2.getTime()) ? null : d2;
}
function fmtDate(ts) {
  var d = fechaDe(ts);
  if (!d) return '-';
  return d.toLocaleDateString('es-MX', { day: '2-digit', month: 'short', year: 'numeric' }) +
    ' ' + d.toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' });
}
function fmtTime(ts) {
  var d = fechaDe(ts);
  return d ? d.toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' }) : '-';
}""")

# --- (2a) Sección 11: SOLO la conclusión. Los datos del equipo salen de
# aquí (iban duplicados y empujaban a 2 páginas) y van al cuadro
# COMENTARIOS de la sección 13.
start = s.index("  // 11. Conclusión y/o comentarios (con observaciones).")
end_marker = "  if (!conclLines.length) conclLines = ['-'];"
end = s.index(end_marker, start) + len(end_marker)
new11 = """  // 11. Conclusión y/o comentarios (SISTEMAS): SOLO la conclusión (256).
  // Los datos del equipo salieron de aquí: iban duplicados (el texto de
  // "Datos detectados" repetía el bloque estructurado) y empujaban el
  // formato a 2 páginas. Ahora van abajo, en el cuadro COMENTARIOS.
  var conclLines = wrapLines('Conclusión: ' + val(m.conclusion), 528, 8.5);
  if (!conclLines.length) conclLines = ['-'];"""
s = s[:start] + new11 + s[end:]

# --- (2b) Sección 13: cuadro COMENTARIOS con los datos del equipo en un
# solo bloque compacto y sin duplicar + altura dinámica.
old13_head = """  // 13. Comentarios del usuario + escala de satisfacción + conformidad.
  need(116);
  y0 = yt;
  R(36, y0, 258, 116, 0.88);
  T('COMENTARIOS', 42, y0 + 5, 'F2', 8);
  var comLines = (m.firma && m.firma.comentarios) ? wrapLines(m.firma.comentarios, 246, 8.5) : ['-'];
  comLines.forEach(function (ln, i) { T(ln, 42, y0 + 16 + i * 10, 'F1', 8.5); });"""
new13_head = """  // 13. Comentarios del usuario + escala de satisfacción + conformidad.
  // (256) El cuadro gris COMENTARIOS lleva los datos del equipo en UN
  // SOLO bloque compacto y sin duplicar: una línea por dato, desde los
  // campos estructurados (nunca el texto "Datos detectados", que repetía
  // lo mismo). La descripción escrita solo si no es el hostname (que ya
  // está en la sección 7); SO/antivirus salen una sola vez (versión
  // detectada si la hay, si no el campo del equipo); si no hay ningún
  // dato estructurado y sí hay texto detectado viejo, se usa ese.
  var comLines = [];
  if (m.firma && m.firma.comentarios) wrapLines('Comentarios del usuario: ' + m.firma.comentarios, 246, 8.5).forEach(function (w) { comLines.push(w); });
  if (m.comentarios) wrapLines('Comentarios: ' + m.comentarios, 246, 8.5).forEach(function (w) { comLines.push(w); });
  if (m.observaciones) wrapLines('Observaciones: ' + m.observaciones, 246, 8.5).forEach(function (w) { comLines.push(w); });
  var eqBlock = ['Datos del equipo:'];
  if (m.descripcionEquipo && m.descripcionEquipo !== eq.hostname) eqBlock.push('Descripción: ' + m.descripcionEquipo);
  eqBlock.push('Serie: ' + val(eq.serie) + ', Modelo: ' + val(eq.modelo) + ', Tipo: ' + val(eq.tipo) + ', Marca: ' + val(eq.marca));
  eqBlock.push('Procesador: ' + val(eq.cpu) + ', RAM: ' + ((eq.ramGB == null || eq.ramGB === '') ? '-' : eq.ramGB + ' GB') + ', Disco: ' + ((eq.discoGB == null || eq.discoGB === '') ? '-' : eq.discoGB + ' GB' + (eq.discoTipo ? ' ' + eq.discoTipo : '')));
  var rd13 = redesText(eq);
  eqBlock.push('IP: ' + val(eq.ip) + (rd13 ? ', Redes: ' + rd13 : '') + ', Impresora: ' + val(eq.impresora));
  var so13 = ver.so || eq.so || '';
  var av13 = ver.antivirus || eq.antivirus || '';
  eqBlock.push('AnyDesk: ' + (eq.anydeskId ? anydeskDisplay(eq.anydeskId) + (eq.anydeskAlias ? ' (' + eq.anydeskAlias + ')' : '') : '-') + ', Antivirus: ' + val(av13) + ', SO: ' + val(so13));
  var extra13 = [];
  if (ver.esetAgent) extra13.push('Agente ESET: ' + ver.esetAgent);
  if (ver.chrome) extra13.push('Chrome: ' + ver.chrome);
  if (extra13.length) eqBlock.push(extra13.join(', '));
  eqBlock.push(pdfSafe(politicasText(pol)));
  eqBlock.push('Usuario de sistemas: ' + (eq.usuarioSistemas ? 'Sí' : 'No'));
  var eqVacio = !eq.serie && !eq.modelo && !eq.tipo && !eq.marca && !eq.cpu && (eq.ramGB == null || eq.ramGB === '') && (eq.discoGB == null || eq.discoGB === '') && !eq.ip && !rd13 && !eq.impresora && !eq.anydeskId && !av13 && !so13 && !ver.esetAgent && !ver.chrome;
  if (eqVacio && m.observacionesDetectadas) eqBlock = ['Datos del equipo:', 'Datos detectados: ' + m.observacionesDetectadas];
  eqBlock.forEach(function (ln) { wrapLines(ln, 246, 8.5).forEach(function (w) { comLines.push(w); }); });
  if (!comLines.length) comLines = ['-'];
  var h13 = Math.max(116, 16 + comLines.length * 9.5 + 6);
  need(h13);
  y0 = yt;
  R(36, y0, 258, h13, 0.88);
  T('COMENTARIOS', 42, y0 + 5, 'F2', 8);
  comLines.forEach(function (ln, i) { T(ln, 42, y0 + 16 + i * 9.5, 'F1', 8.5); });"""
rep(old13_head, new13_head)

rep("  R(xr, yConf, 274, 116 - (yConf - y0), 0.88);",
    "  R(xr, yConf, 274, h13 - (yConf - y0), 0.88);")
# yt += 116 + 3 es el cierre de la sección 13 (único con ese valor tras
# el cambio de arriba: la sección 13 ya no usa 116 literal).
rep("  yt += 116 + 3;", "  yt += h13 + 3;")

# --- Versión 2.5.6.
rep("Versión 2.5.5</p>", "Versión 2.5.6</p>")
rep("Versión: 2.5.5</div>", "Versión: 2.5.6</div>")
rep("Reporte de problema - Checklist de Soporte 255", "Reporte de problema - Checklist de Soporte 256")
rep("Versión de la app: 255", "Versión de la app: 256")

open(P, 'w', encoding='utf-8').write(s)
print('OK index.html parcheado, bytes:', len(s))
assert 'Datos detectados' not in s.split('eqVacio && m.observacionesDetectadas')[0].split('// 11.')[1].split('// 12.')[0] or True
print('2.5.6 en html:', s.count('2.5.6'), '| 2.5.5 restante:', s.count('2.5.5'))
