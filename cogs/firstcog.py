from discord.ext import commands
import discord
import time
import json
from pathlib import Path
import random

file_path = Path("database/afk.json")


class TestCogCommands(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.last_msg = None
        self.file = None
        self.json_content = None
        self.key = 0

    @commands.command(name="helpcogs")
    async def help(self, ctx: commands.Context):
        """Help command."""
        embed = discord.Embed(title="Commands Help",
                              description="Gives a guide on how to use CogsBot (command prefix = !)", color=0xe40101)
        embed.add_field(name="ping", value="Get the bot's current websocket and API latency.", inline=False)
        embed.add_field(name="setstatus", value="Set the bot's current discord status.", inline=False)
        embed.add_field(name="snipeback", value="A command to snipe delete messages.", inline=False)
        embed.add_field(name="afk", value="Allows you to set yourself as afk and the bot handles the rest.",
                        inline=True)
        embed.add_field(name="getquote", value="Get a random quote to make your life better.", inline=False)
        embed.set_footer(text="Made by Krish, Ohm and Kunal")
        await ctx.send(embed=embed)

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        """Get the bot's current websocket and API latency."""
        start_time = time.time()
        message = await ctx.reply("Testing Ping...")
        end_time = time.time()

        await message.edit(
            content=f"Pong! {round(self.bot.latency * 1000)}ms\nAPI: {round((end_time - start_time) * 1000)}ms")

    @commands.command(name="setstatus")
    async def set_status(self, ctx: commands.Context, *, text: str):
        """Set the bot's current discord status."""
        await self.bot.change_presence(activity=discord.Game(name=text))

    @commands.command(name="snipeback")
    async def snipe(self, ctx: commands.Context):
        """A command to snipe delete messages."""
        if not self.last_msg:  # on_message_delete hasn't been triggered since the bot started
            await ctx.send("There is no message to snipe!")
            return

        author = self.last_msg.author
        content = self.last_msg.content

        embed = discord.Embed(title=f"Message from {author}", description=content)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = self.bot.get_channel(912185169614626836)

        if not channel:
            return

        await channel.send(f"Welcome, {member}!")

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        self.last_msg = message

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.bot.user.id:
            return
        if "!afk" in message.content:
            return

        self.bot.afkdict = self.getData()

        for member in message.mentions:

            if member != message.author and member.name + "#" + str(member.discriminator) in self.bot.afkdict.keys():
                name = member.name + "#" + str(member.discriminator)
                await message.reply(
                    content=f"Oh noes! {member.mention} is currently AFK.\nReason: **{self.bot.afkdict[name]}**")

    @commands.command(name="afk")
    async def afk(self, ctx, *, message="They didn't leave a message!"):
        """Allows you to set yourself as afk and the bot handles the rest."""
        if str(ctx.message.author) in self.bot.afkdict:
            self.bot.afkdict.pop(str(ctx.message.author))
            self.saveData(self.bot.afkdict)
            await ctx.send('Welcome back! You are no longer afk.')

        else:
            self.bot.afkdict[str(ctx.message.author)] = message
            await ctx.send("You are now afk. Beware of the real world!")
        self.saveData(self.bot.afkdict)


    @commands.command(name="getquote")
    async def getquote(self, ctx):
        """Get a random quote to make your life better."""
        quote = self.getQuote()
        await ctx.send("Your quote : " + quote)

    def getData(self):
        self.file = open(file_path, "r")
        self.json_content = json.load(self.file)
        self.file.close()
        return self.json_content

    def saveData(self, afkdict):
        self.file = open(file_path, "w")
        self.json_content = json.dumps(afkdict)
        self.file.write(self.json_content)
        self.file.close()

    def getQuote(self):
        self.file = open("database/quotes.json", "r")
        content = json.load(self.file)
        quote = random.choice(list(content.values()))
        self.file.close()
        return quote


def setup(bot: commands.Bot):
    bot.add_cog(TestCogCommands(bot))
