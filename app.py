from flask import Flask, render_template, request, jsonify
import requests
import json

from util import commodity, container, getCity, getCommodity, getContainer
from fetchProductOffers import run

app = Flask(__name__)

@app.route("/", methods=["GET"])
def enterCityDetails():
    print(request.args)
    return render_template('city.html')

@app.route("/completeForm", methods=["POST"])
def completeForm():
    # print(request.form)
    token = "Bearer eyJ0eXAiOiJKV1QiLCJraWQiOiJQbStTdGZEejRmY0tzdk5iUTBscGNETWlyNEk9IiwiYWxnIjoiUlMyNTYifQ.eyJhdF9oYXNoIjoidndmUE1RLXg5UEZKX1ZQQ3JHYU9EdyIsInN1YiI6ImJob29taV9zaGlwcGluZyIsImZpcnN0bmFtZSI6Ikt1c2giLCJhdWRpdFRyYWNraW5nSWQiOiIyYTBhMjlmMy04OGY5LTRlMmItODY4My00NmUyN2Q4MWQwOGItMTQzMjE4NTIiLCJyb2xlcyI6WyJQYXltZW50cyIsIkludm9pY2VzIiwiQm9va2luZyIsIkNvbnRyYWN0UmF0ZSIsIldCT0xBcHByb3ZlciIsIkRvY3VtZW50YXRpb24iLCJCYXNpY0N1c3RvbWVyIl0sImlzcyI6Imh0dHBzOi8vaWFtLm1hZXJzay5jb20vYWNtL29hdXRoMi9tYXUiLCJ0b2tlbk5hbWUiOiJpZF90b2tlbiIsIm9mZmljZSI6IkthbmRsYSAtIElOIiwiYWNyIjoiMCIsImF6cCI6ImJjYTAwMSIsImF1dGhfdGltZSI6MTYyMzE4NjE5NywicGVyc29uaWQiOiI0MTAwMjQyOTIwNSIsImV4cCI6MTYyMzE5MzM5OSwiY3VzdG9tZXJfY29kZSI6IjQxMDAyNDI5MDk0IiwiaWF0IjoxNjIzMTg2MTk5LCJlbWFpbCI6ImJob29taXNoaXBwaW5nQGdtYWlsLmNvbSIsIm5vbmNlIjoid1oybkVFa2NoZnIyMXJIQTdEbmgiLCJsYXN0bmFtZSI6IlRoYWNrZXIiLCJhdWQiOiJiY2EwMDEiLCJjX2hhc2giOiJYdmt2d09iQXVfaGszSFJJNW1qT2JnIiwiY2FycmllciI6Ik1BRVUiLCJyZWFsbSI6Ii9tYXUiLCJ0b2tlblR5cGUiOiJKV1RUb2tlbiIsInVzZXJuYW1lIjoiYmhvb21pX3NoaXBwaW5nIn0.d9srnTHxWu8XXOlFEIABJ-q9_wAzUfGOk75kcxMuFtDECjo9nOjMlKPn_9dYKhBkCfgIzOAtcvEn5sYx-uOixv-eua_c4gtPwgMaW4mJRS6J0YV7Xc7cpgmCUiekR-zlizKRTHFa0RxhyeAhNPrqzGZFJnGYdORwpEWi3Vy4qhz0U2QePgg5OqfmCEgr5WUCGKPqTXJ3G5vMxLPEXYKErZGyxaULI2oHDws6W4zvGkt57hdR2tLWqIGxoCzaXcW1KzjNs-_tE0baDYwO1dSglz1lbpdcRhxosI990xr5BpujKcwMP_fVIWhunjnSwnAE0cTAXyvTxcHvJKcvgyfOBA"
    data = dict(request.form)
    FROM = data["FROM"].split(";")
    FROM = getCity(FROM, data["FROM_MODE"])

    TO = data["TO"].split(";")
    TO = getCity(TO, data["TO_MODE"])

    _commodity = getCommodity(data["COMMODITY"], data["isDangerous"])
    _container = getContainer(data["CONTAINER"], data["weight"], data["quantity"], data["isShipperOwnedContainer"], data["isNonOperatingReefer"])

    print(run(token, FROM, TO, _commodity, _container, data["date"]))

    return {}

@app.route("/data", methods=["POST"])
def getCityDetails():
    if request.method == "GET":
        return render_template('error.html')

    elif request.method == "POST":
        form_data =  request.form
        form_data = dict(form_data)

        headers = {'authority': 'api.maersk.com','accept': 'application/json, text/plain, */*','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36','origin': 'https://www.maersk.com','sec-fetch-site': 'same-site','sec-fetch-mode': 'cors','sec-fetch-dest': 'empty','referer': 'https://www.maersk.com/','accept-language': 'en-US,en;q=0.9'}
        try:
            _from = requests.get(f"https://api.maersk.com/locations/?brand=maeu&cityName={form_data['_from']}&type=city&pageSize=50", headers = headers)
            _from = _from.json()
            
            _to = requests.get(f"https://api.maersk.com/locations/?brand=maeu&type=city&pageSize=50&cityName={form_data['_to']}", headers = headers)
            _to = _to.json()
        except:
            print("Cannot get city details")

        return render_template('completeForm.html', _from  = _from, _to = _to, commodity = commodity, container = container)


if __name__== '__main__':
    app.run(host='localhost', port = 5000)