# Checklist de Soporte — app en la nube (2.5.6)

App para preparar equipos de cómputo antes de asignarlos a un usuario,
recibir y entregar equipos de renta, y levantar órdenes de mantenimiento
preventivo con firma del usuario. Los datos se sincronizan entre todos los
teléfonos del equipo mediante Firebase (Firestore), con caché offline.

- **Versión actual:** 2.5.6 (`versionCode` 60, `versionName` "2.5.6" en
  `android/app/build.gradle`; iOS `MARKETING_VERSION` 2.5.6 /
  `CURRENT_PROJECT_VERSION` 60).
- **Repositorio público:** https://github.com/gcruzhz/checklist-soporte-cloud
- **Autor:** Gerardo Cruz Hernandez (gerardo.cruzhz@linux.com)
- **App Android:** `mx.gerardo.checklistsoporte` (Capacitor).
- **Firebase:** proyecto `checklist-soporte` — Auth, Firestore y Hosting
  (plan Spark, sin Cloud Functions). Hosting público:
  https://checklist-soporte.web.app/firma.html

> La línea local `checklist-app/` (1.x) es legado y está archivada: se
> menciona aquí solo como referencia histórica, no se documenta en detalle.
> Todo lo de este README describe la app en la nube (2.x).

> **Últimos cambios (2.5.9):** en «Equipos detectados» (Por preparar y
> Mantenimientos) cada equipo trae «📲 Compartir por WhatsApp» y «✉️
> Compartir por correo» con todas sus características detectadas
> (hardware, redes, AnyDesk, versiones, políticas, impresora); compartir
> no lo marca como usado. Historial completo
> en [docs/CHANGELOG.md](docs/CHANGELOG.md).

## Qué hace

Al abrir la app se elige la sección (selector de Inicio):

| Sección | Qué hace |
|---|---|
| **Por preparar** | Checklist de preparación de equipos nuevos o reasignados, sincronizado entre teléfonos. |
| **Recibir renta** | Recepción de equipos de renta: inventario, daños y accesorios. |
| **Entrega Renta** | Entrega de equipos de renta recibidos, con Excel y envío por WhatsApp/correo. |
| **Mantenimientos Preventivos** | Órdenes de servicio con folio automático y firma del usuario por enlace. |
| **Equipo / chat** | Presencia (quién está en línea) y chat grupal e individual efímero (24 h). |
| **Usuarios** (admin) | Alta, edición, activación/desactivación, borrado y desbloqueo de usuarios; claves de IA. |

### Por preparar

- Checklist de **23 puntos** para equipo nuevo (24 contando el punto
  «Limpieza física del equipo», que solo aparece en equipos reasignados),
  en tres grupos: Equipo y hardware, Software, y Datos del usuario.
  Puntos opcionales (VPN, Sistema Lapi Fox, Alfaprinter) no cuentan para
  el avance. «Office instalado y activado» ofrece Office 365 o LibreOffice.
- Cada punto se puede marcar **N/A** o quitarse si no aplica; los puntos
  que el técnico agrega se conservan cuando la plantilla se actualiza.
- Estados: **En preparación** → **Listo para entregar** (al 100 %) →
  **Entregado**. Mientras no llega al 100 % se muestra «Equipo con
  pendientes». Hay opción **«No listo»** y se puede reabrir un equipo
  entregado para completarlo al 100 %.
- **Borradores:** un equipo detectado o en curso se puede guardar para
  después («Guardar para después») y el botón «Guardar avance» guarda el
  progreso mientras se revisa el checklist.
- **Detección de equipo:** el programa de escritorio (repo aparte,
  `checklist-desktop`) reporta las características reales del equipo a
  Firestore (colección `detectados`); en la app aparece el panel
  «Equipos detectados» y el botón «Detectar este equipo» / «Usar este
  equipo» llena el formulario. Los dos puntos físicos (el equipo enciende
  sin daños; teclado, pantalla y puertos funcionan) nunca los marca el
  detector: se marcan a mano.
- **Reasignación / asignación:** botón «Reasignar» por tarjeta y botón
  grande «Reasignar Equipo» arriba. Se registra quién era el usuario
  anterior («Era de») y a quién se reasigna («Se reasigna a»); el historial
  queda en la tarjeta, el PDF, el WhatsApp y una columna del Excel. También
  se puede solicitar hacerse cargo de un equipo de otro analista.
