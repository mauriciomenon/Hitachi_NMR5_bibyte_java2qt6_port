import QtQuick
import QtQuick.Layouts

Item {
    property string title: ""
    default property alias content: contentItem.data
    implicitHeight: 120
    Layout.fillWidth: true

    Rectangle {
        anchors.fill: parent
        anchors.topMargin: 8
        color: Theme.colors.sectionBg
        border.color: Theme.colors.inputBorder
        radius: 2
    }

    Rectangle {
        x: 20
        y: 0
        width: sectionTitle.width + 8
        height: sectionTitle.height
        color: Theme.colors.sectionBg
    }

    Text {
        id: sectionTitle
        x: 24
        y: 0
        text: parent.title
        color: Theme.colors.text
        font.pixelSize: 12
        font.bold: true
        padding: 4
    }

    Item {
        id: contentItem
        anchors.fill: parent
        anchors.topMargin: 18
        anchors.leftMargin: 0
        anchors.rightMargin: 0
        anchors.bottomMargin: 0
    }
}
