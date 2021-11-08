import requests
import json

incursionsEndpoint = "https://esi.evetech.net/latest/incursions"
routeBaseEndpoint = "https://esi.evetech.net/latest/route"

with open("prod_data/incursions_universe.json", "r") as incursionUniverse:
    possibleIncursionSpawns = json.load(incursionUniverse)

with open("current_focus/last.json") as lastFocus:
    lastFocusData = json.load(lastFocus)

def getHSIncursion():
    incursionList = requests.get(incursionsEndpoint).json()
    for focus in incursionList:
        constellationID = focus['constellation_id']
        try:
            spawnStaticData = possibleIncursionSpawns[str(constellationID)]
            # return spawnStaticData
            j = getJumps(lastFocusData['id'],spawnStaticData['headquarters_system_id'])
            return {
                "focus": focus,
                "static": spawnStaticData,
                "jumps": j
            }
        except Exception as e:
            pass
    #! Returning Hardcoded Data for testing
    # return None
    # return {
    #     "static": {
    #         "constellation_id": 20000496,
    #         "constellation_name": "Stadakorn",
    #         "faction": "Minmatar",
    #         "faction_id": "minmatar",
    #         "faction_icon": "https://wiki.eveuniversity.org/images/thumb/e/e6/Isis_minmatar.png/120px-Isis_minmatar.png",
    #         "is_island_spawn": True,
    #         "headquarters_system_name": "Egbonbet",
    #         "headquarters_system_id": 30003401,
    #         "staging_system_name": "Situner",
    #         "vanguard_system_names": "Agtver, Datulen, Erego, Meimungen, Totkubad",
    #         "assualt_system_names": "Evettullur, Hjortur, Tamekamur",
    #         "routes": {
    #             "jita": {
    #                 "secure": {
    #                     "jumps": 20,
    #                     "routeURL": "https://eve-gatecheck.space/eve/#Egbonbet:Jita:secure",
    #                 },
    #                 "shortest": {
    #                     "jumps": 19,
    #                     "routeURL": "https://eve-gatecheck.space/eve/#Egbonbet:Jita:shortest",
    #                 },
    #             },
    #             "dodixie": {
    #                 "secure": {
    #                     "jumps": 14,
    #                     "routeURL": "https://eve-gatecheck.space/eve/#Egbonbet:Dodixie:secure",
    #                 },
    #                 "shortest": {
    #                     "jumps": 14,
    #                     "routeURL": "https://eve-gatecheck.space/eve/#Egbonbet:Dodixie:shortest",
    #                 },
    #             },
    #             "amarr": {
    #                 "secure": {
    #                     "jumps": 27,
    #                     "routeURL": "https://eve-gatecheck.space/eve/#Egbonbet:Amarr:secure",
    #                 },
    #                 "shortest": {
    #                     "jumps": 18,
    #                     "routeURL": "https://eve-gatecheck.space/eve/#Egbonbet:Amarr:shortest",
    #                 },
    #             },
    #             "rens": {
    #                 "secure": {
    #                     "jumps": 7,
    #                     "routeURL": "https://eve-gatecheck.space/eve/#Egbonbet:Rens:secure",
    #                 },
    #                 "shortest": {
    #                     "jumps": 7,
    #                     "routeURL": "https://eve-gatecheck.space/eve/#Egbonbet:Rens:shortest",
    #                 },
    #             },
    #             "hek": {
    #                 "secure": {
    #                     "jumps": 10,
    #                     "routeURL": "https://eve-gatecheck.space/eve/#Egbonbet:Hek:secure",
    #                 },
    #                 "shortest": {
    #                     "jumps": 10,
    #                     "routeURL": "https://eve-gatecheck.space/eve/#Egbonbet:Hek:shortest",
    #                 },
    #             },
    #         },
    #     },
    #     "focus": {
    #         "constellation_id": 20000496,
    #         "faction_id": 500019,
    #         "has_boss": True,
    #         "infested_solar_systems": [
    #             30033410,
    #             30003400,
    #             30003401,
    #             30003402,
    #             30003403,
    #             30003404,
    #             30003405,
    #             30003406,
    #             30003407,
    #             30003408,
    #         ],
    #         "influence": 0.5,
    #         "staging_solar_system_id": 30003406,
    #         "state": "withdrawing",
    #         "type": "Incursion",
    #     },
    # }

def getJumps(originID , destinationID):
    routeURL = f"{routeBaseEndpoint}/{originID}/{destinationID}"
    shortestRoute = requests.get(routeURL , params={"flag": "shortest"}).json()
    secureRoute = requests.get(routeURL , params={"flag": "secure"}).json()
    if(type(shortestRoute)!=list and type(secureRoute)!=list):
        return {
            "shortest": 0,
            "secure": 0
        }
    else:
        # return len(route)
        return {
            "shortest": len(shortestRoute),
            "secure": len(secureRoute)
        }
    

