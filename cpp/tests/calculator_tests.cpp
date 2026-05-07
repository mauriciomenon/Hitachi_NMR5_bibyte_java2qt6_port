#include "AnalogCalculator.h"
#include "PointCalculator.h"

#include <QtTest/QtTest>

#include <cmath>

namespace {

void expectNear(double actual, double expected, double epsilon)
{
    QVERIFY2(std::abs(actual - expected) <= epsilon, qPrintable(QStringLiteral("expected %1, got %2")
        .arg(expected, 0, 'f', 6)
        .arg(actual, 0, 'f', 6)));
}

} // namespace

class CalculatorTests final : public QObject {
    Q_OBJECT

private slots:
    void analogMeasuredInput();
    void analogCurrentInput();
    void analogRawInput();
    void analogInvalidRanges();
    void pointSostat();
    void pointDigital();
    void pointBlock();
    void pointPseudoAndInvalidText();
};

void CalculatorTests::analogMeasuredInput()
{
    const AnalogResult result = AnalogCalculator::calculate(4.0, 20.0, 0.0, 10.0, 5.0, AnalogInputMode::Measured);
    QVERIFY(result.ok);
    expectNear(result.measured, 5.0, 0.0001);
    expectNear(result.current, 12.0, 0.0001);
    expectNear(result.bias, -2.5, 0.0001);
    expectNear(result.scale, 0.625, 0.0001);
    QCOMPARE(result.rawInt, 16383);
    QCOMPARE(result.rawHex, QStringLiteral("0x3fff"));
    expectNear(result.rangePercent, 50.0, 0.0001);
    QVERIFY(!result.outOfScale);
}

void CalculatorTests::analogCurrentInput()
{
    const AnalogResult result = AnalogCalculator::calculate(4.0, 20.0, 0.0, 10.0, 12.0, AnalogInputMode::CurrentMa);
    QVERIFY(result.ok);
    expectNear(result.measured, 5.0, 0.0001);
    expectNear(result.current, 12.0, 0.0001);
    QCOMPARE(result.rawInt, 16383);
}

void CalculatorTests::analogRawInput()
{
    const AnalogResult result = AnalogCalculator::calculate(4.0, 20.0, 0.0, 10.0, 16383.0, AnalogInputMode::RawInt16);
    QVERIFY(result.ok);
    expectNear(result.measured, 4.9998, 0.001);
    expectNear(result.current, 11.9998, 0.001);
    QCOMPARE(result.rawInt, 16383);
    QCOMPARE(result.rawHex, QStringLiteral("0x3fff"));
}

void CalculatorTests::analogInvalidRanges()
{
    const AnalogResult rangeResult = AnalogCalculator::calculate(4.0, 20.0, 10.0, 10.0, 5.0, AnalogInputMode::Measured);
    QVERIFY(!rangeResult.ok);
    QCOMPARE(rangeResult.error, QStringLiteral("Range superior deve ser diferente do inferior"));

    const AnalogResult currentResult = AnalogCalculator::calculate(4.0, 4.0, 0.0, 10.0, 5.0, AnalogInputMode::Measured);
    QVERIFY(!currentResult.ok);
    QCOMPARE(currentResult.error, QStringLiteral("Limites de corrente invalidos"));
}

void CalculatorTests::pointSostat()
{
    const PointResult bitbyte = PointCalculator::bitbyteFromPtno(QStringLiteral("0"));
    QVERIFY(bitbyte.ok);
    QCOMPARE(bitbyte.value, 8193);
    QCOMPARE(bitbyte.message, QStringLiteral("SOSTAT"));

    const PointResult ptno = PointCalculator::ptnoFromBitbyte(QStringLiteral("8193"));
    QVERIFY(ptno.ok);
    QCOMPARE(ptno.value, 0);
    QCOMPARE(ptno.message, QStringLiteral("SOSTAT"));
}

void CalculatorTests::pointDigital()
{
    const PointResult bitbyte = PointCalculator::bitbyteFromPtno(QStringLiteral("10000"));
    QVERIFY(bitbyte.ok);
    QCOMPARE(bitbyte.value, 0);
    QCOMPARE(bitbyte.message, QStringLiteral("2WAY sem timestamp"));

    const PointResult ptno = PointCalculator::ptnoFromBitbyte(QStringLiteral("0"));
    QVERIFY(ptno.ok);
    QCOMPARE(ptno.value, 10000);
    QCOMPARE(ptno.message, QStringLiteral("2WAY sem timestamp"));

    const PointResult invalid = PointCalculator::ptnoFromBitbyte(QStringLiteral("1"));
    QVERIFY(!invalid.ok);
    QCOMPARE(invalid.message, QStringLiteral("Entrada fora dos intervalos validos"));
}

void CalculatorTests::pointBlock()
{
    const PointResult first = PointCalculator::bitbyteFromPtno(QStringLiteral("25000"));
    QVERIFY(first.ok);
    QCOMPARE(first.value, 4608);

    const PointResult lastInByte = PointCalculator::bitbyteFromPtno(QStringLiteral("25007"));
    QVERIFY(lastInByte.ok);
    QCOMPARE(lastInByte.value, 4615);

    const PointResult nextBlock = PointCalculator::bitbyteFromPtno(QStringLiteral("25008"));
    QVERIFY(nextBlock.ok);
    QCOMPARE(nextBlock.value, 4624);

    const PointResult ptno = PointCalculator::ptnoFromBitbyte(QStringLiteral("4615"));
    QVERIFY(ptno.ok);
    QCOMPARE(ptno.value, 25007);

    const PointResult invalid = PointCalculator::ptnoFromBitbyte(QStringLiteral("4616"));
    QVERIFY(!invalid.ok);
    QCOMPARE(invalid.message, QStringLiteral("Entrada fora dos intervalos validos"));
}

void CalculatorTests::pointPseudoAndInvalidText()
{
    const PointResult bitbyte = PointCalculator::bitbyteFromPtno(QStringLiteral("50000"));
    QVERIFY(bitbyte.ok);
    QCOMPARE(bitbyte.value, 7000);
    QCOMPARE(bitbyte.message, QStringLiteral("PseudoPoint"));

    const PointResult ptno = PointCalculator::ptnoFromBitbyte(QStringLiteral("7000"));
    QVERIFY(ptno.ok);
    QCOMPARE(ptno.value, 50000);
    QCOMPARE(ptno.message, QStringLiteral("PseudoPoint"));

    const PointResult invalid = PointCalculator::bitbyteFromPtno(QStringLiteral("abc"));
    QVERIFY(!invalid.ok);
    QCOMPARE(invalid.message, QStringLiteral("Entrada invalida"));
}

QTEST_APPLESS_MAIN(CalculatorTests)

#include "calculator_tests.moc"
