import random
import json
import os
from pynput import keyboard
from plyer import notification
from pyfiglet import Figlet
from colorama import init, Fore, Style
init()
colors = [Fore.RED, Fore.BLUE, Fore.YELLOW, Fore.CYAN, Fore.MAGENTA, Fore.WHITE]
import pygetwindow as gw

SETTINGS_FILE = "settings.json"
ACHIEVEMENTS_FILE = "achievements.json"
STATS_FILE = "stats.json"

compliments = [
    "💪 Nice job, champ!",
    "🌟 You're doing great.",
    "🐉 Keep typing, you beast.",
    "😎 That was smooth typing.",
    "⌨️ The keyboard loves you.",
    "⚡ Dang, your fingers are fast.",
    "👑 Code god in the making.",
    "🔥 You're on fire! 🔥",
    "💼 Respect the hustle.",
    "🏆 Typing like a legend."
]

roasts = [
    "💩 Wow, you call that typing?",
    "🫠 I've seen toddlers type faster.",
    "🙃 Is that a typo or your best work?",
    "🐌 Even snails are passing you.",
    "😬 Might wanna reboot your brain.",
    "📉 Productivity just took a nosedive.",
    "🤡 You type like it’s your first day.",
    "⏳ Any slower and we’d time travel.",
    "🛑 Please stop. You're embarrassing us.",
    "🔥 This keyboard deserves better."
]

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)
            return (
                data.get("trigger_limit", random.randint(20, 50)),
                data.get("mode", "popup"),
                data.get("hacker_mode", False),
                data.get("colorful_mode", False),
                data.get("target_app", "All Apps"),
                data.get("self_roast_mode", False)
            )
    else:
        return random.randint(20, 50), "popup", False, False, "All Apps", False

def load_achievements():
    if os.path.exists(ACHIEVEMENTS_FILE):
        with open(ACHIEVEMENTS_FILE, "r") as f:
            return json.load(f)
    else:
        data = {
            "Finger Fury": False
        }
        with open(ACHIEVEMENTS_FILE, "w") as f:
            json.dump(data, f, indent=2)
        return data

def unlock_achievement(name):
    if not achievements.get(name):
        achievements[name] = True
        with open(ACHIEVEMENTS_FILE, "w") as f:
            json.dump(achievements, f, indent=2)

        message = f"🏆 Achievement Unlocked: {name}"
        if compliment_mode == "popup":
            show_popup(message)
        else:
            print(Fore.YELLOW + message + Style.RESET_ALL)

def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as f:
            return json.load(f)
    else:
        data = {
            "total_keys": 0
        }
        with open(STATS_FILE, "w") as f:
            json.dump(data, f, indent=2)
        return data

def on_release(key):
    if key in [keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
        pressed_keys.discard("ctrl")
    elif key in [keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r]:
        pressed_keys.discard("shift")

key_count = 0
compliments_paused = False
trigger_limit, compliment_mode, hacker_mode, colorful_mode, target_app, self_roast_mode = load_settings()
achievements = load_achievements()
stats = load_stats()
pressed_keys = set()

def show_popup(message):
    notification.notify(
        title="Keyboard Compliment",
        message=message,
        timeout=3
    )

def on_press(key):
    global key_count, trigger_limit, compliment_mode, hacker_mode, colorful_mode, target_app, compliments_paused, self_roast_mode

    if key in [keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
      pressed_keys.add("ctrl")
    if key in [keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r]:
      pressed_keys.add("shift")

    # print(f"[KEY PRESSED] {key}")
    # print(f"[MODS] {pressed_keys}")

    # Ctrl + Shift + P to pause
    if (
        hasattr(key, 'char') and key.char == '\x10' and
        "shift" in pressed_keys
    ):
        compliments_paused = not compliments_paused
        state = "paused" if compliments_paused else "resumed"
        print(Fore.CYAN + f"⏸️ Compliments {state}." + Style.RESET_ALL)
        return

    try:
        active_title = gw.getActiveWindowTitle()
    except:
        active_title = None

    if target_app != "All Apps":
        if not active_title or target_app.lower() not in active_title.lower():
            return

    key_count += 1

    stats["total_keys"] += 1
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=2)

    if stats["total_keys"] == 1000:
        # print("🎯 Reached 20 total keys!")
        unlock_achievement("Finger Fury")

    if key_count >= trigger_limit and not compliments_paused:
        compliment = random.choice(roasts if self_roast_mode else compliments)

        if compliment_mode == "popup":
            show_popup(compliment)
        else:
            font = 'slant'
            f = Figlet(font=font)
            art = f.renderText(compliment)

            if hacker_mode:
                print(Fore.GREEN + art + Style.RESET_ALL)
            elif colorful_mode:
                color = random.choice(colors)
                print(color + art + Style.RESET_ALL)
            else:
                print(art)


        key_count = 0
        trigger_limit, compliment_mode, hacker_mode, colorful_mode, target_app, self_roast_mode = load_settings()

def main():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    main()
