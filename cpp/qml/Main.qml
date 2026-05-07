import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: root
    width: 1220
    height: 900
    minimumWidth: 980
    minimumHeight: 820
    visible: true
    title: "IEC-870-5 Unbalanced Mode - Qt/QML"
    color: "#202224"

    property string pointInput: ""
    property string pointResult: "Resultado"
    property string limInf: "4"
    property string limSup: "20"
    property string rangeInf: "0"
    property string rangeSup: "10"
    property string analogMode: "Medido"
    property string analogValue: "5"
    property var analogResult: ({})
    property string searchDraft: ""

    Component.onCompleted: calculateAnalog()

    function calculateAnalog() {
        analogResult = backend.calculateAnalog(limInf, limSup, rangeInf, rangeSup, analogValue, analogMode)
    }

    function applyPreset(low, high, rLow, rHigh, measured) {
        limInf = low
        limSup = high
        rangeInf = rLow
        rangeSup = rHigh
        analogValue = measured
        calculateAnalog()
    }

    function convertPoint(toBitbyte) {
        var result = toBitbyte ? backend.bitbyteFromPtno(pointInput) : backend.ptnoFromBitbyte(pointInput)
        if (!result.ok) {
            pointResult = result.message
            return
        }
        pointResult = result.display
    }

    RowLayout {
        anchors.fill: parent
        anchors.margins: 8
        spacing: 8

        ColumnLayout {
            Layout.preferredWidth: 410
            Layout.maximumWidth: 410
            Layout.fillHeight: true
            spacing: 8

            Text {
                text: "Conversao de Pontos SCADA"
                color: "#f1f3f5"
                font.pixelSize: 16
                font.bold: true
            }

            ColumnLayout {
                Layout.fillWidth: true
                spacing: 8

                RowLayout {
                    Layout.fillWidth: true
                    TextField {
                        id: pointField
                        Layout.fillWidth: true
                        Layout.preferredHeight: 34
                        placeholderText: "Digite PTNO ou BitByte"
                        text: root.pointInput
                        onTextChanged: root.pointInput = text
                    }
                    Button {
                        Layout.preferredWidth: 34
                        Layout.preferredHeight: 34
                        text: "x"
                        onClicked: {
                            pointInput = ""
                            pointResult = "Resultado"
                        }
                    }
                }

                Label {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 28
                    text: pointResult
                    color: "#9aa3ab"
                    verticalAlignment: Text.AlignVCenter
                    leftPadding: 12
                    background: Rectangle {
                        color: "#17191b"
                        border.color: "#2f353a"
                        radius: 4
                    }
                }

                RowLayout {
                    Layout.alignment: Qt.AlignHCenter
                    spacing: 16
                    Button {
                        text: "To BitByte"
                        Layout.preferredWidth: 96
                        Layout.preferredHeight: 28
                        onClicked: convertPoint(true)
                    }
                    Button {
                        text: "To PTNO"
                        Layout.preferredWidth: 96
                        Layout.preferredHeight: 28
                        onClicked: convertPoint(false)
                    }
                }
            }

            Text {
                text: "Conversao Raw Counts - Bias/Scale"
                color: "#f1f3f5"
                font.pixelSize: 16
                font.bold: true
                Layout.topMargin: 12
            }

            ColumnLayout {
                Layout.fillWidth: true
                spacing: 8

                SectionBox {
                    title: "Valores de corrente do transdutor (mA)"
                    GridLayout {
                        anchors.fill: parent
                        anchors.margins: 18
                        columns: 4
                        columnSpacing: 10
                        rowSpacing: 8
                        FieldLabel { text: "Limite inferior" }
                        CalcField { text: limInf; onTextEdited: limInf = text }
                        FieldLabel { text: "Limite superior" }
                        CalcField { text: limSup; onTextEdited: limSup = text }
                        FieldLabel { text: "Valores tipicos:" }
                        Button { text: "0-20 mA"; Layout.preferredWidth: 84; onClicked: applyPreset("0", "20", "0", "20", "10") }
                        Item { Layout.preferredWidth: 84 }
                        Button { text: "4-20 mA"; Layout.preferredWidth: 84; onClicked: applyPreset("4", "20", "0", "10", "5") }
                    }
                }

                SectionBox {
                    title: "Escala do equipamento"
                    implicitHeight: 164
                    GridLayout {
                        anchors.fill: parent
                        anchors.margins: 18
                        columns: 4
                        columnSpacing: 10
                        rowSpacing: 10
                        FieldLabel { text: "Range inf" }
                        CalcField { text: rangeInf; onTextEdited: rangeInf = text }
                        FieldLabel { text: "Range sup" }
                        CalcField { text: rangeSup; onTextEdited: rangeSup = text }
                        FieldLabel { text: "Entrada" }
                        ComboBox {
                            Layout.preferredWidth: 84
                            Layout.preferredHeight: 30
                            model: ["Medido", "mA", "INT16", "HEX16"]
                            currentIndex: model.indexOf(analogMode)
                            onActivated: analogMode = currentText
                        }
                        FieldLabel { text: "Valor" }
                        CalcField { text: analogValue; onTextEdited: analogValue = text }
                        Item { Layout.columnSpan: 4; Layout.preferredHeight: 4 }
                        Button {
                            text: "Calcular"
                            Layout.columnSpan: 4
                            Layout.alignment: Qt.AlignHCenter
                            Layout.preferredWidth: 84
                            Layout.preferredHeight: 28
                            onClicked: calculateAnalog()
                        }
                    }
                }

                SectionBox {
                    title: "Resultado"
                    implicitHeight: 250
                    ColumnLayout {
                        anchors.fill: parent
                        anchors.margins: 18
                        spacing: 6
                        RowLayout {
                            Layout.fillWidth: true
                            ResultValue { text: analogResult.ok ? analogResult.rawHex : "--" }
                            ResultValue { text: analogResult.ok ? "INT16 " + analogResult.rawInt : "--" }
                        }
                        ResultRow { label: "Medido"; value: analogResult.ok ? analogResult.measured : "--" }
                        ResultRow { label: "mA"; value: analogResult.ok ? analogResult.current : "--" }
                        ResultRow { label: "BIAS"; value: analogResult.ok ? analogResult.bias : "--" }
                        ResultRow { label: "SCALE"; value: analogResult.ok ? analogResult.scale : "--" }
                        ResultRow { label: "INT16"; value: analogResult.ok ? analogResult.rawInt : "--" }
                        ResultRow { label: "HEX16"; value: analogResult.ok ? analogResult.rawHex : "--" }
                    }
                }

                Label {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 28
                    text: analogResult.ok
                        ? Number(analogResult.current).toPrecision(4)
                            + " mA | " + Number(analogResult.rangePercent).toFixed(1)
                            + "% range | " + Number(analogResult.rawPercent).toFixed(1)
                            + "% raw"
                        : analogResult.message
                    color: analogResult.outOfScale ? "#ffb454" : "#b8c0c7"
                    leftPadding: 8
                    verticalAlignment: Text.AlignVCenter
                    background: Rectangle { color: "#1b1e20" }
                }
            }
        }

        ColumnLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 8

            Text {
                text: "Localizacao das UTRs"
                color: "#f1f3f5"
                font.pixelSize: 16
                font.bold: true
            }

            RowLayout {
                Layout.fillWidth: true
                TextField {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 34
                    placeholderText: "Buscar nas tabelas"
                    text: searchDraft
                    onTextChanged: searchDraft = text
                    onAccepted: tables.searchText = searchDraft
                }
                Button {
                    text: "Ir"
                    Layout.preferredWidth: 42
                    Layout.preferredHeight: 34
                    onClicked: tables.searchText = searchDraft
                }
            }

            RowLayout {
                Layout.fillWidth: true
                Layout.fillHeight: true
                spacing: 8
                DataPanel {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Layout.preferredWidth: 3
                    title: "Localizacao das UTRs"
                    headers: ["UTR", "SOM", "Logic", "Link", "Localizacao", "Unidade", "Cota [m]", "Eixo"]
                    keys: ["utr", "som", "logic", "link", "localizacao", "unidade", "cota", "eixo"]
                    widths: [72, 78, 44, 42, 150, 70, 70, 54]
                    rows: tables.filteredRtuRows
                }
                DataPanel {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Layout.preferredWidth: 2
                    title: "Codigo e Cores dos Cabos de UTRs"
                    headers: ["Cor", "P&B", "Par", "Fio", "Anilha", "Cor an."]
                    keys: ["cor", "pb", "par", "fio", "anilha", "corAnilha"]
                    widths: [86, 74, 44, 50, 64, 70]
                    rows: tables.filteredCableRows
                }
            }
        }
    }
}
