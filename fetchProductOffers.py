import requests
from unittest import TestCase
from time import sleep
from copy import deepcopy
from random import uniform

from util import getCommodity, getContainer, getCity

assertListEqual = TestCase().assertListEqual
assertDictEqual = TestCase().assertDictEqual

def indexByData(offers):
    offersIndexedByDate = {}
    try:
        for offer in offers:
            # Offer with no price
            if offer.get("offerFilteredReasons", None) and offer["offerFilteredReasons"].get("departureDate", None):
                if offersIndexedByDate.get(offer["offerFilteredReasons"]["departureDate"], None) is None:
                    date = offer["offerFilteredReasons"]["departureDate"]
                    offersIndexedByDate[date] = {}
            elif offer["routeScheduleWithPrices"]: # Offer with price
                pricesOffered = []
                date = offer["routeScheduleWithPrices"]["routeScheduleFull"]["fromLocation"]["date"]
                prices = offer["routeScheduleWithPrices"]["price"]["prices_per_container"]
                for p in prices:
                    if p["bas"]["ratetypecode"] == "Freight":
                        price = {}
                        price[p["bas"]["chargedescription"]] = p["bas"]["amount"]
                        price["currency"] = p["bas"]["currency"]
                        pricesOffered.append(price)

                    if len(p["surcharges_per_container"]) > 0:
                        for surPrice in p["surcharges_per_container"]:
                            if surPrice["ratetypecode"] == "Freight":
                                price = {}
                                price[surPrice["chargedescription"]] = surPrice["amount"]
                                price["currency"] = surPrice["currency"]
                                pricesOffered.append(price)
                    pricesOffered.append({"total": offer["routeScheduleWithPrices"]["price"]["total"], "currency": offer["routeScheduleWithPrices"]["price"]["totalPriceCurrency"]})
                offersIndexedByDate[date] = pricesOffered
    except Exception as e:
        print("#" * 10, "Error in indexByData", "#" * 10)

    return offersIndexedByDate

def fetchProducts(token, data):
    offered = []
    weekOffset = 0

    url = 'https://api.maersk.com/productoffer/v2/productoffers'
    headers = {'authority': 'api.maersk.com','pragma': 'no-cache','cache-control': 'no-cache','authorization': token,'content-type': 'application/json','accept': 'application/json, text/plain, */*','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36','origin': 'https://www.maersk.com','sec-fetch-site': 'same-site','sec-fetch-mode': 'cors','sec-fetch-dest': 'empty','referer': 'https://www.maersk.com/','accept-language': 'en-US,en;q=0.9'}
    
    while 1:
        try:
            print(weekOffset)
            data["weekOffset"] = weekOffset
            response = requests.post(url, headers = headers, json = data)
            results = response.json()
            weekOffset = results.get("nextOffsetWeek", None)
            if weekOffset is None:
                offers = results.get("offers", None)
                if offers and (type(offers) == type([]) and len(offers) > 0):
                    offered.extend(offers)
                break
            else:
                offers = results.get("offers", None)
                if offers and (type(offers) == type([]) and len(offers) > 0):
                    offered.extend(offers)
        except Exception as e:
            print("#" * 10, "Error in fetchProducts", "#" * 10)
            break

    if len(offered) > 0:
        return offered
    return []


def run(token, _from, _to, commodity, container):
    ########################################
    # Request data
    token = "Bearer eyJ0eXAiOiJKV1QiLCJraWQiOiJQbStTdGZEejRmY0tzdk5iUTBscGNETWlyNEk9IiwiYWxnIjoiUlMyNTYifQ.eyJhdF9oYXNoIjoiWnVsQ3ZOc3ZNR2F2UG9lb2daU3VjUSIsInN1YiI6ImJob29taV9zaGlwcGluZyIsImZpcnN0bmFtZSI6Ikt1c2giLCJhdWRpdFRyYWNraW5nSWQiOiIyYTBhMjlmMy04OGY5LTRlMmItODY4My00NmUyN2Q4MWQwOGItMTkyMzc3OSIsInJvbGVzIjpbIlBheW1lbnRzIiwiSW52b2ljZXMiLCJCb29raW5nIiwiQ29udHJhY3RSYXRlIiwiV0JPTEFwcHJvdmVyIiwiRG9jdW1lbnRhdGlvbiIsIkJhc2ljQ3VzdG9tZXIiXSwiaXNzIjoiaHR0cHM6Ly9pYW0ubWFlcnNrLmNvbS9hY20vb2F1dGgyL21hdSIsInRva2VuTmFtZSI6ImlkX3Rva2VuIiwib2ZmaWNlIjoiS2FuZGxhIC0gSU4iLCJhY3IiOiIwIiwiYXpwIjoiYmNhMDAxIiwiYXV0aF90aW1lIjoxNjIyOTc1NTM3LCJwZXJzb25pZCI6IjQxMDAyNDI5MjA1IiwiZXhwIjoxNjIyOTgyNzQxLCJjdXN0b21lcl9jb2RlIjoiNDEwMDI0MjkwOTQiLCJpYXQiOjE2MjI5NzU1NDEsImVtYWlsIjoiYmhvb21pc2hpcHBpbmdAZ21haWwuY29tIiwibm9uY2UiOiJVamxqVHFQU1hzb3ozY25pSVJCWSIsImxhc3RuYW1lIjoiVGhhY2tlciIsImF1ZCI6ImJjYTAwMSIsImNfaGFzaCI6ImJrN2ZXaXdzVkw1SVE1SzlFM2ljZ1EiLCJjYXJyaWVyIjoiTUFFVSIsInJlYWxtIjoiL21hdSIsInRva2VuVHlwZSI6IkpXVFRva2VuIiwidXNlcm5hbWUiOiJiaG9vbWlfc2hpcHBpbmcifQ.CIr94Y5cyjAA0-JZxN7M9nNIMw--Jgg6FEmJTmHnb6qA8qYXsdkkjkEGCZ8UyAnifWXMKrsuMKFdUXpMIccdEabwTp8_cihWipn5bFrPJl-tnWPsUG1xEHP5qjAMxmHqSygQpYKFvXXmfyywxdZ8OixiuZNybNbmOviUFb0HzRI8MbAocWXL0jIMN-LIXBHArMrG10Vb-GlHIHKN5B0oXESQiAPM7buDQk8ulmR72O9mzgZDlT8J_I7cx2z9zbov02WI-tWu7NarQFSY-mTllJQaDfvqI72J-5LF5jvJSgx3sh99Z72qe232E_nNHZzL36o19pjSBOa03Eyagc4MGA"
    _from = getCity(, "CY")
    _to = getCity(, "CY")
    commodity = getCommodity("Adhesive tape, plastic", False)
    container = getContainer("20 Dry Standard", 18000, 1, False, False)
    date = "2021-06-09"
    ########################################

    offersEmpty = 0
    previousOffers = {}
    while 1:
        data = {"from": _from,"to": _to,"commodity": commodity,"containers": [container],"unit": "KG","shipmentPriceCalculationDate": date,"brandCode": "MAEU","customerCode": "41002429094","isSameRequest": False,"weekOffset": 0,"loadAFLS": False}

        secs = uniform(300.254, 420.123)
        sleep(secs)
        print(secs)

        offers = fetchProducts(token, data)
        offers = indexByData(offers)

        if bool(offers):
            try:
                assertDictEqual(previousOffers, offers)
            except Exception as e:
                for i in offers:
                    print(i, offers[i])

                print("Email Sent")

                print(e)
                previousOffers = deepcopy(offers)
        else:
            offersEmpty += 1

    if offersEmpty >= 3:
        print("Failure Email Sent")