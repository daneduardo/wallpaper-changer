@echo off
REM Script para instalar dependencias de Wallpaper Changer
echo.
echo ========================================
echo   Wallpaper Changer - Instalador
echo ========================================
echo.

REM Verificar si Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado o no esta en el PATH
    echo Descarga Python desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [INFO] Actualizando pip...
python -m pip install --upgrade pip setuptools wheel

echo.
echo [INFO] Instalando dependencias...
pip install --only-binary :all: -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ADVERTENCIA] Intento de instalacion alternativa...
    pip install Flask==2.3.3
    pip install pystray==0.19.4
    pip install --upgrade Pillow
)

echo.
echo [EXITO] Instalacion completada
echo.
pause
