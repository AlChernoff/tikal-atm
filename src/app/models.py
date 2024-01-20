from enum import Enum
from typing import Dict, List
from pydantic import BaseModel

from .db import database


class WithdrawalRequestModel(BaseModel):
    amount: float


class RefillRequestModel(BaseModel):
    money: dict


class InventoryTypes(Enum):
    BILL = 'BILL'
    COIN = 'COIN'


class Inventory(BaseModel):
    __table__ = "inventory"
    type: InventoryTypes
    value: float
    amount: int

    @classmethod
    async def get_inventory(cls) -> List[Dict]:
        """
        Method to fetch inventory from  db
        :rtype: dict

        """
        query = "SELECT type,value,amount  FROM inventory WHERE amount >0"
        result = await database.fetch_all(query=query)
        result_dict = [dict(u) for u in result]
        return result_dict

    @classmethod
    async def update_inventory(cls, money: Dict) -> None:
        """
        Method to update inventory amounts in db
        :param money: Values to be updated
        """
        transaction = await database.transaction()
        try:
            for entry in money:
                query = f"UPDATE inventory set amount={money[entry]} where value={entry};"
                await database.execute(query)
        except:
            await transaction.rollback()
        else:
            await transaction.commit()
