# 🖼️ Wallpaper Changer

Una aplicación de Windows que cambia automáticamente el fondo de pantalla a intervalos regulares, con soporte para múltiples monitores y una interfaz web para configuración.

## ✨ Características

- ✅ Cambio automático de wallpaper en múltiples monitores
- ✅ Detección automática de orientación (vertical/horizontal)
- ✅ Interfaz web moderna para configuración
- ✅ Bandeja del sistema (System Tray)
- ✅ Ejecución en segundo plano
- ✅ Configuración persistente (JSON)
- ✅ Logging detallado
- ✅ Compatible con Windows 11

## 📋 Requisitos

- **Python 3.8+** (64-bit) - [Descargar aquí](https://www.python.org/downloads/)
- **Windows 7 o superior**
- **Carpetas de imágenes** configuradas
- **pip** (incluido con Python)

## 🚀 Instalación

### 1. Clonar o descargar el repositorio

```bash
git clone <tu-repo>
cd wallpaper-changer
```

### 2. Crear carpetas de imágenes

Crea las siguientes carpetas en `C:\Users\TuUsuario\Documents`:

```
Wallpapers/
├── PORTRAIT/    (imágenes verticales)
└── NORMALES/    (imágenes horizontales)
```

**O** modifica las rutas en `mywallpaperchanger.py` según tus preferencias.

### 3. Instalar dependencias

#### Opción A: Instalador automático (Recomendado)

```bash
install_dependencies.bat
```

Simplemente haz doble clic en el archivo `install_dependencies.bat`

#### Opción B: Instalación manual

```bash
pip install --only-binary :all: -r requirements.txt
```

#### Opción C: Instalación sin Pillow (si hay problemas)

```bash
pip install Flask==2.3.3 pystray==0.19.4
pip install --upgrade Pillow
```

## 🎮 Uso

### Opción 1: Ejecutar con Interface Web (Recomendado)

```bash
python app.py
```

Luego abre tu navegador en `http://localhost:5000`

### Opción 2: Ejecutar en bandeja del sistema

```bash
python mywallpaperchanger.py
```

### Opción 3: Ejecutar en segundo plano (Windows)

Haz doble clic en `run_background.vbs`

## 🔧 Configuración

### A través de la interfaz web:

1. Abre `http://localhost:5000`
2. Configura:
   - **Intervalo de cambio**: Selecciona cada cuánto tiempo cambiar
   - **Carpeta Vertical**: Ruta de imágenes en orientación vertical
   - **Carpeta Horizontal**: Ruta de imágenes en orientación horizontal
3. Haz clic en "Guardar Configuración"

### Archivo de configuración (wallpaper_config.json):

```json
{
    "intervalo": 3600,
    "carpeta_portrait": "C:\\Users\\daned\\Documents\\Wallpapers\\PORTRAIT",
    "carpeta_normales": "C:\\Users\\daned\\Documents\\Wallpapers\\NORMALES"
}
```

## 🖼️ Estructura de archivos

```
wallpaper-changer/
├── mywallpaperchanger.py       # Aplicación principal
├── app.py                       # Servidor Flask (web UI)
├── requirements.txt             # Dependencias
├── install_dependencies.bat     # Instalador automático
├── run_background.vbs           # Script para ejecutar en background
├── wallpaper_config.json        # Configuración (se genera automáticamente)
├── templates/
│   └── index.html              # Interfaz web
└── README.md                    # Este archivo
```

## 🌐 Interfaz Web

La interfaz web proporciona:

- 📊 Configuración visual de parámetros
- 🔢 Contador de imágenes por carpeta
- 🔄 Botón para cambiar wallpaper inmediatamente
- 💾 Guardado automático de configuración
- ✅ Validación en tiempo real

## 🎯 Opciones de intervalo

- 1 minuto
- 10 minutos
- 30 minutos
- 1 hora
- 6 horas
- 12 horas
- 24 horas

## 🖥️ Iniciar con Windows

### Opción 1: Crear acceso directo en Inicio

1. Presiona `Win + R` y escribe `shell:startup`
2. Copia `run_background.vbs` a esa carpeta

### Opción 2: Agregar a Tareas Programadas

1. Abre "Programador de Tareas"
2. Crea una tarea nueva
3. Acción: `python.exe`
4. Argumentos: `C:\ruta\a\mywallpaperchanger.py`
5. Ejecutar con privilegios: ✓

## 📝 Características Técnicas

### Compatibilidad de monitores

- Detecta automáticamente orientación (vertical/horizontal)
- Selecciona carpeta apropiada según orientación
- Soporta múltiples monitores con diferentes orientaciones

### Gestión de recursos

- Logging detallado en consola
- Manejo robusto de errores
- Liberación correcta de recursos COM
- Thread daemon para ejecución en background

### Rendimiento

- Cambios de wallpaper rápidos
- Bajo consumo de memoria
- No ralentiza el sistema

## 🐛 Solucionar problemas

### ERROR: Failed to build 'Pillow'

**Solución 1: Usar instalador automático**
```bash
install_dependencies.bat
```

**Solución 2: Instalar pre-built wheels**
```bash
pip install --only-binary :all: -r requirements.txt
```

**Solución 3: Instalar solo lo necesario**
```bash
pip install Flask==2.3.3 pystray==0.19.4
pip install --upgrade Pillow
```

**Solución 4: Descargar e instalar Pillow manualmente**
- Descarga desde: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pillow
- Instala con: `pip install Pillow-10.0.0-cp311-cp311-win_amd64.whl` (ajusta la versión según tu Python)

### "No se pudo crear la instancia de IDesktopWallpaper"

- Asegúrate de usar Python 64-bit
- Verifica: `python -c "import struct; print(struct.calcsize('P') * 8)"`
- Debe mostrar `64`

### Las imágenes no se encuentran

- Verifica que las rutas existan
- Usa caracteres ASCII en nombres de carpetas
- Comprueba los permisos de lectura

### La interface web no carga

- Verifica que Flask esté instalado: `pip install Flask`
- Cambia el puerto si 5000 está en uso
- Desactiva firewall temporalmente

### Python no está en el PATH

- Reinstala Python y marca "Add Python to PATH" durante la instalación
- O agrega manualmente la ruta de instalación al PATH

## 💡 Tips y Trucos

- Use `mywallpaperchanger.py` para máximo control (system tray)
- Use `app.py` para cambios frecuentes de configuración
- Coloca imágenes en las carpetas correctas (PORTRAIT vs NORMALES)
- Aumenta el intervalo para cambios menos frecuentes y menor consumo de recursos

## 📄 Licencia

Libre para uso personal y educativo.

## 👨‍💻 Autor

Daned

---

**¿Problemas? Sigue los pasos de solución de problemas arriba o abre un issue**
