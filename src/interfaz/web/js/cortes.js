/* Pestana Cortar videos: linea de tiempo, cortes, clases, overlay del esqueleto y exportar. API: interfaz/api/etiquetado.py */
const $F=s=>document.querySelector(s), v=$F('#v');
let CFG={clases:[]}, VID=[], L={}, cur=null, sel=0, loopSeg=false, save=null, filtro='', curFps=0, zoom=1;
const COLORS={bien:'#a8e6b8',mal:'#f4a8a8',base:'#a8c8f0',descarte:'#cfd3da'};
const ICONS={bien:'✓',mal:'✗'};
const colorOf=c=>{const base=c?(COLORS[c]||'#c9cdd6'):'#39404e';
  return c==='descarte'?`${base} repeating-linear-gradient(45deg,rgba(20,22,26,.35) 0 6px,transparent 6px 12px)`:base};
const f=n=>(+n||0).toFixed(2);
const tc=t=>{t=Math.max(0,+t||0);const h=Math.floor(t/3600),m=Math.floor(t%3600/60),sec=Math.floor(t%60),ms=Math.round((t%1)*1000),p=(n,l=2)=>String(n).padStart(l,'0');return p(h)+':'+p(m)+':'+p(sec)+'.'+p(ms,3)};
const segs=()=>cur&&L[cur]?L[cur].segmentos:[];
const msg=t=>{$F('#msg').textContent=t;$F('#msg').style.display='block';setTimeout(()=>$F('#msg').style.display='none',4000)};

let TIPO='';  // carpeta de ejercicio elegida en el listbox; '' = todas
fetch('/api/config').then(r=>r.json()).then(async c=>{
  CFG=c; VID=c.videos; await cargarPersonas(); L=await (await fetch('/api/labels')).json();
  const tipos=[...new Set(VID.map(x=>x.file.split('/')[0]))].sort();
  const sel=$F('#tipoVid');
  sel.innerHTML=(tipos.length>1?'<option value="">Todos los ejercicios</option>':'')+
    tipos.map(t=>`<option value="${t}">${(VID.find(x=>x.file.startsWith(t+'/'))||{}).ejercicio||t}</option>`).join('');
  if(tipos.length===1) TIPO=tipos[0];
  sel.value=TIPO;
  resumen(); listar(); if(VID.length) abrir((VID.find(x=>!TIPO||x.file.startsWith(TIPO+'/'))||VID[0]).file);
  actualizarBoton();
});
function cambiarTipoVid(){ TIPO=$F('#tipoVid').value; listar(); const v=VID.find(x=>!TIPO||x.file.startsWith(TIPO+'/')); if(v) abrir(v.file); }

async function actualizarBoton(){
  const r=await (await fetch('/api/export_estado')).json();
  $F('#bexp').textContent=`⬇ Generar Cortes (${r.pendientes}/${r.total})`;
}

function completo(file){ const s=(L[file]||{}).segmentos; return !!s && s.length>0 && s.every(x=>x.clase); }
function listar(){
  const d=$F('#lista'); d.querySelectorAll('.vi').forEach(e=>e.remove());
  const delTipo=VID.filter(x=>!TIPO||x.file.startsWith(TIPO+'/'));
  $F('#prog').textContent=`${delTipo.filter(x=>completo(x.file)).length}/${delTipo.length} completos`;
  delTipo.filter(x=>!filtro||String(x.id).includes(filtro)).forEach(x=>{
    const n=(L[x.file]?.segmentos||[]).filter(s=>s.clase).length;
    const nombre='#'+x.id;
    const e=document.createElement('div');
    e.className='vi'+(x.file===cur?' act':''); e.onclick=()=>abrir(x.file);
    e.innerHTML=`<span><b>${nombre}</b><br><small>${(x.dur_ms/1000).toFixed(1)}s · ${x.persona||'sin persona'}</small></span>
      <span class="fbadge ${n?'ok':''}">${n}</span>`;
    d.appendChild(e);
  });
}
$F('#filtro').addEventListener('input',e=>{filtro=e.target.value.trim();listar()});
function siguienteVideo(){
  const otros=VID.filter(x=>(!TIPO||x.file.startsWith(TIPO+'/')) && x.file!==cur && !completo(x.file));
  if(!otros.length) return;
  const cnt=f=>(L[f]?.segmentos||[]).filter(s=>s.clase).length;
  otros.sort((a,b)=>cnt(a.file)-cnt(b.file)); // prioriza los que tienen contador 0
  abrir(otros[0].file);
}
let PERSONAS=[];
async function cargarPersonas(){ try{ PERSONAS=(await (await fetch('/api/personas')).json()).personas; }catch(e){ PERSONAS=['P1','P2','P3','P4','P5']; } }
function pintarPersonaVid(){
  const x=VID.find(y=>y.file===cur), s=$F('#personaVid'); if(!s) return;
  s.innerHTML='<option value="">sin persona</option>'+PERSONAS.map(p=>`<option>${p}</option>`).join('');
  s.value=(x&&x.persona)||''; s.disabled=!x;
}
async function cambiarPersonaVid(){
  const x=VID.find(y=>y.file===cur); if(!x) return;
  const persona=$F('#personaVid').value||null;
  const r=await fetch('/api/raw/persona',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:x.id,persona})});
  if(!r.ok){ msg('⚠ '+((await r.json()).error||r.statusText)); pintarPersonaVid(); return; }
  x.persona=persona; msg(`Video ${x.id}: ${persona||'sin persona'}`); listar();
}
function abrir(file){ cur=file; sel=0; pintarPersonaVid(); curFps=(VID.find(x=>x.file===file)||{}).fps||0; v.src='/data/'+file; v.load(); listar(); cargarOverlay(file); }

