#include "AnalogCalculator.h"
#include "AppBackend.h"
#include "PointCalculator.h"
#include "TableData.h"

#include <QtTest/QtTest>

#include <QTemporaryDir>
#include <QFile>

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
    void backendAnalogModeIds();
    void analogRawBoundaries();
    void backendAcceptsDotDecimalInput();
    void backendAcceptsCommaDecimalInput();
    void backendRejectsInvalidRaw();
    void pointBoundaryCases();
    void pointSostat();
    void pointDigital();
    void pointBlock();
    void pointPseudoAndInvalidText();
    void tableDataLoadsCsvRows();
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

void CalculatorTests::backendAnalogModeIds()
{
    const AppBackend backend;
    const QVariantList modeOptions = backend.analogModeOptions();
    QCOMPARE(modeOptions.size(), 4);
    QCOMPARE(modeOptions.first().toMap().value(QStringLiteral("mode")).toString(), backend.analogModeMeasured());

    const QVariantMap measured = backend.calculateAnalog(
        QStringLiteral("4"),
        QStringLiteral("20"),
        QStringLiteral("0"),
        QStringLiteral("10"),
        QStringLiteral("5"),
        QStringLiteral("measured"));
    QVERIFY(measured.value(QStringLiteral("ok")).toBool());
    QCOMPARE(measured.value(QStringLiteral("rawHex")).toString(), QStringLiteral("0x3fff"));

    const QVariantMap current = backend.calculateAnalog(
        QStringLiteral("4"),
        QStringLiteral("20"),
        QStringLiteral("0"),
        QStringLiteral("10"),
        QStringLiteral("12"),
        QStringLiteral("current_ma"));
    QVERIFY(current.value(QStringLiteral("ok")).toBool());
    QCOMPARE(current.value(QStringLiteral("rawInt")).toInt(), 16383);

    const QVariantMap invalid = backend.calculateAnalog(
        QStringLiteral("4"),
        QStringLiteral("20"),
        QStringLiteral("0"),
        QStringLiteral("10"),
        QStringLiteral("5"),
        QStringLiteral("Medido"));
    QVERIFY(!invalid.value(QStringLiteral("ok")).toBool());
    QCOMPARE(invalid.value(QStringLiteral("message")).toString(), QStringLiteral("Modo analogico invalido"));
}

void CalculatorTests::analogRawBoundaries()
{
    const AnalogResult low = AnalogCalculator::calculate(4.0, 20.0, 0.0, 10.0, 0.0, AnalogInputMode::RawInt16);
    QVERIFY(low.ok);
    expectNear(low.measured, 0.0, 0.0001);
    expectNear(low.current, 4.0, 0.0001);
    QCOMPARE(low.rawInt, 0);
    expectNear(low.rawPercent, 0.0, 0.0001);
    QVERIFY(!low.outOfScale);

    const AnalogResult high = AnalogCalculator::calculate(
        4.0, 20.0, 0.0, 10.0, AnalogCalculator::RawMax, AnalogInputMode::RawInt16);
    QVERIFY(high.ok);
    expectNear(high.measured, 10.0, 0.0001);
    expectNear(high.current, 20.0, 0.0001);
    QCOMPARE(high.rawInt, AnalogCalculator::RawMax);
    expectNear(high.rawPercent, 100.0, 0.0001);
    QVERIFY(!high.outOfScale);

    const AnalogResult out = AnalogCalculator::calculate(4.0, 20.0, 0.0, 10.0, 20.0, AnalogInputMode::Measured);
    QVERIFY(out.ok);
    QVERIFY(out.outOfScale);
}

void CalculatorTests::backendAcceptsDotDecimalInput()
{
    const AppBackend backend;
    const QVariantMap result = backend.calculateAnalog(
        QStringLiteral("4.0"),
        QStringLiteral("20.0"),
        QStringLiteral("0.0"),
        QStringLiteral("10.0"),
        QStringLiteral("5.5"),
        QStringLiteral("measured"));

    QVERIFY(result.value(QStringLiteral("ok")).toBool());
    QCOMPARE(result.value(QStringLiteral("rawHex")).toString(), QStringLiteral("0x4665"));
}

void CalculatorTests::backendAcceptsCommaDecimalInput()
{
    const AppBackend backend;
    const QVariantMap result = backend.calculateAnalog(
        QStringLiteral("4,0"),
        QStringLiteral("20,0"),
        QStringLiteral("0,0"),
        QStringLiteral("10,0"),
        QStringLiteral("5,5"),
        backend.analogModeMeasured());

    QVERIFY(result.value(QStringLiteral("ok")).toBool());
    QCOMPARE(result.value(QStringLiteral("rawHex")).toString(), QStringLiteral("0x4665"));
}

void CalculatorTests::backendRejectsInvalidRaw()
{
    const AppBackend backend;
    const QVariantMap highHex = backend.calculateAnalog(
        QStringLiteral("4"),
        QStringLiteral("20"),
        QStringLiteral("0"),
        QStringLiteral("10"),
        QStringLiteral("0x8000"),
        QStringLiteral("raw_hex16"));
    QVERIFY(!highHex.value(QStringLiteral("ok")).toBool());
    QCOMPARE(highHex.value(QStringLiteral("message")).toString(), QStringLiteral("Valor raw invalido"));

    const QVariantMap highInt = backend.calculateAnalog(
        QStringLiteral("4"),
        QStringLiteral("20"),
        QStringLiteral("0"),
        QStringLiteral("10"),
        QString::number(AnalogCalculator::RawMax + 1),
        QStringLiteral("raw_int16"));
    QVERIFY(!highInt.value(QStringLiteral("ok")).toBool());
    QCOMPARE(highInt.value(QStringLiteral("message")).toString(), QStringLiteral("Valor raw invalido"));
}

