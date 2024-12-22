@echo off

REM Variables
set PROJECT_FOLDER=%~dp0
set PROJECT_NAME=picii-image-viewer
set MAIN_SCRIPT=main.py
set INSTALL_DIR=%USERPROFILE%\AppData\Local\%PROJECT_NAME%
set CONTEXT_MENU_SCRIPT="%USERPROFILE%\AppData\Local\%PROJECT_NAME%\run_picii_image_viewer.ps1"

REM Install dependencies
pip install -r requirements.txt

REM Verificar si el script se ejecuta desde la carpeta correcta
if not exist "%PROJECT_FOLDER%%MAIN_SCRIPT%" (
    echo Error: Ejecuta este script desde la carpeta '%PROJECT_NAME%' que contiene '%MAIN_SCRIPT%'.
    exit /b 1
)

REM Crear el directorio de instalación si no existe
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
)

REM Copiar los archivos necesarios al directorio de instalación
xcopy "%PROJECT_FOLDER%%MAIN_SCRIPT%" "%INSTALL_DIR%" /Y
xcopy "%PROJECT_FOLDER%app" "%INSTALL_DIR%\app" /E /Y
xcopy "%PROJECT_FOLDER%assets" "%INSTALL_DIR%\assets" /E /Y
echo El proyecto '%PROJECT_NAME%' se instaló en %INSTALL_DIR%.

REM Crear el script de PowerShell para ejecutar el proyecto
echo @echo off > "%CONTEXT_MENU_SCRIPT%"
echo powershell.exe -NoProfile -ExecutionPolicy Bypass -Command ^\"& { python \"%INSTALL_DIR%\%MAIN_SCRIPT%\" '%%1' }^\" >> "%CONTEXT_MENU_SCRIPT%"
attrib +R +S +H "%CONTEXT_MENU_SCRIPT%"

REM Agregar entrada al menú contextual de Windows
powershell -Command "Set-ItemProperty -Path 'HKCU:\\Software\\Classes\\Directory\\Background\\shell\\RunPiciiImageViewer' -Name '(default)' -Value 'Run Picii Image Viewer'"
powershell -Command "New-Item -Path 'HKCU:\\Software\\Classes\\Directory\\Background\\shell\\RunPiciiImageViewer\\command' -Value '\"%CONTEXT_MENU_SCRIPT%\" \"%V\"'"

REM Mensaje final
echo La acción ha sido añadida al menú contextual. Ahora puedes usarla haciendo clic derecho en cualquier carpeta.
pause
