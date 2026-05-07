#pragma once

#include <QObject>
#include <QVariantList>

class TableProvider final : public QObject {
    Q_OBJECT
    Q_PROPERTY(QVariantList rtuRows READ rtuRows CONSTANT)
    Q_PROPERTY(QVariantList cableRows READ cableRows CONSTANT)
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
    QString searchText_;

    void refreshFilteredRows();
    [[nodiscard]] static QVariantList filterRows(const QVariantList& rows, const QString& searchText);
};
