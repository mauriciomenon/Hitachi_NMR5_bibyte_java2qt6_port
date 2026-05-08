#include "AppBackend.h"

#include "AnalogCalculator.h"
#include "PointCalculator.h"

namespace {

struct ParsedAnalogInput {
    bool ok = false;
    QString error;
    double limInf = 0.0;
    double limSup = 0.0;
    double rangeInf = 0.0;
    double rangeSup = 0.0;
    double inputValue = 0.0;
    AnalogInputMode mode = AnalogInputMode::Measured;
};

int parseHex16ToInt(const QString& value, bool* ok)
{
    QString text = value.trimmed().toLower();
    if (text.startsWith(QStringLiteral("0x"))) {
        text = text.mid(2);
    }
    const int rawValue = text.toInt(ok, 16);
    if (!*ok || rawValue > AnalogCalculator::RawMax) {
        *ok = false;
        return 0;
    }
    return rawValue;
}

QString formatRawHex(int rawInt)
{
    return QStringLiteral("0x%1").arg(rawInt & 0xFFFF, 4, 16, QLatin1Char('0'));
}

ParsedAnalogInput parseAnalogInput(
    const QString& limInf,
    const QString& limSup,
    const QString& rangeInf,
    const QString& rangeSup,
    const QString& value,
    const QString& inputMode)
{
    ParsedAnalogInput parsed;
    bool ok = false;
    parsed.limInf = limInf.toDouble(&ok);
    if (!ok) {
        parsed.error = QStringLiteral("Limite inferior invalido");
        return parsed;
    }
    parsed.limSup = limSup.toDouble(&ok);
    if (!ok) {
        parsed.error = QStringLiteral("Limite superior invalido");
        return parsed;
    }
    parsed.rangeInf = rangeInf.toDouble(&ok);
    if (!ok) {
        parsed.error = QStringLiteral("Range inferior invalido");
        return parsed;
    }
    parsed.rangeSup = rangeSup.toDouble(&ok);
    if (!ok) {
        parsed.error = QStringLiteral("Range superior invalido");
        return parsed;
    }

    if (inputMode == QStringLiteral("measured")) {
        parsed.mode = AnalogInputMode::Measured;
        parsed.inputValue = value.toDouble(&ok);
        parsed.error = ok ? QString() : QStringLiteral("Valor medido invalido");
    } else if (inputMode == QStringLiteral("current_ma")) {
        parsed.mode = AnalogInputMode::CurrentMa;
        parsed.inputValue = value.toDouble(&ok);
        parsed.error = ok ? QString() : QStringLiteral("Valor mA invalido");
    } else if (inputMode == QStringLiteral("raw_hex16")) {
        parsed.mode = AnalogInputMode::RawHex16;
        parsed.inputValue = parseHex16ToInt(value, &ok);
        parsed.error = ok ? QString() : QStringLiteral("Valor raw invalido");
    } else if (inputMode == QStringLiteral("raw_int16")) {
        parsed.mode = AnalogInputMode::RawInt16;
        parsed.inputValue = value.toInt(&ok);
        if (parsed.inputValue < 0 || parsed.inputValue > AnalogCalculator::RawMax) {
            ok = false;
        }
        parsed.error = ok ? QString() : QStringLiteral("Valor raw invalido");
    } else {
        parsed.error = QStringLiteral("Modo analogico invalido");
        return parsed;
    }
    parsed.ok = ok;
    return parsed;
}

} // namespace

AppBackend::AppBackend(QObject* parent)
    : QObject(parent)
{
}

QVariantMap AppBackend::makeError(const QString& message)
{
    return {
        {QStringLiteral("ok"), false},
        {QStringLiteral("message"), message},
    };
}

QVariantMap AppBackend::pointResultMap(const PointResult& result)
{
    if (!result.ok) {
        return makeError(result.message);
    }
    return {
        {QStringLiteral("ok"), true},
        {QStringLiteral("value"), result.value},
        {QStringLiteral("message"), result.message},
        {QStringLiteral("display"), result.message.isEmpty()
            ? QString::number(result.value)
            : QStringLiteral("%1 (%2)").arg(result.value).arg(result.message)},
    };
}

QVariantMap AppBackend::bitbyteFromPtno(const QString& value) const
{
    return pointResultMap(PointCalculator::bitbyteFromPtno(value));
}

QVariantMap AppBackend::ptnoFromBitbyte(const QString& value) const
{
    return pointResultMap(PointCalculator::ptnoFromBitbyte(value));
}

QVariantMap AppBackend::calculateAnalog(
    const QString& limInf,
    const QString& limSup,
    const QString& rangeInf,
    const QString& rangeSup,
    const QString& value,
    const QString& inputMode) const
{
    const ParsedAnalogInput parsed = parseAnalogInput(
        limInf, limSup, rangeInf, rangeSup, value, inputMode);
    if (!parsed.ok) {
        return makeError(parsed.error);
    }

    const auto result = AnalogCalculator::calculate(
        parsed.limInf,
        parsed.limSup,
        parsed.rangeInf,
        parsed.rangeSup,
        parsed.inputValue,
        parsed.mode);
    if (!result.ok) {
        return makeError(result.error);
    }

    return {
        {QStringLiteral("ok"), true},
        {QStringLiteral("measured"), result.measured},
        {QStringLiteral("current"), result.current},
        {QStringLiteral("bias"), result.bias},
        {QStringLiteral("scale"), result.scale},
        {QStringLiteral("rawInt"), result.rawInt},
        {QStringLiteral("rawHex"), formatRawHex(result.rawInt)},
        {QStringLiteral("rangePercent"), result.rangePercent},
        {QStringLiteral("rawPercent"), result.rawPercent},
        {QStringLiteral("outOfScale"), result.outOfScale},
    };
}
