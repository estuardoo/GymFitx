# `scripts/camara.py`

```text
Utilidad: descubre que indices de camara responden en esta maquina.

    python scripts/camara.py

El panel web hace lo mismo desde el boton "Detectar camaras" (endpoint
/api/cameras); ambos caminos usan src.captura.fuentes.camara.list_cameras para no duplicar
la logica de sondeo.
```

