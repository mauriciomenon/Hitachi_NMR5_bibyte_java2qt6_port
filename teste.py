import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
    QHeaderView, QSizePolicy
)
from PyQt6.QtCore import Qt

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("IEC-870-5 Unbalanced Mode")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.setupInitialComponents(layout)
        self.setupMainTable(layout)
        self.setupSecondTable(layout)

        self.showMaximized()

    def setupInitialComponents(self, layout):
        layout.addWidget(QLabel("SOSTAT"))
        layout.addWidget(QLabel("Conversor BitByte <-> PTNO"))

        self.entry_bitbyte = QLineEdit()
        layout.addWidget(self.entry_bitbyte)

        buttons_layout = QHBoxLayout()
        self.createButton("Calcular PTNO", self.calcula_1, buttons_layout)
        self.createButton("Calcular Bit...", self.calcula_2, buttons_layout)
        layout.addLayout(buttons_layout)

        self.entry_ptno_bitbyte_resultbox = QLineEdit("Resultado")
        self.entry_ptno_bitbyte_resultbox.setReadOnly(True)
        self.entry_ptno_bitbyte_resultbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.entry_ptno_bitbyte_resultbox)

        self.createButton("Limpar valores", self.limpar_valores, layout)
        layout.addWidget(QLabel("Localização/código de cores dos cabos"))
        self.createButton("Localização das UTRs", lambda: None, layout)
        self.createButton("Código e Cores dos Cabos de UTRs", lambda: None, layout)

    def setupMainTable(self, layout):
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["Nome da UTR", "Código SOM", "Logic", "Link", "Localização Física", "Unidade", "Cota [m]", "Eixo (Casa de Força)"])
        self.table.setSortingEnabled(True)
        layout.addWidget(self.table)
        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.add_table_data()
        self.createButton("Procurar Geral", self.procurar_geral, layout)

    def setupSecondTable(self, layout):
        self.second_table = QTableWidget()
        self.second_table.setColumnCount(4)
        self.second_table.setHorizontalHeaderLabels(["Nome da UTR", "Localização", "Detalhes", "Observações"])
        self.second_table.setSortingEnabled(True)
        layout.addWidget(self.second_table)
        self.second_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.second_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.populate_second_table()

    def createButton(self, text, function, layout):
        button = QPushButton(text)
        button.clicked.connect(function)
        layout.addWidget(button)

    def limpar_valores(self):
        self.entry_bitbyte.clear()
        self.entry_ptno_bitbyte_resultbox.setText("Resultado")
        self.entry_ptno_bitbyte_resultbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def procurar_geral(self):
        search_text = self.entry_bitbyte.text().strip().lower()
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and search_text in item.text().strip().lower():
                    item.setSelected(True)

    def calcula_1(self):
        t1 = self.entry_bitbyte.text().strip()
        try:
            n1 = int(t1)
            result, message, title = self.calculo_1_logica(n1)
            QMessageBox.information(self, title, message)
            self.entry_ptno_bitbyte_resultbox.setText(str(result))
        except ValueError:
            QMessageBox.warning(self, "Erro", "Entrada inválida. Por favor, insira um número válido.")

    def calcula_2(self):
        t2 = self.entry_bitbyte.text().strip()
        try:
            n2 = int(t2)
            result, message, title = self.calculo_2_logica(n2)
            QMessageBox.information(self, title, message)
            self.entry_ptno_bitbyte_resultbox.setText(str(result))
        except ValueError:
            QMessageBox.warning(self, "Erro", "Entrada inválida. Por favor, insira um número válido.")

    def add_table_data(self):
        data = [
            ["UTR501", "A01R01", "1", "1", "Casa de Força", "U01", "108", "C-D"],
            # Adicione mais dados conforme necessário...
        ]

        self.table.setRowCount(len(data))
        for row_index, row_data in enumerate(data):
            for column_index, cell_data in enumerate(row_data):
                self.table.setItem(row_index, column_index, QTableWidgetItem(str(cell_data)))


    def populate_second_table(self):
        data = [
            ["UTR101", "Local A", "Detalhe 1", "Observação A"],
            # Adicione mais dados conforme necessário...
        ]

        self.second_table.setRowCount(len(data))
        for row_index, row_data in enumerate(data):
            for column_index, cell_data in enumerate(row_data):
                self.second_table.setItem(
                    row_index, column_index, QTableWidgetItem(str(cell_data))
                )


def main():
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
