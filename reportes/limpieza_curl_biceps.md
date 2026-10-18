# Informe de limpieza: curl_biceps

2026-10-17T22:01:47 · umbrales de `params.yaml`: min_frames=10, max_nan_pct=20

- Clips en el manifest: **4** (base: 1, bien: 3)
- No entran al entrenamiento (base / desmarcados / sin .npz): **1**
- Muestras usadas en la ultima corrida (`run_-`): **-**

## Motivos

- clase base: 1

## Clips marcados

| clip | clase | cuadros | % NaN | motivos |
|---|---|---|---|---|
| curl_biceps/base/160547_curl_biceps_s02_base.mp4 | base | 176 | 0.0 | clase base (referencia, no se entrena) |
