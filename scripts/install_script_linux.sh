#!/bin/bash

# Variables
PROJECT_FOLDER="$(pwd)"
PROJECT_NAME="picii-image-viewer"
MAIN_SCRIPT="main.py"
INSTALL_DIR="$HOME/.local/share/$PROJECT_NAME"
ACTION_FILE="$HOME/.local/share/nautilus/scripts/RunPiciiImageViewer"

# Verificar si el script se ejecuta desde la carpeta correcta
if [ ! -f "$PROJECT_FOLDER/$MAIN_SCRIPT" ]; then
    echo "Error: Ejecuta este script desde la carpeta '$PROJECT_NAME' que contiene '$MAIN_SCRIPT'."
    exit 1
fi

# Crear el directorio de instalación si no existe
mkdir -p "$INSTALL_DIR"

# Copiar la carpeta del proyecto al directorio de instalación
cp "$PROJECT_FOLDER/$MAIN_SCRIPT" "$INSTALL_DIR/"
cp -r "$PROJECT_FOLDER/app" "$INSTALL_DIR/"
cp -r "$PROJECT_FOLDER/assets" "$INSTALL_DIR/"
chmod -R +x "$INSTALL_DIR"
echo "El proyecto '$PROJECT_NAME' se instaló en $INSTALL_DIR"

# Crear la acción para el menú contextual
mkdir -p "$(dirname "$ACTION_FILE")"
cat << EOF > "$ACTION_FILE"
#!/bin/bash
python3 "$INSTALL_DIR/$MAIN_SCRIPT" "\$1"
EOF
chmod +x "$ACTION_FILE"

# Mensaje final
echo "La acción ha sido añadida al menú contextual. Reinicia Nautilus para aplicar los cambios."