- **Regla de 15 días en Entregados:** un equipo entregado se ve en
  Todos/Entregados durante 15 días (`DELIVERED_VISIBLE_DAYS = 15` en
  `www/index.html`); después solo lo ve el admin. El equipo entregado más
  reciente aparece arriba (orden por `deliveredAt` descendente).
- Cada analista ve primero sus propios equipos; los de otros analistas se
  ven en solo lectura pero se pueden compartir por WhatsApp o correo.
  El admin ve a todos con permisos completos.
- Exporta a Excel y PDF por equipo; compartir por WhatsApp o correo es una
  foto del momento del envío (si luego el equipo llega al 100 %, un mensaje
  ya enviado puede seguir mostrando puntos pendientes).

### Recibir renta / Entrega Renta

- Cada equipo de renta lleva: tipo (Laptop, iPad o PC), modelo, número de
  inventario, capacidad (iPad), CPU (PC), accesorios, daños y observaciones.
- Accesorios por tipo (verificados en `www/index.html`,
  `ACCS_POR_TIPO`):
  - **Laptop:** mouse, cargador, maletín.
  - **iPad:** cargador, cable (sin campo de versión).
  - **PC:** cable de corriente, mouse, teclado, cable de video, tarjeta
    de video adicional.
- En Recibir renta se revisan daños (con o sin daños, descripción y foto)
  y se puede pedir a la IA que revise los daños de la foto.
- El equipo recibido en Recibir renta aparece en Entrega Renta, agrupado
  por tipo, con su checklist de entrega.
- **Excel agrupado por tipo:** una tabla por tipo (Laptop, CPU, iPad) con
  columnas # Inventario y el nombre del tipo; las filas listan modelo más
  accesorios (p. ej. laptop: «INSPIRON 3501, MOUSE, CARGADOR, MALETA»;
  iPad: «IPAD 2 AIR WIFI 16 GB»). Incluye columna **Analista** con quien
  recibió el equipo y quien lo entregó.
- **Selección en Entrega Renta:** se marca uno a uno (checkbox por
  equipo) o todos/ninguno; WhatsApp, correo y Excel actúan sobre los
  marcados; sin selección, sobre todos los entregados visibles.
- **Regla de 15 días:** igual que en Por preparar, un equipo de renta
  entregado lo ve el usuario normal 15 días; después solo el admin.

### Mantenimientos Preventivos

- La orden de servicio se crea con **folio automático desde 00001**
  (transacción en Firestore, `config/folios.siguiente`, 5 dígitos; el
  folio nunca se reutiliza) o se guarda como **borrador sin folio**.
- Empresa: **Lapi, Ludi o Lapi Hemodiálisis** (el bloque de contacto solo
  aparece para Lapi). Tipo hardware y software marcados por defecto.
- Serie, hostname y modelo son obligatorios y se marcan en rojo si están
  vacíos; el técnico se llena solo con el login. El detector de escritorio
  aporta políticas de Windows, usuario «sistemas», impresora, versiones y
  datos de hardware.
- **Firma del técnico** en canvas dentro de la app.
- **Firma del usuario por enlace de WhatsApp** a `firma.html` (Hosting):
  el usuario escribe nombre, área, comentarios y satisfacción 0–10 y
  firma, sin app ni cuenta. Si ya firmó, la página muestra «Ya firmaste
  esta orden» y no deja firmar dos veces.
- **PDF formato F0.S1.01 Rev0, tamaño carta (612×792) en 1 página**,
  generado solo cuando están las dos firmas; el bloque de conformidad del
  usuario va al final, a la derecha. La preparación de equipos sigue en
  formato A4.
- **Botón Actualizar:** vuelve a leer la orden desde la nube (por ejemplo,
  para traer la firma del usuario recién hecha) sin salir de la pantalla.
- **Bloqueo de Mantenimientos por usuario:** el admin puede bloquear o
  desbloquear Mantenimientos a un usuario normal (campo
  `users/{uid}.mantBloqueado`); el usuario bloqueado sale a Inicio. El
  admin nunca se bloquea a sí mismo ni a otro admin. El bloqueo se aplica
  en vivo, sin cerrar sesión.
