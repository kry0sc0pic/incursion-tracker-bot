from nextcord import Embed , Colour
hubInline = False
sysInline = True


def generateEmbed(focusInfo: dict , filename: str = "influence.png"):
    state = focusInfo['focus']['state']
    print(focusInfo)
    if state == "established":
        color = Colour.green()
        image = "https://i.imgur.com/7vBkyVW.png"
    elif state == "mobilizing":
        color = Colour.orange()
        image = "https://i.imgur.com/RZWxq0V.png"
    else:
        color = Colour.red()
        image = "https://i.imgur.com/xE6RsRH.png"

    if focusInfo['static']['is_island_spawn']:
        e = Embed(title=focusInfo["static"]["constellation_name"],description="**THIS IS AN ISLAND SPAWN,FOLLOW ISLAND GUIDE ISSUED BY THE COMMUNITY YOU FLY WITH**" , color=color)
    else:    
        e = Embed(title=focusInfo["static"]["constellation_name"],color=color)
    
    
    e.add_field(
        name="**System Information:**",
        value=f"‎‎\n**Headquarters: **‎‎{focusInfo['static']['headquarters_system_name']}\n**Vanguards: **{focusInfo['static']['vanguard_system_names']}\n**Assault: **{focusInfo['static']['assualt_system_names']}",
        inline=False,
    )
    e.add_field(
        name="‎‎",
        value=f"**Shortest: **[**{focusInfo['jumps']['shortest']}**](https://www.youtube.com/watch?v=dQw4w9WgXcQ)  Jumps\n**Safest: **[**{focusInfo['jumps']['secure']}**](https://www.youtube.com/watch?v=dQw4w9WgXcQ) Jumps‎‎‎"
    )

    e.add_field(name="**Trade Hubs:**", value="‎‎", inline=False)
    for hub in focusInfo["static"]["routes"].keys():
        e.add_field(
            name=hub.capitalize(),
            inline=hubInline,
            value=f'[**Safest**]({focusInfo["static"]["routes"][str(hub)]["secure"]["routeURL"]}) - **{focusInfo["static"]["routes"][str(hub)]["secure"]["jumps"]}** Jumps\n[**Shortest**]({focusInfo["static"]["routes"][str(hub)]["shortest"]["routeURL"]}) - **{focusInfo["static"]["routes"][str(hub)]["shortest"]["jumps"]}** Jumps',
        )
    # e.add_field(name="Ship Replacement Program",value="[Sign Up!](https://www.youtube.com/watch?v=dQw4w9WgXcQ)")
    e.set_thumbnail(url=focusInfo["static"]["faction_icon"])
    e.set_image(url=image)
    return e

def noFocusEmbed():
    e = Embed(
        title="No Focus",
        description="Waiting for new HS Focus to Spawn",
        colour=Colour.purple()
    )
    return e
