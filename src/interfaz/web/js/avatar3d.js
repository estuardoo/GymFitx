/* SIM 4: avatar 3D. Los 33 puntos world del .npz son los huesos; encima va el volumen (musculos) hecho con
   cilindros y elipsoides. Modulo ES: three.js va local en js/vendor (sin internet). Lo usa sim.js via window.avatar3d. */
import * as THREE from './vendor/three.module.min.js';

const $A = s => document.querySelector(s);
const V = (x = 0, y = 0, z = 0) => new THREE.Vector3(x, y, z);

// musculos: [desde, hasta, radio en "desde", radio en "hasta", posicion del vientre 0-1]  (metros)
const MUSCULOS = [
  ['LEFT_SHOULDER', 'LEFT_ELBOW', .050, .038, .35], ['RIGHT_SHOULDER', 'RIGHT_ELBOW', .050, .038, .35],
  ['LEFT_ELBOW', 'LEFT_WRIST', .040, .027, .30], ['RIGHT_ELBOW', 'RIGHT_WRIST', .040, .027, .30],
  ['LEFT_HIP', 'LEFT_KNEE', .085, .055, .38], ['RIGHT_HIP', 'RIGHT_KNEE', .085, .055, .38],
  ['LEFT_KNEE', 'LEFT_ANKLE', .058, .036, .30], ['RIGHT_KNEE', 'RIGHT_ANKLE', .058, .036, .30],
];
const HUESOS = [
  ['LEFT_SHOULDER', 'RIGHT_SHOULDER'], ['LEFT_HIP', 'RIGHT_HIP'],
  ['LEFT_SHOULDER', 'LEFT_ELBOW'], ['LEFT_ELBOW', 'LEFT_WRIST'], ['RIGHT_SHOULDER', 'RIGHT_ELBOW'], ['RIGHT_ELBOW', 'RIGHT_WRIST'],
  ['LEFT_SHOULDER', 'LEFT_HIP'], ['RIGHT_SHOULDER', 'RIGHT_HIP'],
  ['LEFT_HIP', 'LEFT_KNEE'], ['LEFT_KNEE', 'LEFT_ANKLE'], ['RIGHT_HIP', 'RIGHT_KNEE'], ['RIGHT_KNEE', 'RIGHT_ANKLE'],
  ['LEFT_ANKLE', 'LEFT_HEEL'], ['LEFT_HEEL', 'LEFT_FOOT_INDEX'], ['LEFT_ANKLE', 'LEFT_FOOT_INDEX'],
  ['RIGHT_ANKLE', 'RIGHT_HEEL'], ['RIGHT_HEEL', 'RIGHT_FOOT_INDEX'], ['RIGHT_ANKLE', 'RIGHT_FOOT_INDEX'],
  ['LEFT_WRIST', 'LEFT_INDEX'], ['LEFT_WRIST', 'LEFT_PINKY'], ['RIGHT_WRIST', 'RIGHT_INDEX'], ['RIGHT_WRIST', 'RIGHT_PINKY'],
];
const ARTICULACIONES = ['LEFT_SHOULDER', 'RIGHT_SHOULDER', 'LEFT_ELBOW', 'RIGHT_ELBOW', 'LEFT_WRIST', 'RIGHT_WRIST',
  'LEFT_HIP', 'RIGHT_HIP', 'LEFT_KNEE', 'RIGHT_KNEE', 'LEFT_ANKLE', 'RIGHT_ANKLE'];
const SUAVIZADO = 2;   // ventana de +-2 cuadros (la profundidad 3D de una sola camara tiembla)

const S = { ren: null, scene: null, cam: null, cont: null, d: null, t: [], pts: [], idx: {}, f: 0, play: false,
  last: 0, az: .5, el: .12, dist: 3.2, huesos: [], musculos: [], formas: [], piso: null };

