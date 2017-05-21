# SlackPoloBot

## A Slack Bot for interacting with the Poloniex API, allowing you to buy and sell cryptocurrencies as well as receive alerts on price changes. Perfect for the altcoin daytrader!
Quick Demo:

![demo](https://i.imgur.com/goHtOtJ.gif)

### Commands
- coins - list coins available in account
- balance - list coin balances in account
- alerts - check for pricing alerts for available coins
- price <coin> - see latest price for a coin
- buy <coin> <amount> - create a Buy Order!
- sell <count> <amount> - create a Sell Order!

### How to install
` pip install -r requirements.txt`
- Modify slackbot/plugins/polo.py and add your API Key/Secret Key
- Modify slockbot/settings.py and add your Slackbot API key
- `python run.py`