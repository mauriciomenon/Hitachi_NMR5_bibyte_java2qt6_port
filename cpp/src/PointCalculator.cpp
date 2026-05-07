#include "PointCalculator.h"

namespace {

constexpr int kSostatPtnoMin = 0;
constexpr int kSostatPtnoMax = 2047;
constexpr int kSostatBitbyteBase = 8193;
constexpr int kDigitalBitbyteMin = 0;
constexpr int kDigitalBitbyteMax = 2047;
constexpr int kDigitalPtnoMin = 10000;
constexpr int kDigitalPtnoMax = 11023;
constexpr int kDigitalAnalogPtnoMin = 15000;
constexpr int kDigitalAnalogPtnoMax = 16023;
constexpr int kDigitalAnalogBitbyteBase = 2048;
constexpr int kDigitalAnalogBitbyteMax = 4095;
constexpr int kBlock1PtnoMin = 25000;
constexpr int kBlock1PtnoMax = 25063;
constexpr int kBlock1BitbyteBase = 4608;
constexpr int kBlock1BitbyteMax = 4727;
constexpr int kBlock1ReverseOffset = 20392;
constexpr int kBlock2PtnoMin = 36000;
constexpr int kBlock2PtnoMax = 36063;
constexpr int kBlock2BitbyteBase = 5632;
constexpr int kBlock2BitbyteMax = 5751;
constexpr int kBlock2ReverseOffset = 30368;
constexpr int kBlock3PtnoMin = 36088;
constexpr int kBlock3PtnoMax = 36095;
constexpr int kBlock3BitbyteBase = 5808;
constexpr int kBlock3BitbyteMax = 5815;
constexpr int kPseudoBitbyteMin = 7000;
constexpr int kPseudoBitbyteMax = 8192;
constexpr int kPseudoPtnoBase = 50000;

} // namespace

int PointCalculator::parseInteger(const QString& value, bool* ok)
{
    const int parsed = value.trimmed().toInt(ok);
    return *ok ? parsed : -1;
}

int PointCalculator::bitbyteFromPtnoBlock(int value, int rangeStart, int resultOffset)
{
    const int block = ((value - rangeStart) / 8) * 16;
    const int offset = ((value - rangeStart) % 8) + resultOffset;
    return block + offset;
}

int PointCalculator::ptnoFromBitbyteBlock(int value, int rangeStart, int resultOffset)
{
    if (((value - rangeStart) % 16) > 7) {
        return -1;
    }
    const int block = (value - rangeStart) / 16;
    return (value + resultOffset) - (8 * block);
}

int PointCalculator::bitbyteFromPtnoValue(int ptno)
{
    if (ptno >= kSostatPtnoMin && ptno <= kSostatPtnoMax) {
        return kSostatBitbyteBase + ptno;
    }
    if (ptno >= kDigitalPtnoMin && ptno <= kDigitalPtnoMax) {
        return (ptno - kDigitalPtnoMin) * 2;
    }
    if (ptno >= kDigitalAnalogPtnoMin && ptno <= kDigitalAnalogPtnoMax) {
        return ((ptno - kDigitalAnalogPtnoMin) * 2) + kDigitalAnalogBitbyteBase;
    }
    if (ptno >= kBlock1PtnoMin && ptno <= kBlock1PtnoMax) {
        return bitbyteFromPtnoBlock(ptno, kBlock1PtnoMin, kBlock1BitbyteBase);
    }
    if (ptno >= kBlock2PtnoMin && ptno <= kBlock2PtnoMax) {
        return bitbyteFromPtnoBlock(ptno, kBlock2PtnoMin, kBlock2BitbyteBase);
    }
    if (ptno >= kBlock3PtnoMin && ptno <= kBlock3PtnoMax) {
        return bitbyteFromPtnoBlock(ptno, kBlock3PtnoMin, kBlock3BitbyteBase);
    }
    if (ptno >= kPseudoPtnoBase && ptno <= kPseudoPtnoBase + (kPseudoBitbyteMax - kPseudoBitbyteMin)) {
        return kPseudoBitbyteMin + (ptno - kPseudoPtnoBase);
    }
    return -1;
}

