/* Pestana Entrenamiento: clips a usar, modelos y corridas. API: interfaz/api/entrenamiento.py */
let modelosCargados=false;
async function cargarModelos(){
  if(modelosCargados) return;
  const ms=await (await fetch('/api/modelos')).json();
  const cont=$F('#modelchecks');
  if(!ms.length){ cont.innerHTML='<span class="hint">No se pudo listar modelos (revisa que scikit-learn este instalado)</span>'; return; }
  cont.innerHTML=ms.map(m=>`<label class="mchk"><input type="checkbox" value="${m}" checked> ${m}</label>`).join('')+
    '<button type="button" class="mtodos" onclick="document.querySelectorAll(\'#modelchecks input\').forEach(c=>{c.checked=true})">Activar todos</button>';
  modelosCargados=true;
}

async function cargarTipos(){
  const tipos=await (await fetch('/api/tipos')).json();  // {type: ejercicio}
  const sel=$F('#trainTipo');
  const actual=sel.value;
  sel.innerHTML=Object.entries(tipos).map(([t,ej])=>`<option value="${t}">(${t}) ${ej}</option>`).join('')
    || '<option value="">(sin ejercicios exportados)</option>';
  const zancada=Object.entries(tipos).find(([,ej])=>ej==='zancada');   // zancada por defecto
  if([...sel.options].some(o=>o.value===actual)) sel.value=actual;
  else if(zancada) sel.value=zancada[0];
  sel.onchange=cargarClipsTrain;
}

// --- Clips para entrenar: marcar/desmarcar con clic y ver cada uno ----------
let TCLIPS=[], tclipActual=null;
async function cargarClipsTrain(){
  const t=$F('#trainTipo').value;
  TCLIPS=await (await fetch('/api/entrenar/clips'+(t?`?tipo=${t}`:''))).json();
  const cs=[...new Set(TCLIPS.map(c=>c.clase))].sort(), actual=$F('#tclipsClase').value;
  $F('#tclipsClase').innerHTML='<option value="">todas</option>'+cs.map(c=>`<option ${c===actual?'selected':''}>${c}</option>`).join('');
  renderClipsTrain();
}
function clipsVisibles(){
  const cl=$F('#tclipsClase').value, ver=$F('#tclipsVer').value, fl=$F('#tclipsFiltro').value.trim().toLowerCase();
  return TCLIPS.filter(c=>(!cl||c.clase===cl) && (!ver||(ver==='si')===c.usar) && (!fl||c.clip.toLowerCase().includes(fl)));
}
function renderVideosTrain(){
  const porVideo={};
  TCLIPS.forEach(c=>{ (porVideo[c.origen]=porVideo[c.origen]||[]).push(c); });
  // de mayor a menor cantidad de clips; el nombre no repite el ejercicio, ya elegido arriba en el selector
  const entradas=Object.entries(porVideo).sort((a,b)=>b[1].length-a[1].length);
  $F('#tclipsVideos').innerHTML=entradas.map(([vid,cs],i)=>{
    const n=cs.filter(c=>c.usar).length;
    const nombre=vid.replace('.mp4','').split('/').slice(1).join('/');
    return `<tr data-i="${i}" class="${n?'':'off'}"><td><input type="checkbox" ${n?'checked':''} ${n&&n<cs.length?'data-parcial="1"':''}></td>`+
           `<td>${nombre}</td><td>${n}/${cs.length}</td></tr>`;
  }).join('') || '<tr><td colspan="3" class="hint">—</td></tr>';
  const grupos=entradas.map(([,cs])=>cs);
  $F('#tclipsVideos').querySelectorAll('tr[data-i]').forEach(tr=>{
    const cs=grupos[+tr.dataset.i], chk=tr.querySelector('input');
    chk.indeterminate = cs.some(c=>c.usar) && cs.some(c=>!c.usar);
    chk.onclick=e=>{e.stopPropagation(); marcarClips(cs, e.target.checked);};
  });
}

