"""Buyer model"""

from szte_python_kotprog.models.product import Product
from szte_python_kotprog.models.base_user import BaseUser


class Buyer(BaseUser):
    """Buyer model"""

    def __str__(self) -> str:
        return f"Buyer:{self.alias}"
    
    def __repr__(self) -> str:
        return self.__str__()
        