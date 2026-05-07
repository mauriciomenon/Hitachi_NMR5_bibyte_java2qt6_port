#pragma once

#include <QString>

struct AnalogResult {
    bool ok = false;
    QString error;
    double measured = 0.0;
    double current = 0.0;
    double bias = 0.0;
    double scale = 0.0;
    int rawInt = 0;
    QString rawHex;
    double rangePercent = 0.0;
    double rawPercent = 0.0;
    bool outOfScale = false;
};

enum class AnalogInputMode {
    Measured,
    CurrentMa,
    RawInt16,
    RawHex16,
};

class AnalogCalculator final {
public:
    [[nodiscard]] static AnalogResult calculate(
        double limInf,
        double limSup,
        double rangeInf,
        double rangeSup,
        double inputValue,
        AnalogInputMode inputMode);
};
