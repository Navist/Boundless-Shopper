import json
import time

shopStands = {}
shopRequests = {}
theseShops = {}

with open('shopStands/shopStands.json', 'r') as f:
    shopStands = json.load(f)

with open('shopRequests/shopRequests.json', 'r') as f:
    shopRequests = json.load(f)

def search():
    
    keepSearching = True
    while keepSearching == True:
        accum = []
        option = input("Which search feature? Shops or Requests.\n").lower()
        
        item = input("What item?\n")
        whatMin = float(input("What is your minimum quantity?\n"))
        p = None
        if option == 'shops':
            p = shopStands.get(item)
            price = float(input("Below what price?\n"))
            
            if p == None:
                print("That item isn't an item I can search for or it doesn't exist.")
            elif p != None:
                for x in p['results']:            
                    if float(x['item_count']) > whatMin and float(x['price']) < price:
                        theseShops[x['world']['display_name']] = {
                            'World': x['world']['display_name'],
                            'Shop Name': x['beacon_name'],
                            'Quantity': x['item_count'],
                            'Price': x['price']
                        }
                        accum.append(f"World: {x['world']['display_name']}\n    Shop Name: {x['beacon_name']}\n    Quantity Available: {x['item_count']}\n    Price Each: {x['price']}\n")

        elif option == 'requests':
            price = float(input("Above what price?\n"))
            # item = input("What item?\n")
            p = shopRequests.get(item)

            if p == None:
                print("That item isn't an item I can search for or it doesn't exist.")
            elif p != None:
                for x in p['results']:
                    if float(x['item_count']) > whatMin and float(x['price']) > price:
                        theseShops[x['world']['display_name']] = {
                            'World': x['world']['display_name'],
                            'Shop Name': x['beacon_name'],
                            'Quantity': x['item_count'],
                            'Price': x['price']
                        }
                        accum.append(f"World: {x['world']['display_name']}\n    Shop Name: {x['beacon_name']}\n    Quantity Available: {x['item_count']}\n    Price Each: {x['price']}\n")
        else:
            print("Invalid option choice. Try again.")
        if len(theseShops) == 0:
            print("No results found within your parameters.")
        else:
            print("\n".join(accum))
        with open('searchReturn.json', 'w') as f:
            json.dump(theseShops, f, indent=4, default=str)

        againOrNot = input("Would you like to perform another search? Yes or No?\n")
        if againOrNot.lower() == "yes":
            keepSearching = True
        elif againOrNot.lower() == "no":
            break
        else:
            print("Invalid option. Exiting...")
            break



search()