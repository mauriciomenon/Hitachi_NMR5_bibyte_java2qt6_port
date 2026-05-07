import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

TextField {
    Layout.fillWidth: true
    Layout.preferredHeight: 30
    readOnly: true
    selectByMouse: true
    color: "#dce3e8"
    font.pixelSize: 12
    leftPadding: 10
    rightPadding: 10
    horizontalAlignment: Text.AlignRight
    verticalAlignment: Text.AlignVCenter
    background: Rectangle {
        color: "#151719"
        border.color: "#d5d8db"
        radius: 4
    }
}
