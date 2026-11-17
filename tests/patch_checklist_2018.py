#!/usr/bin/env python3
"""Parche 2.0.18: el campo Analista responsable cambia con el login (antes se quedaba con el usuario anterior)."""
import re
P = '/home/hatch/workspace/android/checklist-cloud/www/index.html'
s = open(P).read()
orig = s

def rep(old, new, n=1):
    global s
    assert old in s, 'NO ENCONTRADO: ' + old[:90]
    s = s.replace(old, new, n)

# 1. Version visible
rep('Versión 2.0.17', 'Versión 2.0.18')
rep('Versión: 2.0.17', 'Versión: 2.0.18')
rep("Checklist de Soporte 2.0.17", "Checklist de Soporte 2.0.18")
rep('Versión de la app: 2.0.17', 'Versión de la app: 2.0.18')

# 2. prefillTecnico: actualizar el campo cuando cambia el usuario que inició sesión.
# Antes solo lo llenaba si estaba vacío, así que se quedaba con el analista anterior.
rep("""function prefillTecnico() {
  var f = document.getElementById('fTec');
  if (f && !f.value && technicianName()) f.value = technicianName();
  var t = document.getElementById('tecnicoLine');
  if (t) t.textContent = technicianName() ? 'Analista: ' + technicianName() : '';
}""",
"""var prefillUserName = '';
function prefillTecnico() {
  var f = document.getElementById('fTec');
  var name = technicianName();
  if (f && name && (!f.value || f.value === prefillUserName)) { f.value = name; prefillUserName = name; }
  var t = document.getElementById('tecnicoLine');
  if (t) t.textContent = name ? 'Analista: ' + name : '';
}""")

assert s != orig
open(P, 'w').write(s)
print('OK parche 2.0.18 aplicado')
print('Quedan "2.0.17":', len(re.findall(r'2\.0\.17', s)))
