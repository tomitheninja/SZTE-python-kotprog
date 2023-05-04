"""Seller model"""

from szte_python_kotprog.models.county import County
from .product import Product
from .base_user import BaseUser


class Seller(BaseUser):
    """Seller model"""
    products: list[Product]
    counties: list[County]
    
    def __init__(self, alias: str, counties: list[County]):
        super().__init__(alias)
        self.products = []
        self.counties = counties if counties is not None else []

    def __str__(self) -> str:
        return f"{self.alias} => {self.counties}{self.products}"
    
    def __repr__(self) -> str:
        return self.__str__()
        