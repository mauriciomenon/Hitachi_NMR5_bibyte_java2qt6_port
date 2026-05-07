import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

TextField {
    Layout.preferredWidth: 132
    Layout.preferredHeight: 30
    selectByMouse: true
    color: "#f1f3f5"
    font.pixelSize: 12
    horizontalAlignment: Text.AlignRight
    leftPadding: 8
    rightPadding: 8
    background: Rectangle {
        color: "#151719"
        border.color: "#d5d8db"
        radius: 4
    }
}
