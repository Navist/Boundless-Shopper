import requests
import json
import time
import asyncio

requestsURL = 'https://api.boundlexx.app/api/v1/'
worldsData = {}

worldTest = {}
world = {}
colors = {}


with open('worlds/worldsData.json', 'r') as f:
    worldsData = json.load(f)

with open('worlds/colors.json', 'r') as f:
    colors = json.load(f)

async def runGets():
    task1 = asyncio.create_task(getWorld())

    await task1


def getColors():

    data = requests.get(requestsURL + 'colors?lang=english&limit=5000')
    JSON = json.loads(data.text)

    for x in JSON['results']:
        colors[x['game_id']] = x

    with open('worlds/colors.json', 'w') as f:
        json.dump(colors, f, indent=4, default=str)

def addColorIDs():
    for x in worldsData:
        p = worldsData.get(x)

        if len(p['colors']) == 0:
            continue
        for y in p['colors']:
            l = colors.get(str(y['color']['game_id']))
            y['color'].update({'name': l['localization'][0]['name']})
        print(f"{x} updated.")
    writeToFile('worlds/worldsData.json', worldsData)

def getWorldsWithColors():
    again = True
    
    while again == True:
        accum = []
        colorChoice = input("Which color are you looking for?\n")
        typeChoice = input("Which type of block are you looking for? Examples are: Brick, Rock, Trunk\n")
        for x in worldsData:
            p = worldsData.get(x)
            if len(p['colors']) == 0:
                continue

            for y in p['colors']:
                if colorChoice.lower() in y['color']['name'].lower() and typeChoice.lower() in y['item']['name'].lower():
                    if x in accum:
                        continue
                    else:
                        accum.append(f"""{x} - Tier: {p['tier']}
{y['item']['name']}
{y['color']['name']}
""")
            
        if len(accum) == 0:
            print("No results found.\n")
            again = keepTheWhileGoing()
        else:        
            print("\n".join(accum))
            again = keepTheWhileGoing()



def getWorldsOre():
    again = True
    while again == True:
        whichOre = input("Which ore would you like to find?\n").lower()
        whatPerc = input("Above what percentage?\n").lower()        
        maxTier = int(input("What max tier world would you like?\n"))
        accum = []
        for x in worldsData:
            p = worldsData.get(x)
            for y in p['resources']:
                # data = json.loads(requests.get(p['results']['world']['url']).text)['tier']
                try:
                    tier = int(p['tier'])
                except:
                    continue
                itemName = y['item']['name'].lower()
                percentage = y['percentage']
                avg = y['average_per_chunk']
                if whichOre.lower() in itemName and float(percentage) > float(whatPerc) and tier <= maxTier:
                    accum.append(f"""{x} - Tier: {tier}
        Item Name: {itemName}
        Percentage: {percentage}
        Average per Chunk: {avg}
    """)
        print("\n".join(accum))
        again = keepTheWhileGoing()
        

def keepTheWhileGoing():
        l = input("Would you like to go again? Yes or No?\n").lower()
        if l == 'yes':
            return True
        elif l == 'no':
            print("Exiting...")
            return False
        else:
            print("That wasn't an option. Exiting...")
            return False

async def getWorld():
    count = 0

    for x in worldsData:
        # if count == 300:
        #     break
        p = worldsData.get(x)
        if p == None:
            continue
        print(f"Pulling data for {x}")
        try:
            gameID = p['id']
        except:
            gameID = p['data']['id']
        try:
            if p['is_creative'] == True or p["is_locked"] == True:
                print(f"Skipping world {x}")
                continue
        except:
            if p['data']['is_creative'] == True or p['data']["is_locked"] == True:
                print(f"Skipping world {x}")            
        data = requests.get(requestsURL + f'worlds/{gameID}/polls')
        JSON = json.loads(data.text)

        getResources = requests.get(JSON['results'][0]['resources_url'])
        resources = json.loads(getResources.text)

        getColors = requests.get(requestsURL + f'worlds/{gameID}/block-colors')
        colors = json.loads(getColors.text)
        worldTest[x] = {
            'results': JSON['results'][0],
            'resources': resources['resources'],
            'colors': colors['block_colors']
        }
        
        count += 1

    writeToFile('worlds/worldsDataTest.json', worldTest)
    

def fixWorldData():
    worldTestData = {}
    with open('worlds/worldTest.json', 'r') as f:
        worldTestData = json.load(f)

    with open('worlds/worldTest.json', 'w') as f:
        json.dump(worldTestData, f, indent=4, default=4)

    for x in worldTestData:
        print()

        time.sleep(4)


def getWorlds():
    data = requests.get(requestsURL + 'worlds' + '?limit=5000&offset=0')
    JSON = json.loads(data.text)
    
    print(data)

    while JSON['next'] != None:
        for x in JSON['results']:
            worldData[x['text_name']] = x

        data = requests.get(JSON['next'])
        JSON = json.loads(data.text)
    else:
        print(data)
        for x in JSON['results']:
            worldsData[x['text_name']] = x
    writeToFile('worlds/worldsData.json', worldsData)



def writeToFile(filename, dataDict):
    with open(f"{filename}", 'w') as f:
        json.dump(dataDict, f, indent=4, default=str)


def searchWorlds(colorChoice, typeChoice):
    accum = {}
    for x in worldsData:
        p = worldsData.get(x)

        for y in p['colors']:
            if colorChoice in y['color']['name'] and typeChoice in y['item']['name']:
                accum[x] = {
                    'tier': x['tier']
                }


# fixWorldData()
# getWorlds()
# getWorld()
# getColors()
# addColorIDs()
# asyncio.run(runGets())

whichFeature = input("Which feature? Color or Ore?\n")

if whichFeature == "Color":
    getWorldsWithColors()
elif whichFeature == 'Ore':
    getWorldsOre()



