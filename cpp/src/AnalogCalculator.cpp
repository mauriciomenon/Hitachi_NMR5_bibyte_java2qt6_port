#include "AnalogCalculator.h"

#include <QtMath>

namespace {

AnalogResult errorResult(const QString& message)
{
    return {.ok = false, .error = message};
}

} // namespace

AnalogResult AnalogCalculator::calculate(
    double limInfValue,
    double limSupValue,
    double rangeInfValue,
    double rangeSupValue,
    double inputValue,
    AnalogInputMode inputMode)
{
    const double rangeSpan = rangeSupValue - rangeInfValue;
    const double currentSpan = limSupValue - limInfValue;
    if (qFuzzyIsNull(rangeSpan)) {
        return errorResult(QStringLiteral("Range superior deve ser diferente do inferior"));
    }
    if (qFuzzyIsNull(currentSpan)) {
        return errorResult(QStringLiteral("Limites de corrente invalidos"));
    }

    double measuredValue = 0.0;
    double currentMa = 0.0;
    if (inputMode == AnalogInputMode::Measured) {
        measuredValue = inputValue;
        currentMa = ((measuredValue - rangeInfValue) * currentSpan / rangeSpan) + limInfValue;
    } else if (inputMode == AnalogInputMode::CurrentMa) {
        currentMa = inputValue;
    } else {
        currentMa = limInfValue + ((inputValue / RawMax) * currentSpan);
    }
    if (inputMode != AnalogInputMode::Measured) {
        measuredValue = ((currentMa - limInfValue) * rangeSpan / currentSpan) + rangeInfValue;
    }

    const double scale = rangeSpan / currentSpan;
    const double bias = rangeInfValue - (scale * limInfValue);
    const int rawInt = static_cast<int>(((currentMa - limInfValue) / currentSpan) * RawMax);
    const double currentLow = qMin(limInfValue, limSupValue);
    const double currentHigh = qMax(limInfValue, limSupValue);

    return {
        .ok = true,
        .measured = measuredValue,
        .current = currentMa,
        .bias = bias,
        .scale = scale,
        .rawInt = rawInt,
        .rangePercent = ((measuredValue - rangeInfValue) / rangeSpan) * 100.0,
        .rawPercent = (static_cast<double>(rawInt) / RawMax) * 100.0,
        .outOfScale = currentMa < currentLow || currentMa > currentHigh
            || rawInt < 0 || rawInt > RawMax,
    };
}
