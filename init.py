from re import findall
import discord
from discord.ext import commands

from functions import *

description = '''Link filter bot.
'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!d ', help_command=None, description=description, intents=intents)

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
  # remove all domains using .gift TLD
  urllist = findurls(message.content)
  print(urllist)
  
  if 0==1:
    await ctx.send('Possible scam link has been deleted!', delete_after=5)
    

# Token
with open('token.txt', 'r') as file:
    dtoken = file.read().replace('\n', '')

bot.run(dtoken)
