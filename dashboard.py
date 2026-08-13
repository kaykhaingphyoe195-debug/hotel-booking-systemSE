from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout
)
from database import search_rooms, get_user_bookings, cancel_booking
from booking import BookingWindow

class DashboardWindow(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle("Hotel Booking Management System")
        self.resize(900, 650)

        main_layout = QVBoxLayout()
        title = QLabel(f"Welcome, {user[1]}")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        main_layout.addWidget(title)

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search room number or room type...")
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.load_rooms)
        all_button = QPushButton("Show All")
        all_button.clicked.connect(lambda: (self.search_input.clear(), self.load_rooms()))
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        search_layout.addWidget(all_button)
        main_layout.addLayout(search_layout)

        main_layout.addWidget(QLabel("Hotel Rooms"))
        self.room_table = QTableWidget()
        self.room_table.setColumnCount(5)
        self.room_table.setHorizontalHeaderLabels(
            ["ID", "Room Number", "Room Type", "Price", "Status"]
        )
        self.room_table.setSelectionBehavior(QTableWidget.SelectRows)
        main_layout.addWidget(self.room_table)

        book_button = QPushButton("Book Selected Room")
        book_button.clicked.connect(self.book_selected_room)
        main_layout.addWidget(book_button)

        main_layout.addWidget(QLabel("My Bookings"))
        self.booking_table = QTableWidget()
        self.booking_table.setColumnCount(10)
        self.booking_table.setHorizontalHeaderLabels(
            ["Booking ID", "Room", "Type", "Price", "Check-in", "Check-out",
             "Status", "Total", "20% Deposit", "Payment"]
        )
        self.booking_table.setSelectionBehavior(QTableWidget.SelectRows)
        main_layout.addWidget(self.booking_table)

        cancel_button = QPushButton("Cancel Selected Booking")
        cancel_button.clicked.connect(self.cancel_selected_booking)
        main_layout.addWidget(cancel_button)
        cancel_button.setStyleSheet("""
    QPushButton {
        background-color: #e74c3c;
        color: white;
        border-radius: 4px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #c0392b;
    }
""")
        

        logout_button = QPushButton("Logout")
        logout_button.clicked.connect(self.logout)
        main_layout.addWidget(logout_button)
        self.setStyleSheet("""
    QWidget {
        background-color: #f5f7fb;
        color: #222222;
        font-size: 14px;
    }

    QLabel {
        color: #333333;
        padding: 3px;
    }

    QLineEdit, QComboBox, QDateEdit {
        background-color: white;
        color: #222222;
        border: 1px solid #cccccc;
        border-radius: 5px;
        padding: 7px;
    }

    QPushButton {
        background-color: #2563eb;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 8px 15px;
        font-weight: bold;
    }

    QPushButton:hover {
        background-color: #1d4ed8;
    }

    QTableWidget {
        background-color: white;
        color: #222222;
        gridline-color: #d1d5db;
        border: 1px solid #d1d5db;
        border-radius: 5px;
    }

    QTableWidget::item {
        padding: 6px;
    }

    QTableWidget::item:selected {
        background-color: #dbeafe;
        color: #1e3a8a;
    }

    QHeaderView::section {
        background-color: #1e3a8a;
        color: white;
        padding: 8px;
        font-weight: bold;
        border: none;
    }
""")
        self.setLayout(main_layout)
        self.load_rooms()
        self.load_bookings()

    def load_rooms(self):
        rooms = search_rooms(self.search_input.text().strip())
        self.room_table.setRowCount(0)
        for row, room in enumerate(rooms):
            self.room_table.insertRow(row)
            for col, value in enumerate(room):
                self.room_table.setItem(row, col, QTableWidgetItem(str(value)))

    def book_selected_room(self):
        row = self.room_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a room.")
            return

        room_id = int(self.room_table.item(row, 0).text())
        room_number = self.room_table.item(row, 1).text()
        room_type = self.room_table.item(row, 2).text()
        price = float(self.room_table.item(row, 3).text())
        status = self.room_table.item(row, 4).text()

        if status != "Available":
            QMessageBox.warning(self, "Unavailable", "This room is already booked.")
            return

        self.booking_window = BookingWindow(
            self.user[0], room_id, room_number, room_type, price, self
        )
        self.booking_window.show()

    def load_bookings(self):
        bookings = get_user_bookings(self.user[0])
        self.booking_table.setRowCount(0)
        for row, booking in enumerate(bookings):
            self.booking_table.insertRow(row)
            for col, value in enumerate(booking):
                self.booking_table.setItem(row, col, QTableWidgetItem(str(value)))

    def cancel_selected_booking(self):
        row = self.booking_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a booking.")
            return

        booking_id = int(self.booking_table.item(row, 0).text())
        success, message = cancel_booking(booking_id, self.user[0])
        if success:
            QMessageBox.information(self, "Success", message)
            self.load_rooms()
            self.load_bookings()
        else:
            QMessageBox.warning(self, "Error", message)

    def logout(self):
        self.close()
        from login import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()