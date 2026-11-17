# -*- coding: utf-8 -*-
"""Parche 2.5.5 parte B: puntos 6 y 7 (renta).
6) La opcion de exportar existe (boton "Abrir" la generaba) pero ningun
   boton decia "Exportar a Excel": el encabezado decia "Exportar a Excel:"
   y el boton decia "Abrir". Se renombra el boton en ambas vistas de renta
   a "Exportar a Excel" y se deshabilita cuando no hay nada que exportar.
7) (a) Seleccion en Entrega Renta: checkbox por equipo entregado +
   Seleccionar todos / Ninguno; WhatsApp/Correo/Exportar actuan sobre la
   seleccion, o sobre todos los entregados si no hay seleccion (con toast).
   (b) Visibilidad 15 dias: el entregado lo sigue viendo el usuario normal
   15 dias (entregadoAt, respaldo createdAt); pasado ese tiempo solo admin.
   Se guarda entregadoAt al entregar y se limpia al reabrir; rentaToCloudDoc
   y rentaFromCloud lo incluyen para que sobreviva la nube.
Uso: python3 tests/patch_20255b.py
"""
import io, sys

P = '/home/hatch/workspace/android/checklist-cloud/www/index.html'
s = io.open(P, encoding='utf-8').read()
n0 = len(s)

def rep(old, new, cnt=1, tag=''):
    global s
    c = s.count(old)
    assert c == cnt, 'REP %s: esperado %d, hallado %d: %r' % (tag, cnt, c, old[:90])
    s = s.replace(old, new)

# --- PUNTO 6: boton "Exportar a Excel" en ambas vistas de renta ---
rep('<button class="btn-green" id="btnAbrirRec">📂 Abrir</button>',
    '<button class="btn-green" id="btnAbrirRec">📊 Exportar a Excel</button>', tag='P6-rec-btn')
rep('<button class="btn-green" id="btnAbrirFor">📂 Abrir</button>',
    '<button class="btn-green" id="btnAbrirFor">📊 Exportar a Excel</button>', tag='P6-for-btn')

# --- PUNTO 7: estado de seleccion + helpers (antes de rentaList) ---
rep('''function rentaList(flow) {''',
'''// (255) Seleccion en Entrega Renta: checkbox por equipo entregado.
// Compartir (WhatsApp/correo) y Exportar a Excel actuan sobre los
// marcados; sin seleccion, sobre todos los entregados visibles.
var rentaSelFor = {};
// (255) Entregados de renta: como Por preparar (DELIVERED_VISIBLE_DAYS =
// 15) — el usuario normal los sigue viendo 15 dias despues de la entrega;
// pasado ese tiempo solo los ve el admin. Sin entregadoAt (registros
// viejos), se usa createdAt como respaldo.
function rentaEntregadoVisible(r) {
  if (!r || r.estado !== 'entregado') return true;
  if (!CLOUD_ENABLED || cloudRole === 'admin') return true;
  var t = r.entregadoAt || r.createdAt || 0;
  return (Date.now() - t) <= DELIVERED_VISIBLE_DAYS * 86400000;
}
function rentaEntregadosFor() {
  return rentaList('for').filter(function (r) { return r.estado === 'entregado'; });
}
function rentaSelListFor() {
  var todos = rentaEntregadosFor();
  var sel = todos.filter(function (r) { return rentaSelFor[r.id]; });
  return { todos: todos, sel: sel };
}
function rentaSelTodosFor(sel) {
  rentaEntregadosFor().forEach(function (r) { if (sel) rentaSelFor[r.id] = true; else delete rentaSelFor[r.id]; });
  render();
}
function rentaActualizarSelInfo() {
  var el = document.getElementById('rentaSelInfo');
  if (!el) return;
  var l = rentaSelListFor();
  el.textContent = l.sel.length ? ('Seleccionados: ' + l.sel.length + ' de ' + l.todos.length + ' entregados.') : ('Sin selección: se exportan/comparten todos los entregados (' + l.todos.length + ').');
}
function rentaList(flow) {''', tag='P7-helpers')

# --- PUNTO 7b: filtro de 15 dias en rentaList('for') ---
rep('''  var list = state.renta.slice();
  // Entregados solo los ve el admin; a los usuarios ya no les aparecen.
  if (CLOUD_ENABLED && cloudRole !== 'admin') list = list.filter(function (r) { return r.estado !== 'entregado'; });
  return list.sort(function (a, b) { return a.createdAt - b.createdAt; });''',
'''  var list = state.renta.slice();
  // Entregados: el usuario normal los ve 15 dias (rentaEntregadoVisible);
  // pasado ese tiempo solo los ve el admin.
  list = list.filter(rentaEntregadoVisible);
  return list.sort(function (a, b) { return a.createdAt - b.createdAt; });''', tag='P7-rentaList')

