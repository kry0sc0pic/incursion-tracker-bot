import asyncio
import json
from nextcord.ext import commands,tasks
from util.focus import generateEmbed,noFocusEmbed
from util.esi import getHSIncursion
from util.tsparser import getNowTS
class Updater(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.guild_only()
    # @commands.has_any_role(895714070815211581,826051937400782879)
    @commands.command(aliases=['stop'])
    async def pause(self,ctx):
        try:
            self.liveFocusStatus.stop()
            m = await ctx.send("Pausing Live Focus Updates")
        except:
            m = await ctx.send("Failed To Pause Live Focus Updates")

        await asyncio.sleep(5)
        await m.delete()

    @commands.guild_only()
    # @commands.has_any_role(895714070815211581,826051937400782879) 
    @commands.command(aliases=['start'])
    async def resume(self,ctx):
        try:
            self.liveFocusStatus.start()
            m = await ctx.send("Starting Live Focus Updates")
        except:
            m = await ctx.send("Failed To Start Live Focus Updates")

        await asyncio.sleep(5)
        await m.delete()

    @tasks.loop(seconds=5)
    async def liveFocusStatus(self):
        with open('guild_config/config.json','r') as conf:
            data = json.load(conf)
        log_channel = self.client.get_channel(data['log_channel'])
        channelID = data['channel_id']
        messageID = data['message_id']
        channel = self.client.get_channel(channelID)
        message = await channel.fetch_message(messageID)
        while True:
            try:
                incursion = getHSIncursion() # Get Incursion

            # Load Data
                with open('current_focus/focus.json','r') as lastUpdate:
                    lastUpdateData = json.load(lastUpdate)
                print(lastUpdateData)

                # Check if focus has gone down
                if(lastUpdateData["focusUp"]==True and incursion==None):
                    print("Focus Down , New Focus in 2-3 days?")
                    with open('current_focus/focus.json','w') as lastUpdate:
                        lastUpdateData['focusUp'] = False
                        json.dump(lastUpdateData , lastUpdate)
                    print("cp1")
                    e = noFocusEmbed()
                    await message.edit(embed=e)
                    await log_channel.send(f"Focus is Down\nUpdated Focus Embed\n⏱ | Last Updated: {getNowTS()}") 

                elif(lastUpdateData['focusUp']==False and incursion == None):
                    print("No Focus")
                    e = noFocusEmbed()
                    await message.edit(embed=e)
                    await log_channel.send(f"No Focus Spawned\nUpdated Focus Embed\n⏱ | Last Updated: {getNowTS()}")
                
                elif(lastUpdateData['focusUp']==False and incursion != None):
                    print("NEW SPAWN")
                    with open('current_focus/focus.json','w') as lastUpdate:
                        lastUpdateData['focusUp'] = True
                        lastUpdateData['influence'] = incursion['focus']['influence']
                        lastUpdateData['notifications']['influence_zero'] = False
                        lastUpdateData['notifications']['mobilized'] = False
                        lastUpdateData['notifications']['withdrawing'] = False
                        lastUpdateData['status'] = "established"
                        with open('current_focus/last.json','r') as lastData:
                            lD = json.load(lastData)
                        with open('current_focus/last.json','w') as lastData:
                            lD['id'] = lastData['id']
                            json.dump(lD,lastData)
                        lastUpdateData['id'] = str(incursion['static']['headquarters_system_id'])
                        print(lastUpdateData)
                        json.dump(lastUpdateData,lastUpdate)
                    embed_to_send = generateEmbed(focusInfo=incursion)
                    embed_to_send.set_footer(text=f"⏱ Last Updated: {getNowTS()}")
                    await message.edit(embed=embed_to_send)
                    await log_channel.send(f"New Focus Spawned\nUpdated Focus Embed\n⏱ | Last Updated: {getNowTS()}")
                    eMSG = await channel.send("@everyone")
                    await asyncio.sleep(10)
                    await eMSG.delete()

                # Check if Focus has Mobilized
                elif(incursion['focus']['state']=="mobilizing" and lastUpdateData['notifications']['mobilized']==False):
                    print('MOBILIZED')
                    with open('current_focus/focus.json','w') as lastUpdate:
                        lastUpdateData['status'] = "mobilized"
                        lastUpdateData['notifications']['mobilized'] = True
                        json.dump(lastUpdateData , lastUpdate)
                    
                    embed_to_send = generateEmbed(focusInfo=incursion)
                    embed_to_send.set_footer(text=f"⏱ Last Updated: {getNowTS()}")
                    await message.edit(embed=embed_to_send)
                    await log_channel.send(f"Focus has Mobilized\nUpdated Focus Embed\n⏱ | Last Updated: {getNowTS()}")


                # Check if focus has Withdrawn
                elif(incursion['focus']['state']=="withdrawing" and lastUpdateData['notifications']['withdrawing']==False):
                    print("Withdrawing")
                    with open('current_focus/focus.json','w') as lastUpdate:
                        lastUpdateData['status'] = "mobilized"
                        lastUpdateData['notifications']['withdrawing'] = True
                        json.dump(lastUpdateData , lastUpdate)
                    embed_to_send = generateEmbed(focusInfo=incursion)
                    embed_to_send.set_footer(text=f"⏱ Last Updated: {getNowTS()}")
                    await message.edit(embed=embed_to_send)
                    await log_channel.send(f"Focus has Mobilized\nUpdated Focus Embed\n⏱ | Last Updated: {getNowTS()}")


                # 0 Influence
                elif(lastUpdateData['influence']<1.0 and incursion['focus']['influence']==1.0 and lastUpdateData['notifications']['influence_zero']==False):
                    print("0 Influence")
                    with open('current_focus/focus.json','w') as lastUpdate:
                        lastUpdateData['notifications']['influence_zero'] = True
                        json.dump(lastUpdateData , lastUpdate)
                    # eMSG = await channel.send("@everyone")
                    # await asyncio.sleep(10)
                    # await eMSG.delete()
                    #TODO: Something IDK

                # Check for new spawn
                elif(lastUpdateData['focusUp']==False and incursion != None):
                    print("NEW SPAWN")
                    with open('current_focus/focus.json','w') as lastUpdate:
                        lastUpdateData['focusUp'] = True
                        lastUpdateData['influence'] = incursion['focus']['influence']
                        lastUpdateData['notifications']['influence_zero'] = False
                        lastUpdateData['notifications']['mobilized'] = False
                        lastUpdateData['notifications']['withdrawing'] = False
                        print(lastUpdateData)
                        json.dump(lastUpdateData,lastUpdate)
                    embed_to_send = generateEmbed(focusInfo=incursion)
                    embed_to_send.set_footer(text=f"⏱ Last Updated: {getNowTS()}")
                    await message.edit(embed=embed_to_send)
                    await log_channel.send(f"New Focus Spawned\nUpdated Focus Embed\n⏱ | Last Updated: {getNowTS()}")
                    eMSG = await channel.send("@everyone")
                    await asyncio.sleep(10)
                    await eMSG.delete()
                
                

                else:
                    print("REGULAR UPDATE")
                    embed_to_send = generateEmbed(focusInfo=incursion,filename="updatedInfluence.png")
                    embed_to_send.set_footer(text=f"⏱ | Last Updated: {getNowTS()}")
                    await message.edit(embed=embed_to_send)
                    await log_channel.send(f"REGULAR\nUpdated Focus Embed\n⏱ | Last Updated: {getNowTS()}")
                await asyncio.sleep(58)
            except Exception as e:
                print(e)

def setup(client):
    client.add_cog(Updater(client))