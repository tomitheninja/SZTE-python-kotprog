"""Adattárolás"""

from discord.ext import commands

from szte_python_kotprog.models.county import County
from szte_python_kotprog.models.profile import Profile
from szte_python_kotprog.models.seller import Seller

class DataStoreCog(commands.Cog):
    """Adattárolást kivitelező fogaskerék"""
    def __init__(self, bot):
        self.bot = bot
        self.profiles = {}
        self.products = []
        
    def save_seller_profile(self, discordId: int, alias: str, counties: list[County]):
        if self.profiles.get(discordId) is None:
            self.profiles[discordId] = Profile(discordId, None, Seller(alias, counties))
        else:
            self.profiles[discordId].seller.alias = alias
            self.profiles[discordId].seller.counties = counties
        
    
