import discord
from discord import client
from discord.ext import commands
import tldextract
from paginator import Pag

from functions import *

description = '''Link filter bot.
'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!d ', help_command=None, description=description, intents=intents)

setupdb()
@bot.event
async def on_reaction_add(reaction, user):
  
  print("adding reaction")

@bot.event
async def on_reaction_remove(reaction, user):
  print("removing reaction")

@bot.event
async def on_raw_reaction_add(payload):
  pass

@bot.event
async def on_raw_reaction_remove(payload):
  pass


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

@bot.command()
async def addlink(ctx, table:str, msg):
  blacklistOptions=['blacklist','b','bl','blist','black']
  whitelistOptions=['whitelist','w','wl','wlist','white']
  if table in blacklistOptions:
    tabletoedit='blacklist'
  elif table in whitelistOptions:
    tabletoedit='whitelist'
  else:
    return await ctx.send('That is not a vaild option please say {0} to blacklist a url or {1} to white list a url'.format(", ".join(blacklistOptions[:-1]) +" or "+blacklistOptions[-1], ", ".join(whitelistOptions[:-1]) +" or "+whitelistOptions[-1]))
  url = findurls(msg)[0]
  if not url:
    await ctx.send('No valid URL has been given.')
  else:
    inserturls(ctx.guild.id,tldextract.extract(url).registered_domain,tabletoedit)
    await ctx.send('URL has been added!')

@bot.command()
async def removelink(ctx, table:str, *, msg):
  blacklistOptions=['blacklist','b','bl','blist','black']
  whitelistOptions=['whitelist','w','wl','wlist','white']
  if table in blacklistOptions:
    tabletoedit='blacklist'
  elif table in whitelistOptions:
    tabletoedit='whitelist'
  else:
    return await ctx.send('That is not a vaild option please say {0} to blacklist a url or {1} to white list a url'.format(", ".join(blacklistOptions[:-1]) +" or "+blacklistOptions[-1], ", ".join(whitelistOptions[:-1]) +" or "+whitelistOptions[-1]))
  url = findurls(msg)[0]
  if not url:
    await ctx.send('No valid URL has been given.')
  else:
    deleteurls(ctx.guild.id,tldextract.extract(url).registered_domain,tabletoedit)
    await ctx.send('URL has been deleted!')

@bot.command()
async def viewblacklist(ctx):
  urls = retriveurls(ctx.guild.id,'blacklist')
  if not urls:
    urls = ['Currently no blacklisted urls']
  
  pages=[]
  SIZED_CHUNKS = 10
  cchunk = [urls[i:i + SIZED_CHUNKS] for i in range(0, len(urls), SIZED_CHUNKS)]
  for chunk in cchunk:
    chunk.insert(0,'**Custom blacklist:**')
    contenttoadd = '\n'.join(chunk)
    pages.append(contenttoadd)
  
  gchunk = [blacklist[i:i + SIZED_CHUNKS] for i in range(0, len(blacklist), SIZED_CHUNKS)]
  for chunk in gchunk:
    chunk.insert(0,'**Global blacklist:**')
    contenttoadd = '\n'.join(chunk)
    pages.append(contenttoadd)
  await Pag(title='Viewing **blacklisted** urls', color=discord.Colour.green(), entries=pages, length=1).start(ctx)

@bot.command()
async def viewwhitelist(ctx):
  urls = retriveurls(ctx.guild.id,'whitelist')
  if not urls:
    urls = ['Currently no whitelisted urls']
  
  pages=[]
  SIZED_CHUNKS = 10
  cchunk = [urls[i:i + SIZED_CHUNKS] for i in range(0, len(urls), SIZED_CHUNKS)]
  for chunk in cchunk:
    chunk.insert(0,'**Custom whitelist:**')
    contenttoadd = '\n'.join(chunk)
    pages.append(await Pag(client=bot, pages=pages).createPage(title='Viewing **whitelisted** urls',description=contenttoadd,colour=discord.Colour.green()))
  
  gchunk = [whitelist[i:i + SIZED_CHUNKS] for i in range(0, len(whitelist), SIZED_CHUNKS)]
  for chunk in gchunk:
    chunk.insert(0,'**Global whitelist:**')
    contenttoadd = '\n'.join(chunk)
    pages.append(await Pag(client=bot, pages=pages).createPage(title='Viewing **whitelisted** urls',description=contenttoadd,colour=discord.Colour.green()))
  await Pag(client=bot, pages=pages).start(ctx=ctx)

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
      print(checkurl(message.guild.id, urlextract.registered_domain, 'whitelist'))
      if urlextract.registered_domain in blacklist or checkurl(message.guild.id, urlextract.registered_domain, 'blacklist'):
        if urlextract.registered_domain not in whitelist and not checkurl(message.guild.id, urlextract.registered_domain, 'whitelist'):
          await deletemsg(message)


# Token
with open('token.txt', 'r') as file:
    dtoken = file.read().replace('\n', '')

bot.run(dtoken)
