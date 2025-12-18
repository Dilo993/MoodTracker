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
.venv\Scripts\activate
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

- `test/test_unit.py` — testy jednostkowe skupione na pojedynczych klasach i metodach:
	- sprawdza, że `JSONStorage` tworzy plik przy inicjalizacji i potrafi zapisać/wczytać listę wpisów,
	- weryfikuje, że `JSONStorage.export_csv()` tworzy plik CSV oraz katalogi jeśli ich brak,
	- testuje `MoodTracker` z `FakeStorage`: `set_user()`, `add_entry()` (przypisanie `user` i zapis),
		`delete_entry()`, `edit_entry()` oraz obliczanie średniej nastroju (pusty zbiór → 0, obliczenie średniej).

- `test/test_integration.py` — testy integracyjne weryfikujące współpracę `MoodTracker` i `JSONStorage` oraz eksport CSV:
	- czy wpisy są poprawnie zapisywane do pliku i wczytywane (persistencja),
	- obsługa wielu użytkowników i rozróżnianie wpisów po polu `user`,
	- eksport CSV zawiera wszystkie kolumny (`date`, `mood`, `energy`, `note`, `user`) i poprawną liczbę wierszy,
	- operacje `delete_entry()` i `edit_entry()` są trwałe (zmiany zapisane w pliku),
	- ponowne uruchomienie/tracker z istniejącym storage ładuje uprzednio zapisane wpisy,
	- obsługa znaków Unicode w notatkach oraz poprawny export,
	- eksport do zagnieżdżonej ścieżki tworzy brakujące katalogi,
	- eksport radzi sobie z brakującymi kluczami (np. brak `energy`) i zapisuje puste pola w CSV,
	- test z wieloma wpisami sprawdza kompletność i zgodność pól `user` w wyeksportowanym CSV.

## Uwagi deweloperskie
- `JSONStorage` przy inicjalizacji tworzy pustą listę w pliku, jeśli plik nie istnieje.
- Eksport CSV używa kolejności pól `date,mood,energy,note,user` i wstawia puste wartości gdy brakuje kluczy.
- `MoodTracker` przechowuje wpisy w pamięci (`self.entries`) i zapisuje/odczytuje je przez przekazany obiekt storage — ułatwia to testowanie przy użyciu podmiany storage (np. `FakeStorage`).