- Cada técnico ve solo sus órdenes (`tecnicoUid` propio); el admin ve
  todas y puede borrar órdenes.

### Equipo / chat

- **Presencia:** latido cada 2 minutos mientras la app está abierta;
  se ve quién está en línea.
- **Chat grupal** (colección `chat`) y **chat individual 1 a 1**
  (colección `dm`), ambos **efímeros: los mensajes de más de 24 horas se
  borran** (la app los limpia sola). Máximo 500 caracteres por mensaje.
- **Moderación admin:** el admin puede borrar cualquier mensaje del chat
  grupal o individual.

### Inteligencia artificial

- **Gemini** (Google AI Studio, gratis) como motor principal y
  **DeepSeek** como respaldo automático si Gemini falla. Las claves las
  guarda el admin en Usuarios → Inteligencia artificial y viven en
  Firestore (`config/ai`: campos `key` y `deepseekKey`). Modelos usados
  (ver `www/index.html`): Gemini `gemini-3.8-flash` (con
  `gemini-3.5-flash-lite` y `gemini-flash-latest` como reintentos),
  DeepSeek `deepseek-flash` con visión.
- **«¿Qué falta?»**: en cada equipo en preparación o listo, dice qué
  puntos obligatorios y opcionales faltan y en qué orden conviene hacerlos.
- **«Revisar daños con IA»**: en Recibir renta, fotografía el equipo y la
  IA describe los daños visibles; el resultado se guarda en el equipo y se
  ve en todos los teléfonos.
- **«Resumen con IA»**: en equipos entregados, la IA redacta el mensaje
  de WhatsApp.
- Las fotos enviadas a revisión de daños se mandan a Google: no
  fotografiar datos sensibles.

### Roles, login y seguridad

- **Roles:** `admin` y `usuario` (campo `rol` en `users/{uid}`).
  El admin crea, edita, activa/desactiva y borra usuarios, cambia
  contraseñas, desbloquea cuentas y guarda las claves de IA. El admin no
  puede borrar su propia cuenta.
- **Login por usuario y contraseña** (no por correo): el nombre de usuario
  se resuelve a su correo de acceso en la colección `usernames`.
  El correo real es opcional al crear usuarios y sirve como contacto y
  para recuperar la contraseña.
- **Recordar sesión** (checkbox en el login): con él, la sesión sobrevive
  al cerrar la app; sin él, termina al cerrar.
- **Huella en el teléfono:** tras el primer login con contraseña se
  ofrece entrar con huella/rostro (biométricos del teléfono, plugin
  `@capgo/capacitor-native-biometric`); se activa y se quita desde el
  botón Contraseña de la cuenta. En escritorio no hay sesión recordada
  ni huella: el `.exe` pide login cada vez que se abre.
- **Bloqueo tras 10 intentos fallidos** (`MAX_LOGIN_ATTEMPTS = 10` en
  `www/cloud/firebase.js`, colección `loginAttempts`): solo para usuarios
  normales, nunca para el admin; el admin desbloquea desde Usuarios.
- **«Olvidé mi contraseña»:** envía un correo de restablecimiento en
  español cuando la cuenta tiene un correo real. El usuario puede cambiar
  su propia contraseña (pide la actual); el admin puede cambiar la de un
  usuario (la cuenta se recrea con la contraseña nueva).
- Sin config real de Firebase la app arranca en **modo local** (como la
  1.8): sin login obligatorio y sin sincronización. Con config real, el
  login es obligatorio.

## Stack

| Capa | Tecnología (verificada en `package.json` / código) |
|---|---|
| App | Vanilla JS en un solo archivo, `www/index.html` (324 170 B) |
| Contenedor móvil | Capacitor 8.6.0 (`@capacitor/core`, `android`, `ios`, `cli`) |
| Nube | Firebase 11.10.0 — Auth (Email/Contraseña), Firestore con caché offline persistente, Hosting |
| Módulo nube | `www/cloud/firebase.js` (ESM) empaquetado con esbuild a `www/cloud/firebase.bundle.js` (md5 `57fa245b…`) y expuesto como `window.Cloud` |
| Plugins Capacitor | Camera, Filesystem, Share, SplashScreen, FileOpener, NativeBiometric (`@capgo/capacitor-native-biometric` 8.9.3), Assets |
| Build web | esbuild 0.28.2 (`pnpm build:cloud`) |
| Tests | Node puro, sin framework (`tests/test20*.js`) |
| Escritorio | Electron, repo aparte (`checklist-desktop`): detector + smoke tests |

