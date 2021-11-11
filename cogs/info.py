import discord
from discord.ext import commands
import time

class Info(commands.Cog):
    """Commands pertaining to system information like ping, server stats, etc."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Get the bot's current websocket and API latency."""
        start_time = time.time()
        message = await ctx.send("Testing Ping...")
        end_time = time.time()

        await message.edit(content=f"Pong! {round(self.bot.latency * 1000)}ms\nAPI: {round((end_time - start_time) * 1000)}ms")


def setup(bot):
    """Add class as a cog"""
    bot.add_cog(Info(bot))