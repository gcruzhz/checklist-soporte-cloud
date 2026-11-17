#!/usr/bin/env python3
"""Parche 2.2.1b: los botones de IA encuentran su equipo (data-ai-falta/data-ai-wa
no estaban en la lista de atributos que resuelve el id del equipo)."""
P = '/home/hatch/workspace/android/checklist-cloud/www/index.html'
s = open(P).read()
orig = s

def rep(old, new, n=1):
    global s
    assert old in s, 'NO ENCONTRADO: ' + old[:90]
    s = s.replace(old, new, n)

# ---------- 1. Versión visible ----------
rep('Versión 2.2.0', 'Versión 2.2.1')
rep('Versión: 2.2.0', 'Versión: 2.2.1')
rep('Checklist de Soporte 2.2.0', 'Checklist de Soporte 2.2.1')
rep('Versión de la app: 2.2.0', 'Versión de la app: 2.2.1')

# ---------- 2. El arreglo: los botones de IA resuelven el id del equipo ----------
rep("""  var prepId = q('data-prep') || q('data-deliver') || q('data-ready') || q('data-unready') || q('data-reopen') || q('data-add-extra') || q('data-del-prep') || q('data-save-extra') || q('data-pdf') || q('data-xlsx') || q('data-wa') || q('data-mail') || q('data-reassign') || q('data-save-reassign') || q('data-expand') || q('data-collapse') || q('data-choice');""",
"""  var prepId = q('data-prep') || q('data-deliver') || q('data-ready') || q('data-unready') || q('data-reopen') || q('data-add-extra') || q('data-del-prep') || q('data-save-extra') || q('data-pdf') || q('data-xlsx') || q('data-wa') || q('data-mail') || q('data-reassign') || q('data-save-reassign') || q('data-expand') || q('data-collapse') || q('data-choice') || q('data-ai-falta') || q('data-ai-wa');""")

assert s != orig
open(P, 'w').write(s)
print('OK parche 2.2.1b (index.html) aplicado')
print('Quedan "2.2.0":', len(__import__('re').findall(r'2\.2\.0', s)))
