import discord

class Pag():
    def __init__(self, client, pages):
        self.buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"]
        self.currentpage = 0
        self.pages = pages
        self.client = client

    async def start(self, ctx):

        msg = await ctx.send(embed=self.pages)

        for button in self.buttons:
            await msg.add_reaction(button)

        while True:
            try:
                reaction, user = await self.client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in self.buttons, timeout=60.0)
            except:
                pass

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

                for button in self.buttons:
                    await msg.remove_reaction(button, ctx.author)

                if self.currentpage != previous_page:
                    await msg.edit(embed=self.pages[self.currentpage])

    async def createPage(self, title: str, description: str, colour: discord.Colour):
        embed = discord.Embed()
        if title:
            embed.title = title
        if description:
            embed.description = description  
        if colour:
            embed.colour = colour
        return embed
