import tkinter as tk
import json

SETTINGS_FILE = "settings.json"


def apply_settings():
    try:
        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)
    except FileNotFoundError:
        settings = {}

    settings["trigger_limit"] = frequency_slider.get()
    settings["mode"] = mode_var.get()
    settings["hacker_mode"] = hacker_mode_var.get()
    settings["colorful_mode"] = colorful_mode_var.get()
    settings["target_app"] = app_var.get()
    settings["self_roast_mode"] = self_roast_var.get()
    settings["use_custom_compliments"] = use_custom_compliments_var.get()
    settings["quote_mode"] = quote_mode_var.get()
    settings["autostart"] = autostart_var.get()
    settings["speak_compliment"] = speak_compliment_var.get()

    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)

    print(f"Saved settings: {settings}")


# GUI
root = tk.Tk()
root.title("Keylogger Settings")
root.geometry("600x600")

autostart_var = tk.BooleanVar(value=False)
tk.Checkbutton(root, text="Start on Boot", variable=autostart_var).pack()

speak_compliment_var = tk.BooleanVar(value=False)
tk.Checkbutton(root, text="Speak Compliments Out Loud",
               variable=speak_compliment_var).pack()

hacker_mode_var = tk.BooleanVar(value=False)
tk.Checkbutton(root, text="Enable Hacker Mode",
               variable=hacker_mode_var).pack()

colorful_mode_var = tk.BooleanVar(value=False)
tk.Checkbutton(root, text="Enable Colorful Mode",
               variable=colorful_mode_var).pack()

self_roast_var = tk.BooleanVar(value=False)
tk.Checkbutton(root, text="Enable Self-Roast Mode",
               variable=self_roast_var).pack()

use_custom_compliments_var = tk.BooleanVar(value=False)
tk.Checkbutton(root, text="Use Custom Compliment File",
               variable=use_custom_compliments_var).pack()

quote_mode_var = tk.BooleanVar(value=False)
tk.Checkbutton(root, text="Use Online Quotes Instead of Compliments",
               variable=quote_mode_var).pack()

label = tk.Label(root, text="Compliment Frequency (keystrokes):")
label.pack(pady=10)

frequency_slider = tk.Scale(root, from_=10, to=100, orient=tk.HORIZONTAL)
frequency_slider.set(30)
frequency_slider.pack()

mode_var = tk.StringVar(value="popup")
mode_label = tk.Label(root, text="Compliment Mode:")
mode_label.pack()

app_label = tk.Label(root, text="Track In App:")
app_label.pack(pady=10)

app_var = tk.StringVar(value="All Apps")
app_choices = ["All Apps", "Notepad", "Visual Studio Code"]
app_dropdown = tk.OptionMenu(root, app_var, *app_choices)
app_dropdown.pack()

mode_options = [("Pop-up", "popup"), ("Terminal", "terminal")]
for text, value in mode_options:
    tk.Radiobutton(root, text=text, variable=mode_var, value=value).pack()

apply_btn = tk.Button(root, text="Apply", command=apply_settings)
apply_btn.pack(pady=20)

root.mainloop()
