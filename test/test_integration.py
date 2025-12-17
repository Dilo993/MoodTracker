import os
import json
import csv
import tempfile
import shutil
import pytest

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from storage import JSONStorage
from tracker import MoodTracker

def make_storage_file(tmp_path, name="moods.json"):
    p = tmp_path / name
    return str(p)

#1 sprawdza czy MoodTracker zapisuje wpisy do pliku przez JSONStorage
def test_tracker_persists_entries_to_file(tmp_path):
    path = make_storage_file(tmp_path)
    js = JSONStorage(path)
    t = MoodTracker(js)
    t.set_user("intuser")
    t.add_entry({"date":"2025-03-01","mood":5,"energy":5,"note":"ok"})
    js2 = JSONStorage(path)
    assert js2.load_entries()[0]["user"] == "intuser"

#2 sprawdza czy wpisy dla wielu użytkowników są poprawnie zapisywane i rozróżniane
def test_multiple_users_entries_saved(tmp_path):
    path = make_storage_file(tmp_path)
    js = JSONStorage(path)
    t = MoodTracker(js)
    t.set_user("u1")
    t.add_entry({"date":"2025-03-02","mood":3,"energy":2,"note":"a"})
    t.set_user("u2")
    t.add_entry({"date":"2025-03-03","mood":8,"energy":7,"note":"b"})
    loaded = js.load_entries()
    users = {e.get("user") for e in loaded}
    assert users == {"u1","u2"}

#3 sprawdza czy eksport do CSV zawiera wszystkie kolumny, w tym user
def test_export_csv_integration_contains_all_columns(tmp_path):
    path = make_storage_file(tmp_path)
    out = tmp_path / "out.csv"
    js = JSONStorage(path)
    t = MoodTracker(js)
    t.set_user("u3")
    t.add_entry({"date":"2025-04-01","mood":1,"energy":2,"note":"z"})
    js.export_csv(str(out))
    with open(out, encoding="utf-8", newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert "date" in reader.fieldnames and "user" in reader.fieldnames
        assert len(rows) == 1
        
#4 sprawdza czy usunięcie wpisu jest zapisywane w pliku
def test_delete_entry_persists(tmp_path):
    path = make_storage_file(tmp_path)
    js = JSONStorage(path)
    t = MoodTracker(js)
    t.set_user("u4")
    t.add_entry({"date":"d","mood":5,"energy":5,"note":""})
    t.delete_entry(0)
    assert js.load_entries() == []
    
#5 sprawdza czy edycja wpisu jest zapisywana w pliku
def test_edit_entry_persists(tmp_path):
    path = make_storage_file(tmp_path)
    js = JSONStorage(path)
    t = MoodTracker(js)
    t.set_user("u5")
    t.add_entry({"date":"ed","mood":1,"energy":1,"note":"n"})
    t.edit_entry(0, {"date":"ed","mood":10,"energy":9,"note":"edited","user":"u5"})
    assert js.load_entries()[0]["mood"] == 10
    
#6 sprawdza storage z uprzednio zapisanymi wpisami
def test_reload_tracker_loads_existing_entries(tmp_path):
    path = make_storage_file(tmp_path)
    js = JSONStorage(path)
    js.save_entries([{"date":"r","mood":2,"energy":2,"note":"x","user":"ruser"}])
    t = MoodTracker(js)
    assert len(t.entries) == 1
    assert t.entries[0]["user"] == "ruser"

#7 sprawdza obsługa znaków unicode
def test_unicode_note_and_csv_export(tmp_path):
    path = make_storage_file(tmp_path)
    out = tmp_path / "u_out.csv"
    js = JSONStorage(path)
    t = MoodTracker(js)
    t.set_user("uni")
    t.add_entry({"date":"2025-05-01","mood":4,"energy":4,"note":"żółć — тест"})
    js.export_csv(str(out))
    with open(out, encoding="utf-8", newline='') as f:
        text = f.read()
        assert "żółć" in text or "тест" in text
        
#8 sprawdza eksport CSV do zagnieżdżonej ścieżki tworzy brakujące katalogi i plik
def test_export_csv_creates_nested_dir(tmp_path):
    path = make_storage_file(tmp_path)
    js = JSONStorage(path)
    nested = tmp_path / "a" / "b" / "c" / "file.csv"
    js.save_entries([])
    js.export_csv(str(nested))
    assert nested.exists()

#9 sprawdza exporter CSV radzi sobie z brakującymi 
def test_export_handles_missing_keys_in_entries(tmp_path):
    path = make_storage_file(tmp_path)
    out = tmp_path / "missing.csv"
    js = JSONStorage(path)
    js.save_entries([{"date":"2025-06-01","mood":3}])
    js.export_csv(str(out))
    with open(out, encoding="utf-8", newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert rows[0]["energy"] == ""

#10 sprawdza eksport CSV z wieloma wpisami zawiera wszystkie kolumny i poprawną liczbę wierszy
def test_export_csv_multiple_entries_contains_all_columns_and_rows(tmp_path):
    fjson = tmp_path / "data_multi.json"
    fcsv = tmp_path / "out_multi.csv"
    js = JSONStorage(str(fjson))
    entries = [
        {"date":"2025-07-01","mood":1,"energy":2,"note":"a","user":"u1"},
        {"date":"2025-07-02","mood":2,"energy":3,"note":"b","user":"u2"},
    ]
    js.save_entries(entries)
    js.export_csv(str(fcsv))
    assert fcsv.exists()
    with open(fcsv, newline='', encoding="utf-8") as cf:
        reader = csv.DictReader(cf)
        rows = list(reader)
        assert len(rows) == 2
        assert set(r["user"] for r in rows) == {"u1","u2"}