// --- Overlay: esqueleto detectado dibujado en vivo sobre el video -----------
let OV=null, ovOn=true, ovPedido=0;
const cv=$F('#vover'), cx2=cv.getContext('2d');
let ejercicioActual='';

function toggleOverlay(){ ovOn=!ovOn; if(ovOn&&!OV&&cur) cargarOverlay(cur); dibujarOverlay(); }
async function cargarOverlay(file){
  OV=null; dibujarOverlay();
  if(!ovOn) return;
  const pedido=++ovPedido;
  estadoMano('detectando puntos… (la primera vez tarda)');
  try{
    const r=await (await fetch('/api/overlay?file='+encodeURIComponent(file))).json();
    if(pedido!==ovPedido) return;  // ya se abrio otro video
    OV=r.t_ms&&r.t_ms.length?r:null;
    ejercicioActual=r.exercise||ejercicioActual;
    estadoMano(OV?`puntos · ${r.t_ms.length} cuadros`:('sin puntos: '+(r.error||'')));
  }catch(e){ if(pedido===ovPedido) estadoMano('overlay: '+e.message); }
  dibujarOverlay();
}
function estadoMano(t){ const el=$F('#vmano'); el.textContent=t; el.style.display=t&&ovOn?'block':'none'; }
function idxCuadro(tms){  // ultimo cuadro detectado con t <= tms (busqueda binaria)
  const T=OV.t_ms; let lo=0, hi=T.length-1;
  if(tms<T[0]) return -1;
  while(lo<hi){ const m=(lo+hi+1)>>1; if(T[m]<=tms) lo=m; else hi=m-1; }
  return lo;
}
function dibujarOverlay(){
  const w=v.clientWidth, h=v.clientHeight;
  if(cv.width!==w||cv.height!==h){ cv.width=w; cv.height=h; cv.style.width=w+'px'; cv.style.height=h+'px'; }
  cx2.clearRect(0,0,w,h);
  if(!ovOn||!OV||!v.videoWidth) return;
  const i=idxCuadro(v.currentTime*1000);
  if(i<0 || v.currentTime*1000-OV.t_ms[i]>250) return;  // sin deteccion cerca de este instante
  // el video se ve con object-fit: contain -> calcular el rectangulo real de la imagen
  const esc=Math.min(w/v.videoWidth, h/v.videoHeight), vw=v.videoWidth*esc, vh=v.videoHeight*esc;
  const ox=(w-vw)/2, oy=(h-vh)/2, P=([x,y])=>[ox+x*vw, oy+y*vh];
  const linea=(pts,pares,color,grosor)=>{ cx2.strokeStyle=color; cx2.lineWidth=grosor; cx2.beginPath();
    pares.forEach(([a,b])=>{ const p=pts[a], q=pts[b]; if(p&&q&&p[0]!=null&&q[0]!=null){ const [x1,y1]=P(p),[x2,y2]=P(q); cx2.moveTo(x1,y1); cx2.lineTo(x2,y2);} });
    cx2.stroke(); };
  const puntos=(pts,color,r)=>{ cx2.fillStyle=color; pts.forEach(p=>{ if(p&&p[0]!=null){ const [x,y]=P(p); cx2.beginPath(); cx2.arc(x,y,r,0,7); cx2.fill(); } }); };
  // solo los puntos del catalogo del ejercicio: son los que se guardan y entrenan
  const pts=OV.puntos[i];
  linea(pts, OV.conexiones||[], '#4cff8a', 2.5); puntos(pts,'#ffffff',3.2);
}
addEventListener('resize', dibujarOverlay);
v.onloadedmetadata=()=>{ if(!L[cur]) L[cur]={segmentos:[{ini:0,fin:v.duration,clase:null,reps:0}]};
  const s=segs(); if(s.length) s[s.length-1].fin=Math.max(s[s.length-1].fin,v.duration); render(); };
