/* Pestana Panel: estado, rutina, camara, selector de cuerpo y sesion. API: interfaz/api/sesion.py, grabaciones.py */
const $ = s => document.querySelector(s);
const fmt = n => n === null || n === undefined ? "—" : (+n).toFixed(1);
let STATE = null, SEL = null, ACTIVA = false, GRABANDO = false, PAUSADO = false, TAB = "panel";
let RECS_ALL = [];
let ENTRENOS = [], CONTEO = {n:0, bien:0, mal:0, otra:0, run:null};

const banda = s => s >= 85 ? "good" : s >= 65 ? "warn" : "bad";
const bandaTxt = s => s >= 85 ? "muy parecido" : s >= 65 ? "aceptable" : "revisar";

/* ---------------------------- estado ---------------------------- */
let PRIMERA_CARGA = true;

async function cargarEstado(){
  STATE = await (await fetch("/api/state")).json();
  $("#fecha").textContent = STATE.fecha;
  $("#racha").textContent = STATE.racha;
  if (STATE.publicar) pintarPublicar(STATE.publicar);
  pintarAlmacen();
  // El default sale del catalogo completo, no de la rutina armada: asi la
  // camara se prende sola aunque todavia no hayas elegido ningun ejercicio
  // para tu rutina de hoy -- no depende de ese paso.
  if (!SEL && STATE.ejercicios.length)   // zancada por defecto
    SEL = (STATE.ejercicios.find(e => e.slug === "zancada") || STATE.ejercicios[0]).slug;
  pintarRutina();
  cargarEntrenos();
  aplicarRegionesPorDefecto();
  const s = STATE.sesion;
  const selModelo = $("#sel-modelo");
  if (!selModelo.options.length){
    selModelo.innerHTML = STATE.modelos.map(m => `<option value="${m.clave}">${m.nombre}</option>`).join("");
  }
  selModelo.value = s.modelo;
  ACTIVA = !!s.activa; GRABANDO = !!s.grabando; PAUSADO = !!s.pausado;
  actualizarControlesCamara();
  if (s.activa) abrirVivo(s.name || s.exercise, s.modo);

  // Al abrir el panel la camara se prende sola con el ejercicio por defecto
  // -- no hace falta tocar nada para empezar a verte. Solo pasa una vez.
  if (PRIMERA_CARGA){
    PRIMERA_CARGA = false;
    if (!ACTIVA && SEL){ await prenderCamara(); actualizarControlesCamara(); }
  }
}

/* ---- entrenamientos del ejercicio seleccionado (bajo Rutina) + conteo en vivo del modelo ---- */
async function cargarEntrenos(){
  try { ENTRENOS = await (await fetch("/api/entrenamientos")).json(); } catch { ENTRENOS = []; }
  pintarEntrenos();
}

let _contPrev = 0;
function reiniciarConteo(){ CONTEO = {n:0, bien:0, mal:0, otra:0, run:null}; pintarEntrenos(); }

function pintarContador(){   // numero grande a un costado del video; crece con cada repeticion contada
  const el = $("#cont-n"); if (!el) return;
  el.textContent = CONTEO.n;
  $("#cont-det").textContent = CONTEO.n ? `${CONTEO.bien} bien · ${CONTEO.mal} mal` : "";
  if (CONTEO.n > _contPrev){
    const c = $("#cont"); c.classList.remove("pop"); void c.offsetWidth; c.classList.add("pop");
  }
  _contPrev = CONTEO.n;
}

