class Orders:

    def __init__(self, ameritrade_json):
        # try:
        #     self.all_orders = ameritrade_json['securitiesAccount']['orderStrategies']
        #     self.seen_order_ids = [order['orderId'] for order in self.all_orders]
        # except:
        self.all_orders = []
        self.seen_order_ids = []
        # self.seen_order_ids = [] #testing purposes
        self.active_order_ids = []

    def get_new_orders(self, ameritrade_json):
        try:
            orders = ameritrade_json['securitiesAccount']['orderStrategies']
            new_orders = []
            for order in orders:
                order_id = order['orderId']
                if order_id not in self.seen_order_ids:
                    new_orders.append(order)
                    if order['status'] == "QUEUED":
                        self.active_order_ids.append(order_id)
                    self.seen_order_ids.append(order_id)
        except Exception as e:
            print(ameritrade_json)
            new_orders = []
        return new_orders

