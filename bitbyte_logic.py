"""Java-compatible BitByte/PTNO calculations.

The original Java utility is not a strict mathematical inverse for every
supported value. SOSTAT identity points and 2WAY no timestamp points share part
of the BitByte space, so reverse conversion follows the Java behavior.
"""


def parse_input(value):
    if value is None:
        return -1
    try:
        return int(str(value).strip())
    except ValueError:
        return -1


def bitbyte_from_ptno(value):
    ptno = parse_input(value)
    if ptno < 0:
        return -1

    if 0 <= ptno <= 2047:
        return ptno
    if 10000 <= ptno <= 11023:
        return (ptno - 10000) * 2
    if 15000 <= ptno <= 16023:
        return ((ptno - 15000) * 2) + 2048
    if 25000 <= ptno <= 25063:
        return _bitbyte_from_ptno_block(ptno, 25000, 4608)
    if 36000 <= ptno <= 36063:
        return _bitbyte_from_ptno_block(ptno, 36000, 5632)
    if 36088 <= ptno <= 36095:
        return _bitbyte_from_ptno_block(ptno, 36088, 5808)

    return -1


def bitbyte_from_ptno_result(value):
    ptno = parse_input(value)
    result = bitbyte_from_ptno(value)

    if result < 0:
        return -1, _invalid_message(), "Erro"
    if 0 <= ptno <= 2047:
        return (
            result,
            "Calculadora para SOSTAT, verifique a SOANLG para pontos analogicos",
            "SOSTAT",
        )
    return result, "", "Resultado"


def ptno_from_bitbyte(value):
    bitbyte = parse_input(value)
    if bitbyte < 0:
        return -1

    if 0 <= bitbyte <= 2047:
        if bitbyte % 2 != 0:
            return -1
        return (bitbyte // 2) + 10000
    if 2048 <= bitbyte <= 4095:
        if bitbyte % 2 != 0:
            return -1
        return (bitbyte + 27952) // 2
    if 4608 <= bitbyte <= 4727:
        return _ptno_from_bitbyte_block(bitbyte, 4608, 20392)
    if 5632 <= bitbyte <= 5751:
        return _ptno_from_bitbyte_block(bitbyte, 5632, 30368)
    if 5808 <= bitbyte <= 5815:
        return 36088 + (bitbyte - 5808)
    if 7000 <= bitbyte <= 8192:
        return 0

    return -1


def ptno_from_bitbyte_result(value):
    bitbyte = parse_input(value)
    result = ptno_from_bitbyte(value)

    if result < 0:
        return -1, _invalid_message(), "Erro"
    if 0 <= bitbyte <= 2047:
        return result, "2WAY sem timestamp, verificar se e analogico", "Resultado"
    if 7000 <= bitbyte <= 8192:
        return result, "PseudoPoint retorna PTNO 0", "Atencao"
    return result, "", "Resultado"


def _bitbyte_from_ptno_block(value, range_start, result_offset):
    block = ((value - range_start) // 8) * 16
    offset = ((value - range_start) % 8) + result_offset
    return block + offset


def _ptno_from_bitbyte_block(value, range_start, result_offset):
    if ((value - range_start) % 16) > 7:
        return -1

    block = (value - range_start) // 16
    return (value + result_offset) - (8 * block)


def _invalid_message():
    return "Entrada invalida. Verifique valores e intervalos validos na documentacao."
