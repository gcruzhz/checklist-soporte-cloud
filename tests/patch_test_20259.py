# Parche de pruebas 2.5.9: test20258.js -> test20259.js (ya copiado).
P = '/home/hatch/workspace/android/checklist-cloud/tests/test20259.js'
s = open(P, encoding='utf-8').read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'NO ENCONTRADO x%d (esperado %d): %r' % (c, n, old[:120])
    s = s.replace(old, new)

# --- SRC y versión 2.5.9 (orden: primero 2.5.8 -> 2.5.9, luego 2.5.7 -> 2.5.8).
rep("const SRC = fs.readFileSync(__dirname + '/checklist20258.js', 'utf8');",
    "const SRC = fs.readFileSync(__dirname + '/checklist20259.js', 'utf8');")
rep("html.includes('Versión 2.5.8')", "html.includes('Versión 2.5.9')", n=4)
rep("html.includes('Versión: 2.5.8')", "html.includes('Versión: 2.5.9')", n=2)
rep("html.includes('Versión 2.5.7')", "html.includes('Versión 2.5.8')", n=2)
rep("!html.includes('2.5.7')", "!html.includes('2.5.8')", n=3)
rep("(html.match(/2\\.5\\.8/g) || []).length", "(html.match(/2\\.5\\.9/g) || []).length")
rep("var n258 = ", "var n259 = ")
rep("n258 === 2", "n259 === 2", n=2)
rep("'AM0) versión 2.5.8:'", "'AM0) versión 2.5.9:'")
rep("'AP0) estáticos 2.5.8:", "'AP0) estáticos 2.5.9:")
rep("'AR0) versión 2.5.8 visible:'", "'AR0) versión 2.5.9 visible:'")
rep("'| 0 de 2.5.7:'", "'| 0 de 2.5.8:'", n=2)
rep("'| ocurrencias 2.5.8:'", "'| ocurrencias 2.5.9:'")
rep("'BA0) versión 2.5.8 sin 2.5.7:'", "'BA0) versión 2.5.9 sin 2.5.8:'")
rep("'BB0) 2.5.8 en 2 sitios:'", "'BB0) 2.5.9 en 2 sitios:'")
rep("html.indexOf('Soporte 258')", "html.indexOf('Soporte 259')", n=2)

