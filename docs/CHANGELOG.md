# Changelog — Checklist de Soporte (nube)

Resumen por versión, 2.0.0 → 2.5.15. Fuentes: el historial registrado
del proyecto (memoria 2026-11-12 a 2026-11-17) y las series de tests
(`tests/test20*.js`). Las versiones 2.0.1–2.0.4 no tienen registro y
no se documentan con supuestos.

## 2.5.15 — 2026-11-19

- **Vista «Responsiva»: «Enviar formulario en blanco» al número de
  WhatsApp configurado.** El botón `#btnRespBlanco` ahora lee el
  número del campo «Número de WhatsApp para enviar el formulario»
  (`#fResp-wa`) en el momento de pulsar y, si es válido, abre
  `wa.me/<número>?text=` con el mismo mensaje de invitación y el
  enlace `responsiva.html?id=…` (normalizador `mantWaNumber`: 10
  dígitos → prefijo 52; un número ya con 52 se respeta; espacios y
  guiones se quitan). Si el campo está vacío o el número no es válido
  (menos de 10 dígitos), mantiene el comportamiento anterior: abre
  `wa.me/?text=` para elegir contacto y avisa con «No hay número de
  WhatsApp configurado, elige el contacto». Con número avisa
  «Responsiva creada, enviada al número de WhatsApp.». Cómo se guarda
  el número y el envío directo del formulario del técnico NO cambian.
  Nada más cambia: ni `responsiva.html`, ni `firebase.js`, ni
  `firestore.rules`, ni el flujo de archivar/ver anteriores. El bundle
  de Firebase NO cambia esta vez: md5 `f9c4918d91bfbf4057433c43c54d708a`
  (506 932 B), mismo en APK y escritorio.
- Tests `test20265.js`: **903 true / 0 false** (896 de 2.5.14 + 7
  nuevas de la serie 265: versión 2.5.15 y bundle sin cambio, número
  con 52, número inválido cae al chooser, número con espacios y
  guiones se normaliza, el envío directo sigue igual). Los tests 263C
  (ahora con número: wa.me/525512345678) y 264B (ahora con el campo
  vacío: chooser + toast) se actualizaron al comportamiento nuevo.
  Detector tests sin cambios: 473/0. Smoke-265 VEREDICTO OK (clics
  reales en Electron: con número abre wa.me/525512345678 con la
  invitación y el enlace; sin número abre el chooser con el toast).
  El parche web y el de tests son reproducibles
  (`tests/patch_20265_web.py`, `tests/patch_20265_test.py`).
- APK 2.5.15 (versionCode 69): 15 772 993 B, md5
  `ed43fd8278cb797257b36973720b76ad`, firma permanente verificada
  (apksigner v2, 1 firmante: CN=Gerardo Cruz Hernandez), bundle sin
  cambio dentro (`f9c4918d…`, 506 932 B), `www/index.html` md5
  `db7493b921db8d49d2e60e0bf87319c7`.
  Escritorio 2.5.15 en el CHANGELOG del repo desktop.

## 2.5.14 — 2026-11-19

- **Vista «Responsiva»: texto de invitación, botón Archivar y
  «Ver responsivas anteriores».** Texto exacto «Por favor llena tus
  datos para crear tu responsiva» en tres sitios: (a) subtítulo en la
  vista Responsiva, junto al botón «Enviar formulario en blanco»;
  (b) mensaje de WhatsApp del enlace en blanco, antes del enlace
  (sustituye el «Hola, llena tu responsiva…»); (c) encabezado de la
  página pública `hosting/public/responsiva.html`, antes de los 6
  campos. Cada tarjeta activa de «Responsivas enviadas» (pendiente y
  llenada) trae ahora «📥 Archivar»: pide confirmación con
  «¿Archivar esta responsiva? Podrás verla en Responsivas
  anteriores.» y marca la responsiva como archivada (nueva
  `archivarResponsiva(id, archivado)` en `www/cloud/firebase.js`,
  expuesta en `window.Cloud`: `archivado: true` +
  `archivadoEn: ms` con update/merge; restaurar pone
  `archivado: false` y `archivadoEn: null`). Archivar NO borra nada:
  la tarjeta sale de la lista principal y pasa a la sección
  «Responsivas archivadas», que se muestra con el botón/toggle
  «📂 Ver responsivas anteriores» debajo de la lista principal (el
  toggle vive solo durante la sesión); cada tarjeta archivada muestra
  los mismos datos, el estado y la fecha de archivado, con su botón
  «↩️ Restaurar» (vuelve a la lista principal, sin confirmación). Sin
  archivadas muestra «No hay responsivas archivadas». La suscripción
  ya devuelve los docs y el filtrado es en la app. `firestore.rules`
  NO se toca: la rama update propio/admin no restringe campos, así
  que archivar/restaurar ya están permitidos. El formulario directo
  del técnico y el flujo de enviar en blanco NO se tocan salvo el
  texto nuevo. El bundle de Firebase cambia esta vez: md5 nuevo
  `f9c4918d91bfbf4057433c43c54d708a` (506 932 B), mismo en APK y
  escritorio.
- Tests `test20264.js`: **896 true / 0 false** (876 de 2.5.13 + 20
  nuevas de la serie 264: texto exacto en la vista, en el mensaje de
  WhatsApp en blanco y en `responsiva.html` servida en local por HTTP;
  archivar con confirmación (No no archiva, Sí archiva y avisa), la
  tarjeta sale de la principal y entra en archivadas, el toggle
  muestra/oculta la sección, restaurar la devuelve, sin archivadas el
  mensaje vacío, sin nube archivar avisa y no llama, el formulario
  directo y la suscripción siguen intactos). Detector tests sin
  cambios: 473/0. El parche web y el de tests son reproducibles
  (`tests/patch_20264_web.py`, `tests/patch_test_20264.py`).
- APK 2.5.14 (versionCode 68): 15 772 873 B, md5
  `89bb86e14cf31c2ca61201da4c3ef13d`, firma permanente verificada
  (apksigner v2, 1 firmante: CN=Gerardo Cruz Hernandez), bundle nuevo
  dentro (`f9c4918d…`, 506 932 B), `www/index.html` md5
  `e64acbbba466759205431be5f47c63b9`.
  Escritorio 2.5.14 en el CHANGELOG del repo desktop.

## 2.5.13 — 2026-11-19

