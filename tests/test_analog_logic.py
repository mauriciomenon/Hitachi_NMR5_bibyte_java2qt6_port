import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from analog_logic import calculate_analog


def test_calculate_analog_defaults_match_rawcounts_v12():
    result = calculate_analog(4, 20, 0, 10, 5)

    assert result.current_ma == 12.0
    assert result.bias == -2.5
    assert result.scale == 10
    assert result.raw_int16 == 19660
    assert result.raw_hex16 == "0x4ccc"


def test_calculate_analog_scaled_range_keeps_v12_formula():
    result = calculate_analog(4, 20, 0, 100, 50)

    assert result.current_ma == 12.0
    assert result.bias == -25.0
    assert result.scale == 100
    assert result.raw_int16 == 19660
    assert result.raw_hex16 == "0x4ccc"


def test_calculate_analog_uses_configured_current_limits():
    result = calculate_analog(0, 10, 0, 100, 5)

    assert result.current_ma == 0.5
    assert result.bias == 0.0
    assert result.scale == 100
    assert result.raw_int16 == 1638
    assert result.raw_hex16 == "0x0666"


def test_calculate_analog_formats_negative_raw_as_hex16():
    result = calculate_analog(4, 20, 0, 10, -5)

    assert result.raw_int16 < 0
    assert result.raw_hex16 == "0xe667"


def test_calculate_analog_rejects_zero_range_span():
    with pytest.raises(ValueError, match="Range superior"):
        calculate_analog(4, 20, 10, 10, 5)


def test_calculate_analog_rejects_zero_current_span():
    with pytest.raises(ValueError, match="Limite superior"):
        calculate_analog(4, 4, 0, 10, 5)
