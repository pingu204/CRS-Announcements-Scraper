"""
Last Updated:
07/29/2024
"""

import os
from dotenv import load_dotenv

from discord.ext import commands
import discord

intents = discord.Intents.all()
intents.members = True
intents.guilds = True
intents.reactions = True

bot = commands.Bot(prefix='$', help_command=None, intents=intents)

# Bot secrets
load_dotenv()
BOT_TOKEN = os.getenv("TOKEN")

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    activity = discord.Activity(name='UP Naming Mahal', type=discord.ActivityType.listening)
    await bot.change_presence(activity=activity)

# Load cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(BOT_TOKEN)

