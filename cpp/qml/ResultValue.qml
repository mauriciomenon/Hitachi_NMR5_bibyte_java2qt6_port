import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Label {
    Layout.fillWidth: true
    Layout.preferredHeight: 28
    color: "#dce3e8"
    font.pixelSize: 11
    leftPadding: 10
    verticalAlignment: Text.AlignVCenter
    background: Rectangle {
        color: "#151719"
        border.color: "#d5d8db"
        radius: 4
    }
}

