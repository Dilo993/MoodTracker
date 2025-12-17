# Punkt startowy aplikacji, uruchamia GUI

from ui import MoodTrackerApp

if __name__ == "__main__":
    app = MoodTrackerApp()
    app.run()
    
#przypominajka testy: pytest -q