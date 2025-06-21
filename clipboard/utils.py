import keyboard
import pyperclip as clipboard
import time

history = []
MAX_HISTORY = 20
show_gui_flag = False


def clipboard_manager():
    global show_gui_flag, history
    last_clipboard_content = ""
    while True:
        try:
            if keyboard.is_pressed("ctrl") and keyboard.is_pressed("c"):
                time.sleep(0.1)
                current_content = clipboard.paste()

                if current_content and current_content != last_clipboard_content:
                    last_clipboard_content = current_content
                    if not history or history[-1] != current_content:
                        if len(history) >= MAX_HISTORY:
                            history.pop(0)
                        history.append(current_content)
                        print(f"[Copied] {current_content[:80]}")

                while keyboard.is_pressed("c") or keyboard.is_pressed("ctrl"):
                    time.sleep(0.01)

            elif (
                keyboard.is_pressed("ctrl")
                and keyboard.is_pressed("shift")
                and keyboard.is_pressed("v")
            ):
                show_gui_flag = True
                while (
                    keyboard.is_pressed("v")
                    or keyboard.is_pressed("shift")
                    or keyboard.is_pressed("ctrl")
                ):
                    time.sleep(0.01)

            time.sleep(0.05)

        except Exception as e:
            print(f"\nError: {e}")
            time.sleep(1)
