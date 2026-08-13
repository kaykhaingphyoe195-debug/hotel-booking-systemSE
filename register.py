from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from database import register_user

class RegisterWindow(QWidget):
    def __init__(self, login_window=None):
        super().__init__()
        self.login_window = login_window
        self.setWindowTitle("Hotel Booking - Registration")
        self.setFixedSize(400, 350)

        layout = QVBoxLayout()
        title = QLabel("Create New Account")
        title.setStyleSheet("font-size: 22px; font-weight: bold;")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm Password")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)

        register_button = QPushButton("Register")
        register_button.clicked.connect(self.register)
        back_button = QPushButton("Back to Login")
        back_button.clicked.connect(self.back_to_login)

        for widget in [title, self.username_input, self.email_input,
                       self.password_input, self.confirm_password_input,
                       register_button, back_button]:
            layout.addWidget(widget)
        self.setLayout(layout)

    def register(self):
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not username or not email or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
            return
        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return

        success, message = register_user(username, password, email)
        if success:
            QMessageBox.information(self, "Success", message)
            self.back_to_login()
        else:
            QMessageBox.warning(self, "Registration Error", message)

    def back_to_login(self):
        self.close()
        if self.login_window:
            self.login_window.show()
