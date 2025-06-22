# 📋 Lino - Clipboard Manager for Linux

**Lino** is a lightweight, native clipboard manager designed for Linux desktops.  
Inspired by [PowerToys Clipboard History], Lino helps you store, search, and reuse copied text with ease.

---

## ✨ Features

- 📌 Stores clipboard history (up to 20 items)
- 🔍 Live search for copied items
- 💬 One-click to copy from history
- 🖼️ Beautiful Qt-based GUI
- 🖥️ System tray integration
- 🚪 Exit from tray menu

---

## 📸 Preview

> ![Preview Screenshot](assets/lino_clipboard_demo.gif)

---

## 🚀 How to Run

### 1. Clone and set up

```bash
git clone git@github.com:Bugsfounder/lino.git
cd lino
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

---

### Bugs to Fix:

- on history panel, when click on already copied item, the again append it and note remove the clicked item.
