/* Pestana Sistema: servidor SQL, tablas del dataset, librerias, Python, apagar, log y Publicar. API: interfaz/api/sistema.py, publicar.py */
/* ---------------------------- sistema ---------------------------- */
function irATab(nombre){
  TAB = nombre;
  // las vistas del dataset se ocultan y todas las pestanas se apagan: se prende solo la elegida
  ["app","trainview","rankview","descompview","puntosview","pipeview","pitchview"].forEach(id => {
    const e = document.getElementById(id); if (e) e.style.display = "none"; });
  document.querySelectorAll("header .tab").forEach(b => b.classList.remove("act"));
  $("#tab-" + nombre).style.display = "block";
  $("#tab-" + (nombre === "panel" ? "sistema" : "panel")).style.display = "none";
  $("#tab-btn-" + nombre).classList.add("act");
  if (nombre === "sistema"){ cargarLog(); cargarLibrerias(); cargarVersionPython(); cargarPublicar(); pintarAlmacen(); cargarServidorSql(); cargarDroidcam(); cargarRespaldoSql(); cargarSql(false); cargarMatriz(); }
}
$("#tab-btn-panel").onclick = () => irATab("panel");
$("#tab-btn-sistema").onclick = () => irATab("sistema");

/* ---------------------------- publicar (Cloudflare) ---------------------------- */
let PUB_TIMER = null;
function pintarPublicar(p){
  const activo = p.activo || p.iniciando;
  $("#pub-dot").className = "dot " + (p.url ? "on" : "off");
  $("#pub-txt").textContent = p.url ? "publicado" : p.iniciando ? "abriendo enlace…" : "apagado";
  $("#btn-pub-iniciar").disabled = !!activo;
  $("#btn-pub-detener").disabled = !activo;
  const pill = $("#pub-pill");
  pill.style.display = p.url ? "" : "none";
  if (p.url){ $("#pub-pill-url").href = p.url; $("#pub-pill-url").textContent = "público"; }
  let hint = "";
  if (p.url) hint = `Enlace: <a href="${p.url}" target="_blank">${p.url}</a>
      <button class="b-blue" style="padding:2px 8px" onclick="navigator.clipboard.writeText('${p.url}')">Copiar</button>
      · ${p.con_clave ? "usuario: <b>" + (p.usuario || "?") + "</b> (la clave se muestra solo al crearla)" : "<b>SIN clave</b>: cualquiera con el enlace entra"}`;
  else if (p.error) hint = "⚠ " + p.error;
  if (hint) $("#pub-hint").innerHTML = hint;
  clearTimeout(PUB_TIMER);
  if (p.iniciando || (p.activo && !p.url)) PUB_TIMER = setTimeout(cargarPublicar, 2000);
}
async function cargarPublicar(){
  try { pintarPublicar(await (await fetch("/api/publicar/estado")).json()); } catch(e) {}
}
function mostrarClave(c){
  if (c) alert(`Guardá esta clave, no se vuelve a mostrar:\n\nusuario: ${c.usuario}\nclave: ${c.clave}`);
}
$("#btn-pub-iniciar").onclick = async () => {
  $("#pub-hint").textContent = "iniciando cloudflared (la primera vez se descarga, ~50 MB)…";
  const r = await (await fetch("/api/publicar/iniciar", {method:"POST", headers:{"Content-Type":"application/json"},
    body: JSON.stringify({con_clave: $("#pub-clave").checked})})).json();
  mostrarClave(r.nueva_clave);
  pintarPublicar(r);
};
$("#btn-pub-detener").onclick = async () => pintarPublicar(await (await fetch("/api/publicar/detener", {method:"POST"})).json());
$("#btn-pub-clave").onclick = async () => {
  if (!confirm("¿Generar una clave nueva? La anterior deja de servir.")) return;
  mostrarClave(await (await fetch("/api/publicar/nueva_clave", {method:"POST"})).json());
  cargarPublicar();
};

