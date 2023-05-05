"""Product search cog"""

import discord
from discord.ext import commands
from szte_python_kotprog.cogs.data_store import DataStoreCog
from szte_python_kotprog.models.county import County

from szte_python_kotprog.ui.search import (
    SearchHitEmbed,
    SearchSelectCountiesView,
    SearchView,
)


class SearchCog(commands.Cog):
    """Product search cog"""
    bot: commands.Bot

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command("keres", aliases=["keresés"])
    async def search(self, ctx: commands.Context):
        """Search for products"""
        data_store: DataStoreCog = self.bot.get_cog("DataStoreCog")
        if data_store is None:
            return

        profile = data_store.profiles.get(ctx.author.id)
        if profile is None:
            await self.bot.get_cog("BuyerProfileCog").profile(ctx)
            return
        buyer = profile.buyer
        if buyer is None:
            await self.bot.get_cog("BuyerProfileCog").profile(ctx)
            return

        counties_to_pick_from = data_store.get_populated_counties()
        default_counties = buyer.counties

        if len(counties_to_pick_from) == 0:
            await ctx.send("Nincs elérhető megye", ephemeral=True)
            return
        await ctx.send(
            "Kereséshez először válassz megyéket, amelyekben keresel!",
            view=SearchSelectCountiesView(
                self.bot, counties_to_pick_from, default_counties
            ),
            ephemeral=True,
        )

    async def search_interaction(
        self,
        interaction: discord.Interaction,
        counties: list[County] = None,
        product_name: str = None,
    ):
        """Search for products"""
        if counties is None:
            counties = []
        data_store: DataStoreCog = self.bot.get_cog("DataStoreCog")
        if data_store is None:
            return
        data_store.save_county_preferences(interaction.user.id, counties)
        hits = data_store.search_product(counties, product_name)
        await interaction.response.send_message(
            "__Találatok:__",
            embeds=[SearchHitEmbed(x) for x in hits],
            view=SearchView(self.bot, hits, counties, product_name),
            ephemeral=True,
        )
