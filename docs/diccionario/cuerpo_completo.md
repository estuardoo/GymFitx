# Diccionario de datos: cuerpo_completo

2370 columnas = las de `datos/final/cuerpo_completo/X.npy` (contrastado al generarlo) · componentes `xyzap` · 30 cuadros por ciclo.

Lo genera `python -m src.preparacion.etapas formatear cuerpo_completo` (etapa 3.5). El CSV trae ademas `cuadro` y `descripcion`.

| columna | tipo | unidad | rango | origen | transformacion |
|---|---|---|---|---|---|
| f01_NOSE_x | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_NOSE_y | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_NOSE_z | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_LEFT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_LEFT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_LEFT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_RIGHT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_RIGHT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_RIGHT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_LEFT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_LEFT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_LEFT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_RIGHT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_RIGHT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_RIGHT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_LEFT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_LEFT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_LEFT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_RIGHT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_RIGHT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_RIGHT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_LEFT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_LEFT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_LEFT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_RIGHT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_RIGHT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_RIGHT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_LEFT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_LEFT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_LEFT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_RIGHT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_RIGHT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_RIGHT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_LEFT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_LEFT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_LEFT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_RIGHT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_RIGHT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_RIGHT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_LEFT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_LEFT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_LEFT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_RIGHT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_RIGHT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_RIGHT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_LEFT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_LEFT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_LEFT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_RIGHT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_RIGHT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_RIGHT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_LEFT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_LEFT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_LEFT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_RIGHT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_RIGHT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_RIGHT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_LEFT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_LEFT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_LEFT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_RIGHT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_RIGHT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_RIGHT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_LEFT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_LEFT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_LEFT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_RIGHT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_RIGHT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_RIGHT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f01_codo_izq | angle | grados | 0..1 | C12>C14>C16 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f01_cadera_izq | angle | grados | 0..1 | C12>C24>C26 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f01_codo_der | angle | grados | 0..1 | C13>C15>C17 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f01_cadera_der | angle | grados | 0..1 | C13>C25>C27 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f01_hombro_izq | angle | grados | 0..1 | C24>C12>C14 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f01_rodilla_izq | angle | grados | 0..1 | C24>C26>C28 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f01_hombro_der | angle | grados | 0..1 | C25>C13>C15 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f01_rodilla_der | angle | grados | 0..1 | C25>C27>C29 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f01_tobillo_izq | angle | grados | 0..1 | C26>C28>C32 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f01_tobillo_der | angle | grados | 0..1 | C27>C29>C33 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f02_NOSE_x | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_NOSE_y | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_NOSE_z | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_LEFT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_LEFT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_LEFT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_RIGHT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_RIGHT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_RIGHT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_LEFT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_LEFT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_LEFT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_RIGHT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_RIGHT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_RIGHT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_LEFT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_LEFT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_LEFT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_RIGHT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_RIGHT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_RIGHT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_LEFT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_LEFT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_LEFT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_RIGHT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_RIGHT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_RIGHT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_LEFT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_LEFT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_LEFT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_RIGHT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_RIGHT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_RIGHT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_LEFT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_LEFT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_LEFT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_RIGHT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_RIGHT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_RIGHT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_LEFT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_LEFT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_LEFT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_RIGHT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_RIGHT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_RIGHT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_LEFT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_LEFT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_LEFT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_RIGHT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_RIGHT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_RIGHT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_LEFT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_LEFT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_LEFT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_RIGHT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_RIGHT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_RIGHT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_LEFT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_LEFT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_LEFT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_RIGHT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_RIGHT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_RIGHT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_LEFT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_LEFT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_LEFT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_RIGHT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_RIGHT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_RIGHT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f02_codo_izq | angle | grados | 0..1 | C12>C14>C16 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f02_cadera_izq | angle | grados | 0..1 | C12>C24>C26 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f02_codo_der | angle | grados | 0..1 | C13>C15>C17 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f02_cadera_der | angle | grados | 0..1 | C13>C25>C27 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f02_hombro_izq | angle | grados | 0..1 | C24>C12>C14 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f02_rodilla_izq | angle | grados | 0..1 | C24>C26>C28 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f02_hombro_der | angle | grados | 0..1 | C25>C13>C15 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f02_rodilla_der | angle | grados | 0..1 | C25>C27>C29 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f02_tobillo_izq | angle | grados | 0..1 | C26>C28>C32 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f02_tobillo_der | angle | grados | 0..1 | C27>C29>C33 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f03_NOSE_x | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_NOSE_y | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_NOSE_z | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_LEFT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_LEFT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_LEFT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_RIGHT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_RIGHT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_RIGHT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_LEFT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_LEFT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_LEFT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_RIGHT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_RIGHT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_RIGHT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_LEFT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_LEFT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_LEFT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_RIGHT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_RIGHT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_RIGHT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_LEFT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_LEFT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_LEFT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_RIGHT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_RIGHT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_RIGHT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_LEFT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_LEFT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_LEFT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_RIGHT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_RIGHT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_RIGHT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_LEFT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_LEFT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_LEFT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_RIGHT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_RIGHT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_RIGHT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_LEFT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_LEFT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_LEFT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_RIGHT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_RIGHT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_RIGHT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_LEFT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_LEFT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_LEFT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_RIGHT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_RIGHT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_RIGHT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_LEFT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_LEFT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_LEFT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_RIGHT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_RIGHT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_RIGHT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_LEFT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_LEFT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_LEFT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_RIGHT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_RIGHT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_RIGHT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_LEFT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_LEFT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_LEFT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_RIGHT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_RIGHT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_RIGHT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f03_codo_izq | angle | grados | 0..1 | C12>C14>C16 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f03_cadera_izq | angle | grados | 0..1 | C12>C24>C26 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f03_codo_der | angle | grados | 0..1 | C13>C15>C17 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f03_cadera_der | angle | grados | 0..1 | C13>C25>C27 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f03_hombro_izq | angle | grados | 0..1 | C24>C12>C14 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f03_rodilla_izq | angle | grados | 0..1 | C24>C26>C28 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f03_hombro_der | angle | grados | 0..1 | C25>C13>C15 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f03_rodilla_der | angle | grados | 0..1 | C25>C27>C29 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f03_tobillo_izq | angle | grados | 0..1 | C26>C28>C32 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f03_tobillo_der | angle | grados | 0..1 | C27>C29>C33 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f04_NOSE_x | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_NOSE_y | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_NOSE_z | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_LEFT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_LEFT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_LEFT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_RIGHT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_RIGHT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_RIGHT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_LEFT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_LEFT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_LEFT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_RIGHT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_RIGHT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_RIGHT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_LEFT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_LEFT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_LEFT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_RIGHT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_RIGHT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_RIGHT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_LEFT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_LEFT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_LEFT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_RIGHT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_RIGHT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_RIGHT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_LEFT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_LEFT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_LEFT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_RIGHT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_RIGHT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_RIGHT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_LEFT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_LEFT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_LEFT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_RIGHT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_RIGHT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_RIGHT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_LEFT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_LEFT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_LEFT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_RIGHT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_RIGHT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_RIGHT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_LEFT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_LEFT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_LEFT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_RIGHT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_RIGHT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_RIGHT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_LEFT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_LEFT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_LEFT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_RIGHT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_RIGHT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_RIGHT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_LEFT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_LEFT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_LEFT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_RIGHT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_RIGHT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_RIGHT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_LEFT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_LEFT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_LEFT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_RIGHT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_RIGHT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_RIGHT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f04_codo_izq | angle | grados | 0..1 | C12>C14>C16 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f04_cadera_izq | angle | grados | 0..1 | C12>C24>C26 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f04_codo_der | angle | grados | 0..1 | C13>C15>C17 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f04_cadera_der | angle | grados | 0..1 | C13>C25>C27 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f04_hombro_izq | angle | grados | 0..1 | C24>C12>C14 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f04_rodilla_izq | angle | grados | 0..1 | C24>C26>C28 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f04_hombro_der | angle | grados | 0..1 | C25>C13>C15 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f04_rodilla_der | angle | grados | 0..1 | C25>C27>C29 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f04_tobillo_izq | angle | grados | 0..1 | C26>C28>C32 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f04_tobillo_der | angle | grados | 0..1 | C27>C29>C33 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f05_NOSE_x | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_NOSE_y | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_NOSE_z | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_LEFT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_LEFT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_LEFT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_RIGHT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_RIGHT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_RIGHT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_LEFT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_LEFT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_LEFT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_RIGHT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_RIGHT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_RIGHT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_LEFT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_LEFT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_LEFT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_RIGHT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_RIGHT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_RIGHT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_LEFT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_LEFT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_LEFT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_RIGHT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_RIGHT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_RIGHT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_LEFT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_LEFT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_LEFT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_RIGHT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_RIGHT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_RIGHT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_LEFT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_LEFT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_LEFT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_RIGHT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_RIGHT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_RIGHT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_LEFT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_LEFT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_LEFT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_RIGHT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_RIGHT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_RIGHT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_LEFT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_LEFT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_LEFT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_RIGHT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_RIGHT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_RIGHT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_LEFT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_LEFT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_LEFT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_RIGHT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_RIGHT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_RIGHT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_LEFT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_LEFT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_LEFT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_RIGHT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_RIGHT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_RIGHT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_LEFT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_LEFT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_LEFT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_RIGHT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_RIGHT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_RIGHT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f05_codo_izq | angle | grados | 0..1 | C12>C14>C16 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f05_cadera_izq | angle | grados | 0..1 | C12>C24>C26 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f05_codo_der | angle | grados | 0..1 | C13>C15>C17 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f05_cadera_der | angle | grados | 0..1 | C13>C25>C27 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f05_hombro_izq | angle | grados | 0..1 | C24>C12>C14 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f05_rodilla_izq | angle | grados | 0..1 | C24>C26>C28 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f05_hombro_der | angle | grados | 0..1 | C25>C13>C15 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f05_rodilla_der | angle | grados | 0..1 | C25>C27>C29 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f05_tobillo_izq | angle | grados | 0..1 | C26>C28>C32 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f05_tobillo_der | angle | grados | 0..1 | C27>C29>C33 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f06_NOSE_x | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_NOSE_y | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_NOSE_z | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_LEFT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_LEFT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_LEFT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_RIGHT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_RIGHT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_RIGHT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_LEFT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_LEFT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_LEFT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_RIGHT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_RIGHT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_RIGHT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_LEFT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_LEFT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_LEFT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_RIGHT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_RIGHT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_RIGHT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_LEFT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_LEFT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_LEFT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_RIGHT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_RIGHT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_RIGHT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_LEFT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_LEFT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_LEFT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_RIGHT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_RIGHT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_RIGHT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_LEFT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_LEFT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_LEFT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_RIGHT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_RIGHT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_RIGHT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_LEFT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_LEFT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_LEFT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_RIGHT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_RIGHT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_RIGHT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_LEFT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_LEFT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_LEFT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_RIGHT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_RIGHT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_RIGHT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_LEFT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_LEFT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_LEFT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_RIGHT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_RIGHT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_RIGHT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_LEFT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_LEFT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_LEFT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_RIGHT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_RIGHT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_RIGHT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_LEFT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_LEFT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_LEFT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_RIGHT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_RIGHT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_RIGHT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f06_codo_izq | angle | grados | 0..1 | C12>C14>C16 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f06_cadera_izq | angle | grados | 0..1 | C12>C24>C26 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f06_codo_der | angle | grados | 0..1 | C13>C15>C17 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f06_cadera_der | angle | grados | 0..1 | C13>C25>C27 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f06_hombro_izq | angle | grados | 0..1 | C24>C12>C14 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f06_rodilla_izq | angle | grados | 0..1 | C24>C26>C28 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f06_hombro_der | angle | grados | 0..1 | C25>C13>C15 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f06_rodilla_der | angle | grados | 0..1 | C25>C27>C29 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f06_tobillo_izq | angle | grados | 0..1 | C26>C28>C32 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f06_tobillo_der | angle | grados | 0..1 | C27>C29>C33 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f07_NOSE_x | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_NOSE_y | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_NOSE_z | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_LEFT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_LEFT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_LEFT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_RIGHT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_RIGHT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_RIGHT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_LEFT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_LEFT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_LEFT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_RIGHT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_RIGHT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_RIGHT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_LEFT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_LEFT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_LEFT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_RIGHT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_RIGHT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_RIGHT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_LEFT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_LEFT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_LEFT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_RIGHT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_RIGHT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_RIGHT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_LEFT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_LEFT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_LEFT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_RIGHT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_RIGHT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_RIGHT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_LEFT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_LEFT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_LEFT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_RIGHT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_RIGHT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_RIGHT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_LEFT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_LEFT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_LEFT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_RIGHT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_RIGHT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_RIGHT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_LEFT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_LEFT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_LEFT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_RIGHT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_RIGHT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_RIGHT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_LEFT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_LEFT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_LEFT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_RIGHT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_RIGHT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_RIGHT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_LEFT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_LEFT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_LEFT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_RIGHT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_RIGHT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_RIGHT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_LEFT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_LEFT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_LEFT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_RIGHT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_RIGHT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_RIGHT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f07_codo_izq | angle | grados | 0..1 | C12>C14>C16 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f07_cadera_izq | angle | grados | 0..1 | C12>C24>C26 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f07_codo_der | angle | grados | 0..1 | C13>C15>C17 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f07_cadera_der | angle | grados | 0..1 | C13>C25>C27 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f07_hombro_izq | angle | grados | 0..1 | C24>C12>C14 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f07_rodilla_izq | angle | grados | 0..1 | C24>C26>C28 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f07_hombro_der | angle | grados | 0..1 | C25>C13>C15 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f07_rodilla_der | angle | grados | 0..1 | C25>C27>C29 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f07_tobillo_izq | angle | grados | 0..1 | C26>C28>C32 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f07_tobillo_der | angle | grados | 0..1 | C27>C29>C33 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f08_NOSE_x | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_NOSE_y | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_NOSE_z | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_LEFT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_LEFT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_LEFT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_RIGHT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_RIGHT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_RIGHT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_LEFT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_LEFT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_LEFT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_RIGHT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_RIGHT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_RIGHT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_LEFT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_LEFT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_LEFT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_RIGHT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_RIGHT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_RIGHT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_LEFT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_LEFT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_LEFT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_RIGHT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_RIGHT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_RIGHT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_LEFT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_LEFT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_LEFT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_RIGHT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_RIGHT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_RIGHT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_LEFT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_LEFT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_LEFT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_RIGHT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_RIGHT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_RIGHT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_LEFT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_LEFT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_LEFT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_RIGHT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_RIGHT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_RIGHT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_LEFT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_LEFT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_LEFT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_RIGHT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_RIGHT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_RIGHT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_LEFT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_LEFT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_LEFT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_RIGHT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_RIGHT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_RIGHT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_LEFT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_LEFT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_LEFT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_RIGHT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_RIGHT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_RIGHT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_LEFT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_LEFT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_LEFT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_RIGHT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_RIGHT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_RIGHT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f08_codo_izq | angle | grados | 0..1 | C12>C14>C16 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f08_cadera_izq | angle | grados | 0..1 | C12>C24>C26 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f08_codo_der | angle | grados | 0..1 | C13>C15>C17 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f08_cadera_der | angle | grados | 0..1 | C13>C25>C27 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f08_hombro_izq | angle | grados | 0..1 | C24>C12>C14 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f08_rodilla_izq | angle | grados | 0..1 | C24>C26>C28 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f08_hombro_der | angle | grados | 0..1 | C25>C13>C15 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f08_rodilla_der | angle | grados | 0..1 | C25>C27>C29 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f08_tobillo_izq | angle | grados | 0..1 | C26>C28>C32 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f08_tobillo_der | angle | grados | 0..1 | C27>C29>C33 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f09_NOSE_x | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_NOSE_y | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_NOSE_z | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_LEFT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_LEFT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_LEFT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_RIGHT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_RIGHT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_RIGHT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_LEFT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_LEFT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_LEFT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_RIGHT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_RIGHT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_RIGHT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_LEFT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_LEFT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_LEFT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_RIGHT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_RIGHT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_RIGHT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_LEFT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_LEFT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_LEFT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_RIGHT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_RIGHT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_RIGHT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_LEFT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_LEFT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_LEFT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_RIGHT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_RIGHT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_RIGHT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_LEFT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_LEFT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_LEFT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_RIGHT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_RIGHT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_RIGHT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_LEFT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_LEFT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_LEFT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_RIGHT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_RIGHT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_RIGHT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_LEFT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_LEFT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_LEFT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_RIGHT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_RIGHT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_RIGHT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_LEFT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_LEFT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_LEFT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_RIGHT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_RIGHT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_RIGHT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_LEFT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_LEFT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_LEFT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_RIGHT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_RIGHT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_RIGHT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_LEFT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_LEFT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_LEFT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_RIGHT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_RIGHT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_RIGHT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f09_codo_izq | angle | grados | 0..1 | C12>C14>C16 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f09_cadera_izq | angle | grados | 0..1 | C12>C24>C26 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f09_codo_der | angle | grados | 0..1 | C13>C15>C17 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f09_cadera_der | angle | grados | 0..1 | C13>C25>C27 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f09_hombro_izq | angle | grados | 0..1 | C24>C12>C14 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f09_rodilla_izq | angle | grados | 0..1 | C24>C26>C28 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f09_hombro_der | angle | grados | 0..1 | C25>C13>C15 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f09_rodilla_der | angle | grados | 0..1 | C25>C27>C29 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f09_tobillo_izq | angle | grados | 0..1 | C26>C28>C32 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f09_tobillo_der | angle | grados | 0..1 | C27>C29>C33 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f10_NOSE_x | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_NOSE_y | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_NOSE_z | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_LEFT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_LEFT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_LEFT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_RIGHT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_RIGHT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_RIGHT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_LEFT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_LEFT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_LEFT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_RIGHT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_RIGHT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_RIGHT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_LEFT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_LEFT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_LEFT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_RIGHT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_RIGHT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_RIGHT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_LEFT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_LEFT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_LEFT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_RIGHT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_RIGHT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_RIGHT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_LEFT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_LEFT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_LEFT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_RIGHT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_RIGHT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_RIGHT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_LEFT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_LEFT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_LEFT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_RIGHT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_RIGHT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_RIGHT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_LEFT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_LEFT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_LEFT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_RIGHT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_RIGHT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_RIGHT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_LEFT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_LEFT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_LEFT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_RIGHT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_RIGHT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_RIGHT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_LEFT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_LEFT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_LEFT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_RIGHT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_RIGHT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_RIGHT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_LEFT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_LEFT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_LEFT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_RIGHT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_RIGHT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_RIGHT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_LEFT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_LEFT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_LEFT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_RIGHT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_RIGHT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_RIGHT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f10_codo_izq | angle | grados | 0..1 | C12>C14>C16 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f10_cadera_izq | angle | grados | 0..1 | C12>C24>C26 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f10_codo_der | angle | grados | 0..1 | C13>C15>C17 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f10_cadera_der | angle | grados | 0..1 | C13>C25>C27 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f10_hombro_izq | angle | grados | 0..1 | C24>C12>C14 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f10_rodilla_izq | angle | grados | 0..1 | C24>C26>C28 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f10_hombro_der | angle | grados | 0..1 | C25>C13>C15 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f10_rodilla_der | angle | grados | 0..1 | C25>C27>C29 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f10_tobillo_izq | angle | grados | 0..1 | C26>C28>C32 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f10_tobillo_der | angle | grados | 0..1 | C27>C29>C33 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f11_NOSE_x | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_NOSE_y | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_NOSE_z | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_LEFT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_LEFT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_LEFT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_RIGHT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_RIGHT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_RIGHT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_LEFT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_LEFT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_LEFT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_RIGHT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_RIGHT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_RIGHT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_LEFT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_LEFT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_LEFT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_RIGHT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_RIGHT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_RIGHT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_LEFT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_LEFT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_LEFT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_RIGHT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_RIGHT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_RIGHT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_LEFT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_LEFT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_LEFT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_RIGHT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_RIGHT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_RIGHT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_LEFT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_LEFT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_LEFT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_RIGHT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_RIGHT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_RIGHT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_LEFT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_LEFT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_LEFT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_RIGHT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_RIGHT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_RIGHT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_LEFT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_LEFT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_LEFT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_RIGHT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_RIGHT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_RIGHT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_LEFT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_LEFT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_LEFT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_RIGHT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_RIGHT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_RIGHT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_LEFT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_LEFT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_LEFT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_RIGHT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_RIGHT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_RIGHT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_LEFT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_LEFT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_LEFT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_RIGHT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_RIGHT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_RIGHT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f11_codo_izq | angle | grados | 0..1 | C12>C14>C16 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f11_cadera_izq | angle | grados | 0..1 | C12>C24>C26 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f11_codo_der | angle | grados | 0..1 | C13>C15>C17 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f11_cadera_der | angle | grados | 0..1 | C13>C25>C27 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f11_hombro_izq | angle | grados | 0..1 | C24>C12>C14 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f11_rodilla_izq | angle | grados | 0..1 | C24>C26>C28 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f11_hombro_der | angle | grados | 0..1 | C25>C13>C15 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f11_rodilla_der | angle | grados | 0..1 | C25>C27>C29 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f11_tobillo_izq | angle | grados | 0..1 | C26>C28>C32 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f11_tobillo_der | angle | grados | 0..1 | C27>C29>C33 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f12_NOSE_x | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_NOSE_y | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_NOSE_z | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_LEFT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_LEFT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_LEFT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_RIGHT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_RIGHT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_RIGHT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_LEFT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_LEFT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_LEFT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_RIGHT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_RIGHT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_RIGHT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_LEFT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_LEFT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_LEFT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_RIGHT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_RIGHT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_RIGHT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_LEFT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_LEFT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_LEFT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_RIGHT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_RIGHT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_RIGHT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_LEFT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_LEFT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_LEFT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_RIGHT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_RIGHT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_RIGHT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_LEFT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_LEFT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_LEFT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_RIGHT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_RIGHT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_RIGHT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_LEFT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_LEFT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_LEFT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_RIGHT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_RIGHT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_RIGHT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_LEFT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_LEFT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_LEFT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_RIGHT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_RIGHT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_RIGHT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_LEFT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_LEFT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_LEFT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_RIGHT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_RIGHT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_RIGHT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_LEFT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_LEFT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_LEFT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_RIGHT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_RIGHT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_RIGHT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_LEFT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_LEFT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_LEFT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_RIGHT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_RIGHT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_RIGHT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f12_codo_izq | angle | grados | 0..1 | C12>C14>C16 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f12_cadera_izq | angle | grados | 0..1 | C12>C24>C26 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f12_codo_der | angle | grados | 0..1 | C13>C15>C17 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f12_cadera_der | angle | grados | 0..1 | C13>C25>C27 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f12_hombro_izq | angle | grados | 0..1 | C24>C12>C14 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f12_rodilla_izq | angle | grados | 0..1 | C24>C26>C28 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f12_hombro_der | angle | grados | 0..1 | C25>C13>C15 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f12_rodilla_der | angle | grados | 0..1 | C25>C27>C29 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f12_tobillo_izq | angle | grados | 0..1 | C26>C28>C32 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f12_tobillo_der | angle | grados | 0..1 | C27>C29>C33 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f13_NOSE_x | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_NOSE_y | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_NOSE_z | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_LEFT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_LEFT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_LEFT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_RIGHT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_RIGHT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_RIGHT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_LEFT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_LEFT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_LEFT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_RIGHT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_RIGHT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_RIGHT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_LEFT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_LEFT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_LEFT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_RIGHT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_RIGHT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_RIGHT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_LEFT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_LEFT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_LEFT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_RIGHT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_RIGHT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_RIGHT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_LEFT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_LEFT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_LEFT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_RIGHT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_RIGHT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_RIGHT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_LEFT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_LEFT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_LEFT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_RIGHT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_RIGHT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_RIGHT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_LEFT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_LEFT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_LEFT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_RIGHT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_RIGHT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_RIGHT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_LEFT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_LEFT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_LEFT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_RIGHT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_RIGHT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_RIGHT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_LEFT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_LEFT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_LEFT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_RIGHT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_RIGHT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_RIGHT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_LEFT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_LEFT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_LEFT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_RIGHT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_RIGHT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_RIGHT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_LEFT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_LEFT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_LEFT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_RIGHT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_RIGHT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_RIGHT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f13_codo_izq | angle | grados | 0..1 | C12>C14>C16 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f13_cadera_izq | angle | grados | 0..1 | C12>C24>C26 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f13_codo_der | angle | grados | 0..1 | C13>C15>C17 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f13_cadera_der | angle | grados | 0..1 | C13>C25>C27 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f13_hombro_izq | angle | grados | 0..1 | C24>C12>C14 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f13_rodilla_izq | angle | grados | 0..1 | C24>C26>C28 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f13_hombro_der | angle | grados | 0..1 | C25>C13>C15 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f13_rodilla_der | angle | grados | 0..1 | C25>C27>C29 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f13_tobillo_izq | angle | grados | 0..1 | C26>C28>C32 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f13_tobillo_der | angle | grados | 0..1 | C27>C29>C33 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f14_NOSE_x | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_NOSE_y | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_NOSE_z | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_LEFT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_LEFT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_LEFT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_RIGHT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_RIGHT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_RIGHT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_LEFT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_LEFT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_LEFT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_RIGHT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_RIGHT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_RIGHT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_LEFT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_LEFT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_LEFT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_RIGHT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_RIGHT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_RIGHT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_LEFT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_LEFT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_LEFT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_RIGHT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_RIGHT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_RIGHT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_LEFT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_LEFT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_LEFT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_RIGHT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_RIGHT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_RIGHT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_LEFT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_LEFT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_LEFT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_RIGHT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_RIGHT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_RIGHT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_LEFT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_LEFT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_LEFT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_RIGHT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_RIGHT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_RIGHT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_LEFT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_LEFT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_LEFT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_RIGHT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_RIGHT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_RIGHT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_LEFT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_LEFT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_LEFT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_RIGHT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_RIGHT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_RIGHT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_LEFT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_LEFT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_LEFT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_RIGHT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_RIGHT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_RIGHT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_LEFT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_LEFT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_LEFT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_RIGHT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_RIGHT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_RIGHT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f14_codo_izq | angle | grados | 0..1 | C12>C14>C16 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f14_cadera_izq | angle | grados | 0..1 | C12>C24>C26 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f14_codo_der | angle | grados | 0..1 | C13>C15>C17 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f14_cadera_der | angle | grados | 0..1 | C13>C25>C27 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f14_hombro_izq | angle | grados | 0..1 | C24>C12>C14 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f14_rodilla_izq | angle | grados | 0..1 | C24>C26>C28 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f14_hombro_der | angle | grados | 0..1 | C25>C13>C15 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f14_rodilla_der | angle | grados | 0..1 | C25>C27>C29 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f14_tobillo_izq | angle | grados | 0..1 | C26>C28>C32 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f14_tobillo_der | angle | grados | 0..1 | C27>C29>C33 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f15_NOSE_x | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_NOSE_y | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_NOSE_z | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_LEFT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_LEFT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_LEFT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_RIGHT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_RIGHT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_RIGHT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_LEFT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_LEFT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_LEFT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_RIGHT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_RIGHT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_RIGHT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_LEFT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_LEFT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_LEFT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_RIGHT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_RIGHT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_RIGHT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_LEFT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_LEFT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_LEFT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_RIGHT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_RIGHT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_RIGHT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_LEFT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_LEFT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_LEFT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_RIGHT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_RIGHT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_RIGHT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_LEFT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_LEFT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_LEFT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_RIGHT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_RIGHT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_RIGHT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_LEFT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_LEFT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_LEFT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_RIGHT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_RIGHT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_RIGHT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_LEFT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_LEFT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_LEFT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_RIGHT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_RIGHT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_RIGHT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_LEFT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_LEFT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_LEFT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_RIGHT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_RIGHT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_RIGHT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_LEFT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_LEFT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_LEFT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_RIGHT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_RIGHT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_RIGHT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_LEFT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_LEFT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_LEFT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_RIGHT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_RIGHT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_RIGHT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f15_codo_izq | angle | grados | 0..1 | C12>C14>C16 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f15_cadera_izq | angle | grados | 0..1 | C12>C24>C26 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f15_codo_der | angle | grados | 0..1 | C13>C15>C17 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f15_cadera_der | angle | grados | 0..1 | C13>C25>C27 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f15_hombro_izq | angle | grados | 0..1 | C24>C12>C14 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f15_rodilla_izq | angle | grados | 0..1 | C24>C26>C28 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f15_hombro_der | angle | grados | 0..1 | C25>C13>C15 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f15_rodilla_der | angle | grados | 0..1 | C25>C27>C29 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f15_tobillo_izq | angle | grados | 0..1 | C26>C28>C32 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f15_tobillo_der | angle | grados | 0..1 | C27>C29>C33 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f16_NOSE_x | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_NOSE_y | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_NOSE_z | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_LEFT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_LEFT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_LEFT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_RIGHT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_RIGHT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_RIGHT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_LEFT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_LEFT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_LEFT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_RIGHT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_RIGHT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_RIGHT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_LEFT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_LEFT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_LEFT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_RIGHT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_RIGHT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_RIGHT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_LEFT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_LEFT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_LEFT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_RIGHT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_RIGHT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_RIGHT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_LEFT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_LEFT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_LEFT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_RIGHT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_RIGHT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_RIGHT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_LEFT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_LEFT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_LEFT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_RIGHT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_RIGHT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_RIGHT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_LEFT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_LEFT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_LEFT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_RIGHT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_RIGHT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_RIGHT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_LEFT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_LEFT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_LEFT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_RIGHT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_RIGHT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_RIGHT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_LEFT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_LEFT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_LEFT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_RIGHT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_RIGHT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_RIGHT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_LEFT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_LEFT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_LEFT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_RIGHT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_RIGHT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_RIGHT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_LEFT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_LEFT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_LEFT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_RIGHT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_RIGHT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_RIGHT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f16_codo_izq | angle | grados | 0..1 | C12>C14>C16 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f16_cadera_izq | angle | grados | 0..1 | C12>C24>C26 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f16_codo_der | angle | grados | 0..1 | C13>C15>C17 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f16_cadera_der | angle | grados | 0..1 | C13>C25>C27 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f16_hombro_izq | angle | grados | 0..1 | C24>C12>C14 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f16_rodilla_izq | angle | grados | 0..1 | C24>C26>C28 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f16_hombro_der | angle | grados | 0..1 | C25>C13>C15 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f16_rodilla_der | angle | grados | 0..1 | C25>C27>C29 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f16_tobillo_izq | angle | grados | 0..1 | C26>C28>C32 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f16_tobillo_der | angle | grados | 0..1 | C27>C29>C33 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f17_NOSE_x | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_NOSE_y | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_NOSE_z | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_LEFT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_LEFT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_LEFT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_RIGHT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_RIGHT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_RIGHT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_LEFT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_LEFT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_LEFT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_RIGHT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_RIGHT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_RIGHT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_LEFT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_LEFT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_LEFT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_RIGHT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_RIGHT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_RIGHT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_LEFT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_LEFT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_LEFT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_RIGHT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_RIGHT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_RIGHT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_LEFT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_LEFT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_LEFT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_RIGHT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_RIGHT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_RIGHT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_LEFT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_LEFT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_LEFT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_RIGHT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_RIGHT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_RIGHT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_LEFT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_LEFT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_LEFT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_RIGHT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_RIGHT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_RIGHT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_LEFT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_LEFT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_LEFT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_RIGHT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_RIGHT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_RIGHT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_LEFT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_LEFT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_LEFT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_RIGHT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_RIGHT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_RIGHT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_LEFT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_LEFT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_LEFT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_RIGHT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_RIGHT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_RIGHT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_LEFT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_LEFT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_LEFT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_RIGHT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_RIGHT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_RIGHT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f17_codo_izq | angle | grados | 0..1 | C12>C14>C16 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f17_cadera_izq | angle | grados | 0..1 | C12>C24>C26 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f17_codo_der | angle | grados | 0..1 | C13>C15>C17 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f17_cadera_der | angle | grados | 0..1 | C13>C25>C27 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f17_hombro_izq | angle | grados | 0..1 | C24>C12>C14 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f17_rodilla_izq | angle | grados | 0..1 | C24>C26>C28 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f17_hombro_der | angle | grados | 0..1 | C25>C13>C15 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f17_rodilla_der | angle | grados | 0..1 | C25>C27>C29 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f17_tobillo_izq | angle | grados | 0..1 | C26>C28>C32 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f17_tobillo_der | angle | grados | 0..1 | C27>C29>C33 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f18_NOSE_x | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_NOSE_y | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_NOSE_z | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_LEFT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_LEFT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_LEFT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_RIGHT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_RIGHT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_RIGHT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_LEFT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_LEFT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_LEFT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_RIGHT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_RIGHT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_RIGHT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_LEFT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_LEFT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_LEFT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_RIGHT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_RIGHT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_RIGHT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_LEFT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_LEFT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_LEFT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_RIGHT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_RIGHT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_RIGHT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_LEFT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_LEFT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_LEFT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_RIGHT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_RIGHT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_RIGHT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_LEFT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_LEFT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_LEFT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_RIGHT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_RIGHT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_RIGHT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_LEFT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_LEFT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_LEFT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_RIGHT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_RIGHT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_RIGHT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_LEFT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_LEFT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_LEFT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_RIGHT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_RIGHT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_RIGHT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_LEFT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_LEFT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_LEFT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_RIGHT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_RIGHT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_RIGHT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_LEFT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_LEFT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_LEFT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_RIGHT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_RIGHT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_RIGHT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_LEFT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_LEFT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_LEFT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_RIGHT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_RIGHT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_RIGHT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f18_codo_izq | angle | grados | 0..1 | C12>C14>C16 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f18_cadera_izq | angle | grados | 0..1 | C12>C24>C26 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f18_codo_der | angle | grados | 0..1 | C13>C15>C17 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f18_cadera_der | angle | grados | 0..1 | C13>C25>C27 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f18_hombro_izq | angle | grados | 0..1 | C24>C12>C14 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f18_rodilla_izq | angle | grados | 0..1 | C24>C26>C28 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f18_hombro_der | angle | grados | 0..1 | C25>C13>C15 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f18_rodilla_der | angle | grados | 0..1 | C25>C27>C29 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f18_tobillo_izq | angle | grados | 0..1 | C26>C28>C32 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f18_tobillo_der | angle | grados | 0..1 | C27>C29>C33 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f19_NOSE_x | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_NOSE_y | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_NOSE_z | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_LEFT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_LEFT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_LEFT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_RIGHT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_RIGHT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_RIGHT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_LEFT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_LEFT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_LEFT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_RIGHT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_RIGHT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_RIGHT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_LEFT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_LEFT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_LEFT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_RIGHT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_RIGHT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_RIGHT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_LEFT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_LEFT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_LEFT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_RIGHT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_RIGHT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_RIGHT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_LEFT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_LEFT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_LEFT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_RIGHT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_RIGHT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_RIGHT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_LEFT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_LEFT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_LEFT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_RIGHT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_RIGHT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_RIGHT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_LEFT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_LEFT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_LEFT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_RIGHT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_RIGHT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_RIGHT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_LEFT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_LEFT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_LEFT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_RIGHT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_RIGHT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_RIGHT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_LEFT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_LEFT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_LEFT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_RIGHT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_RIGHT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_RIGHT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_LEFT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_LEFT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_LEFT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_RIGHT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_RIGHT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_RIGHT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_LEFT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_LEFT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_LEFT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_RIGHT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_RIGHT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_RIGHT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f19_codo_izq | angle | grados | 0..1 | C12>C14>C16 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f19_cadera_izq | angle | grados | 0..1 | C12>C24>C26 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f19_codo_der | angle | grados | 0..1 | C13>C15>C17 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f19_cadera_der | angle | grados | 0..1 | C13>C25>C27 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f19_hombro_izq | angle | grados | 0..1 | C24>C12>C14 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f19_rodilla_izq | angle | grados | 0..1 | C24>C26>C28 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f19_hombro_der | angle | grados | 0..1 | C25>C13>C15 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f19_rodilla_der | angle | grados | 0..1 | C25>C27>C29 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f19_tobillo_izq | angle | grados | 0..1 | C26>C28>C32 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f19_tobillo_der | angle | grados | 0..1 | C27>C29>C33 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f20_NOSE_x | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_NOSE_y | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_NOSE_z | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_LEFT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_LEFT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_LEFT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_RIGHT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_RIGHT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_RIGHT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_LEFT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_LEFT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_LEFT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_RIGHT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_RIGHT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_RIGHT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_LEFT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_LEFT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_LEFT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_RIGHT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_RIGHT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_RIGHT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_LEFT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_LEFT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_LEFT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_RIGHT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_RIGHT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_RIGHT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_LEFT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_LEFT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_LEFT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_RIGHT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_RIGHT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_RIGHT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_LEFT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_LEFT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_LEFT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_RIGHT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_RIGHT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_RIGHT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_LEFT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_LEFT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_LEFT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_RIGHT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_RIGHT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_RIGHT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_LEFT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_LEFT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_LEFT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_RIGHT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_RIGHT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_RIGHT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_LEFT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_LEFT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_LEFT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_RIGHT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_RIGHT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_RIGHT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_LEFT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_LEFT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_LEFT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_RIGHT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_RIGHT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_RIGHT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_LEFT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_LEFT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_LEFT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_RIGHT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_RIGHT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_RIGHT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f20_codo_izq | angle | grados | 0..1 | C12>C14>C16 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f20_cadera_izq | angle | grados | 0..1 | C12>C24>C26 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f20_codo_der | angle | grados | 0..1 | C13>C15>C17 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f20_cadera_der | angle | grados | 0..1 | C13>C25>C27 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f20_hombro_izq | angle | grados | 0..1 | C24>C12>C14 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f20_rodilla_izq | angle | grados | 0..1 | C24>C26>C28 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f20_hombro_der | angle | grados | 0..1 | C25>C13>C15 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f20_rodilla_der | angle | grados | 0..1 | C25>C27>C29 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f20_tobillo_izq | angle | grados | 0..1 | C26>C28>C32 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f20_tobillo_der | angle | grados | 0..1 | C27>C29>C33 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f21_NOSE_x | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_NOSE_y | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_NOSE_z | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_LEFT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_LEFT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_LEFT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_RIGHT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_RIGHT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_RIGHT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_LEFT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_LEFT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_LEFT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_RIGHT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_RIGHT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_RIGHT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_LEFT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_LEFT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_LEFT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_RIGHT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_RIGHT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_RIGHT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_LEFT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_LEFT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_LEFT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_RIGHT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_RIGHT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_RIGHT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_LEFT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_LEFT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_LEFT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_RIGHT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_RIGHT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_RIGHT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_LEFT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_LEFT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_LEFT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_RIGHT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_RIGHT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_RIGHT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_LEFT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_LEFT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_LEFT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_RIGHT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_RIGHT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_RIGHT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_LEFT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_LEFT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_LEFT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_RIGHT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_RIGHT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_RIGHT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_LEFT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_LEFT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_LEFT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_RIGHT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_RIGHT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_RIGHT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_LEFT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_LEFT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_LEFT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_RIGHT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_RIGHT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_RIGHT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_LEFT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_LEFT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_LEFT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_RIGHT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_RIGHT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_RIGHT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f21_codo_izq | angle | grados | 0..1 | C12>C14>C16 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f21_cadera_izq | angle | grados | 0..1 | C12>C24>C26 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f21_codo_der | angle | grados | 0..1 | C13>C15>C17 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f21_cadera_der | angle | grados | 0..1 | C13>C25>C27 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f21_hombro_izq | angle | grados | 0..1 | C24>C12>C14 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f21_rodilla_izq | angle | grados | 0..1 | C24>C26>C28 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f21_hombro_der | angle | grados | 0..1 | C25>C13>C15 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f21_rodilla_der | angle | grados | 0..1 | C25>C27>C29 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f21_tobillo_izq | angle | grados | 0..1 | C26>C28>C32 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f21_tobillo_der | angle | grados | 0..1 | C27>C29>C33 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f22_NOSE_x | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_NOSE_y | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_NOSE_z | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_LEFT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_LEFT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_LEFT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_RIGHT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_RIGHT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_RIGHT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_LEFT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_LEFT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_LEFT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_RIGHT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_RIGHT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_RIGHT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_LEFT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_LEFT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_LEFT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_RIGHT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_RIGHT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_RIGHT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_LEFT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_LEFT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_LEFT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_RIGHT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_RIGHT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_RIGHT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_LEFT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_LEFT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_LEFT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_RIGHT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_RIGHT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_RIGHT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_LEFT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_LEFT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_LEFT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_RIGHT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_RIGHT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_RIGHT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_LEFT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_LEFT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_LEFT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_RIGHT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_RIGHT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_RIGHT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_LEFT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_LEFT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_LEFT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_RIGHT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_RIGHT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_RIGHT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_LEFT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_LEFT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_LEFT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_RIGHT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_RIGHT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_RIGHT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_LEFT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_LEFT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_LEFT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_RIGHT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_RIGHT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_RIGHT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_LEFT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_LEFT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_LEFT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_RIGHT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_RIGHT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_RIGHT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f22_codo_izq | angle | grados | 0..1 | C12>C14>C16 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f22_cadera_izq | angle | grados | 0..1 | C12>C24>C26 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f22_codo_der | angle | grados | 0..1 | C13>C15>C17 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f22_cadera_der | angle | grados | 0..1 | C13>C25>C27 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f22_hombro_izq | angle | grados | 0..1 | C24>C12>C14 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f22_rodilla_izq | angle | grados | 0..1 | C24>C26>C28 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f22_hombro_der | angle | grados | 0..1 | C25>C13>C15 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f22_rodilla_der | angle | grados | 0..1 | C25>C27>C29 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f22_tobillo_izq | angle | grados | 0..1 | C26>C28>C32 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f22_tobillo_der | angle | grados | 0..1 | C27>C29>C33 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f23_NOSE_x | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_NOSE_y | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_NOSE_z | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_LEFT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_LEFT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_LEFT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_RIGHT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_RIGHT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_RIGHT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_LEFT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_LEFT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_LEFT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_RIGHT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_RIGHT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_RIGHT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_LEFT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_LEFT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_LEFT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_RIGHT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_RIGHT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_RIGHT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_LEFT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_LEFT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_LEFT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_RIGHT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_RIGHT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_RIGHT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_LEFT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_LEFT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_LEFT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_RIGHT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_RIGHT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_RIGHT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_LEFT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_LEFT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_LEFT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_RIGHT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_RIGHT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_RIGHT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_LEFT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_LEFT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_LEFT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_RIGHT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_RIGHT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_RIGHT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_LEFT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_LEFT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_LEFT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_RIGHT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_RIGHT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_RIGHT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_LEFT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_LEFT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_LEFT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_RIGHT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_RIGHT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_RIGHT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_LEFT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_LEFT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_LEFT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_RIGHT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_RIGHT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_RIGHT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_LEFT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_LEFT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_LEFT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_RIGHT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_RIGHT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_RIGHT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f23_codo_izq | angle | grados | 0..1 | C12>C14>C16 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f23_cadera_izq | angle | grados | 0..1 | C12>C24>C26 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f23_codo_der | angle | grados | 0..1 | C13>C15>C17 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f23_cadera_der | angle | grados | 0..1 | C13>C25>C27 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f23_hombro_izq | angle | grados | 0..1 | C24>C12>C14 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f23_rodilla_izq | angle | grados | 0..1 | C24>C26>C28 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f23_hombro_der | angle | grados | 0..1 | C25>C13>C15 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f23_rodilla_der | angle | grados | 0..1 | C25>C27>C29 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f23_tobillo_izq | angle | grados | 0..1 | C26>C28>C32 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f23_tobillo_der | angle | grados | 0..1 | C27>C29>C33 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f24_NOSE_x | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_NOSE_y | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_NOSE_z | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_LEFT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_LEFT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_LEFT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_RIGHT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_RIGHT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_RIGHT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_LEFT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_LEFT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_LEFT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_RIGHT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_RIGHT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_RIGHT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_LEFT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_LEFT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_LEFT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_RIGHT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_RIGHT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_RIGHT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_LEFT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_LEFT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_LEFT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_RIGHT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_RIGHT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_RIGHT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_LEFT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_LEFT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_LEFT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_RIGHT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_RIGHT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_RIGHT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_LEFT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_LEFT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_LEFT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_RIGHT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_RIGHT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_RIGHT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_LEFT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_LEFT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_LEFT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_RIGHT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_RIGHT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_RIGHT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_LEFT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_LEFT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_LEFT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_RIGHT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_RIGHT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_RIGHT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_LEFT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_LEFT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_LEFT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_RIGHT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_RIGHT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_RIGHT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_LEFT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_LEFT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_LEFT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_RIGHT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_RIGHT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_RIGHT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_LEFT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_LEFT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_LEFT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_RIGHT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_RIGHT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_RIGHT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f24_codo_izq | angle | grados | 0..1 | C12>C14>C16 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f24_cadera_izq | angle | grados | 0..1 | C12>C24>C26 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f24_codo_der | angle | grados | 0..1 | C13>C15>C17 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f24_cadera_der | angle | grados | 0..1 | C13>C25>C27 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f24_hombro_izq | angle | grados | 0..1 | C24>C12>C14 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f24_rodilla_izq | angle | grados | 0..1 | C24>C26>C28 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f24_hombro_der | angle | grados | 0..1 | C25>C13>C15 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f24_rodilla_der | angle | grados | 0..1 | C25>C27>C29 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f24_tobillo_izq | angle | grados | 0..1 | C26>C28>C32 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f24_tobillo_der | angle | grados | 0..1 | C27>C29>C33 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f25_NOSE_x | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_NOSE_y | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_NOSE_z | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_LEFT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_LEFT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_LEFT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_RIGHT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_RIGHT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_RIGHT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_LEFT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_LEFT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_LEFT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_RIGHT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_RIGHT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_RIGHT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_LEFT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_LEFT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_LEFT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_RIGHT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_RIGHT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_RIGHT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_LEFT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_LEFT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_LEFT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_RIGHT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_RIGHT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_RIGHT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_LEFT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_LEFT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_LEFT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_RIGHT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_RIGHT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_RIGHT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_LEFT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_LEFT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_LEFT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_RIGHT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_RIGHT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_RIGHT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_LEFT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_LEFT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_LEFT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_RIGHT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_RIGHT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_RIGHT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_LEFT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_LEFT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_LEFT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_RIGHT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_RIGHT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_RIGHT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_LEFT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_LEFT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_LEFT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_RIGHT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_RIGHT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_RIGHT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_LEFT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_LEFT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_LEFT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_RIGHT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_RIGHT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_RIGHT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_LEFT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_LEFT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_LEFT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_RIGHT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_RIGHT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_RIGHT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f25_codo_izq | angle | grados | 0..1 | C12>C14>C16 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f25_cadera_izq | angle | grados | 0..1 | C12>C24>C26 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f25_codo_der | angle | grados | 0..1 | C13>C15>C17 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f25_cadera_der | angle | grados | 0..1 | C13>C25>C27 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f25_hombro_izq | angle | grados | 0..1 | C24>C12>C14 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f25_rodilla_izq | angle | grados | 0..1 | C24>C26>C28 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f25_hombro_der | angle | grados | 0..1 | C25>C13>C15 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f25_rodilla_der | angle | grados | 0..1 | C25>C27>C29 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f25_tobillo_izq | angle | grados | 0..1 | C26>C28>C32 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f25_tobillo_der | angle | grados | 0..1 | C27>C29>C33 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f26_NOSE_x | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_NOSE_y | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_NOSE_z | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_LEFT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_LEFT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_LEFT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_RIGHT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_RIGHT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_RIGHT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_LEFT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_LEFT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_LEFT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_RIGHT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_RIGHT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_RIGHT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_LEFT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_LEFT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_LEFT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_RIGHT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_RIGHT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_RIGHT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_LEFT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_LEFT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_LEFT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_RIGHT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_RIGHT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_RIGHT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_LEFT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_LEFT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_LEFT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_RIGHT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_RIGHT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_RIGHT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_LEFT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_LEFT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_LEFT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_RIGHT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_RIGHT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_RIGHT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_LEFT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_LEFT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_LEFT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_RIGHT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_RIGHT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_RIGHT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_LEFT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_LEFT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_LEFT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_RIGHT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_RIGHT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_RIGHT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_LEFT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_LEFT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_LEFT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_RIGHT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_RIGHT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_RIGHT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_LEFT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_LEFT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_LEFT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_RIGHT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_RIGHT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_RIGHT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_LEFT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_LEFT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_LEFT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_RIGHT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_RIGHT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_RIGHT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f26_codo_izq | angle | grados | 0..1 | C12>C14>C16 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f26_cadera_izq | angle | grados | 0..1 | C12>C24>C26 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f26_codo_der | angle | grados | 0..1 | C13>C15>C17 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f26_cadera_der | angle | grados | 0..1 | C13>C25>C27 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f26_hombro_izq | angle | grados | 0..1 | C24>C12>C14 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f26_rodilla_izq | angle | grados | 0..1 | C24>C26>C28 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f26_hombro_der | angle | grados | 0..1 | C25>C13>C15 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f26_rodilla_der | angle | grados | 0..1 | C25>C27>C29 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f26_tobillo_izq | angle | grados | 0..1 | C26>C28>C32 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f26_tobillo_der | angle | grados | 0..1 | C27>C29>C33 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f27_NOSE_x | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_NOSE_y | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_NOSE_z | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_LEFT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_LEFT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_LEFT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_RIGHT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_RIGHT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_RIGHT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_LEFT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_LEFT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_LEFT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_RIGHT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_RIGHT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_RIGHT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_LEFT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_LEFT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_LEFT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_RIGHT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_RIGHT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_RIGHT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_LEFT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_LEFT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_LEFT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_RIGHT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_RIGHT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_RIGHT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_LEFT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_LEFT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_LEFT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_RIGHT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_RIGHT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_RIGHT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_LEFT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_LEFT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_LEFT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_RIGHT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_RIGHT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_RIGHT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_LEFT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_LEFT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_LEFT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_RIGHT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_RIGHT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_RIGHT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_LEFT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_LEFT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_LEFT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_RIGHT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_RIGHT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_RIGHT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_LEFT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_LEFT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_LEFT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_RIGHT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_RIGHT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_RIGHT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_LEFT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_LEFT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_LEFT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_RIGHT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_RIGHT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_RIGHT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_LEFT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_LEFT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_LEFT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_RIGHT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_RIGHT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_RIGHT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f27_codo_izq | angle | grados | 0..1 | C12>C14>C16 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f27_cadera_izq | angle | grados | 0..1 | C12>C24>C26 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f27_codo_der | angle | grados | 0..1 | C13>C15>C17 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f27_cadera_der | angle | grados | 0..1 | C13>C25>C27 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f27_hombro_izq | angle | grados | 0..1 | C24>C12>C14 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f27_rodilla_izq | angle | grados | 0..1 | C24>C26>C28 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f27_hombro_der | angle | grados | 0..1 | C25>C13>C15 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f27_rodilla_der | angle | grados | 0..1 | C25>C27>C29 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f27_tobillo_izq | angle | grados | 0..1 | C26>C28>C32 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f27_tobillo_der | angle | grados | 0..1 | C27>C29>C33 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f28_NOSE_x | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_NOSE_y | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_NOSE_z | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_LEFT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_LEFT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_LEFT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_RIGHT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_RIGHT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_RIGHT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_LEFT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_LEFT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_LEFT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_RIGHT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_RIGHT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_RIGHT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_LEFT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_LEFT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_LEFT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_RIGHT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_RIGHT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_RIGHT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_LEFT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_LEFT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_LEFT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_RIGHT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_RIGHT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_RIGHT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_LEFT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_LEFT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_LEFT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_RIGHT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_RIGHT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_RIGHT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_LEFT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_LEFT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_LEFT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_RIGHT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_RIGHT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_RIGHT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_LEFT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_LEFT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_LEFT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_RIGHT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_RIGHT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_RIGHT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_LEFT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_LEFT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_LEFT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_RIGHT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_RIGHT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_RIGHT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_LEFT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_LEFT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_LEFT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_RIGHT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_RIGHT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_RIGHT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_LEFT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_LEFT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_LEFT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_RIGHT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_RIGHT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_RIGHT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_LEFT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_LEFT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_LEFT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_RIGHT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_RIGHT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_RIGHT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f28_codo_izq | angle | grados | 0..1 | C12>C14>C16 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f28_cadera_izq | angle | grados | 0..1 | C12>C24>C26 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f28_codo_der | angle | grados | 0..1 | C13>C15>C17 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f28_cadera_der | angle | grados | 0..1 | C13>C25>C27 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f28_hombro_izq | angle | grados | 0..1 | C24>C12>C14 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f28_rodilla_izq | angle | grados | 0..1 | C24>C26>C28 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f28_hombro_der | angle | grados | 0..1 | C25>C13>C15 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f28_rodilla_der | angle | grados | 0..1 | C25>C27>C29 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f28_tobillo_izq | angle | grados | 0..1 | C26>C28>C32 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f28_tobillo_der | angle | grados | 0..1 | C27>C29>C33 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f29_NOSE_x | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_NOSE_y | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_NOSE_z | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_LEFT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_LEFT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_LEFT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_RIGHT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_RIGHT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_RIGHT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_LEFT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_LEFT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_LEFT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_RIGHT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_RIGHT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_RIGHT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_LEFT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_LEFT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_LEFT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_RIGHT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_RIGHT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_RIGHT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_LEFT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_LEFT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_LEFT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_RIGHT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_RIGHT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_RIGHT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_LEFT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_LEFT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_LEFT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_RIGHT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_RIGHT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_RIGHT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_LEFT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_LEFT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_LEFT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_RIGHT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_RIGHT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_RIGHT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_LEFT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_LEFT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_LEFT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_RIGHT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_RIGHT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_RIGHT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_LEFT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_LEFT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_LEFT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_RIGHT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_RIGHT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_RIGHT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_LEFT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_LEFT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_LEFT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_RIGHT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_RIGHT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_RIGHT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_LEFT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_LEFT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_LEFT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_RIGHT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_RIGHT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_RIGHT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_LEFT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_LEFT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_LEFT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_RIGHT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_RIGHT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_RIGHT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f29_codo_izq | angle | grados | 0..1 | C12>C14>C16 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f29_cadera_izq | angle | grados | 0..1 | C12>C24>C26 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f29_codo_der | angle | grados | 0..1 | C13>C15>C17 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f29_cadera_der | angle | grados | 0..1 | C13>C25>C27 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f29_hombro_izq | angle | grados | 0..1 | C24>C12>C14 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f29_rodilla_izq | angle | grados | 0..1 | C24>C26>C28 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f29_hombro_der | angle | grados | 0..1 | C25>C13>C15 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f29_rodilla_der | angle | grados | 0..1 | C25>C27>C29 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f29_tobillo_izq | angle | grados | 0..1 | C26>C28>C32 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f29_tobillo_der | angle | grados | 0..1 | C27>C29>C33 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f30_NOSE_x | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_NOSE_y | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_NOSE_z | kpoint | coordenada | 0..100 | MediaPipe Pose NOSE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_LEFT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_LEFT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_LEFT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_RIGHT_SHOULDER_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_RIGHT_SHOULDER_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_RIGHT_SHOULDER_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_SHOULDER, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_LEFT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_LEFT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_LEFT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_RIGHT_ELBOW_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_RIGHT_ELBOW_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_RIGHT_ELBOW_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ELBOW, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_LEFT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_LEFT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_LEFT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_RIGHT_WRIST_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_RIGHT_WRIST_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_RIGHT_WRIST_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_WRIST, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_LEFT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_LEFT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_LEFT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_RIGHT_PINKY_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_RIGHT_PINKY_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_RIGHT_PINKY_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_PINKY, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_LEFT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_LEFT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_LEFT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_RIGHT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_RIGHT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_RIGHT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_LEFT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_LEFT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_LEFT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_RIGHT_THUMB_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_RIGHT_THUMB_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_RIGHT_THUMB_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_THUMB, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_LEFT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_LEFT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_LEFT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_RIGHT_HIP_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_RIGHT_HIP_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_RIGHT_HIP_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HIP, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_LEFT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_LEFT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_LEFT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_RIGHT_KNEE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_RIGHT_KNEE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_RIGHT_KNEE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_KNEE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_LEFT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_LEFT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_LEFT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_RIGHT_ANKLE_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_RIGHT_ANKLE_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_RIGHT_ANKLE_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_ANKLE, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_LEFT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_LEFT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_LEFT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_RIGHT_HEEL_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_RIGHT_HEEL_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_RIGHT_HEEL_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_HEEL, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_LEFT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_LEFT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_LEFT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose LEFT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_RIGHT_FOOT_INDEX_x | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje x | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_RIGHT_FOOT_INDEX_y | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje y | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_RIGHT_FOOT_INDEX_z | kpoint | coordenada | 0..100 | MediaPipe Pose RIGHT_FOOT_INDEX, eje z | caja 100x100 (rectangulo), 2 decimales; remuestreado a 30 cuadros |
| f30_codo_izq | angle | grados | 0..1 | C12>C14>C16 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f30_cadera_izq | angle | grados | 0..1 | C12>C24>C26 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f30_codo_der | angle | grados | 0..1 | C13>C15>C17 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f30_cadera_der | angle | grados | 0..1 | C13>C25>C27 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f30_hombro_izq | angle | grados | 0..1 | C24>C12>C14 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f30_rodilla_izq | angle | grados | 0..1 | C24>C26>C28 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f30_hombro_der | angle | grados | 0..1 | C25>C13>C15 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f30_rodilla_der | angle | grados | 0..1 | C25>C27>C29 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f30_tobillo_izq | angle | grados | 0..1 | C26>C28>C32 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
| f30_tobillo_der | angle | grados | 0..1 | C27>C29>C33 | valor / 180, recortado a 0..1; remuestreado a 30 cuadros |