function pintarAlmacen(){
  const a = (STATE && STATE.almacen) || {};
  $("#db-dot").className = "dot " + (a.conectado ? "on" : "off");
  $("#db-txt").textContent = a.conectado ? "conectado" : "sin conexión";
  $("#db-hint").textContent = (a.error ? a.error + " — " : "")
    + (a.pendientes ? `${a.pendientes} repetición(es) esperando para guardarse (se reintenta sola cada 30 s, no se pierden).`
                    : "Historial, rutina y repeticiones se guardan en SQL Server.");
}

async function cargarServidorSql(){
  try {
    const s = await (await fetch("/api/system/sql")).json();
    $("#db-host").value = s.host; $("#db-base").value = s.base;
    $("#db-dot").className = "dot " + (s.conectado ? "on" : "off");
    $("#db-txt").textContent = s.conectado ? "conectado" : "sin conexión";
    if (s.error) $("#db-hint").textContent = s.error;
    $("#db-archivo").textContent = (s.guardado ? "Guardado en " : "Se guardará en ") + s.archivo
      + " (se lee al arrancar el panel).";
  } catch (e) {}
}
$("#btn-db-guardar").onclick = async () => {
  $("#db-hint").textContent = "Conectando…";
  const r = await fetch("/api/system/sql", {method:"POST", headers:{"Content-Type":"application/json"},
    body: JSON.stringify({host: $("#db-host").value, base: $("#db-base").value})});
  if (!r.ok){ $("#db-hint").textContent = (await r.json()).detail || "No se pudo guardar."; return; }
  await cargarServidorSql();
  if (!(await (await fetch("/api/system/sql")).json()).error) pintarAlmacen();
  cargarSql(false);
};

async function cargarLog(){
  const r = await (await fetch("/api/log?lines=300")).json();
  const esc = s => s.replace(/&/g,"&amp;").replace(/</g,"&lt;");
  $("#log-sistema").innerHTML = r.lineas.length
    ? r.lineas.map(esc).join("<br>")
    : `<span style="color:var(--muted)">Sin eventos todavía.</span>`;
  $("#log-sistema").scrollTop = $("#log-sistema").scrollHeight;
}

async function cargarLibrerias(){
  const r = await (await fetch("/api/libraries")).json();
  $("#librerias").innerHTML = `<table><thead><tr>
      <th>Librería</th><th>Solicitada</th><th>Instalada</th><th></th>
    </tr></thead><tbody>` +
    r.librerias.map(l => `<tr>
      <td>${l.nombre}</td>
      <td>${l.requerida || "—"}</td>
      <td>${l.version ? '<span class="okmark">✓ v' + l.version + '</span>' : '<span class="errmark">✗ falta</span>'}</td>
      <td>${l.nombre === "python" ? ""
        : `<button onclick="actualizarLibreria('${l.nombre}')">Actualizar</button>`}</td>
    </tr>`).join("") +
    `</tbody></table>`;
}

async function actualizarLibreria(nombre){
  const hint = $("#libs-hint");
  hint.textContent = `Actualizando ${nombre}…`;
  try {
    const r = await fetch("/api/system/libraries/update", {method:"POST",
      headers:{"Content-Type":"application/json"}, body: JSON.stringify({nombre})});
    const d = await r.json();
    hint.textContent = r.ok ? `${nombre} actualizado.` : `Error: ${d.detail || "no se pudo actualizar."}`;
  } catch (e) { hint.textContent = `Error de red actualizando ${nombre}.`; }
  await cargarLibrerias();
}

$("#btn-libs-actualizar-todo").onclick = async () => {
  const hint = $("#libs-hint");
  hint.textContent = "Actualizando todas las librerías (puede tardar)…";
  try {
    const r = await fetch("/api/system/libraries/update", {method:"POST",
      headers:{"Content-Type":"application/json"}, body: JSON.stringify({})});
    const d = await r.json();
    hint.textContent = r.ok ? "Listo, todas actualizadas." : `Error: ${d.detail || "no se pudo actualizar."}`;
  } catch (e) { hint.textContent = "Error de red actualizando."; }
  await cargarLibrerias();
};

