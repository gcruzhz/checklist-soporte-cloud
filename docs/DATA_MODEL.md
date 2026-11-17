# Modelo de datos — Firestore

Colecciones y campos clave verificados en `www/cloud/firebase.js`,
`www/index.html` (funciones `*ToCloudDoc` / `*FromCloud`) y
`firestore.rules`. Todo lo que no se pudo verificar en el código se
marca como **«según código»** (es decir, inferido de un solo punto del
código) o **por confirmar**.

Convenciones: los documentos llevan su `id` como ID del documento de
Firestore (no como campo, salvo donde se indica); `createdAt` /
`updatedAt` son milisegundos (epoch, `Date.now()`), salvo `lastSeen` y
los `createdAt` de `chat`/`dm`, que son `serverTimestamp()`.

## `users/{uid}` — usuarios de la app

Creado por `bootstrapAdmin` (primer admin) o `createUserByAdmin`.
Campos verificados:

| Campo | Tipo / valor |
|---|---|
| `email` | string. Correo de contacto (y de recuperación). En el alta por admin puede ser el correo real del usuario o un correo de acceso generado (`usuario@checklist.local`, versionado `.2`, `.3`… si el original ya existe en Auth). |
| `nombre` | string. Nombre visible (p. ej. el del técnico). |
| `usuario` | string, minúsculas. Nombre de usuario para entrar (puede ser `''` si no se definió). |
| `rol` | `'admin'` o `'usuario'`. |
| `activo` | boolean. `false` = usuario desactivado, no puede entrar. |
| `mantBloqueado` | boolean. Solo lo pone el admin (`setMantBloqueado`): bloquea Mantenimientos sin desactivar al usuario. El admin nunca se lo pone a sí mismo ni a otro admin. |
| `createdAt` | número (epoch ms). |

Reglas: lectura para activos; creación solo en bootstrap o por admin;
actualización y borrado solo admin. El admin no puede borrar su propia
cuenta (según código de la app; la regla lo permitiría — por confirmar
dónde se aplica exactamente esa restricción).

## `usernames/{nombreMinusculas}` — resolución usuario → acceso

| Campo | Tipo / valor |
|---|---|
| `email` | string. Correo de acceso en Auth (puede ser `@checklist.local`). |
| `emailReal` | string. Correo real del usuario (contacto / recuperación). |
| `uid` | string. UID de Auth del usuario. |
| `rol` | `'admin'` o `'usuario'`. |

Lectura pública (para entrar con usuario sin sesión); escritura solo
admin. `resolveUsername` busca por nombre en minúsculas;
`resolveEmail` busca por `email` o por `emailReal`.

## `preparations/{id}` — equipos en Por preparar

El documento que se guarda es el que devuelve `prepToCloudDoc(p)` en
`www/index.html`. Campos:

| Campo | Tipo / valor |
|---|---|
| `id` | string (mismo que el ID del documento). |
| `createdAt` | número (epoch ms). |
| `deliveredAt` | número o `null`. Se pone al entregar. |
| `readyAt` | número o `null`. |
| `checks` | objeto `{ [idPunto]: boolean }` con los puntos marcados. |
| `extraItems` | array. Puntos agregados por el técnico. |
| `naItems` | objeto `{ [idPunto]: true }`. Puntos marcados N/A. |
| `removedItems` | array. Puntos quitados por el técnico. |
| `noListo` | objeto o `null`. Marcador «No listo»; se limpia solo al llegar al 100 %. |
| `autoDetectado` | array. Puntos que marcó el detector (según código). |
| `borrador` | boolean. `true` = guardado para después. |
| `tecnicoUid` | string. UID del técnico dueño del equipo. |
| `tecnico` | string. Nombre del técnico/analista responsable. |
| `reasignaciones` | array. Historial de reasignaciones (`Era de` → `Se reasigna a`). Estructura interna por confirmar. |
| `asignaciones` | array. Historial de asignaciones (según código). Estructura interna por confirmar. |
| `solicitudAsignacion` | objeto o `null`. Solicitud de hacerse cargo de un equipo ajeno. Estructura interna por confirmar. |
| `versiones` | `{ so, antivirus, esetAgent, chrome }` (strings; `''` si no hay). Versiones detectadas de SO, antivirus, agente ESET y Chrome. |
| `equipo` | objeto (ver abajo). |
| `usuario` | `{ nombre, area, correo }` (strings). Usuario al que se asigna el equipo. |
| `updatedAt` | número (epoch ms, lo pone `upsertPrep`). |

