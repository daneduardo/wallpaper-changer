import os
import time
import random
import threading
import ctypes
from ctypes import wintypes
import pystray
from PIL import Image, ImageDraw

# --- Set Windows 11 Wallpaper ---
# Ruta de la carpeta que contiene las imágenes
CARPETA_IMAGENES_PORTRAIT = r"C:\Users\daned\Documents\Wallpapers\PORTRAIT"
CARPETA_IMAGENES_NORMALES = r"C:\Users\daned\Documents\Wallpapers\NORMALES"
EXTENSIONES_VALIDAS = {'.jpg', '.jpeg', '.png', '.bmp'}

# Tiempo de espera entre cambios de fondo (en segundos)
# Ejemplo: 60 segundos = 1 minuto, 3600 segundos = 1 hora, 86400 segundos = 1 día
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

# Eventos de control
stop_event = threading.Event()
trigger_event = threading.Event()

# =========================================================
# DEFINICION DE LA INTERFAZ DE WINDOWS 11 (COM)
# =========================================================

# Definimos la interfaz INTERNA DE WINDOWS 11 PARA CAMBIAR EL FONDO DE PANTALLA

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

# Tabla de metodos virtuales para IDesktopWallpaper
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
         # Otros métodos no se definen aquí para simplificar
     ]
IDesktopWallpaper._fields_ = [("lpVtbl", ctypes.POINTER(IDesktopWallpaper_VTable))]

def inicializar_wallpaper_manager():
        # Inicializa y devuelve una instancia de IDesktopWallpaper
        ctypes.windll.ole32.CoInitialize(None)
        p_desktop_wallpaper = ctypes.POINTER(IDesktopWallpaper)()
        # Crear instancia usando CoCreateInstance directamente
        # CLSID, None, CLSCTX_LOCAL_SERVER, IID, result pointer
        clsid_struct = (ctypes.c_ubyte * 16).from_buffer_copy(CLSID_DesktopWallpaper)
        iid_struct = (ctypes.c_ubyte * 16).from_buffer_copy(IID_IDesktopWallpaper)

        hr=ctypes.windll.ole32.CoCreateInstance(
            ctypes.byref(clsid_struct),
            None,
            4,  # CLSCTX_LOCAL_SERVER
            ctypes.byref(iid_struct),
            ctypes.byref(p_desktop_wallpaper)
        )

        if hr != 0:
            raise Exception("No se pudo crear la instancia de IDesktopWallpaper. Código de error: {}".format(hr))
        return p_desktop_wallpaper
        
# =========================================================
# FUNCIONES PRINCIPALES
# =========================================================
        
def obtener_imagenes(carpeta):
        """Obtiene una lista de rutas de imágenes en la carpeta especificada."""
        if not os.path.exists(carpeta):
            return []
        return [os.path.join(carpeta, f)
                for f in os.listdir(carpeta)
                if f.lower().endswith(tuple(EXTENSIONES_VALIDAS))]

    
def cambiar_wallpapars(manager):
    vtbl = manager.contents.lpVtbl.contents
    count = ctypes.c_uint()
    vtbl.GetMonitorDevicePathCount(manager, ctypes.byref(count))
    print(f"\n-- Hora de cambio de fondo: {time.strftime('%Y-%m-%d %H:%M:%S')} | Monitores detectados: {count.value} --")

    for i in range(count.value):
        monitor_id = ctypes.c_wchar_p()
        vtbl.GetMonitorDevicePathAt(manager, i, ctypes.byref(monitor_id))

        rect = RECT()
        hr = vtbl.GetMonitorRECT(manager, monitor_id, ctypes.byref(rect))
    
        if hr == 0:
            ancho = rect.right - rect.left
            alto = rect.bottom - rect.top
        
        if alto > ancho:
            carpeta_seleccionada = CARPETA_IMAGENES_PORTRAIT
        else:
            carpeta_seleccionada = CARPETA_IMAGENES_NORMALES

        imagenes = obtener_imagenes(carpeta_seleccionada)

        if imagenes:
                vtbl.SetWallpaper(manager, monitor_id, random.choice(imagenes))
        ctypes.windll.ole32.CoTaskMemFree(monitor_id)

# =========================================================
# HILO DE CAMBIO DE FONDO
# =========================================================
def bucle_wallpaper():
    try:
         manager = inicializar_wallpaper_manager()
         cambiar_wallpapars(manager)
         while not stop_event.is_set():
            evento_activado = trigger_event.wait(timeout=intervalo_actual)
            if stop_event.is_set():
                 break
            if evento_activado:
                  trigger_event.clear()
            cambiar_wallpapars(manager)
    except Exception as e:
        print("Error en el hilo de cambio de fondo:", e)
    finally:
            ctypes.windll.ole32.CoUninitialize()

# =========================================================
# FUNCIONES DE LA BARRA DE SISTEMA
# =========================================================
def set_tiempo(segundos):
    def wrapper(icon, item):
        global intervalo_actual
        intervalo_actual = segundos
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
     # Construccion dinamica del submenu de tiempos
    items_tiempo = []
    for texto, segundos in OPCIONES_TIEMPO.items():
        items_tiempo.append(
            pystray.MenuItem(
                texto, 
                set_tiempo(segundos), 
                checked=is_checked(segundos),
                radio=True # Hace que funcionen como botones de radio
            )
        )
    menu = pystray.Menu(
            pystray.MenuItem('Cambiar Ahora', lambda icon, item: trigger_event.set()),
            pystray.MenuItem('Frecuencia', pystray.Menu(*items_tiempo)),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem('Salir', lambda icon, item: [stop_event.set(), trigger_event.set(), icon.stop()])
        )   
    icon = pystray.Icon("WallpaperChanger", crear_icono(), "Wallpaper Changer", menu)
     
    t=threading.Thread(target=bucle_wallpaper, daemon=True)
    t.start()
     
    icon.run()

if __name__ == "__main__":
    if ctypes.sizeof(ctypes.c_voidp) * 8 == 32:
        os._exit(1)
    iniciar_tray_icon()