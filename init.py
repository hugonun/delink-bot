import discord
from discord.ext import commands
import tldextract
from utils.paginator import Pag
from utils.functions import *
import os

description = '''Link filter bot.'''

intents = discord.Intents.default()
intents.members = True
help_command = commands.DefaultHelpCommand(
    no_category = 'Need some help?'
)
bot = commands.Bot(command_prefix='!d ', help_command= help_command, description=description, intents=intents)

setupdb()

# Whitelist and blacklist
with open('whitelist.txt', 'r') as file:
  whitelist = file.read().splitlines()

with open('blacklist.txt', 'r') as file:
  blacklist = file.read().splitlines()

whitelist = [item for item in whitelist if not(item == '' or item.startswith('#'))]
blacklist = [item for item in blacklist if not(item == '' or item.startswith('#'))]

#################
### Bot event ###
#################

@bot.event
async def on_ready():
  print(f'Logged in as {bot.user} (ID: {bot.user.id})')
  print('------')
  game = discord.Game("word.exe")
  await bot.change_presence(status=discord.Status.online, activity=game)

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
