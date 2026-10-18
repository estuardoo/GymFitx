/* Pestana SIM: verificacion visual de deteccion + normalizacion de un clip. API: interfaz/api/sim.py
   Vista 1: video original. Vista 2: esqueleto crudo (points_screen) sincronizado con el video (misma
   tecnica de cortes.js: idxCuadro + tolerancia de 250ms), con angulos. Vista 3: independiente, el clip
   normalizado (DTW-alineado) contra el base, animado por indice de cuadro (no por tiempo real). */
const simState = {tipo:'', clips:{}, base:'', clip:'', crudo:null, normalizado:null, playing3:false, frame3:0, modo2:'video_mov'};

async function cargarSimTipos(){
  const r = await (await fetch('/api/sim/opciones')).json();
  const sel=$F('#simTipo');
  sel.innerHTML = Object.entries(r.tipos||{}).map(([t,ej])=>`<option value="${t}">${ej} (type ${t})</option>`).join('')
    || '<option value="">(sin ejercicios exportados)</option>';
  sel.value = r.tipo;
  aplicarSimOpciones(r);
}
async function cargarSimOpciones(){
  const tipo=+$F('#simTipo').value; if(!tipo) return;
  aplicarSimOpciones(await (await fetch('/api/sim/opciones?tipo='+tipo)).json());
}
function aplicarSimOpciones(r){
  simState.tipo = r.tipo; simState.clips = r.clips||{base:[],bien:[],mal:[]};
  simState.base = (simState.clips.base||[])[0] || '';
  $F('#simBaseInfo').textContent = simState.base ? `Base: ${simState.base}` : '(este ejercicio no tiene ningun clip "base")';
  simState.clip = ''; simState.crudo = null; simState.normalizado = null;
  renderSimClips();
  const primero = (simState.clips.bien||[])[0] || (simState.clips.mal||[])[0];
  if(primero) elegirSimClip(primero); else { $F('#simV1').removeAttribute('src'); $F('#simC2Info').textContent=''; renderSimLeyenda3(); }
}
function renderSimClips(){
  const filas=[...(simState.clips.base||[]).map(c=>({nombre:c,clase:'base'})),
               ...(simState.clips.bien||[]).map(c=>({nombre:c,clase:'bien'})),
               ...(simState.clips.mal||[]).map(c=>({nombre:c,clase:'mal'}))];
  $F('#simClips').innerHTML = filas.map(f=>
    `<tr class="${f.nombre===simState.clip?'rank-mejor':''}" style="cursor:pointer" onclick="elegirSimClip('${f.nombre}')"><td>${f.nombre.split('/').pop()}</td><td>${f.clase}</td></tr>`
  ).join('') || '<tr><td colspan="2" class="hint">Sin clips</td></tr>';
}

async function elegirSimClip(clip){
  simState.clip = clip; renderSimClips();
  $F('#simV1').src = '/dataset/' + clip;
  simState.crudo = null; simState.normalizado = null; simState.frame3 = 0;
  simState.playing3 = false; $F('#simB3pp').textContent = '▶ Play';
  if(sim3Timer){ clearInterval(sim3Timer); sim3Timer=null; }
  $F('#simC2Info').textContent = 'cargando...';
  $F('#simLeyenda3').innerHTML = '';
  const [crudo, normalizado] = await Promise.all([
    fetch('/api/sim/crudo?clip='+encodeURIComponent(clip)).then(r=>r.json()),
    simState.base ? fetch(`/api/sim/normalizado?tipo=${simState.tipo}&base=${encodeURIComponent(simState.base)}&clip=${encodeURIComponent(clip)}`).then(r=>r.json()) : Promise.resolve(null),
  ]);
  simState.crudo = crudo.error ? null : crudo;
  $F('#simC2Info').textContent = crudo.error || `${crudo.nombres.length} puntos · ${crudo.t_ms.length} cuadros`;
  simState.normalizado = (normalizado && !normalizado.error) ? normalizado : null;
  cargarAvatarSim(clip);
  const nFrames = simState.normalizado ? (simState.normalizado.base[0]||[]).length : 0;
  $F('#simSlider3').max = Math.max(0, nFrames-1);
  $F('#simSlider3').value = 0;
  if(!simState.base) $F('#simLeyenda3').innerHTML = '<span class="hint">Este ejercicio no tiene clip "base"</span>';
  else if(normalizado && normalizado.error) $F('#simLeyenda3').innerHTML = `<span class="hint">${normalizado.error}</span>`;
  else renderSimLeyenda3();
  dibujarSim3();
}