function pintarEntrenos(){
  pintarContador();
  const cont = $("#entrenos"), ex = STATE && STATE.ejercicios.find(e => e.slug === SEL);
  if (!cont || !ex){ if (cont) cont.innerHTML = ""; return; }
  const dueño = ex.clasificador || ex.slug, ses = STATE.sesion || {};
  const runs = ENTRENOS.filter(m => m.exercise === dueño).sort((a, b) => (b.fecha || "").localeCompare(a.fecha || ""));
  const uso = ACTIVA && ses.clasificador ? ses.clasificador.run : ex.clasificador_run;
  let estado;
  if (!runs.length) estado = "Sin entrenamientos de este ejercicio todavía.";
  else if (!ACTIVA) estado = "Prende la cámara para contar repeticiones con el modelo.";
  else if (!ses.clasificador) estado = "⚠ Ningún entrenamiento sirve en vivo (reentrena).";
  else if (!ses.contando) estado = "⚠ Sin base y este entrenamiento no tiene clase «fuera»: graba la base o reentrena.";
  else estado = `<b>Contando${ses.conteo === "modelo" ? " (solo el modelo)" : " (por base)"}:</b> ${CONTEO.n} reps · ${CONTEO.bien} bien · ${CONTEO.mal} mal`
    + (CONTEO.otra ? ` · ${CONTEO.otra} otras` : "") + ` <span class="ex-sub">(${ses.clasificador.run})</span>`;
  cont.innerHTML = `<div class="eh">Entrenamientos · ${ex.name}</div><div class="cuenta">${estado}</div>`
    + runs.map(m => {
      const ok = !!m.criterio, es = m.dir === uso;
      const f1 = m.f1_macro != null ? `F1 ${(+m.f1_macro).toFixed(2)}` : `acc ${(+m.accuracy).toFixed(2)}`;
      return `<div class="er ${ok ? "ok" : "off"} ${es ? "uso" : ""}" ${ok ? `onclick="usarEntreno('${m.dir}')"` : ""}
        title="${ok ? "Usar este entrenamiento para contar en vivo" : "Entrenado antes de guardar su spec: reentrena para usarlo en vivo"}">
        <b>${es ? "●" : "○"} ${m.dir}</b><span>${m.mejor_modelo}</span><span class="ex-sub">${f1} · ${(m.fecha || "").slice(0, 10)}${m.fuera ? " · cuenta sola" : ""}</span></div>`;
    }).join("");
}

async function usarEntreno(run){
  if (!ACTIVA){ alert("Prende la cámara primero."); return; }
  const r = await fetch("/api/session/clasificador", {method:"POST", headers:{"Content-Type":"application/json"},
    body: JSON.stringify({run})});
  if (!r.ok){ alert((await r.json()).detail); return; }
  reiniciarConteo();
  await cargarEstado();
}

function actualizarControlesCamara(){
  const cam = $("#btn-cam-power"), grupo = $("#grab-controls"),
        grab = $("#btn-grabar"), stop = $("#btn-detener-grab");
  cam.textContent = ACTIVA ? "Apagar cámara" : "Prender cámara";
  cam.className = ACTIVA ? "b-red" : "b-blue";
  cam.disabled = !ACTIVA && !SEL;
  $("#video-off").style.display = ACTIVA ? "none" : "flex";
  document.querySelector(".video").classList.toggle("grabando", GRABANDO && !PAUSADO);

  // Los botones de grabar/detener siempre se VEN si la camara esta prendida;
  // solo quedan usables (no disabled) si ademas hay un ejercicio elegido.
  grupo.style.display = ACTIVA ? "flex" : "none";
  grab.disabled = !SEL;
  if (!GRABANDO){ grab.textContent = "Grabar"; grab.className = "b-green"; }
  else if (PAUSADO){ grab.textContent = "Reanudar"; grab.className = "b-amber"; }
  else { grab.textContent = "Pausar"; grab.className = "b-red"; }
  stop.disabled = !GRABANDO;
  pintarEntrenos();
}

async function cargarGrabaciones(){
  const r = await (await fetch("/api/recordings?limit=60")).json();
  RECS_ALL = r.grabaciones;
  $("#disco").textContent =
    `${r.disco.sesiones} sesiones · ${r.disco.videos} videos · ${r.disco.mb} MB en input/raw/`;
  renderGrabaciones();
}

