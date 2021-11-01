import re
import sqlite3

import tldextract
from discord.ext.commands.core import guild_only
con = sqlite3.connect('delink.db')
cur = con.cursor()

def findurls(s):
  regex = r"(?i)\b(((https?|ftp|smtp):\/\/)?(www.)?[a-zA-Z0-9_.-]+\.[a-zA-Z0-9_.-]+(\/[a-zA-Z0-9#]+\/?)*/*)$"
  url = re.findall(regex,s)
  return [x[0] for x in url]

async def deletemsg(message):
  await message.delete()
  await message.channel.send('WARNING: Your message has been deleted for containing a possible scam URL.', delete_after=5)

def setupdb():
  cur.execute('''CREATE TABLE IF NOT EXISTS blacklist
  (guild_id int, url text, UNIQUE(guild_id, url))''')

  cur.execute('''CREATE TABLE IF NOT EXISTS whitelist
  (guild_id int, url text, UNIQUE(guild_id, url))''')

  con.commit()

def inserturls(guild_id, url, table):
  cur.execute('''INSERT OR IGNORE INTO %s VALUES (?,?)''' % (table), (guild_id,url))
  con.commit()
      
def deleteurls(guild_id, url, table):
  cur.execute('''DELETE FROM %s WHERE url = ? AND guild_id = ?''' % (table), (guild_id,url))
  con.commit()

def retriveurls(guild_id, table):
  cur.execute('''SELECT url FROM %s WHERE guild_id = ?''' % (table), (guild_id,))
  return cur.fetchall()

def checkurl(guild_id, url, table):
  cur.execute('''SELECT url FROM %s WHERE guild_id = ? AND url = ?''' % (table), (guild_id,url))
  return cur.fetchone()
