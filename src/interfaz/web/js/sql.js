/* Sistema → Tablas del dataset: normalizacion por ejercicio y generar tablas. API: /api/sql/* */
function cambiarModoSql(){
  const rect=$F('#sqlModo').value==='rectangulo';
  $F('#sqlModoRect').style.display=rect?'flex':'none';
  $F('#sqlModoPunto').style.display=rect?'none':'flex';
}

async function cargarSql(mostrarResumen=true){
  const tSel=$F('#sqlTipo').value;
  const e=await (await fetch('/api/sql/estado'+(tSel?`?tipo=${tSel}`:''))).json();
  const tipos=e.tipos||{};
  $F('#sqlTipo').innerHTML=Object.entries(tipos).map(([t,ej])=>`<option value="${t}" ${+t===e.tipo?'selected':''}>${ej} (type ${t})</option>`).join('')||'<option value="">(sin clips)</option>';
  $F('#sqlstatus').innerHTML = e.conectado
    ? `<span class="okmark">✓ conectado</span>${e.tablas_faltantes.length?' · tablas por crear: '+e.tablas_faltantes.join(', '):' · tablas listas'}`
    : `<span class="errmark">✗ sin conexion</span> — ${e.error||''}`;
  const puntos=e.puntos_disponibles||[];
  const opt=n=>puntos.map(p=>`<option ${p===n?'selected':''}>${p}</option>`).join('');
  if(!puntos.length){
    $F('#sqlCentro').innerHTML=$F('#sqlEscA').innerHTML=$F('#sqlEscB').innerHTML='<option>— exporta un clip primero —</option>';
  }else{
    $F('#sqlCentro').innerHTML=opt(e.config.punto_centro);
    $F('#sqlEscA').innerHTML=opt(e.config.punto_escala_a);
    $F('#sqlEscB').innerHTML=opt(e.config.punto_escala_b);
  }
  $F('#sqlModo').value=e.config.modo||'rectangulo';
  $F('#sqlNFrames').value=e.config.n_frames_fijo;
  cambiarModoSql();
  if(mostrarResumen) $F('#sqlresumen').textContent = e.clips_totales
    ? `${e.clips_totales} clips exportados · ${e.clips_sin_puntos_crudos} sin puntos crudos (grabados antes de esta funcion, no se pueden completar retroactivamente)`
    : 'Todavia no hay clips exportados.';
}

function configSqlActual(){
  return {modo:$F('#sqlModo').value, n_frames_fijo:+$F('#sqlNFrames').value||30,
          punto_centro:$F('#sqlCentro').value, punto_escala_a:$F('#sqlEscA').value, punto_escala_b:$F('#sqlEscB').value,
          puntos_caja: null};   // siempre todos los puntos del catalogo (pestaña Puntos)
}

async function guardarConfigSql(){
  const tSel=$F('#sqlTipo').value;
  const j=await (await fetch('/api/sql/config'+(tSel?`?tipo=${tSel}`:''),{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(configSqlActual())})).json();
  msg(j.aviso||'Configuracion guardada');
}

// Ejercicios archivados que aun dejan clips o datos: ver cuantos son, confirmar y quitarlos del manifest y de SQL
async function depurarArchivados(){
  const plan=await (await fetch('/api/archivados/plan')).json();
  if(!plan.length){ $F('#sqlresumen').textContent='No hay ejercicios archivados con datos pendientes.'; return; }
  const txt=plan.map(d=>`• ${d.slug}: ${d.clips_manifest} clips en el manifest, ${d.clips_disco} en disco`+(d.sql_archivos==null?'':`, ${d.sql_archivos} en SQL`)).join('\n');
  if(!confirm(`Se quitan del manifest y de SQL (todas sus tablas) estos ejercicios, que ya no estan en la rutina:\n\n${txt}\n\nLos archivos pasan a datos/archivados/ (no se borran). ¿Continuar?`)) return;
  $F('#bdepurar').disabled=true;
  try{
    const r=await fetch('/api/archivados/depurar',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'});
    const j=await r.json();
    if(!r.ok) throw new Error(j.error||j.detail||'error desconocido');
    const pend=j.filter(x=>x.sql_error||x.errores.length);
    $F('#sqlresumen').textContent=`Listo: ${j.length} ejercicio(s) quitados · ${j.reduce((a,x)=>a+x.clips,0)} clips del manifest · ${j.reduce((a,x)=>a+(x.sql?x.sql.archivos:0),0)} archivos de SQL`+(pend.length?` · ATENCION: ${pend.length} quedaron pendientes (${pend[0].sql_error||pend[0].errores[0]}); vuelve a pulsar el boton`:'');
    msg('Archivados depurados');
  }catch(e){ msg('Error: '+e.message); }
  $F('#bdepurar').disabled=false;
  cargarSql(false);
}

async function generarSql(){
  await guardarConfigSql();
  $F('#bsqlgen').disabled=true; $F('#bsqlgen').textContent='Generando…';
  try{
    const r=await fetch('/api/sql/generar',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'});
    const j=await r.json();
    if(!r.ok) throw new Error(j.error||'error desconocido');
    const detErr = Object.values(j.deteccion_errores||{});
    $F('#sqlresumen').textContent=`Listo: ${j.archivos_nuevos} nuevos · ${j.archivos_actualizados} actualizados · ${j.archivos_sin_cambios} sin cambios (misma configuracion) · ${j.frames} frames crudos · ${j.frames_fix} frames normalizados`+(j.omitidos_sin_puntos?` · ${j.omitidos_sin_puntos} clips omitidos (sin puntos crudos)`:'')+(detErr.length?` · ATENCION: deteccion fallo en ${detErr.length} video(s) -- ${detErr[0]}`:'');
    msg('Tablas SQL actualizadas');
  }catch(e){ msg('Error: '+e.message); }
  $F('#bsqlgen').disabled=false; $F('#bsqlgen').textContent='🗄️ Generar / actualizar tablas';
  cargarSql(false);
}
