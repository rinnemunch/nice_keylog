from collections import deque
import sys
import time
import pygame
from datetime import datetime
import pygetwindow as gw
import random
import json
import os
from pynput import keyboard
from plyer import notification
from pyfiglet import Figlet
from colorama import init, Fore, Style
init()
colors = [Fore.RED, Fore.BLUE, Fore.YELLOW,
          Fore.CYAN, Fore.MAGENTA, Fore.WHITE]

recent_keys = deque(maxlen=100)
start_time = time.time()

SETTINGS_FILE = "settings.json"
ACHIEVEMENTS_FILE = "achievements.json"
STATS_FILE = "stats.json"
DAILY_STATS_FILE = "daily_stats.json"
WORD_STATS_FILE = "top_words.json"

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

pygame.mixer.init()


def play_sound():
    try:
        pygame.mixer.Sound("chime.wav").play()
    except Exception as e:
        print(Fore.RED + f"[Sound Error] {e}" + Style.RESET_ALL)


def get_keys_per_minute():
    now = time.time()
    one_minute_ago = now - 60

    recent = [t for t in recent_keys if t >= one_minute_ago]
    return len(recent)


def animate_text(text, delay=0.05, color=Fore.CYAN):
    lines = text.splitlines()
    for i in range(1, len(lines) + 1):
        print(color + "\n".join(lines[:i]) + Style.RESET_ALL)
        time.sleep(delay)


def animate_sparkle_text(text, delay=0.05, base_color=Fore.CYAN):
    sparkle = ['✨', '★', '*', '•']
    for line in text.splitlines():
        shine = random.choice(sparkle)
        print(base_color + line + " " + shine + Style.RESET_ALL)
        time.sleep(delay)

    print(Style.RESET_ALL)


def animate_figlet(text, delay=0.03, color=Fore.CYAN):
    f = Figlet(font='slant')
    lines = f.renderText(text).splitlines()
    for line in lines:
        print(color + line + Style.RESET_ALL)
        time.sleep(delay)


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
                data.get("self_roast_mode", False),
                data.get("time_mode", True)
            )
    else:
        return random.randint(20, 50), "popup", False, False, "All Apps", False, True


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
            data = json.load(f)
    else:
        data = {}

    data.setdefault("total_keys", 0)
    data.setdefault("streak", 0)
    return data


