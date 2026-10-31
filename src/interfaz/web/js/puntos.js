/* Pestana Kpoints: tablero de kpoints, angulos y proporciones de la definicion. API: /api/puntos/* */
// UN solo grafico con los 33 puntos del cuerpo (MediaPipe Pose).
let ptCatalogoPose=null, ptTipos=null, ptActual=null, ptReglas=[];
let ptFeatures=[], ptKpoints=[], ptCadena=[];
let ptResaltar=null;                                   // nombre base de la fila marcada en la matriz (banda plateada)
let ptModo='marcar';                                   // 'marcar' = elegir kpoints | 'recorrido' = armar una fila
let ptPresets=[];
let ptEditando=null;                                    // nombre base de la fila que se esta editando EN SU LUGAR (null = ninguna)
let ptNombre='';                                        // nombre base de la fila libre (la ultima de la matriz)
const PT_COLORES={cabeza:'#b39ddb', brazos:'#ffa726', manos:'#ffd54f', torso:'#8bc34a',
                   cadera:'#ff9e80', piernas:'#64b5f6', pies:'#f06292'};
const PT_PLATA='#dfe4ee';
const PT_MORADO='#a67cff';   // borde de los kpoints marcados

async function cargarCatalogosPuntos(){
  if(!ptTipos) ptTipos = await (await fetch('/api/puntos/tipos')).json();
  if(!ptCatalogoPose) ptCatalogoPose = await (await fetch('/api/puntos/catalogo?source=pose')).json();
}

async function cargarListaEjercicios(){
  const ejercicios = await (await fetch('/api/puntos/ejercicios')).json();
  $F('#ptEjercicio').innerHTML = ejercicios.length ? ejercicios.map(e=>`<option value="${e}">${e}</option>`).join('')
    : '<option value="">— no hay ejercicios en ejercicios/ —</option>';
  if(ejercicios.includes('zancada')) $F('#ptEjercicio').value='zancada';   // zancada por defecto
  if(ejercicios.length) await cargarEjercicioPuntos();
}

let ptSnapshot='';
const _estadoEditor = () => JSON.stringify([ptKpoints, ptFeatures]);
const ptConCambios = () => ptSnapshot !== '' && ptSnapshot !== _estadoEditor();   // hay algo editado sin guardar

async function crearEjercicioPuntos(){
  const campo = $F('#ptNuevoNombre');
  const nombre = campo.value.trim();
  if(!nombre) return;
  const r = await fetch('/api/puntos/crear',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({nombre})});
  const j = await r.json();
  if(!r.ok) return msg('Error: '+j.error);
  campo.value='';
  await cargarListaEjercicios();
  $F('#ptEjercicio').value = nombre;
  await cargarEjercicioPuntos();
  msg(j.sql && j.sql.ok ? `Ejercicio '${nombre}' creado y conectado a SQL (type ${j.sql.type})`
                        : `Ejercicio '${nombre}' creado. SQL sin conexion: se sube solo cuando vuelva`);
}

async function eliminarEjercicioPuntos(){
  const nombre = $F('#ptEjercicio').value;
  if(!nombre) return;
  if(!confirm(`Eliminar el ejercicio '${nombre}' de la app?\nEl ejercicio queda inactivo (se recupera creandolo de nuevo con el mismo nombre); clips, grabaciones y SQL no se tocan.`)) return;
  const r = await fetch('/api/puntos/eliminar',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({nombre})});
  const j = await r.json();
  if(!r.ok) return msg('Error: '+j.error);
  ptActual=null; ptSnapshot='';
  await cargarListaEjercicios();
  msg(`Ejercicio '${nombre}' eliminado (copia: ejercicios/.respaldos/${j.respaldo})`);
}

async function cargarEjercicioPuntos(sincronizar=true){
  const ejercicio = $F('#ptEjercicio').value;
  if(!ejercicio) return;
  ptActual = await (await fetch('/api/puntos/definicion?ejercicio='+encodeURIComponent(ejercicio))).json();
  ptFeatures = (ptActual.features||[]).map(f=>({...f, points:[...(f.points||[])], reference:[...(f.reference||[])]}));
  ptKpoints = (ptActual.kpoints||[]).map(k=>({...k, origen:{...k.origen}}));
  ptModo='marcar'; ptCadena=[]; ptResaltar=null; ptNombre=''; ptEditando=null;
  ptReglas = (ptActual.reglas||[]).map(r=>({...r}));
  ordenarKpoints();
  ordenarFeatures();
  ptSnapshot = _estadoEditor();
  renderTodoPuntos();
  renderReglas();
  renderNormalizacion();
  if(sincronizar) refrescarEstadoSql();
}

function renderTodoPuntos(){
  renderCapas(); renderDiagrama(); renderTablaKpoints(); renderTablaFeaturesPuntos(); renderAngulosConocidos();
}

// ---------------------------------------------------------------- modo
function cambiarModo(m){
  ptModo = m;
  if(m==='marcar'){ ptCadena=[]; ptEditando=null; }
  renderTodoPuntos();
}

function renderCapas(){
  const n = ptKpoints.filter(k=>k.origen.tipo==='landmark').length;
  const pon = (id, on, txt) => { const b=$F('#'+id); b.className = 'mchk'+(on?' on':''); if(txt) b.textContent=txt; };
  pon('capaPose', true, `Cuerpo 33 · ${n}`);
  pon('modoMarcar', ptModo==='marcar');
  pon('modoRecorrido', ptModo==='recorrido');
  $F('#kpModelos').textContent = 'Modelo que corre: Pose';
  $F('#kpAyuda').textContent = ptModo==='marcar'
    ? 'Clic en un punto: lo marca o lo quita del catalogo.'
    : 'Clic en los puntos del recorrido, en orden, minimo 3 (esten marcados o no). Los kpoints marcados llevan borde morado. Al agregar la fila, o al activar su ∠ o %, los que no estaban marcados se marcan solos.';
}

