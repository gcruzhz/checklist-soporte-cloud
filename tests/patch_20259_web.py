# Parche web 2.5.9: compartir características de un equipo detectado
# por WhatsApp y por correo (ambos paneles de detectados).
import sys

P = '/home/hatch/workspace/android/checklist-cloud/www/index.html'
s = open(P, encoding='utf-8').read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'NO ENCONTRADO x%d (esperado %d): %r' % (c, n, old[:120])
    s = s.replace(old, new)

# --- 1. Botones de compartir en cada tarjeta de #detList (Por preparar).
rep("""      '<div class="actions"><button class="btn-green" data-det-use="' + esc(d.id) + '">Usar este equipo</button>' +
      '<button class="btn-dark" data-det-save="' + esc(d.id) + '">💾 Guardar para después</button>' +
      '<button class="btn-ghost" data-det-del="' + esc(d.id) + '">Descartar</button></div></div>';""",
"""      '<div class="actions"><button class="btn-green" data-det-use="' + esc(d.id) + '">Usar este equipo</button>' +
      '<button class="btn-dark" data-det-save="' + esc(d.id) + '">💾 Guardar para después</button>' +
      '<button class="btn-dark" data-det-wa="' + esc(d.id) + '">📲 Compartir por WhatsApp</button>' +
      '<button class="btn-dark" data-det-mail="' + esc(d.id) + '">✉️ Compartir por correo</button>' +
      '<button class="btn-ghost" data-det-del="' + esc(d.id) + '">Descartar</button></div></div>';""")

# --- 2. Botones de compartir en cada tarjeta de #mantDetList (Mantenimientos).
rep("""            '<div class="actions"><button class="btn-green" data-mant-det-use="' + esc(d.id) + '">🔧 Dar mantenimiento a este equipo</button></div></div>';""",
"""            '<div class="actions"><button class="btn-green" data-mant-det-use="' + esc(d.id) + '">🔧 Dar mantenimiento a este equipo</button>' +
            '<button class="btn-dark" data-mant-det-wa="' + esc(d.id) + '">📲 Compartir por WhatsApp</button>' +
            '<button class="btn-dark" data-mant-det-mail="' + esc(d.id) + '">✉️ Compartir por correo</button></div></div>';""")

# --- 3. Texto y correo para compartir un detectado (después de shareAvanceMail).
rep("""// Avance por correo: abre el correo con el resumen como cuerpo del mensaje.
function shareAvanceMail(p) {
  var asunto = 'Avance — ' + (p.equipo.marca || 'Equipo') + ' ' + (p.equipo.modelo || '');
  window.location.href = 'mailto:?subject=' + encodeURIComponent(asunto) + '&body=' + encodeURIComponent(avanceText(p));
}""",
"""// Avance por correo: abre el correo con el resumen como cuerpo del mensaje.
function shareAvanceMail(p) {
  var asunto = 'Avance — ' + (p.equipo.marca || 'Equipo') + ' ' + (p.equipo.modelo || '');
  window.location.href = 'mailto:?subject=' + encodeURIComponent(asunto) + '&body=' + encodeURIComponent(avanceText(p));
}
// Texto para compartir un equipo detectado (259): solo las
// características que el detector realmente encontró; los campos vacíos
// se omiten (no se imprime '—' ni 'sin datos'). Funciona aunque el
// equipo aún no se haya guardado como preparación: es solo el documento
// detectado. Reutiliza los helpers de formato (hardware, redes, AnyDesk,
// versiones, políticas, impresora, usuario de sistemas).
function detShareText(d) {
  d = d || {};
  var det = d.detalles || {};
  var ver = d.versiones || {};
  var lines = ['🖥️ Checklist de Soporte — Equipo detectado', ''];
  var titulo = ((d.marca || '') + ' ' + (d.modelo || '')).trim();
  lines.push(titulo || 'Equipo detectado');
  if (d.tipo) lines.push('Tipo: ' + d.tipo);
  if (d.serie) lines.push('Serie: ' + d.serie);
  if (d.hostname) lines.push('Hostname: ' + d.hostname);
  var hw = hardwareLine(d);
  if (hw) lines.push(hw);
  var rd = redesLine(d);
  if (rd) lines.push(rd);
  var ad = anydeskLine(d);
  if (ad) lines.push(ad);
  var vl = versionesLine(ver);
  if (vl) lines.push(vl);
  if (d.so && !ver.so) lines.push('SO: ' + d.so);
  var av = ver.antivirus || d.antivirus || det.antivirus || '';
  if (av && vl.indexOf('Antivirus:') === -1) lines.push('Antivirus: ' + av);
  var imp = d.impresora || det.impresora || '';
  if (imp) lines.push('Impresora: ' + imp);
  var pol = d.politicas || det.politicas || null;
  if (pol) lines.push(politicasText(pol));
  var us = (typeof d.usuarioSistemas !== 'undefined') ? d.usuarioSistemas : det.usuarioSistemas;
  if (typeof us === 'boolean') lines.push('Usuario de sistemas: ' + (us ? 'Sí' : 'No'));
  var esc2 = escritorioLine(d);
  if (esc2) lines.push(esc2);
  var osf = osFuenteLine(d);
  if (osf) lines.push(osf);
  var detL = detLineFor(d);
  if (detL) lines.push(detL);
  if (d.detectadoEn) lines.push('Detectado: ' + fmtDate(d.detectadoEn) + (d.detectadoPor ? ' por ' + d.detectadoPor : ''));
  else if (d.detectadoPor) lines.push('Detectado por: ' + d.detectadoPor);
  return lines.join('\\n');
}
// Compartir un equipo detectado por correo: asunto con hostname o modelo
// y el mismo texto en el cuerpo (mismo patrón mailto: de shareAvanceMail).
function detShareMail(d) {
  var asunto = 'Equipo detectado: ' + (d.hostname || d.modelo || 'Equipo');
  window.location.href = 'mailto:?subject=' + encodeURIComponent(asunto) + '&body=' + encodeURIComponent(detShareText(d));
}""")

