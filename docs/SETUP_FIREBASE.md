# Setup de Firebase — Checklist de Soporte (nube)

Guía para dejar funcionando el backend de la app 2.5.6. Todo lo descrito
aquí se verificó en `www/cloud/firebase.js`, `firestore.rules`,
`hosting/firebase.json` y `hosting/README.md`. Lo que no se pudo verificar
en el código se marca como **por confirmar**.

## 1. Crear el proyecto Firebase

1. En la [consola de Firebase](https://console.firebase.google.com),
   crear el proyecto **`checklist-soporte`** (es el proyecto default
   registrado en `hosting/.firebaserc`).
2. Plan **Spark** (gratuito). La app **no usa Cloud Functions**: todo el
   backend son Auth, Firestore y Hosting.
3. Registrar una app web (icono `</>`): Firebase entrega el objeto de
   configuración con `apiKey`, `authDomain`, `projectId`,
   `storageBucket`, `messagingSenderId` y `appId`. Esos son exactamente
   los 6 campos de `www/firebase-config.js` (ver
   `www/firebase-config.example.js`).

## 2. Authentication — Email/Contraseña

1. Consola → Authentication → Método de acceso → activar
   **Correo electrónico/Contraseña**.
2. No se necesita ningún otro proveedor. El login de la app es por
   **usuario y contraseña** (ver § 6): la app resuelve el nombre de
   usuario a su correo de acceso en la colección `usernames`
   (`resolveUsername` en `www/cloud/firebase.js`).
3. El correo de restablecimiento de contraseña («Olvidé mi contraseña»)
   lo envía Firebase Auth con `sendPasswordResetEmail`; el mensaje sale
   en español cuando la cuenta tiene un correo real guardado.

## 3. Firestore — base en modo producción

1. Consola → Firestore Database → Crear base de datos → **modo de
   producción** (las reglas de este repo son las que mandan, no las de
   prueba) y la región que corresponda.
2. La app usa caché offline persistente
   (`initializeFirestore` con `persistentLocalCache` en
   `www/cloud/firebase.js`), así que los teléfonos siguen trabajando sin
   conexión y sincronizan al volver.

## 4. Publicar `firestore.rules`

El archivo `firestore.rules` en la raíz del repo es la fuente de verdad
de la seguridad. Resumen de lo que permite (leer el archivo para el
detalle exacto):

- `users/{uid}`: lectura para usuarios activos; creación solo en
  bootstrap (primer admin) o por un admin; actualización y borrado solo
  admin.
- `usernames/{name}`: lectura pública (para entrar con usuario);
  escritura solo admin.
- `loginAttempts/{uid}`: lectura y escritura públicas (el login revisa
  el bloqueo sin sesión); solo el admin borra (desbloquea).
- `config/admin`: lectura pública; creación una sola vez por un usuario
  autenticado; nunca se actualiza ni se borra.
- `config/ai`: lectura para activos; escritura solo admin.
- `config/folios`: lectura para activos; el contador `siguiente` solo
  sube de uno en uno.
- `preparations`, `renta`, `detectados`: lectura/escritura para usuarios
  activos.
- `mantenimientos`: listar solo propios (o todo si admin); lectura por
  id pública (para `firma.html` sin sesión); crear con el propio
  `tecnicoUid`; actualizar el propio o el admin, o la firma pública que
  solo toca `firma` y `estado` → `'firmada'`; borrar el propio o el admin.
- `chat`, `dm`: lectura/escritura para activos (el DM solo entre sus dos
  participantes); borrado por admin, o por cualquier activo si el mensaje
  tiene más de 24 h.
- `presence`: cada usuario escribe solo su propio registro.

### Cómo publicarlas

Desde la consola: Firestore Database → Reglas → pegar el contenido de
`firestore.rules` → Publicar.

O con la CLI (requiere Firebase CLI con sesión en la cuenta del
proyecto):

```bash
firebase deploy --only firestore:rules
```

> Por confirmar: si existe un `firebase.json` en la raíz del repo para
> el deploy de reglas. Hoy el único `firebase.json` del repo está en
> `hosting/firebase.json` y solo configura Hosting; el deploy de reglas
> desde CLI con ese archivo no está verificado.

## 5. Hosting — `firma.html`

La página pública de firma vive en `hosting/public/`:

| Archivo | Qué es |
|---|---|
| `hosting/public/firma.html` | La página: lee `?id=`, carga el doc de `mantenimientos`, muestra folio/técnico/caso/falla/equipo/fecha y el formulario de firma. |
| `hosting/public/firebase-config.js` | Config del proyecto (copia de los valores de `www/firebase-config.js`). NO se versiona; hay un `firebase-config.example.js` con la forma. |
| `hosting/firebase.json` | Config de Hosting: `public: "public"`. |

URL en producción:

```
https://checklist-soporte.web.app/firma.html?id=<id del doc en mantenimientos>
```

El `id` del documento es el secreto: cualquiera que conozca el enlace
puede leer esa orden y firmarla (las reglas lo permiten a propósito).
No compartir el enlace fuera del usuario que debe firmar.

### Desplegar

```bash
cd hosting
firebase deploy --only hosting
# o, para probar antes sin afectar producción:
firebase hosting:channel:deploy preview-firma --only hosting
```

Requisitos: Firebase CLI instalado y con sesión en la cuenta del
proyecto (`firebase login`). Detalle y verificación en
`hosting/README.md`.

## 6. Crear el primer admin

El primer admin se crea **desde la propia app**, no desde la consola:

1. Con la app instalada y la config real puesta, abrir la app: si
   `config/admin` no existe o `initialized` no es `true`, la app ofrece
   crear el primer administrador.
2. La app crea el usuario en Auth (`bootstrapAdmin` en
   `www/cloud/firebase.js`), guarda su documento en `users/{uid}` con
   `{ email, nombre, rol: 'admin', activo: true, createdAt }` y marca
   `config/admin = { initialized: true }`.
3. A partir de ahí, solo un admin puede crear más usuarios (desde la
   pestaña Usuarios de la app).

Si un alta de admin quedó a medias (el usuario existe en Auth pero su
documento en `users` no se guardó), el código trae `repairAdmin`, que
lo deja como admin y marca inicializado.

> Si el documento `config/admin` ya existe con `initialized: true`, el
> bootstrap ya no se ofrece. Para rehacerlo habría que borrar ese
> documento a mano desde la consola — por confirmar el procedimiento
> exacto, no está documentado en el código.

## 7. Claves de IA — `config/ai`

Las claves **no van en el código ni en `firebase-config.js`**. El admin
las guarda desde la app (Usuarios → Inteligencia artificial) y viven en
Firestore:

| Campo en `config/ai` | Qué es | Función en `firebase.js` |
|---|---|---|
| `key` | Clave de Gemini (Google AI Studio, gratis) | `getAiKey` / `setAiKey` |
| `deepseekKey` | Clave de DeepSeek (respaldo, cobra por uso) | `getDeepseekKey` / `setDeepseekKey` |

Las reglas permiten leer `config/ai` a cualquier usuario activo y
escribirla solo al admin, y el documento nunca se borra por reglas
(`delete: if false`). Guardar una clave no borra la otra (cada setter
usa `setDoc` con `{ merge: true }`).

## 8. Notas de seguridad

- **La `apiKey` web es pública por diseño.** Va en el JavaScript de la
  app y en `hosting/public/firebase-config.js`. La seguridad real la dan
  las reglas de Firestore (`firestore.rules`) y que Auth exige sesión
  para casi todo. No intentar «esconder» la apiKey.
- **Lo que NUNCA se comparte ni se versiona:**
  - El **keystore de firma** de la APK (ver `docs/BUILD_APK.md`) y sus
    contraseñas (`keys/checklist-keystore.properties`, fuera del repo).
  - Las **contraseñas** de los usuarios.
  - Las **claves de IA** (Gemini / DeepSeek): viven en `config/ai`, no
    en archivos.
  - El archivo real `firebase-config.js` (está en el `.gitignore`).
- **El enlace de firma es un secreto por enlace:** quien tenga el
  `firma.html?id=...` puede leer esa orden y firmarla. Mandarlo solo
  por WhatsApp al usuario que debe firmar.
- **Fotos de daños:** las fotos enviadas a revisión de daños con IA se
  mandan a Google. No fotografiar datos sensibles.
- Las fotos (serie, daños, firmas en canvas) viajan en base64 dentro
  del documento de Firestore y **se recortan si pasan de ~700 KB**
  (`MAX_FOTO_CLOUD = 700000`): un documento de Firestore no puede
  pasar de 1 MB.
