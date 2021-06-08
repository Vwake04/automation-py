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
    token = "Bearer eyJ0eXAiOiJKV1QiLCJraWQiOiJQbStTdGZEejRmY0tzdk5iUTBscGNETWlyNEk9IiwiYWxnIjoiUlMyNTYifQ.eyJhdF9oYXNoIjoidExmUVI3VW9lTlBLZlVHb20yUVl2ZyIsInN1YiI6ImJob29taV9zaGlwcGluZyIsImZpcnN0bmFtZSI6Ikt1c2giLCJhdWRpdFRyYWNraW5nSWQiOiIyYTBhMjlmMy04OGY5LTRlMmItODY4My00NmUyN2Q4MWQwOGItMTQxNTUzMzUiLCJyb2xlcyI6WyJQYXltZW50cyIsIkludm9pY2VzIiwiQm9va2luZyIsIkNvbnRyYWN0UmF0ZSIsIldCT0xBcHByb3ZlciIsIkRvY3VtZW50YXRpb24iLCJCYXNpY0N1c3RvbWVyIl0sImlzcyI6Imh0dHBzOi8vaWFtLm1hZXJzay5jb20vYWNtL29hdXRoMi9tYXUiLCJ0b2tlbk5hbWUiOiJpZF90b2tlbiIsIm9mZmljZSI6IkthbmRsYSAtIElOIiwiYWNyIjoiMCIsImF6cCI6ImJjYTAwMSIsImF1dGhfdGltZSI6MTYyMzE3ODIwNSwicGVyc29uaWQiOiI0MTAwMjQyOTIwNSIsImV4cCI6MTYyMzE4NTQwNywiY3VzdG9tZXJfY29kZSI6IjQxMDAyNDI5MDk0IiwiaWF0IjoxNjIzMTc4MjA3LCJlbWFpbCI6ImJob29taXNoaXBwaW5nQGdtYWlsLmNvbSIsIm5vbmNlIjoiM1c4RWNkeFlkM25Qamd0R0xsSVAiLCJsYXN0bmFtZSI6IlRoYWNrZXIiLCJhdWQiOiJiY2EwMDEiLCJjX2hhc2giOiIzODZmX010d2NLRjNXVFVRcFktSjd3IiwiY2FycmllciI6Ik1BRVUiLCJyZWFsbSI6Ii9tYXUiLCJ0b2tlblR5cGUiOiJKV1RUb2tlbiIsInVzZXJuYW1lIjoiYmhvb21pX3NoaXBwaW5nIn0.XP3go19JNE-LYIZaD9Tgi6TU1Hb9-9NGoXTzDZJZxNkks-pKXf4ptdptWTiUaFMUGgGQZLqEnpdu_AsWtbMjJgbQzAt4ZIrERN_-DkmRf2BYSpbhjkqCft7tec6Kun25CQtIoaObm2FVsTQ_yKSEEopnojCB23sxnuhITHM4q2lVjKM9qv5qGP1C_mBmN_o4j7tBi8ABah1N1REpQTcOvVh98cp8A3Y3AE2bnM9ADPaoIi7XJmCml1dVByv_fZKYUPkfnYFUIF3zlN-eTx3ji_sHycL515rYq5Kanjm6AVDl-GrXS5GBB9hqmVBk8YPc9WMtjfgcTLb7qrDctcc9zg"
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