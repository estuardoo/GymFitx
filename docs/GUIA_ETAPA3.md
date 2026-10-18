# Guia de la etapa 3 (CRISP-DM) — que hacer y como verificarlo

Todo el codigo ya esta. Esta guia es lo que **solo tu puedes hacer** (cuentas, tokens, decisiones) y como comprobar cada criterio.

## 1. Flujo del dia a dia
1. Abre un **issue** en GitHub (ej. «Subir max_nan_pct a 25»).
2. Edita `params.yaml` o el codigo. El entrenamiento y las etapas leen del **disco**.
3. `dvc repro` (rehace solo lo que cambio) → revisa `reportes/` y `docs/diccionario/`.
4. Anota/ajusta la decision en `docs/decisiones/`.
5. `dvc push` (datos al remoto) y envia a GitHub con **`subir_github/SUBIR_GITHUB.bat`** con rama nueva, issue `N` y «Abrir PR» (commit `Refs #N`, PR `Closes #N`). Si es una version del conjunto, etiqueta `datos-vN`.
6. Otra persona revisa y hace merge.

Respaldo SQL: Sistema → «Datos en disco · respaldo en SQL Server». Con *al cortar* y *al entrenar* activos, SQL se actualiza solo; «Respaldar ahora» lo fuerza. Descomposicion/Ranking aun leen SQL, por eso conviene dejarlos activos.

## 2. Preparar DVC (una vez)
```
scripts\iniciar_dvc.bat                       # instala dvc, git init, dvc init, dvc add de lo pesado
dvc remote add -d almacen D:\respaldo_dvc     # elige UNO (decision 0010):
#   carpeta/unidad de red:  dvc remote add -d almacen \\servidor\gymfitx
#   Google Drive:           dvc remote add -d almacen gdrive://<ID_CARPETA>
dvc push
git add datos/*.dvc datos/.gitignore .dvc dvc.yaml dvc.lock params.yaml
```
Si `pip install dvc` falla compilando `antlr4`: `pip install "setuptools<70" wheel` primero (ya lo hace el .bat).
Luego `dvc repro` genera `dvc.lock`: **commitealo**.

## 3. GitHub (una vez)
- En `subir_github/SUBIR_GITHUB.bat`: usuario, token, URL del repo y rama, rama `main`, nombre, correo y **token** (fine-grained: Contents RW, Pull requests RW, Issues RW y Administration *read* para ver la proteccion). El token queda solo en `subir_github/config.json` (ignorado por git); no lo pegues en chats ni commits.
- Settings → Branches → regla sobre `main`: *Require a pull request* (1 aprobacion), *Require status checks* (`calidad`), sin pushes directos. Verifica con el boton «Ver proteccion».
- Variable de repo `DVC_ACTIVO=true` (+ secret del remoto) cuando el remoto sea accesible desde el CI: activa clonar → `dvc pull` → `dvc repro --force` → `dvc.lock` sin cambios.
- Issues sugeridos: umbrales de limpieza (0005) · clase fuera (0006) · agrupar por persona (0002) · remoto DVC (0010) · mover Descomposicion/Ranking a disco · `exportar_slurm` a disco. Reemplaza los `#pendiente` de `docs/decisiones/` por su numero.

### Varios integrantes
- **Un token por persona**, guardado en su propio equipo (SUBIR_GITHUB → Guardar → `subir_github/config.json`, que no se sube). No se comparte ni se manda: si alguien lo pierde se revoca el suyo sin afectar a los demas. Nombre y correo tambien son de cada uno (firman sus commits).
- El dueño agrega a cada persona en GitHub → Settings → Collaborators (permiso **Write**). «👤 ¿Quien soy?» confirma que el token sirve y puede enviar.
- Cada quien trabaja en su rama (`ana/umbrales`): elige la rama en el selector, marca el **modulo/area** a enviar, «⬇ Traer cambios» antes de enviar, y abre un Pull Request; otra persona lo revisa y hace el merge a `main` (protegida).
- Para continuar la rama de un compañero basta elegirla en el selector.

## 4. Verificacion por criterio
| Criterio | Comando / evidencia |
|---|---|
| 1 Reproducibilidad | `dvc repro --force && git diff --exit-code dvc.lock` (lo hace el CI) |
| 2 Separacion datos/codigo | `git ls-files datos` solo lista `.dvc`; el crudo no es `outs` de ninguna etapa |
| 3 Cobertura de decisiones | `pytest tests/test_trazabilidad.py` + `docs/decisiones/README.md` |
| 4 Parametrizacion | ningun umbral en `src/`: `grep -rn "params(" src/` y `params.yaml` |
| 5 Diccionario | `docs/diccionario/<ej>.md` (falla la etapa si no coincide el numero de columnas) |
| 6 Informe de limpieza | `reportes/limpieza_<ej>.md` + `dvc metrics show` |
| 7 Traza de colaboracion | historial de PR con `Closes #N`, rama protegida, etiquetas `datos-vN` |

## 5. Lo que falta de tu lado (no lo puedo hacer yo)
1. Elegir y crear el **remoto DVC** (0010) y correr `dvc push`.
2. Crear el **token** y activar la **proteccion de rama**; abrir los issues.
3. Congelar el entorno: `pip freeze > requirements.lock.txt` en tu `.venv` y commitearlo.
4. Enlazar el **informe de calidad de la etapa 2** desde `docs/decisiones/0005` (justifica los umbrales con datos reales).
5. Confirmar si el prefijo numerico del nombre del video es el **ID de la persona** (si si, el grupo de validacion pasa a persona).
6. Commitear `dvc.lock` tras el primer `dvc repro`.
