from nextcord.ext import commands
from util.esi import getHSIncursion
from util.focus import noFocusEmbed , generateEmbed

class Utility(commands.Cog):
    def __init__(self,client):
        self.client = client


    @commands.guild_only()
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command()
    async def focus(self,ctx):
        incursion = getHSIncursion()
        if incursion is None:
            e = noFocusEmbed()
        else:
           e = generateEmbed(incursion,filename="influence.png")
        # file = File("temp/influence.png", filename="influence.png")
        # e.set_image(url="attachment://influence.png")
        await ctx.send(embed=e)
           
    @commands.guild_only()
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command()
    async def route(self,ctx):
        pass

def setup(client):
    client.add_cog(Utility(client))