function renderGrabaciones(){
  const filtradas = SEL ? RECS_ALL.filter(g => g.exercise === SEL) : RECS_ALL;

  const fEx = $("#rec-filtro");
  if (SEL){
    const nombre = (STATE?.ejercicios.find(e => e.slug === SEL) || {}).name || SEL;
    fEx.innerHTML = `Mostrando: <b>${nombre}</b>`;
  } else {
    fEx.innerHTML = `Elegí un ejercicio de la rutina para ver sus grabaciones`;
  }

  const c = $("#recs");
  if (!filtradas.length){
    c.innerHTML = `<div class="vacio">Aún no hay sesiones archivadas${SEL ? " de este ejercicio" : ""}</div>`;
    return;
  }
  // Listbox simple: un nombre de archivo por línea, clic lo reproduce
  // (debajo de Rutina). Sin botones ni vínculos de descarga aparte.
  c.innerHTML = filtradas.map(g => {
    const nombre = g.ruta_relativa.split("/").pop();
    const sel = g.ruta_relativa === RUTA_VISTA ? " sel" : "";
    return g.existe_video
      ? `<div class="rec-item${sel}" onclick="ver('${g.ruta_relativa}','${g.exercise}')" title="Clic para reproducir">${nombre}</div>`
      : `<div class="rec-item sin-video" title="Sin video guardado">${nombre} (sin video)</div>`;
  }).join("");
}

let RUTA_VISTA = null, EJ_VISTO = null;

function ver(ruta, exercise){
  RUTA_VISTA = ruta; EJ_VISTO = exercise || null;
  renderGrabaciones();   // repinta la lista para marcar en verde pastel el video elegido
  $("#player").classList.add("on");
  const v = $("#vplayer");
  v.src = "/data/" + ruta;   // /data/ convierte a H.264 al vuelo; /recordings/ es el mp4v crudo, que el navegador no decodifica
  v.play().catch(() => {});
  v.scrollIntoView({behavior:"smooth", block:"nearest"});
}

function usarComoBaseActual(){
  if (!RUTA_VISTA) return;
  const nombre = (STATE?.ejercicios.find(e => e.slug === EJ_VISTO) || {}).name || EJ_VISTO || "este ejercicio";
  usarComoBase(RUTA_VISTA, nombre);
}

async function usarComoBase(ruta, nombre){
  if (!confirm(`¿Usar esta grabación como nuevo movimiento base de "${nombre}"?\n\n`+
               `Esto reemplaza la calibración actual (umbrales y puntaje de referencia).`)) return;
  const r = await fetch("/api/recordings/use_as_base", {
    method:"POST", headers:{"Content-Type":"application/json"},
    body: JSON.stringify({ruta_relativa: ruta})
  });
  const d = await r.json();
  if (!r.ok){ alert(d.detail || "No se pudo recalibrar la base."); return; }
  alert(`Base recalibrada: ${d.n_reps} repeticiones, tau ${d.tau}.`);
  await cargarEstado();
}

async function cargarHistorial(){
  const h = await (await fetch("/api/history?days=14")).json();
  pintarGrafico(h.diario); pintarTabla(h.recientes);
}

/* ---------------------------- rutina ---------------------------- */
async function seleccionar(slug, ev){
  if (ev && ev.target.closest("button, input, select, label")) return;
  if (SEL === slug) return;
  if (ACTIVA && GRABANDO){ alert("Detén la grabación antes de cambiar de ejercicio."); return; }

  SEL = slug;
  reiniciarConteo();
  pintarRutina(); renderGrabaciones(); actualizarControlesCamara(); pintarEntrenos();
  aplicarRegionesPorDefecto();

  if (!ACTIVA) return;   // se aplicara recien cuando prendas la camara
  const r = await fetch("/api/session/exercise", {method:"POST", headers:{"Content-Type":"application/json"},
    body: JSON.stringify({exercise: slug})});
  if (!r.ok){ alert((await r.json()).detail); return; }
  const info = await r.json();
  actualizarTituloVivo(info.name, "preview");
  await empujarRegiones();
}