- **Vista «Responsiva»: enviar el formulario EN BLANCO por WhatsApp
  (mismo patrón que la firma de Mantenimientos).** Botón nuevo
  «📤 Enviar formulario en blanco» (`#btnRespBlanco`): crea el
  documento en la colección nueva `responsivas` (estado `pendiente`,
  sin datos, `creadoPor` = uid actual, `creadoPorNombre` = nombre del
  técnico) y abre `wa.me/?text=` con el enlace
  `https://checklist-soporte.web.app/responsiva.html?id=<id>` para
  elegir el contacto (el destinatario es el colaborador, no el número
  guardado); toast «Responsiva creada, elige el contacto en
  WhatsApp». Sin nube avisa con toast y no abre nada. Nueva página
  pública `hosting/public/responsiva.html` (mismo estilo que
  `firma.html`, sin login): lee `?id=`, si no existe muestra «No se
  encontró la responsiva», si ya está llenada muestra «Esta
  responsiva ya fue llenada» con los datos, si está pendiente muestra
  el formulario con los 6 campos (todos obligatorios, mismo orden que
  la app) y al enviar guarda `datos` + `estado: 'llenada'` +
  `llenadoEn`, con confirmación y botón Cerrar (mismo patrón que
  `firma.html`). Nueva sección «Responsivas enviadas» (`#respList`,
  suscrita en vivo con `subscribeResponsivas`: admin ve todas,
  usuario normal solo las que creó): cada tarjeta muestra estado
  (Pendiente / Llenada + fecha) y quién la creó; la llenada trae los
  6 datos y los botones «📲 Compartir por WhatsApp» (texto con los 6
  datos), «✉️ Enviar por correo» (mailto «Responsiva: <nombre>») y
  «💾 Guardar en Excel» (.xlsx real con el patrón
  `buildXlsxFromTable`; Capacitor Share si está, si no descarga por
  `<a>`, si no toast honesto); la pendiente trae «🔗 Copiar enlace»
  (portapapeles, o wa.me con el enlace si no hay). La lista se
  actualiza sola cuando el colaborador llena el formulario. El
  formulario directo del técnico (2.5.11/2.5.12, con borrador local)
  sigue intacto.
- `crearResponsiva` y `subscribeResponsivas` en
  `www/cloud/firebase.js` (expuestas en `window.Cloud`); bloque nuevo
  `responsivas` en `firestore.rules` (list propio/admin, get público
  por id, create propio con estado `pendiente`, update propio/admin O
  público restringido a `datos`+`estado`+`llenadoEn` con estado
  `llenada` y los 6 campos no vacíos, delete propio/admin).
  Reglas publicadas en la consola de Firebase y `responsiva.html`
  desplegada en Hosting el 2026-11-19 (HTTP 200): el enlace ya
  funciona en vivo. El bundle de Firebase cambia esta vez: md5 nuevo
  `de3d2dce1924710dc8458d10f47a1c45` (506 783 B), mismo en APK y
  escritorio.
- Tests `test20263.js`: **876 true / 0 false** (861 de 2.5.12 + 15
  nuevas de la serie 263: botón y lista en HTML, funciones en la app,
  firebase.js y reglas; sin nube avisa y no abre nada; crea con el
  nombre del técnico y abre wa.me con el enlace; suscripción con uid
  propio y lista con pendiente y llenada; dispatch: copiar enlace,
  WhatsApp, correo y Excel .xlsx con los 6 datos; la lista se
  actualiza sola al llenarse; el formulario directo sigue intacto).
  `responsiva.html` verificada en local con Firebase simulado (sin
  tocar Firestore real): 8/8 (sin id, pendiente, envío vacío bloquea,
  envío lleno guarda, ya llenada, inexistente, colección correcta).
  El parche web y el de tests son reproducibles
  (`tests/patch_20263_web.py`, `tests/patch_test_20263.py`).
- APK 2.5.13 (versionCode 67): 15 771 981 B, md5
  `b875849f6e965a0f51cad3b17edb47e2`, firma permanente verificada
  (apksigner v2, 1 firmante), bundle nuevo dentro.
  Escritorio 2.5.13 en el CHANGELOG del repo desktop.

## 2.5.12 — 2026-11-19

- **Vista «Responsiva»: el formulario ahora se puede guardar y cerrar.**
  Botón nuevo «💾 Guardar y cerrar» (`#btnRespGuardar`) junto a Enviar
  y Limpiar: guarda los 6 campos tal como están (aunque estén
  incompletos, un borrador puede estar a medias) en localStorage
  (`checklist-soporte-resp-borrador-v1`), muestra el toast «Responsiva
  guardada» y vuelve a Inicio. Al abrir la vista Responsiva, si hay un
  borrador guardado los 6 campos se restauran (también la primera vez
  tras arrancar); sin borrador el formulario abre vacío, como antes. El
  número de WhatsApp NO forma parte del borrador: persiste aparte, en
  su propia clave (`checklist-soporte-resp-wa-v1`). Al enviar (con
  número configurado o sin él, vía `shareText`), tras abrir WhatsApp el
  borrador se borra y los 6 campos se vacían: la próxima abre vacía. Si
  la validación falla o el número es inválido, no se borra nada.
  «Limpiar» vacía los 6 campos y borra también el borrador. El
  borrador vive solo en el teléfono (localStorage); no va a la nube ni
  a Firestore.
- `respGuardarBorrador`, `respCargarBorrador`, `respBorrarBorrador`,
  `respGuardarYCerrar` y `respDespuesDeEnviar` en `www/index.html`;
  `showVista('resp')` restaura el borrador; `respEnviar` y
  `respLimpiar` actualizados; botón `#btnRespGuardar` en `#viewResp`.
- Tests `test20262.js`: **861 true / 0 false** (847 de 2.5.11 + 14
  nuevas de la serie 262: guardar el borrador completo e incompleto y
  volver a Inicio, restaurarlo al reabrir, no tocar el número,
  enviar con y sin número borra el borrador y vacía los campos, enviar
  con validación fallida no borra el borrador, Limpiar borra el
  borrador; la serie 261 se ajustó porque Enviar ya vacía los campos).
  El parche web y el de tests son reproducibles
  (`tests/patch_20262_web.py`, `tests/patch_test_20262.py`).
- Solo código, tests y docs en este cambio: la APK 2.5.12
  (versionCode 66) y el escritorio se construyen aparte; el bundle
  de Firebase sigue con md5 `57fa245be36954586955b6005296f937`, sin
  cambios.

## 2.5.11 — 2026-11-19

