import os
import time
import random
import threading
import ctypes
from ctypes import wintypes
import pystray
from PIL import Image, ImageDraw
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Configuration ---
CONFIG_FILE = "wallpaper_config.json"
CARPETA_IMAGENES_PORTRAIT = r"C:\Users\daned\Documents\Wallpapers\PORTRAIT"
CARPETA_IMAGENES_NORMALES = r"C:\Users\daned\Documents\Wallpapers\NORMALES"
EXTENSIONES_VALIDAS = {'.jpg', '.jpeg', '.png', '.bmp'}

OPCIONES_TIEMPO = {
    "1 minuto": 60,
    "10 minutos": 600,
    "30 minutos": 1800,
    "1 hora": 3600,
    "6 horas": 21600,
    "12 horas": 43200,
    "24 horas": 86400
}

intervalo_actual = 300
stop_event = threading.Event()
trigger_event = threading.Event()
current_wallpapers = {}

# =========================================================
# CONFIG MANAGEMENT
# =========================================================
def cargar_configuracion():
    global intervalo_actual, CARPETA_IMAGENES_PORTRAIT, CARPETA_IMAGENES_NORMALES
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                intervalo_actual = config.get('intervalo', 300)
                CARPETA_IMAGENES_PORTRAIT = config.get('carpeta_portrait', CARPETA_IMAGENES_PORTRAIT)
                CARPETA_IMAGENES_NORMALES = config.get('carpeta_normales', CARPETA_IMAGENES_NORMALES)
                logger.info("Configuración cargada correctamente")
        except Exception as e:
            logger.error(f"Error cargando configuración: {e}")

def guardar_configuracion():
    try:
        config = {
            'intervalo': intervalo_actual,
            'carpeta_portrait': CARPETA_IMAGENES_PORTRAIT,
            'carpeta_normales': CARPETA_IMAGENES_NORMALES
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
        logger.info("Configuración guardada correctamente")
    except Exception as e:
        logger.error(f"Error guardando configuración: {e}")

# =========================================================
# WINDOWS 11 WALLPAPER INTERFACE (COM)
# =========================================================

CLSID_DesktopWallpaper = b"\x10\x31\xcf\xc2\x0e\x46\xc1\x4f\xb9\xd0\x8a\x1c\x0c\x9c\xc4\xbd"
IID_IDesktopWallpaper = b"\xa9\x56\x2b\xb9\x55\x8b\x14\x4e\x9a\x89\x01\x99\xbb\xb6\xf9\x3b"

class IDesktopWallpaper(ctypes.Structure):
    pass

class RECT(ctypes.Structure):
    _fields_ = [
        ("left", ctypes.c_long),
        ("top", ctypes.c_long),
        ("right", ctypes.c_long),
        ("bottom", ctypes.c_long),
    ]

class IDesktopWallpaper_VTable(ctypes.Structure):
    _fields_ = [
        ("QueryInterface", ctypes.CFUNCTYPE(ctypes.c_long, ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p))),
        ("AddRef", ctypes.CFUNCTYPE(ctypes.c_ulong, ctypes.c_void_p)),
        ("Release", ctypes.CFUNCTYPE(ctypes.c_ulong, ctypes.c_void_p)),
        ("SetWallpaper", ctypes.CFUNCTYPE(ctypes.c_long, ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_wchar_p)),
        ("GetWallpaper", ctypes.CFUNCTYPE(ctypes.c_long, ctypes.c_void_p, ctypes.c_wchar_p, ctypes.POINTER(ctypes.c_wchar_p))),
        ("GetMonitorDevicePathAt", ctypes.CFUNCTYPE(ctypes.c_long, ctypes.c_void_p, ctypes.c_uint, ctypes.POINTER(ctypes.c_wchar_p))),
        ("GetMonitorDevicePathCount", ctypes.CFUNCTYPE(ctypes.c_long, ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint))),
        ("GetMonitorRECT", ctypes.CFUNCTYPE(ctypes.c_long, ctypes.c_void_p, ctypes.c_wchar_p, ctypes.POINTER(RECT))),
    ]
IDesktopWallpaper._fields_ = [("lpVtbl", ctypes.POINTER(IDesktopWallpaper_VTable))]

def inicializar_wallpaper_manager():
    try:
        ctypes.windll.ole32.CoInitialize(None)
        p_desktop_wallpaper = ctypes.POINTER(IDesktopWallpaper)()
        clsid_struct = (ctypes.c_ubyte * 16).from_buffer_copy(CLSID_DesktopWallpaper)
        iid_struct = (ctypes.c_ubyte * 16).from_buffer_copy(IID_IDesktopWallpaper)

        hr = ctypes.windll.ole32.CoCreateInstance(
            ctypes.byref(clsid_struct),
            None,
            4,
            ctypes.byref(iid_struct),
            ctypes.byref(p_desktop_wallpaper)
        )

        if hr != 0:
            raise Exception(f"Error CoCreateInstance: {hr}")
        return p_desktop_wallpaper
    except Exception as e:
        logger.error(f"Error inicializando wallpaper manager: {e}")
        return None

# =========================================================
# MAIN FUNCTIONS
# =========================================================

