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
        self.activity_collection = order['orderActivityCollection'][0]
        self.order = order
        self.avg_price = self.calc_avg_price()

    def calc_avg_price(self):
        execution_legs = self.activity_collection['executionLegs']

        total_quant = 0
        total_price = 0
        for leg in execution_legs:
            leg_quant = leg['quantity']
            leg_price = leg['price']
            total_quant += leg_quant
            total_price += leg_price * leg_quant

        return total_price // total_quant