// --- Vista 1-2: video + esqueleto crudo, superpuesto y sincronizado ----------
// El canvas va absolutamente posicionado ENCIMA del video (ver #simWrap1/#simC2 en estilos.css), fuera del
// flujo normal -- asi su tamano (que depende del video) nunca reacomoda el resto de la pagina ni mueve la
// barra de scroll cuando el video termina y sus dimensiones internas cambian.
const simCv2 = $F('#simC2'), simCx2 = simCv2.getContext('2d');
function idxCuadroSim(t, tms){
  let lo=0, hi=t.length-1;
  if(!t.length || tms<t[0]) return -1;
  while(lo<hi){ const m=(lo+hi+1)>>1; if(t[m]<=tms) lo=m; else hi=m-1; }
  return lo;
}
function simSetModo2(m){
  simState.modo2 = m;
  document.querySelectorAll('.simmodo').forEach(b=>b.classList.toggle('on', b.dataset.modo===m));
  dibujarSim2();
}
function dibujarSim2(){
  const v1=$F('#simV1');
  const w=v1.clientWidth, h=v1.clientHeight;
  if(simCv2.width!==w||simCv2.height!==h){ simCv2.width=w; simCv2.height=h; simCv2.style.width=w+'px'; simCv2.style.height=h+'px'; }
  simCx2.clearRect(0,0,w,h);
  if(simState.modo2==='solo_mov'){ simCx2.fillStyle='#000'; simCx2.fillRect(0,0,w,h); }
  if(simState.modo2==='video') return;   // solo el video: nada mas que dibujar
  const d=simState.crudo;
  if(!d || !d.t_ms.length || !v1.videoWidth) return;
  const i=idxCuadroSim(d.t_ms, v1.currentTime*1000);
  if(i<0 || v1.currentTime*1000-d.t_ms[i]>250) return;
  // el video se ve con su proporcion propia (misma tecnica que cortes.js): calcular el rectangulo real
  const esc=Math.min(w/v1.videoWidth, h/v1.videoHeight), vw=v1.videoWidth*esc, vh=v1.videoHeight*esc;
  const ox=(w-vw)/2, oy=(h-vh)/2, P=([x,y])=>[ox+x*vw, oy+y*vh];
  const pts=d.puntos[i];
  simCx2.strokeStyle='#4cff8a'; simCx2.lineWidth=2.5; simCx2.beginPath();
  (d.conexiones||[]).forEach(([a,b])=>{ const p=pts[a], q=pts[b];
    if(p&&q&&p[0]!=null&&q[0]!=null){ const [x1,y1]=P(p),[x2,y2]=P(q); simCx2.moveTo(x1,y1); simCx2.lineTo(x2,y2); } });
  simCx2.stroke();
  simCx2.fillStyle='#4cff8a';
  pts.forEach(p=>{ if(p&&p[0]!=null){ const [x,y]=P(p); simCx2.beginPath(); simCx2.arc(x,y,3,0,7); simCx2.fill(); } });
  const ang=d.angulos[i]||[];
  simCx2.fillStyle='#ffd54f'; simCx2.font='bold 11px system-ui';
  (d.nombres_angulos||[]).forEach((_n,k)=>{
    if(ang[k]==null) return;
    const idxs=(d.angulos_puntos[k]||[]).map(n=>d.nombres.indexOf(n)).filter(ix=>ix>=0 && pts[ix] && pts[ix][0]!=null);
    if(!idxs.length) return;
    const cx=idxs.reduce((s,ix)=>s+pts[ix][0],0)/idxs.length, cy=idxs.reduce((s,ix)=>s+pts[ix][1],0)/idxs.length;
    const [x,y]=P([cx,cy]);
    simCx2.fillText(Math.round(ang[k]), x+4, y-4);
  });
}
requestAnimationFrame(function loopSim2(){
  if($F('#simview').style.display!=='none') dibujarSim2();
  requestAnimationFrame(loopSim2);
});

