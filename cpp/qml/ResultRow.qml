import QtQuick
import QtQuick.Layouts

RowLayout {
    property string label: ""
    property string value: ""
    Layout.fillWidth: true
    spacing: 8

    FieldLabel {
        text: parent.label
        Layout.preferredHeight: 28
    }

    ResultValue {
        text: parent.value
    }
}
