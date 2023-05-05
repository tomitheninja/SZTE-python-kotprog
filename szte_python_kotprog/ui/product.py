"""UI elements for product management"""
from discord import ui
import discord
from discord.ext.commands import Bot
from szte_python_kotprog.cogs.data_store import DataStoreCog

from szte_python_kotprog.models.product import Product


class ProductManageView(ui.View):
    """Button definition for product management"""

    bot: Bot
    products: list[Product]

    def __init__(self, bot: Bot, products: list[Product] = None):
        if products is None:
            products = []
        super().__init__()
        self.bot = bot
        self.products = products

        add = ui.Button(label="Új termék", style=discord.ButtonStyle.success)
        modify = ui.Button(label="Módosítás", style=discord.ButtonStyle.primary)
        remove = ui.Button(label="Törlés", style=discord.ButtonStyle.danger)
        sell = ui.Button(label="Eladás rögzítése", style=discord.ButtonStyle.secondary)

        add.callback = self.add
        modify.callback = self.modify
        remove.callback = self.remove
        sell.callback = self.sell

        self.add_item(add)
        self.add_item(modify)
        self.add_item(remove)
        self.add_item(sell)

    async def add(self, interaction: discord.Interaction):
        """Callback for add button"""
        await interaction.response.send_modal(ProductEditModal(self.bot))

    async def modify(self, interaction: discord.Interaction):
        """Callback for modify button"""
        await interaction.response.send_message(
            "Válaszd ki a terméket!",
            view=ProductSelectEditedView(self.bot, self.products),
            ephemeral=True,
        )

    async def remove(self, interaction: discord.Interaction):
        """Callback for remove button"""
        await interaction.response.send_message(
            "Válaszd ki a törölni kívánt termékeket! [max 25]",
            view=ProductSelectDeletedView(self.bot, self.products),
            ephemeral=True,
        )

    async def sell(self, interaction: discord.Interaction):
        """Callback for sell button"""
        await interaction.response.send_message(
            "Válaszd ki a terméket!",
            view=ProductSelectSellView(self.bot, self.products),
            ephemeral=True,
        )


class ProductManageEmbed(discord.Embed):
    """Embed definition for product management"""

    products: list[Product]

    def __init__(self, products: list[Product] = None):
        if products is None:
            products = []
        super().__init__()
        self.products = products
        self.title = "Termékeid"
        self.add_field(
            name="Termékek", value="\n".join([str(p) for p in products]), inline=False
        )
        self.color = discord.Color.blurple()


class ProductEditModal(ui.Modal):
    """Modal definition for product editing"""

    name_input: ui.TextInput
    description_input: ui.TextInput
    price_input: ui.TextInput
    quantity_input: ui.TextInput

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

        self.name_input = ui.TextInput(label="Név", default=name)
        self.description_input = ui.TextInput(
            label="Leírás", default=description, style=discord.TextStyle.paragraph
        )
        self.price_input = ui.TextInput(
            label="Ár (Ft-ban) [csak szám]",
            default=str(price) if price is not None else "",
            placeholder="Csak nemnegatív egész szám írható",
        )

        self.quantity_input = ui.TextInput(
            label="Elérhető mennyiség [csak szám]",
            default=str(quantity) if quantity is not None else "",
            placeholder="Csak nemnegatív egész szám írható",
        )
        self.add_item(self.name_input)
        self.add_item(self.description_input)
        self.add_item(self.price_input)
        self.add_item(self.quantity_input)

    # pylint: disable=arguments-differ
    async def on_submit(self, interaction: discord.Interaction):
        try:
            price = int(str(self.price_input))
            quantity = int(str(self.quantity_input))
            if price < 0 or quantity < 0:
                raise ValueError("")
        except ValueError:
            await interaction.response.send_message(
                "Ár és mennyiség csak nemnegatív egész szám lehet!",
                view=ProductEditErrorView(
                    self.bot,
                    str(self.name_input),
                    str(self.description_input),
                    str(self.price_input),
                    str(self.quantity_input),
                ),
                ephemeral=True,
            )
            return

        if self.bot.get_cog("SellerProfileCog") is not None:
            await self.bot.get_cog("SellerProfileCog").edit_product(
                interaction,
                str(self.name_input),
                str(self.description_input),
                int(str(self.price_input)),
                int(str(self.quantity_input)),
            )


