from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QDateEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
    QComboBox
)

from PyQt5.QtCore import QDate

from database import create_booking, DEPOSIT_RATE


class BookingWindow(QWidget):

    def __init__(
        self,
        user_id,
        room_id,
        room_number,
        room_type,
        price,
        parent=None
    ):
        super().__init__(parent)

        # Store booking information
        self.user_id = user_id
        self.room_id = room_id
        self.room_number = room_number
        self.room_type = room_type
        self.price = price

        # Window settings
        self.setWindowTitle("Hotel Booking & Payment")
        self.setFixedSize(430, 600)

        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(8)

        # -------------------------------------------------
        # TITLE
        # -------------------------------------------------

        title = QLabel("Book Hotel Room")

        title.setStyleSheet("""
            QLabel {
                color: #1e3a8a;
                font-size: 22px;
                font-weight: bold;
                padding: 8px;
            }
        """)

        layout.addWidget(title)

        # -------------------------------------------------
        # ROOM INFORMATION
        # -------------------------------------------------

        room_number_label = QLabel(
            f"Room Number: {room_number}"
        )

        room_type_label = QLabel(
            f"Room Type: {room_type}"
        )

        room_price_label = QLabel(
            f"Room Price: ${price:.2f} / night"
        )

        room_number_label.setStyleSheet("""
            QLabel {
                color: #374151;
                font-size: 14px;
                padding: 3px;
            }
        """)

        room_type_label.setStyleSheet("""
            QLabel {
                color: #374151;
                font-size: 14px;
                padding: 3px;
            }
        """)

        room_price_label.setStyleSheet("""
            QLabel {
                color: #2563eb;
                font-size: 15px;
                font-weight: bold;
                padding: 3px;
            }
        """)

        layout.addWidget(room_number_label)
        layout.addWidget(room_type_label)
        layout.addWidget(room_price_label)

        # -------------------------------------------------
        # CHECK-IN DATE
        # -------------------------------------------------

        check_in_title = QLabel("Check-in Date")

        check_in_title.setStyleSheet("""
            QLabel {
                color: #374151;
                font-weight: bold;
                padding-top: 5px;
            }
        """)

        layout.addWidget(check_in_title)

        self.check_in = QDateEdit()

        self.check_in.setCalendarPopup(True)
        self.check_in.setMinimumDate(QDate.currentDate())
        self.check_in.setDate(QDate.currentDate())

        self.check_in.setStyleSheet("""
            QDateEdit {
                background-color: white;
                color: #222222;
                border: 1px solid #cbd5e1;
                border-radius: 5px;
                padding: 7px;
            }
        """)

        self.check_in.dateChanged.connect(
            self.update_payment
        )

        layout.addWidget(self.check_in)

        # -------------------------------------------------
        # CHECK-OUT DATE
        # -------------------------------------------------

        check_out_title = QLabel("Check-out Date")

        check_out_title.setStyleSheet("""
            QLabel {
                color: #374151;
                font-weight: bold;
                padding-top: 5px;
            }
        """)

        layout.addWidget(check_out_title)

        self.check_out = QDateEdit()

        self.check_out.setCalendarPopup(True)
        self.check_out.setMinimumDate(
            QDate.currentDate().addDays(1)
        )
        self.check_out.setDate(
            QDate.currentDate().addDays(1)
        )

        self.check_out.setStyleSheet("""
            QDateEdit {
                background-color: white;
                color: #222222;
                border: 1px solid #cbd5e1;
                border-radius: 5px;
                padding: 7px;
            }
        """)

        self.check_out.dateChanged.connect(
            self.update_payment
        )

        layout.addWidget(self.check_out)

        # -------------------------------------------------
        # PAYMENT SUMMARY LABELS
        # -------------------------------------------------

        self.nights_label = QLabel()
        self.total_label = QLabel()
        self.deposit_label = QLabel()
        self.balance_label = QLabel()

        # Number of nights
        self.nights_label.setStyleSheet("""
            QLabel {
                color: #374151;
                background-color: #f3f4f6;
                padding: 8px;
                border-radius: 5px;
                font-size: 15px;
                font-weight: bold;
            }
        """)

        # Total amount
        self.total_label.setStyleSheet("""
            QLabel {
                color: #1e40af;
                background-color: #dbeafe;
                padding: 10px;
                border-radius: 6px;
                font-size: 16px;
                font-weight: bold;
            }
        """)

        # 20% deposit
        self.deposit_label.setStyleSheet("""
            QLabel {
                color: #991b1b;
                background-color: #fee2e2;
                padding: 10px;
                border-radius: 6px;
                font-size: 16px;
                font-weight: bold;
            }
        """)

        # Remaining balance
        self.balance_label.setStyleSheet("""
            QLabel {
                color: #065f46;
                background-color: #d1fae5;
                padding: 10px;
                border-radius: 6px;
                font-size: 16px;
                font-weight: bold;
            }
        """)

        layout.addWidget(self.nights_label)
        layout.addWidget(self.total_label)
        layout.addWidget(self.deposit_label)
        layout.addWidget(self.balance_label)

        # -------------------------------------------------
        # PAYMENT METHOD
        # -------------------------------------------------

        payment_title = QLabel("Payment Method")

        payment_title.setStyleSheet("""
            QLabel {
                color: #374151;
                font-weight: bold;
                padding-top: 5px;
            }
        """)

        layout.addWidget(payment_title)

        self.payment_method = QComboBox()

        self.payment_method.addItems([
            "Cash",
            "KBZ Pay",
            "Wave Pay",
            "Credit/Debit Card"
        ])

        self.payment_method.setStyleSheet("""
            QComboBox {
                background-color: white;
                color: #222222;
                border: 1px solid #cbd5e1;
                border-radius: 5px;
                padding: 8px;
            }

            QComboBox QAbstractItemView {
                background-color: white;
                color: #222222;
                selection-background-color: #dbeafe;
                selection-color: #1e3a8a;
            }
        """)

        layout.addWidget(self.payment_method)

        # -------------------------------------------------
        # DEPOSIT NOTICE
        # -------------------------------------------------

        note = QLabel(
            "Booking requires a 20% deposit payment."
        )

        note.setStyleSheet("""
            QLabel {
                color: #92400e;
                background-color: #fef3c7;
                padding: 10px;
                border-radius: 6px;
                font-weight: bold;
            }
        """)

        layout.addWidget(note)

        # -------------------------------------------------
        # BOOKING BUTTON
        # -------------------------------------------------

        book_button = QPushButton(
            "Pay 20% Deposit & Confirm Booking"
        )

        book_button.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 11px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #1d4ed8;
            }

            QPushButton:pressed {
                background-color: #1e40af;
            }
        """)

        book_button.clicked.connect(
            self.confirm_booking
        )

        layout.addWidget(book_button)

        # Set layout
        self.setLayout(layout)

        # Calculate payment when window opens
        self.update_payment()

    # =====================================================
    # CALCULATE PAYMENT
    # =====================================================

    def calculate_amounts(self):

        nights = self.check_in.date().daysTo(
            self.check_out.date()
        )

        total = nights * self.price

        deposit = total * DEPOSIT_RATE

        balance = total - deposit

        return nights, total, deposit, balance

    # =====================================================
    # UPDATE PAYMENT DISPLAY
    # =====================================================

    def update_payment(self):

        nights, total, deposit, balance = (
            self.calculate_amounts()
        )

        self.nights_label.setText(
            f"Number of Nights: {nights}"
        )

        self.total_label.setText(
            f"Total Amount: ${total:.2f}"
        )

        self.deposit_label.setText(
            f"20% Deposit Required: ${deposit:.2f}"
        )

        self.balance_label.setText(
            f"Remaining Balance: ${balance:.2f}"
        )

    # =====================================================
    # CONFIRM BOOKING
    # =====================================================

    def confirm_booking(self):

        check_in = self.check_in.date()
        check_out = self.check_out.date()

        # Check dates
        if check_out <= check_in:

            QMessageBox.warning(
                self,
                "Invalid Date",
                "Check-out date must be after check-in date."
            )

            return

        # Calculate payment
        nights, total, deposit, balance = (
            self.calculate_amounts()
        )

        # Get payment method
        method = self.payment_method.currentText()

        # Confirm payment
        reply = QMessageBox.question(
            self,
            "Confirm Payment",

            f"Room Number: {self.room_number}\n"
            f"Room Type: {self.room_type}\n\n"
            f"Number of Nights: {nights}\n"
            f"Total Amount: ${total:.2f}\n"
            f"20% Deposit: ${deposit:.2f}\n"
            f"Remaining Balance: ${balance:.2f}\n"
            f"Payment Method: {method}\n\n"
            "Do you want to pay the 20% deposit "
            "and confirm this booking?",

            QMessageBox.Yes | QMessageBox.No,

            QMessageBox.No
        )

        # User selected No
        if reply != QMessageBox.Yes:
            return

        # -------------------------------------------------
        # SAVE BOOKING TO DATABASE
        # -------------------------------------------------

        success, message = create_booking(
            self.user_id,
            self.room_id,
            check_in.toString("yyyy-MM-dd"),
            check_out.toString("yyyy-MM-dd"),
            total,
            deposit,
            method
        )

        # -------------------------------------------------
        # BOOKING SUCCESS
        # -------------------------------------------------

        if success:

            QMessageBox.information(
                self,
                "Booking Successful",
                "Booking confirmed successfully!\n\n"
                f"20% Deposit Paid: ${deposit:.2f}\n"
                f"Remaining Balance: ${balance:.2f}"
            )

            # Close booking window
            self.close()

            # Refresh Dashboard
            if self.parent():

                if hasattr(
                    self.parent(),
                    "load_rooms"
                ):
                    self.parent().load_rooms()

                if hasattr(
                    self.parent(),
                    "load_bookings"
                ):
                    self.parent().load_bookings()

        # -------------------------------------------------
        # BOOKING FAILED
        # -------------------------------------------------

        else:

            QMessageBox.warning(
                self,
                "Booking Error",
                message
            )