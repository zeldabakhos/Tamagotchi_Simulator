import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

from game import calculate_statistics, update_game
from storage import load_game, save_game
from tamagotchi import Tamagotchi


class TamagotchiGUI:
    def __init__(self, window):
        self.window = window
        self.pets = [Tamagotchi("Mochi"), Tamagotchi("Luna"), Tamagotchi("Pip")]
        self.selected_index = 0

        window.title("Tamagotchi Simulator")
        window.geometry("680x680")
        window.minsize(600, 650)

        content = ttk.Frame(window, padding=20)
        content.pack(fill="both", expand=True)
        ttk.Label(content, text="Tamagotchi Simulator", font=("Arial", 22, "bold")).pack()
        ttk.Label(content, text="Care for all three pets. Each care action advances one turn.").pack(pady=8)

        self.pet_selector = ttk.Combobox(content, state="readonly")
        self.pet_selector.pack(fill="x", pady=8)
        self.pet_selector.bind("<<ComboboxSelected>>", self.select_pet)

        status_frame = ttk.LabelFrame(content, text="Selected pet", padding=12)
        status_frame.pack(fill="x", pady=8)
        status_frame.columnconfigure(1, weight=1)
        self.pet_title = ttk.Label(status_frame, font=("Arial", 14, "bold"))
        self.pet_title.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 8))
        self.stat_labels = {}
        self.stat_bars = {}
        for row, stat in enumerate(("hunger", "health", "boredom", "exhaustion"), start=1):
            ttk.Label(status_frame, text=stat.capitalize()).grid(row=row, column=0, sticky="w", padx=(0, 12))
            bar = ttk.Progressbar(status_frame, maximum=100)
            bar.grid(row=row, column=1, sticky="ew", pady=4)
            label = ttk.Label(status_frame, width=8, anchor="e")
            label.grid(row=row, column=2)
            self.stat_bars[stat] = bar
            self.stat_labels[stat] = label

        actions = ttk.Frame(content)
        actions.pack(fill="x", pady=8)
        self.action_buttons = []
        for action in ("feed", "play", "sleep", "heal"):
            button = ttk.Button(
                actions, text=action.capitalize(),
                command=lambda chosen_action=action: self.perform_action(chosen_action),
            )
            button.pack(side="left", fill="x", expand=True, padx=3)
            self.action_buttons.append(button)

        self.statistics_label = ttk.Label(content, justify="left")
        self.statistics_label.pack(anchor="w", pady=8)

        controls = ttk.Frame(content)
        controls.pack(fill="x", pady=8)
        ttk.Button(controls, text="Save game", command=self.save).pack(side="left", padx=3)
        ttk.Button(controls, text="Load game", command=self.load).pack(side="left", padx=3)
        ttk.Button(controls, text="Quit", command=window.destroy).pack(side="right", padx=3)

        ttk.Label(content, text="Activity").pack(anchor="w")
        self.activity = scrolledtext.ScrolledText(content, height=6, wrap="word", state="disabled")
        self.activity.pack(fill="both", expand=True, pady=(4, 0))
        self.refresh()
        self.log("Welcome! Select a pet and choose an action. Lower needs and higher health are better.")

    def select_pet(self, event):
        self.selected_index = self.pet_selector.current()
        self.refresh()

    def refresh(self):
        names = []
        for pet in self.pets:
            state = "Alive" if pet.is_alive() else "Deceased"
            names.append(f"{pet.name} ({state})")
        self.pet_selector["values"] = names
        self.pet_selector.current(self.selected_index)

        pet = self.pets[self.selected_index]
        self.pet_title.config(text=names[self.selected_index])
        for stat in self.stat_labels:
            value = getattr(pet, stat)
            self.stat_labels[stat].config(text=f"{value}/100")
            self.stat_bars[stat]["value"] = value

        state = "normal" if pet.is_alive() else "disabled"
        for button in self.action_buttons:
            button.config(state=state)

        statistics = calculate_statistics(self.pets)
        self.statistics_label.config(text=(
            f"Living pets: {statistics['living']}    Dead pets: {statistics['dead']}\n"
            f"Average health (living pets): {statistics['average_health']:.1f}/100\n"
            f"All pets - Hunger: {statistics['average_hunger']:.1f}    "
            f"Boredom: {statistics['average_boredom']:.1f}    "
            f"Exhaustion: {statistics['average_exhaustion']:.1f}"
        ))

    def log(self, message):
        self.activity.config(state="normal")
        self.activity.insert("end", message + "\n")
        self.activity.see("end")
        self.activity.config(state="disabled")

    def perform_action(self, action):
        pet = self.pets[self.selected_index]
        try:
            if action == "feed":
                pet.feed()
            elif action == "play":
                pet.play()
            elif action == "sleep":
                pet.sleep()
            elif action == "heal":
                pet.heal()
        except ValueError as error:
            messagebox.showerror("Cannot perform action", str(error), parent=self.window)
            return

        self.log(f"{pet.name}: {action.capitalize()}.")
        for message in update_game(self.pets):
            self.log(message)
        self.refresh()
        if not any(pet.is_alive() for pet in self.pets):
            self.log("All pets have died. You can load a saved game or quit.")

    def save(self):
        try:
            save_game(self.pets)
        except OSError as error:
            messagebox.showerror("Save failed", str(error), parent=self.window)
            return
        self.log("Game saved to savegame.json.")

    def load(self):
        try:
            pets = load_game()
        except (ValueError, OSError) as error:
            messagebox.showerror("Load failed", str(error), parent=self.window)
            return
        self.pets = pets
        self.selected_index = 0
        self.refresh()
        self.log("Game loaded from savegame.json. The first pet is selected.")


if __name__ == "__main__":
    if tk.TkVersion < 8.6:
        raise SystemExit(
            "This interface needs Tk 8.6 or newer. The macOS system Tk is too old.\n"
            "Run with the supported Python runtime:\n"
            "uv run --managed-python --python 3.13 gui.py"
        )
    root = tk.Tk()
    app = TamagotchiGUI(root)
    root.mainloop()
