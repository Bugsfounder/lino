import keyboard
import pyperclip as clipboard
import time
import threading
from queue import Queue

history = []
MAX_HISTORY = 20
clipboard_queue = Queue()


def safe_clipboard_access():
    """Safely access clipboard with retries and error handling"""
    for _ in range(3):  # Try up to 3 times
        try:
            return clipboard.paste()
        except Exception as e:
            print(f"Clipboard access error: {e}")
            time.sleep(0.1)
    return ""


def clipboard_manager():
    last_clipboard_content = ""
    while True:
        try:
            # Check for Ctrl+C (copy)
            if keyboard.is_pressed("ctrl") and keyboard.is_pressed("c"):
                time.sleep(0.1)  # Allow copy to complete
                current_content = safe_clipboard_access()

                if current_content and current_content != last_clipboard_content:
                    print(
                        f"\nCopied: {current_content[:100]}{'...' if len(current_content) > 100 else ''}"
                    )
                    last_clipboard_content = current_content

                    # Update history
                    if not history or history[-1] != current_content:
                        if len(history) >= MAX_HISTORY:
                            history.pop(0)
                        history.append(current_content)

                # Wait until keys are released
                while keyboard.is_pressed("c") or keyboard.is_pressed("ctrl"):
                    time.sleep(0.01)

            # Check for Ctrl+V (paste)
            elif (
                keyboard.is_pressed("ctrl")
                and keyboard.is_pressed("v")
                and not keyboard.is_pressed("shift")
            ):
                if last_clipboard_content:
                    print(f"\nPasting last copied item")
                else:
                    print("\nClipboard empty")

                while keyboard.is_pressed("v") or keyboard.is_pressed("ctrl"):
                    time.sleep(0.01)

            # Check for Ctrl+Shift+V (history)
            elif (
                keyboard.is_pressed("ctrl")
                and keyboard.is_pressed("shift")
                and keyboard.is_pressed("v")
            ):
                print("\n=== Clipboard History (Ctrl+Shift+V) ===")
                for i, item in enumerate(reversed(history), 1):
                    print(f"{i}. {item[:100]}{'...' if len(item) > 100 else ''}")
                print("=" * 50)

                while (
                    keyboard.is_pressed("v")
                    or keyboard.is_pressed("shift")
                    or keyboard.is_pressed("ctrl")
                ):
                    time.sleep(0.01)

            # Check for Win+V
            elif keyboard.is_pressed("win") and keyboard.is_pressed("v"):
                print("\n[Win+V pressed - Windows clipboard history]")
                while keyboard.is_pressed("v") or keyboard.is_pressed("win"):
                    time.sleep(0.01)

            time.sleep(0.01)

        except Exception as e:
            print(f"\nError in clipboard manager: {e}")
            time.sleep(1)


def main():
    print("Clipboard Manager Started")
    print("Shortcuts:")
    print("Ctrl+C - Copy to history")
    print("Ctrl+V - Paste last item")
    print("Ctrl+Shift+V - Show history (newest first)")
    print("Win+V - System clipboard history")
    print("Press Ctrl+C in terminal to exit\n")

    # Start manager thread
    manager_thread = threading.Thread(target=clipboard_manager, daemon=True)
    manager_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down clipboard manager...")
        # Give thread time to clean up
        time.sleep(0.5)


if __name__ == "__main__":
    main()
