# Informe de limpieza: sentadilla

2026-10-17T22:01:48 · umbrales de `params.yaml`: min_frames=10, max_nan_pct=20

- Clips en el manifest: **84** (base: 1, bien: 17, mal: 66)
- No entran al entrenamiento (base / desmarcados / sin .npz): **1**
- Muestras usadas en la ultima corrida (`run_-`): **-**

## Motivos

- clase base: 1

## Clips marcados

| clip | clase | cuadros | % NaN | motivos |
|---|---|---|---|---|
| sentadilla/base/160513_sentadilla_s08_base.mp4 | base | 182 | 0.0 | clase base (referencia, no se entrena) |
