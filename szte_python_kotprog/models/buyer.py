"""Buyer model"""

from szte_python_kotprog.models.product import Product
from szte_python_kotprog.models.base_user import BaseUser


class Buyer(BaseUser):
    """Buyer model"""

    cart: list[Product]
        