pragma Singleton

import QtQuick

QtObject {
    id: theme

    property string currentName: "dark"
    property var colors: dark

    readonly property var dark: ({
        window: "#202224",
        text: "#f1f3f5",
        labelText: "#e1e5e9",
        mutedText: "#9aa3ab",
        resultText: "#dce3e8",
        summaryText: "#b8c0c7",
        warning: "#ffb454",
        inputBg: "#151719",
        inputBorder: "#d5d8db",
        readOnlyBg: "#17191b",
        readOnlyBorder: "#2f353a",
        sectionBg: "#2b2e31",
        labelBg: "#1b1e20",
        tableBg: "#151719",
        tableBorder: "#343a40",
        tableHeaderBg: "#2f3438",
        tableHeaderBorder: "#4c535a",
        rowEven: "#151719",
        rowOdd: "#1b1e20",
        scrollbar: "#6f7a84",
        buttonBg: "#2f3438",
        accent: "#7aa2f7"
    })

    readonly property var light: ({
        window: "#e8eaed",
        text: "#202124",
        labelText: "#2f3438",
        mutedText: "#5f6972",
        resultText: "#202124",
        summaryText: "#334155",
        warning: "#b45309",
        inputBg: "#f8fafc",
        inputBorder: "#4b5563",
        readOnlyBg: "#eef2f7",
        readOnlyBorder: "#9aa3ab",
        sectionBg: "#dfe3e8",
        labelBg: "#cfd6dd",
        tableBg: "#f8fafc",
        tableBorder: "#9aa3ab",
        tableHeaderBg: "#d3d9df",
        tableHeaderBorder: "#8b949e",
        rowEven: "#f8fafc",
        rowOdd: "#edf2f7",
        scrollbar: "#7b8794",
        buttonBg: "#d3d9df",
        accent: "#2563eb"
    })

    readonly property var gruvbox: ({
        window: "#282828",
        text: "#fbf1c7",
        labelText: "#ebdbb2",
        mutedText: "#a89984",
        resultText: "#fbf1c7",
        summaryText: "#d5c4a1",
        warning: "#fabd2f",
        inputBg: "#1d2021",
        inputBorder: "#d5c4a1",
        readOnlyBg: "#1d2021",
        readOnlyBorder: "#665c54",
        sectionBg: "#32302f",
        labelBg: "#1d2021",
        tableBg: "#1d2021",
        tableBorder: "#504945",
        tableHeaderBg: "#3c3836",
        tableHeaderBorder: "#665c54",
        rowEven: "#1d2021",
        rowOdd: "#282828",
        scrollbar: "#928374",
        buttonBg: "#3c3836",
        accent: "#b8bb26"
    })

    readonly property var dracula: ({
        window: "#282a36",
        text: "#f8f8f2",
        labelText: "#f8f8f2",
        mutedText: "#bfbfbf",
        resultText: "#f8f8f2",
        summaryText: "#d7d7e0",
        warning: "#ffb86c",
        inputBg: "#191a21",
        inputBorder: "#f8f8f2",
        readOnlyBg: "#21222c",
        readOnlyBorder: "#44475a",
        sectionBg: "#343746",
        labelBg: "#21222c",
        tableBg: "#191a21",
        tableBorder: "#44475a",
        tableHeaderBg: "#343746",
        tableHeaderBorder: "#6272a4",
        rowEven: "#191a21",
        rowOdd: "#21222c",
        scrollbar: "#6272a4",
        buttonBg: "#343746",
        accent: "#bd93f9"
    })

    function setTheme(name) {
        if (name === "light") {
            colors = light
            currentName = name
            return
        }
        if (name === "gruvbox") {
            colors = gruvbox
            currentName = name
            return
        }
        if (name === "dracula") {
            colors = dracula
            currentName = name
            return
        }
        colors = dark
        currentName = "dark"
    }
}