function renderClipsTrain(){
  renderVideosTrain();
  const vis=clipsVisibles();
  $F('#tclipsBody').innerHTML=vis.map((c,i)=>
    `<tr data-i="${i}" class="${c.usar?'':'off'} ${c.clip===tclipActual?'viendo':''}"><td><input type="checkbox" ${c.usar?'checked':''}></td>`+
    `<td>${c.clip.split('/').pop()}</td><td><span class="sw" style="background:${colorOf(c.clase)}"></span> ${c.clase}</td><td>${f(c.dur)}s</td></tr>`).join('')
    || '<tr><td colspan="4" class="hint">Sin clips para este ejercicio -- genera los cortes primero.</td></tr>';
  $F('#tclipsBody').querySelectorAll('tr[data-i]').forEach(tr=>{
    const c=vis[+tr.dataset.i];
    tr.querySelector('input').onclick=e=>{e.stopPropagation(); marcarClips([c], e.target.checked);};
    tr.onclick=()=>verClipTrain(c);
  });
  const usados=TCLIPS.filter(c=>c.usar), porClase={};
  usados.forEach(c=>porClase[c.clase]=(porClase[c.clase]||0)+1);
  $F('#tclipsInfo').textContent=`${usados.length}/${TCLIPS.length} marcados · `+Object.entries(porClase).map(([k,n])=>`${k}: ${n}`).join(' · ');
}
async function marcarClips(lista, usar){
  if(!lista.length) return;
  const cambios={}; lista.forEach(c=>{c.usar=usar; cambios[c.clip]=usar;});
  renderClipsTrain();
  const t=$F('#trainTipo').value;
  await fetch('/api/entrenar/seleccion',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({cambios, tipo:t?+t:null})});
}
const marcarClipsVisibles=usar=>marcarClips(clipsVisibles(), usar);
function verClipTrain(c){
  tclipActual=c.clip;
  const vid=$F('#tclipVideo'); vid.src='/dataset/'+c.clip.split('/').map(encodeURIComponent).join('/'); vid.play().catch(()=>{});
  $F('#tclipNombre').textContent=`${c.clip} · ${c.clase} · origen ${c.origen} (${f(c.ini)}–${f(c.fin)}s)`;
  renderClipsTrain();
}
function navClipTrain(d){
  const vis=clipsVisibles(); if(!vis.length) return;
  const i=vis.findIndex(c=>c.clip===tclipActual);
  verClipTrain(vis[Math.min(vis.length-1, Math.max(0, i<0?0:i+d))]);
}
function toggleClipActual(){
  const c=TCLIPS.find(x=>x.clip===tclipActual); if(c) marcarClips([c], !c.usar);
}
addEventListener('keydown',e=>{
  if($F('#trainview').style.display==='none' || /INPUT|SELECT/.test(e.target.tagName)) return;
  if(e.key.toLowerCase()==='u'){ toggleClipActual(); e.preventDefault(); }
  else if(e.key==='ArrowDown'){ navClipTrain(1); e.preventDefault(); }
  else if(e.key==='ArrowUp'){ navClipTrain(-1); e.preventDefault(); }
});

$F('#testpct').oninput=()=>{ const p=+$F('#testpct').value||20; $F('#kinfo').textContent=`≈ ${Math.max(2,Math.round(100/p))}-fold`; };
$F('#testpct').oninput();

const esc=t=>String(t).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
// [1,2,3,5] -> "1-3|5"
function rangos(ns){ const o=[]; for(let i=0;i<ns.length;){ let j=i; while(j+1<ns.length&&ns[j+1]===ns[j]+1) j++; o.push(j>i?`${ns[i]}-${ns[j]}`:`${ns[i]}`); i=j+1; } return o.join('|'); }
function vsAnterior(v){
  if(!v) return '<span class="hint">primer entrenamiento</span>';
  const ico={mejoro:'▲ mejoró',empeoro:'▼ empeoró',igual:'≈ igual'}[v.veredicto];
  const col={mejoro:'#1a7f4b',empeoro:'#c0392b',igual:'inherit'}[v.veredicto];
  const d=x=>(x>=0?'+':'')+(x*100).toFixed(1);
  return `<b style="color:${col}">${ico}</b> vs #${v.contra}<br><span class="hint">F1 ${d(v.delta_f1)} · acc ${d(v.delta_accuracy)}`+
    (v.delta_anidado!=null?` · anidada ${d(v.delta_anidado)}`:'')+(v.veredicto==='igual'?` · ruido ±${(v.ruido*100).toFixed(1)}`:'')+`<br>${v.cambios.length?esc(v.cambios.join('; ')):'sin cambios de parámetros'}</span>`;
}

