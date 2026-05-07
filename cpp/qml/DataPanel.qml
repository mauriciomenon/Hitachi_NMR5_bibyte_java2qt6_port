import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    property string title: ""
    property var headers: []
    property var keys: []
    property var widths: []
    property var rows: []
    spacing: 8

    Button {
        text: parent.title
        Layout.fillWidth: true
        Layout.preferredHeight: 28
    }

    Rectangle {
        Layout.fillWidth: true
        Layout.fillHeight: true
        color: "#151719"
        border.color: "#343a40"

        ColumnLayout {
            anchors.fill: parent
            spacing: 0

            Row {
                Layout.fillWidth: true
                height: 32

                Rectangle {
                    width: 28
                    height: parent.height
                    color: "#2f3438"
                    border.color: "#4c535a"
                }

                Repeater {
                    model: headers.length
                    Rectangle {
                        width: widths[index]
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
                        width: 28
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
                            width: widths[columnIndex]
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
