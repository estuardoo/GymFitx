# `src/interfaz/tunel.py`

```text
Publicar el panel en internet con un tunel de Cloudflare (boton del panel).

NO se activa solo: el panel arranca siempre local (127.0.0.1). Desde la
pestana Sistema -> "Publicar en internet" se prende/apaga el tunel.

- Tunel: Cloudflare "quick tunnel" (gratis, sin cuenta). Da un enlace
  https://<algo>.trycloudflare.com que cambia cada vez que se prende.
  cloudflared se busca en el PATH o en herramientas/; si no esta se descarga
  solo a herramientas/ (Windows).
- Login (HTTP Basic): se exige SOLO a lo que llega por el tunel (Cloudflare
  agrega la cabecera cf-connecting-ip). Desde esta PC se entra sin clave.
  Credenciales en datos/acceso.json (solo el hash, nunca la clave en texto).
- Por el tunel NUNCA se permiten /api/system/* ni /api/publicar/* (apagar,
  reinstalar librerias, cambiar Python, apagar el tunel): solo desde la PC.
```

## Constantes

`ACCESO`, `CLOUDFLARED_URL`, `REALM`, `RUTAS_SOLO_LOCAL`

## `_archivo`

`def _archivo() -> Path`

_sin docstring_

## `_hash`

`def _hash(clave: str, sal: str) -> str`

_sin docstring_

## `fijar_clave`

`def fijar_clave(clave: str, usuario: str='gymfitx') -> None`

_sin docstring_

## `nueva_clave`

`def nueva_clave(usuario: str | None=None) -> dict`

```text
Genera una clave aleatoria, la guarda (hash) y la devuelve UNA vez.
```

## `credenciales`

`def credenciales() -> dict | None`

_sin docstring_

## `credencial_valida`

`def credencial_valida(cabecera: str) -> bool`

_sin docstring_

## `viene_del_tunel`

`def viene_del_tunel(headers: dict[str, str], cliente: str | None) -> bool`

_sin docstring_

## class `ProteccionTunel`

```text
Pide usuario/clave a lo que llega por el tunel y bloquea las rutas de
sistema desde afuera. Lo local pasa sin tocar.
```

### `ProteccionTunel.__init__`

`def __init__(self, app) -> None`

_sin docstring_

### `ProteccionTunel.__call__`

`async def __call__(self, scope, receive, send)`

_sin docstring_

## `_responder`

`async def _responder(scope, send, codigo: int, texto: str, extra=())`

_sin docstring_

## `cloudflared`

`def cloudflared() -> str`

_sin docstring_

## `estado`

`def estado() -> dict`

_sin docstring_

## `iniciar`

`def iniciar(puerto: int, con_clave: bool=True, log=None) -> dict`

```text
Prende el tunel en segundo plano. La URL aparece en estado() apenas
Cloudflare la asigna (unos segundos). Si se pide clave y todavia no hay
credenciales, se crean y se devuelven UNA vez en 'nueva_clave'.
```

## `detener`

`def detener() -> dict`

_sin docstring_

