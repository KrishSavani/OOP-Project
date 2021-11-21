import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
import discord



load_dotenv()

token = getenv("TOKEN")

bot = commands.Bot(command_prefix="!")

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

bot.load_extension("cogs.firstcog")

bot.run(token)
