"""Felhasználói kombinált profil modell"""
from szte_python_kotprog.models.buyer import Buyer
from szte_python_kotprog.models.seller import Seller


class Profile:
    """Felhasználói kombinált profil modell"""
    buyer: Buyer
    seller: Seller
    discordId: int

    def __init__(self, discordId: int, buyer: Buyer, seller: Seller) -> None:
        self.discordId = discordId
        self.buyer = buyer
        self.seller = seller

    def __str__(self) -> str:
        return f"{self.buyer}-{self.seller}"
    
    def __repr__(self) -> str:
        return self.__str__()
    