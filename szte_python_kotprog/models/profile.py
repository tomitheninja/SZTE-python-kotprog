"""Combined profile model"""
from szte_python_kotprog.models.buyer import Buyer
from szte_python_kotprog.models.seller import Seller


class Profile:
    """Combined profile model"""

    buyer: Buyer
    seller: Seller
    discord_id: int

    def __init__(self, discord_id: int, buyer: Buyer, seller: Seller) -> None:
        self.discord_id = discord_id
        self.buyer = buyer
        self.seller = seller

    def __str__(self) -> str:
        return f"{self.buyer}-{self.seller}"

    def __repr__(self) -> str:
        return self.__str__()