async function cargarEntrenamientos(){
  const hs=await (await fetch('/api/entrenamientos')).json();
  const tb=$F('#trainhist'); tb.innerHTML='';
  hs.slice().reverse().forEach(m=>{
    const tr=document.createElement('tr'), P=m.parametros||{};
    const pct1=v=>v!=null?(v*100).toFixed(1)+'%':'—';
    const kp=P.kpoints, an=P.angulos;
    const kpTxt=kp==null?'?':(kp.length?`${kp.length}: ${rangos(kp.map((_,i)=>i+1))}`:'—');
    const _n=t=>an.filter(a=>a[2]===t||(t==='angle'&&!a[2])).length;
    const anTxt=an==null?'?':(an.length?`<b>${an.length}</b> <span class="hint">(∠ ${_n('angle')} · % ${_n('proporcion')}${_n('distance_ratio')?' · ÷ '+_n('distance_ratio'):''})</span><br>`+an.map(a=>`<span class="cod" title="${esc(a[0])}">${esc(a[1])}</span>`).join(' '):'sin angulos activos');
    const clips=P.clips?Object.entries(P.clips).map(([c,n])=>`${c} ${n}`).join(' · '):'—';
    tr.innerHTML=`<td>#${m.numero}</td><td>${m.fecha.replace('T',' ')}</td>`+
      `<td style="min-width:230px">${vsAnterior(m.vs_anterior)}</td><td>${m.mejor_modelo||'—'}</td>`+
      `<td>${pct1(m.accuracy)}</td><td>${pct1(m.f1_macro)}${m.f1_std!=null?` <span class="hint">±${(m.f1_std*100).toFixed(1)}</span>`:''}</td>`+
      `<td>${pct1(m.anidado&&m.anidado.f1_macro)}</td>`+
      `<td>${m.linea_base?`${pct1(m.linea_base.f1_macro)} <span class="hint">(${(m.f1_macro>=m.linea_base.f1_macro?'+':'')}${((m.f1_macro-m.linea_base.f1_macro)*100).toFixed(1)})</span>`:'—'}</td>`+
      `<td>${pct1(m.reporte&&m.reporte.mal&&m.reporte.mal.recall)}</td><td>${pct1(m.reporte&&m.reporte.bien&&m.reporte.bien.precision)}</td>`+
      `<td>${P.frames??'—'}</td>`+
      `<td title="${esc((kp||[]).map((n,i)=>(i+1)+' '+n).join('\n'))}">${kpTxt}</td>`+
      `<td title="${esc((an||[]).map(a=>(a[2]==='proporcion'?'% ':'∠ ')+a[0]+' ('+a[1]+')').join('\n'))}" style="max-width:260px;overflow-wrap:anywhere">${anTxt}</td>`+
      `<td>${clips}</td>`;
    tr.onclick=()=>mostrarEntrenamiento(m);
    tb.appendChild(tr);
  });
  if(hs.length) mostrarEntrenamiento(hs[hs.length-1]); else $F('#trainres').style.display='none';
}

// "min–max (media) / tope": cuantas iteraciones uso cada modelo en los folds y si freno antes del tope
const itTxt=i=>!i?'—':`${i.min===i.max?i.max:i.min+'–'+i.max} / ${i.tope}${i.freno?' ⏹':''}`;

