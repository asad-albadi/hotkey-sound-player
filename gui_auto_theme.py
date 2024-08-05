import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from ttkthemes import ThemedTk
from pynput import keyboard
import pygame
import json
import os

CONFIG_FILE = "config.json"

class HotkeySoundApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotkey Sound Player")

        self.sound_hotkey_pairs = []
        self.hotkeys = []

        # Set Fluent UI theme
        self.set_fluent_ui_theme()

        # Create UI elements
        self.create_widgets()

        # Load configuration from file
        self.load_config()

        # Listener state
        self.listener_running = False

        # Initialize pygame mixer
        pygame.mixer.init()

    def set_fluent_ui_theme(self):
        self.root.set_theme('arc')

    def create_widgets(self):
        frame = ttk.Frame(self.root)
        frame.grid(row=0, column=0, padx=0, pady=0, sticky='nsew')

        # Sound file selection
        self.sound_label = ttk.Label(frame, text="Sound File:")
        self.sound_label.grid(row=0, column=0, padx=10, pady=5)

        self.sound_entry = ttk.Entry(frame, width=50)
        self.sound_entry.grid(row=0, column=1, padx=10, pady=5)

        self.sound_button = ttk.Button(frame, text="Browse", command=self.browse_file)
        self.sound_button.grid(row=0, column=2, padx=10, pady=5)

        # Hotkey combination input
        self.hotkey_label = ttk.Label(frame, text="Hotkey Combination:")
        self.hotkey_label.grid(row=1, column=0, padx=10, pady=5)

        self.hotkey_entry = ttk.Entry(frame, width=50)
        self.hotkey_entry.grid(row=1, column=1, padx=10, pady=5)

        # Add sound-hotkey pair button
        self.add_button = ttk.Button(frame, text="Add", command=self.add_sound_hotkey_pair)
        self.add_button.grid(row=1, column=2, padx=10, pady=5)

        # Table to display sound-hotkey pairs
        self.pair_table = ttk.Treeview(frame, columns=("Sound File", "Hotkey Combination"), show="headings")
        self.pair_table.heading("Sound File", text="Sound File")
        self.pair_table.heading("Hotkey Combination", text="Hotkey Combination")
        self.pair_table.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        # Remove selected pair button
        self.remove_button = ttk.Button(frame, text="Remove Selected", command=self.remove_selected_pair)
        self.remove_button.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

        # Start/Stop toggle button
        self.toggle_button = ttk.Button(frame, text="Start", command=self.toggle_listener)
        self.toggle_button.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

    def browse_file(self):
        sound_file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.ogg *.wav *.oga")])
        if sound_file:
            self.sound_entry.delete(0, tk.END)
            self.sound_entry.insert(0, sound_file)

    def add_sound_hotkey_pair(self):
        sound_file = self.sound_entry.get()
        hotkey_combination = self.hotkey_entry.get()

        if not sound_file or not hotkey_combination:
            messagebox.showwarning("Input Error", "Please provide both a sound file and a hotkey combination.")
            return

        try:
            hotkey = keyboard.HotKey(
                keyboard.HotKey.parse(hotkey_combination),
                lambda: self.on_detection_play_sound(sound_file)
            )
            self.hotkeys.append(hotkey)
        except Exception as e:
            messagebox.showerror("Hotkey Error", f"Invalid hotkey combination: {e}")
            return

        self.sound_hotkey_pairs.append((sound_file, hotkey_combination))
        self.update_table()
        self.save_config()

    def remove_selected_pair(self):
        selected_item = self.pair_table.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a pair to remove.")
            return

        index = self.pair_table.index(selected_item)
        del self.sound_hotkey_pairs[index]
        del self.hotkeys[index]
        self.update_table()
        self.save_config()

    def update_table(self):
        self.pair_table.delete(*self.pair_table.get_children())
        for sound_file, hotkey_combination in self.sound_hotkey_pairs:
            self.pair_table.insert("", "end", values=(sound_file, hotkey_combination))

    def on_detection_play_sound(self, sound_file):
        print(f"Key combination detected! Playing sound: {sound_file}")
        self.play_sound(sound_file)

    def play_sound(self, file_path):
        sound = pygame.mixer.Sound(file_path)
        sound.play()

    def for_canonical(self, f):
        return lambda k: f(self.listener.canonical(k))

    def press_handler(self, key):
        for hotkey in self.hotkeys:
            hotkey.press(self.listener.canonical(key))

    def release_handler(self, key):
        for hotkey in self.hotkeys:
            hotkey.release(self.listener.canonical(key))

    def toggle_listener(self):
        if self.listener_running:
            self.stop_listener()
        else:
            self.start_listener()

    def start_listener(self):
        if not hasattr(self, 'listener') or not self.listener.running:
            self.listener = keyboard.Listener(
                on_press=self.for_canonical(self.press_handler),
                on_release=self.for_canonical(self.release_handler)
            )
            self.listener.start()
            self.listener_running = True
            self.toggle_button.config(text="Stop")
            messagebox.showinfo("Listener Started", "Hotkey listener started.")

    def stop_listener(self):
        if hasattr(self, 'listener') and self.listener.running:
            self.listener.stop()
            self.listener_running = False
            self.toggle_button.config(text="Start")
            # Stop any currently playing sound
            pygame.mixer.stop()
            messagebox.showinfo("Listener Stopped", "Hotkey listener stopped.")

    def save_config(self):
        config = {"sound_hotkey_pairs": self.sound_hotkey_pairs}
        with open(CONFIG_FILE, "w") as config_file:
            json.dump(config, config_file)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as config_file:
                config = json.load(config_file)
                self.sound_hotkey_pairs = config.get("sound_hotkey_pairs", [])
                for sound_file, hotkey_combination in self.sound_hotkey_pairs:
                    try:
                        hotkey = keyboard.HotKey(
                            keyboard.HotKey.parse(hotkey_combination),
                            lambda: self.on_detection_play_sound(sound_file)
                        )
                        self.hotkeys.append(hotkey)
                    except Exception as e:
                        messagebox.showerror("Hotkey Error", f"Invalid hotkey combination in config: {e}")
                self.update_table()

if __name__ == "__main__":
    root = ThemedTk()
    app = HotkeySoundApp(root)
    root.mainloop()
