#!/usr/bin/env python3
"""Parche 2.3.0 (Parte B): equipos detectados en Por preparar.
- firebase.js: reportDetected / subscribeDetectados / deleteDetectado /
  markDetectadoUsado (colección `detectados`).
- index.html: botón 'Detectar este equipo' (solo con window.Desktop),
  panel 'Equipos detectados' con Usar/Descartar, suscripción solo con
  sesión; versión visible 2.3.0.
- firestore.rules: match /detectados/{id} (solo local, NO publicar).
- android/app/build.gradle: versionCode 43, versionName 2.3.0.
Cada reemplazo con assert: si el texto viejo no está, se para.
"""
import re

def rep(s, old, new, n=1):
    assert old in s, 'NO ENCONTRADO: ' + old[:90]
    return s.replace(old, new, n)

# ---------- 1. firebase.js ----------
P = '/home/hatch/workspace/android/checklist-cloud/www/cloud/firebase.js'
s = open(P).read()
orig = s

s = rep(s, """async function getAllPreparations() {
  const snap = await getDocs(collection(db, 'preparations'));
  return snap.docs.map((d) => Object.assign({ id: d.id }, d.data()));
}""",
"""async function getAllPreparations() {
  const snap = await getDocs(collection(db, 'preparations'));
  return snap.docs.map((d) => Object.assign({ id: d.id }, d.data()));
}

// Equipos detectados (2.3.0): el detector de escritorio reporta los equipos
// que ve en la red (colección detectados) y los teléfonos los listan para
// usarlos en un equipo nuevo o descartarlos. El id es la serie si existe,
// si no hostname + '-' + detectadoEn.
async function reportDetected(info) {
  const d = Object.assign({}, info || {});
  if (!d.id) d.id = d.serie ? String(d.serie) : (d.hostname || '') + '-' + (d.detectadoEn || Date.now());
  if (!d.detectadoEn) d.detectadoEn = Date.now();
  if (d.usado === undefined) d.usado = false;
  return setDoc(doc(db, 'detectados', String(d.id)), d, { merge: true });
}
function subscribeDetectados(cb) {
  return onSnapshot(
    query(collection(db, 'detectados'), orderBy('detectadoEn', 'desc'), limit(50)),
    (snap) => cb(snap.docs.map((d) => Object.assign({ id: d.id }, d.data()))),
    (err) => console.warn('[Cloud] Error en snapshot de detectados:', err)
  );
}
async function deleteDetectado(id) {
  return deleteDoc(doc(db, 'detectados', id));
}
async function markDetectadoUsado(id) {
  return updateDoc(doc(db, 'detectados', id), { usado: true });
}""")

s = rep(s, """  subscribePreparations,
  upsertPrep,
  deletePrep,
  getAllPreparations,""",
"""  subscribePreparations,
  upsertPrep,
  deletePrep,
  getAllPreparations,
  reportDetected,
  subscribeDetectados,
  deleteDetectado,
  markDetectadoUsado,""")

assert s != orig
open(P, 'w').write(s)
print('OK firebase.js')

# ---------- 2. index.html ----------
P = '/home/hatch/workspace/android/checklist-cloud/www/index.html'
s = open(P).read()
orig = s

# 2.0 Versión visible 2.3.0 (4 lugares)
s = rep(s, 'Versión 2.2.7', 'Versión 2.3.0')
s = rep(s, 'Versión: 2.2.7', 'Versión: 2.3.0')
s = rep(s, 'Checklist de Soporte 2.2.7', 'Checklist de Soporte 2.3.0')
s = rep(s, 'Versión de la app: 2.2.7', 'Versión de la app: 2.3.0')
assert '2.2.7' not in s, 'queda 2.2.7 en index.html'

# 2.1 Botones en el menú de Por preparar (Detectar oculto por defecto)
s = rep(s, """    <button class="menu-btn dark wide" id="btnShowRe"><span class="ic">&#128260;</span><span>Reasignar Equipo<small>equipo no nuevo</small></span></button>""",
"""    <button class="menu-btn dark wide" id="btnShowRe"><span class="ic">&#128260;</span><span>Reasignar Equipo<small>equipo no nuevo</small></span></button>
    <button class="menu-btn dark" id="btnDetectar" hidden><span class="ic">&#128187;</span><span>Detectar este equipo<small>solo en escritorio</small></span></button>
    <button class="menu-btn dark" id="btnShowDet"><span class="ic">&#128187;</span><span>Equipos detectados<small>equipos en la red</small></span></button>""")

