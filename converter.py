from pyproj import Transformer
import folium
# Add packages for cv export
import pandas as pd
import tempfile

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

    try:

        if mode == "Easting / Northing":

            if easting is None or northing is None:
                return "Error: Please enter both Easting and Northing values."

            try:
                easting = float(easting)
                northing = float(northing)
            except ValueError:
                return "Error: Easting and Northing must be numbers."

            lat, lon = easting_northing_to_latlon(easting, northing)
            return f"Latitude: {lat:.6f}, Longitude: {lon:.6f}"

        elif mode == "Grid Reference":

            if not gridref or len(gridref.strip()) < 4:
                return "Error: Invalid grid reference format."

            result = gridref_to_en(gridref)

            if result is None:
                return "Error: Grid reference not recognised."

            e, n = result
            lat, lon = easting_northing_to_latlon(e, n)

            return f"Latitude: {lat:.6f}, Longitude: {lon:.6f}"

        else:
            return "Error: Invalid conversion mode."

    except Exception as e:
        return f"Unexpected error: {str(e)}"

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

# ----------------------------
# CSV Export
# ----------------------------

def export_csv(mode, easting=None, northing=None, gridref=None, result_text=None):
    """
    Export conversion result to CSV file.
    """

    data = {
        "mode": mode,
        "input_easting": easting,
        "input_northing": northing,
        "input_gridref": gridref,
        "result": result_text
    }

    df = pd.DataFrame([data])

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    df.to_csv(tmp.name, index=False)
    tmp.close()

    return tmp.name
