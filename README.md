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

-Poniżej znajduje się tabela z przypadkami testowymi manualnymi.

| TestCase | Title | Preconditions | Steps | Expected Result |
|---|---|---|---|---|
| TC01 | Uruchomienie aplikacji | Python 3 zainstalowany, zależności dostępne | 1. Uruchom `python main.py`.<br>2. Obserwuj, czy okno aplikacji się otwiera. | Aplikacja uruchamia się bez błędów, główne okno widoczne. |
| TC02 | Ustawienie użytkownika | Aplikacja uruchomiona | 1. W polu "Nazwa użytkownika" wpisz nazwę.<br>2. Kliknij "Ustaw użytkownika". | Nazwa użytkownika zapisana, przycisk "Zapisz wpis" odblokowany. |
| TC03 | Dodawanie wpisu (poprawne dane) | Ustawiony użytkownik | 1. Ustaw wartości suwaków Mood i Energy.<br>2. Wpisz notatkę.<br>3. Kliknij "Zapisz wpis". | Wpis pojawia się w historii z datą, mood, energy, note i polem `user`. |
| TC04 | Historia pokazuje tylko wpisy bieżącego użytkownika | Są wpisy różnych użytkowników zapisane | 1. Ustaw użytkownika A i dodaj wpis.<br>2. Ustaw użytkownika B i dodaj wpis.<br>3. Ustaw ponownie użytkownika A. | W historii widoczne są tylko wpisy użytkownika A. |
| TC05 | Eksport CSV (poprawny przebieg) | Co najmniej jeden wpis dla bieżącego użytkownika | 1. Kliknij "Eksportuj CSV".<br>2. Wybierz lokalizację i zapisz plik.<br>3. Otwórz plik CSV w edytorze tekstu. | Plik zawiera nagłówki `date,mood,energy,note,user` i wiersze odpowiadające wpisom. |
| TC06 | Eksport CSV bez wybrania pliku (anulowanie) | Aplikacja uruchomiona | 1. Kliknij "Eksportuj CSV".<br>2. W oknie zapisu kliknij Anuluj. | Brak błędu; aplikacja pozostaje w stanie poprzednim. |
| TC07 | Eksport CSV gdy wpisy mają brakujące pola | W pliku JSON znajdują się wpisy bez niektórych kluczy (np. brak "note") | 1. Uruchom eksport CSV.<br>2. Otwórz wygenerowany plik. | Brakujące pola będą puste w CSV (puste komórki), eksport nie powoduje wyjątku. |
| TC08 | Walidacja zapisu do `data/moods.json` | Dodany nowy wpis przez UI | 1. Dodaj wpis przez GUI.<br>2. Otwórz `data/moods.json`. | Nowy wpis znajduje się w JSON z polem `user` równym ustawionemu użytkownikowi. |
| TC09 | Obsługa znaków unicode w notatce i eksporcie | Ustawiony użytkownik | 1. Wprowadź notatkę zawierającą polskie znaki i emoji.<br>2. Zapisz wpis i wyeksportuj CSV. | Znaki unicode poprawnie zapisane w JSON i CSV bez utraty danych. |
| TC10 | Obsługa błędów podczas eksportu (np. brak uprawnień) | Wybierz katalog docelowy bez praw zapisu (lub symuluj błąd) | 1. Kliknij "Eksportuj CSV" i wybierz lokalizację bez praw zapisu. | Wyświetlenie komunikatu o błędzie, aplikacja nie ulega awarii. |

## Uwagi deweloperskie
- `JSONStorage` przy inicjalizacji tworzy pustą listę w pliku, jeśli plik nie istnieje.
- Eksport CSV używa kolejności pól `date,mood,energy,note,user` i wstawia puste wartości gdy brakuje kluczy.
- `MoodTracker` przechowuje wpisy w pamięci (`self.entries`) i zapisuje/odczytuje je przez przekazany obiekt storage — ułatwia to testowanie przy użyciu podmiany storage (np. `FakeStorage`).

