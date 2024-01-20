from fastapi import FastAPI, HTTPException, status
from typing import List, Dict

from .consts import MAXIMUM_SINGLE_TRANSACTION_AMOUNT, SUPPORTED_INVENTORY_VALUES
from .data import data
from .db import database, metadata, engine
from .exceptions import InvalidAmountException, MaximumAmountException, UnknownInventoryException

from .models import WithdrawalRequestModel, RefillRequestModel, Inventory
from .utils import insert_from_json, withdraw_cash, clean_db, is_valid_withdrawl

metadata.create_all(engine)
app = FastAPI()


@app.on_event("startup")
async def startup():
    """ Is called on server startup event. Inits DB connection, creates tables and seeds db with initial data. """
    await database.connect()
    await clean_db(data)
    await insert_from_json(data)


@app.on_event("shutdown")
async def shutdown():
    """ On shutdown closes db connection. """
    await database.disconnect()


@app.post("/atm/withdrawal")
async def process_withdrawal(request: WithdrawalRequestModel) -> Dict:
    """
    POST API endpoint which is called to withdraw cash from ATM.
    Has validation that amount is greater than zero and is float, also that amount is less or equal 2000
    and that it not more than 2 numbers after .

    request example: {"amount": 200}
    response example: {"bills": {"100.0": 2},"coins": {}}
    :param request: WithdrawalRequestModel it has float parameter amount - amount for single withdrawal transaction
    """
    if request.amount <= 0:
        raise InvalidAmountException(
            detail="Withdrawal amount should be greater than 0 and max 2 digits after .")

    if not is_valid_withdrawl(request.amount):
        raise InvalidAmountException(
            detail="Withdrawal amount should be greater than 0 and max 2 digits after .")

    if request.amount > MAXIMUM_SINGLE_TRANSACTION_AMOUNT:
        raise MaximumAmountException(
            "Sorry, maximum value for single withdrawal should be less than or equal to  2000")

    available_inventory: List[Dict] = await Inventory.get_inventory()
    return await withdraw_cash(request.amount, available_inventory)


@app.get("/atm/inventory")
async def get_available_inventory() -> List[Dict]:
    """
    GET API endpoint which is called to check available inventory  in ATM.
    response example: [{"type": "BILL","value": 200,"amount": 1}]
    """
    return await Inventory.get_inventory()


@app.post("/atm/refill")
async def refill_inventory(request: RefillRequestModel) -> List[Dict]:
    """
    POST API endpoint which is called to refill inventory in  ATM.
    Has validation that provided inventory types are supported.
    request example: {"money":{"0.1": 5,"5": 20,"20": 15,"100": 30}}
    response example: "New inventory is: [{'type': 'COIN', 'value': 10.0, 'amount': 10}]

    :param request: RefillRequestModel it has dict parameter money - inventory types which should be refilled
    :return: Message with an updated inventory.
    """
    inventory_types: List[str] = list(request.money.keys())
    if list(set(inventory_types).difference(SUPPORTED_INVENTORY_VALUES)):
        raise UnknownInventoryException(
            detail=f"One of bills/coins is not supported. Supported values are: {SUPPORTED_INVENTORY_VALUES}")
    else:
        try:
            await Inventory.update_inventory(request.money)
            return f"New inventory is: {await Inventory.get_inventory()}"
        except:
            raise HTTPException(detail="Please try again later. ATM is on maintenance",
                                status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
