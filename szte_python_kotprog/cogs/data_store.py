"""Adattárolás"""

import logging
import pickle

from discord.ext import commands

from szte_python_kotprog.models.county import County
from szte_python_kotprog.models.product import Product
from szte_python_kotprog.models.profile import Profile
from szte_python_kotprog.models.seller import Seller
from szte_python_kotprog.models.buyer import Buyer

class DataStore:
    def __init__(self):
        self.profiles: dict[int, Profile] = {}
        self.products: list[Product] = []
        
    def __str__(self) -> str:
        return f"DataStore(profiles={self.profiles}, products={self.products})"
        
    def __repr__(self) -> str:
        return self.__str__()

class DataStoreCog(commands.Cog):
    """Adattárolást kivitelező fogaskerék"""
    def __init__(self, bot, config, data = None):
        self.data: DataStore = data if data != None else DataStore()
        self.bot: commands.Bot = bot
        self.config: dict = config
        
    @property
    def products(self):
        return self.data.products
    
    @property
    def profiles(self):
        return self.data.profiles

    def save_to_file(self):
        """Adatok mentése fájlba"""
        with open(self.config.get("pickle", "data.pickle"), "wb") as f:
            pickle.dump(self.bot.get_cog("DataStoreCog").data, f)

    def save_seller_profile(self, discord_id: int, alias: str, counties: list[County]):
        if self.profiles.get(discord_id) is None:
            self.profiles[discord_id] = Profile(discord_id, None, Seller(alias, counties))
        elif self.profiles[discord_id].seller is None:
            self.profiles[discord_id].seller = Seller(alias, counties)
        else:
            self.profiles[discord_id].seller.alias = alias
            self.profiles[discord_id].seller.counties = counties

        self.save_to_file()
        
    def save_buyer_profile(self, discord_id: int, alias: str):
        if self.profiles.get(discord_id) is None:
            self.profiles[discord_id] = Profile(discord_id, Buyer(alias), None)
        elif self.profiles[discord_id].buyer is None:
            self.profiles[discord_id].buyer = Buyer(alias)
        else:
            self.profiles[discord_id].buyer.alias = alias

        self.save_to_file()
        
    def save_product(self, seller_discord_id: int, name: str, description: str, price: int, quantity: int):
        if self.profiles.get(seller_discord_id) is None:
            return
        seller = self.profiles[seller_discord_id].seller
        if seller is None:
            return
        for product in seller.products:
            if (product.name == name):
                product.description = description
                product.price = price
                product.quantity = quantity
                self.save_to_file()
                return
        
        product = Product(seller, name, description, price, quantity)
        self.products.append(product)
        seller.products.append(product)
        self.save_to_file()
    
    def delete_products(self, discord_id: int, names: list[str]):
        profile = self.profiles.get(discord_id)
        if profile is None:
            return
        seller = profile.seller
        if seller is None:
            return
        for name in names:
            for product in self.products:
                if product.name == name and product.seller == seller:
                    self.products.remove(product)
                    seller.products.remove(product)
                    self.save_to_file()
                    break

