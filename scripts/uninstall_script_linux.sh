#!/bin/bash

# Variables
PROJECT_NAME="picii-image-viewer"
INSTALL_DIR="$HOME/.local/share/$PROJECT_NAME"
ACTION_FILE="$HOME/.local/share/nautilus/scripts/RunPiciiImageViewer"

# Confirmación del usuario
echo "Este script eliminará todos los archivos relacionados con $PROJECT_NAME."
read -p "¿Estás seguro de que deseas continuar? (y/n): " confirm

if [[ "$confirm" != "y" ]]; then
    echo "Desinstalación cancelada."
    exit 0
fi

# Eliminar el directorio de instalación
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "Directorio $INSTALL_DIR eliminado."
else
    echo "El directorio $INSTALL_DIR no existe."
fi

# Eliminar el archivo del menú contextual
if [ -f "$ACTION_FILE" ]; then
    rm -f "$ACTION_FILE"
    echo "Archivo $ACTION_FILE eliminado."
else
    echo "El archivo $ACTION_FILE no existe."
fi

# Reiniciar Nautilus para aplicar los cambios
echo "Reiniciando Nautilus..."
nautilus -q

# Mensaje final
echo "$PROJECT_NAME ha sido completamente desinstalado."
