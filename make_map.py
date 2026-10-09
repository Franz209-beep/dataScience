"""
make_map.py – erzeugt journey_map.html (interaktive Karte meines Werdegangs)

Basiert auf dem Notebook myJourney.ipynb aus dem Kurs:
folium + Großkreis-Bögen (pyproj) + Esri-Kacheln (kein API-Key nötig).
Statt "World_Light_Gray" wird die dunkle Variante genutzt, passend zur schwarzen Seite.

Installation:   pip install folium pyproj
Ausführen:      python make_map.py
Ergebnis:       journey_map.html (im selben Ordner wie index.html)
"""

import folium
from pyproj import Geod

geod = Geod(ellps="WGS84")

# ------------------------------------------------------------------
# Stationen (chronologisch). TODO: Texte in "popup" anpassen.
# ------------------------------------------------------------------
stops = [
    {"city": "Rathenow, Germany",  "lat": 52.6047, "lon": 12.3364, "popup": "Born &amp; raised 🏡"},
    {"city": "Potsdam, Germany",   "lat": 52.3906, "lon": 13.0645, "popup": "[Was hast du in Potsdam gemacht?] 🎓"},
    {"city": "Berlin, Germany",    "lat": 52.5200, "lon": 13.4050, "popup": "Dual studies Business Informatics @ HWR · Bayer (2023–2026) 🎓💼"},
    {"city": "Barcelona, Spain",   "lat": 41.3874, "lon": 2.1686,  "popup": "[Was hast du in Barcelona gemacht?] ☀️"},
    {"city": "Berlin, Germany",    "lat": 52.5200, "lon": 13.4050, "popup": "Junior HR Data Quality Consultant @ Bayer · Master BIPM @ HWR (since 2026) 💼🎓"},
]

ACCENT = "#e3324a"  # gleiche Farbe wie auf der Seite

# Karte mit dunklen Esri-Kacheln (Basis + Beschriftungen)
m = folium.Map(
    location=[48, 8],
    zoom_start=4,
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}",
    attr="Tiles &copy; Esri --- Esri, HERE, Garmin, and contributors",
)
folium.TileLayer(
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Reference/MapServer/tile/{z}/{y}/{x}",
    attr="Esri",
    overlay=True,
    control=False,
).add_to(m)

# Orte, die mehrfach vorkommen (Berlin), bekommen EINEN Marker mit allen Stationen im Popup
places = {}
for no, stop in enumerate(stops, start=1):
    key = (stop["lat"], stop["lon"])
    places.setdefault(key, {"city": stop["city"], "entries": []})
    places[key]["entries"].append(f"<b>{no}.</b> {stop['popup']}")

for (lat, lon), place in places.items():
    numbers = " / ".join(e.split("</b>")[0].replace("<b>", "").rstrip(".") for e in place["entries"])
    folium.Marker(
        [lat, lon],
        popup=folium.Popup(f"<b>{place['city']}</b><br>" + "<br>".join(place["entries"]), max_width=280),
        tooltip=place["city"],
        icon=folium.DivIcon(
            icon_size=(40, 26),
            icon_anchor=(20, 13),
            html=(
                f"<div style='background:{ACCENT};color:#fff;border-radius:13px;height:26px;"
                f"min-width:26px;padding:0 7px;display:inline-flex;align-items:center;"
                f"justify-content:center;font:600 12px sans-serif;white-space:nowrap;"
                f"border:2px solid #fff;box-shadow:0 1px 6px rgba(0,0,0,.6)'>{numbers}</div>"
            ),
        ),
    ).add_to(m)


# Funktion aus dem Kurs-Notebook: viele Zwischenpunkte auf dem Großkreis
def great_circle_points(lat1, lon1, lat2, lon2, npts=100):
    points = geod.npts(lon1, lat1, lon2, lat2, npts)
    return [(lat1, lon1)] + [(lat, lon) for lon, lat in points] + [(lat2, lon2)]


# Bögen zwischen aufeinanderfolgenden Stationen (Rückweg gestrichelt)
for i in range(len(stops) - 1):
    start, end = stops[i], stops[i + 1]
    arc = great_circle_points(start["lat"], start["lon"], end["lat"], end["lon"], npts=60)
    is_return = i > 0 and (end["lat"], end["lon"]) == (stops[i - 1]["lat"], stops[i - 1]["lon"])
    folium.PolyLine(
        arc,
        color=ACCENT,
        weight=3,
        opacity=0.85,
        dash_array="6 8" if is_return else None,
    ).add_to(m)

# Ausschnitt so wählen, dass alle Stationen sichtbar sind
m.fit_bounds([[s["lat"], s["lon"]] for s in stops], padding=(30, 30))

m.save("journey_map.html")
print(f"journey_map.html mit {len(stops)} Stationen ({len(places)} Orten) erstellt.")