function syncUI(){
  $F('#t').textContent=tc(v.currentTime)+' / '+tc(v.duration);
  $F('#vtime').textContent=tc(v.currentTime);
  const pct=(100*v.currentTime/(v.duration||1))+'%';
  $F('#play').style.left=pct; $F('#vprogfill').style.width=pct;
}
v.ontimeupdate=()=>{
  const s=segs()[sel];
  if(loopSeg&&s&&(v.currentTime>=s.fin-0.02||v.currentTime<s.ini-0.05)) v.currentTime=s.ini;
  syncUI();
};
v.onplay=v.onpause=()=>$F('#bpp').textContent=v.paused?'▶ Play':'⏸ Pausa';
requestAnimationFrame(function loopUI(){ if(!v.paused&&!v.ended) syncUI(); if(ovOn) dibujarOverlay(); requestAnimationFrame(loopUI); });
const pp=()=>v.paused?v.play():v.pause();
const sk=d=>v.currentTime=Math.min(Math.max(0,v.currentTime+d),v.duration||0);

const snap=t=>curFps>0?Math.round(t*curFps)/curFps:t;
function punto(t){
  t=snap(t??v.currentTime); const S=segs(), i=S.findIndex(s=>t>s.ini+0.05&&t<s.fin-0.05);
  if(i<0) return msg('Punto demasiado cerca de un corte existente');
  S.splice(i+1,0,{ini:t,fin:S[i].fin,clase:S[i].clase,reps:0});
  S[i].fin=t; sel=i+1; render();
}
function borrarPunto(i){ const S=segs(); if(i<1||i>=S.length) return;
  if(S[i].clase && !confirm(`El segmento ${i+1} ya esta clasificado como "${S[i].clase}". Quitar de todas formas?`)) return;
  S[i-1].fin=S[i].fin; S.splice(i,1); sel=Math.min(sel,S.length-1); render(); }
const borrarUlt=()=>borrarPunto(sel||1);

