# Class name must be Strategy
class Strategy():
    # option setting needed
    def __setitem__(self, key, value):
        self.options[key] = value

    # option setting needed
    def __getitem__(self, key):
        return self.options.get(key, '')

    def __init__(self):
        # strategy property needed
        self.subscribedBooks = {
            'Binance': {
                'pairs': ['BTC-USDT'],
            },
        }

        # seconds for broker to call trade()
        # do not set the frequency below 60 sec.
        # 10 * 60 for 10 mins
        self.period = 20 * 60
        self.options = {}

        # user defined class attribute
        self.last_type = 'sell'
        
        self.counter = 5
        self.first_trade = 1
        self.idle_counter = 0
        # Record the cost of buying BTC
        self.cost = 0

        # History of price
        # {'price': 'amount', ...}
        self.buy_price = {} 
        self.close_price_trace = np.array([])
        self.open_price_trace = np.array([])
        self.change_trace = []

	
    # called every self.period
    def trade(self, information):
        # for single pair strategy, user can choose which exchange/pair to use when launch, get current exchange/pair from information
        exchange = list(information['candles'])[0]
        pair = list(information['candles'][exchange])[0]
        own_usdt = self['assets'][exchange]['USDT']
        own_btc = self['assets'][exchange]['BTC']

        # Parameters 
        amp_thres = float(self['amp_thres'])
        change_long = int(self['change_long'])
        

        Log('My usdt: ' + str(self['assets'][exchange]['USDT']))
        Log('My btc: ' + str(self['assets'][exchange]['BTC']))
        cur_open = information['candles'][exchange][pair][0]['open']
        cur_close = information['candles'][exchange][pair][0]['close']
        cur_high = information['candles'][exchange][pair][0]['high']
        cur_low = information['candles'][exchange][pair][0]['low']
        change = (float(cur_close) - float(cur_open)) / float(cur_open)
        amptitude = (float(cur_high) - float(cur_low)) / float(cur_high)

        # Append history data
        # self.close_price_trace = np.append(self.close_price_trace, [float(cur_close)])
        #self.open_price_trace = np.append(self.open_price_trace, [float(cur_open)])
        #self.change_trace.append([change, amptitude])
        # Shorten the change_trace
        #self.change_trace = self.change_trace[-change_long:]

        Log("Amtitude: "+str(amptitude)+ ", Change: "+str(change))
        # Special Case: if amptitude is larger than an threshold
        if float(amptitude) >= float(amp_thres):
            Log("Transaction")
            Log('My usdt: ' + str(self['assets'][exchange]['USDT']) + 'My btc: ' + str(self['assets'][exchange]['BTC']))
            if change > 0:
                # Sell the BTC
                Log('Sell BTCs')
                amount = float(amptitude*5)
                # If the amount over the keep BTC
                if amount > own_btc:
                    amount = own_btc
                amount = amount * (-1.0)
                
                if own_btc == 0:
                    return []
                else:
                    return [
                        {
                            'exchange': exchange,
                            'amount': amount, # TBD
                            'price': -1,
                            'type': 'MARKET',
                            'pair': pair,
                        }
                    ]
                
            elif change < 0:
                # Buy the BTC
                Log('Buy BTCs')
                amount = float(amptitude*7)
                prepare = float(cur_close) * amount
                if prepare > own_usdt:
                    prepare = own_usdt
                amount = prepare / float(cur_close)
                return [
                    {
                        'exchange': exchange,
                        'amount': amount, # TBD
                        'price': 1,
                        'type': 'MARKET',
                        'pair': pair,
                    }
                ]

        # Normal Case: Look ahead the history data
        else:
            #average = self.change_average()
            #Log("Change average: " + str(average))
            return []

        #return []
	
    def change_average(self):
        sumary = 0
        num = 0
        for item in self.change_trace:
            sumary = sumary + item[0]
            num = num + 1
        average = sumary / num
        return average


    def on_order_state_change(self, order):
        Log("on order state change message: " + str(order) + " order price: " + str(order["price"]))