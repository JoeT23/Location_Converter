from pyproj import Transformer

# ----------------------------
# Transformer (BNG → WGS84); this is the first step for location conversion
# ----------------------------
transformer = Transformer.from_crs(
    "EPSG:27700",
    "EPSG:4326",
    always_xy=True
)

def easting_northing_to_latlon(easting, northing):
    """
    Convert UK National Grid coordinates to latitude/longitude.
    """

    lon, lat = transformer.transform(easting, northing)

    return lat, lon
