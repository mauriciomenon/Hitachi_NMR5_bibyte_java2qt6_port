#pragma once

#include <QString>
#include <QVariantList>

class TableData final {
public:
    [[nodiscard]] static QVariantList rtuRows();
    [[nodiscard]] static QVariantList cableRows();
    [[nodiscard]] static QVariantList rtuRowsFromCsv(const QString& filePath, QString* error = nullptr);
    [[nodiscard]] static QVariantList cableRowsFromCsv(const QString& filePath, QString* error = nullptr);
};
