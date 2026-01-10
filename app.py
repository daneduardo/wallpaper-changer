from flask import Flask, render_template, request, jsonify, send_file
import json
import os
import threading
import webbrowser
import time
import logging
import mywallpaperchanger as wpc

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
CONFIG_FILE = "wallpaper_config.json"

def cargar_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error cargando config: {e}")
    
    return {
        'intervalo': 300,
        'carpeta_portrait': wpc.CARPETA_IMAGENES_PORTRAIT,
        'carpeta_normales': wpc.CARPETA_IMAGENES_NORMALES
    }

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@app.route('/')
def index():
    config = cargar_config()
    return render_template('index.html', config=config, opciones=wpc.OPCIONES_TIEMPO)

@app.route('/api/config', methods=['GET'])
def get_config():
    config = cargar_config()
    return jsonify(config)

@app.route('/api/config', methods=['POST'])
def save_config():
    data = request.json
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        
        wpc.intervalo_actual = data['intervalo']
        wpc.CARPETA_IMAGENES_PORTRAIT = data['carpeta_portrait']
        wpc.CARPETA_IMAGENES_NORMALES = data['carpeta_normales']
        wpc.trigger_event.set()
        
        logger.info("Configuración guardada correctamente")
        return jsonify({'success': True, 'message': 'Configuración guardada'})
    except Exception as e:
        logger.error(f"Error guardando config: {e}")
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/cambiar-ahora', methods=['POST'])
def cambiar_ahora():
    try:
        wpc.trigger_event.set()
        logger.info("Cambio de wallpaper iniciado desde web")
        return jsonify({'success': True, 'message': 'Cambio de wallpaper iniciado'})
    except Exception as e:
        logger.error(f"Error en cambiar-ahora: {e}")
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/imagenes/<tipo>', methods=['GET'])
def get_imagenes(tipo):
    try:
        carpeta = wpc.CARPETA_IMAGENES_PORTRAIT if tipo == 'portrait' else wpc.CARPETA_IMAGENES_NORMALES
        imagenes = wpc.obtener_imagenes(carpeta)
        return jsonify({'count': len(imagenes), 'imagenes': [os.path.basename(img) for img in imagenes]})
    except Exception as e:
        logger.error(f"Error obteniendo imágenes: {e}")
        return jsonify({'count': 0, 'imagenes': []}), 400

@app.route('/api/current-wallpaper', methods=['GET'])
def get_current_wallpaper():
    return jsonify(wpc.current_wallpapers)


@app.route('/api/monitors', methods=['GET'])
def get_monitors():
    try:
        count = wpc.obtener_cantidad_monitores()
        return jsonify({'count': int(count)})
    except Exception as e:
        logger.error(f"Error obteniendo monitores: {e}")
        return jsonify({'count': 1}), 500

@app.route('/api/serve-image', methods=['GET'])
def serve_image():
    path = request.args.get('path')
    if not path:
        return "No path provided", 400
    
    # Basic security check: ensure file exists
    if os.path.exists(path) and os.path.isfile(path):
        return send_file(path)
    
    return "File not found", 404

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    logger.error(f"Server error: {error}")
    return jsonify({'error': 'Server error'}), 500

def open_browser():
    """Abre el navegador después de que el servidor esté listo"""
    time.sleep(2)  # Espera a que Flask se inicie
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    # Verificar que el directorio de templates existe
    if not os.path.exists('templates'):
        logger.error("ERROR: Carpeta 'templates' no encontrada")
        logger.info("Crea la carpeta: templates/")
        logger.info("Y coloca index.html dentro")
        exit(1)
    
    # Crear carpeta static si no existe
    if not os.path.exists('static'):
        os.makedirs('static')

    # Cargar configuración y arrancar el bucle de wallpaper
    wpc.cargar_configuracion()
    wallpaper_thread = threading.Thread(target=wpc.bucle_wallpaper, daemon=True)
    wallpaper_thread.start()
    
    # Iniciar hilo para abrir navegador
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    logger.info("=" * 50)
    logger.info("🌐 Wallpaper Changer Web Interface")
    logger.info("=" * 50)
    logger.info("Abriendo navegador en: http://127.0.0.1:5000")
    logger.info("Presiona CTRL+C para detener el servidor")
    logger.info("=" * 50)
    
    try:
        app.run(debug=False, host='127.0.0.1', port=5000, use_reloader=False)
    except KeyboardInterrupt:
        logger.info("Servidor detenido")