async function cambioRutina(){
  const items = [...document.querySelectorAll("#rutina input[type=checkbox]")]
    .filter(c => c.checked)
    .map(c => ({exercise: c.dataset.slug,
                target_reps: +document.querySelector(`[data-reps="${c.dataset.slug}"]`).value || 10}));
  const r = await (await fetch("/api/routine", {method:"POST", headers:{"Content-Type":"application/json"},
                                                body: JSON.stringify(items)})).json();
  STATE.rutina = r.rutina;
  pintarRutina();
}

function pintarRutina(){
  const cont = $("#rutina");
  if (!STATE.ejercicios.length){
    cont.innerHTML = `<div class="vacio">No hay ejercicios definidos todavía.</div>`;
    return;
  }
  cont.innerHTML = `<table><tbody>` + STATE.ejercicios.map(ex => {
    const enRutina = STATE.rutina.find(r => r.exercise === ex.slug);
    const hoy = STATE.hoy[ex.slug];
    const reps = enRutina ? enRutina.target_reps : 10;
    const hechas = hoy ? hoy.reps : 0;
    const pct = enRutina ? Math.min(100, reps ? hechas / reps * 100 : 0) : 0;
    const prom = hoy ? fmt(hoy.avg_score) : "—";
    const sub = enRutina ? `${hechas} / ${reps} reps hoy · promedio ${prom}` : "";
    return `<tr class="fila-ex ${ex.slug===SEL?"sel":""}" onclick="seleccionar('${ex.slug}',event)">
      <td>
        <input type="checkbox" data-slug="${ex.slug}" ${enRutina ? "checked" : ""} onchange="cambioRutina()">
      </td>
      <td>
        <div class="ex-name">${ex.name}</div>
        ${sub ? `<div class="ex-sub">${sub}</div>` : ""}
        ${enRutina ? `<div class="bar"><i style="width:${pct}%"></i></div>` : ""}
        ${ex.tiene_base ? "" : '<span class="badge warn" style="margin-top:4px;display:inline-block">sin base</span>'}
      </td>
      <td class="num">
        <input type="number" min="1" max="99" data-reps="${ex.slug}" value="${reps}" onchange="cambioRutina()">
      </td>
      <td class="acc">
        <button class="iconbtn" title="Subir videos bien / mal" onclick="abrirVideos('${ex.slug}')">🎞</button>
        <button class="iconbtn" title="Editar" onclick="abrirEjercicio('${ex.slug}')">✎</button>
        <button class="iconbtn danger" title="Archivar" onclick="archivarEjercicio('${ex.slug}')">🗑</button>
      </td>
    </tr>`;
  }).join("") + `</tbody></table>`;
}

/* ------------------------ crear / editar / archivar ejercicio ------------------------ */
let EJ_EDIT = null;   // slug en edicion; null = nuevo

function abrirEjercicio(slug){
  EJ_EDIT = slug || null;
  const ex = slug ? STATE.ejercicios.find(e => e.slug === slug) : null;
  $("#dlg-ej-titulo").textContent = ex ? `Editar · ${ex.slug}` : "Nuevo ejercicio";
  $("#ej-slug").value = ex ? ex.slug : "";
  $("#ej-slug").disabled = !!ex;   // renombrar romperia type, clips y base
  $("#ej-name").value = ex ? ex.name : "";
  $("#ej-desc").value = ex ? ex.description : "";
  $("#ej-dir").value = ex ? ex.direction : "down_up";
  $("#ej-min").value = ex ? ex.min_duration_ms : 600;
  $("#ej-max").value = ex ? ex.max_duration_ms : 6000;
  $("#ej-aviso").textContent = ex
    ? "Puntos y ángulos se editan en la pestaña Kpoints. Si cambias dirección o duración, graba la base de nuevo."
    : "Después de crearlo, define sus puntos en Kpoints y graba la base.";
  $("#dlg-ej").showModal();
}

