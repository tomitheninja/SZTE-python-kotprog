"""Entry point"""

import json
import sys
import pickle
import logging

import discord
from discord.ext import commands
from szte_python_kotprog.cogs.contact import ContactCog

from szte_python_kotprog.cogs.search import SearchCog

from .cogs.data_store import DataStoreCog
from .cogs.seller_profile import SellerProfileCog
from .cogs.buyer_profile import BuyerProfileCog

discord.utils.setup_logging()


if len(sys.argv) < 2:
    logging.warning("Nincs megadva fájlnév! (Alapértelmezett: config.json)")
    sys.argv.append("config.json")

try:
    with open(sys.argv[1], "r", encoding="UTF-8") as file:
        config: dict = json.load(file)
except FileNotFoundError:
    logging.error("A megadott konfigurációs fájl nem létezik! [%s]", sys.argv[1])
    sys.exit(1)
except json.JSONDecodeError:
    logging.error("A megadott fájl nem JSON formátumú!")
    sys.exit(1)

if config.get("dc_token") is None or config.get("dc_token").strip() == "":
    logging.error("A megadott fájl nem tartalmazza a DC API kulcsot!")
    sys.exit(1)

intent = discord.Intents.default()
intent.message_content = True

bot = commands.Bot(command_prefix=config.get("prefix", "!"), intents=intent)

# pylint: disable=invalid-name
data_store = None
try:
    with open(config.get("pickle", "data.pickle"), "rb") as file:
        data_store = pickle.load(file)
except FileNotFoundError:
    logging.warning("A megadott pickle fájl nem létezik! létrehozok egy újat!")
except pickle.UnpicklingError:
    logging.error("A megadott pickle fájl nem pickle formátumú!")
    sys.exit(1)
except EOFError:
    logging.error("Sérült pickle fájl!")
    sys.exit(1)

# @bot.hybrid_command(name="test")
# async def test(ctx: commands.Context):
#     await ctx.interaction.response.send_modal(ProductEditModal(lambda x: None))


@bot.event
async def on_ready():
    """After bot is ready, sync the tree and add cogs"""
    if bot.get_cog("DataStoreCog") is None:
        await bot.add_cog(DataStoreCog(bot, config, data_store))
    if bot.get_cog("SellerProfileCog") is None:
        await bot.add_cog(SellerProfileCog(bot))
    if bot.get_cog("BuyerProfileCog") is None:
        await bot.add_cog(BuyerProfileCog(bot))
    if bot.get_cog("SearchCog") is None:
        await bot.add_cog(SearchCog(bot))
    if bot.get_cog("ContactCog") is None:
        await bot.add_cog(ContactCog(bot))
    logging.info("Bot is starting sync...")
    await bot.tree.sync()
    logging.info("Bot is ready!")


bot.run(config["dc_token"], log_handler=None)
