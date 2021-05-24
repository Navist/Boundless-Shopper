import requests
import json
import time
import asyncio

requestsURL = 'https://api.boundlexx.app/api/v1/'
dataRetrieved = 'All data retreived for request baskets on world '

results = {}
ignoreList = {}
blockNameIgnoreList = []
blockIDIgnoreList = []


with open('blockIgnoreList.json', 'r') as f:
    ignoreList = json.load(f)

blockNameIgnoreList = ignoreList['item']
blockIDIgnoreList = ignoreList['id']

def getWorldsData():
    data = requests.get(requestsURL + 'worlds')
    JSON = json.loads(data.text)

    writeToFile('worlds/worldsData', JSON)

    return JSON

async def getShopStands():
    global results
    with open('items/itemsData.json', 'r') as f:
        results = json.load(f)

    task1 = asyncio.create_task(getShopStandData())
    task2 = asyncio.create_task(getShopRequestData())

    await task1
    await task2

async def getShopRequests():
    global results

    task2 = asyncio.create_task(getShopRequestData())

    await task2


async def getWorldDataAsync():
    task1 = asyncio.create_task(getItemsData())

    await task1

def getItemName(localization):
    itemName = ''
    for y in localization:
        if y['lang'] == 'english':
            itemName = y['name']
            break
    return itemName

async def getShopStandData():
    JSON = {}
    for x in results:
        p = results.get(x)
        gameID = p['game_id']
        if gameID in blockIDIgnoreList:
            print(f"Skipping {x}")
            continue
        data = requests.get(requestsURL + f'items/{gameID}/shop-stands')
        
        itemName = p['localization'][0]['name']
        if itemName == 'skip':
            continue
        elif p['has_colors'] == True:
            continue
        print(f"ShopStand: {data}\n{itemName}\n")
        try:
            JSON[itemName] = json.loads(data.text)
        except:
            continue
        
    getAllJSON('shopStands/shopStands', JSON)
    

async def getShopRequestData():
    JSON = {}
    for x in results:
        p = results.get(x)
        gameID = p['game_id']
        if gameID in blockIDIgnoreList:
            print(f"Skipping {x}")
            continue        
        data = requests.get(requestsURL + f'items/{gameID}/request-baskets')
        
        itemName = p['localization'][0]['name']
        if itemName == 'skip':
            continue
        elif p['has_colors'] == True:
            continue
        print(f"ShopRequest: {data}\n{itemName}\n")
        try:
            JSON[itemName] = json.loads(data.text)
        except:
            continue
            # count += 1

    getAllJSON('shopRequests/shopRequests', JSON)


async def getItemsData():
    data = requests.get(requestsURL + 'items/?lang=english')
    JSON = json.loads(data.text)
    count = 0

    while JSON['next'] != None:
        print(f'{JSON["next"]}\n{data}')
        for x in JSON['results']:
            if x['game_id'] in blockIDIgnoreList:
                print(f"Skipping {JSON['results'][0]['localization'][0]['name']}")
                continue            
            # if x['has_colors'] == True and x['is_block'] == True:
            #     continue
            itemName = x['localization'][0]['name']
            results[itemName] = x
        data = requests.get(JSON['next'])
        JSON = json.loads(data.text)
        count += 1
            
    else:
        for x in JSON['results']:
            itemName = x['localization'][0]['name']
            results[itemName] = x
        print(data)
    with open('items/itemsData.json', 'w') as f:
        json.dump(results, f, indent=4, default=str)me
            

def getItemData():
    data = requests.get(requestsURL + 'items/1')
    JSON = json.loads(data.text)
    writeToFile("itemData.json", JSON)


def getMetals():
    data = requests.get(requestsURL + 'metals')
    JSON = json.loads(data.text)

    writeToFile("metalsData.json", JSON)


def getWorldShopStands(id):
    data = requests.get(requestsURL + f'worlds/{id}/shop-stands')
    JSON = json.loads(data.text)

    writeToFile("worldShopStands.json", JSON)


def getWorldRequestBaskets(id):
    data = requests.get(requestsURL + f'worlds/{id}/request-baskets')
    JSON = json.loads(data.text)

    getAllJSON('requestBaskets/worldRequestBaskets', JSON)


def getAllJSON(location, JSON):
    partPath = location.split('/')[1]

    writeToFile(f"{location}.json", JSON)
    print(f"All JSON data saved for {partPath}")


def writeToFile(filename, dataDict):
    with open(f"{filename}", 'w') as f:
        json.dump(dataDict, f, indent=4, default=str)


## Generic Data
# getItemsData()
# getItemData()
# getMetals()

#main
asyncio.run(getShopStands())
# asyncio.run(getShopRequests())
# asyncio.run(getWorldDataAsync())

## Stands
# asyncio.run(getShopStandData())
# getWorldShopStands()

## Requests
# asyncio.run(getShopRequestData())
# getWorldRequestBaskets()