async function _post(url, body){
  const r = await fetch(url, {method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify(body)});
  const j = await r.json();
  if (!r.ok) throw new Error(j.error || j.detail || r.statusText);
  return j;
}

async function guardarEjercicio(){
  const slug = EJ_EDIT || $("#ej-slug").value.trim();
  try {
    if (!EJ_EDIT) await _post("/api/puntos/crear", {nombre: slug});
    const r = await _post("/api/puntos/modificar", {
      nombre: slug, name: $("#ej-name").value || slug, description: $("#ej-desc").value,
      direction: $("#ej-dir").value, min_duration_ms: $("#ej-min").value, max_duration_ms: $("#ej-max").value});
    $("#dlg-ej").close();
    if (r.base_invalida) alert("Cambió la segmentación: graba la base de este ejercicio de nuevo.");
    SEL = slug;
    await cargarEstado();
  } catch (e) { $("#ej-aviso").textContent = "⚠ " + e.message; }
}

let VID_SLUG = null;
async function _contarClips(){
  const n = await (await fetch("/api/ejercicio/clips?slug=" + encodeURIComponent(VID_SLUG))).json();
  for (const c of ["bien", "mal"]) $("#vid-n-" + c).textContent = `(${n[c]} en el dataset)`;
}
function abrirVideos(slug){
  VID_SLUG = slug;
  $("#vid-slug").textContent = slug;
  $("#vid-aviso").textContent = "";
  for (const c of ["bien", "mal"]) $("#vid-" + c).value = "";
  _contarClips();
  $("#dlg-vid").showModal();
}

async function _subirClase(clase, reemplazar){
  const fd = new FormData();
  fd.append("slug", VID_SLUG); fd.append("clase", clase); fd.append("reemplazar", reemplazar ? "true" : "false");
  for (const f of $("#vid-" + clase).files) fd.append("archivos", f);
  const r = await fetch("/api/ejercicio/clips", {method: "POST", body: fd});
  const j = await r.json();
  if (!r.ok) throw new Error(j.error || j.detail || r.statusText);
  return j;
}

async function subirVideos(){
  const aviso = $("#vid-aviso"), btn = $("#vid-subir");
  btn.disabled = true; aviso.textContent = "Subiendo y detectando puntos… (puede tardar)";
  const lineas = [];
  try {
    for (const clase of ["bien", "mal"]) {
      if (!$("#vid-" + clase).files.length) continue;
      const j = await _subirClase(clase, false);
      lineas.push(`${clase}: ${j.ok.length} subido(s)`);
      lineas.push(...j.errores.map(e => "⚠ " + e));
      if (j.sql_error) lineas.push("⚠ SQL no respondió: quedó local, usa Sistema → Generar tablas. " + j.sql_error);
      else if (j.sql) lineas.push(`SQL: ${j.sql.archivos_nuevos} archivo(s) nuevo(s), ${j.sql.omitidos_sin_puntos} sin puntos`);
    }
    if (!lineas.length) lineas.push("Elige al menos un video.");
  } catch (e) { lineas.push("⚠ " + e.message); }
  aviso.textContent = lineas.join("\n");
  btn.disabled = false;
  _contarClips();
}