`equipo` (dentro de `preparations`):

| Campo | Tipo / valor |
|---|---|
| `tipo` | string. Por confirmar los valores exactos (según código: Laptop / PC / …). |
| `marca`, `modelo`, `serie`, `inventario`, `hostname` | strings. |
| `cpu` | string. Procesador. |
| `ramGB`, `discoGB` | número o `''`. |
| `discoTipo` | string (`HDD` / `SSD` / `NVMe`, según el detector). |
| `ip`, `ipTipo` | strings. IP e indicación estática/dinámica. |
| `anydeskId`, `anydeskAlias` | strings. Número y alias de AnyDesk. |
| `redes` | array de `{ nombre, ip, ipTipo }`. Adaptadores cableado e inalámbrico. |
| `fotoSerie` | string (base64) o `null`. Foto del número de serie; **no viaja si pasa de ~700 KB** (`MAX_FOTO_CLOUD`). |

### Plantilla del checklist (local, no en Firestore)

La plantilla de puntos vive en cada teléfono (`defaultTemplate()` en
`www/index.html`, 24 entradas; 23 para equipo nuevo y 1 solo para
reasignados). Grupos: `hardware`, `software`, `datos`. Cada punto:
`{ id, group, text, options?, optional?, reassignOnly? }`. La plantilla
se actualiza sola al abrir la app (`templateVersion === 3`) y conserva
los puntos que el técnico agregó.

## `renta/{id}` — equipos de renta

Documento de `rentaToCloudDoc(rec)`:

| Campo | Tipo / valor |
|---|---|
| `id` | string. |
| `tipo` | `'Laptop'`, `'iPad'` o `'PC'`. |
| `modelo` | string. |
| `inventario` | string. Número de inventario de renta. |
| `capacidad` | string. Capacidad (iPad). |
| `cpu` | string. CPU (PC). |
| `accesorios` | objeto `{ [clave]: boolean }`. Claves por tipo: Laptop `mouse, cargador, maletin`; iPad `cargador, cable`; PC `cableCorriente, mouse, teclado, cableVideo, tarjetaVideo`. |
| `sinDanos` | boolean. |
| `danos` | string. Descripción de daños. |
| `obs` | string. Observaciones. |
| `fotoDanos` | string (base64) o `''`. Solo en Recibir renta; no viaja si pasa de 700 000 caracteres. |
| `danosIA` | string. Resultado de «Revisar daños con IA». |
| `estado` | `'recibido'` (Recibir renta), `'en formateo'` (Entrega Renta, según código), `'entregado'`. Otros estados por confirmar. |
| `flujo` | `'rec'` (Recibir renta) o `'for'` (Entrega Renta, según código — en el código aparece el literal `'for'`). |
| `entregados` | objeto (según código; estructura interna por confirmar). |
| `recibidoPor` | string. Analista que recibió el equipo. |
| `entregadoPor` | string. Analista que entregó el equipo. |
| `entregadoAt` | número o `null`. Se pone al entregar; manda para la regla de 15 días. |
| `creadoPor` | `{ uid, email }` o `null`. Quién registró el equipo. |
| `createdAt`, `updatedAt` | número (epoch ms). |

Regla de 15 días (`rentaEntregadoVisible` en `www/index.html`):
un equipo con `estado === 'entregado'` lo ve el usuario normal solo si
`Date.now() - (entregadoAt || createdAt) <= 15 * 86400000`; el admin lo
ve siempre.

