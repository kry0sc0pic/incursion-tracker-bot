# Import Libraries
from selenium import webdriver
import json
import requests
import time

# Load Static Data Needed

with open('static_data/faction_logo.json','r') as factionLogos:
    factionLogoData = json.load(factionLogos)


# Constants
incursionConstellationCount = 98
possibleConstellationsList = 'https://wiki.eveuniversity.org/Constellation_layouts_for_Incursions'
esiSearchEndpoint = 'https://esi.evetech.net/latest/universe/ids'
headers = {"Content-Type": "text/plain"}
incursionSpawnData = {}
# Main Run Function
def run():
    # Clear out old data
    with open('static_data/incursions_universe.json','w') as incursionsdata:
        incursionsdata.write('')

    # Open Browser    
    scraper = webdriver.Chrome(executable_path='driver/chromedriver.exe')
    
    # Open Ecve Uni Page
    scraper.get(possibleConstellationsList)
    time.sleep(3)
    scraper.execute_script('window.scrollBy(0,document.body.scrollHeight)') # Scroll to Bottom to make sure full page load
    
    # Iterate through every possible spawn to generate data
    for i in range(incursionConstellationCount):
        i+=1
        try:
            # print(scraper.find_element_by_xpath(f'/html/body/div[4]/div[2]/div[4]/div/table[3]/tbody/tr[{i}]/td[1]/a[1]/img').get_attribute("alt"))
            incursionFocusFactionID = scraper.find_element_by_xpath(f'/html/body/div[4]/div[2]/div[4]/div/table[3]/tbody/tr[{i}]/td[1]/a[1]/img').get_attribute("alt").split(' ')[2].strip()      
            
        except Exception:
            incursionFocusFactionID = scraper.find_element_by_xpath(f'/html/body/div[4]/div[2]/div[4]/div/table[3]/tbody/tr[{i}]/td[1]/a[1]/img').get_attribute("alt")
            if(str(incursionFocusFactionID).split(' ')[0].lower().strip() == 'khanid'):
                incursionFocusFactionID = 'khanid'
            else:
                incursionFocusFactionID = 'ammatar'
        incursionFocusIslandSpawn = False
        incursionConstellationName = scraper.find_element_by_xpath(f'/html/body/div[4]/div[2]/div[4]/div/table[3]/tbody/tr[{i}]/td[1]').text.strip()
        incursionStagingSystemName = scraper.find_element_by_xpath(f'/html/body/div[4]/div[2]/div[4]/div/table[3]/tbody/tr[{i}]/td[2]').text.strip()
        incursionVanguardSystemNames = scraper.find_element_by_xpath(f'/html/body/div[4]/div[2]/div[4]/div/table[3]/tbody/tr[{i}]/td[3]').text.strip()
        incursionAssualtSystemNames =  scraper.find_element_by_xpath(f'/html/body/div[4]/div[2]/div[4]/div/table[3]/tbody/tr[{i}]/td[4]').text.strip()
        
        # No 70 is cringe (HQ maybe be Silen)
        try:
            incursionHeadquartersSystemName = scraper.find_element_by_xpath(f'/html/body/div[4]/div[2]/div[4]/div/table[3]/tbody/tr[{i}]/td[5]').text.strip()
        except Exception:
            incursionHeadquartersSystemName = 'unknown'
        
        # Check Island Spawn
        try:
            _ = scraper.find_element_by_xpath(f'/html/body/div[4]/div[2]/div[4]/div/table[3]/tbody/tr[{i}]/td[1]/a[3]')
            incursionFocusIslandSpawn = True
        except:
            incursionFocusIslandSpawn = False

        
        # Get System and Constellation IDs
        incursionConstellationID = requests.post(esiSearchEndpoint,headers=headers,data=f'["{incursionConstellationName}"]').json()["constellations"][0]['id']
        if(incursionHeadquartersSystemName!='unknown'):
            incursionHeadquartersSystemID = requests.post(esiSearchEndpoint,headers=headers,data=f'["{incursionHeadquartersSystemName}"]').json()["systems"][0]['id']
        else:
            incursionHeadquartersSystemID = 0
        # Add an entry in the database
        incursionSpawnData[incursionConstellationID] = {
            "constellation_id": incursionConstellationID,
            "constellation_name": incursionConstellationName,
            "faction": incursionFocusFactionID.capitalize(),
            "faction_id": incursionFocusFactionID.lower(),
            "faction_icon": factionLogoData[incursionFocusFactionID.lower()],
            "is_island_spawn": incursionFocusIslandSpawn,
            "headquarters_system_name": incursionHeadquartersSystemName,
            "headquarters_system_id": incursionHeadquartersSystemID,
            "staging_system_name": incursionStagingSystemName,
            "vanguard_system_names": incursionVanguardSystemNames,
            "assualt_system_names": incursionAssualtSystemNames,
        }
        
        print(f"[{i}/98] {incursionConstellationName} - HQ: {incursionHeadquartersSystemName}  -  [{incursionFocusFactionID.capitalize()}] - [Island {incursionFocusIslandSpawn}]")
    with open('static_data/incursions_universe.json','w') as incursionData:
        json.dump(incursionSpawnData , incursionData)      
    print('Data Saved!')
        
if __name__ == '__main__':
    run()