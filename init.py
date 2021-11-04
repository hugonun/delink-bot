import discord
from discord.ext import commands
from discord.ext.commands.core import has_guild_permissions
import tldextract
from paginator import Pag

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


PAGES=[]
SIZED_CHUNKS = 10
pagniator = Pag(client=bot, pages=PAGES)

async def chunktopage(chunk: list, color: discord.Color, title: str, insertbefore: str):
  for tempchunk in chunk:
    tempchunk.insert(0,insertbefore)
    contenttoadd = '\n'.join(tempchunk)
    PAGES.append(await pagniator.createPage(title=title,description=contenttoadd,color=color))
    
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
@commands.check_any(has_guild_permissions(manage_webhooks=True),has_guild_permissions(manage_guild=True), has_guild_permissions(administrator=True))
async def addlink(ctx, table:str, msg):
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
async def addlink_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send('To use the removelink command do: {0}removelink <blacklist or whitelist> <url>')
  elif isinstance(error, commands.NoPrivateMessage):
    await ctx.send('This command may not be used in dms')
  elif isinstance(error, commands.MissingPermissions):
    await ctx.send('You are missing the requirred permissions')

@bot.command()
@commands.check_any(has_guild_permissions(manage_webhooks=True),has_guild_permissions(manage_guild=True), has_guild_permissions(administrator=True))
async def removelink(ctx, table:str, msg):
  tabletoedit = whattabletoedit(table=table)
  if tabletoedit != 'blacklist' and tabletoedit != 'whitelist':
    return await ctx.send(tabletoedit)

  url = findurls(msg)[0]
  if not url:
    await ctx.send('No valid URL has been given.')
  else:
    deleteurl(ctx.guild.id,tldextract.extract(url).registered_domain,tabletoedit)
    await ctx.send('URL has been deleted!')
  
@removelink.error
async def removelink_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send('To use the removelink command do: {0}removelink <blacklist or whitelist> <url>')
  elif isinstance(error, commands.NoPrivateMessage):
    await ctx.send('This command may not be used in dms')
  elif isinstance(error, commands.MissingPermissions):
    await ctx.send('You are missing the requirred permissions')

@bot.command()
async def viewblacklist(ctx):
  PAGES.clear()
  #urls = retriveurls(ctx.guild.id,'blacklist')
  urls = [item for t in retriveurls(ctx.guild.id,'blacklist') for item in t]

  if not urls:
    urls = ['Currently no blacklisted urls']
  
  cchunk = chunkarray(array=urls, size=SIZED_CHUNKS)
  gchunk = chunkarray(array=blacklist, size=SIZED_CHUNKS)
  await chunktopage(chunk=cchunk, color=discord.Color.red(),title="Viewing **blacklisted** urls", insertbefore="**Custom blacklist:**")
  await chunktopage(chunk=gchunk, color=discord.Color.red(),title="Viewing **blacklisted** urls", insertbefore="**Global blacklist:**")
  pagniator.set_pages(pages=PAGES)
  await pagniator.start(ctx=ctx)
  
@bot.command()
async def viewwhitelist(ctx):
  PAGES.clear()
  #urls = retriveurls(ctx.guild.id,'whitelist')
  urls = [item for t in retriveurls(ctx.guild.id,'whitelist') for item in t]

  if not urls:
    urls = ['Currently no whitelisted urls']
  
  cchunk = chunkarray(array=urls, size=SIZED_CHUNKS)
  gchunk = chunkarray(array=blacklist, size=SIZED_CHUNKS)
  await chunktopage(chunk=cchunk, color=discord.Color.green(),title="Viewing **whitelisted** urls", insertbefore="**Custom whitelist:**")
  await chunktopage(chunk=gchunk, color=discord.Color.green(),title="Viewing **whitelisted** urls", insertbefore="**Global whitelist:**")
  pagniator.set_pages(pages=PAGES)
  await pagniator.start(ctx=ctx)

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
