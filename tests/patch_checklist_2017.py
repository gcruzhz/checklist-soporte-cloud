#!/usr/bin/env python3
"""Parche 2.0.17: el botón grande Reasignar Equipo sí lo ven todos (corrección de Gerardo)."""
import re
P = '/home/hatch/workspace/android/checklist-cloud/www/index.html'
s = open(P).read()
orig = s

def rep(old, new, n=1):
    global s
    assert old in s, 'NO ENCONTRADO: ' + old[:90]
    s = s.replace(old, new, n)

# 1. Version visible
rep('Versión 2.0.16', 'Versión 2.0.17')
rep('Versión: 2.0.16', 'Versión: 2.0.17')
rep("Checklist de Soporte 2.0.16", "Checklist de Soporte 2.0.17")
rep('Versión de la app: 2.0.16', 'Versión de la app: 2.0.17')

# 2. El botón grande Reasignar Equipo ya no se oculta para los usuarios
rep("""  document.getElementById('tabUsuarios').hidden = !isAdmin;
  document.getElementById('btnShowRe').hidden = !isAdmin;""",
"""  document.getElementById('tabUsuarios').hidden = !isAdmin;""")

# 3. Guardar reasignación ya no exige ser admin (si no, el botón visible no guardaría nada)
rep("""document.getElementById('btnReGuardar').addEventListener('click', function () {
  if (cloudRole !== 'admin') return;
  var id = document.getElementById('fReEquipo').value;""",
"""document.getElementById('btnReGuardar').addEventListener('click', function () {
  var id = document.getElementById('fReEquipo').value;""")

assert s != orig
open(P, 'w').write(s)
print('OK parche 2.0.17 aplicado')
print('Quedan "2.0.16":', len(re.findall(r'2\.0\.16', s)))
print('Quedan "btnShowRe\').hidden":', len(re.findall(r"btnShowRe'\)\.hidden", s)))
