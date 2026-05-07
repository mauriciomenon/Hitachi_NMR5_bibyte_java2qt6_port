import sys
from pathlib import Path

from analog_logic import calculate_analog
from bitbyte_data import CABLE_COLOR_DATA, RTU_DATA
from bitbyte_logic import bitbyte_from_ptno_result, ptno_from_bitbyte_result
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QGridLayout,
    QGroupBox,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
    QSizePolicy,
)


ANALOG_LABEL_WIDTH = 86
ANALOG_CONTROL_WIDTH = 84
ANALOG_ROW_HEIGHT = 30
SEARCH_ROW_HEIGHT = 34
SUBTITLE_ROW_HEIGHT = 28


class AnalogPanel(QGroupBox):
    def __init__(self):
        super().__init__("Conversão Raw Counts - Bias/Scale")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        analog_layout = QVBoxLayout(self)
        analog_layout.setSpacing(8)

        self.analog_lim_inf = QLineEdit("4")
        self.analog_lim_inf.setObjectName("analogInputNarrow")
        self.analog_lim_sup = QLineEdit("20")
        self.analog_lim_sup.setObjectName("analogInputNarrow")
        self.analog_range_inf = QLineEdit("0")
        self.analog_range_inf.setObjectName("analogInputNarrow")
        self.analog_range_sup = QLineEdit("10")
        self.analog_range_sup.setObjectName("analogInputNarrow")
        self.analog_measured = QLineEdit("5")
        self.analog_measured.setObjectName("analogInputNarrow")
        self.analog_input_mode = QComboBox()
        self.analog_input_mode.addItems(["Medido", "mA", "INT16", "HEX16"])
        self.analog_input_mode.setObjectName("analogInputMode")
        self.analog_current = QLabel("--")
        self.analog_current.setObjectName("analogOutputValue")
        self.analog_measured_result = QLabel("--")
        self.analog_measured_result.setObjectName("analogOutputValue")
        self.analog_bias = QLabel("--")
        self.analog_bias.setObjectName("analogOutputValue")
        self.analog_scale = QLabel("--")
        self.analog_scale.setObjectName("analogOutputValue")
        self.analog_raw_int = QLabel("--")
        self.analog_raw_int.setObjectName("analogOutputValue")
        self.analog_raw_hex = QLabel("--")
        self.analog_raw_hex.setObjectName("analogOutputValue")
        self.analog_primary_hex = QLabel("--")
        self.analog_primary_hex.setObjectName("analogPrimaryValue")
        self.analog_primary_int = QLabel("--")
        self.analog_primary_int.setObjectName("analogPrimaryIntValue")
        self.analog_status = QLabel("--")
        self.analog_status.setObjectName("analogStatusOk")

        self.preset_4_20 = QPushButton("4-20 mA")
        self.preset_4_20.setObjectName("analogPresetButton")
        self.preset_4_20.setToolTip("Automacao: 4-20mA com escala 0-10")
        self.preset_4_20.clicked.connect(self.apply_4_20_preset)
        self.preset_0_20 = QPushButton("0-20 mA")
        self.preset_0_20.setObjectName("analogPresetButton")
        self.preset_0_20.clicked.connect(self.apply_0_20_preset)
        self.preset_0_20.setFixedWidth(ANALOG_CONTROL_WIDTH)
        self.preset_4_20.setFixedWidth(ANALOG_CONTROL_WIDTH)
        self.preset_0_20.setFixedHeight(ANALOG_ROW_HEIGHT)
        self.preset_4_20.setFixedHeight(ANALOG_ROW_HEIGHT)
        self.analog_button = self.create_compact_button(
            "Calcular", ANALOG_CONTROL_WIDTH
        )
        self.analog_button.clicked.connect(lambda: self.calculate_analog())
        self.analog_lim_inf.setFixedWidth(ANALOG_CONTROL_WIDTH)
        self.analog_lim_sup.setFixedWidth(ANALOG_CONTROL_WIDTH)
        self.analog_range_inf.setFixedWidth(ANALOG_CONTROL_WIDTH)
        self.analog_range_sup.setFixedWidth(ANALOG_CONTROL_WIDTH)
        self.analog_input_mode.setFixedWidth(ANALOG_CONTROL_WIDTH)
        self.analog_measured.setFixedWidth(ANALOG_CONTROL_WIDTH)
        for field in (
            self.analog_lim_inf,
            self.analog_lim_sup,
            self.analog_range_inf,
            self.analog_range_sup,
            self.analog_input_mode,
            self.analog_measured,
        ):
            field.setFixedHeight(ANALOG_ROW_HEIGHT)

        current_box = QGroupBox("Valores de corrente do transdutor (mA)")
        current_box.setObjectName("calcSection")
        current_layout = self.create_analog_grid(current_box)
        current_layout.addWidget(
            self.create_inline_label("Limite inferior", ANALOG_LABEL_WIDTH), 0, 0
        )
        current_layout.addWidget(self.analog_lim_inf, 0, 1)
        current_layout.addWidget(
            self.create_inline_label("Limite superior", ANALOG_LABEL_WIDTH), 0, 2
        )
        current_layout.addWidget(self.analog_lim_sup, 0, 3)
        current_layout.addWidget(
            self.create_inline_label("Valores tipicos:", ANALOG_LABEL_WIDTH), 1, 0
        )
        current_layout.addWidget(self.preset_0_20, 1, 1)
        current_layout.addWidget(self.preset_4_20, 1, 3)
        analog_layout.addWidget(current_box)

        scale_box = QGroupBox("Escala do equipamento")
        scale_box.setObjectName("calcSection")
        scale_layout = self.create_analog_grid(scale_box)
        scale_layout.addWidget(
            self.create_inline_label("Range inf", ANALOG_LABEL_WIDTH), 0, 0
        )
        scale_layout.addWidget(self.analog_range_inf, 0, 1)
        scale_layout.addWidget(
            self.create_inline_label("Range sup", ANALOG_LABEL_WIDTH), 0, 2
        )
        scale_layout.addWidget(self.analog_range_sup, 0, 3)
        scale_layout.addWidget(
            self.create_inline_label("Entrada", ANALOG_LABEL_WIDTH), 1, 0
        )
        scale_layout.addWidget(self.analog_input_mode, 1, 1)
        scale_layout.addWidget(
            self.create_inline_label("Valor", ANALOG_LABEL_WIDTH), 1, 2
        )
        scale_layout.addWidget(self.analog_measured, 1, 3)
        scale_layout.addWidget(
            self.analog_button, 2, 0, 1, 4, Qt.AlignmentFlag.AlignHCenter
        )
        analog_layout.addWidget(scale_box)

        result_box = QGroupBox("Resultado")
        result_box.setObjectName("calcSection")
        result_layout = QGridLayout(result_box)
        result_layout.setHorizontalSpacing(8)
        result_layout.setVerticalSpacing(4)
        result_layout.setContentsMargins(10, 10, 10, 10)
        primary_layout = QHBoxLayout()
        primary_layout.setSpacing(6)
        primary_layout.addWidget(self.analog_primary_hex, 1)
        primary_layout.addWidget(self.analog_primary_int, 1)
        result_layout.addLayout(primary_layout, 0, 0, 1, 2)
        result_labels = [
            ("Medido", self.analog_measured_result),
            ("mA", self.analog_current),
            ("BIAS", self.analog_bias),
            ("SCALE", self.analog_scale),
            ("INT16", self.analog_raw_int),
            ("HEX16", self.analog_raw_hex),
        ]
        for row, (label, value_label) in enumerate(result_labels):
            result_label = QLabel(label)
            result_label.setObjectName("analogResultLabel")
            result_layout.addWidget(result_label, row + 1, 0)
            result_layout.addWidget(value_label, row + 1, 1)
        analog_layout.addWidget(result_box)

        analog_layout.addWidget(self.analog_status)
        self.calculate_analog(show_warning=False)

    def create_compact_button(self, text, width):
        button = QPushButton(text)
        button.setObjectName("compactButton")
        button.setFixedWidth(width)
        button.setFixedHeight(ANALOG_ROW_HEIGHT)
        return button

    def create_inline_label(self, text, width):
        label = QLabel(text)
        label.setObjectName("analogInlineLabel")
        label.setFixedWidth(width)
        label.setFixedHeight(ANALOG_ROW_HEIGHT)
        return label

    def create_analog_grid(self, parent):
        layout = QGridLayout(parent)
        layout.setHorizontalSpacing(8)
        layout.setVerticalSpacing(7)
        layout.setContentsMargins(8, 10, 8, 10)
        layout.setColumnStretch(4, 1)
        return layout

    def calculate_analog(self, show_warning=True):
        try:
            result = calculate_analog(
                self.analog_lim_inf.text(),
                self.analog_lim_sup.text(),
                self.analog_range_inf.text(),
                self.analog_range_sup.text(),
                self.analog_measured.text(),
                self.current_analog_input_mode(),
            )
        except ValueError as exc:
            if show_warning:
                QMessageBox.warning(self, "Erro", str(exc))
            return

        self.analog_measured_result.setText(f"{result.measured_value:.6g}")
        self.analog_current.setText(f"{result.current_ma:.6g}")
        self.analog_bias.setText(f"{result.bias:.6g}")
        self.analog_scale.setText(f"{result.scale:.6g}")
        self.analog_raw_int.setText(str(result.raw_int16))
        self.analog_raw_hex.setText(result.raw_hex16)
        self.analog_primary_hex.setText(result.raw_hex16)
        self.analog_primary_int.setText(f"INT16 {result.raw_int16}")
        if result.out_of_scale:
            self.analog_status.setObjectName("analogStatusWarning")
        else:
            self.analog_status.setObjectName("analogStatusOk")
        self.analog_status.setText(self.format_analog_status(result))
        status_style = self.analog_status.style()
        if status_style is not None:
            status_style.unpolish(self.analog_status)
            status_style.polish(self.analog_status)

    def apply_4_20_preset(self):
        self.apply_preset("4", "20", "0", "10", "5")

    def apply_0_20_preset(self):
        self.apply_preset("0", "20", "0", "20", "10")

    def apply_preset(self, lim_inf, lim_sup, range_inf, range_sup, measured):
        self.analog_lim_inf.setText(lim_inf)
        self.analog_lim_sup.setText(lim_sup)
        self.analog_range_inf.setText(range_inf)
        self.analog_range_sup.setText(range_sup)
        self.analog_measured.setText(measured)
        self.calculate_analog()

    def current_analog_input_mode(self):
        mode_map = {
            "Medido": "measured",
            "mA": "current_ma",
            "INT16": "raw_int16",
            "HEX16": "raw_hex16",
        }
        return mode_map[self.analog_input_mode.currentText()]

    def format_analog_status(self, result):
        status_parts = (
            f"{result.current_ma:.4g} mA",
            f"{result.range_percent:.1f}% range",
            f"{result.raw_percent:.1f}% raw",
        )
        if result.out_of_scale:
            return "FORA ESCALA | " + " | ".join(status_parts)
        return " | ".join(status_parts)


