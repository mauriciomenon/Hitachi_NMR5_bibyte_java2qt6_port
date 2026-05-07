import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    id: panel
    property string title: ""
    property var headers: []
    property var keys: []
    property var widths: []
    property var rows: []
    property int indexWidth: 28
    property var columnWidths: []
    spacing: 8

    onWidthsChanged: recalculateColumnWidths()
    Component.onCompleted: recalculateColumnWidths()

    function recalculateColumnWidths() {
        if (typeof tableFrame === "undefined") {
            return
        }

        var total = 0
        for (var i = 0; i < widths.length; i += 1) {
            total += Number(widths[i])
        }

        var nextWidths = []
        var used = 0
        var available = Math.max(0, tableFrame.width - indexWidth)

        for (var columnIndex = 0; columnIndex < widths.length; columnIndex += 1) {
            if (total <= 0) {
                nextWidths.push(0)
            } else if (columnIndex === widths.length - 1) {
                nextWidths.push(Math.max(0, available - used))
            } else {
                var calculatedWidth = Math.max(0, Math.floor(available * Number(widths[columnIndex]) / total))
                nextWidths.push(calculatedWidth)
                used += calculatedWidth
            }
        }

        columnWidths = nextWidths
    }

    function columnPixelWidth(columnIndex) {
        if (columnIndex >= columnWidths.length) {
            return 0
        }
        return columnWidths[columnIndex]
    }

    Button {
        text: parent.title
        Layout.fillWidth: true
        Layout.preferredHeight: 28
    }

    Rectangle {
        id: tableFrame
        Layout.fillWidth: true
        Layout.fillHeight: true
        color: "#151719"
        border.color: "#343a40"
        onWidthChanged: panel.recalculateColumnWidths()

        ColumnLayout {
            anchors.fill: parent
            spacing: 0

            Row {
                Layout.fillWidth: true
                height: 32

                Rectangle {
                    width: panel.indexWidth
                    height: parent.height
                    color: "#2f3438"
                    border.color: "#4c535a"
                }

                Repeater {
                    model: headers.length
                    Rectangle {
                        width: panel.columnPixelWidth(index)
                        height: 32
                        color: "#2f3438"
                        border.color: "#4c535a"

                        Text {
                            anchors.centerIn: parent
                            text: headers[index]
                            color: "#f1f3f5"
                            font.pixelSize: 10
                            font.bold: true
                        }
                    }
                }
            }

            ListView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true
                model: rows

                delegate: Row {
                    id: rowDelegate
                    required property int index
                    required property var modelData
                    width: ListView.view.width
                    height: 28

                    Rectangle {
                        width: panel.indexWidth
                        height: 28
                        color: "#2f3438"
                        border.color: "#4c535a"

                        Text {
                            anchors.centerIn: parent
                            text: index + 1
                            color: "#f1f3f5"
                            font.pixelSize: 10
                            font.bold: true
                        }
                    }

                    Repeater {
                        model: headers.length
                        Rectangle {
                            property int columnIndex: index
                            property string columnKey: keys[columnIndex] || ""
                            width: panel.columnPixelWidth(columnIndex)
                            height: 28
                            color: (rowDelegate.index % 2 === 0) ? "#151719" : "#1b1e20"

                            Text {
                                anchors.fill: parent
                                anchors.leftMargin: 6
                                anchors.rightMargin: 4
                                verticalAlignment: Text.AlignVCenter
                                text: rowDelegate.modelData && parent.columnKey.length > 0
                                    && rowDelegate.modelData[parent.columnKey] !== undefined
                                    ? String(rowDelegate.modelData[parent.columnKey])
                                    : ""
                                color: "#f1f3f5"
                                font.pixelSize: 12
                                elide: Text.ElideRight
                            }
                        }
                    }
                }

                ScrollBar.vertical: ScrollBar {}
            }
        }
    }
}
