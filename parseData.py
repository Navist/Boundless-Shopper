import json
import os
import time
from operator import itemgetter

items = []
ignoreList = {}
blockNameIgnoreList = []
blackIDIgnoreList = []
shopStands = {}
shopRequests = {}
requestBaskets = {}

count = 0

writeIt = ['items', 'shopStands', 'shopRequests']

curDir = r'E:\Desktop Stuff\Program Stuff\BoundlessMarketSearch'

with open('blockIgnoreList.json', 'r') as f:
    ignoreList = json.load(f)

blockNameIgnoreList = ignoreList['item']
blockIDIgnoreList = ignoreList['id']

l = os.scandir(curDir)


with open('shopStands/shopStands.json', 'r') as f:
    shopStands = json.load(f)

with open('shopRequests/shopRequests.json', 'r') as f:
    shopRequests = json.load(f)


#Convert prices to ints

for x in writeIt:
    if x == 'items':
        continue
    m = eval(x)
    for y in m:
        getItem = m.get(y)
        if len(getItem['results']) == 0:
            continue
        else:
            for p in getItem['results']:
                p['price'] = float(p['price'])

for x in writeIt:
    m = eval(x)
    for y in m:
        getItem = m.get(y)
        try:
            sorted(getItem['results'], key=itemgetter('price'), reverse=True)
        except KeyError:
            continue

def comparePricing():
    bestPrices = {}
    bestShopStand = ''
    quantityMin = float(input("What is your minimum amount? Must be number!\n"))
    priceMin = int(input("What is your minimum margin? Must be number!\n"))
    quantityMinreached = False
    buyFromThese = {}

    for x in shopRequests:
        buyersName = ''
        shopStandsItem = shopStands.get(x)
        bestPriceShop = {}
        if len(shopStandsItem['results']) == 0:
            continue
        for p in shopStandsItem['results']:
            if float(p['item_count']) > quantityMin:
                bestShopStand = p['price']
                bestPriceShop.update(p)
                quantityMinreached = True
                break
        
        if quantityMinreached == False:
            continue
        shopRequestsItem = shopRequests.get(x)
        for y in shopRequestsItem['results']:
            if y['item_count'] < quantityMin:
                continue
            if len(bestPriceShop) == 0:
                continue
            if y['price'] > bestShopStand:
                yPrice = y['price']
                bestPricePrice = bestPriceShop['price']
                if (yPrice - bestPricePrice) < priceMin:
                    continue
                getShop = bestPrices.get(y['beacon_name'])
                if getShop == None:
                    bestPrices[y['beacon_name']] = {
                        # x = item name
                        x: [
                            f"World: {y['world']['display_name']}",
                            f"Price: {y['price']}",
                            f"Quantity: {y['item_count']}",
                            {
                                'Shop Name': bestPriceShop['beacon_text_name'],
                                'World': bestPriceShop['world']['display_name'],
                                'Quantity': bestPriceShop['item_count'],
                                'Price': bestPriceShop['price']
                            }
                        ]
                    }
                else:
                    if len(bestPriceShop) == 0:
                        pass
                    else:
                        getShop[x] = [
                                f"World: {y['world']['display_name']}",
                                f"Price: {y['price']}",
                                f"Quantity: {y['item_count']}",
                                {
                                    'Shop Name': bestPriceShop['beacon_text_name'],
                                    'World': bestPriceShop['world']['display_name'],
                                    'Quantity': bestPriceShop['item_count'],
                                    'Price': bestPriceShop['price']
                                }
                            ]

                getShopMasterList = buyFromThese.get(bestPriceShop['world']['display_name'])
                if getShopMasterList == None:
                    buyFromThese[bestPriceShop['world']['display_name']] = {
                        bestPriceShop['beacon_name']: {
                            x: {
                                'MaxToBuy': y['item_count'],
                                'AvailableToBuy': bestPriceShop['item_count'],                                
                                'Buy/Sell': f"{bestPriceShop['price']}/{y['price']}",
                                'ProfitMargin': (y['price'] - bestPriceShop['price']),
                                'Sell To': y['beacon_name'],
                                'On World': y['world']['display_name']
                            }
                        }
                    }
                else:
                    k = getShopMasterList.get(bestPriceShop['beacon_name'])
                    profitMargin = y['price'] - bestPriceShop['price']

                    if k != None:
                        k[x] = {
                                'MaxToBuy': y['item_count'],
                                'AvailableToBuy': bestPriceShop['item_count'],
                                'Buy/Sell': f"{bestPriceShop['price']}/{y['price']}",
                                'ProfitMargin': profitMargin,
                                'Sell To': y['beacon_name'],
                                'On World': y['world']['display_name']
                        }
                    else:
                        getShopMasterList = {
                            x: {
                                'MaxToBuy': y['item_count'],
                                'AvailableToBuy': bestPriceShop['item_count'],
                                'Buy/Sell': f"{bestPriceShop['price']}/{y['price']}",
                                'ProfitMargin': profitMargin,
                                'Sell To': y['beacon_name'],
                                'On World': y['world']['display_name']
                            }
                        }

    with open('bestPrices.json','w') as f:
        json.dump(bestPrices, f, indent=4, default=str)

    with open('bestRoute.json', 'w') as f:
        json.dump(buyFromThese, f, indent=4, default=str)

comparePricing()