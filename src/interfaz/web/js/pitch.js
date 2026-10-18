/* Pestana Pitch: laminas del .pptx. API: /api/pitch */
// --- modulo Pitch: las laminas del .pptx, ya convertidas a PNG, dentro de la
// misma ventana (flechas, miniaturas y pantalla completa) ------------------
let LAMINAS=[], lamina=0;
async function verPitch(){
  mostrarVista('pitch'); v.pause();
  if(!LAMINAS.length){
    const r=await (await fetch('/api/pitch')).json();
    LAMINAS=r.laminas||[];
    $F('#pitchPptx').style.display = r.pptx ? '' : 'none';
    if(r.pptx) $F('#pitchPptx').href='/pitch/'+encodeURIComponent(r.pptx);
    $F('#pitchMinis').innerHTML=LAMINAS.map((n,i)=>`<img src="/pitch/${encodeURIComponent(n)}" onclick="irLamina(${i})" data-i="${i}">`).join('');
  }
  irLamina(lamina);
}
function irLamina(i){
  if(!LAMINAS.length){ $F('#pitchInfo').textContent='No hay laminas en la carpeta pitch/'; return; }
  lamina=Math.min(LAMINAS.length-1, Math.max(0, i));
  $F('#pitchImg').src='/pitch/'+encodeURIComponent(LAMINAS[lamina]);
  $F('#pitchNum').textContent=`${lamina+1} / ${LAMINAS.length}`;
  $F('#pitchInfo').textContent=`${LAMINAS.length} laminas · flechas ← → para pasar`;
  $F('#pitchMinis').querySelectorAll('img').forEach(e=>e.classList.toggle('act', +e.dataset.i===lamina));
}
const pasarLamina=d=>irLamina(lamina+d);
function pantallaCompletaPitch(){
  const el=$F('#pitchWrap');
  document.fullscreenElement ? document.exitFullscreen() : el.requestFullscreen?.();
}
addEventListener('keydown',e=>{
  if($F('#pitchview').style.display==='none' || /INPUT|SELECT/.test(e.target.tagName)) return;
  if(e.key==='ArrowLeft'||e.key==='PageUp'){ pasarLamina(-1); e.preventDefault(); }
  else if(e.key==='ArrowRight'||e.key==='PageDown'||e.key===' '){ pasarLamina(1); e.preventDefault(); }
});
