# 0010 · Remoto de datos de DVC

- **Estado:** **pendiente de elegir** · **Etapa:** transversal · **Issue:** #pendiente
- **Contexto:** los clips y grabaciones pesan demasiado para Git; DVC guarda punteros `.dvc` en Git y los datos en un remoto.
- **Opciones:** carpeta/unidad de red (simple, sin cuentas) · Google Drive (gratis, requiere autenticar) · S3/Azure (pago, para equipos).
- **Recomendacion:** carpeta de red o disco externo mientras sea un equipo pequeno; cambiar luego es `dvc remote modify`.
- **Al decidir:** reemplazar este estado por «aceptada», anotar el remoto y ejecutar `dvc push`.
