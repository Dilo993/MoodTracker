# MoodTracker

Lekka aplikacja do ręcznego śledzenia nastroju i energii, zapisywana lokalnie w formacie JSON z możliwością eksportu do CSV.

# Autor

Blady Bartłomiej

## Spis treści
- Opis
- Wymagania
- Instalacja
- Uruchomienie
- Funkcjonalności
- Struktura projektu
- Testy
- Scenariusze manualne
- Uwagi deweloperskie

## Opis
`MoodTracker` pozwala użytkownikom zapisywać codzienne wpisy z pola `mood` (0-10), `energy` (0-10) oraz krótką notatką. Wpisy są zapisywane w pliku JSON (`data/moods.json`). Aplikacja oferuje prosty interfejs GUI (CustomTkinter) i eksport danych do CSV.

## Wymagania
- Python 3.8+
- Biblioteka `customtkinter` (opcjonalna, tylko dla GUI)

Instalacja zależności (opcjonalnie w wirtualnym środowisku):

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install customtkinter
```

## Instalacja
1. Sklonuj repozytorium lub skopiuj katalog projektu.
2. Upewnij się, że masz zainstalowany Python i ewentualnie `customtkinter`.

## Uruchomienie
- Uruchom aplikację GUI:

```bash
python main.py
```

Po uruchomieniu: ustaw nazwę użytkownika, wprowadź wartości nastroju i energii, dodaj notatkę i zapisz wpis. Skorzystaj z przycisku "Eksportuj CSV" aby zapisać dane do pliku CSV.

## Funkcjonalności
- Dodawanie wpisów z datą, nastrojem, energią i notatką.
- Obsługa wielu użytkowników (pole `user` jest dodawane automatycznie po ustawieniu użytkownika).
- Eksport wszystkich wpisów z JSON do pliku CSV z nagłówkami: `date,mood,energy,note,user`.
- Eksporter tworzy brakujące katalogi jeśli to konieczne.

## Struktura projektu
- `main.py` — punkt startowy aplikacji, uruchamia GUI.
- `ui.py` — warstwa interfejsu użytkownika (CustomTkinter).
- `tracker.py` — logika biznesowa (`MoodTracker`).
- `storage.py` — obsługa zapisu/odczytu (`JSONStorage`) i eksportu CSV.
- `data/moods.json` — domyczne miejsce przechowywania wpisów.
- `test/` — testy jednostkowe i integracyjne (pytest).

## Testy
Projekt zawiera testy w katalogu `test/` wykorzystujące `pytest`.

Uruchom wszystkie testy:

```bash
pytest -q
```

Kilka istotnych testów pokrywających:
- inicjalizację i zapis `JSONStorage`,
- eksport do CSV i tworzenie katalogów,
- funkcje `MoodTracker` (set_user, add/edit/delete entry, średnia nastroju),
- obsługa znaków unicode oraz brakujących pól przy eksporcie.

## Scenariusze manualne
Plik ze szczegółowymi przypadkami testowymi manualnymi znajduje się w `manual_tests.txt`.

## Uwagi deweloperskie
- `JSONStorage` przy inicjalizacji tworzy pustą listę w pliku, jeśli plik nie istnieje.
- Eksport CSV używa kolejności pól `date,mood,energy,note,user` i wstawia puste wartości gdy brakuje kluczy.
- `MoodTracker` przechowuje wpisy w pamięci (`self.entries`) i zapisuje/odczytuje je przez przekazany obiekt storage — ułatwia to testowanie przy użyciu podmiany storage (np. `FakeStorage`).

