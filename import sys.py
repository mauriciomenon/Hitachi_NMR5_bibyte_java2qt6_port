import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IEC-870-5 Unbalanced Mode")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Seção de Conversor BitByte <-> PTNO
        sostat_label = QLabel("SOSTAT")
        layout.addWidget(sostat_label)

        conversor_label = QLabel("Conversor BitByte <-> PTNO")
        layout.addWidget(conversor_label)

        self.entry_bitbyte = QLineEdit()
        layout.addWidget(self.entry_bitbyte)

        calcular_ptno_button = QPushButton("Calcular PTNO")
        layout.addWidget(calcular_ptno_button)

        self.entry_ptno = QLineEdit()
        layout.addWidget(self.entry_ptno)

        calcular_bit_button = QPushButton("Calcular Bit...")
        layout.addWidget(calcular_bit_button)

        limpar_button = QPushButton("Limpar valores")
        layout.addWidget(limpar_button)

        # Seção de Localização/código de cores dos cabos
        localizacao_label = QLabel("Localização/código de cores dos cabos")
        layout.addWidget(localizacao_label)

        localizacao_button = QPushButton("Localização das UTRs")
        layout.addWidget(localizacao_button)

        cod_cores_button = QPushButton("Código e Cores dos Cabos de UTRs")
        layout.addWidget(cod_cores_button)

        # Tabela completa
        self.table_frame = QWidget()
        layout.addWidget(self.table_frame)

        self.table = QTableWidget()
        self.table.setColumnCount(17)
        self.table.setHorizontalHeaderLabels(["UTR", "Code", "Logic", "Link", "Local", "Unidade", "Cota", "Eixo"] * 2)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        layout_table = QVBoxLayout()
        layout_table.addWidget(self.table)
        self.table_frame.setLayout(layout_table)

        # Botão Procurar Geral
        self.create_button("Procurar Geral", self.procurar_geral, layout_table)

    def create_button(self, text, function, layout):
        button = QPushButton(text)
        button.clicked.connect(function)
        layout.addWidget(button)

    def procurar_geral(self):
        # Lógica de pesquisa geral aqui
        # Por exemplo, você pode iterar pelos itens da tabela e encontrar correspondências com a pesquisa
        search_text = self.entry_bitbyte.text().strip().lower()
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and search_text in item.text().strip().lower():
                    item.setSelected(True)

def main():
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()