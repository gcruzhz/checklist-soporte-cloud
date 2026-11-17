# Parche 2.5.0c: www/index.html — CSS, tabs (Inicio + Mantenimientos),
# vista #viewInicio (selector de 4 secciones) y vista #viewMant completa.
import io

P = '/home/hatch/workspace/android/checklist-cloud/www/index.html'
s = io.open(P, encoding='utf-8').read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'NO ENCONTRADO o repetido (%d): %r' % (c, old[:100])
    s = s.replace(old, new)

# 1. CSS: cuadro destacado de serie/hostname/modelo, canvas de firma, línea de ids.
rep("""  .empty { text-align: center; color: #888; padding: 26px 10px; }""",
"""  .empty { text-align: center; color: #888; padding: 26px 10px; }
  .mant-hero { border: 2px solid #73BA25; border-radius: 12px; padding: 10px; margin-bottom: 10px; background: #f4faf0; }
  .mant-hero .field label { font-weight: 700; color: #0C322C; }
  .sig-canvas { width: 100%; height: 140px; border: 1px solid #ccc; border-radius: 8px; background: #fff; touch-action: none; }
  .mant-id-line { font-weight: 700; font-size: 14px; color: #0C322C; margin-bottom: 6px; }""")

# 2. Tabs: Inicio primero, Mantenimientos tras Entrega Renta.
rep("""  <div class="tabs" id="tabs">
    <button class="tab on" data-v="preparar">🖥️ Por preparar</button>
    <button class="tab" data-v="rec">📥 Recibir renta</button>
    <button class="tab" data-v="for">📦 Entrega Renta</button>""",
"""  <div class="tabs" id="tabs">
    <button class="tab" data-v="inicio">🏠 Inicio</button>
    <button class="tab on" data-v="preparar">🖥️ Por preparar</button>
    <button class="tab" data-v="rec">📥 Recibir renta</button>
    <button class="tab" data-v="for">📦 Entrega Renta</button>
    <button class="tab" data-v="mant">🔧 Mantenimientos</button>""")

# 3. Vista Inicio antes de viewPreparar.
rep("""  <div id="viewPreparar">""",
"""  <div id="viewInicio" hidden>
    <div class="card">
      <b>¿Qué quieres hacer?</b>
      <div class="share-note">Elige una sección para empezar. Se pregunta cada vez que abres la app.</div>
    </div>
    <div class="menu-btns">
      <button class="menu-btn green" id="btnGoPreparar"><span class="ic">🖥️</span><span>Por preparar<small>equipos por preparar</small></span></button>
      <button class="menu-btn dark" id="btnGoRec"><span class="ic">📥</span><span>Recibir renta<small>revisar equipos que llegan</small></span></button>
      <button class="menu-btn dark" id="btnGoFor"><span class="ic">📦</span><span>Entrega Renta<small>entregar equipos de renta</small></span></button>
      <button class="menu-btn green" id="btnGoMant"><span class="ic">🔧</span><span>Mantenimientos Preventivos<small>órdenes de servicio con folio</small></span></button>
    </div>
  </div>
  <div id="viewPreparar">""")