# 2.2 Panel de equipos detectados (antes de la barra de compartir)
s = rep(s, """  <div class="card share-bar" id="shareBar">""",
"""  <div class="panel" id="detBox" hidden>
    <b>&#128187; Equipos detectados</b>
    <div class="share-note">Equipos que el detector vio en la red. Toca «Usar este equipo» para llenar el formulario de Nuevo equipo con sus datos.</div>
    <div id="detList"></div>
  </div>

  <div class="card share-bar" id="shareBar">""")

# 2.3 El panel nuevo también cierra los demás
s = rep(s, "['newBox', 'tplBox', 'reBox'].forEach(function (p) { if (p !== id) document.getElementById(p).hidden = true; });",
           "['newBox', 'tplBox', 'reBox', 'detBox'].forEach(function (p) { if (p !== id) document.getElementById(p).hidden = true; });")

# 2.4 Estado: suscripción y lista de detectados
s = rep(s, "var cloudPrepUnsub = null;",
           "var cloudPrepUnsub = null;\nvar cloudDetectadosUnsub = null;\nvar detectados = [];")

# 2.5 Helpers de nube + render de detectados (tras cloudDeletePrep)
s = rep(s, """function cloudDeletePrep(id) {
  if (!CLOUD_ENABLED || !cloudUser || !window.Cloud) return;
  window.Cloud.deletePrep(id).catch(function (e) { console.warn('No se pudo borrar el equipo en la nube', e); });
}""",
"""function cloudDeletePrep(id) {
  if (!CLOUD_ENABLED || !cloudUser || !window.Cloud) return;
  window.Cloud.deletePrep(id).catch(function (e) { console.warn('No se pudo borrar el equipo en la nube', e); });
}
function cloudMarkDetectadoUsado(id) {
  if (!CLOUD_ENABLED || !cloudUser || !window.Cloud || !window.Cloud.markDetectadoUsado) return;
  window.Cloud.markDetectadoUsado(id).catch(function (e) { console.warn('No se pudo marcar el equipo detectado como usado', e); });
}
function cloudDeleteDetectado(id) {
  if (!CLOUD_ENABLED || !cloudUser || !window.Cloud || !window.Cloud.deleteDetectado) return;
  window.Cloud.deleteDetectado(id).catch(function (e) { console.warn('No se pudo descartar el equipo detectado', e); });
}
// Equipos detectados (2.3.0): solo se listan los NO usados, con sus datos
// y dos acciones: usarlo (llena Nuevo equipo) o descartarlo.
function renderDetectados() {
  var box = document.getElementById('detList');
  if (!box) return;
  var list = detectados.filter(function (d) { return !d.usado; });
  if (!list.length) { box.innerHTML = '<div class="empty">No hay equipos detectados pendientes.</div>'; return; }
  box.innerHTML = list.map(function (d) {
    return '<div class="card"><h2>' + esc(d.hostname || 'Equipo') + '</h2>' +
      '<div class="sub">' + esc((d.marca || '') + ' ' + (d.modelo || '')) + ' · Serie: ' + esc(d.serie || '—') + '</div>' +
      '<div class="sub">CPU: ' + esc(d.cpu || '—') + ' · RAM: ' + (d.ramGB != null ? esc(d.ramGB) + ' GB' : '—') + ' · Disco: ' + (d.discoGB != null ? esc(d.discoGB) + ' GB' : '—') + ' · SO: ' + esc(d.so || '—') + '</div>' +
      '<div class="sub">Detectado ' + timeAgo(d.detectadoEn) + (d.detectadoPor ? ' por ' + esc(d.detectadoPor) : '') + '</div>' +
      '<div class="actions"><button class="btn-green" data-det-use="' + esc(d.id) + '">Usar este equipo</button>' +
      '<button class="btn-ghost" data-det-del="' + esc(d.id) + '">Descartar</button></div></div>';
  }).join('');
}""")

# 2.6 Al cerrar sesión (onAuthChanged sin usuario) se cancela la suscripción
s = rep(s, """    if (cloudUnsub) { cloudUnsub(); cloudUnsub = null; }
    if (cloudPrepUnsub) { cloudPrepUnsub(); cloudPrepUnsub = null; }""",
"""    if (cloudUnsub) { cloudUnsub(); cloudUnsub = null; }
    if (cloudPrepUnsub) { cloudPrepUnsub(); cloudPrepUnsub = null; }
    if (cloudDetectadosUnsub) { cloudDetectadosUnsub(); cloudDetectadosUnsub = null; }""")

