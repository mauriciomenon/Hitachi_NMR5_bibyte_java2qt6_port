import sys
from pathlib import Path

from analog_logic import AnalogResult, calculate_analog
from bitbyte_data import CABLE_COLOR_DATA, RTU_DATA
from bitbyte_logic import bitbyte_from_ptno_result, ptno_from_bitbyte_result
from PyQt6.QtGui import QColor, QPainter, QPen
from PyQt6.QtCore import QRectF, Qt
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


class AnalogGraph(QWidget):
    def __init__(self):
        super().__init__()
        self._result = AnalogResult(
            5.0,
            12.0,
            -2.5,
            10.0,
            19660,
            "0x4ccc",
            50.0,
            60.0,
            False,
        )
        self.setMinimumSize(260, 48)
        self.setMaximumHeight(56)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def set_result(self, result):
        self._result = result
        self.update()

    def paintEvent(self, a0):
        super().paintEvent(a0)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        bar_rect = QRectF(14, 18, self.width() - 28, 14)
        if bar_rect.width() <= 0 or bar_rect.height() <= 0:
            return

        painter.fillRect(self.rect(), QColor("#151515"))

        raw_fraction = self._result.raw_int16 / 32767
        clamped_fraction = max(0.0, min(raw_fraction, 1.0))
        marker_x = bar_rect.left() + clamped_fraction * bar_rect.width()
        fill_rect = QRectF(
            bar_rect.left(),
            bar_rect.top(),
            marker_x - bar_rect.left(),
            bar_rect.height(),
        )
        fill_color = (
            QColor("#e08f2a") if self._result.out_of_scale else QColor("#2da9e9")
        )

        painter.setPen(QPen(QColor("#555b61"), 1))
        painter.drawRoundedRect(bar_rect, 4, 4)
        painter.setBrush(fill_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(fill_rect, 4, 4)

        painter.setPen(QPen(QColor("#f1f3f5"), 2))
        painter.drawLine(
            int(marker_x),
            int(bar_rect.top()) - 6,
            int(marker_x),
            int(bar_rect.bottom()) + 6,
        )
        painter.drawEllipse(int(marker_x) - 3, int(bar_rect.center().y()) - 3, 6, 6)


class AnalogPanel(QGroupBox):
    def __init__(self):
        super().__init__("Analogico Raw Counts BIAS/SCALE v1.12")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        analog_layout = QVBoxLayout(self)
        analog_layout.setSpacing(6)
        analog_form_layout = QGridLayout()
        analog_form_layout.setHorizontalSpacing(6)
        analog_form_layout.setVerticalSpacing(6)
        analog_layout.addLayout(analog_form_layout)

        self.analog_lim_inf = QLineEdit("4")
        self.analog_lim_sup = QLineEdit("20")
        self.analog_range_inf = QLineEdit("0")
        self.analog_range_sup = QLineEdit("10")
        self.analog_measured = QLineEdit("5")
        self.analog_input_mode = QComboBox()
        self.analog_input_mode.addItems(["Medido", "mA", "INT16", "HEX16"])
        self.analog_current = QLabel("--")
        self.analog_measured_result = QLabel("--")
        self.analog_bias = QLabel("--")
        self.analog_scale = QLabel("--")
        self.analog_raw_int = QLabel("--")
        self.analog_raw_hex = QLabel("--")
        self.analog_primary_hex = QLabel("--")
        self.analog_primary_hex.setObjectName("analogPrimaryValue")
        self.analog_primary_int = QLabel("--")
        self.analog_primary_int.setObjectName("analogPrimaryIntValue")
        self.analog_status = QLabel("--")
        self.analog_status.setObjectName("analogStatusOk")
        self.analog_graph = AnalogGraph()

        fields = [
            ("Lim inf mA", self.analog_lim_inf),
            ("Lim sup mA", self.analog_lim_sup),
            ("Range inf", self.analog_range_inf),
            ("Range sup", self.analog_range_sup),
            ("Entrada", self.analog_input_mode),
            ("Valor", self.analog_measured),
        ]
        for row, (label, field) in enumerate(fields):
            analog_form_layout.addWidget(QLabel(label), row, 0)
            analog_form_layout.addWidget(field, row, 1)

        result_labels = [
            ("MEDIDO", self.analog_measured_result),
            ("mA", self.analog_current),
            ("BIAS", self.analog_bias),
            ("SCALE", self.analog_scale),
            ("INT16", self.analog_raw_int),
            ("HEX16", self.analog_raw_hex),
        ]
        for row, (label, value_label) in enumerate(result_labels):
            analog_form_layout.addWidget(QLabel(label), row, 2)
            analog_form_layout.addWidget(value_label, row, 3)

        primary_layout = QHBoxLayout()
        primary_layout.addWidget(self.analog_primary_hex, 3)
        primary_layout.addWidget(self.analog_primary_int, 2)
        analog_layout.addLayout(primary_layout)
        analog_layout.addWidget(self.analog_status)
        analog_layout.addWidget(self.analog_graph)
        analog_button = QPushButton("Calcular analogico")
        analog_button.clicked.connect(lambda: self.calculate_analog())
        analog_layout.addWidget(analog_button)
        self.calculate_analog(show_warning=False)

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
        self.analog_primary_hex.setText(f"0x{result.raw_hex16[2:].upper()}")
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
        self.analog_graph.set_result(result)

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
        controls_panel.setMaximumWidth(440)
        controls_layout = QVBoxLayout(controls_panel)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(6)
        self.setupInitialComponents(controls_layout)
        self.setupSecondTable(controls_layout)
        layout.addWidget(controls_panel, 0)

        tables_panel = QWidget()
        tables_layout = QVBoxLayout(tables_panel)
        tables_layout.setContentsMargins(0, 0, 0, 0)
        tables_layout.addWidget(QLabel("Localizacao das UTRs"))

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar nas tabelas")
        tables_layout.addWidget(self.search_input)
        self.createButton("Procurar Geral", self.procurar_geral, tables_layout)

        self.setupMainTable(tables_layout)
        layout.addWidget(tables_panel, 1)

        self.resize(1220, 760)

    def applyStyle(self):
        style_path = Path(__file__).with_name("style.qss")
        self.setStyleSheet(style_path.read_text(encoding="utf-8"))

    def setupInitialComponents(self, layout):
        bitbyte_box = QGroupBox("SOSTAT")
        bitbyte_layout = QVBoxLayout(bitbyte_box)
        layout.addWidget(bitbyte_box)

        bitbyte_layout.addWidget(QLabel("Conversor BitByte <-> PTNO"))

        self.entry_input = QLineEdit()
        bitbyte_layout.addWidget(self.entry_input)

        buttons_layout = QHBoxLayout()
        self.createButton("Calcular PTNO", self.calcula_2, buttons_layout)
        self.createButton("Calcular BitByte", self.calcula_1, buttons_layout)
        bitbyte_layout.addLayout(buttons_layout)

        self.entry_ptno_bitbyte_resultbox = QLineEdit("Resultado")
        self.entry_ptno_bitbyte_resultbox.setReadOnly(True)
        self.entry_ptno_bitbyte_resultbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bitbyte_layout.addWidget(self.entry_ptno_bitbyte_resultbox)

        self.createButton("Limpar valores", self.limpar_valores, bitbyte_layout)

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
            header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
            header.setStretchLastSection(False)
            header.setSectionResizeMode(4, QHeaderView.ResizeMode.Interactive)
            self.table.setColumnWidth(4, 260)
        layout.addWidget(panel)

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
            header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
            header.setStretchLastSection(False)
            self.second_table.setColumnWidth(0, 86)
            self.second_table.setColumnWidth(1, 62)
            self.second_table.setColumnWidth(2, 38)
            self.second_table.setColumnWidth(3, 38)
            self.second_table.setColumnWidth(4, 42)
            self.second_table.setColumnWidth(5, 78)
        layout.addWidget(panel)

    def createButton(self, text, function, layout):
        button = QPushButton(text)
        button.clicked.connect(function)
        layout.addWidget(button)

    def configure_table(self, table):
        table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        table.setAlternatingRowColors(True)
        table.setShowGrid(False)
        table.setWordWrap(False)
        vertical_header = table.verticalHeader()
        if vertical_header is not None:
            vertical_header.setDefaultSectionSize(28)

    def limpar_valores(self):
        self.entry_input.clear()
        self.entry_ptno_bitbyte_resultbox.setText("Resultado")
        self.entry_ptno_bitbyte_resultbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

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
