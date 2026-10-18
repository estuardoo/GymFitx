/* Pestana Descomposicion: series por punto e indicador contra el base. API: /api/descomp/* */
// --- Descomposicion de movimiento -------------------------------------------

const dcState = {kpoints:[], activos:new Set(), datos:null, base:'', bien:'', mal:'', clipsBien:[], clipsMal:[]};
const DC_COLORES = ['#2f6feb','#e05a5a','#4caf7d','#e0a95a','#a678e0','#5ac8e0','#e05ac2','#8fd13f'];

async function cargarDescompTipos(){
  const tipos=await (await fetch('/api/tipos')).json();
  const sel=$F('#dcTipo');
  sel.innerHTML=Object.entries(tipos).map(([t,ej])=>`<option value="${t}">${ej} (type ${t})</option>`).join('')
    || '<option value="">(sin ejercicios exportados)</option>';
  if(sel.value) await cargarDescompOpciones();
}

async function cargarDescompOpciones(){
  const tipo=+$F('#dcTipo').value; if(!tipo) return;
  const r=await (await fetch('/api/descomp/opciones',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({tipo})})).json();
  dcState.base = r.clips.base[0]||'';
  dcState.bien = ''; dcState.mal = '';
  dcState.clipsBien = r.clips.bien; dcState.clipsMal = r.clips.mal;
  $F('#dcBaseInfo').textContent = dcState.base ? `Base: ${dcState.base}` : '(este ejercicio no tiene ningun clip marcado como "base")';
  dcState.kpoints = r.kpoints;
  dcState.activos = new Set(r.kpoints.slice(0, 3));  // los primeros 3 activos por defecto, para no saturar el grafico
  dcState.datos = null;
  renderDcClips();
  renderDcKpoints();
  $F('#dcSvgMov').innerHTML='';
  $F('#dcResumenHead').innerHTML=''; $F('#dcResumen').innerHTML='';
  cargarDescompRanking();
  if(dcState.base) analizarDescomp();  // ya con la base sola se ve su propia linea de movimiento
}

async function cargarDescompRanking(){
  const tipo=+$F('#dcTipo').value;
  if(!tipo){ $F('#dcRanking').innerHTML=''; return; }
  const r=await (await fetch('/api/descomp/ranking',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({tipo})})).json();
  const filas=r.ranking||[];
  const conKg=filas.filter(f=>f.kg!=null);
  const maxKg=conKg.length?Math.max(...conKg.map(f=>f.kg)):null;
  $F('#dcRanking').innerHTML = filas.length ? filas.map(f=>
    `<tr class="${f.kg!=null&&f.kg===maxKg?'dc-mejor':''}"><td>${f.archivo.split('/').pop()}</td><td>${f.clase}</td><td>${f.kg!=null?f.kg.toFixed(2):'—'}</td><td>${f.n}</td></tr>`
  ).join('') : '<tr><td colspan="4" class="hint">Sin datos -- genera/actualiza tablas SQL.</td></tr>';
}

function renderDcClips(){
  const filas=[...dcState.clipsBien.map(c=>({nombre:c,clase:'bien'})), ...dcState.clipsMal.map(c=>({nombre:c,clase:'mal'}))];
  $F('#dcClips').innerHTML = filas.map(f=>{
    const activo = f.clase==='bien' ? f.nombre===dcState.bien : f.nombre===dcState.mal;
    return `<tr class="${activo?'rank-mejor':''}" style="cursor:pointer" onclick="elegirDcClip('${f.nombre}','${f.clase}')"><td>${f.nombre.split('/').pop()}</td><td>${f.clase}</td></tr>`;
  }).join('');
}
function elegirDcClip(nombre, clase){
  if(clase==='bien') dcState.bien = dcState.bien===nombre ? '' : nombre;
  else dcState.mal = dcState.mal===nombre ? '' : nombre;
  renderDcClips();
  analizarDescomp();
}

function renderDcKpoints(){
  $F('#dcKpoints').innerHTML = dcState.kpoints.map((k,i)=>
    `<tr class="${dcState.activos.has(k)?'rank-mejor':''}" style="cursor:pointer" onclick="toggleDcKpoint('${k}')"><td>${i+1}</td><td>${k}</td></tr>`).join('');
}
function toggleDcKpoint(k){
  if(dcState.activos.has(k)) dcState.activos.delete(k); else dcState.activos.add(k);
  renderDcKpoints();
  if(dcState.datos) dibujarDescomp();
}

