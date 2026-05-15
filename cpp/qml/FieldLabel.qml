import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Label {
    Layout.preferredWidth: 86
    Layout.preferredHeight: 30
    color: Theme.colors.labelText
    font.pixelSize: 10
    font.bold: true
    leftPadding: 8
    verticalAlignment: Text.AlignVCenter
    background: Rectangle { color: Theme.colors.labelBg }
}
