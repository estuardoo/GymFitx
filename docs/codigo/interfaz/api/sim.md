# `src/interfaz/api/sim.py`

```text
SIM: verificacion visual de deteccion + normalizacion, sin recalcular nada nuevo.

3 vistas de un clip elegido:
  1. El video original (.mp4 ya cortado).
  2. Esqueleto CRUDO superpuesto en pantalla (points_screen guardado en el .npz del clip por
     src/etiquetado/exportar.recorta_npz) + el valor de cada angulo/proporcion activa, junto a sus puntos.
  3. Esqueleto NORMALIZADO (table_frames_fix de SQL) del clip elegido, YA ALINEADO en tiempo (DTW) contra
     el clip 'base' de su ejercicio -- la MISMA alineacion que calcula table_indicator (ver
     src/evaluacion/similitud.py), asi que lo que se ve aca es exactamente lo que puntua el sistema.
```

## `_conexiones_por_nombre`

`def _conexiones_por_nombre(catalogo, nombres)`

```text
Pares (i, j) de PUNTOS.conexiones_kpoints() pero reindexados a la POSICION de cada kpoint dentro de
'nombres' (el orden real del arreglo que se dibuja, que puede venir en otro orden -- o ser un
subconjunto -- del catalogo del ejercicio), en vez del orden del catalogo. conexiones_kpoints() da
indices relativos a 'catalogo'; ac se traduce cada uno por nombre y se descarta el hueso si algun
extremo no esta en 'nombres', en vez de tirar TODAS las conexiones por un solo kpoint que no coincida.
```

## `_fila_de`

`def _fila_de(clip)`

_sin docstring_

## `_npz_de`

`def _npz_de(clip)`

```text
(fila del manifest, .npz abierto) del clip, o LookupError con el motivo.
```

## `sim_opciones`

`def sim_opciones(tipo=None)`

Ruta: **GET /api/sim/opciones**

```text
Ejercicio(s) y sus clips por clase (igual que Descomposicion) -- para los selectores del panel.
```

## `_puntos_por_metrica`

`def _puntos_por_metrica(nombres, kpoints, features)`

```text
{nombre_metrica: [nombres de puntos involucrados]} -- para poner el numero de cada angulo/proporcion
cerca de sus puntos (centroide).
```

## `sim_crudo`

`def sim_crudo(clip: str)`

Ruta: **GET /api/sim/crudo**

```text
Puntos SIN normalizar (coordenadas de pantalla 0-1, ver points_screen) + angulos/proporciones,
cuadro a cuadro, con su tiempo relativo al INICIO DEL CLIP -- para el overlay sincronizado sobre el
video ya cortado (vista 2).
```

## `sim_cuerpo3d`

`def sim_cuerpo3d(clip: str)`

Ruta: **GET /api/sim/cuerpo3d**

```text
Puntos 3D en metros (world, origen en la cadera) del clip, cuadro a cuadro, para el avatar 3D de SIM.
```

## `sim_normalizado`

`def sim_normalizado(tipo: int, base: str, clip: str)`

Ruta: **GET /api/sim/normalizado**

```text
Puntos normalizados+remuestreados (table_frames_fix de SQL) del clip 'base' y del 'clip' elegido, con
este ultimo YA ALINEADO en tiempo (DTW) a los frames del base -- misma funcion (alinear(), ver
evaluacion/similitud.py) que calcula table_indicator. No renormaliza nada: es la tabla que ya arma
tablas.py, solo que aca se ve animada en vez de reducida a un numero (vista 3).
```