void CalculatorTests::pointBoundaryCases()
{
    const PointResult sostatMax = PointCalculator::bitbyteFromPtno(QStringLiteral("2047"));
    QVERIFY(sostatMax.ok);
    QCOMPARE(sostatMax.value, 10240);
    const PointResult sostatMaxReverse = PointCalculator::ptnoFromBitbyte(QStringLiteral("10240"));
    QVERIFY(sostatMaxReverse.ok);
    QCOMPARE(sostatMaxReverse.value, 2047);

    const PointResult digitalMax = PointCalculator::bitbyteFromPtno(QStringLiteral("11023"));
    QVERIFY(digitalMax.ok);
    QCOMPARE(digitalMax.value, 2046);
    const PointResult digitalMaxReverse = PointCalculator::ptnoFromBitbyte(QStringLiteral("2046"));
    QVERIFY(digitalMaxReverse.ok);
    QCOMPARE(digitalMaxReverse.value, 11023);

    const PointResult digitalAnalogMin = PointCalculator::bitbyteFromPtno(QStringLiteral("15000"));
    QVERIFY(digitalAnalogMin.ok);
    QCOMPARE(digitalAnalogMin.value, 2048);
    const PointResult digitalAnalogMax = PointCalculator::bitbyteFromPtno(QStringLiteral("16023"));
    QVERIFY(digitalAnalogMax.ok);
    QCOMPARE(digitalAnalogMax.value, 4094);
    const PointResult digitalAnalogOdd = PointCalculator::ptnoFromBitbyte(QStringLiteral("2049"));
    QVERIFY(!digitalAnalogOdd.ok);

    const PointResult block2Max = PointCalculator::bitbyteFromPtno(QStringLiteral("36063"));
    QVERIFY(block2Max.ok);
    QCOMPARE(block2Max.value, 5751);
    const PointResult block2Reverse = PointCalculator::ptnoFromBitbyte(QStringLiteral("5751"));
    QVERIFY(block2Reverse.ok);
    QCOMPARE(block2Reverse.value, 36063);

    const PointResult block3Min = PointCalculator::bitbyteFromPtno(QStringLiteral("36088"));
    QVERIFY(block3Min.ok);
    QCOMPARE(block3Min.value, 5808);
    const PointResult block3Max = PointCalculator::bitbyteFromPtno(QStringLiteral("36095"));
    QVERIFY(block3Max.ok);
    QCOMPARE(block3Max.value, 5815);

    const PointResult pseudoMax = PointCalculator::bitbyteFromPtno(QStringLiteral("51192"));
    QVERIFY(pseudoMax.ok);
    QCOMPARE(pseudoMax.value, 8192);
    const PointResult pseudoMaxReverse = PointCalculator::ptnoFromBitbyte(QStringLiteral("8192"));
    QVERIFY(pseudoMaxReverse.ok);
    QCOMPARE(pseudoMaxReverse.value, 51192);
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

void CalculatorTests::tableDataLoadsCsvRows()
{
    QTemporaryDir tempDir;
    QVERIFY(tempDir.isValid());

    const QString rtuPath = tempDir.filePath(QStringLiteral("rtu_rows.csv"));
    QFile rtuFile(rtuPath);
    QVERIFY(rtuFile.open(QIODevice::WriteOnly | QIODevice::Text));
    rtuFile.write("utr,som,logic,link,localizacao,unidade,cota,eixo\n");
    rtuFile.write("UTR999,Z99R01,99,88,Teste,U99,123,A-B\n");
    rtuFile.close();

    QString error;
    const QVariantList rows = TableData::rtuRowsFromCsv(rtuPath, &error);
    QCOMPARE(error, QString());
    QCOMPARE(rows.size(), 1);
    const QVariantMap row = rows.first().toMap();
    QCOMPARE(row.value(QStringLiteral("utr")).toString(), QStringLiteral("UTR999"));
    QCOMPARE(row.value(QStringLiteral("text")).toString(), QStringLiteral("utr999 z99r01 99 88 teste u99 123 a-b"));

    const QString badPath = tempDir.filePath(QStringLiteral("bad.csv"));
    QFile badFile(badPath);
    QVERIFY(badFile.open(QIODevice::WriteOnly | QIODevice::Text));
    badFile.write("wrong,header\n");
    badFile.close();

    const QVariantList invalidRows = TableData::rtuRowsFromCsv(badPath, &error);
    QVERIFY(invalidRows.isEmpty());
    QCOMPARE(error, QStringLiteral("Cabecalho CSV invalido"));

    error.clear();
    const QVariantList missingRows = TableData::cableRowsFromCsv(tempDir.filePath(QStringLiteral("missing.csv")), &error);
    QVERIFY(missingRows.isEmpty());
    QVERIFY(!error.isEmpty());

    const QString shortPath = tempDir.filePath(QStringLiteral("short.csv"));
    QFile shortFile(shortPath);
    QVERIFY(shortFile.open(QIODevice::WriteOnly | QIODevice::Text));
    shortFile.write("cor,pb,par,fio,anilha,corAnilha\n");
    shortFile.write("Azul,Preto,1,11,I\n");
    shortFile.close();

    error.clear();
    const QVariantList shortRows = TableData::cableRowsFromCsv(shortPath, &error);
    QVERIFY(shortRows.isEmpty());
    QCOMPARE(error, QStringLiteral("Linha CSV invalida: 2"));
}

QTEST_APPLESS_MAIN(CalculatorTests)

#include "calculator_tests.moc"