# --- Serie 259 nueva, antes de process.exit(0).
serie259 = """
  // 259: serie nueva — compartir características de un equipo detectado
  // por WhatsApp y por correo (ambos paneles).
  // 259A: botones en las tarjetas de #detList y #mantDetList; el texto
  // incluye las características presentes y omite las vacías.
  function det259(over) { return Object.assign({ id: 'DET-SHARE', hostname: 'PC-SHARE', marca: 'Dell', modelo: 'Pro 14 PC14250', serie: '8TKKQJ4', tipo: 'Laptop', cpu: 'Intel Core Ultra 5 235U', ramGB: 16, discoGB: 512, discoTipo: 'NVMe', so: 'Windows 11 Pro 26H2', ip: '192.168.1.78', ipTipo: 'Dinámica', redes: [{ nombre: 'Wi-Fi', ip: '192.168.1.78', ipTipo: 'Dinámica' }, { nombre: 'Ethernet', ip: '192.168.1.10', ipTipo: 'Estática' }], anydeskId: '123456789', anydeskAlias: 'ROBIT5', usado: false, checks: { t18: true }, detalles: { impresora: 'HP LaserJet Pro', politicas: { cambioDias: 42, minLongitud: 0, bloqueoIntentos: 10, bloqueoSegundos: 300, bloqueoManual: false }, politicasFuente: 'directiva (secedit)', usuarioSistemas: true, escritorioRutas: ['C:\\\\Users\\\\Gerardo\\\\Desktop'], atajosVistos: 5, osFuente: 'registro' }, versiones: { so: 'Windows 11 Pro 26H2 (compilación 26300)', antivirus: 'ESET Security 13.1.2036.0', esetAgent: '13.3.1192.0', chrome: '157.0.8103.79' }, detectadoEn: Date.now() - 3600000, detectadoPor: 'Gerardo' }, over || {}); }
  detectados = [det259()];
  renderDetectados();
  var html259det = document.getElementById('detList').innerHTML;
  var a259detBtns = html259det.indexOf('data-det-wa="DET-SHARE"') !== -1 && html259det.indexOf('data-det-mail="DET-SHARE"') !== -1 && html259det.indexOf('Compartir por WhatsApp') !== -1 && html259det.indexOf('Compartir por correo') !== -1 && html259det.indexOf('data-det-use="DET-SHARE"') !== -1 && html259det.indexOf('data-det-save="DET-SHARE"') !== -1 && html259det.indexOf('data-det-del="DET-SHARE"') !== -1;
  renderMantDetectados();
  var html259mant = document.getElementById('mantDetList').innerHTML;
  var a259mantBtns = html259mant.indexOf('data-mant-det-wa="DET-SHARE"') !== -1 && html259mant.indexOf('data-mant-det-mail="DET-SHARE"') !== -1 && html259mant.indexOf('Compartir por WhatsApp') !== -1 && html259mant.indexOf('Compartir por correo') !== -1 && html259mant.indexOf('data-mant-det-use="DET-SHARE"') !== -1;
  var txt259 = detShareText(detectados[0]);
  var a259txt = txt259.indexOf('Dell Pro 14 PC14250') !== -1 && txt259.indexOf('Serie: 8TKKQJ4') !== -1 && txt259.indexOf('Hostname: PC-SHARE') !== -1 && txt259.indexOf('Procesador: Intel Core Ultra 5 235U') !== -1 && txt259.indexOf('RAM: 16 GB') !== -1 && txt259.indexOf('Disco: 512 GB NVMe') !== -1 && txt259.indexOf('IP: 192.168.1.78 (Dinámica)') !== -1 && txt259.indexOf('Wi-Fi: 192.168.1.78 (Dinámica)') !== -1 && txt259.indexOf('AnyDesk: 123 456 789 (ROBIT5)') !== -1 && txt259.indexOf('ESET Security 13.1.2036.0') !== -1 && txt259.indexOf('Agente ESET: 13.3.1192.0') !== -1 && txt259.indexOf('Chrome: 157.0.8103.79') !== -1 && txt259.indexOf('Impresora: HP LaserJet Pro') !== -1 && txt259.indexOf('Políticas:') !== -1 && txt259.indexOf('cambio cada 42 días') !== -1 && txt259.indexOf('Usuario de sistemas: Sí') !== -1 && txt259.indexOf('por Gerardo') !== -1 && (txt259.match(/Detectado:/g) || []).length === 2;
  var txt259min = detShareText({ id: 'MIN', hostname: '', marca: '', modelo: '', serie: '', usado: false });
  var a259min = txt259min.indexOf('Serie:') === -1 && txt259min.indexOf('Hostname:') === -1 && txt259min.indexOf('Procesador:') === -1 && txt259min.indexOf('AnyDesk:') === -1 && txt259min.indexOf('Políticas:') === -1 && txt259min.indexOf('Impresora:') === -1 && txt259min.indexOf('Usuario de sistemas:') === -1 && txt259min.indexOf('sin datos') === -1 && txt259min.indexOf('Equipo detectado') !== -1;
  console.log('259A) botones en #detList:', a259detBtns, '| botones en #mantDetList:', a259mantBtns, '| texto con características:', a259txt, '| mínimo omite vacíos:', a259min);
  // 259B: clic en WhatsApp abre wa.me con el texto (ambos paneles); el
  // equipo sigue sin usar y no se llama a Cloud; id inexistente no abre nada.
  var opened259 = [];
  global.open = function (u) { opened259.push(String(u)); return null; };
  var cloud259 = [];
  global.Cloud.upsertPrep = async function (d) { cloud259.push(['upsertPrep']); };
  global.Cloud.markDetectadoUsado = async function () { cloud259.push(['markUsado']); };
  global.Cloud.deleteDetectado = async function () { cloud259.push(['deleteDetectado']); };
  function clickDet259(sel, id) {
    document.getElementById('detList')._h.click[0]({ target: { closest: function (s) { return s === sel ? { getAttribute: function () { return id; } } : null; } } });
  }
  function clickMant259(sel, id) {
    document.getElementById('mantDetList')._h.click[0]({ target: { closest: function (s) { return s === sel ? { getAttribute: function () { return id; } } : null; } } });
  }
  detectados = [det259()];
  opened259.length = 0;
  clickDet259('[data-det-wa]', 'DET-SHARE');
  var wa259txt = opened259.length === 1 && opened259[0].indexOf('https://wa.me/?text=') === 0 ? decodeURIComponent(opened259[0].split('text=')[1]) : '';
  var b259wa = opened259.length === 1 && wa259txt.indexOf('PC-SHARE') !== -1 && wa259txt.indexOf('8TKKQJ4') !== -1 && wa259txt.indexOf('ESET Security 13.1.2036.0') !== -1;
  var b259sigue = detectados[0].usado === false && detectados.length === 1 && cloud259.length === 0;
  opened259.length = 0;
  clickMant259('[data-mant-det-wa]', 'DET-SHARE');
  var b259mantWa = opened259.length === 1 && opened259[0].indexOf('https://wa.me/?text=') === 0 && decodeURIComponent(opened259[0].split('text=')[1]).indexOf('PC-SHARE') !== -1 && detectados[0].usado === false && cloud259.length === 0;
  opened259.length = 0;
  clickDet259('[data-det-wa]', 'NO-EXISTE');
  var b259nada = opened259.length === 0;
  console.log('259B) WhatsApp #detList abre wa.me con texto:', b259wa, '| sigue sin usar y sin Cloud:', b259sigue, '| WhatsApp #mantDetList:', b259mantWa, '| id inexistente no abre nada:', b259nada);
  // 259C: correo abre mailto con asunto (hostname o modelo) y el mismo
  // texto en el cuerpo; el equipo sigue sin usar.
  global.location.href = '';
  clickDet259('[data-det-mail]', 'DET-SHARE');
  var mail259 = global.location.href;
  var c259mail = mail259.indexOf('mailto:?subject=') === 0 && decodeURIComponent(mail259.split('subject=')[1].split('&body=')[0]) === 'Equipo detectado: PC-SHARE' && decodeURIComponent(mail259.split('&body=')[1]).indexOf('PC-SHARE') !== -1 && decodeURIComponent(mail259.split('&body=')[1]).indexOf('Políticas:') !== -1 && detectados[0].usado === false && cloud259.length === 0;
  global.location.href = '';
  clickMant259('[data-mant-det-mail]', 'DET-SHARE');
  var c259mantMail = global.location.href.indexOf('mailto:?subject=') === 0 && decodeURIComponent(global.location.href.split('subject=')[1].split('&body=')[0]) === 'Equipo detectado: PC-SHARE';
  detectados = [det259({ hostname: '', modelo: 'Pro 14' })];
  global.location.href = '';
  clickDet259('[data-det-mail]', 'DET-SHARE');
  var c259asunto = decodeURIComponent(global.location.href.split('subject=')[1].split('&body=')[0]) === 'Equipo detectado: Pro 14';
  console.log('259C) correo #detList asunto+cuerpo:', c259mail, '| correo #mantDetList:', c259mantMail, '| asunto usa modelo sin hostname:', c259asunto);
  // 259D: compartir no guarda nada en localStorage; mailto 259; botones
  // y funciones presentes en el código.
  var ls259 = JSON.stringify(global.localStorage._d);
  var d259noguarda = ls259.indexOf('PC-SHARE') === -1 && ls259.indexOf('8TKKQJ4') === -1 && ls259.indexOf('ESET Security') === -1;
  var d259mailto = html.indexOf('Soporte 259') !== -1;
  var d259src = SRC.indexOf('data-det-wa') !== -1 && SRC.indexOf('data-det-mail') !== -1 && SRC.indexOf('data-mant-det-wa') !== -1 && SRC.indexOf('data-mant-det-mail') !== -1 && SRC.indexOf('function detShareText') !== -1 && SRC.indexOf('function detShareMail') !== -1;
  console.log('259D) nada guardado en localStorage:', d259noguarda, '| mailto 259:', d259mailto, '| botones y funciones en el código:', d259src);
"""
rep("""  console.log('258D) sin Desktop buscar avisa sin llamar:', d258buscar, '| instalar avisa sin llamar:', d258instalar, '| nada guardado en localStorage:', d258noguarda, '| mailto 258:', d258mailto);

  process.exit(0);""",
"""  console.log('258D) sin Desktop buscar avisa sin llamar:', d258buscar, '| instalar avisa sin llamar:', d258instalar, '| nada guardado en localStorage:', d258noguarda, '| mailto 258:', d258mailto);
""" + serie259 + """
  process.exit(0);""")

open(P, 'w', encoding='utf-8').write(s)
print('OK test20259.js, bytes:', len(s))
print('259 refs:', s.count('259'), '| 258 refs:', s.count('258'))
