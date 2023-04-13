from discord.ext import commands
import discord
import asyncio
import os 

import credentials

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', help_command=None, intents=intents)

async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def load_async():
    await load_extensions()

asyncio.run(load_async())

bot.run(credentials.token)
