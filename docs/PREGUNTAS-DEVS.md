# Preguntas frecuentes para los devs — Checklist de Soporte

Respuestas listas para pasarle a un desarrollador que va a tomar la app.
Versión actual: **2.5.8** (2026-11-17). Repos y documentación completa en
[GitHub](#código-y-documentación).

## ¿En qué lenguaje está?

**JavaScript en todo.** La app es una sola página web (HTML, CSS y
JavaScript, **sin framework** como React o Vue). Lo nativo de Android e
iOS es mínimo: solo lo que genera Capacitor.

## ¿En qué se hizo la interfaz gráfica de ambas?

Es **la misma interfaz para las dos**: un solo archivo `www/index.html`
con CSS propio.

- **Teléfono (APK):** esa misma página corre dentro de Capacitor, en un
  WebView.
- **Escritorio (Windows/Linux):** la misma página corre dentro de
  Electron, en Chromium.

Los PDF y el Excel se generan con código propio, sin librerías de diseño.

## ¿Qué herramientas se usaron?

| Para qué | Herramienta |
|---|---|
| Login, base de datos y hosting de la página de firmas | Firebase: Auth, Firestore y Hosting (proyecto `checklist-soporte`, plan Spark, sin Cloud Functions) |
| App de teléfono | Capacitor 8.6.0 |
| App de escritorio | Electron 38.8.6, electron-builder 26.18.0 |
| Empaquetar el JavaScript | esbuild |
| Paquetes | pnpm |
| Compilar la APK | Gradle con Android SDK |
| Leer el número de serie por foto | Tesseract.js (OCR, local) |
| IA («¿Qué falta?», daños por foto, resumen) | Google Gemini primero, DeepSeek como respaldo |
| Detector de equipos Windows | JavaScript + PowerShell (lee gpedit.msc / Registry.pol, `net accounts`, hardware, AnyDesk, impresoras, políticas) |

## ¿Qué me pueden preguntar los devs?

- **Acceso al proyecto de Firebase** (consola, proyecto
  `checklist-soporte`) y **a GitHub** (usuario `gcruzhz`, repos públicos).
- **Quién es admin:** Gerardo es el admin; él crea y desactiva usuarios
  desde la app, y puede bloquearle Mantenimientos a un usuario sin
  desactivarlo.
- **Cómo se publican las reglas de Firestore y la página de firmas**
  (`firma.html` en Firebase Hosting): con el Firebase CLI, desde la
  sesión autorizada de Gerardo.
- **Dónde están las claves de Gemini y DeepSeek:** en Firestore
  (`config/ai`), **no en el código**.
- **Qué falta por hacer:** el instalador NSIS de Windows está roto (se
  entrega un .exe portable en ZIP); iOS necesita una Mac; los archivos de
  Windows van sin firmar por decisión de Gerardo.
- **Cómo se prueba todo:** en teléfono y PC reales (ver `docs/TESTING.md`).
  Pendiente de probar en 2.5.8: la búsqueda y la instalación reales de
  actualizaciones de Windows en una PC con pendientes, el aviso de
  administrador (UAC) y el aviso de reinicio (la app nunca reinicia
  sola). Ya probado en 2.5.7: el cambio de contraseña del usuario
  Windows «sistemas» se entregó en esa versión.

## Código y documentación

- Nube: https://github.com/gcruzhz/checklist-soporte-cloud
- Escritorio: https://github.com/gcruzhz/checklist-soporte-desktop
- Paquete completo para devs (código + docs + binarios que no van a
  GitHub): ZIP 2.5.8 en Drive —
  https://drive.google.com/file/d/1iuvGqqKc9SGclImkjqFwqLKycdafSSVv/view?usp=drivesdk
- En cada repo: `docs/CHANGELOG.md` (historial por versión),
  `docs/SETUP_FIREBASE.md` (cómo levantar el backend),
  `docs/DATA_MODEL.md` (colecciones de Firestore),
  `docs/BUILD_APK.md` (cómo compilar) y `docs/TESTING.md`.

## Lo que NO va a GitHub

Archivos binarios (iconos, splash, OCR y el wrapper de Gradle). Esos van
en el ZIP de Drive, y en la documentación dice cómo regenerarlos.

## Regla vigente

Desde el 2026-11-17, cada versión que se entrega también se sube a GitHub
como parte de la entrega. Este documento se incluye en el próximo push.