function ticks(){
  const el=$F('#tlticks'); el.innerHTML=''; if(!v.duration) return;
  const d=v.duration, step = d<=8?1 : d<=20?2 : d<=60?5 : d<=180?15:30;
  for(let t=0;t<=d+0.001;t+=step){
    const s=document.createElement('span');
    s.style.left=(100*Math.min(t,d)/d)+'%';
    s.textContent=(d<=8?t.toFixed(1):Math.round(t))+'s';
    el.appendChild(s);
  }
}
function render(){
  const S=segs(), tl=$F('#tl'); tl.querySelectorAll('.sg').forEach(e=>e.remove());
  const ca=$F('#cutabove'), cb=$F('#cutbelow');
  ca.querySelectorAll('.mb').forEach(e=>e.remove()); cb.querySelectorAll('.mb').forEach(e=>e.remove());
  ticks();
  const tb=$F('#tb'); tb.innerHTML='';
  S.forEach((s,i)=>{
    const bg=colorOf(s.clase);
    const pos=`left:${100*s.ini/v.duration}%;width:${100*(s.fin-s.ini)/v.duration}%;background:${bg}`;
    const d=document.createElement('div'); d.className='sg'+(i===sel?' sel':'');
    d.style.cssText+=pos;
    d.title=`#${i+1} ${s.clase||'sin clase'}`;
    d.innerHTML=`<b>${i+1}</b>`+(ICONS[s.clase]?`<i>${ICONS[s.clase]}</i>`:'');
    d.onclick=e=>{e.stopPropagation();sel=i;render()};
    tl.appendChild(d);
    const mb1=document.createElement('div'); mb1.className='mb'; mb1.style.cssText=pos; ca.appendChild(mb1);
    cb.appendChild(mb1.cloneNode());
    const opt=['<option value="">— sin clase —</option>'].concat(CFG.clases.map(c=>`<option ${c===s.clase?'selected':''}>${c}</option>`)).join('');
    const tr=document.createElement('tr'); tr.className=i===sel?'sel':'';
    tr.innerHTML=`<td><span class="sw" style="background:${bg}"></span></td><td>${i+1}</td><td>${f(s.ini)}</td><td>${f(s.fin)}</td><td>${f(s.fin-s.ini)}</td>
      <td><select>${opt}</select></td>
      <td><input type="number" min="0" value="${s.reps||0}"></td>
      <td><button title="Reproducir">▶</button>${i?'<button title="Quitar este corte">✖</button>':''}</td>`;
    const [cs,ri]=tr.querySelectorAll('select,input');
    cs.onchange=e=>{s.clase=e.target.value||null;render();if(segs().every(x=>x.clase))siguienteVideo()};
    ri.onchange=e=>{s.reps=+e.target.value;guardar()};
    const bs=tr.querySelectorAll('td:last-child button');
    bs[0].onclick=()=>{sel=i;v.currentTime=s.ini;v.play();render()};
    if(bs[1]) bs[1].onclick=()=>borrarPunto(i);
    tr.onclick=e=>{if(e.target.tagName=='TD'){sel=i;v.currentTime=s.ini;render()}};
    tb.appendChild(tr);
  });
  $F('#bl').className=loopSeg?'on':''; $F('#bv').className=v.loop?'on':'';
  resumen(); listar(); guardar();
}
function resumen(){
  const cont={}; CFG.clases.forEach(c=>cont[c]=0);
  Object.values(L).forEach(x=>(x.segmentos||[]).forEach(s=>{if(s.clase) cont[s.clase]=(cont[s.clase]||0)+1}));
  $F('#resumen').innerHTML=CFG.clases.map(c=>`<span class="legchip"><i style="background:${colorOf(c)}"></i>${ICONS[c]?ICONS[c]+' ':''}${c}: ${cont[c]||0}</span>`).join('');
}
const tlEl=$F('#tl');
let scrubbing=false;
function seekFromEvent(e){
  const r=tlEl.getBoundingClientRect();
  const x=Math.min(Math.max(e.clientX-r.left,0),r.width);
  v.currentTime=v.duration*x/r.width; syncUI();
}
tlEl.addEventListener('mousedown',e=>{scrubbing=true;seekFromEvent(e)});
addEventListener('mousemove',e=>{if(scrubbing)seekFromEvent(e)});
addEventListener('mouseup',()=>scrubbing=false);

function borrarCercaDe(t){
  const S=segs(); let bi=-1,bd=Infinity;
  for(let i=1;i<S.length;i++){ const d=Math.abs(S[i].ini-t); if(bi<0||d<bd){bi=i;bd=d;} }
  if(bi<0) return msg('No hay cortes para quitar');
  borrarPunto(bi);
}
function wireCutBar(bar,glyph,onClick){
  bar.addEventListener('mousemove',e=>{
    const r=bar.getBoundingClientRect(), pct=(100*Math.min(Math.max(e.clientX-r.left,0),r.width)/r.width)+'%';
    glyph.style.left=pct; glyph.style.display='block';
  });
  bar.addEventListener('mouseleave',()=>glyph.style.display='none');
  bar.addEventListener('click',e=>{
    const r=bar.getBoundingClientRect();
    onClick(v.duration*Math.min(Math.max(e.clientX-r.left,0),r.width)/r.width);
  });
}
wireCutBar($F('#cutbelow'),$F('#cbglyph'),t=>punto(t));
wireCutBar($F('#cutabove'),$F('#capglyph'),t=>borrarCercaDe(t));

function setZoom(z){
  zoom=Math.min(8,Math.max(1,z));
  $F('#tlinner').style.width=(zoom*100)+'%';
  $F('#zoomLbl').textContent=zoom.toFixed(1)+'x';
}
$F('#zoomIn').onclick=()=>setZoom(zoom+0.5);
$F('#zoomOut').onclick=()=>setZoom(zoom-0.5);
$F('#tlscroll').addEventListener('wheel',e=>{e.preventDefault();setZoom(zoom+(e.deltaY<0?0.5:-0.5))});

function guardar(){ clearTimeout(save); save=setTimeout(()=>
  fetch('/api/labels',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(L)}).then(actualizarBoton),400); }

