import sqlite3
import sys
import traceback

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QDialog


class EditDB(QDialog):
    def __init__(self):
        super(EditDB, self).__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)

    def accept(self) -> None:
        try:
            with sqlite3.connect('coffee.sqlite') as con:
                cur = con.cursor()
                cur.execute('INSERT INTO coffee(Name, Roasting, Type, Taste, Price, Size) VALUES (?,?,?,?,?,?)',
                            (self.NameLineEdit.text(), self.RoastingLineEdit.text(), self.TypeLineEdit.text(),
                             self.TasteLineEdit.text(), self.PriceLineEdit.text(), self.SizeLineEdit.text()))
                con.commit()
            self.done(0)
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", str(e))
            self.done(1)

    def reject(self) -> None:
        self.done(0)


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi("main.ui", self)
        self.table()
        self.addInfoButton.clicked.connect(self.run)

    def run(self) -> None:
        sys.excepthook = except_hook
        EDB = EditDB()
        if EDB.exec() == QDialog.Accepted:
            self.table()

    def table(self) -> None:
        try:
            with sqlite3.connect('coffee.sqlite') as con:
                cur = con.cursor()
                cur.execute("SELECT Name, Roasting, Type, Taste, Price, Size FROM coffee")
                db = cur.fetchall()
                self.tableWidget.setColumnCount(len(db[0]))
                self.tableWidget.setRowCount(len(db))
                self.tableWidget.setHorizontalHeaderLabels(["Name", "Roasting", "Type", "Taste", "Price", "Size"])
                for i, row in enumerate(db):
                    for j, value in enumerate(row):
                        self.tableWidget.setItem(i, j, QTableWidgetItem(value))
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", str(e))


def except_hook(cls, exception, trace):
    tb = "".join(traceback.format_exception(cls, exception, trace))
    print(tb)
    QMessageBox.critical(None, "Critical Error", tb)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    win = Window()
    win.show()
    sys.exit(app.exec())
