/* En vivo: WebSocket de eventos, grafico e historial, y el arranque del panel. API: /ws, /api/history */
/* ---------------------------- websocket ---------------------------- */
function conectar(){
  const ws = new WebSocket(`ws://${location.host}/ws`);
  ws.onopen = () => { $("#wsdot").className = "dot on"; $("#wstxt").textContent = "en línea"; };
  ws.onclose = () => {
    $("#wsdot").className = "dot off"; $("#wstxt").textContent = "sin conexión";
    setTimeout(conectar, 2000);
  };
  ws.onmessage = ev => manejar(JSON.parse(ev.data));
  setInterval(() => { if (ws.readyState === 1) ws.send("ping"); }, 20000);
}

function manejar(e){
  if (e.type === "status"){
    // el contador grande sigue la cifra del servidor (la misma del video), aunque se pierda algun evento "rep"
    if (ACTIVA && !GRABANDO && e.reps > CONTEO.n){ CONTEO.n = e.reps; pintarContador(); }
    const f = $("#feats");
    f.innerHTML = Object.entries(e.features).map(([k,v],i) =>
      `<b>${k}</b><span>${v === null ? "—" : v.toFixed(1) + (e.unidades[i] === "deg" ? "°" : "")}</span>`
    ).join("") + `<b>fps cámara</b><span>${e.fps_camara ?? "—"}</span><b>fps detección</b><span>${e.fps}</span>` +
      (e.señal !== null && e.señal !== undefined ? `<b>señal</b><span>${e.señal}</span>` : "") +
      (e.reglas || []).map(r => `<b>${r.nombre}</b><span style="color:var(--${r.ok ? "good" : "critical"})">${r.angulo}°${r.ok ? "" : " (Δ" + r.desvio + ")"}</span>`
        + (!r.ok && r.mensaje ? `<b style="color:var(--critical)">⚠</b><span>${r.mensaje}</span>` : "")).join("");
  }
  else if (e.type === "rep"){
    const s = e.score.total;
    if (e.n === 1) CONTEO = {n:0, bien:0, mal:0, otra:0, run:null};
    CONTEO.n = e.n;
    const c = e.clasificador && e.clasificador.clase;
    if (c === "bien") CONTEO.bien++; else if (c === "mal") CONTEO.mal++; else if (c) CONTEO.otra++;
    pintarEntrenos();
    $("#hero").textContent = s.toFixed(0);
    $("#top-hint").textContent = `rep ${e.n}${e.target ? " / " + e.target : ""} · prom ${e.promedio}`;
    $("#hero").style.color = `var(--${banda(s) === "good" ? "good" : banda(s) === "warn" ? "warning" : "critical"})`;
    const peor = e.peor[0];
    $("#consejo").className = "consejo on";
    $("#consejo").innerHTML = e.contador === "modelo"
      ? `Ciclo ${e.n}: <b>${c || "?"}</b> (${s.toFixed(0)}).`
      : s >= 85
      ? `Rep ${e.n}: <b>${bandaTxt(s)}</b> (${s.toFixed(0)}). Sigue así.`
      : `Rep ${e.n}: ${bandaTxt(s)} (${s.toFixed(0)}). Lo que más se desvía de tu base:
         <b>${peor.feature}</b>.`;
    const comparacion = e.modelos ? Object.values(e.modelos)
      .map(m => `${m.nombre} ${m.total ?? "—"}${m.clase ? " [" + m.clase + "]" : ""} (${m.latencia_ms}ms)`).join(" · ") : "";
    const l = $("#log");
    l.innerHTML = `rep ${String(e.n).padStart(2)}  ${s.toFixed(1).padStart(5)}  ${peor.feature}`
      + (comparacion ? `<br><span style="color:var(--ink-2);font-size:11.5px">${comparacion}</span>` : "")
      + `<br>` + l.innerHTML;
    cargarHistorial();
  }
  else if (e.type === "template_saved"){
    $("#hero").textContent = "OK";
    $("#top-hint").textContent = `base con ${e.template.n_reps} reps`;
    $("#hero").style.color = "var(--good)";
  }
  else if (e.type === "error"){
    $("#consejo").className = "consejo on";
    $("#consejo").textContent = e.message;
  }
  else if (e.type === "paused"){
    PAUSADO = true; actualizarControlesCamara();
  }
  else if (e.type === "resumed"){
    PAUSADO = false; actualizarControlesCamara();
  }
  else if (e.type === "grabando"){
    reiniciarConteo();
    GRABANDO = true; PAUSADO = false; actualizarControlesCamara();
    const nombre = (STATE.ejercicios.find(x => x.slug === e.exercise) || {}).name || e.exercise;
    actualizarTituloVivo(nombre, e.modo);
  }
  else if (e.type === "grabacion_detenida"){
    reiniciarConteo();
    GRABANDO = false; PAUSADO = false; actualizarControlesCamara();
  }
  else if (e.type === "grabacion"){
    cargarGrabaciones();
  }
  else if (e.type === "gesto"){
    $("#consejo").className = "consejo on";
    $("#consejo").textContent = "✋ Gesto detectado (muñeca sostenida en la esquina).";
  }
  else if (e.type === "aviso"){
    $("#consejo").className = "consejo on";
    $("#consejo").textContent = e.message;
  }
  else if (e.type === "stopped"){
    reiniciarConteo();
    ACTIVA = false; GRABANDO = false; PAUSADO = false;
    if (e.motivo && e.motivo !== "detenido desde el panel"){
      $("#consejo").className = "consejo on";
      $("#consejo").textContent = "La cámara se detuvo: " + e.motivo;
    }
    actualizarControlesCamara();
    cargarEstado(); cargarHistorial(); cargarGrabaciones();
  }
}

