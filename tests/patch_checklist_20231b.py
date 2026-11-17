#!/usr/bin/env python3
"""Parche 2.3.1b: t3/t4 también detectables.

El encargo de 2.3.1 mapea t3 (batería) y t4 (serie) como auto-marcables
por el detector, y la lista de nunca-marcar es solo t1/t2/t26, t12 y
t13-t17. El parche 2.3.1a los dejó fuera de DETECTABLE_IDS por error;
aquí se corrige en index.html y en la serie AO del test.
"""
import re
import sys

ROOT = '/home/hatch/workspace/android/checklist-cloud/'
HTML = ROOT + 'www/index.html'
TEST = ROOT + 'tests/test20231.js'


def rep(path, old, new):
    with open(path, encoding='utf-8') as f:
        s = f.read()
    assert old in s, 'NO ENCONTRADO en %s: %r' % (path, old[:90])
    assert s.count(old) == 1, 'MÁS DE UNA OCURRENCIA en %s: %r' % (path, old[:90])
    with open(path, 'w', encoding='utf-8') as f:
        f.write(s.replace(old, new))
    print('OK:', path.split('/')[-1], '->', new[:70].replace('\n', ' '))


# --- www/index.html ---
rep(HTML,
    "// Checks del detector (2.3.1): el detector de escritorio reporta qué\n"
    "// software encontró (d.checks) y detalles (d.detalles, p. ej.\n"
    "// officeDetectado). Solo los ids de software de la plantilla actual\n"
    "// pueden nacer marcados; hardware, datos, Invgate y la limpieza nunca.",
    "// Checks del detector (2.3.1): el detector de escritorio reporta qué\n"
    "// software y hardware encontró (d.checks) y detalles (d.detalles, p. ej.\n"
    "// officeDetectado). Solo los ids detectables de la plantilla actual\n"
    "// pueden nacer marcados (t3/t4 de hardware y el software); datos,\n"
    "// Invgate y la limpieza nunca.")
rep(HTML,
    "var DETECTABLE_IDS = ['t6', 't7', 't8', 't9', 't10', 't11', 't18', 't19', 't20', 't21', 't22', 't23', 't24', 't25'];",
    "var DETECTABLE_IDS = ['t3', 't4', 't6', 't7', 't8', 't9', 't10', 't11', 't18', 't19', 't20', 't21', 't22', 't23', 't24', 't25'];")
rep(HTML,
    "var DET_SHORT = {\n"
    "  t6: 'SO actualizado', t7: 'Antivirus', t8: 'Office', t9: 'Impresoras',",
    "var DET_SHORT = {\n"
    "  t3: 'Batería y cargador', t4: 'Etiqueta y serie',\n"
    "  t6: 'SO actualizado', t7: 'Antivirus', t8: 'Office', t9: 'Impresoras',")

# --- tests/test20231.js ---
rep(TEST,
    "const detFull = { t6: true, t7: true, t8: 'Office 365', t9: true, t10: true, t11: true, t18: true, t19: true, t20: true, t21: true, t22: true, t23: true, t24: true, t25: true };",
    "const detFull = { t3: true, t4: true, t6: true, t7: true, t8: 'Office 365', t9: true, t10: true, t11: true, t18: true, t19: true, t20: true, t21: true, t22: true, t23: true, t24: true, t25: true };")
rep(TEST,
    "console.log('AO1) mapeo completo: 14 puntos:', fFull.ids.length === 14, '| Office 365:', fFull.checks.t8 === 'Office 365', '| nombres cortos en orden de plantilla:', detectedNames(fFull.checks, fFull.ids).join(', ') === 'SO actualizado, Antivirus, Office 365, Impresoras, VPN, Inicio rápido desactivado, Chrome, Adobe Reader, WinRAR, Lapi Fox, Alfaweb, Alfaprinter, Accesos directos, AnyDesk Gris');",
    "console.log('AO1) mapeo completo: 16 puntos:', fFull.ids.length === 16, '| Office 365:', fFull.checks.t8 === 'Office 365', '| t3/t4 de hardware:', fFull.checks.t3 === true && fFull.checks.t4 === true, '| nombres cortos en orden de plantilla:', detectedNames(fFull.checks, fFull.ids).join(', ') === 'Batería y cargador, Etiqueta y serie, SO actualizado, Antivirus, Office 365, Impresoras, VPN, Inicio rápido desactivado, Chrome, Adobe Reader, WinRAR, Lapi Fox, Alfaweb, Alfaprinter, Accesos directos, AnyDesk Gris');")
rep(TEST,
    "const fNever = filterDetectedChecks({ t1: true, t2: true, t3: true, t4: true, t12: true, t13: true, t15: true, t16: true, t17: true, t26: true, t99: true, foo: true, t18: true });",
    "const fNever = filterDetectedChecks({ t1: true, t2: true, t12: true, t13: true, t15: true, t16: true, t17: true, t26: true, t99: true, foo: true, t18: true });")
rep(TEST,
    "checks: { t18: true, t19: true, t20: true, t8: 'Office 365', t1: true, t12: true, t99: true }, detalles: { officeDetectado: true } }];",
    "checks: { t3: true, t4: true, t18: true, t19: true, t20: true, t8: 'Office 365', t1: true, t12: true, t99: true }, detalles: { officeDetectado: true } }];")
rep(TEST,
    "'| preparación nace con checks detectados:', !!savedDet && savedDet.checks.t18 === true && savedDet.checks.t19 === true && savedDet.checks.t20 === true && savedDet.checks.t8 === 'Office 365', '| sin t1 ni t12 ni t99:', !!savedDet && savedDet.checks.t1 === undefined && savedDet.checks.t12 === undefined && savedDet.checks.t99 === undefined, '| autoDetectado:', !!savedDet && savedDet.autoDetectado.join(',') === 't8,t18,t19,t20', '| sube a la nube con autoDetectado:', upDet.length === 1 && upDet[0].autoDetectado.join(',') === 't8,t18,t19,t20',",
    "'| preparación nace con checks detectados:', !!savedDet && savedDet.checks.t3 === true && savedDet.checks.t4 === true && savedDet.checks.t18 === true && savedDet.checks.t19 === true && savedDet.checks.t20 === true && savedDet.checks.t8 === 'Office 365', '| sin t1 ni t12 ni t99:', !!savedDet && savedDet.checks.t1 === undefined && savedDet.checks.t12 === undefined && savedDet.checks.t99 === undefined, '| autoDetectado:', !!savedDet && savedDet.autoDetectado.join(',') === 't3,t4,t8,t18,t19,t20', '| sube a la nube con autoDetectado:', upDet.length === 1 && upDet[0].autoDetectado.join(',') === 't3,t4,t8,t18,t19,t20',")

print('Parche 2.3.1b aplicado.')
