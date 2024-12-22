@echo off
:: Variables
set PROJECT_NAME=picii-image-viewer
set INSTALL_DIR="C:\Program Files\%PROJECT_NAME%"
set CONTEXT_MENU_NAME=Abrir en Picii Image Viewer

:: Check if the script is running as Administrator
openfiles >nul 2>&1
if %errorlevel% neq 0 (
    echo This script needs to be run as Administrator.
    pause
    exit /b
)

:: Remove the installation directory
if exist %INSTALL_DIR% (
    echo Deleting installation directory...
    rmdir /s /q %INSTALL_DIR%
    if %errorlevel% neq 0 (
        echo Failed to delete the installation directory. Please check permissions or delete it manually.
    ) else (
        echo Installation directory deleted successfully.
    )
) else (
    echo Installation directory not found. Skipping...
)

:: Remove context menu entry from the registry
echo Removing context menu entry...
REG DELETE "HKEY_CLASSES_ROOT\Directory\shell\%CONTEXT_MENU_NAME%" /f
if %errorlevel% neq 0 (
    echo Failed to remove the context menu entry. It may have been deleted already.
) else (
    echo Context menu entry removed successfully.
)

:: Final message
echo The project '%PROJECT_NAME%' has been uninstalled.