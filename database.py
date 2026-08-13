import sqlite3

DATABASE_NAME = "hotel.db"
DEPOSIT_RATE = 0.20

def get_connection():
    return sqlite3.connect(DATABASE_NAME)

def register_user(username, password, email):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            (username, password, email)
        )
        conn.commit()
        return True, "Registration successful."
    except sqlite3.IntegrityError:
        return False, "Username or email already exists."
    finally:
        conn.close()

def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, email FROM users WHERE username=? AND password=?",
        (username, password)
    )
    user = cursor.fetchone()
    conn.close()
    return user

def search_rooms(keyword=""):
    conn = get_connection()
    cursor = conn.cursor()
    if keyword:
        cursor.execute("""
            SELECT room_id, room_number, room_type, price, status
            FROM rooms
            WHERE room_number LIKE ? OR room_type LIKE ?
        """, (f"%{keyword}%", f"%{keyword}%"))
    else:
        cursor.execute("""
            SELECT room_id, room_number, room_type, price, status
            FROM rooms
        """)
    rooms = cursor.fetchall()
    conn.close()
    return rooms

def get_room(room_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT room_id, room_number, room_type, price, status FROM rooms WHERE room_id=?",
        (room_id,)
    )
    room = cursor.fetchone()
    conn.close()
    return room

def create_booking(user_id, room_id, check_in, check_out,
                   total_amount, deposit_amount, payment_method):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT status FROM rooms WHERE room_id=?", (room_id,))
    room = cursor.fetchone()
    if room is None:
        conn.close()
        return False, "Room not found."
    if room[0] != "Available":
        conn.close()
        return False, "This room is not available."

    # The booking is created only after the 20% deposit is confirmed.
    cursor.execute("""
        INSERT INTO bookings
        (user_id, room_id, check_in, check_out, status,
         total_amount, deposit_amount, payment_status, payment_method)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id, room_id, check_in, check_out, "Booked",
        total_amount, deposit_amount, "Paid", payment_method
    ))
    cursor.execute(
        "UPDATE rooms SET status='Booked' WHERE room_id=?", (room_id,)
    )
    conn.commit()
    conn.close()
    return True, (
        f"Room booked successfully. 20% deposit paid: "
        f"${deposit_amount:.2f}. Remaining balance: "
        f"${total_amount - deposit_amount:.2f}."
    )

def get_user_bookings(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT bookings.booking_id, rooms.room_number, rooms.room_type,
               rooms.price, bookings.check_in, bookings.check_out,
               bookings.status, bookings.total_amount,
               bookings.deposit_amount, bookings.payment_status
        FROM bookings
        JOIN rooms ON bookings.room_id = rooms.room_id
        WHERE bookings.user_id = ?
        ORDER BY bookings.booking_id DESC
    """, (user_id,))
    bookings = cursor.fetchall()
    conn.close()
    return bookings

def cancel_booking(booking_id, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT room_id FROM bookings
        WHERE booking_id=? AND user_id=? AND status='Booked'
    """, (booking_id, user_id))
    booking = cursor.fetchone()
    if booking is None:
        conn.close()
        return False, "Booking not found."

    room_id = booking[0]
    cursor.execute("""
        UPDATE bookings SET status='Cancelled'
        WHERE booking_id=? AND user_id=?
    """, (booking_id, user_id))
    cursor.execute(
        "UPDATE rooms SET status='Available' WHERE room_id=?", (room_id,)
    )
    conn.commit()
    conn.close()
    return True, "Booking cancelled successfully."
