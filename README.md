# Hotel Booking Management System

## Project Overview
A Python desktop Hotel Booking Management System using PyQt5 and SQLite3.

## Features
- User Registration
- User Login
- Hotel Room Search
- Room Availability
- Room Booking
- View My Bookings
- Cancel Booking
- SQLite database
- Error handling and validation

## Technologies
- Python 3
- PyQt5
- SQLite3
- Git and GitHub

## Database Schema

### users
- id
- username
- password
- email

### rooms
- room_id
- room_number
- room_type
- price
- status

### bookings
- booking_id
- user_id
- room_id
- check_in
- check_out
- status

## Installation
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Run
```bash
python init_db.py
python main.py
```

## GitHub Workflow
- Minimum 10 descriptive commits
- At least 2 branches
- At least 1 Pull Request
- At least 2 Issues

## Author
Yamin Shwe Zin Aung


## 20% Deposit Payment Feature

The booking system now requires a **20% deposit payment** before a booking is confirmed.

- Total amount = room price × number of nights
- Deposit = total amount × 20%
- Remaining balance = total amount − deposit
- Payment method is stored with the booking
- Booking is created only after the user confirms the deposit
- Existing `hotel.db` files are automatically migrated with the new payment columns
