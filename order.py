
class Order:

    def __init__(self, order):
        self.order_type = order['orderType']
        self.session = order['session']
        self.quant = int(order['quantity'])
        self.filled = int(order['filledQuantity'])

        self.duration = order['duration']
        self.status = order['status']
        self.specifics = order['orderLegCollection'][0]
        self.symbol = self.specifics['instrument']['symbol']
        self.instruction = self.specifics['instruction']
        self.effect = self.specifics['positionEffect']
        self.order = order

    def avg_price(self):
        price = self.order['price']
