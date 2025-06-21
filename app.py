import random
from pynput import keyboard
from plyer import notification
import json
import tkinter as tk
import os

SETTINGS_FILE = "settings.json"

compliments = [
    "Nice job, champ!",
    "You're doing great.",
    "Keep typing, you beast.",
    "That was smooth typing.",
    "The keyboard loves you.",
    "Dang, your fingers are fast.",
    "Code god in the making.",
    "You're on fire!",
    "Respect the hustle.",
    "Typing like a legend."
]

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)
            return (
                data.get("trigger_limit", random.randint(20, 50)),
                data.get("mode", "popup")
            )
    else:
        return random.randint(20, 50), "popup"


key_count = 0
trigger_limit, compliment_mode = load_settings()

# JSON
def apply_settings():
    selected_value = frequency_slider.get()
    settings = {
        "trigger_limit": selected_value
    }
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)
    print(f"Saved trigger_limit: {selected_value}")

def show_popup(message):
    notification.notify(
        title="Keyboard Compliment",
        message=message,
        timeout=3  # number of seconds
    )

def on_press(key):
    global key_count, trigger_limit, compliment_mode
    key_count += 1

    if key_count >= trigger_limit:
        compliment = random.choice(compliments)

        if compliment_mode == "popup":
            show_popup(compliment)
        else:
            print(compliment)

        key_count = 0
        trigger_limit, compliment_mode = load_settings()


def main():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# Main window
root = tk.Tk()
root.title("Keylogger Settings")
root.geometry("300x200")

# Frequency
label = tk.Label(root, text="Compliment Frequency (keystrokes):")
label.pack(pady=10)

# Slider
frequency_slider = tk.Scale(root, from_=10, to=100, orient=tk.HORIZONTAL)
frequency_slider.set(30)  # Default value
frequency_slider.pack()

# Mode toggle
mode_var = tk.StringVar(value="popup")  # default

mode_label = tk.Label(root, text="Compliment Mode:")
mode_label.pack()

mode_options = [("Pop-up", "popup"), ("Terminal", "terminal")]
for text, value in mode_options:
    tk.Radiobutton(root, text=text, variable=mode_var, value=value).pack()

# Apply button
def apply_settings():
    selected_value = frequency_slider.get()
    selected_mode = mode_var.get()

    settings = {
        "trigger_limit": selected_value,
        "mode": selected_mode
    }

    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)

    print(f"Saved settings: {settings}")


# Run
root.mainloop()

if __name__ == "__main__":
    main()
