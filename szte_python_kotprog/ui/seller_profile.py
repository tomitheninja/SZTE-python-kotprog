"""UI for seller profile management"""

from discord import SelectOption, ui
import discord
from discord.ext.commands import Bot
from discord.colour import Colour

from szte_python_kotprog.models.county import County
from szte_python_kotprog.models.product import Product
from szte_python_kotprog.ui.product import ProductManageEmbed, ProductManageView


class SellerProfileView(ui.View):
    """Button definition for seller profile management"""

    bot: Bot
    name: str
    counties: list[County]
    products: list[Product]

    def __init__(
        self,
        bot: Bot,
        registered: bool,
        name: str = None,
        counties: list[County] = None,
        products: list[Product] = None,
    ):
        if counties is None:
            counties = []
        if products is None:
            products = []
        self.bot = bot
        self.name = name
        self.counties = counties
        self.products = products

        super().__init__()
        btn = ui.Button(
            label="Szerkesztés" if registered else "Regisztráció",
            style=discord.ButtonStyle.primary,
        )

        btn.callback = self.edit
        self.add_item(btn)

        if registered:
            manage = ui.Button(
                label="Termékek kezelése", style=discord.ButtonStyle.primary
            )
            manage.callback = self.manage
            self.add_item(manage)

    async def edit(self, interaction: discord.Interaction):
        """Callback for edit button"""
        await interaction.response.send_modal(
            SellerRegisterModal(self.bot, self.name, self.counties)
        )

    async def manage(self, interaction: discord.Interaction):
        """Callback for manage button"""
        await interaction.response.send_message(
            embed=ProductManageEmbed(self.products),
            view=ProductManageView(self.bot, self.products),
            ephemeral=True,
        )


class SellerProfileEmbed(discord.Embed):
    """Embed definition for seller profile management"""

    def __init__(
        self,
        registered: bool = False,
        name: str = None,
        counties: list[County] = None,
        products: list[Product] = None,
    ):
        if counties is None:
            counties = []
        if products is None:
            products = []
        super().__init__()
        self.title = "Eladói profil"
        self.color = Colour.green() if registered else Colour.red()
        if registered:
            self.add_field(name="Név", value=name, inline=False)
            self.add_field(
                name="Kiszolgált vármegyék",
                value=", ".join([x.name for x in counties]),
                inline=False,
            )
            if len(products) == 0:
                self.add_field(name="Termékek", value="*Nincs termék*", inline=False)
            else:
                self.add_field(
                    name="Termékek",
                    value="\n".join([f"- {str(x)}" for x in products]),
                    inline=False,
                )
        else:
            self.description = "Még nem regisztráltál eladóként."


class SellerRegisterModal(ui.Modal, title="Eladó regisztráció"):
    """Modal definition for seller profile registration"""

    bot: Bot
    orig_name: str
    orig_counties: list[County]

    def __init__(
        self,
        bot: Bot,
        orig_name: str = None,
        orig_counties: list[County] = None,
    ) -> None:
        if orig_counties is None:
            orig_counties = []
        super().__init__()
        self.bot = bot
        self.orig_name = orig_name
        self.orig_counties = orig_counties

        self.name = ui.TextInput(
            label="Álnév (így fognak a vásárlóid látni)", default=orig_name
        )
        self.add_item(self.name)

    # pylint: disable=arguments-differ
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Kiváló {self.name}! Most add meg a kiszolgált területeket:",
            view=SellerSelectRegions(self.bot, str(self.name), self.orig_counties),
            ephemeral=True,
        )


class SellerSelectRegions(ui.View):
    """View definition for seller region selection"""

    bot: Bot
    name: str
    orig_counties: list[County]

    def __init__(self, bot: Bot, name: str, orig_counties: list[County] = None):
        super().__init__()
        if orig_counties is None:
            orig_counties = []

        self.bot = bot
        self.name = name
        self.orig_counties = orig_counties

        self.regions = ui.Select(
            placeholder="Kiszolgált területek",
            options=[
                SelectOption(
                    label=c.name, value=c.name, default=(c in self.orig_counties)
                )
                for c in County
            ],
            max_values=20,
        )
        self.add_item(self.regions)
        self.regions.callback = self.callback

    async def callback(self, interaction: discord.Interaction):
        """Callback for region selection"""
        if self.bot.get_cog("SellerProfileCog") is None:
            return
        await self.bot.get_cog("SellerProfileCog").edit_profile(
            interaction, str(self.name), [County[x] for x in self.regions.values]
        )
