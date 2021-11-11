import discord
from discord.ext import commands
from functions import *

from init import whitelist, blacklist, PAGES, SIZED_CHUNKS, pagniator

class Viewlists(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def chunktopage(self, chunk: list, color: discord.Color, title: str, insertbefore: str):
        for tempchunk in chunk:
            tempchunk.insert(0,insertbefore)
            contenttoadd = '\n'.join(tempchunk)
            PAGES.append(await pagniator.createPage(title=title,description=contenttoadd,color=color))

    @commands.command()
    async def viewblacklist(self, ctx):
        PAGES.clear()
        urls = [item for t in retriveurls(ctx.guild.id,'blacklist') for item in t]

        if not urls:
            urls = ['Currently no blacklisted urls']
        
        cchunk = chunkarray(array=urls, size=SIZED_CHUNKS)
        gchunk = chunkarray(array=blacklist, size=SIZED_CHUNKS)
        await self.chunktopage(chunk=cchunk, color=discord.Color.red(),title="Viewing **blacklisted** urls", insertbefore="**Custom blacklist:**")
        await self.chunktopage(chunk=gchunk, color=discord.Color.red(),title="Viewing **blacklisted** urls", insertbefore="**Global blacklist:**")
        pagniator.set_pages(pages=PAGES)
        await pagniator.start(ctx=ctx)
    
    @commands.command()
    async def viewwhitelist(self, ctx):
        PAGES.clear()
        urls = [item for t in retriveurls(ctx.guild.id,'whitelist') for item in t]

        if not urls:
            urls = ['Currently no whitelisted urls']
        
        cchunk = chunkarray(array=urls, size=SIZED_CHUNKS)
        gchunk = chunkarray(array=whitelist, size=SIZED_CHUNKS)
        await self.chunktopage(chunk=cchunk, color=discord.Color.green(),title="Viewing **whitelisted** urls", insertbefore="**Custom whitelist:**")
        await self.chunktopage(chunk=gchunk, color=discord.Color.green(),title="Viewing **whitelisted** urls", insertbefore="**Global whitelist:**")
        pagniator.set_pages(pages=PAGES)
        await pagniator.start(ctx=ctx)

def setup(bot):
    bot.add_cog(Viewlists(bot))