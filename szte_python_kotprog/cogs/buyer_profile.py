"""Buyer profile cog"""

from discord.ext import commands
import discord
from szte_python_kotprog.cogs.data_store import DataStoreCog
from szte_python_kotprog.ui.buyer_profile import BuyerProfileEmbed, BuyerProfileView


class BuyerProfileCog(commands.Cog):
    """Buyer profile cog"""

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.hybrid_command(name="profil", brief="Vásárlói profil")
    async def profile(self, ctx: commands.Context):
        """Render buyer profile from command"""
        await self._profile(ctx.author.id, ctx.send)

    async def profile_interaction(self, interaction: discord.Interaction):
        """Render buyer profile from interaction"""
        await self._profile(interaction.user.id, interaction.response.send_message)

    async def _profile(self, user_id: int, send: callable):
        """Render buyer profile"""
        data_store: DataStoreCog = self.bot.get_cog("DataStoreCog")
        if data_store is not None:
            profile = data_store.profiles.get(user_id)
            buyer = profile.buyer if profile is not None else None
            await send(
                view=BuyerProfileView(buyer is not None, self.edit_profile),
                embed=BuyerProfileEmbed(
                    buyer is not None,
                    buyer.alias if buyer is not None else None
                ),
                ephemeral=True,
            )

    async def edit_profile(self, interaction: discord.Interaction, name: str):
        """Edit buyer profile"""
        data_store: DataStoreCog = self.bot.get_cog("DataStoreCog")
        if data_store is None:
            return
        data_store.save_buyer_profile(interaction.user.id, name)
        await self.profile_interaction(interaction)
