import pytest

from src.tools import (
    get_booking,
    calculate_refund,
    search_policies,
)

from src.helpers import (
    tokenize,
)

@pytest.mark.parametrize("booking_id,expected", [
    ("CW-1001", 90.0),
    ("CW-1002", 340.0),
    ("CW-1003", 50.0),
    ("CW-1004", 73.0),
    ("CW-1005", 0.0),
    ("CW-1006", 0.0),
    ("CW-1007", 186.0),
    ("CW-1008", 0.0),
    ("CW-1009", 169.0),
    ("CW-1010", 170.0),
])
def test_refunds(booking_id, expected):
    result = calculate_refund(booking_id)
    assert result["total_refund_eur"] == expected


def test_existing_booking():
    booking = get_booking("CW-1001")
    assert booking["id"] == "CW-1001"


def test_missing_booking():
    booking = get_booking("CW-9999")
    assert booking["error"] == "Booking not found"

def test_tokenize():
    result = tokenize("How much is the deposit for an e-bike?")
    assert {"deposit", "electric", "bike"} <= result


def test_policy_search():
    results = search_policies("What is the deposit?")
    assert any(
        result["heading"] == "Deposit"
        for result in results
    )