class ProductEditErrorView(ui.View):
    """View definition for product editing error (and retry)"""

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
        """Callback for retry button"""
        await interaction.response.send_modal(
            ProductEditModal(*self.args, **self.kwargs)
        )


class ProductSelectEditedView(ui.View):
    """View definition to select product for editing"""

    bot: Bot
    products: list[Product]
    select: ui.Select

    def __init__(self, bot: Bot, products: list[Product] = None):
        if products is None:
            products = []
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
        """Callback for select dropdown"""
        selected_product: Product = None
        for product in self.products:
            if product.name == self.select.values[0]:
                selected_product = product
                break
        if selected_product is None:
            await interaction.response.send_message(
                "A kiválasztott termék nem található!", ephemeral=True
            )
            return
        await interaction.response.send_modal(
            ProductEditModal(
                self.bot,
                selected_product.name,
                selected_product.description,
                selected_product.price,
                selected_product.quantity,
            )
        )


class ProductSelectDeletedView(ui.View):
    """View definition to select product for deletion"""

    bot: Bot
    products: list[Product]
    select: ui.Select

    def __init__(self, bot: Bot, products: list[Product] = None):
        if products is None:
            products = []
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
        """Callback for select dropdown"""
        if self.bot.get_cog("SellerProfileCog") is not None:
            await self.bot.get_cog("SellerProfileCog").delete_products(
                interaction, self.select.values
            )


class ProductSelectSellView(ui.View):
    """View definition to select sold product"""

    bot: Bot
    products: list[Product]
    select: ui.Select

    def __init__(self, bot: Bot, products: list[Product] = None):
        if products is None:
            products = []
        super().__init__()
        self.bot = bot
        self.products = products

        self.select = ui.Select(
            placeholder="Válassz terméket",
            options=[
                discord.SelectOption(label=str(p), value=str(p.name))
                for p in products
                if p.quantity > 0
            ],
            max_values=1,
            min_values=1,
        )
        self.select.callback = self.callback
        self.add_item(self.select)

    async def callback(self, interaction: discord.Interaction):
        """Callback for select dropdown"""
        data_store: DataStoreCog = self.bot.get_cog("DataStoreCog")
        if data_store is None:
            return
        for product in data_store.products:
            if (
                product.name == self.select.values[0]
                and product in product.seller.products
            ):
                await interaction.response.send_modal(
                    ProductSellModal(self.bot, product)
                )
                break


class ProductSellModal(ui.Modal, title="Termék eladása"):
    """Modal definition for quantity of product sold"""
    orig_quantity: str
    product: Product
    bot: Bot

    def __init__(self, bot: Bot, product: Product, orig_quantity: str = "1"):
        super().__init__()
        self.bot = bot
        self.orig_quantity = orig_quantity
        self.product = product

        self.quantity_input = ui.TextInput(
            label="Mennyiség [csak szám]", default=self.orig_quantity
        )
        self.add_item(self.quantity_input)

    # pylint: disable=arguments-differ
    async def on_submit(self, interaction: discord.Interaction):
        """Callback for submit button"""
        try:
            quantity = int(str(self.quantity_input))
            if quantity < 1 or quantity > self.product.quantity:
                raise ValueError
        except ValueError:
            await interaction.response.send_message(
                f"Csak 0-nál nagyobb, de a készletnél ({self.product.quantity})"
                " kisebb vagy egyenlő szám lehet!",
                view=ProductSellErrorView(
                    self.bot, self.product, str(self.quantity_input)
                ),
                ephemeral=True,
            )
            return
        if self.bot.get_cog("SellerProfileCog") is not None:
            await self.bot.get_cog("SellerProfileCog").edit_product(
                interaction,
                self.product.name,
                self.product.description,
                self.product.price,
                self.product.quantity - int(str(self.quantity_input)),
            )


class ProductSellErrorView(ui.View):
    """View definition for product selling error (and retry)"""

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
        """Callback for retry button"""
        await interaction.response.send_modal(
            ProductSellModal(*self.args, **self.kwargs)
        )