async function cargarVersionPython(){
  const r = await (await fetch("/api/system/python")).json();
  const detectadas = r.detectadas.length ? r.detectadas : [r.actual];
  $("#sel-pyver").innerHTML = detectadas.map(v =>
    `<option value="${v}" ${v === r.actual ? "selected" : ""}>${v}${v === r.actual ? " (actual)" : ""}</option>`
  ).join("");
  $("#pyver-hint").textContent = r.detectadas.length
    ? `En uso: Python ${r.actual_completa || r.actual}.`
    : `En uso: Python ${r.actual_completa || r.actual}. No se detectaron otras versiones instaladas (lanzador "py" no disponible).`;
  $("#btn-pyver-cambiar").disabled = !r.detectadas.length;
}

$("#btn-pyver-cambiar").onclick = async () => {
  const version = $("#sel-pyver").value;
  if (!confirm(`¿Cambiar a Python ${version}? El panel se reinicia y reinstala todo, tarda varios minutos.`)) return;
  if (ACTIVA) await apagarCamara();
  const r = await fetch("/api/system/python_version", {method:"POST",
    headers:{"Content-Type":"application/json"}, body: JSON.stringify({version})});
  const d = await r.json();
  if (!r.ok){ alert(d.detail || "No se pudo cambiar de versión."); return; }
  $("#wstxt").textContent = "reiniciando con Python " + version + "…";
};

$("#btn-apagar").onclick = async () => {
  if (!confirm("¿Apagar el panel? Se cerrará el programa (y la ventana de comandos).")) return;
  if (ACTIVA) await apagarCamara();
  await fetch("/api/system/shutdown", {method:"POST"});
  $("#wstxt").textContent = "apagando…";
};

$("#btn-reiniciar").onclick = async () => {
  if (!confirm("¿Reiniciar el panel? Se relanzará automáticamente.")) return;
  if (ACTIVA) await apagarCamara();
  await fetch("/api/system/restart", {method:"POST"});
  $("#wstxt").textContent = "reiniciando…";
};


/* ---------------------------- modelos de entrenamiento: matriz de epocas y parada ---------------------------- */
// API: interfaz/api/entrenamiento.py (/api/modelos/matriz). Defaults y validacion: nucleo/config.py (MODELOS_MATRIZ)
const MATRIZ_NOTAS = {
  random_forest: "árboles", extra_trees: "árboles", adaboost: "rondas", lightgbm: "rondas", catboost: "rondas", xgboost: "rondas",
  gradient_boosting: "rondas (puede parar antes)", hist_gradient_boosting: "rondas (puede parar antes)",
  logistic: "optimizador (para al converger)", sgd_logistico: "pasadas (para al converger)", mlp: "épocas de la red (para al converger)",
};
const MATRIZ_COLS = ["epocas", "max_iter", "parar", "paciencia", "tol"];
let MATRIZ = {};
async function cargarMatriz(){
  MATRIZ = await (await fetch("/api/modelos/matriz")).json();
  const celda = (n, k, v) => v == null ? '<td class="hint">—</td>'
    : k === "parar" ? `<td><input type="checkbox" data-m="${n}" data-k="${k}" ${v ? "checked" : ""}></td>`
    : `<td><input type="number" min="${k === "tol" ? 0 : 1}" step="${k === "tol" ? "any" : 1}" style="width:90px" data-m="${n}" data-k="${k}" value="${v}"></td>`;
  $("#matrizModelos").innerHTML = Object.entries(MATRIZ).map(([n, f]) =>
    `<tr><td>${n}</td><td class="hint">${MATRIZ_NOTAS[n] || "no itera (un solo ajuste)"}</td>${MATRIZ_COLS.map(k => celda(n, k, f[k])).join("")}</tr>`).join("");
}
async function guardarMatriz(){
  const cambios = {};
  document.querySelectorAll("#matrizModelos input").forEach(i => {
    const n = i.dataset.m, k = i.dataset.k, v = k === "parar" ? i.checked : (k === "tol" ? parseFloat(i.value) : parseInt(i.value, 10));
    if (v !== MATRIZ[n][k]) (cambios[n] = cambios[n] || {})[k] = v;
  });
  const r = await fetch("/api/modelos/matriz", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({cambios})});
  const j = await r.json();
  $("#modelosMsg").textContent = r.ok ? "Guardado: se usa en el próximo entrenamiento." : "Error: " + (j.error || r.status);
  if (r.ok) cargarMatriz();
}

