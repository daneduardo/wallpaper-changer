# mywallpaper_changer

Pequeño script para cambiar el fondo de pantalla en Windows. El archivo principal es `mywallpaper_changer.pyw` ubicado en la raíz del proyecto.

## Requisitos
- Windows
- Python 3.8+
- Módulos estándar de Python (`os`, `glob`, `ctypes`, `random`, `time`, etc.).

Si usas un entorno virtual, actívalo antes de ejecutar el script.

## Uso

Ejecutar en segundo plano (sin consola):

```powershell
pythonw mywallpaper_changer.pyw
```

Ejecutar con consola (para ver mensajes de depuración):

```powershell
python mywallpaper_changer.pyw
```

## Estructura esperada

- `Wallpapers/` — carpeta con subcarpetas como `NORMALES/`, `PORTRAIT/`.
- `mywallpaper_changer.pyw` — script principal.

## Funciones y fragmentos útiles

Si al ejecutar ves el error "obtener_imagenes is not defined", añade la siguiente función cerca del inicio de `mywallpaper_changer.pyw`:

```python
def obtener_imagenes(carpeta):
    import os
    import glob

    patrones = ('*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.tif', '*.tiff', '*.webp')
    imagenes = []
    for p in patrones:
        imagenes.extend(glob.glob(os.path.join(carpeta, p)))
    imagenes = [os.path.abspath(p) for p in imagenes if os.path.isfile(p)]
    imagenes.sort()
    return imagenes

# Para búsqueda recursiva, usa pathlib.Path(carpeta).rglob("*") y filtra por sufijos.
```

## Problemas comunes

- Error: `obtener_imagenes is not defined` — falta la función; pega el snippet anterior.
- Problemas con `monitor_id_ptr` o llamadas a la API de Windows — asegúrate de crear buffers/`c_wchar_p` correctamente (ej.: `ctypes.create_unicode_buffer(260)`).

## Contribuciones y pruebas

Si quieres que añada validación adicional o un instalador (requirements.txt), dime y lo preparo.

---
Archivo creado para ayudar a ejecutar y depurar `mywallpaper_changer.pyw`.
