@echo off
REM Script para iniciar el servidor web de Wallpaper Changer
setlocal enabledelayedexpansion

echo.
echo ========================================
echo   Wallpaper Changer - Web Interface
echo ========================================
echo.

REM Verificar si Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado o no esta en el PATH
    pause
    exit /b 1
)

REM Verificar si el archivo app.py existe
if not exist "app.py" (
    echo [ERROR] app.py no encontrado en la carpeta actual
    echo Asegurate de ejecutar este script desde la carpeta del proyecto
    pause
    exit /b 1
)

REM Verificar si la carpeta templates existe
if not exist "templates" (
    echo [ERROR] Carpeta 'templates' no encontrada
    echo Crea la carpeta y coloca index.html dentro
    pause
    exit /b 1
)

REM Verificar si Flask esta instalado
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo [ADVERTENCIA] Flask no esta instalado
    echo Instalando dependencias...
    pip install Flask
)

echo [INFO] Iniciando servidor web...
echo.
echo El navegador se abrira automaticamente en: http://127.0.0.1:5000
echo.
echo Presiona CTRL+C para detener el servidor
echo.
timeout /t 2

python app.py

pause
