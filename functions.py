import re
import sqlite3
import os

# make directory for database if it doesnt exist already
path = '{0}/.data/'.format(os.getcwd())
os.makedirs(path, exist_ok=True)

con = sqlite3.connect('.data/delink.db')
cur = con.cursor()

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
  """Use a regex to pull any url from a message"""
  regex = r"(?i)\b(((https?|ftp|smtp):\/\/)?(www.)?[a-zA-Z0-9_.-]+\.[a-zA-Z0-9_.-]+(\/[a-zA-Z0-9#]+\/?)*/*)$"
  url = re.findall(regex,s)
  return [x[0] for x in url]

async def deletemsg(message):
  """Delete any message"""
  await message.delete()
  await message.channel.send('WARNING: Your message has been deleted for containing a possible scam URL.', delete_after=5)

def setupdb():
  """Ensure the database is setup correctly"""
  cur.execute('''CREATE TABLE IF NOT EXISTS blacklist
  (guild_id int, url text, UNIQUE(guild_id, url))''')

  cur.execute('''CREATE TABLE IF NOT EXISTS whitelist
  (guild_id int, url text, UNIQUE(guild_id, url))''')

  con.commit()

def inserturl(guild_id, url, table):
  """Insert a url into the specified table/list. EX: blacklist or whitelist"""
  cur.execute('''INSERT OR IGNORE INTO %s VALUES (?,?)''' % (table), (guild_id,url))
  con.commit()
      
def deleteurl(guild_id, url, table):
  """Delete a url from the specified table/list. EX: blacklist or whitelist"""
  cur.execute('''DELETE FROM %s WHERE url = ? AND guild_id = ?''' % (table), (guild_id,url))
  con.commit()

def retriveurls(guild_id, table):
  """Retrieve all urls from the specified table/list. EX: blacklist or whitelist"""
  cur.execute('''SELECT url FROM %s WHERE guild_id = ?''' % (table), (guild_id,))
  return cur.fetchall()

def checkurl(guild_id, url, table):
  """Check if a url is in local white/black list"""
  cur.execute('''SELECT url FROM %s WHERE guild_id = ? AND url = ?''' % (table), (guild_id,url))
  return cur.fetchone()
