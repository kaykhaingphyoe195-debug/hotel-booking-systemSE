import sqlite3

DATABASE_NAME = "hotel.db"

def initialize_database():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            room_id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_number TEXT UNIQUE NOT NULL,
            room_type TEXT NOT NULL,
            price REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'Available'
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            room_id INTEGER NOT NULL,
            check_in TEXT NOT NULL,
            check_out TEXT NOT NULL,
            status TEXT NOT NULL,
            total_amount REAL NOT NULL DEFAULT 0,
            deposit_amount REAL NOT NULL DEFAULT 0,
            payment_status TEXT NOT NULL DEFAULT 'Pending',
            payment_method TEXT DEFAULT '',
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (room_id) REFERENCES rooms(room_id)
        )
    """)

    # Add payment columns to an existing database created by an older version.
    cursor.execute("PRAGMA table_info(bookings)")
    booking_columns = {row[1] for row in cursor.fetchall()}
    migrations = [
        ("total_amount", "REAL NOT NULL DEFAULT 0"),
        ("deposit_amount", "REAL NOT NULL DEFAULT 0"),
        ("payment_status", "TEXT NOT NULL DEFAULT 'Pending'"),
        ("payment_method", "TEXT DEFAULT ''")
    ]
    for column, definition in migrations:
        if column not in booking_columns:
            cursor.execute(f"ALTER TABLE bookings ADD COLUMN {column} {definition}")

    rooms = [
        ("101", "Single", 30.00, "Available"),
        ("102", "Single", 30.00, "Available"),
        ("201", "Double", 50.00, "Available"),
        ("202", "Double", 50.00, "Available"),
        ("301", "Deluxe", 80.00, "Available"),
        ("302", "Deluxe", 80.00, "Available"),
        ("401", "Suite", 120.00, "Available"),
        ("402", "Suite", 120.00, "Available")
    ]

    for room in rooms:
        try:
            cursor.execute("""
                INSERT INTO rooms (room_number, room_type, price, status)
                VALUES (?, ?, ?, ?)
            """, room)
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    initialize_database()