## `mantenimientos/{id}` — órdenes de Mantenimientos Preventivos

Documento de `mantToCloudDoc(m)`:

| Campo | Tipo / valor |
|---|---|
| `id` | string. |
| `createdAt` | número (epoch ms). |
| `folio` | string de 5 dígitos (`'00001'…`) o `null` (borrador sin folio). Lo asigna `asignarFolio()` por transacción. |
| `estado` | `'borrador'` o `'firmada'` (según código; otros estados por confirmar). |
| `tecnicoUid` | string. UID del técnico dueño. |
| `tecnico` | string. Nombre del técnico. |
| `empresa` | `'Lapi'`, `'Ludi'` o `'Lapi Hemodiálisis'` (default `'Lapi'`). |
| `anio` | número. Año del caso (selector en el formulario). |
| `tipo` | string, default `'SOFTWARE/HARDWARE'`. |
| `area` | string. Área del usuario. |
| `responsable` | string. Responsable del equipo. |
| `tiempoReparacion`, `tiempoViaje`, `tiempoSistemaCaido` | strings. Default `'/'` en el formulario (según código). |
| `fechaServicio`, `fechaTermino` | strings (fechas). |
| `tituloCaso` | string. Default «Mantenimiento Preventivo sistemas» + año. |
| `tipoFalla` | string. Default `'/'` en el formulario (según código). |
| `identificacion` | `{ impresora, cpu, monitor, teclado, mouse, noBreak }` (booleans). Componentes identificados. |
| `descripcionEquipo` | string. Default: el hostname. |
| `condiciones` | `{ impresora, cpu, monitor, teclado, mouse, noBreak, notas }`. Condiciones encontradas. |
| `preventivo` | `{ impresora, cpu, monitor, teclado, mouse, noBreak }` (booleans). Revisión preventiva. |
| `descripcionCambios` | string. Default: texto estándar de mantenimiento preventivo. |
| `conclusion`, `comentarios` | strings. |
| `fechaPlaneacion`, `fechaCompromiso`, `periodoPrueba`, `fechaLiberacion` | strings (fechas; default `'/'` salvo la fecha de liberación, que sigue siendo campo de fecha). |
| `observaciones`, `observacionesDetectadas` | strings. |
| `whatsappUsuario` | string. Teléfono/WhatsApp del usuario para el enlace de firma. |
| `firmaTecnico` | string (data URL PNG del canvas) o `''`. No viaja si pasa de ~700 KB. |
| `firma` | objeto o `null`. Firma del usuario (ver abajo). |
| `updatedAt` | número (epoch ms). |

`equipo` (dentro de `mantenimientos`) — mismo shape que en
`preparations`, más:

| Campo extra | Tipo / valor |
|---|---|
| `impresora` | string. Primera impresora real (según el detector). |
| `antivirus` | string. |
| `politicas` | `{ cambioDias, minLongitud, bloqueoIntentos, bloqueoSegundos, bloqueoManual, cumpleCambio, cumpleLongitud, cumpleIntentos, cumpleBloqueo, cumple }`. Políticas de contraseña/bloqueo de Windows reportadas por el detector. |
| `politicasFuente` | string. Origen de las políticas (según código). |
| `usuarioSistemas` | boolean. Si existe cuenta/perfil Windows «sistemas». |
| `so` | string. Sistema operativo. |

`firma` (firma del usuario, la escribe `firma.html` / `guardarFirma`):

| Campo | Tipo / valor |
|---|---|
| `nombre` | string (obligatorio). |
| `area` | string (obligatorio). |
| `comentarios` | string (opcional). |
| `satisfaccion` | número 0–10 o `null` (0–3 INACEPTABLE, 4–7 ACEPTABLE, 8–10 EXCELENTE). |
| `firma` | string (data URL PNG del canvas, obligatorio). |
| `firmadoEn` | `serverTimestamp()`. |

Al guardar la firma, `estado` pasa a `'firmada'`.