// ---------------------------------------------------------------- geometria del grafico unico
function _geometria(){
  const pts=[], mapa={}, huesos=[];
  ptCatalogoPose.puntos.forEach(p=>{
    mapa['pose|'+p.nombre] = [p.x, p.y];
    pts.push({fuente:'pose', nombre:p.nombre, x:p.x, y:p.y, grupo:p.grupo});
  });
  ptCatalogoPose.esqueleto.forEach(([a,b])=>huesos.push([mapa['pose|'+a], mapa['pose|'+b]]));
  return {pts, mapa, ocultos:new Set(), huesos};
}

// filtro de brillo neon (se re-declara en cada render: el <svg> se reemplaza entero)
const SVG_FILTRO_NEON = `<defs><filter id="neon" x="-80%" y="-80%" width="260%" height="260%">
  <feGaussianBlur stdDeviation="0.9" result="b"/>
  <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter></defs>`;

// --- kpoints del catalogo <-> puntos del grafico
const _kpDe = (fuente, landmark) => ptKpoints.find(k=>k.origen.tipo==='landmark' && k.origen.fuente===fuente && k.origen.landmark===landmark);
const _claveClic = p => ({fuente:p.fuente, landmark:p.nombre});
function _kpDePunto(p){
  const c = _claveClic(p);
  return _kpDe(c.fuente, c.landmark) || null;
}
function _coordKp(kp, g){
  if(kp.origen.tipo==='landmark'){
    if(kp.origen.fuente==='pose' && g.ocultos.has(kp.origen.landmark)) return null;
    return g.mapa[kp.origen.fuente+'|'+kp.origen.landmark] || null;
  }
  const [a,b] = kp.origen.de.map(n=>ptKpoints.find(k=>k.numero===n));
  const pa=a&&_coordKp(a,g), pb=b&&_coordKp(b,g);
  return pa&&pb ? [(pa[0]+pb[0])/2, (pa[1]+pb[1])/2] : null;
}

// recorrido a resaltar: el que se esta armando o, si no hay, la fila marcada en la matriz
function _recorridoActivo(){
  if(ptCadena.length) return ptCadena;
  const fila = ptResaltar && _filasFeatures().find(f=>f.base===ptResaltar);
  return fila ? fila.cadena : [];
}

function _coordNombre(nombre, g){
  const i = _info(nombre);
  if(i) return g.mapa[i.fuente+'|'+i.landmark] || null;
  const kp = ptKpoints.find(k=>k.nombre===nombre);
  return kp ? _coordKp(kp, g) : null;
}
const _grupoNombre = nombre => {
  const i = _info(nombre);
  if(i){ const q = _catDe(i.fuente).puntos.find(x=>x.nombre===i.landmark); return q ? q.grupo : null; }
  const kp = ptKpoints.find(k=>k.nombre===nombre);
  return kp ? _posicionKp(kp, {}).grupo : null;
};
// nombres con los que un punto del grafico puede estar en un recorrido (kpoint marcado o pendiente)
function _nombresPunto(p){
  const c = _claveClic(p), kp = _kpDePunto(p);
  return [kp && kp.nombre, _pend(c.fuente, c.landmark)].filter(Boolean);
}

function renderDiagrama(){
  if(!ptActual || !ptCatalogoPose) return;
  const g = _geometria();
  // fondo: el mismo esqueleto del video (lo dibuja el servidor con sesion/overlay.py)
  const figura = `<image href="/api/puntos/figura.png" x="-22" y="-32" width="144" height="138" style="pointer-events:none"/>`;

  // banda plateada pastel DEBAJO de los puntos: la parte del cuerpo que arma el recorrido (este o no marcado cada punto)
  const activo = _recorridoActivo();
  const rec = activo.map(n=>_coordNombre(n,g)).filter(Boolean);
  const banda = rec.length ? `<polyline points="${rec.map(c=>`${c[0]*100},${(1-c[1])*100}`).join(' ')}" fill="none" stroke="${PT_PLATA}" stroke-width="4.6" stroke-linecap="round" stroke-linejoin="round" opacity=".55" style="pointer-events:none"/>`
    + rec.map(c=>`<circle cx="${c[0]*100}" cy="${(1-c[1])*100}" r="3.4" fill="${PT_PLATA}" opacity=".55" style="pointer-events:none"/>`).join('') : '';

  const puntos = g.pts.map((p,i)=>{
    const cx=p.x*100, cy=(1-p.y)*100;
    const kp=_kpDePunto(p), on=!!kp;
    const color = PT_COLORES[p.grupo] || '#8b93a3';
    const nombres = _nombresPunto(p);
    const iC = Math.max(...nombres.map(n=>ptCadena.indexOf(n)));      // lugar en el recorrido que se esta armando (-1 = no esta)
    const enRecorrido = !on && iC>=0;                                     // en el recorrido que se esta armando
    const r = on || enRecorrido ? 1.9 : 1.4;
    const fondo = on ? color : '#101216', anillo = on ? PT_MORADO : enRecorrido ? '#fff' : color;   // borde morado = kpoint marcado
    const cod = _codigoDe(p.fuente, p.nombre);
    const etiqueta = (on ? _kEtq(kp.nombre) : cod) + (iC>=0 ? '·'+(iC+1) : '');
    const id = ptCatalogoPose.puntos.findIndex(q=>q.nombre===p.nombre);
    return `<circle data-i="${i}" cx="${cx}" cy="${cy}" r="${r}" fill="${fondo}" stroke="${anillo}" stroke-width="${on?0.6:enRecorrido?0.35:0.3}" ${on?'filter="url(#neon)"':''} style="cursor:pointer"><title>${cod} ${_descLandmark(p.fuente,p.nombre)} (${p.fuente}, id ${id})${on?' — marcado':''}</title></circle>`
      + `<text x="${cx}" y="${cy-2.6}" font-size="2.5" fill="${(on||enRecorrido)?'#fff':'#9aa3b2'}" font-weight="${on||enRecorrido?700:400}" text-anchor="middle" style="pointer-events:none">${etiqueta}</text>`;
  }).join('');

  $F('#kpSvg').innerHTML = SVG_FILTRO_NEON + figura + banda + puntos;
  $F('#kpSvg').querySelectorAll('circle[data-i]').forEach(c=>c.addEventListener('click', ()=>clicDiagrama(g.pts[+c.dataset.i])));

  const grupos = [...new Set(activo.map(_grupoNombre).filter(Boolean))];
  $F('#ptZona').textContent = grupos.length ? 'Zona del recorrido: ' + grupos.join(' · ') : '';
}

