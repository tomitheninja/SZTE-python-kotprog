"""Belépési pont"""

import json
import sys
import discord
from discord.ext import commands
import pickle

from .cogs.data_store import DataStoreCog
from .cogs.seller_profile import SellerProfileCog

if len(sys.argv) < 2:
    print("Nincs megadva fájlnév! (Alapértelmezett: config.json)")
    sys.argv.append("config.json")

try:
    with open(sys.argv[1], "r", encoding="UTF-8") as f:
        data = json.load(f)
except FileNotFoundError:
    print("A megadott fájl nem létezik!")
    sys.exit(1)
except json.JSONDecodeError:
    print("A megadott fájl nem JSON formátumú!")
    sys.exit(1)

if data.get("dc_token") is None or data.get("dc_token").strip() == "":
    print("A megadott fájl nem tartalmazza a DC API kulcsot!")
    sys.exit(1)

intent = discord.Intents.default()
intent.message_content = True

bot = commands.Bot(command_prefix="!", intents=intent)

data_store_cog = None
try:
    with open(data.get("pickle"), "rb") as f:
        data_store_cog = pickle.load(f)
except FileNotFoundError:
    print("A megadott pickle fájl nem létezik! létrehozok egy újat!")
except pickle.UnpicklingError:
    print("A megadott pickle fájl nem pickle formátumú!")
    sys.exit(1)

@bot.event
async def on_ready():
    """Indulás után a parancs fa szinkronizálása"""
    if data_store_cog is not None:
        bot.add_cog(data_store_cog)
    else:
        await bot.add_cog(DataStoreCog(bot))
    await bot.add_cog(SellerProfileCog(bot))
    print("Bot is starting sync...")
    await bot.tree.sync()
    print("Bot is ready!")


bot.run(data["dc_token"])
