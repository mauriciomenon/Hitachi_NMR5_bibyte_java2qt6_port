import QtQuick
import QtQuick.Layouts

RowLayout {
    property string label: ""
    property string value: ""
    property int labelWidth: 86
    property int valueWidth: 132
    Layout.fillWidth: false
    Layout.preferredWidth: labelWidth + valueWidth + spacing
    Layout.preferredHeight: 24
    spacing: 8

    FieldLabel {
        text: parent.label
        Layout.preferredWidth: parent.labelWidth
        Layout.preferredHeight: 24
    }

    ResultValue {
        text: parent.value
        Layout.fillWidth: true
        Layout.preferredWidth: parent.valueWidth
        Layout.preferredHeight: 24
    }
}
