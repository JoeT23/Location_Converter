from pyproj import Transformer

transformer = Transformer.from_crs(
    "EPSG:27700",
    "EPSG:4326",
    always_xy=True
)

GRID = [
    ["SV","SW","SX","SY","SZ","TV","TW"],
    ["SQ","SR","SS","ST","SU","TQ","TR"],
    ["SL","SM","SN","SO","SP","TL","TM"],
    ["SF","SG","SH","SJ","SK","TF","TG"],
    ["SA","SB","SC","SD","SE","TA","TB"],
    ["NV","NW","NX","NY","NZ","OV","OW"],
    ["NQ","NR","NS","NT","NU","OQ","OR"],
    ["NL","NM","NN","NO","NP","OL","OM"],
    ["NF","NG","NH","NJ","NK","OF","OG"],
    ["NA","NB","NC","ND","NE","OA","OB"]
]

# ----------------------------
# GRID → EASTING/NORTHING
# ----------------------------
def gridref_to_en(gridref):

    gridref = gridref.replace(" ", "").upper()

    if len(gridref) < 4:
        return None

    letters = gridref[:2]
    digits = gridref[2:]

    for r in range(len(GRID)):
        for c in range(len(GRID[r])):
            if GRID[r][c] == letters:

                half = len(digits) // 2
                e_part = digits[:half]
                n_part = digits[half:]

                easting = c * 100000 + int(e_part.ljust(5, "0"))
                northing = (9 - r) * 100000 + int(n_part.ljust(5, "0"))

                return easting, northing

    return None


# ----------------------------
# EASTING/NORTHING → LAT/LON
# ----------------------------
def easting_northing_to_latlon(easting, northing):
    lon, lat = transformer.transform(easting, northing)
    return lat, lon


# ----------------------------
# UNIFIED CONVERSION FUNCTION
# ----------------------------
def convert(mode, easting=None, northing=None, gridref=None):

    if mode == "Easting / Northing":

        if easting is None or northing is None:
            return "Missing input values"

        lat, lon = easting_northing_to_latlon(float(easting), float(northing))
        return f"Latitude: {lat:.6f}, Longitude: {lon:.6f}"

    elif mode == "Grid Reference":

        result = gridref_to_en(gridref)

        if result is None:
            return "Invalid grid reference"

        e, n = result
        lat, lon = easting_northing_to_latlon(e, n)

        return f"Latitude: {lat:.6f}, Longitude: {lon:.6f}"

    else:
        return "Invalid mode"


# ----------------------------
# Folium MAP
# ----------------------------

import folium

def generate_map(lat, lon):
    """
    Generate an interactive Folium map centered on given coordinates.
    """

    m = folium.Map(location=[lat, lon], zoom_start=12)

    folium.Marker(
        [lat, lon],
        popup="Converted Location"
    ).add_to(m)

    return m._repr_html_()
