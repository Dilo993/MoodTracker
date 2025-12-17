# Logika biznesowa

class MoodTracker:
    def __init__(self, storage):
        self.storage = storage
        self.entries = self.storage.load_entries()
        self.current_user = None
    
    def set_user(self, username):
        self.current_user = username

    def add_entry(self, entry):
        # Dodaj nazwę użytkownika do zapisu
        if self.current_user:
            entry["user"] = self.current_user
        self.entries.append(entry)
        self.storage.save_entries(self.entries)
    
    def delete_entry(self, index):
        if 0 <= index < len(self.entries):
            self.entries.pop(index)
            self.storage.save_entries(self.entries)
    
    def edit_entry(self, index, new_entry):
        if 0 <= index < len(self.entries):
            self.entries[index] = new_entry
            self.storage.save_entries(self.entries)
    
    def get_average_mood(self):
        if not self.entries:
            return 0
        return sum(e["mood"] for e in self.entries) / len(self.entries)