- **Vista «Responsiva»: formulario que se envía por WhatsApp al número
  configurado.** Quinto botón «📋 Responsiva» en el selector de Inicio
  (solo desde Inicio, no hay pestaña). El formulario pide Nombre
  Completo, Número de colaborador, Sucursal, Puesto, Jefe Directo y
  Área, todos obligatorios: si falta alguno se marca en rojo
  (`.campo-falta`, se quita al escribir) y el toast nombra los que
  faltan. Debajo, el campo «Número de WhatsApp para enviar el
  formulario» (tel, ejemplo de 10 dígitos) se guarda en localStorage
  (`checklist-soporte-resp-wa-v1`) al escribir y se carga al abrir la
  vista; no se manda a la nube. Al enviar, con los 6 campos y número
  válido (al menos 10 dígitos), abre
  `https://wa.me/<número>?text=...` con el número normalizado por
  `mantWaNumber` (10 dígitos → 52…) y el texto con el título
  «Responsiva — Checklist de Soporte», la fecha de hoy y los 6 campos
  con sus etiquetas. Sin número configurado abre `wa.me/?text=...`
  (vía `shareText`) para elegir el contacto y avisa con toast. El
  botón «Limpiar» vacía los 6 campos, no el número. El envío no guarda
  el formulario en la nube ni en localStorage.
- `respEnviar`, `respTexto`, `respCargarWa`, `respLimpiar` y
  `RESP_CAMPOS` en `www/index.html`; vista `#viewResp`, botón
  `#btnGoResp`, campos `#fResp-nombre`, `#fResp-colaborador`,
  `#fResp-sucursal`, `#fResp-puesto`, `#fResp-jefe`, `#fResp-area`,
  `#fResp-wa`, botones `#btnRespEnviar` y `#btnRespLimpiar`.
- Tests `test20261.js`: **847 true / 0 false** (832 de 2.5.10 + 15
  nuevas de la serie 261: vista y botón, 6 campos en orden, validación
  en rojo sin abrir WhatsApp, wa.me con 52 y los 6 datos y fecha, sin
  número abre wa.me/?text= y avisa, número persistido en
  localStorage, Limpiar vacía los 6 campos); detector 473/0;
  smoke-261 VEREDICTO OK.
- Solo código, tests, smoke y docs en este cambio: la APK 2.5.11
  (versionCode 65) y el escritorio se construyen aparte; el bundle
  de Firebase sigue con md5 `57fa245be36954586955b6005296f937`, sin
  cambios.

## 2.5.10 — 2026-11-17

- **Compartir un equipo detectado: WhatsApp recortado hasta Impresora,
  correo completo.** El botón «📲 Compartir por WhatsApp» manda ahora
  solo hasta la línea «Impresora: ...» (marca, modelo, tipo, serie,
  hostname, hardware, redes, AnyDesk, versiones detectadas, impresora)
  y ya no incluye políticas, usuario sistemas, escritorio revisado, SO
  detectado por, puntos detectados ni fecha/quién detectó. El botón
  «✉️ Compartir por correo» sigue mandando el texto completo, como en
  2.5.9. Si no hay impresora, el texto de WhatsApp termina en la última
  línea presente, sin dejar una línea de Impresora vacía.
- `detShareText(d, corto)` en `www/index.html`: con `corto=true`
  (WhatsApp) vuelve tras la línea de Impresora; sin el parámetro
  (correo, vía `detShareMail`) construye el texto completo de 2.5.9.
  El panel de «Equipos detectados» en pantalla no cambió.
- Tests `test20260.js`: **832 true / 0 false** (823 de 2.5.9 + 9
  nuevas de la serie 260: WhatsApp corto en ambos paneles, correo
  completo en ambos paneles, sin impresora no hay línea Impresora,
  panel sin cambios); detector 473/0; smoke-260 VEREDICTO OK.
- APK 2.5.10: 15 768 085 B, md5 `a8085d122467b985b4222e559039efbd`,
  versionCode 64, firma permanente, se instala sobre la 2.5.9.

## 2.5.9 — 2026-11-17

- **Compartir un equipo detectado por WhatsApp y por correo**: cada
  tarjeta de «Equipos detectados» (en Por preparar y en Mantenimientos)
  tiene dos botones nuevos junto a los de siempre: «📲 Compartir por
  WhatsApp» y «✉️ Compartir por correo». Comparten las características
  detectadas del equipo en texto claro y compacto, sin guardarlo como
  preparación: hostname, marca, modelo, serie, CPU, RAM, disco + tipo,
  sistema operativo + versión, IP + tipo y redes, AnyDesk (id y alias),
  antivirus + versión, agente ESET, Chrome, impresora, políticas
  (cambio de contraseña, longitud mínima, bloqueo, usuario sistemas) y
  fecha de detección + quién lo detectó. Los campos vacíos se omiten
  (no se listan con «-» ni «sin datos»).
- **Mismo patrón que el compartir de preparación**: WhatsApp abre
  `wa.me/?text=` sin número fijo (en escritorio `main.js` lo manda al
  navegador del sistema con `setWindowOpenHandler`); correo abre
  `mailto:` con asunto «Equipo detectado: \<hostname o modelo\>» y el
  mismo texto en el cuerpo. Compartir no marca el equipo como usado ni
  llama a la nube.
- Funciones nuevas en `www/index.html`: `detShareText(d)` (construye
  el texto reutilizando `hardwareLine`, `redesLine`, `anydeskLine`,
  `versionesLine`, `politicasText`, `escritorioLine`, `osFuenteLine`,
  `detLineFor`, `fmtDate`) y `detShareMail(d)`; listeners de `#detList`
  (`data-det-wa` / `data-det-mail`) y de `#mantDetList`
  (`data-mant-det-wa` / `data-mant-det-mail`).
- Bundle de Firebase sin cambios (`57fa245b…`).
- Tests `test20259.js`: 823 true / 0 false; tests del detector 473
  pasaron / 0 fallaron; smoke-259 VEREDICTO OK.

## 2.5.8 — 2026-11-17

- **Actualizaciones de Windows (solo escritorio)**: botón «🔄
  Actualizaciones de Windows» junto a Detectar y Contraseña de
  sistemas en Por preparar. Abre un panel con la última actualización
  instalada (Get-HotFix), la fecha de la última búsqueda, el número de
  actualizaciones pendientes con su lista (primeras 10 + «y N más») y
  los botones «Buscar actualizaciones» e «Instalar actualizaciones».
- **La búsqueda usa la API de Windows Update Agent (COM)** sin el
  módulo PSWindowsUpdate (no viene instalado en Windows):
  `Microsoft.Update.Session` → `CreateUpdateSearcher()` →
  `Search("IsInstalled=0 and Type='Software'")`. La búsqueda NO
  necesita elevación y puede tardar varios minutos; los botones se
  deshabilitan mientras corre una operación.
- **Instalar pide permiso de administrador** (UAC) si la app no corre
  elevada (mismo patrón que 2.5.7: `.ps1` temporal que se borra al
  terminar; la salida del proceso elevado se captura por archivo
  temporal). La instalación vuelve a buscar las pendientes en la
  misma sesión y las instala (`ResultCode 2`); puede tardar mucho.
  **La app NUNCA reinicia sola**: si Windows pide reinicio, solo lo
  avisa en el panel y en el mensaje.