def obtener_imagenes(carpeta):
    """Obtiene una lista de rutas de imágenes en la carpeta especificada."""
    if not os.path.exists(carpeta):
        logger.warning(f"Carpeta no existe: {carpeta}")
        return []
    try:
        return [os.path.join(carpeta, f)
                for f in os.listdir(carpeta)
                if f.lower().endswith(tuple(EXTENSIONES_VALIDAS))]
    except Exception as e:
        logger.error(f"Error leyendo carpeta {carpeta}: {e}")
        return []

def cambiar_wallpapers(manager):
    """Cambia el wallpaper en todos los monitores detectados."""
    global current_wallpapers
    if manager is None:
        logger.error("Manager no inicializado")
        return
    
    try:
        vtbl = manager.contents.lpVtbl.contents
        count = ctypes.c_uint()
        vtbl.GetMonitorDevicePathCount(manager, ctypes.byref(count))
        logger.info(f"Cambio de fondo: {time.strftime('%Y-%m-%d %H:%M:%S')} | Monitores: {count.value}")
        nuevos_wallpapers = {}

        for i in range(count.value):
            monitor_id = ctypes.c_wchar_p()
            vtbl.GetMonitorDevicePathAt(manager, i, ctypes.byref(monitor_id))

            rect = RECT()
            hr = vtbl.GetMonitorRECT(manager, monitor_id, ctypes.byref(rect))
        
            if hr == 0:
                ancho = abs(rect.right - rect.left)
                alto = abs(rect.bottom - rect.top)
                logger.info(f"Monitor {i + 1} Dim: {ancho}x{alto}")
                carpeta_seleccionada = CARPETA_IMAGENES_PORTRAIT if alto > ancho else CARPETA_IMAGENES_NORMALES
            else:
                logger.warning(f"No se pudo obtener RECT para monitor {i + 1}, usando Normales")
                carpeta_seleccionada = CARPETA_IMAGENES_NORMALES

            imagenes = obtener_imagenes(carpeta_seleccionada)
            if imagenes:
                imagen_seleccionada = random.choice(imagenes)
                vtbl.SetWallpaper(manager, monitor_id, imagen_seleccionada)
                nuevos_wallpapers[i + 1] = imagen_seleccionada
                logger.info(f"Monitor {i + 1}: {os.path.basename(imagen_seleccionada)}")
            else:
                logger.warning(f"No hay imágenes en {carpeta_seleccionada}")
                
            ctypes.windll.ole32.CoTaskMemFree(monitor_id)
            
        # Actualizar el diccionario global solo al final para evitar mostrar monitores viejos
        current_wallpapers = nuevos_wallpapers
    except Exception as e:
        logger.error(f"Error cambiando wallpaper: {e}")

# =========================================================
# WALLPAPER LOOP THREAD
# =========================================================
def bucle_wallpaper():
    manager = inicializar_wallpaper_manager()
    if manager is None:
        logger.error("No se pudo inicializar el manager de wallpaper")
        return
    
    try:
        cambiar_wallpapers(manager)
        while not stop_event.is_set():
            evento_activado = trigger_event.wait(timeout=intervalo_actual)
            if stop_event.is_set():
                break
            if evento_activado:
                trigger_event.clear()
            cambiar_wallpapers(manager)
    except Exception as e:
        logger.error(f"Error en bucle_wallpaper: {e}")
    finally:
        ctypes.windll.ole32.CoUninitialize()

# =========================================================
# SYSTEM TRAY FUNCTIONS
# =========================================================
def set_tiempo(segundos):
    def wrapper(icon, item):
        global intervalo_actual
        intervalo_actual = segundos
        guardar_configuracion()
        trigger_event.set()
    return wrapper

def is_checked(segundos):
    def wrapper(item):
        return intervalo_actual == segundos
    return wrapper

def crear_icono():
    icon_image = Image.new('RGB', (64, 64), color=(73, 109, 137))
    draw = ImageDraw.Draw(icon_image)
    draw.text((10, 25), "WP", fill=(255, 255, 255))
    return icon_image

def iniciar_tray_icon():
    items_tiempo = []
    for texto, segundos in OPCIONES_TIEMPO.items():
        items_tiempo.append(
            pystray.MenuItem(
                texto, 
                set_tiempo(segundos), 
                checked=is_checked(segundos),
                radio=True
            )
        )
    menu = pystray.Menu(
        pystray.MenuItem('Cambiar Ahora', lambda icon, item: trigger_event.set()),
        pystray.MenuItem('Frecuencia', pystray.Menu(*items_tiempo)),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem('Salir', lambda icon, item: [stop_event.set(), trigger_event.set(), icon.stop()])
    )   
    icon = pystray.Icon("WallpaperChanger", crear_icono(), "Wallpaper Changer", menu)
     
    t = threading.Thread(target=bucle_wallpaper, daemon=True)
    t.start()
    
    try:
        icon.run()
    except Exception as e:
        logger.error(f"Error en tray icon: {e}")

if __name__ == "__main__":
    if ctypes.sizeof(ctypes.c_voidp) * 8 == 32:
        logger.error("Se requiere Python 64-bit")
        os._exit(1)
    
    cargar_configuracion()
    iniciar_tray_icon()