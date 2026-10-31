/* Cambio de pestanas del dataset y entrada directa por #hash. Va al final: usa funciones de todos los anteriores. */

// En algunos navegadores, tocar un <video> (click para reproducir/pausar, o terminar solo) le da foco al
// control nativo y el navegador hace scroll para mantenerlo visible -- eso es lo que se ve como "la barra
// se baja"/"sale de foco". El scroll lo dispara el propio click/foco, ANTES de que 'play' llegue a
// avisar -- por eso se fija la posicion en 'pointerdown' (lo primero que pasa al hacer click) y se
// reimpone un cuadro despues (cuando el navegador ya intento moverla), y de nuevo en 'play'/'pause'/
// 'ended' por si el salto llega mas tarde. Aplica a los 4 <video> del dataset (Cut/Edit, SIM, Ranking,
// Entrenamiento), no solo a SIM.
document.querySelectorAll('video').forEach(vid=>{
  const fijar=()=>{ const x=window.scrollX, y=window.scrollY; requestAnimationFrame(()=>window.scrollTo(x, y)); };
  ['pointerdown', 'play', 'pause', 'ended'].forEach(ev=>vid.addEventListener(ev, fijar));
});

function mostrarVista(v){
  // pestanas nativas de GYMFITX (Panel/Sistema) se ocultan al entrar a una vista de dataset
  ["tab-panel","tab-sistema"].forEach(id=>{const e=document.getElementById(id); if(e) e.style.display='none';});
  ["tab-btn-panel","tab-btn-sistema"].forEach(id=>{const e=document.getElementById(id); if(e) e.classList.remove('act');});
  $F('#app').style.display = v==='videos' ? 'flex' : 'none';
  $F('#simview').style.display = v==='sim' ? 'block' : 'none';
  $F('#trainview').style.display = v==='train' ? 'block' : 'none';
  $F('#rankview').style.display = v==='rank' ? 'block' : 'none';
  $F('#descompview').style.display = v==='descomp' ? 'block' : 'none';
  $F('#puntosview').style.display = v==='puntos' ? 'block' : 'none';
  $F('#pipeview').style.display = v==='pipe' ? 'block' : 'none';
  $F('#pitchview').style.display = v==='pitch' ? 'block' : 'none';
  $F('#ahpcview').style.display = v==='ahpc' ? 'block' : 'none';
  $F('#tabPuntos').classList.toggle('act', v==='puntos');
  $F('#tabVideos').classList.toggle('act', v==='videos');
  $F('#tabSim').classList.toggle('act', v==='sim');
  $F('#tabTrain').classList.toggle('act', v==='train');
  $F('#tabRank').classList.toggle('act', v==='rank');
  $F('#tabDescomp').classList.toggle('act', v==='descomp');
  $F('#tabPipe').classList.toggle('act', v==='pipe');
  $F('#tabPitch').classList.toggle('act', v==='pitch');
  $F('#tabAhpc').classList.toggle('act', v==='ahpc');
}
function verVideos(){ mostrarVista('videos'); }
function verSim(){ mostrarVista('sim'); cargarSimTipos(); }

function verPipe(){ mostrarVista('pipe'); v.pause(); pFijado=false; detallePaso(0); }
function verTrain(){ mostrarVista('train'); v.pause(); cargarEntrenamientos(); cargarModelos(); cargarTipos().then(cargarClipsTrain); }
function verRank(){ mostrarVista('rank'); v.pause(); cargarRanking(); }
function verDescomp(){ mostrarVista('descomp'); cargarDescompTipos(); }
async function verPuntos(){ mostrarVista('puntos'); await cargarCatalogosPuntos(); await cargarListaEjercicios(); }
function irAKpoints(){ irATab('panel'); verPuntos(); }
async function verAhpc(){ mostrarVista('ahpc'); await cargarAhpc(); }

// abrir_interfaz.bat abre http://.../#cortar para entrar directo a esta pestana
if (location.hash === '#cortar') verVideos();
// publicar.bat abre #sistema: el boton "Publicar en internet" vive ahi
if (location.hash === '#sistema') irATab('sistema');