- Tests `test20258.js`: 809 true / 0 false; tests del detector 473
  pasaron / 0 fallaron; smoke-258 VEREDICTO OK.
- APK 2.5.8: 15 766 905 bytes, md5
  `0736f9bf250d6def8c8fe302b1de4882`, versionCode 62, misma firma
  permanente, instala sobre 2.5.7. Escritorio 2.5.8 en Drive
  (AppImage, .deb y portable .exe en ZIP).
- Pendiente de probar con datos reales: búsqueda e instalación reales
  en una PC con actualizaciones pendientes, el aviso de UAC y el aviso
  de reinicio.

## 2.5.7 — 2026-11-17

- **Contraseña del usuario local Windows «sistemas» (solo escritorio)**:
  botón «🔑 Contraseña de sistemas» junto a Detectar en Por preparar.
  Abre un panel con usuario (por defecto «sistemas», editable),
  contraseña actual, nueva y confirmar; «Verificar» solo comprueba la
  actual y «Cambiar contraseña» la verifica y la cambia. La web valida
  que la nueva no esté vacía y que coincida con la confirmación antes
  de tocar Windows.
- **Las contraseñas nunca salen de la PC**: no se guardan en
  localStorage, no van a Firestore, no se registran en logs ni se
  muestran en pantalla. Windows no permite leer la contraseña actual;
  la única forma de «compararla» es validarla con
  `ValidateCredentials`. El cambio usa `Set-LocalUser` y **pide permiso
  de administrador** (UAC) si la app no corre elevada.
- Tests `test20257.js`: 790 true / 0 false; tests del detector 440
  pasaron / 0 fallaron; smoke-257 VEREDICTO OK.
- APK 2.5.7: 15 765 573 bytes, md5
  `1467ee732e93461d95cb5953ccd84312`, versionCode 61, misma firma
  permanente, instala sobre 2.5.6. Escritorio 2.5.7 en Drive
  (AppImage, .deb y portable .exe en ZIP).
- Pendiente de probar con datos reales: cambio real de contraseña en
  una PC, el aviso de UAC, verificación de una contraseña vieja
  correcta y de una incorrecta.

## 2.5.6 — 2026-11-17

- PDF de la orden de mantenimiento en **1 página carta**: la orden
  completa (ROBIT5) y una orden de estrés caben en una página; los
  datos del equipo salieron de Conclusión y van una sola vez en el
  cuadro gris COMENTARIOS de abajo a la izquierda (sin el rótulo
  «Datos detectados», sin duplicados).
- Fecha de conformidad válida: se corrigió el «Invalid Date» (el
  normalizador nuevo acepta Date, milisegundos, ISO y Timestamp de
  Firestore); la conformidad ya **no lleva hora** (título «FECHA,
  NOMBRE Y FIRMA DE CONFORMIDAD», solo `Fecha:`).
- Tests `test20256.js`: 770 true / 0 false; smoke-256 VEREDICTO OK.
- APK 2.5.6: 15 763 763 bytes, md5
  `a56b00198a1fc34d669ef4ec5be82f20`, versionCode 60, misma firma
  permanente, instala sobre 2.5.5. Escritorio 2.5.6 en Drive
  (AppImage, .deb y portable .exe en ZIP).
- Pendiente de probar con datos reales: el PDF carta impreso en una
  página; el PDF de una orden real sin datos duplicados, con fecha de
  conformidad válida y sin hora.

## 2.5.5 — 2026-11-17

- **Selección en Entrega Renta**: checkbox por equipo entregado;
  WhatsApp, Correo y Exportar a Excel actúan sobre los marcados; sin
  selección, sobre todos los entregados (con aviso); contador
  «Seleccionados: 2 de 3» y «Seleccionar todos / Ninguno».
- Entregados de renta con la misma **regla de 15 días** que Por
  preparar (`entregadoAt` se guarda al entregar, reabrir lo limpia;
  sin `entregadoAt` usa `createdAt`); después de 15 días solo el admin
  los ve.
- **Botón «📊 Exportar a Excel» en renta**: antes el botón que generaba
  el Excel se llamaba «📂 Abrir» y no se veía como opción; ahora el
  nombre dice lo que hace, en ambas vistas (Recibir y Entrega).
- **Responsable, Área y firma del usuario ya no son obligatorios**
  para crear la orden: se llenan solos con lo que el usuario manda en
  el formulario de firma (`firma.html`); sin firma la vista dice
  «Pendiente de firma». El PDF sigue exigiendo ambas firmas.
- **Campo obligatorio faltante marcado en rojo** (borde rojo + fondo
  claro) y el aviso nombra los que faltan; la marca se quita sola al
  escribir en el campo.
- **Detector: políticas desde gpedit.msc**: lee `Machine\Registry.pol`
  y `User\Registry.pol` (binario PReg) para inactividad y salvapantallas,
  y `secedit /export` para cuentas (edad máxima, longitud mínima,
  complejidad, intentos y duración de bloqueo; 0 = bloqueo manual);
  si secedit falla (necesita admin), usa `net accounts`. Cada valor
  lleva su fuente («gpedit (Registry.pol)», «directiva (secedit)»,
  «net accounts», «registro»).
- PDF de mantenimiento: tamaño **carta 612×792, 1 página**;
  DESCRIPCIÓN DEL EQUIPO solo con el hostname; el resto de los datos
  (marca, modelo, serie, CPU, RAM, disco, IP, impresora, AnyDesk,
  antivirus, SO, versiones, políticas, usuario sistemas) va al final,
  en Conclusión/Comentarios. La preparación sigue en A4.
- Tests `test20255.js`: 754 true / 0 false; detector 410/0;
  smoke-255 VEREDICTO OK.
- APK 2.5.5: 15 762 991 bytes, md5
  `8414c022f433979e7fa4f2a9c0e504f1`, versionCode 59, misma firma
  permanente, instala sobre 2.5.4. Escritorio 2.5.5 en Drive
  (AppImage, .deb y portable .exe en ZIP).
- Pendiente de probar con datos reales: orden sin responsable/área y
  que la firma los llene; campo en rojo; detector con gpedit.msc en
  una PC real (secedit necesita admin); PDF carta impreso; Excel de
  renta con selección; entregado de más de 15 días oculto al usuario
  normal y visible al admin.

## 2.5.4 — 2026-11-17

- **Botón «🔄 Actualizar»** en la vista de la orden: relee la orden
  de la nube y avisa si el usuario ya firmó o si aún no hay cambios.
