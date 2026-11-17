#!/usr/bin/env python3
"""Parche 2.0.20b: aviso cuando falta elegir Office + limpieza del chat al entrar."""
import re
P = '/home/hatch/workspace/android/checklist-cloud/www/index.html'
s = open(P).read()
orig = s

def rep(old, new, n=1):
    global s
    assert old in s, 'NO ENCONTRADO: ' + old[:90]
    s = s.replace(old, new, n)

# 1. Version visible
rep('Versión 2.0.19', 'Versión 2.0.20')
rep('Versión: 2.0.19', 'Versión: 2.0.20')
rep("Checklist de Soporte 2.0.19", "Checklist de Soporte 2.0.20")
rep('Versión de la app: 2.0.19', 'Versión de la app: 2.0.20')

# 2. CSS del aviso de opción pendiente
rep("  .msg.mine .txt { background: #e8f3df; border-radius: 10px; padding: 6px 9px; display: inline-block; }",
    "  .msg.mine .txt { background: #e8f3df; border-radius: 10px; padding: 6px 9px; display: inline-block; }\n  .choice-hint { color: #b3261e; font-size: 13px; font-weight: 700; }")

# 3. Tarjeta: si falta elegir Office, avisar con ⚠️
rep("""      if (it.options) {
        var opts = it.options.map(function (o) {
          var sel = p.checks[it.id] === o;
          return '<button class="chip' + (sel ? ' on' : '') + '" data-choice="' + it.id + '" data-prep="' + p.id + '" data-value="' + esc(o) + '"' + (locked ? ' disabled' : '') + '>' + esc(o) + '</button>';
        }).join(' ');
        return '<div class="item' + (checked ? ' done' : '') + '" style="flex-wrap:wrap">' +
          '<label>' + esc(it.text) + '</label> ' + opts + del + '</div>';
      }""",
"""      if (it.options) {
        var opts = it.options.map(function (o) {
          var sel = p.checks[it.id] === o;
          return '<button class="chip' + (sel ? ' on' : '') + '" data-choice="' + it.id + '" data-prep="' + p.id + '" data-value="' + esc(o) + '"' + (locked ? ' disabled' : '') + '>' + esc(o) + '</button>';
        }).join(' ');
        var hint = checked ? '' : ' <span class="choice-hint">⚠️ Elige una opción</span>';
        return '<div class="item' + (checked ? ' done' : '') + '" style="flex-wrap:wrap">' +
          '<label>' + esc(it.text) + '</label> ' + opts + hint + del + '</div>';
      }""")

# 4. Nota del chat: los mensajes se borran a las 24 horas
rep("Quién está en línea ahora y el chat interno del equipo. Los mensajes los ven todos los usuarios activos.",
    "Quién está en línea ahora y el chat interno del equipo. Los mensajes los ven todos los usuarios activos y se borran solos después de 24 horas: el chat no guarda historial.")

# 5. Al entrar, limpiar los mensajes viejos del chat
rep("""  var beat = function () { window.Cloud.heartbeat(technicianName(), cloudRole || 'usuario'); };
  beat();""",
"""  var beat = function () { window.Cloud.heartbeat(technicianName(), cloudRole || 'usuario'); };
  beat();
  if (window.Cloud.pruneChat) window.Cloud.pruneChat();""")

assert s != orig
open(P, 'w').write(s)
print('OK parche 2.0.20b (index.html) aplicado')
print('Quedan "2.0.19":', len(re.findall(r'2\.0\.19', s)))
