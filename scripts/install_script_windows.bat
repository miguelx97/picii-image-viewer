@echo off
:: Variables
set PROJECT_FOLDER=%cd%
set PROJECT_NAME=picii-image-viewer
set MAIN_SCRIPT=main.py
set INSTALL_DIR="C:\Program Files\%PROJECT_NAME%"
set CONTEXT_MENU_NAME=Abrir en Picii Image Viewer

:: Detect Python dynamically
for /f "delims=" %%i in ('where python') do set PYTHON_PATH=%%i
if not defined PYTHON_PATH (
    echo Python could not be found. Please ensure it is installed and added to your PATH.
    exit /b 1
)

set COMMAND="%PYTHON_PATH%" "%INSTALL_DIR%\%MAIN_SCRIPT%"\" "\"%%1"\"

:: Verificar si el script está siendo ejecutado como administrador
openfiles >nul 2>&1
if %errorlevel% neq 0 (
    echo This script needs to be run as Administrator.
    pause
    exit /b
)

:: Install Python dependencies
pip install -r requirements.txt || (
    echo Failed to install dependencies. Make sure pip is installed and in your PATH.
    exit /b 1
)

:: Verify script is running from the correct directory
if not exist "%PROJECT_FOLDER%\%MAIN_SCRIPT%" (
    echo Error: Please run this script from the '%PROJECT_NAME%' folder containing '%MAIN_SCRIPT%'.
    exit /b 1
)

:: Create the installation directory
if not exist "%INSTALL_DIR%" (
    mkdir %INSTALL_DIR%
)

:: Copy project files to the installation directory
xcopy /s /y %PROJECT_FOLDER% %INSTALL_DIR%

:: Add context menu entry using REG ADD
echo Adding context menu entry...
REG ADD "HKEY_CLASSES_ROOT\Directory\shell\%CONTEXT_MENU_NAME%" /ve /t REG_SZ /f /d "%CONTEXT_MENU_NAME%"
REG ADD "HKEY_CLASSES_ROOT\Directory\shell\%CONTEXT_MENU_NAME%\command" /ve /t REG_SZ /f /d "%COMMAND%"

:: Final message
echo The project '%PROJECT_NAME%' has been installed in %INSTALL_DIR%.
echo A context menu option has been added. You can now right-click on a folder to run the script.