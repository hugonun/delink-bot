import discord
from discord.ext import commands
import tldextract

from functions import *

description = '''Link filter bot.
'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!d ', help_command=None, description=description, intents=intents)

# Whitelist and blacklist
with open('whitelist.txt', 'r') as file:
  whitelist = file.read().splitlines()

with open('blacklist.txt', 'r') as file:
  blacklist = file.read().splitlines()

whitelist = [item for item in whitelist if not(item == '' or item.startswith('#'))]
blacklist = [item for item in blacklist if not(item == '' or item.startswith('#'))]

@bot.event
async def on_ready():
  print(f'Logged in as {bot.user} (ID: {bot.user.id})')
  print('------')
  game = discord.Game("word.exe")
  await bot.change_presence(status=discord.Status.online, activity=game)

@bot.command()
async def ping(ctx):
  await ctx.send('Pong!')

@bot.event
async def on_message(message):
  # read blacklist.txt and whitelist.txt, and filter from there
  urllist = findurls(message.content)
  if urllist:
    for url in urllist:
      urlextract = tldextract.extract(url)
      # Filter by TLD
      if urlextract.suffix in ['gift','gifts']:
        if urlextract.registered_domain not in whitelist:
          await deletemsg(message)
      # Filter by blacklist
      if urlextract.registered_domain in blacklist:
        if urlextract.registered_domain not in whitelist:
          await deletemsg(message)

# Token
with open('token.txt', 'r') as file:
    dtoken = file.read().replace('\n', '')

bot.run(dtoken)
