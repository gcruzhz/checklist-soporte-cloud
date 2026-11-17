# Hosting — Página pública de firma (Checklist de Soporte)

Página pública para que el usuario final firme una orden de mantenimiento desde
el celular, sin app y sin cuenta. URL:

    https://checklist-soporte.web.app/firma.html?id=<id del doc en `mantenimientos`>

## Archivos

- `public/firma.html` — la página. Lee `?id=`, carga el doc de `mantenimientos`
  con el SDK web de Firebase (compat, gstatic), muestra folio/técnico/caso/
  falla/equipo/fecha, y el formulario de firma.
- `public/firebase-config.js` — config del proyecto (copia de valores de
  `www/firebase-config.js`). La apiKey es pública por diseño; la seguridad la
  dan las reglas de Firestore.
- `firebase.json` — hosting, `public: "public"`.
- `.firebaserc` — proyecto default `checklist-soporte`.

## Cómo desplegar (agente principal, con Firebase CLI y login)

```bash
cd ~/workspace/android/checklist-cloud/hosting
firebase deploy --only hosting
# o, para probar antes sin afectar producción:
firebase hosting:channel:deploy preview-firma --only hosting
```

Requisitos previos (pendientes, no hechos aquí):
1. Firebase CLI instalado y con sesión en la cuenta gerardo.cruzhz@gmail.com
   (`firebase login`).
2. Reglas de Firestore para `mantenimientos` publicadas por el agente del
   teléfono: lectura pública del doc por id y escritura SOLO de los campos
   `firma` y `estado`. Sin esas reglas, la página carga la orden pero el
   envío falla con `permission-denied`.
3. Anonymous Auth es OPCIONAL: la página no pide login y funciona igual con
   o sin él (las reglas son públicas por link).

## Comportamiento

- Campos obligatorios (decisión de Gerardo): **nombre, área y firma**.
  El envío se bloquea si falta alguno y muestra cuáles faltan.
- Satisfacción 0–10 opcional (0–3 INACEPTABLE, 4–7 ACEPTABLE, 8–10 EXCELENTE);
  si no se elige, se guarda `satisfaccion: null`.
- La firma se guarda como PNG del canvas (trazo, pocos KB) en
  `firma: {nombre, area, comentarios, satisfaccion, firma, firmadoEn}` y
  `estado: 'firmada'` (update con merge sobre el doc existente).
  `firmadoEn` usa `serverTimestamp()` de Firestore.
- Si el doc ya tiene firma, muestra "Ya firmaste esta orden" con los datos
  y no permite firmar dos veces.

## Verificación local (hecha 2026-11-15)

- Servido con `python3 -m http.server` y comprobado con curl (200, HTML completo).
- Prueba con jsdom + mock de Firestore (ver `/tmp/firma-test/`):
  carga de orden, bloqueo sin nombre/área/firma, envío correcto con los 3
  datos, vista de "ya firmada" y error sin `?id=`.
- NO probado: despliegue real, carga desde un teléfono real por WhatsApp,
  ni escritura real en Firestore (no había credenciales de servicio en la VM).
