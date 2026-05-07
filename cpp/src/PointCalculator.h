#pragma once

#include <QString>

struct PointResult {
    bool ok = false;
    int value = -1;
    QString message;
};

class PointCalculator final {
public:
    [[nodiscard]] static PointResult bitbyteFromPtno(const QString& value);
    [[nodiscard]] static PointResult ptnoFromBitbyte(const QString& value);

private:
    [[nodiscard]] static int parseInteger(const QString& value, bool* ok);
    [[nodiscard]] static int bitbyteFromPtnoValue(int ptno);
    [[nodiscard]] static int ptnoFromBitbyteValue(int bitbyte);
    [[nodiscard]] static QString ptnoMessage(int ptno);
    [[nodiscard]] static QString bitbyteMessage(int bitbyte);
    [[nodiscard]] static int bitbyteFromPtnoBlock(int value, int rangeStart, int resultOffset);
    [[nodiscard]] static int ptnoFromBitbyteBlock(int value, int rangeStart, int resultOffset);
};