function clicDiagrama(p){
  if(ptModo==='recorrido'){
    // cualquier punto sirve, este marcado o no: los no marcados quedan pendientes (morado) hasta que se marquen
    const nombres = _nombresPunto(p), i = ptCadena.findIndex(n=>nombres.includes(n));
    if(i>=0) ptCadena.splice(i,1); else ptCadena.push(nombres[0]);
  } else {
    const c=_claveClic(p), existe=_kpDePunto(p);
    if(existe) quitarKpoint(existe);
    else agregarKpoint(c.fuente, c.landmark);
  }
  renderTodoPuntos();
}

function agregarKpoint(fuente, landmark){
  let kp=_kpDe(fuente, landmark);
  if(!kp){
    const numero=_siguienteNumeroKp();
    kp={numero, nombre:_nombreKpAuto(landmark, fuente, numero), origen:{tipo:'landmark', fuente, landmark}};
    ptKpoints.push(kp);
    ordenarKpoints();
    _renombrarPuntos(_pend(fuente, landmark), kp.nombre);            // las filas que lo esperaban dejan de estar pendientes
  }
  return kp;
}

// Marca en el catalogo los puntos de estas cadenas que aun no lo estan (nombres '~...' o crudos de MediaPipe).
// Devuelve los codigos marcados.
function _marcarPendientes(cadenas){
  const agregados = [];
  [...new Set(cadenas.flat())].forEach(n=>{
    const i = _info(n);
    if(!i || !i.pend) return;
    const kp = agregarKpoint(i.fuente, i.landmark);
    if(kp.nombre!==n) _renombrarPuntos(n, kp.nombre);
    agregados.push(_codigoDe(i.fuente, i.landmark));
  });
  return agregados;
}

// cambia un nombre de punto en las filas y en el recorrido en construccion
function _renombrarPuntos(de, a){
  const cambiar = l => (l||[]).map(n=>n===de ? a : n);
  ptFeatures.forEach(f=>{ f.points = cambiar(f.points); if(f.reference) f.reference = cambiar(f.reference); if(f.cadena) f.cadena = cambiar(f.cadena); });
  ptCadena = cambiar(ptCadena);
}

// quitar un kpoint del catalogo NO borra las filas que lo usan: quedan pendientes (morado)
function quitarKpoint(kp){
  if(kp.origen.tipo==='landmark') _renombrarPuntos(kp.nombre, _pend(kp.origen.fuente, kp.origen.landmark));
  ptKpoints = ptKpoints.filter(k=>k!==kp);
}

// marca de una vez todos los puntos de una capa (hace falta 💾 Guardar)
function kpTodosCapa(capa){
  ptCatalogoPose.puntos.forEach(p=>agregarKpoint('pose', p.nombre));
  renderTodoPuntos();
}

// ---------------------------------------------------------------- catalogo: orden, numeros y nombres
// Orden: por ID de MediaPipe, de menor a mayor; los derivados al final. K01, K02... es la posicion en esta lista: las filas apuntan por NOMBRE, asi que
// renumerar no las rompe.
const _ORDEN_FUENTE={pose:0};
function ordenarKpoints(){
  const clave = k => k.origen.tipo==='landmark'
    ? [_ORDEN_FUENTE[k.origen.fuente], _indiceMediapipe(k.origen.fuente, k.origen.landmark)] : [9, k.numero];
  ptKpoints.sort((a,b)=>{const x=clave(a), y=clave(b); return x[0]-y[0] || x[1]-y[1];});
  const nuevo = new Map(ptKpoints.map((k,i)=>[k.numero,i+1]));
  ptKpoints.forEach(k=>{ if(k.origen.tipo==='derivado') k.origen.de = k.origen.de.map(n=>nuevo.get(n)); });
  ptKpoints.forEach((k,i)=>{ k.numero=i+1; });
}
// Codigo del punto: C01..C33 = Cuerpo 33 (ID de MediaPipe + 1); D01.. = derivados. Es fijo: existe aunque el punto no este marcado.
const _codigoDe = (fuente, landmark) => `C${String(_indiceMediapipe(fuente, landmark)+1).padStart(2,'0')}`;
// Un recorrido puede usar un punto que todavia NO esta marcado en el catalogo: se guarda como '~fuente|LANDMARK'
// (pendiente, se ve en morado) y se resuelve solo cuando el punto se marca.
const _pend = (fuente, landmark) => `~${fuente}|${landmark}`;
const _esPend = n => n.startsWith('~');
// {fuente, landmark, pend} del punto de un recorrido; null si es un derivado o no existe
function _info(nombre){
  if(_esPend(nombre)){ const [fuente, landmark] = nombre.slice(1).split('|'); return {fuente, landmark, pend:true}; }
  const kp = ptKpoints.find(k=>k.nombre===nombre);
  if(kp) return kp.origen.tipo==='landmark' ? {fuente:kp.origen.fuente, landmark:kp.origen.landmark, pend:false} : null;
  // nombre crudo de MediaPipe (filas viejas de la definicion): es un punto que todavia no esta marcado en el catalogo
  if(ptCatalogoPose && ptCatalogoPose.puntos.some(q=>q.nombre===nombre)) return {fuente:'pose', landmark:nombre, pend:true};
  return null;
}
const _kEtq = nombre => {
  const i = _info(nombre);
  if(i) return _codigoDe(i.fuente, i.landmark);
  const kp = ptKpoints.find(k=>k.nombre===nombre);
  return kp ? 'D'+String(ptKpoints.filter(k=>k.origen.tipo!=='landmark').indexOf(kp)+1).padStart(2,'0') : nombre;
};
// C01>C02>C03: los kpoints marcados en el catalogo llevan borde morado, los que no, sin borde
const _marcado = nombre => ptKpoints.some(k=>k.nombre===nombre);
const _cadenaHtml = cadena => cadena.map(n=>`<span class="cod${_marcado(n)?' marcado':''}" title="${_marcado(n)?'Marcado en el catalogo de kpoints':'No marcado en el catalogo'}">${_kEtq(n)}</span>`).join('>');
const _filaActiva = f => !!(_on(f.ang) || f.pros.some(_on) || _on(f.ratio));
// orden de un punto: por ID de MediaPipe
const _valKp = nombre => {
  const i = _info(nombre);
  if(i) return _ORDEN_FUENTE[i.fuente]*1000 + _indiceMediapipe(i.fuente, i.landmark);
  const kp = ptKpoints.find(k=>k.nombre===nombre);
  return kp ? 9000+kp.numero : 99999;
};

