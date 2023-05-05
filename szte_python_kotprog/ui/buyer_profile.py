"""UI elements for buyer profile management"""

from discord import ui
import discord
from discord.colour import Colour

class BuyerProfileView(ui.View):
    """Button definition for buyer profile management"""
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
    """Embed definition for buyer profile"""
    def __init__(self, registered: bool = False, name: str = None):
        super().__init__()
        self.title = "Vásárlói profil"
        self.color = Colour.green() if registered else Colour.red()
        if registered:
            self.add_field(name="Név", value=name, inline=False)
        else:
            self.description = "Még nem regisztráltál vásárlóként."


class BuyerRegisterModal(ui.Modal, title="Vásárló regisztráció"):
    """Modal definition for buyer registration"""
    callback: callable
    orig_name: str

    def __init__(self, callback: callable, origName: str = None) -> None:
        super().__init__()
        self.callback = callback
        self.orig_name = origName

        self.name = ui.TextInput(label="Álnév (így fognak az eladók látni)", default=self.orig_name)
        self.add_item(self.name)

    # pylint: disable=arguments-differ
    async def on_submit(self, interaction: discord.Interaction):
        if self.callback is None:
            return
        await self.callback(interaction, str(self.name))
