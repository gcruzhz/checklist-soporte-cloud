#!/usr/bin/env python3
"""Parche 2.2.6b: la foto solo abría la galería.
Causa: los botones usan un <input type="file" capture="environment"> y el
WebView de Capacitor ignora el atributo capture: solo abre el selector de
archivos, sin opción de cámara. Solución: plugin @capacitor/camera con
source 'PROMPT' (menú nativo Tomar foto / Elegir de la galería). El selector
de archivos queda como respaldo si el plugin no está. El plugin ya está
instalado (@capacitor/camera 8.x) y su dist/plugin.js copiado a
www/cap-plugins/camera-plugin.js. OJO: los valores del enum son MAYÚSCULAS
('PROMPT') y resultType es 'dataUrl' (verificado en el plugin instalado)."""
P = '/home/hatch/workspace/android/checklist-cloud/www/index.html'
s = open(P).read()
orig = s

def rep(old, new, n=1):
    global s
    assert old in s, 'NO ENCONTRADO: ' + old[:90]
    s = s.replace(old, new, n)

# ---------- 1. Versión visible ----------
rep('Versión 2.2.5', 'Versión 2.2.6')
rep('Versión: 2.2.5', 'Versión: 2.2.6')
rep('Checklist de Soporte 2.2.5', 'Checklist de Soporte 2.2.6')
rep('Versión de la app: 2.2.5', 'Versión de la app: 2.2.6')

# ---------- 2. Script del plugin de cámara ----------
rep('<script src="cap-plugins/native-biometric-plugin.js"></script>',
    '<script src="cap-plugins/native-biometric-plugin.js"></script>\n<script src="cap-plugins/camera-plugin.js"></script>')

# ---------- 3. Quitar capture="environment" (el WebView lo ignora) ----------
rep('<input type="file" id="fFotoSerie" accept="image/*" capture="environment" hidden>',
    '<input type="file" id="fFotoSerie" accept="image/*" hidden>')
rep('<input type="file" id="fFotoDanos" accept="image/*" capture="environment" hidden>',
    '<input type="file" id="fFotoDanos" accept="image/*" hidden>')

# ---------- 4. Foto de serie con menú nativo ----------
old_serie = """// Foto del numero de serie: camara o galeria, reducida a max 1024 px para no llenar el telefono.
window._fotoSerie = null;
document.getElementById('btnFotoSerie').addEventListener('click', function () {
  document.getElementById('fFotoSerie').click();
});
document.getElementById('fFotoSerie').addEventListener('change', function (e) {
  var file = e.target.files && e.target.files[0];
  if (!file) return;
  var reader = new FileReader();
  reader.onload = function (ev) {
    var img = new Image();
    img.onload = function () {
      var max = 1024, w = img.width, h = img.height;
      if (w > max || h > max) {
        var k = Math.min(max / w, max / h);
        w = Math.round(w * k); h = Math.round(h * k);
      }
      var cv = document.createElement('canvas');
      cv.width = w; cv.height = h;
      cv.getContext('2d').drawImage(img, 0, 0, w, h);
      window._fotoSerie = cv.toDataURL('image/jpeg', 0.82);
      document.getElementById('fotoSeriePreview').innerHTML =
        '<img src="' + window._fotoSerie + '" alt="Foto del número de serie">' +
        '<button type="button" class="btn-ghost" id="btnQuitarFoto" style="margin-top:6px">Quitar foto</button>';
      document.getElementById('btnQuitarFoto').addEventListener('click', function () {
        window._fotoSerie = null;
        document.getElementById('fotoSeriePreview').innerHTML = '';
        document.getElementById('fFotoSerie').value = '';
      });
    };
    img.src = ev.target.result;
  };
  reader.readAsDataURL(file);
});"""
new_serie = """// Foto del numero de serie: camara o galeria, reducida a max 1024 px para no llenar el telefono.
window._fotoSerie = null;
// Reduce una foto (data URL) a max px y JPEG con la calidad dada.
function reducePhoto(dataUrl, max, quality, done) {
  var img = new Image();
  img.onload = function () {
    var w = img.width, h = img.height;
    if (w > max || h > max) {
      var k = Math.min(max / w, max / h);
      w = Math.round(w * k); h = Math.round(h * k);
    }
    var cv = document.createElement('canvas');
    cv.width = w; cv.height = h;
    cv.getContext('2d').drawImage(img, 0, 0, w, h);
    done(cv.toDataURL('image/jpeg', quality));
  };
  img.src = dataUrl;
}
function setFotoSerie(dataUrl) {
  window._fotoSerie = dataUrl;
  document.getElementById('fotoSeriePreview').innerHTML =
    '<img src="' + window._fotoSerie + '" alt="Foto del número de serie">' +
    '<button type="button" class="btn-ghost" id="btnQuitarFoto" style="margin-top:6px">Quitar foto</button>';
  document.getElementById('btnQuitarFoto').addEventListener('click', function () {
    window._fotoSerie = null;
    document.getElementById('fotoSeriePreview').innerHTML = '';
    document.getElementById('fFotoSerie').value = '';
  });
}
// Abre el menú nativo (Tomar foto / Elegir de la galería); si el plugin de
// cámara no está, usa el selector de archivos del sistema.
function pickPhoto(max, quality, onDone) {
  var Cam = window.Capacitor && window.Capacitor.Plugins && window.Capacitor.Plugins.Camera;
  if (Cam && Cam.getPhoto) {
    Cam.getPhoto({ quality: 90, allowEditing: false, resultType: 'dataUrl', source: 'PROMPT' }).then(function (photo) {
      if (photo && photo.dataUrl) reducePhoto(photo.dataUrl, max, quality, onDone);
    }).catch(function () { /* el usuario canceló: no se hace nada */ });
    return true;
  }
  return false;
}
document.getElementById('btnFotoSerie').addEventListener('click', function () {
  if (!pickPhoto(1024, 0.82, setFotoSerie)) document.getElementById('fFotoSerie').click();
});
document.getElementById('fFotoSerie').addEventListener('change', function (e) {
  var file = e.target.files && e.target.files[0];
  if (!file) return;
  var reader = new FileReader();
  reader.onload = function (ev) { reducePhoto(ev.target.result, 1024, 0.82, setFotoSerie); };
  reader.readAsDataURL(file);
});"""
rep(old_serie, new_serie)

