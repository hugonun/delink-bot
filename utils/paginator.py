import asyncio
import discord

class Pag():
    def __init__(self, client, pages=[]):
        self.buttons = [u"\u23EA", u"\u2B05", "⏹️", u"\u27A1", u"\u23E9"]
        self.currentpage = 0
        self.pages = pages
        self.client = client


    def set_pages(self, pages):
        """Dynamically set the pages"""
        self.pages = pages
    
    async def start(self, ctx):
        """Create a reaction listener and handle reaction responses"""
        msg = await ctx.send(embed=self.pages[0])

        for button in self.buttons:
            await msg.add_reaction(button)

        timedout = False
        while not timedout:
            try:
                reaction, user = await self.client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.message.id == msg.id and reaction.emoji in self.buttons, timeout=60.0)
            except asyncio.TimeoutError:
                embed = self.pages[self.currentpage]
                embed.set_footer(text="Timed out")
                timedout = True
                await msg.clear_reactions()

            else:
                previous_page = self.currentpage
                if reaction.emoji == u"\u23EA":
                    self.currentpage = 0

                elif reaction.emoji == u"\u2B05":
                    if self.currentpage > 0:
                        self.currentpage -= 1

                elif reaction.emoji == u"\u27A1":
                    if self.currentpage < len(self.pages)-1:
                        self.currentpage += 1

                elif reaction.emoji == u"\u23E9":
                    self.currentpage = len(self.pages)-1

                elif reaction.emoji == "⏹️":
                    timedout = True
                    await msg.clear_reactions()
                    return

                if self.currentpage != previous_page:
                    await msg.edit(embed=self.pages[self.currentpage])
                
                for button in self.buttons:
                    await msg.remove_reaction(button, ctx.author)

    async def createPage(self, title: str, description: str, color: discord.Color):
        """Create and return a formatted Embed"""
        embed = discord.Embed()
        if title:
            embed.title = title
        if description:
            embed.description = description  
        if color:
            embed.color = color
        return embed
    
    async def chunktopage(self, chunk: list, color: discord.Color, title: str, insertbefore: str):
        """Take formatted chunks and make a page using the paginator class"""
        for tempchunk in chunk:
            tempchunk.insert(0,insertbefore)
            contenttoadd = '\n'.join(tempchunk)
            self.pages.append(await self.createPage(title=title,description=contenttoadd,color=color))