- **«Generar PDF» guarda de verdad**: en el teléfono escribe el PDF
  en Documentos (o Caché si no se puede), verifica que el archivo
  quedó y lo abre; el aviso de éxito sale solo después de verificar.
- **PDF como el formato de papel** F0.S1.01 Rev0: empresas con
  casilla, contacto de Lapi solo para Lapi, «ORDEN DE SERVICIO» con
  folio en cuadro rojo, checkboxes de SOFTWARE/HARDWARE, ÁREA/UNIDAD
  y RESPONSABLE, tiempos y fechas, TÍTULO DEL CASO, TIPO DE FALLA,
  IDENTIFICACIÓN DEL EQUIPO, DESCRIPCIÓN DEL EQUIPO, CONDICIONES
  GENERALES, MANTENIMIENTO PREVENTIVO, DESCRIPCIÓN DE CAMBIOS,
  CONCLUSIÓN/COMENTARIOS, cuatro bloques de fecha con FIRMA SISTEMAS
  y FIRMA ÁREA SOLICITANTE, escala de satisfacción 0–10
  (INACEPTABLE / ACEPTABLE / EXCELENTE) y bloque de conformidad con
  firma del usuario; pie «F0.S1.01» y «Rev0.». Una página.
- **El admin bloquea/desbloquea el acceso a Mantenimientos por
  usuario** (`users/{uid}.mantBloqueado`): botón por usuario en la
  pestaña Usuarios (nunca en admins ni en sí mismo); bloquear no
  desactiva al usuario, solo le cierra Mantenimientos; el bloqueo se
  aplica en vivo sin cerrar sesión.
- Tests `test20254.js`: 699 true / 0 false; smoke-254 VEREDICTO OK.
- APK 2.5.4: 15 760 379 bytes, md5
  `3fe536b8555f2db8ff4d2709511a7d25`, versionCode 58, misma firma
  permanente, instala sobre 2.5.3. Escritorio 2.5.4 en Drive
  (AppImage, .deb y portable .exe).
- Pendiente de probar con datos reales: firma real por el enlace de
  WhatsApp + botón Actualizar; PDF guardado en Documentos y su
  apertura; PDF impreso contra el formato de papel; bloqueo con un
  usuario real bloqueado y su llegada en vivo.

## 2.5.3 — 2026-11-16

- En Entregados (y Devuelto) el equipo entregado más reciente aparece
  arriba: orden por `deliveredAt` descendente (empate: `createdAt`
  descendente); en no-admin se mantiene el agrupado propios-primero;
  las demás vistas no cambian.
- Tests `test20253.js` 668/0; smoke-253 VEREDICTO OK.
- APK 2.5.3: 15 755 027 bytes, md5
  `ccbbc1ca7004bd8dd5d9470041cedb00`, versionCode 57, misma firma
  permanente, instala sobre 2.5.2. Escritorio 2.5.3 en Drive (AppImage,
  .deb y ZIP Windows); primer portable `.exe` único de Windows.
- Pendiente de probar con datos reales: el equipo recién entregado
  arriba en Entregados y Devuelto.

## 2.5.2 — 2026-11-16

- Botón «Detectar equipo» en Mantenimientos (solo escritorio) que
  abre solo el panel de equipos detectados; el botón por equipo pasa a
  llamarse «Dar mantenimiento a este equipo» y abre el formulario de
  mantenimiento prellenado.
- Tests `test20252.js` 661/0; smoke-252 VEREDICTO OK.
- APK 2.5.2: 15 754 879 bytes, md5
  `76345ee84f079b247c2c2fd8487de777`, versionCode 56, misma firma
  permanente, instala sobre 2.5.1. Escritorio 2.5.2 en Drive.
- Pendiente de probar con datos reales: el botón Detectar en
  Mantenimientos en una PC real, la autoapertura del panel y el
  formulario prellenado.

## 2.5.1 — 2026-11-16

- 13 cambios en Mantenimientos Preventivos: empresa (Lapi / Ludi /
  Lapi Hemodiálisis; bloque de contacto solo para Lapi); hardware y
  software marcados por defecto; `'/'` por defecto en tiempos de
  reparación/viaje/caída, tipo de falla y fechas de
  planeación/compromiso/periodo de prueba; título del caso por defecto
  «Mantenimiento Preventivo sistemas» con selector de año; descripción
  del equipo por defecto = hostname; texto de cambios por defecto con
  la redacción de mantenimiento preventivo; solo la fecha de liberación
  sigue siendo campo de fecha, con firmas de técnico y usuario en el
  bloque Liberación; el admin puede borrar órdenes de servicio;
  `firma.html` con botón Cerrar tras firmar; el PDF solo se genera con
  ambas firmas y el bloque de conformidad del usuario va al final, a la
  derecha; compartir una copia que no se puede compartir ahora descarga
  el PDF y lo dice, en vez de afirmar que lo compartió.
- Tests del teléfono 640/0; smoke-251 VEREDICTO OK. Hosting `firma.html`
  2.5.1 desplegado y verificado en vivo.
- APK 2.5.1: 15 754 311 bytes, md5
  `bc3d73f401f827cff63ff985f9fa5494`, versionCode 55, misma firma
  permanente, instala sobre 2.5.0. Escritorio 2.5.1 en Drive.
- Pendiente de probar con datos reales: valores por defecto al abrir
  el formulario, secuencia de folios, enlace de WhatsApp + botón
  Cerrar, PDF con conformidad abajo a la derecha y compartir nativo.

## 2.5.0 — 2026-11-16

- **Mantenimientos Preventivos** (nueva sección): al abrir la app se
  elige la sección (selector de Inicio: Por preparar, Recibir renta,
  Entrega Renta, Mantenimientos Preventivos).
- El detector de Windows ahora reporta políticas (días de cambio de
  contraseña, longitud mínima, intentos de bloqueo, segundos de
  bloqueo, desde `net accounts` + `InactivityTimeoutSecs` /
  `ScreenSaveTimeOut`), si existe cuenta/perfil Windows «sistemas», y
  el primer nombre real de impresora.
- El técnico llena el formulario (serie, hostname y modelo obligatorios
  y marcados, técnico automático desde el login, firma del técnico en
  canvas), crea la orden con **folio automático desde 00001** o guarda
  un borrador sin folio; el usuario recibe un enlace de WhatsApp a
  `firma.html` para poner nombre, área, comentarios y satisfacción
  0–10 y firmar; el PDF solo se genera con ambas firmas y se puede
  compartir con el usuario; cada técnico ve solo sus órdenes, el admin
  ve todas.
- Reglas de Firestore para `mantenimientos` + `config/folios`
  publicadas; Hosting `firma.html` desplegado y verificado en vivo en
  https://checklist-soporte.web.app/firma.html?id=…
