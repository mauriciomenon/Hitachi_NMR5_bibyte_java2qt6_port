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


def add_action_button(text, function, layout, compact=False):
    button = QPushButton(text)
    button.setObjectName("compactButton" if compact else "standardButton")
    button.clicked.connect(function)
    layout.addWidget(button)
    return button


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
        self.setMinimumSize(160, 52)
        self.setMaximumHeight(52)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def set_result(self, result):
        self._result = result
        self.update()

    def paintEvent(self, a0):
        super().paintEvent(a0)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        available_width = self.width() - 24
        bar_width = max(10, int(available_width * 0.25))
        bar_left = (self.width() - bar_width) / 2
        bar_rect = QRectF(bar_left, 24, bar_width, 12)
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
            int(bar_rect.top()),
            int(marker_x),
            int(bar_rect.bottom()),
        )
        painter.drawEllipse(int(marker_x) - 3, int(bar_rect.center().y()) - 3, 6, 6)

        legend_font = painter.font()
        legend_font.setPointSize(4)
        painter.setFont(legend_font)
        legend_text = f"B:{self._result.bias:.3g} S:{self._result.scale:.3g}"
        if bar_rect.width() < 10:
            legend_text = "B"
        elif painter.fontMetrics().horizontalAdvance(legend_text) > bar_rect.width() - 4:
            legend_text = f"{self._result.bias:.2g}|{self._result.scale:.2g}"
        if painter.fontMetrics().horizontalAdvance(legend_text) > bar_rect.width() - 4:
            legend_text = f"{self._result.bias:.2g}"
        legend_rect = QRectF(
            bar_rect.left() + 2,
            bar_rect.top() + 1,
            bar_rect.width() - 4,
            bar_rect.height() - 2,
        )
        painter.fillRect(legend_rect, QColor(22, 24, 26, 180))
        painter.setPen(QPen(QColor("#d8dde3"), 1))
        painter.drawText(
            legend_rect,
            Qt.AlignmentFlag.AlignCenter,
            legend_text,
        )


