import discord
from discord import client
from discord.ext import commands
import tldextract

from functions import *

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

def addlocallists():
  urls = retriveurls('597171669550759936', 'blacklist')
  blacklist.append(url for url in urls if not(url == '' or url.startswith('#')))
  
  urls = retriveurls('597171669550759936', 'whitelist')
  whitelist.append(url for url in urls if not(url == '' or url.startswith('#')))

@bot.event
async def on_ready():
  print(f'Logged in as {bot.user} (ID: {bot.user.id})')
  print('------')
  game = discord.Game("word.exe")
  await bot.change_presence(status=discord.Status.online, activity=game)

@bot.command(# ADDS THIS VALUE TO THE $HELP PING MESSAGE.
	help="Uses come crazy logic to determine if pong is actually the correct value or not.",
	# ADDS THIS VALUE TO THE $HELP MESSAGE.
	brief="Prints pong back to the channel."
  )
async def ping(ctx):
  await ctx.send('Pong!')

@bot.command()
async def addlink(ctx, table:str, *, msg):
  blacklistOptions=['blacklist','b','bl','blist','black']
  whitelistOptions=['whitelist','w','wl','wlist','white']
  print(table in blacklistOptions)
  if table in blacklistOptions:
    tabletoedit='blacklist'
  elif table in whitelistOptions:
    tabletoedit='whitelist'
  else:
    return await ctx.send('That is not a vaild option please say {0} to blacklist a url or {1} to white list a url'.format(", ".join(blacklistOptions[:-1]) +" or "+blacklistOptions[-1], ", ".join(whitelistOptions[:-1]) +" or "+whitelistOptions[-1]))
  urls = findurls(msg)
  inserturls(msg.guild.id,urls,tabletoedit)
  await ctx.send('Adding link')

@bot.command()
async def removelink(ctx, table:str, *, msg):
  blacklistOptions=['blacklist','b','bl','blist','black']
  whitelistOptions=['whitelist','w','wl','wlist','white']
  print(table in blacklistOptions)
  if table in blacklistOptions:
    tabletoedit='blacklist'
  elif table in whitelistOptions:
    tabletoedit='whitelist'
  else:
    return await ctx.send('That is not a vaild option please say {0} to blacklist a url or {1} to white list a url'.format(", ".join(blacklistOptions[:-1]) +" or "+blacklistOptions[-1], ", ".join(whitelistOptions[:-1]) +" or "+whitelistOptions[-1]))
  print(tabletoedit)
  urls = findurls(msg)
  deleteurls(msg.guild.id,urls,tabletoedit)
  await ctx.send('Removing link')

@bot.command()
async def viewblacklist(ctx):
  embed = discord.Embed(author=ctx.message.author, colour=discord.Colour.red(), title='Viewing **blacklisted** urls')
  urls = retriveurls('597171669550759936','blacklist')
  if not urls:
    urls = ['Currently no blacklisted urls']
  print(urls)
  embed.description = 'Custom blacklist: \n'+'\n'.join(urls)
  embed.description += 'Global blacklist: \n'+'\n'.join(blacklist)
  await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
  print(error)
  pass

@addlink.error
async def addlink_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send('Please include whether you want to whitelist or blacklist and then a url(s) to add.\nExample: {0}addlink whitelist google.com'.format(bot.command_prefix))
    
@removelink.error
async def addlink_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send('Please include whether you want to whitelist or blacklist and then a url(s) to add.\nExample: {0}removelink blacklist google.com'.format(bot.command_prefix))

@bot.event
async def on_message(message):
  
  if message.content.startswith('!d'):
    await bot.process_commands(message)

  bot.all_commands
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
