import sys
from PyQt5.QtWidgets import QApplication
from init_db import initialize_database
from login import LoginWindow

def main():
    initialize_database()
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