- APK 2.5.0: 15 751 451 bytes, md5
  `251b6d9e9b6c8c2cc1e2b4ccb2210344`, versionCode 54, misma firma
  permanente, instala sobre 2.4.0. Tests del detector 376/0, del
  teléfono 218/0; smoke de escritorio VEREDICTO OK (folio 00001
  simulado en modo local).
- Pendiente de probar con datos reales: la transacción real del folio
  contra Firestore, la firma en un teléfono real, el enlace de
  WhatsApp, el PDF con ambas firmas, y el detector reportando políticas
  y usuario «sistemas» en una PC real.

## 2.4.0 — 2026-11-15

- **Cero diálogos nativos**: la app ya no usa `alert`/`confirm`/
  `prompt` (71 alert → toast, 11 confirm → modal, 1 prompt → modal);
  los tests fallan en voz alta si alguno se llama. Esto ataca el bug
  del teclado que moría en escritorio tras «Usar este equipo».
- Arreglo latente de borrador: «Usar este equipo» ahora limpia el
  borrador en curso y restaura el texto del botón Guardar.
- Línea de diagnóstico de foco en Acerca de («Foco: sí/no · Elemento
  activo: …») para probar el bug del teclado en una PC real.
- Tests `test20240.js` 199/0; detector 338/0; smoke VEREDICTO OK.
- APK 2.4.0: 15 732 195 bytes, md5
  `91aacd1f695bf1e99fed71d78174bb29`, versionCode 53, misma firma
  permanente, instala sobre 2.3.9.
- Pendiente: la prueba de aceptación en una PC real (login → Detectar
  → «Usar este equipo» → escribir en formulario, búsqueda y chat).

## 2.3.9 — 2026-11-15

- Botón **«💾 Guardar avance»** en las tarjetas propias en
  preparación/listo (también borradores y con pendientes; el admin en
  cualquier tarjeta; nunca en equipos ajenos ni entregados).
- Tests `test20239.js` 190/0; detector 338/0.
- APK 2.3.9: 15 730 679 bytes, md5
  `95e734f4880c23784f67f496ca0b720f`, versionCode 52, misma firma
  permanente, instala sobre 2.3.8.

## 2.3.8 — 2026-11-15

- «Equipo con pendientes» hasta llegar al 100 %, luego «Listo para
  entregar»; el equipo detectado se puede guardar para después como
  borrador («Guardar para después»); Por preparar muestra solo los
  equipos del propio analista; el detector decide Windows 11 por número
  de build, lee los módulos de RAM instalados y detecta ambas
  instancias de ESET.
- Tests `test20238.js` 181/0; detector 338/0.
- APK 2.3.8: 15 730 239 bytes, md5
  `bd65b4049a6747109942b678ef257a52`, versionCode 51, misma firma
  permanente, instala sobre 2.3.7. Escritorio 2.3.8 en Drive.

## 2.3.7 — 2026-11-14

- **Permisos por analista**: un equipo es propio cuando
  `tecnicoUid` coincide con el usuario, o el nombre del técnico
  coincide, o el usuario registró una reasignación en él. Los equipos
  ajenos son de solo lectura para usuarios normales (solo compartir por
  WhatsApp/correo o solicitar asignación); el admin no tiene
  restricciones. Pestañas por analista: Nuevo / Reasignado / Devuelto.
- «Asignar a…» cambia el analista responsable; «Solicitar asignación»
  la pide al admin (Aprobar/Rechazar). Asignación ≠ Reasignación: la
  reasignación cambia al usuario final del equipo.
- APK 2.3.7: md5 `f164524343c45ba00a8b41fb2e4eda78`, versionCode 50,
  misma firma permanente.

## 2.3.6 — 2026-11-14

- Detector: nombre del SO endurecido (varias fuentes), redes con IP
  por adaptador (cableado e inalámbrico, estática/dinámica).
- Por punto sin marcar: **N/A** (se excluye del avance) y **✕ quitar**
  (con Restaurar).
- **Compartir avance** y **No listo** en equipos con avance < 100 %;
  entrega con < 100 % abre un panel (Reabrir para completar /
  Entregar así); Reabrir limpia `deliveredAt` y `readyAt`.
- APK 2.3.6: md5 `66c5c8cba34d1fc6260cc6cb610e0876`, versionCode 49,
  misma firma permanente.

## 2.3.5 — 2026-11-14

- Atajos de escritorio rehechos: carpetas de Escritorio del registro
  (User Shell Folders), glob `OneDrive*`, Escritorio público y Menú
  Inicio; coincidencia por nombre Y por destino; exclusión `/print/i`
  para no marcar Alfaweb por error.
- APK 2.3.5: md5 `6a4904956a21501266edb7a8dff23e52`, versionCode 48, misma firma permanente.

## 2.3.4 — 2026-11-14

- RAM en GiB corregida; resolver de nombre del SO de Windows.
- APK 2.3.4: md5 `1cde373d1877c88bb917ee87fa005f9c`, versionCode 47,
  misma firma permanente.

## 2.3.3 — 2026-11-14

- `machineId` como id del documento en `detectados` (serie real o
  hostname + MAC); cada detección pone `usado=false` de nuevo;
  bloqueo por máquina («Equipo detectado ✓»); versión del Agente ESET
  en `versiones.esetAgent`.
- APK 2.3.3: md5 `f4dee9a256dba511a44d4c84467f7a66`, versionCode 46,
  misma firma permanente.

## 2.3.2 — 2026-11-14

- Detector corregido tras los fallos reportados en 2.3.1: detecta
  Invgate, Adobe Acrobat (en vez de solo Reader), Alfaweb como atajo de
  escritorio y los atajos de navegador hcweb y gabinete; agrega
  versiones de software (versión del SO Windows, versión del antivirus
  Eset Nod, versión de Chrome) y datos de hardware (procesador, RAM,
  disco con tipo HDD/SSD/NVMe, IP del equipo e indicación de estática o
  dinámica, y número de AnyDesk).
- El `.exe` de escritorio ahora pide login cada vez que se abre, sin
  sesión recordada y sin huella en escritorio; en el teléfono siguen
  el recordar sesión y la huella.
- Pendiente de confirmar en una PC real: que detecte todo esto, en
  especial Invgate y el número de AnyDesk.
- APK 2.3.2: md5 `366a718a82c53a7ed4f3ba715a50c657`, versionCode 45.

## 2.3.1 — 2026-11-13

- El detector llena el checklist (`detectChecks()`): los puntos
  detectables se marcan solos y quedan registrados en `autoDetectado`.
  Primera versión con los fallos de detección que corrigió 2.3.2.
- APK 2.3.1: md5 `d1b3d902f02d8528c7ecca7e36e162a0`, versionCode 44.

