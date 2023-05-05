"""Product model."""

from szte_python_kotprog.models.base_user import BaseUser


class Product:
    """A product in the store."""

    seller: BaseUser
    name: str
    description: str
    price: int
    quantity: int

    def __init__(
        self, seller: BaseUser, name: str, description: str, price: int, quantity: int
    ) -> None:
        self.seller: BaseUser = seller
        self.name: str = name
        self.description: str = description
        self.price: int = price
        self.quantity: int = quantity

    def __str__(self) -> str:
        return f"{self.name} - {self.price} Ft ({self.quantity}x)"

    def __repr__(self) -> str:
        return self.__str__()
