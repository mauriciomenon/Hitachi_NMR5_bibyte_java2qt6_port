#include "TableProvider.h"

#include "TableData.h"

TableProvider::TableProvider(QObject* parent)
    : QObject(parent)
    , rtuRows_(TableData::rtuRows())
    , cableRows_(TableData::cableRows())
{
    refreshFilteredRows();
}

QVariantList TableProvider::rtuRows() const
{
    return rtuRows_;
}

QVariantList TableProvider::cableRows() const
{
    return cableRows_;
}

QVariantList TableProvider::filteredRtuRows() const
{
    return filteredRtuRows_;
}

QVariantList TableProvider::filteredCableRows() const
{
    return filteredCableRows_;
}

QString TableProvider::searchText() const
{
    return searchText_;
}

void TableProvider::setSearchText(const QString& value)
{
    const QString nextSearch = value.trimmed().toLower();
    if (nextSearch == searchText_) {
        return;
    }
    searchText_ = nextSearch;
    refreshFilteredRows();
    emit searchTextChanged();
    emit rowsChanged();
}

void TableProvider::refreshFilteredRows()
{
    filteredRtuRows_ = filterRows(rtuRows_, searchText_);
    filteredCableRows_ = filterRows(cableRows_, searchText_);
}

QVariantList TableProvider::filterRows(const QVariantList& rows, const QString& searchText)
{
    if (searchText.isEmpty()) {
        return rows;
    }

    QVariantList filtered;
    for (const auto& rowValue : rows) {
        const QVariantMap row = rowValue.toMap();
        if (row.value(QStringLiteral("text")).toString().contains(searchText)) {
            filtered.append(row);
        }
    }
    return filtered;
}

