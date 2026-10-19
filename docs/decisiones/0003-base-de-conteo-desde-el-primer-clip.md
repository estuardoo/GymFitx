# 0003 · Base de conteo desde el primer clip «bien»

- **Estado:** aceptada · **Etapa:** uso en vivo (fuera de etapa 3) · **Issue:** #4
- **Contexto:** contar repeticiones necesita saber que es «arriba» y «abajo» de la senal de cada ejercicio.
- **Decision:** se toma el recorrido P10..P90 de la senal del primer clip bien; la repeticion cuenta al volver a `frac_fin` del recorrido.
- **Parametro:** `base_clip.frac_low`, `frac_high`, `frac_fin`.
- **Codigo:** `src/evaluacion/base_clip.py`.
