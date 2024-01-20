from fastapi import status, HTTPException


class InvalidAmountException(HTTPException):
    """Exception raised for errors if the Amount of available inventory is less than withdrawal amount

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, detail: str, status_code: status = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=detail)


class MaximumAmountException(HTTPException):
    """Exception raised for errors if the Amount of single withdrawal is more  than 2000

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, detail: str, status_code: status = status.HTTP_422_UNPROCESSABLE_ENTITY):
        super().__init__(status_code=status_code, detail=detail)


class NotEnoughInventoryException(HTTPException):
    """Exception raised for errors if the Amount of available inventory is less than withdrawal amount

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, detail, status_code: status = status.HTTP_409_CONFLICT):
        super().__init__(status_code=status_code, detail=detail)


class TooMuchCoinsException(HTTPException):
    """Exception raised for errors if the Amount of coins is more  than 50 or equal

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, detail: str, status_code: status = status.HTTP_422_UNPROCESSABLE_ENTITY):
        super().__init__(status_code=status_code, detail=detail)


class UnknownInventoryException(HTTPException):
    """Exception raised for errors if any of inventory types in refill payload are not supported

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, detail: str, status_code: status = status.HTTP_422_UNPROCESSABLE_ENTITY):
        super().__init__(status_code=status_code, detail=detail)
