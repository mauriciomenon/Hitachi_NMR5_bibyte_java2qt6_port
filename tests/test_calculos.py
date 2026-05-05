import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bitbyte_logic import bitbyte_from_ptno, ptno_from_bitbyte


def test_calculo_1_valid_ranges():
    assert bitbyte_from_ptno("100") == 100
    assert bitbyte_from_ptno("10100") == 200
    assert bitbyte_from_ptno("15100") == 2248
    assert bitbyte_from_ptno("25008") == 4624
    assert bitbyte_from_ptno("36008") == 5648
    assert bitbyte_from_ptno("36088") == 5808
    assert bitbyte_from_ptno("36095") == 5815


def test_calculo_1_invalid_ranges():
    for value in ("invalid", "-1", "2050", "12000", "20000", "36070", "40000"):
        assert bitbyte_from_ptno(value) == -1


def test_calculo_2_valid_ranges():
    assert ptno_from_bitbyte("0") == 10000
    assert ptno_from_bitbyte("200") == 10100
    assert ptno_from_bitbyte("2046") == 11023
    assert ptno_from_bitbyte("2248") == 15100
    assert ptno_from_bitbyte("4608") == 25000
    assert ptno_from_bitbyte("4624") == 25008
    assert ptno_from_bitbyte("4727") == 25063
    assert ptno_from_bitbyte("5632") == 36000
    assert ptno_from_bitbyte("5648") == 36008
    assert ptno_from_bitbyte("5751") == 36063
    assert ptno_from_bitbyte("5808") == 36088
    assert ptno_from_bitbyte("5815") == 36095
    assert ptno_from_bitbyte("7000") == 0


def test_calculo_2_invalid_ranges():
    for value in (
        "invalid",
        "-5",
        "1",
        "2047",
        "2049",
        "4616",
        "4736",
        "5760",
        "5816",
        "9000",
    ):
        assert ptno_from_bitbyte(value) == -1


def test_trimmed_and_none_inputs():
    assert bitbyte_from_ptno(" 15100 ") == 2248
    assert ptno_from_bitbyte("\t2248\n") == 15100
    assert bitbyte_from_ptno(None) == -1
    assert ptno_from_bitbyte(None) == -1


def test_java_compatible_collision_is_intentional():
    assert bitbyte_from_ptno("100") == 100
    assert bitbyte_from_ptno("10050") == 100
    assert ptno_from_bitbyte("100") == 10050
