from dataclasses import dataclass


@dataclass(frozen=True)
class AnalogResult:
    measured_value: float
    current_ma: float
    bias: float
    scale: float
    raw_int16: int
    raw_hex16: str
    range_percent: float
    raw_percent: float
    out_of_scale: bool


def calculate_analog(lim_inf, lim_sup, range_inf, range_sup, value, input_mode="measured"):
    lim_inf_value = float(lim_inf)
    lim_sup_value = float(lim_sup)
    range_inf_value = float(range_inf)
    range_sup_value = float(range_sup)
    input_value = parse_analog_input(value, input_mode)

    range_span = range_sup_value - range_inf_value
    if range_span == 0:
        raise ValueError("Range superior deve ser diferente do range inferior.")

    if lim_sup_value == 0:
        raise ValueError("Limite superior deve ser diferente de zero.")

    current_span = lim_sup_value - lim_inf_value
    if current_span == 0:
        raise ValueError("Limite superior deve ser diferente do limite inferior.")

    if input_mode == "measured":
        measured_value = input_value
        current_ma = current_from_measured(
            measured_value,
            lim_inf_value,
            current_span,
            range_inf_value,
            range_span,
        )
    elif input_mode == "current_ma":
        current_ma = input_value
        measured_value = measured_from_current(
            current_ma,
            lim_inf_value,
            current_span,
            range_inf_value,
            range_span,
        )
    elif input_mode in ("raw_int16", "raw_hex16"):
        raw_from_input = input_value
        current_ma = current_from_raw(raw_from_input, lim_sup_value)
        measured_value = measured_from_current(
            current_ma,
            lim_inf_value,
            current_span,
            range_inf_value,
            range_span,
        )
    else:
        raise ValueError("Modo analogico invalido.")

    scale = lim_sup_value * range_span / current_span
    bias = range_sup_value - scale
    raw_int16 = int((current_ma / lim_sup_value) * (2**15 - 1))
    raw_hex16 = f"0x{raw_int16 & 0xFFFF:04x}"
    range_percent = ((measured_value - range_inf_value) / range_span) * 100
    raw_percent = (raw_int16 / (2**15 - 1)) * 100
    current_low = min(lim_inf_value, lim_sup_value)
    current_high = max(lim_inf_value, lim_sup_value)
    out_of_sensor_range = not current_low <= current_ma <= current_high
    out_of_raw_range = raw_int16 < 0 or raw_int16 > 32767
    out_of_scale = out_of_sensor_range or out_of_raw_range

    return AnalogResult(
        measured_value=measured_value,
        current_ma=current_ma,
        bias=bias,
        scale=scale,
        raw_int16=raw_int16,
        raw_hex16=raw_hex16,
        range_percent=range_percent,
        raw_percent=raw_percent,
        out_of_scale=out_of_scale,
    )


def parse_analog_input(value, input_mode):
    if input_mode == "raw_hex16":
        return parse_hex16_to_int(value)
    if input_mode == "raw_int16":
        return int(value)
    return float(value)


def parse_hex16_to_int(value):
    text = str(value).strip().lower()
    if text.startswith("0x"):
        text = text[2:]
    raw_value = int(text, 16)
    if raw_value > 0xFFFF:
        raise ValueError("HEX16 deve estar entre 0x0000 e 0xffff.")
    if raw_value > 0x7FFF:
        return raw_value - 0x10000
    return raw_value


def current_from_measured(
    measured_value,
    lim_inf_value,
    current_span,
    range_inf_value,
    range_span,
):
    return (
        ((measured_value - range_inf_value) * current_span / range_span)
        + lim_inf_value
    )


def measured_from_current(
    current_ma,
    lim_inf_value,
    current_span,
    range_inf_value,
    range_span,
):
    return ((current_ma - lim_inf_value) * range_span / current_span) + range_inf_value


def current_from_raw(raw_int16, lim_sup_value):
    return (raw_int16 * lim_sup_value) / (2**15 - 1)
