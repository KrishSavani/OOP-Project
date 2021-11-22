# importing required dependencies and libraries after installing the relevant modules
import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
import discord

load_dotenv()   # loads the .env file

token = getenv("TOKEN")  # importing the token value from .env file

# creating object of class commands.Bot (instancation) with a command prefix "!"
bot = commands.Bot(command_prefix="!")

# defining required discord intents (used for implementing some commands later)
intents = discord.Intents.default()
intents.members = True

# passing intents in bot object
bot = commands.Bot(command_prefix="!", intents=intents)

# loads the cog file (firstcog.py) to implement commands/functionalities
bot.load_extension("cogs.firstcog")

bot.afkdict = {}    # defining the afkdict on bot/client side to use it later everywhere


@bot.event              # event listener (gets data of any event)
async def on_ready():   # function called when bot is initialised
    print(
        f'{bot.user} is live!\n'
    )

bot.run(token) # passes the token to run the bot