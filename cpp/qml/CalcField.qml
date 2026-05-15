import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

TextField {
    Layout.preferredWidth: 132
    Layout.preferredHeight: 30
    selectByMouse: true
    color: Theme.colors.text
    font.pixelSize: 12
    horizontalAlignment: Text.AlignRight
    leftPadding: 8
    rightPadding: 8
    background: Rectangle {
        color: Theme.colors.inputBg
        border.color: Theme.colors.inputBorder
        radius: 4
    }
}
