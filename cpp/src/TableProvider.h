#pragma once

#include <QObject>
#include <QVariantList>

class TableProvider final : public QObject {
    Q_OBJECT
    Q_PROPERTY(QVariantList rtuRows READ rtuRows NOTIFY rowsChanged)
    Q_PROPERTY(QVariantList cableRows READ cableRows NOTIFY rowsChanged)
    Q_PROPERTY(QVariantList filteredRtuRows READ filteredRtuRows NOTIFY rowsChanged)
    Q_PROPERTY(QVariantList filteredCableRows READ filteredCableRows NOTIFY rowsChanged)
    Q_PROPERTY(QString searchText READ searchText WRITE setSearchText NOTIFY searchTextChanged)

public:
    explicit TableProvider(QObject* parent = nullptr);

    [[nodiscard]] QVariantList rtuRows() const;
    [[nodiscard]] QVariantList cableRows() const;
    [[nodiscard]] QVariantList filteredRtuRows() const;
    [[nodiscard]] QVariantList filteredCableRows() const;
    [[nodiscard]] QString searchText() const;
    void setSearchText(const QString& value);

signals:
    void rowsChanged();
    void searchTextChanged();

private:
    QVariantList rtuRows_;
    QVariantList cableRows_;
    QVariantList filteredRtuRows_;
    QVariantList filteredCableRows_;
    QStringList rtuSearchIndex_;
    QStringList cableSearchIndex_;
    QString searchText_;

    void loadExternalRows();
    void rebuildSearchIndexes();
    void refreshFilteredRows();
    [[nodiscard]] static QStringList searchIndex(const QVariantList& rows);
    [[nodiscard]] static QVariantList filterRows(
        const QVariantList& rows,
        const QStringList& index,
        const QString& searchText);
};