/* ---------------------------- gráfico ---------------------------- */
function pintarGrafico(dias){
  const svg = $("#chart"), W = 720, H = 220, L = 38, R = 12, T = 14, B = 30;
  const iw = W - L - R, ih = H - T - B;
  if (!dias.length){
    svg.innerHTML = `<text x="${W/2}" y="${H/2}" text-anchor="middle" fill="var(--muted)"
      font-size="13">Todavía no hay repeticiones registradas</text>`;
    return;
  }
  // Rellena los dias sin repeticiones: omitirlos falsearia la constancia.
  const porDia = Object.fromEntries(dias.map(d => [d.day, d]));
  const ult = [];
  for (let i = 13; i >= 0; i--){
    const f = new Date(); f.setDate(f.getDate() - i);
    const k = f.toISOString().slice(0,10);
    ult.push(porDia[k] || {day:k, avg_score:null, reps:0});
  }
  const n = ult.length, paso = iw / n, bw = Math.min(paso - 6, 42);
  const y = v => T + ih - (v / 100) * ih;
  const p = [];

  for (const g of [0, 25, 50, 75, 100]){
    p.push(`<line x1="${L}" x2="${W-R}" y1="${y(g)}" y2="${y(g)}"
      stroke="${g === 0 ? "var(--axis)" : "var(--grid)"}" stroke-width="1"/>`);
    p.push(`<text x="${L-8}" y="${y(g)+4}" text-anchor="end" fill="var(--muted)"
      font-size="11">${g}</text>`);
  }
  // Referencia: 90 = una repetición tan buena como tu promedio al calibrar.
  p.push(`<line x1="${L}" x2="${W-R}" y1="${y(90)}" y2="${y(90)}" stroke="var(--good)"
    stroke-width="1.5" stroke-dasharray="4 4" opacity=".8"/>`);
  p.push(`<text x="${W-R}" y="${y(90)-6}" text-anchor="end" fill="var(--good)"
    font-size="10.5">meta 90</text>`);

  ult.forEach((d, i) => {
    const x = L + i * paso + (paso - bw) / 2;
    if (d.avg_score === null){
      p.push(`<line x1="${x}" x2="${x+bw}" y1="${y(0)}" y2="${y(0)}"
        stroke="var(--muted)" stroke-width="2.5" opacity=".45"/>`);
    } else {
      const v = d.avg_score;
      const alto = Math.max(ih - (y(v) - T), 2), yy = y(v), r = Math.min(4, bw / 2, alto);
      p.push(`<path d="M${x} ${yy+alto} L${x} ${yy+r} Q${x} ${yy} ${x+r} ${yy}
        L${x+bw-r} ${yy} Q${x+bw} ${yy} ${x+bw} ${yy+r} L${x+bw} ${yy+alto} Z"
        fill="var(--series-1)"/>`);
    }
    p.push(`<rect x="${L + i*paso}" y="${T}" width="${paso}" height="${ih}" fill="transparent"
      data-d="${d.day}" data-v="${d.avg_score === null ? "" : d.avg_score}"
      data-r="${d.reps}" class="hit"/>`);
    if (n <= 8 || i % 2 === 0)
      p.push(`<text x="${x + bw/2}" y="${H - B + 16}" text-anchor="middle" fill="var(--muted)"
        font-size="10.5">${d.day.slice(5)}</text>`);
  });
  svg.innerHTML = p.join("");

  const tip = $("#tip");
  svg.querySelectorAll(".hit").forEach(el => {
    el.onmouseenter = ev => {
      tip.className = "tip on";
      tip.innerHTML = el.dataset.v === ""
        ? `<b>${el.dataset.d}</b>sin entrenamiento`
        : `<b>${el.dataset.d}</b>${(+el.dataset.v).toFixed(1)} puntos · ${el.dataset.r} reps`;
      const r = svg.getBoundingClientRect(), c = tip.parentElement.getBoundingClientRect();
      tip.style.left = (ev.clientX - c.left + 12) + "px";
      tip.style.top  = (ev.clientY - c.top  - 10) + "px";
    };
    el.onmouseleave = () => { tip.className = "tip"; };
  });
}

function pintarTabla(todas){
  const reps = todas.slice(0, 12);
  if (!reps.length){ $("#tabla").innerHTML = `<div class="vacio">Sin repeticiones todavía</div>`; return; }
  $("#tabla").innerHTML = `<table><thead><tr>
      <th>Hora</th><th>Ejercicio</th><th class="num">Puntaje</th>
      <th class="num">Duración</th><th>Lectura</th></tr></thead><tbody>` +
    reps.map(r => `<tr>
      <td>${r.ts.slice(11,16)}</td><td>${r.exercise}</td>
      <td class="num">${fmt(r.score)}</td>
      <td class="num">${(r.duration_ms/1000).toFixed(1)} s</td>
      <td><span class="st ${banda(r.score)}">${bandaTxt(r.score)}</span></td>
    </tr>`).join("") + `</tbody></table>`;
}

/* ---------------------------- arranque ---------------------------- */
// El .bat abre el navegador con un tiempo de espera fijo antes de que el
// servicio termine de levantar; si esta pagina carga antes que el backend
// este escuchando, el primer fetch falla. En vez de rendirse, reintenta
// sin limite hasta que el servicio responda -- no hay nada que "timeoutear",
// solo hay que esperar a que arranque.
async function arrancar(){
  for (;;){
    try { await cargarEstado(); break; }
    catch (e) { await new Promise(r => setTimeout(r, 1000)); }
  }
  cargarHistorial(); cargarGrabaciones(); cargarCamaras(); conectar();
}
arrancar();

setInterval(() => {
  if (!ACTIVA) cargarEstado();
  if (TAB === "sistema") cargarLog();
}, 15000);
