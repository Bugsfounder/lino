# Lino AppImage Build Guide

## Project Structure

## 🔧 Build Steps

### 1. Build PyInstaller Binary

Run this from the **project root**:

```bash
pyinstaller --onefile manager/main.py -n lino \
--add-data="manager/mood:mood" \
--add-data="clipboard:clipboard" \
--add-data="quick_launcher:quick_launcher" \
--add-data="logger:logger"
```

2.  Copy Binary to AppDir

```
    cp dist/lino AppDir/usr/bin/lino
    chmod +x AppDir/usr/bin/lino
```

3.  Build AppImage

```
    appimage-builder --recipe AppImageBuilder.yml
```

4.  Run the AppImage

````
    ./Lino-1.0.0-x86_64.AppImage
    ```
````
