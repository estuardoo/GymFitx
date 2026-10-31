# `src/entrenamiento/entrenar.py`

```text
Etapa 6: orquesta un entrenamiento: datos -> modelos + validacion -> reportes -> modelo.joblib con su spec.
```

## `entrenar`

`def entrenar(test_pct=None, modelos=None, tipo=None, features='ambos', fuera=True, personas=None)`

```text
Entrena y compara clasificadores sobre table_frames_fix de los clips del
manifest, con el mismo k-fold para todos.

- Criterio: F1 macro (no accuracy): con clases desbalanceadas un modelo que
  dice siempre la clase mayoritaria ya saca buen accuracy.
- 'linea_base' (DummyClassifier, clase mas frecuente) se reporta para
  comparar; nunca puede ganar.
- 'anidado' = estimacion sin sesgo del procedimiento de seleccion.
- El modelo guardado lleva su 'spec' (puntos, normalizacion, features)
  para que el panel en vivo arme exactamente el mismo vector.
- 'personas' = las personas (P1, P2...) cuyos clips entran; None = todas.
```

