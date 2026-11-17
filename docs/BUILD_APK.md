# Compilar la APK — Checklist de Soporte 2.5.6

## Requisitos

| Herramienta | Versión / nota (verificada en el repo y en `~/workspace/android/`) |
|---|---|
| JDK | **21 Temurin** (Capacitor 8 / AGP 8.13 exigen JDK 21; con JDK 17 el build falla con `invalid source release: 21`). En este entorno: `~/workspace/android/jdk21/`. |
| Android SDK | En `~/workspace/android/sdk/`; entorno listo en `~/workspace/android/env.sh` (cargarlo con `source`). |
| Node | Por confirmar la versión exacta usada; el proyecto usa `esbuild` 0.28.2 y Capacitor 8.6.0. |
| pnpm | **Standalone** (`~/.local/share/pnpm/bin/pnpm`). `npm install` falla en este sandbox con `EPERM chown`; `--unsafe-perm` no lo arregla. |
| Gradle | Lo trae el wrapper del proyecto Android (`android/gradlew`). |

Notas del entorno (ver `~/AGENTS.md`): Java no sale a internet por
defecto en este sandbox — el proxy de egreso exige IPv4 y su CA está
importada en el JDK; si el build falla con `PKIX path building failed`,
correr `~/workspace/android/refresh-ca.sh` y parar el daemon de Gradle
(`./gradlew --stop`) antes de reintentar. Si un build largo muere sin
log claro, revisar si la VM se reinició (`date` / `uptime`).

## Pasos

```bash
cd ~/workspace/android/checklist-cloud

# 1. Dependencias
pnpm install

# 2. Si cambió www/cloud/firebase.js, regenerar el bundle
#    (la app instalada usa el bundle, NO el .js)
pnpm build:cloud
#    Verifica el md5 del bundle: APK y escritorio deben llevar el mismo.

# 3. Sincronizar la web con Android/iOS
npx cap sync

# 4. Compilar la APK release
cd android
./gradlew assembleRelease
```

La APK queda en `android/app/build/outputs/apk/release/` (ruta estándar
de Gradle; por confirmar la ruta exacta en la próxima compilación).

> **Nunca `pnpm dlx cap sync`**: `dlx` resuelve `cap` a un paquete npm
> ajeno (`cap@0.2.1`) y el sync falla o ensucia el proyecto. Para
> sincronizar Capacitor usar siempre **`npx cap sync`** (el CLI local
> del proyecto).

## Versionado

Al subir de versión hay que tocar estos tres sitios (y que coincidan):

1. **Android** — `android/app/build.gradle`, en `defaultConfig`:
   `versionCode 60` y `versionName "2.5.6"` (valores actuales).
   `versionCode` sube en 1 por cada release; `versionName` es la
   versión visible.
2. **iOS** — `ios/App/App.xcodeproj/project.pbxproj`:
   `MARKETING_VERSION = 2.5.6;` y `CURRENT_PROJECT_VERSION = 60;`
   (en las dos configuraciones de build).
3. **En la app** — las líneas de versión en `www/index.html`:
   `Versión 2.5.6` en el login y `Versión: 2.5.6` en la pantalla de
   información (buscar `Versión` en el archivo).

El `package.json` del repo sigue en `"version": "1.0.0"` y no se usa
como versión de la app (por confirmar si debe alinearse).

## Firma

- La APK release se firma con `signingConfigs.release` en
  `android/app/build.gradle`, que lee `../../keys/checklist-keystore.properties`
  (fuera del repo, en `~/workspace/android/keys/`).
- **El keystore NO está incluido en el repo** — está en el `.gitignore`
  (`*.keystore`) y no se comparte. Cada desarrollador que compile desde
  este repo usa el keystore debug o su propio keystore release.
- **La firma permanente de Gerardo NO se comparte.** Cambiar de firma
  exige desinstalar la app instalada una vez; a partir de ahí las
  actualizaciones con la misma firma funcionan. (Lección del keystore
  debug: se regeneraba en cada reinicio de la VM y Android bloqueaba las
  actualizaciones.)
- `minifyEnabled false` en el build release; sin ofuscación.
- `android/app/build.gradle` aplica el plugin de Google Services solo
  si existe `android/app/google-services.json`; sin él, el log avisa que
  las push no funcionarán (no se usan en la app, por confirmar).

## Proxy (opcional)

Si compilas detrás de un proxy HTTP, copia `android/gradle.properties.example` a
`android/gradle.properties` y llena ahí `systemProp.http/https.proxyHost`,
`proxyPort`, `proxyUser` y `proxyPassword`. Ese archivo NO se versiona
(está en `.gitignore`): nunca commitees credenciales de proxy.

## Activos binarios (solo en el ZIP, no en el snapshot de GitHub)

Algunos archivos binarios NO se suben a GitHub con el conector (solo
acepta texto UTF-8); sí están en el ZIP completo de Drive. Si clonas
solo desde GitHub, regenéralos así antes de compilar:

- **Iconos y splash de Android e iOS** (`android/app/src/main/res/**/splash.png`,
  `ic_launcher*.png`, `ios/App/App/Assets.xcassets/**`, `icons/*.webp`):
  se regeneran con `npx @capacitor/assets generate` a partir de
  `assets/icon.png` y `assets/splash.png`. Esos dos a su vez se regeneran
  con `node make-lab-assets.cjs` (desde el `.webp` de `assets/`) o
  `node make-splash.cjs` (desde `assets/icon-source.svg`).
- **`www/lab-icon.png`**: `node make-lab-assets.cjs`.
- **`www/ocr/`** (`tesseract-core.wasm`, `lang/eng.traineddata.gz`):
  archivos vendored de la librería tesseract.js (OCR de la foto del
  número de serie); se descargan de nuevo del paquete tesseract.js
  (versión en `package.json`).
- **`android/gradle/wrapper/gradle-wrapper.jar`**: el JAR del wrapper
  de Gradle; si falta, genera el wrapper con un Gradle instalado
  (`gradle wrapper --gradle-version 8.14.3`) o descárgalo de la
  distribución oficial de Gradle.
