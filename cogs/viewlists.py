import discord
from discord.ext import commands
from utils.functions import *
from utils.paginator import Pag

from init import whitelist, blacklist

class Viewlists(commands.Cog):
    """View a specified list"""

    def __init__(self, bot):
        self.bot = bot
        self.SIZED_CHUNKS = 10

    @commands.command(aliases=['viewblacklist', 'bl', 'blist'])
    async def blacklist(self, ctx):
        """View the current blacklisted links, globally and local."""
        paginator = Pag(client=self.bot)

        urls = [item for t in retriveurls(ctx.guild.id,'blacklist') for item in t]

        if not urls:
            urls = ['Currently no blacklisted urls']
        
        cchunk = chunkarray(array=urls, size=self.SIZED_CHUNKS)
        gchunk = chunkarray(array=blacklist, size=self.SIZED_CHUNKS)
        await paginator.chunktopage(chunk=cchunk, color=discord.Color.red(),title="Viewing **blacklisted** urls", insertbefore="**Custom blacklist:**")
        await paginator.chunktopage(chunk=gchunk, color=discord.Color.red(),title="Viewing **blacklisted** urls", insertbefore="**Global blacklist:**")
        await paginator.start(ctx=ctx)
    
    @commands.command(aliases=['viewwhitelist', 'wl', 'wlist'])
    async def whitelist(self, ctx):
        """View the current whitelisted links, globally and local."""
        paginator = Pag(client=self.bot)

        urls = [item for t in retriveurls(ctx.guild.id,'whitelist') for item in t]

        if not urls:
            urls = ['Currently no whitelisted urls']
        
        cchunk = chunkarray(array=urls, size=self.SIZED_CHUNKS)
        gchunk = chunkarray(array=whitelist, size=self.SIZED_CHUNKS)
        await paginator.chunktopage(chunk=cchunk, color=discord.Color.green(),title="Viewing **whitelisted** urls", insertbefore="**Custom whitelist:**")
        await paginator.chunktopage(chunk=gchunk, color=discord.Color.green(),title="Viewing **whitelisted** urls", insertbefore="**Global whitelist:**")
        await paginator.start(ctx=ctx)

def setup(bot):
    """Add class as a cog"""
    bot.add_cog(Viewlists(bot))