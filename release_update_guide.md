# Lino AppImage Packaging & Release Guide

This document helps you revisit and remember the complete process of building and releasing your `Lino` app as an AppImage, including how to prepare for future versions.

---

## ✅ Project Structure

directory looks like:

```
LINO/
├── AppDir/
│   └── usr/bin/lino   (Python entrypoint script)
├── clipboard/         (Your app source)
├── AppImageBuilder.yml
├── README.md
├── env/               (Python virtual environment)
```

---

## ✅ 1. Create Python Entrypoint

Your entry Python file should be like this:

```bash
AppDir/usr/bin/lino
```

With content:

```python
#!/usr/bin/env python3
from clipboard.main import main
main()
```

Make it executable:

```bash
chmod +x AppDir/usr/bin/lino
```

---

## ✅ 2. Sample AppImageBuilder.yml

```yaml
version: 1

AppDir:
  path: ./AppDir
  app_info:
    id: com.bugsfounder.lino
    name: Lino
    icon: lino
    version: "1.0.0"
    exec: usr/bin/lino
  apt:
    arch: amd64
    sources:
      - sourceline: deb http://deb.debian.org/debian bookworm main
    include:
      - libqt5gui5
      - libqt5core5a
      - libqt5widgets5
      - python3
      - python3-pyqt5
  files:
    include: []
    exclude: []

AppImage:
  arch: x86_64
  update-information: "gh-releases-zsync|bugsfounder|lino|latest|*.AppImage.zsync"
```

---

## ✅ 3. Build AppImage

Run these commands from project root:

```bash
# Activate env if not already
source env/bin/activate

# Build
appimage-builder --recipe AppImageBuilder.yml
```

> If version error comes, use:

```bash
export APPIMAGE_BUILDER_SKIP_APT_VERSION_CHECK=1
```

After successful build, you’ll get:

```
Lino-x86_64.AppImage
Lino-x86_64.AppImage.zsync (optional)
```

---

## ✅ 4. GitHub Release Upload

1. Push code to GitHub.
2. Go to **Releases** → **Draft new release**
3. Fill:

   - Tag: `v1.0.0`
   - Title: `Lino v1.0.0`
   - Description (optional)

4. Attach:

   - `.AppImage`
   - `.AppImage.zsync` (for updates)

5. Click **"Publish Release"**.

---

## ✅ 5. .gitignore (important!)

Add these:

```
__pycache__/
*.pyc
.env
env/
*.AppImage
*.zsync
AppDir/
```

---

## 🔁 Future Versions (v1.1.0, v2.0 etc)

1. Update version in `AppImageBuilder.yml`
2. Rebuild AppImage
3. Create a new GitHub release with tag `v1.1.0`, and repeat upload steps.

---

## 🔧 Troubleshooting

- `InvalidVersion '1.22.6ubuntu6'`: Use `APPIMAGE_BUILDER_SKIP_APT_VERSION_CHECK=1`
- `Main executable is not an elf`: Ensure entry script is Python and marked executable
- `zsyncmake not found`: Install it with `sudo apt install zsync`

---

## 📌 Extra Notes

- You don’t need to include system scripts like `init.d`, `pam`, etc. Clean AppDir if needed.
- Only include your own app binary & minimal dependencies.
- Always test `.AppImage` before uploading.

---

## ❤️ Final Tip

Keep this doc saved and version-controlled in your project (e.g. `RELEASE_GUIDE.md`) so future you (or team) never forgets the process.

---

<!-- sudo apt install zsync -->
