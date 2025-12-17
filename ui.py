import customtkinter as ctk
from tracker import MoodTracker
from storage import JSONStorage
from datetime import date
from tkinter import filedialog, messagebox

class MoodTrackerApp:
    def __init__(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.geometry("600x500")
        
        # Logika
        self.storage = JSONStorage("data/moods.json")
        self.tracker = MoodTracker(self.storage)
        
        # GUI
        self.setup_ui()
    
    def setup_ui(self):
        
        # Eksport CSV
        self.export_btn = ctk.CTkButton(self.root, text="Eksportuj CSV", command=self.export_csv)
        self.export_btn.place(x=10, y=10)
        
        # Pole logowania
        self.username_label = ctk.CTkLabel(self.root, text="Nazwa użytkownika")
        self.username_label.pack(pady=(40,0))
        self.username_entry = ctk.CTkEntry(self.root, placeholder_text="Wpisz nazwę użytkownika")
        self.username_entry.pack(pady=5, fill="x", padx=20)
        self.set_user_btn = ctk.CTkButton(self.root, text="Ustaw użytkownika", command=self.set_username)
        self.set_user_btn.pack(pady=(0,10))
        
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
        
        self.save_btn = ctk.CTkButton(self.root, text="Zapisz wpis", command=self.add_entry, state="disabled")
        self.save_btn.pack(pady=10)

        # Historia wpisów w przewijalnym frame
        self.history_frame = ctk.CTkScrollableFrame(self.root, width=550, height=200)
        self.history_frame.pack(pady=10)
        self.update_history()
    
    def add_entry(self):
        # Nie przyjmuj wpisu bez ustawionego użytkownika
        if not getattr(self, "current_user", None):
            messagebox.showwarning("Brak użytkownika", "Ustaw najpierw nazwę użytkownika.")
            return

        entry = {
            "date": str(date.today()),
            "mood": int(self.mood_entry.get()),
            "energy": int(self.energy_entry.get()),
            "note": self.note_entry.get()
        }
        self.tracker.add_entry(entry)
        self.update_history()
    
    def set_username(self):
        name = self.username_entry.get().strip()
        if not name:
            self.save_btn = ctk.CTkButton(self.root,text="Podaj użytkownika")
            messagebox.showwarning("Użytkownik", "Podaj nazwę użytkownika.")
            return
        self.tracker.set_user(name)
        # Zapisz lokalnie informację, że użytkownik jest ustawiony i odblokuj zapis
        self.current_user = name
        self.save_btn.configure(state="normal")
        self.update_history()
    
    def export_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv")],
                                                 initialfile="moods.csv",
                                                 title="Zapisz jako")
        if not file_path:
            return
        try:
            self.storage.export_csv(file_path)
            messagebox.showinfo("Eksport", "Plik CSV został zapisany.")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się wyeksportować pliku:\n{e}")
    
    def update_history(self):
        # Usuń stare wpisy
        for widget in self.history_frame.winfo_children():
            widget.destroy()
        
        # Dodaj tylko wpisy bieżącego użytkownika
        current_user = getattr(self, "current_user", None)
        for e in self.tracker.entries:
            if current_user and e.get("user") == current_user:
                text = f"{e['date']} - Mood: {e['mood']}, Energy: {e['energy']}, Note: {e['note']}"
                lbl = ctk.CTkLabel(self.history_frame, text=text, anchor="w")
                lbl.pack(fill="x", pady=2, padx=5)
    
    def run(self):
        self.root.mainloop()