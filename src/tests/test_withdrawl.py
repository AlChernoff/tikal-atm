import pytest

from app.exceptions import TooMuchCoinsException, NotEnoughInventoryException
from app.utils import process_withdrawl


def test_empty_input(test_app):
    response = test_app.post(
        url="/atm/withdrawal",
        headers={"Content-Type": "application/json"},
        json={},
    )
    assert response.status_code == 422


def test_not_valid_input(test_app):
    response = test_app.post(
        url="/atm/withdrawal",
        headers={"Content-Type": "application/json"},
        json={"amount": "abc"},
    )
    assert response.status_code == 422


def test_not_valid_input_3_digits_after_dot(test_app):
    response = test_app.post(
        url="/atm/withdrawal",
        headers={"Content-Type": "application/json"},
        json={"amount": 2.2222},
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Withdrawal amount should be greater than 0 and max 2 digits after .'}


def test_negative_amount(test_app):
    response = test_app.post(
        url="/atm/withdrawal",
        headers={"Content-Type": "application/json"},
        json={"amount": -10},
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Withdrawal amount should be greater than 0 and max 2 digits after .'}


def test_zero_amount(test_app):
    response = test_app.post(
        url="/atm/withdrawal",
        headers={"Content-Type": "application/json"},
        json={"amount": 0},
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Withdrawal amount should be greater than 0 and max 2 digits after .'}


def test_not_valid__exceeds_limit_amount(test_app):
    response = test_app.post(
        url="/atm/withdrawal",
        headers={"Content-Type": "application/json"},
        json={"amount": 2001},
    )
    assert response.status_code == 422
