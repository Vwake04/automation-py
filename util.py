import json
import requests
import smtplib, ssl

commodity = []
with open("commodity.json") as f:
    commodity = json.load(f)

container = []
with open("container.json") as f:
    container = json.load(f)

def getCity(data, serviceMode):
    return {
        "maerskGeoId": data[0],
        "countryCode": data[1],
        "maerskServiceMode": serviceMode,
        "maerskRkstCode": data[2]
    }

def getCommodity(commodityName, isDangerous = False):
    for d in commodity:
        if d["commodityName"] == commodityName:
            return {
                "id": d["commodityCode"],
                "name": d["commodityName"],
                "isDangerous": bool(int(isDangerous)),
                "dangerousDetails": []
            }
    return {}            

def getContainer(containerName, weight, quantity = 1, isShipperOwnedContainer = False, isNonOperatingReefer = False):
    for d in container:
        if d["sizeTypeDisplayName"] == containerName:
            return {
                "isoCode": d["isoContainerSizeTypeCd"],
                "name": d["sizeTypeDisplayName"],
                "size": d["sizeCd"],
                "type": d["typeCd"],
                "weight": int(weight),
                "quantity": int(quantity),
                "isReefer": d["reeferFlag"],
                "isNonOperatingReefer": bool(int(isNonOperatingReefer)),
                "isShipperOwnedContainer": bool(int(isShipperOwnedContainer))
            }
    return {}            

def sendMail(body):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "facemefaith@gmail.com"
    receiver_email = "facemefaith@gmail.com"
    password = "grey@tal"
    message = f"""\
    Subject: Hi there

    {body}"""

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

# print(getCommodity("Albacore, frozen, fish", False))
# print(getContainer("40 Dry Standard", 18000, 1, False, False))