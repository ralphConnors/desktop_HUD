from tkinter import *
import os, sys, subprocess
import keyboard
from config_utils import load_config, save_config

hud_process = None
parent_pid = None
toggle_pressed = False

def start_drag(event):
    app._offset_x = event.x_root - app.winfo_x()
    app._offset_y = event.y_root - app.winfo_y()

def do_drag(event):
    app.geometry(f"+{event.x_root - app._offset_x}+{event.y_root - app._offset_y}")

def save_and_reload():
    global hud_process, parent_pid

    new_config = {
        "label_bg": bg_entry.get(),
        "fg_color": fg_entry.get(),
        "light_color": light_entry.get(),
        "font_setting": [font_entry.get(), font_setting[1], font_setting[2]]
    }
    save_config(new_config)
    
    if hud_process and hud_process.poll() is None:
        hud_process.terminate()
        hud_process.wait()
    elif parent_pid:
        try:
            os.kill(parent_pid, 9)
        except Exception:
            pass
        parent_pid = None

    hud_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "keyboard_HUD.py")
    hud_process = subprocess.Popen([sys.executable, hud_path])

def toggle_state():
    global toggle_pressed
    try:
        if keyboard.is_pressed('ctrl') and keyboard.is_pressed('space'):
            if not toggle_pressed:
                if app.winfo_viewable():
                    app.withdraw()
                else:
                    app.deiconify()
                toggle_pressed = True
        else:
            toggle_pressed = False
    except:
        pass
    app.after(50, toggle_state)

config = load_config()
label_bg = config.get("label_bg")
fg_color = config.get("fg_color")
light_color = config.get("light_color")
font_setting = tuple(config.get("font_setting"))
bg_color = "#222222"
gui_color = "#121212"

if len(sys.argv) >= 3:
    initial_pos = f"+{sys.argv[1]}+{sys.argv[2]}"
else:
    initial_pos = "+50+50"

try:
    parent_pid = int(sys.argv[3]) if len(sys.argv) >= 4 else None
except (IndexError, ValueError):
    parent_pid = None

app = Tk()

# Configurations
app.config(bg=bg_color)
app.wm_attributes("-transparentcolor", bg_color)
app.overrideredirect(True)
app.attributes("-topmost", True)
app.geometry(initial_pos)

title = Label(app, text="HUD Configuration", font=font_setting, bg=gui_color, fg=fg_color, padx=14, pady=10)
bg_label = Label(app, text="Background Color", font=font_setting, bg=gui_color, fg=fg_color, padx=14, pady=10)
bg_entry = Entry(app, font=font_setting, bg=gui_color, fg=light_color)
fg_label = Label(app, text="Foreground Color", font=font_setting, bg=gui_color, fg=fg_color, padx=14, pady=10)
fg_entry = Entry(app, font=font_setting, bg=gui_color, fg=light_color)
light_label = Label(app, text="Highlight Color", font=font_setting, bg=gui_color, fg=fg_color, padx=14, pady=10)
light_entry = Entry(app, font=font_setting, bg=gui_color, fg=light_color)
font_label = Label(app, text="Font Name", font=font_setting, bg=gui_color, fg=fg_color, padx=14, pady=10)
font_entry = Entry(app, font=font_setting, bg=gui_color, fg=light_color)
save_button = Button(app, text="SAVE & RELOAD HUD", font=font_setting, bg=gui_color, fg=fg_color, padx=14, pady=10, command=save_and_reload)

for widget, desig, entry_weave in [
    (title, "label", None),
    (bg_label, "label", None),
    (bg_entry, "entry", label_bg),
    (fg_label, "label", None),
    (fg_entry, "entry", fg_color),
    (light_label, "label", None),
    (light_entry, "entry", light_color),
    (font_label, "label", None),
    (font_entry, "entry", font_setting[0]),
    (save_button, "button", None)
]:
    if desig == "entry":
        widget.insert(0, entry_weave)

    widget.pack(expand=True, fill="both", padx=14, pady=10)
    widget.bind("<Button-1>", start_drag)
    widget.bind("<B1-Motion>", do_drag)

toggle_state()
app.bind("<Button-1>", start_drag)
app.bind("<B1-Motion>", do_drag)
app.bind("<Escape>", lambda _: app.destroy())
app.mainloop()