int PointCalculator::ptnoFromBitbyteValue(int bitbyte)
{
    if (bitbyte >= kDigitalBitbyteMin && bitbyte <= kDigitalBitbyteMax) {
        return bitbyte % 2 == 0 ? (bitbyte / 2) + kDigitalPtnoMin : -1;
    }
    if (bitbyte >= kDigitalAnalogBitbyteBase && bitbyte <= kDigitalAnalogBitbyteMax) {
        return bitbyte % 2 == 0
            ? ((bitbyte - kDigitalAnalogBitbyteBase) / 2) + kDigitalAnalogPtnoMin
            : -1;
    }
    if (bitbyte >= kBlock1BitbyteBase && bitbyte <= kBlock1BitbyteMax) {
        return ptnoFromBitbyteBlock(bitbyte, kBlock1BitbyteBase, kBlock1ReverseOffset);
    }
    if (bitbyte >= kBlock2BitbyteBase && bitbyte <= kBlock2BitbyteMax) {
        return ptnoFromBitbyteBlock(bitbyte, kBlock2BitbyteBase, kBlock2ReverseOffset);
    }
    if (bitbyte >= kBlock3BitbyteBase && bitbyte <= kBlock3BitbyteMax) {
        return kBlock3PtnoMin + (bitbyte - kBlock3BitbyteBase);
    }
    if (bitbyte >= kPseudoBitbyteMin && bitbyte <= kPseudoBitbyteMax) {
        return kPseudoPtnoBase + (bitbyte - kPseudoBitbyteMin);
    }
    if (bitbyte >= kSostatBitbyteBase && bitbyte <= kSostatBitbyteBase + kSostatPtnoMax) {
        return bitbyte - kSostatBitbyteBase;
    }
    return -1;
}

QString PointCalculator::ptnoMessage(int ptno)
{
    if (ptno <= kSostatPtnoMax) {
        return QStringLiteral("SOSTAT");
    }
    if (ptno >= kDigitalPtnoMin && ptno <= kDigitalPtnoMax) {
        return QStringLiteral("2WAY sem timestamp");
    }
    if (ptno >= kPseudoPtnoBase && ptno <= kPseudoPtnoBase + (kPseudoBitbyteMax - kPseudoBitbyteMin)) {
        return QStringLiteral("PseudoPoint");
    }
    return {};
}

QString PointCalculator::bitbyteMessage(int bitbyte)
{
    if (bitbyte <= kDigitalBitbyteMax) {
        return QStringLiteral("2WAY sem timestamp");
    }
    if (bitbyte >= kPseudoBitbyteMin && bitbyte <= kPseudoBitbyteMax) {
        return QStringLiteral("PseudoPoint");
    }
    if (bitbyte >= kSostatBitbyteBase && bitbyte <= kSostatBitbyteBase + kSostatPtnoMax) {
        return QStringLiteral("SOSTAT");
    }
    return {};
}

PointResult PointCalculator::bitbyteFromPtno(const QString& value)
{
    bool ok = false;
    const int ptno = parseInteger(value, &ok);
    if (!ok || ptno < 0) {
        return {.ok = false, .message = QStringLiteral("Entrada invalida")};
    }

    const int result = bitbyteFromPtnoValue(ptno);
    if (result < 0) {
        return {.ok = false, .message = QStringLiteral("Entrada fora dos intervalos validos")};
    }

    return {.ok = true, .value = result, .message = ptnoMessage(ptno)};
}

PointResult PointCalculator::ptnoFromBitbyte(const QString& value)
{
    bool ok = false;
    const int bitbyte = parseInteger(value, &ok);
    if (!ok || bitbyte < 0) {
        return {.ok = false, .message = QStringLiteral("Entrada invalida")};
    }

    const int result = ptnoFromBitbyteValue(bitbyte);
    if (result < 0) {
        return {.ok = false, .message = QStringLiteral("Entrada fora dos intervalos validos")};
    }

    return {.ok = true, .value = result, .message = bitbyteMessage(bitbyte)};
}
