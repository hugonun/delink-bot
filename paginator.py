import asyncio
import discord

class Pag():
    def __init__(self, client, pages):
        self._buttons = [u"\u23EA", u"\u2B05", "⏹️", u"\u27A1", u"\u23E9"]
        self._currentpage = 0
        self._pages = pages
        self._client = client

    def set_pages(self, pages):
        self._pages = pages
    
    async def start(self, ctx):

        msg = await ctx.send(embed=self._pages[0])

        for button in self._buttons:
            await msg.add_reaction(button)

        while True:
            try:
                reaction, user = await self._client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in self._buttons, timeout=60.0)
            except asyncio.TimeoutError:
                embed = self._pages[self._currentpage]
                embed.set_footer(text="Timed out")
                await msg.clear_reactions()

            else:
                previous_page = self._currentpage
                if reaction.emoji == u"\u23EA":
                    self._currentpage = 0

                elif reaction.emoji == u"\u2B05":
                    if self._currentpage > 0:
                        self._currentpage -= 1

                elif reaction.emoji == u"\u27A1":
                    if self._currentpage < len(self._pages)-1:
                        self._currentpage += 1

                elif reaction.emoji == u"\u23E9":
                    self._currentpage = len(self._pages)-1

                elif reaction.emoji == "⏹️":
                    await msg.clear_reactions()
                    return

                for button in self._buttons:
                    await msg.remove_reaction(button, ctx.author)

                if self._currentpage != previous_page:
                    await msg.edit(embed=self._pages[self._currentpage])

    async def createPage(self, title: str, description: str, colour: discord.Colour):
        embed = discord.Embed()
        if title:
            embed.title = title
        if description:
            embed.description = description  
        if colour:
            embed.colour = colour
        return embed
