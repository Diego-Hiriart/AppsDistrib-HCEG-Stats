from flask import Flask, request, json, jsonify, Response
from flask_cors import CORS
from hcegStatsClasses import *
import requests
import json
from datetime import datetime

app = Flask(__name__)#Get currentt module name (what is running now)
CORS(app, resources={r"/api/stats": {"origins": ["http://localhost:3001", "https://hceg-gui.azurewebsites.net", "127.0.0.1"]}})

@app.route('/api/stats', methods=['GET'])
def getStats():
    try:
        invoicesReq = requests.get("https://hceg-dbapi.azurewebsites.net/api/invoices")
        jsonInvoices = json.loads(invoicesReq.content)
        products = {}
        yearlyNumSales = {}
        yearlyRevenue = {}
        yearlyRevAvrg = {}
        for invoice in jsonInvoices:
            orderItemsReq = requests.get("https://hceg-dbapi.azurewebsites.net/api/order-items/search?id={0}".format(invoice["orderId"]))
            jsonItems = json.loads(orderItemsReq.content)
            for orderItem in jsonItems:
                if str(orderItem["productId"]) in products:
                    products[str(orderItem["productId"])] += 1
                else:
                    products[str(orderItem["productId"])] = 1
            orderDateReq = requests.get("https://hceg-dbapi.azurewebsites.net/api/orders/search?id={0}".format(invoice["orderId"]))
            jsonOrderDate = json.loads(orderDateReq.content)["date"]
            if str(datetime.fromisoformat(jsonOrderDate).year) in yearlyNumSales:
                yearlyNumSales[str(datetime.fromisoformat(jsonOrderDate).year)] += 1
            else:
                yearlyNumSales[str(datetime.fromisoformat(jsonOrderDate).year)] = 1
            if str(datetime.fromisoformat(jsonOrderDate).year) in yearlyRevenue:
                yearlyRevenue[str(datetime.fromisoformat(jsonOrderDate).year)] += invoice["total"]
            else:
                yearlyRevenue[str(datetime.fromisoformat(jsonOrderDate).year)] = invoice["total"]
        topProdId = max(products, key=products.get)
        productReq = requests.get("https://hceg-dbapi.azurewebsites.net/api/products/search?id={0}".format(topProdId))
        jsonProduct = json.loads(productReq.content)
        topProduct = Product(jsonProduct["productId"], jsonProduct["name"], jsonProduct["price"])
        for i in yearlyRevenue:
            yearlyRevAvrg[i] = yearlyRevenue[i] / yearlyNumSales[i]
        statsResponse = StatsResponse(topProduct, yearlyNumSales, yearlyRevenue, yearlyRevAvrg)
        return Response(status=200, content_type='application/json', response=jsonify(statsResponse.serialize()).data)
    except Exception as excp:
        return Response(str(excp), status=500)

if __name__ == '__main__':
    app.run()