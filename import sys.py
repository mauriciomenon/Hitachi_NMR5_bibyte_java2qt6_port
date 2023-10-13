from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex, QSize
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableView, QSizePolicy

class MyTableModel(QAbstractTableModel):
    def __init__(self, data, headers):
        super().__init__()
        self._data = data
        self._headers = headers

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._data[0])

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._headers[section]

class MyTableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('TableRTU')

        layout = QVBoxLayout()

        self.table = QTableView()

        headers = ["UTR", "Code", "Logic", "Link", "Local", "Unidade", "Cota", "Eixo", "", "UTR", "Code", "Logic", "Link", "Local", "Unidade", "Cota", "Eixo"]
        data = [
            ["UTR501", "A01R01", "1", "1", "CF", "U1", "108", "C-D","","UTR520", "C45A01", "20", "19", "GIS", "U2", "124", "A-B"],
            ["UTR502", "A02R01", "2", "2", "CF", "U2", "108", "C-D","","UTR520-1", "C45A02", "21", "20", "GIS", "U3", "124", "A-B"],
            # Adicione mais linhas de dados aqui
        ]

        self.model = MyTableModel(data, headers)
        self.table.setModel(self.model)

        layout.addWidget(self.table)

        self.setLayout(layout)

        # Personalização adicional do layout e estilo da tabela
        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.table.setSortingEnabled(True)
        self.resize(QSize(890, 585))

if __name__ == '__main__':
    app = QApplication([])
    app.setStyle('Fusion')

    table_view = MyTableWidget()
    table_view.show()

    app.exec()