// descripcion en castellano de un punto
const _PARTE_POSE={EYE_INNER:'Ojo (interior)', EYE:'Ojo', EYE_OUTER:'Ojo (exterior)', EAR:'Oreja', SHOULDER:'Hombro', ELBOW:'Codo',
  WRIST:'Muñeca', PINKY:'Meñique (cuerpo)', INDEX:'Índice (cuerpo)', THUMB:'Pulgar (cuerpo)', HIP:'Cadera', KNEE:'Rodilla',
  ANKLE:'Tobillo', HEEL:'Talón', FOOT_INDEX:'Punta del pie'};
function _descLandmark(fuente, landmark){
  if(landmark==='NOSE') return 'Nariz';
  const boca = landmark.match(/^MOUTH_(LEFT|RIGHT)$/);
  if(boca) return 'Boca '+(boca[1]==='LEFT'?'izq.':'der.');
  const m = landmark.match(/^(LEFT|RIGHT)_(.+)$/);
  return m ? `${_PARTE_POSE[m[2]]||m[2]} ${m[1]==='LEFT'?'izq.':'der.'}` : landmark;
}
const _descKp = nombre => {
  const i = _info(nombre);
  if(i) return _descLandmark(i.fuente, i.landmark);
  return ptKpoints.find(k=>k.nombre===nombre) ? 'Punto medio de dos kpoints' : nombre;
};
const _siguienteNumeroKp = ()=> ptKpoints.length ? Math.max(...ptKpoints.map(k=>k.numero))+1 : 1;
const _nombreKpAuto = landmark => landmark;
const _catDe = () => ptCatalogoPose;
const _indiceMediapipe = (fuente, landmark) => ptCatalogoPose.puntos.findIndex(p=>p.nombre===landmark);

function agregarKpointDerivado(){
  if(ptKpoints.length<2) return msg('Necesitas al menos 2 kpoints ya creados para promediar');
  const nums = ptKpoints.map(k=>`${k.numero}: ${_kEtq(k.nombre)} ${_descKp(k.nombre)}`).join('\n');
  const a = +prompt('Numero (el de la izquierda) del primer punto a promediar:\n'+nums);
  const b = a && +prompt('Numero (el de la izquierda) del segundo punto a promediar:\n'+nums);
  if(!a || !b) return;
  const numero = _siguienteNumeroKp();
  ptKpoints.push({numero, nombre:'derivado_'+numero, origen:{tipo:'derivado', de:[a,b]}});
  ordenarKpoints();
  renderTodoPuntos();
}

function eliminarKpoint(numero){
  const kp = ptKpoints.find(k=>k.numero===numero);
  if(kp) quitarKpoint(kp);
  renderTodoPuntos();
}

// ---------------------------------------------------------------- tabla de kpoints
function _pastelFondo(grupo, alpha){
  const hex = PT_COLORES[grupo];
  if(!hex) return 'transparent';
  const n = parseInt(hex.slice(1),16);
  return `rgba(${(n>>16)&255},${(n>>8)&255},${n&255},${alpha==null?.22:alpha})`;
}

// los landmarks solo pierden el LEFT_/RIGHT_
function _codigoLandmark(nombre){
  return nombre.replace(/^(LEFT_|RIGHT_)/, '');
}

function _ladoDeOrigen(o){
  if(o.tipo!=='landmark') return '—';
  if(o.landmark.startsWith('LEFT_')) return 'I';
  if(o.landmark.startsWith('RIGHT_')) return 'D';
  return 'C';
}

function _posicionKp(kp, cache){
  if(cache[kp.numero]) return cache[kp.numero];
  let pos;
  if(kp.origen.tipo==='landmark'){
    const p = ptCatalogoPose.puntos.find(x=>x.nombre===kp.origen.landmark);
    pos = p ? {x:p.x, y:p.y, grupo:p.grupo} : {x:0.5, y:0.5, grupo:null};
  } else {
    const [a,b] = kp.origen.de.map(n=>ptKpoints.find(k=>k.numero===n));
    const pa=_posicionKp(a,cache), pb=_posicionKp(b,cache);
    pos = {x:(pa.x+pb.x)/2, y:(pa.y+pb.y)/2, grupo:pa.grupo};
  }
  cache[kp.numero]=pos;
  return pos;
}

function renderTablaKpoints(){
  const cache={};
  $F('#kpTabla').innerHTML = ptKpoints.map(k=>{
    const esLandmark = k.origen.tipo==='landmark';
    const codigo = esLandmark ? _codigoLandmark(k.origen.landmark) : `prom(${k.origen.de.join(',')})`;
    const id = esLandmark ? _indiceMediapipe(k.origen.fuente, k.origen.landmark) : '—';
    const idTitulo = esLandmark ? `${k.origen.landmark} (${k.origen.fuente})` : 'Punto derivado (promedio)';
    const grupo = _posicionKp(k,cache).grupo;
    const color = PT_COLORES[grupo] || '#8b93a3';
    return `<tr style="background:${_pastelFondo(grupo)}">
      <td class="hint" title="${_descKp(k.nombre)}" style="cursor:help"><span class="cod marcado">${_kEtq(k.nombre)}</span></td>
      <td class="hint" title="${idTitulo}" style="cursor:help">${id}</td>
      <td class="hint">${_ladoDeOrigen(k.origen)}</td>
      <td class="hint">${codigo}</td>
      <td><span onclick="eliminarKpoint(${k.numero})" title="Clic para quitar del catálogo"
           style="display:inline-block;width:11px;height:11px;border-radius:50%;background:${color};cursor:pointer;box-shadow:0 0 5px 1px ${color}"></span></td>
     </tr>`;
  }).join('') || '<tr><td colspan="5" class="hint">Sin kpoints todavia -- clic en el grafico.</td></tr>';
}

