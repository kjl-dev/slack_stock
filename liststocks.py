import requests
import json
import formatutils


def execute(command):
    if command.lower() == "gainers":
        return get_leaders('gainers')
    elif command.lower() == "losers":
        return get_leaders('losers')
    elif command.lower() == "active":
        return get_leaders('mostactive')
    else:
        return "Unsupported command '{}'".format(command)


def get_leaders(type):
    response = ""
    api_request = 'https://api.iextrading.com/1.0/stock/market/list/{}'.format(type)
    api_response = requests.get(api_request).content
    json_response = json.loads(api_response)

    for item in json_response:
        response += '\n*{} ({})* : {:.3f} : {:.3f} ({:.2%})' \
            .format(item['companyName'], item['symbol'], item['latestPrice'], item['change'], item['changePercent'])

    return response


def get_prices(records):
    response = ""
    for row in records:
        api_request = 'https://api.iextrading.com/1.0/stock/{}/quote'.format(row['symbol'])
        api_response = requests.get(api_request).content
        json_response = json.loads(api_response)

        price_format = formatutils.get_number_format(json_response['latestPrice'])
        response += '\n*{} ({})* : ' + price_format \
            .format(json_response['companyName'], json_response['symbol'], json_response['latestPrice'])

    return response
