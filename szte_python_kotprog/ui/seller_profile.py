from discord import SelectOption, ui
import discord
from discord.ext.commands import Bot
from discord.colour import Colour

from szte_python_kotprog.models.county import County
from szte_python_kotprog.models.product import Product
from szte_python_kotprog.ui.product import ProductManageEmbed, ProductManageView


class SellerProfileView(ui.View):
    bot: Bot
    name: str
    counties: list[County]
    products: list[Product]

    def __init__(
        self,
        bot: Bot,
        registered: bool,
        name: str = None,
        counties: list[County] = [],
        products: list[Product] = [],
    ):
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
        await interaction.response.send_modal(
            SellerRegisterModal(self.bot, self.name, self.counties)
        )

    async def manage(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            embed=ProductManageEmbed(self.products),
            view=ProductManageView(self.bot, self.products),
            ephemeral=True,
        )


class SellerProfileEmbed(discord.Embed):
    def __init__(
        self,
        registered: bool = False,
        name: str = None,
        counties: list[County] = [],
        products: list[Product] = [],
    ):
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
    bot: Bot
    origName: str
    origCounties: list[County]

    def __init__(
        self,
        bot: Bot,
        origName: str = None,
        origCounties: list[County] = [],
    ) -> None:
        super().__init__()
        self.bot = bot
        self.origName = origName
        self.origCounties = origCounties

        self.name = ui.TextInput(
            label="Álnév (így fognak a vásárlóid látni)", default=origName
        )
        self.add_item(self.name)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Kiváló {self.name}! Most add meg a kiszolgált területeket:",
            view=SellerSelectRegions(self.bot, str(self.name), self.origCounties),
            ephemeral=True,
        )


class SellerSelectRegions(ui.View):
    bot: Bot
    name: str
    origCounties: list[County]

    def __init__(self, bot: Bot, name: str, origCounties: list[County] = []):
        super().__init__()

        self.bot = bot
        self.name = name
        self.origCounties = origCounties

        self.regions = ui.Select(
            placeholder="Kiszolgált területek",
            options=[
                SelectOption(
                    label=c.name, value=c.name, default=(c in self.origCounties)
                )
                for c in County
            ],
            max_values=20,
        )
        self.add_item(self.regions)
        self.regions.callback = self.on_submit

    async def on_submit(self, interaction: discord.Interaction):
        if self.bot.get_cog("SellerProfileCog") is None:
            return
        await self.bot.get_cog("SellerProfileCog").edit_profile(
            interaction, str(self.name), [County[x] for x in self.regions.values]
        )
