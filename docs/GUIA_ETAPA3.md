# Guia de la etapa 3 (CRISP-DM) — que hacer y como verificarlo

Todo el codigo ya esta. Esta guia es lo que **solo tu puedes hacer** (cuentas, tokens, decisiones) y como comprobar cada criterio.

## 1. Flujo del dia a dia
1. Abre un **issue** en GitHub (ej. «Subir max_nan_pct a 25»).
2. Edita `parameters/config.json` o el codigo. El entrenamiento y las etapas leen del **disco**.
3. `dvc repro` (rehace solo lo que cambio) → revisa `reportes/` y `docs/diccionario/`.
4. Anota/ajusta la decision en `docs/decisiones/`.
5. `dvc push` (datos al remoto) y envia a GitHub con **GITHUB_LOADER2** (hace `dvc push` y luego `git push`) con rama nueva, issue `N` y «Abrir PR» (commit `Refs #N`, PR `Closes #N`). Si es una version del conjunto, etiqueta `datos-vN`.
6. Otra persona revisa y hace merge.

Respaldo SQL: Sistema → «Datos en disco · respaldo en SQL Server». Con *al cortar* y *al entrenar* activos, SQL se actualiza solo; «Respaldar ahora» lo fuerza. Descomposicion/Ranking aun leen SQL, por eso conviene dejarlos activos.

## 2. Preparar DVC (una vez por equipo)
El repo ya trae `.dvc/config` con el remoto `almacen` (Google Drive, decision 0010) y `gdrive_use_service_account = true`. **Falta lo que solo tu PC puede hacer:**
```
scripts\iniciar_dvc.bat        # instala dvc, dvc add de lo pesado (crea input/*.dvc) y dvc repro (crea dvc.lock)
dvc remote modify --local almacen gdrive_service_account_json_file_path C:\ruta\clave.json   # la clave va SOLO aqui (config.local, no se versiona)
dvc push                       # 1o el contenido ...
git add .dvc dvc.yaml dvc.lock parameters input/*.dvc input/.gitignore output/reportes docs/diccionario
git commit -m "datos: registrar el conjunto crudo y la corrida de la etapa 3" ; git push   # 2o el historial
```
La carpeta de Drive debe ser una **unidad compartida** donde la cuenta de servicio sea Editor (si es una carpeta personal, `dvc push` falla con «cuota agotada»).
Si `pip install dvc` falla compilando `antlr4`: `pip install "setuptools<70" wheel` primero (ya lo hace el .bat).
`dvc.lock` y `input/*.dvc` **se commitean**: sin ellos no hay forma de saber que datos produjeron que tabla (criterios 1 y 2).

## 3. GitHub (una vez)
- En GITHUB_LOADER2 (⚙): usuario, **token** (fine-grained: Contents RW, Pull requests RW, Issues RW y Administration *read* para ver la proteccion), URL del repo y carpeta. El token queda solo en `CLAUDE\KEYS\github_loader.json`, fuera del proyecto; no lo pegues en chats ni commits.
- Settings → Branches → regla sobre `main`: *Require a pull request* (1 aprobacion), *Require status checks* (`calidad`), sin pushes directos. Verifica con el boton «Ver proteccion».
- Variable de repo `DVC_ACTIVO=true` (+ secret del remoto) cuando el remoto sea accesible desde el CI: activa clonar → `dvc pull` → `dvc repro --force` → `dvc.lock` sin cambios.
- Issues sugeridos: umbrales de limpieza (0005) · clase fuera (0006) · agrupar por persona (0002) · remoto DVC (0010) · mover Descomposicion/Ranking a disco · `exportar_slurm` a disco. Reemplaza los `#pendiente` de `docs/decisiones/` por su numero.

### Varios integrantes
- **Un token por persona**, guardado en su propio equipo (`KEYS\github_loader.json`, fuera del proyecto). No se comparte ni se manda: si alguien lo pierde se revoca el suyo sin afectar a los demas. Nombre y correo tambien son de cada uno (firman sus commits).
- El dueño agrega a cada persona en GitHub → Settings → Collaborators (permiso **Write**). «👤 ¿Quien soy?» confirma que el token sirve y puede enviar.
- Cada quien trabaja en su rama (`ana/umbrales`): elige la rama en el selector, marca el **modulo/area** a enviar, «⬇ Traer cambios» antes de enviar, y abre un Pull Request; otra persona lo revisa y hace el merge a `main` (protegida).
- Para continuar la rama de un compañero basta elegirla en el selector.

## 3b. Llaves y versiones
- **Llaves**: viven en `D:\05 PROYECTOS\CLAUDE\KEYS\` (fuera de este proyecto, para que GITHUB_LOADER2 sirva a cualquier carpeta): `github_loader.json` (usuarios, tokens, repo; clave `gdrive_key` = ruta del JSON de la cuenta de servicio de Drive). Este repo no trae codigo ni plantillas de llaves.
- **Publicar en el orden correcto**: GITHUB_LOADER2 hace `dvc push` (si el proyecto tiene `.dvc/` y hay `gdrive_key`) y despues `git push`; si el `dvc push` falla, no envia el historial. Anota cada bloque subido en `bloques/<proyecto>.estado.json`.
- **CI**: los *secrets* de GitHub (`GDRIVE_CREDENTIALS_DATA`) son el equivalente del `.env`; nunca se escribe una llave en el repo. Si una llegara a un commit, borrarla despues no basta: hay que **revocarla**.
- **Versiones**: un solo `requirements.txt` con versiones exactas (Python 3.11); lo usan `UPDATE.bat`, GitHub Actions y el panel. Para subir una version: cambiala ahi, corre `pytest` y abre un PR.

## 4. Verificacion por criterio
| Criterio | Comando / evidencia |
|---|---|
| 1 Reproducibilidad | `dvc repro --force && git diff --exit-code dvc.lock` (lo hace el CI) |
| 2 Separacion datos/codigo | `git ls-files input` solo lista `.dvc`; el crudo no es `outs` de ninguna etapa |
| 3 Cobertura de decisiones | `pytest tests/test_trazabilidad.py` + `docs/decisiones/README.md` |
| 4 Parametrizacion | ningun umbral en `src/`: `grep -rn "params(" src/` y `parameters/config.json` |
| 5 Diccionario | `docs/diccionario/<ej>.md` (falla la etapa si no coincide el numero de columnas) |
| 6 Informe de limpieza | `reportes/limpieza_<ej>.md` + `dvc metrics show` |
| 7 Traza de colaboracion | historial de PR con `Closes #N`, rama protegida, etiquetas `datos-vN` |

## 5. Lo que falta de tu lado (no lo puedo hacer yo)
1. Elegir y crear el **remoto DVC** (0010) y correr `dvc push`.
2. Crear el **token** y activar la **proteccion de rama**; abrir los issues.
3. ~~Congelar el entorno~~ hecho: `requirements.txt` con versiones exactas.
4. Enlazar el **informe de calidad de la etapa 2** desde `docs/decisiones/0005` (justifica los umbrales con datos reales).
5. Confirmar si el prefijo numerico del nombre del video es el **ID de la persona** (si si, el grupo de validacion pasa a persona).
6. Commitear `dvc.lock` tras el primer `dvc repro`.