// --- Vista 3: normalizado (base vs clip), independiente -- animada por indice de cuadro, no por tiempo real
const simCv3 = $F('#simC3'), simCx3 = simCv3.getContext('2d');
let sim3Timer = null;
function simTogglePlay3(){
  simState.playing3 = !simState.playing3;
  $F('#simB3pp').textContent = simState.playing3 ? '⏸ Pausa' : '▶ Play';
  if(sim3Timer){ clearInterval(sim3Timer); sim3Timer=null; }
  if(simState.playing3) sim3Timer=setInterval(()=>{
    const n = simState.normalizado ? (simState.normalizado.base[0]||[]).length : 0;
    if(!n) return;
    if(simState.frame3 >= n-1){ simTogglePlay3(); return; }   // llego al final: se para, no vuelve a 0
    simState.frame3++;
    $F('#simSlider3').value = simState.frame3;
    dibujarSim3();
  }, 120);  // ~8 cuadros/seg: alcanza para ver si van sincronizados, sin marear
}
function simIrAFrame3(i){ simState.frame3=i; dibujarSim3(); }
function simCalcBBox(d){
  let minX=Infinity,minY=Infinity,maxX=-Infinity,maxY=-Infinity;
  [d.base, d.otro].forEach(serie=>serie.forEach(kp=>kp.forEach(([x,y])=>{
    if(x<minX)minX=x; if(x>maxX)maxX=x; if(y<minY)minY=y; if(y>maxY)maxY=y;
  })));
  return {minX,minY,maxX,maxY};
}
function dibujarSim3(){
  const w=simCv3.clientWidth||300, h=w;  // cuadrado: el normalizado ya viene con la proporcion correcta
  if(simCv3.width!==Math.round(w)||simCv3.height!==Math.round(h)){ simCv3.width=Math.round(w); simCv3.height=Math.round(h); }
  simCx3.fillStyle='#0b1fb0'; simCx3.fillRect(0,0,simCv3.width,simCv3.height);  // "fondo azul fuerte" pedido
  const d=simState.normalizado;
  $F('#simFrame3Info').textContent = d ? `cuadro ${simState.frame3+1}/${(d.base[0]||[]).length}` : '';
  if(!d || !d.nombres.length) return;
  if(!d._bbox) d._bbox = simCalcBBox(d);
  const {minX,minY,maxX,maxY}=d._bbox, W=simCv3.width, H=simCv3.height, PAD=20;
  const rx=(maxX-minX)||1, ry=(maxY-minY)||1, esc=Math.min((W-2*PAD)/rx, (H-2*PAD)/ry);
  const P=(x,y)=>[PAD+(x-minX)*esc, PAD+(y-minY)*esc];
  const frame=simState.frame3;
  const dibujaEsqueleto=(serie, color)=>{
    simCx3.strokeStyle=color; simCx3.lineWidth=2; simCx3.beginPath();
    (d.conexiones||[]).forEach(([a,b])=>{ const p=serie[a]&&serie[a][frame], q=serie[b]&&serie[b][frame];
      if(p&&q){ const [x1,y1]=P(p[0],p[1]),[x2,y2]=P(q[0],q[1]); simCx3.moveTo(x1,y1); simCx3.lineTo(x2,y2); } });
    simCx3.stroke();
    simCx3.fillStyle=color;
    serie.forEach(kp=>{ const p=kp&&kp[frame]; if(p){ const [x,y]=P(p[0],p[1]); simCx3.beginPath(); simCx3.arc(x,y,3.5,0,7); simCx3.fill(); } });
  };
  dibujaEsqueleto(d.base, '#5ec8ff');    // base: azul
  dibujaEsqueleto(d.otro, '#a8e6b8');    // clip elegido (seleccionado): verde pastel
}
addEventListener('resize', ()=>{ if($F('#simview').style.display!=='none') dibujarSim3(); });
function renderSimLeyenda3(){
  const d=simState.normalizado;
  if(!d){ $F('#simLeyenda3').innerHTML=''; return; }
  const vals=d.indicadores.filter(v=>v!=null);
  const kg = vals.length ? (vals.reduce((a,b)=>a+b,0)/vals.length).toFixed(2) : '—';
  $F('#simLeyenda3').innerHTML = `<span class="legchip"><i style="background:#5ec8ff"></i>base</span>` +
    `<span class="legchip"><i style="background:#a8e6b8"></i>${simState.clip.split('/').pop()}</span>` +
    `<span class="hint">KG ${kg}</span>`;
}

// --- Vista 4: avatar 3D (js/avatar3d.js) ---------------------------------------------------------
async function cargarAvatarSim(clip){
  if(!window.avatar3d) return;
  window.avatar3d.vacio('cargando...');
  const d = await fetch('/api/sim/cuerpo3d?clip='+encodeURIComponent(clip)).then(r=>r.json());
  if(simState.clip !== clip) return;   // se eligio otro clip mientras cargaba
  if(d.error) window.avatar3d.vacio(d.error); else window.avatar3d.cargar(d);
}