function mostrarEntrenamiento(m){
  $F('#trainres').style.display='block';
  $F('#trainnum').textContent='#'+m.numero;
  $F('#trainbest').textContent=m.mejor_modelo||'—';
  $F('#trainacc').textContent=(m.accuracy*100).toFixed(1)+'%';
  const pct=v=>v==null?'—':(v*100).toFixed(1)+'%';
  $F('#trainf1').textContent=pct(m.f1_macro);
  $F('#trainbase').textContent=m.linea_base?`F1 ${pct(m.linea_base.f1_macro)} · acc ${pct(m.linea_base.accuracy)}`:'— (corrida vieja)';
  $F('#trainanid').textContent=m.anidado?`F1 ${pct(m.anidado.f1_macro)} · acc ${pct(m.anidado.accuracy)}`:(m.criterio?'— (muy pocos clips)':'— (corrida vieja)');
  $F('#trainmeta').textContent=`${m.n_muestras} clips · ${m.k}-fold (test ${m.test_pct}%) · features: ${featTxt(m.features)} · ${m.fecha.replace('T',' ')}`+(m.excluidas&&m.excluidas.length?` · excluidas por pocos clips: ${m.excluidas.join(', ')}`:'')+(m.excluidos_manual&&m.excluidos_manual.length?` · ${m.excluidos_manual.length} clips desmarcados`:'')+(m.desincronizados&&m.desincronizados.length?` · ⚠ ${m.desincronizados.length} clips quedaron fuera por estar con otro catalogo de puntos: dale a "Generar cortes" y luego a "Generar / actualizar tablas"`:'');
  const ord=(m.modelos||[]).slice().sort((a,b)=>(b.f1_macro??-1)-(a.f1_macro??-1));
  $F('#trainmodels').innerHTML=ord.map(mm=>
    `<tr${mm.nombre===m.mejor_modelo?' class="sel"':''}><td>${mm.nombre}</td><td>${mm.error?'—':(mm.accuracy*100).toFixed(1)+'%'}</td><td>${mm.error?'—':(mm.f1_macro*100).toFixed(1)+'%'}</td><td>${itTxt(mm.iteraciones)}</td><td>${mm.error?'error: '+mm.error:mm.tiempo_seg+'s'}</td></tr>`).join('');
  const im=m.iteraciones_mejor;
  $F('#trainiters').textContent=im?`${im.usadas} de ${im.tope}${im.usadas<im.tope?' (frenó antes)':' (llegó al tope)'}`:'— (no itera / corrida vieja)';
  $F('#imgComp').src=`/entrenamientos/run_${m.numero}/comparacion.png?t=${Date.now()}`;
  $F('#trainrep').innerHTML=Object.entries(m.reporte).filter(([k])=>!['accuracy'].includes(k)).map(([cl,r])=>
    `<tr><td>${cl}</td><td>${(r.precision*100).toFixed(0)}%</td><td>${(r.recall*100).toFixed(0)}%</td><td>${(r['f1-score']*100).toFixed(0)}%</td><td>${r.support}</td></tr>`).join('');
  $F('#imgConf').src=`/entrenamientos/run_${m.numero}/confusion.png?t=${Date.now()}`;
  $F('#imgRoc').src=`/entrenamientos/run_${m.numero}/roc.png?t=${Date.now()}`;
}

// lo que entra al vector: letras x,y,z (ejes de cada kpoint), a (angulos), p (proporciones)
const featSel=()=>[...document.querySelectorAll('#featchecks input:checked')].map(c=>c.value).join('');
const _FEAT_LEGADO={puntos:'xyz',angulos:'ap',ambos:'xyzap'};
const featTxt=f=>{ const u=_FEAT_LEGADO[f]||f||'xyz'; const ej=[...'xyz'].filter(c=>u.includes(c)).join(' ').toUpperCase();
  return [ej&&('kpoints '+ej), u.includes('a')&&'∠', u.includes('p')&&'%'].filter(Boolean).join(' + ')||'—'; };

async function entrenar(){
  if(!featSel()) return msg('Activa al menos una cosa para el modelo: X, Y, Z, angulos o proporciones');
  const pct=+$F('#testpct').value||20;
  const modelos=[...document.querySelectorAll('#modelchecks input:checked')].map(c=>c.value);
  if(!modelos.length) return msg('Selecciona al menos un modelo');
  $F('#btrain').disabled=true; $F('#btrain').textContent='Entrenando…';
  try{
    const tipo=$F('#trainTipo').value;
    const resp=await fetch('/api/entrenar',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({test_pct:pct, modelos, tipo:tipo?+tipo:null, features:featSel()})});
    const m=await resp.json();
    if(!resp.ok) throw new Error(m.error||'error desconocido');
    await cargarEntrenamientos();
    msg(`Entrenamiento #${m.numero} listo: ${m.mejor_modelo} · F1 ${(m.f1_macro*100).toFixed(1)}% (línea base ${(m.linea_base.f1_macro*100).toFixed(1)}%)`+(m.anidado?` · CV anidada F1 ${(m.anidado.f1_macro*100).toFixed(1)}%`:'')+(m.vs_anterior?` · ${{mejoro:'MEJORÓ',empeoro:'EMPEORÓ',igual:'igual'}[m.vs_anterior.veredicto]} vs #${m.vs_anterior.contra} (F1 ${(m.vs_anterior.delta_f1>=0?'+':'')}${(m.vs_anterior.delta_f1*100).toFixed(1)})`:''));
  }catch(e){ msg('Error al entrenar: '+e.message); }
  $F('#btrain').disabled=false; $F('#btrain').textContent='▶ Entrenar';
}