## 2.3.0 — 2026-11-13

- El programa de escritorio lee las características reales del equipo
  y las manda a la nube; la APK trae el panel «Equipos detectados» y en
  Por preparar el botón «Detectar este equipo» llena el formulario con
  «Usar este equipo». Reglas de Firestore para el detector publicadas.
- Instala como actualización sobre 2.2.7 sin desinstalar ni perder datos.
- Versión portable de Windows 2.3.0 entregada como ZIP en Drive. El
  `.exe` instalador sigue sin funcionar (el «Checklist de Soporte Setup
  2.3.0.exe» de 237 KB no debe ejecutarse); el instalador NSIS sigue
  pendiente sin fecha. Instaladores de Mac y iPhone pendientes porque
  necesitan una Mac.
- APK 2.3.0: md5 `f896a334312604c3d6624ce57d60803d`, versionCode 43.

## 2.2.7 — 2026-11-13

- Campo **Hostname** en la preparación de equipos (se muestra en la
  tarjeta, el PDF, el WhatsApp y el Excel).
- APK 2.2.7: md5 `0b5f17f7b018e3a10ba88b0b3f85074e`, versionCode 42.

## 2.2.6 — 2026-11-13

- Cámara nativa para las fotos (serie y daños) con
  `@capacitor/camera` (origen PROMPT: cámara o galería); la APK **no**
  declara el permiso CAMERA de Android.
- APK 2.2.6: md5 `b30e59141f208aa1ace9eb7105c63a8c`, versionCode 41.

## 2.2.5 — 2026-11-13

- **DeepSeek como respaldo de la IA** (`deepseek-flash`): si Gemini
  falla o no tiene clave, la app intenta con DeepSeek. La clave se
  guarda en Firestore `config/ai`.
- APK 2.2.5: md5 `5568cc9b2358dcbff12ed2a6641dbd20`, versionCode 40.

## 2.2.4 — 2026-11-13

- Cadena de 3 modelos Gemini (`gemini-3.8-flash`,
  `gemini-3.5-flash-lite`, `gemini-flash-latest`) con avance solo en
  404/503/429 y un reintento de red.
- APK 2.2.4: md5 `1f07159139dbe7d9f202679bc21195a2`, versionCode 39.

## 2.2.3 — 2026-11-13

- Modelo `gemini-3.8-flash` + respaldo `gemini-flash-latest`.
- APK 2.2.3: md5 `1297e65743829c810c57c2acf5d95d1b`, versionCode 38.

## 2.2.2 — 2026-11-13

- `apiMessage` + textos de error de la IA y un reintento de red.
- APK 2.2.2: md5 `9f19ef2952f2713e7c7e7971cace0f8d`, versionCode 37.

## 2.2.1 — 2026-11-13

- Arreglo: los botones de IA estaban muertos porque faltaban en la
  cadena de despacho de clics.
- APK 2.2.1: md5 `450fc5a6202512ac9fdb9512d14deefe`, versionCode 36.

## 2.2.0 — 2026-11-13

- Tres funciones de IA con Gemini gratis: «¿Qué falta?» en cada equipo
  en preparación o listo; «Revisar daños con IA» en Recibir renta
  (foto del equipo, la IA describe los daños visibles, se guarda en el
  equipo y se ve en todos los teléfonos); «Resumen con IA» en equipos
  entregados (la IA redacta el mensaje de WhatsApp).
- La clave gratuita de Gemini ya está guardada en la app. Las fotos de
  revisión de daños se mandan a Google: no fotografiar datos sensibles.
- APK 2.2.0: md5 `2a48955dd60e208d3f3194cb0746093c`, versionCode 35.

## 2.1.3 — 2026-11-13

- Arreglo del arranque reportado ese día: tras instalar, la app
  mostraba la interfaz como si ya hubiera entrado y luego pedía
  usuario. Ahora la interfaz empieza oculta y solo aparece cuando la
  sesión está confirmada, y el splash ya no desaparece a los 3 segundos
  fijos sino que espera a que la app decida si muestra el login o la
  interfaz: al abrir se ve solo el splash con el logo y luego va
  directo al login.
- APK 2.1.3: md5 `99f97f55f30ec19c79e8823609dec8e6`, versionCode 34.

## 2.1.2 — 2026-11-13

- El login dice «Ingresa con tu usuario para ver y registrar equipos»,
  el logo del login flota suavemente y la tarjeta anima al entrar; la
  pestaña Usuarios trae botón Editar por usuario para cambiar nombre,
  usuario y correo. El correo que cambia es el de contacto /
  recuperación; el correo de login no cambia porque solo el propio
  usuario puede cambiarlo — si el admin luego cambia la contraseña, la
  cuenta se recrea con el correo nuevo.
- APK 2.1.2: md5 `383265bbdc521983c23baf65f4f7b675`, versionCode 33.

## 2.1.1 — 2026-11-13

- Moderación del chat por el admin: 🗑️ en cada mensaje (grupo y DM).
- APK 2.1.1: md5 `0f1c858877fda184ce28f4d181eb03e3`, versionCode 32.

## 2.1 — 2026-11-13

- Por preparar ya se sincroniza entre teléfonos (colección
  `preparations`), igual que la renta; chat individual (DM) en Equipo.
- APK 2.1: md5 `baec572b135d6377b2afddd3b847b464`, versionCode 31.

## 2.0.20 — 2026-11-13

- Pista de la opción de Office (elegir Office 365 o LibreOffice para
  llegar al 100 %); chat efímero de 24 h (auto-borrado).
- APK 2.0.20: md5 `81d06beb6fe7bf2f523b426e620e2c96`, versionCode 30.

## 2.0.19 — 2026-11-13

- Pestaña **💬 Equipo**: presencia (quién está en línea) + chat de
  grupo entre analistas.
- APK 2.0.19: md5 `7f5abb2b4574b8bba3853c607fba26a7`, versionCode 29.

## 2.0.18 — 2026-11-13

- Arreglo del bug reportado ese día: tras entrar como Gerardo y como
  Alejandro, el campo «Analista responsable» se quedaba en Axel Danyael
  y no cambiaba con el login, así que los equipos nuevos se guardaban
  con el analista equivocado. Ahora el campo cambia con el login y un
  nombre escrito a mano en el campo se respeta.
- APK 2.0.18: md5 `59695948c5d4b42ac61b3d72beb40783`, versionCode 28.

## 2.0.17 — 2026-11-13

