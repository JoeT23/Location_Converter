import pytest
from converter import (
    easting_northing_to_latlon,
    gridref_to_en,
    convert
)

# ----------------------------
# TEST 1: Easting/Northing conversion
# ----------------------------
def test_easting_northing_to_latlon():
    lat, lon = easting_northing_to_latlon(530000, 180000)

    assert isinstance(lat, float)
    assert isinstance(lon, float)

    # sanity check (UK should be roughly in this range)
    assert 49 <= lat <= 61
    assert -10 <= lon <= 2


# ----------------------------
# TEST 2: Grid reference conversion (valid input)
# ----------------------------
def test_gridref_to_en_valid():
    result = gridref_to_en("TQ300800")

    assert result is not None

    e, n = result
    assert isinstance(e, (int, float))
    assert isinstance(n, (int, float))


# ----------------------------
# TEST 3: Grid reference conversion (invalid input)
# ----------------------------
def test_gridref_to_en_invalid():
    result = gridref_to_en("INVALID")

    assert result is None


# ----------------------------
# TEST 4: Unified convert function (E/N mode)
# ----------------------------
def test_convert_easting_mode():
    result = convert("Easting / Northing", 530000, 180000)

    assert "Latitude" in result


# ----------------------------
# TEST 5: Unified convert function (grid mode)
# ----------------------------
def test_convert_grid_mode():
    result = convert("Grid Reference", None, None, "TQ300800")

    assert "Latitude" in result
