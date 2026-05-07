#include "TableData.h"

#include <QString>
#include <QVariantMap>

namespace {

QVariantMap makeRtuRow(
    const QString& utr,
    const QString& som,
    const QString& logic,
    const QString& link,
    const QString& localizacao,
    const QString& unidade,
    const QString& cota,
    const QString& eixo)
{
    const QString text = QStringList{utr, som, logic, link, localizacao, unidade, cota, eixo}
        .join(QStringLiteral(" "))
        .toLower();
    return {
        {QStringLiteral("utr"), utr},
        {QStringLiteral("som"), som},
        {QStringLiteral("logic"), logic},
        {QStringLiteral("link"), link},
        {QStringLiteral("localizacao"), localizacao},
        {QStringLiteral("unidade"), unidade},
        {QStringLiteral("cota"), cota},
        {QStringLiteral("eixo"), eixo},
        {QStringLiteral("text"), text},
    };
}

QVariantMap makeCableRow(
    const QString& cor,
    const QString& pb,
    const QString& par,
    const QString& fio,
    const QString& anilha,
    const QString& corAnilha)
{
    const QString text = QStringList{cor, pb, par, fio, anilha, corAnilha}
        .join(QStringLiteral(" "))
        .toLower();
    return {
        {QStringLiteral("cor"), cor},
        {QStringLiteral("pb"), pb},
        {QStringLiteral("par"), par},
        {QStringLiteral("fio"), fio},
        {QStringLiteral("anilha"), anilha},
        {QStringLiteral("corAnilha"), corAnilha},
        {QStringLiteral("text"), text},
    };
}

} // namespace

QVariantList TableData::rtuRows()
{
    return {
        makeRtuRow("UTR501", "A01R01", "1", "1", "Casa de Forca", "U01", "108", "C-D"),
        makeRtuRow("UTR502", "A02R01", "2", "2", "Casa de Forca", "U02", "108", "C-D"),
        makeRtuRow("UTR503", "A03R01", "3", "3", "Casa de Forca", "U03", "108", "C-D"),
        makeRtuRow("UTR504", "A04R01", "4", "4", "Casa de Forca", "U04", "108", "C-D"),
        makeRtuRow("UTR505", "A05R01", "5", "5", "Casa de Forca", "U05", "108", "C-D"),
        makeRtuRow("UTR506", "A06R01", "6", "1", "Casa de Forca", "U06", "108", "C-D"),
        makeRtuRow("UTR507", "A07R01", "7", "7", "Casa de Forca", "U07", "108", "C-D"),
        makeRtuRow("UTR508", "A08R01", "8", "8", "Casa de Forca", "U08", "108", "C-D"),
        makeRtuRow("UTR509", "A09R01", "9", "9", "Casa de Forca", "U09", "108", "C-D"),
        makeRtuRow("UTR610", "B10R01", "10", "10", "Casa de Forca", "U10", "108", "C-D"),
        makeRtuRow("UTR611", "B11R01", "11", "11", "Casa de Forca", "U11", "108", "C-D"),
        makeRtuRow("UTR612", "B12R01", "12", "12", "Casa de Forca", "U12", "108", "C-D"),
        makeRtuRow("UTR613", "B13R01", "13", "13", "Casa de Forca", "U13", "108", "C-D"),
        makeRtuRow("UTR614", "B14R01", "14", "14", "Casa de Forca", "U14", "108", "C-D"),
        makeRtuRow("UTR615", "B15R01", "15", "15", "Casa de Forca", "U15", "108", "C-D"),
        makeRtuRow("UTR616", "B16R01", "16", "16", "Casa de Forca", "U16", "108", "C-D"),
        makeRtuRow("UTR617", "B17R01", "17", "17", "Casa de Forca", "U17", "108", "C-D"),
        makeRtuRow("UTR618", "B18R01", "18", "18", "Casa de Forca", "U18", "108", "C-D"),
        makeRtuRow("UTR520", "C45A01", "20", "19", "GIS", "U02", "124", "A-B"),
        makeRtuRow("UTR520-1", "C45A02", "21", "20", "GIS", "U03", "124", "A-B"),
        makeRtuRow("UTR521", "C45A03", "22", "21", "GIS", "U05", "124", "A-B"),
        makeRtuRow("UTR522", "C45A04", "23", "22", "GIS", "U08", "124", "A-B"),
        makeRtuRow("UTR620", "D45A01", "24", "23", "GIS", "U12", "124", "A-B"),
        makeRtuRow("UTR621", "D45A02", "25", "24", "GIS", "U14", "124", "A-B"),
        makeRtuRow("UTR622", "D45A03", "26", "25", "GIS", "U16", "124", "A-B"),
        makeRtuRow("UTR622-1", "D45A04", "27", "26", "GIS", "U17", "124", "A-B"),
        makeRtuRow("UTR530", "J61A01", "30", "27", "Casa de Forca", "U3", "115", "C-D"),
        makeRtuRow("UTR531", "J61A02", "31", "28", "Casa de Forca", "U8", "115", "C-D"),
        makeRtuRow("UTR532", "J61A03", "32", "29", "Casa de Forca", "AMD2", "127.6", "C-D"),
        makeRtuRow("UTR533", "J61A04", "33", "30", "Casa de Forca", "AMD3", "144.5", "A-B"),
        makeRtuRow("UTR534", "J61A05", "34", "31", "Casa de Forca", "U7", "127.6", "C-D"),
        makeRtuRow("UTR534-1", "J61A06", "35", "32", "GIS", "U9A", "132", "A-B"),
    };
}

