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
            self.done(QDialog.Accepted)
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", str(e))
            self.done(QDialog.Rejected)

    def reject(self) -> None:
        self.done(QDialog.Rejected)


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi("main.ui", self)
        self.table()
        self.addInfoButton.clicked.connect(self.run)
        self.deleteInfoButton.clicked.connect(self.delete_record)

    def run(self) -> None:
        sys.excepthook = except_hook
        EDB = EditDB()
        if EDB.exec() == QDialog.Accepted:
            self.table()

    def delete_record(self) -> None:
        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
            coffee_name = self.tableWidget.item(selected_row, 0).text()
            try:
                with sqlite3.connect('coffee.sqlite') as con:
                    cur = con.cursor()
                    cur.execute('DELETE FROM coffee WHERE Name = ?', (coffee_name,))
                    con.commit()
                self.table()
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Database Error", str(e))
        else:
            QMessageBox.warning(self, "Selection Error", "Пожалуйста, выберите запись для удаления")

    def table(self) -> None:
        try:
            with sqlite3.connect('coffee.sqlite') as con:
                cur = con.cursor()
                cur.execute("SELECT Name, Roasting, Type, Taste, Price, Size FROM coffee")
                db = cur.fetchall()

                self.tableWidget.clear()
                self.tableWidget.setColumnCount(len(db[0]) if db else 0)
                self.tableWidget.setRowCount(len(db))
                self.tableWidget.setHorizontalHeaderLabels(["Name", "Roasting", "Type", "Taste", "Price", "Size"])

                for i, row in enumerate(db):
                    for j, value in enumerate(row):
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(value)))
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", str(e))


def except_hook(cls, exception, trace):
    tb = "".join(traceback.format_exception(cls, exception, trace))
    print(tb)
    QMessageBox.critical(None, "Critical Error", tb)


# Точка входа (Entry point)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    win = Window()
    win.show()
    sys.exit(app.exec())
