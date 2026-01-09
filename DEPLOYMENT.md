# 🚀 Guía de Despliegue - Wallpaper Changer Web

## Requisitos Previos

✅ Python 3.8 o superior (64-bit)  
✅ Las dependencias instaladas (`pip install -r requirements.txt`)  
✅ Las carpetas de imágenes creadas  

## 📋 Checklist de Configuración

Antes de iniciar, verifica que tengas:

```
wallpaper-changer/
├── app.py                           ✓ Servidor Flask
├── mywallpaperchanger.py           ✓ Código principal
├── requirements.txt                 ✓ Dependencias
├── templates/
│   └── index.html                   ✓ Interfaz web
├── start_web.bat                    ✓ Iniciar web (Windows)
└── wallpaper_config.json            ✓ Configuración (se genera automáticamente)

C:\Users\TuUsuario\Documents\Wallpapers/
├── PORTRAIT/                        ✓ Imágenes verticales
└── NORMALES/                        ✓ Imágenes horizontales
```

## 🚀 Opción 1: Inicio Rápido (Recomendado)

### En Windows:

1. **Haz doble clic en `start_web.bat`**
2. El navegador se abrirá automáticamente en `http://127.0.0.1:5000`
3. Configura según tus preferencias

### En Terminal:

```bash
python app.py
```

El navegador se abrirá automáticamente.

## 🚀 Opción 2: Inicio Manual

```bash
# 1. Abre CMD o PowerShell
# 2. Navega a la carpeta del proyecto
cd C:\Users\daned\OneDrive\Documentos\GitHub\wallpaper-changer

# 3. Inicia el servidor
python app.py

# 4. Abre tu navegador en:
# http://127.0.0.1:5000
```

## 🌐 Acceso a la Interfaz Web

**URL Local:**
```
http://127.0.0.1:5000
```

**Desde otros equipos en la red:**
```
http://TU_IP_LOCAL:5000
```

Para encontrar tu IP:
- En CMD: `ipconfig`
- Busca "IPv4 Address" (ejemplo: 192.168.1.100)

## 🔧 Configuración Inicial

1. **Verifica las carpetas de imágenes**
   - Si no existen, crea:
     - `C:\Users\TuUsuario\Documents\Wallpapers\PORTRAIT`
     - `C:\Users\TuUsuario\Documents\Wallpapers\NORMALES`
   - O actualiza las rutas en la interfaz web

2. **Carga imágenes**
   - Coloca imágenes `.jpg`, `.png`, `.bmp` en las carpetas
   - La interfaz mostrará el contador automáticamente

3. **Configura el intervalo**
   - Selecciona cada cuánto tiempo cambiar wallpaper
   - Haz clic en "Guardar Configuración"

4. **Prueba**
   - Click en "Cambiar Ahora" para cambiar inmediatamente

## 📊 Estructura de Carpetas de Imágenes

**Recomendado:**

```
Wallpapers/
├── PORTRAIT/
│   ├── imagen1.jpg          (1080x1920 o similar)
│   ├── imagen2.jpg
│   └── ...
└── NORMALES/
    ├── wallpaper1.jpg       (1920x1080 o similar)
    ├── wallpaper2.png
    └── ...
```

**Formatos soportados:**
- `.jpg` / `.jpeg`
- `.png`
- `.bmp`

## 🛑 Detener el Servidor

Presiona `CTRL+C` en la terminal donde ejecutaste `python app.py`

```
^C
```

## 🔄 Reiniciar el Servidor

Simplemente ejecuta nuevamente:
```bash
python app.py
```

## ⚙️ Puertos Alternativos

Si el puerto 5000 está ocupado, edita `app.py`:

```python
if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=8080)  # Cambiar 5000 por 8080
```

Luego accede en: `http://127.0.0.1:8080`

## 🌍 Acceder desde Otros Equipos

Si quieres acceder desde otro equipo en la red:

1. Edita `app.py` y cambia:
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

2. Accede desde otro equipo usando:
```
http://TU_IP_LOCAL:5000
```

⚠️ **Nota:** Esto expondrá la app en tu red local. Ten cuidado con la seguridad.

## 🐛 Solucionar Problemas

### "No se encuentra Flask"
```bash
pip install Flask==2.3.3
```

### "No se encuentra mywallpaperchanger"
- Asegúrate de ejecutar `app.py` desde la carpeta correcta
- Verifica que `mywallpaperchanger.py` esté en la misma carpeta

### "Carpeta templates no encontrada"
```bash
# Crea la carpeta
mkdir templates

# Coloca index.html dentro
```

### El navegador no se abre automáticamente
- Abre manualmente: `http://127.0.0.1:5000`
- O revisa el puerto en `app.py`

### "Address already in use"
- Puerto 5000 está en uso
- Cambia el puerto en `app.py` (línea 90)
- O cierra la aplicación que usa ese puerto

## 📝 Configuración Avanzada

### Cambiar carpetas de imágenes desde la interfaz

1. En la web, edita los campos de ruta
2. Haz clic "Guardar Configuración"
3. Las nuevas rutas se aplicarán inmediatamente

### Ver logs detallados

Los logs aparecen en la terminal donde ejecutaste `app.py`:
```
2024-01-15 10:30:45,123 - INFO - GET /api/config
2024-01-15 10:30:46,456 - INFO - Cambio de fondo: 2024-01-15 10:30:46
```

## ✅ Verificación Final

- [ ] Python 3.8+ instalado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Carpetas de imágenes existen
- [ ] `templates/index.html` está presente
- [ ] Servidor se inicia sin errores
- [ ] Navegador abre en `http://127.0.0.1:5000`
- [ ] Puedes ver y cambiar configuración

---

**¿Necesitas más ayuda? Revisa el README.md principal**
