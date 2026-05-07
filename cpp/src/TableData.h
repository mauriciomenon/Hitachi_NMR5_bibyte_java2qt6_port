#pragma once

#include <QVariantList>

class TableData final {
public:
    [[nodiscard]] static QVariantList rtuRows();
    [[nodiscard]] static QVariantList cableRows();
};

