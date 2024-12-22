@echo off

REM Variables
set PROJECT_NAME=picii-image-viewer
set INSTALL_DIR=%USERPROFILE%\AppData\Local\%PROJECT_NAME%
set CONTEXT_MENU_SCRIPT="%USERPROFILE%\AppData\Local\%PROJECT_NAME%\run_picii_image_viewer.ps1"

REM Confirmación del usuario
echo Este script eliminará todos los archivos relacionados con %PROJECT_NAME%.
set /p confirm="¿Estás seguro de que deseas continuar? (y/n): "
if /i not "%confirm%"=="y" (
    echo Desinstalación cancelada.
    exit /b 0
)

REM Eliminar el directorio de instalación
if exist "%INSTALL_DIR%" (
    rmdir /S /Q "%INSTALL_DIR%"
    echo Directorio %INSTALL_DIR% eliminado.
) else (
    echo El directorio %INSTALL_DIR% no existe.
)

REM Eliminar la entrada del menú contextual
echo Eliminando la entrada del menú contextual...
powershell -Command "Remove-Item -Path 'HKCU:\\Software\\Classes\\Directory\\Background\\shell\\RunPiciiImageViewer' -Recurse -ErrorAction SilentlyContinue"
if %errorlevel% equ 0 (
    echo Entrada del menú contextual eliminada.
) else (
    echo No se encontró la entrada del menú contextual.
)

REM Mensaje final
echo %PROJECT_NAME% ha sido completamente desinstalado.
pause
