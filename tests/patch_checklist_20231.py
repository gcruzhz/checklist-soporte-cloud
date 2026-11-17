#!/usr/bin/env python3
"""Parche 2.3.1: al usar un equipo detectado, la preparación nueva nace
con los puntos de software y hardware ya marcados por el detector.
- index.html: versión 2.3.1 (4 lugares + comentario), helpers
  filterDetectedChecks / detShortName / detLineFor / detectedNames,
  det-use guarda window._detectedChecks/_detectedDetalles, btnShowNew
  limpia el guardado, btnAdd crea la preparación con checks detectados
  y autoDetectado, prepToCloudDoc/prepFromCloud llevan autoDetectado,
  renderDetectados muestra la línea 'Detectado: ...', cardHtml muestra
  la nota 'Puntos marcados por el detector: ...', btnDetectar muestra
  progreso 'Detectando software...'.
- android/app/build.gradle: versionCode 44, versionName 2.3.1.
- firebase.js: SIN CAMBIOS (reportDetected ya pasa el objeto entero
  con setDoc merge, así que checks/detalles viajan tal cual).
Cada reemplazo con assert: si el texto viejo no está, se para.
"""
import re

def rep(s, old, new, n=1):
    assert old in s, 'NO ENCONTRADO: ' + old[:90]
    return s.replace(old, new, n)

# ---------- 1. index.html ----------
P = '/home/hatch/workspace/android/checklist-cloud/www/index.html'
s = open(P).read()
orig = s

# 1.0 Versión visible 2.3.1 (4 lugares + comentario del feature)
s = rep(s, 'Versión 2.3.0', 'Versión 2.3.1')
s = rep(s, 'Versión: 2.3.0', 'Versión: 2.3.1')
s = rep(s, 'Checklist de Soporte 2.3.0', 'Checklist de Soporte 2.3.1')
s = rep(s, 'Versión de la app: 2.3.0', 'Versión de la app: 2.3.1')
s = rep(s, '// Equipos detectados (2.3.0):', '// Equipos detectados (2.3.1):')
assert '2.3.0' not in s, 'queda 2.3.0 en index.html'

# 1.1 Helpers del detector (antes del comentario de renderDetectados)
s = rep(s, """// Equipos detectados (2.3.1): solo se listan los NO usados, con sus datos
// y dos acciones: usarlo (llena Nuevo equipo) o descartarlo.""",
"""// Checks del detector (2.3.1): el detector de escritorio reporta qué
// software encontró (d.checks) y detalles (d.detalles, p. ej.
// officeDetectado). Solo los ids de software de la plantilla actual
// pueden nacer marcados; hardware, datos, Invgate y la limpieza nunca.
var DETECTABLE_IDS = ['t6', 't7', 't8', 't9', 't10', 't11', 't18', 't19', 't20', 't21', 't22', 't23', 't24', 't25'];
var DET_SHORT = {
  t6: 'SO actualizado', t7: 'Antivirus', t8: 'Office', t9: 'Impresoras',
  t10: 'VPN', t11: 'Inicio rápido desactivado', t18: 'Chrome',
  t19: 'Adobe Reader', t20: 'WinRAR', t21: 'Lapi Fox', t22: 'Alfaweb',
  t23: 'Alfaprinter', t24: 'Accesos directos', t25: 'AnyDesk Gris'
};
function detShortName(id, val) {
  if (id === 't8') return (typeof val === 'string' && val) ? val : 'Office';
  if (DET_SHORT[id]) return DET_SHORT[id];
  var t = defaultTemplate().find(function (x) { return x.id === id; });
  return t ? t.text : id;
}
// Filtra los checks crudos del detector contra la plantilla actual:
// t8 solo si su valor es una de sus opciones; ids desconocidos se ignoran.
function filterDetectedChecks(raw) {
  var tpl = {};
  defaultTemplate().forEach(function (t) { tpl[t.id] = t; });
  var checks = {};
  var ids = [];
  DETECTABLE_IDS.forEach(function (id) {
    var t = tpl[id];
    if (!t) return;
    var v = raw ? raw[id] : undefined;
    if (id === 't8') {
      if (typeof v === 'string' && (t.options || []).indexOf(v) !== -1) { checks[id] = v; ids.push(id); }
      return;
    }
    if (v === true) { checks[id] = true; ids.push(id); }
  });
  return { checks: checks, ids: ids };
}
function detectedNames(checks, ids) {
  var list = ids || Object.keys(checks || {});
  return list.filter(function (id) { return checks && checks[id] !== undefined && checks[id] !== false; }).map(function (id) { return detShortName(id, checks[id]); });
}
function detLineFor(d) {
  var f = filterDetectedChecks(d.checks || {});
  var parts = detectedNames(f.checks, f.ids);
  if (d.detalles && d.detalles.officeDetectado && !f.checks.t8) parts.push('Office instalado, activación sin verificar');
  if (!parts.length) return '';
  return 'Detectado: ' + parts.map(function (n) { return esc(n); }).join(', ');
}
// Equipos detectados (2.3.1): solo se listan los NO usados, con sus datos
// y dos acciones: usarlo (llena Nuevo equipo) o descartarlo.""")

