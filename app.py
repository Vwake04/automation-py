from flask import Flask, render_template, request, jsonify
from flask.ext.wtf import Form, RadioField
import requests
import json

app = Flask(__name__)

@app.route("/", methods=["GET"])
def enterCityDetails():
    print(request.args)
    return render_template(r'city.html')

@app.route("/completeForm", methods=["POST"])
def completeForm():
    print(request.form)

@app.route("/data", methods=["POST"])
def getCityDetails():
    if request.method == "GET":
        return render_template('error.html')
    elif request.method == "POST":
        form_data =  request.form
        form_data = dict(form_data)
        print(form_data)

        headers = {'authority': 'api.maersk.com','accept': 'application/json, text/plain, */*','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36','origin': 'https://www.maersk.com','sec-fetch-site': 'same-site','sec-fetch-mode': 'cors','sec-fetch-dest': 'empty','referer': 'https://www.maersk.com/','accept-language': 'en-US,en;q=0.9'}
        # try:
        _from = requests.get(f"https://api.maersk.com/locations/?brand=maeu&cityName={form_data['_from']}&type=city&pageSize=50", headers = headers)
        _from = _from.json()
        
        _to = requests.get(f"https://api.maersk.com/locations/?brand=maeu&type=city&pageSize=50&cityName={form_data['_to']}", headers = headers)
        _to = _to.json()

        radioOptions = RadioField()
        # return render_template('completeForm.html', citiesFrom = _from, citiesTo = _to)


if __name__== '__main__':
    app.run(host='localhost', port = 5000)