from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox
import pyodbc
import Models.Materias
import functions

class HomeWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Home")
        self.setGeometry(300, 300, 300, 200)
        functions.FunctionsU.startQuery()
        print("Programa finalizado.")



if __name__ == "__main__":
    app = QApplication([])
    home_window = HomeWindow()
    home_window.show()
    app.exec()