// Vacia las tablas SQL de los clips y vuelve a cortar todo (cortes -> puntos -> tablas crudas y normalizadas)
async function rehacerTodo(){
  if(!confirm('BLANQUEAR las tablas SQL de los clips (frames crudos, normalizados, base e indicadores) y volver a cortar y cargar TODO desde cero?\n\nNo borra tus videos, tus etiquetas ni los ejercicios (.yaml).')) return;
  msg('Vaciando tablas SQL…');
  try{
    const r=await fetch('/api/sql/blanquear',{method:'POST'}); const j=await r.json();
    if(!r.ok) throw new Error(j.error||'error');
    msg('Tablas vaciadas ('+Object.values(j.borradas).reduce((a,b)=>a+b,0)+' filas). Regenerando…');
  }catch(e){
    if(!confirm('SQL no respondio ('+e.message+').\n¿Regenerar solo los cortes locales de todos modos? Las tablas SQL quedarian sin tocar.')) return;
  }
  await exportar(true,true);
  if(typeof cargarSql==='function') cargarSql(false);
}

async function exportar(todo=false, sinConfirmar=false){
  const n=Object.values(L).flatMap(x=>x.segmentos).filter(s=>s.clase&&!CFG.no_exportar.includes(s.clase)).length;
  if(!n) return msg('No hay segmentos clasificados para exportar');
  if(!sinConfirmar && !confirm(todo ? `Regenerar TODOS los cortes (${n} segmentos), aunque no hayan cambiado?` : `Cortar ${n} segmentos a input/bronze/<clase>/ ?`)) return;
  msg('Cortando con ffmpeg… (si faltan puntos, tambien se detectan: puede tardar mas)');
  const btns=[$F('#bexp'),$F('#bexpTodo')], txt0=btns.map(b=>b.textContent);
  btns.forEach(b=>b.disabled=true);
  const nv=Object.values(L).filter(x=>(x.segmentos||[]).some(s=>s.clase&&!CFG.no_exportar.includes(s.clase))).length;
  const pintar=(h,t,v)=>{ $F('#expProg').style.display='block'; $F('#expBar').style.width=(t?100*h/t:0)+'%';
    $F('#expTxt').textContent=`⏳ Video ${h}/${t}`; $F('#expVid').textContent=v?v.split('/').pop():'';
    btns.forEach(b=>b.textContent=`⏳ Video ${h}/${t}`); msg(`Cortando… ${h}/${t} videos${v?' · '+v.split('/').pop():''}`); };
  pintar(0,nv,'');   // se ve al instante, antes de la primera respuesta del servidor
  const sondeo=setInterval(async()=>{
    try{ const p=await (await fetch('/api/export_progreso',{cache:'no-store'})).json(); if(p.activo) pintar(p.hecho,p.total,p.video); }catch(e){}
  },400);
  let r;
  try{ r=await (await fetch('/api/export'+(todo?'?todo=true':''),{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(L)})).json(); }
  finally{ clearInterval(sondeo); $F('#expProg').style.display='none'; btns.forEach((b,i)=>{b.disabled=false; b.textContent=txt0[i];}); }
  const sql = r.sql ? ` · SQL: ${r.sql.archivos_nuevos+r.sql.archivos_actualizados} clips subidos` : (r.sql_error ? ` · SQL no disponible: ${r.sql_error}` : '');
  const detErr = Object.values(r.deteccion_errores||{});
  const det = detErr.length ? ` · deteccion de puntos fallo en ${detErr.length} video(s): ${detErr[0]}` : '';
  msg(`Listo: ${r.clips} clips en dataset/ + ${r.manifest}`+(r.saltados?` · ${r.saltados} videos sin cambios (no se repitieron)`:'')+(r.errores.length?` · ${r.errores.length} errores: ${r.errores[0]}`:'')+sql+det);
  actualizarBoton();
}

addEventListener('keydown',e=>{
  if(/INPUT|SELECT/.test(e.target.tagName)) return;
  if($F('#app').style.display==='none') return;  // atajos del cortador solo en su pestana
  const S=segs(), k=e.key;
  if(k.toLowerCase()=='m'){ toggleOverlay(); e.preventDefault(); return; }
  if(k==' '){e.preventDefault();pp()}
  else if(k=='ArrowLeft') sk(e.shiftKey?-1:-.1);
  else if(k=='ArrowRight') sk(e.shiftKey?1:.1);
  else if(k.toLowerCase()=='p') punto();
  else if(k.toLowerCase()=='l'){loopSeg=!loopSeg;render()}
  else if(k=='Delete') borrarPunto(sel);
  else if(k>='1'&&k<='9'&&CFG.clases[k-1]&&S[sel]){S[sel].clase=CFG.clases[k-1];render()}
  else return;
  e.preventDefault();
});
