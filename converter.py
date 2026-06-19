# Add easting and northing function to the grid ref function
from pyproj import Transformer

# ----------------------------
# Transformer (BNG → WGS84)
# ----------------------------
transformer = Transformer.from_crs(
    "EPSG:27700",
    "EPSG:4326",
    always_xy=True
)

# ----------------------------
# GRID SYSTEM (simplified UK grid)
# ----------------------------
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
    """
    Convert UK grid reference (e.g. TQ300800) to easting/northing.
    """

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
