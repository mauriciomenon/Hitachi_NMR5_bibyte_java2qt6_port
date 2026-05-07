#include "AppBackend.h"
#include "TableProvider.h"

#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include <QQuickStyle>

int main(int argc, char* argv[])
{
    QGuiApplication app(argc, argv);
    QGuiApplication::setApplicationName(QStringLiteral("NMR5 Qt/QML"));
    QQuickStyle::setStyle(QStringLiteral("Fusion"));

    AppBackend backend;
    TableProvider tables;
    QQmlApplicationEngine engine;
    engine.rootContext()->setContextProperty(QStringLiteral("backend"), &backend);
    engine.rootContext()->setContextProperty(QStringLiteral("tables"), &tables);
    engine.loadFromModule(QStringLiteral("NMR5"), QStringLiteral("Main"));

    if (engine.rootObjects().isEmpty()) {
        return 1;
    }
    return app.exec();
}
