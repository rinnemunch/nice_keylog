import random
import json
import os
from pynput import keyboard
from plyer import notification

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

def show_popup(message):
    notification.notify(
        title="Keyboard Compliment",
        message=message,
        timeout=3
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

if __name__ == "__main__":
    main()