## `detectados/{id}` — equipos detectados por el escritorio

Lo escribe el detector de escritorio con `reportDetected(info)`:

| Campo | Tipo / valor |
|---|---|
| `id` | string. `info.machineId` si viene; si no, la serie, y si no, `hostname + '-' + detectadoEn`. |
| `detectadoEn` | número (epoch ms, lo pone `reportDetected`). |
| `usado` | boolean. `false` en cada detección nueva; `true` cuando el teléfono lo usa (`markDetectadoUsado`). Volver a detectar un equipo usado lo trae de vuelta al panel. |
| resto | según código: los campos que reporte el detector (`hostname`, `serie`, `marca`, `modelo`, versiones, hardware, IPs, AnyDesk, políticas…). El shape exacto del detector vive en el repo `checklist-desktop`, no en este. |

La suscripción del teléfono trae los últimos 50 por `detectadoEn`
descendente.

## `presence/{uid}` — presencia

| Campo | Tipo / valor |
|---|---|
| `uid` | string. |
| `nombre` | string. |
| `rol` | `'admin'` o `'usuario'`. |
| `lastSeen` | `serverTimestamp()`. Latido cada 2 minutos con la app abierta. |

Cada usuario escribe solo su propio documento.

## `chat/{id}` — chat grupal (efímero 24 h)

| Campo | Tipo / valor |
|---|---|
| `uid` | string. UID del remitente. |
| `nombre` | string. Nombre visible del remitente. |
| `texto` | string, máximo 500 caracteres. |
| `createdAt` | `serverTimestamp()`. |

Se leen los últimos 50 en orden cronológico. `pruneChat()` borra los
de más de 24 h (chat y DM). El admin puede borrar cualquier mensaje;
un activo puede borrar mensajes de más de 24 h.

## `dm/{id}` — chat individual 1 a 1 (efímero 24 h)

| Campo | Tipo / valor |
|---|---|
| `participants` | array de 2 UID ordenados (`[uidA, uidB].sort()`). |
| `from` | string. UID del remitente. |
| `to` | string. UID del destinatario. |
| `nombre` | string. Nombre visible del remitente. |
| `texto` | string, máximo 500 caracteres. |
| `createdAt` | `serverTimestamp()`. |

Solo los dos participantes pueden leerlo (reglas). Sin historial:
igual que el grupal, se borra lo de más de 24 h.

## `config/admin` — flag de inicialización

| Campo | Tipo / valor |
|---|---|
| `initialized` | boolean `true` cuando ya existe el primer admin. |

Lectura pública; creación una sola vez por un usuario autenticado;
nunca se actualiza ni se borra (reglas).

## `config/folios` — contador de folios

| Campo | Tipo / valor |
|---|---|
| `siguiente` | int. Próximo folio a asignar; empieza en 1. La transacción `asignarFolio()` lo lee, devuelve el folio con 5 dígitos y lo sube en 1. |

Las reglas solo permiten subirlo de uno en uno y solo cambiar ese
campo.

## `config/ai` — claves de IA

| Campo | Tipo / valor |
|---|---|
| `key` | string. Clave de Gemini. |
| `deepseekKey` | string. Clave de DeepSeek. |

Lectura para activos; escritura solo admin; nunca se borra por reglas.
Ver `docs/SETUP_FIREBASE.md` § 7.

## `loginAttempts/{uid}` — intentos de acceso

| Campo | Tipo / valor |
|---|---|
| `count` | int. Intentos fallidos acumulados. |
| `locked` | boolean. `true` cuando `count >= 10` (`MAX_LOGIN_ATTEMPTS`). |
| `email` | string. Correo del intento. |
| `updatedAt` | número (epoch ms). |

Lectura y escritura públicas por reglas (el login revisa el bloqueo
sin sesión); solo el admin borra el documento (desbloquea).
El bloqueo aplica solo a usuarios normales, nunca al admin (lógica de
la app, no de las reglas).
