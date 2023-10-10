import tkinter as tk
import pyautogui
import threading
import keyboard
from tkinter import ttk

# Global variables
autoclicking = False
click_interval = 1.0  # Default click interval in seconds
mouse_button = "Left Mouse Button"  # Default mouse button
start_hotkey = "F6"
stop_hotkey = "F5"
shutdown_hotkey = "l"
cps = 0  # CPS counter

# Function to toggle autoclick
def toggle_autoclick():
    global autoclicking
    autoclicking = not autoclicking
    if autoclicking:
        autoclick_button.config(text="Stop Autoclick")
        autoclick_thread = threading.Thread(target=start_cps_check)
        autoclick_thread.start()
    else:
        autoclick_button.config(text="Start Autoclick")

# Function to start autoclicking
def autoclick():
    while autoclicking:
        if mouse_button == "Left Mouse Button":
            pyautogui.click(button='left')
        else:
            pyautogui.click(button='right')
        pyautogui.PAUSE = click_interval

# Function to start CPS check
def start_cps_check():
    global cps
    cps = 0
    while autoclicking:
        cps += 1
        cps_label.config(text="CPS: {}".format(cps))
        cps_label.update()
        if mouse_button == "Left Mouse Button":
            pyautogui.click(button='left')
        else:
            pyautogui.click(button='right')
        pyautogui.PAUSE = click_interval

# Function to stop autoclicking and CPS check
def stop_autoclick():
    global autoclicking, cps
    autoclicking = False
    autoclick_button.config(text="Start Autoclick")
    cps_label.config(text="CPS: {}".format(cps))
    cps = 0

# Function to change settings
def update_settings():
    global click_interval, start_hotkey, stop_hotkey, shutdown_hotkey, mouse_button
    interval_str = interval_entry.get()
    start_hotkey = start_hotkey_entry.get()
    stop_hotkey = stop_hotkey_entry.get()

    # Check if the interval_str is a valid float
    try:
        click_interval = float(interval_str)
    except ValueError:
        print("Invalid click interval value:", interval_str)

# Function to shut down the script
def shutdown_script():
    # root.configure(bg="red")
    root.destroy()

# Function to listen for hotkeys
def check_hotkeys(event):
    if event.name == start_hotkey:
        toggle_autoclick()
    elif event.name == stop_hotkey:
        stop_autoclick()
    elif event.name == shutdown_hotkey:
        shutdown_script()

# Create the main window
root = tk.Tk()
root.title("Autoclicker")
root.geometry("300x350")

# Create labels and input fields for settings
settings_label = tk.Label(root, text="Settings", font=("Helvetica", 14))
settings_label.pack()

interval_label = tk.Label(root, text="Click Interval (seconds):")
interval_label.pack()
interval_entry = tk.Entry(root)
interval_entry.pack()

start_hotkey_label = tk.Label(root, text="Start Hotkey:")
start_hotkey_label.pack()
start_hotkey_entry = tk.Entry(root)
start_hotkey_entry.pack()

stop_hotkey_label = tk.Label(root, text="Stop Hotkey:")
stop_hotkey_label.pack()
stop_hotkey_entry = tk.Entry(root)
stop_hotkey_entry.pack()

# Create a label for mouse button selection
mouse_button_label = tk.Label(root, text="Select Mouse Button:")
mouse_button_label.pack()

# Create radio buttons to select the mouse button
left_mouse_button_radio = tk.Radiobutton(root, text="Left Mouse Button", variable=mouse_button, value="Left Mouse Button")
right_mouse_button_radio = tk.Radiobutton(root, text="Right Mouse Button", variable=mouse_button, value="Right Mouse Button")
left_mouse_button_radio.pack()
right_mouse_button_radio.pack()

update_button = tk.Button(root, text="Update Settings", command=update_settings)
update_button.pack()

# Create the main button to toggle autoclick
autoclick_button = tk.Button(root, text="Start Autoclick", command=toggle_autoclick)
autoclick_button.pack()

# Create a label to display CPS
cps_label = tk.Label(root, text="CPS: 0", font=("Helvetica", 14))
cps_label.pack()

# Start listening for hotkeys
keyboard.on_press(check_hotkeys)

root.mainloop()