async function importarCarpeta(){
  const aviso = $("#vid-aviso"), btn = $("#vid-carpeta-ir"), carpeta = $("#vid-carpeta").value.trim();
  if (!carpeta){ aviso.textContent = "Escribe la ruta de la carpeta."; return; }
  btn.disabled = true; aviso.textContent = "Iniciando…";
  try {
    const r = await fetch("/api/ejercicio/clips/carpeta", {method:"POST", headers:{"Content-Type":"application/json"},
      body: JSON.stringify({slug: VID_SLUG, carpeta})});
    if (!r.ok) throw new Error((await r.json()).error || r.statusText);
    let p;
    do {
      await new Promise(ok => setTimeout(ok, 1500));
      p = await (await fetch("/api/ejercicio/clips/carpeta/progreso")).json();
      aviso.textContent = `Importando ${p.hecho} / ${p.total}… ${p.archivo}`;
    } while (p.activo);
    const x = p.resultado || {};
    aviso.textContent = x.error ? "⚠ " + x.error : [
      `Listo: ${x.ok} nuevo(s) (${Object.entries(x.por_clase).map(([c, n]) => c + " " + n).join(", ")}), ${x.saltados} ya estaban.`,
      x.originales && x.originales.videos ? `Originales reconstruidos: ${x.originales.nuevos} nuevo(s) de ${x.originales.videos} (pestaña Cut/Edit, y columnas nuevas en indice.csv).` : "",
      ...x.errores.map(e => "⚠ " + e),
      x.sql_error ? "⚠ SQL no respondió: quedó local, usa Sistema → Generar tablas. " + x.sql_error : ""].filter(Boolean).join("\n");
  } catch (e) { aviso.textContent = "⚠ " + e.message; }
  btn.disabled = false;
  _contarClips(); cargarEstado();
}

async function archivarEjercicio(slug){
  if (!confirm(`¿Archivar "${slug}"? Sale de la app y de la rutina, y se borran sus clips del manifest y todos sus datos de SQL. ` +
    `Los archivos (clips, grabaciones) no se borran: pasan a sistema/archivados/.`)) return;
  try {
    const r = await _post("/api/puntos/eliminar", {nombre: slug});
    const d = r.depurado || {};
    if (d.error || d.sql_error || (d.errores || []).length)
      alert("Archivado, pero quedó algo pendiente: " + (d.error || d.sql_error || d.errores.join("; ")) + "\nUsa Sistema → «Quitar de SQL lo archivado» para reintentar.");
    if (SEL === slug) SEL = null;
    await cargarEstado();
  } catch (e) { alert(e.message); }
}

/* ---------------------------- cámara ---------------------------- */
async function cargarCamaras(){
  const btn = $("#btn-cam-refresh"), sel = $("#sel-camera"), hint = $("#cam-hint");
  const prev = sel.value;
  btn.disabled = true;
  sel.innerHTML = `<option>Buscando…</option>`;
  hint.style.display = "none";
  try {
    const r = await (await fetch("/api/cameras")).json();
    const usb = r.camaras.map(c => `<option value="${c.index}">${c.name || ("Cámara " + c.index)} · ${c.width}×${c.height}</option>`);
    const droid = (r.droidcams || []).map(d => `<option class="opt-droid" value="droid:${d.ip}">📱 ${d.nombre ? d.nombre + " · " : "DroidCam · "}${d.ip}</option>`);
    sel.innerHTML = (usb.length || droid.length) ? usb.concat(droid).join("")
      : `<option value="0">Cámara 0 (predeterminada)</option>`;
    if (prev && [...sel.options].some(o => o.value === prev)) sel.value = prev;
    pintarSelectorCamara();
    if (!r.camaras.length && !(r.droidcams || []).length){
      hint.style.display = "block";
      hint.textContent = (r.nombres_windows && r.nombres_windows.length)
        ? `Windows ve conectada(s): ${r.nombres_windows.join(", ")}, pero no se pudo abrir ninguna. ` +
          `Revisa Configuración → Privacidad y seguridad → Cámara, o que no la tenga abierta otra app (Teams/Zoom/Meet).`
        : `No se detectó ninguna cámara. Verifica que esté conectada y vuelve a pulsar 🔄.`;
    }
  } finally {
    btn.disabled = false;
  }
}
$("#btn-cam-refresh").onclick = cargarCamaras;
function pintarSelectorCamara(){   // el selector se tiñe de amarillo pastel cuando la cámara elegida es un DroidCam
  const sel = $("#sel-camera"); sel.classList.toggle("droid", sel.value.startsWith("droid:"));
}
function camaraElegida(){   // {camera, droidcam} para /api/session/camera_on
  const v = $("#sel-camera").value;
  return v.startsWith("droid:") ? {camera: 0, droidcam: v.slice(6)} : {camera: +v || 0};
}

