from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from database import login_user
from register import RegisterWindow
from dashboard import DashboardWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hotel Booking System - Login")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()
        title = QLabel("Hotel Booking System")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login)
        register_button = QPushButton("Create New Account")
        register_button.clicked.connect(self.open_register)

        for widget in [title, self.username_input, self.password_input,
                       login_button, register_button]:
            layout.addWidget(widget)
        self.setLayout(layout)

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        if not username or not password:
            QMessageBox.warning(self, "Error",
                                "Please enter username and password.")
            return

        user = login_user(username, password)
        if user:
            self.dashboard = DashboardWindow(user)
            self.dashboard.show()
            self.close()
        else:
            QMessageBox.warning(self, "Login Failed",
                                "Invalid username or password.")

    def open_register(self):
        self.register_window = RegisterWindow(self)
        self.register_window.show()
        self.hide()
