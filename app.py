import random
from pynput import keyboard

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
trigger_limit = random.randint(20,50)

def on_press(key):
  global key_count, trigger_limit

  key_count += 1

  if key_count >= trigger_limit:
    print(random.choice(compliments))
    key_count = 0
    trigger_limit = random.randint(20,50)
