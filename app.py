import random
from pynput import keyboard
from plyer import notification
import json
import tkinter as tk

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

key_count = 0
trigger_limit = random.randint(20, 50)
SETTINGS_FILE = "settings.json"

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
    global key_count, trigger_limit
    key_count += 1

    if key_count >= trigger_limit:
        compliment = random.choice(compliments)
        show_popup(compliment)
        key_count = 0
        trigger_limit = random.randint(20, 50)

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

# Apply button
def apply_settings():
    selected_value = frequency_slider.get()
    print("Apply clicked. Frequency:", selected_value)

apply_btn = tk.Button(root, text="Apply", command=apply_settings)
apply_btn.pack(pady=20)

# Run
root.mainloop()

if __name__ == "__main__":
    main()