// ---------------------------------------------------------------- atajos de angulos (plantillas de ESTA app, no vienen de MediaPipe)
const _clavePunto = p => p.fuente+'|'+p.landmark;
function renderAngulosConocidos(){
  ptPresets = [];
  (ptCatalogoPose.angulos_conocidos||[]).forEach(p=>ptPresets.push({nombre:p.nombre, puntos:p.puntos.map(l=>({fuente:'pose', landmark:l}))}));
  const val = p => p.puntos.map(q=>_ORDEN_FUENTE[q.fuente]*1000+_indiceMediapipe(q.fuente, q.landmark));
  ptPresets.sort((a,b)=>{ const x=val(a), y=val(b); for(let i=0;i<3;i++) if(x[i]!==y[i]) return x[i]-y[i]; return 0; });
  // un atajo ya presente en la matriz (mismos puntos, en cualquier sentido) se marca en verde para no repetirlo
  const cadenas = _filasFeatures().map(f=>({base:f.base, ks:f.cadena.map(n=>{ const i=_info(n); return i ? i.fuente+'|'+i.landmark : '?'; })}));
  ptPresets.forEach(p=>{
    const ks = p.puntos.map(_clavePunto), rev = [...ks].reverse().join();
    const hay = cadenas.find(c=>c.ks.join()===ks.join() || c.ks.join()===rev);
    p.fila = hay ? hay.base : null;
  });
  $F('#kpAngulosConocidos').innerHTML = ptPresets.map((p,i)=>
    `<button class="mchk${p.fila?' on':''}" onclick="agregarAnguloConocido(${i})" title="${p.puntos.map(q=>_descLandmark(q.fuente,q.landmark)).join(' > ')}${p.fila?' — ya esta en la matriz':''}">${p.fila?'✓ ':''}${p.nombre} <small>${p.puntos.map(q=>_codigoDe(q.fuente,q.landmark)).join('>')}</small></button>`
  ).join('') || '<span class="hint">(sin atajos)</span>';
}

function agregarAnguloConocido(i){
  const preset = ptPresets[i];
  if(preset.fila){ _seleccionarFila(preset.fila); return msg(`'${preset.nombre}' ya esta en la matriz (fila '${preset.fila}')`); }
  const nombres = preset.puntos.map(p=>agregarKpoint(p.fuente, p.landmark).nombre);
  ptFeatures = ptFeatures.filter(f=>f.name!==preset.nombre);
  ptFeatures.push(..._featuresDeCadena(preset.nombre, nombres, true, true));
  ordenarFeatures();
  _seleccionarFila(preset.nombre);
  msg(`Angulo '${preset.nombre}' agregado a la matriz (falta 💾 Guardar)`);
}

// ---------------------------------------------------------------- matriz de angulos y proporciones
function deshacerCadena(){ ptCadena.pop(); renderTodoPuntos(); }

function limpiarFormFeaturePuntos(){
  ptCadena=[]; ptNombre=''; ptEditando=null;
  renderTodoPuntos();
}

// Una FILA de la matriz = un recorrido de kpoints (3 o mas, de cuerpo). En la definicion sigue siendo un feature
// 'angle' (solo con 3 puntos) y un feature 'proporcion' por tramo, con 'activo:false' cuando esta apagado.
// Siempre ordenadas del kpoint menor al mayor: primero los C01..
function _filasFeatures(){
  const filas=[], por={};
  ptFeatures.forEach(f=>{
    const base = f.type==='proporcion' ? f.name.replace(/_p\d+$/, '') : f.name;
    const fila = por[base] || (por[base] = (filas.push({base, cadena:[], ang:null, pros:[], ratio:null}), filas[filas.length-1]));
    if(f.type==='angle'){ fila.ang=f; if(!fila.cadena.length) fila.cadena=[...f.points]; }
    else if(f.type==='proporcion'){ fila.pros.push(f); fila.cadena=[...f.cadena]; }
    else { fila.ratio=f; fila.cadena=[...f.points, ...(f.reference||[])]; }
  });
  return filas.sort((a,b)=>{
    const x=a.cadena.map(_valKp), y=b.cadena.map(_valKp);
    for(let i=0;i<Math.min(x.length,y.length);i++) if(x[i]!==y[i]) return x[i]-y[i];
    return x.length-y.length || a.base.localeCompare(b.base);
  });
}
// deja ptFeatures en el mismo orden que la matriz (asi se guarda en la definicion)
function ordenarFeatures(){ ptFeatures = _filasFeatures().flatMap(f=>[f.ang, ...f.pros, f.ratio].filter(Boolean)); }
const _on = f => f && f.activo!==false;

// Seleccion exclusiva: elegir una fila cancela lo que se estaba armando en la fila libre
function _seleccionarFila(base){
  const fila = _filasFeatures().find(f=>f.base===base);
  ptCadena=[]; ptNombre=''; ptEditando=null; ptModo='marcar'; ptResaltar=base; renderTodoPuntos();   // el recorrido solo agrega puntos mientras esta activado
}
function resaltarFila(i){ _seleccionarFila(_filasFeatures()[i].base); }
// la fila libre no pinta nada hasta que tenga puntos; al elegirla se suelta la fila marcada
// la fila libre se activa/desactiva con clic: solo activada agrega los puntos que toques
function seleccionarLibre(){
  const estabaActiva = ptModo==='recorrido' && !ptEditando;
  ptResaltar=null; ptEditando=null; ptCadena=[]; ptNombre='';
  ptModo = estabaActiva ? 'marcar' : 'recorrido';
  renderTodoPuntos();
}
function cancelarEdicion(){ ptEditando=null; ptCadena=[]; ptNombre=''; ptModo='marcar'; renderTodoPuntos(); }

