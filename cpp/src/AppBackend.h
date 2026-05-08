#pragma once

#include <QObject>
#include <QString>
#include <QVariantList>
#include <QVariantMap>

struct PointResult;
enum class AnalogInputMode;

class AppBackend final : public QObject {
    Q_OBJECT
    Q_PROPERTY(QString analogModeMeasured READ analogModeMeasured CONSTANT)

public:
    explicit AppBackend(QObject* parent = nullptr);

    [[nodiscard]] QString analogModeMeasured() const;

    Q_INVOKABLE QVariantList analogModeOptions() const;
    Q_INVOKABLE QVariantMap bitbyteFromPtno(const QString& value) const;
    Q_INVOKABLE QVariantMap ptnoFromBitbyte(const QString& value) const;
    Q_INVOKABLE QVariantMap calculateAnalog(
        const QString& limInf,
        const QString& limSup,
        const QString& rangeInf,
        const QString& rangeSup,
        const QString& value,
        const QString& inputMode) const;

private:
    [[nodiscard]] static QVariantMap makeError(const QString& message);
    [[nodiscard]] static QVariantMap pointResultMap(const PointResult& result);
};
