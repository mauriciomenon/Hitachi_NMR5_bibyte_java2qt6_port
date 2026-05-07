cmake_minimum_required(VERSION 3.21)

project(NMR5QtQml VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)

find_package(Qt6 REQUIRED COMPONENTS Core Gui Qml Quick QuickControls2)

if(Qt6_VERSION VERSION_GREATER_EQUAL "6.8.0")
    qt_policy(SET QTP0001 NEW)
    qt_policy(SET QTP0004 NEW)
endif()

qt_standard_project_setup()

qt_add_executable(nmr5_qml
    src/AnalogCalculator.cpp
    src/AnalogCalculator.h
    src/AppBackend.cpp
    src/AppBackend.h
    src/main.cpp
    src/PointCalculator.cpp
    src/PointCalculator.h
    src/TableData.cpp
    src/TableData.h
    src/TableProvider.cpp
    src/TableProvider.h
)

qt_add_qml_module(nmr5_qml
    URI NMR5
    VERSION 1.0
    QML_FILES
        qml/CalcField.qml
        qml/DataPanel.qml
        qml/FieldLabel.qml
        qml/Main.qml
        qml/ResultRow.qml
        qml/ResultValue.qml
        qml/SectionBox.qml
)

target_link_libraries(nmr5_qml
    PRIVATE
        Qt6::Core
        Qt6::Gui
        Qt6::Qml
        Qt6::Quick
        Qt6::QuickControls2
)
