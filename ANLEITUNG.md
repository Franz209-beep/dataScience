# Anleitung: Vorstellungsseite auf GitHub Pages

## Ordnerstruktur
```
bipm-intro/
├── index.html          ← deine Seite (Texte anpassen)
├── make_map.py         ← erzeugt die Karte
├── myJourney_Franz.ipynb ← dasselbe als Notebook (für Colab)
├── journey_map.html    ← fertige Karte (wird per iframe eingebunden)
└── images/             ← deine Fotos (Platzhalter ersetzen)
```

## 1. Inhalte anpassen (≈ 30–60 min)
1. **Fotos** in `images/` mit denselben Dateinamen ersetzen:
   | Datei | Wo auf der Seite |
   |---|---|
   | `me.jpg` | Porträt oben |
   | `rathenow1.jpg`, `rathenow2.jpg` | Born & raised |
   Tipp: vorher auf ~1200 px Breite verkleinern (z. B. squoosh.app), sonst lädt die Seite langsam.
   Achtung: GitHub unterscheidet Groß-/Kleinschreibung – `Me.JPG` ≠ `me.jpg`.
2. **index.html** öffnen (VS Code o. Ä.) und alle `[eckigen Klammern]` sowie
   LinkedIn/GitHub-Links ersetzen.
   Interessen: Begriffe in den `<li>`-Zeilen unter „Interests“ austauschen. Arbeitsstationen: 7 Zeilen in „Work experience“, nicht benötigte löschen.
3. **make_map.py**: Popup-Texte für Potsdam und Barcelona ergänzen (Stationen:
   Rathenow → Potsdam → Berlin → Barcelona → Berlin).
   Koordinaten: Rechtsklick in Google Maps → erste Zeile kopieren.
4. Karte neu bauen:
   ```bash
   pip install folium pyproj
   python make_map.py
   ```
   Ohne lokales Python: `myJourney_Franz.ipynb` in Google Colab öffnen, alle Zellen ausführen – die Karte wird angezeigt und als journey_map.html heruntergeladen.
5. Lokal prüfen: `python -m http.server` im Ordner starten → http://localhost:8000
   (Doppelklick auf index.html geht meist auch.)

## 2. Auf GitHub Pages veröffentlichen (≈ 10 min)
1. Auf github.com einloggen → **New repository**, z. B. `bipm-intro`, **Public**.
2. **Add file → Upload files** → den *Inhalt* des Ordners hochladen
   (index.html, journey_map.html, make_map.py und den Ordner `images` per Drag & Drop) → **Commit**.
3. **Settings → Pages** → Source: *Deploy from a branch*, Branch: `main`, Ordner `/ (root)` → **Save**.
4. Nach 1–2 Minuten ist die Seite online unter
   `https://DEIN-USERNAME.github.io/bipm-intro/`
5. Link testen (auch auf dem Handy) und in das Google Sheet des Kurses eintragen / an Prof. Loecher schicken.

## Warum die Karte funktioniert (gut für die Abgabe zu erwähnen)
Die Studentenseiten vom letzten Jahr nutzten Kartendienste, die inzwischen einen
API-Key verlangen. Hier wird **folium** (Python → Leaflet.js) mit
**OpenStreetMap**-Kacheln genutzt – frei, ohne Key. Auch CartoDB-Kacheln
verlangen inzwischen einen Key, deshalb bewusst OSM.

## Häufige Fehler
- Bild wird nicht angezeigt → Dateiname/Endung exakt prüfen (`.jpg` vs `.jpeg`, Groß-/Kleinschreibung).
- 404 auf GitHub Pages → Datei muss genau `index.html` heißen und im Repo-Wurzelverzeichnis liegen.
- Karte leer → `journey_map.html` vergessen hochzuladen.
- Änderungen nicht sichtbar → 1–2 Minuten warten, Seite mit Strg+F5 neu laden.
