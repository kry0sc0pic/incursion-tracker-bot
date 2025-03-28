#* Import modules
from nextcord import Activity, ActivityType , Status
import json
from nextcord.ext import commands
import json
from nextcord.ext import commands,tasks
from util.focus import generateEmbed,noFocusEmbed
from util.esi import getHSIncursion
from util.tsparser import getNowTS
import asyncio
import pymongo

#* Loading Bot Configuration
with open('config/bot.json','r') as configFile:
    config = json.load(configFile)

#* Create Discord Client
bot = commands.Bot(command_prefix='?',help_command=None)
statusActivity = Activity(type=ActivityType.watching , name=config['status'])
@tasks.loop(minutes=20)
async def liveFocusStatus():
    with open('config/guild.json','r') as conf:
        config = json.load(conf)
    log_channel = bot.get_channel(config['log_channel'])
    channelID = config['channel_id']
    messageID = config['message_id']
    channel = bot.get_channel(channelID)
    message = await channel.fetch_message(messageID)
    while True:
        try:
            doc = pymongo.MongoClient("mongodb+srv://vargur:inrustwetrust@cluster0.g0cm2.mongodb.net/incursions?retryWrites=true&w=majority")['incursions']['focus_data'].find_one()
            lastUpdateData = {
                "focusUp":doc['focusUp'],
                "status":doc['status'],
                "influence":doc['influence'],
                "id": doc['id'],
                "last_id": doc['last_id'],
                "notifications": {
                    "influence_zero": doc['influence_zero'],
                    "mobilized": doc['mobilized'],
                    "withdrawing": doc['withdrawing'],
                }
                }
            incursion = getHSIncursion() # Get Incursion



            # Check if focus has gone down
            if(lastUpdateData["focusUp"]==True and incursion==None):
                print("Focus Down , New Focus in 2-3 days?")
                doc['focusUp'] = False
                e = noFocusEmbed()
                
                pymongo.MongoClient("mongodb+srv://vargur:inrustwetrust@cluster0.g0cm2.mongodb.net/incursions?retryWrites=true&w=majority")['incursions']['focus_data'].update_one({'_id': 'data'},{"$set":doc})
                try:
                    await message.edit(embed=e)
                except Exception as e:
                    print("error: ",e)
                await log_channel.send(f"Focus is Down\nUpdated Focus Embed\n⏱ | Last Updated: {getNowTS()}") 


            # If no new focus has spawned
            elif(lastUpdateData['focusUp']==False and incursion == None):
                print("No Focus")
                e = noFocusEmbed()
                await message.edit(embed=e)
                await log_channel.send(f"No Focus Spawned\nUpdated Focus Embed\n⏱ | Last Updated: {getNowTS()}")
            
            # If new focus has spawned
            elif(lastUpdateData['focusUp']==False and incursion != None):
                print("NEW SPAWN")
                print(f"LAST UPDATE: \n {lastUpdateData}")
                print("----------------------------------------------------")
                print(f"INCURSION DATA: \n {incursion}")
                lID = doc['id']
                doc['focusUp'] = True
                doc['influence'] = incursion['focus']['influence']
                doc['influence_zero'] = False
                doc['mobilized'] = False
                doc['withdrawing'] = False
                doc['status'] = incursion['focus']['state']
                doc['last_id'] = lID
                doc['id'] = incursion['static']['headquarters_system_id']
                
                pymongo.MongoClient("mongodb+srv://vargur:inrustwetrust@cluster0.g0cm2.mongodb.net/incursions?retryWrites=true&w=majority")['incursions']['focus_data'].update_one({'_id': 'data'},{"$set":doc})
                embed_to_send = generateEmbed(focusInfo=incursion)
                embed_to_send.set_footer(text=f"⏱ Last Updated: {getNowTS()}")
                await message.edit(embed=embed_to_send)
                await log_channel.send(f"New Focus Spawned\nUpdated Focus Embed\n⏱ | Last Updated: {getNowTS()}")
                # eMSG = await channel.send("@everyone")
                await asyncio.sleep(10)
                # await eMSG.delete()

            # Check if Focus has Mobilized
            elif(incursion['focus']['state']=="mobilizing" and lastUpdateData['notifications']['mobilized']==False):
                print('MOBILIZED')
                doc['status'] = "mobilizing"
                doc['mobilized'] = True
                pymongo.MongoClient("mongodb+srv://vargur:inrustwetrust@cluster0.g0cm2.mongodb.net/incursions?retryWrites=true&w=majority")['incursions']['focus_data'].update_one({'_id': 'data'},{'$set': doc})
                embed_to_send = generateEmbed(focusInfo=incursion)
                embed_to_send.set_footer(text=f"⏱ Last Updated: {getNowTS()}")
                await message.edit(embed=embed_to_send)
                await log_channel.send(f"Focus has Mobilized\nUpdated Focus Embed\n⏱ | Last Updated: {getNowTS()}")


            # Check if focus has Withdrawn
            elif(incursion['focus']['state']=="withdrawing" and lastUpdateData['notifications']['withdrawing']==False):
                print("Withdrawing")
                doc['status'] = "withdrawing"
                doc['withdrawing'] = True
                pymongo.MongoClient("mongodb+srv://vargur:inrustwetrust@cluster0.g0cm2.mongodb.net/incursions?retryWrites=true&w=majority")['incursions']['focus_data'].update_one({'_id': 'data'},{'$set': doc})
                embed_to_send = generateEmbed(focusInfo=incursion)
                embed_to_send.set_footer(text=f"⏱ Last Updated: {getNowTS()}")
                await log_channel.send(f"Focus has Withdrawn\nUpdated Focus Embed\n⏱ | Last Updated: {getNowTS()}")
                await message.edit(embed=embed_to_send)
                


            # 0 Influence
            elif(lastUpdateData['influence']<1.0 and incursion['focus']['influence']==1.0 and lastUpdateData['notifications']['influence_zero']==False):
                print("0 Influence")
                doc['influence_zero'] = True
                pymongo.MongoClient("mongodb+srv://vargur:inrustwetrust@cluster0.g0cm2.mongodb.net/incursions?retryWrites=true&w=majority")['incursions']['focus_data'].update_one({'_id': 'data'},{'$set': doc})

        
            
            

            else:
                print("REGULAR UPDATE")
                embed_to_send = generateEmbed(focusInfo=incursion,filename="updatedInfluence.png")
                embed_to_send.set_footer(text=f"⏱ | Last Updated: {getNowTS()}")
                await message.edit(embed=embed_to_send)
                await log_channel.send(f"REGULAR\nUpdated Focus Embed\n⏱ | Last Updated: {getNowTS()}")
            await asyncio.sleep((60*10)-2)
        except Exception as e:
            print(e)


#* Control Commands for Update Task
@commands.guild_only()
# @commands.has_any_role(895714070815211581,826051937400782879)
@commands.command(aliases=['stop'])
async def pause(self,ctx):
    try:
        liveFocusStatus.stop()
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

#* Bot Ready Callback
@bot.event
async def on_ready():
    print("Bot Is Up!")
    print(f"{bot.user.name}#{bot.user.discriminator}")
    await bot.change_presence(activity=statusActivity , status=Status.idle)
    print("Starting Updater task")
    liveFocusStatus.start()


#* Load Modules
for m in config['modules']:
    bot.load_extension(m)
    
#* Run the Bot
bot.run(config['token'])