# --- 4. Listener de #detList: atender data-det-wa y data-det-mail.
# (259) Compartir características: no marca el equipo como usado ni
# guarda nada; solo abre WhatsApp o el correo con el texto.
rep("""document.getElementById('detList').addEventListener('click', function (e) {
  var t = e.target;
  var use = t.closest('[data-det-use]');
  var del = t.closest('[data-det-del]');
  var sav = t.closest('[data-det-save]');
  if (!use && !del && !sav) return;
  var id = (use || del || sav).getAttribute(use ? 'data-det-use' : del ? 'data-det-del' : 'data-det-save');""",
"""document.getElementById('detList').addEventListener('click', function (e) {
  var t = e.target;
  var use = t.closest('[data-det-use]');
  var del = t.closest('[data-det-del]');
  var sav = t.closest('[data-det-save]');
  var wa = t.closest('[data-det-wa]');
  var mail = t.closest('[data-det-mail]');
  if (!use && !del && !sav && !wa && !mail) return;
  var el = use || del || sav || wa || mail;
  var id = el.getAttribute(use ? 'data-det-use' : del ? 'data-det-del' : sav ? 'data-det-save' : wa ? 'data-det-wa' : 'data-det-mail');
  // (259) Compartir características: no marca el equipo como usado ni
  // guarda nada; solo abre WhatsApp o el correo con el texto.
  if (wa || mail) {
    var dd = detectados.find(function (x) { return String(x.id) === String(id); });
    if (!dd) return;
    if (wa) shareText(detShareText(dd)); else detShareMail(dd);
    return;
  }""")

# --- 5. Listener de #mantDetList: atender data-mant-det-wa y data-mant-det-mail.
rep("""document.getElementById('mantDetList').addEventListener('click', function (e) {
  var b = e.target.closest('[data-mant-det-use]');
  if (b) mantUseDetectado(b.getAttribute('data-mant-det-use'));
});""",
"""document.getElementById('mantDetList').addEventListener('click', function (e) {
  var b = e.target.closest('[data-mant-det-use]');
  if (b) { mantUseDetectado(b.getAttribute('data-mant-det-use')); return; }
  // (259) Compartir características del equipo detectado (igual que en
  // Por preparar): no marca el equipo como usado ni guarda nada.
  var wa = e.target.closest('[data-mant-det-wa]');
  var mail = e.target.closest('[data-mant-det-mail]');
  if (!wa && !mail) return;
  var el = wa || mail;
  var dd = detectados.find(function (x) { return String(x.id) === String(el.getAttribute(wa ? 'data-mant-det-wa' : 'data-mant-det-mail')); });
  if (!dd) return;
  if (wa) shareText(detShareText(dd)); else detShareMail(dd);
});""")

# --- 6. Versiones 2.5.9 + mailto 259.
rep('Versión 2.5.8', 'Versión 2.5.9')
rep('Versión: 2.5.8', 'Versión: 2.5.9')
rep('Reporte de problema - Checklist de Soporte 258', 'Reporte de problema - Checklist de Soporte 259')
rep('Versión de la app: 258', 'Versión de la app: 259')

open(P, 'w', encoding='utf-8').write(s)
print('OK index.html, bytes:', len(s))
print('2.5.9:', s.count('2.5.9'), '| 2.5.8 restante:', s.count('2.5.8'), '| 258 mailto restante:', s.count('Soporte 258'))
print('data-det-wa:', s.count('data-det-wa'), '| data-det-mail:', s.count('data-det-mail'), '| data-mant-det-wa:', s.count('data-mant-det-wa'), '| data-mant-det-mail:', s.count('data-mant-det-mail'), '| detShareText:', s.count('detShareText'), '| detShareMail:', s.count('detShareMail'))
