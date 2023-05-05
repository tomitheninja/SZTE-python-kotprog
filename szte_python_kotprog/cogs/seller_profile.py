"""Seller profile cog"""

from discord.ext import commands
import discord
from szte_python_kotprog.cogs.data_store import DataStoreCog
from szte_python_kotprog.models.county import County
from szte_python_kotprog.ui.product import ProductManageEmbed, ProductManageView
from szte_python_kotprog.ui.seller_profile import SellerProfileEmbed, SellerProfileView


class SellerProfileCog(commands.Cog):
    """Seller profile cog"""

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.hybrid_command(name="eladói-profil")
    async def profile(self, ctx: commands.Context):
        """Render seller profile from command"""
        await self._profile(ctx.author.id, ctx.send)

    async def profile_interaction(self, interaction: discord.Interaction):
        """Render seller profile from interaction"""
        await self._profile(interaction.user.id, interaction.response.send_message)

    async def _profile(self, user_id: int, send: callable):
        """Render seller profile"""
        data_store: DataStoreCog = self.bot.get_cog("DataStoreCog")
        if data_store is not None:
            profile = data_store.profiles.get(user_id)
            seller = profile.seller if profile is not None else None
            if seller is not None:
                await send(
                    view=SellerProfileView(
                        self.bot, True, seller.alias, seller.counties, seller.products
                    ),
                    embed=SellerProfileEmbed(
                        True, seller.alias, seller.counties, seller.products
                    ),
                    ephemeral=True,
                )
            else:
                await send(
                    view=SellerProfileView(self.bot, False),
                    embed=SellerProfileEmbed(),
                    ephemeral=True,
                )

    async def edit_profile(
        self, interaction: discord.Interaction, name: str, counties: list[County]
    ):
        """Edit seller profile"""
        data_store: DataStoreCog = self.bot.get_cog("DataStoreCog")
        if data_store is None:
            return
        data_store.save_seller_profile(interaction.user.id, name, counties)
        await self.profile_interaction(interaction)

    async def edit_product(
        self,
        interaction: discord.Interaction,
        name: str,
        description: str,
        price: int,
        quantity: int,
    ):
        """Edit product (forward to data store and reply)"""
        data_store: DataStoreCog = self.bot.get_cog("DataStoreCog")
        if data_store is None:
            return
        data_store.save_product(interaction.user.id, name, description, price, quantity)
        profile = data_store.profiles.get(interaction.user.id)
        if profile is None:
            return
        seller = profile.seller
        if seller is None:
            return
        await interaction.response.send_message(
            embed=ProductManageEmbed(seller.products),
            view=ProductManageView(self.bot, seller.products),
            ephemeral=True,
        )

    async def delete_products(self, interaction: discord.Interaction, names: list[str]):
        """Delete products (forward to data store and reply)"""
        data_store: DataStoreCog = self.bot.get_cog("DataStoreCog")
        if data_store is None:
            return
        data_store.delete_products(interaction.user.id, names)
        profile = data_store.profiles.get(interaction.user.id)
        if profile is None:
            return
        seller = profile.seller
        if seller is None:
            return
        await interaction.response.send_message(
            embed=ProductManageEmbed(seller.products),
            view=ProductManageView(self.bot, seller.products),
            ephemeral=True,
        )
