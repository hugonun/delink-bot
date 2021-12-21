import re
import sqlite3
import os
import tldextract
import requests

# make directory for database if it doesnt exist already
path = '{0}/.data/'.format(os.getcwd())
os.makedirs(path, exist_ok=True)

con = sqlite3.connect('.data/delink.db')
cur = con.cursor()

# temporary copy, TODO: move to separate file
with open('whitelist.txt', 'r') as file:
  whitelist = file.read().splitlines()

with open('blacklist.txt', 'r') as file:
  blacklist = file.read().splitlines()

whitelist = [item for item in whitelist if not(item == '' or item.startswith('#'))]
blacklist = [item for item in blacklist if not(item == '' or item.startswith('#'))]

r = requests.get('https://api.hyperphish.com/gimme-domains')
if r.status_code == 200:
  blacklist = blacklist + r.json()

def chunkarray(array: list, size: int):
  """Return a list of specified sized lists from a list"""
  return [array[i:i + size] for i in range(0, len(array), size)]
    
def whattabletoedit(table):
  """Determine what table to edit"""
  blacklistOptions=['blacklist','b','bl','blist','black']
  whitelistOptions=['whitelist','w','wl','wlist','white']

  if table in blacklistOptions:
    return 'blacklist'
  elif table in whitelistOptions:
    return 'whitelist'
  else:
    return 'That is not a vaild option please say {0} to blacklist a url or {1} to white list a url'.format(", ".join(blacklistOptions[:-1]) +" or "+blacklistOptions[-1], ", ".join(whitelistOptions[:-1]) +" or "+whitelistOptions[-1])

def findurls(s):
  """Use a regex to pull URLs from a message"""
  regex = r"(?i)\b(((https?|ftp|smtp):\/\/)?(www.)?[a-zA-Z0-9_.-]+\.[a-zA-Z0-9_.-]+(\/[a-zA-Z0-9#]+\/?)*\/*)"
  url = re.findall(regex,s)
  return [x[0] for x in url]

async def deletemsg(message):
  """Delete specified message"""
  await message.delete()
  await message.channel.send('WARNING: Your message has been deleted for containing a possible scam URL. <@' + str(message.author.id) + '>', delete_after=5)

def setupdb():
  """Ensure the database is setup correctly"""
  cur.execute('''CREATE TABLE IF NOT EXISTS blacklist
  (guild_id int, url text, UNIQUE(guild_id, url))''')

  cur.execute('''CREATE TABLE IF NOT EXISTS whitelist
  (guild_id int, url text, UNIQUE(guild_id, url))''')

  cur.execute('''CREATE TABLE IF NOT EXISTS guildsettings
  (guild_id int, logchannel int, mutelogchannel int, muterank int, deletesbeforemute int, UNIQUE(guild_id))''')

  cur.execute('''CREATE TABLE IF NOT EXISTS mutecandidates
  (user_id int, guild_id int, deletions int, lastdelete int)''')

  con.commit()

def inserturl(guild_id, url, table):
  """Insert a URL into the specified table. EX: blacklist or whitelist"""
  cur.execute('''INSERT OR IGNORE INTO %s VALUES (?,?)''' % (table), (guild_id,url))
  con.commit()
      
def deleteurl(guild_id, url, table):
  """Delete a URL from the specified table. EX: blacklist or whitelist"""
  cur.execute('''DELETE FROM %s WHERE url = ? AND guild_id = ?''' % (table), (guild_id,url))
  con.commit()

def retriveurls(guild_id, table):
  """Retrieve all URLs from the specified table. EX: blacklist or whitelist"""
  cur.execute('''SELECT url FROM %s WHERE guild_id = ?''' % (table), (guild_id,))
  return cur.fetchall()

def checkurl(guild_id, url, table):
  """Check if a URL is in the white/black list table"""
  cur.execute('''SELECT url FROM %s WHERE guild_id = ? AND url = ?''' % (table), (guild_id,url))
  return cur.fetchone()

def checkblacklisturl(guild_id, url):
  urlextract = tldextract.extract(url)
  # Check registered domain
  if urlextract.registered_domain in blacklist:
    return True
  # Check subdomains
  elif urlextract.subdomain and not urlextract.subdomain == "www":
    suburl = urlextract.subdomain.split('.')
    if suburl[0] == 'www':
      suburl.pop(0)
    suburl.reverse()
    oldsub = '.'
    for sub in suburl:
      urltocheck = sub + oldsub + urlextract.registered_domain
      oldsub = '.' + sub + oldsub
      if urltocheck in blacklist:
        return True
  # Check in DB (TODO: Check subdomains too)
  elif checkurl(guild_id, urlextract.registered_domain, 'blacklist'):
    return True
  # Pass
  else:
    return False

