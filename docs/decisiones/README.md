# Decisiones de diseno (ADR)

Cadena que pide CRISP-DM: **decision → justificacion → codigo → parametro → salida → metrica**. Cada archivo la completa para una decision; cada seccion de `params.yaml` esta citada en alguna (lo verifica `tests/test_trazabilidad.py`) y las etapas de `dvc.yaml` apuntan aqui desde su `desc`.

| # | Decision | Etapa | Parametro (params.yaml) | Estado |
|---|---|---|---|---|
| [0001](0001-datos-en-disco-crudo-y-respaldo-sql.md) | Disco = fuente, SQL = respaldo | 3.1 | `seleccion` | aceptada |
| [0002](0002-particion-por-grabacion.md) | Validacion por grabacion | 3.5 | `entrenamiento` | aceptada |
| [0003](0003-base-de-conteo-desde-el-primer-clip.md) | Base de conteo | vivo | `base_clip` | aceptada |
| [0004](0004-reglas-de-postura-en-el-yaml.md) | Reglas en `ejercicios/*.yaml` | 3.3 | — | aceptada |
| [0005](0005-umbrales-de-limpieza.md) | Umbrales de limpieza | 3.2 | `limpieza` | aceptada |
| [0006](0006-clase-fuera-registros-generados.md) | Clase «fuera» generada | 3.3 | `construccion` | aceptada |
| [0007](0007-formato-del-vector.md) | Formato del vector | 3.5 | `formato` | aceptada |
| [0008](0008-documentacion-del-codigo.md) | Docs del codigo generadas | — | — | aceptada |
| [0009](0009-flujo-github-ramas-pr-y-proteccion.md) | Flujo GitHub | crit. 7 | — | aceptada |
| [0010](0010-remoto-de-datos-dvc.md) | Remoto DVC | — | — | **pendiente** |

Plantilla de una nueva: copiar la 0005 y rellenar Estado · Contexto · Decision · Parametro · Codigo · Salida/metrica · Issue.
Los `#pendiente` se reemplazan por el numero del issue de GitHub al crearlo (commits `Refs #N`, PR `Closes #N`).
