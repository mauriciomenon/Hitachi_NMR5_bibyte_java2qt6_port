import sys
from PyQt6.QtWidgets import (
    QApplication,
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
)
from PyQt6.QtCore import Qt


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IEC-870-5 Unbalanced Mode")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Seção de Conversor BitByte <-> PTNO
        sostat_label = QLabel("SOSTAT")
        layout.addWidget(sostat_label)

        conversor_label = QLabel("Conversor BitByte <-> PTNO")
        layout.addWidget(conversor_label)

        self.entry_bitbyte = QLineEdit()
        layout.addWidget(self.entry_bitbyte)

        buttons_layout = QHBoxLayout()  # Botões de cálculo

        calcular_ptno_button = QPushButton("Calcular PTNO")
        calcular_ptno_button.clicked.connect(self.calcula_1)
        buttons_layout.addWidget(calcular_ptno_button)

        calcular_bit_button = QPushButton("Calcular Bit...")
        calcular_bit_button.clicked.connect(self.calcula_2)
        buttons_layout.addWidget(calcular_bit_button)

        layout.addLayout(buttons_layout)

        # central_widget.setLayout(layout)    # layout resultado
        # central_widget = QWidget()
        # self.setCentralWidget(central_widget)
        # layout = QVBoxLayout()
        # central_widget.setLayout(layout)  # Layout horizontal para os botões

        self.entry_ptno_bitbyte_resultbox = QLineEdit("Resultado")
        self.entry_ptno_bitbyte_resultbox.setReadOnly(True)
        self.entry_ptno_bitbyte_resultbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.entry_ptno_bitbyte_resultbox)

        limpar_button = QPushButton("Limpar valores")
        limpar_button.clicked.connect(self.limpar_valores)
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
        self.table.setHorizontalHeaderLabels(
            ["UTR", "Code", "Logic", "Link", "Local", "Unidade", "Cota", "Eixo"] * 2
        )
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        layout_table = QVBoxLayout()
        layout_table.addWidget(self.table)
        self.table_frame.setLayout(layout_table)

        # Botão Procurar Geral
        self.create_button("Procurar Geral", self.procurar_geral, layout_table)

    def create_button(self, text, function, layout):
        button = QPushButton(text)
        button.clicked.connect(function)
        layout.addWidget(button)

    def limpar_valores(self):
        self.entry_bitbyte.clear()
        self.entry_ptno_bitbyte_resultbox.setText("Resultado")
        self.entry_ptno_bitbyte_resultbox.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )  # Re-centraliza o texto após limpeza

    def procurar_geral(self):
        # Lógica de pesquisa geral aqui
        search_text = self.entry_bitbyte.text().strip().lower()
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and search_text in item.text().strip().lower():
                    item.setSelected(True)

    # Funções de cálculo
    def calcula_1(self):
        t1 = self.entry_bitbyte.text().strip()
        try:
            n1 = int(t1)
            result, message, title = self.calculo_1_logica(n1)
            QMessageBox.information(self, title, message)
            self.entry_ptno_bitbyte_resultbox.setText(str(result))
        except ValueError:
            QMessageBox.warning(
                self, "Erro", "Entrada inválida. Por favor, insira um número válido."
            )

    def calculo_1_logica(self, n1):
        result = 0
        message = "Não definido"
        title = "Erro"

        if 0 <= n1 <= 2047:
            result = n1
            message = (
                "Calculadora para SOSTAT, verifique a SOANLG para pontos analógicos"
            )
            title = "Erro"
        elif 10000 <= n1 <= 11023:
            result = (n1 - 10000) * 2
            message = "Resultado para um ponto 2WAY sem TimeStamp"
        elif 15000 <= n1 <= 16023:
            result = ((n1 - 15000) * 2) + 2048
        elif 25000 <= n1 <= 25063:
            result = (((n1 - 25000) // 8) * 16) + (((n1 - 25000) % 8) + 4608)
        elif 36000 <= n1 <= 36063:
            result = (((n1 - 36000) // 8) * 16) + (((n1 - 36000) % 8) + 5632)
        elif 36088 <= n1 <= 36095:
            result = (((n1 - 36064) // 8) * 16) + (((n1 - 36064) % 8) + 5760)
            message = f"Resultado: {result}"
        else:
            message = "Verifique valores e intervalos válidos na documentação"
            title = "Erro:"
            result = 0
        return result, message, title

    def calcula_2(self):
        t2 = self.entry_bitbyte.text().strip()
        try:
            n2 = int(t2)
            result, message, title = self.calculo_2_logica(n2)
            QMessageBox.information(self, title, message)
            # self.entry_bitbyte.setText(str(result))
            self.entry_ptno_bitbyte_resultbox.setText(str(result))
        except ValueError:
            QMessageBox.warning(
                self, "Erro", "Entrada inválida. Por favor, insira um número válido."
            )

    def calculo_2_logica(self, n2):
        result = 0
        # message = ""
        # title = "Resultado"

        if 0 <= n2 <= 2047:
            result = (n2 // 2) + 10000
            message = "Cuidado, pode ser ponto Analógico"
        elif 2048 <= n2 <= 4095:
            if n2 % 2 != 0:
                message = "PTNO deve ser um número par"
                title = "Erro"
            else:
                result = (n2 + 27952) // 2
        elif 4096 <= n2 <= 4607:
            message = "Intervalo não utilizado"
            title = "Erro"
        elif 4608 <= n2 <= 5119:
            message = "TBD resto"  # ... [restante da lógica de cálculo] ...
            title = "TBD"
        elif 5120 <= n2 <= 5631:
            message = "Intervalo não utilizado"
            title = "Erro"
        elif 5632 <= n2 <= 6143:
            message = "TBD resto"  # ... [restante da lógica de cálculo] ...
            title = "TBD"
        elif 6144 <= n2 <= 6999:
            message = "Intervalo não utilizado"
            title = "Erro"
        elif 7000 <= n2 <= 8192:
            result = 0
            message = "Todo Pseudo point tem BITBYTE nulo"
            title = "Atenção"
        else:
            message = "Verifique valores e intervalos válidos na documentação"
            title = "Erro:"
            result = 0
        return result, message, title


def main():
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
