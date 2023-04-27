from typing import Optional
from discord import SelectOption, ui
import discord
from discord.colour import Colour
from discord.utils import MISSING

from szte_python_kotprog.models.county import County
from szte_python_kotprog.models.product import Product


class SellerProfileView(ui.View):
    
    def __init__(self, registered: bool, callback: callable):
        super().__init__()
        btn = ui.Button(label= "Szerkesztés" if registered else "Regisztráció", style=discord.ButtonStyle.primary)
        
        async def edit(interaction: discord.Interaction):
            await interaction.response.send_modal(SellerRegisterModal(callback))
        
        btn.callback = edit
        self.add_item(btn)
        
        if registered:
            manage = ui.Button(label="Termékek kezelése", style=discord.ButtonStyle.primary)
            manage.callback = self.manage
            self.add_item(manage)
            
    async def manage(self, interaction: discord.Interaction):
        await interaction.response.send_message(content="kezelés")
            
class SellerProfileEmbed(discord.Embed):
    def __init__(self, registered: bool = False, name: str = None, counties: list[County] = None, products: list[Product] = None):
        super().__init__()
        self.title = "Eladói profil"
        self.color = Colour.green() if registered else Colour.red()
        if registered:
            self.add_field(name="Név", value=name, inline=False)
            self.add_field(name="Kiszolgált vármegyék", value=", ".join([x.name for x in counties]), inline=False)
            self.add_field(name="Termékek", value="\n".join([f"- {str(x.name)}" for x in products]), inline=False)
        else:
            self.description = "Még nem regisztráltál eladóként."
    
            
        

class SellerRegisterModal(ui.Modal, title="Eladó regisztráció"):
    callback: callable
    def __init__(self, callback: callable) -> None:
        super().__init__()
        self.callback = callback
    
    name = ui.TextInput(label="Álnév")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Kiváló {self.name}! Most add meg a kiszolgált területeket:",
            view=SellerSelectRegions(str(self.name), self.callback),
            ephemeral=True,
        )


class SellerSelectRegions(ui.View):
    regions = ui.Select(
        placeholder="Kiszolgált területek",
        options=[SelectOption(label=c.name, value=c.name) for c in County],
        max_values=20,
    )
    
    name: str
    callback: callable

    def __init__(self, name: str, callback: callable):
        super().__init__()
        self.add_item(self.regions)
        self.name = name
        self.callback = callback
        self.regions.callback = self.on_submit

    async def on_submit(self, interaction: discord.Interaction):
        if self.callback is None:
            return
        await self.callback(interaction, self.name, [County[x] for x in self.regions.values])
