"""Seller model"""

from szte_python_kotprog.models.county import County
from .product import Product
from .base_user import BaseUser


class Seller(BaseUser):
    """Seller model"""
    products: list[Product] = []

    def __str__(self) -> str:
        return f"{self.alias} - {self.counties} - {self.products}"
        