import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: root
    width: 1200
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
        anchors.leftMargin: 12
        anchors.topMargin: 8
        anchors.rightMargin: 12
        anchors.bottomMargin: 8
        spacing: 8

        ColumnLayout {
            Layout.preferredWidth: 340
            Layout.maximumWidth: 340
            Layout.fillHeight: true
            Layout.alignment: Qt.AlignTop
            spacing: 8

            Text {
                Layout.preferredWidth: 300
                Layout.alignment: Qt.AlignHCenter
                text: "Conversao de Pontos SCADA"
                color: "#f1f3f5"
                font.pixelSize: 16
                font.bold: true
                horizontalAlignment: Text.AlignHCenter
            }

            ColumnLayout {
                Layout.preferredWidth: 300
                Layout.maximumWidth: 300
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

                TextField {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 28
                    readOnly: true
                    selectByMouse: true
                    text: pointResult
                    color: "#9aa3ab"
                    font.pixelSize: 12
                    verticalAlignment: Text.AlignVCenter
                    leftPadding: 12
                    rightPadding: 12
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
                        text: "BitByte"
                        Layout.preferredWidth: 96
                        Layout.preferredHeight: 28
                        onClicked: convertPoint(true)
                    }
                    Button {
                        text: "PTNO"
                        Layout.preferredWidth: 96
                        Layout.preferredHeight: 28
                        onClicked: convertPoint(false)
                    }
                }
            }

            Text {
                Layout.preferredWidth: 300
                Layout.alignment: Qt.AlignHCenter
                text: "Conversao Raw Counts - Bias/Scale"
                color: "#f1f3f5"
                font.pixelSize: 16
                font.bold: true
                horizontalAlignment: Text.AlignHCenter
                Layout.topMargin: 12
            }

            ColumnLayout {
                Layout.preferredWidth: 300
                Layout.maximumWidth: 300
                spacing: 8

                SectionBox {
                    title: "Valores de corrente do transdutor (mA)"
                    implicitHeight: currentForm.implicitHeight + 54
                    ColumnLayout {
                        id: currentForm
                        anchors.left: parent.left
                        anchors.top: parent.top
                        anchors.leftMargin: 12
                        anchors.topMargin: 18
                        width: parent.width - 24
                        spacing: 8
                        RowLayout {
                            spacing: 10
                            FieldLabel { text: "Lim. inferior" }
                            CalcField { text: limInf; onTextEdited: limInf = text }
                        }
                        RowLayout {
                            spacing: 10
                            FieldLabel { text: "Lim. superior" }
                            CalcField { text: limSup; onTextEdited: limSup = text }
                        }
                        RowLayout {
                            spacing: 10
                            FieldLabel { text: "Faixas:" }
                            RowLayout {
                                spacing: 4
                                Button { text: "0-20 mA"; Layout.preferredWidth: 68; font.pixelSize: 10; onClicked: applyPreset("0", "20", "0", "20", "10") }
                                Button { text: "4-20 mA"; Layout.preferredWidth: 68; font.pixelSize: 10; onClicked: applyPreset("4", "20", "0", "10", "5") }
                            }
                        }
                    }
                }

                SectionBox {
                    title: "Escala do equipamento"
                    implicitHeight: scaleForm.implicitHeight + 54
                    ColumnLayout {
                        id: scaleForm
                        anchors.left: parent.left
                        anchors.top: parent.top
                        anchors.leftMargin: 12
                        anchors.topMargin: 18
                        width: parent.width - 24
                        spacing: 8
                        RowLayout {
                            spacing: 10
                            FieldLabel { text: "Range inf" }
                            CalcField { text: rangeInf; onTextEdited: rangeInf = text }
                        }
                        RowLayout {
                            spacing: 10
                            FieldLabel { text: "Range sup" }
                            CalcField { text: rangeSup; onTextEdited: rangeSup = text }
                        }
                        RowLayout {
                            spacing: 10
                            FieldLabel { text: "Entrada" }
                            ComboBox {
                                Layout.preferredWidth: 132
                                Layout.preferredHeight: 30
                                model: ["Medido", "mA", "INT16", "HEX16"]
                                currentIndex: model.indexOf(analogMode)
                                onActivated: analogMode = currentText
                            }
                        }
                        RowLayout {
                            spacing: 10
                            FieldLabel { text: "Valor" }
                            CalcField {
                                text: analogValue
                                onTextEdited: analogValue = text
                                onAccepted: calculateAnalog()
                            }
                        }
                        Button {
                            text: "Calcular"
                            Layout.alignment: Qt.AlignHCenter
                            Layout.preferredWidth: 84
                            Layout.preferredHeight: 28
                            onClicked: calculateAnalog()
                        }
                    }
                }

                SectionBox {
                    id: resultSection
                    title: "Resultado"
                    implicitHeight: resultContent.implicitHeight + 38
                    ColumnLayout {
                        id: resultContent
                        x: 10
                        y: 10
                        width: parent.width - 20
                        spacing: 3
                        ResultRow { label: "Hexa"; value: analogResult.ok ? analogResult.rawHex : "--" }
                        ResultRow { label: "INT16"; value: analogResult.ok ? analogResult.rawInt : "--" }
                        ResultRow { label: "Decimal"; value: analogResult.ok ? analogResult.measured : "--" }
                        ResultRow { label: "mA"; value: analogResult.ok ? analogResult.current : "--" }
                        ResultRow { label: "BIAS"; value: analogResult.ok ? analogResult.bias : "--" }
                        ResultRow { label: "SCALE"; value: analogResult.ok ? analogResult.scale : "--" }
                        TextField {
                            Layout.fillWidth: false
                            Layout.preferredWidth: 226
                            Layout.preferredHeight: 30
                            Layout.topMargin: 5
                            readOnly: true
                            selectByMouse: true
                            horizontalAlignment: Text.AlignRight
                            leftPadding: 8
                            rightPadding: 8
                            font.pixelSize: 12
                            text: analogResult.ok
                                ? Number(analogResult.current).toPrecision(4)
                                    + " mA | " + Number(analogResult.rangePercent).toFixed(1)
                                    + "% range | " + Number(analogResult.rawPercent).toFixed(1)
                                    + "% raw"
                                : analogResult.message
                            color: analogResult.outOfScale ? "#ffb454" : "#b8c0c7"
                            background: Rectangle { color: "#1b1e20" }
                        }
                    }
                }
            }

            Item {
                Layout.fillHeight: true
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
                spacing: 20
                DataPanel {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Layout.preferredWidth: 3
                    title: "Localizacao das UTRs"
                    headers: ["UTR", "SOM", "Logic", "Link", "Localizacao", "Unidade", "Cota [m]", "Eixo"]
                    keys: ["utr", "som", "logic", "link", "localizacao", "unidade", "cota", "eixo"]
                    widths: [84, 74, 40, 38, 126, 58, 54, 42]
                    rows: tables.filteredRtuRows
                }
                DataPanel {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Layout.preferredWidth: 2
                    title: "Codigo e Cores dos Cabos de UTRs"
                    headers: ["Cor", "P&B", "Par", "Fio", "Anilha", "Cor an."]
                    keys: ["cor", "pb", "par", "fio", "anilha", "corAnilha"]
                    widths: [76, 60, 38, 38, 46, 64]
                    rows: tables.filteredCableRows
                }
            }
        }
    }
}
