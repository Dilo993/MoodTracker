# Obsługa zapisu/odczytu danych

import json
import os
import csv

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

    def export_csv(self, csv_path):
        entries = self.load_entries()
        # Upewnij się, że katalog docelowy istnieje
        dirname = os.path.dirname(csv_path)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname, exist_ok=True)
        # pola w ustalonej kolejności, dodano 'user'
        fieldnames = ["date", "mood", "energy", "note", "user"]
        with open(csv_path, "w", newline='', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for e in entries:
                # upewnij się, że wszystkie klucze istnieją
                row = {k: e.get(k, "") for k in fieldnames}
                writer.writerow(row)