// angulo (solo con 3 puntos) y una proporcion por tramo, para un recorrido
function _featuresDeCadena(nombre, cadena, angOn, proOn){
  const out=[];
  if(cadena.length===3) out.push({name:nombre, type:'angle', points:[...cadena], activo:angOn});
  for(let i=0;i<cadena.length-1;i++)
    out.push({name:`${nombre}_p${i+1}`, type:'proporcion', points:[cadena[i],cadena[i+1]], cadena:[...cadena], activo:proOn});
  return out;
}

function alternarUso(i, cual){
  const fila = _filasFeatures()[i];
  if(cual==='ang'){
    if(fila.ang) fila.ang.activo = !_on(fila.ang);
    else ptFeatures.push(..._featuresDeCadena(fila.base, fila.cadena, true, false).filter(f=>f.type==='angle'));   // la fila venia sin angulo
  } else if(cual==='pro'){
    if(fila.pros.length){ const nuevo = !fila.pros.every(_on); fila.pros.forEach(p=>{ p.activo=nuevo; }); }
    else ptFeatures.push(..._featuresDeCadena(fila.base, fila.cadena, false, true).filter(f=>f.type==='proporcion'));   // la fila venia sin proporciones
  } else fila.ratio.activo = !_on(fila.ratio);
  // una fila activa necesita sus kpoints: si alguno no estaba marcado se marca
  const activa = cual==='ang' ? _on(fila.ang) || ptFeatures.some(f=>f.name===fila.base && f.type==='angle' && _on(f))
    : cual==='pro' ? ptFeatures.some(f=>f.name.startsWith(fila.base+'_p') && f.type==='proporcion' && _on(f)) : _on(fila.ratio);
  const marcados = activa ? _marcarPendientes([fila.cadena]) : [];
  ordenarFeatures();
  _seleccionarFila(fila.base);
  if(marcados.length) msg(`Se marcaron los kpoints de la fila: ${marcados.join(', ')}`);
}

function eliminarFilaPuntos(i){
  const base = _filasFeatures()[i].base;
  ptFeatures = ptFeatures.filter(f=>(f.type==='proporcion' ? f.name.replace(/_p\d+$/, '') : f.name)!==base);
  if(ptResaltar===base) ptResaltar=null;
  renderTodoPuntos();
}

// La fila se edita EN SU LUGAR: se le pueden quitar o AGREGAR kpoints (3 o mas) y ✔ la actualiza (con otro nombre, la renombra).
function editarFilaCadena(i){
  const fila = _filasFeatures()[i];
  if(ptEditando===fila.base) return cancelarEdicion();       // ✎ otra vez = salir de la edicion
  ptCadena = [...fila.cadena]; ptNombre = fila.base; ptEditando = fila.base; ptResaltar = fila.base; ptModo = 'recorrido';
  renderTodoPuntos();
}

function agregarFilaCadena(){
  if(ptCadena.length<3) return msg('El recorrido necesita al menos 3 kpoints');
  const editando = ptEditando;
  let nombre = ptNombre.trim() || editando || '';
  if(!nombre){                                                  // sin nombre: fila_N libre
    let n = _filasFeatures().length+1;
    while(ptFeatures.some(f=>f.name===`fila_${n}` || f.name.startsWith(`fila_${n}_p`))) n++;
    nombre = `fila_${n}`;
  }
  const previa = _filasFeatures().find(f=>f.base===(editando||nombre));   // al reemplazar una fila se conservan sus ✓/✗
  const angOn = previa && previa.ang ? _on(previa.ang) : true;
  const proOn = previa && previa.pros.length ? previa.pros.every(_on) : true;
  const esDe = base => f => (f.type==='proporcion' ? f.name.replace(/_p\d+$/, '') : f.name)===base;
  ptFeatures = ptFeatures.filter(f=>!esDe(nombre)(f) && !(editando && esDe(editando)(f)));
  const cadena = [...ptCadena];
  ptFeatures.push(..._featuresDeCadena(nombre, cadena, angOn, proOn));
  const marcados = (angOn || proOn) ? _marcarPendientes([cadena]) : [];     // una fila activa necesita sus kpoints
  ordenarFeatures();
  ptEditando = null;
  _seleccionarFila(nombre);
  msg(`Fila '${nombre}' ${editando ? 'actualizada' : 'agregada a la matriz'}${marcados.length ? ` (se marcaron ${marcados.join(', ')})` : ''} (falta 💾 Guardar)`);
}

