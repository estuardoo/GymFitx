/* Pestana Ranking: corridas ordenadas por F1 macro. API: /api/entrenamientos */
function configTexto(m){
  const c=m.config; if(!c) return '—';
  const base=c.modo==='punto' ? `punto: ${c.punto_centro}-${c.punto_escala_a}-${c.punto_escala_b}` : `rect ${c.ancho&&c.alto?`${c.ancho}x${c.alto}`:'100x100'}`;
  return `${base} · ${c.n_frames_fijo}f`;
}

async function cargarRanking(){
  const hs=await (await fetch('/api/entrenamientos')).json();
  // ranking por F1 macro (con clases desbalanceadas la accuracy engana)
  const f1de=m=>m.f1_macro??(m.reporte&&m.reporte['macro avg']?m.reporte['macro avg']['f1-score']:-1);
  const ord=hs.slice().sort((a,b)=>f1de(b)-f1de(a));
  const tb=$F('#rankhist'); tb.innerHTML='';
  ord.forEach((m,i)=>{
    const f1m=m.reporte&&m.reporte['macro avg']?m.reporte['macro avg']['f1-score']*100:null;
    const tr=document.createElement('tr');
    if(i===0) tr.className='rank-mejor';
    tr.innerHTML=`<td>#${m.numero}</td><td>${m.exercise||'—'}</td><td>${configTexto(m)}</td><td>${m.mejor_modelo||'—'}</td><td>${(m.accuracy*100).toFixed(1)}%</td><td>${f1m!=null?f1m.toFixed(1)+'%':'—'}</td><td>${m.errores!=null?m.errores+'/'+m.n_muestras:'—'}</td><td>${m.fecha.replace('T',' ')}</td>`;
    tr.onclick=()=>mostrarRanking(m);
    tb.appendChild(tr);
  });
  if(ord.length) mostrarRanking(ord[0]); else $F('#rankres').style.display='none';
}

function mostrarRanking(m){
  $F('#rankres').style.display='block';
  $F('#ranknum').textContent='#'+m.numero;
  $F('#rankmodelo').textContent=m.mejor_modelo||'—';
  $F('#rankerrores').textContent=m.errores!=null?`${m.errores}/${m.n_muestras} errores (${(100*m.errores/m.n_muestras).toFixed(1)}%)`:'este entrenamiento no guardo el detalle por clip';
  $F('#rimgConf').src=`/entrenamientos/run_${m.numero}/confusion.png?t=${Date.now()}`;
  $F('#rankclips').innerHTML=(m.predicciones||[]).map(p=>
    `<tr${p.ok?'':' class="errfila"'}><td>${p.clip}</td><td>${p.real}</td><td>${p.prediccion}</td><td>${p.ok?'<span class="okmark">✓</span>':'<span class="errmark">✗</span>'}</td></tr>`).join('');
}