QVariantList TableData::cableRows()
{
    return {
        makeCableRow("Azul", "Preto", "1", "11", "I", "Rosa"),
        makeCableRow("Vermelho", "Branco", "1", "12", "I", "Rosa"),
        makeCableRow("Cinza", "Preto", "2", "13", "I", "Rosa"),
        makeCableRow("Amarelo", "Branco", "2", "14", "I", "Rosa"),
        makeCableRow("Verde", "Preto", "3", "15", "I", "Rosa"),
        makeCableRow("Marrom", "Branco", "3", "16", "I", "Rosa"),
        makeCableRow("Preto", "Preto", "4", "17", "I", "Rosa"),
        makeCableRow("Branco", "Branco", "4", "18", "I", "Rosa"),
        makeCableRow("Ciano", "-", "-", "19", "I", "Rosa"),
        makeCableRow("Azul", "Preto", "5", "21", "II", "Rosa"),
        makeCableRow("Vermelho", "Branco", "5", "22", "II", "Rosa"),
        makeCableRow("Cinza", "Preto", "6", "23", "II", "Rosa"),
        makeCableRow("Amarelo", "Branco", "6", "24", "II", "Rosa"),
        makeCableRow("Verde", "Preto", "7", "25", "II", "Rosa"),
        makeCableRow("Marrom", "Branco", "7", "26", "II", "Rosa"),
        makeCableRow("Preto", "Preto", "8", "27", "II", "Rosa"),
        makeCableRow("Branco", "Branco", "8", "28", "II", "Rosa"),
        makeCableRow("Ciano", "-", "-", "29", "II", "Rosa"),
        makeCableRow("Azul", "Preto", "9", "31", "III", "Rosa"),
        makeCableRow("Vermelho", "Branco", "9", "32", "III", "Rosa"),
        makeCableRow("Cinza", "Preto", "10", "33", "III", "Rosa"),
        makeCableRow("Amarelo", "Branco", "10", "34", "III", "Rosa"),
        makeCableRow("Verde", "Preto", "11", "35", "III", "Rosa"),
        makeCableRow("Marrom", "Branco", "11", "36", "III", "Rosa"),
    };
}
