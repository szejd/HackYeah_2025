from app.models.location import LocationData
import folium
import os
from pathlib import Path
from app.schemas.enums import LocationType
from app.crud.location import get_all_locations


class OSMMap:
    def __init__(self, center=(50.061945, 19.936857), zoom_start=13):
        self.center = center
        self.zoom_start = zoom_start
        self.markers: list[folium.Marker] = []

    def add_marker(self, lat, lon, label=None, category: LocationType = LocationType.ORGANISATION):
        if category == LocationType.ORGANISATION:
            icon = folium.Icon(color="blue")
        elif category == LocationType.EVENT:
            icon = folium.Icon(color="pink")
        else:
            return
        marker = folium.Marker((lat, lon), popup=label if label else f"({lat}, {lon})", icon=icon)
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
    # my_map.add_marker(50.0677, 19.9915, "HackYeah 2025", LocationType.EVENT)
    for location in locations:
        my_map.add_marker(location.latitude, location.longitude, location.name)
    my_map.generate_map(map_location=map_location)


# Example usage
# if __name__ == "__main__":
#     generate_map_with_locations(locations=)
