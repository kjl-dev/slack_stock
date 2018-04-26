import requests
import json
import os
from pymongo import MongoClient

MONGODB_URI = os.environ['MONGODB_URI']
MONGODB_NAME = os.environ['MONGODB_NAME']

client = MongoClient(MONGODB_URI)
db = client[MONGODB_NAME]
temp_collection = db['temp_symbols']
collection = db['symbols']

api_request = 'https://api.iextrading.com/1.0/ref-data/symbols'
api_response = requests.get(api_request).content
json_response = json.loads(api_response)

for item in json_response:
    symbol = item['symbol']

    try:
        quote_request = 'https://api.iextrading.com/1.0/stock/{}/quote'.format(symbol)
        quote_data = requests.get(quote_request).content
        json_quote_response = json.loads(quote_data)
        
        sector = json_quote_response['sector'].lower().replace(" ", "-")
        latestPrice = float(json_quote_response['latestPrice'])

        print("saving {} : {} : {:.3f}".format(symbol, sector, latestPrice))

        temp_symbols = db.temp_symbols
        temp_symbols.insert_one(
            {
                "symbol": symbol,
                "sector": sector,
                "latestPrice": latestPrice
            }
        )

    except:
        print("An error occured when saving symbol {}".format(symbol))


collection.drop()
temp_collection.renameCollection("symbols")
