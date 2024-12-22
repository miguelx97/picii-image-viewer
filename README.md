# Picii Image Viewer

This project is a utility that allows you to view images in a selected folder by running a Python script directly from the Nautilus file manager context menu.

---

## Requirements

- **Python 3** installed on your system.
- if you use linux: **Nautilus** file manager (GNOME).

---

## Installation

### Step 1: Clone the repository

Clone the project from your preferred version control system or download it as a compressed file and extract it.

```bash
git clone https://github.com/miguelx97/picii-image-viewer.git
cd picii-image-viewer
```

### Step 2: Make the installation script executable (Linux)

Navigate to the project directory and ensure that the `install_script.sh` file is executable:

```bash
chmod +x scripts/install_script_linux.sh
```

### Step 3: Run the installation script

Run the installation script to set up the utility:

Linux:

```bash
sh scripts/install_script_linux.sh
```

Windows:

```bash
./scripts/install_script_windows.sh
```

### Step 4: Restart Nautilus (Linux)

After installation, restart Nautilus to apply the changes:

```bash
nautilus -q
```

---

## Usage

### Run the script from the context menu

1. Open the Nautilus file manager.
2. Right-click on any folder.
3. From the context menu, select **Scripts > RunPiciiImageViewer**.
4. The Python script will run and process the selected folder.

---

## Project Structure

The installation script will only copy the following elements:

- `main.py`: The main project file.
- `app/`: Contains the core logic for the project.
- `assets/`: Holds additional resources needed for execution.

---

## Uninstallation

If you want to remove the script and its integration run the uninstall script:

Linux

```bash
sh scripts/uninstall_script_linux.sh
```

Windows:

```bash
./scripts/install_script_windows.sh
```

---

## Contributions

If you have suggestions or encounter any issues, feel free to create an **issue** or submit a **pull request**.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.

## Technologies:

Python
Kivy (UI)
FileChooserIconView (File explorer)
Pickle (Persistence)

## Testing:

```
python3 main.py
```

OR

```
start.sh
```