# ---------- 5. Foto de daños con menú nativo ----------
old_danos = """// Foto de daños de renta: camara o galeria, reducida a max 800 px.
window._fotoDanos = null;
document.getElementById('btnFotoDanos').addEventListener('click', function () {
  document.getElementById('fFotoDanos').click();
});
document.getElementById('fFotoDanos').addEventListener('change', function (e) {
  var file = e.target.files && e.target.files[0];
  if (!file) return;
  var reader = new FileReader();
  reader.onload = function (ev) {
    var img = new Image();
    img.onload = function () {
      var max = 800, w = img.width, h = img.height;
      if (w > max || h > max) {
        var k = Math.min(max / w, max / h);
        w = Math.round(w * k); h = Math.round(h * k);
      }
      var cv = document.createElement('canvas');
      cv.width = w; cv.height = h;
      cv.getContext('2d').drawImage(img, 0, 0, w, h);
      window._fotoDanos = cv.toDataURL('image/jpeg', 0.75);
      document.getElementById('fotoDanosPreview').innerHTML =
        '<img src="' + window._fotoDanos + '" alt="Foto de daños">' +
        '<button type="button" class="btn-ghost" id="btnQuitarFotoDanos" style="margin-top:6px">Quitar foto</button>';
      document.getElementById('btnQuitarFotoDanos').addEventListener('click', function () {
        window._fotoDanos = null;
        document.getElementById('fotoDanosPreview').innerHTML = '';
        document.getElementById('fFotoDanos').value = '';
      });
    };
    img.src = ev.target.result;
  };
  reader.readAsDataURL(file);
});"""
new_danos = """// Foto de daños de renta: camara o galeria, reducida a max 800 px.
window._fotoDanos = null;
function setFotoDanos(dataUrl) {
  window._fotoDanos = dataUrl;
  document.getElementById('fotoDanosPreview').innerHTML =
    '<img src="' + window._fotoDanos + '" alt="Foto de daños">' +
    '<button type="button" class="btn-ghost" id="btnQuitarFotoDanos" style="margin-top:6px">Quitar foto</button>';
  document.getElementById('btnQuitarFotoDanos').addEventListener('click', function () {
    window._fotoDanos = null;
    document.getElementById('fotoDanosPreview').innerHTML = '';
    document.getElementById('fFotoDanos').value = '';
  });
}
document.getElementById('btnFotoDanos').addEventListener('click', function () {
  if (!pickPhoto(800, 0.75, setFotoDanos)) document.getElementById('fFotoDanos').click();
});
document.getElementById('fFotoDanos').addEventListener('change', function (e) {
  var file = e.target.files && e.target.files[0];
  if (!file) return;
  var reader = new FileReader();
  reader.onload = function (ev) { reducePhoto(ev.target.result, 800, 0.75, setFotoDanos); };
  reader.readAsDataURL(file);
});"""
rep(old_danos, new_danos)

assert s != orig
open(P, 'w').write(s)
print('OK parche 2.2.6b (index.html) aplicado')
print('Quedan "2.2.5":', len(__import__('re').findall(r'2\.2\.5', s)))
print('Quedan capture=environment:', s.count('capture="environment"'))
print('pickPhoto:', s.count('pickPhoto'), '| PROMPT:', s.count("'PROMPT'"), '| camera-plugin.js:', s.count('camera-plugin.js'))
