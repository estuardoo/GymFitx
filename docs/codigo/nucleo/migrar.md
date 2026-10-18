# `src/nucleo/migrar.py`

```text
Trae los datos del proyecto viejo (GYMFITX, con core/ + fgml/) a este.

    python -m src.nucleo.migrar                 # origen por defecto: ../GYMFITX
    python -m src.nucleo.migrar --origen D:\otro\GYMFITX

Solo COPIA: el proyecto viejo queda intacto como respaldo. Nunca pisa un
archivo que ya exista aca. Se corre sola una vez desde GYMFITX.bat y deja
datos/.migrado.json; despues no vuelve a hacer nada.

Que se trae (y a donde):
    recordings/                 -> datos/grabaciones/
    templates/*.npz             -> datos/plantillas/
    models/*.task               -> modelos/
    fgml/dataset/               -> datos/clips/
    fgml/entrenamientos/        -> datos/entrenamientos/
    fgml/labels.json            -> datos/etiquetas.json   (y el resto de json del cortador)
    fgml/pipeline.yaml          -> datos/ajustes.yaml
    fgml/pitch/                 -> docs/pitch/
    exercises/*.yaml            -> ejercicios/            (tus catalogos de puntos editados)
    gymfitx.db, acceso.json, pendientes_sql.jsonl, cloudflared.exe
No se trae: fgml/data/ (copia vieja de recordings), .preview_cache (se
regenera sola) ni codigo.
```

## `plan`

`def plan(origen: Path, raiz: Path, datos: Path) -> list[tuple[Path, Path]]`

```text
(origen, destino) de cada carpeta o archivo a copiar.
```

## `_copiar`

`def _copiar(a: Path, b: Path, sobrescribir: bool) -> int`

```text
Copia a -> b (archivo o carpeta). Devuelve cuantos archivos copio.
```

## `migrar`

`def migrar(origen: Path, raiz: Path=ROOT, datos: Path=DATOS_DIR) -> dict`

_sin docstring_

## `main`

`def main() -> None`

_sin docstring_

