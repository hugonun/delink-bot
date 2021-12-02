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
        
    @commands.command()
    async def invite(self, ctx):
        """Invite the bot to your server."""
        await ctx.send("https://discord.com/oauth2/authorize?client_id=903114852631969802&scope=bot&permissions=2147871808")
        
    @commands.command()
    async def support(self, ctx):
        """Join our support server."""
        await ctx.send("https://discord.com/invite/Gf3panp2bw")


def setup(bot):
    """Add class as a cog"""
    bot.add_cog(Info(bot))
