import random
from pynput import keyboard
from plyer import notification

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

if __name__ == "__main__":
    main()