- Incluye todo lo de 2.0.16 (compilada y verificada, no liberada como
  APK aparte): «Cuenta de red creada» quitada de los datos del usuario
  en Equipo nuevo y Reasignar Equipo; los botones por tarjeta PDF /
  Compartir, Reasignar y Eliminar son solo de admin, mientras el botón
  grande «Reasignar Equipo» lo ven todos los usuarios y cualquier
  usuario puede guardar una reasignación; «Limpieza física del equipo»
  aparece solo en equipos reasignados, no en los nuevos; los usuarios
  normales siguen marcando Listo y Entregado y exportando a Excel o
  mandando por WhatsApp y correo.
- APK 2.0.17: md5 `0955a223d85779a5c9c89e4c060f340d`, versionCode 27.

## 2.0.16

- Ver 2.0.17 (no se liberó como APK aparte).

## 2.0.15 — 2026-11-13

- Nueva plantilla por defecto para equipos nuevos: «Limpieza física
  del equipo» quitada de Equipo y hardware; «Office instalado y
  activado» ahora ofrece Office 365 o LibreOffice, y la elección se ve
  en el PDF y en el mensaje de WhatsApp; VPN configurada, Sistema Lapi
  Fox y Alfaprinter son opcionales y no cuentan para el avance; puntos
  nuevos: Google Chrome, Adobe Reader, WinRAR, Alfaweb, Accesos
  directos historia clínica y estudios de gabinete, y AnyDesk Gris; la
  plantilla se actualiza sola al abrir la app, conserva los puntos que
  el usuario agregó, y los equipos guardados conservan sus marcas.
- APK 2.0.15: md5 `214ca6f2dcbbf8c428529b12f9e9570c`, versionCode 25.

## 2.0.14 — 2026-11-13

- Vista Todos paginada (5 equipos entregados por página).
- APK 2.0.14: md5 `17bb6feef70fccdf0d8af58846870a17`, versionCode 24.

## 2.0.13 — 2026-11-13

- Botón «Reasignar Equipo» de ancho completo arriba, junto a «Nuevo
  equipo»: abre un panel para preparar equipo que no es nuevo; se elige
  el equipo de una lista (marca, modelo, serie, usuario actual), «Era
  de» se llena solo con el usuario actual, «Se reasigna a» toma el
  nuevo usuario, y al guardar vuelve a En preparación con el usuario
  anterior registrado; «Otro equipo» permite meter a mano un equipo no
  listado, como equipo usado con su historial.
- APK 2.0.13: md5 `3183c52d59904d2863e03a380e561227`, versionCode 23.

## 2.0.12 — 2026-11-13

- Los equipos entregados se ven en Todos/Entregados 15 días con Excel,
  WhatsApp y el nuevo «Enviar por correo», y después solo los ve el
  admin; guardar un equipo nuevo cambia solo a En preparación,
  completando la cadena preparación → Listos → Entregados; cada tarjeta
  trae botón «Reasignar» («Era de» prellenado, «Se reasigna a») que
  devuelve el equipo a En preparación con el historial de usuario
  anterior/nuevo registrado en la tarjeta, el PDF, el WhatsApp y una
  columna nueva del Excel.
- APK 2.0.12: md5 `33e053370109c5215adb011e8b9269ed`, versionCode 22.

## 2.0.11 — 2026-11-13

- Cambio automático de pestaña al marcar Listo/Entregado; Excel y
  WhatsApp solo en Entregados.
- APK 2.0.11: md5 `4de3a0d8dae4822d491e7a7613163ba5`, versionCode 21.

## 2.0.10 — 2026-11-13

- Botón **Listo** (`readyAt`); «Técnico» pasa a llamarse «Analista»
  en toda la app.
- APK 2.0.10: md5 `7de3ff5ac381974725764169e7111797`, versionCode 20.

## 2.0.9 — 2026-11-13

- Incluye todo lo de 2.0.8 (nunca liberada como APK aparte): bloqueo de
  cuenta tras 10 intentos fallidos de login solo para usuarios normales
  (nunca el admin), botón de desbloqueo del admin, y cambio de
  contraseña del admin y por usuario.
- Nuevo en 2.0.9: enlace «Olvidé mi contraseña» que manda un correo de
  restablecimiento en español cuando la cuenta tiene un correo real, y
  login biométrico (huella) ofrecido tras el primer login con
  contraseña, gestionable desde el botón Contraseña de la cuenta.
- Volver a dar de alta a un usuario borrado ya funciona: con la misma
  contraseña recupera la cuenta como estaba, y con otra contraseña crea
  una cuenta nueva con el mismo nombre de usuario; solo un nombre de
  usuario o correo activo da «ya registrado».
- APK 2.0.9: md5 `eef2c2fd0853b7a2f9d5666a53d585f1`, versionCode 19.

## 2.0.8

- Ver 2.0.9 (no se liberó como APK aparte).

## 2.0.7 — 2026-11-13

- El admin puede borrar usuarios; el equipo de renta entregado solo lo
  ve el admin, no los usuarios normales; compartir desde Recibir renta
  y Entrega Renta ofrece WhatsApp o correo y adjunta de verdad el
  Excel (arregla el bug en el que decía que el archivo se guardó pero
  no guardaba nada); el campo «Cuenta de red» se quitó de la
  preparación de equipos, de su Excel y de su PDF.
- El admin no puede borrar su propia cuenta.
- APK 2.0.7: md5 `139a3a0c14e0f779f70b58fd2cc17dcd`, versionCode 17.

## 2.0.6 — 2026-11-13

- Se quitaron los registros de acceso de la pantalla de login; login
  por usuario y contraseña, con correo opcional al crear usuarios;
  checkbox de recordar sesión; Por preparar muestra el nombre del
  técnico que entró, y el Excel de renta agrega una columna Analista
  (llamada Técnico en 2.0.6, renombrada en 2.0.10) con quien recibió el
  equipo en Recibir renta y quien lo entregó en Entrega Renta.
- APK 2.0.6: md5 `5d16ea691f870064360c82ca5a501312`, versionCode 16.

## 2.0.5 — 2026-11-12

- Arreglo del login: `#loginView {display:flex}` ganaba a `[hidden]`;
  con `[hidden]{display:none!important}` el login ya aparece.
  Confirmado por Gerardo: «Ya entre».
- APK 2.0.5: versionCode 15.

## 2.0.0 — 2026-11-12 (aprobada)

- Primera versión en la nube: una app con roles admin/usuario, login,
  equipos de renta sincronizados entre teléfonos por Firestore
  (con offline), el admin crea/desactiva usuarios desde la app, y
  secciones Por preparar, Recibir renta y Entrega Renta con inventario
  y accesorios por tipo (laptop: cargador, mouse, maletín; iPad:
  capacidad, cargador, cable; PC: CPU, capacidad, cable de corriente,
  mouse, teclado, cable de video, tarjeta de video adicional), cada
  sección de renta con su reporte de Excel.
- APK 2.0.0: versionCode 10.
