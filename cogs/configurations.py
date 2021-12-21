import discord
from discord.ext import commands
from discord.ext.commands.core import has_guild_permissions
from utils.functions import *
import tldextract

class configurations(commands.Cog):
    """All commands pertaining to configurations like adding or removing links."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check_any(has_guild_permissions(manage_webhooks=True),has_guild_permissions(manage_guild=True), has_guild_permissions(administrator=True))
    async def removelink(self, ctx, table:str, msg):
        """Remove a link from the custom white/black list"""
        tabletoedit = whattabletoedit(table=table)
        if tabletoedit != 'blacklist' and tabletoedit != 'whitelist':
            return await ctx.send(tabletoedit)

        url = findurls(msg)[0]
        if not url:
            await ctx.send('No valid URL has been given.')
        else:
            if deleteurl(ctx.guild.id,tldextract.extract(url).registered_domain,tabletoedit):
                await ctx.send('URL has been deleted!')
            else:
                await ctx.send('URL has not been found.')
    
    @removelink.error
    async def removelink_error(self, ctx, error):
        """Handle errors thrown from the removelink command"""
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'To use the removelink command do: {self.bot.command_prefix}removelink <blacklist or whitelist> <url>')
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send('This command may not be used in DMs.')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send('You are missing the required permissions.')
    
    @commands.command()
    @commands.check_any(has_guild_permissions(manage_webhooks=True),has_guild_permissions(manage_guild=True), has_guild_permissions(administrator=True))
    async def addlink(self, ctx, table:str, msg):
        """Add a link to the custom white/black list"""
        tabletoedit = whattabletoedit(table=table)
        if tabletoedit != 'blacklist' and tabletoedit != 'whitelist':
            return await ctx.send(tabletoedit)
        
        reversetabletoedit = "whitelist" if tabletoedit == "blacklist" else "blacklist"
        
        url = findurls(msg)[0]
        if not url:
            await ctx.send('No valid URL has been given.')
        else:
            if checkurl(ctx.guild.id,tldextract.extract(url).registered_domain,reversetabletoedit):
                await ctx.send(f'Error: URL `{tldextract.extract(url).registered_domain}` already exists in your {reversetabletoedit}, to remove it, use `{self.bot.command_prefix}removelink {reversetabletoedit} {tldextract.extract(url).registered_domain}`')
            else:
                inserturl(ctx.guild.id,tldextract.extract(url).registered_domain,tabletoedit)
                await ctx.send(f'URL `{self.bot.command_prefix}` has been added!')

            

    @addlink.error
    async def addlink_error(self, ctx, error):
        """Handle errors thrown from the addlink command"""
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'To use the addlink command do: {self.bot.command_prefix}addlink <blacklist or whitelist> <url>')
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send('This command may not be used in DMs.')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send('You are missing the required permissions.')

def setup(bot):
    """Add class as a cog"""
    bot.add_cog(configurations(bot))
