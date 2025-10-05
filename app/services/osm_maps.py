from app.models.location import LocationData
import folium
import os
from pathlib import Path
from app.schemas.enums import LocationType


class OSMMap:
    def __init__(self, center=(50.061945, 19.936857), zoom_start=13):
        self.center = center
        self.zoom_start = zoom_start
        self.markers: list[folium.Marker] = []

    def add_marker(
        self, lat, lon, label=None, category: LocationType = LocationType.ORGANISATION, description: str | None = None
    ):
        popup = label if label else f"({lat}, {lon})"
        if category == LocationType.ORGANISATION:
            icon = folium.Icon(color="blue")
        elif category == LocationType.EVENT:
            popup = f"""
                <div style="font-family:Arial,sans-serif;max-width:350px;padding:16px;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.1);background:#fff;">
                    <h1 style="margin-top:0;color:#2c3e50;">Event: {popup}</h1>
                    <p style="margin:4px 0;color:#34495e;">{description if description is not None else ""}</p>
                    <a href="YOUR_REGISTRATION_URL"
                       style="display:inline-block;padding:10px 24px;margin-top:12px;background:#3498db;color:#fff;font-weight:bold;text-decoration:none;border-radius:4px;box-shadow:0 1px 4px rgba(52,152,219,0.2);transition:background 0.2s;"
                       onmouseover="this.style.background='#de476c';"
                       onmouseout="this.style.background='#e77e98';">
                       Zarejestruj!
                    </a>
                </div>
            """
            icon = folium.Icon(color="pink")
        else:
            return
        marker = folium.Marker((lat, lon), popup=popup, icon=icon)
        # marker = folium.Marker((lat, lon), popup=html_message, icon=icon,
        #               tooltip=marker_object.marker_name)
        # self.markers.append({'lat': lat, 'lon': lon, 'label': label})
        self.markers.append(marker)

    def generate_map(self, map_location: str | Path = "osm_map.html"):
        m = folium.Map(location=self.center, zoom_start=self.zoom_start)
        for marker in self.markers:
            marker.add_to(m)
        # Add click handler (for getting coordinates)
        m.add_child(folium.LatLngPopup())  # Shows lat/lon on click in the map
        m.save(map_location)


def generate_map_with_locations(locations: list[LocationData], map_filename: str = "osm_map.html"):
    map_location = Path(
        os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "templates", map_filename)
    )
    my_map = OSMMap()
    # my_map.add_marker(50.0530, 19.9336, "Smok Wawelski", LocationType.ORGANISATION)
    # my_map.add_marker(50.0617, 19.9334, "Collegium Maius", LocationType.ORGANISATION)
    my_map.add_marker(
        50.0677,
        19.9915,
        "HackYeah 2025",
        LocationType.EVENT,
        description="największy stacjonarny hackathon w Europie, który odbywa się w dniach 4-5 października 2025 w TAURON Arenie Kraków",
    )
    for location in locations:
        my_map.add_marker(location.latitude, location.longitude, location.name)
    my_map.generate_map(map_location=map_location)


# Example usage
# if __name__ == "__main__":
#     generate_map_with_locations(locations=)
