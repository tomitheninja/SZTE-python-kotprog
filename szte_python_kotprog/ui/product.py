from typing import Optional
from discord import ui
import discord
from discord.ext.commands import Bot

from szte_python_kotprog.models.product import Product


class ProductManageView(ui.View):
    bot: Bot
    products: list[Product]

    def __init__(self, bot: Bot, products: list[Product] = []):
        super().__init__()
        self.bot = bot
        self.products = products

        add = ui.Button(label="Új termék", style=discord.ButtonStyle.success)
        modify = ui.Button(label="Módosítás", style=discord.ButtonStyle.primary)
        remove = ui.Button(label="Törlés", style=discord.ButtonStyle.danger)

        add.callback = self.add
        modify.callback = self.modify
        remove.callback = self.remove

        self.add_item(add)
        self.add_item(modify)
        self.add_item(remove)

    async def add(self, interaction: discord.Interaction):
        await interaction.response.send_modal(ProductEditModal(self.bot))
        
    async def modify(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Válaszd ki a terméket!",
            view=ProductSelectEditedView(self.bot, self.products),
            ephemeral=True,
        )

    async def remove(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Válaszd ki a törölni kívánt termékeket! [max 25]",
            view=ProductSelectDeletedView(self.bot, self.products),
            ephemeral=True,
        )

class ProductManageEmbed(discord.Embed):
    products: list[Product]

    def __init__(self, products: list[Product] = []):
        super().__init__()
        self.products = products
        self.title = "Termékeid"
        self.add_field(
            name="Termékek", value="\n".join([str(p) for p in products]), inline=False
        )
        self.color = discord.Color.blurple()


class ProductEditModal(ui.Modal):
    nameInput: ui.TextInput
    descriptionInput: ui.TextInput
    priceInput: ui.TextInput
    quantityInput: ui.TextInput

    bot: Bot

    def __init__(
        self,
        bot: Bot,
        name: str = None,
        description: str = None,
        price: int = None,
        quantity: int = None,
    ):
        super().__init__(title="Termék szerkesztése")
        self.bot = bot
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

        self.nameInput = ui.TextInput(label="Név", default=name)
        self.descriptionInput = ui.TextInput(
            label="Leírás", default=description, style=discord.TextStyle.paragraph
        )
        self.priceInput = ui.TextInput(
            label="Ár (Ft-ban) [csak szám]",
            default=str(price) if price is not None else "",
            placeholder="Csak nemnegatív egész szám írható",
        )

        self.quantityInput = ui.TextInput(
            label="Elérhető mennyiség [csak szám]",
            default=str(quantity) if quantity is not None else "",
            placeholder="Csak nemnegatív egész szám írható",
        )
        self.add_item(self.nameInput)
        self.add_item(self.descriptionInput)
        self.add_item(self.priceInput)
        self.add_item(self.quantityInput)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            p = int(str(self.priceInput))
            q = int(str(self.quantityInput))
            if p < 0 or q < 0:
                raise ValueError("")
        except ValueError:
            await interaction.response.send_message(
                "Ár és mennyiség csak nemnegatív egész szám lehet!",
                view=ProductEditErrorView(
                    self.bot,
                    str(self.nameInput),
                    str(self.descriptionInput),
                    str(self.priceInput),
                    str(self.quantityInput),
                ),
                ephemeral=True,
            )
            return

        if self.bot.get_cog("SellerProfileCog") is not None:
            await self.bot.get_cog("SellerProfileCog").edit_product(
                interaction,
                str(self.nameInput),
                str(self.descriptionInput),
                int(str(self.priceInput)),
                int(str(self.quantityInput)),
            )


class ProductEditErrorView(ui.View):
    args: tuple
    kwargs: dict

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.btn = ui.Button(label="Újra", style=discord.ButtonStyle.primary)
        self.btn.callback = self.callback
        self.args = args
        self.kwargs = kwargs
        self.add_item(self.btn)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(
            ProductEditModal(*self.args, **self.kwargs)
        )


class ProductSelectEditedView(ui.View):
    bot: Bot
    products: list[Product]
    select: ui.Select

    def __init__(self, bot: Bot, products: list[Product] = []):
        super().__init__()
        self.bot = bot
        self.products = products

        self.select = ui.Select(
            placeholder="Válassz terméket",
            options=[
                discord.SelectOption(label=str(p), value=str(p.name)) for p in products
            ],
            max_values=1,
            min_values=1,
        )
        self.select.callback = self.callback
        self.add_item(self.select)
        
    async def callback(self, interaction: discord.Interaction):
        selectedProduct: Product = None
        for p in self.products:
            if p.name == self.select.values[0]:
                selectedProduct = p
                break
        if selectedProduct is None:
            await interaction.response.send_message("A kiválasztott termék nem található!", ephemeral=True)
            return
        await interaction.response.send_modal(ProductEditModal(
            self.bot,
            selectedProduct.name,
            selectedProduct.description,
            selectedProduct.price,
            selectedProduct.quantity
        ))
            
class ProductSelectDeletedView(ui.View):
    bot: Bot
    products: list[Product]
    select: ui.Select
    
    def __init__(self, bot: Bot, products: list[Product] = []):
        super().__init__()
        self.bot = bot
        self.products = products
        
        self.select = ui.Select(
            placeholder="Válassz terméket",
            options=[
                discord.SelectOption(label=str(p), value=str(p.name)) for p in products
            ],
            max_values=min(25, len(products)),
            min_values=0,
        )
        self.select.callback = self.callback
        self.add_item(self.select)
        
    async def callback(self, interaction: discord.Interaction):
        if self.bot.get_cog("SellerProfileCog") is not None:
            await self.bot.get_cog("SellerProfileCog").delete_products(interaction, self.select.values)