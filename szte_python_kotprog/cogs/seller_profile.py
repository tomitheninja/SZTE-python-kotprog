"""Eladói profil modul"""

from discord.ext import commands
from discord import app_commands
import discord
from szte_python_kotprog.cogs.data_store import DataStoreCog
from szte_python_kotprog.models.county import County
from szte_python_kotprog.ui.modal import Questionnaire
from szte_python_kotprog.ui.profile import ProfileViewEditBtn
from szte_python_kotprog.ui.seller_profile import SellerProfileEmbed, SellerProfileView


class SellerProfileCog(commands.Cog):
    """Fogaskerék az eladói profilhoz"""

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="eladói-profil")
    async def seller_profile(self, ctx: commands.Context):
        """Eladói profil"""
        data_store: DataStoreCog = self.bot.get_cog("DataStoreCog")
        if data_store is not None:
            profile = data_store.profiles.get(ctx.author.id)
            if profile is not None:
                seller = profile.seller
                await ctx.send(view=SellerProfileView(True, self.edit_profile), embed=SellerProfileEmbed(True, seller.alias, seller.counties, seller.products), ephemeral=True)
            else:
                await ctx.send(view=SellerProfileView(False, self.edit_profile), embed=SellerProfileEmbed(), ephemeral=True)
                
    async def seller_profile_interaction(self, interaction: discord.Interaction):
        data_store: DataStoreCog = self.bot.get_cog("DataStoreCog")
        if data_store is not None:
            profile = data_store.profiles.get(interaction.user.id)
            if profile is not None:
                seller = profile.seller
                await interaction.response.send_message(view=SellerProfileView(True, self.edit_profile), embed=SellerProfileEmbed(True, seller.alias, seller.counties, seller.products), ephemeral=True)
            else:
                await interaction.response.send_message(view=SellerProfileView(False, self.edit_profile), embed=SellerProfileEmbed(), ephemeral=True)
                
    async def edit_profile(self, interaction: discord.Interaction, name: str, counties: list[County]):
        data_store: DataStoreCog = self.bot.get_cog("DataStoreCog")
        if data_store is None:
            return
        print("Saving profile...", name, counties)
        data_store.save_seller_profile(interaction.user.id, name, counties)
        print(data_store.__dict__)
        await self.seller_profile_interaction(interaction)
        
        