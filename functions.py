import re

def findurls(s):
      regex = r"(?i)\b(((https?|ftp|smtp):\/\/)?(www.)?[a-zA-Z0-9_.-]+\.[a-zA-Z0-9_.-]+(\/[a-zA-Z0-9#]+\/?)*/*)$"
      url = re.findall(regex,s)
      return [x[0] for x in url]

async def deletemsg(message):
    await message.delete()
    await message.channel.send('WARNING: Your message has been deleted for containing a possible scam URL.', delete_after=5)