# 2.7 Al entrar se suscribe a detectados (junto a renta y preparaciones)
s = rep(s, """    if (cloudPrepUnsub) cloudPrepUnsub();
    cloudPrepUnsub = window.Cloud.subscribePreparations(function (docs) {
      state.preparations = mergePrepsWithLocal(docs);
      save(); render();
    });""",
"""    if (cloudPrepUnsub) cloudPrepUnsub();
    cloudPrepUnsub = window.Cloud.subscribePreparations(function (docs) {
      state.preparations = mergePrepsWithLocal(docs);
      save(); render();
    });
    if (window.Cloud.subscribeDetectados) {
      if (cloudDetectadosUnsub) cloudDetectadosUnsub();
      cloudDetectadosUnsub = window.Cloud.subscribeDetectados(function (docs) {
        detectados = docs || [];
        renderDetectados();
      });
    }""")

# 2.8 En render(): el botón Detectar solo existe si hay window.Desktop
s = rep(s, """  document.getElementById('shareBar').hidden = filterStatus !== 'entregado';""",
"""  document.getElementById('shareBar').hidden = filterStatus !== 'entregado';
  var btnDet = document.getElementById('btnDetectar');
  if (btnDet) btnDet.hidden = !window.Desktop;""")

# 2.9 Botones Detectar / Equipos detectados y acciones de la lista
s = rep(s, """document.getElementById('btnShowRe').addEventListener('click', function () { fillReEquipo(); togglePanel('reBox'); });""",
"""document.getElementById('btnShowRe').addEventListener('click', function () { fillReEquipo(); togglePanel('reBox'); });
document.getElementById('btnShowDet').addEventListener('click', function () { renderDetectados(); togglePanel('detBox'); });
document.getElementById('btnDetectar').addEventListener('click', function () {
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
});
document.getElementById('detList').addEventListener('click', function (e) {
  var t = e.target;
  var use = t.closest('[data-det-use]');
  var del = t.closest('[data-det-del]');
  if (!use && !del) return;
  var id = (use || del).getAttribute(use ? 'data-det-use' : 'data-det-del');
  if (use) {
    var d = detectados.find(function (x) { return String(x.id) === String(id); });
    if (!d) return;
    document.getElementById('fTipo').value = d.tipo || 'Desktop';
    document.getElementById('fMarca').value = d.marca || '';
    document.getElementById('fModelo').value = d.modelo || '';
    document.getElementById('fSerie').value = d.serie || '';
    document.getElementById('fHostname').value = d.hostname || '';
    cloudMarkDetectadoUsado(d.id);
    document.getElementById('detBox').hidden = true;
    document.getElementById('newBox').hidden = false;
    updateSaveBtn();
    return;
  }
  if (del) {
    if (!confirm('¿Descartar este equipo detectado?')) return;
    cloudDeleteDetectado(id);
  }
});""")

# 2.10 Cerrar sesión con el botón también cancela la suscripción
s = rep(s, """  stopEquipo();
  if (cloudUnsub) { cloudUnsub(); cloudUnsub = null; }""",
"""  stopEquipo();
  if (cloudUnsub) { cloudUnsub(); cloudUnsub = null; }
  if (cloudDetectadosUnsub) { cloudDetectadosUnsub(); cloudDetectadosUnsub = null; }""")

assert s != orig
open(P, 'w').write(s)
print('OK index.html')

# ---------- 3. firestore.rules (solo local) ----------
P = '/home/hatch/workspace/android/checklist-cloud/firestore.rules'
s = open(P).read()
orig = s
s = rep(s, """    match /preparations/{id} {
      allow read, write: if isActive();
    }""",
"""    match /preparations/{id} {
      allow read, write: if isActive();
    }

    // Equipos detectados: el detector de escritorio los reporta y los
    // teléfonos los leen para usarlos o descartarlos.
    match /detectados/{id} {
      allow read, write: if isActive();
    }""")
assert s != orig
open(P, 'w').write(s)
print('OK firestore.rules')

# ---------- 4. android/app/build.gradle ----------
P = '/home/hatch/workspace/android/checklist-cloud/android/app/build.gradle'
s = open(P).read()
orig = s
s = rep(s, '        versionCode 42', '        versionCode 43')
s = rep(s, '        versionName "2.2.7"', '        versionName "2.3.0"')
assert s != orig
open(P, 'w').write(s)
print('OK build.gradle')
print('Parche 2.3.0 aplicado')
