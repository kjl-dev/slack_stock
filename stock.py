import requests
import json
from formatutils import get_number_format


def execute(symbol, commands=None):
    response = get_quote(symbol)

    if not response:
        return "Unknown symbol"

    if commands is not None:
        for command in commands:
            if command.lower() == "history":
                response += get_history(symbol)
            elif command.lower() == "news":
                response += get_news(symbol)
            elif command.lower() == "links":
                response += get_links(symbol)

    return response


def get_quote(symbol):
    api_request = 'https://api.iextrading.com/1.0/stock/{}/quote'.format(symbol)
    api_response = requests.get(api_request).content

    if "Unknown symbol".encode('utf-8') == api_response:
        return

    json_response = json.loads(api_response)

    company_name = json_response['companyName']
    latest_price = json_response['latestPrice']
    open_price = json_response['open']
    close_price = json_response['close']
    high = json_response['high']
    low = json_response['low']
    week_52_high = json_response['week52High']
    week_52_low = json_response['week52Low']

    response = ""

    if company_name:
        response += '*{} : {}*'.format(company_name, symbol)
    else:
        response += '*{}*'.format(symbol)

    response += '\n*Latest Price:* ' + get_number_format(latest_price).format(latest_price)
    response += '    *Change:* {:.2%}'.format(json_response['changePercent'])
    response += '    *Volume:* {:,}'.format(json_response['latestVolume'])
    response += '\n*Open:* ' + get_number_format(open_price).format(open_price)
    response += '    *Close:* ' + get_number_format(close_price).format(close_price)
    response += '\n*High:* ' + get_number_format(high).format(high)
    response += '    *Low:*  ' + get_number_format(low).format(low)
    response += '\n*52w High:* ' + get_number_format(week_52_high).format(week_52_high)
    response += '    *52w Low:* ' + get_number_format(week_52_low).format(week_52_low)

    return response


def get_history(symbol):
    api_request = 'https://api.iextrading.com/1.0/stock/{}/stats'.format(symbol)
    api_response = requests.get(api_request).content
    json_response = json.loads(api_response)

    response = '\n*---HISTORY---*'
    response += '\n<https://finviz.com/chart.ashx?t={}&ty=c&ta=1&p=d&s=l>'.format(symbol)
    response += '\n*5d:* {:.2%}'.format(json_response['day5ChangePercent'])
    response += '\n*1m:* {:.2%}'.format(json_response['month1ChangePercent'])
    response += '     *3m:* {:.2%}'.format(json_response['month3ChangePercent'])
    response += '     *6m:* {:.2%}'.format(json_response['month6ChangePercent'])
    response += '\n*1y:* {:.2%}'.format(json_response['year1ChangePercent'])
    response += '     *2y:* {:.2%}'.format(json_response['year2ChangePercent'])
    response += '     *5y:* {:.2%}'.format(json_response['year5ChangePercent'])

    return response


def get_news(symbol):
    api_request = 'https://api.iextrading.com/1.0/stock/{}/news/last/5'.format(symbol)
    api_response = requests.get(api_request).content
    json_response = json.loads(api_response)

    response = '\n*---NEWS---*'
    for article in json_response:
        response += '\n<{}|{}> : {:.10} '.format(article['url'], article['headline'], article['datetime'])

    return response


def get_links(symbol):
    response = '\n*---LINKS---*'
    response += '\n<https://stocktwits.com/symbol/{}|StockTwits>'.format(symbol)
    response += ' | <https://finviz.com/quote.ashx?t={}|FinViz>'.format(symbol)
    response += ' | <https://www.google.com/search?tbm=fin&q={}|Google Finance>'.format(symbol)
    response += ' | <https://finance.yahoo.com/quote/{}|Yahoo Finance>'.format(symbol)
    response += ' | <https://www.marketwatch.com/investing/stock/{}|MarketWatch>'.format(symbol)
    return response