## Estructura del repo

| Carpeta / archivo | Qué contiene |
|---|---|
| `www/index.html` | Toda la app: HTML, CSS y JS (login, secciones, Excel/PDF, IA, chat). |
| `www/cloud/firebase.js` | Módulo ESM con toda la lógica Firebase; expone `window.Cloud`. |
| `www/cloud/firebase.bundle.js` | Bundle generado con esbuild (`pnpm build:cloud`). **Se versiona**: la app lo necesita. Si cambia `firebase.js`, hay que regenerarlo. |
| `www/firebase-config.js` | Config del proyecto Firebase (NO se versiona; ver `firebase-config.example.js`). |
| `www/cap-plugins/`, `www/ocr/` | Plugins y recursos web de la app. |
| `www/manifest.json`, `www/*.png` | Manifiesto e iconos (logo de herramientas de laboratorio). |
| `android/` | Proyecto Android (Capacitor). `android/app/build.gradle`: `versionCode`/`versionName` y firma release. |
| `ios/` | Proyecto iOS (Capacitor). Versión en `MARKETING_VERSION` / `CURRENT_PROJECT_VERSION`. |
| `firestore.rules` | Reglas de seguridad de Firestore (qué puede leer/escribir cada rol). |
| `hosting/` | Hosting de Firebase: `firebase.json` y `hosting/public/firma.html` + su `firebase-config.js`. |
| `tests/` | Tests de regresión por versión (`test20*.js`) y las extracciones del `<script>` de cada versión (`checklist20*.js`, `checklist-*.html.bak`). |
| `docs/` | Esta documentación: setup, modelo de datos, build de APK, testing y changelog. |
| `capacitor.config.json` | Config de Capacitor (`appId` `mx.gerardo.checklistsoporte`, `webDir` `www`). |
| `package.json` | Dependencias y script `build:cloud`. |
| `assets/`, `icons/` | Recursos para generar iconos/splash (`make-lab-assets.cjs`, `make-splash.cjs`). |

## Inicio rápido

```bash
# 1. Dependencias (pnpm standalone; ver docs/BUILD_APK.md)
pnpm install

# 2. Configuración de Firebase (ver docs/SETUP_FIREBASE.md)
cp www/firebase-config.example.js www/firebase-config.js
# ... llenar www/firebase-config.js con los datos del proyecto ...
cp hosting/public/firebase-config.example.js hosting/public/firebase-config.js
# ... mismos valores ...

# 3. Si cambió www/cloud/firebase.js, regenerar el bundle
pnpm build:cloud

# 4. Sincronizar la web con Android/iOS
npx cap sync

# 5a. Probar en el navegador (modo local si no hay config real)
#     Servir www/ con cualquier servidor estático, p. ej.:
#     python3 -m http.server --directory www 8080

# 5b. Compilar la APK (detalle en docs/BUILD_APK.md)
cd android && ./gradlew assembleRelease
```

> **Nunca `pnpm dlx cap sync`**: `dlx` resuelve `cap` a un paquete npm
> ajeno y el sync falla. Siempre **`npx cap sync`** (el CLI local del
> proyecto).

## Documentación

- [docs/SETUP_FIREBASE.md](docs/SETUP_FIREBASE.md) — crear el proyecto
  Firebase, Auth, Firestore, reglas, Hosting, claves de IA y primer admin.
- [docs/DATA_MODEL.md](docs/DATA_MODEL.md) — colecciones y campos de
  Firestore, verificados en el código.
- [docs/BUILD_APK.md](docs/BUILD_APK.md) — requisitos, compilación y
  firma de la APK.
- [docs/TESTING.md](docs/TESTING.md) — tests de regresión y smoke de
  escritorio.
- [docs/CHANGELOG.md](docs/CHANGELOG.md) — qué cambió en cada versión
  2.0.0 → 2.5.6.
- [hosting/README.md](hosting/README.md) — la página pública de firma
  (`firma.html`).