# --- PUNTO 7b: mismo filtro en entregaCola ---
rep('''  var list = state.renta.slice();
  // Entregados solo los ve el admin; a los usuarios ya no les aparecen.
  if (CLOUD_ENABLED && cloudRole !== 'admin') list = list.filter(function (r) { return r.estado !== 'entregado'; });
  return list.sort(function (a, b) { return (orden[a.tipo] - orden[b.tipo]) || (a.createdAt - b.createdAt); });''',
'''  var list = state.renta.slice();
  // Entregados: el usuario normal los ve 15 dias (rentaEntregadoVisible);
  // pasado ese tiempo solo los ve el admin.
  list = list.filter(rentaEntregadoVisible);
  return list.sort(function (a, b) { return (orden[a.tipo] - orden[b.tipo]) || (a.createdAt - b.createdAt); });''', tag='P7-entregaCola')

# --- PUNTO 6: boton de exportar deshabilitado sin datos (renderRenta) ---
rep('''function renderRenta(flow) {
  var list = rentaList(flow);
  var box = document.getElementById(flow === 'rec' ? 'list-rec' : 'list-for');''',
'''function renderRenta(flow) {
  var list = rentaList(flow);
  var btnExp = document.getElementById(flow === 'rec' ? 'btnAbrirRec' : 'btnAbrirFor');
  if (btnExp) btnExp.disabled = flow === 'rec' ? !list.length : !list.some(function (r) { return r.estado === 'entregado'; });
  var box = document.getElementById(flow === 'rec' ? 'list-rec' : 'list-for');''', tag='P6-renderRenta')

# --- PUNTO 6+7: renderEntrega — boton deshabilitado sin entregados + seccion de seleccion ---
rep('''function renderEntrega() {
  var box = document.getElementById('list-for');
  var cola = entregaCola();''',
'''function renderEntrega() {
  var box = document.getElementById('list-for');
  var cola = entregaCola();
  var btnExpFor = document.getElementById('btnAbrirFor');
  if (btnExpFor) btnExpFor.disabled = !cola.some(function (r) { return r.estado === 'entregado'; });''', tag='P7-renderEntrega-btn')

rep('''    var msg = (CLOUD_ENABLED && cloudRole !== 'admin' && state.renta.length)
      ? 'No hay equipos por entregar. Los ya entregados solo los ve el administrador.'
      : 'No hay equipos de renta todavía. Agrégalos en Recibir renta.';''',
'''    var msg = (CLOUD_ENABLED && cloudRole !== 'admin' && state.renta.length)
      ? 'No hay equipos por entregar. Los entregados hace más de 15 días solo los ve el administrador.'
      : 'No hay equipos de renta todavía. Agrégalos en Recibir renta.';''', tag='P7-renderEntrega-msg')

rep('''  html += '<div class="actions">' +
    '<button class="btn-ghost" data-entrega-nav="prev"' + (idx === 0 ? ' disabled' : '') + '>← Anterior</button>' +
    '<button class="btn-ghost" data-entrega-nav="next"' + (idx === cola.length - 1 ? ' disabled' : '') + '>Siguiente →</button></div>';
  box.innerHTML = html;
}''',
'''  html += '<div class="actions">' +
    '<button class="btn-ghost" data-entrega-nav="prev"' + (idx === 0 ? ' disabled' : '') + '>← Anterior</button>' +
    '<button class="btn-ghost" data-entrega-nav="next"' + (idx === cola.length - 1 ? ' disabled' : '') + '>Siguiente →</button></div>';
  var entregados = cola.filter(function (r) { return r.estado === 'entregado'; });
  if (entregados.length) {
    html += '<div class="sub" style="margin-top:14px"><b>Equipos entregados (' + entregados.length + ')</b> — marca los que quieres exportar o compartir:</div>';
    html += '<div class="actions"><button class="btn-ghost" data-renta-sel-all>Seleccionar todos</button><button class="btn-ghost" data-renta-sel-none>Ninguno</button></div>';
    html += '<div class="share-note" id="rentaSelInfo"></div>';
    html += entregados.map(function (r) {
      var chk = rentaSelFor[r.id] ? ' checked' : '';
      return '<div class="sub"><label><input type="checkbox" data-renta-sel="' + esc(r.id) + '"' + chk + ' style="width:auto"> ' + esc(r.tipo + ' ' + (r.modelo || '') + ' · Inv. ' + (r.inventario || '—') + ' · Entregado por ' + (r.entregadoPor || '—')) + '</label></div>';
    }).join('');
  }
  box.innerHTML = html;
  rentaActualizarSelInfo();
}''', tag='P7-renderEntrega-sel')

