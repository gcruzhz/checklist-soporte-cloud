#!/usr/bin/env python3
"""Parche 2.0.16: quitar 'Cuenta de red creada' de la plantilla; PDF/Reasignar/Eliminar solo admin; Limpieza fisica solo para reasignados."""
import re
P = '/home/hatch/workspace/android/checklist-cloud/www/index.html'
s = open(P).read()
orig = s

def rep(old, new, n=1):
    global s
    assert old in s, 'NO ENCONTRADO: ' + old[:90]
    s = s.replace(old, new, n)

# 1. Version visible
rep('Versión 2.0.15', 'Versión 2.0.16')
rep('Versión: 2.0.15', 'Versión: 2.0.16')
rep("Checklist de Soporte 2.0.15", "Checklist de Soporte 2.0.16")
rep('Versión de la app: 2.0.15', 'Versión de la app: 2.0.16')

# 2. Plantilla: fuera t14 (Cuenta de red creada); t26 Limpieza solo para reasignados
rep("    { id: 't4', group: 'hardware', text: 'Etiqueta de inventario y número de serie registrados' },",
    "    { id: 't4', group: 'hardware', text: 'Etiqueta de inventario y número de serie registrados' },\n    { id: 't26', group: 'hardware', text: 'Limpieza física del equipo', reassignOnly: true },")
rep("    { id: 't14', group: 'datos', text: 'Cuenta de red creada' },\n", "")

# 3. Migracion v3: la plantilla guardada pierde t14 y gana t26, conservando los puntos del usuario
rep("  if (state.templateVersion === 2) return;\n  var oldIds = ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12', 't13', 't14', 't15', 't16', 't17'];",
    "  if (state.templateVersion === 3) return;\n  var oldIds = ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12', 't13', 't14', 't15', 't16', 't17', 't18', 't19', 't20', 't21', 't22', 't23', 't24', 't25'];")
rep("  state.templateVersion = 2;\n  save();",
    "  state.templateVersion = 3;\n  save();")

# 4. allItems: los puntos solo-reasignacion solo aparecen en equipos reasignados
rep("""function allItems(prep) {
  var items = state.template.map(function (t) { return { id: t.id, group: t.group, text: t.text, extra: false, options: t.options, optional: !!t.optional }; });""",
"""function allItems(prep) {
  var isRe = !!(prep.reasignaciones && prep.reasignaciones.length);
  var items = state.template.filter(function (t) { return !t.reassignOnly || isRe; }).map(function (t) { return { id: t.id, group: t.group, text: t.text, extra: false, options: t.options, optional: !!t.optional, reassignOnly: !!t.reassignOnly }; });""")

# 5. Tarjeta: PDF / Compartir, Reasignar y Eliminar solo para el admin
rep("""  actions += '<button class="btn-dark" data-pdf="' + p.id + '">PDF / Compartir</button>';""",
"""  if (cloudRole === 'admin') actions += '<button class="btn-dark" data-pdf="' + p.id + '">PDF / Compartir</button>';""")
rep("""  actions += '<button class="btn-ghost" data-reassign="' + p.id + '">Reasignar</button>';
  actions += '<button class="btn-danger" data-del-prep="' + p.id + '">Eliminar</button>';""",
"""  if (cloudRole === 'admin') actions += '<button class="btn-ghost" data-reassign="' + p.id + '">Reasignar</button>';
  if (cloudRole === 'admin') actions += '<button class="btn-danger" data-del-prep="' + p.id + '">Eliminar</button>';""")

# 6. El boton grande "Reasignar Equipo" tambien es solo para el admin
rep("""  document.getElementById('tabUsuarios').hidden = !isAdmin;""",
"""  document.getElementById('tabUsuarios').hidden = !isAdmin;
  document.getElementById('btnShowRe').hidden = !isAdmin;""")

# 7. Guardar reasignacion: solo admin (por si el panel se abre por otro camino)
rep("""document.getElementById('btnReGuardar').addEventListener('click', function () {
  var id = document.getElementById('fReEquipo').value;""",
"""document.getElementById('btnReGuardar').addEventListener('click', function () {
  if (cloudRole !== 'admin') return;
  var id = document.getElementById('fReEquipo').value;""")

# 8. Editor de plantilla: marcar el punto solo-reasignacion
rep("""    return '<div class="tpl-item"><span class="tag">' + GROUPS[t.group] + '</span><span>' + esc(t.text) + '</span>' +""",
"""    return '<div class="tpl-item"><span class="tag">' + GROUPS[t.group] + '</span><span>' + esc(t.text) + (t.reassignOnly ? ' <i>(solo reasignación)</i>' : '') + '</span>' +""")

assert s != orig
open(P, 'w').write(s)
print('OK parche 2.0.16 aplicado')
print('Quedan "2.0.15":', len(re.findall(r'2\.0\.15', s)))
print('Quedan "Cuenta de red creada":', len(re.findall(r'Cuenta de red creada', s)))
print('Limpieza física:', len(re.findall(r'Limpieza física del equipo', s)))