/* ---------------------------- selector de cuerpo ---------------------------- */
const REGIONES_TODAS = ["cabeza", "manos", "brazos", "torso", "cadera", "piernas", "pies"];
let REGIONES_ACTIVAS = new Set(REGIONES_TODAS);

function regionesSeleccionadas(){
  return [...REGIONES_ACTIVAS];
}

function pintarSelectorCuerpo(){
  document.querySelectorAll(".region-shape").forEach(el => {
    el.classList.toggle("off", !REGIONES_ACTIVAS.has(el.dataset.region));
  });
}

async function empujarRegiones(){
  if (!ACTIVA) return;
  await fetch("/api/session/overlay", {method:"POST", headers:{"Content-Type":"application/json"},
    body: JSON.stringify({regiones: regionesSeleccionadas()})});
}

async function alternarRegion(clave){
  if (REGIONES_ACTIVAS.has(clave)) REGIONES_ACTIVAS.delete(clave); else REGIONES_ACTIVAS.add(clave);
  pintarSelectorCuerpo();
  await empujarRegiones();
}

document.querySelectorAll(".region-shape").forEach(el => {
  el.onclick = () => alternarRegion(el.dataset.region);
});

function aplicarRegionesPorDefecto(){
  const ex = STATE && STATE.ejercicios.find(e => e.slug === SEL);
  if (!ex) return;
  REGIONES_ACTIVAS = new Set(ex.regiones_default && ex.regiones_default.length
    ? [...ex.regiones_default, "cabeza"] : REGIONES_TODAS);   // la cabeza siempre activa
  pintarSelectorCuerpo();
}

/* ---------------------------- sesión ---------------------------- */
function actualizarTituloVivo(nombre, modo){
  const titulos = {preview:"Cámara · ", grabar:"Grabando base · ", evaluar:"Entrenando · "};
  $("#vivo-titulo").textContent = (titulos[modo] || "Cámara · ") + nombre;
  $("#top-hint").textContent = modo === "grabar" ? "haz 5 reps lentas"
    : modo === "preview" ? "colócate en posición" : "esperando rep";
  $("#hero").textContent = modo === "grabar" ? "REC" : "—";
  $("#hero").style.color = modo === "grabar" ? "var(--serious)" : "var(--ink)";
  $("#hero").classList.toggle("parpadeando", modo === "grabar");
}

function abrirVivo(nombre, modo){
  actualizarTituloVivo(nombre, modo);
  $("#stream").src = "/video?t=" + Date.now();
  $("#log").innerHTML = "";
}

async function prenderCamara(silencioso){
  if (!SEL){ alert("Selecciona un ejercicio primero."); return false; }
  const item = STATE.rutina.find(r => r.exercise === SEL);
  const r = await fetch("/api/session/camera_on", {
    method:"POST", headers:{"Content-Type":"application/json"},
    body: JSON.stringify({exercise:SEL, reps: item ? item.target_reps : 10,
                          video: $("#chk-video").checked,
                          ...camaraElegida(),
                          fps: +$("#fps-slider").value || 30,
                          regiones: regionesSeleccionadas()})
  });
  if (!r.ok){ if (!silencioso) alert((await r.json()).detail); return false; }
  const info = await r.json();
  ACTIVA = true; GRABANDO = false; PAUSADO = false; reiniciarConteo();
  abrirVivo(info.name, "preview");
  return true;
}

async function apagarCamara(){
  const r = await (await fetch("/api/session/stop", {method:"POST"})).json();
  ACTIVA = false; GRABANDO = false; PAUSADO = false;
  $("#stream").src = ""; $("#feats").innerHTML = "";
  if (r.error) alert("No se pudo construir la plantilla:\n\n" + r.error);
  await cargarHistorial(); await cargarGrabaciones();
  return r;
}

