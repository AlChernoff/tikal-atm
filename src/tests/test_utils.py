import pytest

from app.exceptions import TooMuchCoinsException, NotEnoughInventoryException
from app.utils import process_withdrawl

from app.utils import is_valid_withdrawl


@pytest.mark.anyio
async def test_withdraw_cash():
    inventory_list = [
        {
            "type": "BILL",
            "value": 200,
            "amount": 1
        }
    ]
    result = await process_withdrawl(200, inventory_list)
    expected_result = ({200: 0}, {'bills': {200: 1}, 'coins': {}})

    assert result == expected_result


@pytest.mark.anyio
async def test_withdraw_cash_with_coins():
    inventory_list = [
        {
            "type": "BILL",
            "value": 200,
            "amount": 1
        },
        {
            "type": "COIN",
            "value": 1,
            "amount": 1
        }
    ]
    result = await process_withdrawl(201, inventory_list)
    expected_result = ({200: 0, 1: 0}, {'bills': {200: 1}, 'coins': {1: 1}})

    assert result == expected_result


@pytest.mark.anyio
async def test_withdraw_cash_with_coins_too_much():
    inventory_list = [
        {
            "type": "COIN",
            "value": 1,
            "amount": 51
        }
    ]
    with pytest.raises(TooMuchCoinsException):
        await process_withdrawl(51, inventory_list)


@pytest.mark.anyio
async def test_withdraw_not_enough_amount():
    inventory_list = [
        {
            "type": "COIN",
            "value": 1,
            "amount": 1
        }
    ]
    with pytest.raises(NotEnoughInventoryException):
        await process_withdrawl(200, inventory_list)


def test_is_valid_withdrawl__int():
    assert is_valid_withdrawl(1)


def test_is_valid_withdrawl__rational_1():
    assert is_valid_withdrawl(1.1)


def test_is_valid_withdrawl__rational_2():
    assert is_valid_withdrawl(1.12)


def test_is_valid_withdrawl__rational_3():
    assert is_valid_withdrawl(1.124) is False
