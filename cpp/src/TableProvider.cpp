#include "TableProvider.h"

#include "TableData.h"

#include <QCoreApplication>
#include <QDebug>
#include <QDir>
#include <QFileInfo>
#include <QTimer>

#include <functional>

namespace {

QStringList dataFileCandidates(const QString& fileName)
{
    const QDir appDir(QCoreApplication::applicationDirPath());
    const QDir currentDir(QDir::currentPath());
    return {
        QStringLiteral(":/data/%1").arg(fileName),
        appDir.filePath(QStringLiteral("data/%1").arg(fileName)),
        appDir.filePath(QStringLiteral("../data/%1").arg(fileName)),
        appDir.filePath(QStringLiteral("../share/nmr5-qml/data/%1").arg(fileName)),
        currentDir.filePath(QStringLiteral("data/%1").arg(fileName)),
    };
}

QVariantList loadRows(
    const QString& fileName,
    const std::function<QVariantList(const QString&, QString*)>& loadCsv,
    const std::function<QVariantList()>& fallback)
{
    for (const QString& candidate : dataFileCandidates(fileName)) {
        if (!QFileInfo::exists(candidate)) {
            continue;
        }

        QString error;
        const QVariantList rows = loadCsv(candidate, &error);
        if (!rows.isEmpty()) {
            return rows;
        }
        qWarning() << "Invalid table data file" << candidate << error << "- using compiled fallback";
        return fallback();
    }
    return fallback();
}

} // namespace

TableProvider::TableProvider(QObject* parent)
    : QObject(parent)
    , rtuRows_(TableData::rtuRows())
    , cableRows_(TableData::cableRows())
{
    rebuildSearchIndexes();
    refreshFilteredRows();
    QTimer::singleShot(0, this, &TableProvider::loadExternalRows);
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
    filteredRtuRows_ = filterRows(rtuRows_, rtuSearchIndex_, searchText_);
    filteredCableRows_ = filterRows(cableRows_, cableSearchIndex_, searchText_);
}

void TableProvider::loadExternalRows()
{
    rtuRows_ = loadRows(
        QStringLiteral("rtu_rows.csv"),
        TableData::rtuRowsFromCsv,
        TableData::rtuRows);
    cableRows_ = loadRows(
        QStringLiteral("cable_rows.csv"),
        TableData::cableRowsFromCsv,
        TableData::cableRows);
    rebuildSearchIndexes();
    refreshFilteredRows();
    emit rowsChanged();
}

void TableProvider::rebuildSearchIndexes()
{
    rtuSearchIndex_ = searchIndex(rtuRows_);
    cableSearchIndex_ = searchIndex(cableRows_);
}

QStringList TableProvider::searchIndex(const QVariantList& rows)
{
    QStringList index;
    index.reserve(rows.size());
    for (const auto& rowValue : rows) {
        index.append(rowValue.toMap().value(QStringLiteral("text")).toString());
    }
    return index;
}

QVariantList TableProvider::filterRows(
    const QVariantList& rows,
    const QStringList& index,
    const QString& searchText)
{
    if (searchText.isEmpty()) {
        return rows;
    }

    QVariantList filtered;
    for (qsizetype rowIndex = 0; rowIndex < rows.size() && rowIndex < index.size(); ++rowIndex) {
        if (index.at(rowIndex).contains(searchText)) {
            filtered.append(rows.at(rowIndex));
        }
    }
    return filtered;
}