const matHueso = new THREE.MeshStandardMaterial({ color: 0xe6e9ef, roughness: .5, metalness: .1 });
const matMusculo = new THREE.MeshStandardMaterial({ color: 0xb8473d, roughness: .62, metalness: 0 });

function unitaria(a, b) {   // dos vectores perpendiculares a la direccion a->b
  const d = b.clone().sub(a).normalize();
  const ref = Math.abs(d.y) < .9 ? V(0, 1, 0) : V(1, 0, 0);
  const u = new THREE.Vector3().crossVectors(d, ref).normalize();
  return [u, new THREE.Vector3().crossVectors(d, u).normalize()];
}

// cilindro (afinado) entre a y b: la altura unitaria se estira con la longitud del eje
function colocarSegmento(mesh, a, b) {
  const [u, w] = unitaria(a, b);
  mesh.matrix.makeBasis(u, b.clone().sub(a), w).setPosition(a.clone().add(b).multiplyScalar(.5));
}
function colocarElipsoide(mesh, c, x, y, z) { mesh.matrix.makeBasis(x, y, z).setPosition(c); }

function malla(geo, mat, grupo) {
  const m = new THREE.Mesh(geo, mat);
  m.matrixAutoUpdate = false;
  S.scene.add(m); grupo.push(m);
  return m;
}
const esfera = new THREE.SphereGeometry(1, 20, 14);

function construir() {
  for (const [a, b, r0, r1] of MUSCULOS) {
    const cil = malla(new THREE.CylinderGeometry(r1, r0, 1, 22, 1), matMusculo, S.musculos);
    const sa = malla(esfera, matMusculo, S.musculos), sb = malla(esfera, matMusculo, S.musculos);
    const vientre = malla(esfera, matMusculo, S.musculos);
    S.formas.push({ tipo: 'musculo', a, b, r0, r1, cil, sa, sb, vientre, t: MUSCULOS.find(m => m[0] === a && m[1] === b)[4] });
  }
  for (const k of ['torso', 'abdomen', 'pelvis', 'cabeza', 'cuello', 'manoL', 'manoR', 'pieL', 'pieR', 'delL', 'delR', 'glutL', 'glutR']) {
    const m = k === 'cuello'
      ? malla(new THREE.CylinderGeometry(.045, .055, 1, 18, 1), matMusculo, S.musculos)
      : malla(esfera, matMusculo, S.musculos);
    S.formas.push({ tipo: k, mesh: m });
  }
  for (const [a, b] of HUESOS) S.formas.push({ tipo: 'hueso', a, b, mesh: malla(new THREE.CylinderGeometry(.011, .011, 1, 10, 1), matHueso, S.huesos) });
  for (const n of ARTICULACIONES) S.formas.push({ tipo: 'junta', n, mesh: malla(esfera, matHueso, S.huesos) });
}

function suavizar(p) {   // media movil por coordenada, ignorando huecos (null)
  return p.map((cuadro, i) => cuadro.map((pt, j) => {
    let n = 0; const s = [0, 0, 0];
    for (let k = Math.max(0, i - SUAVIZADO); k <= Math.min(p.length - 1, i + SUAVIZADO); k++) {
      const q = p[k][j];
      if (q && q[0] !== null) { n++; s[0] += q[0]; s[1] += q[1]; s[2] += q[2]; }
    }
    return n && pt && pt[0] !== null ? s.map(v => v / n) : pt;
  }));
}

const espejo = () => $A('#avEspejo').checked;
function punto(i, n) {   // world MediaPipe (x der, y abajo, z hacia la camara negativo) -> three (y arriba); espejo = como el Panel
  const q = S.pts[i][S.idx[n]];
  return q && q[0] !== null ? V((espejo() ? -1 : 1) * q[0], -q[1], -q[2]) : null;
}