class SostatPanel(QGroupBox):
    def __init__(self):
        super().__init__("Conversão de Pontos SCADA")
        self.setObjectName("sostatPanel")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMaximumHeight(166)
        bitbyte_layout = QVBoxLayout(self)
        bitbyte_layout.setContentsMargins(8, 8, 8, 8)
        bitbyte_layout.setSpacing(1)

        self.entry_input = QLineEdit()
        self.entry_input.setPlaceholderText("Digite PTNO ou BitByte")
        self.entry_input.setObjectName("ptnoInput")
        self.entry_input.setFixedHeight(SEARCH_ROW_HEIGHT)
        entry_row = QHBoxLayout()
        entry_row.setContentsMargins(0, 0, 0, 0)
        entry_row.setSpacing(8)
        entry_row.addWidget(self.entry_input)
        clear_button = self.createButton("x", self.limpar_valores, entry_row, compact=True)
        clear_button.setFixedWidth(28)
        clear_button.setFixedHeight(SEARCH_ROW_HEIGHT)
        bitbyte_layout.addLayout(entry_row)
        bitbyte_layout.addSpacing(13)

        self.entry_ptno_bitbyte_resultbox = QLabel("Resultado")
        self.entry_ptno_bitbyte_resultbox.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        self.entry_ptno_bitbyte_resultbox.setObjectName("ptnoResult")
        self.entry_ptno_bitbyte_resultbox.setFixedHeight(SUBTITLE_ROW_HEIGHT)
        bitbyte_layout.addWidget(self.entry_ptno_bitbyte_resultbox)
        bitbyte_layout.addSpacing(5)

        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(14)
        buttons_layout.addStretch(1)
        ptno_button = self.createButton("PTNO", self.calcula_2, buttons_layout, compact=True)
        bitbyte_button = self.createButton("BitByte", self.calcula_1, buttons_layout, compact=True)
        ptno_button.setFixedWidth(84)
        bitbyte_button.setFixedWidth(84)
        ptno_button.setFixedHeight(ANALOG_ROW_HEIGHT)
        bitbyte_button.setFixedHeight(ANALOG_ROW_HEIGHT)
        buttons_layout.addStretch(1)
        bitbyte_layout.addLayout(buttons_layout)

    def createButton(self, text, function, layout, compact=False):
        button = QPushButton(text)
        button.setObjectName("compactButton" if compact else "standardButton")
        if not compact:
            button.setFixedHeight(SUBTITLE_ROW_HEIGHT)
        button.clicked.connect(function)
        layout.addWidget(button)
        return button

    def limpar_valores(self):
        self.entry_input.clear()
        self.entry_ptno_bitbyte_resultbox.setText("Resultado")
        self.entry_ptno_bitbyte_resultbox.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )

    def calcula_1(self):
        result, message, title = bitbyte_from_ptno_result(self.entry_input.text())
        if result < 0:
            QMessageBox.warning(self, title, message)
            self.entry_ptno_bitbyte_resultbox.setText("Resultado")
            return

        if message:
            QMessageBox.information(self, title, message)
        self.entry_ptno_bitbyte_resultbox.setText(str(result))

    def calcula_2(self):
        result, message, title = ptno_from_bitbyte_result(self.entry_input.text())
        if result < 0:
            QMessageBox.warning(self, title, message)
            self.entry_ptno_bitbyte_resultbox.setText("Resultado")
            return

        if message:
            QMessageBox.information(self, title, message)
        self.entry_ptno_bitbyte_resultbox.setText(str(result))


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("IEC-870-5 Unbalanced Mode")
        self.applyStyle()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        controls_panel = QWidget()
        controls_panel.setMinimumWidth(390)
        controls_panel.setMaximumWidth(410)
        controls_layout = QVBoxLayout(controls_panel)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(5)
        self.setupInitialComponents(controls_layout)
        layout.addWidget(controls_panel, 0)

        tables_panel = QWidget()
        tables_layout = QVBoxLayout(tables_panel)
        tables_layout.setContentsMargins(0, 0, 0, 0)
        tables_layout.addWidget(QLabel("Localizacao das UTRs"))

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar nas tabelas")
        self.search_input.setObjectName("searchInput")
        self.search_input.setFixedHeight(34)
        search_layout = QHBoxLayout()
        search_layout.setSpacing(8)
        search_layout.addWidget(self.search_input)
        search_button = self.createButton(
            "Ir", self.procurar_geral, search_layout, compact=True
        )
        search_button.setFixedWidth(42)
        search_button.setFixedHeight(SEARCH_ROW_HEIGHT)
        tables_layout.addLayout(search_layout)

        tables_body_layout = QHBoxLayout()
        tables_body_layout.setSpacing(8)
        self.setupMainTable(tables_body_layout)
        self.setupSecondTable(tables_body_layout)
        tables_layout.addLayout(tables_body_layout)
        layout.addWidget(tables_panel, 1)

        self.resize(1220, 680)

    def applyStyle(self):
        style_path = Path(__file__).with_name("style.qss")
        self.setStyleSheet(style_path.read_text(encoding="utf-8"))

    def setupInitialComponents(self, layout):
        self.sostat_panel = SostatPanel()
        layout.addWidget(self.sostat_panel)

        self.analog_panel = AnalogPanel()
        layout.addWidget(self.analog_panel)

    def setupMainTable(self, layout):
        panel = QWidget()
        panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(0, 0, 0, 0)
        self.createButton("Localizacao das UTRs", self.focus_main_table, panel_layout)
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            [
                "UTR",
                "SOM",
                "Logic",
                "Link",
                "Localizacao",
                "Unidade",
                "Cota [m]",
                "Eixo",
            ]
        )
        panel_layout.addWidget(self.table)
        self.configure_table(self.table)
        self.add_table_data()
        self.table.setSortingEnabled(True)
        header = self.table.horizontalHeader()
        if header is not None:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
            header.setStretchLastSection(False)
            self.table.setColumnWidth(0, 62)
            self.table.setColumnWidth(1, 62)
            self.table.setColumnWidth(2, 34)
            self.table.setColumnWidth(3, 28)
            self.table.setColumnWidth(4, 114)
            self.table.setColumnWidth(5, 46)
            self.table.setColumnWidth(6, 52)
            self.table.setColumnWidth(7, 44)
        layout.addWidget(panel, 3)

    def setupSecondTable(self, layout):
        panel = QWidget()
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(0, 0, 0, 0)
        self.createButton(
            "Codigo e Cores dos Cabos de UTRs", self.focus_second_table, panel_layout
        )
        self.second_table = QTableWidget()
        self.second_table.setColumnCount(6)
        self.second_table.setHorizontalHeaderLabels(
            [
                "Cor",
                "P&B",
                "Par",
                "Fio",
                "Anilha",
                "Cor an.",
            ]
        )
        panel_layout.addWidget(self.second_table)
        self.configure_table(self.second_table)
        self.populate_second_table()
        self.second_table.setSortingEnabled(True)
        header = self.second_table.horizontalHeader()
        if header is not None:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
            header.setStretchLastSection(False)
            self.second_table.setColumnWidth(0, 68)
            self.second_table.setColumnWidth(1, 60)
            self.second_table.setColumnWidth(2, 30)
            self.second_table.setColumnWidth(3, 34)
            self.second_table.setColumnWidth(4, 14)
            self.second_table.setColumnWidth(5, 70)
        layout.addWidget(panel, 2)

    def createButton(self, text, function, layout, compact=False):
        button = QPushButton(text)
        button.setObjectName("compactButton" if compact else "standardButton")
        if not compact:
            button.setFixedHeight(SUBTITLE_ROW_HEIGHT)
        button.clicked.connect(function)
        layout.addWidget(button)
        return button

    def configure_table(self, table):
        table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        table.setAlternatingRowColors(True)
        table.setShowGrid(False)
        table.setWordWrap(False)
        vertical_header = table.verticalHeader()
        if vertical_header is not None:
            vertical_header.setDefaultSectionSize(26)
            vertical_header.setFixedWidth(28)

    def focus_main_table(self):
        self.table.setFocus()
        if self.table.rowCount() > 0:
            self.table.scrollToItem(self.table.item(0, 0))

    def focus_second_table(self):
        self.second_table.setFocus()
        if self.second_table.rowCount() > 0:
            self.second_table.scrollToItem(self.second_table.item(0, 0))

    def procurar_geral(self):
        search_text = self.search_input.text().strip().lower()
        self.table.clearSelection()
        self.second_table.clearSelection()
        self.select_matching_items(self.table, search_text)
        self.select_matching_items(self.second_table, search_text)

    def select_matching_items(self, table, search_text):
        if not search_text:
            return
        for row in range(table.rowCount()):
            for col in range(table.columnCount()):
                item = table.item(row, col)
                if item and search_text in item.text().strip().lower():
                    item.setSelected(True)

    def add_table_data(self):
        self.populate_table(self.table, RTU_DATA)

    def populate_second_table(self):
        self.populate_table(self.second_table, CABLE_COLOR_DATA)

    def populate_table(self, table, data):
        table.setRowCount(len(data))
        for row_index, row_data in enumerate(data):
            for column_index, cell_data in enumerate(row_data):
                table.setItem(row_index, column_index, QTableWidgetItem(str(cell_data)))


def main():
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
