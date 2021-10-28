from nextcord import Activity, ActivityType , Status
import json
from nextcord.embeds import Embed
from nextcord.ext import commands

#* Loading Bot Configuration
with open('bot_config/config.json','r') as configFile:
    config = json.load(configFile)

#* Create Discord Client
bot = commands.Bot(command_prefix='?',help_command=None)
statusActivity = Activity(type=ActivityType.watching , name=config['status'])

#* Startup Tasks
@bot.event
async def on_ready():
    print("Bot Is Up!")
    print(f"{bot.user.name}#{bot.user.discriminator}")
    await bot.change_presence(activity=statusActivity , status=Status.idle)

@bot.command()
async def reset(ctx):
    m1 = await ctx.send("Unloading Modules")
    for m in config['modules']:
        bot.unload_extension(m)
    m2 = await ctx.send("Loading Modules")
    for m in config['modules']:
        bot.load_extension(m)
    await m1.delete()
    await m2.delete()
# Load Modules
for m in config['modules']:
    bot.load_extension(m)
    
#? Run the Bot
bot.run(config['token'])
