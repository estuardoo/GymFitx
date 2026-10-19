# 0010 · Remoto de datos de DVC

- **Estado:** aceptada · **Etapa:** transversal · **Issue:** #11
- **Contexto:** los clips y grabaciones pesan demasiado para Git; DVC guarda punteros `.dvc` en Git y los datos en un remoto.
- **Opciones:** carpeta/unidad de red (simple, sin cuentas) · Google Drive (gratis, requiere autenticar) · S3/Azure (pago, para equipos).
- **Decision:** Google Drive. Carpeta de datos: `gdrive://18962pKBkjQCjkrObexJy9XNaVhUbxXrr` (ID de carpeta; no da acceso por si solo, la carpeta debe ser privada y compartida solo con el equipo).
- **Autenticacion:** cuenta de servicio (no la cuenta personal de usuario) con la carpeta compartida como Editor. Sus credenciales van en `.dvc/config.local` (no se versiona), nunca en el repo.
- **Riesgo conocido:** si se usa OAuth con la cuenta personal en modo de prueba, la autorizacion caduca a los 7 dias. Por eso se usa cuenta de servicio.
- **Al cambiar:** `dvc remote modify` sobre el remoto `almacen` y `dvc push` antes de cerrar el cambio.
