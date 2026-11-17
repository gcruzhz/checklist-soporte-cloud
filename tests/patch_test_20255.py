# -*- coding: utf-8 -*-
"""Parche tests telefono 2.5.5.
- test20255.js: checklist20254.js -> checklist20255.js y aserciones de
  version 2.5.4 -> 2.5.5 (anterior 2.5.3 -> 2.5.4).
- Inserta la serie 255 (tests/test-255-snippet.js) antes de process.exit.
Uso: python3 tests/patch_test_20255.py
"""
import io

P = '/home/hatch/workspace/android/checklist-cloud/tests/test20255.js'
s = io.open(P, encoding='utf-8').read()
n0 = len(s)

def rep(old, new, cnt=1, tag=''):
    global s
    c = s.count(old)
    assert c == cnt, 'REP %s: esperado %d, hallado %d: %r' % (tag, cnt, c, old[:90])
    s = s.replace(old, new)

rep("const SRC = fs.readFileSync(__dirname + '/checklist20254.js', 'utf8');",
    "const SRC = fs.readFileSync(__dirname + '/checklist20255.js', 'utf8');", tag='src')
rep("console.log('AM0) versión 2.5.4:', html.includes('Versión 2.5.4'), '| sin 2.5.2:', !html.includes('Versión 2.5.3')",
    "console.log('AM0) versión 2.5.5:', html.includes('Versión 2.5.5'), '| sin 2.5.4:', !html.includes('Versión 2.5.4')", tag='AM0')
rep("console.log('AP0) estáticos 2.5.4: versión:', html.includes('Versión 2.5.4') && !html.includes('Versión 2.5.3')",
    "console.log('AP0) estáticos 2.5.5: versión:', html.includes('Versión 2.5.5') && !html.includes('Versión 2.5.4')", tag='AP0')
rep("  // AR0: versión 2.5.4 en los lugares visibles y 0 de 2.5.3 en todo el html.",
    "  // AR0: versión 2.5.5 en los lugares visibles y 0 de 2.5.4 en todo el html.", tag='AR0-com')
rep("  var n254 = (html.match(/2\\.5\\.4/g) || []).length;",
    "  var n255 = (html.match(/2\\.5\\.5/g) || []).length;", tag='AR0-n')
rep("  console.log('AR0) versión 2.5.4 visible:', html.includes('Versión 2.5.4') && html.includes('Versión: 2.5.4'), '| 0 de 2.5.3:', !html.includes('2.5.3'), '| ocurrencias 2.5.4:', n254 === 2);",
    "  console.log('AR0) versión 2.5.5 visible:', html.includes('Versión 2.5.5') && html.includes('Versión: 2.5.5'), '| 0 de 2.5.4:', !html.includes('2.5.4'), '| ocurrencias 2.5.5:', n255 === 2);", tag='AR0')
rep("  var ba0html = html.includes('Versión 2.5.4') && html.includes('Versión: 2.5.4') && !html.includes('2.5.3');",
    "  var ba0html = html.includes('Versión 2.5.5') && html.includes('Versión: 2.5.5') && !html.includes('2.5.4');", tag='BA0')
rep("  console.log('BA0) versión 2.5.4 sin 2.5.3:', ba0html,",
    "  console.log('BA0) versión 2.5.5 sin 2.5.4:', ba0html,", tag='BA0-log')
rep("  // BB0: versión 2.5.4 en 2 sitios exactos, 0 de 2.5.3 y 0 diálogos nativos.",
    "  // BB0: versión 2.5.5 en 2 sitios exactos, 0 de 2.5.4 y 0 diálogos nativos.", tag='BB0-com')
rep("  console.log('BB0) 2.5.4 en 2 sitios:', n254 === 2, '| 0 de 2.5.3:', !html.includes('2.5.3'), '| 0 alert/confirm/prompt:', bb0nat);",
    "  console.log('BB0) 2.5.5 en 2 sitios:', n255 === 2, '| 0 de 2.5.4:', !html.includes('2.5.4'), '| 0 alert/confirm/prompt:', bb0nat);", tag='BB0')

snip = io.open('/home/hatch/workspace/android/checklist-cloud/tests/test-255-snippet.js', encoding='utf-8').read()
anchor = "  process.exit(0);\n})();\n"
assert s.count(anchor) == 1, 'ancla process.exit no hallada'
s = s.replace(anchor, snip + "\n" + anchor)

io.open(P, 'w', encoding='utf-8').write(s)
print('OK patch test 20255: %d -> %d caracteres' % (n0, len(s)))
