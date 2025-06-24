---
# Lino

## Overview

Lino provides **one unique tray app** as the central hub for launching and controlling all modules like Clipboard Manager, Quick Launcher, etc.
---

## Key Idea

- **Single tray icon** runs in background.
- User presses a **single global shortcut** (e.g., `Ctrl+Space`) to open this tray UI.
- Tray UI shows:

  - Fun messages or jokes
  - Buttons/list for launching modules
  - Shortcut keys info

- After launching a module via tray, the tray UI hides automatically.
- To launch another module or view shortcuts, press shortcut key again.

---

## Benefits

- Keeps system clean with only one tray process.
- No need for multiple tray icons or complicated system integration.
- Easy to maintain and extend modules.
- Fun, interactive, and user-friendly experience.

---

## Functionalities & Shortcut Table

| Functionality            | Description                               | Trigger / Shortcut           |
| ------------------------ | ----------------------------------------- | ---------------------------- |
| Open Lino Tray UI        | Show the central tray window with options | Global Shortcut (Ctrl+Space) |
| Launch Clipboard Manager | Starts Clipboard Manager module           | Click button in Tray UI      |
| Launch Quick Launcher    | Starts Quick Launcher module              | Click button in Tray UI      |
| Show Shortcut Keys       | Display all shortcuts for Lino modules    | Button inside Tray UI        |
| Show Fun Message / Joke  | Shows random jokes or emojis on tray open | On tray open                 |
| Exit Lino                | Quit the entire Lino application          | Button inside Tray UI        |

---

## How It Works

1. **Startup**: Lino tray app launches in background, listens for global shortcut.
2. **Shortcut Pressed**: Tray UI pops up with a welcome message and module buttons.
3. **Module Launch**: User clicks any module button; tray hides and module window shows.
4. **Repeat**: User presses shortcut again to open tray for next action.

---

## Technical Notes

- The tray app manages global shortcut using system-level hooks (e.g., `pynput`).
- Modules run as separate processes or windows, launched on demand.
- Tray UI updates daily with fun messages or emojis to engage users.
- Adding new modules only requires adding buttons to the tray UI.

---

## Next Steps

- Build the tray UI with PyQt5.
- Implement global shortcut listener inside tray app.
- Add buttons and functionality for existing modules.
- Create config for jokes/messages and shortcuts.

---

### 🎯 Shortcut Key Table for Lino Modules

| Module / Action            | Recommended Shortcut | Reason (UX & Safety)                      |
| -------------------------- | -------------------- | ----------------------------------------- |
| 🌐 Open Lino Tray UI       | `Ctrl + Space`       | Comfortable, easy access (like Spotlight) |
| 📋 Clipboard Manager       | `Ctrl + Shift + V`   | Natural for paste-related action          |
| 🚀 Quick Launcher          | `Alt + Space`        | Familiar to users (like GNOME Run)        |
| 🤖 AI Assistant / Chat     | `Ctrl + Shift + A`   | "A" for assistant, rarely conflicts       |
| 📁 File Search Tool        | `Ctrl + Shift + F`   | Standard for find/search                  |
| 🔎 App Search & Run        | `Alt + Shift + R`    | "R" for run, uncommon combo               |
| 🎨 Appearance/Theme Switch | `Ctrl + Shift + T`   | "T" for theme, not used much globally     |
| 🛠️ Settings Panel          | `Ctrl + Shift + S`   | "S" for settings                          |
| 🐧 Pet / LOMY Module       | `Ctrl + Shift + P`   | "P" for pet, easy and playful             |
| ❌ Exit / Quit Lino        | `Ctrl + Shift + Q`   | Standard quit (only from tray UI)         |

---

### 🧠 Tips:

- All combos use `Ctrl+Shift+` or `Alt+Shift+` → avoids OS conflicts.
- Avoid `Ctrl+Alt+...` → often reserved by Linux DEs (like switching workspaces).
- Always let user **customize shortcuts** via config if possible (future feature).
- In your tray UI, you can **show this table** when user clicks “Shortcuts”.

---

<!-- sudo apt install libqt5x11extras5 -->
