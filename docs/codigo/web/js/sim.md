# `src/interfaz/web/js/sim.js`

> Pestana SIM: verificacion visual de deteccion + normalizacion de un clip. API: interfaz/api/sim.py Vista 1: video original. Vista 2: esqueleto crudo (points_screen) sincronizado con el video (misma tecnica de cortes.js: idxCuadro + tolerancia de 250ms), con angulos. Vista 3: independiente, el clip normalizado (DTW-alineado) contra el base, animado por indice de cuadro (no por tiempo real).

## Funciones

- `aplicarSimOpciones`
- `cargarAvatarSim`
- `cargarSimOpciones`
- `cargarSimTipos`
- `dibujarSim2`
- `dibujarSim3`
- `elegirSimClip`
- `idxCuadroSim`
- `renderSimClips`
- `renderSimLeyenda3`
- `simCalcBBox`
- `simIrAFrame3`
- `simSetModo2`
- `simTogglePlay3`
