"""
TP RATTRAPAGE ANDREAS FIVEL
"""

import uuid
from bookings_db import bookings_db

def get_all_bookings(offset, limit):
    return list(bookings_db.values())[offset:offset + limit]

def get_booking(booking_id):
    return bookings_db.get(booking_id)

def create_booking(data):
    booking_id = str(uuid.uuid4())
    new_booking = {"booking_id": booking_id, **data}
    bookings_db[booking_id] = new_booking
    return new_booking

def update_booking(booking_id, data):
    if booking_id in bookings_db:
        bookings_db[booking_id] = {"booking_id": booking_id, **data}
        return bookings_db[booking_id]
    return None

def delete_booking(booking_id):
    return bookings_db.pop(booking_id, None) is not None

def get_room_type_statistics():
    stats = {"SINGLE": 0, "DELUXE": 0, "SUITE": 0}
    for booking in bookings_db.values():
        if not booking["is_cancelled"]:
            stats[booking["room_type"]] += 1
    return stats
