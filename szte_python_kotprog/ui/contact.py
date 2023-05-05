"""UI elements for the contacting sellers"""

import discord
from discord import ui
from discord.ext.commands import Bot

from szte_python_kotprog.models.product import Product


class ContactSellerView(ui.View):
    """Button definition for confirming contact with seller"""

    bot: Bot
    product: Product

    confirm_btn: ui.Button
    cancel_btn: ui.Button

    def __init__(self, bot: Bot, product: Product):
        super().__init__()
        self.bot = bot
        self.product = product

        self.confirm_btn = ui.Button(label="Igen", style=discord.ButtonStyle.primary)
        self.cancel_btn = ui.Button(label="Mégse", style=discord.ButtonStyle.secondary)

        self.confirm_btn.callback = self.confirm_btn_callback
        self.cancel_btn.callback = self.cancel_btn_callback

        self.add_item(self.confirm_btn)
        self.add_item(self.cancel_btn)

    async def confirm_btn_callback(self, interaction: discord.Interaction):
        """Confirm contact with seller"""
        await interaction.response.send_message("Kapcsolatfelvétel megerősítve!")

    async def cancel_btn_callback(self, interaction: discord.Interaction):
        """Cancel contact with seller"""
        await interaction.response.send_message("Kapcsolatfelvétel megszakítva!")