function renderTablaFeaturesPuntos(){
  // aplica = la fila puede tener ese calculo; existe/on = ya esta creado y activo (si no existe se muestra ✗ y al pulsarlo se crea)
  const uso = (i, cual, aplica, on, tip) => aplica
    ? `<button class="uso ${on?'on':'off'}" onclick="event.stopPropagation();alternarUso(${i},'${cual}')" title="${tip}: ${on?'en uso':'apagado'}">${on?'✓':'✗'}</button>`
    : `<button class="uso na" disabled title="${tip}: no aplica">–</button>`;
  const filas = _filasFeatures();
  const html = filas.map((f,i)=>{
    const botones = f.ratio
      ? uso(i,'ratio',true,_on(f.ratio),'Razon de distancia') + uso(i,'',false,false,'Proporcion')
      : uso(i,'ang',f.cadena.length===3,_on(f.ang),'Angulo') + uso(i,'pro',f.cadena.length>=3,f.pros.length>0 && f.pros.every(_on),'Proporcion');
    if(ptEditando===f.base) return `<tr class="sel editando" onclick="event.stopPropagation()">
      <td>${i+1}</td>
      <td><input value="${ptNombre.replace(/"/g,'&quot;')}" placeholder="nombre (opcional)" oninput="ptNombre=this.value" style="width:100%;margin-bottom:3px">
        ${ptCadena.length ? `<b>${_cadenaHtml(ptCadena)}</b><div class="hint">${ptCadena.map(n=>_descKp(n)).join(' > ')}</div>`
          : '<span class="hint">Toca los kpoints en el gráfico (mínimo 3)</span>'}</td>
      <td class="hint">${ptCadena.length===3 ? '∠ y %' : ptCadena.length>3 ? '%' : ''}</td>
      <td><button onclick="agregarFilaCadena()" title="Guardar los cambios de esta fila">✔</button> <button onclick="deshacerCadena()" title="Quitar el ultimo punto">↶</button> <button class="mchk on" onclick="cancelarEdicion()" title="Edicion activa: pulsa para salir sin guardar">✎</button></td>
     </tr>`;
    return `<tr class="${ptResaltar===f.base?'sel':''}" onclick="resaltarFila(${i})" title="${f.base}">
      <td>${i+1}</td>
      <td><b>${_cadenaHtml(f.cadena)}</b><div class="hint">${f.cadena.map(n=>_descKp(n)).join(' > ')}</div></td>
      <td>${botones}</td>
      <td><button onclick="event.stopPropagation();editarFilaCadena(${i})" title="Editar (quitar o agregar kpoints)">✎</button> <button onclick="event.stopPropagation();eliminarFilaPuntos(${i})" title="Eliminar">🗑</button></td>
     </tr>`;
  }).join('');
  // la ultima fila siempre esta libre: se arma con clic en el grafico y ✔ la agrega (y aparece otra libre)
  const libre = ptEditando ? `<tr class="libre"><td>${filas.length+1}</td><td class="hint" colspan="3">Editando la fila ${filas.findIndex(f=>f.base===ptEditando)+1}: ✔ guarda, ✎ sale sin guardar.</td></tr>`
    : `<tr class="libre${ptModo==='recorrido'?' activa':''}${ptCadena.length?' sel':''}" onclick="seleccionarLibre()">
      <td>${filas.length+1}</td>
      <td><input value="${ptNombre.replace(/"/g,'&quot;')}" placeholder="nombre (opcional)" oninput="ptNombre=this.value" onclick="event.stopPropagation()" style="width:100%;margin-bottom:3px">
        ${ptCadena.length ? `<b>${_cadenaHtml(ptCadena)}</b><div class="hint">${ptCadena.map(_descKp).join(' > ')}</div>`
          : '<span class="hint">Fila libre: haz clic aquí y toca los kpoints en el gráfico (mínimo 3)</span>'}</td>
      <td class="hint">${ptCadena.length===3 ? '∠ y %' : ptCadena.length>3 ? '%' : ''}</td>
      <td><button onclick="event.stopPropagation();agregarFilaCadena()" title="Agregar la fila a la matriz">✔</button> <button onclick="event.stopPropagation();deshacerCadena()" title="Quitar el ultimo punto">↶</button> <button onclick="event.stopPropagation();limpiarFormFeaturePuntos()" title="Vaciar la fila libre">✖</button></td>
     </tr>`;
  $F('#ptFeatTabla').innerHTML = html + libre;
}

// ---------------------------------------------------------------- SQL y guardar
// SQL es la fuente que manda: al abrir el tipo se compara con SQL. Si SQL tiene otra version se carga esa; si no hay
// conexion se trabaja en local y lo guardado se sube solo cuando vuelva.
async function refrescarEstadoSql(){
  const el = $F('#kpSqlEstado');
  if(!$F('#ptEjercicio').value) return;
  el.style.color = '#8b93a3'; el.textContent = 'SQL: comprobando…';
  try{
    const j = await (await fetch('/api/puntos/sincronizar?ejercicio='+encodeURIComponent($F('#ptEjercicio').value))).json();
    if(j.estado==='sincronizado'){ el.style.color='#4caf7d'; el.textContent='SQL ✓ sincronizado'; }
    else if(j.estado==='enviado'){ el.style.color='#4caf7d'; el.textContent='SQL ✓ '+j.detalle; }
    else if(j.estado==='traido'){
      if(ptConCambios()){ el.style.color='#e0a95a'; el.textContent='SQL tiene otra version, pero tienes cambios sin guardar: al guardar mandas tu version'; }
      else { await cargarEjercicioPuntos(false); el.style.color='#4caf7d'; el.textContent='SQL ✓ se cargó la version de SQL'; msg('Se cargó la version que estaba en SQL'); }
    }
    else if(j.estado==='conflicto'){ el.style.color='#e05a5a'; el.textContent='SQL difiere y no se pudo aplicar: '+j.detalle; }
    else { el.style.color='#e05a5a'; el.textContent = j.pendiente ? '⏳ SQL sin conexión: guardado en local, se subirá solo' : 'SQL sin conexión: se trabaja en local y se sube solo al volver'; }
  }catch(e){ el.style.color='#e05a5a'; el.textContent='SQL sin respuesta'; }
}
setInterval(()=>{ const v=$F('#puntosview'); if(v && v.style.display!=='none') refrescarEstadoSql(); }, 30000);

