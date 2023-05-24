from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from home import HomeWindow


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(300, 300, 300, 200)

        self.username_label = QLabel("Username:", self)
        self.username_label.move(20, 20)
        self.username_input = QLineEdit(self)
        self.username_input.move(100, 20)

        self.password_label = QLabel("Password:", self)
        self.password_label.move(20, 50)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.move(100, 50)

        self.login_button = QPushButton("Login", self)
        self.login_button.move(100, 100)
        self.login_button.clicked.connect(self.login)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "admin" and password == "password":
            home_window = HomeWindow()
            self.close()
            home_window.show()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password!")

if __name__ == "__main__":
    app = QApplication([])
    login_window = LoginWindow()
    login_window.show()
    app.exec()
