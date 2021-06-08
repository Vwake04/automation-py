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
    token = "Bearer eyJ0eXAiOiJKV1QiLCJraWQiOiJQbStTdGZEejRmYBA"
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