async function analizarDescomp(){
  const tipo=+$F('#dcTipo').value;
  if(!dcState.base) return;  // sin clip 'base' para este ejercicio, nada que comparar
  const resp=await fetch('/api/descomp/analizar',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({tipo, base:dcState.base, bien:dcState.bien, mal:dcState.mal, activos:[...dcState.activos]})});
  const r=await resp.json();
  if(!resp.ok) return msg('Error: '+(r.error||'desconocido'));
  dcState.datos=r;
  dibujarDescomp();
}

function dibujarDescomp(){
  dibujarGraficoDc('#dcSvgMov', '#dcLegMov', dcState.datos.series.base, dcState.datos.series.bien, dcState.datos.series.mal);
  renderDcResumenKpoints();
}

// "bien" siempre en azules pastel, "mal" siempre en rojos pastel (unos pocos
// tonos por familia, para distinguir kpoints sin perder el codigo de color
// por clase). La base usa DC_COLORES (solida, gruesa) como su identidad.
const DC_PASTEL_BIEN = ['#8fb8f0', '#a6cdf2', '#bcd9f5', '#9fc8e8'];
const DC_PASTEL_MAL  = ['#f0a3a3', '#f2b8ad', '#f5c2ba', '#e89999'];

// Distancia de una serie (x,y) a su PROPIO promedio, por frame -- lo mismo
// que suma SStot en evaluacion/similitud.indicador(). Una sola linea: cuanto se mueve ese
// kpoint en el clip, sin comparar contra nada mas todavia.
function distDeMedia(serie){
  const n=serie.x.length;
  const mx=serie.x.reduce((a,b)=>a+b,0)/n, my=serie.y.reduce((a,b)=>a+b,0)/n;
  const out=[];
  for(let i=0;i<n;i++) out.push(Math.hypot(serie.x[i]-mx, serie.y[i]-my));
  return out;
}
// Distancia frame a frame entre dos series -- lo mismo que suma SSres en
// evaluacion/similitud.indicador(). Es el "error" de 'cmp' contra 'base' en cada frame.
function distEntre(cmp, base){
  const n=Math.min(cmp.x.length, base.x.length);
  const out=[];
  for(let i=0;i<n;i++) out.push(Math.hypot(cmp.x[i]-base.x[i], cmp.y[i]-base.y[i]));
  return out;
}