# --- PUNTO 7: entregadoAt al crear (null) y al entregar/reabrir ---
rep("    recibidoPor: technicianName(), entregadoPor: ''",
    "    recibidoPor: technicianName(), entregadoPor: '', entregadoAt: null", tag='P7-saveRenta')
rep("    recibidoPor: rec.recibidoPor || '', entregadoPor: rec.entregadoPor || '',",
    "    recibidoPor: rec.recibidoPor || '', entregadoPor: rec.entregadoPor || '', entregadoAt: rec.entregadoAt || null,", tag='P7-toCloud')
rep("    recibidoPor: doc.recibidoPor || '', entregadoPor: doc.entregadoPor || ''",
    "    recibidoPor: doc.recibidoPor || '', entregadoPor: doc.entregadoPor || '', entregadoAt: doc.entregadoAt || null", tag='P7-fromCloud')
rep('''    rec.estado = 'entregado';
    rec.entregadoPor = technicianName();''',
'''    rec.estado = 'entregado';
    rec.entregadoPor = technicianName();
    rec.entregadoAt = Date.now();''', tag='P7-deliver')
rep("  if (t.hasAttribute('data-renta-reopen')) { rec.estado = 'revisado'; rec.entregadoPor = ''; cloudUpsert(rec); save(); render(); return; }",
    "  if (t.hasAttribute('data-renta-reopen')) { rec.estado = 'revisado'; rec.entregadoPor = ''; rec.entregadoAt = null; cloudUpsert(rec); save(); render(); return; }", tag='P7-reopen')

# --- PUNTO 7a: exportar/compartir usan la seleccion en 'for' ---
rep('''async function openXlsxRenta(flow) {
  var list = rentaList(flow);
  if (!list.length) { showToast('No hay equipos de renta en esta sección.'); return; }''',
'''async function openXlsxRenta(flow) {
  var list = rentaList(flow);
  if (flow === 'for') {
    var lSel = rentaSelListFor();
    if (!lSel.todos.length) { showToast('No hay equipos de renta en esta sección.'); return; }
    list = lSel.sel.length ? lSel.sel : lSel.todos;
    if (!lSel.sel.length) showToast('Sin selección: se exportan todos los equipos entregados.');
  }
  if (!list.length) { showToast('No hay equipos de renta en esta sección.'); return; }''', tag='P7-openXlsxRenta')
rep('''async function shareRentaFile(flow, channel) {
  var list = rentaList(flow);
  if (!list.length) { showToast('No hay equipos de renta en esta sección.'); return; }''',
'''async function shareRentaFile(flow, channel) {
  var list = rentaList(flow);
  if (flow === 'for') {
    var lSel2 = rentaSelListFor();
    if (!lSel2.todos.length) { showToast('No hay equipos de renta en esta sección.'); return; }
    list = lSel2.sel.length ? lSel2.sel : lSel2.todos;
    if (!lSel2.sel.length) showToast('Sin selección: se comparten todos los equipos entregados.');
  }
  if (!list.length) { showToast('No hay equipos de renta en esta sección.'); return; }''', tag='P7-shareRentaFile')

# --- PUNTO 7a: botones Seleccionar todos / Ninguno en el dispatch de #list-for ---
rep('''    if (sig >= 0 && sig < cola.length) { state.entregaActual = cola[sig].id; save(); render(); }
    return;
  }''',
'''    if (sig >= 0 && sig < cola.length) { state.entregaActual = cola[sig].id; save(); render(); }
    return;
  }
  if (t.closest('[data-renta-sel-all]')) { rentaSelTodosFor(true); return; }
  if (t.closest('[data-renta-sel-none]')) { rentaSelTodosFor(false); return; }''', tag='P7-sel-btns')

# --- PUNTO 7a: listener 'change' para los checkboxes de seleccion ---
rep('''});

// Acceso con huella (biométricos del teléfono + credencial guardada segura).''',
'''});
document.getElementById('list-for').addEventListener('change', function (e) {
  var t = e.target;
  var cb = t.closest ? t.closest('[data-renta-sel]') : null;
  if (!cb) return;
  var id = cb.getAttribute('data-renta-sel');
  if (!id) return;
  if (cb.checked) rentaSelFor[id] = true; else delete rentaSelFor[id];
  rentaActualizarSelInfo();
});

// Acceso con huella (biométricos del teléfono + credencial guardada segura).''', tag='P7-change-listener')

io.open(P, 'w', encoding='utf-8').write(s)
print('OK patch 20255b: %d -> %d bytes' % (n0, len(s)))
