import json
import requests

def getCity(cityRkstCode, serviceMode):
    headers = {'authority': 'api.maersk.com','accept': 'application/json, text/plain, */*','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36','origin': 'https://www.maersk.com','sec-fetch-site': 'same-site','sec-fetch-mode': 'cors','sec-fetch-dest': 'empty','referer': 'https://www.maersk.com/','accept-language': 'en-US,en;q=0.9'}
    try:
        data = requests.get(f"https://api.maersk.com/locations/?brand=maeu&type=city&pageSize=50&maerskRkstCode={cityRkstCode}")
        data = data.json()
        return {
            "maerskGeoId": data["maerskGeoLocationId"],
            "countryCode": data["countryCode"],
            "maerskServiceMode": serviceMode,
            "maerskRkstCode": data["maerskRkstCode"]
        }

    except Exception as e:
        print("Cannot get city details")

def getCommodity(commodityName, isDangerous = False):
    data = []
    with open("commodity.json") as f:
        data = json.load(f)

    for d in data:
        if d["commodityName"] == commodityName:
            return {
                "id": d["commodityCode"],
                "name": d["commodityName"],
                "isDangerous": isDangerous,
                "dangerousDetails": []
            }
    return {}            

def getContainer(containerName, weight, quantity = 1, isShipperOwnedContainer = False, isNonOperatingReefer = False):
    data = []
    with open("container.json") as f:
        data = json.load(f)

    for d in data:
        if d["sizeTypeDisplayName"] == containerName:
            return {
                "isoCode": d["isoContainerSizeTypeCd"],
                "name": d["sizeTypeDisplayName"],
                "size": d["sizeCd"],
                "type": d["typeCd"],
                "weight": weight,
                "quantity": quantity,
                "isReefer": d["reeferFlag"],
                "isNonOperatingReefer": isNonOperatingReefer,
                "isShipperOwnedContainer": isShipperOwnedContainer
            }
    return {}            

# print(getCommodity("Albacore, frozen, fish", False))
# print(getContainer("40 Dry Standard", 18000, 1, False, False))