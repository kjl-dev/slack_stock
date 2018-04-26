import os
import stock
from pymongo import MongoClient

MONGODB_URI = os.environ['MONGODB_URI']
MONGODB_NAME = os.environ['MONGODB_NAME']

client = MongoClient(MONGODB_URI)
db = client[MONGODB_NAME]
collection = db['symbols']


def execute(request_string):
    response = ""

    if request_string.lower() == "show-sectors":
        result = collection.distinct("sector")

        response = "Supported sectors for random stock filtering:"
        for sector in result:
            if sector:
                response += "\n" + sector

        return response

    else:
        query = []

        if request_string:
            commands = request_string.split(" ")
            for command in commands:
                if command.lower().startswith("less:"):
                    price = command.split(":")
                    query.append({'$match': {'latestPrice': {'$lte': float(price[1])}}})
                elif command.lower().startswith("more:"):
                    price = command.split(":")
                    query.append({'$match': {'latestPrice': {'$gte': float(price[1])}}})
                else:
                    query.append({'$match': {'sector': command}})

        query.append({'$sample': {'size': 1}})

        result = list(collection.aggregate(query))

        for record in result:
            response += stock.get_quote(record['symbol'])

    return response
