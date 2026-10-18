/* Pestana AHPC: arma el paquete listo para el cluster (datos .npz + script busqueda_features_slurm.py +
   .sbatch por ejercicio). API: interfaz/api/ahpc.py -- este modulo no toca cortes/tablas, solo empaqueta
   lo que ya esta en SQL. */

async function cargarAhpc(){
  const cont=$F('#ahpcLista');
  cont.innerHTML='<span class="hint">Cargando…</span>';
  const filas=await (await fetch('/api/ahpc/ejercicios')).json();
  if(!filas.length){ cont.innerHTML='<span class="hint">Sin clips en el manifest todavia -- corta algun video primero.</span>'; return; }
  cont.innerHTML=`<table><thead><tr><th></th><th>Ejercicio</th><th>Clips</th><th></th></tr></thead><tbody>${
    filas.map(f=>`<tr>
      <td><input type="checkbox" class="ahpcChk" value="${esc(f.ejercicio)}" ${f.listo?'checked':'disabled'}></td>
      <td>${esc(f.ejercicio)}</td>
      <td>${f.clips}</td>
      <td>${f.listo?'':'<span class="hint">sin catalogo de kpoints</span>'}</td>
    </tr>`).join('')
  }</tbody></table>`;
}
function ahpcTodos(marcar){ document.querySelectorAll('.ahpcChk:not(:disabled)').forEach(c=>c.checked=marcar); }

async function ahpcDescargar(){
  const ejercicios=[...document.querySelectorAll('.ahpcChk:checked')].map(c=>c.value);
  if(!ejercicios.length) return msg('Elige al menos un ejercicio');
  const b=$F('#bahpc'); b.disabled=true; b.textContent='Empaquetando…';
  $F('#ahpcMsg').textContent='';
  try{
    const r=await fetch('/api/ahpc/exportar',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({ejercicios})});
    if(!r.ok){ const j=await r.json().catch(()=>({})); throw new Error(j.error||'error desconocido'); }
    const cd=r.headers.get('Content-Disposition')||'';
    const nombre=(cd.match(/filename="([^"]+)"/)||[])[1]||'ahpc_slurm.zip';
    const errores=r.headers.get('X-Ahpc-Errores');
    const blob=await r.blob();
    const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download=nombre;
    document.body.appendChild(a); a.click(); a.remove();
    msg(errores?`Descargado: ${nombre} -- fallaron: ${Object.keys(JSON.parse(errores)).join(', ')}`:`Descargado: ${nombre}`);
  }catch(e){ msg('Error: '+e.message); }
  b.disabled=false; b.textContent='⬇ Descargar paquete SLURM';
}
