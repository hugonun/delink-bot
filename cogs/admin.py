from discord.ext import commands
import discord

class Admin(commands.Cog):
    """Admin-only commands that make the bot dynamic."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, extension):
        """Loads a module."""
        try:
            self.bot.load_extension(f'cogs.{extension}')
        except Exception as e:
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, extension):
        """Unloads a module."""
        try:
            self.bot.unload_extension(f'cogs.{extension}')
        except Exception as e:
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def _reload(self, ctx, extension):
        """Reloads a module."""
        try:
            self.bot.unload_extension(f'cogs.{extension}')
            self.bot.load_extension(f'cogs.{extension}')
        except Exception as e:
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def adminstats(self, ctx):
        """Show stats."""
        i = 0
        x = ''
        for guild in ctx.bot.guilds:
            i += 1
            x += '[{0}] {1} ({2}members) [{3}]\n'.format(i, guild.name, guild.member_count, guild.id)
        await ctx.send(x)

def setup(bot):
    """Add class as a cog"""
    bot.add_cog(Admin(bot))