function actualizar() {
  if (!S.pts.length) return;
  const i = S.f, P = n => punto(i, n);
  const mid = (a, b) => a && b ? a.clone().add(b).multiplyScalar(.5) : null;
  const sI = P('LEFT_SHOULDER'), sD = P('RIGHT_SHOULDER'), hI = P('LEFT_HIP'), hD = P('RIGHT_HIP');
  const mS = mid(sI, sD), mH = mid(hI, hD);
  const ver = (m, ok) => { m.visible = !!ok; return !!ok; };

  // cabeza: ejes desde las orejas y la nariz
  const oI = P('LEFT_EAR'), oD = P('RIGHT_EAR'), nariz = P('NOSE');
  let cab = null;
  if (oI && oD && nariz) {
    const c = mid(oI, oD), x = oD.clone().sub(oI).normalize(), f = nariz.clone().sub(c);
    const y = new THREE.Vector3().crossVectors(f, x).normalize(), z = new THREE.Vector3().crossVectors(x, y);
    cab = { c: c.clone().addScaledVector(y, .02).addScaledVector(z, -.02), x, y, z };
  }

  for (const f of S.formas) {
    if (f.tipo === 'hueso') {
      const a = P(f.a), b = P(f.b);
      if (ver(f.mesh, a && b)) colocarSegmento(f.mesh, a, b);
    } else if (f.tipo === 'junta') {
      const a = P(f.n);
      if (ver(f.mesh, a)) f.mesh.matrix.makeScale(.022, .022, .022).setPosition(a);
    } else if (f.tipo === 'musculo') {
      const a = P(f.a), b = P(f.b), ok = a && b;
      ver(f.cil, ok); ver(f.sa, ok); ver(f.sb, ok); ver(f.vientre, ok);
      if (!ok) continue;
      colocarSegmento(f.cil, a, b);
      f.sa.matrix.makeScale(f.r0, f.r0, f.r0).setPosition(a);
      f.sb.matrix.makeScale(f.r1, f.r1, f.r1).setPosition(b);
      const d = b.clone().sub(a), [u, w] = unitaria(a, b), r = (f.r0 + (f.r1 - f.r0) * f.t) * 1.2;
      colocarElipsoide(f.vientre, a.clone().addScaledVector(d, f.t), u.clone().multiplyScalar(r), d.clone().multiplyScalar(.3), w.clone().multiplyScalar(r));
    } else if (f.tipo === 'delL' || f.tipo === 'delR') {
      const a = f.tipo === 'delL' ? sI : sD;
      if (ver(f.mesh, a)) f.mesh.matrix.makeScale(.062, .062, .062).setPosition(a);
    } else if (f.tipo === 'glutL' || f.tipo === 'glutR') {
      const a = f.tipo === 'glutL' ? hI : hD;
      if (ver(f.mesh, a)) f.mesh.matrix.makeScale(.085, .085, .085).setPosition(a);
    }
  }

  // tronco: pecho, abdomen y pelvis a lo largo de la columna (cadera -> hombros)
  const f = t => S.formas.find(x => x.tipo === t).mesh;
  const okT = ver(f('torso'), mS && mH && sI && sD), okA = ver(f('abdomen'), mS && mH), okP = ver(f('pelvis'), mH && hI && hD);
  if (okT && okA && okP) {
    const col = mS.clone().sub(mH), anchoS = sD.clone().sub(sI), anchoH = hD.clone().sub(hI);
    const fr = new THREE.Vector3().crossVectors(anchoS, col).normalize().multiplyScalar(-1);   // hacia delante del pecho
    const unit = v => v.clone().normalize();
    colocarElipsoide(f('torso'), mH.clone().addScaledVector(col, .70), unit(anchoS).multiplyScalar(anchoS.length() * .54), col.clone().multiplyScalar(.30), fr.clone().multiplyScalar(.10));
    colocarElipsoide(f('abdomen'), mH.clone().addScaledVector(col, .34), unit(anchoH).multiplyScalar(anchoH.length() * .62), col.clone().multiplyScalar(.26), fr.clone().multiplyScalar(.085));
    colocarElipsoide(f('pelvis'), mH, unit(anchoH).multiplyScalar(anchoH.length() * .62), col.clone().multiplyScalar(.12), fr.clone().multiplyScalar(.095));
  }
  // cabeza y cuello
  if (ver(f('cabeza'), cab)) colocarElipsoide(f('cabeza'), cab.c, cab.x.clone().multiplyScalar(.085), cab.y.clone().multiplyScalar(.115), cab.z.clone().multiplyScalar(.10));
  if (ver(f('cuello'), cab && mS)) colocarSegmento(f('cuello'), mS, cab.c.clone().addScaledVector(cab.y, -.07));
  // manos y pies: elipsoides alargados
  for (const [lado, L] of [['L', 'LEFT'], ['R', 'RIGHT']]) {
    const w = P(`${L}_WRIST`), i1 = P(`${L}_INDEX`), p1 = P(`${L}_PINKY`);
    if (ver(f('mano' + lado), w && i1 && p1)) {
      const m = mid(i1, p1), d = m.clone().sub(w), x = i1.clone().sub(p1).normalize().multiplyScalar(.045);
      const z = new THREE.Vector3().crossVectors(x, d).normalize().multiplyScalar(.022);
      colocarElipsoide(f('mano' + lado), w.clone().addScaledVector(d, .55), x, d.clone().multiplyScalar(.9), z);
    }
    const t = P(`${L}_ANKLE`), h = P(`${L}_HEEL`), pt = P(`${L}_FOOT_INDEX`);
    if (ver(f('pie' + lado), t && h && pt)) {
      const d = pt.clone().sub(h), y = V(0, 1, 0), x = new THREE.Vector3().crossVectors(d, y).normalize().multiplyScalar(.04);
      colocarElipsoide(f('pie' + lado), h.clone().addScaledVector(d, .5), x, d.clone().multiplyScalar(.58), y.multiplyScalar(.035));
    }
  }
  filtrar();   // las casillas Huesos/Musculos apagan encima de lo que ya muestra el cuadro
  $A('#simAvSlider').value = i;
  $A('#simAvInfo').textContent = `cuadro ${i + 1}/${S.pts.length} · ${Math.round(S.t[i] || 0)} ms`;
}