# 1.2 prepToCloudDoc / prepFromCloud llevan autoDetectado
s = rep(s, """    checks: p.checks || {}, extraItems: p.extraItems || [], reasignaciones: p.reasignaciones || [],
    equipo: { tipo: eq.tipo || '', marca: eq.marca || '', modelo: eq.modelo || '', serie: eq.serie || '', inventario: eq.inventario || '', hostname: eq.hostname || '', fotoSerie: foto },""",
"""    checks: p.checks || {}, extraItems: p.extraItems || [], reasignaciones: p.reasignaciones || [],
    autoDetectado: p.autoDetectado || [],
    equipo: { tipo: eq.tipo || '', marca: eq.marca || '', modelo: eq.modelo || '', serie: eq.serie || '', inventario: eq.inventario || '', hostname: eq.hostname || '', fotoSerie: foto },""")
s = rep(s, """    checks: doc.checks || {}, extraItems: doc.extraItems || [], reasignaciones: doc.reasignaciones || [],
    equipo: { tipo: eq.tipo || '', marca: eq.marca || '', modelo: eq.modelo || '', serie: eq.serie || '', inventario: eq.inventario || '', hostname: eq.hostname || '', fotoSerie: eq.fotoSerie || null },""",
"""    checks: doc.checks || {}, extraItems: doc.extraItems || [], reasignaciones: doc.reasignaciones || [],
    autoDetectado: doc.autoDetectado || [],
    equipo: { tipo: eq.tipo || '', marca: eq.marca || '', modelo: eq.modelo || '', serie: eq.serie || '', inventario: eq.inventario || '', hostname: eq.hostname || '', fotoSerie: eq.fotoSerie || null },""")

# 1.3 renderDetectados: línea 'Detectado: ...' con lo detectado
s = rep(s, """  box.innerHTML = list.map(function (d) {
    return '<div class="card"><h2>' + esc(d.hostname || 'Equipo') + '</h2>' +""",
"""  box.innerHTML = list.map(function (d) {
    var detLine = detLineFor(d);
    return '<div class="card"><h2>' + esc(d.hostname || 'Equipo') + '</h2>' +""")
s = rep(s, """      '<div class="sub">Detectado ' + timeAgo(d.detectadoEn) + (d.detectadoPor ? ' por ' + esc(d.detectadoPor) : '') + '</div>' +""",
"""      '<div class="sub">Detectado ' + timeAgo(d.detectadoEn) + (d.detectadoPor ? ' por ' + esc(d.detectadoPor) : '') + '</div>' +
      (detLine ? '<div class="sub">' + detLine + '</div>' : '') +""")

# 1.4 cardHtml: nota del detector (solo tarjeta completa)
s = rep(s, """  var deliveredLine = p.deliveredAt ? '<div class="delivered-line">Entregado el ' + fmtDate(p.deliveredAt) + '</div>' : '';""",
"""  var deliveredLine = p.deliveredAt ? '<div class="delivered-line">Entregado el ' + fmtDate(p.deliveredAt) + '</div>' : '';
  var detNote = (p.autoDetectado && p.autoDetectado.length)
    ? '<div class="sub">Puntos marcados por el detector: ' + esc(detectedNames(p.checks, p.autoDetectado).join(', ')) + '</div>' : '';""")
s = rep(s, """    '<div class="pct">' + pct + '% completado</div>' + deliveredLine + reassignLine +""",
"""    '<div class="pct">' + pct + '% completado</div>' + deliveredLine + reassignLine + detNote +""")

# 1.5 btnShowNew: abrir el formulario en blanco limpia el guardado
s = rep(s, """document.getElementById('btnShowNew').addEventListener('click', function () { togglePanel('newBox'); });""",
"""document.getElementById('btnShowNew').addEventListener('click', function () { window._detectedChecks = null; window._detectedDetalles = null; togglePanel('newBox'); });""")

