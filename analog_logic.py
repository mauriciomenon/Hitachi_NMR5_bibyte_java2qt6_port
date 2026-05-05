from dataclasses import dataclass


@dataclass(frozen=True)
class AnalogResult:
    current_ma: float
    bias: float
    scale: float
    raw_int16: int
    raw_hex16: str


def calculate_analog(lim_inf, lim_sup, range_inf, range_sup, measured):
    lim_inf_value = float(lim_inf)
    lim_sup_value = float(lim_sup)
    range_inf_value = float(range_inf)
    range_sup_value = float(range_sup)
    measured_value = float(measured)

    range_span = range_sup_value - range_inf_value
    if range_span == 0:
        raise ValueError("Range superior deve ser diferente do range inferior.")

    current_ma = (
        (measured_value - range_inf_value)
        * (lim_sup_value - lim_inf_value)
        / range_span
        + lim_inf_value
    )
    current_span = lim_sup_value - lim_inf_value
    if current_span == 0:
        raise ValueError("Limite superior deve ser diferente do limite inferior.")

    bias = ((lim_sup_value * range_inf_value) - (lim_inf_value * range_sup_value)) / current_span
    scale = range_sup_value
    raw_int16 = int((current_ma / lim_sup_value) * (2**15 - 1))
    raw_hex16 = f"0x{raw_int16 & 0xFFFF:04x}"

    return AnalogResult(
        current_ma=current_ma,
        bias=bias,
        scale=scale,
        raw_int16=raw_int16,
        raw_hex16=raw_hex16,
    )
