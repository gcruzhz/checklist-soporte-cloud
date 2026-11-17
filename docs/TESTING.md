# Testing — Checklist de Soporte (nube)

## Tests de regresión por versión (`tests/test20*.js`)

Cada versión tiene su propio archivo de test, nombrado por serie:

| Archivo | Serie que cubre |
|---|---|
| `tests/test2016.js` … `tests/test20213.js` | 2.0.16 … 2.1.3 |
| `tests/test20220.js` … `tests/test20227.js` | 2.2.0 … 2.2.7 |
| `tests/test20230.js` … `tests/test20240.js` | 2.3.0 … 2.4.0 |
| `tests/test20250.js` … `tests/test20256.js` | 2.5.0 … 2.5.6 |

### Cómo correrlos

```bash
cd ~/workspace/android/checklist-cloud
node tests/test20256.js
```

No hay framework ni `npm test` útil (el script `test` de
`package.json` es el placeholder por defecto y falla a propósito).
Es Node puro: `node tests/test20XX.js` y el proceso sale con código 0
si todo pasa.

### Qué cubren

Cada archivo acumula las series de su versión y las anteriores: cada
serie nueva agrega casos con letra (p. ej. en `test20256.js`: `256A`
orden completa ROBIT5 en 1 página carta, `256B` datos en COMENTARIOS,
`256C` fechas válidas sin «Invalid Date»; antes `255A–255G` selección
y Excel de Entrega Renta y regla de 15 días, `254D–254H` bloqueo de
Mantenimientos y firma en vivo, `253A–253F` orden de Entregados por
`deliveredAt` desc, `252A–252F` botón Detectar en Mantenimientos).

Resultado verificado de la serie actual (ejecutado 2026-11-17):

```
tests/test20256.js → 770 true / 0 false
```

### El harness

Cada archivo de test es autocontenido. La cabecera explica el
mecanismo:

- Lee el `<script>` extraído de la versión, p. ej.
  `tests/checklist20256.js` (el JavaScript de `www/index.html` de esa
  versión, guardado aparte), con `fs.readFileSync` y lo ejecuta con
  `eval(SRC)` (línea marcada `>>> EVAL`).
- **Antes** del `eval` se siembran los stubs: `localStorage`,
  `document`/`window`/`navigator`/`location` falsos (elementos con
  `classList`, `dataset`, `addEventListener`, `getContext()`…), un
  `Cloud` falso con las funciones que usa la app, `Blob`, y `alert` /
  `confirm` / `prompt` que **lanzan un error si se llaman** (desde
  2.4.0 la app ya no usa diálogos nativos; si alguno quedara, el test
  debe fallar en voz alta en vez de tragarlo con un stub silencioso).
- Para probar migraciones se puede sembrar `localStorage` **antes** de
  la línea `eval`.
- Cada caso imprime su resultado con `console.log('256A) …:', true/false)`.
- Al final, `process.exit(0)`.

Para la siguiente versión: copiar el archivo de test anterior, cambiar
`checklist20250.js` por el nuevo extraído (según la cabecera del
harness) y agregar la serie nueva.

En `tests/` quedan también los `.bak` (`checklist-2.x.html.bak`,
`firebase-2.x.js.bak`, `firma-2.5.0.html.bak`) y los scripts de parche
(`patch_*.py`, `patch_test_*.py`) usados para aplicar cada cambio.
Están en el `.gitignore` (`*.bak`) y no se versionan.

## Smoke de escritorio (repo `checklist-desktop`)

El programa de escritorio (Electron, repo aparte
`~/workspace/android/checklist-desktop/`) tiene sus propios smoke
tests en `scripts/smoke-*.js` (p. ej. `smoke-250-mant.js`,
`smoke-251-mant.js`, `smoke-252-mant.js`, `smoke-253-orden.js`,
`smoke-254-orden.js`, `smoke-255-orden.js` y `smoke-256-orden.js`.

Se corren con Electron bajo X virtual:

```bash
cd ~/workspace/android/checklist-desktop
xvfb-run -a ./node_modules/.bin/electron --no-sandbox scripts/smoke256-orden.js
```

Cada smoke abre la app de escritorio en Electron, simula el flujo
(detector, mantenimientos, orden en PDF) y termina con un veredicto
(`VEREDICTO OK` o el fallo). Los resultados de referencia están en el
changelog (`docs/CHANGELOG.md`): p. ej. 2.5.3 `smoke-253 VEREDICTO OK`,
2.5.1 `smoke-251 VEREDICTO OK`.
