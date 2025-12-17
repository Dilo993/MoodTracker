import os
import json
import csv
import tempfile
import pytest

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from storage import JSONStorage
from tracker import MoodTracker


class FakeStorage:
    def __init__(self):
        self._entries = []
    def load_entries(self):
        return list(self._entries)
    def save_entries(self, entries):
        self._entries = list(entries)

#1 sprawdza czy inicjalizacja JSONStorage tworzy plik jeśli nie istnieje
def test_jsonstorage_init_creates_file():
    tmp = tempfile.NamedTemporaryFile(delete=False)
    path = tmp.name
    tmp.close()
    os.remove(path)
    js = JSONStorage(path)
    assert os.path.exists(path)
    os.remove(path)
    print("PASS: test_jsonstorage_init_creates_file")

#2 sprawdza zapis i ponowne wczytanie wpisów
def test_jsonstorage_save_and_load_entries(tmp_path):
    f = tmp_path / "data.json"
    js = JSONStorage(str(f))
    entries = [{"date":"2025-01-01","mood":5}]
    js.save_entries(entries)
    loaded = js.load_entries()
    assert loaded == entries
    print("PASS: test_jsonstorage_save_and_load_entries")

#3 sprawdza eksport do CSV tworzy plik i zawartość
def test_jsonstorage_export_csv_creates_file_and_content(tmp_path):
    fjson = tmp_path / "data.json"
    fcsv = tmp_path / "out.csv"
    js = JSONStorage(str(fjson))
    entries = [{"date":"2025-01-02","mood":7,"energy":8,"note":"ok","user":"u1"}]
    js.save_entries(entries)
    js.export_csv(str(fcsv))
    assert fcsv.exists()
    with open(fcsv, newline='', encoding="utf-8") as cf:
        reader = csv.DictReader(cf)
        rows = list(reader)
        assert len(rows) == 1
        assert rows[0]["date"] == "2025-01-02"
        assert rows[0]["user"] == "u1"
    print("PASS: test_jsonstorage_export_csv_creates_file_and_content")

#4 sprawdza eksport do CSV tworzy katalog jeśli nie istnieje
def test_jsonstorage_export_creates_nonexistent_dir(tmp_path):
    fjson = tmp_path / "data.json"
    js = JSONStorage(str(fjson))
    entries = []
    js.save_entries(entries)
    outdir = tmp_path / "subdir" / "out.csv"
    js.export_csv(str(outdir))
    assert outdir.exists()
    print("PASS: test_jsonstorage_export_creates_nonexistent_dir")

#5 sprawdza ustawienie użytkownika w MoodTracker zapisuje użytkownika
def test_moodtracker_set_user():
    storage = FakeStorage()
    t = MoodTracker(storage)
    t.set_user("alice")
    assert t.current_user == "alice"
    print("PASS: test_moodtracker_set_user")

#6 sprawdza dodanie wpisu przypisuje aktualnego użytkownika i zapisuje wpisy w magazynie
def test_moodtracker_add_entry_sets_user_and_saves():
    storage = FakeStorage()
    t = MoodTracker(storage)
    t.set_user("bob")
    entry = {"date":"2025-02-01","mood":6,"energy":4,"note":"x"}
    t.add_entry(entry.copy())
    assert len(t.entries) == 1
    saved = storage.load_entries()
    assert saved[0]["user"] == "bob"
    assert saved[0]["mood"] == 6
    print("PASS: test_moodtracker_add_entry_sets_user_and_saves")

#7 sprawdza usuwanie wpisu po indeksie
def test_moodtracker_delete_entry():
    storage = FakeStorage()
    t = MoodTracker(storage)
    t.entries = [{"date":"d1"},{"date":"d2"}]
    storage.save_entries(t.entries)
    t.delete_entry(0)
    assert len(t.entries) == 1
    assert t.entries[0]["date"] == "d2"
    print("PASS: test_moodtracker_delete_entry")

#8 sprawdza edycja wpisu po indeksie
def test_moodtracker_edit_entry():
    storage = FakeStorage()
    t = MoodTracker(storage)
    t.entries = [{"date":"d1","mood":1}]
    storage.save_entries(t.entries)
    t.edit_entry(0, {"date":"d1","mood":9})
    assert t.entries[0]["mood"] == 9
    print("PASS: test_moodtracker_edit_entry")

#9 sprawdza średnia nastroju przy braku wpisów zwraca 0
def test_get_average_mood_empty_returns_zero():
    storage = FakeStorage()
    t = MoodTracker(storage)
    t.entries = []
    assert t.get_average_mood() == 0
    print("PASS: test_get_average_mood_empty_returns_zero")

#10 sprawdza oblicza prawidłową średnią z kilku wpisów mood
def test_get_average_mood_computes_average():
    storage = FakeStorage()
    t = MoodTracker(storage)
    t.entries = [{"mood":2},{"mood":6},{"mood":4}]
    assert pytest.approx(t.get_average_mood(), rel=1e-3) == 4.0
    print("PASS: test_get_average_mood_computes_average")