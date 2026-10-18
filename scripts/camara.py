"""Utilidad: descubre que indices de camara responden en esta maquina.

    python scripts/camara.py

El panel web hace lo mismo desde el boton "Detectar camaras" (endpoint
/api/cameras); ambos caminos usan src.captura.fuentes.camara.list_cameras para no duplicar
la logica de sondeo.
"""



from src.captura.fuentes.camara import list_cameras, nombres_camaras_windows  # noqa: E402

print("Probando indices 0 a 7 (DSHOW y MSMF)...\n")
encontradas = list_cameras(max_index=8)

for c in encontradas:
    print(f"  camara {c['index']}: OK  ({c['width']}x{c['height']})")

if encontradas:
    print(f"\nUsa:  python scripts/evaluar.py --exercise <slug> --camera {encontradas[0]['index']}")
else:
    vistas = nombres_camaras_windows()
    if vistas:
        print("Windows ve estas camaras conectadas, pero OpenCV no pudo abrir ninguna:")
        for n in vistas:
            print(f"  - {n}")
        print("\nProbablemente sea un permiso de Windows (Configuracion > Privacidad y "
              "seguridad > Camara > 'Permitir que las aplicaciones de escritorio "
              "accedan a la camara') o que otra app (Teams, Zoom, Meet) la tenga abierta.")
    else:
        print("Ninguna camara respondio, y Windows tampoco reporta ninguna conectada. "
              "Revisa el cable/USB o el Administrador de dispositivos.")
