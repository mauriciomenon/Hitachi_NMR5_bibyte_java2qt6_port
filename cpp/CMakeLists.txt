cmake_minimum_required(VERSION 3.21)

project(NMR5QtQml VERSION 0.1.0 LANGUAGES CXX)

include(GNUInstallDirs)
include(CTest)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)

find_package(Qt6 REQUIRED COMPONENTS Core Gui Qml Quick QuickControls2)

if(Qt6_VERSION VERSION_GREATER_EQUAL "6.8.0")
    qt_policy(SET QTP0001 NEW)
    qt_policy(SET QTP0004 NEW)
endif()

qt_standard_project_setup()

set_source_files_properties(qml/Theme.qml PROPERTIES QT_QML_SINGLETON_TYPE TRUE)

add_library(nmr5_calculators STATIC
    src/AnalogCalculator.cpp
    src/AnalogCalculator.h
    src/PointCalculator.cpp
    src/PointCalculator.h
)

target_include_directories(nmr5_calculators
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/src
)

target_link_libraries(nmr5_calculators
    PUBLIC
        Qt6::Core
)

add_library(nmr5_backend STATIC
    src/AppBackend.cpp
    src/AppBackend.h
)

target_link_libraries(nmr5_backend
    PUBLIC
        nmr5_calculators
        Qt6::Core
)

qt_add_executable(nmr5_qml
    src/main.cpp
    src/TableData.cpp
    src/TableData.h
    src/TableProvider.cpp
    src/TableProvider.h
)

qt_add_resources(nmr5_qml table_data
    PREFIX "/"
    FILES
        data/rtu_rows.csv
        data/cable_rows.csv
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
        qml/Theme.qml
)

target_link_libraries(nmr5_qml
    PRIVATE
        nmr5_backend
        nmr5_calculators
        Qt6::Core
        Qt6::Gui
        Qt6::Qml
        Qt6::Quick
        Qt6::QuickControls2
)

if(BUILD_TESTING)
    find_package(Qt6 REQUIRED COMPONENTS Test)

    add_executable(nmr5_calculator_tests
        src/TableData.cpp
        src/TableData.h
        tests/calculator_tests.cpp
    )

    target_link_libraries(nmr5_calculator_tests
        PRIVATE
            nmr5_backend
            nmr5_calculators
            Qt6::Test
    )

    add_test(NAME nmr5_calculator_tests COMMAND nmr5_calculator_tests)
endif()

install(TARGETS nmr5_qml
    BUNDLE DESTINATION .
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

install(DIRECTORY data/
    DESTINATION ${CMAKE_INSTALL_DATADIR}/nmr5-qml/data
    FILES_MATCHING PATTERN "*.csv"
)

set(CPACK_PACKAGE_NAME "nmr5-qml")
set(CPACK_PACKAGE_VENDOR "NMR5")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "NMR5 Qt/QML interface slice")
set(CPACK_PACKAGE_VERSION ${PROJECT_VERSION})
set(CPACK_GENERATOR "TGZ;ZIP")

include(CPack)

add_custom_target(package_pure
    COMMAND ${CMAKE_CPACK_COMMAND} --config "${CMAKE_BINARY_DIR}/CPackConfig.cmake"
    DEPENDS nmr5_qml
    COMMENT "Generating pure package without bundled Qt runtime"
)

if(APPLE)
    add_custom_target(package_with_qt
        COMMAND bash "${CMAKE_CURRENT_SOURCE_DIR}/scripts/package_macos_qt.sh"
            "$<TARGET_FILE:nmr5_qml>"
            "${CMAKE_BINARY_DIR}/deploy"
            "${PROJECT_VERSION}"
        WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
        DEPENDS nmr5_qml
        COMMENT "Generating macOS package with bundled Qt runtime"
    )
elseif(WIN32)
    add_custom_target(package_with_qt
        COMMAND powershell -ExecutionPolicy Bypass -File
            "${CMAKE_CURRENT_SOURCE_DIR}/scripts/package_windows_qt.ps1"
            -BuildDir "${CMAKE_BINARY_DIR}"
            -InstallDir "${CMAKE_BINARY_DIR}/deploy/nmr5_qml"
            -Version "${PROJECT_VERSION}"
        WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
        DEPENDS nmr5_qml
        COMMENT "Generating Windows package with bundled Qt runtime"
    )
elseif(UNIX)
    add_custom_target(package_with_qt
        COMMAND bash "${CMAKE_CURRENT_SOURCE_DIR}/scripts/package_linux_qt.sh"
            "$<TARGET_FILE:nmr5_qml>"
            "${CMAKE_BINARY_DIR}/deploy"
            "${PROJECT_VERSION}"
        WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
        DEPENDS nmr5_qml
        COMMENT "Generating Linux package with bundled Qt runtime"
    )
endif()

add_custom_target(package_all
    DEPENDS package_pure package_with_qt
)
