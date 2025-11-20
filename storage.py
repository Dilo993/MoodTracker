# Obsługa zapisu/odczytu danych

import json
import os

class JSONStorage:
    def __init__(self, filepath):
        self.filepath = filepath
        if not os.path.exists(filepath):
            with open(filepath, "w") as f:
                json.dump([], f)
    
    def load_entries(self):
        with open(self.filepath, "r") as f:
            return json.load(f)
    
    def save_entries(self, entries):
        with open(self.filepath, "w") as f:
            json.dump(entries, f, indent=4)