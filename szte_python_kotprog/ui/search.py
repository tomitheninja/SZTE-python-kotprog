"""UI elements for the search page"""

import discord
from discord import ui
from discord.ext.commands import Bot

# from szte_python_kotprog.cogs.search import SearchCog

from szte_python_kotprog.models.county import County
from szte_python_kotprog.models.product import Product


class SearchSelectCountiesView(ui.View):
    """Button and select definition for county selection"""

    bot: Bot
    counties: list[County]
    default_counties: list[County]
    county_input: ui.Select

    def __init__(
        self,
        bot: Bot,
        counties: list[County] = None,
        default_counties: list[County] = None,
    ):
        if default_counties is None:
            default_counties = []
        if counties is None:
            counties = list(County)
        super().__init__()
        self.bot = bot
        self.counties = counties
        self.default_counties = default_counties

        self.county_input = ui.Select(
            placeholder="Válassz vármegyét!",
            options=[
                discord.SelectOption(
                    label=county.name,
                    value=county.value,
                    default=(county in default_counties),
                )
                for county in counties
            ],
            min_values=1,
            max_values=min(len(counties), 25),
        )

        self.default_btn = ui.Button(
            label="Előző keresés alapján", style=discord.ButtonStyle.secondary
        )
        self.all_btn = ui.Button(
            label="Keresés mindenhol", style=discord.ButtonStyle.primary
        )

        self.county_input.callback = self.county_input_callback
        self.default_btn.callback = self.default_btn_callback
        self.all_btn.callback = self.all_btn_callback

        self.add_item(self.county_input)
        self.add_item(self.default_btn)
        self.add_item(self.all_btn)

    async def county_input_callback(self, interaction: discord.Interaction):
        """Callback for county selection"""
        search = self.bot.get_cog("SearchCog")
        await search.search_interaction(
            interaction, [County(int(x)) for x in self.county_input.values]
        )

    async def default_btn_callback(self, interaction: discord.Interaction):
        """Callback for default query button"""
        search = self.bot.get_cog("SearchCog")
        await search.search_interaction(interaction, self.default_counties)

    async def all_btn_callback(self, interaction: discord.Interaction):
        """Callback for country wide query button"""
        search = self.bot.get_cog("SearchCog")
        await search.search_interaction(interaction, self.counties)


class SearchHitEmbed(discord.Embed):
    """Embed for a search hit"""

    def __init__(self, product: Product):
        super().__init__()
        self.set_author(name=f"Eladó: {product.seller.alias}")
        self.color = discord.Color.green()
        self.add_field(name="Ár", value=f"{product.price} Ft", inline=True)
        self.add_field(
            name="Elérhető mennyiség", value=f"{product.quantity} db", inline=True
        )
        self.title = product.name
        self.description = product.description


class SearchView(ui.View):
    """View for the search page"""

    bot: Bot
    hits: list[Product]
    counties: list[County]
    product_name: str

    products_listed: dict[int, Product]

    def __init__(
        self,
        bot: Bot,
        hits: list[Product],
        counties: list[County] = None,
        product_name: str = None,
    ):
        super().__init__()
        if counties is None:
            data_store = bot.get_cog("DataStoreCog")
            counties = data_store.get_populated_counties()
        self.bot = bot
        self.hits = hits
        self.counties = counties
        self.product_name = product_name

        self.products_listed = {}
        options = []
        for hit in hits:
            self.products_listed[hash(hit)] = hit
            options.append(discord.SelectOption(label=str(hit), value=hash(hit)))

        self.select = ui.Select(
            placeholder="Valamelyik megtetszett?",
            options=options,
            min_values=0,
            max_values=1,
        )

        self.search_btn = ui.Button(
            label="Kulcsszavak szerinti szűrés", style=discord.ButtonStyle.primary
        )

        self.search_btn.callback = self.search_btn_callback
        self.select.callback = self.select_callback

        self.add_item(self.select)
        self.add_item(self.search_btn)

    async def search_btn_callback(self, interaction: discord.Interaction):
        """Callback for the search button"""
        await interaction.response.send_modal(
            SearchModal(self.bot, self.counties, self.product_name)
        )

    async def select_callback(self, interaction: discord.Interaction):
        """Callback for the result select"""
        if interaction.channel.type != discord.ChannelType.private:
            await interaction.response.send_message(
                "Privát üzenetben folytatódik a munkamenet!", ephemeral=True
            )
        else:
            await interaction.response.send_message("Egy pillanat!")
        await self.bot.get_cog("ContactCog").prompt_contact(
            interaction.user, self.products_listed[int(self.select.values[0])]
        )


class SearchModal(ui.Modal, title="Keresés"):
    """Modal for the search page"""

    bot: Bot
    counties: list[County]
    product_name: str

    def __init__(
        self, bot: Bot, counties: list[County] = None, product_name: str = None
    ):
        super().__init__()
        self.bot = bot
        self.counties = counties
        self.product_name = product_name

        self.product_name_input = ui.TextInput(
            label="Keresett termék neve", default=self.product_name
        )
        self.add_item(self.product_name_input)

    # pylint: disable=arguments-differ
    async def on_submit(self, interaction: discord.Interaction):
        """Callback for the submit button""" ""
        await self.bot.get_cog("SearchCog").search_interaction(
            interaction, self.counties, str(self.product_name_input.value)
        )