function cuadroEn(t) {   // ultimo cuadro con tiempo <= t
  let lo = 0, hi = S.t.length - 1;
  while (lo < hi) { const m = (lo + hi + 1) >> 1; if (S.t[m] <= t) lo = m; else hi = m - 1; }
  return lo;
}

function camara() {
  S.cam.position.set(S.dist * Math.sin(S.az) * Math.cos(S.el), .1 + S.dist * Math.sin(S.el), S.dist * Math.cos(S.az) * Math.cos(S.el));
  S.cam.lookAt(0, -.05, 0);
}

function bucle(ts) {
  requestAnimationFrame(bucle);
  if (!S.ren) return;
  const vid = $A('#simV1');
  if ($A('#avSeguir').checked && vid && vid.src && !vid.paused && S.pts.length) {
    S.f = cuadroEn(vid.currentTime * 1000); actualizar();
  } else if (S.play && S.pts.length) {
    S.cursor = (S.cursor ?? S.t[S.f]) + (ts - S.last);
    if (S.cursor > S.t[S.t.length - 1]) S.cursor = S.t[0];
    S.f = cuadroEn(S.cursor); actualizar();
  }
  S.last = ts;
  S.ren.render(S.scene, S.cam);
}

function iniciar() {
  if (S.ren) return;
  S.cont = $A('#simAv');
  S.scene = new THREE.Scene();
  S.scene.background = new THREE.Color(0x0d1117);
  S.cam = new THREE.PerspectiveCamera(40, 1, .05, 50);
  S.ren = new THREE.WebGLRenderer({ antialias: true });
  S.ren.setPixelRatio(Math.min(devicePixelRatio, 2));
  S.cont.appendChild(S.ren.domElement);
  S.scene.add(new THREE.HemisphereLight(0xffffff, 0x2a2f3a, 1.5));
  const sol = new THREE.DirectionalLight(0xffffff, 2.2); sol.position.set(2, 3, 3); S.scene.add(sol);
  S.piso = new THREE.GridHelper(3, 12, 0x3a4150, 0x232833); S.scene.add(S.piso);
  construir();
  const ajustar = () => { const w = S.cont.clientWidth, h = S.cont.clientHeight; if (!w || !h) return; S.ren.setSize(w, h); S.cam.aspect = w / h; S.cam.updateProjectionMatrix(); };
  new ResizeObserver(ajustar).observe(S.cont); ajustar();
  // orbitar con el mouse: arrastrar gira, rueda acerca
  let arr = null;
  const cv = S.ren.domElement; cv.style.touchAction = 'none';
  cv.addEventListener('pointerdown', e => { arr = [e.clientX, e.clientY]; cv.setPointerCapture(e.pointerId); });
  cv.addEventListener('pointerup', () => { arr = null; });
  cv.addEventListener('pointermove', e => { if (!arr) return; S.az -= (e.clientX - arr[0]) * .008; S.el = Math.max(-1.2, Math.min(1.4, S.el + (e.clientY - arr[1]) * .008)); arr = [e.clientX, e.clientY]; camara(); });
  cv.addEventListener('wheel', e => { e.preventDefault(); S.dist = Math.max(1.2, Math.min(8, S.dist * (1 + Math.sign(e.deltaY) * .08))); camara(); }, { passive: false });
  $A('#avHuesos').onchange = $A('#avMusculos').onchange = $A('#avEspejo').onchange = actualizar;
  $A('#avSuavizar').onchange = () => { if (S.d) cargar(S.d, true); };
  camara(); requestAnimationFrame(bucle);
}

