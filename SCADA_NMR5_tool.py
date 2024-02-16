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
    QSizePolicy,
)
from PyQt6.QtCore import Qt


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("IEC-870-5 Unbalanced Mode")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Configurações iniciais (labels, botões, etc.)
        self.setupInitialComponents(layout)

        # Configuração da tabela principal
        self.setupMainTable(layout)

        # Configuração da segunda tabela (Localização das UTRs)
        self.setupSecondTable(layout)

        self.showMaximized()

    def setupInitialComponents(self, layout):
        # Componentes como labels, lineEdits, e botões...
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
        # Configuração da tabela principal
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            [
                "Nome da UTR",
                "Código SOM",
                "Logic",
                "Link",
                "Localização Física",
                "Unidade",
                "Cota [m]",
                "Eixo (Casa de Força)",
            ]
        )
        self.table.setSortingEnabled(True)
        layout.addWidget(self.table)
        self.table.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self.addTableData(self.table)
        self.createButton("Procurar Geral", self.procurar_geral, layout)

    def setupSecondTable(self, layout):
        # Configuração da segunda tabela (Localização das UTRs)
        self.second_table = QTableWidget()
        self.second_table.setColumnCount(
            4
        )  # Por exemplo, se a segunda tabela tiver 4 colunas
        self.second_table.setHorizontalHeaderLabels(
            ["Nome da UTR", "Localização", "Detalhes", "Observações"]
        )
        self.second_table.setSortingEnabled(True)
        layout.addWidget(self.second_table)
        self.second_table.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.second_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self.addTableData(
            self.second_table
        )  # Você pode precisar de uma função diferente para preencher esta tabela

    def createButton(self, text, function, layout):
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

    def add_table_data(self):
        # Dados a serem inseridos na tabela
        data = [
            ["UTR501", "A01R01", "1", "1", "Casa de Força", "U01", "108", "C-D"],
            ["UTR502", "A02R01", "2", "2", "Casa de Força", "U02", "108", "C-D"],
            ["UTR503", "A03R01", "3", "3", "Casa de Força", "U03", "108", "C-D"],
            ["UTR504", "A04R01", "4", "4", "Casa de Força", "U04", "108", "C-D"],
            ["UTR505", "A05R01", "5", "5", "Casa de Força", "U05", "108", "C-D"],
            ["UTR506", "A06R01", "6", "1", "Casa de Força", "U06", "108", "C-D"],
            ["UTR507", "A07R01", "7", "7", "Casa de Força", "U07", "108", "C-D"],
            ["UTR508", "A08R01", "8", "8", "Casa de Força", "U08", "108", "C-D"],
            ["UTR509", "A09R01", "9", "9", "Casa de Força", "U09", "108", "C-D"],
            ["UTR610", "B10R01", "10", "10", "Casa de Força", "U10", "108", "C-D"],
            ["UTR611", "B11R01", "11", "11", "Casa de Força", "U11", "108", "C-D"],
            ["UTR612", "B12R01", "12", "12", "Casa de Força", "U12", "108", "C-D"],
            ["UTR613", "B13R01", "13", "13", "Casa de Força", "U13", "108", "C-D"],
            ["UTR614", "B14R01", "14", "14", "Casa de Força", "U14", "108", "C-D"],
            ["UTR615", "B15R01", "15", "15", "Casa de Força", "U15", "108", "C-D"],
            ["UTR616", "B16R01", "16", "16", "Casa de Força", "U16", "108", "C-D"],
            ["UTR617", "B17R01", "17", "17", "Casa de Força", "U17", "108", "C-D"],
            ["UTR618", "B18R01", "18", "18", "Casa de Força", "U18", "108", "C-D"],
            ["UTR520", "C45A01", "20", "19", "GIS", "U02", "124", "A-B"],
            ["UTR520-1", "C45A02", "21", "20", "GIS", "U03", "124", "A-B"],
            ["UTR521", "C45A03", "22", "21", "GIS", "U05", "124", "A-B"],
            ["UTR522", "C45A04", "23", "22", "GIS", "U08", "124", "A-B"],
            ["UTR620", "D45A01", "24", "23", "GIS", "U12", "124", "A-B"],
            ["UTR621", "D45A02", "25", "24", "GIS", "U14", "124", "A-B"],
            ["UTR622", "D45A03", "26", "25", "GIS", "U16", "124", "A-B"],
            ["UTR622-1", "D45A04", "27", "26", "GIS", "U17", "124", "A-B"],
            ["UTR530", "J61A01", "30", "27", "Casa de Força", "U3", "115", "C-D"],
            ["UTR531", "J61A02", "31", "28", "Casa de Força", "U8", "115", "C-D"],
            ["UTR532", "J61A03", "32", "29", "Casa de Força", "AMD2", "127.6", "C-D"],
            ["UTR533", "J61A04", "33", "30", "Casa de Força", "AMD3", "144.5", "A-B"],
            ["UTR534", "J61A05", "34", "31", "Casa de Força", "U7", "127.6", "C-D"],
            ["UTR534-1", "J61A06", "35", "32", "GIS", "U9A", "132", "A-B"],
            ["UTR630", "K61A01", "36", "33", "Casa de Força", "U12", "115", "C-D"],
            ["UTR631", "K61A02", "37", "34", "Casa de Força", "AMC2", "127.6", "C-D"],
            ["UTR632", "K61A03", "38", "35", "Casa de Força", "U16", "115", "C-D"],
            ["UTR633", "K61A04", "39", "36", "Casa de Força", "AMC1", "144.5", "A-B"],
            ["UTR634", "K61A05", "40", "37", "Casa de Força", "U15", "115", "C-D"],
            ["UTR540", "J61A07", "41", "38", "Barragem", "U3", "214", ""],
            ["UTR541", "J61A08", "42", "39", "Barragem", "U9", "144.5", ""],
            ["UTR640", "K61A06", "43", "40", "Barragem", "U13", "214", ""],
            ["UTR641", "K61A07", "44", "41", "Barragem", "U16", "214", ""],
            ["UTR501-1", "A01R02", "51", "43", "Casa de Força", "U01", "98", "A-B"],
            ["UTR502-1", "A02R02", "52", "44", "Casa de Força", "U02", "98", "A-B"],
            ["UTR503-1", "A03R02", "53", "45", "Casa de Força", "U03", "98", "A-B"],
            ["UTR504-1", "A04R02", "54", "46", "Casa de Força", "U04", "98", "A-B"],
            ["UTR505-1", "A05R02", "55", "47", "Casa de Força", "U05", "98", "A-B"],
            ["UTR506-1", "A06R02", "56", "48", "Casa de Força", "U06", "98", "A-B"],
            ["UTR507-1", "A07R02", "57", "49", "Casa de Força", "U07", "98", "A-B"],
            ["UTR508-1", "A08R02", "58", "50", "Casa de Força", "U08", "98", "A-B"],
            ["UTR509-1", "A09R02", "59", "51", "Casa de Força", "U09", "98", "A-B"],
            ["UTR610-1", "B10R02", "60", "52", "Casa de Força", "U10", "98", "A-B"],
            ["UTR611-1", "B11R02", "61", "53", "Casa de Força", "U11", "98", "A-B"],
            ["UTR612-1", "B12R02", "62", "54", "Casa de Força", "U12", "98", "A-B"],
            ["UTR613-1", "B13R02", "63", "55", "Casa de Força", "U13", "98", "A-B"],
            ["UTR614-1", "B14R02", "64", "56", "Casa de Força", "U14", "98", "A-B"],
            ["UTR615-1", "B15R02", "65", "57", "Casa de Força", "U15", "98", "A-B"],
            ["UTR616-1", "B16R02", "66", "58", "Casa de Força", "U16", "98", "A-B"],
            ["UTR617-1", "B17R02", "67", "59", "Casa de Força", "U17", "98", "A-B"],
            ["UTR618-1", "B18R02", "68", "60", "Casa de Força", "U18", "98", "A-B"],
            ["UTR550", "H20A01", "80", "62", "Vertedouro", "", "214", ""],
            ["UTR570-2", "T75A04", "81", "63", "Casa de Força", "U10", "131", "C-D"],
            ["UTR670-1", "T75A05", "82", "64", "Casa de Força", "U9A", "131", "C-D"],
            ["UTR570-1", "T75A03", "84", "70", "Casa de Força", "U9A", "131", "C-D"],
            ["UTR670-2", "T75A06", "87", "71", "Casa de Força", "U10", "131", "C-D"],
        ]

        # Configuração do número de linhas com base nos dados
        self.table.setRowCount(len(data))

        # Preenchimento da tabela com os dados
        # Preenche a tabela com os dados
        for row_index, row_data in enumerate(data):
            for column_index, cell_data in enumerate(row_data):
                self.table.setItem(
                    row_index, column_index, QTableWidgetItem(str(cell_data))
                )


def main():
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