# 1.6 btnDetectar: progreso mientras la promesa está pendiente
s = rep(s, """document.getElementById('btnDetectar').addEventListener('click', function () {
  if (!window.Desktop || !window.Desktop.detect) { alert('La detección solo funciona en la app de escritorio.'); return; }
  if (!cloudUser) { alert('Inicia sesión para reportar el equipo detectado.'); return; }
  var p;
  try { p = Promise.resolve(window.Desktop.detect()); } catch (e) { alert('No se pudo detectar el equipo.'); return; }
  p.then(function (info) {
    if (!window.Cloud || !window.Cloud.reportDetected) throw new Error('sin-nube');
    var data = Object.assign({}, info || {});
    data.detectadoPor = technicianName();
    return window.Cloud.reportDetected(data);
  }).then(function () { alert('Equipo detectado, ya aparece en los teléfonos'); }).catch(function (e) { alert('No se pudo detectar el equipo.' + (e && e.message ? ' ' + e.message : '')); });
});""",
"""document.getElementById('btnDetectar').addEventListener('click', function () {
  var btn = document.getElementById('btnDetectar');
  if (!window.Desktop || !window.Desktop.detect) { alert('La detección solo funciona en la app de escritorio.'); return; }
  if (!cloudUser) { alert('Inicia sesión para reportar el equipo detectado.'); return; }
  var oldHtml = btn.innerHTML;
  btn.disabled = true;
  btn.innerHTML = '<span class="ic">&#128187;</span><span>Detectando software...</span>';
  var p;
  try { p = Promise.resolve(window.Desktop.detect()); } catch (e) { btn.disabled = false; btn.innerHTML = oldHtml; alert('No se pudo detectar el equipo.'); return; }
  p.then(function (info) {
    if (!window.Cloud || !window.Cloud.reportDetected) throw new Error('sin-nube');
    var data = Object.assign({}, info || {});
    data.detectadoPor = technicianName();
    return window.Cloud.reportDetected(data);
  }).then(function () { alert('Equipo detectado, ya aparece en los teléfonos'); }).catch(function (e) { alert('No se pudo detectar el equipo.' + (e && e.message ? ' ' + e.message : '')); }).then(function () { btn.disabled = false; btn.innerHTML = oldHtml; });
});""")

# 1.7 det-use: guarda los checks y detalles detectados para ese uso
s = rep(s, """    document.getElementById('fHostname').value = d.hostname || '';
    cloudMarkDetectadoUsado(d.id);""",
"""    document.getElementById('fHostname').value = d.hostname || '';
    window._detectedChecks = d.checks || {};
    window._detectedDetalles = d.detalles || {};
    cloudMarkDetectadoUsado(d.id);""")

# 1.8 btnAdd: la preparación nace con los checks detectados
s = rep(s, """  var v = function (id) { return document.getElementById(id).value.trim(); };
  var prep = {
    id: uid(), createdAt: Date.now(), deliveredAt: null, readyAt: null, checks: {}, extraItems: [], reasignaciones: [],
    equipo: { tipo: v('fTipo'), marca: v('fMarca'), modelo: v('fModelo'), serie: v('fSerie'), inventario: v('fInv'), hostname: v('fHostname'), fotoSerie: window._fotoSerie || null },""",
"""  var v = function (id) { return document.getElementById(id).value.trim(); };
  var det = filterDetectedChecks(window._detectedChecks || {});
  var prep = {
    id: uid(), createdAt: Date.now(), deliveredAt: null, readyAt: null, checks: det.checks, autoDetectado: det.ids, extraItems: [], reasignaciones: [],
    equipo: { tipo: v('fTipo'), marca: v('fMarca'), modelo: v('fModelo'), serie: v('fSerie'), inventario: v('fInv'), hostname: v('fHostname'), fotoSerie: window._fotoSerie || null },""")
s = rep(s, """  state.preparations.push(prep);
  cloudUpsertPrep(prep);
  save();
  ['fMarca', 'fModelo', 'fSerie', 'fInv', 'fHostname', 'fTec', 'fUser', 'fArea', 'fCorreo'].forEach(function (id) { document.getElementById(id).value = ''; });""",
"""  state.preparations.push(prep);
  window._detectedChecks = null;
  window._detectedDetalles = null;
  cloudUpsertPrep(prep);
  save();
  ['fMarca', 'fModelo', 'fSerie', 'fInv', 'fHostname', 'fTec', 'fUser', 'fArea', 'fCorreo'].forEach(function (id) { document.getElementById(id).value = ''; });""")

assert s != orig
open(P, 'w').write(s)
print('OK index.html')

# ---------- 2. android/app/build.gradle ----------
P = '/home/hatch/workspace/android/checklist-cloud/android/app/build.gradle'
s = open(P).read()
orig = s
s = rep(s, '        versionCode 43', '        versionCode 44')
s = rep(s, '        versionName "2.3.0"', '        versionName "2.3.1"')
assert s != orig
open(P, 'w').write(s)
print('OK build.gradle')
print('Parche 2.3.1 aplicado')