async function guardarEjercicioPuntos(){
  const ejercicio = $F('#ptEjercicio').value;
  if(!ejercicio) return;
  ordenarFeatures();
  // Union: los puntos que usa una fila y no estan marcados en el catalogo se marcan (asi todo lo que se mide queda en el catalogo)
  const agregados = _marcarPendientes(ptFeatures.map(f=>[...f.points, ...(f.reference||[]), ...(f.cadena||[])]));
  if(agregados.length) msg(`Se marcaron ${agregados.length} kpoints que usaban las filas: ${agregados.join(', ')}`);
  renderTodoPuntos();
  const source = 'pose';
  const body = {ejercicio, source, kpoints: ptKpoints, features: ptFeatures};
  const r = await fetch('/api/puntos/definicion',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
  const j = await r.json();
  if(!r.ok){ $F('#ptResumen').textContent='Error: '+j.error; return msg('Error: '+j.error); }
  ptActual.source = source; ptSnapshot = _estadoEditor();
  const sql = j.sql && j.sql.ok ? `SQL (type ${j.sql.type}) actualizado` : 'SQL sin conexion: guardado en local, se subira solo cuando vuelva';
  const aviso = j.features_cambiaron ? ' Cambiaron las filas o su orden: graba de nuevo la base de este ejercicio (la anterior ya no se usa).' : '';
  msg((agregados.length ? `Se marcaron ${agregados.length} kpoints que usaban las filas (${agregados.join(', ')}). ` : '')+'Guardado en la definicion. '+sql);
  $F('#ptResumen').textContent = `${ptKpoints.length} kpoint(s) y ${ptFeatures.length} feature(s) guardadas${agregados.length ? ` (${agregados.length} se marcaron solos porque las filas los usaban: ${agregados.join(', ')})` : ''}. ${sql}. Si cambio el orden o los puntos, vuelve a generar cortes y tablas SQL para reentrenar.${aviso}`;
  refrescarEstadoSql();
}


// ---------------------------------------------------------------- reglas de postura
function renderReglas(){
  const t = $F('#ptReglasTabla');
  if(!t) return;
  const txt = (i,k,w)=>`<input value="${(ptReglas[i][k]||'').toString().replace(/"/g,'&quot;')}" style="width:${w}px" onchange="ptReglas[${i}].${k}=this.value">`;
  const num = (i,k)=>`<input type="number" step="any" value="${ptReglas[i][k]??''}" style="width:58px" onchange="ptReglas[${i}].${k}=this.value">`;
  const pts = (i,k)=>`<input value="${(ptReglas[i][k]||[]).join(',')}" style="width:84px" onchange="ptReglas[${i}].${k}=this.value">`;
  const sel = (i,k,ops)=>`<select onchange="ptReglas[${i}].${k}=this.value">${ops.map(([v,e])=>`<option value="${v}"${(ptReglas[i][k]||ops[0][0])===v?' selected':''}>${e}</option>`).join('')}</select>`;
  t.innerHTML = ptReglas.map((r,i)=>`<tr>
    <td>${txt(i,'nombre',120)}</td><td>${pts(i,'a')}</td><td>${pts(i,'b')}</td><td>${pts(i,'c')}</td>
    <td>${num(i,'angulo')}</td><td>${num(i,'tolerancia')}</td>
    <td>${sel(i,'unidad',[['pct','%'],['deg','°']])}</td><td>${sel(i,'lado',[['ambos','±'],['min','≥'],['max','≤']])}</td>
    <td>${sel(i,'fase',[['siempre','siempre'],['bajando','bajando'],['abajo','abajo']])}</td><td>${txt(i,'mensaje',200)}</td>
    <td><input type="checkbox"${r.activo===false?'':' checked'} onchange="ptReglas[${i}].activo=this.checked"></td>
    <td><button onclick="ptReglas.splice(${i},1);renderReglas()">✕</button></td></tr>`).join('')
    || '<tr><td colspan="12" class="hint">Sin reglas.</td></tr>';
}
function agregarRegla(){
  ptReglas.push({nombre:'Espalda recta', a:['C01'], b:['C24','C25'], angulo:90, tolerancia:8, unidad:'pct', activo:true});
  renderReglas();
}
async function guardarReglas(){
  const ejercicio = $F('#ptEjercicio').value;
  if(!ejercicio) return;
  const r = await fetch('/api/puntos/reglas',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({ejercicio, reglas:ptReglas})});
  const j = await r.json();
  if(!r.ok) return msg('Error: '+(j.error||j.detail));
  ptReglas = j.reglas; renderReglas();
  msg(`${ptReglas.length} regla(s) guardadas en la definicion. Reinicia la sesión para que las tome.`);
}


// ---------------------------------------------------------------- normalizacion (gold): origen / escala / cuadros
function renderNormalizacion(){
  const n=(ptActual&&ptActual.normalizacion)||{};
  $F('#ptNormOrigen').value=n.origen||''; $F('#ptNormEscala').value=n.escala||''; $F('#ptNormN').value=n.n_frames||30;
  $F('#ptNormClip').innerHTML='<option value="">(uno del medio)</option>';
  $F('#ptNormMsg').innerHTML = n.error ? `<span class="errmark">⚠ ${n.error}</span>`
    : !n.origen ? 'Este ejercicio no trae hombros y caderas: sin fórmula se usa la caja 100×100 antigua. Define una fórmula.'
    : n.propia ? '' : 'Valores por defecto (todavía no guardados): origen = medio de caderas, escala = largo del tronco.';
}
function _normBody(){
  return {ejercicio:$F('#ptEjercicio').value, origen:$F('#ptNormOrigen').value, escala:$F('#ptNormEscala').value,
          n_frames:+$F('#ptNormN').value||0, clip:$F('#ptNormClip').value||null};
}
async function probarNormalizacion(){
  const r=await fetch('/api/puntos/normalizacion/previa',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(_normBody())});
  const j=await r.json();
  if(!r.ok){ $F('#ptNormMsg').innerHTML=`<span class="errmark">✗ ${j.error||j.detail}</span>`; return; }
  const sel=$F('#ptNormClip'), cur=sel.value;
  sel.innerHTML='<option value="">(uno del medio)</option>'+j.clips.map(c=>`<option value="${c}">${c}</option>`).join('');
  sel.value=String(j.clip);
  const ej=Object.entries(j.ejemplo).map(([k,v])=>`${k} → (${v[0]}, ${v[1]})`).join(' · ');
  $F('#ptNormMsg').innerHTML=`<span class="okmark">✓ clip ${j.clip}</span> · ${j.cuadros} cuadros (${j.validos} con escala válida) · origen típico (${j.origen[0]}, ${j.origen[1]}) · escala = <b>${j.escala}</b> (cuadros: ${j.escala_min} a ${j.escala_max}) · cuadro del medio normalizado: ${ej}`;
}
async function guardarNormalizacion(){
  const r=await fetch('/api/puntos/normalizacion',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(_normBody())});
  const j=await r.json();
  if(!r.ok){ $F('#ptNormMsg').innerHTML=`<span class="errmark">✗ ${j.error||j.detail}</span>`; return; }
  if(ptActual) ptActual.normalizacion={...j.normalizacion, propia:true, error:null};
  $F('#ptNormMsg').innerHTML=`<span class="okmark">✓ guardada</span>`+(j.cambio?' · cambió: «Generar documentación» rehace gold y lo sube a SQL; los modelos ya entrenados usaron la normalización anterior, vuelve a entrenar.':'');
  msg('Normalización guardada');
}
