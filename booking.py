from PyQt5.QtWidgets import (
    QWidget, QLabel, QDateEdit, QPushButton, QVBoxLayout,
    QMessageBox, QComboBox
)
from PyQt5.QtCore import QDate
from database import create_booking, DEPOSIT_RATE

class BookingWindow(QWidget):
    def __init__(self, user_id, room_id, room_number, room_type, price, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.room_id = room_id
        self.room_number = room_number
        self.room_type = room_type
        self.price = price
        self.setWindowTitle("Hotel Booking & Payment")
        self.setMinimumSize(430, 520)

        layout = QVBoxLayout()
        layout.setSpacing(10)
        title = QLabel("Book Hotel Room")
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(title)

        layout.addWidget(QLabel(f"Room Number: {room_number}"))
        layout.addWidget(QLabel(f"Room Type: {room_type}"))
        layout.addWidget(QLabel(f"Room Price: ${price:.2f} / night"))

        layout.addWidget(QLabel("Check-in Date"))
        self.check_in = QDateEdit()
        self.check_in.setCalendarPopup(True)
        self.check_in.setMinimumDate(QDate.currentDate())
        self.check_in.setDate(QDate.currentDate())
        self.check_in.dateChanged.connect(self.update_payment)
        layout.addWidget(self.check_in)

        layout.addWidget(QLabel("Check-out Date"))
        self.check_out = QDateEdit()
        self.check_out.setCalendarPopup(True)
        self.check_out.setMinimumDate(QDate.currentDate().addDays(1))
        self.check_out.setDate(QDate.currentDate().addDays(1))
        self.check_out.dateChanged.connect(self.update_payment)
        layout.addWidget(self.check_out)

        self.nights_label = QLabel()
        self.total_label = QLabel()
        self.deposit_label = QLabel()
        self.balance_label = QLabel()
        for label in [self.nights_label, self.total_label,
                      self.deposit_label, self.balance_label]:
            layout.addWidget(label)

        layout.addWidget(QLabel("Payment Method"))
        self.payment_method = QComboBox()
        self.payment_method.addItems(["Cash", "KBZ Pay", "Wave Pay", "Credit/Debit Card"])
        layout.addWidget(self.payment_method)

        note = QLabel("Booking requires a 20% deposit payment.")
        note.setStyleSheet("font-weight: bold;")
        layout.addWidget(note)

        book_button = QPushButton("Pay 20% Deposit & Confirm Booking")
        book_button.clicked.connect(self.confirm_booking)
        layout.addWidget(book_button)
        layout.addStretch()

        self.setLayout(layout)
        self.update_payment()

    def calculate_amounts(self):
        nights = self.check_in.date().daysTo(self.check_out.date())
        total = nights * self.price
        deposit = total * DEPOSIT_RATE
        balance = total - deposit
        return nights, total, deposit, balance

    def update_payment(self):
        nights, total, deposit, balance = self.calculate_amounts()
        self.nights_label.setText(f"Number of Nights: {nights}")
        self.total_label.setText(f"Total Amount: ${total:.2f}")
        self.deposit_label.setText(f"20% Deposit Required: ${deposit:.2f}")
        self.balance_label.setText(f"Remaining Balance: ${balance:.2f}")

    def confirm_booking(self):
        check_in = self.check_in.date()
        check_out = self.check_out.date()

        if check_out <= check_in:
            QMessageBox.warning(
                self, "Invalid Date",
                "Check-out date must be after check-in date."
            )
            return

        nights, total, deposit, balance = self.calculate_amounts()
        method = self.payment_method.currentText()

        reply = QMessageBox.question(
            self,
            "Confirm Payment",
            f"Total: ${total:.2f}\n"
            f"20% Deposit: ${deposit:.2f}\n"
            f"Remaining Balance: ${balance:.2f}\n"
            f"Payment Method: {method}\n\n"
            "Do you want to pay the 20% deposit and confirm this booking?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        success, message = create_booking(
            self.user_id, self.room_id,
            check_in.toString("yyyy-MM-dd"),
            check_out.toString("yyyy-MM-dd"),
            total, deposit, method
        )

        if success:
            QMessageBox.information(self, "Booking & Payment Successful", message)
            self.close()
            if self.parent():
                self.parent().load_rooms()
                self.parent().load_bookings()
        else:
            QMessageBox.warning(self, "Booking Error", message)
            
        
        
