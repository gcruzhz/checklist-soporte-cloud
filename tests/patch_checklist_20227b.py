#!/usr/bin/env python3
"""Parche 2.2.7b: campo Hostname en equipo nuevo y en reasignado.
El detector de escritorio (2.3.0) lo llenará solo. El campo se guarda en
equipo.hostname, se sincroniza, se muestra en la tarjeta, el PDF, el Excel
y el WhatsApp, y se puede buscar."""
P = '/home/hatch/workspace/android/checklist-cloud/www/index.html'
s = open(P).read()
orig = s

def rep(old, new, n=1):
    global s
    assert old in s, 'NO ENCONTRADO: ' + old[:90]
    s = s.replace(old, new, n)

# ---------- 1. Versión visible ----------
rep('Versión 2.2.6', 'Versión 2.2.7')
rep('Versión: 2.2.6', 'Versión: 2.2.7')
rep('Checklist de Soporte 2.2.6', 'Checklist de Soporte 2.2.7')
rep('Versión de la app: 2.2.6', 'Versión de la app: 2.2.7')

# ---------- 2. Formulario equipo nuevo ----------
rep('<div class="field"><label>No. de inventario</label><input id="fInv" placeholder="Inventario / activo"></div>',
    '<div class="field"><label>No. de inventario</label><input id="fInv" placeholder="Inventario / activo"></div>\n        <div class="field"><label>Hostname</label><input id="fHostname" placeholder="Nombre del equipo en la red"></div>')

# ---------- 3. Formulario reasignar (Otro equipo) ----------
rep('<div class="field"><label>No. de inventario</label><input id="fReInv" placeholder="Inventario / activo"></div>',
    '<div class="field"><label>No. de inventario</label><input id="fReInv" placeholder="Inventario / activo"></div>\n          <div class="field"><label>Hostname</label><input id="fReHostname" placeholder="Nombre del equipo en la red"></div>')

# ---------- 4. Guardar equipo nuevo ----------
rep("equipo: { tipo: v('fTipo'), marca: v('fMarca'), modelo: v('fModelo'), serie: v('fSerie'), inventario: v('fInv'), fotoSerie: window._fotoSerie || null },",
    "equipo: { tipo: v('fTipo'), marca: v('fMarca'), modelo: v('fModelo'), serie: v('fSerie'), inventario: v('fInv'), hostname: v('fHostname'), fotoSerie: window._fotoSerie || null },")
rep("['fMarca', 'fModelo', 'fSerie', 'fInv', 'fTec', 'fUser', 'fArea', 'fCorreo']",
    "['fMarca', 'fModelo', 'fSerie', 'fInv', 'fHostname', 'fTec', 'fUser', 'fArea', 'fCorreo']")

# ---------- 5. Guardar reasignación (Otro equipo) ----------
rep("equipo: { tipo: v('fReTipo'), marca: v('fReMarca'), modelo: v('fReModelo'), serie: v('fReSerie'), inventario: v('fReInv'), fotoSerie: null },",
    "equipo: { tipo: v('fReTipo'), marca: v('fReMarca'), modelo: v('fReModelo'), serie: v('fReSerie'), inventario: v('fReInv'), hostname: v('fReHostname'), fotoSerie: null },")

# ---------- 6. Sincronización nube ----------
rep("equipo: { tipo: eq.tipo || '', marca: eq.marca || '', modelo: eq.modelo || '', serie: eq.serie || '', inventario: eq.inventario || '', fotoSerie: foto },",
    "equipo: { tipo: eq.tipo || '', marca: eq.marca || '', modelo: eq.modelo || '', serie: eq.serie || '', inventario: eq.inventario || '', hostname: eq.hostname || '', fotoSerie: foto },")
rep("equipo: { tipo: eq.tipo || '', marca: eq.marca || '', modelo: eq.modelo || '', serie: eq.serie || '', inventario: eq.inventario || '', fotoSerie: eq.fotoSerie || null },",
    "equipo: { tipo: eq.tipo || '', marca: eq.marca || '', modelo: eq.modelo || '', serie: eq.serie || '', inventario: eq.inventario || '', hostname: eq.hostname || '', fotoSerie: eq.fotoSerie || null },")

# ---------- 7. PDF ----------
rep("row('No. de inventario: ' + (prep.equipo.inventario || '—'), 'F1', 11);",
    "row('No. de inventario: ' + (prep.equipo.inventario || '—'), 'F1', 11);\n  row('Hostname: ' + (prep.equipo.hostname || '—'), 'F1', 11);")

# ---------- 8. Excel ----------
rep("var headers = ['Tipo', 'Marca', 'Modelo', 'No. de serie', 'No. de inventario', 'Usuario', 'Área', 'Correo', 'Analista', 'Estado', 'Avance %', 'Creado', 'Entregado', 'Reasignaciones'];",
    "var headers = ['Tipo', 'Marca', 'Modelo', 'No. de serie', 'No. de inventario', 'Hostname', 'Usuario', 'Área', 'Correo', 'Analista', 'Estado', 'Avance %', 'Creado', 'Entregado', 'Reasignaciones'];")
rep("return [p.equipo.tipo, p.equipo.marca, p.equipo.modelo, p.equipo.serie, p.equipo.inventario,",
    "return [p.equipo.tipo, p.equipo.marca, p.equipo.modelo, p.equipo.serie, p.equipo.inventario, p.equipo.hostname,")

# ---------- 9. WhatsApp (uno y varios) ----------
rep("    'Inventario: ' + (p.equipo.inventario || '—'),",
    "    'Inventario: ' + (p.equipo.inventario || '—'),\n    'Hostname: ' + (p.equipo.hostname || '—'),")
rep("""      ' — Serie: ' + (p.equipo.serie || '—') +
      ' — ' + (p.usuario.nombre || 'sin usuario') +""",
"""      ' — Serie: ' + (p.equipo.serie || '—') +
      (p.equipo.hostname ? ' — Host: ' + p.equipo.hostname : '') +
      ' — ' + (p.usuario.nombre || 'sin usuario') +""")

# ---------- 10. Tarjeta ----------
rep("'<div class=\"sub\">' + esc(p.equipo.tipo) + ' · Serie: ' + esc(p.equipo.serie || '—') + ' · Inv: ' + esc(p.equipo.inventario || '—') + '</div>' +",
    "'<div class=\"sub\">' + esc(p.equipo.tipo) + ' · Serie: ' + esc(p.equipo.serie || '—') + ' · Inv: ' + esc(p.equipo.inventario || '—') + (p.equipo.hostname ? ' · Host: ' + esc(p.equipo.hostname) : '') + '</div>' +")

# ---------- 11. Búsqueda ----------
rep("var hay = [p.equipo.tipo, p.equipo.marca, p.equipo.modelo, p.equipo.serie, p.equipo.inventario,",
    "var hay = [p.equipo.tipo, p.equipo.marca, p.equipo.modelo, p.equipo.serie, p.equipo.inventario, p.equipo.hostname,")

assert s != orig
open(P, 'w').write(s)
print('OK parche 2.2.7b (index.html) aplicado')
print('Quedan "2.2.6":', len(__import__('re').findall(r'2\.2\.6', s)))
print('hostname en index:', s.count('hostname'), '| fHostname:', s.count('fHostname'), '| fReHostname:', s.count('fReHostname'))
