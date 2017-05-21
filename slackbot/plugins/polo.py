#coding: UTF-8
import re
from slackbot.bot import respond_to
from slackbot.bot import listen_to
import poloniex
import json
import sys
import requests
#The following section is commented out since slackbot didn't like configparser
#import configparser
# config = configparser.ConfigParser()
# config.sections()
# config.read('settings.ini')
# # key = config['poloniex']['api']
# # secret = config['poloniex']['secret']
# # alertpercent = config['poloniex']['alert']

alertpercent = 1.00 #example: 3.00 - Should be the last % change in the last hour to see an alert
key = "" #poloniex API key
secret = "" #poloniex secret key


polo = poloniex.Poloniex(key,secret)
balance = polo('returnAvailableAccountBalances')
price = polo('returnTicker')
coinurl = "https://api.coinmarketcap.com/v1/ticker/"
coins = [] #list of coins available

#First we need to populate an array of current available balances
for balances in balance['exchange']:
    coin = balances
    amount = balance['exchange'][balances]
    coins.append(coin)

@respond_to('coins',re.IGNORECASE)
def listcoins(message):
    #List coins available in account
    message.reply("You have the following cryptocurrencies:")
    for item in coins:
        message.reply(item)

@respond_to('balance',re.IGNORECASE)
def listbalance(message):
    #List balances available in account
    balance = polo('returnAvailableAccountBalances')
    message.reply("Your balance is:")
    for balances in balance['exchange']:
        coin = balances
        amount = balance['exchange'][balances]
        replies = "%s: %s" % (coin,amount)
        message.reply(replies)

@respond_to('alerts',re.IGNORECASE)
def pricealerts(message):
    #Check for pricing alerts for available coins
    coindata = requests.get(coinurl)
    coindatajson = json.loads(coindata.content)
    for coin in coins:
        for symbols in coindatajson:
            if symbols["symbol"] == coin:
                percentchange = float(symbols['percent_change_1h'])
                currentusdprice = symbols['price_usd']
                if abs(percentchange) > float(alertpercent):
                    alert = "%s changed %s%% in the last hour. Current price: %s" % (coin,percentchange,currentusdprice)
                    message.reply(alert)

@respond_to('price (.*)',re.IGNORECASE)
def listprice(message,coin):
    #List last price of coin
    if coin != 'BTC':
        coinprice = "BTC_"+coin
        lastprice = json.dumps(price[coinprice]['last']).strip('"')
        replies = "1 %s : %s" % (coin,lastprice)
        message.reply(replies)
    else:
        message.reply("1 BTC = 1 BTC")

@respond_to('sell (.*)',re.IGNORECASE)
def sellcoin(message,something):
    regex = '(.*)( )(.*)'
    match = re.search(regex,something,flags = 0)
    currency = match.group(1)
    amount = match.group(3)
    coinprice = "BTC_"+currency
    rate = json.dumps(price[coinprice]['last']).strip('"')
    totalamount = balance['exchange'][balances]
    replies = "Selling %s %s at %s each" % (amount,currency,rate)
    message.reply(replies)
    sellcoins = polo('sell',{'currencyPair': coinprice,'rate':rate,'amount':amount})
    orderNumber = sellcoins['orderNumber']
    replies = "Order number: %s" % (str(orderNumber))
    message.reply(replies)

@respond_to('buy (.*)',re.IGNORECASE)
def buycoin(message,something):
    regex = '(.*)( )(.*)'
    match = re.search(regex,something,flags = 0)
    currency = match.group(1)
    amount = match.group(3)
    coinprice = "BTC_"+currency
    rate = json.dumps(price[coinprice]['last']).strip('"')
    totalamount = balance['exchange'][balances]
    replies = "Buying %s %s at %s each" % (amount,currency,rate)
    message.reply(replies)
    buycoins = polo('buy',{'currencyPair': coinprice,'rate':rate,'amount':amount})
    orderNumber = (buycoins)['orderNumber']
    replies = "Order number: %s" % (orderNumber)
    message.reply(replies)