# 4. Vista Mantenimientos antes de viewUsuarios.
rep("""  <div id="viewUsuarios" hidden>""",
"""  <div id="viewMant" hidden>
    <div class="card">
      <b>Mantenimientos Preventivos</b>
      <div class="share-note">Órdenes de servicio con folio: crea el mantenimiento, genera la orden y el usuario la firma desde su teléfono con el link que le llega por WhatsApp.</div>
    </div>
    <div class="row" id="mantAdminRow" hidden>
      <select id="mantAdminFilter" style="flex:1"><option value="todos">Todos los usuarios</option></select>
    </div>
    <div class="menu-btns">
      <button class="menu-btn green" id="btnMantNuevo"><span class="ic">🔧</span><span>Nuevo mantenimiento<small>orden de servicio</small></span></button>
      <button class="menu-btn dark" id="btnMantDet"><span class="ic">🖥️</span><span>Equipos detectados<small>usar un equipo de la red</small></span></button>
    </div>
    <div class="panel" id="mantDetBox" hidden>
      <b>🖥️ Equipos detectados</b>
      <div class="share-note">Toca «Usar este equipo» para llenar el mantenimiento con los datos detectados del equipo (serie, hostname, modelo, software, IPs, AnyDesk y políticas).</div>
      <div id="mantDetList"></div>
    </div>
    <div id="mantList"></div>

    <div class="panel" id="mantFormBox" hidden>
      <b id="mantFormTitle">Nuevo mantenimiento</b>
      <div class="mant-hero">
        <div class="share-note">Datos del equipo (obligatorios para crear la orden; se pueden corregir a mano):</div>
        <div class="grid2">
          <div class="field"><label>No. de serie *</label><input id="fM-serie" placeholder="Serie del equipo"></div>
          <div class="field"><label>Hostname *</label><input id="fM-hostname" placeholder="Nombre del equipo en la red"></div>
          <div class="field full"><label>Modelo *</label><input id="fM-modelo" placeholder="ProBook 440, ThinkPad..."></div>
        </div>
      </div>
      <div class="grid2">
        <div class="field"><label>Nombre de quien presta el servicio *</label><input id="fM-tecnico" placeholder="Quien hace el mantenimiento"></div>
        <div class="field"><label>Tipo de mantenimiento *</label><select id="fM-tipo"><option value="SOFTWARE">SOFTWARE</option><option value="HARDWARE">HARDWARE</option></select></div>
        <div class="field"><label>Área *</label><input id="fM-area" placeholder="Área del equipo"></div>
        <div class="field"><label>Responsable *</label><input id="fM-responsable" placeholder="Responsable del equipo"></div>
        <div class="field"><label>Tiempo de reparación</label><input id="fM-tRep" placeholder="Ej. 2 horas"></div>
        <div class="field"><label>Tiempo de viaje</label><input id="fM-tViaje" placeholder="Ej. 30 min"></div>
        <div class="field"><label>Tiempo de sistema caído</label><input id="fM-tCaido" placeholder="Ej. 1 hora"></div>
        <div class="field"><label>Fecha del servicio *</label><input id="fM-fechaServ" type="date"></div>
        <div class="field"><label>Fecha de término</label><input id="fM-fechaTerm" type="date"></div>
        <div class="field full"><label>Título del caso *</label><input id="fM-titulo" placeholder="Título del caso"></div>
        <div class="field full"><label>Tipo de falla *</label><input id="fM-tipoFalla" placeholder="Tipo de falla"></div>
        <div class="field full"><label>Identificación del equipo</label><div class="accs" id="accs-mant-id"></div></div>
        <div class="field full"><label>Descripción del equipo *</label><textarea id="fM-descEquipo" rows="2" placeholder="Descripción del equipo"></textarea></div>
        <div class="field full"><label>Condiciones del equipo</label><div class="accs" id="accs-mant-cond"></div></div>
        <div class="field full"><label>Notas de condiciones</label><input id="fM-condNotas" placeholder="Notas sobre las condiciones..."></div>
        <div class="field full"><label>Mantenimiento preventivo realizado</label><div class="accs" id="accs-mant-prev"></div></div>
        <div class="field full"><label>Descripción de cambios</label><textarea id="fM-descCambios" rows="2" placeholder="Cambios realizados..."></textarea></div>
        <div class="field full"><label>Conclusión</label><textarea id="fM-conclusion" rows="2" placeholder="Conclusión..."></textarea></div>
        <div class="field full"><label>Comentarios</label><textarea id="fM-comentarios" rows="2" placeholder="Comentarios..."></textarea></div>
        <div class="field"><label>Fecha de planeación</label><input id="fM-fechaPlan" type="date"></div>
        <div class="field"><label>Fecha compromiso de instalación</label><input id="fM-fechaComp" type="date"></div>
        <div class="field"><label>Periodo de prueba</label><input id="fM-periodoPrueba" placeholder="Ej. 5 días"></div>
        <div class="field"><label>Fecha de liberación</label><input id="fM-fechaLib" type="date"></div>
        <div class="field full"><label>Observaciones (texto libre del técnico)</label><textarea id="fM-observaciones" rows="2" placeholder="Observaciones..."></textarea></div>
        <div class="field full"><label>Observaciones detectadas (se generan solas con un equipo detectado)</label><textarea id="fM-obsDet" rows="3" readonly placeholder="Sin datos detectados"></textarea></div>
        <div class="field full"><label>WhatsApp del usuario *</label><input id="fM-whatsapp" type="tel" placeholder="10 dígitos, ej. 5512345678"></div>
      </div>
      <b>Datos del equipo (detectados)</b>
      <div class="grid2">
        <div class="field"><label>Tipo de equipo</label><select id="fM-eq-tipo"><option>Laptop</option><option>Desktop</option><option>All in One</option><option>Tablet</option><option>Otro</option></select></div>
        <div class="field"><label>Marca</label><input id="fM-eq-marca" placeholder="HP, Lenovo, Dell..."></div>
        <div class="field"><label>Procesador</label><input id="fM-eq-cpu" placeholder="Intel i5..."></div>
        <div class="field"><label>RAM (GB)</label><input id="fM-eq-ram" type="number" placeholder="16"></div>
        <div class="field"><label>Disco (GB)</label><input id="fM-eq-disco" type="number" placeholder="512"></div>
        <div class="field"><label>Tipo de disco</label><input id="fM-eq-discoTipo" placeholder="SSD, HDD, NVMe"></div>
        <div class="field"><label>IP</label><input id="fM-eq-ip" placeholder="192.168.1.45"></div>
        <div class="field"><label>Redes</label><input id="fM-eq-redes" placeholder="Wi-Fi: 192.168.1.45 (Dinámica)"></div>
        <div class="field"><label>Impresora</label><input id="fM-eq-impresora" placeholder="Impresora detectada"></div>
        <div class="field"><label>AnyDesk (ID)</label><input id="fM-eq-anydesk" placeholder="123456789"></div>
        <div class="field"><label>AnyDesk (alias)</label><input id="fM-eq-anydeskAlias" placeholder="Alias"></div>
        <div class="field"><label>Antivirus</label><input id="fM-eq-antivirus" placeholder="ESET NOD32..."></div>
        <div class="field"><label>Sistema operativo</label><input id="fM-eq-so" placeholder="Windows 11 Pro..."></div>
        <div class="field"><label><input type="checkbox" id="fM-eq-usuarioSistemas" style="width:auto"> Usuario de sistemas</label></div>
        <div class="field"><label>Cambio de contraseña (días)</label><input id="fM-pol-cambio" type="number" placeholder="90"></div>
        <div class="field"><label>Longitud mínima (caracteres)</label><input id="fM-pol-long" type="number" placeholder="10"></div>
        <div class="field"><label>Bloqueo (intentos)</label><input id="fM-pol-intentos" type="number" placeholder="5"></div>
        <div class="field"><label>Bloqueo (segundos)</label><input id="fM-pol-bloqueo" type="number" placeholder="350"></div>
        <div class="field full"><div class="share-note" id="mantPolLine">Políticas: sin datos.</div></div>
      </div>
      <b>Firma del técnico *</b>
      <div class="share-note">Firma con el dedo o el ratón en el recuadro.</div>
      <canvas class="sig-canvas" id="fM-firmaCanvas" width="320" height="140"></canvas>
      <div class="actions"><button class="btn-ghost" id="btnMantFirmaLimpiar" type="button">Limpiar firma</button></div>
      <div class="actions">
        <button class="btn-green" id="btnMantCrear">📄 Crear orden de servicio</button>
        <button class="btn-dark" id="btnMantGuardar">💾 Guardar</button>
        <button class="btn-ghost" id="btnMantCancelar">✕ Cancelar</button>
      </div>
      <p class="save-hint" id="mantSaveHint">«Crear orden de servicio» asigna el folio y ya no se puede editar como borrador. «Guardar» lo deja como borrador sin folio para seguirlo después.</p>
    </div>

    <div class="panel" id="mantOrderBox" hidden>
      <div id="mantOrderBody"></div>
      <div class="actions">
        <button class="btn-green" id="btnMantWaLink">💬 Enviar formulario por WhatsApp</button>
        <button class="btn-dark" id="btnMantPdf">📄 Generar PDF</button>
        <button class="btn-dark" id="btnMantCompartir">📤 Compartir copia con el usuario</button>
        <button class="btn-ghost" id="btnMantVolver">← Volver a la lista</button>
      </div>
      <div class="actions"><button class="btn-danger" id="btnMantCancelarOrden">Cancelar orden</button></div>
      <div class="share-note" id="mantOrderNote"></div>
    </div>
  </div>
  <div id="viewUsuarios" hidden>""")

io.open(P, 'w', encoding='utf-8').write(s)
print('HTML 2.5.0c OK')
