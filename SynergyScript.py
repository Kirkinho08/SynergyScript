import pyautogui
import time
import threading
import keyboard  # Import the keyboard module
from tkinter import Tk, Button, Label, Entry

class MacroApp:
    def __init__(self, master):
        self.master = master
        master.title("Key Press Macro")
        master.geometry("300x200")  # Set the default window size
        
        self.label = Label(master, text="Press 'X' Key Macro")
        self.label.pack()
        
        self.duration_label = Label(master, text="Duration (seconds):")
        self.duration_label.pack()
        self.duration_entry = Entry(master)
        self.duration_entry.pack()
        self.duration_entry.insert(0, "10")
        
        self.interval_label = Label(master, text="Interval (seconds):")
        self.interval_label.pack()
        self.interval_entry = Entry(master)
        self.interval_entry.pack()
        self.interval_entry.insert(0, "0.5")
        
        self.on_button = Button(master, text="On", command=self.turn_on)
        self.on_button.pack()
        
        self.off_button = Button(master, text="Off", command=self.turn_off)
        self.off_button.pack()
        
        self.running = False
        self.paused = False
        self.thread = None

        # Set up the keyboard hook
        keyboard.add_hotkey('x', self.toggle_macro)
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def toggle_macro(self):
        if self.running:
            self.stop_macro()
        else:
            self.start_macro()

    def turn_on(self):
        self.paused = False

    def turn_off(self):
        self.paused = True

    def start_macro(self):
        if not self.running:
            self.running = True
            duration = float(self.duration_entry.get())
            interval = float(self.interval_entry.get())
            key = 'x'  # The key to press
            self.thread = threading.Thread(target=self.press_key_repeatedly, args=(key, duration, interval))
            self.thread.start()

    def stop_macro(self):
        if self.running:
            self.running = False
            if self.thread is not None:
                self.thread.join()
                self.thread = None

    def press_key_repeatedly(self, key, duration, interval):
        start_time = time.time()
        while self.running and time.time() - start_time < duration:
            if not self.paused:
                pyautogui.press(key)
                print(f"Pressed {key} at {time.time()}")
            time.sleep(interval)
        self.running = False  # Reset the flag after the loop finishes

    def on_closing(self):
        self.stop_macro()  # Ensure the macro stops if the window is closed
        keyboard.unhook_all_hotkeys()  # Unhook all hotkeys
        self.master.destroy()

if __name__ == "__main__":
    root = Tk()
    app = MacroApp(root)
    root.mainloop()
