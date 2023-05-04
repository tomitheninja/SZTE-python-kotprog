from discord import SelectOption, ui
import discord
from discord.colour import Colour

from szte_python_kotprog.models.county import County
from szte_python_kotprog.models.product import Product


class BuyerProfileView(ui.View):
    def __init__(self, registered: bool, callback: callable, name: str = None):
        super().__init__()
        btn = ui.Button(
            label="Szerkesztés" if registered else "Regisztráció",
            style=discord.ButtonStyle.primary,
        )

        async def edit(interaction: discord.Interaction):
            await interaction.response.send_modal(BuyerRegisterModal(callback, name))

        btn.callback = edit
        self.add_item(btn)


class BuyerProfileEmbed(discord.Embed):
    def __init__(self, registered: bool = False, name: str = None):
        super().__init__()
        self.title = "Vásárlói profil"
        self.color = Colour.green() if registered else Colour.red()
        if registered:
            self.add_field(name="Név", value=name, inline=False)
        else:
            self.description = "Még nem regisztráltál vásárlóként."


class BuyerRegisterModal(ui.Modal, title="Vásárló regisztráció"):
    callback: callable
    origName: str

    def __init__(self, callback: callable, origName: str = None) -> None:
        super().__init__()
        self.callback = callback
        self.origName = origName

        self.name = ui.TextInput(label="Álnév (így fognak az eladók látni)", default=self.origName)
        self.add_item(self.name)

    async def on_submit(self, interaction: discord.Interaction):
        if self.callback is None:
            return
        await self.callback(interaction, str(self.name))
