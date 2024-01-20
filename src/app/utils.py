from collections import defaultdict
from copy import deepcopy
from fastapi import HTTPException, status
from typing import List, Dict, Iterable, Optional, Tuple

from .db import database, inventory
from .exceptions import TooMuchCoinsException, NotEnoughInventoryException
from .models import Inventory


async def insert_from_json(data: Dict[str, List[Dict]]) -> None:
    """
    Populate DB tables from data object with relevant data.
    :param data: Raw data to populate DB with, where key is the table name, values are future rows in the table.
    """
    for table_name in data.keys():
        table_data: List[Dict] = data[table_name]
        columns: Iterable[str] = list(table_data[0].keys())
        values: List[str] = []

        for row_entry in table_data:
            row_values: List[str] = []

            for column in columns:
                value: Optional[str] = row_entry.get(column)

                if value is not None:
                    row_values.append(f"'{value}'")
                else:
                    row_values.append('NULL')

            values.append(','.join(row_values))

        quoted_columns: List[str] = [f'"{column}"' for column in columns]
        query: str = f"INSERT INTO {table_name} ({', '.join(quoted_columns)}) " \
            f"VALUES {','.join([f'({value})' for value in values])}"
        await database.execute(query)


async def clean_db(data: Dict[str, List[Dict]]) -> None:
    """ Cleans DB data. """
    for table_name in data.keys():
        query = f"TRUNCATE {table_name};"
        await database.execute(query)


async def withdraw_cash(amount: float, available_inventory: List[Dict]) -> Dict:
    """
    Method to process inventory that needed to make withdrawal

    :param amount: withdrawal amount of the single transaction
    :param available_inventory: inventory from db
    """
    changed_inventory, result = await process_withdrawl(amount, available_inventory)
    try:
        await Inventory.update_inventory(changed_inventory)
    except:
        raise HTTPException(detail="Please try again later. ATM is on maintenance",
                            status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    else:
        return result


async def process_withdrawl(amount: float, available_inventory: List[dict]) -> Tuple[Dict, Dict]:
    """
    Method to calculate inventory that needed to make withdrawal

    :param amount: withdrawal amount of the single transaction
    :param available_inventory: inventory from db
    """
    initial_inventory: List[dict] = deepcopy(available_inventory)
    # Initialize variables to track the bills and coins for the withdrawal
    result: Dict[str, Dict] = {"bills": defaultdict(int), "coins": defaultdict(int)}
    changed_inventory: Dict[str, int] = {}
    # Iterate through the available bill denominations
    bills: List[dict] = [d for d in available_inventory if d['type'] == 'BILL']
    bills.sort(key=lambda x: x['value'], reverse=True)

    for bill in bills:
        while True:
            if amount - bill['value'] >= 0 and bill['amount'] > 0:
                amount -= bill['value']
                bill['amount'] -= 1
                changed_inventory[bill['value']] = bill['amount']
                result['bills'][bill['value']] += 1
            else:
                break

    if amount:
        # Iterate through the available coin denominations
        coins: List[dict] = [d for d in available_inventory if d['type'] == 'COIN']
        coins.sort(key=lambda x: x['value'], reverse=True)

        for coin in coins:
            while True:
                if not coin['amount']:
                    break
                decreased_amount: float = round((amount - coin['value']), 2)
                if decreased_amount >= 0:
                    amount = decreased_amount
                    coin['amount'] -= 1
                    changed_inventory[coin['value']] = coin['amount']
                    result['coins'][coin['value']] += 1
                    if result['coins'][coin['value']] == 50:
                        raise TooMuchCoinsException("Sorry, amount of coins is more or equal 50")
                else:
                    break

    if amount:
        raise NotEnoughInventoryException(f"Not enough inventory available, available list is {initial_inventory}")

    return changed_inventory, result


def is_valid_withdrawl(number: float) -> bool:
    """
    Checks if the withdrawl amount is valid or not. System has a limit of 2 digits after decimal.

    :param number: Input withdrawl number.
    :return: Boolean value. True is valid, else False.
    """
    return str(number)[::-1].find('.') <= 2
