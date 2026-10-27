import json
import re
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from .helpers import tokenize, calculate_relevance

DATA_PATH = Path(__file__).resolve().parent.parent / "data"
POLICIES_PATH = DATA_PATH / "policies"
FIXED_NOW = datetime.fromisoformat("2026-06-10T09:00:00+02:00")

def get_booking(booking_id: str) -> dict:

    with open(DATA_PATH / "bookings.json","r", encoding="utf-8") as json_data:
        data = json.load(json_data)

        for item in data:
            if item.get("id") == booking_id:
                return item
        
    return {"error": "Booking not found", "booking_id": booking_id}

def calculate_refund(
    booking_id: str,
    now: datetime = FIXED_NOW
) -> dict:

    booking = get_booking(booking_id)

    if "error" in booking:
        return booking

    if booking.get("status") != "confirmed":
        return {
            "booking_id": booking_id,
            "total_refund_eur": 0.0,
            "reason": "Booking cannot be cancelled"
        }

    start = datetime.fromisoformat(booking["start"])

    hours = (start - now).total_seconds() / 3600

    if hours >= 48:
        refund_rate = Decimal("1")
    elif hours >= 24:
        refund_rate = Decimal("0.5")
    else:
        refund_rate = Decimal("0")

    rental_price = Decimal(str(booking["rental_price_eur"]))
    deposit = Decimal(str(booking["deposit_eur"]))

    rental_refund = rental_price * refund_rate
    total_refund = rental_refund + deposit

    return {
        "booking_id": booking_id,
        "hours_before_start": hours,
        "refund_rate": float(refund_rate),
        "rental_refund_eur": float(rental_refund),
        "deposit_refund_eur": float(deposit),
        "total_refund_eur": float(total_refund),
        "paid_with": booking["paid_with"],
        "booking_fee_refund_eur": 0.0
    }

def search_policies(query: str, limit: int = 3) -> list[dict]:
    results = []
    query_words = tokenize(query)

    if not query_words or limit <= 0:
        return []

    for file in sorted(POLICIES_PATH.glob("*.md")):
        content = file.read_text(encoding="utf-8")

        sections = re.split(r"(?m)^##\s+", content)

        for section in sections:
            section = section.strip()

            if not section:
                continue

            lines = section.splitlines()
            heading = lines[0]

            score = calculate_relevance(
                query_words=query_words,
                section=section,
                heading=heading
            )
            if score > 0:
                results.append({
                    "source": file.name,
                    "heading": heading,
                    "content": section,
                    "score": score
                })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:limit]

if __name__ == "__main__":

    print("BOOKING:")
    print(get_booking("CW-1001"))

    print("\nREFUND:")
    print(calculate_refund("CW-1002"))

    print("\nPOLICY SEARCH:")
    for result in search_policies(
        "What is the deposit for an electric bike?"
    ):
        print(result)