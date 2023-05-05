"""Data storage"""

# import logging
import pickle

from discord.ext import commands
from fuzzywuzzy import process

from szte_python_kotprog.models.county import County
from szte_python_kotprog.models.product import Product
from szte_python_kotprog.models.profile import Profile
from szte_python_kotprog.models.seller import Seller
from szte_python_kotprog.models.buyer import Buyer


class DataStore:
    """Class for data storage"""
    def __init__(self):
        self.profiles: dict[int, Profile] = {}
        self.products: list[Product] = []

    def __str__(self) -> str:
        return f"DataStore(profiles={self.profiles}, products={self.products})"

    def __repr__(self) -> str:
        return self.__str__()


class DataStoreCog(commands.Cog):
    """Data storage cog"""

    def __init__(self, bot, config, data=None):
        self.data: DataStore = data if data is not None else DataStore()
        self.bot: commands.Bot = bot
        self.config: dict = config

    @property
    def products(self):
        """Product list getter"""
        return self.data.products

    @property
    def profiles(self):
        """Profile list getter"""
        return self.data.profiles

    def save_to_file(self):
        """Save data to disk as pickle"""
        with open(self.config.get("pickle", "data.pickle"), "wb") as file:
            pickle.dump(self.bot.get_cog("DataStoreCog").data, file)

    def save_seller_profile(self, discord_id: int, alias: str, counties: list[County]):
        """Save seller profile to data store"""
        if self.profiles.get(discord_id) is None:
            self.profiles[discord_id] = Profile(
                discord_id, None, Seller(alias, counties)
            )
        elif self.profiles[discord_id].seller is None:
            self.profiles[discord_id].seller = Seller(alias, counties)
        else:
            self.profiles[discord_id].seller.alias = alias
            self.profiles[discord_id].seller.counties = counties

        self.save_to_file()

    def save_buyer_profile(self, discord_id: int, alias: str):
        """Save buyer profile to data store"""
        if self.profiles.get(discord_id) is None:
            self.profiles[discord_id] = Profile(discord_id, Buyer(alias), None)
        elif self.profiles[discord_id].buyer is None:
            self.profiles[discord_id].buyer = Buyer(alias)
        else:
            self.profiles[discord_id].buyer.alias = alias

        self.save_to_file()

    def save_product(
        self,
        seller_discord_id: int,
        name: str,
        description: str,
        price: int,
        quantity: int,
    ):
        """Save product to data store"""
        if self.profiles.get(seller_discord_id) is None:
            return
        seller = self.profiles[seller_discord_id].seller
        if seller is None:
            return
        for product in seller.products:
            if product.name == name:
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
        """Delete products from data store"""
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

    def get_populated_counties(self):
        """Get counties that have active sellers"""
        populated_counties = set()
        for profile in self.profiles.values():
            if profile.seller is not None:
                for county in profile.seller.counties:
                    populated_counties.add(county)
        return list(populated_counties)

    def save_county_preferences(self, discord_id: int, counties: list[County]):
        """Save county preferences to data store"""
        profile = self.profiles.get(discord_id)
        if profile is None:
            return
        buyer = profile.buyer
        if buyer is None:
            return
        buyer.counties = counties
        self.save_to_file()

    def search_product(self, counties: list[County] = None, name: str = None):
        """Search for products in counties"""
        if counties is None or len(counties) == 0:
            counties = self.get_populated_counties()

        possible_products = list(self.products)
        for product in possible_products:
            if product.quantity == 0:
                possible_products.remove(product)
                continue
            found = False
            for county in product.seller.counties:
                if county in counties:
                    found = True
                    break
            if not found:
                possible_products.remove(product)

        possible_names = [x.name for x in possible_products]
        filtered_names = possible_names
        if name is not None:
            matches = process.extract(name, possible_names, limit=5)
            filtered_names = [x[0] for x in matches]
        result = []
        for p_name in filtered_names:
            for product in possible_products:
                if product.name == p_name:
                    result.append(product)

        return result
