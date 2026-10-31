# Informe de limpieza: cuerpo_completo

Umbrales de `params.yaml` (limpieza): min_frames=10, max_nan_pct=20, aplicar=True.

- Clips seleccionados para limpiar: **105** de 107 en el manifest
- Salen por la limpieza: **2**
- Quedan para construir: **103** (bien: 50, mal: 53)
- Copias `_N` entre los que quedan (riesgo de fuga si se partiera por clip; se agrupan por grabacion): **0**

## Motivos

- muy corto: 2

## Clips marcados

| clip | clase | cuadros | % NaN | motivos |
|---|---|---|---|---|
| cuerpo_completo/mal/cuerpo_completo__2026-08-25__205453_base_s03_mal_r0.mp4 | mal | 6 | 0.0 | muy corto (<10 cuadros) |
| cuerpo_completo/mal/cuerpo_completo__2026-08-25__231151_base_s03_mal_r0.mp4 | mal | 9 | 0.0 | muy corto (<10 cuadros) |