def load_daily_stats():
    today = datetime.now().strftime("%Y-%m-%d")

    if os.path.exists(DAILY_STATS_FILE):
        with open(DAILY_STATS_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {}

    if today not in data:
        data[today] = 0

    return data, today


def on_release(key):
    if key in [keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
        pressed_keys.discard("ctrl")
    elif key in [keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r]:
        pressed_keys.discard("shift")


key_count = 0
compliments_paused = False
trigger_limit, compliment_mode, hacker_mode, colorful_mode, target_app, self_roast_mode, time_mode = load_settings()
achievements = load_achievements()
stats = load_stats()
daily_stats, current_date = load_daily_stats()
pressed_keys = set()

current_word = ""
word_stats = {}

if os.path.exists(WORD_STATS_FILE):
    with open(WORD_STATS_FILE, "r") as f:
        word_stats = json.load(f)


def show_popup(message):
    notification.notify(
        title="Keyboard Compliment",
        message=message,
        timeout=3
    )


def get_time_based_compliment(roast_mode=False):
    hour = datetime.now().hour

    if roast_mode:
        if 0 <= hour < 3:
            return "🦉 Even the bugs are asleep. What’s your excuse?"
        elif 3 <= hour < 6:
            return "💀 This code’s haunting the night... and not in a good way."
        elif 6 <= hour < 9:
            return "☕ Hope that coffee fixes your spaghetti logic."
        elif 9 <= hour < 12:
            return "📉 Morning errors already? Impressive."
        elif 12 <= hour < 17:
            return "💼 Peak hours, yet here we are debugging nonsense."
        elif 17 <= hour < 21:
            return "🌇 That sunset won’t clean your code."
        else:
            return "🌙 Night mode engaged... unfortunately, so is your typos."
    else:
        if 0 <= hour < 3:
            return "🦇 Night owl mode: Grind god."
        elif 3 <= hour < 6:
            return "🌌 Coding through the void... respect."
        elif 6 <= hour < 9:
            return "🌅 Early bird getting those keys."
        elif 9 <= hour < 12:
            return "☕ Morning flow. You’re dialed in."
        elif 12 <= hour < 17:
            return "💼 Prime productivity hours. Keep it up!"
        elif 17 <= hour < 21:
            return "🌇 Evening warrior mode activated."
        else:
            return "🌙 Late night legend at work."


def on_press(key):
    global key_count, trigger_limit, compliment_mode, hacker_mode, colorful_mode, target_app, compliments_paused, self_roast_mode, time_mode, current_date, current_word, word_stats

    new_date = datetime.now().strftime("%Y-%m-%d")
    if new_date != current_date:
        print(
            Fore.CYAN + f"📊 {current_date} Summary: {daily_stats[current_date]} keys pressed." + Style.RESET_ALL)

        daily_stats[new_date] = 0
        with open(DAILY_STATS_FILE, "w") as f:
            json.dump(daily_stats, f, indent=2)

        current_date = new_date

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
        # print(Fore.CYAN + f"⏸️ Compliments {state}." + Style.RESET_ALL)
        # return

    try:
        active_title = gw.getActiveWindowTitle()
    except:
        active_title = None

    if target_app != "All Apps":
        if not active_title or target_app.lower() not in active_title.lower():
            return

    key_count += 1

    recent_keys.append(time.time())
    kpm = get_keys_per_minute()

    try:
        if hasattr(key, 'char') and key.char.isalnum():
            current_word += key.char.lower()
        elif key in (keyboard.Key.space, keyboard.Key.enter):
            print(f"[DEBUG] Word completed: '{current_word}'")
            if 2 < len(current_word) < 20 and current_word not in ["the", "and", "for"]:
                word_stats[current_word] = word_stats.get(current_word, 0) + 1
                with open(WORD_STATS_FILE, "w") as f:
                    json.dump(word_stats, f, indent=2)
                print(
                    f"[DEBUG] Logged '{current_word}' → count {word_stats[current_word]}")
            current_word = ""
    except:
        pass

    # print(f"[KEY COUNT] {key_count} / {trigger_limit}")

    stats["total_keys"] += 1
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=2)

    daily_stats[current_date] += 1
    with open(DAILY_STATS_FILE, "w") as f:
        json.dump(daily_stats, f, indent=2)

    if stats["total_keys"] == 1000:
        # print("🎯 Reached 20 total keys!")
        unlock_achievement("Finger Fury")

    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=2)

    if key_count >= trigger_limit:
        if compliments_paused or (target_app != "All Apps" and (not active_title or target_app.lower() not in active_title.lower())):
            if stats["streak"] > 0:
                print(
                    Fore.RED + f"💤 Streak broken at {stats['streak']}!" + Style.RESET_ALL)
                stats["streak"] = 0
                with open(STATS_FILE, "w") as f:
                    json.dump(stats, f, indent=2)
            key_count = 0
            return

        stats["streak"] += 1
        print(Fore.GREEN + f"🔥 Streak: {stats['streak']}" + Style.RESET_ALL)

        if stats["streak"] == 5:
            unlock_achievement("Compliment Combo")

        if self_roast_mode:
            if kpm < 20:
                compliment = "🐢 You typing or summoning a snail?"
            elif kpm < 40:
                compliment = "💤 Wake those fingers up!"
            else:
                compliment = random.choice(roasts)
        else:
            if kpm >= 120:
                compliment = "🚀 Slow down, turbo fingers!"
            elif kpm >= 90:
                compliment = "🔥 You’re melting the keyboard!"
            elif kpm >= 60:
                compliment = "⚡ You type like a machine!"
            else:
                compliment = random.choice(compliments)

        if time_mode and random.random() < 0.5:
            compliment += f"\n{get_time_based_compliment(self_roast_mode)}"
            print(Fore.MAGENTA +
                  "[🕒 Time-based compliment triggered]" + Style.RESET_ALL)

        play_sound()

        if compliment_mode == "popup":
            show_popup(compliment)
        else:
            animate_figlet(
                compliment,
                delay=0.05,
                color=random.choice(colors)
            )

        key_count = 0
        # trigger_limit, compliment_mode, hacker_mode, colorful_mode, target_app, self_roast_mode, time_mode = load_settings()


def main():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    main()
