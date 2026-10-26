
from src.tools import (
    get_booking,
    calculate_refund,
    search_policies,
)

from src.helpers import (
    tokenize,
)


def test_existing_booking():
    booking = get_booking("CW-1001")
    assert booking["id"] == "CW-1001"


def test_missing_booking():
    booking = get_booking("CW-9999")
    assert booking["error"] == "Booking not found"


def test_full_refund():
    result = calculate_refund("CW-1001")
    assert result["total_refund_eur"] == 90.0


def test_half_refund():
    result = calculate_refund("CW-1002")
    assert result["total_refund_eur"] == 340.0


def test_deposit_only():
    result = calculate_refund("CW-1003")
    assert result["total_refund_eur"] == 50.0


def test_already_cancelled():
    result = calculate_refund("CW-1005")
    assert result["total_refund_eur"] == 0.0


def test_refund_48_hours():
    result = calculate_refund("CW-1007")
    assert result["total_refund_eur"] == 186.0


def test_refund_24_hours():
    result = calculate_refund("CW-1010")
    assert result["total_refund_eur"] == 170.0


def test_tokenize():
    result = tokenize("How much is the deposit for an e-bike?")
    assert {"deposit", "electric", "bike"} <= result


def test_policy_search():
    results = search_policies("What is the deposit?")
    assert any(
        result["heading"] == "Deposit"
        for result in results
    )
