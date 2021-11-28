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

# Whitelist TODO: Move it out
with open('whitelist.txt', 'r') as file:
  whitelist = file.read().splitlines()

whitelist = [item for item in whitelist if not(item == '' or item.startswith('#'))]

#################
### Bot event ###
#################

@bot.event
async def on_ready():
  print(f'Logged in as {bot.user} (ID: {bot.user.id})')
  print('------')
  activity = discord.Activity(name="links.", type=3)
  await bot.change_presence(status=discord.Status.online, activity=activity)

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
      checkblacklisturl(message.guild.id,url)
      if checkblacklisturl(message.guild.id,url):
        if urlextract.registered_domain not in whitelist and not checkurl(message.guild.id, urlextract.registered_domain, 'whitelist'):
          await deletemsg(message)

# For analytic purposes
@bot.event
async def on_guild_join(guild):
  channel = bot.get_channel(914397885129424976)
  await channel.send('[{0}] {1} ({2}members)'.format(len(bot.guilds), guild.name, guild.member_count))

# Token
with open('token.txt', 'r') as file:
  dtoken = file.read().replace('\n', '')

bot.run(dtoken)
