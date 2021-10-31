import re
import sqlite3

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
      (guild_id text, url text, UNIQUE(guild_id, url))''')

      cur.execute('''CREATE TABLE IF NOT EXISTS whitelist
      (guild_id text, url text, UNIQUE(guild_id, url))''')

      con.commit()

def inserturls(guild_id, urls, table):
      def valuestoinsert(url_pool):
            for url in url_pool:
                  yield (guild_id, url)
      cur.executemany('''INSERT OR IGNORE INTO %s VALUES (?,?)''' % (table), valuestoinsert(urls))
      
      con.commit()
      
def deleteurls(guild_id, urls, table):
      def valuestoinsert(url_pool):
            for url in url_pool:
                  yield (guild_id, url)
      cur.executemany('''DELETE FROM %s WHERE url = ? AND guild_id = ?''' % (table),valuestoinsert(urls))
      
      con.commit()

def retriveurls(guild_id, table):

      print(len(guild_id))
      cur.execute('''SELECT url FROM %s WHERE guild_id = ?''' % (table), (guild_id))

      return cur.fetchall()