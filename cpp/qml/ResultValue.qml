import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

TextField {
    Layout.fillWidth: true
    Layout.preferredHeight: 30
    readOnly: true
    selectByMouse: true
    color: Theme.colors.resultText
    font.pixelSize: 12
    leftPadding: 10
    rightPadding: 10
    horizontalAlignment: Text.AlignRight
    verticalAlignment: Text.AlignVCenter
    background: Rectangle {
        color: Theme.colors.inputBg
        border.color: Theme.colors.inputBorder
        radius: 4
    }
}