class AnalogPanel(QGroupBox):
    def __init__(self):
        super().__init__("Analogico Raw Counts BIAS/SCALE v1.12")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        analog_layout = QVBoxLayout(self)
        analog_layout.setSpacing(2)
        analog_form_layout = QGridLayout()
        analog_form_layout.setHorizontalSpacing(3)
        analog_form_layout.setVerticalSpacing(2)
        analog_form_layout.setContentsMargins(0, 0, 0, 0)
        analog_layout.addLayout(analog_form_layout)

        self.analog_lim_inf = QLineEdit("4")
        self.analog_lim_inf.setObjectName("analogInputNarrow")
        self.analog_lim_sup = QLineEdit("20")
        self.analog_lim_sup.setObjectName("analogInputNarrow")
        self.analog_range_inf = QLineEdit("0")
        self.analog_range_inf.setObjectName("analogInputNarrow")
        self.analog_range_sup = QLineEdit("10")
        self.analog_range_sup.setObjectName("analogInputNarrow")
        self.analog_measured = QLineEdit("5")
        self.analog_measured.setObjectName("analogInputWide")
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
        self.analog_graph = AnalogGraph()

        self.preset_4_20 = QPushButton("4-20 mA")
        self.preset_4_20.setObjectName("analogPresetButton")
        self.preset_4_20.setToolTip("Automacao: 4-20mA com escala 0-10")
        self.preset_4_20.clicked.connect(self.apply_4_20_preset)
        self.preset_0_20 = QPushButton("0-20 mA")
        self.preset_0_20.setObjectName("analogPresetButton")
        self.preset_0_20.clicked.connect(self.apply_0_20_preset)

        preset_label = QLabel("Padrao automacao")
        preset_label.setObjectName("analogPresetLabel")
        preset_layout = QHBoxLayout()
        preset_layout.setSpacing(3)
        preset_layout.addWidget(preset_label)
        preset_layout.addWidget(self.preset_4_20)
        preset_layout.addWidget(self.preset_0_20)
        preset_layout.addStretch(1)
        analog_layout.addLayout(preset_layout)

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
            ("Med", self.analog_measured_result),
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
        analog_button.setObjectName("compactButton")
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
            else:
                self.analog_measured_result.setText("--")
                self.analog_current.setText("--")
                self.analog_bias.setText("--")
                self.analog_scale.setText("--")
                self.analog_raw_int.setText("--")
                self.analog_raw_hex.setText("--")
                self.analog_primary_hex.setText("--")
                self.analog_primary_int.setText("--")
                self.analog_status.setObjectName("analogStatusWarning")
                self.analog_status.setText(str(exc))
                status_style = self.analog_status.style()
                if status_style is not None:
                    status_style.unpolish(self.analog_status)
                    status_style.polish(self.analog_status)
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
        self.analog_graph.set_result(result)

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
        super().__init__("SOSTAT")
        bitbyte_layout = QVBoxLayout(self)
        bitbyte_layout.setContentsMargins(8, 8, 8, 8)
        bitbyte_layout.setSpacing(6)

        bitbyte_layout.addWidget(QLabel("Conversor BitByte <-> PTNO"))

        self.entry_input = QLineEdit()
        self.entry_input.setPlaceholderText("Digite PTNO ou BitByte")
        self.entry_input.setObjectName("ptnoInput")
        entry_row = QHBoxLayout()
        entry_row.setContentsMargins(2, 2, 2, 2)
        entry_row.setSpacing(4)
        entry_row.addWidget(self.entry_input)
        clear_button = add_action_button(
            "x", self.limpar_valores, entry_row, compact=True
        )
        clear_button.setFixedWidth(16)
        bitbyte_layout.addLayout(entry_row)

        self.entry_ptno_bitbyte_resultbox = QLineEdit("Resultado")
        self.entry_ptno_bitbyte_resultbox.setReadOnly(True)
        self.entry_ptno_bitbyte_resultbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.entry_ptno_bitbyte_resultbox.setObjectName("ptnoResult")
        bitbyte_layout.addWidget(self.entry_ptno_bitbyte_resultbox)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        buttons_layout.setContentsMargins(2, 2, 2, 2)
        ptno_button = add_action_button(
            "PTNO", self.calcula_2, buttons_layout, compact=True
        )
        bitbyte_button = add_action_button(
            "BitByte", self.calcula_1, buttons_layout, compact=True
        )
        ptno_button.setFixedWidth(70)
        bitbyte_button.setFixedWidth(70)
        bitbyte_layout.addLayout(buttons_layout)

    def limpar_valores(self):
        self.entry_input.clear()
        self.entry_ptno_bitbyte_resultbox.setText("Resultado")
        self.entry_ptno_bitbyte_resultbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def calcula_1(self):
        self._run_sostat_conversion(bitbyte_from_ptno_result)

    def calcula_2(self):
        self._run_sostat_conversion(ptno_from_bitbyte_result)

    def _run_sostat_conversion(self, converter):
        result, message, title = converter(self.entry_input.text())
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
        controls_panel.setMinimumWidth(360)
        controls_panel.setMaximumWidth(390)
        controls_layout = QVBoxLayout(controls_panel)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(8)
        self.setupInitialComponents(controls_layout)
        layout.addWidget(controls_panel, 0)

        tables_panel = QWidget()
        tables_layout = QVBoxLayout(tables_panel)
        tables_layout.setContentsMargins(0, 0, 0, 0)
        tables_layout.addWidget(QLabel("Localizacao das UTRs"))

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar nas tabelas")
        self.search_input.setObjectName("searchInput")
        search_layout = QHBoxLayout()
        search_layout.setSpacing(3)
        search_layout.addWidget(self.search_input)
        add_action_button("Ir", self.procurar_geral, search_layout, compact=True)
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
        add_action_button(
            "Localizacao das UTRs", self.focus_main_table, panel_layout
        )
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
            self.table.setColumnWidth(0, 70)
            self.table.setColumnWidth(1, 46)
            self.table.setColumnWidth(2, 34)
            self.table.setColumnWidth(3, 30)
            self.table.setColumnWidth(4, 82)
            self.table.setColumnWidth(5, 44)
            self.table.setColumnWidth(6, 54)
            self.table.setColumnWidth(7, 36)
        layout.addWidget(panel, 2)

    def setupSecondTable(self, layout):
        panel = QWidget()
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(0, 0, 0, 0)
        add_action_button(
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
            self.second_table.setColumnWidth(0, 40)
            self.second_table.setColumnWidth(1, 46)
            self.second_table.setColumnWidth(2, 22)
            self.second_table.setColumnWidth(3, 28)
            self.second_table.setColumnWidth(4, 16)
            self.second_table.setColumnWidth(5, 116)
        layout.addWidget(panel, 1)

    def configure_table(self, table):
        table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        table.setAlternatingRowColors(True)
        table.setShowGrid(False)
        table.setWordWrap(False)
        vertical_header = table.verticalHeader()
        if vertical_header is not None:
            vertical_header.setDefaultSectionSize(26)

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
