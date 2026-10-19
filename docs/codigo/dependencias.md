# Dependencias entre ramas de `src/`

Cada celda = cuantos imports hay desde la rama de la FILA hacia la rama de la COLUMNA. La regla del arbol (`tests/test_capas.py`): solo se importa del tronco o de ramas anteriores del pipeline, asi que todo cae bajo la diagonal.

| desde \ hacia | nucleo | almacenamiento | captura | procesamiento | evaluacion | sesion | etiquetado | preparacion | entrenamiento | interfaz |
|---|---|---|---|---|---|---|---|---|---|---|
| **nucleo** |  |  |  |  |  |  |  |  |  |  |
| **almacenamiento** | 6 |  |  |  |  |  |  |  |  |  |
| **captura** | 5 |  |  |  |  |  |  |  |  |  |
| **procesamiento** | 10 |  | 1 |  |  |  |  |  |  |  |
| **evaluacion** | 9 |  |  | 2 |  |  |  |  |  |  |
| **sesion** | 8 |  | 1 | 3 | 4 |  |  |  |  |  |
| **etiquetado** | 17 | 8 |  | 9 | 2 |  |  |  |  |  |
| **preparacion** | 5 |  |  | 5 |  |  | 2 |  |  |  |
| **entrenamiento** | 7 | 4 |  | 2 | 1 |  | 8 | 2 |  |  |
| **interfaz** | 29 | 6 | 2 | 3 | 8 | 4 | 14 | 1 | 6 |  |
