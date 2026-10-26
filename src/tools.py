import json
from datetime import datetime
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data"
FIXED_NOW = datetime.fromisoformat("2026-06-10T09:00:00+02:00")


def get_booking(booking_id: str) -> dict:

    with open(DATA_PATH / "bookings.json") as json_data:
        data = json.load(json_data)

        for item in data:
            if item.get("id") == booking_id:
                return item
        
    return {"error": "Booking not found", "booking_id": booking_id}

def calculate_refund(booking_id: str, now: datetime = FIXED_NOW) -> dict:
    booking = get_booking(booking_id)
    
    if not booking.get("id"):
        return booking
    
    if booking.get("status") != "confirmed":
        return {"total_refund_eur": 0.0, "reason": "Booking cannot be cancelled"}

    start = datetime.fromisoformat(booking["start"])
    hours = (start - now).total_seconds() / 3600
    
    if hours >= 48:
        refund_rate = 1.0
    elif hours >= 24:
        refund_rate = 0.5
    else:
        refund_rate = 0.0
    
    rental_refund = booking["rental_price_eur"] * refund_rate
    total_refund = rental_refund + booking["deposit_eur"]
    
    return {
    "booking_id": booking_id,
    "hours_before_start": hours,
    "refund_rate": refund_rate,
    "rental_refund_eur": rental_refund,
    "deposit_refund_eur": booking["deposit_eur"],
    "total_refund_eur": total_refund,
    "paid_with": booking["paid_with"],
    }