/* ---------------------------- DroidCam ---------------------------- */
let DC_LISTA = [];   // [{nombre, ip}] tal como esta guardado
const dcTexto = d => d.nombre ? `${d.nombre} · ${d.ip}` : d.ip;
async function cargarDroidcam(){
  const r = await (await fetch("/api/system/droidcam")).json();
  DC_LISTA = r.lista;
  $("#dc-lista").innerHTML = DC_LISTA.map((d, i) => `<option value="${i}">${dcTexto(d).replace(/</g, "&lt;")}</option>`).join("");
}
async function guardarDroidcam(lista){
  const r = await fetch("/api/system/droidcam", {method:"POST", headers:{"Content-Type":"application/json"},
    body: JSON.stringify({lista})});
  const j = await r.json();
  if (!r.ok){ $("#dc-hint").textContent = j.detail || "No se pudo guardar."; return false; }
  await cargarDroidcam();
  if (typeof cargarCamaras === "function") cargarCamaras();   // el selector del panel las muestra en amarillo
  return true;
}
const dcCampos = () => ({nombre: $("#dc-nombre").value.trim(), ip: $("#dc-nueva").value.trim()});
$("#dc-lista").onchange = () => {   // elegir una fila la carga en los campos para editarla
  const d = DC_LISTA[+$("#dc-lista").value];
  if (d){ $("#dc-nombre").value = d.nombre; $("#dc-nueva").value = d.ip; }
};
$("#btn-dc-agregar").onclick = async () => {
  const nueva = dcCampos();
  if (!nueva.ip) return;
  if (await guardarDroidcam([...DC_LISTA, nueva])) $("#dc-nombre").value = $("#dc-nueva").value = "";
};
$("#btn-dc-guardar").onclick = async () => {
  const i = $("#dc-lista").selectedIndex, nueva = dcCampos();
  if (i < 0 || !nueva.ip) return;
  await guardarDroidcam(DC_LISTA.map((d, k) => k === i ? nueva : d));
};
$("#btn-dc-quitar").onclick = () => {
  const i = $("#dc-lista").selectedIndex;
  if (i >= 0) guardarDroidcam(DC_LISTA.filter((_, k) => k !== i));
};

const POST_JSON = (url, cuerpo) => fetch(url, {method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify(cuerpo)});

/* ---------------------------- documentacion de datos ---------------------------- */
$("#btn-docs-generar").onclick = async () => {
  $("#docs-msg").textContent = "Generando… (lee los clips del disco)";
  const r = await POST_JSON("/api/docs/generar", {});
  const j = await r.json();
  $("#docs-msg").textContent = r.ok ? "✔ " + Object.entries(j).map(([ej, x]) => x.error ? `${ej}: ${x.error}` : `${ej}: ${x.formatear.filas} filas × ${x.formatear.columnas} columnas`).join(" · ")
    + " → docs/diccionario/, reportes/ y input/gold/" : "Error " + r.status;
};

/* ---------------------------- respaldo en SQL (el disco manda) ---------------------------- */
async function cargarRespaldoSql(){
  const r = await (await fetch("/api/system/respaldo-sql")).json();
  $("#rs-cortar").checked = r.al_cortar; $("#rs-entrenar").checked = r.al_entrenar;
}
$("#btn-rs-guardar").onclick = async () => {
  const r = await POST_JSON("/api/system/respaldo-sql", {al_cortar: $("#rs-cortar").checked, al_entrenar: $("#rs-entrenar").checked});
  $("#rs-msg").textContent = r.ok ? "Guardado en parameters/server.json." : "No se pudo guardar.";
};
$("#btn-rs-ahora").onclick = async () => {
  const b = $("#btn-rs-ahora"); b.disabled = true; $("#rs-msg").textContent = "Copiando a SQL… (puede tardar)";
  try {
    const j = await (await POST_JSON("/api/system/respaldo-sql/ahora", {})).json();
    $("#rs-msg").textContent = j.error ? "⚠ SQL no respondió: " + j.error
      : `✔ ${j.resumen.archivos_nuevos} nuevos · ${j.resumen.archivos_actualizados} actualizados · ${j.resumen.archivos_sin_cambios} sin cambios`;
  } finally { b.disabled = false; }
};
