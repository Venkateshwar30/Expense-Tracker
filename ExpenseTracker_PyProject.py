import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import (QApplication, QFormLayout, QHeaderView,
                               QHBoxLayout, QLineEdit, QMainWindow,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget)
from PySide6.QtCharts import QChartView, QPieSeries, QChart


class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.items = 0
        self.total_sum = 0.0  

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Description", "Price"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        self.description = QLineEdit()
        self.description.setClearButtonEnabled(True)
        self.price = QLineEdit()
        self.price.setClearButtonEnabled(True)
        self.total_label = QLineEdit()  
        self.total_label.setReadOnly(True)  

        self.add = QPushButton("Add")
        self.clear = QPushButton("Clear")
        self.plot = QPushButton("Plot")
        self.total_btn = QPushButton("Calculate Total")  
        self.add.setEnabled(False)

        form_layout = QFormLayout()
        form_layout.addRow("Description", self.description)
        form_layout.addRow("Price", self.price)
        self.right = QVBoxLayout()
        self.right.addLayout(form_layout)
        self.right.addWidget(self.add)
        self.right.addWidget(self.total_btn)  
        self.right.addWidget(self.total_label)
        self.right.addWidget(self.plot)
        self.right.addWidget(self.chart_view)
        self.right.addWidget(self.clear)

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.table)
        self.layout.addLayout(self.right)
        
        self.add.clicked.connect(self.add_element)
        self.plot.clicked.connect(self.plot_data)
        self.clear.clicked.connect(self.clear_table)
        self.total_btn.clicked.connect(self.calculate_total)  
        self.description.textChanged.connect(self.check_disable)
        self.price.textChanged.connect(self.check_disable)

        self.fill_table()

    @Slot()
    def add_element(self):
        des = self.description.text()
        price = float(self.price.text())
 
        self.table.insertRow(self.items)
        description_item = QTableWidgetItem(des)
        price_item = QTableWidgetItem(f"{price:.2f}")
        price_item.setTextAlignment(Qt.AlignRight)

        self.table.setItem(self.items, 0, description_item)
        self.table.setItem(self.items, 1, price_item)

        self.description.clear()
        self.price.clear()

        self.items += 1
        self.calculate_total()  

    @Slot()
    def check_disable(self, s):
        enabled = bool(self.description.text() and self.price.text())
        self.add.setEnabled(enabled)

    @Slot()
    def plot_data(self):
        series = QPieSeries()
        for i in range(self.table.rowCount()):
            text = self.table.item(i, 0).text()
            number = float(self.table.item(i, 1).text())
            series.append(text, number)

        chart = QChart()
        chart.addSeries(series)
        chart.legend().setAlignment(Qt.AlignLeft)
        self.chart_view.setChart(chart)

    def fill_table(self, data=None):
        data = {"Water": 1000, "Electricity": 1000, "Rent": 10000,
                "Supermarket": 3000, "Internet": 500, "EMI": 5000,
                "Public transportation": 1000, "Tea/Coffee": 500, "Restaurants": 2000} if not data else data
        self.total_sum = 0.0  
        for desc, price in data.items():
            description_item = QTableWidgetItem(desc)
            price_item = QTableWidgetItem(f"{price:.2f}")
            price_item.setTextAlignment(Qt.AlignRight)
            self.table.insertRow(self.items)
            self.table.setItem(self.items, 0, description_item)
            self.table.setItem(self.items, 1, price_item)
            self.total_sum += price  
            self.items += 1   

    @Slot()
    def calculate_total(self):
        total=0.0
        for row in range(self.table.rowCount()):
            price_item = self.table.item(row, 1)
            if price_item is not None:
                total += float(price_item.text())

        # Update total label with the calculated total
        self.total_label.setText(f"Total: {total:.2f}")



    @Slot()
    def clear_table(self):
        self.table.setRowCount(0)
        self.items = 0
        self.total_sum = 0.0  
        self.total_label.clear()


class MainWindow(QMainWindow):
    def __init__(self, widget):
        super().__init__()
        self.setWindowTitle("Expense Tracker By Venkateshwar")

        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        exit_action = self.file_menu.addAction("Exit", self.close)
        exit_action.setShortcut("Ctrl+Q")

        self.setCentralWidget(widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    window = MainWindow(widget)
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
