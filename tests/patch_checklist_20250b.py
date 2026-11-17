# Parche 2.5.0b: firestore.rules (mantenimientos + config/folios),
# versionado 2.5.0 / 54 en build.gradle, iOS y www/index.html (todos los 2.4.0).
import io, re

def rep(path, old, new, n=1):
    s = io.open(path, encoding='utf-8').read()
    c = s.count(old)
    assert c == n, '%s: NO ENCONTRADO o repetido (%d): %r' % (path, c, old[:90])
    io.open(path, 'w', encoding='utf-8').write(s.replace(old, new))

R = '/home/hatch/workspace/android/checklist-cloud/firestore.rules'
rep(R, """    // Clave de la IA (Gemini): la guarda el admin una vez y la leen los
    // usuarios activos para preguntarle a la IA desde sus teléfonos.
    match /config/ai {
      allow read: if isActive();
      allow create, update: if isAdmin();
      allow delete: if false;
    }""",
"""    // Clave de la IA (Gemini): la guarda el admin una vez y la leen los
    // usuarios activos para preguntarle a la IA desde sus teléfonos.
    match /config/ai {
      allow read: if isActive();
      allow create, update: if isAdmin();
      allow delete: if false;
    }

    // Mantenimientos preventivos (2.5.0): órdenes de servicio con folio.
    // Un usuario normal solo ve los suyos (tecnicoUid propio); el admin
    // ve todos. La lectura por id es pública para que la página de firma
    // (sin sesión) pueda mostrar la orden: el id del documento es el
    // secreto — cualquiera que lo conozca puede leer esa orden y firmarla.
    // Crear: usuario activo con su propio tecnicoUid. Actualizar: admin o
    // propio, o la firma pública que solo toca 'firma' y 'estado' (a
    // 'firmada', con nombre, área y firma no vacíos). Borrar: admin o propio.
    match /mantenimientos/{id} {
      allow list: if isActive() && (isAdmin() || resource.data.tecnicoUid == request.auth.uid);
      allow get: if true;
      allow create: if isActive() && request.resource.data.tecnicoUid == request.auth.uid;
      allow update: if (isActive() && (isAdmin() || resource.data.tecnicoUid == request.auth.uid))
        || (request.resource.data.diff(resource.data).changedKeys().hasOnly(['firma', 'estado'])
          && request.resource.data.estado == 'firmada'
          && request.resource.data.firma.nombre is string && request.resource.data.firma.nombre.size() > 0
          && request.resource.data.firma.area is string && request.resource.data.firma.area.size() > 0
          && request.resource.data.firma.firma is string && request.resource.data.firma.firma.size() > 0);
      allow delete: if isActive() && (isAdmin() || resource.data.tecnicoUid == request.auth.uid);
    }

    // Folios de órdenes de servicio (2.5.0): config/folios.siguiente es el
    // próximo folio a asignar (empieza en 1). Leer: usuarios activos.
    // Crear: usuario activo con siguiente entero. Actualizar: solo subir
    // el contador de uno en uno.
    match /config/folios {
      allow read: if isActive();
      allow create: if isActive() && request.resource.data.siguiente is int;
      allow update: if isActive()
        && request.resource.data.diff(resource.data).changedKeys().hasOnly(['siguiente'])
        && request.resource.data.siguiente == resource.data.siguiente + 1;
      allow delete: if false;
    }""")

# Android: versionCode 53 -> 54, versionName 2.4.0 -> 2.5.0.
G = '/home/hatch/workspace/android/checklist-cloud/android/app/build.gradle'
rep(G, '        versionCode 53\n        versionName "2.4.0"',
       '        versionCode 54\n        versionName "2.5.0"')

# iOS: MARKETING_VERSION 2.4.0 -> 2.5.0 (x2), CURRENT_PROJECT_VERSION 53 -> 54 (x2).
I = '/home/hatch/workspace/android/checklist-cloud/ios/App/App.xcodeproj/project.pbxproj'
s = io.open(I, encoding='utf-8').read()
assert s.count('MARKETING_VERSION = 2.4.0;') == 2, 'iOS MARKETING_VERSION'
assert s.count('CURRENT_PROJECT_VERSION = 53;') == 2, 'iOS CURRENT_PROJECT_VERSION'
s = s.replace('MARKETING_VERSION = 2.4.0;', 'MARKETING_VERSION = 2.5.0;')
s = s.replace('CURRENT_PROJECT_VERSION = 53;', 'CURRENT_PROJECT_VERSION = 54;')
io.open(I, 'w', encoding='utf-8').write(s)

# www/index.html: todos los 2.4.0 -> 2.5.0 (comentarios incluidos, como en la 2.4.0).
H = '/home/hatch/workspace/android/checklist-cloud/www/index.html'
s = io.open(H, encoding='utf-8').read()
n = s.count('2.4.0')
print('ocurrencias 2.4.0 en index.html:', n)
s = s.replace('2.4.0', '2.5.0')
assert '2.4.0' not in s, 'quedan 2.4.0'
io.open(H, 'w', encoding='utf-8').write(s)
print('reglas + versionado OK; ocurrencias 2.5.0:', s.count('2.5.0'))