function filtrar() {
  const h = $A('#avHuesos').checked, m = $A('#avMusculos').checked;
  S.huesos.forEach(x => { x.visible = x.visible && h; }); S.musculos.forEach(x => { x.visible = x.visible && m; });
}

function cargar(d, mantener) {
  iniciar();
  S.d = d;
  S.idx = Object.fromEntries(d.nombres.map((n, i) => [n, i]));
  S.t = d.t_ms;
  S.pts = $A('#avSuavizar').checked ? suavizar(d.puntos) : d.puntos;
  if (!mantener) { S.f = 0; S.cursor = undefined; S.play = false; $A('#simAvPP').textContent = '▶ Play'; }
  $A('#simAvSlider').max = Math.max(0, S.pts.length - 1);
  // piso: el punto mas bajo de los pies en todo el clip
  let bajo = 0;
  for (const c of S.pts) for (const n of ['LEFT_FOOT_INDEX', 'RIGHT_FOOT_INDEX', 'LEFT_HEEL', 'RIGHT_HEEL']) { const q = c[S.idx[n]]; if (q && q[1] !== null) bajo = Math.max(bajo, q[1]); }
  S.piso.position.y = -bajo - .02;
  actualizar();
}

function alternar() {
  S.play = !S.play; S.cursor = undefined;
  $A('#simAvPP').textContent = S.play ? '⏸ Pausa' : '▶ Play';
}
function irA(i) { S.f = i; S.cursor = S.t[i]; actualizar(); }
function reiniciarCamara() { S.az = .5; S.el = .12; S.dist = 3.2; camara(); }
function vacio(msg) { if (S.ren) { S.pts = []; S.formas.forEach(f => { if (f.mesh) f.mesh.visible = false; }); } $A('#simAvInfo').textContent = msg; }

window.avatar3d = { cargar, alternar, irA, reiniciarCamara, vacio };
