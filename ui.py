import customtkinter as ctk
from tracker import MoodTracker
from storage import JSONStorage
from datetime import date

class MoodTrackerApp:
    def __init__(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("MoodTracker+")
        self.root.geometry("600x500")
        
        # Logika
        self.storage = JSONStorage("data/moods.json")
        self.tracker = MoodTracker(self.storage)
        
        # GUI
        self.setup_ui()
    
    def setup_ui(self):
        # Nagłówek
        self.label = ctk.CTkLabel(self.root, text="MoodTracker+", font=("Arial", 24))
        self.label.pack(pady=10)
        
        # Formularz dodawania wpisu
        self.mood_label = ctk.CTkLabel(self.root, text="Nastrój (0-10)")
        self.mood_label.pack()
        self.mood_entry = ctk.CTkSlider(self.root, from_=0, to=10, number_of_steps=10)
        self.mood_entry.pack(pady=5)
        
        self.energy_label = ctk.CTkLabel(self.root, text="Energia (0-10)")
        self.energy_label.pack()
        self.energy_entry = ctk.CTkSlider(self.root, from_=0, to=10, number_of_steps=10)
        self.energy_entry.pack(pady=5)
        
        self.note_entry = ctk.CTkEntry(self.root, placeholder_text="Notatka")
        self.note_entry.pack(pady=5, fill="x", padx=20)
        
        self.save_btn = ctk.CTkButton(self.root, text="Zapisz wpis", command=self.add_entry)
        self.save_btn.pack(pady=10)
        
        # Historia wpisów w przewijalnym frame
        self.history_frame = ctk.CTkScrollableFrame(self.root, width=550, height=200)
        self.history_frame.pack(pady=10)
        self.update_history()
    
    def add_entry(self):
        entry = {
            "date": str(date.today()),
            "mood": int(self.mood_entry.get()),
            "energy": int(self.energy_entry.get()),
            "note": self.note_entry.get()
        }
        self.tracker.add_entry(entry)
        self.update_history()
    
    def update_history(self):
        # Usuń stare wpisy
        for widget in self.history_frame.winfo_children():
            widget.destroy()
        
        # Dodaj wszystkie wpisy
        for e in self.tracker.entries:
            text = f"{e['date']} - Mood: {e['mood']}, Energy: {e['energy']}, Note: {e['note']}"
            lbl = ctk.CTkLabel(self.history_frame, text=text, anchor="w")
            lbl.pack(fill="x", pady=2, padx=5)
    
    def run(self):
        self.root.mainloop()