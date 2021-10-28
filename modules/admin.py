from nextcord.ext import commands
from nextcord import Embed
import asyncio
import json
class Admin(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command()
    @commands.guild_only()
    @commands.has_any_role(895714070815211581,826051937400782879)
    async def setup(self,ctx):
        guildID = ctx.guild.id
        channelID = ctx.channel.id
        e = Embed(title="Setting Up!")
        message = await ctx.send(embed=e)
        messageID = message.id
        message2 = await ctx.send(f"Message ID: {messageID}\nChannel ID: {channelID}\nGuild ID: {guildID}")
        with open('guild_config/config.json','r') as conf:
            data = json.load(conf)
        with open('guild_config/config.json','w') as conf: 
            data['message_id'] = messageID
            data['guild_id'] = guildID
            data['channel_id'] = channelID
            json.dump(data,conf)
        await asyncio.sleep(2)
        e = Embed(title='Set Up')
        await message.edit(embed=e)
        await message2.delete()

def setup(client):
    client.add_cog(Admin(client))