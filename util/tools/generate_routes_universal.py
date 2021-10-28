'''
SAMPLE
"20000510": {
        "constellation_id": 20000510,
        "constellation_name": "Zemont",
        "faction": "Amarr",
        "faction_id": "amarr",
        "faction_icon": "https://wiki.eveuniversity.org/images/thumb/2/29/Isis_amarr.png/120px-Isis_amarr.png",
        "is_island_spawn": true,
        "headquarters_system_name": "Nakri",
        "headquarters_system_id": 30003496,
        "staging_system_name": "Zaimeth",
        "vanguard_system_names": "Ekid, Raravoss, Sharhelund",
        "assualt_system_names": "Youl"
    }
'''

# Import Libraries
from selenium import webdriver
import json
import time


# Constants
routeTypes = ['secure','shortest']

# Load Static Data

with open('static_data/trade_hubs.json','r') as tradeHubs:
    tradeHubData = json.load(tradeHubs)

with open('static_data/incursions_universe.json','r') as incursionUniverse:
    incursionUniverseData = json.load(incursionUniverse)

def run():
    scraper = webdriver.Chrome(executable_path='driver/chromedriver.exe')
    tradeHubs = tradeHubData.keys()
    constellationIDs = incursionUniverseData.keys()

    with open('static_data/routes_universe.json','w') as routes:
        routes.write('')
    routesData = {}
    i = 1
    maxCount = len(constellationIDs)
    for constellationID in constellationIDs:
        hqSystemName = incursionUniverseData[f"{constellationID}"]["headquarters_system_name"]
        hqSystemID = incursionUniverseData[f"{constellationID}"]["headquarters_system_id"]
        
        routes = {
            
        }
        if(hqSystemName=='unknown'):
            routes = {
                "sys": "un"
            }
        else:
            for hub in tradeHubs:
                secureRouteURL = f"https://eve-gatecheck.space/eve/#{hqSystemName}:{hub.capitalize()}:{routeTypes[0]}"
                shortestRouteURL = f"https://eve-gatecheck.space/eve/#{hqSystemName}:{hub.capitalize()}:{routeTypes[1]}"
                scraper.get(secureRouteURL)
                time.sleep(2)
                secureJumps = int(scraper.find_element_by_xpath('//*[@id="result"]/strong/em').text.split(' ')[-2].strip())
                # shortestRadio = scraper.find_element_by_xpath('//*[@id="shortest"]')
                # checkButton = scraper.find_element_by_xpath('//*[@id="check"]')
                # shortestRadio.click()
                # checkButton.click()
                scraper.back()
                scraper.get(shortestRouteURL)
                time.sleep(2)
                shortestJumps = int(scraper.find_element_by_xpath('//*[@id="result"]/strong/em').text.split(' ')[-2].strip())
                scraper.back()
                # scraper.get(shortestRouteURL)
                # time.sleep(2)
                # shortestJumps = int(scraper.find_element_by_xpath('//*[@id="result"]/strong/em').text.split(' ')[-2].strip())
                # Scrape Data
                routes[hub.lower()] = {}
                routes[hub.lower()]["secure"] = {
                    "jumps": secureJumps,
                    "routeURL": secureRouteURL
                }
                routes[hub.lower()]["shortest"] = {
                    "jumps": shortestJumps,
                    "routeURL": shortestRouteURL
                }
            # print(routes)
        routesData[hqSystemID] = routes
        print(f"[{i}/98]")
        i+=1
        # with open('static_data/incursions_universe.json','w') as incursionUniverse:
        #     incursionUniverseData[constellationID]['routes'] = routes
        #     json.dump(incursionUniverseData , incursionUniverse)
    with open('static_data/routes_universe.json','w') as routesUniverse:
        json.dump(routesData,routesUniverse)

#TODO: This
if __name__ == '__main__':
    run()