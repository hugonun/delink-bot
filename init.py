import discord
from discord.ext import commands
from discord.ext.commands.core import has_guild_permissions
import tldextract
from paginator import Pag
from functions import *
import os

description = '''Link filter bot.
'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!d ', help_command=None, description=description, intents=intents)

setupdb()

# Whitelist and blacklist
with open('whitelist.txt', 'r') as file:
  whitelist = file.read().splitlines()

with open('blacklist.txt', 'r') as file:
  blacklist = file.read().splitlines()

whitelist = [item for item in whitelist if not(item == '' or item.startswith('#'))]
blacklist = [item for item in blacklist if not(item == '' or item.startswith('#'))]

PAGES=[]
SIZED_CHUNKS = 10
pagniator = Pag(client=bot, pages=PAGES)
    
@bot.event
async def on_ready():
  print(f'Logged in as {bot.user} (ID: {bot.user.id})')
  print('------')
  game = discord.Game("word.exe")
  await bot.change_presence(status=discord.Status.online, activity=game)

# @bot.command()
# async def load(ctx, extension):
#   bot.load_extension(f'cogs.{extension}')
#   await ctx.send(f'{extension} has been loaded.')

# @bot.command()
# async def unload(ctx, extension):
#   bot.unload_extension(f'cogs.{extension}')
#   await ctx.send(f'{extension} has been unloaded.')

# @bot.command()
# async def _reload(ctx, extension):
#   try:
#     bot.unload_extension(f'cogs.{extension}')
#     bot.load_extension(f'cogs.{extension}')
#   except Exception as e:
#     await ctx.send('An error occurred.')

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_message(message):
  await bot.process_commands(message)

  # read blacklist.txt and whitelist.txt, and filter from there
  urllist = findurls(message.content)
  if urllist:
    for url in urllist:
      urlextract = tldextract.extract(url)
      # Filter by TLD
      if urlextract.suffix in ['gift','gifts']:
        if url.startswith(('http://', 'https://')):
          if urlextract.registered_domain not in whitelist and not checkurl(message.guild.id, urlextract.registered_domain, 'whitelist'):
            await deletemsg(message)
      # Filter by blacklist
      if urlextract.registered_domain in blacklist or checkurl(message.guild.id, urlextract.registered_domain, 'blacklist'):
        if urlextract.registered_domain not in whitelist and not checkurl(message.guild.id, urlextract.registered_domain, 'whitelist'):
          await deletemsg(message)

# Token
with open('token.txt', 'r') as file:
    dtoken = file.read().replace('\n', '')

bot.run(dtoken)
