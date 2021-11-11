import discord
from discord.ext import commands
from discord.ext.commands.core import has_guild_permissions
from functions import *
import tldextract

class Addlink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check_any(has_guild_permissions(manage_webhooks=True),has_guild_permissions(manage_guild=True), has_guild_permissions(administrator=True))
    async def addlink(self, ctx, table:str, msg):
        tabletoedit = whattabletoedit(table=table)
        if tabletoedit != 'blacklist' and tabletoedit != 'whitelist':
            return await ctx.send(tabletoedit)
        
        url = findurls(msg)[0]
        if not url:
            await ctx.send('No valid URL has been given.')
        else:
            inserturl(ctx.guild.id,tldextract.extract(url).registered_domain,tabletoedit)
            await ctx.send('URL has been added!')

    @addlink.error
    async def addlink_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'To use the removelink command do: {self.bot.command_prefix}removelink <blacklist or whitelist> <url>')
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send('This command may not be used in dms')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send('You are missing the requirred permissions')

def setup(bot):
    bot.add_cog(Addlink(bot))