// Un solo grafico "Movimientos": 1 linea solida por kpoint activo (cuanto se
// mueve en la base) y, solo si hay un clip elegido, 1 linea punteada mas por
// clip (su error contra la base) -- 1 linea sin clip elegido, 2 si eliges
// uno, 3 si eliges bien y mal a la vez. Antes se dibujaban x e y por
// separado (el doble de lineas) comparando posicion absoluta; esto es
// exactamente lo que ya usa el indicador (ver evaluacion/similitud.indicador), asi que el
// grafico ahora explica visualmente por que un indicador sale bajo.
function dibujarGraficoDc(svgSel, legSel, base, bien, mal){
  const svg=$F(svgSel), leg=legSel?$F(legSel):null;
  const activos=[...dcState.activos].filter(k=>base[k]);
  const hayBien = bien && Object.keys(bien).length>0;
  const hayMal = mal && Object.keys(mal).length>0;
  if(!activos.length){ svg.innerHTML=''; if(leg) leg.innerHTML='<span class="hint">Sin puntos activos.</span>'; return; }

  const baseDist={}, bienDist={}, malDist={};
  activos.forEach(k=>{
    baseDist[k]=distDeMedia(base[k]);
    if(hayBien && bien[k]) bienDist[k]=distEntre(bien[k], base[k]);
    if(hayMal && mal[k]) malDist[k]=distEntre(mal[k], base[k]);
  });

  const n=baseDist[activos[0]].length;
  const vals=activos.flatMap(k=>[...baseDist[k], ...(bienDist[k]||[]), ...(malDist[k]||[])]);
  const lo=Math.min(0,...vals), hi=Math.max(...vals,1e-6), W=600, H=200, PAD_L=40, PAD_R=12, PAD_T=8, PAD_B=22;
  const sx=i=>PAD_L+i/((n-1)||1)*(W-PAD_L-PAD_R);
  const sy=v=>H-PAD_B-(v-lo)/((hi-lo)||1)*(H-PAD_T-PAD_B);
  const linea=arr=>arr.map((v,i)=>sx(i)+','+sy(v)).join(' ');

  let out=`<line x1="${PAD_L}" y1="${H-PAD_B}" x2="${W-PAD_R}" y2="${H-PAD_B}" stroke="#39404e"/><line x1="${PAD_L}" y1="${PAD_T}" x2="${PAD_L}" y2="${H-PAD_B}" stroke="#39404e"/>`;

  // eje X del grafico: numero de frame (1..n) -- unos pocos ticks parejos, no todos, para no saturar
  const pasoX=Math.max(1, Math.round((n-1)/6)) || 1;
  for(let i=0;i<n;i+=pasoX){
    out+=`<text x="${sx(i)}" y="${H-PAD_B+11}" font-size="8" fill="#8a93a6" text-anchor="middle">${i+1}</text>`;
  }
  if((n-1)%pasoX!==0) out+=`<text x="${sx(n-1)}" y="${H-PAD_B+11}" font-size="8" fill="#8a93a6" text-anchor="middle">${n}</text>`;

  // eje Y del grafico: del minimo al maximo que realmente aparece, 5 marcas
  for(let j=0;j<=5;j++){
    const v=lo+(hi-lo)*j/5;
    out+=`<text x="${PAD_L-4}" y="${sy(v)+3}" font-size="8" fill="#8a93a6" text-anchor="end">${v.toFixed(2)}</text>`;
  }

  activos.forEach((k,i)=>{
    const color=DC_COLORES[i%DC_COLORES.length];
    out+=`<polyline fill="none" stroke="${color}" stroke-width="2.5" points="${linea(baseDist[k])}"/>`;
    if(bienDist[k]){
      const c=DC_PASTEL_BIEN[i%DC_PASTEL_BIEN.length];
      out+=`<polyline fill="none" stroke="${c}" stroke-width="1.8" stroke-dasharray="2,3" points="${linea(bienDist[k])}"/>`;
    }
    if(malDist[k]){
      const c=DC_PASTEL_MAL[i%DC_PASTEL_MAL.length];
      out+=`<polyline fill="none" stroke="${c}" stroke-width="1.8" stroke-dasharray="2,3" points="${linea(malDist[k])}"/>`;
    }
  });
  svg.innerHTML=out;
  if(leg){
    const chips = activos.map((k,i)=>`<span class="legchip"><i style="background:${DC_COLORES[i%DC_COLORES.length]}"></i>${k}</span>`);
    if(hayBien) chips.push(`<span class="legchip"><i style="background:${DC_PASTEL_BIEN[0]}"></i>bien</span>`);
    if(hayMal) chips.push(`<span class="legchip"><i style="background:${DC_PASTEL_MAL[0]}"></i>mal</span>`);
    leg.innerHTML = chips.join('');
  }
}

function renderDcResumenKpoints(){
  const d=dcState.datos, kpoints=d.kpoints, filas=[];
  if(dcState.bien) filas.push({llave:'bien', nombre:dcState.bien, ind:d.indicadores.bien, kg:d.resumen.bien});
  if(dcState.mal) filas.push({llave:'mal', nombre:dcState.mal, ind:d.indicadores.mal, kg:d.resumen.mal});

  $F('#dcResumenHead').innerHTML = `<tr><th>Llave</th><th>Nombre</th>${kpoints.map((_k,i)=>`<th>K${i+1}</th>`).join('')}<th>KG</th></tr>`;

  // el mayor valor de K individual en toda la tabla (mas parecido), en amarillo
  const todos=filas.flatMap(f=>kpoints.map(k=>f.ind[k])).filter(v=>v!=null);
  const maxK=todos.length?Math.max(...todos):null;

  $F('#dcResumen').innerHTML = filas.map((f,i)=>{
    const celdas=kpoints.map(k=>{
      const v=f.ind[k];
      return `<td${v===maxK?' class="dc-mejor"':''}>${v!=null?v.toFixed(2):'—'}</td>`;
    }).join('');
    return `<tr onclick="seleccionarDcFragmento(${i})"><td>${f.llave}</td><td>${f.nombre.split('/').pop()}</td>${celdas}<td><b>${f.kg!=null?f.kg.toFixed(2):'—'}</b></td></tr>`;
  }).join('');
}
function seleccionarDcFragmento(i){
  [...$F('#dcResumen').children].forEach((tr,j)=>tr.classList.toggle('rank-mejor', j===i));
}
