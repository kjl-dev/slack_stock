from flask import Flask
from flask import request
from flask import jsonify
import stock
import randomstock
import liststocks

app = Flask(__name__)


@app.route('/', methods=['POST'])
def get_stock():
    request_string = request.form.get('text')

    if not request_string:
        return "No symbol provided"

    functions = request_string.split(" ")
    symbol = functions[0].lower()

    # remove duplicates after converting to lowercase
    commands = functions[1:]
    commands = map(str.lower, commands)
    commands = list(set(commands))

    response = stock.execute(symbol, commands)
    return slack_response(response)


@app.route('/stockhelp', methods=['POST'])
def get_help():
    response = "`/stock [symbol]` - Gets current stock quote information for the provided symbol"
    response += "\n     *Optional commands:*"
    response += "\n     history - Gets historical information for the symbol"
    response += "\n     news - Gets recent news articles related to the symbol."
    response += "\n     links - Gets links to various financial sites for the symbol"
    response += "\n     eg `/stock msft history news`"
    response += "\n "
    response += "\n`/stock_list gainers` - Gets the top 10 best performing stocks."
    response += "\n`/stock_list losers` - Gets the top 10 worst performing stocks."
    response += "\n`/stock_list active` - Gets the top 10 most active stocks."
    response += "\n "
    response += "`/stock_random` - Gets a random stock quote."
    response += "\n     *Optional commands:*"
    response += "\n     [sector] - Gets a random stock from within the sector.  " \
                "Execute `/stock_random show-sectors` to view all eligible sectors"
    response += "\n     less:# - Gets a random stock <= the provided price."
    response += "\n     more:# - Gets a random stock >= the provided price."
    response += "\n     eg `/stock_random technology less:10.00 more:5.00`"

    return response


@app.route('/list', methods=['POST'])
def get_list():
    request_string = request.form.get('text')

    if not request_string:
        return "No list provided.  Currently supported list types are 'gainers', 'losers', and 'mostactive'"

    response = liststocks.execute(request_string)

    return slackResponse(response)


@app.route('/randomstock', methods=['POST'])
def get_random_stock():
    request_string = request.form.get('text')
    response = randomstock.execute(request_string)

    return slack_response(response)


def slack_response(response_string, response_type="in_channel"):
    return jsonify(
        response_type=response_type,
        text=response_string
    )