$("#btn-cam-power").onclick = async () => {
  $("#btn-cam-power").disabled = true;
  try {
    if (!ACTIVA) await prenderCamara();
    else await apagarCamara();
  } finally {
    actualizarControlesCamara();
  }
};

async function reabrirSiActiva(el){
  // Cambiar de cámara en el listbox la prende de una, esté activa o no:
  // si ya había una sesión, la reabre con la cámara nueva; si no, la prende.
  // La cámara recién cerrada a veces tarda un instante en liberarse
  // (Windows/DirectShow) y el primer intento de abrir la nueva falla: se
  // reintenta una vez en silencio antes de rendirse y mostrar el error.
  el.disabled = true;
  try {
    if (ACTIVA) await apagarCamara();
    if (!(await prenderCamara(true))){
      await new Promise(res => setTimeout(res, 600));
      await prenderCamara();
    }
  } finally {
    el.disabled = false;
    actualizarControlesCamara();
  }
}
$("#sel-camera").onchange = () => { pintarSelectorCamara(); reabrirSiActiva($("#sel-camera")); };
$("#sel-modelo").onchange = () => fetch("/api/session/modelo", {
  method: "POST", headers: {"Content-Type": "application/json"},
  body: JSON.stringify({modelo: $("#sel-modelo").value}),
});
$("#fps-slider").oninput = () => { $("#fps-val").textContent = $("#fps-slider").value; };
$("#fps-slider").onchange = async () => {
  if (!ACTIVA) return;   // nada que reabrir todavia, solo cambia la opcion elegida
  const fps = +$("#fps-slider").value || 30;
  const r = await (await fetch("/api/session/fps", {method:"POST", headers:{"Content-Type":"application/json"},
    body: JSON.stringify({fps})})).json();
  if (!r.aplicado) await reabrirSiActiva($("#fps-slider"));   // el driver lo ignoro: reabre para forzarlo
};

$("#btn-grabar").onclick = async () => {
  $("#btn-grabar").disabled = true;
  try {
    if (!GRABANDO){
      const r = await fetch("/api/session/grabar", {method:"POST"});
      if (!r.ok){ alert((await r.json()).detail); return; }
      const info = await r.json();
      GRABANDO = true; PAUSADO = false;
      actualizarTituloVivo((STATE.ejercicios.find(e => e.slug === SEL) || {}).name || SEL, info.modo);
    } else {
      await fetch(`/api/session/${PAUSADO ? "resume" : "pause"}`, {method:"POST"});
      PAUSADO = !PAUSADO;
    }
  } finally {
    actualizarControlesCamara();
  }
};

$("#btn-detener-grab").onclick = async () => {
  $("#btn-detener-grab").disabled = true;
  try {
    const r = await (await fetch("/api/session/grabar_detener", {method:"POST"})).json();
    GRABANDO = false; PAUSADO = false;
    actualizarTituloVivo((STATE.ejercicios.find(e => e.slug === SEL) || {}).name || SEL, "preview");
    if (r.error) alert("No se pudo construir la plantilla:\n\n" + r.error);
    await cargarHistorial(); await cargarGrabaciones();
  } finally {
    actualizarControlesCamara();
  }
};


// --- Persona con la que se graba (P1..Pn): se guarda en el video y pasa a sus clips ---
async function cargarPersonasCaptura(){
  const sel = $("#sel-persona"); if (!sel) return;
  try {
    const d = await (await fetch("/api/personas")).json();
    sel.innerHTML = '<option value="">sin persona</option>' + d.personas.map(p => `<option>${p}</option>`).join("");
    sel.value = d.grabando_con || "";
  } catch (e) { /* sin servidor aun: queda "sin persona" */ }
}
$("#sel-persona").onchange = () => fetch("/api/session/persona", {method: "POST", headers: {"Content-Type": "application/json"},
  body: JSON.stringify({persona: $("#sel-persona").value || null})});
cargarPersonasCaptura();
