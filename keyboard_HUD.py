from tkinter import *
from pynput import mouse
import keyboard
import subprocess, os, sys
from config_utils import load_config

# keysets

keyset_1 = [ # MAIN SET
    ("W", "w", 0 ,2),
    ("A", "a", 1, 1),
    ("S", "s", 1, 2),
    ("D", "d", 1, 3),
    ("C", "c", 2, 2),
    ("E", "e", 0, 3),
    ("F", "f", 1, 4)
]

keyset_2 = [ # SECOND SET
    ("Alt", "alt", 0, 0),
    ("     Space     ", "space", 0, 1)
]

keyset_3 = [ # THIRD SET
    ("Shift", "shift", 0, 0),
    ("Ctrl", "ctrl", 1, 0)
]

keyset_4 = [ # MOUSE SET
    ("LMB", mouse.Button.left),
    ("RMB", mouse.Button.right)

]

key_label = []
mouse_label = []
mouse_state = {mouse.Button.left: False, mouse.Button.right: False}
toggle_pressed = False # CTRL+ALT+SHIFT
config_toggle_pressed = False # CTRL+ALT+C
config_process = None

if len(sys.argv) >= 3:
    initial_pos = f"+{sys.argv[1]}+{sys.argv[2]}"
else:
    initial_pos = "+50+50"

def update_state(): # Button event
    check_config_macro()
    toggle_state()
    for key_name, label in key_label:
        try:
            is_pressed = keyboard.is_pressed(key_name)
            label.config(bg=light_color if is_pressed else label_bg)
        except:
            pass
    
    for mouse_name, label in mouse_label:
        try:
            is_pressed = mouse_state.get(mouse_name, False)
            label.config(bg=light_color if is_pressed else label_bg)
        except:
            pass

    app.after(20, update_state)

def toggle_state(): # Toggle event
    global toggle_pressed
    try:
        if keyboard.is_pressed('ctrl') and keyboard.is_pressed('shift') and keyboard.is_pressed('left_alt'):
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

def check_config_macro():
    global config_toggle_pressed, config_process
    try:
        if keyboard.is_pressed('ctrl') and keyboard.is_pressed('alt') and keyboard.is_pressed('c'):
            if not config_toggle_pressed:
                if config_process and config_process.poll() is None:
                    config_process.terminate()
                    config_process.wait()
                else:
                    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config_gui.py")
                    x, y = app.winfo_x(), app.winfo_y()
                    config_process = subprocess.Popen([sys.executable, config_path, str(x), str(y), str(os.getpid())])
                config_toggle_pressed = True
        else:
            config_toggle_pressed = False
    except:
        pass

def update_mouse_state(x, y, button, pressed):
    if button in mouse_state:
        mouse_state[button] = pressed

def start_drag(event):
    app._offset_x = event.x_root - app.winfo_x()
    app._offset_y = event.y_root - app.winfo_y()

def do_drag(event):
    app.geometry(f"+{event.x_root - app._offset_x}+{event.y_root - app._offset_y}")

def keyset_frame(keyset, frame, labelSet):
    if labelSet == key_label:
        for key, key_name, row, column in keyset: 
            frameKey = Label(frame, text=key, font=font_setting, bg=label_bg, fg=fg_color, padx=14, pady=10)
            frameKey.grid(row=row, column=column, sticky="nsew", padx=2, pady=2)
            frameKey.bind("<Button-1>", start_drag)
            frameKey.bind("<B1-Motion>", do_drag)
            labelSet.append((key_name, frameKey))
    elif labelSet == mouse_label:
        for mouseBtnName, mouse_name in keyset:
            frameMouse = Label(frame, text=mouseBtnName, font=font_setting, bg=label_bg, fg=fg_color, padx=14, pady=10)
            frameMouse.pack(side="left", expand=True, fill="both")
            frameMouse.bind("<Button-1>", start_drag)
            frameMouse.bind("<B1-Motion>", do_drag)
            mouse_label.append((mouse_name, frameMouse))

# Configuration.
config = load_config()
label_bg, fg_color, light_color = config.get("label_bg"), config.get("fg_color"), config.get("light_color")
font_setting = tuple(config.get("font_setting"))
bg_color = "#222222"

# App

app = Tk()

# Configurations
app.config(bg=bg_color)
app.wm_attributes("-transparentcolor", bg_color)
app.overrideredirect(True)
app.attributes("-topmost", True)

app.geometry(initial_pos)

app.bind("<Button-1>", start_drag)
app.bind("<B1-Motion>", do_drag)

frame1 = Frame(app, bg=bg_color) # Shift and CTRL frame
frame2 = Frame(app, bg=bg_color) # Main frame
frame3 = Frame(app, bg=bg_color) # Alt and Space frame
frame4 = Frame(app, bg="#224422")

for frame, row, column in [
    (frame1, 0, 0),
    (frame2, 0, 1),
    (frame3, 1, 0),
    (frame4, 0, 2)
]:
    frame.grid(row=row, column=column, sticky="nsew", padx=10, pady=10)
    frame.bind("<Button-1>", start_drag)
    frame.bind("<B1-Motion>", do_drag)

for frame, keyset, labelSet in [
    (frame1, keyset_1, key_label),
    (frame3, keyset_2, key_label),
    (frame2, keyset_3, key_label),
    (frame4, keyset_4, mouse_label)
]:
    keyset_frame(keyset, frame, labelSet)

update_state()
listener = mouse.Listener(on_click=update_mouse_state)
listener.start()
app.bind("<Escape>", lambda _: app.destroy())
app.mainloop()