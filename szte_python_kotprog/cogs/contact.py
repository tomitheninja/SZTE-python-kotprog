"""Cog for keeping contact between buyers and sellers"""

# import logging
import discord
from discord.ext import commands

from szte_python_kotprog.models.product import Product
from szte_python_kotprog.ui.contact import ContactSellerView
from szte_python_kotprog.ui.search import SearchHitEmbed


class ContactCog(commands.Cog):
    """Contact cog"""

    bot: commands.Bot

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        """Handle messages"""
        # logging.info("Message received: %s", msg.content)

    async def prompt_contact(self, requestor: discord.User, product: Product):
        """Prompt the user to contact the seller"""
        await requestor.send(
            "Biztosan fel akarod venni a kapcsolatot a következő eladóval?",
            embed=SearchHitEmbed(product),
            view=ContactSellerView(self.bot, product),
        )
